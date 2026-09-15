from __future__ import annotations

from copy import deepcopy

import pytest

from lib.production_units.edit_merge import (
    build_edit_units,
    merge_edit_units,
    run_edit_units,
)
from lib.production_units.scene_plan_merge import ProductionUnitError


LOCKS = {
    "renderer_family": "explainer-teacher",
    "render_runtime": "remotion",
    "composition_mode": "templated",
}


def edit_fixture():
    scene_plan = {
        "version": "1.0",
        "scenes": [
            {
                "id": "scene-1",
                "type": "animation",
                "description": "Diagnose",
                "start_seconds": 0,
                "end_seconds": 10,
            },
            {
                "id": "scene-2",
                "type": "diagram",
                "description": "Design",
                "start_seconds": 10,
                "end_seconds": 20,
            },
        ],
    }
    asset_manifest = {
        "version": "1.0",
        "assets": [
            {
                "id": "video-1",
                "type": "video",
                "path": "assets/video/video-1.mp4",
                "source_tool": "fake",
                "scene_id": "scene-1",
            },
            {
                "id": "narration-1",
                "type": "narration",
                "path": "assets/audio/narration-1.wav",
                "source_tool": "fake",
                "scene_id": "scene-1",
            },
            {
                "id": "video-2",
                "type": "video",
                "path": "assets/video/video-2.mp4",
                "source_tool": "fake",
                "scene_id": "scene-2",
            },
            {
                "id": "narration-2",
                "type": "narration",
                "path": "assets/audio/narration-2.wav",
                "source_tool": "fake",
                "scene_id": "scene-2",
            },
        ],
    }
    inherited = [
        {
            "unit_id": "asset-unit-0001",
            "ordinal": 0,
            "scene_ids": ["scene-1"],
            "start_seconds": 0,
            "end_seconds": 10,
        },
        {
            "unit_id": "asset-unit-0002",
            "ordinal": 1,
            "scene_ids": ["scene-2"],
            "start_seconds": 10,
            "end_seconds": 20,
        },
    ]
    units = build_edit_units(scene_plan, asset_manifest, inherited)
    results = [
        {
            "unit_id": units[0]["unit_id"],
            "context_capsule_sha256": units[0]["context_capsule_sha256"],
            "edit_fragment": {
                "version": "1.0",
                "cuts": [
                    {
                        "id": "cut-1",
                        "source": "video-1",
                        "in_seconds": 0,
                        "out_seconds": 10,
                    }
                ],
            },
            "cut_timeline": [
                {"cut_id": "cut-1", "start_seconds": 0, "end_seconds": 10}
            ],
        },
        {
            "unit_id": units[1]["unit_id"],
            "context_capsule_sha256": units[1]["context_capsule_sha256"],
            "edit_fragment": {
                "version": "1.0",
                "cuts": [
                    {
                        "id": "cut-2",
                        "source": "video-2",
                        "in_seconds": 2,
                        "out_seconds": 7,
                        "speed": 0.5,
                    }
                ],
            },
            "cut_timeline": [
                {"cut_id": "cut-2", "start_seconds": 10, "end_seconds": 20}
            ],
        },
    ]
    global_context = {
        **LOCKS,
        "audio": {
            "narration": {
                "segments": [
                    {"asset_id": "narration-1", "start_seconds": 0, "end_seconds": 10},
                    {"asset_id": "narration-2", "start_seconds": 10, "end_seconds": 20},
                ]
            }
        },
        "metadata": {"title": "Course fixture"},
    }
    return scene_plan, asset_manifest, units, results, global_context


def test_edit_merge_is_deterministic_and_preserves_global_runtime_locks() -> None:
    scene, assets, units, results, context = edit_fixture()
    first = merge_edit_units(
        scene,
        assets,
        units,
        results,
        production_locks=LOCKS,
        global_edit_context=context,
    )
    second = merge_edit_units(
        scene,
        assets,
        units,
        reversed(results),
        production_locks=LOCKS,
        global_edit_context=context,
    )
    assert first == second
    assert [item["id"] for item in first["edit_decisions"]["cuts"]] == [
        "cut-1",
        "cut-2",
    ]
    assert first["edit_decisions"]["render_runtime"] == "remotion"
    assert first["cut_timeline"][-1]["end_seconds"] == 20


@pytest.mark.parametrize(
    ("mutate", "code"),
    [
        (
            lambda units, results, context: context.update(render_runtime="hyperframes"),
            "RUNTIME_LOCK_DRIFT",
        ),
        (
            lambda units, results, context: results[1]["cut_timeline"][0].update(
                start_seconds=11
            ),
            "CUT_DURATION_MISMATCH",
        ),
        (
            lambda units, results, context: results[1]["edit_fragment"]["cuts"][0].update(
                source="video-1"
            ),
            "UNIT_OWNERSHIP_VIOLATION",
        ),
        (
            lambda units, results, context: results[0].update(
                context_capsule_sha256="sha256:" + "0" * 64
            ),
            "STALE_UNIT_RESULT",
        ),
    ],
)
def test_edit_merge_fails_closed(mutate, code: str) -> None:
    scene, assets, units, results, context = edit_fixture()
    mutate(units, results, context)
    with pytest.raises(ProductionUnitError) as caught:
        merge_edit_units(
            scene,
            assets,
            units,
            results,
            production_locks=LOCKS,
            global_edit_context=context,
        )
    assert caught.value.code == code


def test_duplicate_repair_result_cannot_overwrite_another_unit() -> None:
    scene, assets, units, results, context = edit_fixture()
    results.append(deepcopy(results[0]))
    with pytest.raises(ProductionUnitError) as caught:
        merge_edit_units(
            scene,
            assets,
            units,
            results,
            production_locks=LOCKS,
            global_edit_context=context,
        )
    assert caught.value.code == "DUPLICATE_UNIT_RESULT"


def test_edit_mode_off_is_strict_noop() -> None:
    assert run_edit_units(mode="off", scene_plan={"bad": object()}) is None
