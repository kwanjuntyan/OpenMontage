"""Minimal, read-only B0.2 Workspace shell projection."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

from backlot.workspace.projection.contracts import (
    build_source_snapshot,
    validate_workspace_projection,
)
from backlot.workspace.readers.shell import (
    ShellProjectInput,
    StageCheckpointInput,
    read_shell_project_input,
)


class ShellProjectionNotFound(ValueError):
    """The requested project has no authenticated Workspace identity."""


def _digest(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return f"sha256:{sha256(payload).hexdigest()}"


def _resource_key(project_id: str) -> str:
    return f"project_{sha256(project_id.encode('utf-8')).hexdigest()}"


def _project_ref(project_id: str) -> dict[str, Any]:
    return {
        "project_id": project_id,
        "kind": "project",
        "stage": None,
        "local_id": project_id,
        "resource_key": _resource_key(project_id),
        "parent_refs": [],
        "relation_refs": [],
    }


def _source_identity(project_ref: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: project_ref[key]
        for key in ("project_id", "kind", "stage", "local_id", "resource_key")
    }


def _base_sources(
    record: ShellProjectInput, project_ref: Mapping[str, Any]
) -> list[dict[str, Any]]:
    source_identity = _source_identity(project_ref)
    sources = [
        {
            "source_key": f"project:{record.catalog.project_id}:marker",
            "source_kind": "project_marker",
            "sha256": _digest(record.catalog.marker),
            "resource_ref": source_identity,
        }
    ]
    if record.catalog.manifest is not None and record.catalog.pipeline_type is not None:
        sources.append(
            {
                "source_key": f"pipeline:{record.catalog.pipeline_type}:project:{record.catalog.project_id}",
                "source_kind": "pipeline_manifest",
                "sha256": _digest(record.catalog.manifest),
                "resource_ref": source_identity,
            }
        )
    return sources


def _checkpoint_source(
    project_ref: Mapping[str, Any], stage: StageCheckpointInput
) -> dict[str, Any] | None:
    checkpoint = stage.checkpoint
    if checkpoint is None:
        return None
    status = checkpoint.get("status")
    source_kind = {
        "completed": "approved_checkpoint_artifact",
        "awaiting_human": "awaiting_checkpoint_artifact",
        "in_progress": "working_checkpoint_artifact",
        "failed": "failed_checkpoint_artifact",
    }.get(status)
    if source_kind is None:
        return None
    digest = _digest(checkpoint)
    return {
        "source_key": f"checkpoint:{project_ref['project_id']}:{stage.name}",
        "source_kind": source_kind,
        "sha256": digest,
        "resource_ref": _source_identity(project_ref),
        "revision_ref": {
            "revision_kind": "checkpoint",
            "revision_id": stage.name,
            "stage": stage.name,
            "sha256": digest,
        },
    }


def _stage_summary(stage: StageCheckpointInput) -> dict[str, Any]:
    if stage.invalid:
        status = "invalid"
    elif stage.checkpoint is None:
        status = "pending"
    else:
        status = stage.checkpoint.get("status")
        if status not in {"in_progress", "awaiting_human", "completed", "failed"}:
            status = "invalid"
    return {
        "name": stage.name,
        "status": status,
        "human_approval_default": stage.human_approval_default,
    }


def _current_stage(stages: list[dict[str, Any]]) -> str | None:
    for status in ("in_progress", "awaiting_human", "failed", "invalid", "pending"):
        found = next(
            (stage["name"] for stage in stages if stage["status"] == status), None
        )
        if found is not None:
            return found
    return None


def _gate_state(
    stages: list[dict[str, Any]], checkpoint_inputs: tuple[StageCheckpointInput, ...]
) -> str:
    statuses = {stage["status"] for stage in stages}
    if "invalid" in statuses:
        return "invalid"
    if "failed" in statuses:
        return "failed"
    if "awaiting_human" in statuses:
        return "awaiting_human"
    for stage in checkpoint_inputs:
        if (
            stage.human_approval_default
            and stage.checkpoint is not None
            and stage.checkpoint.get("status") == "completed"
            and stage.checkpoint.get("human_approved") is True
        ):
            return "approved"
    return "none"


def _script_owner_stage(manifest: dict[str, Any] | None) -> str | None:
    """Expose only an unambiguous manifest-declared Script owner for B1B UI routing."""
    stages = manifest.get("stages", []) if manifest else []
    owners = [
        stage.get("name")
        for stage in stages
        if isinstance(stage, dict)
        and isinstance(stage.get("produces"), list)
        and "script" in stage["produces"]
        and isinstance(stage.get("name"), str)
    ]
    return owners[0] if len(owners) == 1 else None


def _authority(
    sources: list[dict[str, Any]], *, invalid: bool, reason: str | None
) -> dict[str, Any]:
    evidence = [
        {"source_key": source["source_key"], "sha256": source["sha256"]}
        for source in sources
    ]
    has_checkpoint = any("checkpoint" in source["source_kind"] for source in sources)
    if invalid:
        return {
            "authority_state": "unavailable",
            "validation_state": "invalid",
            "source_kind": "unavailable",
            "evidence_scope": "checkpoint_validated"
            if has_checkpoint
            else "manifest_only",
            "evidence_refs": evidence,
            "degraded_reasons": [reason or "pipeline_manifest_invalid"],
        }
    return {
        "authority_state": "execution_evidence",
        "validation_state": "validated",
        "source_kind": "derived_projection",
        "evidence_scope": "checkpoint_validated" if has_checkpoint else "manifest_only",
        "evidence_refs": evidence,
        "degraded_reasons": [],
    }


def _diagnostic(
    code: str, snapshot: Mapping[str, Any], project_ref: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "code": code,
        "severity": "warning",
        "message": {
            "classification_evidence_deferred": "Course and candidate classification evidence is deferred to B1.",
            "pipeline_manifest_invalid": "Selected pipeline manifest is unavailable or invalid.",
            "pipeline_manifest_unavailable": "Selected pipeline manifest is unavailable.",
            "invalid_checkpoint": "One or more manifest-declared checkpoints are invalid.",
        }.get(code, "Workspace source is unavailable."),
        "source_keys": [source["source_key"] for source in snapshot["sources"]],
        "resource_refs": [_source_identity(project_ref)],
    }


class ShellProjectionResolver:
    """Resolve a marker/manifest/checkpoint-only Workspace shell projection."""

    def __init__(self, projects_root: Path):
        self.projects_root = Path(projects_root)

    def resolve(self, project_id: str) -> dict[str, Any]:
        try:
            record = read_shell_project_input(self.projects_root, project_id)
        except (OSError, ValueError) as exc:
            raise ShellProjectionNotFound("unknown or unauthenticated project") from exc

        project_ref = _project_ref(record.catalog.project_id)
        sources = _base_sources(record, project_ref)
        stage_summaries = [_stage_summary(stage) for stage in record.stages]
        for stage in record.stages:
            source = _checkpoint_source(project_ref, stage)
            if source is not None:
                sources.append(source)
        snapshot = build_source_snapshot(sources)

        manifest_invalid = record.catalog.manifest is None
        invalid_checkpoint = any(
            stage["status"] == "invalid" for stage in stage_summaries
        )
        reason = (
            record.catalog.manifest_error
            if manifest_invalid
            else ("invalid_checkpoint" if invalid_checkpoint else None)
        )
        diagnostics = []
        if manifest_invalid:
            diagnostics.append(
                _diagnostic(
                    reason or "pipeline_manifest_invalid", snapshot, project_ref
                )
            )
        else:
            diagnostics.append(
                _diagnostic("classification_evidence_deferred", snapshot, project_ref)
            )
            if invalid_checkpoint:
                diagnostics.append(
                    _diagnostic("invalid_checkpoint", snapshot, project_ref)
                )

        projection = {
            "projection_version": "backlot.workspace.v1",
            "projection_kind": "shell",
            "data_schema": "backlot.workspace.shell.v1",
            "resource_ref": project_ref,
            "revision_ref": {
                "revision_kind": "projection",
                "revision_id": f"shell-{record.catalog.project_id}",
                "sha256": snapshot["composite_sha256"],
            },
            "source_snapshot": snapshot,
            "authority": _authority(
                sources,
                invalid=manifest_invalid or invalid_checkpoint,
                reason=reason,
            ),
            "capabilities": {
                "view": {"available": True, "reason": None},
                "mutate": {"available": False, "reason": "observer_only"},
                "classification": {
                    "available": False,
                    "reason": reason
                    if manifest_invalid
                    else "classification_evidence_deferred",
                },
            },
            "diagnostics": diagnostics,
            "data": {
                "version": "backlot.workspace.shell.v1",
                # A selected pipeline name without a validated manifest is not
                # an authoritative v1 pipeline identity.
                "pipeline_type": (
                    record.catalog.pipeline_type
                    if record.catalog.manifest is not None
                    and record.catalog.pipeline_type is not None
                    else "unavailable"
                ),
                "classification": "unavailable",
                "stages": stage_summaries,
                "current_stage": None
                if manifest_invalid
                else _current_stage(stage_summaries),
                "gate_state": "unavailable"
                if manifest_invalid
                else _gate_state(stage_summaries, record.stages),
            },
        }
        if record.catalog.manifest is not None:
            projection["data"]["script_owner_stage"] = _script_owner_stage(
                record.catalog.manifest
            )
        return validate_workspace_projection(projection)


__all__ = ["ShellProjectionNotFound", "ShellProjectionResolver"]
