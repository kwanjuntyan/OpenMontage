from __future__ import annotations

from copy import deepcopy
from itertools import permutations

import pytest

from lib.clp_validator import canonical_digest, canonical_json_bytes
from lib.production_units import scene_plan_merge as m2a


def _script() -> dict:
    return {
        "version": "1.0",
        "title": "Lean M2a fixture",
        "total_duration_seconds": 360,
        "sections": [
            {
                "id": f"s{index + 1}",
                "label": f"Section {index + 1}",
                "text": f"Narration {index + 1}",
                "start_seconds": index * 60,
                "end_seconds": (index + 1) * 60,
            }
            for index in range(6)
        ],
    }


def _clp() -> dict:
    return {
        "version": "2.0",
        "project_id": "lean-m2a",
        "characters": [],
        "locations": [],
        "props": [],
    }


def _style_context() -> dict:
    return {
        "style_playbook": "clean-professional",
        "proposal_packet_sha256": "sha256:" + "a" * 64,
    }


def _nonempty_clp() -> dict:
    return {
        "version": "2.0",
        "project_id": "lean-m2a",
        "characters": [
            {
                "id": "char-guide",
                "name": "Guide",
                "visual_traits": "blue jacket",
                "prompt_anchor": "guide in a blue jacket",
                "policy": "text_anchor_only",
            }
        ],
        "locations": [
            {
                "id": "loc-classroom",
                "name": "Classroom",
                "environment_description": "bright teaching room",
                "prompt_anchor": "bright teaching room",
                "policy": "text_anchor_only",
            }
        ],
        "props": [
            {
                "id": "prop-board",
                "name": "Board",
                "description": "large teaching board",
                "prompt_anchor": "large teaching board",
                "policy": "text_anchor_only",
            }
        ],
    }


def _units() -> list[dict]:
    return m2a.build_scene_plan_units(
        _script(),
        _clp(),
        style_context=_style_context(),
        target_duration_seconds=120,
        hard_max_duration_seconds=180,
    )


def _results(units: list[dict] | None = None) -> list[dict]:
    units = units or _units()
    sections = {section["id"]: section for section in _script()["sections"]}
    results = []
    for unit in units:
        scenes = []
        bindings = []
        for section_id in unit["section_ids"]:
            section = sections[section_id]
            scene_id = f"scene-{section_id}"
            scenes.append(
                {
                    "id": scene_id,
                    "type": "text_card",
                    "description": f"Visual for {section_id}",
                    "start_seconds": section["start_seconds"],
                    "end_seconds": section["end_seconds"],
                    "script_section_id": section_id,
                }
            )
            bindings.append(
                {"shot_id": scene_id, "character_refs": [], "prop_refs": []}
            )
        results.append(
            {
                "unit_id": unit["unit_id"],
                "context_capsule_sha256": unit["context_capsule_sha256"],
                "scene_plan": {
                    "version": "1.0",
                    "style_playbook": "clean-professional",
                    "scenes": scenes,
                },
                "bindings": bindings,
            }
        )
    return results


def _merge(script: dict, clp: dict, units: list[dict], results) -> dict:
    return m2a.merge_scene_plan_units(
        script,
        clp,
        units,
        results,
        style_context=_style_context(),
    )


def _error_code(exc: pytest.ExceptionInfo[m2a.ProductionUnitError]) -> str:
    return exc.value.code


def test_mode_off_returns_before_touching_inputs(monkeypatch: pytest.MonkeyPatch) -> None:
    def unexpected(*args, **kwargs):  # pragma: no cover - only runs on regression
        raise AssertionError("production-unit planner was called while mode=off")

    monkeypatch.setattr(m2a, "build_scene_plan_units", unexpected)
    assert m2a.run_scene_plan_compare(mode="off", script={"invalid": True}) is None
    assert m2a.run_scene_plan_compare(mode=None) is None


def test_configurable_units_cover_sections_once_and_bound_context() -> None:
    units = _units()
    assert [unit["ordinal"] for unit in units] == [0, 1, 2]
    assert [unit["section_ids"] for unit in units] == [
        ["s1", "s2"],
        ["s3", "s4"],
        ["s5", "s6"],
    ]
    assert [section for unit in units for section in unit["section_ids"]] == [
        "s1", "s2", "s3", "s4", "s5", "s6"
    ]
    for unit in units:
        assert unit["clp_manifest_sha256"] == canonical_digest(_clp())
        assert unit["context_capsule_sha256"] == canonical_digest(unit["context_capsule"])
        assert len(canonical_json_bytes(unit["context_capsule"])) <= 4 * 1024 * 1024


def test_capsule_cannot_be_rehashed_after_source_tampering() -> None:
    units = _units()
    units[0]["context_capsule"]["script_sections"][0]["text"] = "tampered"
    units[0]["context_capsule_sha256"] = canonical_digest(units[0]["context_capsule"])
    with pytest.raises(m2a.ProductionUnitError) as exc:
        _merge(_script(), _clp(), units, _results(_units()))
    assert _error_code(exc) == "CAPSULE_CONTENT_MISMATCH"


@pytest.mark.parametrize(
    ("index", "field", "value"),
    [
        (0, "start_seconds", 1),
        (1, "start_seconds", 61),
        (1, "start_seconds", 59),
        (5, "end_seconds", 359),
    ],
)
def test_source_sections_must_cover_the_complete_course_timeline(
    index: int,
    field: str,
    value: int,
) -> None:
    script = _script()
    script["sections"][index][field] = value
    with pytest.raises(m2a.ProductionUnitError) as exc:
        m2a.build_scene_plan_units(script, _clp(), style_context=_style_context())
    assert _error_code(exc) == "SECTION_TIMELINE_COVERAGE"


def test_stale_result_cannot_be_replayed_against_new_context() -> None:
    old_units = _units()
    old_results = _results(old_units)
    changed_script = _script()
    changed_script["sections"][0]["text"] = "new approved wording"
    current_units = m2a.build_scene_plan_units(
        changed_script,
        _clp(),
        style_context=_style_context(),
        target_duration_seconds=120,
        hard_max_duration_seconds=180,
    )
    with pytest.raises(m2a.ProductionUnitError) as exc:
        _merge(changed_script, _clp(), current_units, old_results)
    assert _error_code(exc) == "STALE_UNIT_RESULT"


def test_merge_is_byte_deterministic_across_arrival_orders() -> None:
    units = _units()
    candidates = {
        canonical_json_bytes(
            _merge(_script(), _clp(), units, arrival)
        )
        for arrival in permutations(_results(units))
    }
    assert len(candidates) == 1


def test_merge_rejects_duplicate_scene_refs() -> None:
    units = _units()
    results = _results(units)
    duplicate = results[0]["scene_plan"]["scenes"][0]["id"]
    results[1]["scene_plan"]["scenes"][0]["id"] = duplicate
    results[1]["bindings"][0]["shot_id"] = duplicate
    with pytest.raises(m2a.ProductionUnitError) as exc:
        _merge(_script(), _clp(), units, results)
    assert _error_code(exc) == "DUPLICATE_SCENE_REF"


@pytest.mark.parametrize(
    ("section_ref", "expected"),
    [(None, "MISSING_SECTION_REF"), ("unknown", "UNKNOWN_SECTION_REF")],
)
def test_merge_rejects_missing_or_unknown_section_refs(
    section_ref: str | None,
    expected: str,
) -> None:
    units = _units()
    results = _results(units)
    scene = results[0]["scene_plan"]["scenes"][0]
    if section_ref is None:
        scene.pop("script_section_id")
    else:
        scene["script_section_id"] = section_ref
    with pytest.raises(m2a.ProductionUnitError) as exc:
        _merge(_script(), _clp(), units, results)
    assert _error_code(exc) == expected


def test_final_clp_bindings_have_exact_coverage_and_digests() -> None:
    units = _units()
    merged = _merge(_script(), _clp(), units, _results(units))
    scene_ids = [scene["id"] for scene in merged["scene_plan"]["scenes"]]
    binding_ids = [row["shot_id"] for row in merged["clp_shot_bindings"]["bindings"]]
    assert binding_ids == scene_ids
    assert merged["clp_shot_bindings"]["source_scene_plan_sha256"] == canonical_digest(
        merged["scene_plan"]
    )
    assert merged["clp_shot_bindings"]["clp_manifest_sha256"] == canonical_digest(_clp())

    missing = _results(units)
    missing[1]["bindings"].pop()
    with pytest.raises(m2a.ProductionUnitError) as exc:
        _merge(_script(), _clp(), units, missing)
    assert _error_code(exc) == "INVALID_CLP_BINDINGS"


@pytest.mark.parametrize("bad_ref", ["missing-character", "char-guide"])
def test_nonempty_clp_refs_are_resolved_and_duplicates_rejected(bad_ref: str) -> None:
    clp = _nonempty_clp()
    units = m2a.build_scene_plan_units(
        _script(),
        clp,
        style_context=_style_context(),
        target_duration_seconds=120,
        hard_max_duration_seconds=180,
    )
    results = _results(units)
    for result in results:
        for binding in result["bindings"]:
            binding.update(
                {
                    "character_refs": ["char-guide"],
                    "location_ref": "loc-classroom",
                    "prop_refs": ["prop-board"],
                    "focal_entity": "char-guide",
                }
            )
    valid = m2a.merge_scene_plan_units(
        _script(), clp, units, results, style_context=_style_context()
    )
    assert len(valid["clp_shot_bindings"]["bindings"]) == 6

    if bad_ref == "char-guide":
        results[0]["bindings"][0]["character_refs"] = [bad_ref, bad_ref]
    else:
        results[0]["bindings"][0]["character_refs"] = [bad_ref]
    with pytest.raises(m2a.ProductionUnitError) as exc:
        m2a.merge_scene_plan_units(
            _script(), clp, units, results, style_context=_style_context()
        )
    assert _error_code(exc) == "INVALID_CLP_BINDINGS"


def test_repair_changes_only_the_target_unit_slice() -> None:
    units = _units()
    before_results = _results(units)
    repaired_results = deepcopy(before_results)
    repaired_results[1]["scene_plan"]["scenes"][0]["description"] = "Repaired visual"

    assert canonical_json_bytes(before_results[0]) == canonical_json_bytes(repaired_results[0])
    assert canonical_json_bytes(before_results[2]) == canonical_json_bytes(repaired_results[2])

    before = _merge(_script(), _clp(), units, before_results)
    after = _merge(_script(), _clp(), units, repaired_results)
    before_scenes = {scene["script_section_id"]: scene for scene in before["scene_plan"]["scenes"]}
    after_scenes = {scene["script_section_id"]: scene for scene in after["scene_plan"]["scenes"]}
    for section_id in ("s1", "s2", "s5", "s6"):
        assert canonical_json_bytes(before_scenes[section_id]) == canonical_json_bytes(after_scenes[section_id])
    assert before_scenes["s3"] != after_scenes["s3"]
    assert before["clp_shot_bindings"]["bindings"] == after["clp_shot_bindings"]["bindings"]


def test_unit_cannot_claim_another_units_section() -> None:
    units = _units()
    results = _results(units)
    results[1]["scene_plan"]["scenes"][0]["script_section_id"] = "s1"
    with pytest.raises(m2a.ProductionUnitError) as exc:
        _merge(_script(), _clp(), units, results)
    assert _error_code(exc) == "UNIT_OWNERSHIP_VIOLATION"


def test_compare_only_never_claims_publication() -> None:
    units = _units()
    baseline = _merge(_script(), _clp(), units, _results(units))
    report = m2a.run_scene_plan_compare(
        mode="compare_only",
        script=_script(),
        clp_manifest=_clp(),
        style_context=_style_context(),
        monolithic_baseline=baseline,
        unit_results=_results(units),
        target_duration_seconds=120,
        hard_max_duration_seconds=180,
    )
    assert report is not None
    assert report["publish_allowed"] is False
    assert "candidate" in report
    assert report["comparison"]["both_cover_all_script_sections"] is True
    assert report["comparison"]["same_scene_ids_in_order"] is True


def test_monolithic_baseline_must_bind_exact_source_context() -> None:
    old_units = _units()
    old_baseline = _merge(_script(), _clp(), old_units, _results(old_units))
    changed_script = _script()
    changed_script["sections"][0]["text"] = "new approved baseline wording"
    current_units = m2a.build_scene_plan_units(
        changed_script,
        _clp(),
        style_context=_style_context(),
        target_duration_seconds=120,
        hard_max_duration_seconds=180,
    )
    current_results = _results(current_units)
    with pytest.raises(m2a.ProductionUnitError) as exc:
        m2a.run_scene_plan_compare(
            mode="compare_only",
            script=changed_script,
            clp_manifest=_clp(),
            style_context=_style_context(),
            monolithic_baseline=old_baseline,
            unit_results=current_results,
            target_duration_seconds=120,
            hard_max_duration_seconds=180,
        )
    assert _error_code(exc) == "STALE_BASELINE"


def test_monolithic_baseline_must_preserve_canonical_scene_order() -> None:
    units = _units()
    results = _results(units)
    baseline = _merge(_script(), _clp(), units, results)
    baseline["scene_plan"]["scenes"].reverse()
    baseline["clp_shot_bindings"]["source_scene_plan_sha256"] = canonical_digest(
        baseline["scene_plan"]
    )
    with pytest.raises(m2a.ProductionUnitError) as exc:
        m2a.run_scene_plan_compare(
            mode="compare_only",
            script=_script(),
            clp_manifest=_clp(),
            style_context=_style_context(),
            monolithic_baseline=baseline,
            unit_results=results,
            target_duration_seconds=120,
            hard_max_duration_seconds=180,
        )
    assert _error_code(exc) == "SCENE_ORDER"


def test_strict_clp_is_checked_in_memory_without_resolving_asset_paths() -> None:
    clp = _nonempty_clp()
    character = clp["characters"][0]
    character["policy"] = "strict_reference"
    character["image"] = "assets/images/not-read-by-m2a.png"
    character["asset_sha256"] = "sha256:" + "b" * 64
    character.pop("prompt_anchor")
    units = m2a.build_scene_plan_units(
        _script(), clp, style_context=_style_context(), target_duration_seconds=120
    )
    assert len(units) == 3


def test_sixty_minute_fixture_merges_with_three_minute_default_units() -> None:
    script = {
        "version": "1.0",
        "title": "Sixty minute deterministic fixture",
        "total_duration_seconds": 3600,
        "sections": [
            {
                "id": f"long-{index + 1:02d}",
                "text": f"Minute {index + 1}",
                "start_seconds": index * 60,
                "end_seconds": (index + 1) * 60,
            }
            for index in range(60)
        ],
    }
    units = m2a.build_scene_plan_units(script, _clp(), style_context=_style_context())
    section_by_id = {section["id"]: section for section in script["sections"]}
    results = []
    for unit in units:
        scenes = []
        bindings = []
        for section_id in unit["section_ids"]:
            section = section_by_id[section_id]
            scene_id = f"scene-{section_id}"
            scenes.append(
                {
                    "id": scene_id,
                    "type": "text_card",
                    "description": section["text"],
                    "start_seconds": section["start_seconds"],
                    "end_seconds": section["end_seconds"],
                    "script_section_id": section_id,
                }
            )
            bindings.append(
                {"shot_id": scene_id, "character_refs": [], "prop_refs": []}
            )
        results.append(
            {
                "unit_id": unit["unit_id"],
                "context_capsule_sha256": unit["context_capsule_sha256"],
                    "scene_plan": {
                        "version": "1.0",
                        "style_playbook": "clean-professional",
                        "scenes": scenes,
                    },
                "bindings": bindings,
            }
        )

    merged = _merge(script, _clp(), units, reversed(results))
    assert len(units) == 20
    assert len(merged["scene_plan"]["scenes"]) == 60
    assert merged["scene_plan"]["scenes"][0]["start_seconds"] == 0
    assert merged["scene_plan"]["scenes"][-1]["end_seconds"] == 3600
