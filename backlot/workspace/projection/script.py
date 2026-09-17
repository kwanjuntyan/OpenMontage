"""Authority-aware B1B Script revision-set projection."""

from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
from typing import Any
from backlot.workspace.projection.contracts import (
    build_source_snapshot,
    validate_workspace_projection,
)
from backlot.workspace.projection.types import (
    ScriptDisplay,
    ScriptSection,
    ScriptVoicePerformance,
)
from backlot.workspace.readers.script import (
    ScriptProjectInput,
    read_script_project_input,
)


class ScriptProjectionNotFound(ValueError):
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


def _ref(project_id: str, stage: str) -> dict[str, Any]:
    return {
        "project_id": project_id,
        "kind": "stage",
        "stage": stage,
        "local_id": stage,
        "resource_key": "stage_" + sha256(f"{project_id}:{stage}".encode()).hexdigest(),
        "parent_refs": [],
        "relation_refs": [],
    }


def _identity(ref: dict[str, Any]) -> dict[str, Any]:
    return {
        key: ref[key]
        for key in ("project_id", "kind", "stage", "local_id", "resource_key")
    }


def _sources(record: ScriptProjectInput, ref: dict[str, Any]) -> list[dict[str, Any]]:
    identity = _identity(ref)
    values = [
        {
            "source_key": f"project:{record.catalog.project_id}:marker",
            "source_kind": "project_marker",
            "sha256": _digest(record.catalog.marker),
            "resource_ref": identity,
        }
    ]
    if record.catalog.manifest is not None and record.catalog.pipeline_type is not None:
        values.append(
            {
                "source_key": f"pipeline:{record.catalog.pipeline_type}:project:{record.catalog.project_id}",
                "source_kind": "pipeline_manifest",
                "sha256": _digest(record.catalog.manifest),
                "resource_ref": identity,
            }
        )
    if record.checkpoint is not None and record.owner_stage is not None:
        digest = _digest(record.checkpoint)
        status = record.checkpoint.get("status")
        kind = {
            "completed": "approved_checkpoint_artifact",
            "awaiting_human": "awaiting_checkpoint_artifact",
            "in_progress": "working_checkpoint_artifact",
            "failed": "failed_checkpoint_artifact",
        }.get(status, "failed_checkpoint_artifact")
        values.append(
            {
                "source_key": f"checkpoint:{record.catalog.project_id}:{record.owner_stage}",
                "source_kind": kind,
                "sha256": digest,
                "resource_ref": identity,
                "revision_ref": {
                    "revision_kind": "checkpoint",
                    "revision_id": record.owner_stage,
                    "stage": record.owner_stage,
                    "sha256": digest,
                },
            }
        )
    return values


def _authority(
    source: dict[str, Any] | None,
    state: str,
    stage: str | None,
    reason: str | None = None,
    human_approved: bool | None = None,
) -> dict[str, Any]:
    if state in {"canonical", "candidate"} and source and stage:
        return {
            "authority_state": state,
            "validation_state": "validated",
            "source_kind": "approved_checkpoint_artifact"
            if state == "canonical"
            else "awaiting_checkpoint_artifact",
            "evidence_scope": "checkpoint_validated",
            "evidence_refs": [
                {"source_key": source["source_key"], "sha256": source["sha256"]}
            ],
            "degraded_reasons": [],
            "source_stage": stage,
            "checkpoint_status": "completed"
            if state == "canonical"
            else "awaiting_human",
            "human_approved": human_approved,
        }
    return {
        "authority_state": "unavailable",
        "validation_state": "invalid"
        if reason and "invalid" in reason
        else "unverified",
        "source_kind": "unavailable",
        "evidence_scope": "none",
        "evidence_refs": [],
        "degraded_reasons": [reason or "script_missing"],
    }


def _display_script(value: dict[str, Any]) -> ScriptDisplay:
    """Copy the official Script only through this closed Workspace allowlist."""
    sections: list[ScriptSection] = []
    for section in value["sections"]:
        projected: ScriptSection = {
            key: section[key] for key in ("id", "text", "start_seconds", "end_seconds")
        }
        for key in ("label", "speaker_directions", "source_ref"):
            if key in section:
                projected[key] = section[key]
        if "delivery_cues" in section:
            projected["delivery_cues"] = {
                key: section["delivery_cues"][key]
                for key in (
                    "pace",
                    "energy",
                    "emphasis_words",
                    "pause_before_seconds",
                    "pause_after_seconds",
                    "delivery_note",
                    "provider_text",
                )
                if key in section["delivery_cues"]
            }
        if "enhancement_cues" in section:
            projected["enhancement_cues"] = [
                {
                    key: cue[key]
                    for key in ("type", "description", "timestamp_seconds")
                    if key in cue
                }
                for cue in section["enhancement_cues"]
            ]
        if "pronunciation_guides" in section:
            projected["pronunciation_guides"] = [
                {key: guide[key] for key in ("word", "phonetic")}
                for guide in section["pronunciation_guides"]
            ]
        sections.append(projected)
    display: ScriptDisplay = {
        "version": value["version"],
        "title": value["title"],
        "total_duration_seconds": value["total_duration_seconds"],
        "sections": sections,
    }
    if "voice_performance" in value:
        voice: ScriptVoicePerformance = {
            key: value["voice_performance"][key]
            for key in (
                "performance_intent",
                "pacing_profile",
                "energy_curve",
                "pause_policy",
                "sample_section_id",
            )
            if key in value["voice_performance"]
        }
        if "provider_notes" in value["voice_performance"]:
            voice["provider_notes"] = {
                key: note
                for key, note in value["voice_performance"]["provider_notes"].items()
            }
        display["voice_performance"] = voice
    return display


def _revision(
    record: ScriptProjectInput,
    ref: dict[str, Any],
    snapshot: dict[str, Any],
    source: dict[str, Any],
    state: str,
) -> dict[str, Any]:
    assert record.script is not None
    return {
        "resource_ref": ref,
        "revision_ref": source["revision_ref"],
        "source_snapshot": snapshot,
        "authority": _authority(
            source,
            state,
            record.owner_stage,
            human_approved=record.checkpoint.get("human_approved"),
        ),
        "capabilities": {
            "view": {"available": True, "reason": None},
            "mutate": {"available": False, "reason": "observer_only"},
        },
        "diagnostics": [],
        "data": {
            "version": "backlot.workspace.resource-summary.v1",
            "label": record.script["title"],
            "availability": "available",
            "description": "Validated manifest-owner Script display fields; timing semantics are not inferred.",
            "script": _display_script(record.script),
        },
    }


class ScriptProjectionResolver:
    def __init__(self, projects_root: Path):
        self.projects_root = Path(projects_root)

    def resolve(self, project_id: str) -> dict[str, Any]:
        try:
            record = read_script_project_input(self.projects_root, project_id)
        except (OSError, ValueError) as exc:
            raise ScriptProjectionNotFound() from exc
        owner = record.owner_stage or "script"
        ref = _ref(record.catalog.project_id, owner)
        sources = _sources(record, ref)
        snapshot = build_source_snapshot(sources)
        source = next(
            (
                item
                for item in sources
                if item["source_key"].startswith(
                    f"checkpoint:{record.catalog.project_id}:"
                )
            ),
            None,
        )
        status = record.checkpoint.get("status") if record.checkpoint else None
        valid = record.script is not None and source is not None
        current = (
            _revision(record, ref, snapshot, source, "canonical")
            if valid
            and status == "completed"
            and (
                not record.human_approval_required
                or record.checkpoint.get("human_approved") is True
            )
            else None
        )
        candidates = (
            [_revision(record, ref, snapshot, source, "candidate")]
            if valid and status == "awaiting_human"
            else []
        )
        reason = (
            None
            if current
            else (
                "not_identifiable_from_current_contract"
                if candidates
                else record.invalid_reason
                or (
                    "script_display_snapshot_unavailable"
                    if status in {"in_progress", "failed"}
                    else "script_missing"
                )
            )
        )
        authority = (
            _authority(
                source,
                "canonical",
                owner,
                human_approved=record.checkpoint.get("human_approved"),
            )
            if current
            else _authority(
                source,
                "candidate",
                owner,
                human_approved=record.checkpoint.get("human_approved"),
            )
            if candidates
            else _authority(None, "unavailable", owner, reason)
        )
        projection = {
            "projection_version": "backlot.workspace.v1",
            "projection_kind": "revision_set",
            "data_schema": "backlot.workspace.revision-set.v1",
            "resource_ref": ref,
            "revision_ref": {
                "revision_kind": "projection",
                "revision_id": f"script-{record.catalog.project_id}-{owner}",
                "sha256": snapshot["composite_sha256"],
            },
            "source_snapshot": snapshot,
            "authority": authority,
            "capabilities": {
                "view": {"available": True, "reason": None},
                "mutate": {"available": False, "reason": "observer_only"},
            },
            "diagnostics": []
            if current
            else [
                {
                    "code": reason,
                    "severity": "warning",
                    "message": "Script is unavailable or not canonical under the current contract.",
                    "source_keys": [item["source_key"] for item in sources],
                    "resource_refs": [_identity(ref)],
                }
            ],
            "data": {
                "version": "backlot.workspace.revision-set.v1",
                "current_canonical": current,
                "current_canonical_unavailable_reason": reason,
                "pending_candidates": candidates,
                "historical_revisions": [],
            },
        }
        return validate_workspace_projection(projection)


__all__ = ["ScriptProjectionNotFound", "ScriptProjectionResolver"]
