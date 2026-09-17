"""Bounded, authority-aware Workspace v1 catalog projection resolver."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from backlot.workspace.projection.contracts import (
    WorkspaceContractError,
    build_source_snapshot,
    validate_workspace_contract,
    validate_workspace_projection,
)
from backlot.workspace.readers.catalog import (
    CatalogProjectInput,
    iter_direct_child_project_ids,
    read_catalog_project_input,
)


DEFAULT_PAGE_LIMIT = 50
MAX_PAGE_LIMIT = 100
CURSOR_VERSION = "backlot.workspace.cursor.v1"
CATALOG_SORT_KEY = "project_id"


class CatalogCursorError(ValueError):
    """Raised when a cursor is malformed, stale, or bound to another snapshot."""


def _digest(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return f"sha256:{sha256(payload).hexdigest()}"


def _resource_key(prefix: str, value: str) -> str:
    return f"{prefix}_{sha256(value.encode('utf-8')).hexdigest()}"


def _project_ref(project_id: str) -> dict[str, Any]:
    return {
        "project_id": project_id,
        "kind": "project",
        "stage": None,
        "local_id": project_id,
        "resource_key": _resource_key("project", project_id),
        "parent_refs": [],
        "relation_refs": [],
    }


def _authority(sources: list[Mapping[str, Any]]) -> dict[str, Any]:
    if not sources:
        return {
            "authority_state": "unavailable",
            "validation_state": "invalid",
            "source_kind": "unavailable",
            "evidence_scope": "none",
            "evidence_refs": [],
            "degraded_reasons": ["no_authenticated_projects"],
        }
    return {
        "authority_state": "execution_evidence",
        "validation_state": "validated",
        "source_kind": "derived_projection",
        "evidence_scope": "manifest_only",
        "evidence_refs": [
            {"source_key": source["source_key"], "sha256": source["sha256"]}
            for source in sources
        ],
        "degraded_reasons": [],
    }


def _capabilities(
    *, paginate: bool = False, unavailable: str | None = None
) -> dict[str, Any]:
    values: dict[str, Any] = {
        "view": {"available": True, "reason": None},
        "mutate": {"available": False, "reason": "observer_only"},
    }
    if paginate:
        values["paginate"] = {"available": True, "reason": None}
    if unavailable is not None:
        values["classification"] = {"available": False, "reason": unavailable}
    return values


def _sources(record: CatalogProjectInput, project_ref: Mapping[str, Any]) -> list[dict[str, Any]]:
    resource_identity = {
        key: project_ref[key]
        for key in ("project_id", "kind", "stage", "local_id", "resource_key")
    }
    sources = [
        {
            "source_key": f"project:{record.project_id}:marker",
            "source_kind": "project_marker",
            "sha256": _digest(record.marker),
            "resource_ref": resource_identity,
        },
    ]
    if record.manifest is not None and record.pipeline_type is not None:
        sources.append(
            {
                "source_key": f"pipeline:{record.pipeline_type}:project:{record.project_id}",
                "source_kind": "pipeline_manifest",
                "sha256": _digest(record.manifest),
                "resource_ref": resource_identity,
            }
        )
    return sources


def _diagnostic(
    code: str,
    message: str,
    snapshot: Mapping[str, Any],
    project_ref: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "code": code,
        "severity": "warning",
        "message": message,
        "source_keys": [source["source_key"] for source in snapshot["sources"]],
        "resource_refs": [
            {
                key: project_ref[key]
                for key in ("project_id", "kind", "stage", "local_id", "resource_key")
            }
        ],
    }


def _item(record: CatalogProjectInput) -> dict[str, Any]:
    title = record.marker.get("title")
    if not isinstance(title, str) or not 1 <= len(title) <= 500:
        raise ValueError("authenticated marker has no usable title")
    project_ref = _project_ref(record.project_id)
    snapshot = build_source_snapshot(_sources(record, project_ref))
    revision = {
        "revision_kind": "projection",
        "revision_id": f"catalog-item-{record.project_id}",
        "sha256": snapshot["composite_sha256"],
    }
    if record.manifest is None:
        manifest_reason = record.manifest_error or "pipeline_manifest_unavailable"
        return {
            "project_ref": project_ref,
            "title": title,
            "classification": "unavailable",
            # The marker's selected pipeline has failed validation, so exposing
            # its raw value could itself violate the closed v1 identifier.
            "pipeline_type": "unavailable",
            "revision_ref": revision,
            "source_snapshot": snapshot,
            "authority": {
                "authority_state": "unavailable",
                "validation_state": "invalid",
                "source_kind": "unavailable",
                "evidence_scope": "manifest_only",
                "evidence_refs": [
                    {"source_key": source["source_key"], "sha256": source["sha256"]}
                    for source in snapshot["sources"]
                ],
                "degraded_reasons": [manifest_reason],
            },
            "capabilities": _capabilities(unavailable=manifest_reason),
            "diagnostics": [
                _diagnostic(
                    manifest_reason,
                    "Selected pipeline manifest is unavailable or invalid; classification is unavailable.",
                    snapshot,
                    project_ref,
                )
            ],
        }
    return {
        "project_ref": project_ref,
        "title": title,
        # Course/candidate classification needs B1-owned checkpoint evidence;
        # marker and manifest authority cannot prove an ordinary project.
        "classification": "unavailable",
        "pipeline_type": record.pipeline_type,
        "revision_ref": revision,
        "source_snapshot": snapshot,
        "authority": _authority(snapshot["sources"]),
        "capabilities": _capabilities(unavailable="classification_evidence_deferred"),
        "diagnostics": [
            _diagnostic(
                "classification_evidence_deferred",
                "Course and candidate classification evidence is deferred to B1.",
                snapshot,
                project_ref,
            )
        ],
    }


def _has_usable_title(record: CatalogProjectInput) -> bool:
    title = record.marker.get("title")
    return isinstance(title, str) and 1 <= len(title) <= 500


def _validate_limit(limit: int | None) -> int:
    if limit is None:
        return DEFAULT_PAGE_LIMIT
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_PAGE_LIMIT:
        raise ValueError(f"limit must be an integer between 1 and {MAX_PAGE_LIMIT}")
    return limit


def _cursor_start(
    cursor: Mapping[str, Any] | None,
    *,
    snapshot_sha256: str,
    resource_keys: list[str],
) -> int:
    if cursor is None:
        return 0
    try:
        cursor = validate_workspace_contract(cursor, "pagination_cursor")
    except WorkspaceContractError as exc:
        raise CatalogCursorError(f"cursor is invalid: {exc.code}") from exc
    if cursor.get("version") != CURSOR_VERSION or cursor.get("direction") != "forward":
        raise CatalogCursorError("cursor version or direction is unsupported")
    if cursor.get("sort_key") != CATALOG_SORT_KEY:
        raise CatalogCursorError("cursor sort key does not match this catalog")
    if cursor.get("snapshot_sha256") != snapshot_sha256:
        raise CatalogCursorError("cursor is stale or belongs to another source snapshot")
    last_key = cursor.get("last_resource_key")
    for index, resource_key in enumerate(resource_keys):
        if resource_key == last_key:
            return index + 1
    raise CatalogCursorError("cursor does not name a project in this source snapshot")


class CatalogProjectionResolver:
    """Resolve a no-write catalog from authenticated direct-child projects only."""

    def __init__(self, projects_root: Path):
        self.projects_root = Path(projects_root)

    def resolve(
        self,
        project_ids: Iterable[str] | None = None,
        *,
        limit: int | None = None,
        cursor: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        page_limit = _validate_limit(limit)
        candidates = (
            iter_direct_child_project_ids(self.projects_root)
            if project_ids is None
            else sorted({value for value in project_ids if isinstance(value, str)})
        )
        # Authenticate all candidate marker identities and retain the complete
        # source set for a snapshot-bound cursor.  Defer expensive item
        # envelope construction until after the requested page is selected.
        # This keeps authority/snapshot semantics intact while avoiding work
        # proportional to every catalog item on a 50-item page request.
        records: list[CatalogProjectInput] = []
        # A catalog snapshot still needs every authenticated item before it
        # can issue a snapshot-bound cursor, but a shared selected pipeline is
        # immutable for this resolve.  Revalidating its manifest hundreds of
        # times is needless unbounded work and does not add authority.
        manifest_cache: dict[str, object] = {}
        for project_id in candidates:
            try:
                record = read_catalog_project_input(
                    self.projects_root, project_id, manifest_cache=manifest_cache
                )
                if _has_usable_title(record):
                    records.append(record)
            except (OSError, ValueError):
                # Invalid/missing evidence cannot produce a guessed identity,
                # canonical classification, or legacy fallback.
                continue

        records.sort(key=lambda record: record.project_id)
        all_sources = [
            source
            for record in records
            for source in _sources(record, _project_ref(record.project_id))
        ]
        snapshot = build_source_snapshot(all_sources)
        resource_keys = [_project_ref(record.project_id)["resource_key"] for record in records]
        start = _cursor_start(
            cursor, snapshot_sha256=snapshot["composite_sha256"], resource_keys=resource_keys
        )
        page_records = records[start : start + page_limit]
        page = [_item(record) for record in page_records]
        has_more = start + page_limit < len(records)
        next_cursor = None
        if has_more:
            next_cursor = {
                "version": CURSOR_VERSION,
                "snapshot_sha256": snapshot["composite_sha256"],
                "sort_key": CATALOG_SORT_KEY,
                "last_resource_key": page[-1]["project_ref"]["resource_key"],
                "direction": "forward",
            }
        projection: dict[str, Any] = {
            "projection_version": "backlot.workspace.v1",
            "projection_kind": "catalog",
            "data_schema": "backlot.workspace.catalog.v1",
            "resource_ref": {
                "project_id": "backlot-workspace",
                "kind": "workspace_catalog",
                "stage": None,
                "local_id": "catalog",
                "resource_key": "workspace_catalog_v1",
                "parent_refs": [],
                "relation_refs": [],
            },
            "revision_ref": (
                {
                    "revision_kind": "projection",
                    "revision_id": "catalog-page-v1",
                    "sha256": snapshot["composite_sha256"],
                }
                if all_sources
                else None
            ),
            "source_snapshot": snapshot,
            "authority": _authority(snapshot["sources"]),
            "capabilities": _capabilities(paginate=True),
            "diagnostics": [],
            "data": {
                "version": "backlot.workspace.catalog.v1",
                "items": page,
                "pagination": {
                    "limit": page_limit,
                    "has_more": has_more,
                    "next_cursor": next_cursor,
                },
            },
        }
        return validate_workspace_projection(projection)


__all__ = [
    "CATALOG_SORT_KEY",
    "CURSOR_VERSION",
    "CatalogCursorError",
    "CatalogProjectionResolver",
    "DEFAULT_PAGE_LIMIT",
    "MAX_PAGE_LIMIT",
]
