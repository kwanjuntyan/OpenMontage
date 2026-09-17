"""Read-only authenticated inputs for the Workspace catalog foundation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from lib.checkpoint import read_project_marker
from lib.identity import InvalidProjectIdError, validate_project_id
from lib.pipeline_loader import load_pipeline_readonly


@dataclass(frozen=True)
class CatalogProjectInput:
    """One authenticated marker paired with its validated selected manifest."""

    project_id: str
    marker: dict[str, Any]
    pipeline_type: str | None
    manifest: dict[str, Any] | None
    manifest_error: str | None


def iter_direct_child_project_ids(projects_root: Path) -> Iterable[str]:
    """Yield lexical direct-child candidate names without assigning identity.

    Each candidate is later resolved through ``read_project_marker``; a
    directory name by itself is never emitted as a catalog project identity.
    """
    root = Path(projects_root).resolve()
    if not root.exists() or not root.is_dir():
        return
    for child in sorted(root.iterdir(), key=lambda value: value.name):
        try:
            yield validate_project_id(child.name)
        except InvalidProjectIdError:
            continue


def read_catalog_project_input(
    projects_root: Path, project_id: str
) -> CatalogProjectInput:
    """Read an authenticated marker and its manifest, if the latter validates.

    A marker-authenticated project remains observable as a degraded catalog
    input when its selected manifest is missing or invalid.
    """
    marker = read_project_marker(Path(projects_root), project_id)
    pipeline_type = marker.get("pipeline_type")
    if not isinstance(pipeline_type, str) or not pipeline_type or pipeline_type == "unknown":
        return CatalogProjectInput(
            project_id=project_id,
            marker=marker,
            pipeline_type=None,
            manifest=None,
            manifest_error="pipeline_manifest_unavailable",
        )
    try:
        manifest = load_pipeline_readonly(pipeline_type)
    except Exception:
        return CatalogProjectInput(
            project_id=project_id,
            marker=marker,
            pipeline_type=pipeline_type,
            manifest=None,
            manifest_error="pipeline_manifest_invalid",
        )
    if not isinstance(manifest, dict):
        return CatalogProjectInput(
            project_id=project_id,
            marker=marker,
            pipeline_type=pipeline_type,
            manifest=None,
            manifest_error="pipeline_manifest_invalid",
        )
    return CatalogProjectInput(
        project_id=project_id,
        marker=marker,
        pipeline_type=pipeline_type,
        manifest=manifest,
        manifest_error=None,
    )


__all__ = [
    "CatalogProjectInput",
    "iter_direct_child_project_ids",
    "read_catalog_project_input",
]
