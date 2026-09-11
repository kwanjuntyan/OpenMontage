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


PATTERN_CAT_A = r"^(feat|fix|docs|test|refactor|chore|perf|ci|style|build)(\([\w\-./]+\))?:\s+.{3,}"
PATTERN_CAT_B = r"^(content|data)\([\w\-./]+\):\s+.{3,}"


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


def test_real_hook_allows_deleting_forbidden_files(real_git_repo):
    """Verifies that git rm on a forbidden file (e.g. legacy .mp4) is allowed (R2-4)."""
    repo, _ = real_git_repo
    forbidden = repo / "assets" / "legacy.mp4"
    forbidden.parent.mkdir(parents=True, exist_ok=True)
    forbidden.write_bytes(b"legacy media")

    # Initial commit created bypassing hook via --no-verify
    subprocess.run(["git", "add", "assets/legacy.mp4"], cwd=str(repo), check=True)
    subprocess.run(["git", "commit", "--no-verify", "-m", "Initial commit with legacy file"], cwd=str(repo), check=True)

    # Now delete the legacy file
    subprocess.run(["git", "rm", "assets/legacy.mp4"], cwd=str(repo), check=True)

    # Commit the deletion through the hook
    res = commit_in_repo(repo, "fix(assets): remove legacy mp4 file")
    assert res.returncode == 0, f"Deletion should be allowed, but got error: {res.stderr}"


def test_real_hook_blocks_windows_case_variant(real_git_repo):
    """Verifies that casing variations like 'Projects/' are caught by case-insensitive check (R2-3)."""
    repo, _ = real_git_repo
    p = repo / "Projects" / "c1" / "image.png"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"image data")
    subprocess.run(["git", "add", "Projects/c1/image.png"], cwd=str(repo), check=True)

    res = commit_in_repo(repo, "content(c1): add image")
    assert res.returncode != 0
    assert "資產防護盾" in res.stderr or "二進位防護盾" in res.stderr


def test_real_hook_accepts_unicode_slugs(real_git_repo):
    """Verifies that Chinese/Unicode project IDs in content(...) are accepted by hook regex (R2-5)."""
    repo, _ = real_git_repo
    p = repo / "projects" / "環境ESG" / "project.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('{"id": "esg"}\n', encoding="utf-8")
    subprocess.run(["git", "add", "projects/環境ESG/project.json"], cwd=str(repo), check=True)

    res = commit_in_repo(repo, "content(環境ESG): update environmental pilot project")
    assert res.returncode == 0, f"Unicode slug should be accepted, but got: {res.stderr}"


def test_real_hook_blocks_non_text_in_projects_allowlist(real_git_repo):
    """Verifies that non-text files like .exe or .bin are blocked under projects/ (R2-3)."""
    repo, _ = real_git_repo
    p = repo / "projects" / "c1" / "tool.exe"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"executable payload")
    subprocess.run(["git", "add", "projects/c1/tool.exe"], cwd=str(repo), check=True)

    res = commit_in_repo(repo, "content(c1): add helper tool")
    assert res.returncode != 0
    assert "二進位防護盾" in res.stderr or "純文字" in res.stderr


def test_real_hook_accepts_cjk_extension_unicode_slugs(real_git_repo):
    """Verifies that rare/extension CJK characters like 𠮷 are accepted in commit scopes (R3-Unicode)."""
    repo, _ = real_git_repo
    p = repo / "projects" / "𠮷課程" / "project.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('{"id": "𠮷課程"}\n', encoding="utf-8")
    subprocess.run(["git", "add", "projects/𠮷課程/project.json"], cwd=str(repo), check=True)

    res = commit_in_repo(repo, "content(𠮷課程): 測試罕見漢字與擴展字元")
    assert res.returncode == 0, f"CJK extension character should be accepted, but got: {res.stderr}"


def test_real_hook_blocks_binary_disguised_as_json(real_git_repo):
    """Verifies that binary payloads or NUL bytes disguised as .json in projects/ are blocked (R3-2)."""
    repo, _ = real_git_repo
    p = repo / "projects" / "c1" / "project.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    # Write binary payload with NUL byte disguised as .json
    p.write_bytes(b"{\x00\xff: 'bad'}")
    subprocess.run(["git", "add", "projects/c1/project.json"], cwd=str(repo), check=True)

    res = commit_in_repo(repo, "content(c1): update project metadata")
    assert res.returncode != 0
    assert ("二進位" in res.stderr) or ("JSON" in res.stderr) or ("二進位防護盾" in res.stderr)


def test_unified_policy_checker_staged_and_tree(real_git_repo, tmp_path):
    """Verifies that scripts/check_git_policy.py detects violations in both staged and tree modes (R3-1)."""
    repo, _ = real_git_repo
    checker_script = Path(__file__).resolve().parent.parent.parent / "scripts" / "check_git_policy.py"
    assert checker_script.is_file(), "scripts/check_git_policy.py must exist"

    # Test 1: tree mode clean
    res_clean = subprocess.run([sys.executable, str(checker_script), "--tree"], cwd=str(repo), capture_output=True, encoding="utf-8", errors="replace")
    assert res_clean.returncode == 0

    # Test 2: tree mode catches binary in projects/
    bad_p = repo / "projects" / "c1" / "payload.exe"
    bad_p.parent.mkdir(parents=True, exist_ok=True)
    bad_p.write_bytes(b"bad exe payload")
    res_bad = subprocess.run([sys.executable, str(checker_script), "--tree"], cwd=str(repo), capture_output=True, encoding="utf-8", errors="replace")
    assert res_bad.returncode != 0
    assert "payload.exe" in (res_bad.stderr or "")

    # Test 3: tree mode catches NUL in json
    bad_p.unlink()
    bad_json = repo / "projects" / "c1" / "project.json"
    bad_json.write_bytes(b"{\x00}")
    res_bad_json = subprocess.run([sys.executable, str(checker_script), "--tree"], cwd=str(repo), capture_output=True, encoding="utf-8", errors="replace")
    assert res_bad_json.returncode != 0
    assert "project.json" in (res_bad_json.stderr or "")



