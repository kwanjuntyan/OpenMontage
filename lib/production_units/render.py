"""Offline M4 contracts for unit renders and deterministic master assembly."""

from __future__ import annotations

from copy import deepcopy
import math
from pathlib import PurePosixPath
import re
from typing import Any, Callable, Iterable, Mapping, Sequence

from lib.clp_validator import canonical_digest
from schemas.artifacts import validate_artifact

from .scene_plan_merge import ProductionUnitError


_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def _fail(code: str, message: str) -> None:
    raise ProductionUnitError(code, message)


def _number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail("INVALID_PROBE", f"{field} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        _fail("INVALID_PROBE", f"{field} must be a finite number")
    return result


def _safe_path(value: Any, *, prefix: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        _fail("INVALID_OUTPUT_PATH", "output intent must be a non-empty POSIX path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not value.startswith(prefix):
        _fail("INVALID_OUTPUT_PATH", f"output intent must stay under {prefix!r}")
    return value


def _validate_profile(profile: Mapping[str, Any]) -> dict[str, Any]:
    expected = {
        "name",
        "width",
        "height",
        "fps",
        "video_codec",
        "audio_required",
        "audio_codec",
        "audio_sample_rate",
        "duration_tolerance_seconds",
        "av_sync_tolerance_seconds",
    }
    value = deepcopy(dict(profile))
    if set(value) != expected:
        _fail("INVALID_MEDIA_PROFILE", "media profile fields are incomplete or unknown")
    if (
        not isinstance(value["name"], str)
        or not value["name"]
        or not isinstance(value["width"], int)
        or isinstance(value["width"], bool)
        or value["width"] <= 0
        or not isinstance(value["height"], int)
        or isinstance(value["height"], bool)
        or value["height"] <= 0
        or not isinstance(value["audio_required"], bool)
    ):
        _fail("INVALID_MEDIA_PROFILE", "media profile identity/dimensions are invalid")
    for field in ("fps", "audio_sample_rate", "duration_tolerance_seconds", "av_sync_tolerance_seconds"):
        if _number(value[field], field) < 0:
            _fail("INVALID_MEDIA_PROFILE", f"{field} cannot be negative")
    if not value["video_codec"] or not value["audio_codec"]:
        _fail("INVALID_MEDIA_PROFILE", "media codecs must be explicit")
    return value


def _freeze(document: Mapping[str, Any], field: str) -> dict[str, Any]:
    frozen = deepcopy(dict(document))
    frozen[field] = canonical_digest(
        {key: value for key, value in frozen.items() if key != field}
    )
    return frozen


def build_unit_render_commands(
    edit_bundle: Mapping[str, Any],
    units: Sequence[Mapping[str, Any]],
    *,
    media_profile: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Freeze one render command per edit unit without invoking a renderer."""

    edit = edit_bundle.get("edit_decisions")
    placements = edit_bundle.get("cut_timeline")
    if not isinstance(edit, dict) or not isinstance(placements, list):
        _fail("INVALID_EDIT_BUNDLE", "edit bundle requires decisions and cut timeline")
    try:
        validate_artifact("edit_decisions", edit)
    except Exception as exc:
        _fail("INVALID_EDIT_BUNDLE", str(exc))
    if edit_bundle.get("edit_decisions_sha256") != canonical_digest(edit):
        _fail("STALE_EDIT_BUNDLE", "edit digest changed")
    profile = _validate_profile(media_profile)
    command_rows: list[dict[str, Any]] = []
    cursor: float | None = None
    seen_units: set[str] = set()
    placement_ids = {item["cut_id"] for item in placements}
    if placement_ids != {item["id"] for item in edit["cuts"]}:
        _fail("INVALID_EDIT_BUNDLE", "cut timeline coverage is not exact")
    for ordinal, unit in enumerate(units):
        unit_id = unit.get("unit_id")
        start = _number(unit.get("start_seconds"), "unit start")
        end = _number(unit.get("end_seconds"), "unit end")
        if (
            not isinstance(unit_id, str)
            or not unit_id
            or unit_id in seen_units
            or unit.get("ordinal") != ordinal
            or end <= start
        ):
            _fail("INVALID_UNIT_PLAN", f"invalid render unit at ordinal {ordinal}")
        if cursor is not None and abs(start - cursor) > 1e-6:
            _fail("UNIT_TIMELINE_COVERAGE", "render units have a gap or overlap")
        cut_ids = [
            row["cut_id"]
            for row in placements
            if float(row["start_seconds"]) >= start - 1e-6
            and float(row["end_seconds"]) <= end + 1e-6
        ]
        if not cut_ids:
            _fail("UNIT_TIMELINE_COVERAGE", f"render unit {unit_id!r} has no cuts")
        command_rows.append(
            _freeze(
                {
                    "version": "1.0",
                    "unit_id": unit_id,
                    "ordinal": ordinal,
                    "start_seconds": unit["start_seconds"],
                    "end_seconds": unit["end_seconds"],
                    "cut_ids": cut_ids,
                    "render_runtime": edit["render_runtime"],
                    "renderer_family": edit.get("renderer_family"),
                    "composition_mode": edit.get("composition_mode"),
                    "edit_decisions_sha256": canonical_digest(edit),
                    "media_profile_sha256": canonical_digest(profile),
                    "output_intent": f".production-units/renders/{unit_id}.mp4",
                },
                "command_sha256",
            )
        )
        cursor = end
        seen_units.add(unit_id)
    return command_rows


def _validate_probe(
    probe: Mapping[str, Any],
    *,
    expected_duration: float,
    profile: Mapping[str, Any],
) -> dict[str, Any]:
    required = {
        "duration_seconds",
        "width",
        "height",
        "fps",
        "video_codec",
        "audio_stream_count",
        "audio_codec",
        "audio_sample_rate",
        "av_sync_offset_seconds",
        "decode_scan_passed",
        "pts_monotonic",
    }
    value = deepcopy(dict(probe))
    if set(value) != required:
        _fail("INVALID_PROBE", "probe fields are incomplete or unknown")
    duration = _number(value["duration_seconds"], "probe duration")
    if abs(duration - expected_duration) > float(profile["duration_tolerance_seconds"]):
        _fail("DURATION_MISMATCH", f"probe duration {duration} != {expected_duration}")
    if (
        value["width"] != profile["width"]
        or value["height"] != profile["height"]
        or abs(_number(value["fps"], "probe fps") - float(profile["fps"])) > 1e-6
        or value["video_codec"] != profile["video_codec"]
    ):
        _fail("MEDIA_PROFILE_MISMATCH", "video stream does not match locked profile")
    if not isinstance(value["audio_stream_count"], int) or isinstance(value["audio_stream_count"], bool):
        _fail("INVALID_PROBE", "audio_stream_count must be an integer")
    if profile["audio_required"]:
        if (
            value["audio_stream_count"] != 1
            or value["audio_codec"] != profile["audio_codec"]
            or value["audio_sample_rate"] != profile["audio_sample_rate"]
        ):
            _fail("AUDIO_PROFILE_MISMATCH", "required audio stream is absent or incompatible")
    elif value["audio_stream_count"] not in {0, 1}:
        _fail("AUDIO_PROFILE_MISMATCH", "unexpected audio stream count")
    if abs(_number(value["av_sync_offset_seconds"], "A/V sync")) > float(
        profile["av_sync_tolerance_seconds"]
    ):
        _fail("AV_SYNC_MISMATCH", "A/V sync exceeds profile tolerance")
    if value["decode_scan_passed"] is not True or value["pts_monotonic"] is not True:
        _fail("DECODE_SCAN_FAILED", "full decode/PTS evidence did not pass")
    return value


def make_unit_render_receipt(
    command: Mapping[str, Any],
    *,
    output_sha256: str,
    output_size_bytes: int,
    probe_adapter: Callable[[str], Mapping[str, Any]],
    media_profile: Mapping[str, Any],
) -> dict[str, Any]:
    """Apply an injected probe to synthetic or real output evidence."""

    if command.get("command_sha256") != canonical_digest(
        {key: value for key, value in command.items() if key != "command_sha256"}
    ):
        _fail("RENDER_COMMAND_TAMPERED", "unit render command digest mismatch")
    path = _safe_path(command.get("output_intent"), prefix=".production-units/renders/")
    if not isinstance(output_sha256, str) or not _DIGEST.fullmatch(output_sha256):
        _fail("INVALID_OUTPUT_DIGEST", "output_sha256 must be a PUP digest")
    if not isinstance(output_size_bytes, int) or isinstance(output_size_bytes, bool) or output_size_bytes <= 0:
        _fail("INVALID_OUTPUT_SIZE", "output size must be a positive integer")
    profile = _validate_profile(media_profile)
    if command.get("media_profile_sha256") != canonical_digest(profile):
        _fail("MEDIA_PROFILE_DRIFT", "render command binds another media profile")
    probe = _validate_probe(
        probe_adapter(path),
        expected_duration=float(command["end_seconds"]) - float(command["start_seconds"]),
        profile=profile,
    )
    return _freeze(
        {
            "version": "1.0",
            "unit_id": command["unit_id"],
            "ordinal": command["ordinal"],
            "command_sha256": command["command_sha256"],
            "output": {
                "logical_path": path,
                "sha256": output_sha256,
                "size_bytes": output_size_bytes,
            },
            "probe": probe,
        },
        "receipt_sha256",
    )


def build_assembly_command(
    commands: Sequence[Mapping[str, Any]],
    receipts: Iterable[Mapping[str, Any]],
    *,
    media_profile: Mapping[str, Any],
    final_output_intent: str,
) -> dict[str, Any]:
    """Freeze ordered unit receipts into one re-entrant assembly command."""

    profile = _validate_profile(media_profile)
    receipt_by_unit: dict[str, dict[str, Any]] = {}
    for raw in receipts:
        receipt = deepcopy(dict(raw))
        unit_id = receipt.get("unit_id")
        if unit_id in receipt_by_unit:
            _fail("DUPLICATE_RENDER_RECEIPT", f"duplicate receipt {unit_id!r}")
        if receipt.get("receipt_sha256") != canonical_digest(
            {key: value for key, value in receipt.items() if key != "receipt_sha256"}
        ):
            _fail("RENDER_RECEIPT_TAMPERED", f"receipt {unit_id!r} digest mismatch")
        receipt_by_unit[unit_id] = receipt
    if set(receipt_by_unit) != {item["unit_id"] for item in commands}:
        _fail("RENDER_RECEIPT_COVERAGE", "unit render receipt coverage is not exact")
    ordered = []
    expected_duration = 0.0
    for command in commands:
        receipt = receipt_by_unit[command["unit_id"]]
        if receipt.get("command_sha256") != command.get("command_sha256"):
            _fail("STALE_RENDER_RECEIPT", f"receipt for {command['unit_id']!r} binds another command")
        ordered.append(
            {
                "unit_id": command["unit_id"],
                "receipt_sha256": receipt["receipt_sha256"],
                "input": deepcopy(receipt["output"]),
            }
        )
        expected_duration += float(command["end_seconds"]) - float(command["start_seconds"])
    return _freeze(
        {
            "version": "1.0",
            "assembly_mode": "ordered_concat",
            "inputs": ordered,
            "expected_duration_seconds": expected_duration,
            "media_profile_sha256": canonical_digest(profile),
            "final_output_intent": _safe_path(final_output_intent, prefix="renders/"),
        },
        "command_sha256",
    )


def make_assembly_receipt(
    command: Mapping[str, Any],
    *,
    output_sha256: str,
    output_size_bytes: int,
    probe_adapter: Callable[[str], Mapping[str, Any]],
    media_profile: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate synthetic master evidence and return a render-report candidate."""

    if command.get("command_sha256") != canonical_digest(
        {key: value for key, value in command.items() if key != "command_sha256"}
    ):
        _fail("ASSEMBLY_COMMAND_TAMPERED", "assembly command digest mismatch")
    profile = _validate_profile(media_profile)
    if command.get("media_profile_sha256") != canonical_digest(profile):
        _fail("MEDIA_PROFILE_DRIFT", "assembly command binds another profile")
    path = _safe_path(command.get("final_output_intent"), prefix="renders/")
    if not isinstance(output_sha256, str) or not _DIGEST.fullmatch(output_sha256):
        _fail("INVALID_OUTPUT_DIGEST", "master output digest is invalid")
    if not isinstance(output_size_bytes, int) or isinstance(output_size_bytes, bool) or output_size_bytes <= 0:
        _fail("INVALID_OUTPUT_SIZE", "master output size must be positive")
    probe = _validate_probe(
        probe_adapter(path),
        expected_duration=float(command["expected_duration_seconds"]),
        profile=profile,
    )
    receipt = _freeze(
        {
            "version": "1.0",
            "command_sha256": command["command_sha256"],
            "output": {
                "logical_path": path,
                "sha256": output_sha256,
                "size_bytes": output_size_bytes,
            },
            "probe": probe,
        },
        "receipt_sha256",
    )
    report = {
        "version": "1.0",
        "outputs": [
            {
                "path": path,
                "format": "mp4",
                "codec": profile["video_codec"],
                "audio_codec": profile["audio_codec"] if profile["audio_required"] else "none",
                "resolution": f"{profile['width']}x{profile['height']}",
                "fps": profile["fps"],
                "duration_seconds": probe["duration_seconds"],
                "file_size_bytes": output_size_bytes,
            }
        ],
        "warnings": [],
        "verification_notes": ["PUP unit and master full-decode evidence passed"],
        "metadata": {
            "production_units": {
                "assembly_command_sha256": command["command_sha256"],
                "assembly_receipt_sha256": receipt["receipt_sha256"],
                "unit_count": len(command["inputs"]),
            }
        },
    }
    try:
        validate_artifact("render_report", report)
    except Exception as exc:
        _fail("INVALID_RENDER_REPORT_CANDIDATE", str(exc))
    return {"assembly_receipt": receipt, "render_report": report}


def run_render_units(*, mode: str | None = "off", **kwargs: Any) -> Any:
    """Strict no-op when off; prepare commands only when explicitly enabled."""

    if mode in (None, "off"):
        return None
    if mode not in {"compare_only", "publish_candidate"}:
        _fail("UNSUPPORTED_MODE", f"unsupported render production-unit mode {mode!r}")
    return {
        "mode": mode,
        "publish_allowed": False,
        "commands": build_unit_render_commands(**kwargs),
    }
