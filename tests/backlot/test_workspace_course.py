"""B1A Course projection regressions: proposal-only and fail closed."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backlot.workspace.api_v1.router import (
    create_workspace_router,
    invalidate_workspace_projection_caches,
)
from backlot.workspace.projection.contracts import (
    WorkspaceContractError,
    validate_workspace_projection,
)
from backlot.workspace.projection.course import CourseProjectionResolver
from lib.checkpoint import init_project, write_checkpoint
from tests.contracts.test_phase0_contracts import sample_artifact
from tests.production_units.test_course_manifest import course_manifest


def _course_project(
    root: Path, *, status: str = "completed", approved: bool = True
) -> dict:
    project_id = "course-demo"
    init_project(
        project_id,
        title="Course",
        pipeline_type="animated-explainer",
        pipeline_dir=root,
    )
    write_checkpoint(
        root,
        project_id,
        "research",
        "completed",
        {"research_brief": sample_artifact("research_brief")},
        pipeline_type="animated-explainer",
    )
    proposal = sample_artifact("proposal_packet")
    proposal["production_plan"]["content_form"] = "course_form"
    course = course_manifest()
    course["project_id"] = project_id
    write_checkpoint(
        root,
        project_id,
        "proposal",
        status,
        {"proposal_packet": proposal, "course_manifest": course},
        pipeline_type="animated-explainer",
        human_approved=approved,
    )
    return course


def test_course_projection_exposes_only_approved_current_proposal(
    tmp_path: Path,
) -> None:
    course = _course_project(tmp_path)
    projection = CourseProjectionResolver(tmp_path).resolve("course-demo")
    current = projection["data"]["current_canonical"]
    assert current["authority"]["authority_state"] == "canonical"
    assert current["data"]["course_design"] == course
    assert projection["data"]["pending_candidates"] == []
    assert projection["data"]["historical_revisions"] == []
    assert current["capabilities"]["mutate"] == {
        "available": False,
        "reason": "observer_only",
    }


def test_course_projection_never_promotes_awaiting_candidate_or_loose_file(
    tmp_path: Path,
) -> None:
    _course_project(tmp_path, status="awaiting_human", approved=False)
    loose = course_manifest()
    loose["project_id"] = "course-demo"
    (tmp_path / "course-demo" / "artifacts").mkdir(exist_ok=True)
    (tmp_path / "course-demo" / "artifacts" / "course_manifest.json").write_text(
        json.dumps(loose), encoding="utf-8"
    )
    projection = CourseProjectionResolver(tmp_path).resolve("course-demo")
    assert projection["data"]["current_canonical"] is None
    assert len(projection["data"]["pending_candidates"]) == 1
    assert projection["data"]["historical_revisions"] == []
    assert (
        projection["data"]["current_canonical_unavailable_reason"]
        == "not_identifiable_from_current_contract"
    )


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: value["modules"][0].update(target_duration_seconds=601),
        lambda value: value["modules"][0]["lessons"][0]["objective_ids"].append(
            "missing"
        ),
    ],
)
def test_course_projection_rejects_semantically_invalid_current_manifest(
    tmp_path: Path, mutate
) -> None:
    course = _course_project(tmp_path)
    mutate(course)
    checkpoint = tmp_path / "course-demo" / "checkpoint_proposal.json"
    payload = json.loads(checkpoint.read_text(encoding="utf-8"))
    payload["artifacts"]["course_manifest"] = course
    checkpoint.write_text(json.dumps(payload), encoding="utf-8")
    projection = CourseProjectionResolver(tmp_path).resolve("course-demo")
    assert projection["data"]["current_canonical"] is None
    assert (
        projection["data"]["current_canonical_unavailable_reason"]
        == "proposal_checkpoint_invalid"
    )


def test_workspace_contract_rejects_course_nested_unknowns_semantic_breaks_and_id_drift(
    tmp_path: Path,
) -> None:
    _course_project(tmp_path)
    projection = CourseProjectionResolver(tmp_path).resolve("course-demo")
    for mutate in (
        lambda value: value["data"]["current_canonical"]["data"]["course_design"][
            "modules"
        ][0].update(untrusted=True),
        lambda value: value["data"]["current_canonical"]["data"]["course_design"][
            "modules"
        ][0].update(target_duration_seconds=1),
        lambda value: value["data"]["current_canonical"]["data"]["course_design"][
            "modules"
        ][0]["lessons"][0]["objective_ids"].append("missing"),
        lambda value: value["data"]["current_canonical"]["data"][
            "course_design"
        ].update(project_id="other"),
    ):
        value = deepcopy(projection)
        mutate(value)
        with pytest.raises(WorkspaceContractError):
            validate_workspace_projection(value)


def test_workspace_contract_rejects_course_design_on_top_level_noncourse_summary(
    tmp_path: Path,
) -> None:
    _course_project(tmp_path)
    revision_set = CourseProjectionResolver(tmp_path).resolve("course-demo")
    current = revision_set["data"]["current_canonical"]
    value = {
        **revision_set,
        "projection_kind": "resource_summary",
        "data_schema": "backlot.workspace.resource-summary.v1",
        "resource_ref": {
            **revision_set["resource_ref"],
            "kind": "stage",
            "local_id": "proposal",
            "resource_key": "stage_course_demo_proposal",
        },
        "data": current["data"],
    }
    with pytest.raises(WorkspaceContractError, match="course_design"):
        validate_workspace_projection(value)


def test_ordinary_project_has_explicit_unavailable_course_revision_set(
    tmp_path: Path,
) -> None:
    init_project(
        "ordinary", title="Ordinary", pipeline_type="cinematic", pipeline_dir=tmp_path
    )
    projection = CourseProjectionResolver(tmp_path).resolve("ordinary")
    assert projection["data"]["current_canonical"] is None
    assert projection["data"]["pending_candidates"] == []
    assert projection["authority"]["authority_state"] == "unavailable"
    with pytest.raises(ValueError):
        CourseProjectionResolver(tmp_path).resolve("../ordinary")


def test_course_reader_does_not_read_private_or_history_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _course_project(tmp_path)
    private = tmp_path / "course-demo" / ".production-units" / "secret.json"
    private.parent.mkdir()
    private.write_text("{}", encoding="utf-8")
    history = tmp_path / "course-demo" / "history" / "checkpoint_proposal.json"
    history.parent.mkdir()
    history.write_text("{}", encoding="utf-8")
    before = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    original_open = open

    def guarded_open(path, *args, **kwargs):
        assert ".production-units" not in str(path)
        assert "history" not in str(path)
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", guarded_open)
    assert CourseProjectionResolver(tmp_path).resolve("course-demo")["data"][
        "current_canonical"
    ]
    after = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    assert after == before


def test_course_endpoint_is_project_scoped_cached_and_etag_validated(
    tmp_path: Path,
) -> None:
    _course_project(tmp_path)
    app = FastAPI()
    router, runtime = create_workspace_router(tmp_path)
    app.include_router(router)
    before = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    with TestClient(app) as client:
        first = client.get("/api/workspace/v1/projects/course-demo/course")
        assert first.status_code == 200
        assert first.json()["resource_ref"]["project_id"] == "course-demo"
        assert first.headers["etag"]
        cached = client.get(
            "/api/workspace/v1/projects/course-demo/course",
            headers={"If-None-Match": first.headers["etag"]},
        )
        assert cached.status_code == 304
        assert client.get("/api/workspace/v1/projects/%2E%2E/course").status_code in {
            404,
            422,
        }
    after = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    assert after == before
    assert runtime.hits >= 1


def test_course_cache_is_invalidated_by_project_change(tmp_path: Path) -> None:
    _course_project(tmp_path)
    app = FastAPI()
    router, _ = create_workspace_router(tmp_path)
    app.include_router(router)
    with TestClient(app) as client:
        first = client.get("/api/workspace/v1/projects/course-demo/course")
        checkpoint = tmp_path / "course-demo" / "checkpoint_proposal.json"
        payload = json.loads(checkpoint.read_text(encoding="utf-8"))
        payload["artifacts"]["course_manifest"]["title"] = "Changed course title"
        checkpoint.write_text(json.dumps(payload), encoding="utf-8")
        invalidate_workspace_projection_caches(tmp_path, "course-demo")
        second = client.get("/api/workspace/v1/projects/course-demo/course")
    assert second.headers["etag"] != first.headers["etag"]
    assert (
        second.json()["data"]["current_canonical"]["data"]["label"]
        == "Changed course title"
    )


def test_course_inspector_is_proposal_lazy_and_structured() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "backlot"
        / "workspace"
        / "ui"
        / "workspace.js"
    ).read_text(encoding="utf-8")
    assert 'stageName === "proposal"' in source
    assert 'selectedStage().selected !== "proposal"' in source
    assert 'selectedStage(state.shell).selected === "proposal"' in source
    assert "eventProjectId === state.routeProjectId" in source
    assert "Course Inspector / 課程檢視" in source
    assert "Course identity could not be authenticated." in source
    assert 'class: "course-section"' in source
    assert "JSON.stringify(revision.data?.course_design" not in source
    assert "course:${projectId}" in source
    for label in (
        "Entry requirements",
        "Objectives",
        "conditions:",
        "Assessments",
        "Sources",
        "digest:",
        "Glossary",
        "Notation",
        "Delivery requirements",
    ):
        assert label in source
