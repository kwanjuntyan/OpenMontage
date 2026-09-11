# -*- coding: utf-8 -*-
"""Git bootstrap utility for OpenMontage.

Ensures that the team's Git commit-msg hook is automatically installed and
kept up to date on every system startup with zero manual action required.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def ensure_git_hooks() -> bool:
    """Installs or updates .githooks/commit-msg to .git/hooks/commit-msg silently.

    Returns True if hooks are successfully installed/verified, False otherwise.
    Never raises an exception (gracefully fails open if Git is not present).
    """
    try:
        repo_root = Path(__file__).resolve().parent.parent
        git_dir = repo_root / ".git"

        # If this is not a Git repo (e.g. running in Docker runtime), skip silently
        if not git_dir.is_dir():
            return False

        source_hook = repo_root / ".githooks" / "commit-msg"
        if not source_hook.is_file():
            return False

        target_dir = git_dir / "hooks"
        target_dir.mkdir(parents=True, exist_ok=True)
        target_hook = target_dir / "commit-msg"

        # Check if already installed with same content
        needs_install = True
        if target_hook.is_file():
            try:
                if target_hook.read_bytes() == source_hook.read_bytes():
                    needs_install = False
            except Exception:
                needs_install = True

        if needs_install:
            shutil.copyfile(source_hook, target_hook)
            try:
                # Add executable permission for POSIX systems
                target_hook.chmod(0o755)
            except Exception:
                pass

        # Also set core.hooksPath to .githooks as double guarantee if git is available
        try:
            subprocess.run(
                ["git", "config", "core.hooksPath", ".githooks"],
                cwd=str(repo_root),
                capture_output=True,
                timeout=1,
            )
        except Exception:
            pass

        return True
    except Exception:
        return False


if __name__ == "__main__":
    if ensure_git_hooks():
        print("[OpenMontage] Git commit-msg hook verified & active.")
    else:
        print("[OpenMontage] Notice: Git hook setup skipped (not a git repo or source missing).")
