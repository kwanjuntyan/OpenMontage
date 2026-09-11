# -*- coding: utf-8 -*-
"""Unit tests for automated non-blocking GCS sync capabilities."""

import json
import os
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from lib.checkpoint import write_checkpoint, init_project
from lib.gcs_storage import GCSStorage, gcs_storage
from backlot.server import create_app


def test_is_auto_sync_enabled_respects_env(monkeypatch):
    """Verifies that GCS_AUTO_SYNC controls the auto-sync toggle."""
    storage = GCSStorage(bucket_name="test-bucket")
    storage._checked = True
    storage._bucket = MagicMock()

    # Default is enabled when bucket is present
    monkeypatch.delenv("GCS_AUTO_SYNC", raising=False)
    assert storage.is_auto_sync_enabled() is True

    # Explicitly disabled
    monkeypatch.setenv("GCS_AUTO_SYNC", "false")
    assert storage.is_auto_sync_enabled() is False

    monkeypatch.setenv("GCS_AUTO_SYNC", "0")
    assert storage.is_auto_sync_enabled() is False

    # Explicitly enabled
    monkeypatch.setenv("GCS_AUTO_SYNC", "true")
    assert storage.is_auto_sync_enabled() is True


def test_async_sync_project_assets_non_blocking(tmp_path, monkeypatch):
    """Verifies that async_sync_project_assets executes in a daemon thread and notifies on_complete."""
    proj_dir = tmp_path / "test_proj"
    proj_dir.mkdir()

    storage = GCSStorage(bucket_name="test-bucket")
    storage._checked = True
    storage._bucket = MagicMock()
    monkeypatch.setattr(storage, "sync_project_assets", lambda p: {"mock/path.mp4": "https://gcs.com/mock.mp4"})

    completed_event = threading.Event()
    received_results = {}

    def _callback(res):
        nonlocal received_results
        received_results = res
        completed_event.set()

    thread = storage.async_sync_project_assets(proj_dir, on_complete=_callback)
    assert thread is not None
    assert thread.daemon is True

    # Wait for thread to finish
    assert completed_event.wait(timeout=2.0) is True
    assert received_results == {"mock/path.mp4": "https://gcs.com/mock.mp4"}


def test_async_upload_single_asset_updates_manifest(tmp_path, monkeypatch):
    """Verifies that async_upload_single_asset updates asset_manifest.json with gcs_url."""
    proj_dir = tmp_path / "my_proj"
    proj_dir.mkdir()
    art_dir = proj_dir / "artifacts"
    art_dir.mkdir()
    asset_dir = proj_dir / "assets" / "video"
    asset_dir.mkdir(parents=True)

    test_video = asset_dir / "sc01.mp4"
    test_video.write_text("fake video content")

    manifest_path = art_dir / "asset_manifest.json"
    manifest_data = {
        "version": "1.0",
        "assets": [
            {
                "id": "asset_video_sc01",
                "type": "video",
                "path": "assets/video/sc01.mp4",
                "gcs_url": None
            }
        ]
    }
    manifest_path.write_text(json.dumps(manifest_data, indent=2))

    monkeypatch.setattr("lib.paths.PROJECTS_DIR", tmp_path)

    storage = GCSStorage(bucket_name="test-bucket")
    storage._checked = True
    storage._bucket = MagicMock()
    monkeypatch.setattr(storage, "upload_asset", lambda pid, lp, rel_path=None: "https://gcs.com/test_video.mp4")

    thread = storage.async_upload_single_asset("my_proj", test_video, rel_path="assets/video/sc01.mp4")
    assert thread is not None
    thread.join(timeout=2.0)

    # Verify manifest was updated
    updated = json.loads(manifest_path.read_text())
    assert updated["assets"][0]["gcs_url"] == "https://gcs.com/test_video.mp4"


def test_write_checkpoint_triggers_auto_sync(tmp_path, monkeypatch):
    """Verifies write_checkpoint calls async_sync_project_assets on media stages."""
    init_project("sync_test", title="Sync Test", pipeline_type="unknown", pipeline_dir=tmp_path)

    called = threading.Event()

    def mock_async_sync(p_dir):
        called.set()
        return None

    monkeypatch.setattr("lib.gcs_storage.gcs_storage.is_auto_sync_enabled", lambda: True)
    monkeypatch.setattr("lib.gcs_storage.gcs_storage.async_sync_project_assets", mock_async_sync)

    write_checkpoint(
        tmp_path,
        "sync_test",
        stage="assets",
        status="completed",
        artifacts={
            "asset_manifest": {
                "version": "1.0",
                "assets": [
                    {
                        "id": "asset-1",
                        "type": "video",
                        "path": "assets/video/clip.mp4",
                        "source_tool": "ffmpeg",
                        "scene_id": "scene-1",
                    }
                ],
            }
        },
        human_approved=True
    )

    assert called.wait(timeout=1.0) is True


def test_backlot_sync_gcs_endpoint(tmp_path, monkeypatch):
    """Verifies POST /api/project/{project_id}/sync_gcs starts background sync."""
    proj_dir = tmp_path / "p1"
    proj_dir.mkdir()
    (proj_dir / "project.json").write_text(json.dumps({"project_id": "p1", "title": "P1"}))

    monkeypatch.setattr("backlot.server.PROJECTS_DIR", tmp_path)
    monkeypatch.setattr("lib.paths.PROJECTS_DIR", tmp_path)
    monkeypatch.setattr("lib.gcs_storage.gcs_storage.is_configured", lambda: True)

    sync_called = threading.Event()
    monkeypatch.setattr("lib.gcs_storage.gcs_storage.async_sync_project_assets", lambda p: sync_called.set())

    app = create_app()
    with TestClient(app) as client:
        resp = client.post("/api/project/p1/sync_gcs")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert data["status"] == "sync_started"
        assert sync_called.is_set()
