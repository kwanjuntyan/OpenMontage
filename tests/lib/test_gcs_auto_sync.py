# -*- coding: utf-8 -*-
"""Unit tests for automated non-blocking GCS sync capabilities, thread safety, and URL encoding."""

import concurrent.futures
import json
import os
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from lib.checkpoint import write_checkpoint, init_project
from lib.gcs_storage import GCSStorage, gcs_storage, atomic_update_json, flush_background_sync
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


def test_public_url_percent_encoding():
    """Verifies that public URLs encode special characters, spaces, and Unicode safely."""
    storage = GCSStorage(bucket_name="my-bucket")
    raw_path = "projects/course-31/assets/video/第 1 講 #intro.mp4"
    url = storage.get_public_url(raw_path)
    assert " " not in url
    assert "#" not in url
    assert "%20" in url
    assert "%23" in url
    assert "https://storage.googleapis.com/my-bucket/projects/course-31/assets/video/" in url


def test_atomic_update_json_concurrent_writes(tmp_path):
    """Verifies atomic_update_json prevents race conditions and corrupted JSON during parallel writes."""
    test_file = tmp_path / "manifest.json"
    initial_data = {
        "version": "1.0",
        "assets": [
            {"id": f"asset_{i}", "gcs_url": None} for i in range(20)
        ]
    }
    test_file.write_text(json.dumps(initial_data, indent=2), encoding="utf-8")

    def _worker(asset_idx: int):
        def _updater(data: dict) -> bool:
            data["assets"][asset_idx]["gcs_url"] = f"https://gcs.com/url_{asset_idx}.mp4"
            return True
        atomic_update_json(test_file, _updater)

    # Launch 20 concurrent threads attempting to update different assets in the same file
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futures = [ex.submit(_worker, i) for i in range(20)]
        concurrent.futures.wait(futures)

    # Verify JSON is valid and all 20 updates survived
    result = json.loads(test_file.read_text(encoding="utf-8"))
    for i in range(20):
        assert result["assets"][i]["gcs_url"] == f"https://gcs.com/url_{i}.mp4"


def test_async_sync_project_assets_bounded_executor(tmp_path, monkeypatch):
    """Verifies that async_sync_project_assets executes in worker pool and invokes callback."""
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

    fut = storage.async_sync_project_assets(proj_dir, on_complete=_callback)
    assert fut is not None

    # Wait for completion
    assert completed_event.wait(timeout=2.0) is True
    assert received_results == {"mock/path.mp4": "https://gcs.com/mock.mp4"}

    # Test flush_background_sync
    flush_background_sync(timeout=2.0)


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

    fut = storage.async_upload_single_asset("my_proj", test_video, rel_path="assets/video/sc01.mp4")
    assert fut is not None
    fut.result(timeout=2.0)

    # Verify manifest was updated
    updated = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert updated["assets"][0]["gcs_url"] == "https://gcs.com/test_video.mp4"


def test_write_checkpoint_triggers_auto_sync(tmp_path, monkeypatch):
    """Verifies write_checkpoint calls async_sync_project_assets on media stages."""
    init_project(
        "sync_test",
        title="Sync Test",
        pipeline_type="cinematic",
        pipeline_dir=tmp_path,
    )

    called = threading.Event()

    def mock_async_sync(p_dir):
        called.set()
        return None

    monkeypatch.setattr("lib.gcs_storage.gcs_storage.is_auto_sync_enabled", lambda: True)
    monkeypatch.setattr("lib.gcs_storage.gcs_storage.async_sync_project_assets", mock_async_sync)
    # This unit test isolates the post-write sync hook; DAG prerequisite
    # enforcement has dedicated checkpoint contract coverage.
    monkeypatch.setattr("lib.checkpoint._enforce_stage_prerequisites", lambda *args, **kwargs: None)

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
        pipeline_type="cinematic",
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


def test_is_configured_checks_bucket_existence(monkeypatch):
    """Verifies that is_configured returns False if bucket.exists() returns False (R2-7)."""
    storage = GCSStorage(bucket_name="nonexistent-bucket")
    fake_bucket = MagicMock()
    fake_bucket.exists.return_value = False
    storage._client = MagicMock()
    storage._client.bucket.return_value = fake_bucket

    monkeypatch.setattr("google.cloud.storage.Client", lambda *a, **kw: storage._client)
    assert storage.is_configured() is False


def test_is_configured_returns_false_on_bucket_exists_exception(monkeypatch):
    """Verifies that is_configured returns False if bucket.exists() raises PermissionError/timeout (R3-3)."""
    storage = GCSStorage(bucket_name="forbidden-bucket")
    fake_bucket = MagicMock()
    fake_bucket.exists.side_effect = PermissionError("Forbidden / Access Denied")
    storage._client = MagicMock()
    storage._client.bucket.return_value = fake_bucket

    monkeypatch.setattr("google.cloud.storage.Client", lambda *a, **kw: storage._client)
    assert storage.is_configured() is False

