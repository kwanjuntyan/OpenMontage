"""Resolve and verify the Batch V2 lock on its exact release interpreter.

This command is intentionally run during the network-enabled dependency setup
phase of Linux CI.  The later Batch V2 pytest process remains no-egress.  The
Docker build independently installs the same exact pins and remains the image
qualification gate.
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import unquote, urlsplit


_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_REQUIREMENTS_PATH = _REPOSITORY_ROOT / "requirements-batch-v2.txt"
_CONSTRAINTS_PATH = _REPOSITORY_ROOT / "constraints-batch-v2-py310.txt"
_EXACT_PIN = re.compile(
    r"(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)=="
    r"(?P<version>[A-Za-z0-9][A-Za-z0-9.!+_-]*)"
)
_SHA256 = re.compile(r"[0-9a-f]{64}")
_TARGET_MACHINES = frozenset({"amd64", "x86_64"})


class LockVerificationError(RuntimeError):
    """The candidate lock is not proven for CPython 3.10/Linux x86_64."""


def _canonical_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def load_exact_pins(path: Path) -> dict[str, str]:
    """Load an exact, duplicate-free requirement/constraint file."""

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise LockVerificationError("unable to read the exact dependency pins") from exc
    pins: dict[str, str] = {}
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = _EXACT_PIN.fullmatch(line)
        if match is None:
            raise LockVerificationError("dependency files must contain exact pins only")
        name = _canonical_name(match.group("name"))
        if name in pins:
            raise LockVerificationError("dependency files contain a duplicate pin")
        pins[name] = match.group("version")
    if not pins:
        raise LockVerificationError("dependency files contain no exact pins")
    return pins


def _assert_report_environment(environment: Mapping[str, Any]) -> None:
    python_full_version = environment.get("python_full_version")
    if (
        environment.get("implementation_name") != "cpython"
        or not isinstance(python_full_version, str)
        or not python_full_version.startswith("3.10.")
    ):
        raise LockVerificationError("resolver report must come from CPython 3.10")
    machine = environment.get("platform_machine")
    if (
        environment.get("sys_platform") != "linux"
        or not isinstance(machine, str)
        or machine.lower() not in _TARGET_MACHINES
    ):
        raise LockVerificationError("resolver report must come from Linux x86_64")


def validate_resolver_report(
    report: Mapping[str, Any],
    *,
    requirements_path: Path = _REQUIREMENTS_PATH,
    constraints_path: Path = _CONSTRAINTS_PATH,
) -> dict[str, str]:
    """Verify that pip selected the complete exact binary-wheel closure."""

    if report.get("version") != "1":
        raise LockVerificationError("unsupported pip resolver report version")
    environment = report.get("environment")
    if not isinstance(environment, Mapping):
        raise LockVerificationError("resolver report must include its environment")
    _assert_report_environment(environment)

    requirements = load_exact_pins(requirements_path)
    constraints = load_exact_pins(constraints_path)
    if any(constraints.get(name) != version for name, version in requirements.items()):
        raise LockVerificationError("direct dependency pins must match the constraints")

    installations = report.get("install")
    if not isinstance(installations, list) or not installations:
        raise LockVerificationError(
            "resolver report does not contain the complete exact constraint closure"
        )
    selected: dict[str, str] = {}
    for installation in installations:
        if not isinstance(installation, Mapping):
            raise LockVerificationError("resolver report contains an invalid entry")
        metadata = installation.get("metadata")
        download = installation.get("download_info")
        if not isinstance(metadata, Mapping) or not isinstance(download, Mapping):
            raise LockVerificationError("resolver report contains an invalid entry")
        raw_name = metadata.get("name")
        version = metadata.get("version")
        if not isinstance(raw_name, str) or not isinstance(version, str):
            raise LockVerificationError("resolver report contains an invalid entry")
        name = _canonical_name(raw_name)
        if name in selected:
            raise LockVerificationError("resolver report contains a duplicate distribution")

        url = download.get("url")
        if (
            not isinstance(url, str)
            or not unquote(urlsplit(url).path).lower().endswith(".whl")
        ):
            raise LockVerificationError(
                "every resolved distribution must have a binary wheel"
            )
        archive_info = download.get("archive_info")
        hashes = archive_info.get("hashes") if isinstance(archive_info, Mapping) else None
        sha256 = hashes.get("sha256") if isinstance(hashes, Mapping) else None
        if not isinstance(sha256, str) or _SHA256.fullmatch(sha256) is None:
            raise LockVerificationError(
                "every resolved wheel must carry a lowercase SHA-256"
            )
        selected[name] = version

    if selected != constraints:
        raise LockVerificationError(
            "resolver report does not contain the complete exact constraint closure"
        )
    return selected


def build_resolver_command(
    *,
    report_path: Path,
    requirements_path: Path = _REQUIREMENTS_PATH,
    constraints_path: Path = _CONSTRAINTS_PATH,
    python_executable: str = sys.executable,
) -> list[str]:
    """Build the pip command used by the real CPython 3.10 Linux gate."""

    return [
        python_executable,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--no-cache-dir",
        "--no-input",
        "--dry-run",
        "--ignore-installed",
        "--only-binary=:all:",
        "--report",
        str(report_path),
        "--constraint",
        str(constraints_path),
        "--requirement",
        str(requirements_path),
    ]


def _assert_target_runtime() -> None:
    machine = platform.machine().lower()
    if sys.implementation.name != "cpython" or sys.version_info[:2] != (3, 10):
        raise LockVerificationError("lock resolution requires CPython 3.10")
    if sys.platform != "linux" or machine not in _TARGET_MACHINES:
        raise LockVerificationError("lock resolution requires Linux x86_64")


def resolve_lock() -> int:
    """Run pip's real resolver, then bind its complete report to the lock."""

    _assert_target_runtime()
    with tempfile.TemporaryDirectory(prefix="batch-v2-py310-lock-") as temp_root:
        report_path = Path(temp_root) / "resolver-report.json"
        completed = subprocess.run(
            build_resolver_command(report_path=report_path),
            check=False,
        )
        if completed.returncode != 0:
            raise LockVerificationError("pip could not resolve the Batch V2 lock")
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise LockVerificationError("pip did not produce a valid resolver report") from exc
        if not isinstance(report, Mapping):
            raise LockVerificationError("pip did not produce a valid resolver report")
        selected = validate_resolver_report(report)
    return len(selected)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="batch_v2_verify_py310_lock")
    parser.add_argument("command", choices=("resolve",))
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "resolve":
            package_count = resolve_lock()
    except LockVerificationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 64
    print(
        "Batch V2 lock resolved for CPython 3.10/Linux x86_64: "
        f"{package_count} distributions"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


__all__ = [
    "LockVerificationError",
    "build_resolver_command",
    "load_exact_pins",
    "main",
    "resolve_lock",
    "validate_resolver_report",
]
