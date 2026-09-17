"""B1C Style projection regressions: exact selection, catalog seam, no writes."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backlot.workspace.api_v1.router import create_workspace_router
from backlot.workspace.projection.contracts import (
    WorkspaceContractError,
    validate_workspace_projection,
)
from backlot.workspace.projection.style import StyleProjectionResolver
from lib.checkpoint import init_project, write_checkpoint
from tests.contracts.test_phase0_contracts import sample_artifact


def _project(root: Path, *, status: str = "completed", approved: bool = True) -> dict:
    init_project(
        "style-demo",
        title="Style",
        pipeline_type="animated-explainer",
        pipeline_dir=root,
    )
    write_checkpoint(
        root,
        "style-demo",
        "research",
        "completed",
        {"research_brief": sample_artifact("research_brief")},
        pipeline_type="animated-explainer",
    )
    proposal = sample_artifact("proposal_packet")
    proposal["production_plan"].update(
        {
            "playbook": "flat-motion-graphics",
            "renderer_family": "explainer-data",
            "composition_mode": "templated",
            "art_direction": "Clean diagrams",
        }
    )
    proposal["concept_options"][0]["suggested_playbook"] = "ink-sketch"
    write_checkpoint(
        root,
        "style-demo",
        "proposal",
        status,
        {"proposal_packet": proposal},
        pipeline_type="animated-explainer",
        human_approved=approved,
    )
    return proposal


def test_style_projection_resolves_exact_selected_proposal_and_catalog(
    tmp_path: Path,
) -> None:
    proposal = _project(tmp_path)
    projection = StyleProjectionResolver(tmp_path).resolve("style-demo")
    style = projection["data"]["style"]
    assert (
        style["proposal"]["selected_concept"]["concept_id"]
        == proposal["selected_concept"]["concept_id"]
    )
    assert style["proposal"]["playbook"] == "flat-motion-graphics"
    assert style["resolved_style"]["playbook"] == "flat-motion-graphics"
    assert style["resolved_style"]["historically_frozen"] is False
    assert style["observations"]["scene_plan"]["state"] == "not_yet_corroborated"


def test_style_awaiting_candidate_never_resolves_catalog_current(
    tmp_path: Path,
) -> None:
    _project(tmp_path, status="awaiting_human", approved=False)
    projection = StyleProjectionResolver(tmp_path).resolve("style-demo")
    assert projection["authority"]["authority_state"] == "unavailable"
    assert (
        projection["data"]["style"]["proposal_authority"]["authority_state"]
        == "candidate"
    )
    assert projection["data"]["style"]["resolved_style"] is None


def test_style_conflict_and_invalid_catalog_fail_closed(tmp_path: Path) -> None:
    _project(tmp_path)
    marker = tmp_path / "style-demo" / "project.json"
    value = json.loads(marker.read_text(encoding="utf-8"))
    value["style_playbook"] = "minimalist-diagram"
    marker.write_text(json.dumps(value), encoding="utf-8")
    assert (
        StyleProjectionResolver(tmp_path).resolve("style-demo")["data"]["style"][
            "resolved_style"
        ]
        is None
    )


def test_style_observes_all_manifest_checkpoint_claims_and_invalid_scene(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    research = tmp_path / "style-demo" / "checkpoint_research.json"
    value = json.loads(research.read_text(encoding="utf-8"))
    value["style_playbook"] = "minimalist-diagram"
    research.write_text(json.dumps(value), encoding="utf-8")
    projection = StyleProjectionResolver(tmp_path).resolve("style-demo")
    assert projection["data"]["style"]["resolved_style"] is None
    assert any(
        item["stage"] == "research" and item["value"] == "minimalist-diagram"
        for item in projection["data"]["style"]["checkpoint_observations"]
    )
    (tmp_path / "style-demo" / "checkpoint_scene_plan.json").write_text(
        "{}", encoding="utf-8"
    )
    projection = StyleProjectionResolver(tmp_path).resolve("style-demo")
    assert (
        projection["data"]["style"]["observations"]["scene_plan"]["state"] == "invalid"
    )
    assert projection["data"]["style"]["resolved_style"] is None


def test_style_contract_rejects_forged_resolved_observation_conflict(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    projection = StyleProjectionResolver(tmp_path).resolve("style-demo")
    projection["data"]["style"]["observations"]["project_marker"] = {
        "state": "present",
        "value": "minimalist-diagram",
    }
    with pytest.raises(
        WorkspaceContractError, match="style_resolved_observation_conflict"
    ):
        validate_workspace_projection(projection)
    _project(tmp_path)
    checkpoint = tmp_path / "style-demo" / "checkpoint_proposal.json"
    value = json.loads(checkpoint.read_text(encoding="utf-8"))
    value["artifacts"]["proposal_packet"]["production_plan"]["playbook"] = "../escape"
    checkpoint.write_text(json.dumps(value), encoding="utf-8")
    assert (
        StyleProjectionResolver(tmp_path).resolve("style-demo")["data"]["style"][
            "resolved_style"
        ]
        is None
    )


@pytest.mark.parametrize(
    ("status", "expected_state", "expected_checkpoint"),
    [
        ("in_progress", "display_only", "in_progress"),
        ("failed", "display_only", "failed"),
        ("awaiting_human", "candidate", "awaiting_human"),
        ("completed", "canonical", "completed"),
    ],
)
def test_style_checkpoint_observation_uses_actual_lifecycle(
    tmp_path: Path, status: str, expected_state: str, expected_checkpoint: str
) -> None:
    _project(tmp_path)
    write_checkpoint(
        tmp_path,
        "style-demo",
        "research",
        status,
        {"research_brief": sample_artifact("research_brief")},
        pipeline_type="animated-explainer",
        human_approved=status == "completed",
        style_playbook="flat-motion-graphics",
    )
    observation = next(
        item
        for item in StyleProjectionResolver(tmp_path).resolve("style-demo")["data"][
            "style"
        ]["checkpoint_observations"]
        if item["stage"] == "research"
    )
    assert observation["authority"]["authority_state"] == expected_state
    assert observation["authority"]["checkpoint_status"] == expected_checkpoint


def test_style_conflict_keeps_approved_proposal_field_group(tmp_path: Path) -> None:
    _project(tmp_path)
    marker = tmp_path / "style-demo" / "project.json"
    value = json.loads(marker.read_text(encoding="utf-8"))
    value["style_playbook"] = "minimalist-diagram"
    marker.write_text(json.dumps(value), encoding="utf-8")
    style = StyleProjectionResolver(tmp_path).resolve("style-demo")["data"]["style"]
    assert style["resolved_style"] is None
    assert style["proposal"]["availability"] == "available"
    assert style["proposal_authority"]["authority_state"] == "canonical"


def test_invalid_non_scene_checkpoint_is_a_200_degraded_style_projection(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    (tmp_path / "style-demo" / "checkpoint_script.json").write_text(
        "{}", encoding="utf-8"
    )
    app = FastAPI()
    router, _ = create_workspace_router(tmp_path)
    app.include_router(router)
    with TestClient(app) as client:
        response = client.get("/api/workspace/v1/projects/style-demo/style")
    assert response.status_code == 200
    assert response.json()["data"]["style"]["resolved_style"] is None
    assert response.json()["authority"]["authority_state"] == "unavailable"


def test_style_ordinary_and_invalid_proposal_projects_are_200_unavailable(
    tmp_path: Path,
) -> None:
    init_project(
        "ordinary",
        title="Ordinary",
        pipeline_type="animated-explainer",
        pipeline_dir=tmp_path,
    )
    ordinary = StyleProjectionResolver(tmp_path).resolve("ordinary")
    assert ordinary["data"]["style"]["proposal"]["availability"] == "unavailable"
    assert ordinary["data"]["style"]["resolved_style"] is None
    _project(tmp_path)
    (tmp_path / "style-demo" / "checkpoint_proposal.json").write_text(
        "{}", encoding="utf-8"
    )
    app = FastAPI()
    router, _ = create_workspace_router(tmp_path)
    app.include_router(router)
    with TestClient(app) as client:
        for project_id in ("ordinary", "style-demo"):
            response = client.get(f"/api/workspace/v1/projects/{project_id}/style")
            assert response.status_code == 200
            assert response.json()["data"]["style"]["resolved_style"] is None


def test_style_contract_binds_checkpoint_and_proposal_authority_to_exact_stage_source(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    research = tmp_path / "style-demo" / "checkpoint_research.json"
    research_value = json.loads(research.read_text(encoding="utf-8"))
    research_value["style_playbook"] = "flat-motion-graphics"
    research.write_text(json.dumps(research_value), encoding="utf-8")
    projection = StyleProjectionResolver(tmp_path).resolve("style-demo")
    checkpoint_observations = projection["data"]["style"]["checkpoint_observations"]
    research_observation = next(
        item for item in checkpoint_observations if item["stage"] == "research"
    )
    research_index = checkpoint_observations.index(research_observation)
    forged_observation = deepcopy(projection)
    forged_observation["data"]["style"]["checkpoint_observations"][
        research_index
    ]["authority"]["evidence_refs"] = deepcopy(
        projection["data"]["style"]["proposal_authority"]["evidence_refs"]
    )
    with pytest.raises(
        WorkspaceContractError, match="style_checkpoint_observation_unbound"
    ):
        validate_workspace_projection(forged_observation)

    marker = tmp_path / "style-demo" / "project.json"
    marker_value = json.loads(marker.read_text(encoding="utf-8"))
    marker_value["style_playbook"] = "minimalist-diagram"
    marker.write_text(json.dumps(marker_value), encoding="utf-8")
    unresolved = StyleProjectionResolver(tmp_path).resolve("style-demo")
    assert unresolved["data"]["style"]["resolved_style"] is None
    forged_proposal = deepcopy(unresolved)
    forged_proposal["data"]["style"]["proposal_authority"]["evidence_refs"] = deepcopy(
        research_observation["authority"]["evidence_refs"]
    )
    with pytest.raises(WorkspaceContractError, match="style_field_authority_unbound"):
        validate_workspace_projection(forged_proposal)


def test_style_wire_is_closed_and_catalog_extras_do_not_leak(tmp_path: Path) -> None:
    _project(tmp_path)
    projection = StyleProjectionResolver(tmp_path).resolve("style-demo")
    value = deepcopy(projection)
    value["data"]["style"]["resolved_style"]["catalog"]["identity"]["path"] = "secret"
    with pytest.raises(WorkspaceContractError):
        validate_workspace_projection(value)


def test_style_endpoint_is_project_scoped_cached_and_no_write(tmp_path: Path) -> None:
    _project(tmp_path)
    before = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    app = FastAPI()
    router, runtime = create_workspace_router(tmp_path)
    app.include_router(router)
    with TestClient(app) as client:
        first = client.get("/api/workspace/v1/projects/style-demo/style")
        assert first.status_code == 200 and first.headers["etag"]
        assert (
            client.get(
                "/api/workspace/v1/projects/style-demo/style",
                headers={"If-None-Match": first.headers["etag"]},
            ).status_code
            == 304
        )
        assert client.get("/api/workspace/v1/projects/missing/style").status_code == 404
    after = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    assert after == before and runtime.hits >= 1


def test_style_inspector_is_proposal_lazy_and_read_only() -> None:
    source = (
        Path(__file__).resolve().parents[2] / "backlot/workspace/ui/workspace.js"
    ).read_text(encoding="utf-8")
    assert "Style Inspector / 風格檢視" in source
    assert "style:${projectId}" in source
    assert 'selectedStage().selected !== "proposal"' in source
    assert "Style identity could not be authenticated." in source
    assert (
        "save"
        not in source.lower()
        .split("function renderstyleinspector", 1)[1]
        .split("function renderscriptinspector", 1)[0]
    )
