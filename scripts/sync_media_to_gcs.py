# -*- coding: utf-8 -*-
"""Unified CLI script to synchronize ALL OpenMontage media assets to Google Cloud Storage.

Synchronizes:
  1. CLP reference portraits & props (clp/ -> projects/<id>/clp/ & shared_clp/)
  2. Shot video clips (assets/video/ -> projects/<id>/assets/video/)
  3. Static scene images (assets/images/ -> projects/<id>/assets/images/)
  4. Narration & mix audio (assets/audio/ -> projects/<id>/assets/audio/)
  5. Final master renders (renders/ -> projects/<id>/renders/)

Automatically updates:
  - artifacts/asset_manifest.json (populates gcs_url per asset)
  - artifacts/character_design.json (populates gcs_url per character)
  - artifacts/render_report.json & project.json (populates gcs_url for renders)

Usage:
  python scripts/sync_media_to_gcs.py                 # Sync all projects
  python scripts/sync_media_to_gcs.py -p <project_id>  # Sync specific project
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add repo root to Python path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from lib.gcs_storage import gcs_storage


def sync_all(project_name: str | None = None) -> None:
    projects_dir = REPO_ROOT / "projects"
    if not projects_dir.is_dir():
        print("[Error] projects/ directory not found.")
        return

    if not gcs_storage.is_configured():
        print("[Warning] GCS_BUCKET_NAME is not configured in .env.")
        print("          Set GCS_BUCKET_NAME=<your-bucket> in .env to enable cloud upload.")
        return

    targets = []
    if project_name:
        p_path = projects_dir / project_name
        if not p_path.is_dir():
            print(f"[Error] Project not found: {project_name}")
            return
        targets.append(p_path)
    else:
        targets = [p for p in sorted(projects_dir.iterdir()) if p.is_dir()]

    print("\n=======================================================")
    print(f" OpenMontage Unified Media Cloud Sync")
    print(f" Target Bucket: gs://{gcs_storage.bucket_name}")
    print("=======================================================\n")

    grand_total = 0
    for p in targets:
        print(f"[*] Scanning project: {p.name} ...")
        synced = gcs_storage.sync_project_assets(p)
        if synced:
            for rel_path, url in synced.items():
                print(f"    + [{rel_path}] -> {url}")
            grand_total += len(synced)
        else:
            print(f"    (No media files or already synced)")

    print(f"\n[Done] Unified media sync completed. Total {grand_total} assets processed.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unified sync of all project media assets to GCS.")
    parser.add_argument("--project", "-p", help="Specific project ID to sync", default=None)
    args = parser.parse_args()
    sync_all(args.project)
