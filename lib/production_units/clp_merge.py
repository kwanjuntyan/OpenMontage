"""Pure M2b CLP candidate aggregation and Agent-resolution validation."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable, Mapping, Sequence

from lib.clp_validator import canonical_digest
from schemas.artifacts import validate_artifact

from .scene_plan_merge import ProductionUnitError
from .contracts import execution_report_fields, resolve_execution_contract


_CATEGORIES = ("characters", "locations", "props")


def _fail(code: str, message: str) -> None:
    raise ProductionUnitError(code, message)


def _validate_script_bundle(
    course_manifest: Mapping[str, Any], script_bundle: Mapping[str, Any]
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    try:
        course = deepcopy(dict(course_manifest))
        validate_artifact("course_manifest", course)
    except Exception as exc:
        _fail("INVALID_COURSE_MANIFEST", str(exc))
    script = script_bundle.get("script")
    mappings = script_bundle.get("section_lesson_ids")
    if not isinstance(script, dict) or not isinstance(mappings, list):
        _fail("INVALID_SCRIPT_BUNDLE", "script bundle requires script and section_lesson_ids")
    try:
        validate_artifact("script", script)
    except Exception as exc:
        _fail("INVALID_SCRIPT_BUNDLE", str(exc))
    if (
        script_bundle.get("course_manifest_sha256") != canonical_digest(course)
        or script_bundle.get("script_sha256") != canonical_digest(script)
    ):
        _fail("STALE_SCRIPT_BUNDLE", "script bundle does not bind exact course and script")
    section_ids = [item["id"] for item in script["sections"]]
    mapped_ids: list[str] = []
    lesson_ids = {
        lesson["id"] for module in course["modules"] for lesson in module["lessons"]
    }
    normalized: list[dict[str, str]] = []
    for item in mappings:
        if not isinstance(item, dict) or set(item) != {"section_id", "lesson_id"}:
            _fail("INVALID_SCRIPT_BUNDLE", "invalid section-to-lesson mapping")
        if item["lesson_id"] not in lesson_ids:
            _fail("INVALID_SCRIPT_BUNDLE", f"unknown lesson {item['lesson_id']!r}")
        mapped_ids.append(item["section_id"])
        normalized.append(deepcopy(item))
    if mapped_ids != section_ids or len(mapped_ids) != len(set(mapped_ids)):
        _fail("INVALID_SCRIPT_BUNDLE", "mapping must cover script sections exactly in order")
    return deepcopy(script), normalized


def build_clp_candidate_units(
    course_manifest: Mapping[str, Any],
    script_bundle: Mapping[str, Any],
    script_units: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Reuse approved script-unit lesson ownership for bounded CLP extraction."""

    script, mappings = _validate_script_bundle(course_manifest, script_bundle)
    course = deepcopy(dict(course_manifest))
    section_by_id = {section["id"]: section for section in script["sections"]}
    lesson_for_section = {item["section_id"]: item["lesson_id"] for item in mappings}
    expected_lessons = [
        lesson["id"] for module in course["modules"] for lesson in module["lessons"]
    ]
    actual_lessons: list[str] = []
    seen_unit_ids: set[str] = set()
    units: list[dict[str, Any]] = []
    for ordinal, raw in enumerate(script_units):
        source_unit = deepcopy(dict(raw))
        unit_id = source_unit.get("unit_id")
        lesson_ids = source_unit.get("lesson_ids")
        if (
            not isinstance(unit_id, str)
            or not unit_id
            or unit_id in seen_unit_ids
            or source_unit.get("ordinal") != ordinal
            or not isinstance(lesson_ids, list)
            or not lesson_ids
        ):
            _fail("INVALID_SCRIPT_UNIT_PLAN", f"invalid script unit at ordinal {ordinal}")
        if source_unit.get("course_manifest_sha256") != canonical_digest(course):
            _fail("STALE_SCRIPT_UNIT_PLAN", f"script unit {unit_id!r} binds another course")
        selected_ids = [
            section_id
            for section_id in section_by_id
            if lesson_for_section[section_id] in lesson_ids
        ]
        if not selected_ids:
            _fail("SECTION_COVERAGE", f"script unit {unit_id!r} owns no script sections")
        capsule = {
            "version": "1.0",
            "project_id": course["project_id"],
            "course_manifest_sha256": canonical_digest(course),
            "source_script_sha256": canonical_digest(script),
            "source_script_unit_id": unit_id,
            "lesson_ids": deepcopy(lesson_ids),
            "script_sections": [deepcopy(section_by_id[item]) for item in selected_ids],
            "course_glossary": deepcopy(course["glossary"]),
        }
        units.append(
            {
                "unit_id": f"clp-unit-{ordinal + 1:04d}",
                "ordinal": ordinal,
                "source_script_unit_id": unit_id,
                "lesson_ids": deepcopy(lesson_ids),
                "section_ids": selected_ids,
                "course_manifest_sha256": canonical_digest(course),
                "source_script_sha256": canonical_digest(script),
                "context_capsule": capsule,
                "context_capsule_sha256": canonical_digest(capsule),
            }
        )
        actual_lessons.extend(lesson_ids)
        seen_unit_ids.add(unit_id)
    if actual_lessons != expected_lessons:
        _fail("LESSON_COVERAGE", "CLP units must inherit exact script-unit lesson coverage")
    covered_sections = [section_id for unit in units for section_id in unit["section_ids"]]
    if covered_sections != list(section_by_id):
        _fail("SECTION_COVERAGE", "CLP units must cover every script section exactly once")
    return units


def _collect_candidates(
    course_manifest: Mapping[str, Any],
    script: Mapping[str, Any],
    units: Sequence[Mapping[str, Any]],
    unit_results: Iterable[Mapping[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    unit_by_id = {unit["unit_id"]: unit for unit in units}
    if len(unit_by_id) != len(units):
        _fail("INVALID_UNIT_PLAN", "duplicate CLP unit id")
    result_by_id: dict[str, dict[str, Any]] = {}
    for raw in unit_results:
        result = deepcopy(dict(raw))
        unit_id = result.get("unit_id")
        if unit_id not in unit_by_id:
            _fail("UNKNOWN_UNIT_RESULT", f"unknown CLP result unit {unit_id!r}")
        if unit_id in result_by_id:
            _fail("DUPLICATE_UNIT_RESULT", f"duplicate CLP result for {unit_id!r}")
        if result.get("context_capsule_sha256") != unit_by_id[unit_id]["context_capsule_sha256"]:
            _fail("STALE_UNIT_RESULT", f"CLP result for {unit_id!r} binds the wrong capsule")
        candidate_doc = {
            "version": "2.0",
            "project_id": course_manifest["project_id"],
            "source_script_sha256": canonical_digest(script),
            "candidates": result.get("candidates"),
        }
        if isinstance(result.get("extracted_by"), str):
            candidate_doc["extracted_by"] = result["extracted_by"]
        try:
            validate_artifact("clp_candidates", candidate_doc)
        except Exception as exc:
            _fail("INVALID_UNIT_CANDIDATES", f"unit {unit_id!r}: {exc}")
        result_by_id[unit_id] = result
    if set(result_by_id) != set(unit_by_id):
        _fail("MISSING_UNIT_RESULT", f"missing CLP results for {sorted(set(unit_by_id) - set(result_by_id))}")

    combined = {category: [] for category in _CATEGORIES}
    indexed: list[dict[str, Any]] = []
    for unit in sorted(units, key=lambda item: item["ordinal"]):
        result = result_by_id[unit["unit_id"]]
        for category in _CATEGORIES:
            for index, candidate in enumerate(result["candidates"][category]):
                key = f"{unit['unit_id']}:{category}:{index}"
                combined[category].append(deepcopy(candidate))
                indexed.append(
                    {
                        "candidate_key": key,
                        "unit_id": unit["unit_id"],
                        "category": category,
                        "candidate": deepcopy(candidate),
                    }
                )
    candidate_doc = {
        "version": "2.0",
        "project_id": course_manifest["project_id"],
        "source_script_sha256": canonical_digest(script),
        "candidates": combined,
    }
    validate_artifact("clp_candidates", candidate_doc)
    return candidate_doc, indexed


def merge_clp_candidates(
    course_manifest: Mapping[str, Any],
    script_bundle: Mapping[str, Any],
    units: Sequence[Mapping[str, Any]],
    unit_results: Iterable[Mapping[str, Any]],
    resolution_map: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one Agent-authored course-wide resolution into canonical CLP."""

    script, _ = _validate_script_bundle(course_manifest, script_bundle)
    candidate_doc, indexed = _collect_candidates(
        course_manifest, script, units, unit_results
    )
    resolution = deepcopy(dict(resolution_map))
    expected_candidate_digest = canonical_digest(candidate_doc)
    if set(resolution) != {
        "version",
        "project_id",
        "source_script_sha256",
        "candidate_set_sha256",
        "resolutions",
        "entities",
    }:
        _fail("INVALID_RESOLUTION_MAP", "resolution map has missing or unknown fields")
    if (
        resolution.get("version") != "1.0"
        or resolution.get("project_id") != course_manifest["project_id"]
        or resolution.get("source_script_sha256") != canonical_digest(script)
        or resolution.get("candidate_set_sha256") != expected_candidate_digest
    ):
        _fail("STALE_RESOLUTION_MAP", "resolution map does not bind exact candidates")
    if not isinstance(resolution.get("resolutions"), list) or not isinstance(
        resolution.get("entities"), dict
    ):
        _fail("INVALID_RESOLUTION_MAP", "resolutions and entities must be structured")
    entities = resolution["entities"]
    if set(entities) != set(_CATEGORIES) or any(
        not isinstance(entities[category], list) for category in _CATEGORIES
    ):
        _fail("INVALID_RESOLUTION_MAP", "entities must contain CLP categories")

    entity_category: dict[str, str] = {}
    for category in _CATEGORIES:
        for entity in entities[category]:
            if not isinstance(entity, dict) or not isinstance(entity.get("id"), str):
                _fail("INVALID_RESOLUTION_MAP", f"invalid {category} entity")
            entity_id = entity["id"]
            if entity_id in entity_category:
                _fail("DUPLICATE_ENTITY_ID", f"duplicate resolved entity {entity_id!r}")
            entity_category[entity_id] = category

    expected_keys = {item["candidate_key"] for item in indexed}
    seen_keys: set[str] = set()
    used_entities: set[str] = set()
    for item in resolution["resolutions"]:
        if not isinstance(item, dict):
            _fail("INVALID_RESOLUTION_MAP", "resolution entries must be objects")
        if set(item) not in ({"candidate_key", "disposition"}, {"candidate_key", "disposition", "entity_id"}):
            _fail("INVALID_RESOLUTION_MAP", "resolution entry fields are invalid")
        candidate_key = item.get("candidate_key")
        if candidate_key not in expected_keys or candidate_key in seen_keys:
            _fail("RESOLUTION_COVERAGE", f"unknown or duplicate candidate key {candidate_key!r}")
        disposition = item.get("disposition")
        if disposition == "ignore":
            if "entity_id" in item:
                _fail("INVALID_RESOLUTION_MAP", "ignored candidates cannot name an entity")
        elif disposition == "entity":
            entity_id = item.get("entity_id")
            candidate_category = next(
                candidate["category"] for candidate in indexed if candidate["candidate_key"] == candidate_key
            )
            if entity_category.get(entity_id) != candidate_category:
                _fail("CATEGORY_MISMATCH", f"candidate {candidate_key!r} maps across CLP categories")
            used_entities.add(entity_id)
        else:
            _fail("INVALID_RESOLUTION_MAP", f"invalid disposition {disposition!r}")
        seen_keys.add(candidate_key)
    if seen_keys != expected_keys:
        _fail("RESOLUTION_COVERAGE", f"unresolved candidates: {sorted(expected_keys - seen_keys)}")
    if used_entities != set(entity_category):
        _fail("UNSOURCED_ENTITY", f"resolved entities lack candidates: {sorted(set(entity_category) - used_entities)}")

    clp_manifest = {
        "version": "2.0",
        "project_id": course_manifest["project_id"],
        **{category: deepcopy(entities[category]) for category in _CATEGORIES},
    }
    try:
        validate_artifact("clp_manifest", clp_manifest)
    except Exception as exc:
        _fail("INVALID_MERGED_CLP", str(exc))
    return {
        "clp_candidates": candidate_doc,
        "clp_manifest": clp_manifest,
        "source_script_sha256": canonical_digest(script),
        "candidate_set_sha256": expected_candidate_digest,
        "resolution_map_sha256": canonical_digest(resolution),
        "clp_manifest_sha256": canonical_digest(clp_manifest),
    }


def run_clp_units(
    *,
    production_unit_policy: Mapping[str, Any] | None = None,
    execution_disposition: str | None = None,
    mode: str | None = None,
    course_manifest: Mapping[str, Any] | None = None,
    script_bundle: Mapping[str, Any] | None = None,
    script_units: Sequence[Mapping[str, Any]] | None = None,
    unit_results: Iterable[Mapping[str, Any]] | None = None,
    resolution_map: Mapping[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Prepare or merge CLP units without publishing a checkpoint."""

    contract = resolve_execution_contract(
        stage="clp",
        production_unit_policy=production_unit_policy,
        execution_disposition=execution_disposition,
        legacy_mode=mode,
    )
    if contract is None:
        return None
    if course_manifest is None or script_bundle is None or script_units is None:
        _fail("MISSING_INPUT", "CLP units require course, merged script, and script units")
    units = build_clp_candidate_units(course_manifest, script_bundle, script_units)
    report: dict[str, Any] = {
        **execution_report_fields(contract),
        "publish_allowed": contract["execution_disposition"] == "publish_candidate",
        "units": units,
    }
    supplied = (unit_results is not None, resolution_map is not None)
    if any(supplied) and not all(supplied):
        _fail("MISSING_INPUT", "CLP merge needs both unit results and resolution map")
    if all(supplied):
        report["candidate"] = merge_clp_candidates(
            course_manifest,
            script_bundle,
            units,
            unit_results or [],
            resolution_map or {},
        )
    return report
