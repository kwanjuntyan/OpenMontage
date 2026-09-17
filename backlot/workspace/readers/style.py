"""Contained official observations for the B1C Style read projection."""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any
from lib.checkpoint import CheckpointValidationError, read_checkpoint
from schemas.artifacts import validate_artifact
from styles.playbook_loader import load_playbook
from .catalog import CatalogProjectInput, read_catalog_project_input

_PLAYBOOK_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def _safe_playbook_key(value: object) -> str | None:
    if not isinstance(value, str) or not _PLAYBOOK_KEY.fullmatch(value):
        return None
    if any(token in value for token in ("/", "\\", ".", ":", "\x00")):
        return None
    return value


@dataclass(frozen=True)
class CheckpointStyleObservation:
    stage: str
    checkpoint: dict[str, Any] | None
    value: str | None
    state: str


@dataclass(frozen=True)
class StyleProjectInput:
    catalog: CatalogProjectInput
    proposal_stage: str | None
    proposal_requires_approval: bool
    proposal_checkpoint: dict[str, Any] | None
    proposal: dict[str, Any] | None
    course: dict[str, Any] | None
    selected_concept: dict[str, Any] | None
    scene_stage: str | None
    scene_checkpoint: dict[str, Any] | None
    scene_plan: dict[str, Any] | None
    scene_state: str
    checkpoint_observations: tuple[CheckpointStyleObservation, ...]
    playbook_key: str | None
    playbook: dict[str, Any] | None
    invalid_reason: str | None


def _owners(stages: list[Any], artifact: str) -> list[dict[str, Any]]:
    return [
        stage
        for stage in stages
        if isinstance(stage, dict)
        and isinstance(stage.get("name"), str)
        and isinstance(stage.get("produces"), list)
        and artifact in stage["produces"]
    ]


def _record(
    catalog: CatalogProjectInput,
    proposal_stage: str | None = None,
    *,
    requires: bool = False,
    checkpoint: dict[str, Any] | None = None,
    proposal: dict[str, Any] | None = None,
    course: dict[str, Any] | None = None,
    selected: dict[str, Any] | None = None,
    scene_stage: str | None = None,
    scene_checkpoint: dict[str, Any] | None = None,
    scene_plan: dict[str, Any] | None = None,
    scene_state: str = "not_yet_corroborated",
    observed: tuple[CheckpointStyleObservation, ...] = (),
    key: str | None = None,
    playbook: dict[str, Any] | None = None,
    reason: str | None = None,
) -> StyleProjectInput:
    return StyleProjectInput(
        catalog,
        proposal_stage,
        requires,
        checkpoint,
        proposal,
        course,
        selected,
        scene_stage,
        scene_checkpoint,
        scene_plan,
        scene_state,
        observed,
        key,
        playbook,
        reason,
    )


def read_style_project_input(projects_root: Path, project_id: str) -> StyleProjectInput:
    catalog = read_catalog_project_input(projects_root, project_id)
    stages = catalog.manifest.get("stages", []) if catalog.manifest else []
    proposal_owners = _owners(stages, "proposal_packet")
    if len(proposal_owners) != 1:
        return _record(
            catalog,
            reason="proposal_owner_stage_ambiguous"
            if proposal_owners
            else "proposal_owner_stage_missing",
        )
    proposal_stage = proposal_owners[0]["name"]
    requires = proposal_owners[0].get("human_approval_default") is True
    observed: list[CheckpointStyleObservation] = []
    checkpoints: dict[str, dict[str, Any] | None] = {}
    invalid: set[str] = set()
    for stage in stages:
        if not isinstance(stage, dict) or not isinstance(stage.get("name"), str):
            continue
        name = stage["name"]
        try:
            checkpoint = read_checkpoint(projects_root, catalog.project_id, name)
        except (CheckpointValidationError, OSError, ValueError):
            checkpoints[name] = None
            invalid.add(name)
            observed.append(CheckpointStyleObservation(name, None, None, "invalid"))
            continue
        checkpoints[name] = checkpoint
        if checkpoint is not None and isinstance(checkpoint.get("style_playbook"), str):
            observed.append(
                CheckpointStyleObservation(
                    name, checkpoint, checkpoint["style_playbook"], "present"
                )
            )
    observations = tuple(observed)
    proposal_checkpoint = checkpoints.get(proposal_stage)
    if proposal_stage in invalid:
        return _record(
            catalog,
            proposal_stage,
            requires=requires,
            observed=observations,
            reason="proposal_checkpoint_invalid",
        )
    if proposal_checkpoint is None:
        return _record(
            catalog,
            proposal_stage,
            requires=requires,
            observed=observations,
            reason="proposal_missing",
        )
    artifacts = proposal_checkpoint.get("artifacts")
    proposal = artifacts.get("proposal_packet") if isinstance(artifacts, dict) else None
    try:
        validate_artifact("proposal_packet", proposal)
    except Exception:
        return _record(
            catalog,
            proposal_stage,
            requires=requires,
            checkpoint=proposal_checkpoint,
            observed=observations,
            reason="proposal_invalid",
        )
    selected = [
        item
        for item in proposal["concept_options"]
        if item.get("id") == proposal["selected_concept"]["concept_id"]
    ]
    if len(selected) != 1:
        return _record(
            catalog,
            proposal_stage,
            requires=requires,
            checkpoint=proposal_checkpoint,
            proposal=proposal,
            observed=observations,
            reason="selected_concept_link_invalid",
        )
    course = None
    candidate_course = (
        artifacts.get("course_manifest") if isinstance(artifacts, dict) else None
    )
    if candidate_course is not None:
        try:
            validate_artifact("course_manifest", candidate_course)
            if candidate_course.get("project_id") == catalog.project_id:
                course = candidate_course
        except Exception:
            pass
    scene_owners = _owners(stages, "scene_plan")
    scene_stage = scene_owners[0]["name"] if len(scene_owners) == 1 else None
    scene_checkpoint = None
    scene_plan = None
    scene_state = "not_yet_corroborated"
    if len(scene_owners) > 1 or (scene_stage is not None and scene_stage in invalid):
        scene_state = "invalid"
    elif scene_stage:
        scene_checkpoint = checkpoints.get(scene_stage)
        if scene_checkpoint is not None:
            scene_artifacts = scene_checkpoint.get("artifacts")
            candidate = (
                scene_artifacts.get("scene_plan")
                if isinstance(scene_artifacts, dict)
                else None
            )
            if candidate is None and scene_checkpoint.get("status") in {
                "in_progress",
                "failed",
                "awaiting_human",
            }:
                scene_state = "not_yet_corroborated"
            else:
                try:
                    validate_artifact("scene_plan", candidate)
                    scene_plan = candidate
                    scene_state = (
                        "present"
                        if isinstance(candidate.get("style_playbook"), str)
                        else "invalid"
                    )
                except Exception:
                    scene_state = "invalid"
    key = _safe_playbook_key(proposal.get("production_plan", {}).get("playbook"))
    common = dict(
        requires=requires,
        checkpoint=proposal_checkpoint,
        proposal=proposal,
        course=course,
        selected=selected[0],
        scene_stage=scene_stage,
        scene_checkpoint=scene_checkpoint,
        scene_plan=scene_plan,
        scene_state=scene_state,
        observed=observations,
    )
    if key is None:
        return _record(
            catalog,
            proposal_stage,
            **common,
            reason="selected_playbook_missing_or_unsafe",
        )
    try:
        playbook = load_playbook(key)
    except Exception:
        return _record(
            catalog,
            proposal_stage,
            **common,
            key=key,
            reason="selected_playbook_catalog_invalid_or_missing",
        )
    return _record(catalog, proposal_stage, **common, key=key, playbook=playbook)


__all__ = [
    "CheckpointStyleObservation",
    "StyleProjectInput",
    "read_style_project_input",
]
