"""Fail-closed, name-only credential-material preflight for the M4 CI gate."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


_PRUNED_DIRECTORIES = frozenset({".git", ".venv", ".pytest-tmp", "node_modules"})
_SECRET_SUFFIXES = (".pem", ".p12", ".key")
_JSON_SECRET_MARKERS = (
    "credential",
    "service-account",
    "service_account",
    "client-secret",
    "client_secret",
)


class WorkspaceCredentialMaterialError(RuntimeError):
    """The test checkout may expose credential material to imported code."""


def _sensitive_name(name: str) -> bool:
    lower = name.lower()
    if lower == ".env.example":
        return False
    if lower == ".env" or lower.startswith(".env."):
        return True
    if lower.endswith(_SECRET_SUFFIXES):
        return True
    return lower.endswith(".json") and any(
        marker in lower for marker in _JSON_SECRET_MARKERS
    )


def assert_uncredentialed_workspace(workspace: Path) -> None:
    """Inspect file names only; never open or expose a candidate's contents/path."""
    root = workspace.resolve(strict=True)
    if not root.is_dir():
        raise WorkspaceCredentialMaterialError(
            "unable to inspect the test workspace safely"
        )

    def fail_walk(_error: OSError) -> None:
        raise WorkspaceCredentialMaterialError(
            "unable to inspect the test workspace safely"
        )

    for _directory, child_directories, file_names in os.walk(
        root, followlinks=False, onerror=fail_walk
    ):
        child_directories[:] = [
            name for name in child_directories if name not in _PRUNED_DIRECTORIES
        ]
        if any(_sensitive_name(name) for name in file_names):
            raise WorkspaceCredentialMaterialError(
                "sensitive credential material exists in the test workspace"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--workspace", required=True, type=Path)
    try:
        args = parser.parse_args(argv)
        assert_uncredentialed_workspace(args.workspace)
    except Exception:
        print(
            "ERROR: sensitive credential material exists in the test workspace",
            file=sys.stderr,
        )
        return 64
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
