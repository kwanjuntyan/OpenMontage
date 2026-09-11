# -*- coding: utf-8 -*-
"""CLI script to sync local CLP reference images to Google Cloud Storage.

Scans project clp/ directories, uploads character/prop/landmark reference images
to GCS under shared_clp/, and updates artifacts/character_design.json with the
corresponding gcs_url fields for seamless cross-device team collaboration.

Usage:
  python scripts/sync_clp_to_gcs.py                 # Sync all projects
  python scripts/sync_clp_to_gcs.py --project <id>  # Sync specific project
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add repo root to Python path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from lib.gcs_storage import gcs_storage


def sync_clp(project_name: str | None = None) -> None:
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

    print(f"\n=======================================================")
    print(f" OpenMontage CLP Cloud Sync (GCS: gs://{gcs_storage.bucket_name})")
    print(f"=======================================================\n")

    total_uploaded = 0
    for p in targets:
        clp_dir = p / "clp"
        if not clp_dir.is_dir():
            continue

        images = [f for f in clp_dir.iterdir() if f.is_file() and f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
        if not images:
            continue

        print(f"[*] Syncing project: {p.name} ({len(images)} CLP images)")
        results = gcs_storage.sync_project_clp(p)
        for name, url in results.items():
            print(f"    + {name} -> {url}")
            total_uploaded += 1

    print(f"\n[Done] Sync completed. Total {total_uploaded} CLP assets processed.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync CLP images to GCS.")
    parser.add_argument("--project", "-p", help="Specific project ID to sync", default=None)
    args = parser.parse_args()
    sync_clp(args.project)
