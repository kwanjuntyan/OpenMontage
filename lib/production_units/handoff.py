"""Durable, fail-closed handoff for reviewed Production Unit JSON candidates.

This module is deliberately narrower than a pipeline orchestrator. It owns no
creative decision, provider call, Human Gate, asset publication, or render
publication. It persists an immutable director/reviewer/validator handoff and
then delegates the only canonical write to ``lib.checkpoint.write_checkpoint``.

The mutable ``state.json`` file is a repairable projection of immutable record
digests. It is never approval or publication authority.
"""

from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from functools import lru_cache
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Callable, Iterator, Mapping

import jsonschema

from lib.batch_executor.errors import LocalRunLocked
from lib.batch_executor.storage import LocalRunLock
from lib.checkpoint import (
    CheckpointWriteLocked,
    CheckpointValidationError,
    checkpoint_write_locks,
    get_pipeline_stages,
    read_checkpoint,
    write_checkpoint,
)
from lib.clp_validator import (
    canonical_digest,
    canonical_json_bytes,
    validate_clp_bundle_or_raise,
)
from lib.identity import InvalidProjectIdError, resolve_project_dir
from lib.pipeline_loader import (
    get_stage_human_approval_default,
    load_pipeline_readonly,
)
from schemas.artifacts import validate_artifact

from .contracts import ProductionUnitContractError, resolve_execution_contract


_SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "schemas" / "execution"
_RECORD_SCHEMA = "production_unit_handoff_record"
_STATE_SCHEMA = "production_unit_handoff_state"
_CHECKPOINT_PROVENANCE_SCHEMA = "production_unit_checkpoint_provenance"
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_PUP_STAGES = frozenset({"script", "clp", "scene_plan", "assets", "edit", "compose"})
_JSON_HANDOFF_STAGES = frozenset({"script", "clp", "scene_plan", "edit"})
_CONFLICTING_METADATA_KEYS = frozenset(
    {"production_units", "batch_v2_publication", "pup_render_publication"}
)
_RECORD_FILES = {
    "plan": "plan.json",
    "candidate": "candidate.json",
    "review": "review.json",
    "validation": "validation.json",
    "checkpoint_intent": "checkpoint-intent.json",
    "checkpoint_receipt": "checkpoint-receipt.json",
}
_RECORD_ORDER = tuple(_RECORD_FILES)

CrashHook = Callable[[str], None]


class ProductionUnitHandoffError(RuntimeError):
    """Stable fail-closed error for the M6.0B handoff seam."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"{code}: {message}")


def _fail(code: str, message: str) -> None:
    raise ProductionUnitHandoffError(code, message)


def _identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        _fail("INVALID_IDENTITY", f"{field} is not a safe identifier")
    return value


def _digest(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _DIGEST.fullmatch(value):
        _fail("INVALID_DIGEST", f"{field} is not a PUP sha256 digest")
    return value


def _freeze(
    document: Mapping[str, Any], digest_field: str = "record_sha256"
) -> dict[str, Any]:
    value = deepcopy(dict(document))
    value[digest_field] = canonical_digest(value)
    return value


def _without(document: Mapping[str, Any], field: str) -> dict[str, Any]:
    return {key: deepcopy(value) for key, value in document.items() if key != field}


@lru_cache(maxsize=2)
def _load_schema(name: str) -> dict[str, Any]:
    path = _SCHEMA_ROOT / f"{name}.schema.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _fail("HANDOFF_SCHEMA_UNAVAILABLE", f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        _fail("HANDOFF_SCHEMA_UNAVAILABLE", f"{path} must contain a JSON object")
    return value


def _validate_schema(name: str, document: Mapping[str, Any]) -> dict[str, Any]:
    value = deepcopy(dict(document))
    try:
        jsonschema.validate(instance=value, schema=_load_schema(name))
    except jsonschema.ValidationError as exc:
        _fail("INVALID_HANDOFF_RECORD", f"{name}: {exc.message}")
    return value


def _validate_record(
    document: Mapping[str, Any], expected_type: str
) -> dict[str, Any]:
    value = _validate_schema(_RECORD_SCHEMA, document)
    if value.get("record_type") != expected_type:
        _fail(
            "HANDOFF_RECORD_TYPE_MISMATCH",
            f"expected {expected_type!r}, got {value.get('record_type')!r}",
        )
    expected = canonical_digest(_without(value, "record_sha256"))
    if value.get("record_sha256") != expected:
        _fail("HANDOFF_RECORD_TAMPERED", f"{expected_type} digest mismatch")
    return value


def _validate_state(document: Mapping[str, Any]) -> dict[str, Any]:
    value = _validate_schema(_STATE_SCHEMA, document)
    expected = canonical_digest(_without(value, "state_sha256"))
    if value.get("state_sha256") != expected:
        _fail("HANDOFF_STATE_TAMPERED", "state projection digest mismatch")
    return value


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_immutable(path: Path, document: Mapping[str, Any]) -> bool:
    """Publish one complete record without replacement."""

    payload = canonical_json_bytes(document)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary_path, path)
        except FileExistsError:
            try:
                existing = path.read_bytes()
            except OSError as exc:
                _fail("HANDOFF_RECORD_CONFLICT", f"cannot read existing {path}: {exc}")
            if existing != payload:
                _fail(
                    "HANDOFF_RECORD_CONFLICT",
                    f"immutable handoff record identity was reused: {path.name}",
                )
            return False
        except OSError as exc:
            _fail(
                "IMMUTABLE_PUBLISH_UNAVAILABLE",
                f"atomic no-replace publication failed for {path}: {exc}",
            )
        _fsync_directory(path.parent)
        return True
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def _write_projection(path: Path, document: Mapping[str, Any]) -> None:
    payload = canonical_json_bytes(document)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        _fsync_directory(path.parent)
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def _read_json(path: Path, *, code: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _fail(code, f"cannot read {path}: {exc}")
    if not isinstance(value, dict):
        _fail(code, f"{path} must contain a JSON object")
    return value


class ProductionUnitHandoffCoordinator:
    """One project-scoped, JSON-only candidate handoff coordinator."""

    def __init__(
        self,
        projects_root: str | Path,
        project_id: str,
        handoff_id: str,
    ) -> None:
        self.projects_root = Path(projects_root).resolve()
        self.project_id = _identifier(project_id, "project_id")
        self.handoff_id = _identifier(handoff_id, "handoff_id")
        try:
            self.project_dir = resolve_project_dir(self.projects_root, self.project_id)
        except InvalidProjectIdError as exc:
            _fail("INVALID_PROJECT", str(exc))
        lexical = self.project_dir / ".production-units" / "handoffs" / self.handoff_id
        resolved = lexical.resolve(strict=False)
        if os.path.normcase(str(resolved)) != os.path.normcase(str(lexical)):
            _fail("HANDOFF_PATH_ALIAS", "handoff path changes identity through a symlink")
        try:
            resolved.relative_to(self.project_dir)
        except ValueError:
            _fail("HANDOFF_PATH_ESCAPE", "handoff path escapes the project directory")
        self.handoff_dir = resolved
        self.state_path = self.handoff_dir / "state.json"
        self.lock_path = self.handoff_dir / "coordinator.lock"

    def _record_path(self, record_type: str) -> Path:
        try:
            filename = _RECORD_FILES[record_type]
        except KeyError:
            _fail("HANDOFF_RECORD_TYPE_MISMATCH", f"unknown record type {record_type!r}")
        return self.handoff_dir / filename

    @contextmanager
    def _lock(self) -> Iterator[None]:
        try:
            with LocalRunLock(self.lock_path):
                yield
        except LocalRunLocked as exc:
            _fail("HANDOFF_COORDINATOR_BUSY", str(exc))

    def _project_marker(self) -> dict[str, Any]:
        marker = _read_json(
            self.project_dir / "project.json", code="PROJECT_MARKER_INVALID"
        )
        if marker.get("project_id") != self.project_id:
            _fail("PROJECT_MARKER_INVALID", "project marker identity mismatch")
        _identifier(marker.get("pipeline_type"), "pipeline_type")
        return marker

    def _approved_policy(
        self, stage: str
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]] | None:
        """Resolve policy only from the validated, approved proposal checkpoint."""

        marker = self._project_marker()
        pipeline_type = marker["pipeline_type"]
        stages = get_pipeline_stages(pipeline_type)
        if "proposal" not in stages:
            return None
        proposal = read_checkpoint(self.projects_root, self.project_id, "proposal")
        if proposal is None:
            return None
        if proposal.get("status") != "completed" or proposal.get("human_approved") is not True:
            return None
        packet = (proposal.get("artifacts") or {}).get("proposal_packet")
        policy = (
            (packet.get("production_plan") or {}).get("production_unit_policy")
            if isinstance(packet, dict)
            else None
        )
        if policy is None:
            return None
        if not isinstance(policy, Mapping):
            _fail("APPROVED_POLICY_INVALID", "approved production-unit policy is not an object")
        disposition = None if policy.get("mode") == "off" else "publish_candidate"
        try:
            contract = resolve_execution_contract(
                stage=stage,
                production_unit_policy=policy,
                execution_disposition=disposition,
                allowed_dispositions={"publish_candidate"},
            )
        except ProductionUnitContractError as exc:
            _fail("APPROVED_POLICY_INVALID", str(exc))
        if contract is None:
            return None
        if (
            contract.get("legacy_mode_alias_used") is not False
            or contract.get("policy_mode_authority")
            != "validated_proposal_checkpoint_required"
        ):
            _fail("POLICY_AUTHORITY_INVALID", "legacy or untrusted policy cannot activate handoff")
        return deepcopy(proposal), deepcopy(dict(policy)), contract

    @staticmethod
    def _identity(
        *,
        handoff_id: str,
        project_id: str,
        run_id: str,
        pipeline_type: str,
        stage: str,
        execution_epoch: int,
        control_chain: Mapping[str, Any],
    ) -> dict[str, Any]:
        if (
            isinstance(execution_epoch, bool)
            or not isinstance(execution_epoch, int)
            or execution_epoch < 0
        ):
            _fail("INVALID_EXECUTION_EPOCH", "execution_epoch must be non-negative")
        chain = deepcopy(dict(control_chain))
        if set(chain) != {"chain_id", "event_sequence", "sha256"}:
            _fail("INVALID_CONTROL_CHAIN", "control_chain fields are incomplete or unknown")
        _identifier(chain.get("chain_id"), "control_chain.chain_id")
        if (
            isinstance(chain.get("event_sequence"), bool)
            or not isinstance(chain.get("event_sequence"), int)
            or chain["event_sequence"] < 0
        ):
            _fail("INVALID_CONTROL_CHAIN", "event_sequence must be non-negative")
        _digest(chain.get("sha256"), "control_chain.sha256")
        return {
            "handoff_id": _identifier(handoff_id, "handoff_id"),
            "project_id": _identifier(project_id, "project_id"),
            "run_id": _identifier(run_id, "run_id"),
            "pipeline_type": _identifier(pipeline_type, "pipeline_type"),
            "stage": stage,
            "execution_epoch": execution_epoch,
            "control_chain": chain,
        }

    @staticmethod
    def _checkpoint_ref(stage: str, checkpoint: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "stage": stage,
            "logical_path": f"checkpoint_{stage}.json",
            "sha256": canonical_digest(checkpoint),
        }

    def _target_checkpoint_ref(self, stage: str) -> dict[str, Any]:
        checkpoint = read_checkpoint(self.projects_root, self.project_id, stage)
        return {
            "stage": stage,
            "logical_path": f"checkpoint_{stage}.json",
            "sha256": canonical_digest(checkpoint) if checkpoint is not None else None,
        }

    def _source_checkpoint_refs(
        self, *, pipeline_type: str, stage: str
    ) -> list[dict[str, Any]]:
        manifest = load_pipeline_readonly(pipeline_type)
        stages = get_pipeline_stages(pipeline_type)
        if stage not in stages:
            _fail("UNSUPPORTED_STAGE", f"stage {stage!r} is absent from {pipeline_type!r}")
        stage_defs = {
            row.get("name"): row
            for row in manifest.get("stages", [])
            if isinstance(row, dict) and isinstance(row.get("name"), str)
        }
        refs: list[dict[str, Any]] = []
        for predecessor in stages[: stages.index(stage)]:
            checkpoint = read_checkpoint(self.projects_root, self.project_id, predecessor)
            if checkpoint is None:
                if stage_defs.get(predecessor, {}).get("checkpoint_required", True) is not False:
                    _fail(
                        "SOURCE_CHECKPOINT_MISSING",
                        f"required predecessor {predecessor!r} is missing",
                    )
                continue
            if checkpoint.get("status") != "completed":
                _fail(
                    "SOURCE_CHECKPOINT_NOT_COMPLETED",
                    f"predecessor {predecessor!r} is not completed",
                )
            refs.append(self._checkpoint_ref(predecessor, checkpoint))
        if not any(ref["stage"] == "proposal" for ref in refs):
            _fail("POLICY_CHECKPOINT_MISSING", "approved proposal checkpoint is not a source")
        return refs

    def _load_record(
        self, record_type: str, *, required: bool = True
    ) -> dict[str, Any] | None:
        path = self._record_path(record_type)
        if not path.exists():
            if required:
                _fail("HANDOFF_RECORD_MISSING", f"{record_type} record is missing")
            return None
        value = _validate_record(
            _read_json(path, code="HANDOFF_RECORD_CORRUPT"), record_type
        )
        identity = value["identity"]
        if (
            identity["handoff_id"] != self.handoff_id
            or identity["project_id"] != self.project_id
        ):
            _fail("HANDOFF_IDENTITY_MISMATCH", f"{record_type} belongs elsewhere")
        return value

    def _load_chain(self) -> dict[str, dict[str, Any]]:
        records: dict[str, dict[str, Any]] = {}
        gap = False
        for record_type in _RECORD_ORDER:
            value = self._load_record(record_type, required=False)
            if value is None:
                gap = True
                continue
            if gap:
                _fail(
                    "HANDOFF_RECORD_SEQUENCE_INVALID",
                    f"{record_type} exists after a missing record",
                )
            records[record_type] = value
        if not records:
            return records
        identity = records["plan"]["identity"]
        for record_type, value in records.items():
            if identity != value["identity"]:
                _fail("HANDOFF_IDENTITY_MISMATCH", f"{record_type} identity drift")
        plan = records.get("plan")
        candidate = records.get("candidate")
        review = records.get("review")
        validation = records.get("validation")
        intent = records.get("checkpoint_intent")
        receipt = records.get("checkpoint_receipt")
        if candidate is not None:
            self._assert_stage_artifact_authority(
                identity["pipeline_type"], identity["stage"], candidate["artifacts"]
            )
            if plan["plan_sha256"] != canonical_digest(plan["plan"]):
                _fail("STALE_PLAN", "plan payload digest mismatch")
            contract = plan["execution_contract"]
            if (
                plan["execution_contract_sha256"]
                != contract.get("contract_sha256")
                or contract.get("contract_sha256")
                != canonical_digest(_without(contract, "contract_sha256"))
                or contract.get("stage") != identity["stage"]
                or contract.get("legacy_mode_alias_used") is not False
                or contract.get("policy_mode_authority")
                != "validated_proposal_checkpoint_required"
                or contract.get("execution_disposition") != "publish_candidate"
            ):
                _fail("EXECUTION_CONTRACT_TAMPERED", "plan execution contract is invalid")
            if candidate["plan_record_sha256"] != plan["record_sha256"]:
                _fail("STALE_PLAN", "candidate binds another plan record")
            if (
                candidate["policy_checkpoint"] != plan["policy_checkpoint"]
                or candidate["policy_sha256"] != plan["policy_sha256"]
            ):
                _fail("STALE_POLICY", "candidate policy binding differs from plan")
            if candidate["candidate_sha256"] != canonical_digest(candidate["artifacts"]):
                _fail("CANDIDATE_TAMPERED", "candidate artifact digest mismatch")
            if candidate["merge_evidence_sha256"] != canonical_digest(
                candidate["merge_evidence"]
            ):
                _fail("MERGE_EVIDENCE_TAMPERED", "merge evidence digest mismatch")
            if candidate["artifact_names"] != sorted(candidate["artifacts"]):
                _fail("CANDIDATE_TAMPERED", "artifact_names do not bind artifacts")
        if review is not None:
            if (
                review["candidate_record_sha256"] != candidate["record_sha256"]
                or review["candidate_sha256"] != candidate["candidate_sha256"]
            ):
                _fail("STALE_REVIEW", "review binds another candidate")
            if review["review_evidence_sha256"] != canonical_digest(
                review["review_evidence"]
            ):
                _fail("REVIEW_RECEIPT_TAMPERED", "review evidence digest mismatch")
        if validation is not None:
            if review["decision"] != "accepted":
                _fail("REVIEW_NOT_ACCEPTED", "rejected candidate has validation authority")
            if (
                validation["candidate_record_sha256"] != candidate["record_sha256"]
                or validation["candidate_sha256"] != candidate["candidate_sha256"]
                or validation["review_record_sha256"] != review["record_sha256"]
            ):
                _fail("STALE_VALIDATION", "validation binds another candidate/review")
        if intent is not None:
            if (
                intent["candidate_record_sha256"] != candidate["record_sha256"]
                or intent["candidate_sha256"] != candidate["candidate_sha256"]
                or intent["review_record_sha256"] != review["record_sha256"]
                or intent["validation_record_sha256"] != validation["record_sha256"]
                or intent["target_checkpoint_before"]
                != candidate["target_checkpoint_before"]
                or intent["target_status"] != validation["checkpoint_target_status"]
            ):
                _fail("STALE_CHECKPOINT_INTENT", "checkpoint intent chain mismatch")
        if receipt is not None:
            if (
                receipt["checkpoint_intent_sha256"] != intent["record_sha256"]
                or receipt["candidate_sha256"] != candidate["candidate_sha256"]
                or receipt["status"] != intent["target_status"]
            ):
                _fail("CHECKPOINT_RECEIPT_TAMPERED", "checkpoint receipt chain mismatch")
        return records

    def _projection(
        self, records: Mapping[str, Mapping[str, Any]], revision: int
    ) -> dict[str, Any]:
        plan = records.get("plan")
        if plan is None:
            _fail("HANDOFF_RECORD_MISSING", "plan record is missing")
        identity = plan["identity"]
        state = {
            "version": "1.0",
            "handoff_id": identity["handoff_id"],
            "project_id": identity["project_id"],
            "run_id": identity["run_id"],
            "pipeline_type": identity["pipeline_type"],
            "stage": identity["stage"],
            "execution_epoch": identity["execution_epoch"],
            "control_chain_sha256": identity["control_chain"]["sha256"],
            "revision": revision,
            "records": {
                key: records[key]["record_sha256"] if key in records else None
                for key in _RECORD_ORDER
            },
        }
        return _freeze(state, "state_sha256")

    def _refresh_projection(
        self, records: Mapping[str, Mapping[str, Any]]
    ) -> dict[str, Any]:
        current: dict[str, Any] | None = None
        if self.state_path.exists():
            current = _validate_state(
                _read_json(self.state_path, code="HANDOFF_STATE_CORRUPT")
            )
            identity = records["plan"]["identity"]
            if any(
                current[field] != identity[field]
                for field in (
                    "handoff_id",
                    "project_id",
                    "run_id",
                    "pipeline_type",
                    "stage",
                    "execution_epoch",
                )
            ) or current["control_chain_sha256"] != identity["control_chain"]["sha256"]:
                _fail("HANDOFF_STATE_STALE", "state identity/epoch/control chain drifted")
            derived = {
                key: records[key]["record_sha256"] if key in records else None
                for key in _RECORD_ORDER
            }
            for key, state_digest in current["records"].items():
                if state_digest is not None and state_digest != derived[key]:
                    _fail("HANDOFF_STATE_STALE", f"state points to stale {key}")
            if current["records"] == derived:
                return current
            revision = current["revision"] + 1
        else:
            revision = 0
        state = self._projection(records, revision)
        _validate_state(state)
        _write_projection(self.state_path, state)
        return state

    def _assert_sources_current(self, candidate: Mapping[str, Any]) -> None:
        identity = candidate["identity"]
        current_refs = self._source_checkpoint_refs(
            pipeline_type=identity["pipeline_type"], stage=identity["stage"]
        )
        if current_refs != candidate["source_checkpoints"]:
            _fail("STALE_SOURCE_CHECKPOINT", "predecessor set or digest changed")
        proposal = read_checkpoint(self.projects_root, self.project_id, "proposal")
        if proposal is None:
            _fail("STALE_POLICY", "approved proposal checkpoint disappeared")
        if canonical_digest(proposal) != candidate["policy_checkpoint"]["sha256"]:
            _fail("STALE_POLICY", "approved proposal checkpoint changed")
        packet = (proposal.get("artifacts") or {}).get("proposal_packet") or {}
        policy = (packet.get("production_plan") or {}).get("production_unit_policy")
        if not isinstance(policy, dict) or canonical_digest(policy) != candidate["policy_sha256"]:
            _fail("STALE_POLICY", "approved policy bytes changed")

    @staticmethod
    def _assert_stage_artifact_authority(
        pipeline_type: str, stage: str, artifacts: Mapping[str, Any]
    ) -> None:
        manifest = load_pipeline_readonly(pipeline_type)
        stage_definition = next(
            (
                item
                for item in manifest.get("stages", [])
                if isinstance(item, dict) and item.get("name") == stage
            ),
            None,
        )
        if stage_definition is None:
            _fail("UNSUPPORTED_STAGE", f"stage {stage!r} is absent from manifest")
        allowed = set(stage_definition.get("produces") or []) | set(
            stage_definition.get("optional_produces") or []
        )
        artifact_names = set(artifacts)
        foreign = sorted(artifact_names - allowed)
        if foreign:
            _fail(
                "STAGE_ARTIFACT_AUTHORITY_VIOLATION",
                f"stage {stage!r} may publish only {sorted(allowed)}; "
                f"foreign artifacts: {foreign}",
            )

    @staticmethod
    def _checkpoint_target_status(
        pipeline_type: str, stage: str, artifacts: Mapping[str, Any]
    ) -> str:
        manifest = load_pipeline_readonly(pipeline_type)
        requires_human = get_stage_human_approval_default(manifest, stage)
        if requires_human is None:
            _fail("UNSUPPORTED_STAGE", f"stage {stage!r} is absent from manifest")
        if stage == "clp":
            clp_manifest = artifacts.get("clp_manifest") or {}
            entities = any(
                clp_manifest.get(key) for key in ("characters", "locations", "props")
            )
            candidates = artifacts.get("clp_candidates") or {}
            candidate_groups = candidates.get("candidates") or {}
            extracted = any(
                candidate_groups.get(key)
                for key in ("characters", "locations", "props")
            )
            requires_human = bool(requires_human) or entities or extracted
        return "awaiting_human" if requires_human else "completed"

    def prepare_candidate(
        self,
        *,
        run_id: str,
        stage: str,
        execution_epoch: int,
        control_chain: Mapping[str, Any],
        plan: Mapping[str, Any],
        artifacts: Mapping[str, Any],
        merge_evidence: Mapping[str, Any],
        provider_charge_state: str = "not_applicable",
        crash_hook: CrashHook | None = None,
    ) -> dict[str, Any] | None:
        """Persist a non-canonical candidate, or return ``None`` for policy off."""

        if stage not in _PUP_STAGES:
            _fail("UNSUPPORTED_STAGE", f"M6.0B does not support {stage!r}")
        approved = self._approved_policy(stage)
        if approved is None:
            return None
        if stage not in _JSON_HANDOFF_STAGES:
            if stage == "assets":
                _fail("BATCH_V2_AUTHORITY_REQUIRED", "assets remain Batch V2-owned")
            if stage == "compose":
                _fail("RENDER_AUTHORITY_NOT_QUALIFIED", "render is deferred to M6.0C")
            _fail("UNSUPPORTED_STAGE", f"M6.0B JSON handoff does not support {stage!r}")
        proposal, policy, contract = approved
        if provider_charge_state == "ambiguous":
            _fail(
                "AMBIGUOUS_CHARGED_ATTEMPT",
                "operator resolution is required; this seam never auto-retries provider work",
            )
        if provider_charge_state != "not_applicable":
            _fail(
                "INVALID_CHARGE_STATE",
                "M6.0B JSON handoff has no provider/charge authority",
            )
        marker = self._project_marker()
        pipeline_type = marker["pipeline_type"]
        self._assert_stage_artifact_authority(pipeline_type, stage, artifacts)
        identity = self._identity(
            handoff_id=self.handoff_id,
            project_id=self.project_id,
            run_id=run_id,
            pipeline_type=pipeline_type,
            stage=stage,
            execution_epoch=execution_epoch,
            control_chain=control_chain,
        )
        plan_value = deepcopy(dict(plan))
        artifacts_value = deepcopy(dict(artifacts))
        merge_value = deepcopy(dict(merge_evidence))
        try:
            plan_sha = canonical_digest(plan_value)
            candidate_sha = canonical_digest(artifacts_value)
            merge_sha = canonical_digest(merge_value)
        except (TypeError, ValueError) as exc:
            _fail("NON_CANONICAL_JSON", str(exc))
        source_refs = self._source_checkpoint_refs(
            pipeline_type=pipeline_type, stage=stage
        )
        policy_ref = self._checkpoint_ref("proposal", proposal)
        plan_record = _freeze(
            {
                "version": "1.0",
                "record_type": "plan",
                "identity": identity,
                "policy_checkpoint": policy_ref,
                "policy_sha256": canonical_digest(policy),
                "execution_contract": contract,
                "execution_contract_sha256": contract["contract_sha256"],
                "plan": plan_value,
                "plan_sha256": plan_sha,
            }
        )
        candidate_record = _freeze(
            {
                "version": "1.0",
                "record_type": "candidate",
                "identity": identity,
                "publication_authority": "pup_json_merge",
                "plan_record_sha256": plan_record["record_sha256"],
                "policy_checkpoint": policy_ref,
                "policy_sha256": canonical_digest(policy),
                "source_checkpoints": source_refs,
                "target_checkpoint_before": self._target_checkpoint_ref(stage),
                "artifact_names": sorted(artifacts_value),
                "artifacts": artifacts_value,
                "candidate_sha256": candidate_sha,
                "merge_evidence": merge_value,
                "merge_evidence_sha256": merge_sha,
                "provider_charge_state": provider_charge_state,
            }
        )
        _validate_record(plan_record, "plan")
        _validate_record(candidate_record, "candidate")
        with self._lock():
            _write_immutable(self._record_path("plan"), plan_record)
            if crash_hook is not None:
                crash_hook("plan_persisted")
            _write_immutable(self._record_path("candidate"), candidate_record)
            if crash_hook is not None:
                crash_hook("candidate_persisted")
            records = self._load_chain()
            self._refresh_projection(records)
        return deepcopy(candidate_record)

    def record_review(
        self,
        *,
        decision: str,
        review_evidence: Mapping[str, Any],
        crash_hook: CrashHook | None = None,
    ) -> dict[str, Any]:
        if decision not in {"accepted", "rejected"}:
            _fail("INVALID_REVIEW_DECISION", "review decision must be accepted/rejected")
        evidence = deepcopy(dict(review_evidence))
        try:
            evidence_sha = canonical_digest(evidence)
        except (TypeError, ValueError) as exc:
            _fail("NON_CANONICAL_JSON", str(exc))
        with self._lock():
            records = self._load_chain()
            candidate = records.get("candidate")
            if candidate is None:
                _fail("HANDOFF_RECORD_MISSING", "candidate record is missing")
            self._assert_sources_current(candidate)
            self._refresh_projection(records)
            review = _freeze(
                {
                    "version": "1.0",
                    "record_type": "review",
                    "identity": candidate["identity"],
                    "authority": "stage_review_only",
                    "candidate_record_sha256": candidate["record_sha256"],
                    "candidate_sha256": candidate["candidate_sha256"],
                    "decision": decision,
                    "review_evidence": evidence,
                    "review_evidence_sha256": evidence_sha,
                }
            )
            _validate_record(review, "review")
            _write_immutable(self._record_path("review"), review)
            if crash_hook is not None:
                crash_hook("review_persisted")
            records = self._load_chain()
            self._refresh_projection(records)
            return deepcopy(review)

    def validate_candidate(
        self, *, crash_hook: CrashHook | None = None
    ) -> dict[str, Any]:
        with self._lock():
            records = self._load_chain()
            candidate = records.get("candidate")
            review = records.get("review")
            if candidate is None or review is None:
                _fail("HANDOFF_RECORD_MISSING", "candidate and review are required")
            if review["decision"] != "accepted":
                _fail("REVIEW_NOT_ACCEPTED", "rejected candidate cannot be validated")
            self._assert_sources_current(candidate)
            self._refresh_projection(records)
            artifact_digests: dict[str, str] = {}
            try:
                for name, artifact in candidate["artifacts"].items():
                    validate_artifact(name, artifact, project_dir=self.project_dir)
                    artifact_digests[name] = canonical_digest(artifact)
                validate_clp_bundle_or_raise(
                    candidate["artifacts"], project_dir=self.project_dir
                )
            except Exception as exc:
                _fail("CANONICAL_ARTIFACT_VALIDATION_FAILED", str(exc))
            target_status = self._checkpoint_target_status(
                candidate["identity"]["pipeline_type"],
                candidate["identity"]["stage"],
                candidate["artifacts"],
            )
            validation = _freeze(
                {
                    "version": "1.0",
                    "record_type": "validation",
                    "identity": candidate["identity"],
                    "authority": "canonical_artifact_validator",
                    "candidate_record_sha256": candidate["record_sha256"],
                    "candidate_sha256": candidate["candidate_sha256"],
                    "review_record_sha256": review["record_sha256"],
                    "outcome": "passed",
                    "validated_artifact_digests": artifact_digests,
                    "checkpoint_target_status": target_status,
                }
            )
            _validate_record(validation, "validation")
            _write_immutable(self._record_path("validation"), validation)
            if crash_hook is not None:
                crash_hook("validation_persisted")
            records = self._load_chain()
            self._refresh_projection(records)
            return deepcopy(validation)

    @staticmethod
    def _handoff_metadata(
        candidate: Mapping[str, Any],
        review: Mapping[str, Any],
        validation: Mapping[str, Any],
        intent: Mapping[str, Any],
    ) -> dict[str, Any]:
        identity = candidate["identity"]
        return {
            "version": "1.0",
            "authority": "pup_json_merge",
            "handoff_id": identity["handoff_id"],
            "run_id": identity["run_id"],
            "execution_epoch": identity["execution_epoch"],
            "control_chain": deepcopy(identity["control_chain"]),
            "policy_checkpoint_sha256": candidate["policy_checkpoint"]["sha256"],
            "policy_sha256": candidate["policy_sha256"],
            "plan_record_sha256": candidate["plan_record_sha256"],
            "candidate_record_sha256": candidate["record_sha256"],
            "candidate_sha256": candidate["candidate_sha256"],
            "review_record_sha256": review["record_sha256"],
            "validation_record_sha256": validation["record_sha256"],
            "checkpoint_intent_sha256": intent["record_sha256"],
        }

    def _expected_checkpoint_metadata(
        self,
        candidate: Mapping[str, Any],
        review: Mapping[str, Any],
        validation: Mapping[str, Any],
        intent: Mapping[str, Any],
    ) -> dict[str, Any]:
        metadata = deepcopy(intent["metadata"])
        conflicting = sorted(set(metadata) & _CONFLICTING_METADATA_KEYS)
        if conflicting:
            _fail(
                "HYBRID_PUBLICATION_AUTHORITY",
                f"JSON handoff metadata contains reserved authority keys: {conflicting}",
            )
        metadata["production_units"] = {
            "candidate_handoff": self._handoff_metadata(
                candidate, review, validation, intent
            )
        }
        return metadata

    def _checkpoint_is_exact(
        self,
        checkpoint: Mapping[str, Any] | None,
        candidate: Mapping[str, Any],
        review: Mapping[str, Any],
        validation: Mapping[str, Any],
        intent: Mapping[str, Any],
    ) -> bool:
        if not isinstance(checkpoint, Mapping):
            return False
        identity = candidate["identity"]
        return (
            checkpoint.get("project_id") == identity["project_id"]
            and checkpoint.get("pipeline_type") == identity["pipeline_type"]
            and checkpoint.get("stage") == identity["stage"]
            and checkpoint.get("status") == intent["target_status"]
            and checkpoint.get("human_approved") is False
            and canonical_digest(checkpoint.get("artifacts"))
            == candidate["candidate_sha256"]
            and checkpoint.get("review") == intent["review"]
            and checkpoint.get("cost_snapshot") == intent["cost_snapshot"]
            and checkpoint.get("metadata")
            == self._expected_checkpoint_metadata(candidate, review, validation, intent)
        )

    def _commit_intent_locked(
        self,
        records: dict[str, dict[str, Any]],
        *,
        crash_hook: CrashHook | None,
    ) -> dict[str, Any]:
        candidate = records["candidate"]
        stages = {
            candidate["identity"]["stage"],
            *(ref["stage"] for ref in candidate["source_checkpoints"]),
        }
        try:
            with checkpoint_write_locks(
                self.projects_root, self.project_id, stages
            ):
                return self._commit_intent_with_stage_locks(
                    records, crash_hook=crash_hook
                )
        except CheckpointWriteLocked as exc:
            _fail("CHECKPOINT_STAGE_BUSY", str(exc))

    def _commit_intent_with_stage_locks(
        self,
        records: dict[str, dict[str, Any]],
        *,
        crash_hook: CrashHook | None,
    ) -> dict[str, Any]:
        candidate = records["candidate"]
        review = records["review"]
        validation = records["validation"]
        intent = records["checkpoint_intent"]
        receipt = records.get("checkpoint_receipt")
        self._assert_sources_current(candidate)
        current = read_checkpoint(
            self.projects_root, self.project_id, candidate["identity"]["stage"]
        )
        if receipt is not None:
            if not self._checkpoint_is_exact(
                current, candidate, review, validation, intent
            ):
                _fail("STALE_CHECKPOINT", "checkpoint changed after handoff receipt")
            if canonical_digest(current) != receipt["checkpoint"]["sha256"]:
                _fail("CHECKPOINT_RECEIPT_TAMPERED", "checkpoint differs from receipt")
            return {"receipt": deepcopy(receipt), "idempotent": True}

        if not self._checkpoint_is_exact(
            current, candidate, review, validation, intent
        ):
            current_sha = canonical_digest(current) if current is not None else None
            if current_sha != intent["target_checkpoint_before"]["sha256"]:
                _fail("STALE_CHECKPOINT", "target checkpoint changed after validation")
            identity = candidate["identity"]
            try:
                write_checkpoint(
                    self.projects_root,
                    self.project_id,
                    identity["stage"],
                    intent["target_status"],
                    deepcopy(candidate["artifacts"]),
                    pipeline_type=identity["pipeline_type"],
                    checkpoint_policy="guided",
                    human_approval_required=intent["target_status"]
                    == "awaiting_human",
                    human_approved=False,
                    review=deepcopy(intent["review"]),
                    cost_snapshot=deepcopy(intent["cost_snapshot"]),
                    metadata=self._expected_checkpoint_metadata(
                        candidate, review, validation, intent
                    ),
                )
            except CheckpointValidationError as exc:
                _fail("CHECKPOINT_WRITER_REJECTED", str(exc))
            if crash_hook is not None:
                crash_hook("checkpoint_written")
            current = read_checkpoint(
                self.projects_root, self.project_id, identity["stage"]
            )
        if not self._checkpoint_is_exact(current, candidate, review, validation, intent):
            _fail("CHECKPOINT_ROUNDTRIP_INVALID", "reader did not return exact handoff")
        checkpoint_ref = self._checkpoint_ref(
            candidate["identity"]["stage"], current
        )
        receipt = _freeze(
            {
                "version": "1.0",
                "record_type": "checkpoint_receipt",
                "identity": candidate["identity"],
                "publication_authority": "pup_json_merge",
                "checkpoint_intent_sha256": intent["record_sha256"],
                "candidate_sha256": candidate["candidate_sha256"],
                "checkpoint": checkpoint_ref,
                "status": current["status"],
                "human_approved": False,
            }
        )
        _validate_record(receipt, "checkpoint_receipt")
        _write_immutable(self._record_path("checkpoint_receipt"), receipt)
        if crash_hook is not None:
            crash_hook("checkpoint_receipt_persisted")
        records = self._load_chain()
        self._refresh_projection(records)
        return {"receipt": deepcopy(receipt), "idempotent": False}

    def submit_checkpoint(
        self,
        *,
        cost_snapshot: Mapping[str, Any] | None = None,
        metadata: Mapping[str, Any] | None = None,
        crash_hook: CrashHook | None = None,
    ) -> dict[str, Any]:
        """Commit a reviewed candidate through the existing checkpoint writer.

        This API never accepts ``human_approved=True``. Gated stages are written
        as ``awaiting_human`` and the original workflow owns the later gate.
        """

        metadata_value = deepcopy(dict(metadata or {}))
        conflicting = sorted(set(metadata_value) & _CONFLICTING_METADATA_KEYS)
        if conflicting:
            _fail(
                "HYBRID_PUBLICATION_AUTHORITY",
                f"JSON handoff metadata contains reserved authority keys: {conflicting}",
            )
        cost_value = (
            deepcopy(dict(cost_snapshot)) if cost_snapshot is not None else None
        )
        with self._lock():
            records = self._load_chain()
            for required in ("candidate", "review", "validation"):
                if required not in records:
                    _fail("HANDOFF_RECORD_MISSING", f"{required} record is required")
            candidate = records["candidate"]
            review = records["review"]
            validation = records["validation"]
            if review["decision"] != "accepted":
                _fail("REVIEW_NOT_ACCEPTED", "rejected candidate cannot be checkpointed")
            self._assert_sources_current(candidate)
            self._refresh_projection(records)
            intent = _freeze(
                {
                    "version": "1.0",
                    "record_type": "checkpoint_intent",
                    "identity": candidate["identity"],
                    "publication_authority": "pup_json_merge",
                    "candidate_record_sha256": candidate["record_sha256"],
                    "candidate_sha256": candidate["candidate_sha256"],
                    "review_record_sha256": review["record_sha256"],
                    "validation_record_sha256": validation["record_sha256"],
                    "target_checkpoint_before": candidate["target_checkpoint_before"],
                    "target_status": validation["checkpoint_target_status"],
                    "human_approved": False,
                    "review": deepcopy(review["review_evidence"]),
                    "cost_snapshot": cost_value,
                    "metadata": metadata_value,
                }
            )
            _validate_record(intent, "checkpoint_intent")
            _write_immutable(self._record_path("checkpoint_intent"), intent)
            if crash_hook is not None:
                crash_hook("checkpoint_intent_persisted")
            records = self._load_chain()
            self._refresh_projection(records)
            return self._commit_intent_locked(records, crash_hook=crash_hook)

    def resume_checkpoint(
        self, *, crash_hook: CrashHook | None = None
    ) -> dict[str, Any]:
        """Resume only an already-persisted checkpoint intent."""

        with self._lock():
            records = self._load_chain()
            if "checkpoint_intent" not in records:
                _fail("CHECKPOINT_INTENT_MISSING", "there is no intent to resume")
            self._refresh_projection(records)
            return self._commit_intent_locked(records, crash_hook=crash_hook)


def validate_checkpoint_handoff_provenance(
    checkpoint: Mapping[str, Any], *, projects_root: str | Path
) -> None:
    """Authenticate optional PUP provenance during canonical checkpoint reads.

    The official writer invokes the same validation before its atomic replace.
    A missing provenance object is a legacy/ordinary checkpoint and remains
    unaffected. The later original Human Gate may change only checkpoint
    status/approval while carrying forward the same candidate bytes/provenance.
    """

    metadata = checkpoint.get("metadata")
    if not isinstance(metadata, Mapping):
        return
    production_units = metadata.get("production_units")
    if not isinstance(production_units, Mapping):
        return
    provenance = production_units.get("candidate_handoff")
    if provenance is None:
        return
    if not isinstance(provenance, Mapping):
        _fail("CHECKPOINT_PROVENANCE_INVALID", "candidate_handoff must be an object")
    conflicting = sorted(
        key
        for key in _CONFLICTING_METADATA_KEYS
        if key != "production_units" and key in metadata
    )
    if conflicting:
        _fail(
            "HYBRID_PUBLICATION_AUTHORITY",
            f"PUP JSON checkpoint mixes publication authority: {conflicting}",
        )
    value = _validate_schema(_CHECKPOINT_PROVENANCE_SCHEMA, provenance)
    project_id = checkpoint.get("project_id")
    stage = checkpoint.get("stage")
    if stage not in _JSON_HANDOFF_STAGES:
        _fail("CHECKPOINT_PROVENANCE_INVALID", "JSON handoff appears on wrong stage")
    coordinator = ProductionUnitHandoffCoordinator(
        projects_root, project_id, value["handoff_id"]
    )
    records = coordinator._load_chain()
    required = ("plan", "candidate", "review", "validation", "checkpoint_intent")
    missing = [name for name in required if name not in records]
    if missing:
        _fail(
            "CHECKPOINT_PROVENANCE_INVALID",
            f"checkpoint provenance is missing durable records: {missing}",
        )
    candidate = records["candidate"]
    review = records["review"]
    validation = records["validation"]
    intent = records["checkpoint_intent"]
    identity = candidate["identity"]
    if (
        identity["project_id"] != project_id
        or identity["pipeline_type"] != checkpoint.get("pipeline_type")
        or identity["stage"] != stage
    ):
        _fail("CHECKPOINT_PROVENANCE_INVALID", "checkpoint/handoff identity mismatch")
    expected = coordinator._handoff_metadata(candidate, review, validation, intent)
    if value != expected:
        _fail("CHECKPOINT_PROVENANCE_TAMPERED", "checkpoint provenance digest chain mismatch")
    if canonical_digest(checkpoint.get("artifacts")) != candidate["candidate_sha256"]:
        _fail("CHECKPOINT_PROVENANCE_TAMPERED", "checkpoint artifact differs from candidate")
    direct_transition = (
        checkpoint.get("status") == intent["target_status"]
        and checkpoint.get("human_approved") is False
    )
    original_human_gate_transition = (
        intent["target_status"] == "awaiting_human"
        and checkpoint.get("status") == "completed"
        and checkpoint.get("human_approved") is True
    )
    if not (direct_transition or original_human_gate_transition):
        _fail(
            "CHECKPOINT_PROVENANCE_INVALID",
            "checkpoint status/approval is not the intent or original Human Gate transition",
        )
    receipt = records.get("checkpoint_receipt")
    if original_human_gate_transition and receipt is None:
        _fail(
            "HUMAN_GATE_RECEIPT_MISSING",
            "Human Gate completion requires the durable awaiting_human receipt",
        )
    if original_human_gate_transition and (
        receipt["status"] != "awaiting_human"
        or receipt["human_approved"] is not False
    ):
        _fail(
            "HUMAN_GATE_RECEIPT_INVALID",
            "Human Gate completion requires an awaiting_human/unapproved receipt",
        )
    if receipt is not None and direct_transition:
        if canonical_digest(checkpoint) != receipt["checkpoint"]["sha256"]:
            _fail(
                "CHECKPOINT_RECEIPT_TAMPERED",
                "current checkpoint bytes differ from durable handoff receipt",
            )


__all__ = [
    "ProductionUnitHandoffCoordinator",
    "ProductionUnitHandoffError",
    "validate_checkpoint_handoff_provenance",
]
