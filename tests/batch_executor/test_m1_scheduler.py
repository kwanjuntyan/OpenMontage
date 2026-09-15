from __future__ import annotations

import threading

import pytest

from lib.batch_executor.errors import M1ExecutionError
from lib.batch_executor.retry import full_jitter_delay
from lib.batch_executor.scheduler import BoundedScheduler, projected_makespan
from lib.batch_executor.testing import FakeClock, SequenceRandom


@pytest.mark.parametrize("workers", [1, 2, 3, 4])
def test_scheduler_enforces_global_and_provider_concurrency(workers):
    release = threading.Event()
    enough_started = threading.Event()
    count_lock = threading.Lock()
    active = 0
    maximum = 0
    target = min(workers, 2)

    def blocked():
        nonlocal active, maximum
        with count_lock:
            active += 1
            maximum = max(maximum, active)
            if active == target:
                enough_started.set()
        assert release.wait(5)
        with count_lock:
            active -= 1
        return "ok"

    with BoundedScheduler(
        max_workers=workers,
        provider_caps={"fake": 2},
        provider_spacing_seconds={"fake": 0},
        clock=FakeClock(),
    ) as scheduler:
        futures = [scheduler.submit("fake", blocked) for _ in range(6)]
        assert enough_started.wait(5)
        assert maximum == target
        assert scheduler.max_observed_global <= workers
        assert scheduler.max_observed_by_provider["fake"] <= 2
        release.set()
        assert [future.result(timeout=5) for future in futures] == ["ok"] * 6


def test_selected_gemini_cap_remains_one_with_three_workers():
    release = threading.Event()
    started = threading.Event()

    def blocked():
        started.set()
        assert release.wait(5)

    with BoundedScheduler(
        max_workers=3,
        provider_caps={"gemini_omni": 1},
        provider_spacing_seconds={"gemini_omni": 0},
        clock=FakeClock(),
    ) as scheduler:
        futures = [scheduler.submit("gemini_omni", blocked) for _ in range(3)]
        assert started.wait(5)
        assert scheduler.max_observed_by_provider["gemini_omni"] == 1
        release.set()
        for future in futures:
            future.result(timeout=5)


def test_provider_spacing_uses_fake_clock_without_wall_sleep():
    clock = FakeClock()
    with BoundedScheduler(
        max_workers=3,
        provider_caps={"gemini_omni": 1},
        provider_spacing_seconds={"gemini_omni": 5},
        clock=clock,
    ) as scheduler:
        futures = [scheduler.submit("gemini_omni", lambda: "ok") for _ in range(3)]
        assert [future.result(timeout=5) for future in futures] == ["ok"] * 3
    assert clock.sleeps == [5, 5]
    assert scheduler.rate_limit_wait_seconds == 10


def test_worker_cap_range_and_retry_jitter_are_fail_closed_and_injected():
    for invalid in (0, 5):
        with pytest.raises(M1ExecutionError, match="INVALID_WORKER_CAP"):
            BoundedScheduler(
                max_workers=invalid,
                provider_caps={"fake": 1},
                provider_spacing_seconds={"fake": 0},
                clock=FakeClock(),
            )
    random_source = SequenceRandom([0.25, 0.75])
    assert full_jitter_delay(2, base_seconds=2, cap_seconds=10, random_source=random_source) == 2
    assert full_jitter_delay(5, base_seconds=2, cap_seconds=10, random_source=random_source) == 7.5


def test_forty_item_performance_model_is_deterministic_and_bounded():
    durations = [46.0] * 40
    serial = projected_makespan(durations, workers=1, provider_cap=4)
    parallel = projected_makespan(durations, workers=3, provider_cap=4)
    provider_limited = projected_makespan(durations, workers=3, provider_cap=1)
    assert serial == 1840.0
    assert parallel == 644.0
    assert serial / parallel > 2.8
    assert provider_limited == serial
