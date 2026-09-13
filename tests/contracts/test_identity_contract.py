"""Shared project identity and contained-path regression contracts."""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from lib.identity import InvalidProjectIdError, PROJECT_ID_PATTERN, resolve_project_dir


@pytest.mark.parametrize("project_id", ["..", "../escape", "sub/project", "C:\\escape", "", False])
def test_project_id_rejected_before_resolution(tmp_path, project_id) -> None:
    with pytest.raises(InvalidProjectIdError):
        resolve_project_dir(tmp_path, project_id)


def test_clp_and_checkpoint_schemas_share_runtime_project_id_pattern() -> None:
    from lib.checkpoint import CHECKPOINT_SCHEMA_PATH
    from schemas.artifacts import load_schema

    checkpoint = json.loads(CHECKPOINT_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert checkpoint["properties"]["project_id"]["pattern"] == PROJECT_ID_PATTERN
    for artifact_name in ("clp_manifest", "clp_candidates", "clp_shot_bindings"):
        schema = load_schema(artifact_name)
        assert schema["properties"]["project_id"]["pattern"] == PROJECT_ID_PATTERN


def test_existing_project_symlink_or_junction_cannot_escape_root(tmp_path) -> None:
    outside = tmp_path / "outside"
    root = tmp_path / "projects"
    outside.mkdir()
    root.mkdir()
    link = root / "escaped"
    is_junction = False
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        if sys.platform != "win32":
            pytest.skip("Directory link creation is not permitted in this environment")
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(outside)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            pytest.fail(f"Could not create Windows junction probe: {result.stderr or result.stdout}")
        is_junction = True

    try:
        with pytest.raises(InvalidProjectIdError, match="escapes"):
            resolve_project_dir(root, "escaped")
    finally:
        if is_junction and link.exists():
            os.rmdir(link)


def test_existing_project_symlink_or_junction_cannot_alias_sibling(tmp_path) -> None:
    """An in-root alias must not let project ``alias`` read project ``real``."""
    root = tmp_path / "projects"
    target = root / "real"
    target.mkdir(parents=True)
    link = root / "alias"
    is_junction = False
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        if sys.platform != "win32":
            pytest.skip("Directory link creation is not permitted in this environment")
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            pytest.fail(f"Could not create Windows junction probe: {result.stderr or result.stdout}")
        is_junction = True

    try:
        with pytest.raises(InvalidProjectIdError, match="identity changed"):
            resolve_project_dir(root, "alias")
    finally:
        if is_junction and link.exists():
            os.rmdir(link)
