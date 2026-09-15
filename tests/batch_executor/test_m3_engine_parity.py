from __future__ import annotations

from copy import deepcopy

from lib.batch_executor.cli import _exit_for_result
from lib.batch_executor.contracts import freeze_batch_request
from lib.batch_executor.engine import CloudBatchExecutor, LocalBatchExecutor
from lib.batch_executor.fake_gcs import FakeGCS
from lib.batch_executor.gcs_storage import GCSStore
from lib.batch_executor.media_validation import DeterministicFakeMediaValidator
from lib.batch_executor.runtime import CloudInvocationIdentity
from lib.batch_executor.storage import LocalStore
from lib.batch_executor.testing import FakeClock, ScriptedFakeProvider
from tests.batch_executor.test_m1_engine import _request


def _transition(state):
    return {
        "status": state["status"],
        "items": tuple((item["item_id"], item["state"]) for item in state["items"]),
        "attempts": tuple(
            (
                attempt["item_id"],
                attempt["phase"],
                attempt["retry_action"],
                attempt["acceptance_knowledge"],
            )
            for attempt in state["attempts"]
        ),
        "cost": deepcopy(state["cost"]),
    }


def _result_semantics(result):
    return {
        "request_digest": result["request_digest"],
        "source_bindings": result["source_bindings"],
        "status": result["status"],
        "outcome": result["outcome"],
        "counts": result["counts"],
        "items": tuple((item["item_id"], item["state"]) for item in result["items"]),
        "cost": result["cost"],
        "statistics": result["statistics"],
    }


def test_shared_engine_has_reproducible_forty_item_local_fakegcs_parity(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = _request(batch_request, count=40)
    request["execution_policy"]["storage_profile"] = "portable"
    request = freeze_batch_request(request)
    transport = FakeGCS()
    local_transitions = []
    cloud_transitions = []

    class RecordingLocalStore(LocalStore):
        def save_batch_state(self, state, *, expected_version):
            version = super().save_batch_state(state, expected_version=expected_version)
            local_transitions.append(_transition(state))
            return version

    class RecordingGCSStore(GCSStore):
        def save_batch_state(self, state, *, expected_version):
            version = super().save_batch_state(state, expected_version=expected_version)
            cloud_transitions.append(_transition(state))
            return version

    local_provider = ScriptedFakeProvider()
    local_result = LocalBatchExecutor(
        projects_root=authorized_project["projects_root"],
        provider=local_provider,
        media_validator=DeterministicFakeMediaValidator(),
        clock=FakeClock(),
        store_factory=lambda project_dir, batch_id: RecordingLocalStore(
            project_dir, batch_id
        ),
    ).run(
        request,
        observed_source_revision=source_revision,
        adapter_observation=qualified_adapter_observation,
        invocation_id="parity-local",
    )

    cloud_provider = ScriptedFakeProvider()
    cloud_result = CloudBatchExecutor(
        projects_root=authorized_project["projects_root"],
        provider=cloud_provider,
        media_validator=DeterministicFakeMediaValidator(),
        clock=FakeClock(),
        store_factory=lambda project_dir, batch_id: RecordingGCSStore(
            project_dir,
            batch_id,
            bucket="private-batch-bucket",
            transport=transport,
        ),
    ).run(
        request,
        observed_source_revision=source_revision,
        adapter_observation=qualified_adapter_observation,
        trusted_invocation=CloudInvocationIdentity(
            invocation_id="parity-cloud",
            execution_resource=(
                "projects/cloud-project/locations/us-central1/jobs/batch-v2/"
                "executions/parity"
            ),
            task_id="0",
            mode="run",
        ),
    )

    assert local_result["request_digest"] == cloud_result["request_digest"]
    assert local_result["request_digest"] == request["request_digest"]
    assert _result_semantics(local_result) == _result_semantics(cloud_result)
    assert _exit_for_result(local_result) == _exit_for_result(cloud_result) == 0
    assert local_transitions == cloud_transitions
    assert local_provider.submit_calls == cloud_provider.submit_calls == 40
    assert local_provider.max_active == cloud_provider.max_active == 1
    assert len(
        [
            name
            for name in transport.object_names("private-batch-bucket")
            if "/outputs/" in name
        ]
    ) == 40
