from __future__ import annotations

import json
import threading
from copy import deepcopy

import pytest

from lib.batch_executor.contracts import (
    freeze_batch_request,
)
from lib.batch_executor.engine import CloudBatchExecutor
from lib.batch_executor.errors import InjectedCrash, M1ExecutionError, StorageConflict
from lib.batch_executor.fake_gcs import FakeGCS
from lib.batch_executor.gcs_storage import GCSPreconditionFailed, GCSStore
from lib.batch_executor.media_validation import DeterministicFakeMediaValidator
from lib.batch_executor.ownership import (
    freeze_execution_status_evidence,
    freeze_resume_authorization,
)
from lib.batch_executor.runtime import CloudInvocationIdentity
from lib.batch_executor.testing import FakeClock, ScriptedFakeProvider
from tests.batch_executor.test_m1_engine import _request


OLD_EXECUTION = "projects/cloud-project/locations/us-central1/jobs/batch-v2/executions/old"
NEW_EXECUTION = "projects/cloud-project/locations/us-central1/jobs/batch-v2/executions/new"


def _cloud_request(batch_request, *, count=1, portable=False):
    request = _request(batch_request, count=count)
    request["execution_policy"]["storage_profile"] = (
        "portable" if portable else "cloud_run"
    )
    return freeze_batch_request(request)


def _executor(authorized_project, transport, provider, *, crash_hook=None):
    return CloudBatchExecutor(
        projects_root=authorized_project["projects_root"],
        provider=provider,
        media_validator=DeterministicFakeMediaValidator(),
        clock=FakeClock(),
        crash_hook=crash_hook,
        store_factory=lambda project_dir, batch_id: GCSStore(
            project_dir,
            batch_id,
            bucket="private-batch-bucket",
            transport=transport,
        ),
    )


def _run(
    executor,
    request,
    source_revision,
    observation,
    *,
    invocation_id,
    execution_id,
    mode="run",
    verifier=None,
    authorization=None,
):
    return executor.run(
        request,
        observed_source_revision=source_revision,
        adapter_observation=observation,
        trusted_invocation=CloudInvocationIdentity(
            invocation_id=invocation_id,
            execution_resource=execution_id,
            task_id="0",
            mode=mode,
        ),
        execution_status_verifier=verifier,
        resume_authorization=authorization,
    )


def _leave_active_owner(
    request,
    authorized_project,
    source_revision,
    observation,
    transport,
    *,
    invocation_id="invocation-old",
    execution_id=OLD_EXECUTION,
):
    provider = ScriptedFakeProvider()

    def crash(boundary, _facts):
        if boundary == "state_initialized":
            raise InjectedCrash(boundary)

    with pytest.raises(InjectedCrash):
        _run(
            _executor(authorized_project, transport, provider, crash_hook=crash),
            request,
            source_revision,
            observation,
            invocation_id=invocation_id,
            execution_id=execution_id,
        )
    assert provider.calls == []
    store = GCSStore(
        authorized_project["project_dir"],
        request["batch_id"],
        bucket="private-batch-bucket",
        transport=transport,
    )
    return store.load_batch_state()


class FakeADCStatusVerifier:
    verifier_id = "cloud_run_control_plane_adc"

    def __init__(self, owner, *, status="terminal"):
        self.calls = 0
        self.evidence = freeze_execution_status_evidence(
            {
                "version": "1.0",
                "evidence_id": "evidence-001",
                "batch_id": owner["batch_id"],
                "request_digest": owner["request_digest"],
                "prior_invocation_id": owner["invocation_id"],
                "prior_execution_id": owner["execution_id"],
                "observed_status": status,
                "observed_at": "2026-09-15T00:10:00Z",
                "verifier": "cloud_run_control_plane_adc",
                "execution_resource": owner["execution_id"],
            }
        )

    def verify_stopped(self, recorded_owner):
        self.calls += 1
        assert recorded_owner["execution_id"] == self.evidence["execution_resource"]
        return deepcopy(self.evidence)


def _resume_authorization(owner, generation, *, successor="invocation-new"):
    return freeze_resume_authorization(
        {
            "version": "1.0",
            "authorization_id": "resume-001",
            "batch_id": owner["batch_id"],
            "request_digest": owner["request_digest"],
            "prior_invocation_id": owner["invocation_id"],
            "prior_execution_id": owner["execution_id"],
            "intended_new_invocation_id": successor,
            "intended_new_execution_id": NEW_EXECUTION,
            "intended_new_task_id": "0",
            "expected_state_generation": generation,
            "reason": "Explicitly force ownership only after the prior execution stopped.",
            "decision_reference": "user-reply:resume-001",
            "authorized_at": "2026-09-15T00:11:00Z",
        }
    )


def test_active_prior_owner_blocks_different_ordinary_cloud_run_before_provider(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)
    transport = FakeGCS()
    _leave_active_owner(
        request,
        authorized_project,
        source_revision,
        qualified_adapter_observation,
        transport,
    )
    provider = ScriptedFakeProvider()
    with pytest.raises(M1ExecutionError, match="EXECUTION_OWNER_ACTIVE"):
        _run(
            _executor(authorized_project, transport, provider),
            request,
            source_revision,
            qualified_adapter_observation,
            invocation_id="invocation-other",
            execution_id=NEW_EXECUTION,
        )
    assert provider.calls == []


def test_cloud_engine_rejects_caller_fabricated_identity_object_before_provider(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)
    provider = ScriptedFakeProvider()
    executor = _executor(authorized_project, FakeGCS(), provider)
    with pytest.raises(M1ExecutionError, match="AUTH_CONFIGURATION"):
        executor.run(
            request,
            observed_source_revision=source_revision,
            adapter_observation=qualified_adapter_observation,
            trusted_invocation={
                "invocation_id": "fabricated",
                "execution_resource": NEW_EXECUTION,
                "task_id": "0",
                "mode": "run",
            },
        )
    assert provider.calls == []

    with pytest.raises(M1ExecutionError, match="AUTH_CONFIGURATION"):
        executor.run(
            request,
            observed_source_revision=source_revision,
            adapter_observation=qualified_adapter_observation,
            trusted_invocation=CloudInvocationIdentity(
                invocation_id="fabricated-task",
                execution_resource=NEW_EXECUTION,
                task_id="1",
                mode="run",
            ),
        )
    assert provider.calls == []


@pytest.mark.parametrize(
    "untrusted_signal",
    ["old_timestamp", "self_terminal", "stale_heartbeat", "missing_logs", "topology"],
)
def test_forbidden_takeover_signals_never_replace_exact_proof_or_dispatch(
    untrusted_signal,
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
):
    request = _cloud_request(batch_request)
    transport = FakeGCS()
    state, _ = _leave_active_owner(
        request,
        authorized_project,
        source_revision,
        qualified_adapter_observation,
        transport,
    )
    assert state["owner"]["owner_status"] == "active"
    provider = ScriptedFakeProvider()
    with pytest.raises(M1ExecutionError, match="RESUME_OWNERSHIP_PROOF_INVALID"):
        _run(
            _executor(authorized_project, transport, provider),
            request,
            source_revision,
            qualified_adapter_observation,
            invocation_id=f"resume-{untrusted_signal}",
            execution_id=NEW_EXECUTION,
            mode="resume",
        )
    assert provider.calls == []


def test_self_written_terminal_owner_still_requires_external_stop_proof(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)
    transport = FakeGCS()
    state, generation = _leave_active_owner(
        request,
        authorized_project,
        source_revision,
        qualified_adapter_observation,
        transport,
    )
    state["owner"]["owner_status"] = "terminal"
    state["revision"] += 1
    state["owner"]["state_revision"] = state["revision"]
    store = GCSStore(
        authorized_project["project_dir"],
        request["batch_id"],
        bucket="private-batch-bucket",
        transport=transport,
    )
    store.save_batch_state(state, expected_version=generation)
    provider = ScriptedFakeProvider()
    with pytest.raises(M1ExecutionError, match="RESUME_OWNERSHIP_PROOF_INVALID"):
        _run(
            _executor(authorized_project, transport, provider),
            request,
            source_revision,
            qualified_adapter_observation,
            invocation_id="resume-self-terminal",
            execution_id=NEW_EXECUTION,
            mode="resume",
        )
    assert provider.calls == []


def test_trusted_terminal_evidence_is_persisted_then_cas_and_reread_before_dispatch(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)
    transport = FakeGCS()
    state, _ = _leave_active_owner(
        request,
        authorized_project,
        source_revision,
        qualified_adapter_observation,
        transport,
    )
    verifier = FakeADCStatusVerifier(state["owner"])
    provider = ScriptedFakeProvider()
    result = _run(
        _executor(authorized_project, transport, provider),
        request,
        source_revision,
        qualified_adapter_observation,
        invocation_id="invocation-new",
        execution_id=NEW_EXECUTION,
        mode="resume",
        verifier=verifier,
    )
    assert result["outcome"] == "all_succeeded"
    assert provider.submit_calls == 1
    assert verifier.calls == 1
    assert any(
        "/ownership-evidence/" in name
        for name in transport.object_names("private-batch-bucket")
    )
    store = GCSStore(
        authorized_project["project_dir"],
        request["batch_id"],
        bucket="private-batch-bucket",
        transport=transport,
    )
    terminal, _ = store.load_batch_state()
    assert terminal["owner"]["invocation_id"] == "invocation-new"
    assert terminal["owner"]["execution_id"] == NEW_EXECUTION
    assert terminal["owner"]["owner_status"] == "terminal"
    assert terminal["ownership_proof_digests"] == [verifier.evidence["evidence_digest"]]


def test_human_resume_authorization_is_one_time_and_does_not_dispatch_on_replay(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)
    transport = FakeGCS()
    state, generation = _leave_active_owner(
        request,
        authorized_project,
        source_revision,
        qualified_adapter_observation,
        transport,
    )
    authorization = _resume_authorization(state["owner"], generation)

    def crash(boundary, _facts):
        if boundary == "cloud_owner_acquired":
            raise InjectedCrash(boundary)

    provider = ScriptedFakeProvider()
    with pytest.raises(InjectedCrash):
        _run(
            _executor(authorized_project, transport, provider, crash_hook=crash),
            request,
            source_revision,
            qualified_adapter_observation,
            invocation_id="invocation-new",
            execution_id=NEW_EXECUTION,
            mode="resume",
            authorization=authorization,
        )
    assert provider.calls == []

    replay_provider = ScriptedFakeProvider()
    with pytest.raises(M1ExecutionError, match="RESUME_OWNERSHIP_PROOF_INVALID"):
        _run(
            _executor(authorized_project, transport, replay_provider),
            request,
            source_revision,
            qualified_adapter_observation,
            invocation_id="invocation-new",
            execution_id=NEW_EXECUTION,
            mode="resume",
            authorization=authorization,
        )
    assert replay_provider.calls == []


def test_human_authorization_for_another_successor_execution_never_dispatches(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)
    transport = FakeGCS()
    state, generation = _leave_active_owner(
        request,
        authorized_project,
        source_revision,
        qualified_adapter_observation,
        transport,
    )
    authorization = _resume_authorization(state["owner"], generation)
    provider = ScriptedFakeProvider()
    with pytest.raises(M1ExecutionError, match="RESUME_OWNERSHIP_PROOF_INVALID"):
        _run(
            _executor(authorized_project, transport, provider),
            request,
            source_revision,
            qualified_adapter_observation,
            invocation_id="invocation-new",
            execution_id=f"{NEW_EXECUTION}-different",
            mode="resume",
            authorization=authorization,
        )
    assert provider.calls == []


def test_human_takeover_marks_prior_unknown_paid_dispatch_indeterminate_without_replay(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)
    transport = FakeGCS()

    def crash(boundary, _facts):
        if boundary == "dispatch_recorded":
            raise InjectedCrash(boundary)

    initial_provider = ScriptedFakeProvider()
    with pytest.raises(InjectedCrash):
        _run(
            _executor(
                authorized_project,
                transport,
                initial_provider,
                crash_hook=crash,
            ),
            request,
            source_revision,
            qualified_adapter_observation,
            invocation_id="invocation-old",
            execution_id=OLD_EXECUTION,
        )
    assert initial_provider.calls == []
    store = GCSStore(
        authorized_project["project_dir"],
        request["batch_id"],
        bucket="private-batch-bucket",
        transport=transport,
    )
    state, generation = store.load_batch_state()
    assert state["attempts"][0]["phase"] == "dispatched"
    authorization = _resume_authorization(state["owner"], generation)
    resume_provider = ScriptedFakeProvider()
    result = _run(
        _executor(authorized_project, transport, resume_provider),
        request,
        source_revision,
        qualified_adapter_observation,
        invocation_id="invocation-new",
        execution_id=NEW_EXECUTION,
        mode="resume",
        authorization=authorization,
    )
    assert result["outcome"] == "indeterminate"
    assert result["counts"]["indeterminate"] == 1
    assert resume_provider.calls == []
    terminal, _ = store.load_batch_state()
    assert terminal["attempts"][0]["phase"] == "indeterminate"
    assert terminal["attempts"][0]["retry_action"] == "mark_indeterminate"


def test_blob_uploaded_then_state_cas_failure_resumes_without_generation_replay(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)

    class OneStateCASFailure(FakeGCS):
        def __init__(self):
            super().__init__()
            self.blob_uploaded = False
            self.failed = False

        def write_object(self, **kwargs):
            name = kwargs["name"]
            if "/outputs/" in name:
                self.blob_uploaded = True
            elif (
                name.endswith("/state.json")
                and self.blob_uploaded
                and not self.failed
                and kwargs["if_generation_match"] > 0
            ):
                self.failed = True
                raise GCSPreconditionFailed("injected state CAS loss after blob upload")
            return super().write_object(**kwargs)

    transport = OneStateCASFailure()
    provider = ScriptedFakeProvider()
    with pytest.raises(StorageConflict, match="GCS_PRECONDITION_CONFLICT"):
        _run(
            _executor(authorized_project, transport, provider),
            request,
            source_revision,
            qualified_adapter_observation,
            invocation_id="invocation-old",
            execution_id=OLD_EXECUTION,
        )
    assert provider.submit_calls == 1
    store = GCSStore(
        authorized_project["project_dir"],
        request["batch_id"],
        bucket="private-batch-bucket",
        transport=transport,
    )
    state, _ = store.load_batch_state()
    staged_output = store.attempt_output_path(
        "item-001", "attempt-000001", "clip.mp4"
    )
    assert staged_output.is_file()
    staged_output.unlink()
    verifier = FakeADCStatusVerifier(state["owner"])

    result = _run(
        _executor(authorized_project, transport, provider),
        request,
        source_revision,
        qualified_adapter_observation,
        invocation_id="invocation-new",
        execution_id=NEW_EXECUTION,
        mode="resume",
        verifier=verifier,
    )
    assert result["outcome"] == "all_succeeded"
    assert provider.submit_calls == 1
    assert len(provider.calls) == 1
    assert staged_output.is_file()
    assert transport.successful_creates == 5  # request, state, blob, evidence, result
    assert len([name for name in transport.object_names("private-batch-bucket") if "/outputs/" in name]) == 1


def test_two_concurrent_first_runs_have_one_state_create_winner_and_one_provider(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)
    transport = FakeGCS()
    state_gate = threading.Barrier(2)

    def before_write(_bucket, name, generation):
        if name.endswith("/state.json") and generation == 0:
            state_gate.wait(timeout=10)

    transport.before_write = before_write
    providers = [ScriptedFakeProvider(), ScriptedFakeProvider()]
    outcomes: list[object] = []

    def invoke(index):
        try:
            outcomes.append(
                _run(
                    _executor(authorized_project, transport, providers[index]),
                    request,
                    source_revision,
                    qualified_adapter_observation,
                    invocation_id=f"initial-{index}",
                    execution_id=f"{NEW_EXECUTION}-{index}",
                )
            )
        except BaseException as exc:  # asserted below
            outcomes.append(exc)

    threads = [threading.Thread(target=invoke, args=(index,)) for index in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=15)
        assert not thread.is_alive()

    assert sum(isinstance(value, dict) for value in outcomes) == 1
    failures = [value for value in outcomes if isinstance(value, StorageConflict)]
    assert len(failures) == 1
    assert failures[0].code == "GCS_PRECONDITION_CONFLICT"
    assert sum(provider.submit_calls for provider in providers) == 1


def test_two_proven_successors_have_exactly_one_owner_cas_winner(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)
    transport = FakeGCS()
    state, generation = _leave_active_owner(
        request,
        authorized_project,
        source_revision,
        qualified_adapter_observation,
        transport,
    )
    takeover_gate = threading.Barrier(2)

    def before_write(_bucket, name, expected_generation):
        if name.endswith("/state.json") and expected_generation == generation:
            takeover_gate.wait(timeout=10)

    transport.before_write = before_write
    providers = [ScriptedFakeProvider(), ScriptedFakeProvider()]
    outcomes: list[object] = []

    def invoke(index):
        verifier = FakeADCStatusVerifier(state["owner"])
        try:
            outcomes.append(
                _run(
                    _executor(authorized_project, transport, providers[index]),
                    request,
                    source_revision,
                    qualified_adapter_observation,
                    invocation_id=f"successor-{index}",
                    execution_id=f"{NEW_EXECUTION}-{index}",
                    mode="resume",
                    verifier=verifier,
                )
            )
        except BaseException as exc:  # asserted below
            outcomes.append(exc)

    threads = [threading.Thread(target=invoke, args=(index,)) for index in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=15)
        assert not thread.is_alive()

    assert sum(isinstance(value, dict) for value in outcomes) == 1
    failures = [value for value in outcomes if isinstance(value, StorageConflict)]
    assert len(failures) == 1
    assert failures[0].code == "GCS_PRECONDITION_CONFLICT"
    assert sorted(provider.submit_calls for provider in providers) == [0, 1]


def test_cloud_success_waits_for_blob_reread_and_head_barrier(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)

    class BlockingBlobRead(FakeGCS):
        def __init__(self):
            super().__init__()
            self.entered = threading.Event()
            self.release = threading.Event()
            self.block_once = True

        def read_object(self, **kwargs):
            if "/outputs/" in kwargs["name"] and self.block_once:
                self.block_once = False
                self.entered.set()
                assert self.release.wait(timeout=10)
            return super().read_object(**kwargs)

    transport = BlockingBlobRead()
    provider = ScriptedFakeProvider()
    outcome: list[object] = []

    def invoke():
        try:
            outcome.append(
                _run(
                    _executor(authorized_project, transport, provider),
                    request,
                    source_revision,
                    qualified_adapter_observation,
                    invocation_id="invocation-sync",
                    execution_id=NEW_EXECUTION,
                )
            )
        except BaseException as exc:  # pragma: no cover - asserted below
            outcome.append(exc)

    thread = threading.Thread(target=invoke)
    thread.start()
    assert transport.entered.wait(timeout=10)
    assert outcome == []
    assert thread.is_alive()
    transport.release.set()
    thread.join(timeout=15)
    assert not thread.is_alive()
    assert len(outcome) == 1 and isinstance(outcome[0], dict)
    assert outcome[0]["outcome"] == "all_succeeded"


def test_gcs_transient_retries_storage_only_and_never_resubmits_generation(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)

    class OneBlobUploadFailure(FakeGCS):
        def __init__(self):
            super().__init__()
            self.failed = False

        def write_object(self, **kwargs):
            if "/outputs/" in kwargs["name"] and not self.failed:
                self.failed = True
                raise OSError("injected transient upload transport failure")
            return super().write_object(**kwargs)

    transport = OneBlobUploadFailure()
    provider = ScriptedFakeProvider()
    result = _run(
        _executor(authorized_project, transport, provider),
        request,
        source_revision,
        qualified_adapter_observation,
        invocation_id="invocation-storage-retry",
        execution_id=NEW_EXECUTION,
    )
    assert result["outcome"] == "all_succeeded"
    assert result["statistics"]["retries"] == 1
    assert provider.submit_calls == 1
    store = GCSStore(
        authorized_project["project_dir"],
        request["batch_id"],
        bucket="private-batch-bucket",
        transport=transport,
    )
    state, _ = store.load_batch_state()
    assert state["attempts"][0]["operation_retry_count"] == 1
    assert state["attempts"][0]["phase"] == "durably_committed"


def test_cloud_cancellation_releases_owner_with_generation_cas_and_zero_dispatch(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)

    class RecordingCASFakeGCS(FakeGCS):
        def __init__(self):
            super().__init__()
            self.state_writes = []

        def write_object(self, **kwargs):
            snapshot = super().write_object(**kwargs)
            if kwargs["name"].endswith("/state.json"):
                state = json.loads(kwargs["data"].decode("utf-8"))
                self.state_writes.append(
                    (
                        kwargs["if_generation_match"],
                        snapshot.generation,
                        state["owner"]["owner_status"],
                    )
                )
            return snapshot

    transport = RecordingCASFakeGCS()
    provider = ScriptedFakeProvider()
    cancellation = threading.Event()
    cancellation.set()
    result = _executor(authorized_project, transport, provider).run(
        request,
        observed_source_revision=source_revision,
        adapter_observation=qualified_adapter_observation,
        trusted_invocation=CloudInvocationIdentity(
            invocation_id="cancel-cloud",
            execution_resource=NEW_EXECUTION,
            task_id="0",
            mode="run",
        ),
        cancellation=cancellation,
    )
    assert result["outcome"] == "cancelled"
    assert provider.calls == []
    assert transport.state_writes[0][0] == 0
    for previous, current in zip(
        transport.state_writes, transport.state_writes[1:]
    ):
        assert current[0] == previous[1]
    assert transport.state_writes[-1][2] == "cancelled"
    store = GCSStore(
        authorized_project["project_dir"],
        request["batch_id"],
        bucket="private-batch-bucket",
        transport=transport,
    )
    terminal, _ = store.load_batch_state()
    assert terminal["owner"]["owner_status"] == "cancelled"
    assert terminal["result_ref"]["sha256"]


def test_cloud_result_written_crash_repairs_only_exact_state_link_without_dispatch(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _cloud_request(batch_request)
    transport = FakeGCS()

    def crash(boundary, _facts):
        if boundary == "result_written":
            raise InjectedCrash(boundary)

    initial_provider = ScriptedFakeProvider()
    with pytest.raises(InjectedCrash):
        _run(
            _executor(
                authorized_project,
                transport,
                initial_provider,
                crash_hook=crash,
            ),
            request,
            source_revision,
            qualified_adapter_observation,
            invocation_id="result-owner",
            execution_id=OLD_EXECUTION,
        )
    assert initial_provider.submit_calls == 1
    store = GCSStore(
        authorized_project["project_dir"],
        request["batch_id"],
        bucket="private-batch-bucket",
        transport=transport,
    )
    before, before_generation = store.load_batch_state()
    assert before["owner"]["owner_status"] == "terminal"
    assert "result_ref" not in before
    replacement_provider = ScriptedFakeProvider()
    result = _run(
        _executor(authorized_project, transport, replacement_provider),
        request,
        source_revision,
        qualified_adapter_observation,
        invocation_id="result-link-repair",
        execution_id=NEW_EXECUTION,
    )
    assert result["outcome"] == "all_succeeded"
    assert replacement_provider.calls == []
    repaired, repaired_generation = store.load_batch_state()
    assert repaired_generation > before_generation
    assert repaired["result_ref"]["sha256"]
    assert repaired["owner"]["invocation_id"] == "result-owner"
    assert repaired["owner"]["owner_status"] == "terminal"
