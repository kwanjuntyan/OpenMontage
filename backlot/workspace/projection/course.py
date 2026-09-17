"""Authority-aware B1A Course revision-set projection."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from backlot.workspace.projection.contracts import (
    build_source_snapshot,
    validate_workspace_projection,
)
from backlot.workspace.readers.course import (
    CourseProjectInput,
    read_course_project_input,
)


class CourseProjectionNotFound(ValueError):
    pass


def _digest(value: Any) -> str:
    return (
        "sha256:"
        + sha256(
            json.dumps(
                value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode()
        ).hexdigest()
    )


def _ref(project_id: str) -> dict[str, Any]:
    return {
        "project_id": project_id,
        "kind": "course",
        "stage": "proposal",
        "local_id": project_id,
        "resource_key": "course_" + sha256(project_id.encode()).hexdigest(),
        "parent_refs": [],
        "relation_refs": [],
    }


def _identity(ref: dict[str, Any]) -> dict[str, Any]:
    return {
        key: ref[key]
        for key in ("project_id", "kind", "stage", "local_id", "resource_key")
    }


def _sources(record: CourseProjectInput, ref: dict[str, Any]) -> list[dict[str, Any]]:
    identity = _identity(ref)
    sources = [
        {
            "source_key": f"project:{record.catalog.project_id}:marker",
            "source_kind": "project_marker",
            "sha256": _digest(record.catalog.marker),
            "resource_ref": identity,
        }
    ]
    if record.catalog.manifest is not None and record.catalog.pipeline_type is not None:
        sources.append(
            {
                "source_key": f"pipeline:{record.catalog.pipeline_type}:project:{record.catalog.project_id}",
                "source_kind": "pipeline_manifest",
                "sha256": _digest(record.catalog.manifest),
                "resource_ref": identity,
            }
        )
    if record.checkpoint is not None:
        digest = _digest(record.checkpoint)
        kind = {
            "completed": "approved_checkpoint_artifact",
            "awaiting_human": "awaiting_checkpoint_artifact",
            "in_progress": "working_checkpoint_artifact",
            "failed": "failed_checkpoint_artifact",
        }.get(record.checkpoint.get("status"), "failed_checkpoint_artifact")
        sources.append(
            {
                "source_key": f"checkpoint:{record.catalog.project_id}:proposal",
                "source_kind": kind,
                "sha256": digest,
                "resource_ref": identity,
                "revision_ref": {
                    "revision_kind": "checkpoint",
                    "revision_id": "proposal",
                    "stage": "proposal",
                    "sha256": digest,
                },
            }
        )
    return sources


def _authority(
    source: dict[str, Any], state: str, reason: str | None = None
) -> dict[str, Any]:
    if state == "canonical":
        return {
            "authority_state": "canonical",
            "validation_state": "validated",
            "source_kind": "approved_checkpoint_artifact",
            "evidence_scope": "checkpoint_validated",
            "evidence_refs": [
                {"source_key": source["source_key"], "sha256": source["sha256"]}
            ],
            "degraded_reasons": [],
            "source_stage": "proposal",
            "checkpoint_status": "completed",
            "human_approved": True,
        }
    if state == "candidate":
        return {
            "authority_state": "candidate",
            "validation_state": "validated",
            "source_kind": "awaiting_checkpoint_artifact",
            "evidence_scope": "checkpoint_validated",
            "evidence_refs": [
                {"source_key": source["source_key"], "sha256": source["sha256"]}
            ],
            "degraded_reasons": [],
            "source_stage": "proposal",
            "checkpoint_status": "awaiting_human",
            "human_approved": False,
        }
    return {
        "authority_state": "unavailable",
        "validation_state": "invalid"
        if reason and "invalid" in reason
        else "unverified",
        "source_kind": "unavailable",
        "evidence_scope": "none",
        "evidence_refs": [],
        "degraded_reasons": [reason or "course_manifest_unavailable"],
    }


def _revision(
    record: CourseProjectInput,
    ref: dict[str, Any],
    snapshot: dict[str, Any],
    source: dict[str, Any],
    state: str,
) -> dict[str, Any]:
    course = record.course_manifest
    return {
        "resource_ref": ref,
        "revision_ref": source["revision_ref"],
        "source_snapshot": snapshot,
        "authority": _authority(source, state),
        "capabilities": {
            "view": {"available": True, "reason": None},
            "mutate": {"available": False, "reason": "observer_only"},
        },
        "diagnostics": [],
        "data": {
            "version": "backlot.workspace.resource-summary.v1",
            "label": course["title"],
            "availability": "available",
            "description": "Validated proposal-stage course design.",
            "course_design": course,
        },
    }


class CourseProjectionResolver:
    def __init__(self, projects_root: Path):
        self.projects_root = Path(projects_root)

    def resolve(self, project_id: str) -> dict[str, Any]:
        try:
            record = read_course_project_input(self.projects_root, project_id)
        except (OSError, ValueError) as exc:
            raise CourseProjectionNotFound() from exc
        ref = _ref(record.catalog.project_id)
        sources = _sources(record, ref)
        snapshot = build_source_snapshot(sources)
        checkpoint_source = next(
            (
                source
                for source in sources
                if source["source_key"].endswith(":proposal")
            ),
            None,
        )
        status = record.checkpoint.get("status") if record.checkpoint else None
        valid_course = (
            record.course_manifest is not None and checkpoint_source is not None
        )
        current = None
        candidates: list[dict[str, Any]] = []
        reason = record.invalid_reason or "course_manifest_unavailable"
        if (
            valid_course
            and status == "completed"
            and record.checkpoint.get("human_approved") is True
        ):
            current = _revision(record, ref, snapshot, checkpoint_source, "canonical")
            reason = None
        elif valid_course and status == "awaiting_human":
            candidates = [
                _revision(record, ref, snapshot, checkpoint_source, "candidate")
            ]
            reason = "not_identifiable_from_current_contract"
        elif status == "awaiting_human":
            reason = record.invalid_reason or "not_identifiable_from_current_contract"
        top_authority = (
            _authority(checkpoint_source, "canonical")
            if current
            else _authority(checkpoint_source, "candidate")
            if candidates
            else _authority({}, "unavailable", reason)
        )
        diagnostics = (
            []
            if current
            else [
                {
                    "code": reason or "course_manifest_unavailable",
                    "severity": "warning",
                    "message": "No approved proposal-stage Course manifest is available for display.",
                    "source_keys": [source["source_key"] for source in sources],
                    "resource_refs": [_identity(ref)],
                }
            ]
        )
        projection = {
            "projection_version": "backlot.workspace.v1",
            "projection_kind": "revision_set",
            "data_schema": "backlot.workspace.revision-set.v1",
            "resource_ref": ref,
            "revision_ref": {
                "revision_kind": "projection",
                "revision_id": f"course-{record.catalog.project_id}",
                "sha256": snapshot["composite_sha256"],
            },
            "source_snapshot": snapshot,
            "authority": top_authority,
            "capabilities": {
                "view": {"available": True, "reason": None},
                "mutate": {"available": False, "reason": "observer_only"},
            },
            "diagnostics": diagnostics,
            "data": {
                "version": "backlot.workspace.revision-set.v1",
                "current_canonical": current,
                "current_canonical_unavailable_reason": reason,
                "pending_candidates": candidates,
                "historical_revisions": [],
            },
        }
        return validate_workspace_projection(projection)


__all__ = ["CourseProjectionNotFound", "CourseProjectionResolver"]
