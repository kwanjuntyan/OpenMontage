"""Dynamic fail-closed assertions for the Linux Batch V2 offline CI gate."""

from __future__ import annotations

import argparse
import hashlib
import os
import stat
import sys
import tempfile
from enum import Enum
from pathlib import Path


class GateFailureCategory(str, Enum):
    """Stable, non-sensitive diagnostics for the Linux gate contract."""

    PLATFORM = "platform"
    IDENTITY = "identity"
    PROC_STATUS = "proc_status"
    NO_NEW_PRIVS = "no_new_privs"
    CAP_INH = "cap_inh"
    CAP_PRM = "cap_prm"
    CAP_EFF = "cap_eff"
    CAP_BND = "cap_bnd"
    CAP_AMB = "cap_amb"
    TEMP_LAYOUT = "temp_layout"
    TEMP_ENVIRONMENT = "temp_environment"
    TEMP_WRITE = "temp_write"
    GIT_METADATA = "git_metadata"
    INTERNAL = "internal"


class GateRuntimeContractError(RuntimeError):
    """The isolated test process does not satisfy its runtime contract."""

    def __init__(
        self, category: GateFailureCategory = GateFailureCategory.INTERNAL
    ) -> None:
        if not isinstance(category, GateFailureCategory):
            category = GateFailureCategory.INTERNAL
        self.category = category
        super().__init__("Batch V2 CI assertion failed")


def _is_within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def _resolved_directory(path: Path, category: GateFailureCategory) -> Path:
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise GateRuntimeContractError(category) from exc
    if not resolved.is_dir():
        raise GateRuntimeContractError(category)
    return resolved


def assert_repo_local_temp_layout(
    *, repository: Path, home: Path, os_temp: Path, pytest_basetemp: Path
) -> None:
    """Prove three writable roots are repository-local, disjoint siblings."""
    repository = _resolved_directory(repository, GateFailureCategory.TEMP_LAYOUT)
    roots = tuple(
        _resolved_directory(path, GateFailureCategory.TEMP_LAYOUT)
        for path in (home, os_temp, pytest_basetemp)
    )
    if any(not _is_within(path, repository) for path in roots):
        raise GateRuntimeContractError(GateFailureCategory.TEMP_LAYOUT)
    if len({path.parent for path in roots}) != 1:
        raise GateRuntimeContractError(GateFailureCategory.TEMP_LAYOUT)
    for index, left in enumerate(roots):
        for right in roots[index + 1 :]:
            if _is_within(left, right) or _is_within(right, left):
                raise GateRuntimeContractError(GateFailureCategory.TEMP_LAYOUT)

    configured_home = os.environ.get("HOME")
    configured_temp = os.environ.get("TMPDIR")
    if not configured_home or not configured_temp:
        raise GateRuntimeContractError(GateFailureCategory.TEMP_ENVIRONMENT)
    try:
        resolved_home = Path(configured_home).resolve()
        resolved_temp = Path(configured_temp).resolve()
    except (OSError, RuntimeError, ValueError) as exc:
        raise GateRuntimeContractError(
            GateFailureCategory.TEMP_ENVIRONMENT
        ) from exc
    if resolved_home != roots[0]:
        raise GateRuntimeContractError(GateFailureCategory.TEMP_ENVIRONMENT)
    if resolved_temp != roots[1]:
        raise GateRuntimeContractError(GateFailureCategory.TEMP_ENVIRONMENT)

    previous_tempdir = tempfile.tempdir
    generated_path: Path | None = None
    try:
        tempfile.tempdir = None
        try:
            descriptor, generated_name = tempfile.mkstemp(prefix="batch-v2-gate-")
            os.close(descriptor)
            generated_path = Path(generated_name).resolve(strict=True)
            if not _is_within(generated_path, roots[1]):
                raise GateRuntimeContractError(GateFailureCategory.TEMP_WRITE)
        except GateRuntimeContractError:
            raise
        except Exception as exc:
            raise GateRuntimeContractError(GateFailureCategory.TEMP_WRITE) from exc
    finally:
        if generated_path is not None:
            try:
                generated_path.unlink(missing_ok=True)
            except OSError as exc:
                raise GateRuntimeContractError(GateFailureCategory.TEMP_WRITE) from exc
        tempfile.tempdir = previous_tempdir


def _linux_privilege_state() -> dict[str, str]:
    try:
        lines = Path("/proc/self/status").read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise GateRuntimeContractError(GateFailureCategory.PROC_STATUS) from exc
    return _parse_linux_privilege_state(lines)


def _parse_linux_privilege_state(lines: list[str]) -> dict[str, str]:
    required_fields = {
        "NoNewPrivs",
        "CapInh",
        "CapPrm",
        "CapEff",
        "CapBnd",
        "CapAmb",
    }
    fields: dict[str, str] = {}
    for line in lines:
        key, separator, value = line.partition(":")
        if separator != ":" or key not in required_fields:
            continue
        tokens = value.strip().split()
        if len(tokens) != 1 or key in fields:
            raise GateRuntimeContractError(GateFailureCategory.PROC_STATUS)
        fields[key] = tokens[0]
    if set(fields) != required_fields:
        raise GateRuntimeContractError(GateFailureCategory.PROC_STATUS)
    return fields


def assert_gate_runtime(
    *, repository: Path, home: Path, os_temp: Path, pytest_basetemp: Path
) -> None:
    """Prove no-new-privileges, zero capabilities, and safe temp topology."""
    if sys.platform != "linux":
        raise GateRuntimeContractError(GateFailureCategory.PLATFORM)
    try:
        expected_uid = int(os.environ["BATCH_V2_GATE_UID"])
        expected_gid = int(os.environ["BATCH_V2_GATE_GID"])
    except (KeyError, TypeError, ValueError) as exc:
        raise GateRuntimeContractError(GateFailureCategory.IDENTITY) from exc
    if os.geteuid() != expected_uid or os.getegid() != expected_gid:
        raise GateRuntimeContractError(GateFailureCategory.IDENTITY)

    privilege_state = _linux_privilege_state()
    if privilege_state.get("NoNewPrivs") != "1":
        raise GateRuntimeContractError(GateFailureCategory.NO_NEW_PRIVS)
    capability_categories = {
        "CapInh": GateFailureCategory.CAP_INH,
        "CapPrm": GateFailureCategory.CAP_PRM,
        "CapEff": GateFailureCategory.CAP_EFF,
        "CapBnd": GateFailureCategory.CAP_BND,
        "CapAmb": GateFailureCategory.CAP_AMB,
    }
    for field, category in capability_categories.items():
        try:
            value = int(privilege_state[field], 16)
        except (KeyError, TypeError, ValueError) as exc:
            raise GateRuntimeContractError(GateFailureCategory.PROC_STATUS) from exc
        if value != 0:
            raise GateRuntimeContractError(category)

    assert_repo_local_temp_layout(
        repository=repository,
        home=home,
        os_temp=os_temp,
        pytest_basetemp=pytest_basetemp,
    )


def _hash_tree(hasher: object, path: Path, label: str) -> None:
    try:
        details = path.lstat()
    except FileNotFoundError:
        hasher.update(f"missing:{label}\0".encode())
        return
    file_type = stat.S_IFMT(details.st_mode)
    mode = stat.S_IMODE(details.st_mode)
    hasher.update(f"node:{label}:{file_type:o}:{mode:o}\0".encode())
    if stat.S_ISLNK(details.st_mode):
        hasher.update(os.readlink(path).encode("utf-8", errors="surrogateescape"))
        return
    if stat.S_ISDIR(details.st_mode):
        for child in sorted(path.iterdir(), key=lambda candidate: candidate.name):
            _hash_tree(hasher, child, f"{label}/{child.name}")
        return
    if stat.S_ISREG(details.st_mode):
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                hasher.update(chunk)
        return
    raise GateRuntimeContractError(GateFailureCategory.GIT_METADATA)


def _git_directories(repository: Path) -> tuple[Path, Path]:
    git_entry = repository / ".git"
    if git_entry.is_dir():
        return git_entry, git_entry
    if not git_entry.is_file():
        raise GateRuntimeContractError(GateFailureCategory.GIT_METADATA)
    try:
        marker, separator, raw_path = git_entry.read_text(
            encoding="utf-8"
        ).strip().partition(":")
    except OSError as exc:
        raise GateRuntimeContractError(GateFailureCategory.GIT_METADATA) from exc
    if separator != ":" or marker.strip().lower() != "gitdir":
        raise GateRuntimeContractError(GateFailureCategory.GIT_METADATA)
    git_directory = Path(raw_path.strip())
    if not git_directory.is_absolute():
        git_directory = repository / git_directory
    git_directory = git_directory.resolve(strict=True)
    common_marker = git_directory / "commondir"
    if not common_marker.is_file():
        return git_directory, git_directory
    try:
        common_raw = common_marker.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise GateRuntimeContractError(GateFailureCategory.GIT_METADATA) from exc
    common_directory = Path(common_raw)
    if not common_directory.is_absolute():
        common_directory = git_directory / common_directory
    return git_directory, common_directory.resolve(strict=True)


def git_metadata_digest(repository: Path) -> str:
    """Hash config and hook state without returning paths or file contents."""
    repository = _resolved_directory(repository, GateFailureCategory.GIT_METADATA)
    git_directory, common_directory = _git_directories(repository)
    hasher = hashlib.sha256()
    targets = (
        (git_directory / "config.worktree", "worktree-config"),
        (common_directory / "config", "common-config"),
        (git_directory / "hooks", "worktree-hooks"),
        (common_directory / "hooks", "common-hooks"),
        (repository / ".githooks", "source-hooks"),
    )
    seen: set[Path] = set()
    for path, label in targets:
        normalized = path.absolute()
        if normalized in seen:
            continue
        seen.add(normalized)
        _hash_tree(hasher, path, label)
    return hasher.hexdigest()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers(dest="command", required=True)
    runtime = subparsers.add_parser("gate-runtime", add_help=False)
    runtime.add_argument("--repository", required=True, type=Path)
    runtime.add_argument("--home", required=True, type=Path)
    runtime.add_argument("--os-temp", required=True, type=Path)
    runtime.add_argument("--pytest-basetemp", required=True, type=Path)
    metadata = subparsers.add_parser("git-metadata", add_help=False)
    metadata.add_argument("--workspace", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    failure_category: GateFailureCategory | None = None
    try:
        arguments = _parser().parse_args(argv)
        if arguments.command == "gate-runtime":
            assert_gate_runtime(
                repository=arguments.repository,
                home=arguments.home,
                os_temp=arguments.os_temp,
                pytest_basetemp=arguments.pytest_basetemp,
            )
        else:
            print(git_metadata_digest(arguments.workspace))
    except GateRuntimeContractError as exc:
        failure_category = exc.category
    except Exception:
        failure_category = GateFailureCategory.INTERNAL
    if failure_category is not None:
        print(
            f"ERROR: Batch V2 CI assertion failed [{failure_category.value}]",
            file=sys.stderr,
        )
        return 64
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
