"""Versioned, projection-only Workspace v1 HTTP boundary."""

from __future__ import annotations

import asyncio
import json
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
import re
import time
from typing import Any, Callable
from weakref import WeakSet

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse

from backlot.workspace.projection.catalog import CatalogCursorError, CatalogProjectionResolver
from backlot.workspace.projection.shell import ShellProjectionNotFound, ShellProjectionResolver


def _bad_request(code: str) -> HTTPException:
    return HTTPException(status_code=422, detail={"code": code})


def _decode_cursor(cursor: str | None) -> dict | None:
    if cursor is None:
        return None
    try:
        parsed = json.loads(cursor)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise _bad_request("invalid_cursor") from exc
    if not isinstance(parsed, dict):
        raise _bad_request("invalid_cursor")
    return parsed


def _decode_limit(limit: str | None) -> int | None:
    """Parse the query transport before FastAPI can expose its error shape."""
    if limit is None:
        return None
    if not re.fullmatch(r"[0-9]+", limit):
        raise _bad_request("invalid_limit")
    try:
        return int(limit)
    except ValueError as exc:
        raise _bad_request("invalid_limit") from exc


_CACHE_TTL_SECONDS = 30.0
_CACHE_MAX_ENTRIES = 128
_CACHE_REGISTRY: dict[str, WeakSet["WorkspaceRuntime"]] = {}


def _quoted_etag(projection: dict[str, Any]) -> str:
    """Return the HTTP validator represented by the projection source set."""
    return '"' + projection["source_snapshot"]["composite_sha256"] + '"'


def _if_none_match_matches(request: Request, etag: str) -> bool:
    """Use only exact validators; an invalid header is simply a cache miss."""
    values = request.headers.get("if-none-match", "")
    return etag in {value.strip() for value in values.split(",")}


@dataclass(frozen=True)
class _CacheEntry:
    projection: dict[str, Any]
    etag: str
    project_ids: frozenset[str]
    expires_at: float


class WorkspaceRuntime:
    """Bounded, disposable server-memory projection cache.

    Entries contain only validated projection JSON.  They never retain raw
    producer files and are invalidated by the existing project watcher.
    """

    def __init__(self) -> None:
        self._entries: OrderedDict[str, _CacheEntry] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.invalidations = 0

    def resolve(
        self, key: str, project_ids: frozenset[str], resolver: Callable[[], dict[str, Any]]
    ) -> tuple[dict[str, Any], str, bool]:
        now = time.monotonic()
        entry = self._entries.get(key)
        if entry is not None and entry.expires_at > now:
            self.hits += 1
            self._entries.move_to_end(key)
            return entry.projection, entry.etag, True
        if entry is not None:
            self._entries.pop(key, None)
        self.misses += 1
        projection = resolver()
        etag = _quoted_etag(projection)
        self._entries[key] = _CacheEntry(
            projection=projection,
            etag=etag,
            project_ids=project_ids,
            expires_at=now + _CACHE_TTL_SECONDS,
        )
        self._entries.move_to_end(key)
        while len(self._entries) > _CACHE_MAX_ENTRIES:
            self._entries.popitem(last=False)
        return projection, etag, False

    def invalidate_project(self, project_id: str) -> None:
        keys = [
            key for key, entry in self._entries.items()
            if not entry.project_ids or project_id in entry.project_ids
        ]
        for key in keys:
            self._entries.pop(key, None)
        if keys:
            self.invalidations += len(keys)

    def clear(self) -> None:
        self._entries.clear()


def invalidate_workspace_projection_caches(projects_root: Path, project_id: str) -> None:
    """Watcher hook; a catalog entry has an empty project scope and is global."""
    for runtime in list(_CACHE_REGISTRY.get(str(Path(projects_root).resolve()), WeakSet())):
        runtime.invalidate_project(project_id)


def _projection_response(request: Request, projection: dict[str, Any], etag: str) -> Response:
    headers = {"ETag": etag, "Cache-Control": "no-cache"}
    if _if_none_match_matches(request, etag):
        return Response(status_code=304, headers=headers)
    return JSONResponse(projection, headers=headers)


def _workspace_change_payload(project_id: str) -> dict[str, str]:
    """The sole Workspace event payload: a deliberately coarse invalidation."""
    return {"type": "change", "project_id": project_id}


async def workspace_event_stream(
    subscribe: Callable[[str | None], Any],
    unsubscribe: Callable[[Any], None],
    request: Request,
    *,
    heartbeat_seconds: float = 15.0,
):
    """Yield coarse events without losing distinct project ids in a burst."""
    queue = subscribe(None)
    pending: list[str] = []
    try:
        yield "data: {\"type\":\"hello\"}\n\n"
        while True:
            if await request.is_disconnected():
                return
            if pending:
                yield "data: " + json.dumps(_workspace_change_payload(pending.pop(0))) + "\n\n"
                continue
            try:
                changed = await asyncio.wait_for(queue.get(), timeout=heartbeat_seconds)
            except asyncio.TimeoutError:
                yield "data: {\"type\":\"heartbeat\"}\n\n"
                continue
            changed_ids = {changed}
            while not queue.empty():
                try:
                    changed_ids.add(queue.get_nowait())
                except asyncio.QueueEmpty:
                    break
            pending.extend(sorted(project_id for project_id in changed_ids if isinstance(project_id, str)))
    finally:
        unsubscribe(queue)


def create_workspace_router(
    projects_root: Path,
    *,
    subscribe: Callable[[str | None], Any] | None = None,
    unsubscribe: Callable[[Any], None] | None = None,
) -> tuple[APIRouter, WorkspaceRuntime]:
    """Create the default-off server's opt-in Workspace v1 router.

    This layer has no direct reader imports: projection resolvers remain the
    sole authority boundary between HTTP and canonical project observations.
    """
    router = APIRouter(prefix="/api/workspace/v1")
    catalog = CatalogProjectionResolver(projects_root)
    shell = ShellProjectionResolver(projects_root)
    runtime = WorkspaceRuntime()
    _CACHE_REGISTRY.setdefault(str(Path(projects_root).resolve()), WeakSet()).add(runtime)

    @router.get("/catalog")
    async def get_catalog(
        request: Request,
        limit: str | None = Query(default=None), cursor: str | None = Query(default=None)
    ) -> Response:
        try:
            decoded_limit = _decode_limit(limit)
            decoded_cursor = _decode_cursor(cursor)
            key = "catalog:" + json.dumps(
                {"limit": decoded_limit, "cursor": decoded_cursor},
                sort_keys=True, separators=(",", ":"),
            )
            projection, etag, _ = runtime.resolve(
                key, frozenset(),
                lambda: catalog.resolve(limit=decoded_limit, cursor=decoded_cursor),
            )
            return _projection_response(request, projection, etag)
        except CatalogCursorError as exc:
            raise _bad_request("invalid_cursor") from exc
        except ValueError as exc:
            raise _bad_request("invalid_limit") from exc

    @router.get("/projects/{project_id}/shell")
    async def get_shell(project_id: str, request: Request) -> Response:
        try:
            projection, etag, _ = runtime.resolve(
                f"shell:{project_id}", frozenset({project_id}),
                lambda: shell.resolve(project_id),
            )
            return _projection_response(request, projection, etag)
        except ShellProjectionNotFound as exc:
            raise HTTPException(status_code=404, detail={"code": "workspace_project_not_found"}) from exc

    if subscribe is not None and unsubscribe is not None:
        @router.get("/events")
        async def workspace_events(request: Request) -> StreamingResponse:
            return StreamingResponse(workspace_event_stream(subscribe, unsubscribe, request), media_type="text/event-stream", headers={
                "Cache-Control": "no-cache", "X-Accel-Buffering": "no",
            })

    return router, runtime


__all__ = [
    "WorkspaceRuntime",
    "create_workspace_router",
    "invalidate_workspace_projection_caches",
    "workspace_event_stream",
]
