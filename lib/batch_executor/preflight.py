"""Read-only M0 authorization preflight for the assets batch slice."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping

from lib.checkpoint import CheckpointValidationError, read_checkpoint
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

    proposal_packets = [
        checkpoint["artifacts"]["proposal_packet"]
        for checkpoint in checkpoints.values()
        if isinstance(checkpoint.get("artifacts"), dict)
        and isinstance(checkpoint["artifacts"].get("proposal_packet"), dict)
    ]
    if len(proposal_packets) > 1:
        raise M0ContractError(
            "PROPOSAL_APPROVAL_AMBIGUOUS", "More than one proposal_packet is present"
        )
    if proposal_packets:
        proposal_status = (proposal_packets[0].get("approval") or {}).get("status")
        if proposal_status not in {"approved", "approved_with_changes"}:
            raise M0ContractError(
                "PROPOSAL_NOT_APPROVED", f"Proposal status is {proposal_status!r}"
            )
        if authorization["approval_status"] != proposal_status:
            raise M0ContractError(
                "PROPOSAL_APPROVAL_MISMATCH", "Frozen approval status differs from proposal"
            )
    if authorization["approval_status"] == "approved_with_changes" and not authorization[
        "decision_refs"
    ]:
        raise M0ContractError(
            "APPROVAL_CHANGE_UNBOUND", "approved_with_changes requires immutable decision refs"
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


__all__ = ["PreflightFacts", "preflight_batch_request"]
