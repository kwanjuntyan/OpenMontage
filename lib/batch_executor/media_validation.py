"""Deterministic output hashing and M1 fake-media validation."""

from __future__ import annotations

import hashlib
import json
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


__all__ = ["DeterministicFakeMediaValidator", "MediaValidator", "OutputFacts"]
