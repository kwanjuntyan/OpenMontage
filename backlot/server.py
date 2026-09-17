"""Backlot server — FastAPI app: board state API, SSE change feed, media.

The watcher observes ``projects/`` with watchfiles; on any change it bumps a
per-project version and wakes SSE subscribers, who tell the browser to
refetch state. The server never writes to project directories.
"""

from __future__ import annotations

import asyncio
import json
import mimetypes
import os as _os
import time
from contextlib import asynccontextmanager, suppress
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from backlot.state import (
    PROJECTS_DIR,
    REPO_ROOT,
    _read_contained_project_json,
    load_board_state,
    summarize_project,
)
from lib.identity import InvalidProjectIdError, resolve_project_dir

# Ensure standard MIME types on Windows (where .js is often mapped to text/plain)
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("text/css", ".css")

UI_DIR = Path(__file__).resolve().parent / "ui"
WORKSPACE_UI_DIR = Path(__file__).resolve().parent / "workspace" / "ui"
WORKSPACE_UI_ASSETS = frozenset({"workspace.css", "workspace.js"})
THUMB_CACHE_DIR = REPO_ROOT / ".backlot" / "thumbs"
THUMB_WIDTHS = (320, 640, 960)

# Paths inside a project whose changes are pure noise for the board.
_IGNORE_PARTS = {
    "node_modules",
    ".git",
    "__pycache__",
    ".cache",
    ".production-units",
}

SSE_HEARTBEAT_SECONDS = 15


def _ui_html(name: str, assets: tuple[str, ...]) -> HTMLResponse:
    html = (UI_DIR / name).read_text(encoding="utf-8")
    for asset in assets:
        path = UI_DIR / asset
        if path.is_file():
            version = str(int(path.stat().st_mtime))
            html = html.replace(f"/ui/{asset}", f"/ui/{asset}?v={version}")
    return HTMLResponse(html)


def _workspace_html() -> HTMLResponse:
    """Render the separately-owned, opt-in Workspace browser shell."""
    html = (WORKSPACE_UI_DIR / "workspace.html").read_text(encoding="utf-8")
    for asset in WORKSPACE_UI_ASSETS:
        path = WORKSPACE_UI_DIR / asset
        version = str(int(path.stat().st_mtime))
        html = html.replace(
            f"/ui/workspace/{asset}", f"/ui/workspace/{asset}?v={version}"
        )
    return HTMLResponse(html)


class ChangeHub:
    """Fan-out of project-change notifications to SSE subscribers.

    Subscriptions are filtered: a board subscribed to one project only ever
    receives that project's ids, so unrelated-project bursts can't flood its
    queue and starve out the one notification it actually needs.
    """

    def __init__(self) -> None:
        self._subscribers: dict[asyncio.Queue, Optional[str]] = {}

    def subscribe(self, project_id: Optional[str] = None) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=64)
        self._subscribers[q] = project_id
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        self._subscribers.pop(q, None)

    def publish(self, project_id: str) -> None:
        for q, only in list(self._subscribers.items()):
            if only is not None and only != project_id:
                continue
            try:
                q.put_nowait(project_id)
            except asyncio.QueueFull:
                # Queue holds only THIS subscriber's relevant ids, so a full
                # queue already guarantees a pending wake-up → safe to drop.
                pass


hub = ChangeHub()

# Library summaries are expensive to derive (full state parse per project);
# cache per project and invalidate from the watcher.
_summary_cache: dict[str, dict] = {}


def _invalidate_summary(project_id: str) -> None:
    _summary_cache.pop(project_id, None)


def _cached_summaries() -> list[dict]:
    if not PROJECTS_DIR.is_dir():
        return []
    summaries = []
    for entry in sorted(PROJECTS_DIR.iterdir()):
        if not entry.is_dir() or entry.name.startswith(("_", ".")):
            continue
        try:
            # The projects API is a separate cached enumeration path, so it
            # must enforce the same direct-child identity invariant as the
            # state library.  In-root aliases and out-of-root links are not
            # projects merely because ``Path.is_dir()`` follows them.
            safe_entry = resolve_project_dir(PROJECTS_DIR, entry.name)
        except InvalidProjectIdError:
            _summary_cache.pop(entry.name, None)
            continue
        cached = _summary_cache.get(entry.name)
        if cached is None:
            try:
                cached = summarize_project(safe_entry)
            except Exception:
                cached = {
                    "project_id": entry.name, "title": entry.name,
                    "pipeline_type": "unknown", "has_pipeline_state": False,
                    "poster": None, "live": False, "last_activity": 0,
                    "active_stage": None, "awaiting_human": False,
                    "stage_states": [], "completed_count": 0,
                    "render_count": 0, "scene_count": 0, "error": "unreadable",
                }
            _summary_cache[entry.name] = cached
        summaries.append(cached)
    summaries.sort(key=lambda s: (not s["live"], -(s["last_activity"] or 0)))
    return summaries


# Watch-loop hot path: pure string comparison, no per-path filesystem calls
# (change batches can be thousands of paths during a render).
_PROJECTS_ROOT_STR = _os.path.normcase(str(PROJECTS_DIR.resolve()))


def _project_of_change(path_str: str) -> Optional[str]:
    """Map a changed filesystem path to a project id (None = irrelevant)."""
    norm = _os.path.normcase(_os.path.normpath(path_str))
    if not norm.startswith(_PROJECTS_ROOT_STR):
        return None
    rel = norm[len(_PROJECTS_ROOT_STR):].lstrip("\\/")
    if not rel:
        return None
    parts = rel.replace("\\", "/").split("/")
    if _IGNORE_PARTS.intersection(parts):
        return None
    return parts[0]


async def _watch_projects() -> None:
    """Background task: watch projects/ and publish debounced changes."""
    try:
        from watchfiles import awatch
    except ImportError:
        return  # watcher unavailable → board still works via manual refresh
    if not PROJECTS_DIR.is_dir():
        return
    async for changes in awatch(PROJECTS_DIR, recursive=True, step=400):
        touched: set[str] = set()
        for _change, path_str in changes:
            pid = _project_of_change(path_str)
            if pid:
                touched.add(pid)
        for pid in touched:
            _invalidate_summary(pid)
            # Workspace cache is process-memory only.  Importing this inert
            # hook when the flag is off registers no cache or routes.
            try:
                from backlot.workspace.api_v1.router import invalidate_workspace_projection_caches
                invalidate_workspace_projection_caches(PROJECTS_DIR, pid)
            except Exception:
                pass
            hub.publish(pid)


@asynccontextmanager
async def _lifespan(app: FastAPI):
    """Own and cleanly stop the project watcher with FastAPI's lifespan API."""
    try:
        from lib.git_bootstrap import ensure_git_hooks
        ensure_git_hooks()
    except Exception:
        pass

    task = asyncio.create_task(_watch_projects())
    app.state.watch_task = task
    try:
        yield
    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


def create_app() -> FastAPI:
    app = FastAPI(title="Backlot", docs_url=None, redoc_url=None, lifespan=_lifespan)
    workspace_enabled = _os.environ.get("BACKLOT_WORKSPACE_ENABLED", "").casefold() in {
        "1", "true", "yes", "on"
    }

    if workspace_enabled:
        # Deliberately import and register only after the server-side startup
        # decision.  Flag-off retains the legacy Board's complete route tree.
        from backlot.workspace.api_v1.router import create_workspace_router
        workspace_router, workspace_runtime = create_workspace_router(
            PROJECTS_DIR, subscribe=hub.subscribe, unsubscribe=hub.unsubscribe
        )
        app.state.workspace_runtime = workspace_runtime
        app.include_router(workspace_router)

    # ---- API ----------------------------------------------------------

    @app.get("/api/health")
    async def health() -> dict:
        return {"ok": True, "app": "backlot"}

    @app.get("/api/projects")
    async def projects() -> list:
        return await asyncio.to_thread(_cached_summaries)

    @app.get("/api/project/{project_id}/state")
    async def project_state(project_id: str) -> dict:
        project_dir = _safe_project_dir(project_id)
        return await asyncio.to_thread(load_board_state, project_dir)

    @app.post("/api/project/{project_id}/sync_gcs")
    async def sync_project_gcs(project_id: str) -> dict:
        project_dir = _safe_project_dir(project_id)
        from lib.gcs_storage import gcs_storage
        if not gcs_storage.is_configured():
            return {"ok": False, "error": "GCS not configured"}
        gcs_storage.async_sync_project_assets(project_dir)
        return {"ok": True, "project_id": project_id, "status": "sync_started"}

    @app.get("/api/project/{project_id}/events")
    async def project_events(project_id: str, request: Request) -> StreamingResponse:
        _safe_project_dir(project_id)  # 404 early for unknown projects

        async def stream():
            q = hub.subscribe(project_id)
            try:
                yield _sse({"type": "hello", "project_id": project_id})
                while True:
                    if await request.is_disconnected():
                        return
                    try:
                        await asyncio.wait_for(q.get(), timeout=SSE_HEARTBEAT_SECONDS)
                    except asyncio.TimeoutError:
                        yield _sse({"type": "heartbeat", "ts": time.time()})
                        continue
                    # Coalesce bursts: drain anything else queued.
                    while not q.empty():
                        try:
                            q.get_nowait()
                        except asyncio.QueueEmpty:
                            break
                    yield _sse({"type": "change", "project_id": project_id})
            finally:
                hub.unsubscribe(q)

        return StreamingResponse(stream(), media_type="text/event-stream", headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        })

    @app.get("/api/library/events")
    async def library_events(request: Request) -> StreamingResponse:
        async def stream():
            q = hub.subscribe()
            try:
                yield _sse({"type": "hello"})
                while True:
                    if await request.is_disconnected():
                        return
                    try:
                        changed = await asyncio.wait_for(q.get(), timeout=SSE_HEARTBEAT_SECONDS)
                    except asyncio.TimeoutError:
                        yield _sse({"type": "heartbeat", "ts": time.time()})
                        continue
                    while not q.empty():
                        try:
                            q.get_nowait()
                        except asyncio.QueueEmpty:
                            break
                    yield _sse({"type": "change", "project_id": changed})
            finally:
                hub.unsubscribe(q)

        return StreamingResponse(stream(), media_type="text/event-stream", headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        })

    # ---- Cloud URL Resolver --------------------------------------------

    def _resolve_gcs_url(project_dir: Path, file_path: str) -> Optional[str]:
        """Resolves cloud storage URL for missing media assets (renders, CLP, shot videos, images, audio)."""
        filename = Path(file_path).name
        clean_path = file_path.replace("\\", "/").lstrip("/")

        def _objects(data: dict, key: str):
            values = data.get(key)
            if not isinstance(values, list):
                return ()
            return (value for value in values if isinstance(value, dict))

        def _string(value: object) -> Optional[str]:
            return value if isinstance(value, str) and value else None

        # 1. Check artifacts/asset_manifest.json (unified shot video, audio, image registry)
        manifest_path = project_dir / "artifacts" / "asset_manifest.json"
        manifest = _read_contained_project_json(project_dir, manifest_path)
        if manifest is not None:
            for asset in _objects(manifest, "assets"):
                a_path = _string(asset.get("path"))
                asset_id = _string(asset.get("id"))
                gcs_url = _string(asset.get("gcs_url"))
                normalized_path = a_path.replace("\\", "/") if a_path else ""
                if (
                    normalized_path.endswith(filename)
                    or normalized_path == clean_path
                    or asset_id == Path(file_path).stem
                ) and gcs_url:
                    return gcs_url

        # 2. Check artifacts/character_design.json for CLP assets
        cd_path = project_dir / "artifacts" / "character_design.json"
        cd_data = _read_contained_project_json(project_dir, cd_path)
        if cd_data is not None:
            for char in _objects(cd_data, "characters"):
                image = _string(char.get("image"))
                char_img = Path(image).name if image else ""
                char_id = _string(char.get("id"))
                gcs_url = _string(char.get("gcs_url"))
                if (
                    char_img == filename or char_id == Path(file_path).stem
                ) and gcs_url:
                    return gcs_url

        # 3. Check artifacts/render_report.json for final render
        render_report_path = project_dir / "artifacts" / "render_report.json"
        rep = _read_contained_project_json(project_dir, render_report_path)
        if rep is not None:
            output_path = _string(rep.get("output_path"))
            gcs_url = _string(rep.get("gcs_url"))
            if output_path and output_path.endswith(filename) and gcs_url:
                return gcs_url

        # 4. Check project.json for final render
        project_json_path = project_dir / "project.json"
        pdata = _read_contained_project_json(project_dir, project_json_path)
        if pdata is not None:
            gcs_url = _string(pdata.get("gcs_url"))
            if gcs_url and filename.endswith(".mp4"):
                return gcs_url

        # 5. Check GCS mirror path directly if bucket is configured
        try:
            from lib.gcs_storage import gcs_storage
            if gcs_storage.is_configured():
                # Direct 1:1 mirror: projects/<project_id>/<rel_path>
                return gcs_storage.get_public_url(f"projects/{project_dir.name}/{clean_path}")
        except Exception:
            pass

        return None

    # ---- Thumbnails (downscaled, cached on disk) ------------------------

    @app.get("/thumb/{project_id}/{file_path:path}")
    async def thumb(project_id: str, file_path: str, w: int = 640):
        project_dir = _safe_project_dir(project_id)
        target = (project_dir / file_path).resolve()
        try:
            target.relative_to(project_dir.resolve())
        except ValueError:
            raise HTTPException(status_code=403, detail="path escapes project")
        if not target.is_file():
            # If local file missing on disk, fallback to GCS redirect for images/CLP
            gcs_url = _resolve_gcs_url(project_dir, file_path)
            if gcs_url:
                return RedirectResponse(url=gcs_url, status_code=302)
            raise HTTPException(status_code=404, detail="media not found")
        width = min(THUMB_WIDTHS, key=lambda x: abs(x - w))
        cached = await asyncio.to_thread(_thumbnail_for, target, width)
        if cached is None:
            # Never fall back to raw video bytes for an <img> consumer (F-03);
            # non-thumbable images are safe to serve as-is.
            if target.suffix.lower() in {".mp4", ".webm", ".mov"}:
                raise HTTPException(status_code=404, detail="no poster frame available")
            return FileResponse(target)
        return FileResponse(cached, media_type="image/jpeg")

    # ---- Media (range requests handled by FileResponse) ---------------

    @app.get("/media/{project_id}/{file_path:path}")
    async def media(project_id: str, file_path: str):
        project_dir = _safe_project_dir(project_id)
        target = (project_dir / file_path).resolve()
        try:
            target.relative_to(project_dir.resolve())
        except ValueError:
            raise HTTPException(status_code=403, detail="path escapes project")
        if target.is_file():
            return FileResponse(target, headers={"Cache-Control": "no-cache, must-revalidate"})

        # If local media file not found on disk, check if GCS streaming URL exists
        gcs_url = _resolve_gcs_url(project_dir, file_path)
        if gcs_url:
            return RedirectResponse(url=gcs_url, status_code=302)
        raise HTTPException(status_code=404, detail="media not found")

    # ---- UI ------------------------------------------------------------

    @app.get("/p/{project_id}/workspace")
    async def workspace_page(project_id: str) -> HTMLResponse:
        # This route must precede the legacy /p/{project_path:path} catch-all.
        # Its unconditional registration makes the default-off surface a true
        # 404 rather than a Board page at a Workspace-looking URL.
        if not workspace_enabled:
            raise HTTPException(status_code=404, detail="workspace is disabled")
        return _workspace_html()

    @app.get("/p/{project_id}")
    async def board_page(project_id: str) -> HTMLResponse:
        return _ui_html("board.html", ("board.css", "board.js"))

    @app.get("/p/{project_path:path}")
    async def board_page_path(project_path: str) -> HTMLResponse:
        return _ui_html("board.html", ("board.css", "board.js"))

    @app.get("/")
    async def library_page() -> HTMLResponse:
        return _ui_html("index.html", ("board.css", "library.js"))

    if workspace_enabled:
        @app.get("/ui/workspace/{asset_name}")
        async def workspace_asset(asset_name: str):
            # Explicit allowlisting prevents the Workspace source directory
            # (including README.md) from becoming a browsable static tree.
            if asset_name not in WORKSPACE_UI_ASSETS:
                raise HTTPException(status_code=404, detail="workspace asset not found")
            return FileResponse(WORKSPACE_UI_DIR / asset_name)

    if UI_DIR.is_dir():
        app.mount("/ui", StaticFiles(directory=UI_DIR), name="ui")

    # The board is a long-lived SPA: a tab keeps running whatever board.js it
    # loaded, and browsers heuristically cache /ui assets. no-cache forces a
    # conditional revalidation (cheap 304 via ETag) on every load so UI fixes
    # show up on a plain refresh. Media/thumb responses keep normal caching.
    @app.middleware("http")
    async def ui_no_cache(request, call_next):
        response = await call_next(request)
        path = request.url.path
        if path == "/" or path.startswith("/ui") or path.startswith("/p/"):
            response.headers["Cache-Control"] = "no-cache"
        return response

    return app


def _safe_project_dir(project_id: str) -> Path:
    try:
        project_dir = resolve_project_dir(PROJECTS_DIR, project_id)
    except InvalidProjectIdError:
        raise HTTPException(status_code=400, detail="invalid project id")
    if not project_dir.is_dir():
        raise HTTPException(status_code=404, detail=f"unknown project: {project_id}")
    return project_dir


def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


def _thumbnail_for(source: Path, width: int) -> Optional[Path]:
    """Downscale an image (or extract a video poster frame) to a cached JPEG."""
    suffix = source.suffix.lower()
    is_image = suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    is_video = suffix in {".mp4", ".webm", ".mov"}
    if not (is_image or is_video):
        return None
    try:
        import hashlib
        stat = source.stat()
        key = hashlib.sha1(
            f"{source}|{stat.st_mtime_ns}|{stat.st_size}|{width}".encode()
        ).hexdigest()[:20]
        cached = THUMB_CACHE_DIR / f"{key}.jpg"
        if cached.is_file():
            return cached
        THUMB_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        # Unique temp per request — concurrent misses for the same source
        # must not write (and replace from) the same temp file.
        import uuid
        tmp = THUMB_CACHE_DIR / f"{key}.{uuid.uuid4().hex[:8]}.tmp.jpg"
        if is_video:
            import subprocess
            result = subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.5",
                 "-i", str(source), "-frames:v", "1",
                 "-vf", f"scale={width}:-2", str(tmp)],
                capture_output=True, timeout=30,
            )
            if result.returncode != 0 or not tmp.is_file():
                return None
        else:
            from PIL import Image
            with Image.open(source) as img:
                img = img.convert("RGB")
                img.thumbnail((width, width * 3))
                img.save(tmp, "JPEG", quality=82)
        tmp.replace(cached)
        return cached
    except Exception:
        return None


app = create_app()
