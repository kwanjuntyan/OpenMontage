"""Pure M2b helpers for course-bounded script production units."""

from __future__ import annotations

from copy import deepcopy
import math
from typing import Any, Iterable, Mapping, Sequence

from lib.clp_validator import canonical_digest, canonical_json_bytes
from schemas.artifacts import validate_artifact

from .scene_plan_merge import ProductionUnitError


DEFAULT_TARGET_DURATION_SECONDS = 180.0
DEFAULT_HARD_MAX_DURATION_SECONDS = 480.0
DEFAULT_MAX_CAPSULE_BYTES = 4 * 1024 * 1024
_TOLERANCE = 1e-6


def _fail(code: str, message: str) -> None:
    raise ProductionUnitError(code, message)


def _number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail("INVALID_TIME", f"{field} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        _fail("INVALID_TIME", f"{field} must be a finite number")
    return result


def _validate_course(course_manifest: Mapping[str, Any]) -> dict[str, Any]:
    try:
        course = deepcopy(dict(course_manifest))
        validate_artifact("course_manifest", course)
    except Exception as exc:
        _fail("INVALID_COURSE_MANIFEST", str(exc))
    return course


def _validate_context(style_context: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(style_context, Mapping):
        _fail("INVALID_STYLE_CONTEXT", "style_context must be an object")
    context = deepcopy(dict(style_context))
    if not isinstance(context.get("style_playbook"), str) or not context["style_playbook"]:
        _fail("INVALID_STYLE_CONTEXT", "style_context requires style_playbook")
    try:
        canonical_json_bytes(context)
    except (TypeError, ValueError) as exc:
        _fail("INVALID_STYLE_CONTEXT", str(exc))
    return context


def _course_lessons(course: Mapping[str, Any]) -> list[dict[str, Any]]:
    lessons: list[dict[str, Any]] = []
    cursor = 0.0
    for module in course["modules"]:
        for lesson in module["lessons"]:
            duration = _number(lesson["target_duration_seconds"], "lesson duration")
            item = deepcopy(lesson)
            item["module_id"] = module["id"]
            item["start_seconds"] = cursor
            cursor += duration
            item["end_seconds"] = cursor
            lessons.append(item)
    if abs(cursor - float(course["target_duration_seconds"])) > _TOLERANCE:
        _fail("COURSE_TIMELINE", "lesson timeline does not equal course duration")
    return lessons


def _capsule(
    course: Mapping[str, Any],
    lessons: Sequence[Mapping[str, Any]],
    group: Sequence[Mapping[str, Any]],
    style_context: Mapping[str, Any],
) -> dict[str, Any]:
    lesson_index = {item["id"]: index for index, item in enumerate(lessons)}
    objective_ids = {oid for lesson in group for oid in lesson["objective_ids"]}
    source_ids = {sid for lesson in group for sid in lesson["source_refs"]}
    glossary_ids = {gid for lesson in group for gid in lesson["glossary_ids"]}
    notation_ids = {nid for lesson in group for nid in lesson["notation_ids"]}
    first = lesson_index[group[0]["id"]]
    last = lesson_index[group[-1]["id"]]
    return {
        "version": "1.0",
        "course_identity": {
            "project_id": course["project_id"],
            "title": course["title"],
            "course_promise": deepcopy(course["course_promise"]),
            "target_duration_seconds": course["target_duration_seconds"],
        },
        "lessons": deepcopy(list(group)),
        "objectives": [
            deepcopy(item) for item in course["objectives"] if item["id"] in objective_ids
        ],
        "sources": [
            deepcopy(item) for item in course["sources"] if item["id"] in source_ids
        ],
        "glossary": [
            deepcopy(item) for item in course["glossary"] if item["id"] in glossary_ids
        ],
        "notation": [
            deepcopy(item) for item in course["notation"] if item["id"] in notation_ids
        ],
        "boundary_context": {
            "previous_lesson": (
                {
                    "id": lessons[first - 1]["id"],
                    "title": lessons[first - 1]["title"],
                    "expected_outcome": lessons[first - 1]["expected_outcome"],
                }
                if first > 0
                else None
            ),
            "next_lesson": (
                {
                    "id": lessons[last + 1]["id"],
                    "title": lessons[last + 1]["title"],
                    "expected_outcome": lessons[last + 1]["expected_outcome"],
                }
                if last + 1 < len(lessons)
                else None
            ),
        },
        "style_context": deepcopy(dict(style_context)),
        "course_manifest_sha256": canonical_digest(course),
        "style_context_sha256": canonical_digest(style_context),
    }


def build_script_units(
    course_manifest: Mapping[str, Any],
    *,
    style_context: Mapping[str, Any],
    target_duration_seconds: float = DEFAULT_TARGET_DURATION_SECONDS,
    hard_max_duration_seconds: float = DEFAULT_HARD_MAX_DURATION_SECONDS,
    max_capsule_bytes: int = DEFAULT_MAX_CAPSULE_BYTES,
) -> list[dict[str, Any]]:
    """Group complete lessons at declared curriculum boundaries."""

    course = _validate_course(course_manifest)
    context = _validate_context(style_context)
    target = _number(target_duration_seconds, "target_duration_seconds")
    hard_max = _number(hard_max_duration_seconds, "hard_max_duration_seconds")
    if target <= 0 or hard_max < target:
        _fail("INVALID_UNIT_POLICY", "hard_max must be at least a positive target")
    if isinstance(max_capsule_bytes, bool) or not isinstance(max_capsule_bytes, int) or max_capsule_bytes <= 0:
        _fail("INVALID_UNIT_POLICY", "max_capsule_bytes must be a positive integer")

    lessons = _course_lessons(course)
    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for lesson in lessons:
        lesson_duration = float(lesson["end_seconds"]) - float(lesson["start_seconds"])
        if lesson_duration > hard_max + _TOLERANCE:
            _fail(
                "LESSON_EXCEEDS_HARD_MAX",
                f"lesson {lesson['id']!r} needs a smaller approved lesson boundary",
            )
        if current and float(lesson["end_seconds"]) - float(current[0]["start_seconds"]) > target + _TOLERANCE:
            groups.append(current)
            current = []
        current.append(lesson)
        if float(current[-1]["end_seconds"]) - float(current[0]["start_seconds"]) > hard_max + _TOLERANCE:
            _fail("UNIT_EXCEEDS_HARD_MAX", "approved lesson grouping exceeds hard_max")
    if current:
        groups.append(current)

    units: list[dict[str, Any]] = []
    for ordinal, group in enumerate(groups):
        capsule = _capsule(course, lessons, group, context)
        if len(canonical_json_bytes(capsule)) > max_capsule_bytes:
            _fail("CAPSULE_TOO_LARGE", f"script unit {ordinal + 1} exceeds capsule limit")
        units.append(
            {
                "unit_id": f"script-unit-{ordinal + 1:04d}",
                "ordinal": ordinal,
                "lesson_ids": [item["id"] for item in group],
                "start_seconds": group[0]["start_seconds"],
                "end_seconds": group[-1]["end_seconds"],
                "course_manifest_sha256": canonical_digest(course),
                "style_context_sha256": canonical_digest(context),
                "context_capsule": capsule,
                "context_capsule_sha256": canonical_digest(capsule),
            }
        )
    return units


def _validate_unit_plan(
    course: Mapping[str, Any],
    units: Sequence[Mapping[str, Any]],
    style_context: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    lessons = _course_lessons(course)
    lesson_by_id = {item["id"]: item for item in lessons}
    expected_lesson_ids = [item["id"] for item in lessons]
    actual_lesson_ids: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    for ordinal, raw in enumerate(units):
        unit = deepcopy(dict(raw))
        unit_id = unit.get("unit_id")
        if not isinstance(unit_id, str) or not unit_id or unit_id in by_id:
            _fail("INVALID_UNIT_PLAN", f"invalid or duplicate unit id {unit_id!r}")
        if unit.get("ordinal") != ordinal:
            _fail("UNIT_ORDER", "unit ordinals must be contiguous")
        lesson_ids = unit.get("lesson_ids")
        if not isinstance(lesson_ids, list) or not lesson_ids:
            _fail("INVALID_UNIT_PLAN", f"unit {unit_id!r} has no lessons")
        if any(item not in lesson_by_id for item in lesson_ids):
            _fail("INVALID_UNIT_PLAN", f"unit {unit_id!r} references an unknown lesson")
        selected = [lesson_by_id[item] for item in lesson_ids]
        expected_capsule = _capsule(course, lessons, selected, style_context)
        capsule = unit.get("context_capsule")
        if (
            unit.get("course_manifest_sha256") != canonical_digest(course)
            or unit.get("style_context_sha256") != canonical_digest(style_context)
            or not isinstance(capsule, dict)
            or unit.get("context_capsule_sha256") != canonical_digest(capsule)
            or canonical_json_bytes(capsule) != canonical_json_bytes(expected_capsule)
        ):
            _fail("STALE_UNIT_PLAN", f"unit {unit_id!r} is not derived from exact inputs")
        if (
            unit.get("start_seconds") != selected[0]["start_seconds"]
            or unit.get("end_seconds") != selected[-1]["end_seconds"]
        ):
            _fail("UNIT_BOUNDARY_MISMATCH", f"unit {unit_id!r} has changed bounds")
        actual_lesson_ids.extend(lesson_ids)
        by_id[unit_id] = unit
    if actual_lesson_ids != expected_lesson_ids:
        _fail("LESSON_COVERAGE", "units must cover every lesson exactly once and in order")
    return by_id


def merge_script_units(
    course_manifest: Mapping[str, Any],
    units: Sequence[Mapping[str, Any]],
    unit_results: Iterable[Mapping[str, Any]],
    *,
    style_context: Mapping[str, Any],
) -> dict[str, Any]:
    """Merge script fragments by plan ordinal with exact lesson coverage."""

    course = _validate_course(course_manifest)
    context = _validate_context(style_context)
    unit_by_id = _validate_unit_plan(course, units, context)
    lesson_by_id = {item["id"]: item for item in _course_lessons(course)}
    result_by_id: dict[str, dict[str, Any]] = {}
    for raw in unit_results:
        result = deepcopy(dict(raw))
        unit_id = result.get("unit_id")
        if unit_id not in unit_by_id:
            _fail("UNKNOWN_UNIT_RESULT", f"unknown result unit {unit_id!r}")
        if unit_id in result_by_id:
            _fail("DUPLICATE_UNIT_RESULT", f"duplicate result for {unit_id!r}")
        if result.get("context_capsule_sha256") != unit_by_id[unit_id]["context_capsule_sha256"]:
            _fail("STALE_UNIT_RESULT", f"result for {unit_id!r} binds the wrong capsule")
        result_by_id[unit_id] = result
    if set(result_by_id) != set(unit_by_id):
        _fail("MISSING_UNIT_RESULT", f"missing results for {sorted(set(unit_by_id) - set(result_by_id))}")

    sections: list[dict[str, Any]] = []
    mappings: list[dict[str, str]] = []
    seen_sections: set[str] = set()
    covered_lessons: set[str] = set()
    voice_performance: dict[str, Any] | None = None
    for raw_unit in units:
        unit = unit_by_id[raw_unit["unit_id"]]
        result = result_by_id[unit["unit_id"]]
        fragment = result.get("script")
        mapping = result.get("section_lesson_ids")
        if not isinstance(fragment, dict) or not isinstance(mapping, list):
            _fail("INVALID_SCRIPT_FRAGMENT", f"unit {unit['unit_id']!r} lacks script or mapping")
        fragment_sections = fragment.get("sections")
        if not isinstance(fragment_sections, list) or not fragment_sections:
            _fail("INVALID_SCRIPT_FRAGMENT", f"unit {unit['unit_id']!r} has no sections")
        if fragment.get("version") != "1.0" or fragment.get("title") != course["title"]:
            _fail("SCRIPT_IDENTITY_DRIFT", f"unit {unit['unit_id']!r} changed script identity")
        current_voice = fragment.get("voice_performance")
        if current_voice is not None:
            if voice_performance is None:
                voice_performance = deepcopy(current_voice)
            elif canonical_json_bytes(current_voice) != canonical_json_bytes(voice_performance):
                _fail("VOICE_PERFORMANCE_DRIFT", "script units disagree on voice_performance")
        mapping_by_section: dict[str, str] = {}
        for item in mapping:
            if not isinstance(item, dict) or set(item) != {"section_id", "lesson_id"}:
                _fail("INVALID_SECTION_MAPPING", "section mappings need section_id and lesson_id")
            section_id = item["section_id"]
            if section_id in mapping_by_section:
                _fail("INVALID_SECTION_MAPPING", f"duplicate mapping for {section_id!r}")
            mapping_by_section[section_id] = item["lesson_id"]
        if set(mapping_by_section) != {item.get("id") for item in fragment_sections}:
            _fail("SECTION_MAPPING_COVERAGE", f"unit {unit['unit_id']!r} mapping is not exact")

        ordered = sorted(
            deepcopy(fragment_sections),
            key=lambda item: (_number(item.get("start_seconds"), "section start"), str(item.get("id"))),
        )
        previous_end: float | None = None
        for section in ordered:
            section_id = section.get("id")
            if not isinstance(section_id, str) or not section_id or section_id in seen_sections:
                _fail("DUPLICATE_SECTION_ID", f"invalid or duplicate section {section_id!r}")
            lesson_id = mapping_by_section[section_id]
            if lesson_id not in unit["lesson_ids"]:
                _fail("UNIT_OWNERSHIP_VIOLATION", f"unit cannot write lesson {lesson_id!r}")
            lesson = lesson_by_id[lesson_id]
            start = _number(section.get("start_seconds"), "section start")
            end = _number(section.get("end_seconds"), "section end")
            if end <= start:
                _fail("INVALID_SECTION_TIME", f"section {section_id!r} must end after start")
            if start < float(lesson["start_seconds"]) - _TOLERANCE or end > float(lesson["end_seconds"]) + _TOLERANCE:
                _fail("UNIT_OWNERSHIP_VIOLATION", f"section {section_id!r} exceeds lesson {lesson_id!r}")
            if previous_end is not None and start < previous_end - _TOLERANCE:
                _fail("SECTION_OVERLAP", f"unit {unit['unit_id']!r} contains overlapping sections")
            previous_end = end
            seen_sections.add(section_id)
            covered_lessons.add(lesson_id)
            sections.append(section)
            mappings.append({"section_id": section_id, "lesson_id": lesson_id})

    if covered_lessons != set(lesson_by_id):
        _fail("LESSON_COVERAGE", f"lessons without narration sections: {sorted(set(lesson_by_id) - covered_lessons)}")
    sections.sort(key=lambda item: (_number(item["start_seconds"], "section start"), str(item["id"])))
    mappings.sort(key=lambda item: next(index for index, section in enumerate(sections) if section["id"] == item["section_id"]))
    for prior, current in zip(sections, sections[1:]):
        if float(current["start_seconds"]) < float(prior["end_seconds"]) - _TOLERANCE:
            _fail("SECTION_OVERLAP", "merged script sections overlap")

    script: dict[str, Any] = {
        "version": "1.0",
        "title": course["title"],
        "total_duration_seconds": course["target_duration_seconds"],
        "sections": sections,
    }
    if voice_performance is not None:
        script["voice_performance"] = voice_performance
    try:
        validate_artifact("script", script)
    except Exception as exc:
        _fail("INVALID_MERGED_SCRIPT", str(exc))
    return {
        "script": script,
        "section_lesson_ids": mappings,
        "course_manifest_sha256": canonical_digest(course),
        "style_context_sha256": canonical_digest(context),
        "script_sha256": canonical_digest(script),
    }


def run_script_units(
    *,
    mode: str | None = "off",
    course_manifest: Mapping[str, Any] | None = None,
    style_context: Mapping[str, Any] | None = None,
    unit_results: Iterable[Mapping[str, Any]] | None = None,
    target_duration_seconds: float = DEFAULT_TARGET_DURATION_SECONDS,
    hard_max_duration_seconds: float = DEFAULT_HARD_MAX_DURATION_SECONDS,
) -> dict[str, Any] | None:
    """Return immediately when off; otherwise prepare or merge an opt-in candidate."""

    if mode in (None, "off"):
        return None
    if mode not in {"compare_only", "publish_candidate"}:
        _fail("UNSUPPORTED_MODE", f"unsupported script production-unit mode {mode!r}")
    if course_manifest is None or style_context is None:
        _fail("MISSING_INPUT", "script units require course_manifest and style_context")
    units = build_script_units(
        course_manifest,
        style_context=style_context,
        target_duration_seconds=target_duration_seconds,
        hard_max_duration_seconds=hard_max_duration_seconds,
    )
    report: dict[str, Any] = {
        "mode": mode,
        "publish_allowed": mode == "publish_candidate",
        "units": units,
    }
    if unit_results is not None:
        report["candidate"] = merge_script_units(
            course_manifest,
            units,
            unit_results,
            style_context=style_context,
        )
    return report
