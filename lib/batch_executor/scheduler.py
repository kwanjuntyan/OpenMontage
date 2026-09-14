"""Mechanical bounded thread scheduling and provider quota controls."""

from __future__ import annotations

import heapq
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Callable, Mapping, Protocol, TypeVar

from .errors import M1ExecutionError


T = TypeVar("T")


class Clock(Protocol):
    def monotonic(self) -> float: ...

    def sleep(self, seconds: float) -> None: ...


class BoundedScheduler:
    """One thread pool with per-provider semaphores and request spacing."""

    def __init__(
        self,
        *,
        max_workers: int = 3,
        provider_caps: Mapping[str, int],
        provider_spacing_seconds: Mapping[str, float],
        clock: Clock,
    ):
        if not 1 <= max_workers <= 4:
            raise M1ExecutionError(
                "INVALID_WORKER_CAP", "global worker cap must be between 1 and 4"
            )
        if not provider_caps or any(cap < 1 for cap in provider_caps.values()):
            raise M1ExecutionError(
                "INVALID_PROVIDER_CAP", "provider concurrency caps must be positive"
            )
        self.max_workers = max_workers
        self._clock = clock
        self._pool = ThreadPoolExecutor(
            max_workers=max_workers, thread_name_prefix="batch-v2-worker"
        )
        self._semaphores = {
            provider: threading.BoundedSemaphore(cap)
            for provider, cap in provider_caps.items()
        }
        self._spacing = {
            provider: float(provider_spacing_seconds.get(provider, 0))
            for provider in provider_caps
        }
        self._next_start = {provider: 0.0 for provider in provider_caps}
        self._spacing_locks = {provider: threading.Lock() for provider in provider_caps}
        self._counter_lock = threading.Lock()
        self._active_global = 0
        self._active_by_provider = {provider: 0 for provider in provider_caps}
        self.max_observed_global = 0
        self.max_observed_by_provider = {provider: 0 for provider in provider_caps}
        self.rate_limit_wait_seconds = 0.0

    def __enter__(self) -> "BoundedScheduler":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self._pool.shutdown(wait=True, cancel_futures=True)

    def _run(self, provider: str, fn: Callable[[], T]) -> T:
        try:
            semaphore = self._semaphores[provider]
        except KeyError as exc:
            raise M1ExecutionError(
                "UNKNOWN_PROVIDER_QUOTA", f"No quota policy exists for {provider}"
            ) from exc
        with semaphore:
            with self._spacing_locks[provider]:
                now = self._clock.monotonic()
                wait = max(0.0, self._next_start[provider] - now)
                if wait:
                    self._clock.sleep(wait)
                    with self._counter_lock:
                        self.rate_limit_wait_seconds += wait
                self._next_start[provider] = (
                    self._clock.monotonic() + self._spacing[provider]
                )
            with self._counter_lock:
                self._active_global += 1
                self._active_by_provider[provider] += 1
                self.max_observed_global = max(
                    self.max_observed_global, self._active_global
                )
                self.max_observed_by_provider[provider] = max(
                    self.max_observed_by_provider[provider],
                    self._active_by_provider[provider],
                )
            try:
                return fn()
            finally:
                with self._counter_lock:
                    self._active_global -= 1
                    self._active_by_provider[provider] -= 1

    def submit(self, provider: str, fn: Callable[[], T]) -> Future[T]:
        return self._pool.submit(self._run, provider, fn)


def projected_makespan(
    durations: list[float], *, workers: int, provider_cap: int
) -> float:
    """Deterministic list-scheduling model for the no-wall-clock benchmark."""

    if workers < 1 or provider_cap < 1:
        raise M1ExecutionError("INVALID_WORKER_CAP", "caps must be positive")
    slots = min(workers, provider_cap)
    availability = [0.0] * slots
    heapq.heapify(availability)
    for duration in durations:
        if duration < 0:
            raise M1ExecutionError("INVALID_DURATION", "duration cannot be negative")
        available = heapq.heappop(availability)
        heapq.heappush(availability, available + float(duration))
    return max(availability, default=0.0)


__all__ = ["BoundedScheduler", "Clock", "projected_makespan"]
