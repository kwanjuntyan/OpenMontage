"""B0.2D transport, cache, and foundation-performance regressions.

The synthetic shape here is deliberately not a Course projection fixture: B0.2
does not read Course, scene, asset, event, or history authority.  It proves
that those large on-disk inputs cannot inflate the B0.2 catalog/shell surface.
"""

from __future__ import annotations

import asyncio
import builtins
import json
import math
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backlot import server as server_mod
from backlot import state as state_mod
from backlot.workspace.projection.catalog import CatalogProjectionResolver
from backlot.workspace.readers import catalog as catalog_reader
from backlot.workspace.api_v1 import router as router_mod
from backlot.workspace.api_v1.router import WorkspaceRuntime, workspace_event_stream


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _project(root: Path, project_id: str) -> Path:
    project = root / project_id
    project.mkdir(parents=True)
    _write(project / "project.json", {
        "project_id": project_id, "title": project_id, "pipeline_type": "cinematic",
    })
    return project


def _p95(samples: list[float]) -> float:
    """Return nearest-rank p95 for a non-empty sample set."""
    if not samples:
        raise ValueError("p95 requires at least one sample")
    return sorted(samples)[math.ceil(len(samples) * 0.95) - 1]


@pytest.fixture
def workspace_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[TestClient, Path]:
    root = tmp_path / "projects"
    root.mkdir()
    _project(root, "film")
    monkeypatch.setattr(state_mod, "PROJECTS_DIR", root)
    monkeypatch.setattr(server_mod, "PROJECTS_DIR", root)
    monkeypatch.setattr(server_mod, "_PROJECTS_ROOT_STR", str(root.resolve()))
    monkeypatch.setenv("BACKLOT_WORKSPACE_ENABLED", "true")

    async def no_watch() -> None:
        return None

    monkeypatch.setattr(server_mod, "_watch_projects", no_watch)
    return TestClient(server_mod.create_app()), root


def test_workspace_etag_conditional_get_and_memory_cache(
    workspace_client: tuple[TestClient, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    client, root = workspace_client
    before = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}
    with client:
        first = client.get("/api/workspace/v1/projects/film/shell")
        assert first.status_code == 200
        etag = first.headers["etag"]
        assert etag == '"' + first.json()["source_snapshot"]["composite_sha256"] + '"'
        runtime = client.app.state.workspace_runtime
        misses = runtime.misses
        cached = client.get("/api/workspace/v1/projects/film/shell", headers={"If-None-Match": etag})
        assert cached.status_code == 304
        assert cached.content == b""
        assert cached.headers["etag"] == etag
        assert runtime.hits >= 1 and runtime.misses == misses
        after_read = {
            path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()
        }
        assert after_read == before

        catalog_first = client.get("/api/workspace/v1/catalog?limit=50")
        assert catalog_first.status_code == 200
        catalog_etag = catalog_first.headers["etag"]

        # The normal watcher hook invalidates only disposable memory entries.
        from backlot.workspace.api_v1.router import invalidate_workspace_projection_caches
        _write(root / "film" / "project.json", {
            "project_id": "film", "title": "Changed film", "pipeline_type": "cinematic",
        })
        expected_after_change = {
            path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()
        }
        invalidate_workspace_projection_caches(root, "film")
        changed = client.get("/api/workspace/v1/projects/film/shell", headers={"If-None-Match": etag})
        assert changed.status_code == 200
        changed_catalog = client.get(
            "/api/workspace/v1/catalog?limit=50", headers={"If-None-Match": catalog_etag}
        )
        assert changed_catalog.status_code == 200
        assert changed_catalog.headers["etag"] != catalog_etag
        assert changed_catalog.json()["data"]["items"][0]["title"] == "Changed film"
        assert runtime.invalidations >= 1
        runtime.clear()
        assert not runtime._entries
    after = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}
    assert before != after
    assert after == expected_after_change


def test_workspace_sse_payload_is_coarse_filtered_and_flagged(
    workspace_client: tuple[TestClient, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    client, _ = workspace_client
    queue = server_mod.hub.subscribe("film")
    try:
        server_mod.hub.publish("other")
        assert queue.empty()
        server_mod.hub.publish("film")
        assert queue.get_nowait() == "film"
    finally:
        server_mod.hub.unsubscribe(queue)
    with client:
        # Route existence is feature-flagged.  Do not consume a live stream in
        # TestClient: its deliberately unbounded iterator has no disconnect.
        paths = {route.path for route in client.app.routes}
        assert "/api/workspace/v1/events" in paths
    class Request:
        async def is_disconnected(self) -> bool:
            return False

    async def consume() -> list[dict]:
        local_hub = server_mod.ChangeHub()
        stream = workspace_event_stream(local_hub.subscribe, local_hub.unsubscribe, Request())
        assert await anext(stream) == 'data: {"type":"hello"}\n\n'
        local_hub.publish("film")
        local_hub.publish("other")
        payloads = [json.loads((await anext(stream)).removeprefix("data: ")) for _ in range(2)]
        await stream.aclose()
        assert not local_hub._subscribers
        return payloads

    payloads = asyncio.run(consume())
    assert payloads == [
        {"type": "change", "project_id": "film"},
        {"type": "change", "project_id": "other"},
    ]
    assert all(set(payload) == {"type", "project_id"} for payload in payloads)


def test_catalog_reuses_validated_manifest_per_unique_pipeline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for index in range(3):
        _project(tmp_path, f"film-{index:03d}")
    calls = 0
    original = catalog_reader.load_pipeline_readonly

    def counted(pipeline_type: str):
        nonlocal calls
        calls += 1
        return original(pipeline_type)

    monkeypatch.setattr(catalog_reader, "load_pipeline_readonly", counted)
    started = time.perf_counter()
    projection = CatalogProjectionResolver(tmp_path).resolve(limit=50)
    elapsed = time.perf_counter() - started
    assert len(projection["data"]["items"]) == 3
    assert calls == 1
    # OPEN engineering observation only: avoids a runaway regression while
    # formal B0.2 budgets await measured approval on the integration host.
    assert elapsed < 5.0


def test_foundation_benchmark_uses_100_projects_and_records_open_guards(
    workspace_client: tuple[TestClient, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Reproducible B0.2D baseline; limits remain OPEN, not release policy."""
    client, root = workspace_client
    for index in range(99):
        _project(root, f"catalog-{index:03d}")
    project = root / "film"
    _write(project / "artifacts" / "scene_plan.json", {
        "duration_seconds": 2700,
        "sections": [{"id": f"section-{i}"} for i in range(60)],
        "scenes": [{"id": f"scene-{i}"} for i in range(120)],
        "assets": [{"id": f"asset-{i}"} for i in range(240)],
    })
    (project / "events.jsonl").write_text("\n".join(json.dumps({"path": "/private/nope", "i": i}) for i in range(2500)), encoding="utf-8")
    for index in range(100):
        _write(project / "history" / f"checkpoint_script_{index}.json", {"status": "completed"})
    sidecar = project / ".production-units"
    sidecar.mkdir()
    (sidecar / "private.json").write_text("{}", encoding="utf-8")
    opened: list[str] = []
    original_open = builtins.open

    def observed_open(file, *args, **kwargs):
        opened.append(str(file))
        return original_open(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", observed_open)
    catalog_cold: list[float] = []
    shell_cold: list[float] = []
    with client:
        runtime = client.app.state.workspace_runtime
        # The cold sample intentionally resolves all 100 authenticated
        # projects once.  The remaining measurements are cache/conditional
        # transport samples; production budgets remain OPEN.
        for _ in range(5):
            runtime.clear()
            t0 = time.perf_counter()
            response = client.get("/api/workspace/v1/catalog?limit=50")
            catalog_cold.append(time.perf_counter() - t0)
            assert response.status_code == 200 and len(response.json()["data"]["items"]) == 50
        catalog_etag = response.headers["etag"]
        t0 = time.perf_counter()
        catalog_warm = client.get("/api/workspace/v1/catalog?limit=50")
        catalog_warm_s = time.perf_counter() - t0
        t0 = time.perf_counter()
        catalog_304 = client.get("/api/workspace/v1/catalog?limit=50", headers={"If-None-Match": catalog_etag})
        catalog_304_s = time.perf_counter() - t0
        for _ in range(5):
            runtime.clear()
            t0 = time.perf_counter()
            shell = client.get("/api/workspace/v1/projects/film/shell")
            shell_cold.append(time.perf_counter() - t0)
            assert shell.status_code == 200
        shell_etag = shell.headers["etag"]
        t0 = time.perf_counter()
        shell_warm = client.get("/api/workspace/v1/projects/film/shell")
        shell_warm_s = time.perf_counter() - t0
        t0 = time.perf_counter()
        shell_304 = client.get("/api/workspace/v1/projects/film/shell", headers={"If-None-Match": shell_etag})
        shell_304_s = time.perf_counter() - t0
        from backlot.workspace.api_v1.router import invalidate_workspace_projection_caches
        invalidate_workspace_projection_caches(root, "film")
        assert runtime.hits >= 4 and runtime.misses >= 2 and runtime.invalidations >= 1
    assert catalog_warm.status_code == shell_warm.status_code == 200
    assert catalog_304.status_code == shell_304.status_code == 304
    # Test-infrastructure runaway rail only; payload budgets remain OPEN.
    assert len(response.content) < 5 * 1024 * 1024 and len(shell.content) < 5 * 1024 * 1024
    measurements = {
        "catalog_cold_sample_count": len(catalog_cold),
        "catalog_cold_p95_seconds": round(_p95(catalog_cold), 6),
        "catalog_warm_seconds": round(catalog_warm_s, 6),
        "catalog_304_seconds": round(catalog_304_s, 6),
        "shell_cold_sample_count": len(shell_cold),
        "shell_cold_p95_seconds": round(_p95(shell_cold), 6),
        "shell_warm_seconds": round(shell_warm_s, 6),
        "shell_304_seconds": round(shell_304_s, 6),
        "catalog_payload_bytes": len(response.content),
        "shell_payload_bytes": len(shell.content),
        "cache_hits": runtime.hits,
        "cache_misses": runtime.misses,
        "cache_invalidations": runtime.invalidations,
        "marker_open_count": sum(path.replace("\\", "/").endswith("/project.json") for path in opened),
        "manifest_open_count": sum(path.replace("\\", "/").endswith("/cinematic.yaml") for path in opened),
        "checkpoint_open_count": sum("checkpoint_" in path for path in opened),
        "artifact_open_count": sum("/artifacts/" in path.replace("\\", "/") for path in opened),
        "event_open_count": sum(path.replace("\\", "/").endswith("/events.jsonl") for path in opened),
        "history_open_count": sum("/history/" in path.replace("\\", "/") for path in opened),
    }
    print(json.dumps(measurements, sort_keys=True))
    # These are reproducibility safety rails, not approved product budgets.
    assert _p95(catalog_cold) < 120.0 and _p95(shell_cold) < 120.0
    assert catalog_warm_s < 5.0 and shell_warm_s < 5.0 and catalog_304_s < 5.0 and shell_304_s < 5.0
    # B0.2 readers may open authenticated marker/manifest/checkpoint evidence,
    # never the large loose payloads, history, events, or private sidecars.
    forbidden = ("events.jsonl", "history", "artifacts", ".production-units", ".batch-v2")
    assert not any(any(part in path.replace("\\", "/") for part in forbidden) for path in opened)


def test_large_course_shape_is_not_read_or_transferred_by_foundation(
    workspace_client: tuple[TestClient, Path]
) -> None:
    client, root = workspace_client
    project = root / "film"
    _write(project / "artifacts" / "scene_plan.json", {
        "duration_seconds": 2700,
        "sections": [{"id": f"section-{i}"} for i in range(60)],
        "scenes": [{"id": f"scene-{i}"} for i in range(120)],
        "assets": [{"id": f"asset-{i}"} for i in range(240)],
    })
    (project / "events.jsonl").write_text("\n".join(json.dumps({"path": "/private/nope", "i": i}) for i in range(2500)), encoding="utf-8")
    for index in range(100):
        _write(project / "history" / f"checkpoint_script_{index}.json", {"status": "completed"})
    before = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}
    with client:
        catalog = client.get("/api/workspace/v1/catalog?limit=50")
        shell = client.get("/api/workspace/v1/projects/film/shell")
    assert catalog.status_code == shell.status_code == 200
    # Test-infrastructure runaway rail only; payload budgets remain OPEN.
    assert len(catalog.content) < 5 * 1024 * 1024
    assert len(shell.content) < 5 * 1024 * 1024
    assert b"/private/nope" not in catalog.content + shell.content
    after = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}
    assert after == before


def test_cache_eviction_ttl_and_flag_off_rollback(
    workspace_client: tuple[TestClient, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime = WorkspaceRuntime()
    projection = {"source_snapshot": {"composite_sha256": "sha256:" + "0" * 64}}
    now = [0.0]
    monkeypatch.setattr(router_mod.time, "monotonic", lambda: now[0])
    for index in range(130):
        runtime.resolve(f"key-{index}", frozenset({"film"}), lambda: projection)
    assert len(runtime._entries) == 128
    misses = runtime.misses
    runtime.resolve("key-129", frozenset({"film"}), lambda: projection)
    assert runtime.hits == 1
    now[0] = 31.0
    runtime.resolve("key-129", frozenset({"film"}), lambda: projection)
    assert runtime.misses == misses + 1
    runtime.clear()
    assert not runtime._entries

    client, root = workspace_client
    monkeypatch.delenv("BACKLOT_WORKSPACE_ENABLED", raising=False)
    app = server_mod.create_app()
    paths = {route.path for route in app.routes}
    assert "/api/workspace/v1/catalog" not in paths
    assert "/api/project/{project_id}/events" in paths
    assert "/api/library/events" in paths
    assert "/thumb/{project_id}/{file_path:path}" in paths
    assert "/media/{project_id}/{file_path:path}" in paths
    with TestClient(app) as off:
        assert off.get("/api/workspace/v1/catalog").status_code == 404
        assert off.get("/api/workspace/v1/projects/film/shell").status_code == 404
        assert off.get("/api/workspace/v1/events").status_code == 404
        assert off.get("/p/film/workspace").status_code == 404
        assert off.get("/api/projects").status_code == 200
        assert off.get("/api/project/film/state").status_code == 200
        assert off.get("/media/film/missing.mp4").status_code == 404
