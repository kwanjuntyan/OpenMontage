# -*- coding: utf-8 -*-
"""OpenMontage Smart Commit Assistant (om_commit.py)

Automatically detects staged and unstaged changes, categorizes them into:
  - Category A (Code / Tools / Engine): feat(...), fix(...), docs, test
  - Category B (Course Content / Recipes): content(<course-id>): ...
Generates compliant commit messages and commits with zero manual memorization.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def run_cmd(cmd: list[str]) -> str:
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return res.stdout.strip()


def get_git_status() -> list[tuple[str, str]]:
    """Returns list of (status_code, filepath)."""
    res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, encoding="utf-8")
    if not res.stdout:
        return []
    items = []
    for line in res.stdout.splitlines():
        if len(line) >= 4:
            code = line[:2]
            path = line[3:].strip()
            # Handle quoted paths
            if path.startswith('"') and path.endswith('"'):
                path = path[1:-1]
            items.append((code.strip(), path.replace("\\", "/")))
    return items


def generate_course_commit_msg(project_files: list[str]) -> str:
    """Generates a Category B commit message from a list of project files."""
    # Find all affected project IDs under projects/<project_id>/
    project_ids = set()
    file_types = set()

    for f in project_files:
        parts = f.split("/")
        if len(parts) >= 2 and parts[0] == "projects":
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
        # Shorten course-31-sequence5-vox -> course-31
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

    status_items = get_git_status()
    if not status_items:
        print("[OpenMontage] 乾淨的工作目錄，沒有任何需要提交的改動。 (Working tree clean)")
        return

    course_files = [path for _, path in status_items if path.startswith("projects/")]
    code_files = [path for _, path in status_items if not path.startswith("projects/")]

    print("\n" + "=" * 60)
    print("[OpenMontage 智慧提交助手]")
    print("=" * 60)
    print(f"偵測到變更檔案: 共 {len(status_items)} 個")
    if course_files:
        print(f"  * 類別 B (課程配方資料): {len(course_files)} 個檔案")
    if code_files:
        print(f"  * 類別 A (系統程式碼):   {len(code_files)} 個檔案")
    print("-" * 60)

    # Determine recommended target & message
    files_to_add: list[str] = []
    suggested_msg = ""

    if course_files and not code_files:
        files_to_add = ["projects/"]
        suggested_msg = generate_course_commit_msg(course_files)
    elif code_files and not course_files:
        files_to_add = code_files
        suggested_msg = generate_code_commit_msg(code_files)
    else:
        # Mixed changes: recommend committing course first or code first
        print("[!] 提示：您同時修改了【系統程式碼】與【課程資料】。")
        print("   為了保持乾淨的歷史紀錄，建議將兩者分開提交。")
        print("   1) 先提交 課程資料 (Category B: content)")
        print("   2) 先提交 系統程式碼 (Category A: feat/fix)")
        print("   3) 一併提交所有改動")
        choice = "1"
        if not args.yes:
            choice = input("\n請選擇 [預設 1]: ").strip() or "1"
        if choice == "1":
            files_to_add = ["projects/"]
            suggested_msg = generate_course_commit_msg(course_files)
        elif choice == "2":
            files_to_add = code_files
            suggested_msg = generate_code_commit_msg(code_files)
        else:
            files_to_add = [path for _, path in status_items]
            suggested_msg = generate_code_commit_msg(code_files)

    final_msg = args.message.strip() if args.message.strip() else suggested_msg

    print(f"\n推薦 Commit 訊息: \n  ->  {final_msg}\n")

    if not args.yes and not args.message:
        user_input = input("確認提交？ [Enter 直接同意 / 或輸入自訂訊息 / q 放棄]: ").strip()
        if user_input.lower() in ("q", "quit", "exit"):
            print("已取消提交。")
            return
        if user_input:
            final_msg = user_input

    # Execute git add & git commit
    print(f"\n[Git] 正在暫存檔案...")
    for f in files_to_add:
        subprocess.run(["git", "add", f], check=True)

    print(f"[Git] 正在執行提交...")
    commit_res = subprocess.run(["git", "commit", "-m", final_msg], capture_output=True, text=True, encoding="utf-8")
    if commit_res.returncode == 0:
        print(f"[V] 提交成功！")
        print(commit_res.stdout)
        if args.push:
            print("[Git] 正在推送到遠端...")
            subprocess.run(["git", "push"], check=True)
            print("[*] 推送完成！")
    else:
        print(f"❌ 提交失敗:\n{commit_res.stderr or commit_res.stdout}")


if __name__ == "__main__":
    main()
