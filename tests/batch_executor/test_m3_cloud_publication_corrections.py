from __future__ import annotations

import hashlib
import json
import shutil
import threading
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from lib.batch_executor.contracts import (
    M0ContractError,
    canonical_json_bytes,
    canonical_sha256,
    freeze_batch_request,
    freeze_publication_command,
    load_execution_schema,
)
from lib.batch_executor.engine import CloudBatchExecutor
from lib.batch_executor.errors import InjectedCrash, M2PublicationError
from lib.batch_executor.gcs_storage import GCSObjectNotFound, GCSStore
from lib.batch_executor.media_validation import DeterministicFakeMediaValidator
from lib.batch_executor.publication import (
    CloudAssetsPublisher,
    _checkpoint_cost,
    _publication_metadata,
)
from lib.batch_executor.runtime import CloudInvocationIdentity
from lib.batch_executor.publication_cli import (
    PublicationRuntimeDependencies,
    freeze_publication_runtime_config,
    run_publication_cli,
)
from lib.batch_executor.identity import ADCContext
from lib.batch_executor.runtime import CloudRunExecutionStatus
from lib.batch_executor.storage import LocalStore
from lib.batch_executor.testing import FakeClock, ScriptedFakeProvider
from lib.batch_executor.workspace import materialize_project_snapshot
from lib.checkpoint import read_checkpoint, write_checkpoint
from tests.batch_executor.test_m3_cloud_publication import (
    BUCKET,
    FakeADCStatusVerifier,
    _agent_command,
    _human_command,
    _identity,
    _make_cloud_publication_case,
    _publication_authorization,
    _publication_owner_for_proof,
)


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


def _publisher(case, *, root=None, verifier=None, crash_hook=None):
    return CloudAssetsPublisher(
        projects_root=root or case["projects_root"],
        bucket=BUCKET,
        transport=case["transport"],
        media_validator=DeterministicFakeMediaValidator(),
        execution_status_verifier=verifier,
        crash_hook=crash_hook,
        allow_fake_status_verifier=True,
    )


def _copy_prepublication_project(case, destination_root: Path) -> Path:
    destination_root.mkdir(parents=True)
    destination = destination_root / case["project_id"]
    shutil.copytree(
        case["project_dir"],
        destination,
        ignore=shutil.ignore_patterns(".batch-v2", "checkpoint_assets.json"),
    )
    return destination


def _advance_publication_state_generation(case) -> None:
    """Model a concurrent valid journal CAS without changing canonical GCS data."""

    state, generation = case["gcs_store"].load_publication_state()
    advanced = deepcopy(state)
    advanced["revision"] += 1
    payload = canonical_json_bytes(advanced)
    case["transport"].write_object(
        bucket=BUCKET,
        name=case["gcs_store"].publication_state_object_name,
        data=payload,
        metadata=case["gcs_store"]._record_metadata(
            "publication_state",
            hashlib.sha256(payload).hexdigest(),
            request_digest=advanced["request_digest"],
            logical_revision=str(advanced["revision"]),
        ),
        content_type="application/json",
        if_generation_match=generation,
    )


def _publish_human_transition_in_concurrent_process_model(
    case, command, *, invocation_name: str
) -> int:
    """Use a fresh thread/context to model a separate publication process."""

    failures = []

    def publish_transition():
        try:
            _publisher(
                case,
                verifier=FakeADCStatusVerifier(case["state"]["owner"]),
            ).publish(command, trusted_invocation=_identity(invocation_name))
        except BaseException as exc:  # pragma: no cover - surfaced in caller
            failures.append(exc)

    thread = threading.Thread(target=publish_transition)
    thread.start()
    thread.join(timeout=10)
    if thread.is_alive():
        raise AssertionError("Concurrent Human transition did not finish")
    if failures:
        raise failures[0]
    return case["transport"].write_calls


def _production_root_config(case, tmp_path, command):
    command_generation, _ = case["gcs_store"].write_publication_command_if_absent(
        command
    )
    command_payload = canonical_json_bytes(command)
    snapshot_root = tmp_path / "publication-input" / "projects"
    _copy_prepublication_project(case, snapshot_root)
    workspace_root = (tmp_path / "publication-workspace" / "projects").resolve()
    reference = {
        "uri": (
            f"gs://{BUCKET}/"
            f"{case['gcs_store'].publication_command_object_name(command['command_id'])}"
        ),
        "generation": command_generation,
        "sha256": hashlib.sha256(command_payload).hexdigest(),
        "command_digest": command["command_digest"],
    }
    config = freeze_publication_runtime_config(
        {
            "version": "1.0",
            "config_digest": "0" * 64,
            "profile": "cloud_run_publication",
            "transport_mode": "offline_fake",
            "projects_root": str(workspace_root),
            "input_snapshot_projects_root": str(snapshot_root.resolve()),
            "input_snapshot_object_prefix": (
                "batch-v2-input-snapshots/sha256/" + "b" * 64
            ),
            "bucket": BUCKET,
            "storage_project": "explicit-storage-project",
            "cloud_run_project": "cloud-project",
            "cloud_run_location": "us-central1",
            "source_cloud_run_job": "batch-v2",
            "publication_cloud_run_job": "batch-v2-publish",
            "invocation_id": "production-root-publication",
            "command_ref": reference,
            "proof_kind": "control-plane",
            "authorization_ref": None,
        }
    )
    config_path = (tmp_path / "publication-runtime-config.json").resolve()
    config_path.write_bytes(canonical_json_bytes(config))
    argv = [
        "publish",
        "--config",
        str(config_path),
        "--command-uri",
        reference["uri"],
        "--command-generation",
        str(reference["generation"]),
        "--command-sha256",
        reference["sha256"],
        "--command-digest",
        reference["command_digest"],
    ]
    return config, argv, workspace_root


def test_separate_publication_composition_root_uses_concrete_verifier_offline(
    cloud_publication_case, tmp_path
):
    case = cloud_publication_case
    command = _agent_command(case)
    _, argv, workspace_root = _production_root_config(case, tmp_path, command)

    class FakeADC:
        def resolve(self, *, scopes):
            assert scopes
            return ADCContext(credentials=object(), detected_project="ignored")

    class FakeStatusTransport:
        calls = 0

        def get_execution_status(self, *, credentials, execution_resource):
            self.calls += 1
            assert credentials is not None
            assert execution_resource == case["state"]["owner"]["execution_id"]
            return CloudRunExecutionStatus(
                execution_resource=execution_resource,
                terminal_state="terminal",
                observed_at="2026-09-15T02:00:00Z",
            )

    status = FakeStatusTransport()
    emitted = []
    exit_code = run_publication_cli(
        argv,
        dependencies=PublicationRuntimeDependencies(
            environment={
                "CLOUD_RUN_JOB": "batch-v2-publish",
                "CLOUD_RUN_EXECUTION": "publish-execution-001",
                "CLOUD_RUN_TASK_INDEX": "0",
                "CLOUD_RUN_TASK_COUNT": "1",
                "CLOUD_RUN_TASK_ATTEMPT": "0",
            },
            credential_resolver=FakeADC(),
            gcs_transport=case["transport"],
            cloud_status_transport=status,
            media_validator=DeterministicFakeMediaValidator(),
            allow_offline_fake=True,
        ),
        emit=emitted.append,
    )
    assert exit_code == 0
    assert status.calls == 1
    assert json.loads(emitted[-1])["status"] == "awaiting_human"
    assert (workspace_root / case["project_id"] / "checkpoint_assets.json").is_file()
    assert (
        str(workspace_root).casefold()
        not in str((tmp_path / "publication-input" / "projects").resolve()).casefold()
    )


def test_publication_root_rejects_aliasing_snapshot_and_missing_bound_human_ref(
    cloud_publication_case, tmp_path
):
    case = cloud_publication_case
    command = _agent_command(case)
    config, argv, workspace_root = _production_root_config(case, tmp_path, command)
    aliased = deepcopy(config)
    aliased["input_snapshot_projects_root"] = str(workspace_root)
    aliased["config_digest"] = "0" * 64
    with pytest.raises(M0ContractError, match="WORKSPACE_SNAPSHOT_ALIAS"):
        freeze_publication_runtime_config(aliased)

    human_config = deepcopy(config)
    human_config["proof_kind"] = "human-authorization"
    human_config["authorization_ref"] = {
        "uri": f"gs://{BUCKET}/exact-authorization.json",
        "generation": 1,
        "sha256": "a" * 64,
        "authorization_digest": "c" * 64,
    }
    human_config["config_digest"] = "0" * 64
    human_config = freeze_publication_runtime_config(human_config)
    config_path = Path(argv[2])
    config_path.write_bytes(canonical_json_bytes(human_config))
    emitted = []
    assert (
        run_publication_cli(
            argv,
            dependencies=PublicationRuntimeDependencies(
                gcs_transport=case["transport"], allow_offline_fake=True
            ),
            emit=emitted.append,
        )
        == 2
    )
    assert json.loads(emitted[-1])["error_code"] == (
        "PUBLICATION_RUNTIME_CONFIG_MISMATCH"
    )


def test_publication_snapshot_materialization_never_imports_canonical_assets(
    tmp_path,
):
    snapshot_root = tmp_path / "immutable-input" / "projects"
    source = snapshot_root / "snapshot-project"
    (source / "assets" / "video").mkdir(parents=True)
    (source / "project.json").write_text('{"id":"snapshot-project"}', encoding="utf-8")
    (source / "assets" / "video" / "poison.mp4").write_bytes(b"poison")
    (source / "checkpoint_assets.json").write_text("{}", encoding="utf-8")
    workspace_root = tmp_path / "ephemeral-workspace" / "projects"
    project = materialize_project_snapshot(
        projects_root=workspace_root,
        snapshot_projects_root=snapshot_root,
        project_id="snapshot-project",
        exclude_assets_publication_outputs=True,
    )
    assert (project / "project.json").is_file()
    assert not (project / "assets").exists()
    assert not (project / "checkpoint_assets.json").exists()


def test_publication_root_consumes_only_exact_preexisting_human_authorization(
    cloud_publication_case, tmp_path
):
    case = cloud_publication_case
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    first = _agent_command(case)
    first_receipt = _publisher(case, verifier=verifier).publish(
        first, trusted_invocation=_identity("root-human-first")
    )
    human = _human_command(case, first, first_receipt)
    config, argv, _ = _production_root_config(case, tmp_path, human)
    intended_identity = CloudInvocationIdentity(
        invocation_id=config["invocation_id"],
        execution_resource=(
            "projects/cloud-project/locations/us-central1/jobs/batch-v2-publish/"
            "executions/publish-human-001"
        ),
        task_id="0",
        mode="run",
    )
    authorization = _publication_authorization(case, human, intended_identity)
    authorization_generation = (
        case["gcs_store"].write_publication_authorization_if_absent(authorization)
    )
    authorization_payload = canonical_json_bytes(authorization)
    authorization_ref = {
        "uri": (
            f"gs://{BUCKET}/projects/{case['project_id']}/.batch-v2/runs/"
            f"{human['batch_id']}/publication/authorizations/"
            f"{authorization['authorization_digest']}.json"
        ),
        "generation": authorization_generation,
        "sha256": hashlib.sha256(authorization_payload).hexdigest(),
        "authorization_digest": authorization["authorization_digest"],
    }
    config["proof_kind"] = "human-authorization"
    config["authorization_ref"] = authorization_ref
    config["config_digest"] = "0" * 64
    config = freeze_publication_runtime_config(config)
    config_path = Path(argv[2])
    config_path.write_bytes(canonical_json_bytes(config))
    argv.extend(
        [
            "--authorization-uri",
            authorization_ref["uri"],
            "--authorization-generation",
            str(authorization_ref["generation"]),
            "--authorization-sha256",
            authorization_ref["sha256"],
            "--authorization-digest",
            authorization_ref["authorization_digest"],
        ]
    )
    emitted = []
    assert run_publication_cli(
        argv,
        dependencies=PublicationRuntimeDependencies(
            environment={
                "CLOUD_RUN_JOB": "batch-v2-publish",
                "CLOUD_RUN_EXECUTION": "publish-human-001",
                "CLOUD_RUN_TASK_INDEX": "0",
                "CLOUD_RUN_TASK_COUNT": "1",
                "CLOUD_RUN_TASK_ATTEMPT": "0",
            },
            gcs_transport=case["transport"],
            media_validator=DeterministicFakeMediaValidator(),
            allow_offline_fake=True,
        ),
        emit=emitted.append,
    ) == 0
    assert json.loads(emitted[-1])["status"] == "completed"


def test_empty_cloud_assets_publication_is_rejected_by_frozen_contract(
    cloud_publication_case,
):
    command = deepcopy(_agent_command(cloud_publication_case))
    command["asset_manifest"]["assets"] = []
    command["asset_manifest"]["total_cost_usd"] = 0
    command["asset_manifest_sha256"] = canonical_sha256(command["asset_manifest"])
    command["review_evidence"]["asset_manifest_sha256"] = command[
        "asset_manifest_sha256"
    ]
    command["asset_bindings"] = []
    command["command_digest"] = "0" * 64
    with pytest.raises(M0ContractError, match="EMPTY_ASSETS_PUBLICATION"):
        freeze_publication_command(command)
    assert cloud_publication_case["gcs_store"].load_publication_state() is None


def test_fake_status_verifier_requires_explicit_fakegcs_test_boundary(
    cloud_publication_case,
):
    case = cloud_publication_case
    with pytest.raises(M2PublicationError, match="UNTRUSTED_EXECUTION_EVIDENCE"):
        CloudAssetsPublisher(
            projects_root=case["projects_root"],
            bucket=BUCKET,
            transport=case["transport"],
            media_validator=DeterministicFakeMediaValidator(),
            execution_status_verifier=FakeADCStatusVerifier(case["state"]["owner"]),
        ).publish(
            _agent_command(case),
            trusted_invocation=_identity("spoofed-verifier"),
        )
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()


def test_source_blob_is_downloaded_once_per_transition(cloud_publication_case):
    case = cloud_publication_case
    receipt = case["result"]["items"][0]["storage_receipt"]
    source_name = receipt["locator"].split(f"gs://{BUCKET}/", 1)[1]
    reads = 0
    original = case["transport"].read_object

    def counted_read(*, bucket, name, generation=None):
        nonlocal reads
        if bucket == BUCKET and name == source_name:
            reads += 1
        return original(bucket=bucket, name=name, generation=generation)

    case["transport"].read_object = counted_read
    _publisher(case, verifier=FakeADCStatusVerifier(case["state"]["owner"])).publish(
        _agent_command(case),
        trusted_invocation=_identity("single-source-download"),
    )
    assert reads == 1


def test_completed_manual_authorization_retry_is_idempotent_for_same_invocation(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    identity = _identity("manual-auth-ambiguous-success")
    authorization = _publication_authorization(case, command, identity)

    def crash_after_completion(name, _facts):
        if name == "cloud_publication_state_completed":
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        _publisher(case, crash_hook=crash_after_completion).publish(
            command,
            trusted_invocation=identity,
            publication_authorization=authorization,
        )
    replay = _publisher(case).publish(
        command,
        trusted_invocation=identity,
        publication_authorization=authorization,
    )
    assert replay["idempotent"] is True
    assert replay["status"] == "awaiting_human"
    repaired_state, _ = case["gcs_store"].load_publication_state()
    assert repaired_state["owner"]["owner_status"] == "completed"

    writes_before = case["transport"].write_calls
    replacement_replay = _publisher(case).publish(
        command,
        trusted_invocation=_identity("manual-auth-other-invocation"),
        publication_authorization=authorization,
    )
    assert replacement_replay["idempotent"] is True
    assert case["transport"].write_calls == writes_before
    changed = deepcopy(command)
    changed["command_id"] = "manual-auth-other-command"
    changed = freeze_publication_command(changed)
    with pytest.raises(M2PublicationError):
        _publisher(case).publish(
            changed,
            trusted_invocation=identity,
            publication_authorization=authorization,
        )


def test_completed_rehydrate_never_reopens_owner_or_calls_repair_hook(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    identity = _identity("repair-claim-owner")
    _publisher(case, verifier=verifier).publish(
        command, trusted_invocation=identity
    )

    def forbid_repair_claim(name, _facts):
        if name == "cloud_publication_repair_claim_acquired":
            raise AssertionError("completed replay reopened publication ownership")

    state_before, generation_before = case["gcs_store"].load_publication_state()
    writes_before = case["transport"].write_calls
    replay = _publisher(case, crash_hook=forbid_repair_claim).publish(
        command, trusted_invocation=_identity("repair-claim-replacement")
    )
    assert replay["idempotent"] is True
    closed, generation_after = case["gcs_store"].load_publication_state()
    assert generation_after == generation_before
    assert closed == state_before
    assert case["transport"].write_calls == writes_before


def test_owner_generation_is_rechecked_before_first_canonical_mutation(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    changed = False

    def supersede_after_claim(name, _facts):
        nonlocal changed
        if name != "cloud_publication_claim_acquired" or changed:
            return
        changed = True
        state, generation = case["gcs_store"].load_publication_state()
        payload = canonical_json_bytes(state)
        case["transport"].write_object(
            bucket=BUCKET,
            name=case["gcs_store"].publication_state_object_name,
            data=payload,
            metadata=case["gcs_store"]._record_metadata(
                "publication_state",
                hashlib.sha256(payload).hexdigest(),
                request_digest=state["request_digest"],
                logical_revision=str(state["revision"]),
            ),
            content_type="application/json",
            if_generation_match=generation,
        )

    with pytest.raises(M2PublicationError, match="PUBLICATION_OWNER_LOST"):
        _publisher(
            case,
            verifier=FakeADCStatusVerifier(case["state"]["owner"]),
            crash_hook=supersede_after_claim,
        ).publish(command, trusted_invocation=_identity("stale-before-canonical"))
    assert not (case["project_dir"] / "assets/video/asset-1.mp4").exists()
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()


@pytest.mark.parametrize(
    "boundary",
    [
        "cloud_publication_asset_materialized",
        "cloud_publication_assets_gcs_verified",
        "cloud_publication_checkpoint_written",
    ],
)
def test_owner_generation_is_rechecked_between_canonical_mutations(
    cloud_publication_case, boundary
):
    case = cloud_publication_case
    command = _agent_command(case)
    superseded = False

    def supersede_at_boundary(name, _facts):
        nonlocal superseded
        if name != boundary or superseded:
            return
        superseded = True
        state, generation = case["gcs_store"].load_publication_state()
        payload = canonical_json_bytes(state)
        case["transport"].write_object(
            bucket=BUCKET,
            name=case["gcs_store"].publication_state_object_name,
            data=payload,
            metadata=case["gcs_store"]._record_metadata(
                "publication_state",
                hashlib.sha256(payload).hexdigest(),
                request_digest=state["request_digest"],
                logical_revision=str(state["revision"]),
            ),
            content_type="application/json",
            if_generation_match=generation,
        )

    with pytest.raises(M2PublicationError, match="PUBLICATION_OWNER_LOST"):
        _publisher(
            case,
            verifier=FakeADCStatusVerifier(case["state"]["owner"]),
            crash_hook=supersede_at_boundary,
        ).publish(
            command,
            trusted_invocation=_identity(f"stale-after-{boundary.replace('_', '-')}")
        )
    assert superseded is True

    checkpoint_name = f"projects/{case['project_id']}/checkpoint_assets.json"
    if boundary != "cloud_publication_checkpoint_written":
        assert not (case["project_dir"] / "checkpoint_assets.json").exists()
    with pytest.raises(GCSObjectNotFound):
        case["transport"].head_object(bucket=BUCKET, name=checkpoint_name)

    asset_name = f"projects/{case['project_id']}/assets/video/asset-1.mp4"
    if boundary == "cloud_publication_asset_materialized":
        with pytest.raises(GCSObjectNotFound):
            case["transport"].head_object(bucket=BUCKET, name=asset_name)
    else:
        assert case["transport"].head_object(
            bucket=BUCKET, name=asset_name
        ).data is None


def test_planted_exact_completed_checkpoint_cannot_bypass_prior_human_chain(
    cloud_publication_case,
):
    case = cloud_publication_case
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    first = _agent_command(case)
    first_receipt = _publisher(case, verifier=verifier).publish(
        first, trusted_invocation=_identity("planted-chain-first")
    )
    human = _human_command(case, first, first_receipt)
    write_checkpoint(
        case["projects_root"],
        case["project_id"],
        "assets",
        "completed",
        {"asset_manifest": deepcopy(human["asset_manifest"])},
        pipeline_type=human["pipeline_type"],
        checkpoint_policy="guided",
        human_approval_required=True,
        human_approved=True,
        review={"batch_v2_agent_review": deepcopy(human["review_evidence"])},
        cost_snapshot=_checkpoint_cost(human["cost_snapshot"]),
        metadata={"batch_v2_publication": _publication_metadata(human)},
    )
    assert (
        read_checkpoint(case["projects_root"], case["project_id"], "assets")["status"]
        == "completed"
    )

    with pytest.raises(M2PublicationError, match="HUMAN_APPROVAL_BINDING_INVALID"):
        _publisher(case, verifier=verifier).publish(
            human, trusted_invocation=_identity("planted-chain-second")
        )
    state, _ = case["gcs_store"].load_publication_state()
    assert len(state["completed_commands"]) == 1


def test_completed_agent_publication_rehydrates_a_fresh_materialized_replica(
    cloud_publication_case, tmp_path
):
    case = cloud_publication_case
    snapshot = tmp_path / "agent-snapshot-projects"
    _copy_prepublication_project(case, snapshot)
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    command = _agent_command(case)
    identity = _identity("fresh-agent-replay")
    _publisher(case, verifier=verifier).publish(command, trusted_invocation=identity)

    fresh_root = tmp_path / "fresh-agent-projects"
    fresh_project = _copy_prepublication_project(
        {**case, "project_dir": snapshot / case["project_id"]}, fresh_root
    )
    replay = _publisher(case, root=fresh_root, verifier=verifier).publish(
        command, trusted_invocation=identity
    )
    assert replay["idempotent"] is True
    assert (fresh_project / "assets/video/asset-1.mp4").is_file()
    assert (
        read_checkpoint(fresh_root, case["project_id"], "assets")["status"]
        == "awaiting_human"
    )
    assert (
        fresh_project
        / ".batch-v2"
        / "runs"
        / command["batch_id"]
        / "publication"
        / "commands"
        / f"{command['command_id']}.json"
    ).is_file()


def test_completed_agent_rehydrate_accepts_new_execution_and_writes_no_gcs(
    cloud_publication_case, tmp_path
):
    case = cloud_publication_case
    snapshot = tmp_path / "cross-execution-snapshot"
    _copy_prepublication_project(case, snapshot)
    command = _agent_command(case)
    _publisher(
        case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
    ).publish(command, trusted_invocation=_identity("completed-original"))
    fresh_root = tmp_path / "cross-execution-rehydrate"
    fresh_project = _copy_prepublication_project(
        {**case, "project_dir": snapshot / case["project_id"]}, fresh_root
    )
    writes_before = case["transport"].write_calls

    receipt = _publisher(case, root=fresh_root).publish(
        command, trusted_invocation=_identity("completed-replacement")
    )

    assert receipt["idempotent"] is True
    assert case["transport"].write_calls == writes_before
    assert (fresh_project / "assets/video/asset-1.mp4").is_file()
    assert (
        read_checkpoint(fresh_root, case["project_id"], "assets")["status"]
        == "awaiting_human"
    )


def test_completed_rehydrate_rechecks_authority_after_assets_before_checkpoint(
    cloud_publication_case, tmp_path
):
    case = cloud_publication_case
    snapshot = tmp_path / "pre-checkpoint-toctou-snapshot"
    _copy_prepublication_project(case, snapshot)
    command = _agent_command(case)
    first_receipt = _publisher(
        case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
    ).publish(command, trusted_invocation=_identity("pre-checkpoint-source"))
    human = _human_command(case, command, first_receipt)

    fresh_root = tmp_path / "pre-checkpoint-toctou-rehydrate"
    _copy_prepublication_project(
        {**case, "project_dir": snapshot / case["project_id"]}, fresh_root
    )
    interleaved = False
    transition_writes = None

    def advance_after_assets(name, _facts):
        nonlocal interleaved, transition_writes
        if name == "cloud_publication_recovery_assets_restored" and not interleaved:
            interleaved = True
            transition_writes = _publish_human_transition_in_concurrent_process_model(
                case,
                human,
                invocation_name="pre-checkpoint-human-transition",
            )

    with pytest.raises(M2PublicationError, match="PUBLICATION_OWNER_LOST"):
        _publisher(case, root=fresh_root, crash_hook=advance_after_assets).publish(
            command, trusted_invocation=_identity("pre-checkpoint-reader")
        )

    assert interleaved is True
    assert transition_writes is not None
    assert case["transport"].write_calls == transition_writes
    assert not (fresh_root / case["project_id"] / "checkpoint_assets.json").exists()
    history = fresh_root / case["project_id"] / "history"
    assert not history.exists() or not list(history.glob("checkpoint_assets_*.json"))


def test_completed_rehydrate_rechecks_authority_after_checkpoint_before_receipt(
    cloud_publication_case, tmp_path
):
    case = cloud_publication_case
    snapshot = tmp_path / "pre-receipt-toctou-snapshot"
    _copy_prepublication_project(case, snapshot)
    command = _agent_command(case)
    first_receipt = _publisher(
        case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
    ).publish(command, trusted_invocation=_identity("pre-receipt-source"))
    human = _human_command(case, command, first_receipt)

    fresh_root = tmp_path / "pre-receipt-toctou-rehydrate"
    _copy_prepublication_project(
        {**case, "project_dir": snapshot / case["project_id"]}, fresh_root
    )
    interleaved = False
    transition_writes = None

    def advance_after_checkpoint(name, _facts):
        nonlocal interleaved, transition_writes
        if name == "cloud_publication_recovery_checkpoint_restored" and not interleaved:
            interleaved = True
            transition_writes = _publish_human_transition_in_concurrent_process_model(
                case,
                human,
                invocation_name="pre-receipt-human-transition",
            )

    with pytest.raises(M2PublicationError, match="PUBLICATION_OWNER_LOST"):
        _publisher(case, root=fresh_root, crash_hook=advance_after_checkpoint).publish(
            command, trusted_invocation=_identity("pre-receipt-reader")
        )

    assert interleaved is True
    assert transition_writes is not None
    assert case["transport"].write_calls == transition_writes
    assert (
        read_checkpoint(fresh_root, case["project_id"], "assets")["status"]
        == "awaiting_human"
    )


def test_completed_repair_rechecks_post_repair_generation_before_receipt(
    cloud_publication_case,
):
    case = cloud_publication_case
    command = _agent_command(case)
    identity = _identity("post-repair-owner")
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    _publisher(case, verifier=verifier).publish(
        command, trusted_invocation=identity
    )

    completed_state, completed_generation = (
        case["gcs_store"].load_publication_state()
    )
    repairing_state = deepcopy(completed_state)
    repairing_state["revision"] += 1
    repairing_state["owner"]["owner_status"] = "repairing"
    repairing_state["owner"].pop("completed_at")
    case["gcs_store"].save_publication_state(
        repairing_state, expected_generation=completed_generation
    )
    interleaved = False

    def advance_after_repair(name, _facts):
        nonlocal interleaved
        if name == "cloud_publication_repair_completed" and not interleaved:
            interleaved = True
            _advance_publication_state_generation(case)

    with pytest.raises(M2PublicationError, match="PUBLICATION_OWNER_LOST"):
        _publisher(
            case,
            verifier=verifier,
            crash_hook=advance_after_repair,
        ).publish(command, trusted_invocation=identity)

    assert interleaved is True


def test_same_successor_can_read_only_rehydrate_after_takeover_completion(
    cloud_publication_case, tmp_path
):
    case = cloud_publication_case
    snapshot = tmp_path / "takeover-successor-snapshot"
    _copy_prepublication_project(case, snapshot)
    command = _agent_command(case)
    first_identity = _identity("completed-takeover-first")

    def crash_after_asset(name, _facts):
        if name == "cloud_publication_asset_materialized":
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        _publisher(
            case,
            verifier=FakeADCStatusVerifier(case["state"]["owner"]),
            crash_hook=crash_after_asset,
        ).publish(command, trusted_invocation=first_identity)
    active_state, _ = case["gcs_store"].load_publication_state()
    successor = _identity("completed-takeover-successor")
    _publisher(
        case,
        verifier=FakeADCStatusVerifier(
            _publication_owner_for_proof(case, active_state)
        ),
    ).publish(command, trusted_invocation=successor)

    fresh_root = tmp_path / "takeover-successor-rehydrate"
    fresh_project = _copy_prepublication_project(
        {**case, "project_dir": snapshot / case["project_id"]}, fresh_root
    )
    writes_before = case["transport"].write_calls
    receipt = _publisher(case, root=fresh_root).publish(
        command, trusted_invocation=successor
    )
    assert receipt["idempotent"] is True
    assert case["transport"].write_calls == writes_before
    assert (fresh_project / "assets/video/asset-1.mp4").is_file()


@pytest.mark.parametrize(
    "tamper",
    ["changed-command", "fence", "state", "asset", "checkpoint"],
)
def test_completed_read_only_rehydrate_rejects_changed_authority_without_gcs_writes(
    cloud_publication_case, tmp_path, tamper
):
    case = cloud_publication_case
    snapshot = tmp_path / f"tamper-snapshot-{tamper}"
    _copy_prepublication_project(case, snapshot)
    command = _agent_command(case)
    _publisher(
        case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
    ).publish(command, trusted_invocation=_identity(f"tamper-source-{tamper}"))
    attempted = command
    if tamper == "changed-command":
        attempted = deepcopy(command)
        attempted["review_evidence"]["review_reference"] = "agent-review:changed"
        attempted = freeze_publication_command(attempted)
    elif tamper == "fence":
        case["transport"].corrupt(
            f"gs://{BUCKET}/{case['gcs_store'].publication_fence_object_name}",
            "metadata",
        )
    elif tamper == "state":
        case["transport"].corrupt(
            f"gs://{BUCKET}/{case['gcs_store'].publication_state_object_name}",
            "bytes",
        )
    else:
        state, _ = case["gcs_store"].load_publication_state()
        completion = state["completed_commands"][-1]
        facts = (
            completion["asset_objects"][0]
            if tamper == "asset"
            else completion["checkpoint_snapshot"]
        )
        case["transport"].corrupt(
            f"gs://{BUCKET}/{facts['object_name']}", "bytes"
        )
    fresh_root = tmp_path / f"tampered-{tamper}-rehydrate"
    fresh_project = _copy_prepublication_project(
        {**case, "project_dir": snapshot / case["project_id"]}, fresh_root
    )
    writes_before = case["transport"].write_calls

    with pytest.raises(Exception):
        _publisher(case, root=fresh_root).publish(
            attempted, trusted_invocation=_identity(f"tamper-reader-{tamper}")
        )
    assert case["transport"].write_calls == writes_before
    assert not (
        fresh_root / case["project_id"] / "checkpoint_assets.json"
    ).exists()
    assert not (fresh_project / "assets/video/asset-1.mp4").exists()


def test_human_transition_and_completed_replay_rehydrate_fresh_replicas(
    cloud_publication_case, tmp_path
):
    case = cloud_publication_case
    snapshot = tmp_path / "human-snapshot-projects"
    _copy_prepublication_project(case, snapshot)
    verifier = FakeADCStatusVerifier(case["state"]["owner"])
    first = _agent_command(case)
    first_receipt = _publisher(case, verifier=verifier).publish(
        first, trusted_invocation=_identity("fresh-human-first")
    )
    human = _human_command(case, first, first_receipt)

    human_root = tmp_path / "fresh-human-projects"
    _copy_prepublication_project(
        {**case, "project_dir": snapshot / case["project_id"]}, human_root
    )
    completed = _publisher(case, root=human_root, verifier=verifier).publish(
        human, trusted_invocation=_identity("fresh-human-second")
    )
    assert completed["status"] == "completed"
    archived = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in (
            human_root / case["project_id"] / "history"
        ).glob("checkpoint_assets_*.json")
    ]
    assert len(archived) == 1
    assert archived[0]["status"] == "awaiting_human"
    assert archived[0]["metadata"]["batch_v2_publication"]["command_digest"] == (
        first["command_digest"]
    )

    replay_root = tmp_path / "fresh-completed-projects"
    replay_project = _copy_prepublication_project(
        {**case, "project_dir": snapshot / case["project_id"]}, replay_root
    )
    completed_state, _ = case["gcs_store"].load_publication_state()
    prior_canonical = completed_state["completed_commands"][0]["checkpoint"]
    with pytest.raises(GCSObjectNotFound):
        case["transport"].read_object(
            bucket=BUCKET,
            name=prior_canonical["object_name"],
            generation=prior_canonical["generation"],
        )
    writes_before = case["transport"].write_calls
    replay = _publisher(case, root=replay_root).publish(
        human, trusted_invocation=_identity("fresh-human-replacement")
    )
    assert replay["idempotent"] is True
    assert case["transport"].write_calls == writes_before
    assert (
        read_checkpoint(replay_root, case["project_id"], "assets")["status"]
        == "completed"
    )
    assert (replay_project / "assets/video/asset-1.mp4").is_file()
    command_dir = (
        replay_project
        / ".batch-v2"
        / "runs"
        / human["batch_id"]
        / "publication"
        / "commands"
    )
    assert (command_dir / f"{first['command_id']}.json").is_file()
    assert (command_dir / f"{human['command_id']}.json").is_file()
    assert json.loads(
        (command_dir / f"{first['command_id']}.json").read_text(encoding="utf-8")
    ) == first
    assert json.loads(
        (command_dir / f"{human['command_id']}.json").read_text(encoding="utf-8")
    ) == human
    replay_history = list(
        (replay_project / "history").glob("checkpoint_assets_*.json")
    )
    assert len(replay_history) == 1
    replay_state, _ = case["gcs_store"].load_publication_state()
    prior_completion = replay_state["completed_commands"][0]
    assert hashlib.sha256(replay_history[0].read_bytes()).hexdigest() == (
        prior_completion["checkpoint_snapshot"]["sha256"]
    )
    replay_prior = json.loads(replay_history[0].read_text(encoding="utf-8"))
    assert replay_prior["status"] == "awaiting_human"
    assert replay_prior["metadata"]["batch_v2_publication"]["command_digest"] == (
        first["command_digest"]
    )


def test_publication_command_schema_formally_rejects_empty_assets_and_bindings(
    cloud_publication_case
):
    schema = load_execution_schema("publication_command")
    command = _agent_command(cloud_publication_case)

    no_bindings = deepcopy(command)
    no_bindings["asset_bindings"] = []
    binding_errors = list(
        Draft202012Validator(
            schema["properties"]["asset_bindings"]
        ).iter_errors(no_bindings["asset_bindings"])
    )
    assert any(
        error.validator == "minItems" and list(error.path) == []
        for error in binding_errors
    )

    no_assets = deepcopy(command)
    no_assets["asset_manifest"]["assets"] = []
    asset_errors = list(
        Draft202012Validator(
            schema["properties"]["asset_manifest"]
        ).iter_errors(no_assets["asset_manifest"])
    )
    assert any(
        error.validator == "minItems" and list(error.path) == ["assets"]
        for error in asset_errors
    )

    _publisher(
        cloud_publication_case,
        verifier=FakeADCStatusVerifier(cloud_publication_case["state"]["owner"]),
    ).publish(command, trusted_invocation=_identity("schema-state-source"))
    state, _ = cloud_publication_case["gcs_store"].load_publication_state()
    state["completed_commands"][0]["asset_objects"] = []
    state_schema = load_execution_schema("publication_state")
    completion_schema = state_schema["properties"]["completed_commands"]["items"]
    asset_objects_schema = completion_schema["properties"]["asset_objects"]
    state_errors = list(
        Draft202012Validator(asset_objects_schema).iter_errors(
            state["completed_commands"][0]["asset_objects"]
        )
    )
    assert any(
        error.validator == "minItems" and list(error.path) == []
        for error in state_errors
    )


def test_same_command_checkpoint_timestamp_race_adopts_gcs_authority(
    cloud_publication_case, tmp_path
):
    case = cloud_publication_case
    command = _agent_command(case)
    identity = _identity("checkpoint-convergence")

    def stop_after_claim(name, _facts):
        if name == "cloud_publication_claim_acquired":
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        _publisher(
            case,
            verifier=FakeADCStatusVerifier(case["state"]["owner"]),
            crash_hook=stop_after_claim,
        ).publish(command, trusted_invocation=identity)

    replica_root = tmp_path / "checkpoint-winner-projects"
    replica_project = _copy_prepublication_project(case, replica_root)
    write_checkpoint(
        replica_root,
        case["project_id"],
        "assets",
        "awaiting_human",
        {"asset_manifest": deepcopy(command["asset_manifest"])},
        pipeline_type=command["pipeline_type"],
        checkpoint_policy="guided",
        human_approval_required=True,
        human_approved=False,
        review={"batch_v2_agent_review": deepcopy(command["review_evidence"])},
        cost_snapshot=_checkpoint_cost(command["cost_snapshot"]),
        metadata={"batch_v2_publication": _publication_metadata(command)},
    )
    winner_bytes = (replica_project / "checkpoint_assets.json").read_bytes()
    winner_checkpoint = json.loads(winner_bytes.decode("utf-8"))
    store = case["gcs_store"]
    metadata = store._record_metadata(
        "canonical_checkpoint",
        hashlib.sha256(winner_bytes).hexdigest(),
        client_sha256=hashlib.sha256(winner_bytes).hexdigest(),
        logical_path="checkpoint_assets.json",
        command_digest=command["command_digest"],
        checkpoint_sha256=canonical_sha256(winner_checkpoint),
        status="awaiting_human",
    )
    case["transport"].write_object(
        bucket=BUCKET,
        name=f"projects/{case['project_id']}/checkpoint_assets.json",
        data=winner_bytes,
        metadata=metadata,
        content_type="application/json",
        if_generation_match=0,
    )

    result = _publisher(
        case, verifier=FakeADCStatusVerifier(case["state"]["owner"])
    ).publish(command, trusted_invocation=identity)
    assert result["status"] == "awaiting_human"
    assert (case["project_dir"] / "checkpoint_assets.json").read_bytes() == winner_bytes


def _second_batch_case(case, replica_root: Path):
    request = deepcopy(case["request"])
    request["batch_id"] = "batch-002"
    request = freeze_batch_request(request)
    project_dir = replica_root / case["project_id"]
    transport = case["transport"]
    provider = ScriptedFakeProvider()

    def store_factory(exact_project_dir, batch_id):
        return GCSStore(
            exact_project_dir,
            batch_id,
            bucket=BUCKET,
            transport=transport,
        )

    result = CloudBatchExecutor(
        projects_root=replica_root,
        provider=provider,
        media_validator=DeterministicFakeMediaValidator(),
        clock=FakeClock(),
        store_factory=store_factory,
    ).run(
        request,
        observed_source_revision=request["source_revision"],
        adapter_observation={
            "identity": deepcopy(request["work_items"][0]["identity"]),
            "route_binding": "explicit_request",
            "credential_mode": "adc",
            "hidden_writers": "disabled",
            "available": True,
        },
        trusted_invocation=CloudInvocationIdentity(
            invocation_id="cloud-source-two",
            execution_resource=(
                "projects/cloud-project/locations/us-central1/jobs/batch-v2/"
                "executions/source-two"
            ),
            task_id="0",
            mode="run",
        ),
    )
    store = store_factory(project_dir, request["batch_id"])
    durable_request, request_generation = store.load_request()
    state, state_generation = store.load_batch_state()
    durable_result, result_generation = store.load_result()
    return {
        **case,
        "projects_root": replica_root,
        "project_dir": project_dir,
        "request": durable_request,
        "result": durable_result,
        "result_digest": canonical_sha256(result),
        "state": state,
        "state_revision": state["revision"],
        "gcs_store": store,
        "store": LocalStore(project_dir, request["batch_id"]),
        "provider": provider,
        "cloud_source": {
            "bucket": BUCKET,
            "request": {
                "logical_path": f".batch-v2/runs/{request['batch_id']}/request.json",
                "object_name": store.request_object_name,
                "generation": request_generation,
                "sha256": canonical_sha256(durable_request),
            },
            "state": {
                "logical_path": f".batch-v2/runs/{request['batch_id']}/state.json",
                "object_name": store.state_object_name,
                "generation": state_generation,
                "sha256": canonical_sha256(state),
            },
            "result": {
                "logical_path": f".batch-v2/runs/{request['batch_id']}/result.json",
                "object_name": store.result_object_name,
                "generation": result_generation,
                "sha256": canonical_sha256(durable_result),
            },
        },
    }


def test_distinct_batches_for_one_project_have_one_project_stage_cas_winner(
    cloud_publication_case, tmp_path
):
    first_case = cloud_publication_case
    replica_root = tmp_path / "distinct-batch-projects"
    _copy_prepublication_project(first_case, replica_root)
    second_case = _second_batch_case(first_case, replica_root)
    first_command = _agent_command(first_case, command_id="project-fence-one")
    second_command = _agent_command(second_case, command_id="project-fence-two")
    barrier = threading.Barrier(2)

    def synchronize_claims(_bucket, name, expected_generation):
        if expected_generation == 0 and name.endswith("/publication/assets/fence.json"):
            barrier.wait(timeout=5)

    first_case["transport"].before_write = synchronize_claims
    outcomes = []
    failures = []

    def invoke(case, command, invocation):
        try:
            outcomes.append(
                (
                    case,
                    _publisher(
                        case,
                        verifier=FakeADCStatusVerifier(case["state"]["owner"]),
                    ).publish(command, trusted_invocation=_identity(invocation)),
                )
            )
        except BaseException as exc:
            failures.append((case, exc))

    threads = [
        threading.Thread(
            target=invoke,
            args=(first_case, first_command, "project-fence-one"),
        ),
        threading.Thread(
            target=invoke,
            args=(second_case, second_command, "project-fence-two"),
        ),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=20)
    first_case["transport"].before_write = None

    assert all(not thread.is_alive() for thread in threads)
    assert len(outcomes) == len(failures) == 1
    assert isinstance(failures[0][1], M2PublicationError)
    assert failures[0][1].code == "PROJECT_STAGE_PUBLICATION_CONFLICT"
    losing_project = failures[0][0]["project_dir"]
    assert not (losing_project / "assets/video/asset-1.mp4").exists()
    assert not (losing_project / "checkpoint_assets.json").exists()
