"""Read-only, authenticated inputs for the B0.2 Workspace shell."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from lib.checkpoint import CheckpointValidationError, read_checkpoint

from .catalog import CatalogProjectInput, read_catalog_project_input


@dataclass(frozen=True)
class StageCheckpointInput:
    """One manifest-declared stage and its official checkpoint observation."""

    name: str
    human_approval_default: bool
    checkpoint: dict[str, Any] | None
    invalid: bool


@dataclass(frozen=True)
class ShellProjectInput:
    """Authenticated marker, selected manifest, and validated stage evidence."""

    catalog: CatalogProjectInput
    stages: tuple[StageCheckpointInput, ...]


def read_shell_project_input(projects_root: Path, project_id: str) -> ShellProjectInput:
    """Read only the manifest-declared checkpoints for an authenticated project.

    Missing checkpoints are normal stage observations.  Invalid checkpoints are
    deliberately not parsed or recovered from: their stage is represented as
    invalid by the projection and no loose artifact fallback is consulted.
    """
    catalog = read_catalog_project_input(projects_root, project_id)
    if catalog.manifest is None:
        return ShellProjectInput(catalog=catalog, stages=())

    raw_stages = catalog.manifest.get("stages")
    if not isinstance(raw_stages, list):
        # ``load_pipeline_readonly`` already schema-validates.  Keep this
        # defensive boundary explicit in case its producer contract changes.
        return ShellProjectInput(catalog=catalog, stages=())

    observations: list[StageCheckpointInput] = []
    for raw_stage in raw_stages:
        if not isinstance(raw_stage, dict):
            continue
        name = raw_stage.get("name")
        gate = raw_stage.get("human_approval_default", False)
        if not isinstance(name, str) or not name or not isinstance(gate, bool):
            continue
        try:
            checkpoint = read_checkpoint(projects_root, project_id, name)
        except (CheckpointValidationError, OSError, ValueError):
            observations.append(
                StageCheckpointInput(
                    name=name,
                    human_approval_default=gate,
                    checkpoint=None,
                    invalid=True,
                )
            )
            continue
        observations.append(
            StageCheckpointInput(
                name=name,
                human_approval_default=gate,
                checkpoint=checkpoint,
                invalid=False,
            )
        )
    return ShellProjectInput(catalog=catalog, stages=tuple(observations))


__all__ = ["ShellProjectInput", "StageCheckpointInput", "read_shell_project_input"]
