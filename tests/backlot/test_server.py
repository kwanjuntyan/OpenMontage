"""Server/API tests for Backlot.

These cover the deterministic eval surface in internal/evals/BACKLOT_EVAL_PLAN.md:
API shape, path safety, media/thumb serving, range requests, and loose
performance budgets.
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from backlot import server as server_mod
from backlot import state as state_mod


@pytest.fixture
def projects_root(tmp_path, monkeypatch):
    root = tmp_path / "projects"
    root.mkdir()
    monkeypatch.setattr(state_mod, "PROJECTS_DIR", root)
    monkeypatch.setattr(server_mod, "PROJECTS_DIR", root)
    monkeypatch.setattr(server_mod, "_summary_cache", {})
    monkeypatch.setattr(server_mod, "_PROJECTS_ROOT_STR", __import__("os").path.normcase(str(root.resolve())))
    monkeypatch.setattr(server_mod, "THUMB_CACHE_DIR", tmp_path / "thumbs")
    return root


@pytest.fixture
def client(projects_root, monkeypatch):
    async def no_watch():
        return None

    monkeypatch.setattr(server_mod, "_watch_projects", no_watch)
    with TestClient(server_mod.create_app()) as c:
        yield c


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def _make_project(root: Path, project_id: str = "film") -> Path:
    project = root / project_id
    (project / "artifacts").mkdir(parents=True)
    (project / "assets" / "images").mkdir(parents=True)
    (project / "assets" / "video").mkdir(parents=True)
    (project / "renders").mkdir(parents=True)
    _write_json(
        project / "project.json",
        {
            "project_id": project_id,
            "title": "Film",
            "pipeline_type": "cinematic",
            "created_at": "2026-07-02T00:00:00Z",
        },
    )
    _write_json(
        project / "checkpoint_script.json",
        {
            "version": "1.0",
            "project_id": project_id,
            "pipeline_type": "cinematic",
            "stage": "script",
            "status": "awaiting_human",
            "timestamp": "2026-07-02T00:01:00Z",
            "human_approval_required": True,
            "human_approved": False,
            "artifacts": {
                "script": {
                    "version": "1.0",
                    "title": "Film",
                    "total_duration_seconds": 1,
                    "sections": [
                        {
                            "id": "s1",
                            "text": "Awaiting review.",
                            "start_seconds": 0,
                            "end_seconds": 1,
                        }
                    ],
                }
            },
        },
    )
    return project


def _write_png(path: Path, color: tuple[int, int, int] = (200, 40, 80)) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (24, 16), color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    path.write_bytes(buf.getvalue())


class TestBacklotServerApi:
    def test_health(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"ok": True, "app": "backlot"}

    def test_projects_shape_and_state(self, client, projects_root):
        _make_project(projects_root, "film")

        projects = client.get("/api/projects")
        assert projects.status_code == 200
        body = projects.json()
        assert len(body) == 1
        assert body[0]["project_id"] == "film"
        assert body[0]["awaiting_human"] is True
        assert "stage_states" in body[0]

        state = client.get("/api/project/film/state")
        assert state.status_code == 200
        state_body = state.json()
        assert state_body["project_id"] == "film"
        assert state_body["title"] == "Film"
        assert state_body["stages"]

    def test_projects_api_ignores_linked_project_directory(self, client, projects_root):
        """The cached API enumeration must not bypass project-root identity."""
        _make_project(projects_root, "film")
        outside = projects_root.parent / "outside-secret"
        _make_project(outside.parent, outside.name)
        link = projects_root / "linked-secret"
        is_junction = False
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            if sys.platform != "win32":
                pytest.skip("Directory link creation is not permitted")
            created = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(outside)],
                capture_output=True,
                text=True,
                check=False,
            )
            if created.returncode != 0:
                pytest.fail(
                    "Could not create Windows junction probe: "
                    f"{created.stderr or created.stdout}"
                )
            is_junction = True

        # A stale cache entry must not resurrect an invalid directory alias.
        server_mod._summary_cache[link.name] = {
            "project_id": link.name,
            "title": "Secret",
            "pipeline_type": "cinematic",
            "has_pipeline_state": True,
            "poster": None,
            "live": False,
            "last_activity": 0,
            "active_stage": None,
            "awaiting_human": False,
            "stage_states": [],
            "completed_count": 0,
            "render_count": 0,
            "scene_count": 0,
        }
        try:
            response = client.get("/api/projects")
            assert response.status_code == 200
            assert [item["project_id"] for item in response.json()] == ["film"]
            assert link.name not in server_mod._summary_cache
        finally:
            if is_junction and link.exists():
                os.rmdir(link)
            elif link.is_symlink():
                link.unlink()

    def test_invalid_nan_checkpoint_lifecycle_remains_json_safe(self, client, projects_root):
        project = _make_project(projects_root, "nan-state")
        current = json.loads((project / "checkpoint_script.json").read_text())
        current["timestamp"] = float("nan")
        current["status"] = "completed"
        _write_json(project / "checkpoint_script.json", current)
        _write_json(
            project / "history" / "checkpoint_script_20260913T000000Z.json",
            {"status": "completed", "timestamp": float("nan")},
        )

        response = client.get("/api/project/nan-state/state")

        assert response.status_code == 200
        script_stage = next(
            stage for stage in response.json()["stages"] if stage["name"] == "script"
        )
        assert script_stage["status"] == "invalid"
        assert script_stage["timestamp"] is None
        assert script_stage["history_entries"][-1] == {
            "status": "invalid",
            "timestamp": None,
        }

    @pytest.mark.parametrize(
        ("url", "status"),
        [
            ("/api/project/../state", 404),
            ("/api/project/C:/state", 400),
            ("/api/project/nope/state", 404),
        ],
    )
    def test_project_id_rejects_bad_or_unknown_ids(self, client, url, status):
        response = client.get(url)
        assert response.status_code == status

    def test_media_rejects_path_traversal(self, client, projects_root):
        _make_project(projects_root, "film")
        response = client.get("/media/film/%2E%2E/project.json")
        assert response.status_code == 403

    def test_media_serves_range_requests(self, client, projects_root):
        project = _make_project(projects_root, "film")
        media = project / "renders" / "final.mp4"
        media.write_bytes(b"0123456789")

        response = client.get("/media/film/renders/final.mp4", headers={"Range": "bytes=2-5"})

        assert response.status_code == 206
        assert response.content == b"2345"
        assert response.headers["content-range"].startswith("bytes 2-5/10")

    def test_thumb_downscales_image_and_passes_through_non_media(self, client, projects_root):
        project = _make_project(projects_root, "film")
        _write_png(project / "assets" / "images" / "sc1.png")
        text = project / "artifacts" / "note.txt"
        text.write_text("hello", encoding="utf-8")

        image = client.get("/thumb/film/assets/images/sc1.png?w=320")
        assert image.status_code == 200
        assert image.headers["content-type"] == "image/jpeg"
        assert image.content.startswith(b"\xff\xd8")

        passthrough = client.get("/thumb/film/artifacts/note.txt")
        assert passthrough.status_code == 200
        assert passthrough.content == b"hello"


class TestBacklotPerformanceBudgets:
    def test_projects_and_state_stay_within_loose_budgets(self, client, projects_root):
        for i in range(25):
            project = _make_project(projects_root, f"film-{i:02d}")
            _write_json(
                project / "artifacts" / "scene_plan.json",
                {"version": "1.0", "scenes": [{"id": "sc1", "start_seconds": 0, "end_seconds": 1}]},
            )

        t0 = time.perf_counter()
        cold = client.get("/api/projects")
        cold_s = time.perf_counter() - t0
        assert cold.status_code == 200
        assert cold_s < 2.0

        t1 = time.perf_counter()
        warm = client.get("/api/projects")
        warm_s = time.perf_counter() - t1
        assert warm.status_code == 200
        assert warm_s < 0.150

        t2 = time.perf_counter()
        state = client.get("/api/project/film-00/state")
        state_s = time.perf_counter() - t2
        assert state.status_code == 200
        assert state_s < 0.400

    def test_image_thumb_generation_stays_within_budget(self, client, projects_root):
        project = _make_project(projects_root, "film")
        _write_png(project / "assets" / "images" / "sc1.png")

        t0 = time.perf_counter()
        response = client.get("/thumb/film/assets/images/sc1.png?w=640")
        elapsed = time.perf_counter() - t0

        assert response.status_code == 200
        assert elapsed < 1.5


class TestFindingsFixes:
    """Regression tests for dogfood findings F-03 (thumb video fallback)."""

    def test_thumb_never_serves_raw_video_bytes(self, client, projects_root):
        p = _make_project(projects_root, "vid")
        fake_video = p / "renders" / "final.mp4"
        fake_video.parent.mkdir(parents=True, exist_ok=True)
        # Not a real video: ffmpeg poster extraction will fail.
        fake_video.write_bytes(b"\x00" * 4096)
        res = client.get("/thumb/vid/renders/final.mp4")
        assert res.status_code == 404  # never the raw video bytes (F-03)

    def test_media_and_thumb_redirects_to_gcs_when_local_file_missing(self, client, projects_root):
        p = _make_project(projects_root, "clp-test")
        # Add character_design.json with gcs_url
        _write_json(p / "artifacts" / "character_design.json", {
            "version": "1.0",
            "characters": [
                {
                    "id": "hero",
                    "display_name": "Hero",
                    "image": "clp/hero.png",
                    "gcs_url": "https://storage.googleapis.com/my-bucket/shared_clp/hero.png"
                }
            ]
        })
        # Local file clp/hero.png does NOT exist
        res_media = client.get("/media/clp-test/clp/hero.png", follow_redirects=False)
        assert res_media.status_code == 302
        assert res_media.headers["location"] == "https://storage.googleapis.com/my-bucket/shared_clp/hero.png"

        res_thumb = client.get("/thumb/clp-test/clp/hero.png", follow_redirects=False)
        assert res_thumb.status_code == 302
        assert res_thumb.headers["location"] == "https://storage.googleapis.com/my-bucket/shared_clp/hero.png"

    def test_asset_manifest_unified_media_redirects_to_gcs(self, client, projects_root):
        p = _make_project(projects_root, "manifest-test")
        # Add asset_manifest.json with shot video and narration audio
        _write_json(p / "artifacts" / "asset_manifest.json", {
            "project_id": "manifest-test",
            "assets": [
                {
                    "id": "asset_video_sc01",
                    "type": "video",
                    "path": "assets/video/sc01.mp4",
                    "gcs_url": "https://storage.googleapis.com/my-bucket/projects/manifest-test/assets/video/sc01.mp4"
                },
                {
                    "id": "asset_audio_sc01",
                    "type": "audio",
                    "path": "assets/audio/sc01.mp3",
                    "gcs_url": "https://storage.googleapis.com/my-bucket/projects/manifest-test/assets/audio/sc01.mp3"
                }
            ]
        })
        # 1. Shot video missing locally -> 302 redirect to GCS
        res_v = client.get("/media/manifest-test/assets/video/sc01.mp4", follow_redirects=False)
        assert res_v.status_code == 302
        assert res_v.headers["location"] == "https://storage.googleapis.com/my-bucket/projects/manifest-test/assets/video/sc01.mp4"

        # 2. Audio missing locally -> 302 redirect to GCS
        res_a = client.get("/media/manifest-test/assets/audio/sc01.mp3", follow_redirects=False)
        assert res_a.status_code == 302
        assert res_a.headers["location"] == "https://storage.googleapis.com/my-bucket/projects/manifest-test/assets/audio/sc01.mp3"

    def test_gcs_registry_symlink_cannot_escape_project(self, client, projects_root):
        project = _make_project(projects_root, "contained-registry")
        outside_dir = projects_root.parent / "outside-registry"
        outside = outside_dir / "character_design.json"
        _write_json(
            outside,
            {
                "characters": [
                    {
                        "id": "hero",
                        "image": "clp/hero.png",
                        "gcs_url": "https://outside.invalid/escaped.png",
                    }
                ]
            },
        )
        registry = project / "artifacts" / "character_design.json"
        linked_artifacts = project / "artifacts"
        is_junction = False
        try:
            registry.symlink_to(outside)
        except OSError:
            if sys.platform != "win32":
                pytest.skip("File symlink creation is not permitted")
            linked_artifacts.rmdir()
            created = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(linked_artifacts), str(outside_dir)],
                capture_output=True,
                text=True,
                check=False,
            )
            if created.returncode != 0:
                pytest.fail(
                    "Could not create Windows junction probe: "
                    f"{created.stderr or created.stdout}"
                )
            is_junction = True

        try:
            response = client.get(
                "/media/contained-registry/clp/hero.png", follow_redirects=False
            )

            assert response.status_code == 404
            assert response.headers.get("location") != "https://outside.invalid/escaped.png"
        finally:
            if is_junction and linked_artifacts.exists():
                os.rmdir(linked_artifacts)
            elif registry.is_symlink():
                registry.unlink()
