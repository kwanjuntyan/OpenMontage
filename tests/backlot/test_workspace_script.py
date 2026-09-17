"""B1B Script projection regressions: owner checkpoint only and fail closed."""

from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from backlot.workspace.api_v1.router import create_workspace_router
from backlot.workspace.projection.contracts import (
    WorkspaceContractError,
    build_source_snapshot,
    validate_workspace_projection,
)
from backlot.workspace.projection.script import ScriptProjectionResolver
from lib.checkpoint import init_project, write_checkpoint
from tests.contracts.test_phase0_contracts import sample_artifact


def _project(root: Path, *, status: str = "completed", approved: bool = True) -> dict:
    init_project(
        "film", title="Film", pipeline_type="animated-explainer", pipeline_dir=root
    )
    write_checkpoint(
        root,
        "film",
        "research",
        "completed",
        {"research_brief": sample_artifact("research_brief")},
        pipeline_type="animated-explainer",
    )
    write_checkpoint(
        root,
        "film",
        "proposal",
        "completed",
        {"proposal_packet": sample_artifact("proposal_packet")},
        pipeline_type="animated-explainer",
        human_approved=True,
    )
    script = sample_artifact("script")
    write_checkpoint(
        root,
        "film",
        "script",
        status,
        {"script": script},
        pipeline_type="animated-explainer",
        human_approved=approved,
    )
    return script


def test_script_owner_checkpoint_is_gated_and_closed(tmp_path: Path) -> None:
    script = _project(tmp_path)
    projection = ScriptProjectionResolver(tmp_path).resolve("film")
    current = projection["data"]["current_canonical"]
    assert current["resource_ref"]["kind"] == "stage"
    assert (
        current["resource_ref"]["stage"]
        == current["resource_ref"]["local_id"]
        == "script"
    )
    assert current["data"]["script"]["sections"] == script["sections"]
    assert "metadata" not in current["data"]["script"]


def test_script_projection_omits_valid_open_producer_cue_extras(tmp_path: Path) -> None:
    script = _project(tmp_path)
    script["sections"][0]["enhancement_cues"] = [
        {"type": "overlay", "description": "Show value.", "producer_only": "omit"}
    ]
    script["sections"][0]["pronunciation_guides"] = [
        {"word": "Foxconn", "phonetic": "foks-kon", "producer_only": "omit"}
    ]
    write_checkpoint(
        tmp_path,
        "film",
        "script",
        "completed",
        {"script": script},
        pipeline_type="animated-explainer",
        human_approved=True,
    )
    projected = ScriptProjectionResolver(tmp_path).resolve("film")["data"][
        "current_canonical"
    ]["data"]["script"]["sections"][0]
    assert projected["enhancement_cues"] == [
        {"type": "overlay", "description": "Show value."}
    ]
    assert projected["pronunciation_guides"] == [
        {"word": "Foxconn", "phonetic": "foks-kon"}
    ]


def test_script_wire_rejects_injected_cue_extras(tmp_path: Path) -> None:
    _project(tmp_path)
    projection = ScriptProjectionResolver(tmp_path).resolve("film")
    section = projection["data"]["current_canonical"]["data"]["script"]["sections"][0]
    section["enhancement_cues"] = [
        {"type": "overlay", "description": "Show value.", "producer_only": "reject"}
    ]
    section["pronunciation_guides"] = [
        {"word": "Foxconn", "phonetic": "foks-kon", "producer_only": "reject"}
    ]
    with pytest.raises(WorkspaceContractError):
        validate_workspace_projection(projection)


def test_script_awaiting_is_candidate_and_legacy_is_ignored(tmp_path: Path) -> None:
    _project(tmp_path, status="awaiting_human", approved=False)
    (tmp_path / "film" / "artifacts").mkdir(exist_ok=True)
    (tmp_path / "film" / "artifacts" / "script.json").write_text(
        '{"version":"1.0"}', encoding="utf-8"
    )
    projection = ScriptProjectionResolver(tmp_path).resolve("film")
    assert projection["data"]["current_canonical"] is None
    assert len(projection["data"]["pending_candidates"]) == 1
    assert (
        projection["data"]["current_canonical_unavailable_reason"]
        == "not_identifiable_from_current_contract"
    )


def test_script_invalid_authority_and_working_state_fail_closed(tmp_path: Path) -> None:
    _project(tmp_path, status="in_progress", approved=False)
    projection = ScriptProjectionResolver(tmp_path).resolve("film")
    assert projection["data"]["current_canonical"] is None
    assert (
        projection["data"]["current_canonical_unavailable_reason"]
        == "script_display_snapshot_unavailable"
    )


def test_script_contract_rejects_wrong_outer_identity(tmp_path: Path) -> None:
    _project(tmp_path)
    projection = ScriptProjectionResolver(tmp_path).resolve("film")
    projection["data"]["current_canonical"]["resource_ref"]["local_id"] = "other"
    try:
        validate_workspace_projection(projection)
    except WorkspaceContractError:
        pass
    else:
        raise AssertionError("wrong Script ResourceRef identity was accepted")


def test_script_contract_rejects_retagged_outer_and_member_identity(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    projection = ScriptProjectionResolver(tmp_path).resolve("film")
    for resource in (
        projection["resource_ref"],
        projection["data"]["current_canonical"]["resource_ref"],
    ):
        resource["stage"] = "retagged"
        resource["local_id"] = "retagged"
    with pytest.raises(WorkspaceContractError, match="script_revision_stage_mismatch"):
        validate_workspace_projection(projection)


def test_script_top_level_summary_rejects_null_revision_ref(tmp_path: Path) -> None:
    _project(tmp_path)
    revision_set = ScriptProjectionResolver(tmp_path).resolve("film")
    current = revision_set["data"]["current_canonical"]
    value = {
        **revision_set,
        "projection_kind": "resource_summary",
        "data_schema": "backlot.workspace.resource-summary.v1",
        "revision_ref": None,
        "data": current["data"],
    }
    with pytest.raises(
        WorkspaceContractError, match="script_checkpoint_revision_required"
    ):
        validate_workspace_projection(value)


def test_script_contract_requires_authority_cited_checkpoint_evidence(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    projection = ScriptProjectionResolver(tmp_path).resolve("film")
    current = projection["data"]["current_canonical"]
    original_sources = projection["source_snapshot"]["sources"]
    checkpoint = next(
        source
        for source in original_sources
        if source["source_kind"] == "approved_checkpoint_artifact"
    )
    uncited = {
        **checkpoint,
        "source_key": "checkpoint:film:script:uncited-authority",
        "resource_ref": {
            **checkpoint["resource_ref"],
            "stage": "other",
            "local_id": "other",
        },
    }
    snapshot = build_source_snapshot([*original_sources, uncited])
    projection["source_snapshot"] = snapshot
    projection["revision_ref"]["sha256"] = snapshot["composite_sha256"]
    current["source_snapshot"] = snapshot
    current["authority"]["evidence_refs"] = [
        {"source_key": uncited["source_key"], "sha256": uncited["sha256"]}
    ]
    with pytest.raises(
        WorkspaceContractError, match="script_evidence_identity_mismatch"
    ):
        validate_workspace_projection(projection)


def test_script_endpoint_is_200_unavailable_or_404_and_cached(tmp_path: Path) -> None:
    _project(tmp_path)
    before = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    app = FastAPI()
    router, _ = create_workspace_router(tmp_path)
    app.include_router(router)
    with TestClient(app) as client:
        first = client.get("/api/workspace/v1/projects/film/script")
        assert first.status_code == 200 and first.headers["etag"]
        assert (
            client.get(
                "/api/workspace/v1/projects/film/script",
                headers={"If-None-Match": first.headers["etag"]},
            ).status_code
            == 304
        )
        assert (
            client.get("/api/workspace/v1/projects/missing/script").status_code == 404
        )
    after = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    assert after == before


def test_script_inspector_is_stage_lazy_and_safe() -> None:
    source = (
        Path(__file__).resolve().parents[2] / "backlot/workspace/ui/workspace.js"
    ).read_text(encoding="utf-8")
    assert "Script Inspector / 劇本檢視" in source
    assert "selectedStage().selected !== owner" in source
    assert "Script identity could not be authenticated." in source
    assert "source_ref is free-form and unverified" in source
    assert (
        "Requested section“" not in source
    )  # DOM output contains a readable quoted warning.
    assert "JSON.stringify(script)" not in source


def test_script_inspector_bulk_controls_are_accessible_and_bounded() -> None:
    source = (
        Path(__file__).resolve().parents[2] / "backlot/workspace/ui/workspace.js"
    ).read_text(encoding="utf-8")
    inspector = source.split("function renderScriptInspector()", 1)[1].split(
        "function renderCourseInspector()", 1
    )[0]
    assert 'text: "全部展開"' in inspector
    assert 'text: "全部收合"' in inspector
    assert 'aria-label": "Expand all script sections"' in inspector
    assert 'aria-label": "Collapse all script sections"' in inspector
    assert 'type: "button"' in inspector
    assert (
        "expandAll.disabled = collapseAll.disabled = details.length === 0" in inspector
    )
    assert "detail.hidden = !matched" in inspector
    assert 'list.textContent = ""' not in inspector
    assert "const setAllOpen = (open)" in inspector
    assert 'role: "status", "aria-live": "polite"' in inspector
