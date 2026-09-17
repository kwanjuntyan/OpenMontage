"""B0.2A authenticated, bounded Workspace catalog foundation tests."""

from __future__ import annotations

import builtins
import json
import os
from pathlib import Path

import pytest

from backlot.workspace.projection.catalog import (
    CatalogCursorError,
    CatalogProjectionResolver,
)
from backlot.workspace.projection.contracts import validate_workspace_projection
from lib.checkpoint import CheckpointValidationError, read_project_marker


def _marker(root: Path, project_id: str, *, title: str | None = None, pipeline: str = "cinematic") -> Path:
    project = root / project_id
    project.mkdir(parents=True)
    (project / "project.json").write_text(
        json.dumps(
            {
                "version": "1.0",
                "project_id": project_id,
                "title": title if title is not None else project_id.title(),
                "pipeline_type": pipeline,
            }
        ),
        encoding="utf-8",
    )
    return project


def _tree_snapshot(root: Path) -> dict[str, tuple[bytes, int, int]]:
    return {
        str(path.relative_to(root)): (path.read_bytes(), path.stat().st_mtime_ns, path.stat().st_size)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_public_marker_reader_is_contained_and_authenticates_identity(tmp_path: Path) -> None:
    project = _marker(tmp_path, "valid")
    assert read_project_marker(tmp_path, "valid")["title"] == "Valid"

    (project / "project.json").write_text('{"project_id":"other"}', encoding="utf-8")
    with pytest.raises(CheckpointValidationError, match="identity mismatch"):
        read_project_marker(tmp_path, "valid")
    with pytest.raises(CheckpointValidationError, match="Invalid project_id"):
        read_project_marker(tmp_path, "../valid")


def test_catalog_uses_only_valid_marker_and_manifest_evidence(tmp_path: Path) -> None:
    _marker(tmp_path, "ordinary", title="Ordinary")
    missing = tmp_path / "missing"
    missing.mkdir()
    malformed_json = tmp_path / "malformed-json"
    malformed_json.mkdir()
    (malformed_json / "project.json").write_text("{not json", encoding="utf-8")
    non_object = tmp_path / "non-object"
    non_object.mkdir()
    (non_object / "project.json").write_text("[]", encoding="utf-8")
    _marker(tmp_path, "mismatch")
    (tmp_path / "mismatch" / "project.json").write_text(
        '{"project_id":"elsewhere","title":"Elsewhere","pipeline_type":"cinematic"}',
        encoding="utf-8",
    )
    _marker(tmp_path, "bad-pipeline", pipeline="not-a-real-pipeline")
    _marker(tmp_path, "missing-pipeline", pipeline="")

    projection = CatalogProjectionResolver(tmp_path).resolve()
    items = {
        item["project_ref"]["project_id"]: item for item in projection["data"]["items"]
    }
    assert set(items) == {"bad-pipeline", "missing-pipeline", "ordinary"}
    ordinary = items["ordinary"]
    assert ordinary["classification"] == "unavailable"
    assert ordinary["authority"]["authority_state"] != "canonical"
    assert ordinary["capabilities"]["classification"] == {
        "available": False,
        "reason": "classification_evidence_deferred",
    }
    assert ordinary["diagnostics"][0]["code"] == "classification_evidence_deferred"
    assert ordinary["classification"] not in {"ordinary", "approved_course", "awaiting_course_candidate", "legacy"}
    for project_id, expected_reason in {
        "bad-pipeline": "pipeline_manifest_invalid",
        "missing-pipeline": "pipeline_manifest_unavailable",
    }.items():
        item = items[project_id]
        assert item["classification"] == "unavailable"
        assert item["authority"]["authority_state"] == "unavailable"
        assert item["diagnostics"][0]["code"] == expected_reason
        assert item["capabilities"]["classification"]["reason"] == expected_reason
        assert [source["source_kind"] for source in item["source_snapshot"]["sources"]] == ["project_marker"]
    validate_workspace_projection(projection)


def test_catalog_isolates_schema_invalid_marker_fields(tmp_path: Path) -> None:
    _marker(tmp_path, "good", title="Good")
    _marker(tmp_path, "unsafe-pipeline", title="Unsafe", pipeline="../escape")
    _marker(tmp_path, "oversized-title", title="x" * 501)

    projection = CatalogProjectionResolver(tmp_path).resolve()
    items = {
        item["project_ref"]["project_id"]: item for item in projection["data"]["items"]
    }
    assert set(items) == {"good", "unsafe-pipeline"}
    assert items["unsafe-pipeline"]["pipeline_type"] == "unavailable"
    assert items["unsafe-pipeline"]["classification"] == "unavailable"
    assert items["unsafe-pipeline"]["diagnostics"][0]["code"] == "pipeline_manifest_invalid"
    validate_workspace_projection(projection)


def test_catalog_order_pagination_and_snapshot_bound_cursor(tmp_path: Path) -> None:
    for project_id in ("charlie", "alpha", "bravo"):
        _marker(tmp_path, project_id)
    resolver = CatalogProjectionResolver(tmp_path)
    first = resolver.resolve(limit=2)
    assert [item["project_ref"]["project_id"] for item in first["data"]["items"]] == ["alpha", "bravo"]
    assert first["data"]["pagination"]["has_more"] is True
    second = resolver.resolve(limit=2, cursor=first["data"]["pagination"]["next_cursor"])
    assert [item["project_ref"]["project_id"] for item in second["data"]["items"]] == ["charlie"]

    cursor = first["data"]["pagination"]["next_cursor"]
    assert cursor is not None
    with pytest.raises(CatalogCursorError, match="invalid"):
        resolver.resolve(limit=2, cursor={**cursor, "unexpected": True})
    with pytest.raises(CatalogCursorError, match="invalid"):
        resolver.resolve(limit=2, cursor={key: value for key, value in cursor.items() if key != "last_resource_key"})
    with pytest.raises(CatalogCursorError, match="invalid"):
        resolver.resolve(limit=2, cursor={**cursor, "last_resource_key": 1})
    with pytest.raises(CatalogCursorError, match="sort key"):
        resolver.resolve(limit=2, cursor={**cursor, "sort_key": "title"})
    with pytest.raises(CatalogCursorError, match="does not name"):
        resolver.resolve(limit=2, cursor={**cursor, "last_resource_key": "unknown_key"})

    _marker(tmp_path, "delta")
    with pytest.raises(CatalogCursorError, match="stale"):
        resolver.resolve(limit=2, cursor=cursor)
    with pytest.raises(ValueError, match="between"):
        resolver.resolve(limit=101)


def test_catalog_rejects_alias_and_never_reads_private_sidecars(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _marker(tmp_path, "real")
    sidecar = project / ".production-units"
    sidecar.mkdir()
    (sidecar / "private.json").write_text('{"not":"workspace evidence"}', encoding="utf-8")
    before = _tree_snapshot(tmp_path)
    original_open = builtins.open

    def reject_private_open(file, *args, **kwargs):
        if ".production-units" in str(file):
            raise AssertionError("Workspace catalog attempted a private-sidecar read")
        return original_open(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", reject_private_open)
    projection = CatalogProjectionResolver(tmp_path).resolve()
    assert [item["project_ref"]["project_id"] for item in projection["data"]["items"]] == ["real"]
    assert _tree_snapshot(tmp_path) == before

    alias = tmp_path / "alias"
    try:
        os.symlink(project, alias, target_is_directory=True)
    except OSError:
        pytest.skip("symlink creation is unavailable on this platform")
    assert [item["project_ref"]["project_id"] for item in CatalogProjectionResolver(tmp_path).resolve()["data"]["items"]] == ["real"]
