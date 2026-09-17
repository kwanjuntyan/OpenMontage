"""B0.2C flag-gated Workspace shell browser-source and HTTP regressions."""

from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.request

import pytest
from fastapi.testclient import TestClient

from backlot import server as server_mod
from backlot import state as state_mod


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


@pytest.fixture
def projects_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "projects"
    root.mkdir()
    project = root / "film"
    project.mkdir()
    _write_json(
        project / "project.json",
        {"project_id": "film", "title": "Film", "pipeline_type": "cinematic"},
    )
    monkeypatch.setattr(state_mod, "PROJECTS_DIR", root)
    monkeypatch.setattr(server_mod, "PROJECTS_DIR", root)
    monkeypatch.setattr(server_mod, "_PROJECTS_ROOT_STR", str(root.resolve()))
    return root


def _client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    async def no_watch() -> None:
        return None

    monkeypatch.setattr(server_mod, "_watch_projects", no_watch)
    return TestClient(server_mod.create_app())


def test_workspace_ui_and_assets_are_shielded_when_flag_is_off(
    projects_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("BACKLOT_WORKSPACE_ENABLED", raising=False)
    with _client(monkeypatch) as client:
        assert client.get("/p/film/workspace").status_code == 404
        assert client.get("/ui/workspace/workspace.js").status_code == 404
        assert client.get("/ui/workspace/workspace.css").status_code == 404
        assert client.get("/ui/workspace/README.md").status_code == 404
        assert client.get("/p/film").status_code == 200


def test_workspace_ui_route_precedes_board_catchall_and_exposes_only_assets(
    projects_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("BACKLOT_WORKSPACE_ENABLED", "true")
    with _client(monkeypatch) as client:
        page = client.get("/p/film/workspace?stage=research")
        assert page.status_code == 200
        assert "DIRECTOR WORKSPACE" in page.text
        assert "/ui/workspace/workspace.js?v=" in page.text
        assert client.get("/ui/workspace/workspace.js").status_code == 200
        assert client.get("/ui/workspace/workspace.css").status_code == 200
        assert client.get("/ui/workspace/README.md").status_code == 404
        assert client.get("/p/film").status_code == 200


def test_workspace_shell_gets_do_not_mutate_project_files(
    projects_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("BACKLOT_WORKSPACE_ENABLED", "true")
    before = {
        path.relative_to(projects_root): path.read_bytes()
        for path in projects_root.rglob("*")
        if path.is_file()
    }
    with _client(monkeypatch) as client:
        assert client.get("/p/film/workspace").status_code == 200
        assert client.get("/api/workspace/v1/catalog").status_code == 200
        assert client.get("/api/workspace/v1/projects/film/shell").status_code == 200
    after = {
        path.relative_to(projects_root): path.read_bytes()
        for path in projects_root.rglob("*")
        if path.is_file()
    }
    assert after == before


def test_workspace_browser_source_stays_read_only_and_versioned() -> None:
    source_root = Path(__file__).resolve().parents[2] / "backlot" / "workspace" / "ui"
    source = (source_root / "workspace.js").read_text(encoding="utf-8")
    forbidden = (
        "innerHTML",
        "/api/project/",
        "/api/projects",
        "/media/",
        "/thumb/",
        ".production-units",
        ".batch-v2",
        "board.js",
        "library.js",
    )
    assert not any(token in source for token in forbidden)
    assert 'const API_ROOT = "/api/workspace/v1"' in source


@pytest.fixture
def live_workspace_server(tmp_path: Path) -> str:
    pytest.importorskip("playwright.sync_api")
    projects = tmp_path / "projects"
    projects.mkdir()
    project = projects / "film"
    project.mkdir()
    _write_json(
        project / "project.json",
        {"project_id": "film", "title": "Film", "pipeline_type": "cinematic"},
    )
    other = projects / "other"
    other.mkdir()
    _write_json(
        other / "project.json",
        {"project_id": "other", "title": "Other", "pipeline_type": "cinematic"},
    )
    invalid = projects / "bad-pipeline"
    invalid.mkdir()
    _write_json(
        invalid / "project.json",
        {"project_id": "bad-pipeline", "title": "Bad", "pipeline_type": "not-real"},
    )
    for index in range(51):
        project = projects / f"project-{index:02d}"
        project.mkdir()
        _write_json(
            project / "project.json",
            {
                "project_id": project.name,
                "title": f"Project {index:02d}",
                "pipeline_type": "cinematic",
            },
        )
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    env = dict(os.environ)
    env["BACKLOT_WORKSPACE_ENABLED"] = "true"
    env["OPENMONTAGE_PROJECTS_DIR"] = str(projects)
    server = subprocess.Popen(
        [sys.executable, "-m", "backlot", "serve", "--port", str(port)],
        cwd=Path(__file__).resolve().parents[2],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    deadline = time.time() + 20
    try:
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=1):
                    break
            except OSError:
                time.sleep(0.2)
        else:
            raise RuntimeError("Workspace browser test server did not become healthy")
        yield f"http://127.0.0.1:{port}"
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


def test_workspace_browser_restores_stage_deep_link_and_stays_responsive(
    live_workspace_server: str,
) -> None:
    playwright = pytest.importorskip("playwright.sync_api")
    with playwright.sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 390, "height": 844})
        try:
            page.goto(
                f"{live_workspace_server}/p/film/workspace?stage=research",
                wait_until="networkidle",
            )
            assert page.get_by_role("heading", name="Director Workspace").is_visible()
            assert page.get_by_role("button", name="research").get_attribute("aria-current") == "step"
            search = page.get_by_role("searchbox", name="Search loaded projects")
            search.focus()
            search_node = search.element_handle()
            search.press_sequentially("fi")
            assert search.input_value() == "fi"
            assert page.evaluate("node => node === document.activeElement", search_node)
            assert page.get_by_role("link", name="Film").count() == 1
            search.fill("")
            page.get_by_role("button", name="proposal").click()
            assert "stage=proposal" in page.url
            page.reload(wait_until="networkidle")
            assert page.get_by_role("button", name="proposal").get_attribute("aria-current") == "step"
            assert page.get_by_text("Current stage").is_visible()
            assert page.get_by_text("Capabilities").is_visible()
            assert page.get_by_text("Degraded reasons").is_visible()
            # Conditional refresh is a no-op at the DOM boundary when both
            # visible projections answer 304. A burst has one in-flight and
            # at most one trailing refresh per visible endpoint.
            initial_renders = page.evaluate("() => window.__workspaceDebug.renderCount")
            request_counts = {"catalog": 0, "shell": 0}

            def count_workspace(route):
                if "/catalog" in route.request.url:
                    request_counts["catalog"] += 1
                if "/projects/film/shell" in route.request.url:
                    request_counts["shell"] += 1
                route.continue_()

            page.route("**/api/workspace/v1/**", count_workspace)
            page.evaluate("""() => {
                window.__workspaceDebug.scheduleRefresh('film');
                window.__workspaceDebug.scheduleRefresh('film');
                window.__workspaceDebug.scheduleRefresh('film');
            }""")
            page.wait_for_timeout(500)
            assert request_counts["catalog"] <= 2
            assert request_counts["shell"] <= 2
            assert page.evaluate("() => window.__workspaceDebug.renderCount") == initial_renders
            page.unroute("**/api/workspace/v1/**", count_workspace)
            page.get_by_role("button", name="Load more projects").click()
            assert "stage=proposal" in page.url
            assert page.get_by_text("Authenticated project: film").is_visible()
            page.route(
                "**/api/workspace/v1/projects/other/shell",
                lambda route: (time.sleep(0.4), route.continue_())[1],
            )
            other = page.get_by_role("link", name="Other")
            assert "/p/other/workspace?stage=proposal" in other.get_attribute("href")
            other.click(no_wait_after=True)
            assert page.get_by_text("Authenticated project: film").count() == 0
            page.get_by_role("link", name="Project 00").click(no_wait_after=True)
            page.wait_for_timeout(600)
            assert "/p/project-00/workspace?stage=proposal" in page.url
            assert page.get_by_text("Authenticated project: project-00").is_visible()
            assert page.get_by_text("Authenticated project: other").count() == 0
            page.go_back(wait_until="networkidle")
            assert "/p/other/workspace?stage=proposal" in page.url
            page.go_back(wait_until="networkidle")
            assert "stage=proposal" in page.url
            page.go_back(wait_until="networkidle")
            assert "stage=research" in page.url
            page.goto(f"{live_workspace_server}/p/bad-pipeline/workspace?stage=research", wait_until="networkidle")
            assert page.get_by_text("No validated manifest stage rail is available.").is_visible()
            assert page.get_by_text("Current stage").is_visible()
            assert page.get_by_text("Capabilities").is_visible()
            assert page.get_by_text("Degraded reasons").is_visible()
            size = page.evaluate("() => ({ scroll: document.documentElement.scrollWidth, client: document.documentElement.clientWidth })")
            assert size["scroll"] <= size["client"]
        finally:
            browser.close()
