from __future__ import annotations

import pytest

from lib.production_units.scene_plan_merge import ProductionUnitError
from lib.production_units.script_merge import (
    build_script_units,
    merge_script_units,
    run_script_units,
)
from tests.production_units.test_course_manifest import course_manifest


STYLE_CONTEXT = {
    "style_playbook": "explainer-teacher",
    "tone": "precise and calm",
}


def _units_and_results():
    course = course_manifest()
    units = build_script_units(
        course,
        style_context=STYLE_CONTEXT,
        target_duration_seconds=300,
        hard_max_duration_seconds=480,
    )
    results = [
        {
            "unit_id": units[0]["unit_id"],
            "context_capsule_sha256": units[0]["context_capsule_sha256"],
            "script": {
                "version": "1.0",
                "title": course["title"],
                "total_duration_seconds": course["target_duration_seconds"],
                "voice_performance": {
                    "performance_intent": "calm technical teacher",
                    "pacing_profile": "technical",
                },
                "sections": [
                    {
                        "id": "section-diagnose-a",
                        "text": "First classify what the timeout tells us.",
                        "start_seconds": 0,
                        "end_seconds": 100,
                    },
                    {
                        "id": "section-diagnose-b",
                        "text": "Now separate acceptance from completion.",
                        "start_seconds": 120,
                        "end_seconds": 230,
                    },
                ],
            },
            "section_lesson_ids": [
                {"section_id": "section-diagnose-a", "lesson_id": "lesson-diagnose"},
                {"section_id": "section-diagnose-b", "lesson_id": "lesson-diagnose"},
            ],
        },
        {
            "unit_id": units[1]["unit_id"],
            "context_capsule_sha256": units[1]["context_capsule_sha256"],
            "script": {
                "version": "1.0",
                "title": course["title"],
                "total_duration_seconds": course["target_duration_seconds"],
                "voice_performance": {
                    "performance_intent": "calm technical teacher",
                    "pacing_profile": "technical",
                },
                "sections": [
                    {
                        "id": "section-design-a",
                        "text": "Bind the request to one stable key.",
                        "start_seconds": 250,
                        "end_seconds": 400,
                    },
                    {
                        "id": "section-design-b",
                        "text": "Verify the receipt before retrying.",
                        "start_seconds": 420,
                        "end_seconds": 590,
                    },
                ],
            },
            "section_lesson_ids": [
                {"section_id": "section-design-a", "lesson_id": "lesson-design"},
                {"section_id": "section-design-b", "lesson_id": "lesson-design"},
            ],
        },
    ]
    return course, units, results


def test_build_script_units_uses_approved_lesson_boundaries() -> None:
    course, units, _ = _units_and_results()
    assert [unit["lesson_ids"] for unit in units] == [
        ["lesson-diagnose"],
        ["lesson-design"],
    ]
    assert [(unit["start_seconds"], unit["end_seconds"]) for unit in units] == [
        (0.0, 240.0),
        (240.0, 600.0),
    ]
    assert units[0]["context_capsule"]["boundary_context"]["next_lesson"]["id"] == "lesson-design"
    assert units[1]["course_manifest_sha256"].startswith("sha256:")
    assert course["target_duration_seconds"] == 600


def test_merge_is_deterministic_under_worker_permutation() -> None:
    course, units, results = _units_and_results()
    first = merge_script_units(course, units, results, style_context=STYLE_CONTEXT)
    second = merge_script_units(course, units, reversed(results), style_context=STYLE_CONTEXT)
    assert first == second
    assert [item["id"] for item in first["script"]["sections"]] == [
        "section-diagnose-a",
        "section-diagnose-b",
        "section-design-a",
        "section-design-b",
    ]
    assert {item["lesson_id"] for item in first["section_lesson_ids"]} == {
        "lesson-diagnose",
        "lesson-design",
    }


def test_script_merge_allows_legal_non_narration_gaps() -> None:
    course, units, results = _units_and_results()
    merged = merge_script_units(course, units, results, style_context=STYLE_CONTEXT)
    sections = merged["script"]["sections"]
    assert sections[0]["end_seconds"] < sections[1]["start_seconds"]
    assert sections[-1]["end_seconds"] < merged["script"]["total_duration_seconds"]


@pytest.mark.parametrize(
    ("mutate", "code"),
    [
        (
            lambda units, results: results[0].update(context_capsule_sha256="sha256:" + "0" * 64),
            "STALE_UNIT_RESULT",
        ),
        (lambda units, results: results.pop(), "MISSING_UNIT_RESULT"),
        (
            lambda units, results: results[1]["section_lesson_ids"][0].update(
                lesson_id="lesson-diagnose"
            ),
            "UNIT_OWNERSHIP_VIOLATION",
        ),
        (
            lambda units, results: results[1]["script"]["sections"][0].update(
                start_seconds=200
            ),
            "UNIT_OWNERSHIP_VIOLATION",
        ),
        (
            lambda units, results: results[1]["script"]["voice_performance"].update(
                pacing_profile="energetic"
            ),
            "VOICE_PERFORMANCE_DRIFT",
        ),
    ],
)
def test_script_merge_fails_closed(mutate, code: str) -> None:
    course, units, results = _units_and_results()
    mutate(units, results)
    with pytest.raises(ProductionUnitError) as caught:
        merge_script_units(course, units, results, style_context=STYLE_CONTEXT)
    assert caught.value.code == code


def test_tampered_unit_plan_is_rejected() -> None:
    course, units, results = _units_and_results()
    units[0]["context_capsule"]["course_identity"]["title"] = "Changed"
    with pytest.raises(ProductionUnitError) as caught:
        merge_script_units(course, units, results, style_context=STYLE_CONTEXT)
    assert caught.value.code == "STALE_UNIT_PLAN"


def test_off_mode_has_strict_noop_parity() -> None:
    assert run_script_units(mode="off", course_manifest={"invalid": object()}) is None
    assert run_script_units(mode=None, style_context={"invalid": object()}) is None


def test_legacy_publish_candidate_alias_is_only_an_in_memory_candidate() -> None:
    course, _, results = _units_and_results()
    report = run_script_units(
        mode="publish_candidate",
        course_manifest=course,
        style_context=STYLE_CONTEXT,
        unit_results=results,
        target_duration_seconds=300,
        hard_max_duration_seconds=480,
    )
    assert report is not None
    assert report["policy_mode"] == "auto"
    assert report["policy_mode_authority"] == "none_legacy_diagnostic"
    assert report["execution_contract"]["legacy_mode_alias_used"] is True
    assert report["execution_disposition"] == "publish_candidate"
    assert report["publish_allowed"] is True
    assert report["candidate"]["script_sha256"].startswith("sha256:")


def test_canonical_policy_and_disposition_route_script_units() -> None:
    course, _, results = _units_and_results()
    policy = {
        "mode": "fixed",
        "target_seconds": 300,
        "hard_max_seconds": 480,
        "boundary_priority": "semantic_first",
        "oversize_policy": "allow_with_reason",
        "enabled_stages": ["script"],
    }
    report = run_script_units(
        production_unit_policy=policy,
        execution_disposition="publish_candidate",
        course_manifest=course,
        style_context=STYLE_CONTEXT,
        unit_results=results,
    )
    assert report is not None
    assert report["policy_mode"] == "fixed"
    assert (
        report["policy_mode_authority"]
        == "validated_proposal_checkpoint_required"
    )
    assert report["execution_contract"]["legacy_mode_alias_used"] is False
    assert report["execution_disposition"] == "publish_candidate"
    assert report["mode"] == "publish_candidate"  # M2-M5 output alias
    assert report["execution_contract"]["stage"] == "script"
    assert (
        report["execution_contract"]["contract_sha256"]
        == report["execution_contract_sha256"]
    )
