"""Immutable Cloud input snapshot materialization into an ephemeral workspace."""

from __future__ import annotations

import hashlib
import os
import shutil
import stat
import tempfile
from pathlib import Path

from .errors import M1ExecutionError


def validate_snapshot_roots(
    *, projects_root: str | Path, snapshot_projects_root: str | Path
) -> tuple[Path, Path]:
    """Require physically and lexically disjoint input/output namespaces."""

    output = Path(projects_root)
    snapshot = Path(snapshot_projects_root)
    if not output.is_absolute() or not snapshot.is_absolute():
        raise M1ExecutionError(
            "RUNTIME_CONFIG_INVALID", "Snapshot and workspace roots must be absolute"
        )
    output = Path(os.path.abspath(output))
    snapshot = Path(os.path.abspath(snapshot))
    if os.path.normcase(str(output)) == os.path.normcase(str(snapshot)):
        raise M1ExecutionError(
            "WORKSPACE_SNAPSHOT_ALIAS",
            "Immutable input snapshot cannot be the writable project workspace",
        )
    for child, parent in ((output, snapshot), (snapshot, output)):
        try:
            child.relative_to(parent)
        except ValueError:
            continue
        raise M1ExecutionError(
            "WORKSPACE_SNAPSHOT_ALIAS",
            "Snapshot and writable project namespaces cannot contain one another",
        )
    return output, snapshot


def _digest(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def materialize_project_snapshot(
    *,
    projects_root: str | Path,
    snapshot_projects_root: str | Path,
    project_id: str,
    exclude_assets_publication_outputs: bool = False,
) -> Path:
    """Copy one read-only frozen project snapshot without overwriting conflicts.

    The destination is the container's ephemeral `/workspace/projects` tree;
    the source is a disjoint read-only GCS FUSE `only-dir` mount.  Generated
    `.batch-v2` state is never accepted from the snapshot.
    """

    output_root, snapshot_root = validate_snapshot_roots(
        projects_root=projects_root,
        snapshot_projects_root=snapshot_projects_root,
    )
    source = snapshot_root / project_id
    destination = output_root / project_id
    try:
        source_resolved = source.resolve(strict=True)
        snapshot_resolved = snapshot_root.resolve(strict=True)
        source_resolved.relative_to(snapshot_resolved)
    except (OSError, ValueError) as exc:
        raise M1ExecutionError(
            "WORKSPACE_SNAPSHOT_INVALID", "Exact immutable project snapshot is missing"
        ) from exc
    if source_resolved != Path(os.path.abspath(source)) or not source.is_dir():
        raise M1ExecutionError(
            "WORKSPACE_SNAPSHOT_INVALID", "Snapshot project path is aliased"
        )
    output_root.mkdir(parents=True, exist_ok=True)
    if output_root.resolve(strict=True) != Path(os.path.abspath(output_root)):
        raise M1ExecutionError(
            "WORKSPACE_SNAPSHOT_ALIAS", "Writable workspace root is aliased"
        )
    destination.mkdir(parents=True, exist_ok=True)
    for root, directories, files in os.walk(source, topdown=True, followlinks=False):
        root_path = Path(root)
        safe_directories = []
        for name in sorted(directories):
            if name == ".batch-v2" or (
                exclude_assets_publication_outputs
                and root_path == source
                and name == "assets"
            ):
                continue
            candidate = root_path / name
            mode = candidate.stat(follow_symlinks=False).st_mode
            if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
                raise M1ExecutionError(
                    "WORKSPACE_SNAPSHOT_INVALID", "Snapshot contains a directory alias"
                )
            safe_directories.append(name)
        directories[:] = safe_directories
        relative = root_path.relative_to(source)
        target_directory = destination / relative
        target_directory.mkdir(parents=True, exist_ok=True)
        if target_directory.resolve(strict=True) != Path(
            os.path.abspath(target_directory)
        ):
            raise M1ExecutionError(
                "WORKSPACE_SNAPSHOT_ALIAS", "Writable project subtree is aliased"
            )
        for name in sorted(files):
            if (
                exclude_assets_publication_outputs
                and root_path == source
                and name == "checkpoint_assets.json"
            ):
                continue
            source_file = root_path / name
            mode = source_file.stat(follow_symlinks=False).st_mode
            if (
                stat.S_ISLNK(mode)
                or not stat.S_ISREG(mode)
                or source_file.stat().st_nlink > 1
            ):
                raise M1ExecutionError(
                    "WORKSPACE_SNAPSHOT_INVALID",
                    "Snapshot contains an unsafe file alias",
                )
            target = target_directory / name
            expected = _digest(source_file)
            if target.exists():
                target_mode = target.stat(follow_symlinks=False).st_mode
                if (
                    stat.S_ISLNK(target_mode)
                    or not stat.S_ISREG(target_mode)
                    or target.stat().st_nlink > 1
                    or _digest(target) != expected
                ):
                    raise M1ExecutionError(
                        "WORKSPACE_SNAPSHOT_CONFLICT",
                        "Writable workspace contains data different from the frozen snapshot",
                    )
                continue
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{name}.", suffix=".tmp", dir=target_directory
            )
            os.close(descriptor)
            temporary = Path(temporary_name)
            try:
                shutil.copyfile(source_file, temporary)
                if _digest(temporary) != expected:
                    raise M1ExecutionError(
                        "WORKSPACE_SNAPSHOT_INVALID", "Snapshot copy changed bytes"
                    )
                try:
                    os.link(temporary, target)
                except FileExistsError:
                    if _digest(target) != expected:
                        raise M1ExecutionError(
                            "WORKSPACE_SNAPSHOT_CONFLICT",
                            "Concurrent snapshot materialization differs",
                        )
            finally:
                temporary.unlink(missing_ok=True)
    return destination.resolve(strict=True)


__all__ = ["materialize_project_snapshot", "validate_snapshot_roots"]
