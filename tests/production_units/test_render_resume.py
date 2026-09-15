from __future__ import annotations

from copy import deepcopy

import pytest

from lib.production_units.edit_merge import merge_edit_units
from lib.production_units.render import (
    build_assembly_command,
    build_unit_render_commands,
    make_assembly_receipt,
    make_unit_render_receipt,
    run_render_units,
)
from lib.production_units.scene_plan_merge import ProductionUnitError
from tests.production_units.test_edit_merge import LOCKS, edit_fixture


PROFILE = {
    "name": "course-h264-1080p",
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "video_codec": "h264",
    "audio_required": True,
    "audio_codec": "aac",
    "audio_sample_rate": 48000,
    "duration_tolerance_seconds": 0.05,
    "av_sync_tolerance_seconds": 0.04,
}


class FakeProbe:
    def __init__(self, durations):
        self.durations = durations
        self.calls = []

    def __call__(self, path: str):
        self.calls.append(path)
        return {
            "duration_seconds": self.durations[path],
            "width": 1920,
            "height": 1080,
            "fps": 30,
            "video_codec": "h264",
            "audio_stream_count": 1,
            "audio_codec": "aac",
            "audio_sample_rate": 48000,
            "av_sync_offset_seconds": 0.01,
            "decode_scan_passed": True,
            "pts_monotonic": True,
        }


def _render_fixture():
    scene, assets, units, results, context = edit_fixture()
    bundle = merge_edit_units(
        scene,
        assets,
        units,
        results,
        production_locks=LOCKS,
        global_edit_context=context,
    )
    commands = build_unit_render_commands(bundle, units, media_profile=PROFILE)
    probe = FakeProbe({command["output_intent"]: 10 for command in commands})
    receipts = [
        make_unit_render_receipt(
            command,
            output_sha256=f"sha256:{index + 1:064x}",
            output_size_bytes=1000 + index,
            probe_adapter=probe,
            media_profile=PROFILE,
        )
        for index, command in enumerate(commands)
    ]
    return bundle, units, commands, receipts, probe


def test_synthetic_unit_render_and_master_assembly_contracts() -> None:
    _, _, commands, receipts, probe = _render_fixture()
    assembly = build_assembly_command(
        commands,
        reversed(receipts),
        media_profile=PROFILE,
        final_output_intent="renders/course-master.mp4",
        platform_target="course_master",
    )
    master_probe = FakeProbe({"renders/course-master.mp4": 20})
    result = make_assembly_receipt(
        assembly,
        output_sha256="sha256:" + "f" * 64,
        output_size_bytes=5000,
        probe_adapter=master_probe,
        media_profile=PROFILE,
    )
    assert len(probe.calls) == 2
    assert assembly["expected_duration_seconds"] == 20
    assert result["render_report"]["outputs"][0]["duration_seconds"] == 20
    assert result["render_report"]["outputs"][0]["platform_target"] == "course_master"
    assert result["render_report"]["metadata"]["production_units"]["unit_count"] == 2


def test_unit_receipt_supports_isolated_repair_without_changing_other_command() -> None:
    _, _, commands, receipts, _ = _render_fixture()
    original_second = deepcopy(commands[1])
    repaired_probe = FakeProbe({commands[0]["output_intent"]: 10})
    repaired = make_unit_render_receipt(
        commands[0],
        output_sha256="sha256:" + "e" * 64,
        output_size_bytes=1100,
        probe_adapter=repaired_probe,
        media_profile=PROFILE,
    )
    assert repaired["receipt_sha256"] != receipts[0]["receipt_sha256"]
    assert commands[1] == original_second


@pytest.mark.parametrize(
    ("mutate", "code"),
    [
        (
            lambda command, probe: probe.durations.update(
                {command["output_intent"]: 9.5}
            ),
            "DURATION_MISMATCH",
        ),
        (
            lambda command, probe: setattr(
                probe,
                "__call__",
                lambda path: {},
            ),
            None,
        ),
    ],
)
def test_render_receipt_rejects_bad_evidence(mutate, code) -> None:
    _, _, commands, _, _ = _render_fixture()
    command = commands[0]
    probe = FakeProbe({command["output_intent"]: 10})
    if code is None:
        # Special-case audio removal because assigning __call__ on an instance
        # does not alter Python's special-method lookup.
        def no_audio(path):
            value = probe(path)
            value["audio_stream_count"] = 0
            value["audio_codec"] = None
            value["audio_sample_rate"] = None
            return value

        adapter = no_audio
        expected = "AUDIO_PROFILE_MISMATCH"
    else:
        mutate(command, probe)
        adapter = probe
        expected = code
    with pytest.raises(ProductionUnitError) as caught:
        make_unit_render_receipt(
            command,
            output_sha256="sha256:" + "a" * 64,
            output_size_bytes=100,
            probe_adapter=adapter,
            media_profile=PROFILE,
        )
    assert caught.value.code == expected


def test_assembly_rejects_stale_or_missing_receipt() -> None:
    _, _, commands, receipts, _ = _render_fixture()
    receipts[0]["command_sha256"] = "sha256:" + "0" * 64
    with pytest.raises(ProductionUnitError) as caught:
        build_assembly_command(
            commands,
            receipts,
            media_profile=PROFILE,
            final_output_intent="renders/course-master.mp4",
        )
    assert caught.value.code == "RENDER_RECEIPT_TAMPERED"


def test_render_mode_off_is_strict_noop() -> None:
    assert run_render_units(mode="off", edit_bundle={"bad": object()}) is None
