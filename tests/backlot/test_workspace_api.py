"""B0.2B Workspace API and server-side flag regressions."""

from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backlot import server as server_mod
from backlot import state as state_mod


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _project(root: Path, project_id: str = "film") -> Path:
    project = root / project_id
    project.mkdir(parents=True)
    _write_json(
        project / "project.json",
        {"project_id": project_id, "title": "Film", "pipeline_type": "cinematic"},
    )
    return project


@pytest.fixture
def projects_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "projects"
    root.mkdir()
    monkeypatch.setattr(state_mod, "PROJECTS_DIR", root)
    monkeypatch.setattr(server_mod, "PROJECTS_DIR", root)
    monkeypatch.setattr(server_mod, "_PROJECTS_ROOT_STR", str(root.resolve()))
    return root


def _client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    async def no_watch() -> None:
        return None

    monkeypatch.setattr(server_mod, "_watch_projects", no_watch)
    return TestClient(server_mod.create_app())


def test_workspace_default_off_is_404_without_legacy_regression(
    projects_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _project(projects_root)
    monkeypatch.delenv("BACKLOT_WORKSPACE_ENABLED", raising=False)
    with _client(monkeypatch) as client:
        assert client.get("/api/workspace/v1/catalog").status_code == 404
        assert client.get("/api/workspace/v1/projects/film/shell").status_code == 404
        assert client.get("/p/film/workspace").status_code == 404
        assert client.get("/api/projects").status_code == 200
        assert client.get("/api/project/film/state").status_code == 200
        assert client.get("/p/film").status_code == 200


def test_workspace_flag_on_serves_versioned_catalog_and_shell(
    projects_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _project(projects_root)
    monkeypatch.setenv("BACKLOT_WORKSPACE_ENABLED", "true")
    with _client(monkeypatch) as client:
        catalog = client.get("/api/workspace/v1/catalog")
        assert catalog.status_code == 200
        assert catalog.json()["projection_kind"] == "catalog"
        assert catalog.json()["data_schema"] == "backlot.workspace.catalog.v1"
        assert catalog.json()["data"]["items"][0]["classification"] == "unavailable"

        shell = client.get("/api/workspace/v1/projects/film/shell")
        assert shell.status_code == 200
        body = shell.json()
        assert body["projection_kind"] == "shell"
        assert body["data_schema"] == "backlot.workspace.shell.v1"
        assert [stage["name"] for stage in body["data"]["stages"]][:2] == ["research", "proposal"]
        assert body["data"]["classification"] == "unavailable"
        assert body["data"]["current_stage"] == "research"


def test_workspace_api_rejects_untrusted_cursor_limits_and_project_ids(
    projects_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _project(projects_root)
    monkeypatch.setenv("BACKLOT_WORKSPACE_ENABLED", "1")
    with _client(monkeypatch) as client:
        for value in ("abc", "true", "0", "101"):
            response = client.get("/api/workspace/v1/catalog", params={"limit": value})
            assert response.status_code == 422
            assert response.json() == {"detail": {"code": "invalid_limit"}}
        assert client.get("/api/workspace/v1/catalog?limit=1").status_code == 200
        assert client.get("/api/workspace/v1/catalog?limit=100").status_code == 200
        assert client.get("/api/workspace/v1/catalog?cursor=not-json").json() == {
            "detail": {"code": "invalid_cursor"}
        }
        extra = json.dumps({
            "version": "backlot.workspace.cursor.v1",
            "snapshot_sha256": "sha256:" + "0" * 64,
            "sort_key": "project_id",
            "last_resource_key": "project_x",
            "direction": "forward",
            "extra": True,
        })
        response = client.get("/api/workspace/v1/catalog", params={"cursor": extra})
        assert response.status_code == 422
        assert response.json() == {"detail": {"code": "invalid_cursor"}}
        assert client.get("/api/workspace/v1/projects/nope/shell").status_code == 404
        assert client.get("/api/workspace/v1/projects/%2E%2E/shell").status_code in {404, 422}


def test_shell_uses_manifest_stage_order_and_never_reads_private_sidecars(
    projects_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _project(projects_root)
    private = project / ".production-units"
    private.mkdir()
    (private / "secret.json").write_text("{}", encoding="utf-8")
    before = {path.relative_to(projects_root): path.read_bytes() for path in projects_root.rglob("*") if path.is_file()}
    original_open = builtins.open

    def reject_private_open(path, *args, **kwargs):
        if ".production-units" in str(path).casefold() or ".batch-v2" in str(path).casefold():
            raise AssertionError("Workspace API read a private sidecar")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", reject_private_open)
    monkeypatch.setenv("BACKLOT_WORKSPACE_ENABLED", "on")
    with _client(monkeypatch) as client:
        response = client.get("/api/workspace/v1/projects/film/shell")
    assert response.status_code == 200
    assert response.json()["data"]["stages"][0] == {
        "name": "research", "status": "pending", "human_approval_default": False
    }
    after = {path.relative_to(projects_root): path.read_bytes() for path in projects_root.rglob("*") if path.is_file()}
    assert after == before


def test_shell_keeps_missing_valid_and_invalid_checkpoint_lifecycles_distinct(
    projects_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _project(projects_root)
    common = {
        "version": "1.0",
        "project_id": "film",
        "pipeline_type": "cinematic",
        "timestamp": "2026-07-02T00:01:00Z",
        "artifacts": {},
    }
    _write_json(project / "checkpoint_research.json", {**common, "stage": "research", "status": "in_progress"})
    _write_json(project / "checkpoint_proposal.json", {**common, "stage": "proposal", "status": "failed"})
    _write_json(
        project / "checkpoint_script.json",
        {
            **common,
            "stage": "script",
            "status": "awaiting_human",
            "human_approval_required": True,
            "human_approved": False,
            "artifacts": {
                "script": {
                    "version": "1.0",
                    "title": "Film",
                    "total_duration_seconds": 1,
                    "sections": [{"id": "s1", "text": "Review.", "start_seconds": 0, "end_seconds": 1}],
                }
            },
        },
    )
    (project / "checkpoint_clp.json").write_text("{invalid", encoding="utf-8")
    before = {
        path.relative_to(projects_root): path.read_bytes()
        for path in projects_root.rglob("*")
        if path.is_file()
    }
    monkeypatch.setenv("BACKLOT_WORKSPACE_ENABLED", "true")
    with _client(monkeypatch) as client:
        response = client.get("/api/workspace/v1/projects/film/shell")
    assert response.status_code == 200
    stages = {stage["name"]: stage for stage in response.json()["data"]["stages"]}
    assert stages["research"]["status"] == "in_progress"
    assert stages["proposal"]["status"] == "failed"
    assert stages["script"]["status"] == "awaiting_human"
    assert stages["clp"]["status"] == "invalid"
    assert stages["scene_plan"]["status"] == "pending"
    assert response.json()["data"]["current_stage"] == "research"
    assert response.json()["data"]["gate_state"] == "invalid"
    authority = response.json()["authority"]
    assert authority["authority_state"] == "unavailable"
    assert authority["validation_state"] == "invalid"
    assert authority["source_kind"] == "unavailable"
    assert authority["evidence_scope"] == "checkpoint_validated"
    assert authority["degraded_reasons"] == ["invalid_checkpoint"]
    assert [item["source_key"] for item in authority["evidence_refs"]] == [
        "project:film:marker",
        "pipeline:cinematic:project:film",
        "checkpoint:film:research",
        "checkpoint:film:proposal",
        "checkpoint:film:script",
    ]
    assert any(item["code"] == "invalid_checkpoint" for item in response.json()["diagnostics"])
    after = {
        path.relative_to(projects_root): path.read_bytes()
        for path in projects_root.rglob("*")
        if path.is_file()
    }
    assert after == before


def test_authenticated_project_with_invalid_manifest_has_unavailable_shell(
    projects_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _project(projects_root, "bad-pipeline")
    _write_json(
        projects_root / "bad-pipeline" / "project.json",
        {"project_id": "bad-pipeline", "title": "Bad", "pipeline_type": "not-real"},
    )
    monkeypatch.setenv("BACKLOT_WORKSPACE_ENABLED", "true")
    with _client(monkeypatch) as client:
        response = client.get("/api/workspace/v1/projects/bad-pipeline/shell")
    assert response.status_code == 200
    body = response.json()
    assert body["data"] == {
        "version": "backlot.workspace.shell.v1",
        "pipeline_type": "unavailable",
        "classification": "unavailable",
        "stages": [],
        "current_stage": None,
        "gate_state": "unavailable",
    }
    assert body["authority"]["authority_state"] == "unavailable"
    assert body["authority"]["validation_state"] == "invalid"
    assert body["diagnostics"][0]["code"] == "pipeline_manifest_invalid"
