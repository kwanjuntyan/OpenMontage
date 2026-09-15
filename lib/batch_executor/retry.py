"""M1 typed retry timing primitives."""

from __future__ import annotations

from typing import Protocol


class RandomSource(Protocol):
    def random(self) -> float: ...


def full_jitter_delay(
    retry_index: int,
    *,
    base_seconds: float,
    cap_seconds: float,
    random_source: RandomSource,
    retry_after_seconds: float = 0,
) -> float:
    """Return exponential full jitter, honoring a provider Retry-After floor."""

    ceiling = min(cap_seconds, base_seconds * (2**retry_index))
    jitter = max(0.0, min(1.0, float(random_source.random()))) * ceiling
    return max(float(retry_after_seconds), jitter)


__all__ = ["RandomSource", "full_jitter_delay"]
