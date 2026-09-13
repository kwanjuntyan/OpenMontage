"""Shared identity and contained-path contracts for local pipeline state."""

from __future__ import annotations

import re
from pathlib import Path


PROJECT_ID_PATTERN = r"^[a-zA-Z0-9_-]+$"
PROJECT_ID_RE = re.compile(PROJECT_ID_PATTERN)


class InvalidProjectIdError(ValueError):
    """Raised before any filesystem operation for an unsafe project id."""


def validate_project_id(project_id: object) -> str:
    """Return a safe, non-empty project-directory component."""
    if not isinstance(project_id, str) or not PROJECT_ID_RE.fullmatch(project_id):
        raise InvalidProjectIdError(
            f"Invalid project_id {project_id!r}; expected pattern {PROJECT_ID_PATTERN!r}"
        )
    return project_id


def resolve_project_dir(root: str | Path, project_id: object) -> Path:
    """Resolve exactly one direct-child project beneath *root*.

    Containment alone is insufficient: ``projects/foo -> projects/bar`` stays
    inside the configured root but lets the name ``foo`` address project
    ``bar``.  Require the resolved directory to retain both its direct parent
    and its declared basename so in-root symlink/junction aliases fail closed.
    """
    safe_project_id = validate_project_id(project_id)
    resolved_root = Path(root).resolve()
    project_dir = (resolved_root / safe_project_id).resolve()
    try:
        project_dir.relative_to(resolved_root)
    except ValueError as exc:
        raise InvalidProjectIdError(
            f"Project path escapes configured projects root: {project_dir}"
        ) from exc
    if project_dir.parent != resolved_root or project_dir.name != safe_project_id:
        raise InvalidProjectIdError(
            "Project path identity changed during resolution: "
            f"expected {resolved_root / safe_project_id}, got {project_dir}"
        )
    return project_dir
