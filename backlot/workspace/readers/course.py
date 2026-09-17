"""Contained, official proposal-checkpoint observations for B1A Course."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from lib.checkpoint import CheckpointValidationError, read_checkpoint
from schemas.artifacts import validate_artifact

from .catalog import CatalogProjectInput, read_catalog_project_input


@dataclass(frozen=True)
class CourseProjectInput:
    catalog: CatalogProjectInput
    checkpoint: dict[str, Any] | None
    course_manifest: dict[str, Any] | None
    invalid_reason: str | None


def read_course_project_input(
    projects_root: Path, project_id: str
) -> CourseProjectInput:
    """Read only the authenticated project's manifest-declared proposal checkpoint.

    No history, loose artifact, or producer-private location is consulted.
    """
    catalog = read_catalog_project_input(projects_root, project_id)
    stages = catalog.manifest.get("stages", []) if catalog.manifest else []
    if not any(
        isinstance(stage, dict) and stage.get("name") == "proposal" for stage in stages
    ):
        return CourseProjectInput(catalog, None, None, "proposal_stage_not_declared")
    try:
        checkpoint = read_checkpoint(projects_root, catalog.project_id, "proposal")
    except (CheckpointValidationError, OSError, ValueError):
        return CourseProjectInput(catalog, None, None, "proposal_checkpoint_invalid")
    if checkpoint is None:
        return CourseProjectInput(catalog, None, None, "course_manifest_unavailable")
    artifacts = checkpoint.get("artifacts")
    if not isinstance(artifacts, dict):
        return CourseProjectInput(
            catalog, checkpoint, None, "proposal_artifacts_invalid"
        )
    proposal = artifacts.get("proposal_packet")
    course = artifacts.get("course_manifest")
    try:
        validate_artifact("proposal_packet", proposal)
        validate_artifact("course_manifest", course)
    except Exception:
        return CourseProjectInput(catalog, checkpoint, None, "course_manifest_invalid")
    if (
        proposal.get("production_plan", {}).get("content_form") != "course_form"
        or course.get("project_id") != catalog.project_id
    ):
        return CourseProjectInput(
            catalog, checkpoint, None, "course_manifest_identity_mismatch"
        )
    return CourseProjectInput(catalog, checkpoint, course, None)


__all__ = ["CourseProjectInput", "read_course_project_input"]
