from __future__ import annotations

from copy import deepcopy

import pytest

from lib.clp_validator import canonical_digest
from lib.production_units.clp_merge import (
    build_clp_candidate_units,
    merge_clp_candidates,
    run_clp_units,
)
from lib.production_units.scene_plan_merge import ProductionUnitError
from lib.production_units.script_merge import merge_script_units
from tests.production_units.test_script_merge import STYLE_CONTEXT, _units_and_results


def _fixture():
    course, script_units, script_results = _units_and_results()
    script_bundle = merge_script_units(
        course, script_units, script_results, style_context=STYLE_CONTEXT
    )
    units = build_clp_candidate_units(course, script_bundle, script_units)
    unit_results = [
        {
            "unit_id": units[0]["unit_id"],
            "context_capsule_sha256": units[0]["context_capsule_sha256"],
            "extracted_by": "offline-test",
            "candidates": {
                "characters": [
                    {
                        "name": "Instructor",
                        "frequency": 2,
                        "suggested_role": "teacher",
                        "context_snippets": ["classify the timeout"],
                    }
                ],
                "locations": [],
                "props": [
                    {
                        "name": "Idempotency key",
                        "frequency": 1,
                        "context_snippets": ["stable key"],
                    }
                ],
            },
        },
        {
            "unit_id": units[1]["unit_id"],
            "context_capsule_sha256": units[1]["context_capsule_sha256"],
            "extracted_by": "offline-test",
            "candidates": {
                "characters": [
                    {
                        "name": "Instructor",
                        "frequency": 2,
                        "suggested_role": "teacher",
                        "context_snippets": ["verify the receipt"],
                    }
                ],
                "locations": [
                    {
                        "name": "Operations room",
                        "frequency": 1,
                        "context_snippets": ["production incident"],
                    }
                ],
                "props": [
                    {
                        "name": "Idempotency key",
                        "frequency": 2,
                        "context_snippets": ["request key"],
                    }
                ],
            },
        },
    ]
    candidate_doc = {
        "version": "2.0",
        "project_id": course["project_id"],
        "source_script_sha256": canonical_digest(script_bundle["script"]),
        "candidates": {
            category: [
                deepcopy(candidate)
                for result in unit_results
                for candidate in result["candidates"][category]
            ]
            for category in ("characters", "locations", "props")
        },
    }
    resolution = {
        "version": "1.0",
        "project_id": course["project_id"],
        "source_script_sha256": canonical_digest(script_bundle["script"]),
        "candidate_set_sha256": canonical_digest(candidate_doc),
        "resolutions": [
            {
                "candidate_key": "clp-unit-0001:characters:0",
                "disposition": "entity",
                "entity_id": "char-instructor",
            },
            {
                "candidate_key": "clp-unit-0001:props:0",
                "disposition": "entity",
                "entity_id": "prop-key",
            },
            {
                "candidate_key": "clp-unit-0002:characters:0",
                "disposition": "entity",
                "entity_id": "char-instructor",
            },
            {
                "candidate_key": "clp-unit-0002:locations:0",
                "disposition": "entity",
                "entity_id": "loc-operations",
            },
            {
                "candidate_key": "clp-unit-0002:props:0",
                "disposition": "entity",
                "entity_id": "prop-key",
            },
        ],
        "entities": {
            "characters": [
                {
                    "id": "char-instructor",
                    "name": "Instructor",
                    "visual_traits": "calm instructor in a navy shirt",
                    "prompt_anchor": "same calm navy-shirt instructor",
                    "policy": "text_anchor_only",
                }
            ],
            "locations": [
                {
                    "id": "loc-operations",
                    "name": "Operations room",
                    "environment_description": "quiet room with service dashboards",
                    "prompt_anchor": "same quiet operations room",
                    "policy": "text_anchor_only",
                }
            ],
            "props": [
                {
                    "id": "prop-key",
                    "name": "Idempotency key",
                    "description": "a stable request key shown as K",
                    "prompt_anchor": "same blue key marked K",
                    "policy": "text_anchor_only",
                }
            ],
        },
    }
    return course, script_units, script_bundle, units, unit_results, resolution


def test_clp_candidate_units_inherit_exact_script_coverage() -> None:
    course, script_units, bundle, units, _, _ = _fixture()
    assert [item["source_script_unit_id"] for item in units] == [
        item["unit_id"] for item in script_units
    ]
    assert [section for unit in units for section in unit["section_ids"]] == [
        item["id"] for item in bundle["script"]["sections"]
    ]
    assert all(item["course_manifest_sha256"] == canonical_digest(course) for item in units)


def test_agent_resolution_merges_duplicates_deterministically() -> None:
    course, _, bundle, units, results, resolution = _fixture()
    first = merge_clp_candidates(course, bundle, units, results, resolution)
    second = merge_clp_candidates(
        course, bundle, units, reversed(results), deepcopy(resolution)
    )
    assert first == second
    assert len(first["clp_candidates"]["candidates"]["characters"]) == 2
    assert [item["id"] for item in first["clp_manifest"]["characters"]] == [
        "char-instructor"
    ]
    assert first["resolution_map_sha256"].startswith("sha256:")


@pytest.mark.parametrize(
    ("mutate", "code"),
    [
        (
            lambda results, resolution: resolution.update(
                candidate_set_sha256="sha256:" + "0" * 64
            ),
            "STALE_RESOLUTION_MAP",
        ),
        (
            lambda results, resolution: resolution["resolutions"].pop(),
            "RESOLUTION_COVERAGE",
        ),
        (
            lambda results, resolution: resolution["resolutions"][0].update(
                entity_id="prop-key"
            ),
            "CATEGORY_MISMATCH",
        ),
        (
            lambda results, resolution: results[0].update(
                context_capsule_sha256="sha256:" + "0" * 64
            ),
            "STALE_UNIT_RESULT",
        ),
    ],
)
def test_clp_merge_fails_closed(mutate, code: str) -> None:
    course, _, bundle, units, results, resolution = _fixture()
    mutate(results, resolution)
    with pytest.raises(ProductionUnitError) as caught:
        merge_clp_candidates(course, bundle, units, results, resolution)
    assert caught.value.code == code


def test_duplicate_retry_result_does_not_overwrite_prior_result() -> None:
    course, _, bundle, units, results, resolution = _fixture()
    results.append(deepcopy(results[0]))
    with pytest.raises(ProductionUnitError) as caught:
        merge_clp_candidates(course, bundle, units, results, resolution)
    assert caught.value.code == "DUPLICATE_UNIT_RESULT"


def test_zero_entity_course_is_supported() -> None:
    course, _, bundle, units, results, _ = _fixture()
    for result in results:
        result["candidates"] = {category: [] for category in ("characters", "locations", "props")}
    empty_doc = {
        "version": "2.0",
        "project_id": course["project_id"],
        "source_script_sha256": canonical_digest(bundle["script"]),
        "candidates": {category: [] for category in ("characters", "locations", "props")},
    }
    resolution = {
        "version": "1.0",
        "project_id": course["project_id"],
        "source_script_sha256": canonical_digest(bundle["script"]),
        "candidate_set_sha256": canonical_digest(empty_doc),
        "resolutions": [],
        "entities": {category: [] for category in ("characters", "locations", "props")},
    }
    merged = merge_clp_candidates(course, bundle, units, results, resolution)
    assert merged["clp_manifest"]["characters"] == []


def test_off_mode_is_strict_noop() -> None:
    assert run_clp_units(mode="off", course_manifest={"bad": object()}) is None


def test_prepare_only_does_not_require_results_or_resolution() -> None:
    course, script_units, bundle, _, _, _ = _fixture()
    report = run_clp_units(
        mode="compare_only",
        course_manifest=course,
        script_bundle=bundle,
        script_units=script_units,
    )
    assert report is not None
    assert report["publish_allowed"] is False
    assert len(report["units"]) == 2
