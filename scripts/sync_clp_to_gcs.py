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


from scripts.sync_media_to_gcs import sync_all


def sync_clp(project_name: str | None = None) -> None:
    sync_all(project_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync media/CLP images to GCS.")
    parser.add_argument("--project", "-p", help="Specific project ID to sync", default=None)
    args = parser.parse_args()
    sync_clp(args.project)
