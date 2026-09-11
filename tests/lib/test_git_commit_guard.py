# -*- coding: utf-8 -*-
"""Unit and black-box integration tests for OpenMontage Git commit-msg gatekeeper."""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from lib.git_bootstrap import ensure_git_hooks, get_git_hooks_dir
from scripts.om_commit import generate_course_commit_msg, generate_code_commit_msg, get_git_status


PATTERN_CAT_A = r"^(feat|fix|docs|test|refactor|chore|perf|ci|style|build)(\([a-zA-Z0-9_\-./]+\))?:\s+.{3,}"
PATTERN_CAT_B = r"^(content|data)\([a-zA-Z0-9_\-./]+\):\s+.{3,}"


def is_valid_commit_syntax(msg: str) -> bool:
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
        assert is_valid_commit_syntax(msg) is True, f"Failed for valid message: {msg}"


def test_category_b_valid_formats():
    """Verifies that standard Category B (Course Content) commits are accepted."""
    valid_msgs = [
        "content(course-31): update sequence 5 manifests and script",
        "content(esg): approve episode 1 pilot checkpoints",
        "content(prompts): refine deming collage visual style",
        "data(course-31-sequence4-vox): sync shot video manifests",
    ]
    for msg in valid_msgs:
        assert is_valid_commit_syntax(msg) is True, f"Failed for valid message: {msg}"


def test_invalid_messages_rejected():
    """Verifies that non-compliant commit messages fail syntax validation."""
    invalid_msgs = [
        "update",
        "123",
        "修好了",
        "fixed some bug",
        "content: missing course scope",
        "feat(): empty scope",
        "feat(cloud):",
        "wip",
        "tmp",
    ]
    for msg in invalid_msgs:
        assert is_valid_commit_syntax(msg) is False, f"Should reject: {msg}"


def test_om_commit_generators():
    """Verifies that om_commit automatically infers the correct commit messages."""
    course_files = [
        "projects/course-31-sequence5-vox/artifacts/script.json",
        "projects/course-31-sequence5-vox/artifacts/asset_manifest.json",
    ]
    msg = generate_course_commit_msg(course_files)
    assert msg.startswith("content(course-31):")

    code_files = [
        "lib/gcs_storage.py",
        "tests/lib/test_gcs_auto_sync.py",
    ]
    code_msg = generate_code_commit_msg(code_files)
    assert code_msg.startswith("test(") or code_msg.startswith("feat(")


# --------------------------------------------------------------------------
# Black-Box Integration Tests: Running the Real Hook Against a Real Git Repo
# --------------------------------------------------------------------------

@pytest.fixture
def real_git_repo(tmp_path):
    """Creates a genuine temporary git repo configured with the real commit-msg hook."""
    repo = tmp_path / "sandbox_repo"
    repo.mkdir()

    # Initialize git
    subprocess.run(["git", "init"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "tester@openmontage.org"], cwd=str(repo), check=True)
    subprocess.run(["git", "config", "user.name", "Tester"], cwd=str(repo), check=True)

    # Copy the real .githooks/commit-msg
    real_hook_source = Path(__file__).resolve().parent.parent.parent / ".githooks" / "commit-msg"
    hooks_dir = repo / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    target_hook = hooks_dir / "commit-msg"
    shutil.copyfile(real_hook_source, target_hook)
    try:
        target_hook.chmod(0o755)
    except Exception:
        pass

    return repo, target_hook


def commit_in_repo(repo: Path, msg: str) -> subprocess.CompletedProcess:
    """Invokes git commit inside the test repository."""
    return subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=str(repo),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def test_real_hook_happy_paths(real_git_repo):
    """Verifies that valid Category A and Category B commits succeed with real hook."""
    repo, _ = real_git_repo

    # 1. Category A
    code_file = repo / "lib" / "helper.py"
    code_file.parent.mkdir(parents=True, exist_ok=True)
    code_file.write_text("x = 1\n", encoding="utf-8")
    subprocess.run(["git", "add", "lib/helper.py"], cwd=str(repo), check=True)

    res = commit_in_repo(repo, "feat(core): add helper module")
    assert res.returncode == 0, f"Expected success but got: {res.stderr}"

    # 2. Category B
    course_file = repo / "projects" / "c1" / "project.json"
    course_file.parent.mkdir(parents=True, exist_ok=True)
    course_file.write_text('{"id": "c1"}\n', encoding="utf-8")
    subprocess.run(["git", "add", "projects/c1/project.json"], cwd=str(repo), check=True)

    res = commit_in_repo(repo, "content(c1): create project recipe")
    assert res.returncode == 0, f"Expected success but got: {res.stderr}"


def test_real_hook_blocks_empty_message(real_git_repo):
    """Verifies that empty commit message is strictly blocked (Fail-Closed)."""
    repo, _ = real_git_repo
    f = repo / "lib" / "a.py"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("a = 1\n")
    subprocess.run(["git", "add", "lib/a.py"], cwd=str(repo), check=True)

    res = commit_in_repo(repo, "")
    assert res.returncode != 0
    assert "Commit 訊息不能為空" in res.stderr or "Aborting commit due to empty commit message" in res.stderr


def test_real_hook_blocks_special_commit_with_binary_shield(real_git_repo):
    """Verifies that 'Merge ...' or special messages CANNOT bypass the binary shield."""
    repo, _ = real_git_repo
    media = repo / "projects" / "c1" / "assets" / "video" / "test.mp4"
    media.parent.mkdir(parents=True, exist_ok=True)
    media.write_bytes(b"fake mp4 stream")
    subprocess.run(["git", "add", "projects/c1/assets/video/test.mp4"], cwd=str(repo), check=True)

    # Attempt bypass with Merge message
    res = commit_in_repo(repo, "Merge branch 'feature' into main")
    assert res.returncode != 0
    assert "二進位防護盾" in res.stderr


def test_real_hook_blocks_unicode_quoted_path_media(real_git_repo):
    """Verifies that Chinese/Unicode paths outputted with C-style quotes by Git are caught."""
    repo, _ = real_git_repo
    media = repo / "projects" / "課程A" / "assets" / "測試.mp4"
    media.parent.mkdir(parents=True, exist_ok=True)
    media.write_bytes(b"fake video")
    subprocess.run(["git", "add", "."], cwd=str(repo), check=True)

    res = commit_in_repo(repo, "content(course-a): add intro video")
    assert res.returncode != 0
    assert "二進位防護盾" in res.stderr


def test_real_hook_blocks_mixed_commits(real_git_repo):
    """Verifies that staging both code and projects/ in one commit is blocked."""
    repo, _ = real_git_repo
    (repo / "lib").mkdir(parents=True, exist_ok=True)
    (repo / "lib" / "foo.py").write_text("def foo(): pass\n")

    (repo / "projects" / "c1").mkdir(parents=True, exist_ok=True)
    (repo / "projects" / "c1" / "project.json").write_text("{}\n")

    subprocess.run(["git", "add", "lib/foo.py", "projects/c1/project.json"], cwd=str(repo), check=True)

    res = commit_in_repo(repo, "feat(core): update core and course")
    assert res.returncode != 0
    assert "混雜提交" in res.stderr


def test_real_hook_blocks_semantic_mismatches(real_git_repo):
    """Verifies that calling code 'content' or calling projects 'feat' is blocked."""
    repo, _ = real_git_repo
    (repo / "lib").mkdir(parents=True, exist_ok=True)
    (repo / "lib" / "code.py").write_text("x = 1\n")
    subprocess.run(["git", "add", "lib/code.py"], cwd=str(repo), check=True)

    # Only code staged, but using Category B content message
    res = commit_in_repo(repo, "content(c1): update script")
    assert res.returncode != 0
    assert "名實不符阻斷" in res.stderr

    # Unstage code.py
    subprocess.run(["git", "rm", "-f", "-r", "--cached", "."], cwd=str(repo), check=True)

    # Only project staged, but using Category A feat message
    (repo / "projects" / "c1").mkdir(parents=True, exist_ok=True)
    (repo / "projects" / "c1" / "script.json").write_text("{}\n")
    subprocess.run(["git", "add", "projects/c1/script.json"], cwd=str(repo), check=True)

    res = commit_in_repo(repo, "feat(core): update script engine")
    assert res.returncode != 0
    assert "名實不符阻斷" in res.stderr
