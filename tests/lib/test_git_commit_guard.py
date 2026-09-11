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


def validate_commit(msg: str, staged_files: list[str]) -> tuple[bool, str]:
    """Mirrors the full logic of .githooks/commit-msg (syntax + content awareness)."""
    if msg.startswith("Merge ") or msg.startswith("Revert ") or msg.startswith("Initial commit"):
        return True, "ok"

    is_cat_a = bool(re.match(PATTERN_CAT_A, msg, re.IGNORECASE))
    is_cat_b = bool(re.match(PATTERN_CAT_B, msg, re.IGNORECASE))

    if not is_cat_a and not is_cat_b:
        return False, "invalid_syntax"

    if staged_files:
        BINARY_EXTS = {
            ".mp4", ".mov", ".webm", ".avi", ".mkv",
            ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg",
            ".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".ico",
            ".onnx", ".pth", ".pt", ".bin"
        }
        if any(any(f.lower().endswith(ext) for ext in BINARY_EXTS) for f in staged_files):
            return False, "binary_file_rejected"

        course_files = [f for f in staged_files if f.startswith("projects/")]
        code_files = [f for f in staged_files if not f.startswith("projects/")]

        if course_files and code_files:
            return False, "mixed_commit_rejected"

        if is_cat_b and code_files and not course_files:
            return False, "mismatch_content_with_code"

        if is_cat_a and course_files and not code_files:
            return False, "mismatch_code_with_course"

    return True, "ok"


def test_content_aware_binary_shield():
    """Verifies binary media files are strictly rejected even with valid message."""
    ok, reason = validate_commit("content(course-31): add video", ["projects/course-31/assets/video/sc01.mp4"])
    assert ok is False
    assert reason == "binary_file_rejected"

    ok, reason = validate_commit("feat(ui): add logo", ["assets/logo.png"])
    assert ok is False
    assert reason == "binary_file_rejected"


def test_content_aware_mixed_commits_rejected():
    """Verifies mixing code and course files in one commit is blocked."""
    mixed_files = [
        "lib/gcs_storage.py",
        "projects/course-31-sequence5-vox/artifacts/script.json",
    ]
    ok, reason = validate_commit("feat(cloud): update gcs and course", mixed_files)
    assert ok is False
    assert reason == "mixed_commit_rejected"


def test_content_aware_semantic_mismatch_rejected():
    """Verifies semantic mismatch (calling code changes 'content' or vice-versa) is blocked."""
    # Used content(...) but only modified Python code
    ok, reason = validate_commit("content(course-31): update script", ["lib/gcs_storage.py"])
    assert ok is False
    assert reason == "mismatch_content_with_code"

    # Used feat(...) but only modified course JSON
    ok, reason = validate_commit("feat(pipeline): update script", ["projects/course-31/artifacts/script.json"])
    assert ok is False
    assert reason == "mismatch_code_with_course"


def test_content_aware_valid_cases_pass():
    """Verifies properly classified commits pass both syntax and content checks."""
    # Pure course commit
    ok, reason = validate_commit("content(course-31): update script", ["projects/course-31/artifacts/script.json"])
    assert ok is True
    assert reason == "ok"

    # Pure code commit
    ok, reason = validate_commit("feat(cloud): add background sync", ["lib/gcs_storage.py", "tools/base_tool.py"])
    assert ok is True
    assert reason == "ok"
