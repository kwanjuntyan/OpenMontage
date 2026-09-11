# -*- coding: utf-8 -*-
"""Unit tests for OpenMontage Git commit-msg gatekeeper and smart commit assistant."""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from lib.git_bootstrap import ensure_git_hooks
from scripts.om_commit import generate_course_commit_msg, generate_code_commit_msg


# Patterns mirrored from .githooks/commit-msg
PATTERN_CAT_A = r"^(feat|fix|docs|test|refactor|chore|perf|ci|style|build)(\([a-zA-Z0-9_\-./]+\))?:\s+.{3,}"
PATTERN_CAT_B = r"^(content|data)\([a-zA-Z0-9_\-./]+\):\s+.{3,}"


def is_valid_commit_msg(msg: str) -> bool:
    if msg.startswith("Merge ") or msg.startswith("Revert ") or msg.startswith("Initial commit"):
        return True
    return bool(re.match(PATTERN_CAT_A, msg, re.IGNORECASE) or re.match(PATTERN_CAT_B, msg, re.IGNORECASE))


def test_category_a_valid_formats():
    """Verifies that standard Category A (Code/Tools) commits are accepted."""
    valid_msgs = [
        "feat(cloud): add background gcs auto-sync",
        "fix(backlot): fix video player aspect ratio",
        "docs: update installation instructions",
        "test(gcs): add unit tests for sync worker",
        "refactor(pipeline): clean up stage loader logic",
        "chore(deps): update pytest requirement",
        "perf(render): optimize ffmpeg encoding params",
    ]
    for msg in valid_msgs:
        assert is_valid_commit_msg(msg) is True, f"Failed for valid message: {msg}"


def test_category_b_valid_formats():
    """Verifies that standard Category B (Course Content) commits are accepted."""
    valid_msgs = [
        "content(course-31): update sequence 5 manifests and script",
        "content(esg): approve episode 1 pilot checkpoints",
        "content(prompts): refine deming collage visual style",
        "data(course-31-sequence4-vox): sync shot video manifests",
    ]
    for msg in valid_msgs:
        assert is_valid_commit_msg(msg) is True, f"Failed for valid message: {msg}"


def test_invalid_messages_rejected():
    """Verifies that non-compliant, sloppy commit messages are rejected."""
    invalid_msgs = [
        "update",
        "123",
        "修好了",
        "fixed some bug",
        "content: missing course scope",
        "feat(): empty scope",
        "feat(cloud):",  # too short / empty description
        "wip",
        "tmp",
    ]
    for msg in invalid_msgs:
        assert is_valid_commit_msg(msg) is False, f"Should reject: {msg}"


def test_ensure_git_hooks_installs_correctly(tmp_path, monkeypatch):
    """Verifies that ensure_git_hooks installs hook into .git/hooks."""
    repo = tmp_path / "mock_repo"
    repo.mkdir()
    git_dir = repo / ".git"
    git_dir.mkdir()
    githooks_dir = repo / ".githooks"
    githooks_dir.mkdir()
    source_hook = githooks_dir / "commit-msg"
    source_hook.write_text("#!/bin/sh\necho 'hook active'\n", encoding="utf-8")

    monkeypatch.setattr("lib.git_bootstrap.Path.resolve", lambda self: repo / "lib" / "git_bootstrap.py")

    success = ensure_git_hooks()
    assert success is True
    target_hook = git_dir / "hooks" / "commit-msg"
    assert target_hook.is_file()
    assert target_hook.read_text(encoding="utf-8") == source_hook.read_text(encoding="utf-8")


def test_om_commit_generators():
    """Verifies that om_commit automatically infers the correct commit messages."""
    # Test course content generator
    course_files = [
        "projects/course-31-sequence5-vox/artifacts/script.json",
        "projects/course-31-sequence5-vox/artifacts/asset_manifest.json",
    ]
    msg = generate_course_commit_msg(course_files)
    assert msg.startswith("content(course-31):")
    assert "script" in msg or "manifest" in msg
    assert is_valid_commit_msg(msg) is True

    # Test code generator
    code_files = [
        "lib/gcs_storage.py",
        "tools/video/veo_video.py",
    ]
    code_msg = generate_code_commit_msg(code_files)
    assert code_msg.startswith("feat(")
    assert is_valid_commit_msg(code_msg) is True
