"""Deterministic fake and coordinator-owned production media validation."""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol

from .errors import M1ExecutionError


@dataclass(frozen=True)
class OutputFacts:
    sha256: str
    size_bytes: int
    probe: Mapping[str, Any]


class MediaValidator(Protocol):
    def validate(self, path: Path, output_spec: Mapping[str, Any]) -> OutputFacts: ...


class DeterministicFakeMediaValidator:
    """Validate the explicit offline fake-video envelope used by M1 tests."""

    preamble = b"OPENMONTAGE_FAKE_VIDEO_V1\n"

    def validate(self, path: Path, output_spec: Mapping[str, Any]) -> OutputFacts:
        try:
            payload = path.read_bytes()
        except OSError as exc:
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", f"Output is unreadable: {path.name}"
            ) from exc
        if not payload.startswith(self.preamble) or len(payload) <= len(self.preamble):
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", "Output has no valid fake media envelope"
            )
        try:
            header_bytes, body = payload[len(self.preamble) :].split(b"\n", 1)
            probe = json.loads(header_bytes.decode("utf-8"))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", "Output media probe envelope is malformed"
            ) from exc
        required = {"container", "duration_seconds", "video_codec", "has_audio"}
        if set(probe) != required or not body:
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", "Output media is empty or has incomplete probe facts"
            )
        if probe["container"] != output_spec["container"]:
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", "Output container does not match request"
            )
        if probe["video_codec"] not in output_spec["allowed_video_codecs"]:
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", "Output codec does not match request"
            )
        expected_duration = float(str(output_spec.get("duration", "0s")).rstrip("s") or 0)
        if not expected_duration:
            expected_duration = 8.0
        if abs(float(probe["duration_seconds"]) - expected_duration) > 0.01:
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", "Output duration does not match request"
            )
        if bool(probe["has_audio"]) is not bool(output_spec["audio_expected"]):
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", "Output audio presence does not match request"
            )
        return OutputFacts(
            sha256=hashlib.sha256(payload).hexdigest(),
            size_bytes=len(payload),
            probe=probe,
        )


class FFprobeMediaValidator:
    """Technical validator for production MP4 output; invoked by the coordinator."""

    def __init__(self, *, ffprobe_binary: str = "ffprobe"):
        self.ffprobe_binary = ffprobe_binary

    def validate(self, path: Path, output_spec: Mapping[str, Any]) -> OutputFacts:
        try:
            completed = subprocess.run(
                [
                    self.ffprobe_binary,
                    "-v",
                    "error",
                    "-print_format",
                    "json",
                    "-show_format",
                    "-show_streams",
                    str(path),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID",
                "ffprobe is unavailable or failed to inspect the provider output",
            ) from exc
        if completed.returncode != 0:
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", "ffprobe rejected the provider output"
            )
        try:
            document = json.loads(completed.stdout)
            streams = document["streams"]
            format_facts = document["format"]
            video_streams = [
                stream for stream in streams if stream.get("codec_type") == "video"
            ]
            audio_streams = [
                stream for stream in streams if stream.get("codec_type") == "audio"
            ]
            video = video_streams[0]
            duration = float(format_facts["duration"])
        except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", "ffprobe returned incomplete media facts"
            ) from exc
        codec = {"hevc": "h265"}.get(
            str(video.get("codec_name")), str(video.get("codec_name"))
        )
        format_names = set(str(format_facts.get("format_name", "")).split(","))
        expected_duration = float(
            str(output_spec.get("duration", "0s")).rstrip("s")
        )
        if (
            "mp4" not in format_names
            or output_spec["container"] != "mp4"
            or codec not in output_spec["allowed_video_codecs"]
            or duration <= 0
            or abs(duration - expected_duration) > 1.0
            or bool(audio_streams) is not bool(output_spec["audio_expected"])
        ):
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID",
                "Provider media differs from the frozen MP4/duration/codec/audio contract",
            )
        try:
            payload = path.read_bytes()
        except OSError as exc:
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", "Provider output is unreadable"
            ) from exc
        if not payload:
            raise M1ExecutionError(
                "OUTPUT_TECHNICALLY_INVALID", "Provider output is empty"
            )
        return OutputFacts(
            sha256=hashlib.sha256(payload).hexdigest(),
            size_bytes=len(payload),
            probe={
                "container": "mp4",
                "duration_seconds": duration,
                "video_codec": codec,
                "has_audio": bool(audio_streams),
            },
        )


__all__ = [
    "DeterministicFakeMediaValidator",
    "FFprobeMediaValidator",
    "MediaValidator",
    "OutputFacts",
]
