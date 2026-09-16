from __future__ import annotations

from copy import deepcopy
import json

from backlot import server as server_mod
from backlot import state as state_mod
from backlot.course_projection import _course_delivery_projection
from backlot.state import load_board_state, summarize_project
from lib.checkpoint import init_project, write_checkpoint
from lib.clp_validator import canonical_digest
from tests.contracts.test_phase0_contracts import sample_artifact
from tests.production_units.test_course_manifest import course_manifest


def _course_project(tmp_path, *, project_id: str = "course-board"):
    init_project(
        project_id,
        title="Reliable Systems Course",
        pipeline_type="animated-explainer",
        pipeline_dir=tmp_path,
    )
    write_checkpoint(
        tmp_path,
        project_id,
        "research",
        "completed",
        {"research_brief": sample_artifact("research_brief")},
        pipeline_type="animated-explainer",
    )
    proposal = sample_artifact("proposal_packet")
    proposal["production_plan"].update(
        {
            "content_form": "course_form",
            "production_unit_policy": {
                "mode": "auto",
                "target_seconds": 180,
                "hard_max_seconds": 480,
                "boundary_priority": "semantic_first",
                "oversize_policy": "allow_with_reason",
                "enabled_stages": [
                    "script",
                    "clp",
                    "scene_plan",
                    "assets",
                    "edit",
                    "compose",
                ],
            },
        }
    )
    course = course_manifest()
    course["project_id"] = project_id
    write_checkpoint(
        tmp_path,
        project_id,
        "proposal",
        "completed",
        {
            "proposal_packet": proposal,
            "decision_log": {
                "version": "1.0",
                "project_id": project_id,
                "decisions": [],
            },
            "course_manifest": course,
        },
        pipeline_type="animated-explainer",
        human_approved=True,
    )
    return tmp_path / project_id, course


def test_approved_course_projects_get_outline_and_namespaced_progress(tmp_path) -> None:
    project, course = _course_project(tmp_path)
    write_checkpoint(
        tmp_path,
        project.name,
        "script",
        "in_progress",
        {},
        pipeline_type="animated-explainer",
        metadata={
            "partial_progress": {
                "completed_scene_ids": ["legacy-scene-progress-is-preserved"],
                "production_units": {
                    "total_units": 4,
                    "completed_unit_ids": ["script-u1", "script-u2"],
                    "failed_unit_ids": ["script-u3"],
                    "stale_unit_ids": [],
                    "active_unit_id": "script-u4",
                    "boundary_defect_count": 1,
                    "repair_count": 2,
                },
            }
        },
    )

    state = load_board_state(project)

    assert state["course"]["is_course"] is True
    assert state["course"]["manifest_sha256"] == canonical_digest(course)
    assert state["course"]["module_count"] == 1
    assert state["course"]["lesson_count"] == 2
    assert state["course"]["modules"][0]["lessons"][1]["id"] == "lesson-design"
    assert state["course"]["production_units"]["active"] == {
        "stage": "script",
        "unit_id": "script-u4",
    }
    progress = state["course"]["production_units"]["by_stage"][0]
    assert progress == {
        "stage": "script",
        "total_units": 4,
        "completed_units": 2,
        "failed_units": 1,
        "stale_units": 0,
        "active_unit_id": "script-u4",
        "boundary_defects": 1,
        "repairs": 2,
    }
    script_stage = next(item for item in state["stages"] if item["name"] == "script")
    assert script_stage["partial_progress"]["completed_scene_ids"] == [
        "legacy-scene-progress-is-preserved"
    ]


def test_ordinary_project_state_and_summary_keep_the_legacy_shape(tmp_path) -> None:
    project = init_project(
        "ordinary",
        title="Ordinary",
        pipeline_type="cinematic",
        pipeline_dir=tmp_path,
    )

    state = load_board_state(project)
    summary = summarize_project(project)

    assert "course" not in state
    assert "course" not in summary
    assert "is_course" not in summary


def test_loose_or_mismatched_course_cache_never_becomes_authority(tmp_path) -> None:
    ordinary = init_project(
        "loose-course",
        title="Loose",
        pipeline_type="animated-explainer",
        pipeline_dir=tmp_path,
    )
    loose = course_manifest()
    loose["project_id"] = ordinary.name
    (ordinary / "artifacts" / "course_manifest.json").write_text(
        json.dumps(loose), encoding="utf-8"
    )

    ordinary_state = load_board_state(ordinary)
    assert "course" not in ordinary_state
    assert any(
        item["artifact"] == "course_manifest"
        and item["status"] == "untrusted_cache_ignored"
        for item in ordinary_state["artifact_diagnostics"]
    )

    project, _ = _course_project(tmp_path, project_id="mismatch-course")
    tampered = course_manifest()
    tampered["project_id"] = project.name
    tampered["title"] = "Loose cache tries to win"
    (project / "artifacts" / "course_manifest.json").write_text(
        json.dumps(tampered), encoding="utf-8"
    )

    state = load_board_state(project)
    assert state["course"]["title"] == "Reliable Systems"
    assert any(
        item["artifact"] == "course_manifest"
        and item["status"] == "cache_mismatch_ignored"
        for item in state["artifact_diagnostics"]
    )


def test_invalid_unit_progress_degrades_without_hiding_course(tmp_path) -> None:
    project, _ = _course_project(tmp_path)
    write_checkpoint(
        tmp_path,
        project.name,
        "script",
        "in_progress",
        {},
        pipeline_type="animated-explainer",
        metadata={
            "partial_progress": {
                "production_units": {
                    "total_units": 1,
                    "completed_unit_ids": ["u1"],
                    "failed_unit_ids": ["u1"],
                }
            }
        },
    )

    state = load_board_state(project)
    assert state["course"]["is_course"] is True
    assert state["course"]["production_units"]["by_stage"] == []


def test_delivery_projection_requires_exact_render_digest_and_paths() -> None:
    course = course_manifest()
    report = {
        "version": "1.0",
        "outputs": [
            {
                "path": "renders/course.mp4",
                "format": "mp4",
                "resolution": "1920x1080",
                "duration_seconds": 600,
                "platform_target": "course_master",
            },
            {
                "path": "renders/lesson-design.mp4",
                "format": "mp4",
                "resolution": "1920x1080",
                "duration_seconds": 360,
                "platform_target": "lesson:lesson-design",
            },
        ],
    }
    delivery = {
        "version": "1.0",
        "render_report_sha256": canonical_digest(report),
        "full_master": {"path": "renders/course.mp4"},
        "lesson_exports": [
            {"lesson_id": "lesson-design", "path": "renders/lesson-design.mp4"}
        ],
        "chapter_markers": {"count": 2, "path": "exports/chapters.txt"},
        "captions": [{"format": "vtt", "path": "exports/course.vtt"}],
        "bundle": {"path": "exports/course"},
    }
    checkpoints = {
        "compose": {
            "status": "completed",
            "artifacts": {"render_report": report},
        },
        "publish": {
            "status": "completed",
            "artifacts": {
                "publish_log": {
                    "version": "1.0",
                    "entries": [],
                    "metadata": {"course_delivery": delivery},
                }
            },
        },
    }

    projection = _course_delivery_projection(course, checkpoints)
    assert projection["publish_trace_valid"] is True
    assert projection["full_master"]["status"] == "published"
    assert projection["lesson_exports"][0]["status"] == "published"
    assert projection["captions"] == [{"format": "vtt", "status": "published"}]

    tampered = deepcopy(checkpoints)
    tampered["publish"]["artifacts"]["publish_log"]["metadata"][
        "course_delivery"
    ]["render_report_sha256"] = "sha256:" + "0" * 64
    degraded = _course_delivery_projection(course, tampered)
    assert degraded["publish_trace_valid"] is False
    assert degraded["full_master"]["status"] == "rendered"
    assert degraded["lesson_exports"][0]["status"] == "rendered"
    assert degraded["chapter_markers"]["status"] == "missing"

    escaped = deepcopy(checkpoints)
    escaped_delivery = escaped["publish"]["artifacts"]["publish_log"]["metadata"][
        "course_delivery"
    ]
    escaped_delivery["chapter_markers"]["path"] = "../../outside.txt"
    escaped_delivery["bundle"]["path"] = "C:\\outside"
    escaped_projection = _course_delivery_projection(course, escaped)
    assert escaped_projection["chapter_markers"]["status"] == "missing"
    assert escaped_projection["bundle"]["status"] == "missing"


def test_production_unit_sidecar_is_excluded_from_scans_and_watch() -> None:
    assert ".production-units" in state_mod.SCAN_EXCLUDE
    assert ".production-units" in server_mod._IGNORE_PARTS
    changed = (
        server_mod.PROJECTS_DIR
        / "course"
        / ".production-units"
        / "attempts"
        / "a.json"
    )
    assert server_mod._project_of_change(str(changed)) is None


def test_sidecar_media_cannot_surface_as_a_course_render(tmp_path) -> None:
    project, _ = _course_project(tmp_path)
    hidden = project / ".production-units" / "attempts" / "fake-master.mp4"
    hidden.parent.mkdir(parents=True)
    hidden.write_bytes(b"not a canonical render")

    state = load_board_state(project)
    paths = {
        item["path"]
        for group in state["media"].values()
        if isinstance(group, list)
        for item in group
        if isinstance(item, dict) and "path" in item
    }
    assert not any(".production-units" in path for path in paths)
