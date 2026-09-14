from __future__ import annotations

import hashlib
import json
import shutil
import threading
from copy import deepcopy

import pytest

from backlot.state import load_board_state
from lib.batch_executor.contracts import (
    canonical_json_bytes,
    canonical_sha256,
    freeze_batch_request,
    freeze_publication_authorization,
    freeze_publication_command,
)
from lib.batch_executor.engine import CloudBatchExecutor
from lib.batch_executor.errors import InjectedCrash, M2PublicationError, StorageConflict
from lib.batch_executor.fake_gcs import FakeGCS
from lib.batch_executor.gcs_storage import GCSStore
from lib.batch_executor.media_validation import DeterministicFakeMediaValidator
from lib.batch_executor.ownership import freeze_execution_status_evidence
from lib.batch_executor.publication import CloudAssetsPublisher, LocalAssetsPublisher
from lib.batch_executor.runtime import CloudInvocationIdentity
from lib.batch_executor.storage import LocalStore
from lib.batch_executor.testing import FakeClock, ScriptedFakeProvider
from lib.checkpoint import read_checkpoint, write_checkpoint
from tests.batch_executor.test_m2_publication import _agent_command, _human_command


BUCKET = "private-batch-bucket"
SOURCE_EXECUTION = (
    "projects/cloud-project/locations/us-central1/jobs/batch-v2/executions/source"
)


class FakeADCStatusVerifier:
    verifier_id = "cloud_run_control_plane_adc"

    def __init__(self, owner, *, status="terminal"):
        self.calls = 0
        self.evidence = freeze_execution_status_evidence(
            {
                "version": "1.0",
                "evidence_id": "cloud-publication-source-stopped",
                "batch_id": owner["batch_id"],
                "request_digest": owner["request_digest"],
                "prior_invocation_id": owner["invocation_id"],
                "prior_execution_id": owner["execution_id"],
                "observed_status": status,
                "observed_at": "2026-09-14T09:58:00Z",
                "verifier": self.verifier_id,
                "execution_resource": owner["execution_id"],
            }
        )

    def verify_stopped(self, recorded_owner):
        self.calls += 1
        assert recorded_owner["execution_id"] == self.evidence["execution_resource"]
        return deepcopy(self.evidence)


def _identity(name: str) -> CloudInvocationIdentity:
    return CloudInvocationIdentity(
        invocation_id=name,
        execution_resource=(
            "projects/cloud-project/locations/us-central1/jobs/batch-v2/"
            f"executions/{name}"
        ),
        task_id="0",
        mode="run",
    )


def _make_cloud_publication_case(
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
    *,
    storage_profile="cloud_run",
):
    request = deepcopy(batch_request)
    request["execution_policy"]["storage_profile"] = storage_profile
    request = freeze_batch_request(request)
    transport = FakeGCS()
    provider = ScriptedFakeProvider()

    def store_factory(project_dir, batch_id):
        return GCSStore(
            project_dir,
            batch_id,
            bucket=BUCKET,
            transport=transport,
        )

    result = CloudBatchExecutor(
        projects_root=authorized_project["projects_root"],
        provider=provider,
        media_validator=DeterministicFakeMediaValidator(),
        clock=FakeClock(),
        store_factory=store_factory,
    ).run(
        request,
        observed_source_revision=source_revision,
        adapter_observation=qualified_adapter_observation,
        trusted_invocation=CloudInvocationIdentity(
            invocation_id="cloud-source",
            execution_resource=SOURCE_EXECUTION,
            task_id="0",
            mode="run",
        ),
    )
    gcs_store = store_factory(
        authorized_project["project_dir"], request["batch_id"]
    )
    durable_request, request_generation = gcs_store.load_request()
    state, state_generation = gcs_store.load_batch_state()
    loaded_result = gcs_store.load_result()
    assert loaded_result is not None
    durable_result, result_generation = loaded_result
    assert durable_request == request
    assert durable_result == result
    local_store = LocalStore(
        authorized_project["project_dir"], request["batch_id"]
    )
    cloud_source = {
        "bucket": BUCKET,
        "request": {
            "logical_path": f".batch-v2/runs/{request['batch_id']}/request.json",
            "object_name": gcs_store.request_object_name,
            "generation": request_generation,
            "sha256": canonical_sha256(request),
        },
        "state": {
            "logical_path": f".batch-v2/runs/{request['batch_id']}/state.json",
            "object_name": gcs_store.state_object_name,
            "generation": state_generation,
            "sha256": canonical_sha256(state),
        },
        "result": {
            "logical_path": f".batch-v2/runs/{request['batch_id']}/result.json",
            "object_name": gcs_store.result_object_name,
            "generation": result_generation,
            "sha256": canonical_sha256(result),
        },
    }
    return {
        **authorized_project,
        "request": request,
        "result": result,
        "result_digest": canonical_sha256(result),
        "state": state,
        "state_revision": state["revision"],
        "store": local_store,
        "gcs_store": gcs_store,
        "cloud_source": cloud_source,
        "transport": transport,
        "provider": provider,
    }


@pytest.fixture()
def cloud_publication_case(
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
):
    return _make_cloud_publication_case(
        batch_request,
        authorized_project,
        source_revision,
        qualified_adapter_observation,
    )


def _publisher(case, *, verifier=None, crash_hook=None, allow_portable_fake=False):
    return CloudAssetsPublisher(
        projects_root=case["projects_root"],
        bucket=BUCKET,
        transport=case["transport"],
        media_validator=DeterministicFakeMediaValidator(),
        execution_status_verifier=verifier,
        crash_hook=crash_hook,
        allow_portable_fake=allow_portable_fake,
    )


def test_cloud_agent_publication_is_explicit_data_first_and_checkpoint_last(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    receipt = _publisher(case, verifier=verifier).publish(
        command, trusted_invocation=_identity("publication-agent")
    )

    checkpoint = read_checkpoint(
        case["projects_root"], case["project_id"], "assets"
    )
    assert checkpoint is not None
    assert checkpoint["status"] == "awaiting_human"
    assert checkpoint["human_approved"] is False
    assert checkpoint["artifacts"]["asset_manifest"] == command["asset_manifest"]
    assert receipt["status"] == "awaiting_human"
    assert receipt["publication_state_generation"] >= 1
    assert verifier.calls == 1
    assert case["provider"].submit_calls == 1
    assert case["transport"].background_operations == 0
    assert (case["project_dir"] / "assets/video/asset-1.mp4").is_file()
    names = case["transport"].object_names(BUCKET)
    assert case["gcs_store"].publication_command_object_name(
        command["command_id"]
    ) in names
    assert "projects/batch-project/assets/video/asset-1.mp4" in names
    assert "projects/batch-project/checkpoint_assets.json" in names
    publication_state, publication_generation = (
        case["gcs_store"].load_publication_state()
    )
    assert publication_generation == receipt["publication_state_generation"]
    assert publication_state["owner"]["owner_status"] == "completed"
    assert publication_state["owner"]["command_digest"] == command["command_digest"]
    assert publication_state["completed_commands"][0]["transition"] == (
        "agent_review_to_awaiting_human"
    )
    assert any("/ownership-evidence/" in name for name in names)
    checkpoint_bytes = (case["project_dir"] / "checkpoint_assets.json").read_bytes()
    checkpoint_object = case["transport"].read_object(
        bucket=BUCKET,
        name="projects/batch-project/checkpoint_assets.json",
        generation=receipt["checkpoint_generation"],
    )
    assert checkpoint_object.data == checkpoint_bytes
    assert checkpoint_object.size_bytes == len(checkpoint_bytes)
    assert checkpoint_object.metadata["command_digest"] == command["command_digest"]
    assert checkpoint_object.metadata["client_sha256"] == hashlib.sha256(
        checkpoint_bytes
    ).hexdigest()
    assert checkpoint_object.metadata["checkpoint_sha256"] == canonical_sha256(
        checkpoint
    )


def test_cloud_checkpoint_manifest_overrides_stale_loose_backlot_cache(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    _publisher(
        case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
    ).publish(command, trusted_invocation=_identity("publication-backlot"))
    loose = {
        "version": "1.0",
        "assets": [
            {
                "id": "stale-cloud-cache",
                "type": "video",
                "path": "assets/video/stale-cloud-cache.mp4",
                "source_tool": "legacy",
                "scene_id": "stale-cloud-scene",
            }
        ],
    }
    loose_path = case["project_dir"] / "artifacts" / "asset_manifest.json"
    loose_path.write_text(json.dumps(loose), encoding="utf-8")

    board = load_board_state(case["project_dir"])
    assert board["artifacts"]["asset_manifest"] == command["asset_manifest"]
    assert {
        "artifact": "asset_manifest",
        "status": "cache_mismatch_ignored",
        "reason": "validated Batch V2 checkpoint_assets.json remains authoritative",
    } in board["artifact_diagnostics"]


def test_cloud_publication_suppresses_legacy_checkpoint_sync_and_restores_it(
    cloud_publication_case, monkeypatch
):
    import lib.gcs_storage

    case = cloud_publication_case
    scheduled = []
    monkeypatch.setattr(
        lib.gcs_storage.gcs_storage, "is_auto_sync_enabled", lambda: True
    )
    monkeypatch.setattr(
        lib.gcs_storage.gcs_storage,
        "async_sync_project_assets",
        lambda project_dir: scheduled.append(project_dir),
    )
    command = _agent_command(case)
    _publisher(
        case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
    ).publish(command, trusted_invocation=_identity("publication-hidden-writer"))
    checkpoint_path = case["project_dir"] / "checkpoint_assets.json"
    returned_bytes = checkpoint_path.read_bytes()
    assert scheduled == []
    assert checkpoint_path.read_bytes() == returned_bytes

    write_checkpoint(
        case["projects_root"],
        case["project_id"],
        "assets",
        "awaiting_human",
        {"asset_manifest": command["asset_manifest"]},
        pipeline_type=case["pipeline_type"],
    )
    assert scheduled == [case["project_dir"]]


def test_local_publisher_stays_local_only_and_cloud_requires_external_proof(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    with pytest.raises(M2PublicationError, match="M2_LOCAL_ONLY"):
        LocalAssetsPublisher(
            projects_root=case["projects_root"],
            media_validator=DeterministicFakeMediaValidator(),
        ).publish(command)
    with pytest.raises(M2PublicationError, match="PUBLICATION_STOP_PROOF_REQUIRED"):
        _publisher(case).publish(
            command, trusted_invocation=_identity("publication-no-proof")
        )
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()
    assert not (case["project_dir"] / "assets/video/asset-1.mp4").exists()


def test_cloud_publisher_rejects_caller_json_and_unsafe_invocation_identity(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    publisher = _publisher(
        case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
    )
    with pytest.raises(M2PublicationError, match="PUBLICATION_INVOCATION_INVALID"):
        publisher.publish(command, trusted_invocation={"invocation_id": "caller"})
    unsafe = CloudInvocationIdentity(
        invocation_id="../unsafe",
        execution_resource="caller-status-json",
        task_id="0",
        mode="run",
    )
    with pytest.raises(M2PublicationError, match="PUBLICATION_INVOCATION_INVALID"):
        publisher.publish(command, trusted_invocation=unsafe)
    assert case["gcs_store"].publication_state_object_name not in (
        case["transport"].object_names(BUCKET)
    )


def test_portable_profile_is_allowed_only_for_explicit_offline_fake_qualification(
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
):
    case = _make_cloud_publication_case(
        batch_request,
        authorized_project,
        source_revision,
        qualified_adapter_observation,
        storage_profile="portable",
    )
    command = _agent_command(case)
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    with pytest.raises(M2PublicationError, match="CLOUD_PUBLICATION_PROFILE_INVALID"):
        _publisher(case, verifier=verifier).publish(
            command, trusted_invocation=_identity("portable-not-qualified")
        )
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()

    result = _publisher(
        case, verifier=verifier, allow_portable_fake=True
    ).publish(command, trusted_invocation=_identity("portable-fake-qualified"))
    assert result["status"] == "awaiting_human"


@pytest.mark.parametrize(
    ("mutation", "error"),
    [
        (lambda value: value["cloud_source"].update(bucket="another-bucket"), "BUCKET"),
        (
            lambda value: value["cloud_source"]["state"].update(generation=999),
            "GENERATION",
        ),
        (
            lambda value: value["asset_bindings"][0].update(
                source_locator="gs://another-bucket/foreign"
            ),
            "ASSET_RESULT_BINDING_INVALID",
        ),
    ],
)
def test_cloud_source_and_receipt_authority_mismatch_fail_before_canonical_mutation(
    cloud_publication_case, mutation, error
):
    case = cloud_publication_case
    command = deepcopy(_agent_command(case))
    mutation(command)
    command = freeze_publication_command(command)
    with pytest.raises(M2PublicationError, match=error):
        _publisher(
            case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
        ).publish(command, trusted_invocation=_identity("publication-bad-binding"))
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()
    assert not (case["project_dir"] / "assets/video/asset-1.mp4").exists()


@pytest.mark.parametrize(
    "boundary",
    [
        "cloud_publication_claim_acquired",
        "cloud_publication_command_mirrored",
        "cloud_publication_blob_staged",
        "cloud_publication_asset_materialized",
        "cloud_publication_assets_gcs_verified",
        "cloud_publication_checkpoint_written",
        "cloud_publication_checkpoint_gcs_verified",
        "cloud_publication_state_completed",
    ],
)
def test_cloud_publication_repairs_each_ordered_crash_boundary(
    cloud_publication_case, boundary
):
    case = cloud_publication_case
    command = _agent_command(case)
    identity = _identity(f"repair-{boundary.replace('_', '-')}")
    fired = False

    def crash(name, _facts):
        nonlocal fired
        if name == boundary and not fired:
            fired = True
            raise InjectedCrash(name)

    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    with pytest.raises(InjectedCrash, match=boundary):
        _publisher(case, verifier=verifier, crash_hook=crash).publish(
            command, trusted_invocation=identity
        )
    if boundary in {
        "cloud_publication_claim_acquired",
        "cloud_publication_command_mirrored",
        "cloud_publication_blob_staged",
        "cloud_publication_asset_materialized",
        "cloud_publication_assets_gcs_verified",
    }:
        assert not (case["project_dir"] / "checkpoint_assets.json").exists()

    repaired = _publisher(case, verifier=verifier).publish(
        command, trusted_invocation=identity
    )
    assert repaired["status"] == "awaiting_human"
    assert read_checkpoint(
        case["projects_root"], case["project_id"], "assets"
    )["status"] == "awaiting_human"


def test_cloud_human_gate_requires_later_exact_command_and_replay_is_idempotent(
    cloud_publication_case,
):
    case = cloud_publication_case
    first = _agent_command(case)
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    publisher = _publisher(case, verifier=verifier)
    first_receipt = publisher.publish(
        first, trusted_invocation=_identity("publication-agent-first")
    )
    human = _human_command(case, first, first_receipt)
    completed = publisher.publish(
        human, trusted_invocation=_identity("publication-human-second")
    )
    replay = publisher.publish(
        human, trusted_invocation=_identity("publication-human-replay")
    )

    assert completed["status"] == replay["status"] == "completed"
    assert completed["human_approved"] is replay["human_approved"] is True
    assert replay["idempotent"] is True


@pytest.mark.parametrize(
    "boundary",
    [
        "cloud_publication_checkpoint_written",
        "cloud_publication_checkpoint_gcs_verified",
    ],
)
def test_cloud_human_transition_repairs_checkpoint_crash_boundaries(
    cloud_publication_case, boundary
):
    case = cloud_publication_case
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    first = _agent_command(case)
    suffix = "written" if boundary.endswith("written") else "synced"
    first_receipt = _publisher(case, verifier=verifier).publish(
        first, trusted_invocation=_identity(f"human-crash-first-{suffix}")
    )
    human = _human_command(case, first, first_receipt)
    identity = _identity(f"human-crash-second-{suffix}")
    fired = False

    def crash(name, _facts):
        nonlocal fired
        if name == boundary and not fired:
            fired = True
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash, match=boundary):
        _publisher(case, verifier=verifier, crash_hook=crash).publish(
            human, trusted_invocation=identity
        )
    repaired = _publisher(case, verifier=verifier).publish(
        human, trusted_invocation=identity
    )
    assert repaired["status"] == "completed"
    assert repaired["human_approved"] is True


def _publication_authorization(
    case,
    command,
    identity,
    *,
    authorization_id="pub-auth-1",
    prior_owner=None,
    scope="source_execution",
):
    owner = prior_owner or case["state"]["owner"]
    return freeze_publication_authorization(
        {
            "version": "1.0",
            "canonical_json": "openmontage-canonical-json-v1",
            "authorization_id": authorization_id,
            "authorization_digest": "0" * 64,
            "authorized_at": "2026-09-14T10:01:00Z",
            "scope": scope,
            "batch_id": command["batch_id"],
            "request_digest": command["request_digest"],
            "prior_invocation_id": owner["invocation_id"],
            "prior_execution_id": owner["execution_id"],
            "prior_task_id": owner["task_id"],
            "intended_publication_invocation_id": identity.invocation_id,
            "intended_publication_execution_id": identity.execution_resource,
            "intended_publication_task_id": identity.task_id,
            "command_id": command["command_id"],
            "command_digest": command["command_digest"],
            "source_state_generation": command["cloud_source"]["state"][
                "generation"
            ],
            "source_state_sha256": command["state_ref"]["sha256"],
            "reason": "Explicitly authorize this exact stopped execution publication.",
            "decision_reference": "user-reply:cloud-publication-1",
        }
    )


def test_exact_one_time_human_publication_authorization_can_replace_verifier(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    identity = _identity("publication-human-authorized")
    authorization = _publication_authorization(case, command, identity)
    result = _publisher(case).publish(
        command,
        trusted_invocation=identity,
        publication_authorization=authorization,
    )
    assert result["status"] == "awaiting_human"

    with pytest.raises(M2PublicationError, match="PUBLICATION_AUTHORIZATION_REPLAY"):
        _publisher(case).publish(
            command,
            trusted_invocation=_identity("publication-another"),
            publication_authorization=authorization,
        )


def test_stale_or_corrupt_source_bytes_fail_before_claim_or_canonical_mutation(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    case["transport"].corrupt(
        case["result"]["items"][0]["storage_receipt"]["locator"], "checksum"
    )
    with pytest.raises(M2PublicationError, match="GCS_RECEIPT_INVALID"):
        _publisher(
            case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
    ).publish(command, trusted_invocation=_identity("publication-corrupt"))
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()
    assert not (case["project_dir"] / "assets/video/asset-1.mp4").exists()


def _publication_owner_for_proof(case, publication_state):
    owner = publication_state["owner"]
    return {
        "batch_id": case["request"]["batch_id"],
        "request_digest": case["request"]["request_digest"],
        "invocation_id": owner["invocation_id"],
        "execution_id": owner["execution_id"],
        "task_id": owner["task_id"],
    }


def test_new_process_repairs_crashed_claim_only_after_exact_publication_stop_proof(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    first_identity = _identity("publication-process-crashed")

    def crash(name, _facts):
        if name == "cloud_publication_asset_materialized":
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        _publisher(
            case,
            verifier=FakeADCStatusVerifier(case["state"]["owner"]),
            crash_hook=crash,
        ).publish(command, trusted_invocation=first_identity)
    active, _ = case["gcs_store"].load_publication_state()
    assert active["owner"]["owner_status"] == "active"

    with pytest.raises(
        M2PublicationError, match="EXECUTION_STATUS_VERIFICATION_FAILED"
    ):
        _publisher(
            case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
        ).publish(
            command, trusted_invocation=_identity("publication-wrong-takeover-proof")
        )

    successor = _identity("publication-process-successor")
    prior_publication_owner = _publication_owner_for_proof(case, active)
    result = _publisher(
        case, verifier=FakeADCStatusVerifier(prior_publication_owner)
    ).publish(command, trusted_invocation=successor)
    assert result["status"] == "awaiting_human"
    completed, _ = case["gcs_store"].load_publication_state()
    assert completed["owner"]["invocation_id"] == successor.invocation_id
    assert completed["owner"]["proof"]["scope"] == "publication_takeover"
    assert case["provider"].submit_calls == 1


def test_new_process_can_repair_with_one_time_bound_human_takeover_authorization(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    first_identity = _identity("publication-human-takeover-crashed")

    def crash(name, _facts):
        if name == "cloud_publication_claim_acquired":
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        _publisher(
            case,
            verifier=FakeADCStatusVerifier(case["state"]["owner"]),
            crash_hook=crash,
        ).publish(command, trusted_invocation=first_identity)
    active, _ = case["gcs_store"].load_publication_state()
    successor = _identity("publication-human-takeover-successor")
    authorization = _publication_authorization(
        case,
        command,
        successor,
        authorization_id="pub-takeover-auth-1",
        prior_owner=_publication_owner_for_proof(case, active),
        scope="publication_takeover",
    )
    result = _publisher(case).publish(
        command,
        trusted_invocation=successor,
        publication_authorization=authorization,
    )
    assert result["status"] == "awaiting_human"
    completed, _ = case["gcs_store"].load_publication_state()
    assert authorization["authorization_digest"] in completed[
        "consumed_authorization_digests"
    ]
    assert completed["owner"]["proof"]["scope"] == "publication_takeover"


def test_cloud_publication_command_binds_exact_full_source_bytes_and_generations(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    assert command["cloud_source"]["request"]["sha256"] == canonical_sha256(
        case["request"]
    )
    assert command["cloud_source"]["state"]["sha256"] == canonical_sha256(
        case["state"]
    )
    assert command["cloud_source"]["result"]["sha256"] == canonical_sha256(
        case["result"]
    )
    assert canonical_json_bytes(command)


def test_cloud_publication_staging_symlink_cannot_escape_project_hidden_tree(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    staging_item = (
        case["project_dir"]
        / ".batch-v2"
        / "runs"
        / command["batch_id"]
        / "publication"
        / "staging"
        / command["command_id"]
        / "item-001"
    )
    staging_item.parent.mkdir(parents=True, exist_ok=True)
    escape = case["project_dir"] / "assets" / "video"
    escape.mkdir(parents=True, exist_ok=True)
    try:
        staging_item.symlink_to(escape, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlink creation is unavailable on this platform")

    with pytest.raises(M2PublicationError, match="GCS_RECEIPT_INVALID"):
        _publisher(
            case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
        ).publish(command, trusted_invocation=_identity("staging-symlink"))
    assert case["gcs_store"].load_publication_state() is None
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()
    assert not (escape / "source.mp4").exists()


@pytest.mark.parametrize("corruption", ["bytes", "checksum", "metadata"])
def test_every_gcs_receipt_corruption_fails_before_claim(
    cloud_publication_case, corruption
):
    case = cloud_publication_case
    command = _agent_command(case)
    case["transport"].corrupt(
        case["result"]["items"][0]["storage_receipt"]["locator"], corruption
    )
    with pytest.raises(M2PublicationError, match="GCS_RECEIPT_INVALID"):
        _publisher(
            case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
        ).publish(command, trusted_invocation=_identity(f"corrupt-{corruption}"))
    names = case["transport"].object_names(BUCKET)
    assert case["gcs_store"].publication_state_object_name not in names
    assert not any("/publication/commands/" in name for name in names)
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()


def _rewrite_receipt_authority(case, mutation):
    result = deepcopy(case["result"])
    state = deepcopy(case["state"])
    mutation(result["items"][0]["storage_receipt"])
    mutation(state["storage_receipts"][0])

    result_payload = canonical_json_bytes(result)
    old_result_generation = case["cloud_source"]["result"]["generation"]
    result_snapshot = case["transport"].write_object(
        bucket=BUCKET,
        name=case["gcs_store"].result_object_name,
        data=result_payload,
        metadata=case["gcs_store"]._record_metadata(
            "batch_result",
            canonical_sha256(result),
            request_digest=result["request_digest"],
        ),
        content_type="application/json",
        if_generation_match=old_result_generation,
    )
    state["result_ref"]["sha256"] = canonical_sha256(result)
    state["revision"] += 1
    state["owner"]["state_revision"] += 1
    old_state_generation = case["cloud_source"]["state"]["generation"]
    state_generation = case["gcs_store"].save_batch_state(
        state, expected_version=old_state_generation
    )
    case["result"] = result
    case["result_digest"] = canonical_sha256(result)
    case["state"] = state
    case["state_revision"] = state["revision"]
    case["cloud_source"]["result"].update(
        generation=result_snapshot.generation,
        sha256=canonical_sha256(result),
    )
    case["cloud_source"]["state"].update(
        generation=state_generation,
        sha256=canonical_sha256(state),
    )


@pytest.mark.parametrize(
    ("kind", "error"),
    [
        ("store", "ASSET_RESULT_BINDING_INVALID"),
        ("bucket", "GCS_RECEIPT_INVALID"),
        ("generation", "GCS_RECEIPT_INVALID"),
    ],
)
def test_wrong_receipt_store_bucket_or_generation_never_claims_or_publishes(
    cloud_publication_case, kind, error
):
    case = cloud_publication_case

    def mutate(receipt):
        if kind == "store":
            receipt["store_type"] = "local"
            receipt["locator"] = (
                f".batch-v2/blobs/sha256/{receipt['sha256'][:2]}/{receipt['sha256']}"
            )
            receipt.pop("generation")
            receipt.pop("provider_checksum")
            receipt["verification"]["provider_checksum_verified"] = False
            receipt["verification"]["generation_verified"] = False
        elif kind == "bucket":
            receipt["locator"] = receipt["locator"].replace(
                f"gs://{BUCKET}/", "gs://another-private-bucket/", 1
            )
        else:
            receipt["generation"] += 1000

    _rewrite_receipt_authority(case, mutate)
    command = _agent_command(case)
    with pytest.raises(M2PublicationError, match=error):
        _publisher(
            case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
        ).publish(command, trusted_invocation=_identity(f"bad-receipt-{kind}"))
    assert case["gcs_store"].publication_state_object_name not in (
        case["transport"].object_names(BUCKET)
    )
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()
    assert not (case["project_dir"] / "assets/video/asset-1.mp4").exists()


def test_untrusted_or_wrongly_bound_status_evidence_cannot_claim(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    verifier.verifier_id = "caller_supplied_json"
    with pytest.raises(M2PublicationError, match="UNTRUSTED_EXECUTION_EVIDENCE"):
        _publisher(case, verifier=verifier).publish(
            command, trusted_invocation=_identity("caller-status")
        )

    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    verifier.evidence["prior_invocation_id"] = "another-invocation"
    with pytest.raises(
        M2PublicationError,
        match="(?:EXECUTION_STATUS_VERIFICATION_FAILED|PUBLICATION_STOP_PROOF_MISMATCH)",
    ):
        _publisher(case, verifier=verifier).publish(
            command, trusted_invocation=_identity("wrong-status")
        )
    assert case["gcs_store"].publication_state_object_name not in (
        case["transport"].object_names(BUCKET)
    )


def test_concurrent_publishers_have_one_cas_winner_and_loser_mutates_no_canonical(
    cloud_publication_case,
):
    case = cloud_publication_case
    replica_root = case["projects_root"] / "replica-projects"
    replica_root.mkdir()
    replica_project = replica_root / case["project_id"]
    shutil.copytree(case["project_dir"], replica_project)

    first = _agent_command(case, command_id="publish-race-a")
    second = deepcopy(first)
    second["command_id"] = "publish-race-b"
    second = freeze_publication_command(second)
    barrier = threading.Barrier(2)

    def before_write(_bucket, name, expected_generation):
        if name.endswith("/publication/state.json") and expected_generation == 0:
            barrier.wait(timeout=5)

    case["transport"].before_write = before_write
    outcomes = []
    failures = []

    def invoke(root, command, invocation):
        try:
            result = CloudAssetsPublisher(
                projects_root=root,
                bucket=BUCKET,
                transport=case["transport"],
                media_validator=DeterministicFakeMediaValidator(),
                execution_status_verifier=FakeADCStatusVerifier(
                    case["state"]["owner"]
                ),
            ).publish(command, trusted_invocation=_identity(invocation))
            outcomes.append((root, result))
        except BaseException as exc:
            failures.append((root, exc))

    threads = [
        threading.Thread(
            target=invoke,
            args=(case["projects_root"], first, "publication-race-a"),
        ),
        threading.Thread(
            target=invoke,
            args=(replica_root, second, "publication-race-b"),
        ),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=15)
    case["transport"].before_write = None

    assert all(not thread.is_alive() for thread in threads)
    assert len(outcomes) == len(failures) == 1
    assert isinstance(failures[0][1], M2PublicationError)
    assert failures[0][1].code == "PUBLICATION_CLAIM_CONFLICT"
    winning_root = outcomes[0][0]
    losing_root = failures[0][0]
    assert (winning_root / case["project_id"] / "checkpoint_assets.json").is_file()
    assert not (losing_root / case["project_id"] / "checkpoint_assets.json").exists()
    assert not (losing_root / case["project_id"] / "assets/video/asset-1.mp4").exists()


def test_canonical_gcs_precondition_conflict_never_overwrites_foreign_object(
    cloud_publication_case,
):
    case = cloud_publication_case
    name = "projects/batch-project/assets/video/asset-1.mp4"
    foreign = case["transport"].write_object(
        bucket=BUCKET,
        name=name,
        data=b"foreign-canonical-bytes",
        metadata={"record_type": "foreign"},
        content_type="video/mp4",
        if_generation_match=0,
    )
    command = _agent_command(case)
    with pytest.raises(StorageConflict, match="GCS_PRECONDITION_CONFLICT"):
        _publisher(
            case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
        ).publish(command, trusted_invocation=_identity("canonical-conflict"))
    current = case["transport"].read_object(bucket=BUCKET, name=name)
    assert current.generation == foreign.generation
    assert current.data == b"foreign-canonical-bytes"
    assert case["gcs_store"].publication_state_object_name not in (
        case["transport"].object_names(BUCKET)
    )
    assert not (case["project_dir"] / "assets/video/asset-1.mp4").exists()
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()


def test_checkpoint_gcs_precondition_conflict_never_overwrites_foreign_object(
    cloud_publication_case,
):
    case = cloud_publication_case
    name = "projects/batch-project/checkpoint_assets.json"
    foreign = case["transport"].write_object(
        bucket=BUCKET,
        name=name,
        data=b'{"foreign":true}',
        metadata={"record_type": "foreign"},
        content_type="application/json",
        if_generation_match=0,
    )
    command = _agent_command(case)
    with pytest.raises(StorageConflict, match="GCS_PRECONDITION_CONFLICT"):
        _publisher(
            case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
        ).publish(command, trusted_invocation=_identity("checkpoint-conflict"))
    current = case["transport"].read_object(bucket=BUCKET, name=name)
    assert current.generation == foreign.generation
    assert current.data == b'{"foreign":true}'
    assert case["gcs_store"].load_publication_state() is None
    assert not (case["project_dir"] / "assets/video/asset-1.mp4").exists()
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()


def test_completion_state_cas_conflict_is_repairable_without_republishing_provider(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    identity = _identity("completion-cas-repair")
    injected = False

    def race_after_sync(name, _facts):
        nonlocal injected
        if name != "cloud_publication_checkpoint_gcs_verified" or injected:
            return
        injected = True
        state, generation = case["gcs_store"].load_publication_state()
        payload = canonical_json_bytes(state)
        case["transport"].write_object(
            bucket=BUCKET,
            name=case["gcs_store"].publication_state_object_name,
            data=payload,
            metadata=case["gcs_store"]._record_metadata(
                "publication_state",
                canonical_sha256(state),
                request_digest=state["request_digest"],
                logical_revision=str(state["revision"]),
            ),
            content_type="application/json",
            if_generation_match=generation,
        )

    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    with pytest.raises(M2PublicationError, match="PUBLICATION_COMPLETION_CONFLICT"):
        _publisher(case, verifier=verifier, crash_hook=race_after_sync).publish(
            command, trusted_invocation=identity
        )
    calls_after_conflict = case["provider"].submit_calls
    repaired = _publisher(case, verifier=verifier).publish(
        command, trusted_invocation=identity
    )
    assert repaired["status"] == "awaiting_human"
    assert case["provider"].submit_calls == calls_after_conflict == 1


def test_changed_human_command_cannot_replay_prior_human_gate_evidence(
    cloud_publication_case,
):
    case = cloud_publication_case
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    publisher = _publisher(case, verifier=verifier)
    first = _agent_command(case)
    first_receipt = publisher.publish(
        first, trusted_invocation=_identity("human-replay-first")
    )
    human = _human_command(case, first, first_receipt)
    publisher.publish(human, trusted_invocation=_identity("human-replay-complete"))

    changed = deepcopy(human)
    changed["command_id"] = "publish-human-replayed-evidence"
    changed["created_at"] = "2026-09-14T10:06:00Z"
    changed = freeze_publication_command(changed)
    with pytest.raises(M2PublicationError, match="HUMAN_APPROVAL_BINDING_INVALID"):
        publisher.publish(
            changed, trusted_invocation=_identity("human-replay-attempt")
        )


@pytest.mark.parametrize("reference", ["checkpoint", "command"])
def test_human_transition_rejects_wrong_prior_gcs_generation(
    cloud_publication_case, reference
):
    case = cloud_publication_case
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    publisher = _publisher(case, verifier=verifier)
    first = _agent_command(case)
    first_receipt = publisher.publish(
        first, trusted_invocation=_identity(f"prior-generation-{reference}")
    )
    human = deepcopy(_human_command(case, first, first_receipt))
    field = (
        "prior_checkpoint_ref"
        if reference == "checkpoint"
        else "prior_publication_command_ref"
    )
    human["transition"][field]["gcs_generation"] += 1
    human = freeze_publication_command(human)
    with pytest.raises(M2PublicationError, match="HUMAN_APPROVAL_BINDING_INVALID"):
        publisher.publish(
            human,
            trusted_invocation=_identity(f"wrong-prior-generation-{reference}"),
        )
    checkpoint = read_checkpoint(
        case["projects_root"], case["project_id"], "assets"
    )
    assert checkpoint["status"] == "awaiting_human"


def test_publication_authorization_exact_binding_is_fail_closed(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    identity = _identity("authorization-binding")
    authorization = deepcopy(_publication_authorization(case, command, identity))
    authorization["source_state_generation"] += 1
    authorization = freeze_publication_authorization(authorization)
    with pytest.raises(
        M2PublicationError, match="PUBLICATION_AUTHORIZATION_BINDING_INVALID"
    ):
        _publisher(case).publish(
            command,
            trusted_invocation=identity,
            publication_authorization=authorization,
        )
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()
