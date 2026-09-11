# -*- coding: utf-8 -*-
"""Git bootstrap utility for OpenMontage.

Ensures that the team's Git commit-msg hook is automatically installed and
kept up to date on every system startup with zero manual action required.
Supports worktrees, submodules, and standard git repositories.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def get_git_hooks_dir(repo_root: Path) -> Path | None:
    """Discovers the effective git hooks directory via git rev-parse or fallback."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--git-path", "hooks"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=True,
            timeout=2,
        )
        hooks_rel = res.stdout.strip()
        if hooks_rel:
            p = Path(hooks_rel)
            if not p.is_absolute():
                p = (repo_root / p).resolve()
            return p
    except Exception:
        pass

    # Fallback check for standard .git directory or worktree .git file
    git_entry = repo_root / ".git"
    if git_entry.is_dir():
        return git_entry / "hooks"
    elif git_entry.is_file():
        # Linked worktree: read gitdir: <path>
        try:
            content = git_entry.read_text("utf-8").strip()
            if content.startswith("gitdir:"):
                gitdir = Path(content.split(":", 1)[1].strip())
                if not gitdir.is_absolute():
                    gitdir = (repo_root / gitdir).resolve()
                return gitdir / "hooks"
        except Exception:
            pass

    return None


def ensure_git_hooks() -> bool:
    """Installs or updates .githooks/commit-msg to the effective git hooks path.

    Returns True if hooks are successfully installed and verified, False otherwise.
    """
    repo_root = Path(__file__).resolve().parent.parent
    source_hook = repo_root / ".githooks" / "commit-msg"
    if not source_hook.is_file():
        return False

    # Ensure source hook itself has executable bit on POSIX
    try:
        source_hook.chmod(0o755)
    except Exception:
        pass

    target_dir = get_git_hooks_dir(repo_root)
    if not target_dir:
        return False

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        target_hook = target_dir / "commit-msg"

        needs_copy = True
        if target_hook.is_file():
            try:
                if target_hook.read_bytes() == source_hook.read_bytes():
                    needs_copy = False
            except Exception:
                needs_copy = True

        if needs_copy:
            shutil.copyfile(source_hook, target_hook)

        try:
            target_hook.chmod(0o755)
        except Exception:
            pass

        # Also configure core.hooksPath if possible
        try:
            subprocess.run(
                ["git", "config", "core.hooksPath", ".githooks"],
                cwd=str(repo_root),
                capture_output=True,
                check=True,
                timeout=2,
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
