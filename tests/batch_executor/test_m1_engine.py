from __future__ import annotations

import threading
from copy import deepcopy

import pytest

from lib.batch_executor.contracts import (
    canonical_json_bytes,
    compute_idempotency_digest,
    freeze_batch_request,
    validate_batch_result,
    validate_batch_state,
)
from lib.batch_executor.engine import LocalBatchExecutor
from lib.batch_executor.errors import InjectedCrash
from lib.batch_executor.media_validation import DeterministicFakeMediaValidator
from lib.batch_executor.storage import LocalStore
from lib.batch_executor.testing import FakeClock, FakeProviderStep, ScriptedFakeProvider


def _request(batch_request, *, count=1, max_attempts=1, allowance=0, budget=None):
    request = deepcopy(batch_request)
    request["work_items"] = []
    for index in range(count):
        item = deepcopy(batch_request["work_items"][0])
        item.update(
            {
                "item_id": f"item-{index + 1:03d}",
                "scene_id": f"scene-{index + 1}",
                "asset_id": f"asset-{index + 1}",
                "work_item_digest": "0" * 64,
                "charged_retry_allowance": allowance,
            }
        )
        item["inputs"]["prompt"] += f" Item {index + 1}."
        item["output_spec"]["canonical_destination_intent"] = (
            f"assets/video/asset-{index + 1}.mp4"
        )
        request["work_items"].append(item)
    cap = budget if budget is not None else count * max_attempts * 0.8
    request["authorization"].update(
        {
            "approved_budget_usd": cap,
            "max_authorized_spend_usd": cap,
            "max_total_attempts": count * max_attempts,
        }
    )
    request["execution_policy"]["max_attempts_per_item"] = max_attempts
    return freeze_batch_request(request)


def _executor(authorized_project, provider, *, clock=None, crash_hook=None):
    return LocalBatchExecutor(
        projects_root=authorized_project["projects_root"],
        provider=provider,
        media_validator=DeterministicFakeMediaValidator(),
        clock=clock or FakeClock(),
        crash_hook=crash_hook,
    )


def _run(executor, request, source_revision, observation, **kwargs):
    return executor.run(
        request,
        observed_source_revision=source_revision,
        adapter_observation=observation,
        invocation_id=kwargs.pop("invocation_id", "invocation-m1"),
        **kwargs,
    )


def test_fake_assets_batch_completes_with_exact_accounting_and_paths(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request, count=4)
    provider = ScriptedFakeProvider()
    result = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
    )
    validate_batch_result(result)
    assert result["outcome"] == "all_succeeded"
    assert result["counts"] == {
        "successful": 4,
        "cache_hit": 0,
        "failed": 0,
        "blocked": 0,
        "indeterminate": 0,
        "cancelled": 0,
    }
    assert result["cost"]["known_actual_usd"] == pytest.approx(3.2)
    assert provider.max_active == 1
    assert provider.submit_calls == 4
    for call in provider.calls:
        expected = LocalStore(
            authorized_project["project_dir"], request["batch_id"]
        ).attempt_output_path(call.item_id, call.attempt_id, "clip.mp4")
        assert call.output_path == expected


def test_same_batch_id_with_different_frozen_request_fails_before_provider(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    first = _request(batch_request)
    provider = ScriptedFakeProvider()

    def stop_after_request(name, _facts):
        if name == "request_persisted":
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        _run(
            _executor(authorized_project, provider, crash_hook=stop_after_request),
            first,
            source_revision,
            qualified_adapter_observation,
        )
    changed = deepcopy(first)
    changed["work_items"][0]["inputs"]["prompt"] += " Changed exact request."
    changed["work_items"][0]["work_item_digest"] = "0" * 64
    changed = freeze_batch_request(changed)
    with pytest.raises(Exception, match="REQUEST_CONFLICT"):
        _run(
            _executor(authorized_project, provider),
            changed,
            source_revision,
            qualified_adapter_observation,
            invocation_id="invocation-conflict",
        )
    assert provider.submit_calls == 0


def test_same_request_resume_reuses_only_verified_digest_identity_source_receipt_and_probe(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request, count=2)
    provider = ScriptedFakeProvider()
    executor = _executor(authorized_project, provider)
    first = _run(executor, request, source_revision, qualified_adapter_observation)
    second = _run(
        executor,
        request,
        source_revision,
        qualified_adapter_observation,
        invocation_id="invocation-reuse",
    )
    assert first == second
    assert provider.submit_calls == 2

    receipt = first["items"][0]["storage_receipt"]
    blob = authorized_project["project_dir"] / receipt["locator"]
    blob.write_bytes(b"corrupt")
    with pytest.raises(Exception, match="REUSE_RECEIPT_INVALID"):
        _run(
            executor,
            request,
            source_revision,
            qualified_adapter_observation,
            invocation_id="invocation-corrupt-reuse",
        )
    assert provider.submit_calls == 2


def test_reuse_rejects_state_attempt_not_bound_to_frozen_work_item(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request)
    provider = ScriptedFakeProvider()
    executor = _executor(authorized_project, provider)
    _run(executor, request, source_revision, qualified_adapter_observation)
    store = LocalStore(authorized_project["project_dir"], request["batch_id"])
    state, _ = store.load_batch_state()
    state["attempts"][0]["work_item_digest"] = "e" * 64
    state["attempts"][0]["idempotency_digest"] = compute_idempotency_digest(
        request["request_digest"], "e" * 64
    )
    store.state_path.write_bytes(canonical_json_bytes(state))

    with pytest.raises(Exception, match="REUSE_RECEIPT_INVALID"):
        _run(
            _executor(authorized_project, provider),
            request,
            source_revision,
            qualified_adapter_observation,
            invocation_id="invocation-tampered-state",
        )
    assert provider.submit_calls == 1


@pytest.mark.parametrize(
    "boundary",
    [
        "request_persisted",
        "state_initialized",
        "attempt_reserved",
        "dispatch_recorded",
        "provider_result_recorded",
        "media_validated",
        "blob_committed",
        "item_committed",
        "result_written",
    ],
)
def test_crash_resume_boundaries_never_duplicate_an_accepted_generation(
    boundary,
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
):
    request = _request(batch_request)
    provider = ScriptedFakeProvider()
    fired = False

    def crash_hook(name, _facts):
        nonlocal fired
        if name == boundary and not fired:
            fired = True
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        _run(
            _executor(authorized_project, provider, crash_hook=crash_hook),
            request,
            source_revision,
            qualified_adapter_observation,
        )
    accepted_before_resume = provider.accepted_submit_calls
    result = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
        invocation_id="invocation-resume",
    )
    validate_batch_result(result)
    assert provider.accepted_submit_calls <= max(1, accepted_before_resume)
    if boundary in {"dispatch_recorded", "provider_result_recorded"}:
        assert result["outcome"] in {"all_succeeded", "indeterminate"}
    else:
        assert result["outcome"] == "all_succeeded"


@pytest.mark.parametrize(
    ("boundary", "phase", "acceptance"),
    [
        ("attempt_reserved", "prepared", "not_accepted"),
        ("dispatch_recorded", "dispatched", "unknown"),
    ],
)
def test_predispatch_attempt_and_budget_are_durable_before_any_tool_call(
    boundary,
    phase,
    acceptance,
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
):
    request = _request(batch_request)
    provider = ScriptedFakeProvider()

    def crash(name, _facts):
        if name == boundary:
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        _run(
            _executor(authorized_project, provider, crash_hook=crash),
            request,
            source_revision,
            qualified_adapter_observation,
        )
    state, _ = LocalStore(
        authorized_project["project_dir"], request["batch_id"]
    ).load_batch_state()
    assert provider.submit_calls == 0
    assert state["attempts"][0]["phase"] == phase
    assert state["attempts"][0]["acceptance_knowledge"] == acceptance
    assert state["cost"]["reserved_usd"] == pytest.approx(0.8)


def test_unknown_paid_acceptance_is_indeterminate_and_never_auto_replayed(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request, max_attempts=2, allowance=1)
    provider = ScriptedFakeProvider(
        scripts={
            "item-001": [
                FakeProviderStep.error(
                    "TIMEOUT_OR_NETWORK_UNKNOWN",
                    acceptance="unknown",
                    retry_action="mark_indeterminate",
                ),
                FakeProviderStep.success(),
            ]
        }
    )
    result = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
    )
    assert result["outcome"] == "indeterminate"
    assert result["counts"]["indeterminate"] == 1
    assert provider.submit_calls == 1
    state, _ = LocalStore(
        authorized_project["project_dir"], request["batch_id"]
    ).load_batch_state()
    validate_batch_state(state)
    assert state["attempts"][-1]["phase"] == "indeterminate"


def test_typed_retry_never_turns_poll_or_storage_into_generation_replay(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request, max_attempts=2)
    provider = ScriptedFakeProvider(
        scripts={
            "item-001": [
                FakeProviderStep.error(
                    "REMOTE_JOB_RECOVERABLE",
                    acceptance="accepted",
                    retry_action="poll_remote_operation",
                    provider_operation_id="remote-1",
                ),
                FakeProviderStep.success(kind="poll", provider_operation_id="remote-1"),
            ]
        }
    )
    result = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
    )
    assert result["outcome"] == "all_succeeded"
    assert provider.submit_calls == 1
    assert provider.poll_calls == 1
    assert result["statistics"]["retries"] == 1


def test_known_not_accepted_submit_retries_with_fake_backoff_only(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request, max_attempts=2, budget=1.6)
    provider = ScriptedFakeProvider(
        scripts={
            "item-001": [
                FakeProviderStep.error(
                    "RATE_LIMITED_SUBMIT_REJECTED",
                    acceptance="not_accepted",
                    retry_action="resubmit_generation",
                    retry_after_seconds=7,
                ),
                FakeProviderStep.success(),
            ]
        }
    )
    clock = FakeClock()
    result = _run(
        _executor(authorized_project, provider, clock=clock),
        request,
        source_revision,
        qualified_adapter_observation,
    )
    assert result["outcome"] == "all_succeeded"
    assert provider.submit_calls == 2
    assert clock.sleeps == [7]


def test_retry_deadline_is_durable_across_crash_and_resume(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request, max_attempts=2, budget=1.6)
    provider = ScriptedFakeProvider(
        scripts={
            "item-001": [
                FakeProviderStep.error(
                    "RATE_LIMITED_SUBMIT_REJECTED",
                    acceptance="not_accepted",
                    retry_action="resubmit_generation",
                    retry_after_seconds=7,
                ),
                FakeProviderStep.success(),
            ]
        }
    )
    fired = False

    def crash(name, _facts):
        nonlocal fired
        if name == "retry_wait_persisted" and not fired:
            fired = True
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        _run(
            _executor(authorized_project, provider, clock=FakeClock(), crash_hook=crash),
            request,
            source_revision,
            qualified_adapter_observation,
        )
    state, _ = LocalStore(
        authorized_project["project_dir"], request["batch_id"]
    ).load_batch_state()
    assert state["items"][0]["next_eligible_at"] == "2026-09-14T08:00:07Z"
    resume_clock = FakeClock()
    result = _run(
        _executor(authorized_project, provider, clock=resume_clock),
        request,
        source_revision,
        qualified_adapter_observation,
        invocation_id="invocation-retry-resume",
    )
    assert result["outcome"] == "all_succeeded"
    assert resume_clock.sleeps == [7]
    assert provider.submit_calls == 2


def test_storage_retry_reuses_staged_bytes_and_never_resubmits_generation(
    monkeypatch,
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
):
    request = _request(batch_request)
    provider = ScriptedFakeProvider()
    original = LocalStore.put_verified_blob
    calls = 0

    def transient_once(self, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            from lib.batch_executor.errors import M1ExecutionError

            raise M1ExecutionError("LOCAL_STORAGE_TRANSIENT", "scripted storage fault")
        return original(self, **kwargs)

    monkeypatch.setattr(LocalStore, "put_verified_blob", transient_once)
    result = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
    )
    assert result["outcome"] == "all_succeeded"
    assert calls == 2
    assert provider.submit_calls == 1
    assert result["statistics"]["retries"] == 1


def test_charged_technical_retry_checks_allowance_attempt_elapsed_and_budget(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request, max_attempts=2, allowance=1, budget=1.6)
    provider = ScriptedFakeProvider(
        scripts={
            "item-001": [
                FakeProviderStep.success(valid_media=False),
                FakeProviderStep.success(),
            ]
        }
    )
    result = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
    )
    assert result["outcome"] == "all_succeeded"
    assert provider.submit_calls == 2
    assert result["cost"]["known_actual_usd"] == pytest.approx(1.6)

    blocked_request = _request(
        deepcopy(batch_request), max_attempts=2, allowance=0, budget=1.6
    )
    blocked_request["batch_id"] = "batch-blocked"
    blocked_request = freeze_batch_request(blocked_request)
    blocked_provider = ScriptedFakeProvider(
        scripts={"item-001": [FakeProviderStep.success(valid_media=False)]}
    )
    blocked = _run(
        _executor(authorized_project, blocked_provider),
        blocked_request,
        source_revision,
        qualified_adapter_observation,
    )
    assert blocked["outcome"] == "failed"
    assert blocked_provider.submit_calls == 1


@pytest.mark.parametrize("limit", ["attempt_ceiling", "elapsed", "budget"])
def test_charged_retry_requires_every_frozen_limit(
    limit,
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
):
    if limit == "attempt_ceiling":
        request = _request(batch_request, max_attempts=2, allowance=1, budget=1.6)
        steps = [
            FakeProviderStep.error(
                "PROVIDER_TRANSIENT_PRE_ACCEPT",
                acceptance="not_accepted",
                retry_action="resubmit_generation",
            ),
            FakeProviderStep.success(valid_media=False),
        ]
        clock = FakeClock()
        expected_calls = 2
    else:
        request = _request(batch_request, max_attempts=2, allowance=1, budget=1.6)
        steps = [
            FakeProviderStep.success(
                valid_media=False,
                known_actual_usd=1.0 if limit == "budget" else 0.8,
            )
        ]
        clock = FakeClock()
        expected_calls = 1

    provider = ScriptedFakeProvider(scripts={"item-001": steps})
    if limit == "elapsed":
        delegate = provider

        class ElapsingProvider:
            def invoke(self, call, cancellation):
                facts = delegate.invoke(call, cancellation)
                clock.sleep(3600)
                return facts

        selected_provider = ElapsingProvider()
    else:
        selected_provider = provider
    result = _run(
        _executor(authorized_project, selected_provider, clock=clock),
        request,
        source_revision,
        qualified_adapter_observation,
    )
    assert result["outcome"] == "failed"
    assert provider.submit_calls == expected_calls


def test_every_state_write_and_budget_reservation_is_coordinator_serialized(
    monkeypatch,
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
):
    request = _request(batch_request, count=4)
    provider = ScriptedFakeProvider()
    original = LocalStore.save_batch_state
    writer_threads = []
    exposures = []

    def observe(self, state, *, expected_version):
        writer_threads.append(threading.get_ident())
        exposures.append(
            state["cost"]["reserved_usd"]
            + state["cost"]["known_actual_usd"]
            + state["cost"]["indeterminate_exposure_usd"]
        )
        return original(self, state, expected_version=expected_version)

    monkeypatch.setattr(LocalStore, "save_batch_state", observe)
    coordinator_thread = threading.get_ident()
    result = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
    )
    assert result["outcome"] == "all_succeeded"
    assert set(writer_threads) == {coordinator_thread}
    assert max(exposures) <= request["authorization"]["max_authorized_spend_usd"]


def test_cancellation_is_durable_and_stops_new_dispatch(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request, count=3)
    cancellation = threading.Event()
    provider = ScriptedFakeProvider(cancel_after_submit=1, cancellation=cancellation)
    result = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
        cancellation=cancellation,
    )
    assert result["counts"]["cancelled"] >= 1
    assert provider.submit_calls == 1
    state, _ = LocalStore(
        authorized_project["project_dir"], request["batch_id"]
    ).load_batch_state()
    validate_batch_state(state)
    assert state["owner"]["owner_status"] == "cancelled"
    resumed = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
        invocation_id="invocation-after-cancel",
    )
    assert resumed == result
    assert provider.submit_calls == 1


def test_cancellation_during_retry_wait_preserves_known_rejection_and_stops_replay(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request, max_attempts=2, budget=1.6)
    cancellation = threading.Event()
    provider = ScriptedFakeProvider(
        scripts={
            "item-001": [
                FakeProviderStep.error(
                    "PROVIDER_TRANSIENT_PRE_ACCEPT",
                    acceptance="not_accepted",
                    retry_action="resubmit_generation",
                )
            ]
        },
        cancel_after_submit=1,
        cancellation=cancellation,
    )
    result = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
        cancellation=cancellation,
    )
    assert result["outcome"] == "failed"
    assert provider.submit_calls == 1
    state, _ = LocalStore(
        authorized_project["project_dir"], request["batch_id"]
    ).load_batch_state()
    assert state["attempts"][-1]["acceptance_knowledge"] == "not_accepted"
    assert state["attempts"][-1]["retry_action"] == "do_not_retry"
    state, _ = LocalStore(
        authorized_project["project_dir"], request["batch_id"]
    ).load_batch_state()
    validate_batch_state(state)
    assert state["owner"]["owner_status"] == "cancelled"

    resumed = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
        invocation_id="invocation-after-cancel",
    )
    assert resumed == result
    assert provider.submit_calls == 1


def test_independent_item_continues_and_dependency_is_blocked_without_dispatch(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request, count=3)
    request = deepcopy(request)
    request["work_items"][1]["dependency_item_ids"] = ["item-001"]
    request["work_items"][1]["work_item_digest"] = "0" * 64
    request = freeze_batch_request(request)
    provider = ScriptedFakeProvider(
        scripts={
            "item-001": [
                FakeProviderStep.error(
                    "PROVIDER_PERMANENT_REJECT",
                    acceptance="not_accepted",
                    retry_action="do_not_retry",
                )
            ]
        }
    )
    result = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
    )
    assert result["outcome"] == "partial_failure"
    assert result["counts"] == {
        "successful": 1,
        "cache_hit": 0,
        "failed": 1,
        "blocked": 1,
        "indeterminate": 0,
        "cancelled": 0,
    }
    assert {call.item_id for call in provider.calls} == {"item-001", "item-003"}


def test_forty_item_fake_executor_workload_is_complete_and_model_assertion_is_stable(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    from lib.batch_executor.scheduler import projected_makespan

    request = _request(batch_request, count=40)
    provider = ScriptedFakeProvider()
    result = _run(
        _executor(authorized_project, provider),
        request,
        source_revision,
        qualified_adapter_observation,
    )
    assert result["counts"]["successful"] == 40
    assert provider.submit_calls == 40
    assert provider.max_active == 1
    assert projected_makespan([46.0] * 40, workers=3, provider_cap=3) == 644.0
