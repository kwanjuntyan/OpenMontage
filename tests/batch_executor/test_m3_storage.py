from __future__ import annotations

from copy import deepcopy
import threading
import pytest

from lib.batch_executor.contracts import compute_idempotency_digest, freeze_batch_request
from lib.batch_executor.errors import M1ExecutionError, StorageConflict
from lib.batch_executor.fake_gcs import FakeGCS
from lib.batch_executor.gcs_storage import (
    GCSStore,
    GoogleCloudStorageTransport,
    crc32c_base64,
)
from lib.batch_executor.media_validation import DeterministicFakeMediaValidator
from lib.batch_executor.storage import ExecutionStore, LocalStore
from lib.batch_executor.testing import fake_video_bytes
from tests.batch_executor.test_m0_integrity import _valid_result, _valid_state


def _cloud_request(batch_request):
    request = deepcopy(batch_request)
    request["execution_policy"]["storage_profile"] = "cloud_run"
    return freeze_batch_request(request)


def _gcs_store(authorized_project, transport, *, batch_id="batch-001"):
    return GCSStore(
        authorized_project["project_dir"],
        batch_id,
        bucket="private-batch-bucket",
        transport=transport,
    )


@pytest.mark.parametrize("kind", ["local", "gcs"])
def test_store_protocol_round_trips_immutable_records_and_state_cas(
    kind, authorized_project, batch_request
):
    transport = FakeGCS()
    store: ExecutionStore
    request = batch_request
    if kind == "local":
        store = LocalStore(authorized_project["project_dir"], request["batch_id"])
    else:
        request = _cloud_request(batch_request)
        store = _gcs_store(authorized_project, transport)
    assert isinstance(store, ExecutionStore)

    request_version = store.write_request_if_absent(request)
    loaded_request, loaded_request_version = store.load_request()
    assert loaded_request == request
    assert loaded_request_version == request_version

    state = _valid_state()
    state["revision"] = 0
    state["owner"]["state_revision"] = 0
    state["request_digest"] = request["request_digest"]
    state["owner"]["request_digest"] = request["request_digest"]
    state["attempts"][0]["request_digest"] = request["request_digest"]
    state["attempts"][0]["idempotency_digest"] = compute_idempotency_digest(
        request["request_digest"], state["attempts"][0]["work_item_digest"]
    )
    state_version = store.save_batch_state(state, expected_version=None)
    loaded_state, loaded_state_version = store.load_batch_state()
    assert loaded_state == state
    assert loaded_state_version == state_version

    changed = deepcopy(state)
    changed["revision"] = 1
    changed["owner"]["state_revision"] = 1
    next_version = store.save_batch_state(changed, expected_version=state_version)
    assert next_version != state_version
    with pytest.raises(StorageConflict, match="(?:STATE_VERSION|GCS_PRECONDITION)"):
        store.save_batch_state(changed, expected_version=state_version)

    result = _valid_result()
    result["request_digest"] = request["request_digest"]
    result["items"][0]["storage_receipt"] = deepcopy(
        changed["storage_receipts"][0]
    )
    result_version = store.write_result_if_absent(result)
    loaded_result = store.load_result()
    assert loaded_result is not None
    assert loaded_result == (result, result_version)


def test_crc32c_uses_the_exact_gcs_big_endian_base64_encoding():
    assert crc32c_base64(b"123456789") == "4waSgw=="


def test_google_transport_reloads_the_exact_generation_returned_by_upload():
    calls = []

    class FakeBlob:
        def __init__(self, bucket, name, generation=None):
            self.bucket = bucket
            self.name = name
            self.generation = generation
            self.size = 3
            self.crc32c = crc32c_base64(b"abc")
            self.metadata = {}
            self.content_type = "application/octet-stream"

        def upload_from_string(self, data, **kwargs):
            calls.append(("upload", data, kwargs))
            self.generation = 17

        def reload(self, **kwargs):
            calls.append(("reload", self.generation, kwargs))

    class FakeBucket:
        def __init__(self, name):
            self.name = name

        def blob(self, name, generation=None):
            calls.append(("blob", name, generation))
            return FakeBlob(self, name, generation)

    class FakeClient:
        def bucket(self, name):
            return FakeBucket(name)

    snapshot = GoogleCloudStorageTransport(FakeClient()).write_object(
        bucket="private-batch-bucket",
        name="projects/p/object",
        data=b"abc",
        metadata={"client_sha256": "digest"},
        content_type="application/octet-stream",
        if_generation_match=0,
    )
    assert snapshot.generation == 17
    assert calls == [
        ("blob", "projects/p/object", None),
        (
            "upload",
            b"abc",
            {
                "content_type": "application/octet-stream",
                "if_generation_match": 0,
                "checksum": "crc32c",
            },
        ),
        ("blob", "projects/p/object", 17),
        ("reload", 17, {"if_generation_match": 17}),
    ]


def test_gcs_immutable_request_and_result_never_overwrite_a_different_record(
    authorized_project, batch_request
):
    transport = FakeGCS()
    store = _gcs_store(authorized_project, transport)
    request = _cloud_request(batch_request)
    store.write_request_if_absent(request)
    assert store.write_request_if_absent(request) == store.load_request()[1]

    changed = deepcopy(request)
    changed["work_items"][0]["inputs"]["prompt"] = "different authorized request"
    changed = freeze_batch_request(changed)
    with pytest.raises(StorageConflict, match="REQUEST_CONFLICT"):
        store.write_request_if_absent(changed)

    result = _valid_result()
    result["request_digest"] = request["request_digest"]
    store.write_result_if_absent(result)
    assert store.write_result_if_absent(result) == store.load_result()[1]
    changed_result = deepcopy(result)
    changed_result["agent_review_hints"] = ["Another schema-valid result projection."]
    with pytest.raises(StorageConflict, match="RESULT_CONFLICT"):
        store.write_result_if_absent(changed_result)


def test_gcs_blob_commit_is_private_content_addressed_and_synchronously_verified(
    authorized_project, batch_request
):
    transport = FakeGCS()
    store = _gcs_store(authorized_project, transport)
    request = _cloud_request(batch_request)
    output = store.attempt_output_path("item-001", "attempt-000001", "clip.mp4")
    store.prepare_attempt_directory(output)
    output.write_bytes(fake_video_bytes())
    validator = DeterministicFakeMediaValidator()
    facts = validator.validate(output, request["work_items"][0]["output_spec"] | {"duration": "8s"})

    receipt = store.put_verified_blob(
        source=output,
        logical_path=output.relative_to(authorized_project["project_dir"]).as_posix(),
        batch_id=request["batch_id"],
        item_id="item-001",
        attempt_id="attempt-000001",
        output=facts,
        created_at="2026-09-15T00:00:00Z",
    )

    assert receipt["store_type"] == "gcs"
    assert receipt["locator"].startswith("gs://private-batch-bucket/projects/batch-project/")
    assert receipt["locator"].endswith(f"/outputs/item-001/{facts.sha256}")
    assert receipt["generation"] >= 1
    assert receipt["provider_checksum"]["algorithm"] == "crc32c"
    assert receipt["verification"] == {
        "completed_at": "2026-09-15T00:00:00Z",
        "write_mode": "synchronous",
        "sha256_verified": True,
        "size_verified": True,
        "provider_checksum_verified": True,
        "generation_verified": True,
    }
    assert receipt["access"] == "private"
    assert transport.write_calls == 1
    assert transport.read_calls >= 1
    assert transport.head_calls >= 1
    assert store.verify_receipt(
        receipt,
        validator=validator,
        output_spec=request["work_items"][0]["output_spec"] | {"duration": "8s"},
    )
    assert transport.background_operations == 0


@pytest.mark.parametrize("corruption", ["bytes", "checksum", "metadata", "generation"])
def test_gcs_receipt_verification_fails_closed_on_any_durable_fact_mismatch(
    corruption, authorized_project, batch_request
):
    transport = FakeGCS()
    store = _gcs_store(authorized_project, transport)
    request = _cloud_request(batch_request)
    output = store.attempt_output_path("item-001", "attempt-000001", "clip.mp4")
    store.prepare_attempt_directory(output)
    output.write_bytes(fake_video_bytes())
    validator = DeterministicFakeMediaValidator()
    output_spec = request["work_items"][0]["output_spec"] | {"duration": "8s"}
    facts = validator.validate(output, output_spec)
    receipt = store.put_verified_blob(
        source=output,
        logical_path=output.relative_to(authorized_project["project_dir"]).as_posix(),
        batch_id=request["batch_id"],
        item_id="item-001",
        attempt_id="attempt-000001",
        output=facts,
        created_at="2026-09-15T00:00:00Z",
    )
    if corruption == "generation":
        receipt = deepcopy(receipt)
        receipt["generation"] += 1
    else:
        transport.corrupt(receipt["locator"], corruption)

    with pytest.raises(M1ExecutionError, match="REUSE_RECEIPT_INVALID"):
        store.verify_receipt(receipt, validator=validator, output_spec=output_spec)


def test_gcs_conditional_create_race_reuses_only_exact_bytes_and_metadata(
    authorized_project, batch_request
):
    transport = FakeGCS()
    first = _gcs_store(authorized_project, transport)
    second = _gcs_store(authorized_project, transport)
    request = _cloud_request(batch_request)
    output = first.attempt_output_path("item-001", "attempt-000001", "clip.mp4")
    first.prepare_attempt_directory(output)
    output.write_bytes(fake_video_bytes())
    validator = DeterministicFakeMediaValidator()
    output_spec = request["work_items"][0]["output_spec"] | {"duration": "8s"}
    facts = validator.validate(output, output_spec)
    kwargs = {
        "source": output,
        "logical_path": output.relative_to(authorized_project["project_dir"]).as_posix(),
        "batch_id": request["batch_id"],
        "item_id": "item-001",
        "attempt_id": "attempt-000001",
        "output": facts,
        "created_at": "2026-09-15T00:00:00Z",
    }

    first_receipt = first.put_verified_blob(**kwargs)
    second_receipt = second.put_verified_blob(**kwargs)
    assert second_receipt["generation"] == first_receipt["generation"]
    assert transport.successful_creates == 1

    transport.corrupt(first_receipt["locator"], "metadata")
    with pytest.raises(StorageConflict, match="GCS_PRECONDITION_CONFLICT"):
        second.put_verified_blob(**kwargs)


def test_gcs_materialization_must_remain_in_project_hidden_tree(
    authorized_project, batch_request, tmp_path
):
    transport = FakeGCS()
    store = _gcs_store(authorized_project, transport)
    request = _cloud_request(batch_request)
    output = store.attempt_output_path("item-001", "attempt-000001", "clip.mp4")
    store.prepare_attempt_directory(output)
    output.write_bytes(fake_video_bytes())
    validator = DeterministicFakeMediaValidator()
    output_spec = request["work_items"][0]["output_spec"] | {"duration": "8s"}
    facts = validator.validate(output, output_spec)
    receipt = store.put_verified_blob(
        source=output,
        logical_path=output.relative_to(authorized_project["project_dir"]).as_posix(),
        batch_id=request["batch_id"],
        item_id="item-001",
        attempt_id="attempt-000001",
        output=facts,
        created_at="2026-09-15T00:00:00Z",
    )

    with pytest.raises(M1ExecutionError, match="WORKSPACE_ESCAPE"):
        store.get_verified_blob(receipt, tmp_path / "detached.mp4")
    destination = store.run_dir / "verified" / "item-001.mp4"
    assert store.get_verified_blob(receipt, destination) == destination
    assert destination.read_bytes() == output.read_bytes()


def test_gcs_store_mutations_are_coordinator_thread_only(
    authorized_project, batch_request
):
    store = _gcs_store(authorized_project, FakeGCS())
    request = _cloud_request(batch_request)
    errors = []

    def mutate_from_worker():
        try:
            store.write_request_if_absent(request)
        except BaseException as exc:
            errors.append(exc)

    worker = threading.Thread(target=mutate_from_worker)
    worker.start()
    worker.join(timeout=5)
    assert not worker.is_alive()
    assert len(errors) == 1
    assert getattr(errors[0], "code", None) == "COORDINATOR_WRITER_REQUIRED"
    assert store.load_result() is None
