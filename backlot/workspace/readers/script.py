"""Contained official observations for the manifest-declared Script owner."""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from lib.checkpoint import CheckpointValidationError, read_checkpoint
from schemas.artifacts import validate_artifact
from .catalog import CatalogProjectInput, read_catalog_project_input


@dataclass(frozen=True)
class ScriptProjectInput:
    catalog: CatalogProjectInput
    owner_stage: str | None
    human_approval_required: bool
    checkpoint: dict[str, Any] | None
    script: dict[str, Any] | None
    invalid_reason: str | None


def read_script_project_input(
    projects_root: Path, project_id: str
) -> ScriptProjectInput:
    catalog = read_catalog_project_input(projects_root, project_id)
    stages = catalog.manifest.get("stages", []) if catalog.manifest else []
    owners = [
        stage.get("name")
        for stage in stages
        if isinstance(stage, dict)
        and isinstance(stage.get("produces"), list)
        and "script" in stage["produces"]
        and isinstance(stage.get("name"), str)
    ]
    if len(owners) != 1:
        return ScriptProjectInput(
            catalog,
            None,
            False,
            None,
            None,
            "script_owner_stage_ambiguous" if owners else "script_owner_stage_missing",
        )
    owner = owners[0]
    owner_definition = next(
        stage
        for stage in stages
        if isinstance(stage, dict) and stage.get("name") == owner
    )
    human_approval_required = owner_definition.get("human_approval_default") is True
    try:
        checkpoint = read_checkpoint(projects_root, catalog.project_id, owner)
    except (CheckpointValidationError, OSError, ValueError):
        return ScriptProjectInput(
            catalog,
            owner,
            human_approval_required,
            None,
            None,
            "script_checkpoint_invalid",
        )
    if checkpoint is None:
        return ScriptProjectInput(
            catalog, owner, human_approval_required, None, None, "script_missing"
        )
    artifacts = checkpoint.get("artifacts")
    script = artifacts.get("script") if isinstance(artifacts, dict) else None
    try:
        validate_artifact("script", script)
    except Exception:
        return ScriptProjectInput(
            catalog, owner, human_approval_required, checkpoint, None, "script_invalid"
        )
    return ScriptProjectInput(
        catalog, owner, human_approval_required, checkpoint, script, None
    )


__all__ = ["ScriptProjectInput", "read_script_project_input"]
