"""Read-only M0 authorization preflight for the assets batch slice."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping

from lib.checkpoint import CheckpointValidationError, read_checkpoint, validate_checkpoint
from lib.identity import InvalidProjectIdError, resolve_project_dir
from lib.pipeline_loader import load_pipeline_readonly
from schemas.artifacts import validate_artifact

from .contracts import (
    M0ContractError,
    canonical_json_bytes,
    canonical_sha256,
    validate_adapter_observation,
    validate_batch_request,
    validate_logical_path,
)


@dataclass(frozen=True)
class PreflightFacts:
    """Authenticated facts returned without performing any side effect."""

    project_dir: Path
    manifest_sha256: str
    prerequisite_stages: tuple[str, ...]
    source_binding_ids: tuple[str, ...]
    work_item_ids: tuple[str, ...]
    request_digest: str


ManifestLoader = Callable[[str], Mapping[str, Any]]
CheckpointReader = Callable[[Path, str, str], Mapping[str, Any] | None]

_PROPOSAL_AUTHORIZATION_CATEGORIES = frozenset(
    {"provider_selection", "budget_tradeoff"}
)


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left)) == os.path.normcase(str(right))


def _exact_project_path(project_dir: Path, logical_path: str) -> Path:
    normalized = validate_logical_path(logical_path, field="source logical_path")
    expected = project_dir.joinpath(*PurePosixPath(normalized).parts)
    resolved = expected.resolve(strict=False)
    try:
        resolved.relative_to(project_dir)
    except ValueError as exc:
        raise M0ContractError("SOURCE_PATH_ESCAPE", f"Source escapes project: {logical_path}") from exc
    if not _same_path(expected, resolved):
        raise M0ContractError(
            "SOURCE_PATH_ALIAS",
            f"Source changes identity through a symlink or junction: {expected} -> {resolved}",
        )
    return resolved


def _authenticate_project_marker(
    projects_root: Path, project_id: str, pipeline_type: str
) -> Path:
    try:
        project_dir = resolve_project_dir(projects_root, project_id)
    except InvalidProjectIdError as exc:
        raise M0ContractError("PROJECT_IDENTITY_INVALID", str(exc)) from exc
    if not project_dir.is_dir():
        raise M0ContractError("PROJECT_IDENTITY_INVALID", f"Missing project directory {project_dir}")
    marker_path = _exact_project_path(project_dir, "project.json")
    if not marker_path.is_file():
        raise M0ContractError(
            "PROJECT_MARKER_REQUIRED", f"Batch V2 requires regular file {marker_path}"
        )
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise M0ContractError("PROJECT_MARKER_INVALID", f"Cannot read {marker_path}: {exc}") from exc
    if not isinstance(marker, dict):
        raise M0ContractError("PROJECT_MARKER_INVALID", "project.json must be an object")
    if marker.get("project_id") != project_id or marker.get("pipeline_type") != pipeline_type:
        raise M0ContractError(
            "PROJECT_MARKER_MISMATCH",
            "project.json does not bind the requested project_id and pipeline_type",
        )
    return project_dir


def _required_predecessors(manifest: Mapping[str, Any], target_stage: str) -> tuple[list[dict], dict]:
    stages = list(manifest.get("stages") or [])
    names = [stage.get("name") for stage in stages]
    if target_stage not in names:
        raise M0ContractError(
            "TARGET_STAGE_NOT_DECLARED", f"Pipeline does not declare {target_stage!r}"
        )
    target_index = names.index(target_stage)
    predecessors = [
        stage
        for stage in stages[:target_index]
        if isinstance(stage, dict) and stage.get("checkpoint_required", True) is not False
    ]
    if not predecessors:
        raise M0ContractError(
            "PREREQUISITE_CHAIN_EMPTY", "MVP assets batch requires an approved predecessor chain"
        )
    return predecessors, stages[target_index]


def _load_authenticated_checkpoints(
    *,
    projects_root: Path,
    project_id: str,
    pipeline_type: str,
    predecessor_defs: list[dict],
    evidence_records: list[Mapping[str, Any]],
    checkpoint_reader: CheckpointReader,
) -> dict[str, Mapping[str, Any]]:
    expected_stages = [stage["name"] for stage in predecessor_defs]
    actual_stages = [evidence["stage"] for evidence in evidence_records]
    if actual_stages != expected_stages:
        raise M0ContractError(
            "PREREQUISITE_CHAIN_MISMATCH",
            f"Expected ordered chain {expected_stages}, got {actual_stages}",
        )
    authenticated: dict[str, Mapping[str, Any]] = {}
    for stage_def, evidence in zip(predecessor_defs, evidence_records):
        stage = stage_def["name"]
        try:
            checkpoint = checkpoint_reader(projects_root, project_id, stage)
        except (CheckpointValidationError, OSError, ValueError) as exc:
            raise M0ContractError(
                "CHECKPOINT_VALIDATION_FAILED", f"Cannot validate prerequisite {stage}: {exc}"
            ) from exc
        if checkpoint is None:
            raise M0ContractError("CHECKPOINT_REQUIRED", f"Missing checkpoint for {stage}")
        try:
            validate_checkpoint(dict(checkpoint), pipeline_dir=projects_root)
        except (CheckpointValidationError, OSError, ValueError) as exc:
            raise M0ContractError(
                "CHECKPOINT_VALIDATION_FAILED",
                f"Cannot independently validate prerequisite {stage}: {exc}",
            ) from exc
        if checkpoint.get("pipeline_type") != pipeline_type:
            raise M0ContractError(
                "CHECKPOINT_IDENTITY_MISMATCH", f"Checkpoint {stage} has wrong pipeline"
            )
        if checkpoint.get("status") != "completed":
            raise M0ContractError(
                "CHECKPOINT_NOT_COMPLETED", f"Checkpoint {stage} is not completed"
            )
        requires_approval = bool(stage_def.get("human_approval_default", False))
        if requires_approval and checkpoint.get("human_approved") is not True:
            raise M0ContractError(
                "HUMAN_GATE_NOT_APPROVED", f"Checkpoint {stage} lacks required approval"
            )
        if (
            evidence["status"] != checkpoint.get("status")
            or evidence["human_approved"] is not checkpoint.get("human_approved")
        ):
            raise M0ContractError(
                "CHECKPOINT_EVIDENCE_MISMATCH", f"Stale status/approval evidence for {stage}"
            )
        digest = canonical_sha256(checkpoint)
        if evidence["sha256"] != digest:
            raise M0ContractError(
                "CHECKPOINT_EVIDENCE_MISMATCH", f"Stale checkpoint digest for {stage}"
            )
        authenticated[stage] = checkpoint
    return authenticated


def _authenticate_source_binding(
    binding: Mapping[str, Any],
    *,
    project_dir: Path,
    checkpoints: Mapping[str, Mapping[str, Any]],
) -> None:
    source_type = binding["source_type"]
    logical_path = binding["logical_path"]
    if source_type in {"checkpoint", "checkpoint_artifact"}:
        stage = binding["checkpoint_stage"]
        expected_path = f"checkpoint_{stage}.json"
        if logical_path != expected_path:
            raise M0ContractError(
                "SOURCE_PATH_MISMATCH", f"Checkpoint source must bind {expected_path}"
            )
        checkpoint = checkpoints.get(stage)
        if checkpoint is None:
            raise M0ContractError(
                "SOURCE_NOT_AUTHORIZED", f"Source checkpoint {stage} is outside the approved chain"
            )
        if (
            binding["checkpoint_status"] != checkpoint.get("status")
            or binding["human_approved"] is not checkpoint.get("human_approved")
        ):
            raise M0ContractError(
                "SOURCE_BINDING_MISMATCH", f"Stale checkpoint source binding {binding['binding_id']}"
            )
        bound_value: Any = checkpoint
        if source_type == "checkpoint_artifact":
            artifact_name = binding["artifact_name"]
            artifacts = checkpoint.get("artifacts") or {}
            if artifact_name not in artifacts or not isinstance(artifacts[artifact_name], dict):
                raise M0ContractError(
                    "SOURCE_ARTIFACT_MISSING", f"Checkpoint {stage} lacks {artifact_name}"
                )
            bound_value = artifacts[artifact_name]
            try:
                validate_artifact(artifact_name, bound_value, project_dir=project_dir)
            except Exception as exc:
                raise M0ContractError(
                    "SOURCE_ARTIFACT_INVALID", f"Artifact {artifact_name} failed validation: {exc}"
                ) from exc
        payload = canonical_json_bytes(bound_value)
    else:
        path = _exact_project_path(project_dir, logical_path)
        if not path.is_file():
            raise M0ContractError("SOURCE_FILE_MISSING", f"Missing regular source file {path}")
        try:
            payload = path.read_bytes()
        except OSError as exc:
            raise M0ContractError("SOURCE_FILE_UNREADABLE", f"Cannot read {path}: {exc}") from exc
    if len(payload) != binding["size_bytes"]:
        raise M0ContractError(
            "SOURCE_BINDING_MISMATCH", f"Size changed for {binding['binding_id']}"
        )
    if hashlib.sha256(payload).hexdigest() != binding["sha256"]:
        raise M0ContractError(
            "SOURCE_BINDING_MISMATCH", f"Digest changed for {binding['binding_id']}"
        )


def _validate_clp_binding(
    required_artifacts: set[str], source_bindings: list[Mapping[str, Any]]
) -> None:
    """Bind a scene plan to the exact CLP shot-binding artifact when applicable."""

    if "clp_shot_bindings" not in required_artifacts:
        return
    clp_sources = [
        binding
        for binding in source_bindings
        if binding.get("source_type") == "checkpoint_artifact"
        and binding.get("artifact_name") == "clp_shot_bindings"
    ]
    if len(clp_sources) != 1:
        raise M0ContractError(
            "CLP_BINDING_REQUIRED", "Exactly one clp_shot_bindings source must be frozen"
        )
    clp_digest = clp_sources[0]["sha256"]
    scene_plan_sources = [
        binding
        for binding in source_bindings
        if binding.get("source_type") == "checkpoint_artifact"
        and binding.get("artifact_name") == "scene_plan"
    ]
    if len(scene_plan_sources) != 1 or scene_plan_sources[0].get("clp_binding_digest") != clp_digest:
        raise M0ContractError(
            "CLP_BINDING_MISMATCH",
            "scene_plan source must bind the exact clp_shot_bindings SHA-256",
        )


def _validate_proposal_approval(
    checkpoints: Mapping[str, Mapping[str, Any]], authorization: Mapping[str, Any]
) -> None:
    """Bind a pipeline proposal/cost gate when one exists in the chain."""

    proposal_records = [
        (stage, checkpoint, checkpoint["artifacts"]["proposal_packet"])
        for stage, checkpoint in checkpoints.items()
        if isinstance(checkpoint.get("artifacts"), dict)
        and isinstance(checkpoint["artifacts"].get("proposal_packet"), dict)
    ]
    if len(proposal_records) > 1:
        raise M0ContractError(
            "PROPOSAL_APPROVAL_AMBIGUOUS", "More than one proposal_packet is present"
        )

    basis = authorization.get("authorization_basis")
    if not proposal_records:
        if basis != "explicit_per_batch":
            raise M0ContractError(
                "PROPOSAL_AUTHORIZATION_REQUIRED",
                "validated_proposal_checkpoint authority requires a proposal in the authenticated chain",
            )
        if not str(authorization.get("approval_reference", "")).startswith(
            "explicit-per-batch:"
        ):
            raise M0ContractError(
                "EXPLICIT_BATCH_AUTHORIZATION_INVALID",
                "Legacy no-proposal authority requires an explicit-per-batch reference",
            )
        if authorization.get("approval_status") != "approved" or authorization.get(
            "decision_refs"
        ):
            raise M0ContractError(
                "APPROVAL_CHANGE_UNBOUND",
                "Legacy explicit-per-batch authority cannot claim proposal changes or decision refs",
            )
        return

    if basis != "validated_proposal_checkpoint":
        raise M0ContractError(
            "PROPOSAL_AUTHORIZATION_REQUIRED",
            "A proposal-bearing chain must use validated_proposal_checkpoint authority",
        )

    proposal_stage, proposal_checkpoint, proposal_packet = proposal_records[0]
    if authorization.get("approval_reference") != (
        f"checkpoint:{proposal_stage}:proposal_packet"
    ):
        raise M0ContractError(
            "PROPOSAL_REFERENCE_MISMATCH",
            "Approval reference does not identify the authenticated proposal checkpoint",
        )

    proposal_approval = proposal_packet.get("approval") or {}
    proposal_status = proposal_approval.get("status")
    if proposal_status not in {"approved", "approved_with_changes"}:
        raise M0ContractError(
            "PROPOSAL_NOT_APPROVED", f"Proposal status is {proposal_status!r}"
        )
    if authorization["approval_status"] != proposal_status:
        raise M0ContractError(
            "PROPOSAL_APPROVAL_MISMATCH", "Frozen approval status differs from proposal"
        )

    authenticated_budget: Decimal | None = None
    if not authorization.get("no_cost"):
        proposal_budget = proposal_approval.get("approved_budget_usd")
        if isinstance(proposal_budget, bool) or not isinstance(proposal_budget, (int, float)):
            raise M0ContractError(
                "PROPOSAL_BUDGET_REQUIRED",
                "A paid batch requires approved_budget_usd in the authenticated proposal",
            )
        authenticated_budget = Decimal(str(proposal_budget))
        if (
            Decimal(str(authorization["approved_budget_usd"])) > authenticated_budget
            or Decimal(str(authorization["max_authorized_spend_usd"]))
            > authenticated_budget
        ):
            raise M0ContractError(
                "PROPOSAL_BUDGET_EXCEEDED",
                "Frozen request budget or spend cap exceeds the authenticated proposal budget",
            )

    decision_refs = list(authorization.get("decision_refs") or [])
    if authorization["approval_status"] == "approved_with_changes" and not decision_refs:
        raise M0ContractError(
            "APPROVAL_CHANGE_UNBOUND", "approved_with_changes requires immutable decision refs"
        )

    decision_log = (proposal_checkpoint.get("artifacts") or {}).get("decision_log")
    if not isinstance(decision_log, Mapping) or not isinstance(
        decision_log.get("decisions"), list
    ):
        raise M0ContractError(
            "DECISION_LOG_REQUIRED",
            "Proposal authorization refs must resolve in the proposal checkpoint decision_log",
        )
    decisions_by_id: dict[str, Mapping[str, Any]] = {}
    for decision in decision_log["decisions"]:
        if not isinstance(decision, Mapping) or not isinstance(decision.get("decision_id"), str):
            raise M0ContractError("DECISION_LOG_INVALID", "Decision entry lacks an ID")
        decision_id = decision["decision_id"]
        if decision_id in decisions_by_id:
            raise M0ContractError(
                "DECISION_LOG_INVALID", f"Duplicate decision ID {decision_id!r}"
            )
        decisions_by_id[decision_id] = decision

    referenced_ids: set[str] = set()
    referenced_categories: set[str] = set()
    for reference in decision_refs:
        decision_id = reference["decision_id"]
        if decision_id in referenced_ids:
            raise M0ContractError(
                "DECISION_REFERENCE_DUPLICATE", f"Decision {decision_id!r} is referenced twice"
            )
        referenced_ids.add(decision_id)
        decision = decisions_by_id.get(decision_id)
        if decision is None:
            raise M0ContractError(
                "DECISION_REFERENCE_UNKNOWN",
                f"Decision {decision_id!r} is absent from the proposal checkpoint",
            )
        if reference["sha256"] != canonical_sha256(decision):
            raise M0ContractError(
                "DECISION_DIGEST_MISMATCH", f"Decision {decision_id!r} digest changed"
            )
        category = decision.get("category")
        if category not in _PROPOSAL_AUTHORIZATION_CATEGORIES:
            raise M0ContractError(
                "DECISION_CATEGORY_MISMATCH",
                f"Decision {decision_id!r} is not a provider or budget authorization",
            )
        if decision.get("stage") != proposal_stage:
            raise M0ContractError(
                "DECISION_STAGE_MISMATCH",
                f"Decision {decision_id!r} was not made at the proposal gate",
            )
        if decision.get("user_approved") is not True:
            raise M0ContractError(
                "DECISION_NOT_USER_APPROVED",
                f"Decision {decision_id!r} lacks explicit user approval",
            )
        if category == "provider_selection":
            expected_selection = (
                f"identity-sha256:{canonical_sha256(authorization['allowed_identity'])}"
            )
            selected = decision.get("selected")
            selected_options = [
                option
                for option in decision.get("options_considered", [])
                if isinstance(option, Mapping) and option.get("option_id") == selected
            ]
            if selected != expected_selection or len(selected_options) != 1:
                raise M0ContractError(
                    "DECISION_SELECTION_MISMATCH",
                    "Provider decision does not select the exact frozen adapter identity",
                )
        elif category == "budget_tradeoff":
            if authenticated_budget is None:
                raise M0ContractError(
                    "DECISION_CATEGORY_MISMATCH",
                    "A no-cost batch cannot use a paid budget authorization decision",
                )
            budget_text = format(authenticated_budget.normalize(), "f")
            expected_selection = f"approved-budget-usd:{budget_text}"
            selected = decision.get("selected")
            selected_options = [
                option
                for option in decision.get("options_considered", [])
                if isinstance(option, Mapping) and option.get("option_id") == selected
            ]
            if selected != expected_selection or len(selected_options) != 1:
                raise M0ContractError(
                    "DECISION_SELECTION_MISMATCH",
                    "Budget decision does not select the authenticated proposal budget",
                )
        referenced_categories.add(category)

    required_categories = {"provider_selection"}
    if not authorization.get("no_cost"):
        required_categories.add("budget_tradeoff")
    missing_categories = sorted(required_categories - referenced_categories)
    if missing_categories:
        raise M0ContractError(
            "REQUIRED_DECISION_UNBOUND",
            f"Missing approved proposal decisions for {missing_categories}",
        )


def preflight_batch_request(
    request: Mapping[str, Any],
    *,
    projects_root: str | Path,
    observed_source_revision: Mapping[str, str],
    adapter_observation: Mapping[str, Any],
    manifest_loader: ManifestLoader = load_pipeline_readonly,
    checkpoint_reader: CheckpointReader = read_checkpoint,
) -> PreflightFacts:
    """Authenticate all M0 dispatch prerequisites without invoking a tool."""

    validate_batch_request(request)
    if dict(request["source_revision"]) != dict(observed_source_revision):
        raise M0ContractError("SOURCE_REVISION_MISMATCH", "Materialized source revision is stale")
    validate_adapter_observation(adapter_observation)
    return validate_frozen_request_authority(
        request,
        projects_root=projects_root,
        manifest_loader=manifest_loader,
        checkpoint_reader=checkpoint_reader,
    )


def validate_frozen_request_authority(
    request: Mapping[str, Any],
    *,
    projects_root: str | Path,
    manifest_loader: ManifestLoader = load_pipeline_readonly,
    checkpoint_reader: CheckpointReader = read_checkpoint,
) -> PreflightFacts:
    """Revalidate immutable project/source/gate authority without tool facts.

    M2 uses this read-only subset after execution so a changed predecessor,
    project marker, pipeline manifest, authorization, or source binding cannot
    be published merely because it was valid before M1 dispatch.
    """

    validate_batch_request(request)
    root = Path(projects_root).resolve()
    project_dir = _authenticate_project_marker(
        root, request["project_id"], request["pipeline_type"]
    )
    try:
        manifest = manifest_loader(request["pipeline_type"])
    except Exception as exc:
        raise M0ContractError("PIPELINE_MANIFEST_INVALID", str(exc)) from exc
    if manifest.get("name") != request["pipeline_type"]:
        raise M0ContractError("PIPELINE_MANIFEST_MISMATCH", "Manifest identity changed")
    manifest_digest = canonical_sha256(manifest)
    if request["authorization"]["manifest_sha256"] != manifest_digest:
        raise M0ContractError("PIPELINE_MANIFEST_MISMATCH", "Manifest digest changed")

    predecessor_defs, target_def = _required_predecessors(manifest, request["stage"])
    if request["authorization"]["immediate_predecessor_stage"] != predecessor_defs[-1]["name"]:
        raise M0ContractError(
            "IMMEDIATE_PREDECESSOR_MISMATCH", "Immediate predecessor authorization is stale"
        )
    checkpoints = _load_authenticated_checkpoints(
        projects_root=root,
        project_id=request["project_id"],
        pipeline_type=request["pipeline_type"],
        predecessor_defs=predecessor_defs,
        evidence_records=request["authorization"]["prerequisite_checkpoints"],
        checkpoint_reader=checkpoint_reader,
    )
    _validate_proposal_approval(checkpoints, request["authorization"])

    produced_artifacts = {
        artifact_name
        for checkpoint in checkpoints.values()
        for artifact_name in (checkpoint.get("artifacts") or {})
    }
    required_artifacts = set(target_def.get("required_artifacts_in") or [])
    missing_artifacts = sorted(required_artifacts - produced_artifacts)
    if missing_artifacts:
        raise M0ContractError(
            "REQUIRED_SOURCE_ARTIFACT_MISSING", f"Assets stage requires {missing_artifacts}"
        )

    bound_artifacts: set[str] = set()
    for binding in request["source_bindings"]:
        _authenticate_source_binding(binding, project_dir=project_dir, checkpoints=checkpoints)
        if binding["source_type"] == "checkpoint_artifact":
            bound_artifacts.add(binding["artifact_name"])
    unbound_required = sorted(required_artifacts - bound_artifacts)
    if unbound_required:
        raise M0ContractError(
            "REQUIRED_SOURCE_ARTIFACT_UNBOUND", f"Frozen request does not bind {unbound_required}"
        )
    _validate_clp_binding(required_artifacts, list(request["source_bindings"]))
    return PreflightFacts(
        project_dir=project_dir,
        manifest_sha256=manifest_digest,
        prerequisite_stages=tuple(stage["name"] for stage in predecessor_defs),
        source_binding_ids=tuple(binding["binding_id"] for binding in request["source_bindings"]),
        work_item_ids=tuple(item["item_id"] for item in request["work_items"]),
        request_digest=request["request_digest"],
    )


__all__ = [
    "PreflightFacts",
    "preflight_batch_request",
    "validate_frozen_request_authority",
]
