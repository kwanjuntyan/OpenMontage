"""Offline deterministic test doubles for Batch Executor V2."""

from __future__ import annotations

import json
import threading
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Literal

from .tool_adapter import ProviderCall, ProviderFacts


def fake_video_bytes(
    *, duration_seconds: float = 8.0, has_audio: bool = True, valid: bool = True
) -> bytes:
    if not valid:
        return b"truncated-not-media"
    probe = {
        "container": "mp4",
        "duration_seconds": duration_seconds,
        "has_audio": has_audio,
        "video_codec": "h264",
    }
    header = json.dumps(probe, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return b"OPENMONTAGE_FAKE_VIDEO_V1\n" + header + b"\nFAKE-MEDIA-BYTES"


class FakeClock:
    def __init__(self, initial: datetime | None = None):
        self._wall = initial or datetime(2026, 9, 14, 8, 0, tzinfo=timezone.utc)
        self._monotonic = 0.0
        self._lock = threading.Lock()
        self.sleeps: list[float] = []

    def now(self) -> datetime:
        with self._lock:
            return self._wall

    def monotonic(self) -> float:
        with self._lock:
            return self._monotonic

    def sleep(self, seconds: float) -> None:
        seconds = max(0.0, float(seconds))
        with self._lock:
            self.sleeps.append(seconds)
            self._monotonic += seconds
            self._wall += timedelta(seconds=seconds)


class SequenceRandom:
    def __init__(self, values: list[float] | None = None):
        self._values = deque(values or [0.5])
        self._last = self._values[-1]

    def random(self) -> float:
        if self._values:
            self._last = self._values.popleft()
        return self._last


@dataclass(frozen=True)
class FakeProviderStep:
    success_value: bool
    acceptance: Literal["not_accepted", "accepted", "unknown"]
    retry_action: str = "none"
    error_class: str | None = None
    provider_operation_id: str | None = None
    known_actual_usd: float = 0.8
    potentially_charged_usd: float = 0.0
    retry_after_seconds: float = 0.0
    valid_media: bool = True
    kind: Literal["submit", "poll"] = "submit"

    @classmethod
    def success(
        cls,
        *,
        kind: Literal["submit", "poll"] = "submit",
        provider_operation_id: str | None = None,
        valid_media: bool = True,
        known_actual_usd: float | None = None,
    ) -> "FakeProviderStep":
        return cls(
            success_value=True,
            acceptance="accepted",
            provider_operation_id=provider_operation_id,
            valid_media=valid_media,
            kind=kind,
            known_actual_usd=(
                known_actual_usd
                if known_actual_usd is not None
                else 0.0
                if kind == "poll"
                else 0.8
            ),
        )

    @classmethod
    def error(
        cls,
        error_class: str,
        *,
        acceptance: Literal["not_accepted", "accepted", "unknown"],
        retry_action: str,
        provider_operation_id: str | None = None,
        retry_after_seconds: float = 0.0,
    ) -> "FakeProviderStep":
        known = 0.8 if acceptance == "accepted" else 0.0
        potential = 0.8 if acceptance == "unknown" else 0.0
        return cls(
            success_value=False,
            acceptance=acceptance,
            retry_action=retry_action,
            error_class=error_class,
            provider_operation_id=provider_operation_id,
            known_actual_usd=known,
            potentially_charged_usd=potential,
            retry_after_seconds=retry_after_seconds,
        )


class ScriptedFakeProvider:
    """Scripted provider with call kinds, charges, counters, and no network."""

    def __init__(
        self,
        *,
        scripts: dict[str, list[FakeProviderStep]] | None = None,
        cancel_after_submit: int | None = None,
        cancellation: threading.Event | None = None,
    ):
        self._scripts = {
            item_id: deque(steps) for item_id, steps in (scripts or {}).items()
        }
        self._indices: defaultdict[str, int] = defaultdict(int)
        self._lock = threading.Lock()
        self.calls: list[ProviderCall] = []
        self.submit_calls = 0
        self.poll_calls = 0
        self.accepted_submit_calls = 0
        self.active = 0
        self.max_active = 0
        self.cancel_after_submit = cancel_after_submit
        self.cancellation = cancellation

    def invoke(
        self, call: ProviderCall, cancellation: threading.Event
    ) -> ProviderFacts:
        with self._lock:
            self.calls.append(call)
            self.active += 1
            self.max_active = max(self.max_active, self.active)
            if call.kind == "submit":
                self.submit_calls += 1
            else:
                self.poll_calls += 1
            queue = self._scripts.get(call.item_id)
            step = queue.popleft() if queue else FakeProviderStep.success(kind=call.kind)
            if step.kind != call.kind:
                raise AssertionError(f"Expected fake {step.kind}, got {call.kind}")
            if call.kind == "submit" and step.acceptance == "accepted":
                self.accepted_submit_calls += 1
            should_cancel = (
                self.cancel_after_submit is not None
                and self.submit_calls >= self.cancel_after_submit
            )
        try:
            if step.success_value:
                call.output_path.write_bytes(
                    fake_video_bytes(valid=step.valid_media)
                )
            if should_cancel and self.cancellation is not None:
                self.cancellation.set()
            if step.success_value:
                return ProviderFacts(
                    success=True,
                    acceptance="accepted",
                    known_actual_usd=step.known_actual_usd,
                    potentially_charged_usd=step.potentially_charged_usd,
                    provider_operation_id=step.provider_operation_id
                    or f"fake-operation-{call.item_id}-{call.attempt_id}",
                )
            return ProviderFacts(
                success=False,
                acceptance=step.acceptance,
                known_actual_usd=step.known_actual_usd,
                potentially_charged_usd=step.potentially_charged_usd,
                provider_operation_id=step.provider_operation_id,
                error_class=step.error_class,
                retry_action=step.retry_action,
                sanitized_message=f"Scripted fake {step.error_class}",
                retry_after_seconds=step.retry_after_seconds,
            )
        finally:
            with self._lock:
                self.active -= 1


__all__ = [
    "FakeClock",
    "FakeProviderStep",
    "ScriptedFakeProvider",
    "SequenceRandom",
    "fake_video_bytes",
]
