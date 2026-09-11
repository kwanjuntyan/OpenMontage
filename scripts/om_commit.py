# -*- coding: utf-8 -*-
"""OpenMontage Smart Commit Assistant (om_commit.py)

Automatically detects staged and unstaged changes, categorizes them into:
  - Category A (Code / Tools / Engine): feat(...), fix(...), docs, test
  - Category B (Course Content / Recipes): content(<course-id>): ...
Ensures strict category isolation, NUL-safe status parsing, and zero mixed commits.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import PurePosixPath

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def get_git_status() -> list[tuple[str, str, str]]:
    """Returns list of (index_status, worktree_status, filepath).

    Uses `git status --porcelain=v1 -z --untracked-files=all` for NUL-safe path decoding.
    """
    res = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        capture_output=True,
        check=True
    )
    if not res.stdout:
        return []

    items: list[tuple[str, str, str]] = []
    tokens = res.stdout.split(b"\0")
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if not token:
            i += 1
            continue

        if len(token) >= 3 and token[2:3] == b" ":
            idx_status = chr(token[0])
            work_status = chr(token[1])
            path_bytes = token[3:]
            path_str = os.fsdecode(path_bytes).replace("\\", "/").strip()

            # Handle rename/copy which provides a second path token
            if idx_status in ("R", "C") or work_status in ("R", "C"):
                i += 1
                if i < len(tokens):
                    orig_path = os.fsdecode(tokens[i]).replace("\\", "/").strip()
                    # We track current path
            items.append((idx_status, work_status, path_str))
        i += 1

    return items


def generate_course_commit_msg(project_files: list[str]) -> str:
    """Generates a Category B commit message from a list of project files."""
    project_ids = set()
    file_types = set()

    for f in project_files:
        parts = f.split("/")
        if len(parts) >= 2 and parts[0].lower() == "projects":
            project_ids.add(parts[1])
            filename = parts[-1]
            if "manifest" in filename:
                file_types.add("media manifests")
            elif "script" in filename:
                file_types.add("script")
            elif "scene_plan" in filename:
                file_types.add("scene plan")
            elif "checkpoint" in filename:
                file_types.add("checkpoints")
            elif "render" in filename:
                file_types.add("render report")
            elif "project.json" in filename:
                file_types.add("project identity")
            elif "character" in filename or "clp" in filename:
                file_types.add("character design")
            else:
                file_types.add("recipes")

    if not project_ids:
        scope = "content"
    elif len(project_ids) == 1:
        pid = list(project_ids)[0]
        if pid.startswith("course-31"):
            scope = "course-31"
        elif pid.startswith("esg"):
            scope = "esg"
        else:
            scope = pid
    else:
        scope = "projects"

    actions = ", ".join(sorted(file_types)) if file_types else "recipes"
    return f"content({scope}): update {actions}"


def generate_code_commit_msg(code_files: list[str]) -> str:
    """Generates a Category A commit message from code files."""
    scopes = set()
    for f in code_files:
        if f.startswith("backlot/"):
            scopes.add("backlot")
        elif "gcs" in f or "storage" in f or "cloud" in f:
            scopes.add("cloud")
        elif f.startswith("tools/"):
            scopes.add("tools")
        elif f.startswith("pipeline_defs/") or f.startswith("lib/pipeline"):
            scopes.add("pipeline")
        elif f.startswith("tests/"):
            scopes.add("test")
        elif f.startswith("docs/") or f.endswith(".md"):
            scopes.add("docs")
        elif f.startswith(".githooks/"):
            scopes.add("git")
        else:
            scopes.add("core")

    scope = list(scopes)[0] if len(scopes) == 1 else "core"
    prefix = "test" if scope == "test" else "docs" if scope == "docs" else "feat"
    return f"{prefix}({scope}): update {scope} modules"


def main():
    parser = argparse.ArgumentParser(description="OpenMontage Smart Commit Helper")
    parser.add_argument("-y", "--yes", action="store_true", help="Accept generated message without prompt")
    parser.add_argument("-m", "--message", type=str, default="", help="Custom message override")
    parser.add_argument("-p", "--push", action="store_true", help="Push to remote after committing")
    args = parser.parse_args()

    try:
        status_items = get_git_status()
    except subprocess.CalledProcessError as e:
        print(f"[X] 無法讀取 git status (code {e.returncode})", file=sys.stderr)
        sys.exit(e.returncode)

    if not status_items:
        print("[OpenMontage] 乾淨的工作目錄，沒有任何需要提交的改動。 (Working tree clean)")
        return

    # Check for already staged files in index (case-insensitive for Windows)
    staged_course = [p for idx, _, p in status_items if idx not in (" ", "?") and p.lower().startswith("projects/")]
    staged_code = [p for idx, _, p in status_items if idx not in (" ", "?") and not p.lower().startswith("projects/")]

    all_course = [p for _, _, p in status_items if p.lower().startswith("projects/")]
    all_code = [p for _, _, p in status_items if not p.lower().startswith("projects/")]

    print("\n" + "=" * 60)
    print("[OpenMontage 智慧提交助手]")
    print("=" * 60)
    print(f"偵測到變更檔案: 共 {len(status_items)} 個")
    if all_course:
        print(f"  * 類別 B (課程配方資料): {len(all_course)} 個檔案 (已暫存: {len(staged_course)})")
    if all_code:
        print(f"  * 類別 A (系統程式碼):   {len(all_code)} 個檔案 (已暫存: {len(staged_code)})")
    print("-" * 60)

    # Determine target category
    target_category = ""
    if all_course and not all_code:
        target_category = "course"
    elif all_code and not all_course:
        target_category = "code"
    else:
        # Both exist: user must choose which one to commit first
        print("[!] 提示：您同時修改了【系統程式碼】與【課程資料】。")
        print("   根據團隊規範，禁止混雜提交，必須分開打包：")
        print("   1) 先提交【課程配方資料】(Category B: content)")
        print("   2) 先提交【系統程式碼】(Category A: feat/fix)")
        choice = "1"
        if not args.yes:
            choice = input("\n請選擇 [預設 1]: ").strip() or "1"
        target_category = "course" if choice == "1" else "code"

    files_to_stage: list[str] = []
    files_to_unstage: list[str] = []
    suggested_msg = ""

    if target_category == "course":
        files_to_stage = all_course
        # If code was already staged in index, unstage it to prevent mixed commit
        files_to_unstage = staged_code
        suggested_msg = generate_course_commit_msg(all_course)
    else:
        files_to_stage = all_code
        # If course was already staged in index, unstage it to prevent mixed commit
        files_to_unstage = staged_course
        suggested_msg = generate_code_commit_msg(all_code)

    final_msg = args.message.strip() if args.message.strip() else suggested_msg
    print(f"\n推薦 Commit 訊息: \n  ->  {final_msg}\n")

    if not args.yes and not args.message:
        user_input = input("確認提交？ [Enter 直接同意 / 或輸入自訂訊息 / q 放棄]: ").strip()
        if user_input.lower() in ("q", "quit", "exit"):
            print("已取消提交。")
            return
        if user_input:
            final_msg = user_input

    # Step 1: Unstage conflicting files from index if any
    if files_to_unstage:
        print(f"[Git] 正在自暫存區移出另類別檔案 ({len(files_to_unstage)} 個)，以確保不混雜...")
        # Use git reset HEAD -- <files>
        for batch in [files_to_unstage[i:i+50] for i in range(0, len(files_to_unstage), 50)]:
            subprocess.run(["git", "reset", "HEAD", "--"] + batch, check=True, stdout=subprocess.DEVNULL)

    # Step 2: Stage target files
    print(f"[Git] 正在暫存目標檔案 ({len(files_to_stage)} 個)...")
    for batch in [files_to_stage[i:i+50] for i in range(0, len(files_to_stage), 50)]:
        subprocess.run(["git", "add", "--"] + batch, check=True)

    # Step 3: Execute commit
    print(f"[Git] 正在執行提交...")
    commit_res = subprocess.run(
        ["git", "commit", "-m", final_msg],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    if commit_res.returncode == 0:
        print(f"[V] 提交成功！")
        print(commit_res.stdout)
        if args.push:
            print("[Git] 正在推送到遠端...")
            push_res = subprocess.run(["git", "push"], check=False)
            if push_res.returncode != 0:
                print(f"[X] 推送失敗 (code {push_res.returncode})", file=sys.stderr)
                sys.exit(push_res.returncode)
            print("[*] 推送完成！")
    else:
        print(f"[X] 提交失敗 (code {commit_res.returncode}):\n{commit_res.stderr or commit_res.stdout}", file=sys.stderr)
        sys.exit(commit_res.returncode)


if __name__ == "__main__":
    main()
