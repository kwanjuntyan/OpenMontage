"""Lean M2a helpers for segmented scene-plan experiments.

This module is deliberately pure: it reads no project files, creates no
sidecars, writes no checkpoints, and never publishes a canonical artifact.
Canonical callers provide a non-off approved policy plus
``execution_disposition="compare_only"``. The M2-M5 ``mode`` keyword remains
only as a compatibility alias; ``mode="off"`` returns before validating or
touching any production-unit input.
"""

from __future__ import annotations

from copy import deepcopy
import math
from typing import Any, Iterable, Mapping, Sequence

import jsonschema

from lib.clp_validator import (
    canonical_digest,
    canonical_json_bytes,
    validate_clp_shot_bindings_or_raise,
)
from schemas.artifacts import load_schema, validate_artifact

from .contracts import execution_report_fields, resolve_execution_contract


DEFAULT_TARGET_DURATION_SECONDS = 180.0
DEFAULT_HARD_MAX_DURATION_SECONDS = 480.0
DEFAULT_MAX_CAPSULE_BYTES = 4 * 1024 * 1024
_TIME_TOLERANCE = 1e-6


class ProductionUnitError(ValueError):
    """A stable, typed failure raised before any candidate can be published."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _fail(code: str, message: str) -> None:
    raise ProductionUnitError(code, message)


def _number(value: Any, *, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail("INVALID_TIME", f"{field} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        _fail("INVALID_TIME", f"{field} must be a finite number")
    return result


def _validated_sections(script: Mapping[str, Any]) -> list[dict[str, Any]]:
    try:
        validate_artifact("script", dict(script))
    except Exception as exc:
        _fail("INVALID_SCRIPT", str(exc))

    sections = deepcopy(script["sections"])
    seen: set[str] = set()
    total = _number(script.get("total_duration_seconds"), field="total_duration_seconds")
    previous_end: float | None = None
    for index, section in enumerate(sections):
        section_id = section.get("id")
        if not isinstance(section_id, str) or not section_id:
            _fail("INVALID_SECTION_ID", f"sections[{index}] has no usable id")
        if section_id in seen:
            _fail("DUPLICATE_SECTION_ID", f"section {section_id!r} occurs more than once")
        seen.add(section_id)
        start = _number(section.get("start_seconds"), field=f"sections[{index}].start_seconds")
        end = _number(section.get("end_seconds"), field=f"sections[{index}].end_seconds")
        if end <= start:
            _fail("INVALID_SECTION_TIME", f"section {section_id!r} must end after it starts")
        if end > total:
            _fail(
                "SECTION_TIMELINE_COVERAGE",
                f"section {section_id!r} ends after total_duration_seconds",
            )
        if previous_end is not None and start < previous_end:
            _fail(
                "SECTION_TIMELINE_COVERAGE",
                f"script sections overlap at {start}",
            )
        previous_end = end
    return sections


def _timeline_spans(
    script: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Derive complete visual time from narration sections and legal silent gaps."""

    validated = list(sections) if sections is not None else _validated_sections(script)
    total = _number(script.get("total_duration_seconds"), field="total_duration_seconds")
    spans: list[dict[str, Any]] = []
    cursor = 0.0
    visual_ordinal = 0
    for section in validated:
        start = float(section["start_seconds"])
        end = float(section["end_seconds"])
        if start > cursor:
            visual_ordinal += 1
            spans.append(
                {
                    "id": f"visual-only-{visual_ordinal:04d}",
                    "kind": "visual_only",
                    "start_seconds": cursor,
                    "end_seconds": section["start_seconds"],
                }
            )
        spans.append(
            {
                "id": f"narration:{section['id']}",
                "kind": "narration",
                "start_seconds": section["start_seconds"],
                "end_seconds": section["end_seconds"],
                "script_section_id": section["id"],
            }
        )
        cursor = end
    if cursor < total:
        visual_ordinal += 1
        spans.append(
            {
                "id": f"visual-only-{visual_ordinal:04d}",
                "kind": "visual_only",
                "start_seconds": cursor,
                "end_seconds": script["total_duration_seconds"],
            }
        )
    return spans


def _boundary_span(span: Mapping[str, Any]) -> dict[str, Any]:
    result = {
        "id": span["id"],
        "kind": span["kind"],
        "start_seconds": span["start_seconds"],
        "end_seconds": span["end_seconds"],
    }
    if "script_section_id" in span:
        result["script_section_id"] = span["script_section_id"]
    return result


def _context_capsule(
    *,
    script: Mapping[str, Any],
    clp_manifest: Mapping[str, Any],
    style_context: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    spans: Sequence[Mapping[str, Any]],
    group: Sequence[Mapping[str, Any]],
    script_digest: str,
    clp_digest: str,
    style_context_digest: str,
) -> dict[str, Any]:
    section_by_id = {section["id"]: section for section in sections}
    selected_sections = [
        section_by_id[span["script_section_id"]]
        for span in group
        if span["kind"] == "narration"
    ]
    first_index = next(index for index, span in enumerate(spans) if span["id"] == group[0]["id"])
    last_index = next(index for index, span in enumerate(spans) if span["id"] == group[-1]["id"])
    return {
        "version": "0.2",
        "course": {
            "title": script.get("title"),
            "total_duration_seconds": script["total_duration_seconds"],
        },
        "timeline_spans": deepcopy(list(group)),
        "script_sections": deepcopy(selected_sections),
        "boundary_context": {
            "previous_timeline_span": (
                _boundary_span(spans[first_index - 1]) if first_index > 0 else None
            ),
            "next_timeline_span": (
                _boundary_span(spans[last_index + 1])
                if last_index + 1 < len(spans)
                else None
            ),
        },
        "clp_manifest": deepcopy(dict(clp_manifest)),
        "style_context": deepcopy(dict(style_context)),
        "source_script_sha256": script_digest,
        "clp_manifest_sha256": clp_digest,
        "style_context_sha256": style_context_digest,
    }


def _validate_clp(clp_manifest: Mapping[str, Any]) -> None:
    """Validate the approved CLP envelope without resolving or reading assets."""

    try:
        jsonschema.validate(instance=dict(clp_manifest), schema=load_schema("clp_manifest"))
    except Exception as exc:
        _fail("INVALID_CLP", str(exc))
    seen_ids: set[str] = set()
    for category in ("characters", "locations", "props"):
        for entity in clp_manifest.get(category, []):
            entity_id = entity["id"]
            if entity_id in seen_ids:
                _fail("INVALID_CLP", f"duplicate CLP entity id {entity_id!r}")
            seen_ids.add(entity_id)
            policy = entity["policy"]
            if policy == "strict_reference" and (
                not entity.get("image") or not entity.get("asset_sha256")
            ):
                _fail("INVALID_CLP", f"strict entity {entity_id!r} lacks an image digest")
            if policy == "text_anchor_only" and not entity.get("prompt_anchor"):
                _fail("INVALID_CLP", f"text-anchor entity {entity_id!r} lacks prompt_anchor")


def _validated_style_context(style_context: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(style_context, Mapping):
        _fail("INVALID_STYLE_CONTEXT", "style_context must be an object")
    style = style_context.get("style_playbook")
    if not isinstance(style, str) or not style:
        _fail("INVALID_STYLE_CONTEXT", "style_context requires a non-empty style_playbook")
    result = deepcopy(dict(style_context))
    try:
        canonical_json_bytes(result)
    except (TypeError, ValueError) as exc:
        _fail("INVALID_STYLE_CONTEXT", str(exc))
    return result


def build_scene_plan_units(
    script: Mapping[str, Any],
    clp_manifest: Mapping[str, Any],
    *,
    style_context: Mapping[str, Any],
    target_duration_seconds: float = DEFAULT_TARGET_DURATION_SECONDS,
    hard_max_duration_seconds: float = DEFAULT_HARD_MAX_DURATION_SECONDS,
    max_capsule_bytes: int = DEFAULT_MAX_CAPSULE_BYTES,
) -> list[dict[str, Any]]:
    """Partition complete visual time only at derived timeline boundaries.

    Narration sections stay authoritative. Gaps before, between, or after
    them become explicit visual-only spans so unit ownership remains total.
    """

    target = _number(target_duration_seconds, field="target_duration_seconds")
    hard_max = _number(hard_max_duration_seconds, field="hard_max_duration_seconds")
    if target <= 0 or hard_max <= 0 or hard_max < target:
        _fail("INVALID_UNIT_POLICY", "durations must be positive and hard_max >= target")
    if isinstance(max_capsule_bytes, bool) or not isinstance(max_capsule_bytes, int) or max_capsule_bytes <= 0:
        _fail("INVALID_UNIT_POLICY", "max_capsule_bytes must be a positive integer")

    sections = _validated_sections(script)
    spans = _timeline_spans(script, sections)
    _validate_clp(clp_manifest)
    approved_style_context = _validated_style_context(style_context)
    script_digest = canonical_digest(dict(script))
    clp_digest = canonical_digest(dict(clp_manifest))
    style_context_digest = canonical_digest(approved_style_context)

    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for span in spans:
        start = float(span["start_seconds"])
        end = float(span["end_seconds"])
        if end - start > hard_max + _TIME_TOLERANCE:
            _fail(
                "TIMELINE_SPAN_EXCEEDS_HARD_MAX",
                f"span {span['id']!r} cannot be split safely at a declared boundary",
            )
        if current and end - float(current[0]["start_seconds"]) > target + _TIME_TOLERANCE:
            groups.append(current)
            current = []
        current.append(span)
        if end - float(current[0]["start_seconds"]) > hard_max + _TIME_TOLERANCE:
            _fail("UNIT_EXCEEDS_HARD_MAX", f"unit ending at span {span['id']!r} is too long")
    if current:
        groups.append(current)

    units: list[dict[str, Any]] = []
    for ordinal, group in enumerate(groups):
        capsule = _context_capsule(
            script=script,
            clp_manifest=clp_manifest,
            style_context=approved_style_context,
            sections=sections,
            spans=spans,
            group=group,
            script_digest=script_digest,
            clp_digest=clp_digest,
            style_context_digest=style_context_digest,
        )
        capsule_size = len(canonical_json_bytes(capsule))
        if capsule_size > max_capsule_bytes:
            _fail(
                "CAPSULE_TOO_LARGE",
                f"unit {ordinal + 1} capsule is {capsule_size} bytes (limit {max_capsule_bytes})",
            )
        units.append(
            {
                "unit_id": f"scene-unit-{ordinal + 1:04d}",
                "ordinal": ordinal,
                "start_seconds": group[0]["start_seconds"],
                "end_seconds": group[-1]["end_seconds"],
                "timeline_span_ids": [span["id"] for span in group],
                "section_ids": [
                    span["script_section_id"]
                    for span in group
                    if span["kind"] == "narration"
                ],
                "source_script_sha256": script_digest,
                "clp_manifest_sha256": clp_digest,
                "style_context_sha256": style_context_digest,
                "context_capsule": capsule,
                "context_capsule_sha256": canonical_digest(capsule),
            }
        )
    return units


def _validate_unit_plan(
    script: Mapping[str, Any],
    clp_manifest: Mapping[str, Any],
    style_context: Mapping[str, Any],
    units: Sequence[Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    script_sections = _validated_sections(script)
    timeline_spans = _timeline_spans(script, script_sections)
    expected_sections = [section["id"] for section in script_sections]
    expected_span_ids = [span["id"] for span in timeline_spans]
    span_by_id = {span["id"]: span for span in timeline_spans}
    script_digest = canonical_digest(dict(script))
    clp_digest = canonical_digest(dict(clp_manifest))
    approved_style_context = _validated_style_context(style_context)
    style_context_digest = canonical_digest(approved_style_context)
    by_id: dict[str, dict[str, Any]] = {}
    actual_sections: list[str] = []
    actual_span_ids: list[str] = []
    for expected_ordinal, raw_unit in enumerate(units):
        unit = dict(raw_unit)
        unit_id = unit.get("unit_id")
        if not isinstance(unit_id, str) or not unit_id:
            _fail("INVALID_UNIT_ID", f"unit ordinal {expected_ordinal} has no id")
        if unit_id in by_id:
            _fail("DUPLICATE_UNIT_ID", f"unit {unit_id!r} occurs more than once")
        if unit.get("ordinal") != expected_ordinal:
            _fail("UNIT_ORDER", "unit ordinals must be contiguous and authoritative")
        if (
            unit.get("source_script_sha256") != script_digest
            or unit.get("clp_manifest_sha256") != clp_digest
            or unit.get("style_context_sha256") != style_context_digest
        ):
            _fail("STALE_UNIT_PLAN", f"unit {unit_id!r} does not bind the current script and CLP")
        capsule = unit.get("context_capsule")
        if not isinstance(capsule, dict) or unit.get("context_capsule_sha256") != canonical_digest(capsule):
            _fail("CAPSULE_DIGEST_MISMATCH", f"unit {unit_id!r} capsule was changed")
        span_ids = unit.get("timeline_span_ids")
        if not isinstance(span_ids, list) or not span_ids:
            _fail("INVALID_UNIT_SPANS", f"unit {unit_id!r} has no timeline spans")
        if any(span_id not in span_by_id for span_id in span_ids):
            _fail("INVALID_UNIT_SPANS", f"unit {unit_id!r} references an unknown timeline span")
        selected_spans = [span_by_id[span_id] for span_id in span_ids]
        section_ids = unit.get("section_ids")
        expected_unit_sections = [
            span["script_section_id"]
            for span in selected_spans
            if span["kind"] == "narration"
        ]
        if not isinstance(section_ids, list) or section_ids != expected_unit_sections:
            _fail(
                "INVALID_UNIT_SECTIONS",
                f"unit {unit_id!r} section ids do not match its narration spans",
            )
        expected_capsule = _context_capsule(
            script=script,
            clp_manifest=clp_manifest,
            style_context=approved_style_context,
            sections=script_sections,
            spans=timeline_spans,
            group=selected_spans,
            script_digest=script_digest,
            clp_digest=clp_digest,
            style_context_digest=style_context_digest,
        )
        if canonical_json_bytes(capsule) != canonical_json_bytes(expected_capsule):
            _fail("CAPSULE_CONTENT_MISMATCH", f"unit {unit_id!r} capsule is not derived from its sources")
        if (
            unit.get("start_seconds") != selected_spans[0]["start_seconds"]
            or unit.get("end_seconds") != selected_spans[-1]["end_seconds"]
        ):
            _fail("UNIT_BOUNDARY_MISMATCH", f"unit {unit_id!r} timing does not match its spans")
        actual_sections.extend(section_ids)
        actual_span_ids.extend(span_ids)
        by_id[unit_id] = unit
    if actual_span_ids != expected_span_ids:
        _fail("TIMELINE_COVERAGE", "units must cover every timeline span exactly once and in order")
    if actual_sections != expected_sections:
        _fail("SECTION_COVERAGE", "units must cover every script section exactly once and in order")
    return by_id


def _containing_span(
    spans: Sequence[Mapping[str, Any]],
    *,
    scene_id: Any,
    start: float,
    end: float,
) -> Mapping[str, Any]:
    matches = [
        span
        for span in spans
        if start >= float(span["start_seconds"]) - _TIME_TOLERANCE
        and end <= float(span["end_seconds"]) + _TIME_TOLERANCE
    ]
    if len(matches) != 1:
        _fail(
            "SCENE_TIMELINE_OWNERSHIP",
            f"scene {scene_id!r} must fit wholly inside one narration or visual-only span",
        )
    return matches[0]


def _validate_timeline_scene_coverage(
    script: Mapping[str, Any],
    scenes: Sequence[Mapping[str, Any]],
) -> None:
    sections = _validated_sections(script)
    spans = _timeline_spans(script, sections)
    known_section_ids = {str(section["id"]) for section in sections}
    scenes_by_span: dict[str, list[Mapping[str, Any]]] = {
        str(span["id"]): [] for span in spans
    }
    order_keys: list[tuple[float, float, str]] = []
    for scene in scenes:
        scene_id = scene.get("id")
        start = _number(scene.get("start_seconds"), field=f"scene {scene_id}.start_seconds")
        end = _number(scene.get("end_seconds"), field=f"scene {scene_id}.end_seconds")
        if end <= start:
            _fail("INVALID_SCENE_TIME", f"scene {scene_id!r} must end after it starts")
        order_keys.append((start, end, str(scene_id)))
        span = _containing_span(spans, scene_id=scene_id, start=start, end=end)
        section_id = scene.get("script_section_id")
        if section_id is not None and (not isinstance(section_id, str) or not section_id):
            _fail("INVALID_SECTION_REF", f"scene {scene_id!r} has an invalid script_section_id")
        if isinstance(section_id, str) and section_id not in known_section_ids:
            _fail("UNKNOWN_SECTION_REF", f"scene {scene_id!r} references {section_id!r}")
        if span["kind"] == "narration":
            expected_section_id = span["script_section_id"]
            if section_id is None:
                _fail("MISSING_SECTION_REF", f"scene {scene_id!r} has no script_section_id")
            if section_id != expected_section_id:
                _fail(
                    "SECTION_REF_MISMATCH",
                    f"scene {scene_id!r} occurs in {expected_section_id!r}, not {section_id!r}",
                )
        elif section_id is not None:
            _fail(
                "VISUAL_ONLY_SECTION_REF",
                f"scene {scene_id!r} is in a visual-only span and must omit script_section_id",
            )
        scenes_by_span[str(span["id"])].append(scene)

    if order_keys != sorted(order_keys):
        _fail("SCENE_ORDER", "scenes must be in canonical chronological order")

    for span in spans:
        span_id = str(span["id"])
        ordered = scenes_by_span[span_id]
        if not ordered:
            _fail("MISSING_TIMELINE_COVERAGE", f"timeline span {span_id!r} has no scene")
        cursor = float(span["start_seconds"])
        expected_end = float(span["end_seconds"])
        for scene in ordered:
            start = _number(scene.get("start_seconds"), field=f"scene {scene.get('id')}.start_seconds")
            end = _number(scene.get("end_seconds"), field=f"scene {scene.get('id')}.end_seconds")
            if abs(start - cursor) > _TIME_TOLERANCE:
                relation = "gap" if start > cursor else "overlap"
                _fail("SCENE_TIMELINE_COVERAGE", f"{relation} in span {span_id!r} at {cursor}")
            cursor = end
        if abs(cursor - expected_end) > _TIME_TOLERANCE:
            _fail("SCENE_TIMELINE_COVERAGE", f"span {span_id!r} does not end at {expected_end}")


def merge_scene_plan_units(
    script: Mapping[str, Any],
    clp_manifest: Mapping[str, Any],
    units: Sequence[Mapping[str, Any]],
    unit_results: Iterable[Mapping[str, Any]],
    *,
    style_context: Mapping[str, Any],
) -> dict[str, Any]:
    """Merge unit candidates by plan ordinal, never worker arrival order."""

    _validate_clp(clp_manifest)
    approved_style_context = _validated_style_context(style_context)
    approved_style = approved_style_context["style_playbook"]
    script_sections = _validated_sections(script)
    timeline_spans = _timeline_spans(script, script_sections)
    known_section_ids = {section["id"] for section in script_sections}
    unit_by_id = _validate_unit_plan(script, clp_manifest, approved_style_context, units)
    result_by_id: dict[str, dict[str, Any]] = {}
    for raw_result in unit_results:
        result = deepcopy(dict(raw_result))
        unit_id = result.get("unit_id")
        if unit_id in result_by_id:
            _fail("DUPLICATE_UNIT_RESULT", f"multiple results supplied for {unit_id!r}")
        if unit_id not in unit_by_id:
            _fail("UNKNOWN_UNIT_RESULT", f"result references unknown unit {unit_id!r}")
        expected_capsule_digest = unit_by_id[str(unit_id)]["context_capsule_sha256"]
        if result.get("context_capsule_sha256") != expected_capsule_digest:
            _fail("STALE_UNIT_RESULT", f"result for {unit_id!r} does not bind its exact context capsule")
        result_by_id[str(unit_id)] = result
    if set(result_by_id) != set(unit_by_id):
        missing = sorted(set(unit_by_id) - set(result_by_id))
        _fail("MISSING_UNIT_RESULT", f"missing results for {missing}")

    merged_scenes: list[dict[str, Any]] = []
    binding_by_scene: dict[str, dict[str, Any]] = {}
    style_playbooks: set[str] = set()
    seen_scene_ids: set[str] = set()
    for unit in units:
        unit_id = str(unit["unit_id"])
        result = result_by_id[unit_id]
        candidate = result.get("scene_plan")
        if not isinstance(candidate, dict) or candidate.get("version") != "1.0":
            _fail("INVALID_UNIT_SCENE_PLAN", f"unit {unit_id!r} has no version 1.0 scene_plan")
        style = candidate.get("style_playbook")
        if style != approved_style:
            _fail(
                "STYLE_PLAYBOOK_DRIFT",
                f"unit {unit_id!r} must use approved style_playbook {approved_style!r}",
            )
        style_playbooks.add(style)
        scenes = candidate.get("scenes")
        if not isinstance(scenes, list) or not scenes:
            _fail("INVALID_UNIT_SCENE_PLAN", f"unit {unit_id!r} contains no scenes")
        owned_sections = set(unit["section_ids"])
        owned_span_ids = set(unit["timeline_span_ids"])
        ordered_scenes = sorted(
            deepcopy(scenes),
            key=lambda scene: (
                _number(scene.get("start_seconds"), field=f"scene {scene.get('id')}.start_seconds"),
                _number(scene.get("end_seconds"), field=f"scene {scene.get('id')}.end_seconds"),
                str(scene.get("id")),
            ),
        )
        unit_scene_ids: set[str] = set()
        for scene in ordered_scenes:
            scene_id = scene.get("id")
            if not isinstance(scene_id, str) or not scene_id:
                _fail("INVALID_SCENE_ID", f"unit {unit_id!r} produced a scene without an id")
            if scene_id in seen_scene_ids:
                _fail("DUPLICATE_SCENE_REF", f"scene {scene_id!r} occurs more than once")
            start = _number(scene.get("start_seconds"), field=f"scene {scene_id}.start_seconds")
            end = _number(scene.get("end_seconds"), field=f"scene {scene_id}.end_seconds")
            if end <= start:
                _fail("INVALID_SCENE_TIME", f"scene {scene_id!r} must end after it starts")
            span = _containing_span(timeline_spans, scene_id=scene_id, start=start, end=end)
            if span["id"] not in owned_span_ids:
                _fail(
                    "UNIT_OWNERSHIP_VIOLATION",
                    f"unit {unit_id!r} cannot produce timeline span {span['id']!r}",
                )
            section_id = scene.get("script_section_id")
            if section_id is not None and (not isinstance(section_id, str) or not section_id):
                _fail("INVALID_SECTION_REF", f"scene {scene_id!r} has an invalid script_section_id")
            if isinstance(section_id, str) and section_id not in known_section_ids:
                _fail("UNKNOWN_SECTION_REF", f"scene {scene_id!r} references {section_id!r}")
            if span["kind"] == "narration":
                if section_id is None:
                    _fail("MISSING_SECTION_REF", f"scene {scene_id!r} has no script_section_id")
                if section_id not in owned_sections:
                    _fail(
                        "UNIT_OWNERSHIP_VIOLATION",
                        f"unit {unit_id!r} cannot produce section {section_id!r}",
                    )
                if section_id != span["script_section_id"]:
                    _fail(
                        "SECTION_REF_MISMATCH",
                        f"scene {scene_id!r} is not inside section {section_id!r}",
                    )
            elif section_id is not None:
                _fail(
                    "VISUAL_ONLY_SECTION_REF",
                    f"scene {scene_id!r} is visual-only and must omit script_section_id",
                )
            seen_scene_ids.add(scene_id)
            unit_scene_ids.add(scene_id)
            merged_scenes.append(scene)

        bindings = result.get("bindings")
        if not isinstance(bindings, list):
            _fail("INVALID_UNIT_BINDINGS", f"unit {unit_id!r} must provide bindings")
        for raw_binding in bindings:
            if not isinstance(raw_binding, dict):
                _fail("INVALID_UNIT_BINDINGS", f"unit {unit_id!r} has a non-object binding")
            binding = deepcopy(raw_binding)
            shot_id = binding.get("shot_id")
            if shot_id not in unit_scene_ids:
                _fail(
                    "UNIT_OWNERSHIP_VIOLATION",
                    f"unit {unit_id!r} cannot bind scene {shot_id!r}",
                )
            if shot_id in binding_by_scene:
                _fail("DUPLICATE_SCENE_BINDING", f"scene {shot_id!r} has multiple bindings")
            binding_by_scene[str(shot_id)] = binding

    if len(style_playbooks) > 1:
        _fail("STYLE_PLAYBOOK_DRIFT", "unit scene plans disagree on style_playbook")
    _validate_timeline_scene_coverage(script, merged_scenes)

    scene_plan: dict[str, Any] = {"version": "1.0", "scenes": merged_scenes}
    if style_playbooks:
        scene_plan["style_playbook"] = next(iter(style_playbooks))
    try:
        validate_artifact("scene_plan", scene_plan)
    except Exception as exc:
        _fail("INVALID_MERGED_SCENE_PLAN", str(exc))

    ordered_bindings = [binding_by_scene[scene["id"]] for scene in merged_scenes if scene["id"] in binding_by_scene]
    bindings_doc = {
        "version": "2.0",
        "project_id": clp_manifest["project_id"],
        "source_scene_plan_sha256": canonical_digest(scene_plan),
        "clp_manifest_sha256": canonical_digest(dict(clp_manifest)),
        "bindings": ordered_bindings,
    }
    try:
        validate_artifact("clp_shot_bindings", bindings_doc)
        validate_clp_shot_bindings_or_raise(bindings_doc, dict(clp_manifest), scene_plan)
    except Exception as exc:
        _fail("INVALID_CLP_BINDINGS", str(exc))

    return {
        "scene_plan": scene_plan,
        "clp_shot_bindings": bindings_doc,
        "source_script_sha256": canonical_digest(dict(script)),
        "clp_manifest_sha256": canonical_digest(dict(clp_manifest)),
        "style_context_sha256": canonical_digest(approved_style_context),
        "scene_plan_sha256": canonical_digest(scene_plan),
        "clp_shot_bindings_sha256": canonical_digest(bindings_doc),
    }


def _validate_complete_bundle(
    *,
    label: str,
    bundle: Mapping[str, Any],
    script: Mapping[str, Any],
    clp_manifest: Mapping[str, Any],
    approved_style: str,
    source_script_sha256: str,
    clp_manifest_sha256: str,
    style_context_sha256: str,
) -> dict[str, Any]:
    scene_plan = bundle.get("scene_plan")
    bindings = bundle.get("clp_shot_bindings")
    if not isinstance(scene_plan, dict) or not isinstance(bindings, dict):
        _fail("INVALID_BASELINE", f"{label} requires scene_plan and clp_shot_bindings")
    if (
        bundle.get("source_script_sha256") != source_script_sha256
        or bundle.get("clp_manifest_sha256") != clp_manifest_sha256
        or bundle.get("style_context_sha256") != style_context_sha256
    ):
        _fail("STALE_BASELINE", f"{label} does not bind the exact script, CLP, and style context")
    if scene_plan.get("style_playbook") != approved_style:
        _fail("STYLE_PLAYBOOK_DRIFT", f"{label} does not use the approved style_playbook")
    try:
        validate_artifact("scene_plan", scene_plan)
        _validate_timeline_scene_coverage(script, scene_plan["scenes"])
        validate_artifact("clp_shot_bindings", bindings)
        validate_clp_shot_bindings_or_raise(bindings, dict(clp_manifest), scene_plan)
    except ProductionUnitError:
        raise
    except Exception as exc:
        _fail("INVALID_BASELINE", f"{label}: {exc}")
    return {
        "scene_plan": deepcopy(scene_plan),
        "clp_shot_bindings": deepcopy(bindings),
        "scene_plan_sha256": canonical_digest(scene_plan),
        "clp_shot_bindings_sha256": canonical_digest(bindings),
    }


def run_scene_plan_compare(
    *,
    production_unit_policy: Mapping[str, Any] | None = None,
    execution_disposition: str | None = None,
    mode: str | None = None,
    script: Mapping[str, Any] | None = None,
    clp_manifest: Mapping[str, Any] | None = None,
    style_context: Mapping[str, Any] | None = None,
    monolithic_baseline: Mapping[str, Any] | None = None,
    unit_results: Iterable[Mapping[str, Any]] | None = None,
    target_duration_seconds: float = DEFAULT_TARGET_DURATION_SECONDS,
    hard_max_duration_seconds: float = DEFAULT_HARD_MAX_DURATION_SECONDS,
    max_capsule_bytes: int = DEFAULT_MAX_CAPSULE_BYTES,
) -> dict[str, Any] | None:
    """Run the in-memory M2a comparison path, or do exactly nothing when off."""

    contract = resolve_execution_contract(
        stage="scene_plan",
        production_unit_policy=production_unit_policy,
        execution_disposition=execution_disposition,
        legacy_mode=mode,
        allowed_dispositions={"compare_only"},
        helper_target_seconds=target_duration_seconds,
        helper_hard_max_seconds=hard_max_duration_seconds,
    )
    if contract is None:
        return None
    if script is None or clp_manifest is None or style_context is None:
        _fail("MISSING_INPUT", "compare_only requires approved script, canonical CLP, and style context")
    target_duration_seconds = contract["target_seconds"]
    hard_max_duration_seconds = contract["hard_max_seconds"]
    approved_style_context = _validated_style_context(style_context)
    units = build_scene_plan_units(
        script,
        clp_manifest,
        style_context=approved_style_context,
        target_duration_seconds=target_duration_seconds,
        hard_max_duration_seconds=hard_max_duration_seconds,
        max_capsule_bytes=max_capsule_bytes,
    )
    report: dict[str, Any] = {
        **execution_report_fields(contract),
        "publish_allowed": False,
        "units": units,
        "source_script_sha256": canonical_digest(dict(script)),
        "clp_manifest_sha256": canonical_digest(dict(clp_manifest)),
        "style_context_sha256": canonical_digest(approved_style_context),
    }
    if unit_results is not None:
        if monolithic_baseline is None:
            _fail("MISSING_BASELINE", "a completed compare requires a monolithic baseline")
        candidate = merge_scene_plan_units(
            script,
            clp_manifest,
            units,
            unit_results,
            style_context=approved_style_context,
        )
        baseline = _validate_complete_bundle(
            label="monolithic baseline",
            bundle=monolithic_baseline,
            script=script,
            clp_manifest=clp_manifest,
            approved_style=approved_style_context["style_playbook"],
            source_script_sha256=canonical_digest(dict(script)),
            clp_manifest_sha256=canonical_digest(dict(clp_manifest)),
            style_context_sha256=canonical_digest(approved_style_context),
        )
        baseline_scene_ids = [scene["id"] for scene in baseline["scene_plan"]["scenes"]]
        candidate_scene_ids = [scene["id"] for scene in candidate["scene_plan"]["scenes"]]
        report["baseline"] = baseline
        report["candidate"] = candidate
        report["comparison"] = {
            "both_cover_all_script_sections": True,
            "baseline_scene_count": len(baseline_scene_ids),
            "segmented_scene_count": len(candidate_scene_ids),
            "scene_count_delta": len(candidate_scene_ids) - len(baseline_scene_ids),
            "same_scene_ids_in_order": baseline_scene_ids == candidate_scene_ids,
            "baseline_scene_plan_sha256": baseline["scene_plan_sha256"],
            "segmented_scene_plan_sha256": candidate["scene_plan_sha256"],
        }
    return report
