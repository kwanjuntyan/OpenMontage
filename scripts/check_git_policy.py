# -*- coding: utf-8 -*-
"""OpenMontage Unified Git Policy Checker.

Used by both:
  1. Local client-side hook (.githooks/commit-msg)
  2. Remote GitHub Actions CI (.github/workflows/ci.yml)

Ensures 100% DRY consistency between local guardrails and remote enforcement.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import PurePosixPath

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ALLOWED_EXTS = {
    ".json", ".yaml", ".yml", ".md", ".txt",
    ".srt", ".vtt", ".tsv", ".csv",
    ".html", ".js", ".css"
}

REPO_FORBIDDEN_EXTS = {
    ".mp4", ".mov", ".webm", ".avi", ".mkv",
    ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg",
    ".onnx", ".pth", ".pt", ".bin", ".safetensors", ".ckpt",
    ".tar", ".gz", ".7z", ".rar", ".zip", ".exe", ".dll", ".so"
}

MAX_BLOB_BYTES = 15 * 1024 * 1024  # 15 MB


def is_project_path(path_str: str) -> bool:
    """Case-insensitive check for projects/ directory."""
    return path_str.replace("\\", "/").lower().startswith("projects/")


def check_staged_content(commit_msg: str = "") -> int:
    """Checks staged files in git index (used by commit-msg hook)."""
    try:
        # 1. Get all staged files (including deletions for category check)
        res_all = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "-z"],
            capture_output=True,
            check=True
        )
        all_staged = [
            os.fsdecode(p).replace("\\", "/").strip()
            for p in res_all.stdout.split(b"\0") if p
        ]

        if not all_staged:
            return 0

        # 2. Get added or modified files (excluding deletions 'D')
        res_am = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
            capture_output=True,
            check=True
        )
        added_or_modified = [
            os.fsdecode(p).replace("\\", "/").strip()
            for p in res_am.stdout.split(b"\0") if p
        ]

    except subprocess.CalledProcessError as e:
        print(f"[X] Git diff 指令失敗 (code {e.returncode})，阻斷提交！", file=sys.stderr)
        return 1

    # Check Added/Modified files against policies
    bad_files = []
    for f in added_or_modified:
        posix = PurePosixPath(f)
        suffix = posix.suffix.lower()

        # Rule 1: projects/ strict allowlist
        if is_project_path(f):
            if suffix not in PROJECT_ALLOWED_EXTS:
                bad_files.append((f, f"projects/ 目錄僅允許純文字配方，不允許 '{suffix or '無副檔名'}'"))
            elif suffix == ".json":
                # Quick validation: ensure valid UTF-8 & valid JSON structure (no binary payload disguise)
                try:
                    show_res = subprocess.run(
                        ["git", "show", f":{f}"],
                        capture_output=True,
                        check=True
                    )
                    content = show_res.stdout.decode("utf-8")
                    if "\0" in content:
                        bad_files.append((f, "JSON 檔案內含二進位 NUL 字元，禁止提交"))
                    else:
                        json.loads(content)
                except Exception:
                    bad_files.append((f, "無效的 JSON 內容或非 UTF-8 二進位檔"))
        # Rule 2: repo-wide forbidden binary media/weights
        elif suffix in REPO_FORBIDDEN_EXTS:
            bad_files.append((f, "全代碼庫禁止提交影片、音訊、模型權重或大型壓縮檔"))

    if bad_files:
        print("\n" + "=" * 70, file=sys.stderr)
        print("[X] [OpenMontage 規範守門員 - 二進位防護盾] 禁止提交非合規/多媒體檔案！", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        for b, reason in bad_files[:5]:
            print(f"  * {b} ({reason})", file=sys.stderr)
        if len(bad_files) > 5:
            print(f"  * ... 還有另外 {len(bad_files) - 5} 個檔案", file=sys.stderr)
        print("\n[!] 規範說明：所有媒體資產請存於 GCS 雲端儲存庫，Git 僅保留純文字配方。", file=sys.stderr)
        print("=" * 70 + "\n", file=sys.stderr)
        return 1

    # Check blob size limit (>15MB)
    if added_or_modified:
        try:
            ls_res = subprocess.run(["git", "ls-files", "-s", "-z"], capture_output=True, check=True)
            for entry in ls_res.stdout.split(b"\0"):
                if not entry:
                    continue
                parts = entry.split(b"\t", 1)
                if len(parts) == 2:
                    meta, path_b = parts
                    p_str = os.fsdecode(path_b).replace("\\", "/").strip()
                    if p_str in added_or_modified:
                        sha = meta.split()[1].decode("ascii")
                        s_res = subprocess.run(["git", "cat-file", "-s", sha], capture_output=True, text=True, check=True)
                        if s_res.stdout.strip().isdigit() and int(s_res.stdout.strip()) > MAX_BLOB_BYTES:
                            print(f"\n[X] [OpenMontage 守門員] 檔案超過 15MB: {p_str}", file=sys.stderr)
                            return 1
        except subprocess.CalledProcessError:
            return 1

    # Rule 3: No Mixed Commits (case-insensitive)
    course_files = [f for f in all_staged if is_project_path(f)]
    code_files = [f for f in all_staged if not is_project_path(f)]
    if course_files and code_files:
        print("\n" + "=" * 70, file=sys.stderr)
        print("[X] [OpenMontage 規範守門員 - 分類檢驗] 偵測到「混雜提交」！", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        print(f"系統程式碼 ({len(code_files)} 個) 與 課程配方 ({len(course_files)} 個) 不能同次提交！", file=sys.stderr)
        print("請使用: python scripts/om_commit.py 分批打包。", file=sys.stderr)
        print("=" * 70 + "\n", file=sys.stderr)
        return 1

    return 0


def check_tree_content(repo_dir: str = ".") -> int:
    """Scans repository tree on CI (used by GitHub Actions)."""
    violations = []
    projects_dir = os.path.join(repo_dir, "projects")

    # Check projects directory
    for root, _, files in os.walk(repo_dir):
        rel_root = os.path.relpath(root, repo_dir).replace("\\", "/")
        if rel_root.startswith(".git"):
            continue

        in_projects = is_project_path(rel_root)

        for fname in files:
            fpath = os.path.join(rel_root, fname).replace("\\", "/")
            posix = PurePosixPath(fpath)
            suffix = posix.suffix.lower()

            if in_projects:
                if suffix not in PROJECT_ALLOWED_EXTS:
                    violations.append(f"{fpath} (projects/ 目錄不允許非純文字: '{suffix}')")
                elif suffix == ".json":
                    full_path = os.path.join(root, fname)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            if "\0" in content:
                                violations.append(f"{fpath} (內含二進位 NUL 字元)")
                            else:
                                json.loads(content)
                    except Exception:
                        violations.append(f"{fpath} (無效的 JSON 或二進位檔)")
            elif suffix in REPO_FORBIDDEN_EXTS:
                violations.append(f"{fpath} (全庫禁止媒體/權重檔案)")

            # Check file size
            try:
                if os.path.getsize(os.path.join(root, fname)) > MAX_BLOB_BYTES:
                    violations.append(f"{fpath} (超過 15MB 限制)")
            except Exception:
                pass

    if violations:
        print(f"::error::[Git Policy Violation] 發現 {len(violations)} 個違規項目：", file=sys.stderr)
        for v in violations[:10]:
            print(f"  * {v}", file=sys.stderr)
        if len(violations) > 10:
            print(f"  * ... 還有另外 {len(violations) - 10} 個項目", file=sys.stderr)
        return 1

    print("[Git Policy Check] 全倉庫樹狀結構掃描合規！")
    return 0


def main():
    parser = argparse.ArgumentParser(description="OpenMontage Git Policy Checker")
    parser.add_argument("--staged", action="store_true", help="Check staged files in index")
    parser.add_argument("--tree", action="store_true", help="Check full repo tree (CI mode)")
    parser.add_argument("--msg", type=str, default="", help="Optional commit message to validate")
    args = parser.parse_args()

    if args.tree:
        sys.exit(check_tree_content())
    else:
        sys.exit(check_staged_content(commit_msg=args.msg))


if __name__ == "__main__":
    main()
