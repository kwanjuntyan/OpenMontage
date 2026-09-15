"""M3 adapter from PUP-owned asset slices to Batch Executor V2 work."""

from __future__ import annotations

from copy import deepcopy
import math
from typing import Any, Iterable, Mapping, Sequence

from lib.batch_executor.contracts import (
    canonical_sha256 as batch_sha256,
    exact_identity,
    freeze_batch_request,
    validate_batch_request,
    validate_batch_result,
)
from lib.clp_validator import (
    canonical_digest,
    validate_clp_shot_bindings_or_raise,
)
from schemas.artifacts import validate_artifact


class AssetBatchIntegrationError(ValueError):
    """Fail-closed PUP-to-Batch integration error with a stable code."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _fail(code: str, message: str) -> None:
    raise AssetBatchIntegrationError(code, message)


def _number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail("INVALID_TIME", f"{field} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        _fail("INVALID_TIME", f"{field} must be a finite number")
    return result


def _validated_sources(
    scene_plan: Mapping[str, Any],
    clp_manifest: Mapping[str, Any],
    clp_shot_bindings: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    scene = deepcopy(dict(scene_plan))
    clp = deepcopy(dict(clp_manifest))
    bindings = deepcopy(dict(clp_shot_bindings))
    try:
        validate_artifact("scene_plan", scene)
        validate_artifact("clp_manifest", clp)
        validate_artifact("clp_shot_bindings", bindings)
        validate_clp_shot_bindings_or_raise(bindings, clp, scene)
    except Exception as exc:
        _fail("INVALID_ASSET_SOURCES", str(exc))
    return scene, clp, bindings


def build_asset_units(
    scene_plan: Mapping[str, Any],
    clp_manifest: Mapping[str, Any],
    clp_shot_bindings: Mapping[str, Any],
    *,
    target_duration_seconds: float = 180.0,
    hard_max_duration_seconds: float = 480.0,
) -> list[dict[str, Any]]:
    """Partition an already validated global scene timeline at scene boundaries."""

    scene, clp, bindings = _validated_sources(
        scene_plan, clp_manifest, clp_shot_bindings
    )
    target = _number(target_duration_seconds, "target_duration_seconds")
    hard_max = _number(hard_max_duration_seconds, "hard_max_duration_seconds")
    if target <= 0 or hard_max < target:
        _fail("INVALID_UNIT_POLICY", "hard_max must be at least a positive target")
    scenes = deepcopy(scene["scenes"])
    seen: set[str] = set()
    cursor: float | None = None
    for item in scenes:
        scene_id = item.get("id")
        start = _number(item.get("start_seconds"), "scene start")
        end = _number(item.get("end_seconds"), "scene end")
        if not isinstance(scene_id, str) or not scene_id or scene_id in seen:
            _fail("INVALID_SCENE_PLAN", f"invalid or duplicate scene id {scene_id!r}")
        if end <= start:
            _fail("INVALID_SCENE_PLAN", f"scene {scene_id!r} must end after it starts")
        if cursor is not None and abs(start - cursor) > 1e-6:
            _fail("SCENE_TIMELINE_COVERAGE", f"gap or overlap before scene {scene_id!r}")
        if end - start > hard_max + 1e-6:
            _fail("SCENE_EXCEEDS_HARD_MAX", f"scene {scene_id!r} exceeds hard_max")
        cursor = end
        seen.add(scene_id)

    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for item in scenes:
        end = float(item["end_seconds"])
        if current and end - float(current[0]["start_seconds"]) > target + 1e-6:
            groups.append(current)
            current = []
        current.append(item)
        if end - float(current[0]["start_seconds"]) > hard_max + 1e-6:
            _fail("UNIT_EXCEEDS_HARD_MAX", f"asset unit ending at {item['id']!r} is too long")
    if current:
        groups.append(current)

    return [
        {
            "unit_id": f"asset-unit-{ordinal + 1:04d}",
            "ordinal": ordinal,
            "scene_ids": [item["id"] for item in group],
            "start_seconds": group[0]["start_seconds"],
            "end_seconds": group[-1]["end_seconds"],
            "source_scene_plan_sha256": canonical_digest(scene),
            "clp_manifest_sha256": canonical_digest(clp),
            "clp_shot_bindings_sha256": canonical_digest(bindings),
        }
        for ordinal, group in enumerate(groups)
    ]


def _validate_units(
    units: Sequence[Mapping[str, Any]],
    scene_plan: Mapping[str, Any],
    clp_manifest: Mapping[str, Any],
    clp_shot_bindings: Mapping[str, Any],
) -> dict[str, str]:
    expected_scenes = [item["id"] for item in scene_plan["scenes"]]
    actual_scenes: list[str] = []
    scene_owner: dict[str, str] = {}
    seen_units: set[str] = set()
    for ordinal, unit in enumerate(units):
        unit_id = unit.get("unit_id")
        scene_ids = unit.get("scene_ids")
        if (
            not isinstance(unit_id, str)
            or not unit_id
            or unit_id in seen_units
            or unit.get("ordinal") != ordinal
            or not isinstance(scene_ids, list)
            or not scene_ids
        ):
            _fail("INVALID_UNIT_PLAN", f"invalid asset unit at ordinal {ordinal}")
        if (
            unit.get("source_scene_plan_sha256") != canonical_digest(scene_plan)
            or unit.get("clp_manifest_sha256") != canonical_digest(clp_manifest)
            or unit.get("clp_shot_bindings_sha256")
            != canonical_digest(clp_shot_bindings)
        ):
            _fail("STALE_UNIT_PLAN", f"asset unit {unit_id!r} binds stale sources")
        for scene_id in scene_ids:
            if scene_id in scene_owner:
                _fail("SCENE_COVERAGE", f"scene {scene_id!r} has multiple asset owners")
            scene_owner[scene_id] = unit_id
        actual_scenes.extend(scene_ids)
        seen_units.add(unit_id)
    if actual_scenes != expected_scenes:
        _fail("SCENE_COVERAGE", "asset units must cover every scene exactly once in order")
    return scene_owner


def _exact_binding(
    source_bindings: Iterable[Mapping[str, Any]], artifact_name: str, digest: str
) -> Mapping[str, Any]:
    matches = [
        item
        for item in source_bindings
        if item.get("source_type") == "checkpoint_artifact"
        and item.get("artifact_name") == artifact_name
        and item.get("sha256") == digest
    ]
    if len(matches) != 1:
        _fail(
            "SOURCE_BINDING_MISMATCH",
            f"Batch request needs exactly one exact {artifact_name} checkpoint binding",
        )
    return matches[0]


def compile_asset_batch_request(
    base_request: Mapping[str, Any],
    *,
    scene_plan: Mapping[str, Any],
    clp_manifest: Mapping[str, Any],
    clp_shot_bindings: Mapping[str, Any],
    units: Sequence[Mapping[str, Any]],
    asset_specs: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Compile explicit video specs into one existing Batch V2 request.

    This function does not authorize work, dispatch, retry, reserve cost,
    review media, or publish an asset manifest. Those remain Batch V2 owners.
    """

    scene, clp, bindings = _validated_sources(
        scene_plan, clp_manifest, clp_shot_bindings
    )
    scene_owner = _validate_units(units, scene, clp, bindings)
    request = deepcopy(dict(base_request))
    try:
        validate_batch_request(request)
    except Exception as exc:
        _fail("INVALID_BASE_BATCH_REQUEST", str(exc))
    source_bindings = request["source_bindings"]
    scene_binding = _exact_binding(
        source_bindings, "scene_plan", batch_sha256(scene)
    )
    clp_binding = _exact_binding(
        source_bindings, "clp_shot_bindings", batch_sha256(bindings)
    )
    if scene_binding.get("clp_binding_digest") != clp_binding["sha256"]:
        _fail(
            "CLP_BINDING_MISMATCH",
            "scene-plan source must bind the exact CLP shot-binding digest",
        )

    expected: set[tuple[str, int]] = set()
    for scene_item in scene["scenes"]:
        for index, requirement in enumerate(scene_item.get("required_assets") or []):
            if requirement.get("source") == "generate" and requirement.get("type") == "video":
                expected.add((scene_item["id"], index))
    if not expected:
        _fail("NO_BATCH_V2_WORK", "no generated video requirements use the Batch V2 route")

    specs_by_requirement: dict[tuple[str, int], dict[str, Any]] = {}
    asset_ids: set[str] = set()
    item_ids: set[str] = set()
    for raw in asset_specs:
        spec = deepcopy(dict(raw))
        if set(spec) != {
            "item_id",
            "asset_id",
            "scene_id",
            "required_asset_index",
            "unit_id",
            "inputs",
            "output_spec",
            "estimated_cost_usd",
            "estimated_duration_seconds",
            "charged_retry_allowance",
            "dependency_asset_ids",
        }:
            _fail("INVALID_ASSET_SPEC", "asset spec has missing or unknown fields")
        key = (spec.get("scene_id"), spec.get("required_asset_index"))
        if key not in expected or key in specs_by_requirement:
            _fail("ASSET_COVERAGE", f"unknown or duplicate asset requirement {key!r}")
        if spec.get("unit_id") != scene_owner.get(spec["scene_id"]):
            _fail("UNIT_OWNERSHIP_VIOLATION", f"asset {spec.get('asset_id')!r} has wrong unit")
        if spec.get("asset_id") in asset_ids or spec.get("item_id") in item_ids:
            _fail("DUPLICATE_ASSET_ID", "asset_id and item_id must be unique")
        if not isinstance(spec.get("dependency_asset_ids"), list):
            _fail("INVALID_ASSET_SPEC", "dependency_asset_ids must be an array")
        specs_by_requirement[key] = spec
        asset_ids.add(spec["asset_id"])
        item_ids.add(spec["item_id"])
    if set(specs_by_requirement) != expected:
        _fail("ASSET_COVERAGE", f"missing generated video specs: {sorted(expected - set(specs_by_requirement))}")

    item_for_asset = {spec["asset_id"]: spec["item_id"] for spec in specs_by_requirement.values()}
    spec_for_asset = {
        spec["asset_id"]: spec for spec in specs_by_requirement.values()
    }
    work_items: list[dict[str, Any]] = []
    for scene_item in scene["scenes"]:
        for index, _requirement in enumerate(scene_item.get("required_assets") or []):
            spec = specs_by_requirement.get((scene_item["id"], index))
            if spec is None:
                continue
            unknown_dependencies = set(spec["dependency_asset_ids"]) - set(item_for_asset)
            if unknown_dependencies:
                _fail("UNKNOWN_ASSET_DEPENDENCY", f"unknown dependencies {sorted(unknown_dependencies)}")
            work_items.append(
                {
                    "item_id": spec["item_id"],
                    "scene_id": spec["scene_id"],
                    "asset_id": spec["asset_id"],
                    "work_item_digest": "0" * 64,
                    "identity": exact_identity(),
                    "inputs": deepcopy(spec["inputs"]),
                    # Batch V2 requires every frozen authority source to be
                    # consumed. Preserve its complete authenticated set; the
                    # two exact scene/CLP bindings above are additionally
                    # checked because they define PUP ownership.
                    "source_binding_ids": [
                        source["binding_id"] for source in source_bindings
                    ],
                    "input_references": [],
                    "output_spec": deepcopy(spec["output_spec"]),
                    "estimated_cost_usd": spec["estimated_cost_usd"],
                    "estimated_duration_seconds": spec["estimated_duration_seconds"],
                    "charged_retry_allowance": spec["charged_retry_allowance"],
                    "dependency_item_ids": [
                        item_for_asset[item] for item in spec["dependency_asset_ids"]
                    ],
                }
            )
    request["work_items"] = work_items
    try:
        frozen = freeze_batch_request(request)
    except Exception as exc:
        _fail("BATCH_REQUEST_REJECTED", str(exc))

    receipt = {
        "version": "1.0",
        "route": "batch_v2_owned",
        "source_scene_plan_sha256": canonical_digest(scene),
        "clp_manifest_sha256": canonical_digest(clp),
        "clp_shot_bindings_sha256": canonical_digest(bindings),
        "unit_plan_sha256": canonical_digest(list(units)),
        "batch_id": frozen["batch_id"],
        "batch_request_digest": frozen["request_digest"],
        "items": [
            {
                "unit_id": spec_for_asset[item["asset_id"]]["unit_id"],
                "item_id": item["item_id"],
                "asset_id": item["asset_id"],
                "scene_id": item["scene_id"],
                "work_item_digest": item["work_item_digest"],
            }
            for item in frozen["work_items"]
        ],
    }
    receipt["receipt_sha256"] = canonical_digest(receipt)
    return {"batch_request": frozen, "adapter_receipt": receipt}


def bind_batch_result(
    compilation: Mapping[str, Any], batch_result: Mapping[str, Any]
) -> dict[str, Any]:
    """Bind successful Batch results without claiming publication authority."""

    request = compilation.get("batch_request")
    receipt = compilation.get("adapter_receipt")
    if not isinstance(request, dict) or not isinstance(receipt, dict):
        _fail("INVALID_COMPILATION", "compilation requires Batch request and adapter receipt")
    if receipt.get("receipt_sha256") != canonical_digest(
        {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    ):
        _fail("ADAPTER_RECEIPT_TAMPERED", "adapter receipt digest mismatch")
    try:
        validate_batch_request(request)
        validate_batch_result(batch_result)
    except Exception as exc:
        _fail("INVALID_BATCH_EVIDENCE", str(exc))
    if (
        batch_result["batch_id"] != request["batch_id"]
        or batch_result["request_digest"] != request["request_digest"]
    ):
        _fail("STALE_BATCH_RESULT", "Batch result does not bind the compiled request")
    expected_sources = [
        {"binding_id": item["binding_id"], "sha256": item["sha256"]}
        for item in request["source_bindings"]
    ]
    if batch_result["source_bindings"] != expected_sources:
        _fail("STALE_BATCH_RESULT", "Batch result source bindings changed")
    result_by_id = {item["item_id"]: item for item in batch_result["items"]}
    expected_ids = [item["item_id"] for item in request["work_items"]]
    if set(result_by_id) != set(expected_ids):
        _fail("BATCH_RESULT_COVERAGE", "Batch result item coverage is not exact")
    selected = []
    for item in receipt["items"]:
        result = result_by_id[item["item_id"]]
        if result["state"] not in {"committed", "cache_hit"}:
            _fail("BATCH_RESULT_INCOMPLETE", f"item {item['item_id']!r} is {result['state']}")
        selected.append(
            {
                **deepcopy(item),
                "state": result["state"],
                "storage_receipt_sha256": canonical_digest(result["storage_receipt"]),
            }
        )
    bound = {
        "version": "1.0",
        "route": "batch_v2_owned",
        "batch_id": request["batch_id"],
        "batch_request_digest": request["request_digest"],
        "batch_result_sha256": canonical_digest(dict(batch_result)),
        "adapter_receipt_sha256": receipt["receipt_sha256"],
        "selected_results": selected,
        "publication_authority": "batch_v2_only",
    }
    bound["binding_sha256"] = canonical_digest(bound)
    return bound


def run_asset_units(*, mode: str | None = "off", **kwargs: Any) -> dict[str, Any] | None:
    """Strict no-op when off; otherwise compile only, never execute or publish."""

    if mode in (None, "off"):
        return None
    if mode not in {"compare_only", "publish_candidate"}:
        _fail("UNSUPPORTED_MODE", f"unsupported asset production-unit mode {mode!r}")
    compiled = compile_asset_batch_request(**kwargs)
    return {
        "mode": mode,
        "publish_allowed": False,
        **compiled,
    }
