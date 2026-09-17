"""Versioned, projection-only Workspace v1 HTTP boundary."""

from __future__ import annotations

import json
from pathlib import Path
import re

from fastapi import APIRouter, HTTPException, Query

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


def create_workspace_router(projects_root: Path) -> APIRouter:
    """Create the default-off server's opt-in Workspace v1 router.

    This layer has no direct reader imports: projection resolvers remain the
    sole authority boundary between HTTP and canonical project observations.
    """
    router = APIRouter(prefix="/api/workspace/v1")
    catalog = CatalogProjectionResolver(projects_root)
    shell = ShellProjectionResolver(projects_root)

    @router.get("/catalog")
    async def get_catalog(
        limit: str | None = Query(default=None), cursor: str | None = Query(default=None)
    ) -> dict:
        try:
            return catalog.resolve(limit=_decode_limit(limit), cursor=_decode_cursor(cursor))
        except CatalogCursorError as exc:
            raise _bad_request("invalid_cursor") from exc
        except ValueError as exc:
            raise _bad_request("invalid_limit") from exc

    @router.get("/projects/{project_id}/shell")
    async def get_shell(project_id: str) -> dict:
        try:
            return shell.resolve(project_id)
        except ShellProjectionNotFound as exc:
            raise HTTPException(status_code=404, detail={"code": "workspace_project_not_found"}) from exc

    return router


__all__ = ["create_workspace_router"]
