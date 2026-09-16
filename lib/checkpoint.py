"""Checkpoint writer/reader for pipeline state persistence.

Each stage writes a checkpoint after completion. The orchestrator uses
checkpoints to resume pipelines and to present state at human checkpoints.
"""

from __future__ import annotations

from contextlib import ExitStack, contextmanager
import json
import os
import re
from copy import deepcopy
from functools import lru_cache, wraps
from datetime import datetime, timezone
from pathlib import Path
import threading
from typing import Any, Optional

import jsonschema

from schemas.artifacts import ARTIFACT_NAMES, validate_artifact
from lib.identity import (
    InvalidProjectIdError,
    resolve_project_dir,
)

# All known stages across all pipelines (used only for artifact name lookup).
ALL_KNOWN_STAGES = frozenset([
    "research", "proposal", "idea", "script", "clp", "scene_plan",
    "assets", "edit", "compose", "publish",
])

# Backward-compatible alias — existing code / tests that import STAGES still work.
# New code should use get_pipeline_stages(pipeline_type) instead.
STAGES = ["research", "proposal", "idea", "script", "clp", "scene_plan",
          "assets", "edit", "compose", "publish"]

CANONICAL_STAGE_ARTIFACTS = {
    "research": "research_brief",
    "proposal": "proposal_packet",
    "idea": "brief",
    "script": "script",
    "clp": "clp_manifest",
    "scene_plan": "scene_plan",
    "assets": "asset_manifest",
    "edit": "edit_decisions",
    "compose": "render_report",
    "publish": "publish_log",
}

# Additional artifacts that may be produced alongside canonical ones.
# These are not stage-defining but are required by governance contracts.
SUPPLEMENTARY_ARTIFACTS = {
    "source_media_review",  # Required before first planning stage when user media exists
    "final_review",         # Required by compose stage before presenting to user
    "video_analysis_brief", # Reference-video grounding artifact carried alongside stages
}


def get_pipeline_stages(pipeline_type: str | None) -> list[str]:
    """Return the ordered stage list for a specific pipeline.

    Falls back to STAGES only when no pipeline type was supplied by a legacy
    caller.  Every supplied value, including the literal ``unknown``, must
    resolve to an exact, schema-valid manifest.

    Previous versions used a set intersection here, which produced
    nondeterministic ordering. The fallback now uses a stable list.
    """
    if pipeline_type is None:
        # Deterministic canonical fallback — sorted to ensure stable ordering
        import logging
        logging.getLogger(__name__).warning(
            "get_pipeline_stages called without pipeline_type — "
            "using canonical fallback order. Pass pipeline_type for correctness."
        )
        return list(STAGES)

    try:
        from lib.pipeline_loader import load_pipeline_readonly, get_stage_order
        manifest = load_pipeline_readonly(pipeline_type)
        return get_stage_order(manifest)
    except Exception as exc:
        raise CheckpointValidationError(
            f"Unknown pipeline_type or invalid manifest {pipeline_type!r}: {exc}"
        ) from exc

CHECKPOINT_SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent
    / "schemas"
    / "checkpoints"
    / "checkpoint.schema.json"
)

# Canonical project root. Checkpoints, artifacts, and the project marker all
# live under PROJECTS_DIR/<project_id>/ — this is the location the Backlot
# board watches. Callers may still pass a different pipeline_dir (tests do),
# but production runs should use the default.
from lib.paths import PROJECTS_DIR  # noqa: E402  (single source of truth)

PROJECT_MARKER_FILENAME = "project.json"
HISTORY_DIRNAME = "history"


class CheckpointValidationError(ValueError):
    """Raised when a checkpoint or its canonical artifacts are invalid."""


class CheckpointWriteLocked(CheckpointValidationError):
    """Raised when another writer owns a canonical project/stage checkpoint."""


STAGE_COMPONENT_PATTERN = r"^[a-zA-Z0-9_-]+$"
STAGE_COMPONENT_RE = re.compile(STAGE_COMPONENT_PATTERN)
CHECKPOINT_FORMAT_CHECKER = jsonschema.FormatChecker()
RFC3339_TIMESTAMP_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$"
)


def _validate_stage_component(stage: str) -> str:
    """Return a safe checkpoint filename component or fail before path use."""
    if not isinstance(stage, str) or not STAGE_COMPONENT_RE.fullmatch(stage):
        raise CheckpointValidationError(
            f"Invalid stage path component {stage!r}; expected pattern "
            f"{STAGE_COMPONENT_PATTERN!r}"
        )
    return stage


def _validate_rfc3339_timestamp(value: Any, field: str) -> None:
    """Validate timestamps even when jsonschema's optional checker is absent."""
    if not isinstance(value, str) or not RFC3339_TIMESTAMP_RE.fullmatch(value):
        raise CheckpointValidationError(
            f"{field} must be an ISO-8601 timestamp with timezone, got {value!r}"
        )
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CheckpointValidationError(
            f"{field} is not a real ISO-8601 calendar timestamp: {value!r}"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise CheckpointValidationError(
            f"{field} must include a timezone offset: {value!r}"
        )


def _project_directory(pipeline_dir: Path, project_id: str) -> Path:
    """Resolve one project beneath exactly one configured projects root."""
    try:
        return resolve_project_dir(pipeline_dir, project_id)
    except InvalidProjectIdError as exc:
        raise CheckpointValidationError(str(exc)) from exc


def _contained_project_path(project_dir: Path, *parts: str) -> Path:
    """Resolve a path and reject file/directory symlink or junction escapes."""
    root = Path(project_dir).resolve()
    path = root.joinpath(*parts).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise CheckpointValidationError(
            f"Path escapes exact project root {root}: {path}"
        ) from exc
    return path


_CHECKPOINT_LOCK_GUARD = threading.Lock()
_CHECKPOINT_LOCKS: dict[str, dict[str, Any]] = {}


class _CheckpointStageWriteLock:
    """Non-blocking, process-reentrant OS lock for one canonical stage file."""

    def __init__(self, path: Path):
        self.path = path
        self._key: str | None = None
        self._handle = None
        self._reentrant = False

    def __enter__(self) -> "_CheckpointStageWriteLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        key = os.path.normcase(str(self.path.resolve(strict=False)))
        owner = threading.get_ident()
        with _CHECKPOINT_LOCK_GUARD:
            state = _CHECKPOINT_LOCKS.get(key)
            if state is not None:
                if state["owner"] != owner:
                    raise CheckpointWriteLocked(
                        f"CHECKPOINT_STAGE_BUSY: another writer owns {self.path}"
                    )
                state["depth"] += 1
                self._key = key
                self._reentrant = True
                return self
            _CHECKPOINT_LOCKS[key] = {"owner": owner, "depth": 1}
        self._key = key
        handle = None
        try:
            handle = self.path.open("a+b")
            if os.name == "nt":
                import msvcrt

                handle.seek(0, os.SEEK_END)
                if handle.tell() == 0:
                    handle.write(b"\0")
                    handle.flush()
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, BlockingIOError) as exc:
            if handle is not None:
                handle.close()
            with _CHECKPOINT_LOCK_GUARD:
                _CHECKPOINT_LOCKS.pop(key, None)
            self._key = None
            raise CheckpointWriteLocked(
                f"CHECKPOINT_STAGE_BUSY: another writer owns {self.path}"
            ) from exc
        self._handle = handle
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        key = self._key
        if key is None:
            return
        if self._reentrant:
            with _CHECKPOINT_LOCK_GUARD:
                state = _CHECKPOINT_LOCKS[key]
                state["depth"] -= 1
            self._key = None
            return
        handle = self._handle
        self._handle = None
        try:
            if handle is not None:
                try:
                    if os.name == "nt":
                        import msvcrt

                        handle.seek(0)
                        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        import fcntl

                        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
                finally:
                    handle.close()
        finally:
            with _CHECKPOINT_LOCK_GUARD:
                _CHECKPOINT_LOCKS.pop(key, None)
            self._key = None


@contextmanager
def checkpoint_write_locks(
    pipeline_dir: Path,
    project_id: str,
    stages: list[str] | tuple[str, ...] | set[str],
):
    """Serialize canonical writes for a deterministic set of project stages."""

    project_dir = _project_directory(Path(pipeline_dir), project_id)
    safe_stages = sorted({_validate_stage_component(stage) for stage in stages})
    with ExitStack() as stack:
        for stage in safe_stages:
            lock_path = _contained_project_path(
                project_dir, ".checkpoint-locks", f"{stage}.lock"
            )
            stack.enter_context(_CheckpointStageWriteLock(lock_path))
        yield


def _serialize_checkpoint_write(function):
    @wraps(function)
    def locked(pipeline_dir, project_id, stage, *args, **kwargs):
        with checkpoint_write_locks(pipeline_dir, project_id, {stage}):
            return function(pipeline_dir, project_id, stage, *args, **kwargs)

    return locked


def _authenticate_project_marker(
    project_dir: Path,
    *,
    project_id: str,
    pipeline_type: str,
) -> None:
    """Bind a checkpoint envelope to project.json when the marker exists."""
    marker_path = _contained_project_path(project_dir, PROJECT_MARKER_FILENAME)
    if not marker_path.exists():
        return
    if not marker_path.is_file():
        raise CheckpointValidationError(
            f"Project marker is not a regular file: {marker_path}"
        )
    try:
        with open(marker_path, encoding="utf-8") as handle:
            marker = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise CheckpointValidationError(
            f"Cannot authenticate project marker {marker_path}: {exc}"
        ) from exc
    if not isinstance(marker, dict):
        raise CheckpointValidationError(
            f"Project marker must be a JSON object: {marker_path}"
        )
    if marker.get("project_id") != project_id:
        raise CheckpointValidationError(
            "Project marker identity mismatch: "
            f"expected {project_id!r}, got {marker.get('project_id')!r}"
        )
    if marker.get("pipeline_type") != pipeline_type:
        raise CheckpointValidationError(
            "Project marker pipeline_type mismatch: "
            f"checkpoint uses {pipeline_type!r}, marker has "
            f"{marker.get('pipeline_type')!r}"
        )


def _validate_style_playbook(style_playbook: str | None) -> None:
    """Fail closed when a checkpoint names a visual identity that cannot load."""

    if style_playbook is None:
        return
    try:
        from styles.playbook_loader import list_playbooks, load_playbook

        load_playbook(style_playbook)
    except Exception as exc:
        try:
            available = list_playbooks()
        except Exception:
            available = []
        raise CheckpointValidationError(
            f"Unknown or invalid style_playbook {style_playbook!r}. "
            f"Available playbooks: {available}. Underlying error: {exc}"
        ) from exc


@lru_cache(maxsize=1)
def _load_checkpoint_schema() -> dict[str, Any]:
    with open(CHECKPOINT_SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _validate_artifacts_for_stage(
    stage: str,
    status: str,
    artifacts: dict[str, Any],
    pipeline_type: str | None = None,
    project_dir: Optional[Path] = None,
) -> None:
    # Check declared produces if pipeline_type is known
    checked_produces = False
    if pipeline_type and pipeline_type != "unknown":
        try:
            from lib.pipeline_loader import load_pipeline_readonly
            manifest = load_pipeline_readonly(pipeline_type)
            for st in manifest.get("stages", []):
                if st.get("name") == stage and "produces" in st:
                    checked_produces = True
                    if status in {"completed", "awaiting_human"}:
                        for required_prod in st["produces"]:
                            if required_prod == "decision_log":
                                continue
                            if required_prod not in artifacts:
                                raise CheckpointValidationError(
                                    f"Stage {stage!r} with status {status!r} in pipeline {pipeline_type!r} "
                                    f"must include declared produced artifact {required_prod!r}"
                                )
        except CheckpointValidationError:
            raise
        except Exception as exc:
            raise CheckpointValidationError(
                f"Unknown pipeline_type or invalid manifest {pipeline_type!r}: {exc}"
            ) from exc

    # Valid stages come from the pipeline manifest (get_pipeline_stages), which
    # can declare stages beyond the 9 canonical ones (e.g. character-animation's
    # `character_design`/`rig_plan`, screen-demo's `real_capture`). Those have no
    # canonical artifact, so look it up defensively — a missing entry means the
    # stage simply has no required artifact, not a crash.
    if not checked_produces:
        required_artifact = CANONICAL_STAGE_ARTIFACTS.get(stage)
        if (
            required_artifact is not None
            and status in {"completed", "awaiting_human"}
            and required_artifact not in artifacts
        ):
            raise CheckpointValidationError(
                f"Stage {stage!r} with status {status!r} must include "
                f"canonical artifact {required_artifact!r}"
            )

    for artifact_name, artifact_data in artifacts.items():
        if artifact_name not in ARTIFACT_NAMES:
            raise CheckpointValidationError(
                f"Unknown artifact {artifact_name!r}. Must be registered in ARTIFACT_NAMES."
            )
        if not isinstance(artifact_data, dict):
            raise CheckpointValidationError(
                f"Artifact {artifact_name!r} must be a JSON object matching its schema"
            )
        try:
            validate_artifact(artifact_name, artifact_data, project_dir=project_dir)
        except Exception as exc:
            raise CheckpointValidationError(
                f"Artifact {artifact_name!r} failed schema validation: {exc}"
            ) from exc

    from lib.clp_validator import validate_clp_bundle_or_raise, CLPValidationError
    try:
        validate_clp_bundle_or_raise(artifacts, project_dir=project_dir)
    except CLPValidationError as exc:
        raise CheckpointValidationError(str(exc)) from exc


def _validate_course_and_pup_routing(
    *,
    stage: str,
    status: str,
    artifacts: dict[str, Any],
    pipeline_type: str,
) -> None:
    """Enforce additive course ownership and opt-in PUP capability routing."""

    course_manifest = artifacts.get("course_manifest")
    proposal = artifacts.get("proposal_packet")

    if course_manifest is not None and stage != "proposal":
        raise CheckpointValidationError(
            "course_manifest is only valid at stage 'proposal'; later stages "
            "must consume the approved predecessor without republishing it"
        )

    from lib.pipeline_loader import load_pipeline_readonly

    manifest = load_pipeline_readonly(pipeline_type)
    stage_definition = next(
        (
            item
            for item in manifest.get("stages", [])
            if isinstance(item, dict) and item.get("name") == stage
        ),
        {},
    )
    optional_outputs = set(stage_definition.get("optional_produces") or [])
    if course_manifest is not None and "course_manifest" not in optional_outputs:
        raise CheckpointValidationError(
            f"Pipeline {pipeline_type!r} stage {stage!r} does not declare "
            "course_manifest in optional_produces"
        )

    if stage != "proposal" or not isinstance(proposal, dict):
        return

    production_plan = proposal.get("production_plan")
    if not isinstance(production_plan, dict):
        return  # proposal schema validation reports the structural error

    content_form = production_plan.get("content_form")
    lifecycle_complete = status in {"completed", "awaiting_human"}
    if lifecycle_complete and content_form == "course_form" and course_manifest is None:
        raise CheckpointValidationError(
            "content_form='course_form' requires course_manifest in the same "
            "proposal checkpoint"
        )
    if course_manifest is not None and content_form != "course_form":
        raise CheckpointValidationError(
            "course_manifest requires production_plan.content_form='course_form'"
        )

    policy = production_plan.get("production_unit_policy")
    if not isinstance(policy, dict) or policy.get("mode") in {None, "off"}:
        return

    capability = (manifest.get("extensions") or {}).get("production_units")
    if not isinstance(capability, dict) or capability.get("supported") is not True:
        raise CheckpointValidationError(
            f"Pipeline {pipeline_type!r} does not support Production Units"
        )
    enabled_stages = set(policy.get("enabled_stages") or [])
    supported_stages = set(capability.get("supported_stages") or [])
    unsupported = enabled_stages - supported_stages
    if unsupported:
        raise CheckpointValidationError(
            "Production Unit policy requests unsupported stages: "
            f"{sorted(unsupported)}"
        )
    target = policy.get("target_seconds")
    hard_max = policy.get("hard_max_seconds")
    if hard_max is not None and target is not None and hard_max < target:
        raise CheckpointValidationError(
            "production_unit_policy.hard_max_seconds must be >= target_seconds"
        )


def _find_predecessor_checkpoint(
    stage: str,
    project_id: str,
    pipeline_dir: Optional[Path] = None,
    checkpoint: Optional[dict[str, Any]] = None,
    *,
    required: bool = False,
) -> Optional[dict[str, Any]]:
    """Load one exact, validated predecessor from one authoritative root.

    When ``pipeline_dir`` is provided it is the sole root.  Falling through to
    another checkout's global ``projects`` directory would make a source digest
    attest to the wrong project snapshot.  The default root exists only for
    callers that use the canonical production layout.
    """
    root = Path(pipeline_dir).resolve() if pipeline_dir is not None else PROJECTS_DIR.resolve()
    cp_path = _checkpoint_path(root, project_id, stage)
    if not cp_path.exists():
        if required:
            raise CheckpointValidationError(
                f"Required predecessor checkpoint_{stage}.json not found at exact project root: {cp_path}"
            )
        return None

    try:
        with open(cp_path, encoding="utf-8") as handle:
            predecessor = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise CheckpointValidationError(
            f"Required predecessor checkpoint_{stage}.json is unreadable or invalid JSON: {cp_path}: {exc}"
        ) from exc

    expected_pipeline = checkpoint.get("pipeline_type") if isinstance(checkpoint, dict) else None
    return _authenticate_predecessor_checkpoint(
        predecessor,
        stage=stage,
        project_id=project_id,
        expected_pipeline=expected_pipeline,
        pipeline_dir=root,
        source=str(cp_path),
    )


def _authenticate_predecessor_checkpoint(
    predecessor: Any,
    *,
    stage: str,
    project_id: str,
    expected_pipeline: Any,
    pipeline_dir: Optional[Path],
    source: str = "provided predecessor checkpoint",
) -> dict[str, Any]:
    """Authenticate a full predecessor checkpoint before consuming artifacts.

    This deliberately accepts no bare artifact.  Identity, lifecycle state,
    schema, pipeline policy, approval and the predecessor's own provenance are
    all checked as one operation.
    """
    identity_root = Path(pipeline_dir).resolve() if pipeline_dir is not None else PROJECTS_DIR
    _project_directory(identity_root, project_id)
    _validate_stage_component(stage)
    if not isinstance(predecessor, dict):
        raise CheckpointValidationError(f"{source} must contain a JSON object")

    try:
        jsonschema.validate(
            instance=predecessor,
            schema=_load_checkpoint_schema(),
            format_checker=CHECKPOINT_FORMAT_CHECKER,
        )
    except jsonschema.ValidationError as exc:
        raise CheckpointValidationError(
            f"{source} failed checkpoint schema validation: {exc.message}"
        ) from exc
    try:
        _validate_rfc3339_timestamp(predecessor.get("timestamp"), f"{source} timestamp")
    except CheckpointValidationError as exc:
        raise CheckpointValidationError(f"{source} failed checkpoint schema validation: {exc}") from exc

    if predecessor.get("project_id") != project_id:
        raise CheckpointValidationError(
            f"Predecessor project_id mismatch: expected {project_id!r}, got {predecessor.get('project_id')!r}"
        )
    if predecessor.get("stage") != stage:
        raise CheckpointValidationError(
            f"Predecessor stage mismatch: expected {stage!r}, got {predecessor.get('stage')!r}"
        )
    if expected_pipeline in (None, "unknown"):
        raise CheckpointValidationError(
            "Cannot establish exact predecessor provenance without a concrete pipeline_type"
        )
    if predecessor.get("pipeline_type") != expected_pipeline:
        raise CheckpointValidationError(
            f"Predecessor pipeline_type mismatch: expected {expected_pipeline!r}, "
            f"got {predecessor.get('pipeline_type')!r}"
        )
    if predecessor.get("status") != "completed":
        raise CheckpointValidationError(
            f"Required predecessor checkpoint_{stage}.json status must be completed, "
            f"got {predecessor.get('status')!r}"
        )

    # Validate the predecessor's artifact schemas and its own provenance chain
    # before any downstream digest is compared against it.
    validate_checkpoint(predecessor, pipeline_dir=pipeline_dir)

    pipeline_type = predecessor.get("pipeline_type")
    if _stage_requires_approval(pipeline_type, stage) and predecessor.get("human_approved") is not True:
        raise CheckpointValidationError(
            f"Required predecessor checkpoint_{stage}.json was completed without required human approval"
        )

    return predecessor


def verify_gate_resolution(
    checkpoint: dict[str, Any],
    artifacts: Optional[dict[str, Any]] = None,
    predecessor_checkpoint: Optional[dict[str, Any]] = None,
    pipeline_dir: Optional[Path] = None,
) -> tuple[bool, Optional[str]]:
    """Strictly verify zero-entity auto-pass evidence for unapproved checkpoints.

    Returns (is_valid, error_reason).
    Only returns (True, None) for:
      animated-explainer + clp + completed + human_approved=False +
      gate_resolution: mode="zero_entity_auto" + rule_version="clp_literal_empty_v1" +
      entity_counts all 0 + valid manifest_sha256 matching empty manifest + valid resolved_at (RFC3339 with timezone) +
      source_script_sha256 verified against predecessor script.
    """
    if not isinstance(checkpoint, dict):
        return False, "checkpoint must be a dictionary"
    if checkpoint.get("pipeline_type") != "animated-explainer":
        return False, f"pipeline_type {checkpoint.get('pipeline_type')!r} does not allow zero-entity auto-pass"
    if checkpoint.get("stage") != "clp":
        return False, f"stage {checkpoint.get('stage')!r} does not allow zero-entity auto-pass"
    if checkpoint.get("status") != "completed":
        return False, f"status {checkpoint.get('status')!r} is not completed"
    if checkpoint.get("human_approved") is not False:
        return False, "human_approved must be explicitly boolean False"

    arts = artifacts if artifacts is not None else checkpoint.get("artifacts")
    if not isinstance(arts, dict):
        return False, "artifacts must be a dictionary"
    required_artifact_keys = {"clp_manifest", "clp_candidates"}
    if set(arts) != required_artifact_keys:
        return False, (
            "zero-entity auto-pass artifacts must contain exactly "
            f"{sorted(required_artifact_keys)}, got {sorted(map(str, arts))}"
        )

    # Validate the entire current checkpoint envelope, not only hand-picked
    # gate fields.  Backlot may materialize path-backed artifacts, so validate
    # a shallow copy with that exact resolved map substituted.  Private board
    # metadata (for example ``_mtime``) must be removed by the resolver rather
    # than silently ignored here.
    resolved_checkpoint = dict(checkpoint)
    resolved_checkpoint["artifacts"] = arts
    try:
        jsonschema.validate(
            instance=resolved_checkpoint,
            schema=_load_checkpoint_schema(),
            format_checker=CHECKPOINT_FORMAT_CHECKER,
        )
    except jsonschema.ValidationError as exc:
        return False, f"checkpoint failed schema validation: {exc.message}"
    try:
        _validate_rfc3339_timestamp(
            resolved_checkpoint.get("timestamp"), "checkpoint timestamp"
        )
    except CheckpointValidationError as exc:
        return False, f"checkpoint failed schema validation: {exc}"
    if not isinstance(arts["clp_manifest"], dict):
        return False, "artifacts must contain a valid clp_manifest object"
    if not isinstance(arts["clp_candidates"], dict):
        return False, "artifacts must contain a valid clp_candidates object"

    manifest = arts["clp_manifest"]
    candidates = arts["clp_candidates"]
    project_id = checkpoint.get("project_id")
    for artifact_name, artifact in (
        ("clp_manifest", manifest),
        ("clp_candidates", candidates),
    ):
        if artifact.get("project_id") != project_id:
            return False, (
                f"{artifact_name} project_id mismatch: checkpoint has "
                f"{project_id!r}, artifact has {artifact.get('project_id')!r}"
            )
    try:
        project_root = _project_directory(
            Path(pipeline_dir).resolve() if pipeline_dir is not None else PROJECTS_DIR,
            project_id,
        )
        validate_artifact("clp_manifest", manifest, project_dir=project_root)
        validate_artifact("clp_candidates", candidates, project_dir=project_root)
    except Exception as exc:
        return False, f"CLP artifacts failed schema or semantic validation: {exc}"

    has_entities = bool(
        manifest.get("characters")
        or manifest.get("locations")
        or manifest.get("props")
    )
    if has_entities:
        return False, f"stage 'clp' in pipeline {checkpoint.get('pipeline_type')!r} detected non-empty entities in clp_manifest without human approval."

    cands = candidates
    c_dict = cands.get("candidates") or {}
    cand_count = (
        len(c_dict.get("characters") or [])
        + len(c_dict.get("locations") or [])
        + len(c_dict.get("props") or [])
    )
    if cand_count > 0:
        return False, f"stage 'clp' candidates contains {cand_count} extracted entities, but clp_manifest has zero entities without human approval. Auto-bypass rejected when candidates exist."

    cand_script_sha = cands.get("source_script_sha256")
    if not cand_script_sha or not isinstance(cand_script_sha, str) or not re.match(r"^sha256:[0-9a-f]{64}$", cand_script_sha):
        return False, f"clp_candidates has invalid or missing source_script_sha256: {cand_script_sha!r}"

    # An auto-pass is provenance-bearing evidence.  A caller may supply a full
    # predecessor checkpoint (never a bare script artifact), or this verifier
    # resolves the exact checkpoint from the sole authoritative project root.
    pred_cp = predecessor_checkpoint
    if pred_cp is None and checkpoint.get("project_id"):
        try:
            pred_cp = _find_predecessor_checkpoint(
                "script",
                checkpoint["project_id"],
                pipeline_dir=pipeline_dir,
                checkpoint=checkpoint,
                required=True,
            )
        except CheckpointValidationError as exc:
            return False, str(exc)
    elif pred_cp is not None:
        try:
            pred_cp = _authenticate_predecessor_checkpoint(
                pred_cp,
                stage="script",
                project_id=checkpoint.get("project_id"),
                expected_pipeline=checkpoint.get("pipeline_type"),
                pipeline_dir=pipeline_dir,
            )
        except CheckpointValidationError as exc:
            return False, str(exc)

    script_obj = None
    if isinstance(pred_cp, dict) and isinstance(pred_cp.get("artifacts"), dict):
        script_obj = pred_cp["artifacts"].get("script")

    if not isinstance(script_obj, dict):
        return False, "exact predecessor script artifact is required for zero-entity auto-pass"
    try:
        validate_artifact("script", script_obj)
    except Exception as exc:
        return False, f"predecessor script failed artifact validation: {exc}"

    from lib.clp_validator import canonical_digest
    expected_script_hash = canonical_digest(script_obj)
    if cand_script_sha != expected_script_hash:
        return False, (
            "source_script_sha256 mismatch with predecessor script "
            f"(expected {expected_script_hash}, got {cand_script_sha})"
        )

    gate_res = checkpoint.get("gate_resolution")
    if not isinstance(gate_res, dict):
        return False, "gate_resolution is missing or not a dictionary"
    required_gate_keys = {"mode", "rule_version", "entity_counts", "manifest_sha256", "resolved_at"}
    if set(gate_res) != required_gate_keys:
        return False, (
            "gate_resolution must contain exactly "
            f"{sorted(required_gate_keys)}, got {sorted(gate_res)}"
        )

    if gate_res.get("mode") != "zero_entity_auto":
        return False, f"invalid gate_resolution mode: {gate_res.get('mode')!r}"
    if gate_res.get("rule_version") != "clp_literal_empty_v1":
        return False, f"invalid rule_version: {gate_res.get('rule_version')!r}"

    counts = gate_res.get("entity_counts")
    if (
        not isinstance(counts, dict)
        or set(counts) != {"characters", "locations", "props"}
        or any(type(counts.get(key)) is not int or counts.get(key) != 0 for key in ("characters", "locations", "props"))
    ):
        return False, f"entity_counts must all be 0, got: {counts}"

    manifest_hash = gate_res.get("manifest_sha256")
    if not manifest_hash or not isinstance(manifest_hash, str) or not re.match(r"^sha256:[0-9a-f]{64}$", manifest_hash):
        return False, f"invalid or missing manifest_sha256: {manifest_hash!r}"

    exp_m_hash = canonical_digest(manifest)
    if manifest_hash != exp_m_hash:
        return False, f"manifest_sha256 mismatch (expected {exp_m_hash}, got {manifest_hash})"

    resolved_at = gate_res.get("resolved_at")
    if not resolved_at or not isinstance(resolved_at, str):
        return False, "missing resolved_at"

    try:
        _validate_rfc3339_timestamp(resolved_at, "resolved_at")
    except CheckpointValidationError as exc:
        return False, str(exc)

    return True, None


def validate_checkpoint(
    checkpoint: dict[str, Any],
    pipeline_dir: Optional[Path] = None,
) -> None:
    """Validate checkpoint structure and canonical artifact payloads.

    Resolves the valid stage list from one concrete pipeline manifest.
    Missing, literal ``unknown``, or unloadable pipeline types fail closed.
    """
    if not isinstance(checkpoint, dict):
        raise CheckpointValidationError("Checkpoint must be a JSON object")

    stage = checkpoint.get("stage")
    status = checkpoint.get("status")
    artifacts = checkpoint.get("artifacts")
    pipeline_type = checkpoint.get("pipeline_type")
    project_id = checkpoint.get("project_id")

    projects_root = Path(pipeline_dir).resolve() if pipeline_dir is not None else PROJECTS_DIR
    proj_dir = _project_directory(projects_root, project_id)

    if pipeline_type in (None, "unknown"):
        raise CheckpointValidationError(
            "Checkpoint validation requires a concrete, schema-valid pipeline_type; "
            f"got {pipeline_type!r}"
        )
    _authenticate_project_marker(
        proj_dir,
        project_id=project_id,
        pipeline_type=pipeline_type,
    )
    valid_stages = set(get_pipeline_stages(pipeline_type))

    if not isinstance(stage, str) or stage not in valid_stages:
        raise CheckpointValidationError(
            f"Invalid stage: {stage!r} for pipeline {pipeline_type!r}. "
            f"Valid stages: {sorted(valid_stages)}"
        )
    if not isinstance(status, str):
        raise CheckpointValidationError(f"Invalid status: {status!r}")
    if not isinstance(artifacts, dict):
        raise CheckpointValidationError("Checkpoint artifacts must be a dictionary")

    # Verify project_id matches across checkpoint and artifacts
    if project_id and isinstance(artifacts, dict):
        for art_name, art_data in artifacts.items():
            if isinstance(art_data, dict) and art_data.get("project_id"):
                if art_data["project_id"] != project_id:
                    raise CheckpointValidationError(
                        f"Project ID mismatch: checkpoint has {project_id!r}, "
                        f"but artifact {art_name!r} has {art_data['project_id']!r}"
                    )

    lifecycle_complete = status in {"completed", "awaiting_human"}
    known_pipeline = bool(pipeline_type and pipeline_type != "unknown")

    # CLP sidecars have one producer stage.  Permitting them elsewhere lets a
    # malformed checkpoint trigger self-predecessor recursion or smuggle a
    # second authority into the provenance chain.  scene_plan may carry only
    # an identical clp_manifest cache, checked below against checkpoint_clp.
    if "clp_candidates" in artifacts and stage != "clp":
        raise CheckpointValidationError("clp_candidates is only valid at stage 'clp'")
    if "clp_shot_bindings" in artifacts and stage != "scene_plan":
        raise CheckpointValidationError(
            "clp_shot_bindings is only valid at stage 'scene_plan'"
        )
    if "clp_manifest" in artifacts and stage not in {"clp", "scene_plan"}:
        raise CheckpointValidationError(
            "clp_manifest is only valid at stages 'clp' and 'scene_plan'"
        )
    if "course_manifest" in artifacts and stage != "proposal":
        raise CheckpointValidationError(
            "course_manifest is only valid at stage 'proposal'"
        )

    # Re-enforce every approval gate on reads as well as writes.  Otherwise a
    # hand-edited/legacy checkpoint could mark a manifest-gated stage completed
    # without approval, and a caller-set human_approval_required=True could be
    # silently ignored.  CLP's typed zero-entity exception is handled directly
    # below and is the only non-human completion path.
    manifest_gate = _stage_requires_approval(pipeline_type, stage)
    checkpoint_gate = checkpoint.get("human_approval_required") is True
    if (
        stage != "clp"
        and status == "completed"
        and (bool(manifest_gate) or checkpoint_gate)
        and checkpoint.get("human_approved") is not True
    ):
            raise CheckpointValidationError(
                f"GATE VIOLATION: completed stage {stage!r} requires "
                "human approval (human_approved=True)"
            )

    # Hard Gate Check for CLP: If unapproved, verify gate_resolution.  The
    # verifier resolves and authenticates the exact predecessor script before
    # accepting zero-entity evidence.
    if stage == "clp" and status == "completed" and checkpoint.get("human_approved") is not True:
        is_valid, reason = verify_gate_resolution(checkpoint, artifacts, pipeline_dir=pipeline_dir)
        if not is_valid:
            raise CheckpointValidationError(f"GATE VIOLATION: {reason}")

    # Bind clp_candidates to the one exact, completed predecessor script.  A
    # missing predecessor is an integrity failure, not permission to skip the
    # comparison.  Legacy checkpoints without a declared pipeline remain
    # readable, but a completed checkpoint on a known pipeline cannot bypass.
    if (
        stage == "clp"
        and lifecycle_complete
        and known_pipeline
        and "clp_candidates" in artifacts
    ):
        cands = artifacts["clp_candidates"]
        if not isinstance(cands, dict):
            raise CheckpointValidationError("clp_candidates must be a JSON object")
        cand_script_sha = cands.get("source_script_sha256")
        pred_script_cp = _find_predecessor_checkpoint(
            "script",
            project_id,
            pipeline_dir=pipeline_dir,
            checkpoint=checkpoint,
            required=True,
        )
        pred_script = (pred_script_cp.get("artifacts") or {}).get("script") if pred_script_cp else None
        if not isinstance(pred_script, dict):
            raise CheckpointValidationError(
                "Exact predecessor checkpoint_script.json does not contain a script artifact"
            )
        from lib.clp_validator import canonical_digest
        expected_script_hash = canonical_digest(pred_script)
        if cand_script_sha != expected_script_hash:
            raise CheckpointValidationError(
                "clp_candidates source_script_sha256 mismatch with predecessor checkpoint_script.json "
                f"(expected {expected_script_hash}, got {cand_script_sha})"
            )

    # Predecessor resolution for clp_shot_bindings (e.g. stage 'scene_plan')
    if stage == "scene_plan" and "clp_shot_bindings" in artifacts:
        bindings = artifacts["clp_shot_bindings"]
        local_manifest = artifacts.get("clp_manifest")
        pred_manifest = None
        pred_clp_cp = None

        if lifecycle_complete and known_pipeline:
            pred_clp_cp = _find_predecessor_checkpoint(
                "clp",
                project_id,
                pipeline_dir=pipeline_dir,
                checkpoint=checkpoint,
                required=True,
            )
            if isinstance(pred_clp_cp.get("artifacts"), dict):
                pred_manifest = pred_clp_cp["artifacts"].get("clp_manifest")
            if not isinstance(pred_manifest, dict):
                raise CheckpointValidationError(
                    "Exact predecessor checkpoint_clp.json does not contain a clp_manifest artifact"
                )

        # Anti-Shadowing: If local manifest is provided, verify it does not shadow/override approved predecessor
        if local_manifest and pred_manifest:
            from lib.clp_validator import canonical_digest
            if canonical_digest(local_manifest) != canonical_digest(pred_manifest):
                raise CheckpointValidationError(
                    "Local clp_manifest shadows approved predecessor checkpoint_clp.json with different content"
                )

        # Completed known-pipeline stages may validate only against the exact
        # predecessor.  A local copy is permitted solely as an identical cache.
        manifest = pred_manifest if lifecycle_complete and known_pipeline else (pred_manifest or local_manifest)

        has_refs = False
        if isinstance(bindings, dict):
            for b in bindings.get("bindings", []):
                if isinstance(b, dict) and (
                    b.get("character_refs") or b.get("location_ref") or b.get("prop_refs")
                ):
                    has_refs = True
                    break
            if bindings.get("clp_manifest_sha256"):
                has_refs = True

        if not manifest and has_refs:
            raise CheckpointValidationError(
                "Cannot validate clp_shot_bindings: predecessor clp_manifest not found in "
                "current artifacts or predecessor checkpoint."
            )

        if manifest:
            from lib.clp_validator import validate_clp_shot_bindings_or_raise, CLPValidationError
            try:
                validate_clp_shot_bindings_or_raise(
                    bindings,
                    manifest=manifest,
                    scene_plan=artifacts.get("scene_plan"),
                )
            except CLPValidationError as exc:
                raise CheckpointValidationError(str(exc)) from exc

    _validate_artifacts_for_stage(
        stage,
        status,
        artifacts,
        pipeline_type=pipeline_type,
        project_dir=proj_dir,
    )
    _validate_course_and_pup_routing(
        stage=stage,
        status=status,
        artifacts=artifacts,
        pipeline_type=pipeline_type,
    )

    try:
        jsonschema.validate(
            instance=checkpoint,
            schema=_load_checkpoint_schema(),
            format_checker=CHECKPOINT_FORMAT_CHECKER,
        )
    except jsonschema.ValidationError as exc:
        raise CheckpointValidationError(f"Checkpoint failed schema validation: {exc.message}") from exc
    _validate_rfc3339_timestamp(checkpoint.get("timestamp"), "checkpoint timestamp")

    # Optional M6.0B provenance is additive for ordinary/legacy checkpoints,
    # but when present it must authenticate against the exact durable handoff
    # records on both write and read. Import lazily to avoid coupling the base
    # checkpoint module to the opt-in Production Unit package at import time.
    pup_metadata = (checkpoint.get("metadata") or {}).get("production_units")
    if isinstance(pup_metadata, dict) and "candidate_handoff" in pup_metadata:
        try:
            from lib.production_units.handoff import (
                ProductionUnitHandoffError,
                validate_checkpoint_handoff_provenance,
            )

            validate_checkpoint_handoff_provenance(
                checkpoint,
                projects_root=projects_root,
            )
        except ProductionUnitHandoffError as exc:
            raise CheckpointValidationError(
                f"Production Unit checkpoint provenance failed validation: {exc}"
            ) from exc


def _checkpoint_path(pipeline_dir: Path, project_id: str, stage: str) -> Path:
    safe_stage = _validate_stage_component(stage)
    project_dir = _project_directory(pipeline_dir, project_id)
    return _contained_project_path(project_dir, f"checkpoint_{safe_stage}.json")


def init_project(
    project_id: str,
    *,
    title: str,
    pipeline_type: str,
    pipeline_dir: Optional[Path] = None,
    style_playbook: Optional[str] = None,
) -> Path:
    """Initialize a project workspace with the canonical layout + marker file.

    Creates projects/<project_id>/ with the standard subdirectories and writes
    project.json — the marker the Backlot board uses to render a project's
    identity and stage rail before the first checkpoint exists.

    Idempotent: re-running preserves the original created_at and merges fields.
    Returns the project directory.
    """
    base = pipeline_dir or PROJECTS_DIR
    project_dir = _project_directory(base, project_id)
    if not isinstance(pipeline_type, str) or pipeline_type == "unknown":
        raise CheckpointValidationError(
            f"New projects require a concrete pipeline_type, got {pipeline_type!r}"
        )
    # Resolve the exact catalog entry before creating any directory or marker.
    get_pipeline_stages(pipeline_type)
    _validate_style_playbook(style_playbook)
    marker_path = _contained_project_path(project_dir, PROJECT_MARKER_FILENAME)
    marker: dict[str, Any] = {}
    if marker_path.exists():
        try:
            with open(marker_path, encoding="utf-8") as f:
                marker = json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            raise CheckpointValidationError(
                f"Existing project marker is corrupt: {marker_path}: {exc}"
            ) from exc
        if not isinstance(marker, dict):
            raise CheckpointValidationError(
                f"Existing project marker must be a JSON object: {marker_path}"
            )
        if marker.get("project_id") != project_id:
            raise CheckpointValidationError(
                f"Existing project marker identity mismatch: expected {project_id!r}, "
                f"got {marker.get('project_id')!r}"
            )
        if marker.get("pipeline_type") != pipeline_type:
            raise CheckpointValidationError(
                f"Existing project marker pipeline_type mismatch: expected {pipeline_type!r}, "
                f"got {marker.get('pipeline_type')!r}"
            )

    for sub in (
        "artifacts",
        "assets/images",
        "assets/video",
        "assets/audio",
        "assets/music",
        "renders",
    ):
        _contained_project_path(project_dir, sub).mkdir(parents=True, exist_ok=True)

    marker.setdefault("version", "1.0")
    marker.setdefault("created_at", datetime.now(timezone.utc).isoformat())
    marker["project_id"] = project_id
    marker["title"] = title
    marker["pipeline_type"] = pipeline_type
    if style_playbook is not None:
        marker["style_playbook"] = style_playbook

    with open(marker_path, "w", encoding="utf-8") as f:
        json.dump(marker, f, indent=2)

    return project_dir


def _stage_requires_approval(pipeline_type: Optional[str], stage: str) -> Optional[bool]:
    """Read human_approval_default for a stage from its pipeline manifest.

    Returns None only when no pipeline_type was given by a legacy caller.

    Every provided but unknown or corrupt pipeline_type raises: a typo must
    not silently disable gate enforcement (fail-closed, not fail-open).
    """
    if pipeline_type is None:
        return None
    if pipeline_type == "unknown":
        raise CheckpointValidationError(
            "Unknown pipeline_type 'unknown' cannot resolve gate policy"
        )
    from lib.pipeline_loader import get_stage_human_approval_default, load_pipeline_readonly
    try:
        manifest = load_pipeline_readonly(pipeline_type)
    except FileNotFoundError:
        raise CheckpointValidationError(
            f"Unknown pipeline_type {pipeline_type!r} — cannot resolve gate "
            f"policy for stage {stage!r}. Check the spelling against "
            f"pipeline_defs/*.yaml."
        )
    except Exception as exc:
        raise CheckpointValidationError(
            f"Invalid pipeline_type {pipeline_type!r} — cannot resolve gate policy: {exc}"
        ) from exc
    return get_stage_human_approval_default(manifest, stage)


def _enforce_stage_prerequisites(
    pipeline_dir: Path,
    project_id: str,
    pipeline_type: str | None,
    stage: str,
    status: str,
) -> None:
    """Require completed, approved predecessors before advancing a stage.

    ``in_progress`` and failure heartbeats remain writable so an operator can
    inspect or resume a broken run. Only lifecycle advancement
    (``awaiting_human``/``completed``) is gated.
    """

    if status not in {"awaiting_human", "completed"}:
        return
    if pipeline_type is None:
        return
    if pipeline_type == "unknown":
        raise CheckpointValidationError(
            "Unknown pipeline_type 'unknown' cannot enforce stage prerequisites"
        )

    stages = get_pipeline_stages(pipeline_type)
    if stage not in stages:
        return

    try:
        from lib.pipeline_loader import load_pipeline_readonly

        pipeline_manifest = load_pipeline_readonly(pipeline_type)
    except Exception as exc:
        raise CheckpointValidationError(
            f"Cannot enforce prerequisites for pipeline {pipeline_type!r}: {exc}"
        ) from exc
    stage_definitions = {
        item.get("name"): item
        for item in pipeline_manifest.get("stages", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }

    incomplete: list[str] = []
    unapproved: list[str] = []
    predecessor_artifacts: set[str] = set()
    for predecessor in stages[: stages.index(stage)]:
        path = _checkpoint_path(pipeline_dir, project_id, predecessor)
        if not path.exists():
            predecessor_def = stage_definitions.get(predecessor, {})
            if predecessor_def.get("checkpoint_required", True) is not False:
                incomplete.append(predecessor)
            continue
        try:
            with open(path, encoding="utf-8") as handle:
                checkpoint = json.load(handle)
        except (OSError, json.JSONDecodeError):
            incomplete.append(predecessor)
            continue
        if not isinstance(checkpoint, dict):
            incomplete.append(predecessor)
            continue
        if (
            checkpoint.get("project_id") != project_id
            or checkpoint.get("pipeline_type") != pipeline_type
            or checkpoint.get("stage") != predecessor
        ):
            incomplete.append(predecessor)
            continue
        if checkpoint.get("status") != "completed":
            incomplete.append(predecessor)
            continue
        if (
            _stage_requires_approval(pipeline_type, predecessor)
            and checkpoint.get("human_approved") is not True
        ):
            unapproved.append(predecessor)
            continue
        try:
            validate_checkpoint(checkpoint, pipeline_dir=pipeline_dir)
        except CheckpointValidationError:
            incomplete.append(predecessor)
            continue
        predecessor_artifacts.update((checkpoint.get("artifacts") or {}).keys())

    if incomplete or unapproved:
        details = []
        if incomplete:
            details.append(f"incomplete or missing: {incomplete}")
        if unapproved:
            details.append(f"completed without required approval: {unapproved}")
        raise CheckpointValidationError(
            f"PREREQUISITE VIOLATION: stage {stage!r} cannot advance; "
            + "; ".join(details)
            + f". Pipeline order: {stages}."
        )

    # Enforce required_artifacts_in DAG contract
    try:
        for st in pipeline_manifest.get("stages", []):
            if st.get("name") == stage and "required_artifacts_in" in st:
                for req in st["required_artifacts_in"]:
                    if req not in predecessor_artifacts:
                        raise CheckpointValidationError(
                            f"PREREQUISITE VIOLATION: stage {stage!r} in pipeline {pipeline_type!r} "
                            f"requires artifact {req!r} from predecessor checkpoints, but it was not found."
                        )
    except CheckpointValidationError:
        raise
    except Exception as exc:
        raise CheckpointValidationError(
            f"Cannot enforce prerequisite artifact contract for pipeline {pipeline_type!r}: {exc}"
        ) from exc


def _archive_superseded_checkpoint(path: Path, stage: str) -> None:
    """Copy an existing checkpoint into history/ before it is overwritten.

    Preserves the full run record: stage re-runs (script v1 → v2) and gate
    transitions (awaiting_human → completed) remain reconstructable. Repeated
    in_progress refreshes are NOT archived — they are partial-progress
    heartbeats, not versions.

    Archiving is best-effort and must never crash a checkpoint write: the
    Backlot watcher may hold the file open (Windows denies renames of open
    files), so we copy rather than move, and swallow archival I/O failures.
    """
    if not path.exists():
        return
    try:
        with open(path, encoding="utf-8") as f:
            existing = json.load(f)
    except (json.JSONDecodeError, OSError):
        existing = {}
    if existing.get("status") == "in_progress":
        return

    try:
        import shutil
        stamp = str(existing.get("timestamp", ""))
        safe_stamp = "".join(c for c in stamp if c.isalnum()) or f"{path.stat().st_mtime_ns}"
        history_dir = _contained_project_path(path.parent, HISTORY_DIRNAME)
        history_dir.mkdir(parents=True, exist_ok=True)
        target = _contained_project_path(
            history_dir, f"checkpoint_{stage}_{safe_stamp}.json"
        )
        if target.exists():
            target = _contained_project_path(
                history_dir,
                f"checkpoint_{stage}_{safe_stamp}_{path.stat().st_mtime_ns}.json",
            )
        shutil.copyfile(path, target)
    except OSError:
        import logging
        logging.getLogger(__name__).warning(
            "Could not archive superseded checkpoint %s to history/", path
        )


def _decision_log_path(pipeline_dir: Path, project_id: str) -> Path:
    project_dir = _project_directory(pipeline_dir, project_id)
    return _contained_project_path(project_dir, "decision_log.json")


def _merge_decision_log(
    pipeline_dir: Path, project_id: str, new_log: dict[str, Any]
) -> None:
    """Append new decisions to the project-level decision log.

    Each stage may produce decisions. This function merges them into a
    single cumulative file so reviewers and the bench can inspect the
    full audit trail.
    """
    path = _decision_log_path(pipeline_dir, project_id)
    if path.exists():
        with open(path, encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = {
            "version": "1.0",
            "project_id": project_id,
            "decisions": [],
        }

    existing_ids = {d["decision_id"] for d in existing.get("decisions", [])}
    for decision in new_log.get("decisions", []):
        if decision.get("decision_id") not in existing_ids:
            existing["decisions"].append(decision)

    # Serialize before touching disk and publish via one local atomic replace.
    serialized = json.dumps(existing, indent=2, allow_nan=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = _contained_project_path(path.parent, f"{path.name}.tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(serialized)
    import os

    os.replace(tmp_path, path)


def _candidate_handoff_provenance(checkpoint: dict[str, Any] | None) -> Any:
    if not isinstance(checkpoint, dict):
        return None
    metadata = checkpoint.get("metadata")
    if not isinstance(metadata, dict):
        return None
    production_units = metadata.get("production_units")
    if not isinstance(production_units, dict):
        return None
    return production_units.get("candidate_handoff")


def _enforce_pup_human_gate_transition(
    current: dict[str, Any] | None,
    candidate: dict[str, Any],
) -> None:
    """Keep an existing PUP candidate exact across the original Human Gate."""

    current_provenance = _candidate_handoff_provenance(current)
    candidate_provenance = _candidate_handoff_provenance(candidate)
    is_human_completion = (
        candidate.get("status") == "completed"
        and candidate.get("human_approved") is True
    )
    if not is_human_completion:
        return
    if candidate_provenance is not None and current_provenance is None:
        raise CheckpointValidationError(
            "PUP HUMAN GATE VIOLATION: completed candidate provenance requires "
            "a matching durable awaiting_human checkpoint"
        )
    if current_provenance is None:
        return
    if (
        current.get("status") != "awaiting_human"
        or current.get("human_approved") is not False
        or current.get("human_approval_required") is not True
    ):
        raise CheckpointValidationError(
            "PUP HUMAN GATE VIOLATION: approval must transition the matching "
            "awaiting_human checkpoint"
        )
    if candidate_provenance != current_provenance:
        raise CheckpointValidationError(
            "PUP HUMAN GATE VIOLATION: candidate_handoff provenance must be "
            "preserved exactly"
        )
    if candidate.get("artifacts") != current.get("artifacts"):
        raise CheckpointValidationError(
            "PUP HUMAN GATE VIOLATION: approved artifacts must exactly match "
            "the awaiting_human candidate"
        )


@_serialize_checkpoint_write
def write_checkpoint(
    pipeline_dir: Path,
    project_id: str,
    stage: str,
    status: str,
    artifacts: dict[str, Any],
    *,
    pipeline_type: Optional[str] = None,
    style_playbook: Optional[str] = None,
    checkpoint_policy: str = "guided",
    human_approval_required: bool = False,
    human_approved: bool = False,
    review: Optional[dict] = None,
    cost_snapshot: Optional[dict] = None,
    error: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> Path:
    """Write a checkpoint file for a pipeline stage."""
    # Backfill identity fields from the project marker so omitted kwargs
    # cannot bypass either gate enforcement or style validation.
    lifecycle_advancing = status in {"completed", "awaiting_human"}
    marker = None
    project_dir = _project_directory(pipeline_dir, project_id)
    marker_path = _contained_project_path(project_dir, PROJECT_MARKER_FILENAME)
    if marker_path.exists():
        try:
            with open(marker_path, encoding="utf-8") as f:
                marker = json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            if lifecycle_advancing:
                raise CheckpointValidationError(
                    f"Cannot advance lifecycle with corrupt project marker {marker_path}: {exc}"
                ) from exc
            marker = None
        if marker is not None and not isinstance(marker, dict):
            if lifecycle_advancing:
                raise CheckpointValidationError(
                    f"Cannot advance lifecycle: project marker {marker_path} must be a JSON object"
                )
            marker = None
    if isinstance(marker, dict):
        marker_project_id = marker.get("project_id")
        marker_pipeline_type = marker.get("pipeline_type")
        if marker_project_id != project_id:
            raise CheckpointValidationError(
                f"Project marker identity mismatch: directory/write uses {project_id!r}, "
                f"marker has {marker_project_id!r}"
            )
        if lifecycle_advancing and not isinstance(marker_pipeline_type, str):
            raise CheckpointValidationError(
                "Cannot advance lifecycle: project marker has no concrete pipeline_type"
            )
        if pipeline_type is None:
            pipeline_type = marker_pipeline_type
        elif marker_pipeline_type is not None and pipeline_type != marker_pipeline_type:
            raise CheckpointValidationError(
                f"Project marker pipeline_type mismatch: caller uses {pipeline_type!r}, "
                f"marker has {marker_pipeline_type!r}"
            )
        marker_style = marker.get("style_playbook")
        if style_playbook is None and marker_style:
            style_playbook = marker_style
        elif style_playbook is not None and marker_style and style_playbook != marker_style:
            raise CheckpointValidationError(
                f"Project marker style_playbook mismatch: caller uses {style_playbook!r}, "
                f"marker has {marker_style!r}"
            )
    _validate_style_playbook(style_playbook)

    if pipeline_type is None:
        raise CheckpointValidationError(
            "Checkpoint writes require an explicit, schema-valid pipeline_type"
        )

    valid_stages = (
        set(get_pipeline_stages(pipeline_type))
        if pipeline_type is not None
        else ALL_KNOWN_STAGES
    )
    if stage not in valid_stages:
        raise CheckpointValidationError(
            f"Invalid stage: {stage!r} for pipeline {pipeline_type!r}. "
            f"Valid stages: {sorted(valid_stages)}"
        )

    # --- Gate enforcement (GI-4) ---
    # The pipeline manifest is the binding source of truth for whether a stage
    # gates on human approval; a caller may gate MORE strictly (e.g. a
    # manual_all checkpoint policy) but never less. A gated stage can only be
    # written "completed" with explicit evidence of approval
    # (human_approved=True). Skipping a gate is a hard error.
    #
    # The same gate contract is revalidated by validate_checkpoint on every
    # read, so a hand-edited or legacy envelope cannot bypass this write guard.
    manifest_gate = _stage_requires_approval(pipeline_type, stage)
    gated = bool(manifest_gate) or human_approval_required
    if gated:
        human_approval_required = True
        if status == "completed" and not human_approved:
            gate_source = (
                f"human_approval_default: true in the {pipeline_type!r} manifest"
                if manifest_gate
                else "human_approval_required=True was passed by the caller"
            )
            raise CheckpointValidationError(
                f"GATE VIOLATION: stage {stage!r} requires human approval "
                f"({gate_source}) but status='completed' was written without "
                f"human_approved=True. Correct protocol: write "
                f"status='awaiting_human', present the artifact summary to the "
                f"user, END YOUR TURN, and only after the user approves "
                f"re-write with status='completed', human_approved=True."
            )

    # Hard Gate Check for CLP: If clp_manifest contains non-empty entities,
    # human approval is mandatory even if pipeline default was false (e.g. explainer).
    if stage == "clp" and status == "completed" and not human_approved:
        if pipeline_type != "animated-explainer":
            raise CheckpointValidationError(
                f"GATE VIOLATION: stage 'clp' in pipeline {pipeline_type!r} requires human approval. "
                f"Zero-entity auto-pass is strictly reserved for 'animated-explainer'."
            )
        clp_manifest = (artifacts or {}).get("clp_manifest") or {}
        has_entities = bool(
            clp_manifest.get("characters")
            or clp_manifest.get("locations")
            or clp_manifest.get("props")
        )
        if has_entities:
            raise CheckpointValidationError(
                f"GATE VIOLATION: stage 'clp' in pipeline {pipeline_type!r} detected "
                f"non-empty entities in clp_manifest. Human approval is mandatory when entities exist."
            )
        # Verify candidate consistency: cannot auto-pass zero entities if candidates extracted entities
        clp_candidates = (artifacts or {}).get("clp_candidates") or {}
        cands = clp_candidates.get("candidates") or {}
        cand_count = (
            len(cands.get("characters") or [])
            + len(cands.get("locations") or [])
            + len(cands.get("props") or [])
        )
        if cand_count > 0:
            raise CheckpointValidationError(
                f"GATE VIOLATION: stage 'clp' candidates contains {cand_count} extracted entities, "
                f"but clp_manifest has zero entities without human approval. Auto-bypass rejected when candidates exist."
            )

    _enforce_stage_prerequisites(
        pipeline_dir,
        project_id,
        pipeline_type,
        stage,
        status,
    )

    # Never mutate caller-owned artifact dictionaries while preparing durable
    # state.  In particular, decision-log references are injected only into
    # this private candidate envelope.
    checkpoint_artifacts = deepcopy(artifacts)
    checkpoint = {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": pipeline_type or "unknown",
        "stage": stage,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checkpoint_policy": checkpoint_policy,
        "human_approval_required": human_approval_required,
        "human_approved": human_approved,
        "artifacts": checkpoint_artifacts,
    }
    if style_playbook is not None:
        checkpoint["style_playbook"] = style_playbook
    if review is not None:
        checkpoint["review"] = review
    if cost_snapshot is not None:
        checkpoint["cost_snapshot"] = cost_snapshot
    if error is not None:
        checkpoint["error"] = error
    if metadata is not None:
        checkpoint["metadata"] = metadata

    if stage == "clp" and status == "completed" and not human_approved:
        from lib.clp_validator import canonical_digest
        clp_manifest = checkpoint_artifacts.get("clp_manifest") or {}
        checkpoint["gate_resolution"] = {
            "mode": "zero_entity_auto",
            "rule_version": "clp_literal_empty_v1",
            "entity_counts": {"characters": 0, "locations": 0, "props": 0},
            "manifest_sha256": canonical_digest(clp_manifest),
            "resolved_at": datetime.now(timezone.utc).isoformat(),
        }

    current_checkpoint = read_checkpoint(pipeline_dir, project_id, stage)
    _enforce_pup_human_gate_transition(current_checkpoint, checkpoint)

    # Prepare decision-log references in the private candidate first.  No
    # durable audit state may change until the complete checkpoint validates.
    decision_log = checkpoint_artifacts.get("decision_log")
    if isinstance(decision_log, dict):
        log_ref = str(_decision_log_path(pipeline_dir, project_id))

        # Write decision_log_ref into proposal_packet and render_report
        # artifacts if they are present in this checkpoint.
        for artifact_key in ("proposal_packet", "render_report"):
            if artifact_key in checkpoint_artifacts and isinstance(
                checkpoint_artifacts[artifact_key], dict
            ):
                plan_or_top = checkpoint_artifacts[artifact_key]
                # proposal_packet stores it under production_plan
                if artifact_key == "proposal_packet":
                    plan = plan_or_top.get("production_plan")
                    if isinstance(plan, dict):
                        plan["decision_log_ref"] = log_ref
                else:
                    plan_or_top["decision_log_ref"] = log_ref

    validate_checkpoint(checkpoint, pipeline_dir=pipeline_dir)

    # jsonschema permits arbitrary JSON-shaped metadata.  Prove the entire
    # candidate is actually serializable before any ancillary file is changed.
    serialized_checkpoint = json.dumps(checkpoint, indent=2, allow_nan=False)

    # Validation is the commit barrier for ancillary durable state.  An invalid
    # checkpoint can no longer alter decision_log.json or its caller's objects.
    if isinstance(decision_log, dict):
        _merge_decision_log(pipeline_dir, project_id, decision_log)

    path = _checkpoint_path(pipeline_dir, project_id, stage)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Serialize to a temp file first so a mid-write failure (disk full,
    # unserializable metadata) can never leave the stage with a truncated
    # current checkpoint; then archive the superseded file and swap in the
    # new one atomically.
    tmp_path = _contained_project_path(path.parent, f"{path.name}.tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(serialized_checkpoint)
    # Preserve run history: a superseded completed/awaiting_human checkpoint
    # is copied to history/ (stage versioning, gate audit trail, replay).
    _archive_superseded_checkpoint(path, stage)
    import os
    os.replace(tmp_path, path)

    # Automatic non-blocking GCS sync for media stages (shot videos, audio, images, renders)
    suppress_legacy_sync = False
    try:
        from lib.batch_executor.side_effects import hidden_writers_suppressed

        suppress_legacy_sync = hidden_writers_suppressed()
    except ImportError:
        pass
    if (
        not suppress_legacy_sync
        and stage in {"assets", "edit", "compose"}
        and status in {"completed", "awaiting_human"}
    ):
        try:
            from lib.gcs_storage import gcs_storage
            if gcs_storage.is_auto_sync_enabled():
                gcs_storage.async_sync_project_assets(project_dir)
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug("GCS auto-sync skip: %s", e)

    return path


def read_checkpoint(
    pipeline_dir: Path, project_id: str, stage: str
) -> Optional[dict[str, Any]]:
    """Read a checkpoint file. Returns None if not found."""
    path = _checkpoint_path(pipeline_dir, project_id, stage)
    if not path.exists():
        return None
    try:
        with open(path, encoding="utf-8") as f:
            checkpoint = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise CheckpointValidationError(
            f"Cannot read checkpoint {path}: {exc}"
        ) from exc
    if not isinstance(checkpoint, dict):
        raise CheckpointValidationError(
            f"Checkpoint {path} must contain a JSON object"
        )
    if checkpoint.get("project_id") != project_id or checkpoint.get("stage") != stage:
        raise CheckpointValidationError(
            f"Checkpoint path identity mismatch at {path}: expected "
            f"project_id={project_id!r}, stage={stage!r}; got "
            f"project_id={checkpoint.get('project_id')!r}, "
            f"stage={checkpoint.get('stage')!r}"
        )
    validate_checkpoint(checkpoint, pipeline_dir=pipeline_dir)
    return checkpoint


def get_latest_checkpoint(
    pipeline_dir: Path, project_id: str
) -> Optional[dict[str, Any]]:
    """Find the most recent checkpoint for a project (by file mtime)."""
    project_dir = _project_directory(pipeline_dir, project_id)
    if not project_dir.exists():
        return None

    checkpoints: list[Path] = []
    for candidate in project_dir.glob("checkpoint_*.json"):
        stage_name = candidate.stem[len("checkpoint_"):]
        _validate_stage_component(stage_name)
        checkpoints.append(_contained_project_path(project_dir, candidate.name))
    checkpoints.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    if not checkpoints:
        return None

    try:
        with open(checkpoints[0], encoding="utf-8") as f:
            checkpoint = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise CheckpointValidationError(
            f"Cannot read checkpoint {checkpoints[0]}: {exc}"
        ) from exc
    if not isinstance(checkpoint, dict):
        raise CheckpointValidationError(
            f"Checkpoint {checkpoints[0]} must contain a JSON object"
        )
    selected_stage = checkpoints[0].stem[len("checkpoint_"):]
    if (
        checkpoint.get("project_id") != project_id
        or checkpoint.get("stage") != selected_stage
    ):
        raise CheckpointValidationError(
            f"Checkpoint path identity mismatch at {checkpoints[0]}: expected "
            f"project_id={project_id!r}, stage={selected_stage!r}; got "
            f"project_id={checkpoint.get('project_id')!r}, "
            f"stage={checkpoint.get('stage')!r}"
        )
    validate_checkpoint(checkpoint, pipeline_dir=pipeline_dir)
    return checkpoint


def get_completed_stages(
    pipeline_dir: Path, project_id: str, pipeline_type: str | None = None
) -> list[str]:
    """Return list of stages that have a completed checkpoint.

    When pipeline_type is provided, only checks stages defined in that
    pipeline's manifest — preventing false positives from leftover
    checkpoints of a different pipeline type.
    """
    if pipeline_type is None:
        latest = get_latest_checkpoint(pipeline_dir, project_id)
        if latest is not None:
            pipeline_type = latest.get("pipeline_type")
    stages_to_check = get_pipeline_stages(pipeline_type)
    completed = []
    for stage in stages_to_check:
        cp = read_checkpoint(pipeline_dir, project_id, stage)
        if (
            cp is not None
            and pipeline_type is not None
            and cp.get("pipeline_type") != pipeline_type
        ):
            raise CheckpointValidationError(
                f"Checkpoint pipeline mismatch at stage {stage!r}: requested "
                f"{pipeline_type!r}, found {cp.get('pipeline_type')!r}"
            )
        if cp and cp.get("status") == "completed":
            completed.append(stage)
    return completed


def get_next_stage(
    pipeline_dir: Path, project_id: str, pipeline_type: str | None = None
) -> Optional[str]:
    """Determine the next stage to run based on completed checkpoints.

    Uses pipeline-specific stage order so that pipelines with different
    stage sequences (e.g. cinematic vs explainer) progress correctly.
    """
    if pipeline_type is None:
        project_dir = _project_directory(pipeline_dir, project_id)
        marker_path = _contained_project_path(project_dir, PROJECT_MARKER_FILENAME)
        if marker_path.exists():
            if not marker_path.is_file():
                raise CheckpointValidationError(
                    f"Project marker is not a regular file: {marker_path}"
                )
            try:
                with open(marker_path, encoding="utf-8") as handle:
                    marker = json.load(handle)
            except (OSError, json.JSONDecodeError) as exc:
                raise CheckpointValidationError(
                    f"Cannot infer pipeline from project marker {marker_path}: {exc}"
                ) from exc
            if not isinstance(marker, dict) or marker.get("project_id") != project_id:
                raise CheckpointValidationError(
                    f"Cannot infer pipeline: project marker identity mismatch for {project_id!r}"
                )
            marker_pipeline = marker.get("pipeline_type")
            if not isinstance(marker_pipeline, str) or not marker_pipeline:
                raise CheckpointValidationError(
                    "Cannot infer pipeline: project marker has no concrete pipeline_type"
                )
            # Resolve now so corrupt/unknown catalog entries fail before any
            # generic stage-order fallback can advance the wrong DAG.
            get_pipeline_stages(marker_pipeline)
            pipeline_type = marker_pipeline
        else:
            # Bounded compatibility for marker-less legacy projects: infer
            # from a fully validated persisted checkpoint. Empty/new projects
            # retain the historical canonical first-stage fallback.
            latest = get_latest_checkpoint(pipeline_dir, project_id)
            if latest is not None:
                inferred = latest.get("pipeline_type")
                if not isinstance(inferred, str) or not inferred:
                    raise CheckpointValidationError(
                        "Cannot infer pipeline_type from latest checkpoint"
                    )
                get_pipeline_stages(inferred)
                pipeline_type = inferred

    stages = get_pipeline_stages(pipeline_type) if pipeline_type else STAGES
    optional: set[str] = set()
    if pipeline_type is not None:
        try:
            from lib.pipeline_loader import load_pipeline_readonly

            manifest = load_pipeline_readonly(pipeline_type)
            optional = {
                stage_def["name"]
                for stage_def in manifest.get("stages", [])
                if stage_def.get("checkpoint_required", True) is False
            }
        except Exception as exc:
            raise CheckpointValidationError(
                f"Unknown pipeline_type or invalid manifest {pipeline_type!r}: {exc}"
            ) from exc

    for stage in stages:
        checkpoint = read_checkpoint(pipeline_dir, project_id, stage)
        if checkpoint is not None:
            if (
                pipeline_type is not None
                and checkpoint.get("pipeline_type") != pipeline_type
            ):
                raise CheckpointValidationError(
                    f"Checkpoint pipeline mismatch at stage {stage!r}: expected "
                    f"{pipeline_type!r}, found {checkpoint.get('pipeline_type')!r}"
                )
            if checkpoint.get("status") == "completed":
                continue
            # An optional stage that has started is active work and must not be
            # skipped merely because persisting it was optional.
            return stage
        if stage in optional:
            continue
        return stage
    return None
