"""Pure M4 merge contract for globally timed edit production units."""

from __future__ import annotations

from copy import deepcopy
import math
from typing import Any, Iterable, Mapping, Sequence

from lib.clp_validator import canonical_digest, canonical_json_bytes
from schemas.artifacts import validate_artifact

from .scene_plan_merge import ProductionUnitError
from .contracts import execution_report_fields, resolve_execution_contract


_TOLERANCE = 1e-6
_LOCKS = ("renderer_family", "render_runtime", "composition_mode")


def _fail(code: str, message: str) -> None:
    raise ProductionUnitError(code, message)


def _number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail("INVALID_TIME", f"{field} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        _fail("INVALID_TIME", f"{field} must be a finite number")
    return result


def _validated_inputs(
    scene_plan: Mapping[str, Any], asset_manifest: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    scene = deepcopy(dict(scene_plan))
    assets = deepcopy(dict(asset_manifest))
    try:
        validate_artifact("scene_plan", scene)
        validate_artifact("asset_manifest", assets)
    except Exception as exc:
        _fail("INVALID_EDIT_SOURCES", str(exc))
    scene_ids = [item["id"] for item in scene["scenes"]]
    asset_ids = [item["id"] for item in assets["assets"]]
    if len(scene_ids) != len(set(scene_ids)) or len(asset_ids) != len(set(asset_ids)):
        _fail("INVALID_EDIT_SOURCES", "scene and asset IDs must be unique")
    known_scenes = set(scene_ids)
    for asset in assets["assets"]:
        if asset["scene_id"] not in known_scenes:
            _fail("INVALID_EDIT_SOURCES", f"asset {asset['id']!r} has unknown scene")
    return scene, assets


def build_edit_units(
    scene_plan: Mapping[str, Any],
    asset_manifest: Mapping[str, Any],
    timeline_units: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Bind inherited timeline units to the exact canonical asset inventory."""

    scene, assets = _validated_inputs(scene_plan, asset_manifest)
    expected_scenes = [item["id"] for item in scene["scenes"]]
    scene_by_id = {item["id"]: item for item in scene["scenes"]}
    actual_scenes: list[str] = []
    units: list[dict[str, Any]] = []
    for ordinal, inherited in enumerate(timeline_units):
        scene_ids = inherited.get("scene_ids")
        if inherited.get("ordinal") != ordinal or not isinstance(scene_ids, list) or not scene_ids:
            _fail("INVALID_UNIT_PLAN", f"invalid inherited unit at ordinal {ordinal}")
        if any(scene_id not in scene_by_id for scene_id in scene_ids):
            _fail("INVALID_UNIT_PLAN", "inherited unit references an unknown scene")
        selected = [scene_by_id[scene_id] for scene_id in scene_ids]
        if (
            inherited.get("start_seconds") != selected[0]["start_seconds"]
            or inherited.get("end_seconds") != selected[-1]["end_seconds"]
        ):
            _fail("UNIT_BOUNDARY_MISMATCH", "inherited unit timing changed")
        unit_id = f"edit-unit-{ordinal + 1:04d}"
        unit_asset_ids = [
            item["id"] for item in assets["assets"] if item["scene_id"] in scene_ids
        ]
        capsule = {
            "version": "1.0",
            "source_timeline_unit_id": inherited["unit_id"],
            "scene_ids": deepcopy(scene_ids),
            "scenes": deepcopy(selected),
            "assets": [
                deepcopy(item) for item in assets["assets"] if item["id"] in unit_asset_ids
            ],
            "source_scene_plan_sha256": canonical_digest(scene),
            "asset_manifest_sha256": canonical_digest(assets),
        }
        units.append(
            {
                "unit_id": unit_id,
                "ordinal": ordinal,
                "source_timeline_unit_id": inherited["unit_id"],
                "scene_ids": deepcopy(scene_ids),
                "asset_ids": unit_asset_ids,
                "start_seconds": selected[0]["start_seconds"],
                "end_seconds": selected[-1]["end_seconds"],
                "source_scene_plan_sha256": canonical_digest(scene),
                "asset_manifest_sha256": canonical_digest(assets),
                "context_capsule": capsule,
                "context_capsule_sha256": canonical_digest(capsule),
            }
        )
        actual_scenes.extend(scene_ids)
    if actual_scenes != expected_scenes:
        _fail("SCENE_COVERAGE", "edit units must cover every scene exactly once")
    return units


def _validate_global_context(
    global_edit_context: Mapping[str, Any], production_locks: Mapping[str, Any]
) -> dict[str, Any]:
    context = deepcopy(dict(global_edit_context))
    forbidden = {"version", "cuts", "overlays", "transitions"}.intersection(context)
    if forbidden:
        _fail("INVALID_GLOBAL_EDIT_CONTEXT", f"unit-owned fields are global: {sorted(forbidden)}")
    if set(production_locks) != set(_LOCKS):
        _fail("INVALID_PRODUCTION_LOCKS", "all three production locks are required")
    for name in _LOCKS:
        if context.get(name) != production_locks[name]:
            _fail("RUNTIME_LOCK_DRIFT", f"global edit context changed {name}")
    try:
        canonical_json_bytes(context)
    except (TypeError, ValueError) as exc:
        _fail("INVALID_GLOBAL_EDIT_CONTEXT", str(exc))
    return context


def _asset_refs(edit: Mapping[str, Any]) -> set[str]:
    refs: set[str] = set()
    for cut in edit.get("cuts") or []:
        refs.add(cut["source"])
    for overlay in edit.get("overlays") or []:
        refs.add(overlay["asset_id"])
    audio = edit.get("audio") or {}
    for segment in (audio.get("narration") or {}).get("segments") or []:
        refs.add(segment["asset_id"])
    music = audio.get("music") or edit.get("music") or {}
    if music.get("asset_id"):
        refs.add(music["asset_id"])
    for item in audio.get("sfx") or []:
        if item.get("asset_id"):
            refs.add(item["asset_id"])
    subtitles = edit.get("subtitles") or {}
    if subtitles.get("source"):
        refs.add(subtitles["source"])
    return refs


def merge_edit_units(
    scene_plan: Mapping[str, Any],
    asset_manifest: Mapping[str, Any],
    units: Sequence[Mapping[str, Any]],
    unit_results: Iterable[Mapping[str, Any]],
    *,
    production_locks: Mapping[str, Any],
    global_edit_context: Mapping[str, Any],
) -> dict[str, Any]:
    """Merge worker fragments using separate global placement evidence."""

    scene, assets = _validated_inputs(scene_plan, asset_manifest)
    context = _validate_global_context(global_edit_context, production_locks)
    unit_by_id = {unit["unit_id"]: deepcopy(dict(unit)) for unit in units}
    if len(unit_by_id) != len(units):
        _fail("INVALID_UNIT_PLAN", "duplicate edit unit id")
    expected_scenes = [item["id"] for item in scene["scenes"]]
    actual_scenes = [scene_id for unit in units for scene_id in unit.get("scene_ids", [])]
    if actual_scenes != expected_scenes:
        _fail("SCENE_COVERAGE", "edit units no longer cover scene plan")
    for unit in units:
        if (
            unit.get("source_scene_plan_sha256") != canonical_digest(scene)
            or unit.get("asset_manifest_sha256") != canonical_digest(assets)
            or unit.get("context_capsule_sha256")
            != canonical_digest(unit.get("context_capsule"))
        ):
            _fail("STALE_UNIT_PLAN", f"edit unit {unit.get('unit_id')!r} is stale")

    result_by_id: dict[str, dict[str, Any]] = {}
    for raw in unit_results:
        result = deepcopy(dict(raw))
        unit_id = result.get("unit_id")
        if unit_id not in unit_by_id:
            _fail("UNKNOWN_UNIT_RESULT", f"unknown edit result {unit_id!r}")
        if unit_id in result_by_id:
            _fail("DUPLICATE_UNIT_RESULT", f"duplicate edit result {unit_id!r}")
        if result.get("context_capsule_sha256") != unit_by_id[unit_id]["context_capsule_sha256"]:
            _fail("STALE_UNIT_RESULT", f"edit result {unit_id!r} binds wrong capsule")
        result_by_id[unit_id] = result
    if set(result_by_id) != set(unit_by_id):
        _fail("MISSING_UNIT_RESULT", f"missing edit results {sorted(set(unit_by_id) - set(result_by_id))}")

    cuts: list[dict[str, Any]] = []
    placements: list[dict[str, Any]] = []
    overlays: list[dict[str, Any]] = []
    transitions: list[dict[str, Any]] = []
    seen_cuts: set[str] = set()
    known_assets = {item["id"] for item in assets["assets"]}
    for unit in sorted(units, key=lambda item: item["ordinal"]):
        result = result_by_id[unit["unit_id"]]
        fragment = result.get("edit_fragment")
        placement_rows = result.get("cut_timeline")
        if not isinstance(fragment, dict) or set(fragment) - {"version", "cuts", "overlays", "transitions"}:
            _fail("INVALID_EDIT_FRAGMENT", f"invalid fragment for {unit['unit_id']!r}")
        if fragment.get("version") != "1.0" or not isinstance(fragment.get("cuts"), list):
            _fail("INVALID_EDIT_FRAGMENT", f"unit {unit['unit_id']!r} lacks version/cuts")
        if not isinstance(placement_rows, list):
            _fail("INVALID_CUT_TIMELINE", f"unit {unit['unit_id']!r} lacks cut timeline")
        fragment_cuts = deepcopy(fragment["cuts"])
        placement_by_id: dict[str, dict[str, Any]] = {}
        for row in placement_rows:
            if not isinstance(row, dict) or set(row) != {"cut_id", "start_seconds", "end_seconds"}:
                _fail("INVALID_CUT_TIMELINE", "cut placement fields are invalid")
            if row["cut_id"] in placement_by_id:
                _fail("INVALID_CUT_TIMELINE", f"duplicate placement {row['cut_id']!r}")
            placement_by_id[row["cut_id"]] = row
        if set(placement_by_id) != {cut.get("id") for cut in fragment_cuts}:
            _fail("CUT_TIMELINE_COVERAGE", f"unit {unit['unit_id']!r} placement is not exact")
        primary: list[tuple[float, float, str]] = []
        for cut in fragment_cuts:
            cut_id = cut.get("id")
            if not isinstance(cut_id, str) or not cut_id or cut_id in seen_cuts:
                _fail("DUPLICATE_CUT_ID", f"invalid or duplicate cut {cut_id!r}")
            if cut.get("source") not in known_assets or cut["source"] not in unit["asset_ids"]:
                _fail("UNIT_OWNERSHIP_VIOLATION", f"cut {cut_id!r} uses a foreign asset")
            source_in = _number(cut.get("in_seconds"), "cut in_seconds")
            source_out = _number(cut.get("out_seconds"), "cut out_seconds")
            speed = _number(cut.get("speed", 1.0), "cut speed")
            row = placement_by_id[cut_id]
            start = _number(row["start_seconds"], "placement start")
            end = _number(row["end_seconds"], "placement end")
            if source_out <= source_in or end <= start:
                _fail("INVALID_CUT_TIME", f"cut {cut_id!r} has invalid duration")
            if abs((source_out - source_in) / speed - (end - start)) > _TOLERANCE:
                _fail("CUT_DURATION_MISMATCH", f"cut {cut_id!r} placement disagrees with trim/speed")
            if start < float(unit["start_seconds"]) - _TOLERANCE or end > float(unit["end_seconds"]) + _TOLERANCE:
                _fail("UNIT_OWNERSHIP_VIOLATION", f"cut {cut_id!r} crosses unit boundary")
            if cut.get("layer", "primary") == "primary":
                primary.append((start, end, cut_id))
            seen_cuts.add(cut_id)
            cuts.append(cut)
            placements.append(deepcopy(row))
        primary.sort()
        cursor = float(unit["start_seconds"])
        for start, end, cut_id in primary:
            if abs(start - cursor) > _TOLERANCE:
                _fail("PRIMARY_TIMELINE_COVERAGE", f"gap/overlap before cut {cut_id!r}")
            cursor = end
        if not primary or abs(cursor - float(unit["end_seconds"])) > _TOLERANCE:
            _fail("PRIMARY_TIMELINE_COVERAGE", f"unit {unit['unit_id']!r} is not fully covered")
        for overlay in deepcopy(fragment.get("overlays") or []):
            if overlay.get("asset_id") not in unit["asset_ids"]:
                _fail("UNIT_OWNERSHIP_VIOLATION", "overlay uses a foreign asset")
            if (
                _number(overlay.get("start_seconds"), "overlay start")
                < float(unit["start_seconds"]) - _TOLERANCE
                or _number(overlay.get("end_seconds"), "overlay end")
                > float(unit["end_seconds"]) + _TOLERANCE
            ):
                _fail("UNIT_OWNERSHIP_VIOLATION", "overlay crosses unit boundary")
            overlays.append(overlay)
        for transition in deepcopy(fragment.get("transitions") or []):
            at = _number(transition.get("at_seconds"), "transition time")
            if at < float(unit["start_seconds"]) or at > float(unit["end_seconds"]):
                _fail("UNIT_OWNERSHIP_VIOLATION", "transition crosses unit boundary")
            transitions.append(transition)

    placements.sort(key=lambda row: (float(row["start_seconds"]), row["cut_id"]))
    order = {row["cut_id"]: index for index, row in enumerate(placements)}
    cuts.sort(key=lambda cut: order[cut["id"]])
    edit: dict[str, Any] = {"version": "1.0", "cuts": cuts, **context}
    if overlays:
        edit["overlays"] = sorted(overlays, key=lambda item: (item["start_seconds"], item["asset_id"]))
    if transitions:
        edit["transitions"] = sorted(transitions, key=lambda item: item["at_seconds"])
    try:
        validate_artifact("edit_decisions", edit)
    except Exception as exc:
        _fail("INVALID_MERGED_EDIT", str(exc))
    unknown_refs = _asset_refs(edit) - known_assets
    if unknown_refs:
        _fail("UNRESOLVED_ASSET_REF", f"unknown edit asset refs {sorted(unknown_refs)}")
    return {
        "edit_decisions": edit,
        "cut_timeline": placements,
        "source_scene_plan_sha256": canonical_digest(scene),
        "asset_manifest_sha256": canonical_digest(assets),
        "production_locks_sha256": canonical_digest(dict(production_locks)),
        "edit_decisions_sha256": canonical_digest(edit),
    }


def run_edit_units(
    *,
    production_unit_policy: Mapping[str, Any] | None = None,
    execution_disposition: str | None = None,
    mode: str | None = None,
    **kwargs: Any,
) -> dict[str, Any] | None:
    """Strict no-op when off; otherwise merge a candidate without publishing."""

    contract = resolve_execution_contract(
        stage="edit",
        production_unit_policy=production_unit_policy,
        execution_disposition=execution_disposition,
        legacy_mode=mode,
    )
    if contract is None:
        return None
    result = merge_edit_units(**kwargs)
    return {
        **execution_report_fields(contract),
        "publish_allowed": contract["execution_disposition"] == "publish_candidate",
        "candidate": result,
    }
