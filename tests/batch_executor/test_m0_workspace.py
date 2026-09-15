from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from lib.batch_executor.contracts import (
    M0ContractError,
    derive_attempt_output_path,
    validate_attempt_output_path,
)


@pytest.fixture()
def project_workspace(tmp_path):
    root = tmp_path / "projects"
    project = root / "project-1"
    project.mkdir(parents=True)
    return root, project


def _derive(root):
    return derive_attempt_output_path(
        root,
        "project-1",
        "batch-1",
        "item-1",
        "attempt-1",
        "clip.mp4",
    )


def test_local_and_cloud_materialized_roots_use_same_project_relative_path(tmp_path):
    local_root = tmp_path / "local" / "projects"
    cloud_root = tmp_path / "cloud-job-workspace" / "projects"
    (local_root / "project-1").mkdir(parents=True)
    (cloud_root / "project-1").mkdir(parents=True)
    local = _derive(local_root)
    cloud = _derive(cloud_root)
    expected = Path(
        ".batch-v2/runs/batch-1/attempts/item-1/attempt-1/clip.mp4"
    )
    assert local.relative_to(local_root / "project-1") == expected
    assert cloud.relative_to(cloud_root / "project-1") == expected
    assert local.is_absolute() and cloud.is_absolute()


def test_attempt_staging_is_outside_every_canonical_backlot_path(project_workspace):
    root, project = project_workspace
    output = _derive(root)
    relative = output.relative_to(project)
    assert relative.parts[0] == ".batch-v2"
    assert relative.parts[0] not in {"artifacts", "assets", "renders", "history"}
    assert not relative.name.startswith("checkpoint_")


def test_only_exact_coordinator_derived_output_path_is_accepted(project_workspace):
    root, project = project_workspace
    expected = _derive(root)
    assert (
        validate_attempt_output_path(
            expected,
            projects_root=root,
            project_id="project-1",
            batch_id="batch-1",
            item_id="item-1",
            attempt_id="attempt-1",
            output_name="clip.mp4",
        )
        == expected
    )
    canonical = project / "assets" / "video" / "clip.mp4"
    with pytest.raises(M0ContractError, match="INVALID_OUTPUT_PATH"):
        validate_attempt_output_path(
            canonical,
            projects_root=root,
            project_id="project-1",
            batch_id="batch-1",
            item_id="item-1",
            attempt_id="attempt-1",
            output_name="clip.mp4",
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("batch_id", ".."),
        ("batch_id", "../escape"),
        ("item_id", "item/escape"),
        ("attempt_id", "C:\\escape"),
        ("output_name", "../../clip.mp4"),
    ],
)
def test_traversal_and_absolute_components_are_rejected(project_workspace, field, value):
    root, _ = project_workspace
    values = {
        "batch_id": "batch-1",
        "item_id": "item-1",
        "attempt_id": "attempt-1",
        "output_name": "clip.mp4",
    }
    values[field] = value
    with pytest.raises(M0ContractError, match="INVALID_PATH_COMPONENT"):
        derive_attempt_output_path(root, "project-1", **values)


def test_relative_system_temp_and_lexical_traversal_candidates_are_rejected(
    project_workspace, tmp_path
):
    root, _ = project_workspace
    kwargs = dict(
        projects_root=root,
        project_id="project-1",
        batch_id="batch-1",
        item_id="item-1",
        attempt_id="attempt-1",
        output_name="clip.mp4",
    )
    with pytest.raises(M0ContractError, match="must be absolute"):
        validate_attempt_output_path("clip.mp4", **kwargs)
    with pytest.raises(M0ContractError, match="WORKSPACE_ESCAPE"):
        validate_attempt_output_path(tmp_path / "detached" / "clip.mp4", **kwargs)
    expected = _derive(root)
    traversing = expected.parent / ".." / "attempt-1" / "clip.mp4"
    with pytest.raises(M0ContractError, match="contains traversal"):
        validate_attempt_output_path(str(traversing), **kwargs)


def _make_directory_link(link: Path, target: Path) -> bool:
    """Create a symlink, falling back to a Windows junction.

    Returns true for a junction so cleanup can use os.rmdir without following
    or recursively deleting its target.
    """

    try:
        link.symlink_to(target, target_is_directory=True)
        return False
    except OSError:
        if sys.platform != "win32":
            pytest.skip("Directory symlink creation is not permitted")
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            pytest.skip(f"Directory link/junction creation is not permitted: {result.stderr}")
        return True


@pytest.mark.parametrize("target_location", ["outside", "canonical"])
def test_symlink_or_junction_in_attempt_path_fails_closed(
    project_workspace, tmp_path, target_location
):
    root, project = project_workspace
    outside = tmp_path / "outside"
    outside.mkdir()
    (project / "assets").mkdir()
    target = outside if target_location == "outside" else project / "assets"
    link = project / ".batch-v2"
    is_junction = _make_directory_link(link, target)
    try:
        with pytest.raises(M0ContractError, match="WORKSPACE_(ESCAPE|ALIAS)"):
            _derive(root)
    finally:
        if is_junction and link.exists():
            os.rmdir(link)
