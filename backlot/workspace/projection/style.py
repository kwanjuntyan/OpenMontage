"""Authority-aware B1C Style multi-source projection."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from backlot.workspace.projection.contracts import (
    build_source_snapshot,
    validate_workspace_projection,
)
from backlot.workspace.readers.style import StyleProjectInput, read_style_project_input


class StyleProjectionNotFound(ValueError):
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
        "kind": "project",
        "stage": None,
        "local_id": project_id,
        "resource_key": "project_" + sha256(project_id.encode()).hexdigest(),
        "parent_refs": [],
        "relation_refs": [],
    }


def _identity(ref: dict[str, Any]) -> dict[str, Any]:
    return {
        key: ref[key]
        for key in ("project_id", "kind", "stage", "local_id", "resource_key")
    }


def _checkpoint_source(
    record: StyleProjectInput,
    ref: dict[str, Any],
    stage: str,
    checkpoint: dict[str, Any],
) -> dict[str, Any]:
    digest = _digest(checkpoint)
    status = checkpoint.get("status")
    return {
        "source_key": f"checkpoint:{record.catalog.project_id}:{stage}",
        "source_kind": {
            "completed": "approved_checkpoint_artifact",
            "awaiting_human": "awaiting_checkpoint_artifact",
            "in_progress": "working_checkpoint_artifact",
            "failed": "failed_checkpoint_artifact",
        }.get(status, "failed_checkpoint_artifact"),
        "sha256": digest,
        "resource_ref": _identity(ref),
        "revision_ref": {
            "revision_kind": "checkpoint",
            "revision_id": stage,
            "stage": stage,
            "sha256": digest,
        },
    }


def _sources(record: StyleProjectInput, ref: dict[str, Any]) -> list[dict[str, Any]]:
    values = [
        {
            "source_key": f"project:{record.catalog.project_id}:marker",
            "source_kind": "project_marker",
            "sha256": _digest(record.catalog.marker),
            "resource_ref": _identity(ref),
        }
    ]
    if record.catalog.manifest is not None and record.catalog.pipeline_type is not None:
        values.append(
            {
                "source_key": f"pipeline:{record.catalog.pipeline_type}:project:{record.catalog.project_id}",
                "source_kind": "pipeline_manifest",
                "sha256": _digest(record.catalog.manifest),
                "resource_ref": _identity(ref),
            }
        )
    checkpoints = {
        observation.stage: observation.checkpoint
        for observation in record.checkpoint_observations
        if observation.checkpoint is not None
    }
    if record.proposal_stage and record.proposal_checkpoint is not None:
        checkpoints[record.proposal_stage] = record.proposal_checkpoint
    if record.scene_stage and record.scene_checkpoint is not None:
        checkpoints[record.scene_stage] = record.scene_checkpoint
    for stage, checkpoint in sorted(checkpoints.items()):
        values.append(_checkpoint_source(record, ref, stage, checkpoint))
    if record.playbook is not None:
        digest = _digest(_display_catalog(record.playbook))
        assert record.playbook_key is not None
        catalog_key = sha256(record.playbook_key.encode("utf-8")).hexdigest()
        values.append(
            {
                "source_key": f"style:catalog:{catalog_key}",
                "source_kind": "style_catalog_current",
                "sha256": digest,
                "resource_ref": _identity(ref),
                "revision_ref": {
                    "revision_kind": "content",
                    "revision_id": f"style-catalog-{catalog_key}",
                    "sha256": digest,
                },
            }
        )
    return values


def _copy(value: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    return {key: value[key] for key in keys if key in value}


def _taste(value: dict[str, Any]) -> dict[str, Any]:
    return _copy(
        value,
        (
            "design_read",
            "visual_variance",
            "motion_intensity",
            "information_density",
            "palette_discipline",
            "layout_variation",
            "reference_strategy",
            "anti_patterns",
            "quality_gates",
        ),
    )


def _display_catalog(value: dict[str, Any]) -> dict[str, Any]:
    """Copy a validated playbook only through the closed Workspace allowlist."""
    visual = value["visual_language"]
    typography = value["typography"]
    motion = value["motion"]
    audio = value["audio"]
    assets = value["asset_generation"]
    catalog = {
        "identity": _copy(
            value["identity"], ("name", "category", "mood", "pace", "best_for")
        ),
        "visual_language": {
            "color_palette": _copy(
                visual["color_palette"],
                ("primary", "accent", "background", "text", "muted"),
            ),
            "composition": visual["composition"],
            "texture": visual["texture"],
        },
        "typography": _copy(typography, ("scale_system", "weight_matrix")),
        "motion": _copy(
            motion,
            ("transitions", "animation_style", "pacing_rules", "entrance", "exit"),
        ),
        "audio": _copy(
            audio,
            (
                "voice_style",
                "music_mood",
                "music_volume",
                "sfx_style",
                "ducking_threshold_db",
                "voice_variation_allowed",
                "hero_moment_voice_shift",
                "transition_voice_shift",
            ),
        ),
        "asset_generation": _copy(
            assets,
            (
                "image_prompt_prefix",
                "image_negative_prompt",
                "diagram_style",
                "consistency_anchors",
            ),
        ),
        "quality_rules": list(value["quality_rules"]),
    }
    for key in ("headings", "body", "code", "stat_card"):
        if key in typography:
            catalog["typography"][key] = _copy(
                typography[key],
                ("font", "weight", "tracking", "line_height", "size_multiplier"),
            )
    if "taste_profile" in value:
        catalog["taste_profile"] = _taste(value["taste_profile"])
    return catalog


def _authority(
    source: dict[str, Any] | None,
    state: str,
    stage: str | None,
    reason: str | None = None,
    evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if source:
        lifecycle = {
            "approved_checkpoint_artifact": ("canonical", "completed", True),
            "awaiting_checkpoint_artifact": ("candidate", "awaiting_human", False),
            "working_checkpoint_artifact": ("display_only", "in_progress", None),
            "failed_checkpoint_artifact": ("display_only", "failed", None),
        }.get(source["source_kind"])
        if lifecycle is not None:
            state, checkpoint_status, human_approved = lifecycle
        elif source["source_kind"] == "style_catalog_current":
            state, checkpoint_status, human_approved = "canonical", None, None
        else:
            return _authority(None, "unavailable", stage, reason)
        return {
            "authority_state": state,
            "validation_state": "validated",
            "source_kind": source["source_kind"],
            "evidence_scope": "manifest_only"
            if source["source_kind"] == "style_catalog_current"
            else "checkpoint_validated",
            "evidence_refs": [
                {"source_key": item["source_key"], "sha256": item["sha256"]}
                for item in (evidence or [source])
            ],
            "degraded_reasons": ["current_catalog_not_historically_frozen"]
            if source["source_kind"] == "style_catalog_current"
            else [],
            "source_stage": stage,
            "checkpoint_status": checkpoint_status,
            "human_approved": human_approved,
            "historically_frozen": False
            if source["source_kind"] == "style_catalog_current"
            else None,
        }
    return {
        "authority_state": "unavailable",
        "validation_state": "invalid"
        if reason and "invalid" in reason
        else "unverified",
        "source_kind": "unavailable",
        "evidence_scope": "none",
        "evidence_refs": [],
        "degraded_reasons": [reason or "style_unavailable"],
    }


class StyleProjectionResolver:
    def __init__(self, projects_root: Path):
        self.projects_root = Path(projects_root)

    def resolve(self, project_id: str) -> dict[str, Any]:
        try:
            record = read_style_project_input(self.projects_root, project_id)
        except (OSError, ValueError) as exc:
            raise StyleProjectionNotFound() from exc
        ref = _ref(record.catalog.project_id)
        sources = _sources(record, ref)
        snapshot = build_source_snapshot(sources)
        proposal_source = next(
            (
                item
                for item in sources
                if item["source_key"].startswith(
                    f"checkpoint:{record.catalog.project_id}:{record.proposal_stage}"
                )
            ),
            None,
        )
        catalog_source = next(
            (
                item
                for item in sources
                if item["source_kind"] == "style_catalog_current"
            ),
            None,
        )
        source_by_stage = {
            item["revision_ref"]["stage"]: item
            for item in sources
            if item.get("revision_ref", {}).get("revision_kind") == "checkpoint"
        }
        proposal_status = (
            record.proposal_checkpoint.get("status")
            if record.proposal_checkpoint
            else None
        )
        marker = record.catalog.marker.get("style_playbook")
        proposal_key = (
            record.proposal.get("production_plan", {}).get("playbook")
            if record.proposal
            else None
        )
        scene_key = (
            record.scene_plan.get("style_playbook") if record.scene_plan else None
        )
        checkpoint_key = (
            record.proposal_checkpoint.get("style_playbook")
            if record.proposal_checkpoint
            else None
        )
        observations = {
            "project_marker": {
                "value": marker if isinstance(marker, str) else None,
                "state": "present" if isinstance(marker, str) else "missing",
            },
            "proposal_selection": {
                "value": proposal_key if isinstance(proposal_key, str) else None,
                "state": "present" if isinstance(proposal_key, str) else "invalid",
            },
            "proposal_checkpoint": {
                "value": checkpoint_key if isinstance(checkpoint_key, str) else None,
                "state": "present" if isinstance(checkpoint_key, str) else "missing",
            },
            "scene_plan": {
                "value": scene_key if isinstance(scene_key, str) else None,
                "state": record.scene_state,
            },
        }
        checkpoint_observations = []
        for observation in record.checkpoint_observations:
            source = source_by_stage.get(observation.stage)
            checkpoint_observations.append(
                {
                    "stage": observation.stage,
                    "value": observation.value,
                    "state": observation.state,
                    "authority": _authority(
                        source,
                        "candidate"
                        if source
                        and source["source_kind"] == "awaiting_checkpoint_artifact"
                        else "canonical",
                        observation.stage,
                    )
                    if source and observation.state == "present"
                    else _authority(
                        None,
                        "unavailable",
                        observation.stage,
                        "style_checkpoint_observation_invalid",
                    ),
                }
            )
        present = [
            item["value"]
            for item in observations.values()
            if item["state"] == "present"
        ]
        present.extend(
            item["value"]
            for item in checkpoint_observations
            if item["state"] == "present"
        )
        agreed = bool(present) and len(set(present)) == 1
        proposal_canonical = (
            record.proposal is not None
            and record.selected_concept is not None
            and proposal_status == "completed"
            and (
                not record.proposal_requires_approval
                or record.proposal_checkpoint.get("human_approved") is True
            )
        )
        proposal_candidate = (
            record.proposal is not None
            and record.selected_concept is not None
            and proposal_status == "awaiting_human"
        )
        invalid_observation = any(
            item["state"] == "invalid" for item in observations.values()
        ) or any(item["state"] == "invalid" for item in checkpoint_observations)
        resolved = (
            _display_catalog(record.playbook)
            if proposal_canonical
            and record.invalid_reason is None
            and not invalid_observation
            and agreed
            and catalog_source
            else None
        )
        if resolved is not None:
            resolved = {
                "playbook": proposal_key,
                "catalog": resolved,
                "historically_frozen": False,
            }
        proposal: dict[str, Any] = {
            "availability": "available"
            if proposal_canonical
            else "candidate"
            if proposal_candidate
            else "unavailable"
        }
        if record.proposal and record.selected_concept:
            plan = record.proposal["production_plan"]
            proposal["selected_concept"] = {
                "concept_id": record.selected_concept["id"],
                "visual_approach": record.selected_concept["visual_approach"],
            }
            for key in (
                "playbook",
                "art_direction",
                "renderer_family",
                "render_runtime",
                "composition_mode",
            ):
                if key in plan:
                    proposal[key] = plan[key]
            if "taste_profile" in plan:
                proposal["taste_profile"] = _taste(plan["taste_profile"])
        reason = (
            None
            if resolved is not None
            else (
                record.invalid_reason
                or (
                    "style_checkpoint_observation_invalid"
                    if invalid_observation
                    else "style_observation_conflict"
                    if not agreed
                    else "not_identifiable_from_current_contract"
                    if proposal_status == "awaiting_human"
                    else "style_unavailable"
                )
            )
        )
        binding_evidence = [proposal_source, catalog_source]
        marker_source = next(
            (item for item in sources if item["source_kind"] == "project_marker"), None
        )
        if observations["project_marker"]["state"] == "present":
            binding_evidence.append(marker_source)
        binding_evidence.extend(
            source_by_stage[item["stage"]]
            for item in checkpoint_observations
            if item["state"] == "present" and item["stage"] in source_by_stage
        )
        binding_evidence = [item for item in binding_evidence if item is not None]
        proposal_authority = (
            _authority(proposal_source, "canonical", record.proposal_stage)
            if proposal_canonical
            else _authority(proposal_source, "candidate", record.proposal_stage)
            if proposal_candidate
            else _authority(
                None,
                "unavailable",
                record.proposal_stage,
                record.invalid_reason or "proposal_unavailable",
            )
        )
        authority = (
            _authority(
                proposal_source,
                "canonical",
                record.proposal_stage,
                evidence=binding_evidence,
            )
            if resolved is not None
            else _authority(None, "unavailable", record.proposal_stage, reason)
        )
        if resolved is not None:
            authority["degraded_reasons"] = ["current_catalog_not_historically_frozen"]
        data = {
            "version": "backlot.workspace.resource-summary.v1",
            "label": proposal_key if isinstance(proposal_key, str) else "Style",
            "availability": "available" if resolved is not None else "unavailable",
            "description": "Read-only Style observations; current catalog bytes are not historically frozen.",
            "style": {
                "proposal": proposal,
                "proposal_authority": proposal_authority,
                "observations": observations,
                "checkpoint_observations": checkpoint_observations,
                "resolved_style": resolved,
            },
        }
        if record.course is not None:
            data["style"]["course_style_intent"] = _copy(
                record.course["style_intent"], ("tone", "visual_intent")
            )
            data["style"]["course_authority"] = proposal_authority
        projection = {
            "projection_version": "backlot.workspace.v1",
            "projection_kind": "resource_summary",
            "data_schema": "backlot.workspace.resource-summary.v1",
            "resource_ref": ref,
            "revision_ref": {
                "revision_kind": "projection",
                "revision_id": f"style-{record.catalog.project_id}",
                "sha256": snapshot["composite_sha256"],
            },
            "source_snapshot": snapshot,
            "authority": authority,
            "capabilities": {
                "view": {"available": True, "reason": None},
                "mutate": {"available": False, "reason": "observer_only"},
            },
            "diagnostics": []
            if resolved is not None
            else [
                {
                    "code": reason,
                    "severity": "warning",
                    "message": "Style is unavailable or not current under the bounded Style contract.",
                    "source_keys": [item["source_key"] for item in sources],
                    "resource_refs": [_identity(ref)],
                }
            ],
            "data": data,
        }
        return validate_workspace_projection(projection)


__all__ = ["StyleProjectionNotFound", "StyleProjectionResolver"]
