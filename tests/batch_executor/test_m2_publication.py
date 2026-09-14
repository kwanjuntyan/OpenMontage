from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path

import pytest

from backlot.state import load_board_state
from lib.batch_executor.contracts import (
    M0ContractError,
    canonical_json_bytes,
    canonical_sha256,
    freeze_batch_request,
    freeze_publication_command,
    freeze_self_digest,
    validate_publication_command,
)
from lib.batch_executor.engine import LocalBatchExecutor
from lib.batch_executor.errors import (
    InjectedCrash,
    LocalRunLocked,
    M2PublicationError,
    WorkerWriteViolation,
)
from lib.batch_executor.media_validation import DeterministicFakeMediaValidator
from lib.batch_executor.publication import LocalAssetsPublisher
from lib.batch_executor.side_effects import (
    publication_execution_scope,
    worker_execution_scope,
)
from lib.batch_executor.storage import LocalStore
from lib.batch_executor.testing import FakeClock, ScriptedFakeProvider
from lib.checkpoint import read_checkpoint, write_checkpoint


@pytest.fixture()
def publication_case(
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
):
    provider = ScriptedFakeProvider()
    executor = LocalBatchExecutor(
        projects_root=authorized_project["projects_root"],
        provider=provider,
        media_validator=DeterministicFakeMediaValidator(),
        clock=FakeClock(),
    )
    result = executor.run(
        batch_request,
        observed_source_revision=source_revision,
        adapter_observation=qualified_adapter_observation,
        invocation_id="invocation-m2-source",
    )
    store = LocalStore(
        authorized_project["project_dir"], batch_request["batch_id"]
    )
    state, revision = store.load_batch_state()
    durable_result, result_digest = store.load_result()
    assert durable_result == result
    return {
        **authorized_project,
        "request": batch_request,
        "result": durable_result,
        "result_digest": result_digest,
        "state": state,
        "state_revision": revision,
        "store": store,
        "provider": provider,
    }


@pytest.fixture()
def two_item_publication_case(
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
):
    request = deepcopy(batch_request)
    request["authorization"]["approved_budget_usd"] = 2.0
    request["authorization"]["max_authorized_spend_usd"] = 2.0
    request["authorization"]["max_total_attempts"] = 2
    item = deepcopy(request["work_items"][0])
    item.update(
        {
            "item_id": "item-002",
            "scene_id": "scene-2",
            "asset_id": "asset-2",
        }
    )
    item["inputs"]["prompt"] = "A second approved cinematic shot."
    item["output_spec"][
        "canonical_destination_intent"
    ] = "assets/video/asset-2.mp4"
    request["work_items"].append(item)
    request = freeze_batch_request(request)

    provider = ScriptedFakeProvider()
    result = LocalBatchExecutor(
        projects_root=authorized_project["projects_root"],
        provider=provider,
        media_validator=DeterministicFakeMediaValidator(),
        clock=FakeClock(),
    ).run(
        request,
        observed_source_revision=source_revision,
        adapter_observation=qualified_adapter_observation,
        invocation_id="invocation-m2-two-item-source",
    )
    store = LocalStore(authorized_project["project_dir"], request["batch_id"])
    state, revision = store.load_batch_state()
    durable_result, result_digest = store.load_result()
    assert durable_result == result
    return {
        **authorized_project,
        "request": request,
        "result": durable_result,
        "result_digest": result_digest,
        "state": state,
        "state_revision": revision,
        "store": store,
        "provider": provider,
    }


def _agent_command(case, *, command_id="publish-agent-001"):
    request = case["request"]
    result = case["result"]
    state = case["state"]
    work_item = request["work_items"][0]
    result_items = {item["item_id"]: item for item in result["items"]}
    latest_attempts = {
        item_id: max(
            (
                attempt
                for attempt in state["attempts"]
                if attempt["item_id"] == item_id
            ),
            key=lambda attempt: attempt["dispatch_sequence"],
        )
        for item_id in result_items
    }
    manifest = {
        "version": "1.0",
        "assets": [
            {
                "id": item["asset_id"],
                "type": "video",
                "path": item["output_spec"]["canonical_destination_intent"],
                "source_tool": item["identity"]["tool_name"],
                "scene_id": item["scene_id"],
                "prompt": item["inputs"]["prompt"],
                "model": item["identity"]["model"],
                "provider": item["identity"]["provider"],
                "cost_usd": latest_attempts[item["item_id"]]["cost"][
                    "known_actual_usd"
                ],
                "duration_seconds": float(item["inputs"]["duration"].rstrip("s")),
                "format": "mp4",
            }
            for item in request["work_items"]
        ],
        "total_cost_usd": result["cost"]["known_actual_usd"],
        "metadata": {"reviewed_batch_result": case["result_digest"]},
    }
    manifest_digest = canonical_sha256(manifest)
    command = {
        "version": "1.0",
        "canonical_json": "openmontage-canonical-json-v1",
        "command_id": command_id,
        "command_digest": "0" * 64,
        "created_at": "2026-09-14T10:00:00Z",
        "batch_id": request["batch_id"],
        "request_digest": request["request_digest"],
        "project_id": request["project_id"],
        "pipeline_type": request["pipeline_type"],
        "stage": "assets",
        "identity": deepcopy(work_item["identity"]),
        "result_ref": {
            "logical_path": case["store"].result_path.relative_to(
                case["project_dir"]
            ).as_posix(),
            "sha256": case["result_digest"],
        },
        "state_ref": {
            "logical_path": case["store"].state_path.relative_to(
                case["project_dir"]
            ).as_posix(),
            "sha256": canonical_sha256(state),
            "revision": case["state_revision"],
        },
        "execution_owner": deepcopy(state["owner"]),
        "asset_manifest": manifest,
        "asset_manifest_sha256": manifest_digest,
        "asset_bindings": [
            {
                "item_id": item["item_id"],
                "asset_id": item["asset_id"],
                "storage_receipt_id": receipt["receipt_id"],
                "sha256": receipt["sha256"],
                "size_bytes": receipt["size_bytes"],
                "source_locator": receipt["locator"],
                "canonical_path": item["output_spec"][
                    "canonical_destination_intent"
                ],
            }
            for item in request["work_items"]
            for receipt in [result_items[item["item_id"]]["storage_receipt"]]
        ],
        "review_evidence": {
            "kind": "agent_review",
            "reviewer_id": "agent-main-task",
            "review_reference": "codex:review:m2:agent-001",
            "reviewed_at": "2026-09-14T09:59:00Z",
            "batch_result_sha256": case["result_digest"],
            "asset_manifest_sha256": manifest_digest,
        },
        "cost_snapshot": deepcopy(result["cost"]),
        "transition": {
            "kind": "agent_review_to_awaiting_human",
            "target_status": "awaiting_human",
            "human_approved": False,
        },
    }
    return freeze_publication_command(command)


def _human_command(case, first_command, first_receipt):
    command = deepcopy(first_command)
    command.update(
        {
            "command_id": "publish-human-001",
            "command_digest": "0" * 64,
            "created_at": "2026-09-14T10:05:00Z",
            "transition": {
                "kind": "human_approval_to_completed",
                "target_status": "completed",
                "human_approved": True,
                "prior_checkpoint_ref": {
                    "logical_path": "checkpoint_assets.json",
                    "sha256": first_receipt["checkpoint_sha256"],
                    "status": "awaiting_human",
                },
                "prior_publication_command_ref": {
                    "command_id": first_command["command_id"],
                    "logical_path": first_receipt["command_logical_path"],
                    "sha256": first_command["command_digest"],
                },
                "human_approval_evidence": {
                    "kind": "explicit_human_reply",
                    "approval_id": "human-reply-001",
                    "reply_reference": "codex:message:human-approval-001",
                    "reply_sha256": "a" * 64,
                    "approved_at": "2026-09-14T10:04:00Z",
                    "prior_checkpoint_sha256": first_receipt[
                        "checkpoint_sha256"
                    ],
                    "prior_publication_command_digest": first_command[
                        "command_digest"
                    ],
                    "batch_result_sha256": case["result_digest"],
                    "asset_manifest_sha256": first_command[
                        "asset_manifest_sha256"
                    ],
                },
            },
        }
    )
    return freeze_publication_command(command)


def _publisher(case, **kwargs):
    return LocalAssetsPublisher(
        projects_root=case["projects_root"],
        media_validator=DeterministicFakeMediaValidator(),
        **kwargs,
    )


def test_publication_command_contract_binds_review_result_manifest_cost_and_owner(
    publication_case,
):
    command = _agent_command(publication_case)
    validate_publication_command(command)

    for mutation, match in (
        (lambda value: value["result_ref"].update(sha256="f" * 64), "DIGEST"),
        (lambda value: value["state_ref"].update(revision=999), "DIGEST"),
        (lambda value: value["cost_snapshot"].update(known_actual_usd=0), "DIGEST"),
    ):
        changed = deepcopy(command)
        mutation(changed)
        with pytest.raises(M0ContractError, match=match):
            validate_publication_command(changed)

    active = deepcopy(command)
    active["execution_owner"]["owner_status"] = "active"
    with pytest.raises(M0ContractError, match="EXECUTION_NOT_STOPPED"):
        freeze_publication_command(active)


def test_publication_command_rejects_invalid_manifest_and_noncanonical_paths(
    publication_case,
):
    invalid = deepcopy(_agent_command(publication_case))
    invalid["asset_manifest"]["assets"][0].pop("scene_id")
    with pytest.raises(M0ContractError, match="ASSET_MANIFEST_INVALID"):
        freeze_publication_command(invalid)

    traversal = deepcopy(_agent_command(publication_case))
    traversal["asset_manifest"]["assets"][0]["path"] = "assets/../checkpoint_assets.json"
    traversal["asset_bindings"][0]["canonical_path"] = traversal[
        "asset_manifest"
    ]["assets"][0]["path"]
    with pytest.raises(M0ContractError, match="SCHEMA_VALIDATION_FAILED"):
        freeze_publication_command(traversal)


def test_m2_rejects_portable_two_item_collision_before_any_publication_mutation(
    two_item_publication_case,
):
    case = two_item_publication_case
    command = deepcopy(_agent_command(case))
    command["asset_manifest"]["assets"][1][
        "path"
    ] = "assets/video/ASSET-1.mp4"
    command["asset_bindings"][1][
        "canonical_path"
    ] = "assets/video/ASSET-1.mp4"
    command["asset_manifest_sha256"] = canonical_sha256(command["asset_manifest"])
    command["review_evidence"]["asset_manifest_sha256"] = command[
        "asset_manifest_sha256"
    ]
    command = freeze_self_digest(
        command,
        schema_name="publication_command",
        digest_field="command_digest",
    )

    with pytest.raises(M0ContractError, match="CANONICAL_DESTINATION_COLLISION"):
        _publisher(case).publish(command)

    assert not case["store"].publication_command_path(command["command_id"]).exists()
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()
    assert not list((case["project_dir"] / "assets" / "video").glob("*.mp4"))


def test_m2_rejects_windows_ads_path_before_any_publication_mutation(
    publication_case,
):
    command = deepcopy(_agent_command(publication_case))
    unsafe = "assets/video/asset-1.mp4:alternate"
    command["asset_manifest"]["assets"][0]["path"] = unsafe
    command["asset_bindings"][0]["canonical_path"] = unsafe
    command["asset_manifest_sha256"] = canonical_sha256(command["asset_manifest"])
    command["review_evidence"]["asset_manifest_sha256"] = command[
        "asset_manifest_sha256"
    ]
    command = freeze_self_digest(
        command,
        schema_name="publication_command",
        digest_field="command_digest",
    )

    with pytest.raises(M0ContractError, match="CANONICAL_ASSET_PATH_INVALID"):
        _publisher(publication_case).publish(command)

    assert not publication_case["store"].publication_command_path(
        command["command_id"]
    ).exists()
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()
    assert not list(
        (publication_case["project_dir"] / "assets" / "video").glob("*.mp4")
    )


def test_existing_case_alias_is_rejected_before_command_or_checkpoint(
    publication_case,
):
    command = _agent_command(publication_case)
    receipt = publication_case["result"]["items"][0]["storage_receipt"]
    source = publication_case["project_dir"] / receipt["locator"]
    alias = publication_case["project_dir"] / "assets/video/ASSET-1.mp4"
    alias.write_bytes(source.read_bytes())

    with pytest.raises(M2PublicationError, match="CANONICAL_PATH_ALIAS"):
        _publisher(publication_case).publish(command)

    assert not publication_case["store"].publication_command_path(
        command["command_id"]
    ).exists()
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()
    assert alias.exists()


def test_agent_review_must_not_postdate_its_publication_command(publication_case):
    command = deepcopy(_agent_command(publication_case))
    command["review_evidence"]["reviewed_at"] = "2026-09-14T10:00:01Z"

    with pytest.raises(M0ContractError, match="PUBLICATION_CHRONOLOGY_INVALID"):
        freeze_publication_command(command)


def test_result_must_exist_before_agent_review_and_before_persistence(
    publication_case,
):
    command = deepcopy(_agent_command(publication_case))
    command["review_evidence"]["reviewed_at"] = "2000-01-01T00:00:00Z"
    command = freeze_publication_command(command)

    with pytest.raises(M2PublicationError, match="PUBLICATION_CHRONOLOGY_INVALID"):
        _publisher(publication_case).publish(command)

    assert not publication_case["store"].publication_command_path(
        command["command_id"]
    ).exists()
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()
    assert not list(
        (publication_case["project_dir"] / "assets" / "video").glob("*.mp4")
    )


def test_execution_success_stops_without_canonical_publication(publication_case):
    project = publication_case["project_dir"]
    assert publication_case["result"]["status"] == "awaiting_agent_review"
    assert publication_case["state"]["status"] == "awaiting_agent_review"
    assert not (project / "checkpoint_assets.json").exists()
    assert not (project / "assets" / "video" / "asset-1.mp4").exists()
    assert not (project / "artifacts" / "asset_manifest.json").exists()


def test_agent_review_publishes_awaiting_human_through_official_reader(
    publication_case,
):
    command = _agent_command(publication_case)
    receipt = _publisher(publication_case).publish(command)
    checkpoint = read_checkpoint(
        publication_case["projects_root"], publication_case["project_id"], "assets"
    )

    assert checkpoint is not None
    assert checkpoint["status"] == "awaiting_human"
    assert checkpoint["human_approval_required"] is True
    assert checkpoint["human_approved"] is False
    assert checkpoint["artifacts"]["asset_manifest"] == command["asset_manifest"]
    assert checkpoint["metadata"]["batch_v2_publication"]["command_digest"] == command[
        "command_digest"
    ]
    assert receipt["checkpoint_sha256"] == canonical_sha256(checkpoint)
    assert (
        publication_case["project_dir"] / "assets" / "video" / "asset-1.mp4"
    ).read_bytes() == (
        publication_case["project_dir"]
        / publication_case["result"]["items"][0]["storage_receipt"]["locator"]
    ).read_bytes()
    assert not (
        publication_case["project_dir"] / "artifacts" / "asset_manifest.json"
    ).exists()
    stored_command = (
        publication_case["project_dir"] / receipt["command_logical_path"]
    )
    assert json.loads(stored_command.read_text(encoding="utf-8")) == command


def test_official_in_progress_checkpoint_transitions_without_history(
    publication_case,
):
    write_checkpoint(
        publication_case["projects_root"],
        publication_case["project_id"],
        "assets",
        "in_progress",
        {},
        pipeline_type=publication_case["pipeline_type"],
        metadata={
            "batch_id": publication_case["request"]["batch_id"],
            "request_digest": publication_case["request"]["request_digest"],
            "partial_progress": {"completed_scene_ids": []},
        },
    )

    _publisher(publication_case).publish(_agent_command(publication_case))
    checkpoint = read_checkpoint(
        publication_case["projects_root"], publication_case["project_id"], "assets"
    )
    assert checkpoint["status"] == "awaiting_human"
    history = publication_case["project_dir"] / "history"
    assert not history.exists() or not list(history.glob("checkpoint_assets_*.json"))


def test_different_batch_in_progress_checkpoint_is_not_silently_superseded(
    publication_case,
):
    write_checkpoint(
        publication_case["projects_root"],
        publication_case["project_id"],
        "assets",
        "in_progress",
        {},
        pipeline_type=publication_case["pipeline_type"],
        metadata={"batch_id": "other-batch", "request_digest": "f" * 64},
    )

    with pytest.raises(M2PublicationError, match="CHECKPOINT_PUBLICATION_CONFLICT"):
        _publisher(publication_case).publish(_agent_command(publication_case))
    checkpoint = read_checkpoint(
        publication_case["projects_root"], publication_case["project_id"], "assets"
    )
    assert checkpoint["metadata"]["batch_id"] == "other-batch"


def test_completed_requires_a_separate_exact_human_reply_bound_command(
    publication_case,
):
    publisher = _publisher(publication_case)
    first_command = _agent_command(publication_case)
    first_receipt = publisher.publish(first_command)
    human_command = _human_command(publication_case, first_command, first_receipt)
    completed = publisher.publish(human_command)
    checkpoint = read_checkpoint(
        publication_case["projects_root"], publication_case["project_id"], "assets"
    )

    assert checkpoint["status"] == "completed"
    assert checkpoint["human_approved"] is True
    assert completed["checkpoint_sha256"] == canonical_sha256(checkpoint)
    history = list((publication_case["project_dir"] / "history").glob("checkpoint_assets_*.json"))
    assert len(history) == 1
    prior = json.loads(history[0].read_text(encoding="utf-8"))
    assert canonical_sha256(prior) == first_receipt["checkpoint_sha256"]
    assert prior["status"] == "awaiting_human"


def test_completed_command_cannot_be_first_or_use_mismatched_human_evidence(
    publication_case,
):
    agent = _agent_command(publication_case)
    invalid = deepcopy(agent)
    invalid["transition"] = {
        "kind": "human_approval_to_completed",
        "target_status": "completed",
        "human_approved": True,
    }
    with pytest.raises(M0ContractError, match="SCHEMA_VALIDATION_FAILED"):
        freeze_publication_command(invalid)

    first = _publisher(publication_case).publish(agent)
    human = _human_command(publication_case, agent, first)
    human["transition"]["human_approval_evidence"]["reply_sha256"] = "b" * 64
    with pytest.raises(M0ContractError, match="DIGEST"):
        validate_publication_command(human)

    human = _human_command(publication_case, agent, first)
    human["transition"]["prior_checkpoint_ref"]["sha256"] = "b" * 64
    human["transition"]["human_approval_evidence"]["prior_checkpoint_sha256"] = (
        "b" * 64
    )
    human = freeze_publication_command(human)
    with pytest.raises(M2PublicationError, match="HUMAN_APPROVAL_BINDING_INVALID"):
        _publisher(publication_case).publish(human)


def test_schema_valid_replaced_result_is_rejected_even_when_refs_are_rehashed(
    publication_case,
):
    result = deepcopy(publication_case["result"])
    result["statistics"]["retries"] += 1
    result_digest = canonical_sha256(result)
    publication_case["store"].result_path.write_bytes(canonical_json_bytes(result))
    state = deepcopy(publication_case["state"])
    state["result_ref"]["sha256"] = result_digest
    publication_case["store"].state_path.write_bytes(canonical_json_bytes(state))
    publication_case.update(
        {
            "result": result,
            "result_digest": result_digest,
            "state": state,
            "state_revision": state["revision"],
        }
    )
    command = _agent_command(publication_case)

    with pytest.raises(M2PublicationError, match="RESULT_STATE_MISMATCH"):
        _publisher(publication_case).publish(command)
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()


def test_rehashed_but_wrong_terminal_state_reference_is_rejected(
    publication_case,
):
    command = deepcopy(_agent_command(publication_case))
    command["state_ref"]["sha256"] = "b" * 64
    command = freeze_publication_command(command)

    with pytest.raises(M2PublicationError, match="PUBLICATION_STATE_REF_MISMATCH"):
        _publisher(publication_case).publish(command)
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()


def test_changed_predecessor_source_is_rejected_before_publication(publication_case):
    scene_path = publication_case["project_dir"] / "checkpoint_scene_plan.json"
    scene_checkpoint = json.loads(scene_path.read_text(encoding="utf-8"))
    scene_checkpoint["artifacts"]["scene_plan"]["scenes"][0][
        "description"
    ] = "Changed after BatchResult review."
    scene_path.write_text(json.dumps(scene_checkpoint), encoding="utf-8")

    with pytest.raises(M0ContractError, match="CHECKPOINT_EVIDENCE_MISMATCH"):
        _publisher(publication_case).publish(_agent_command(publication_case))
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()


def test_manifest_binding_cannot_change_the_request_canonical_destination(
    publication_case,
):
    command = deepcopy(_agent_command(publication_case))
    command["asset_manifest"]["assets"][0]["path"] = "assets/video/other.mp4"
    command["asset_bindings"][0]["canonical_path"] = "assets/video/other.mp4"
    command["review_evidence"]["asset_manifest_sha256"] = canonical_sha256(
        command["asset_manifest"]
    )
    command = freeze_publication_command(command)

    with pytest.raises(M2PublicationError, match="ASSET_RESULT_BINDING_INVALID"):
        _publisher(publication_case).publish(command)
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()


def test_manifest_provider_model_prompt_and_cost_are_exact_result_provenance(
    publication_case,
):
    for field, changed, match in (
        ("provider", "other-provider", "ASSET_RESULT_BINDING_INVALID"),
        ("model", "other-model", "ASSET_RESULT_BINDING_INVALID"),
        ("prompt", "rewritten prompt", "ASSET_RESULT_BINDING_INVALID"),
        ("cost_usd", 0.0, "ASSET_COST_BINDING_INVALID"),
    ):
        command = deepcopy(_agent_command(publication_case))
        command["asset_manifest"]["assets"][0][field] = changed
        command["review_evidence"]["asset_manifest_sha256"] = canonical_sha256(
            command["asset_manifest"]
        )
        command = freeze_publication_command(command)
        with pytest.raises(M2PublicationError, match=match):
            _publisher(publication_case).publish(command)
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()


def test_canonical_destination_symlink_escape_fails_before_checkpoint(
    publication_case,
    tmp_path,
):
    project = publication_case["project_dir"]
    video_dir = project / "assets" / "video"
    video_dir.rmdir()
    outside = tmp_path / "outside-assets"
    outside.mkdir()
    try:
        os.symlink(outside, video_dir, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"Directory symlinks are unavailable on this platform: {exc}")

    with pytest.raises(M2PublicationError, match="CANONICAL_PATH_ALIAS"):
        _publisher(publication_case).publish(_agent_command(publication_case))
    assert not (project / "checkpoint_assets.json").exists()
    assert not (outside / "asset-1.mp4").exists()


def test_different_existing_canonical_bytes_fail_before_checkpoint(publication_case):
    target = publication_case["project_dir"] / "assets" / "video" / "asset-1.mp4"
    target.write_bytes(b"different-existing-media")

    with pytest.raises(Exception, match="CANONICAL_ASSET_CONFLICT"):
        _publisher(publication_case).publish(_agent_command(publication_case))
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()


def test_hardlinked_canonical_destination_is_rejected_even_when_bytes_match(
    publication_case,
):
    receipt = publication_case["result"]["items"][0]["storage_receipt"]
    source = publication_case["project_dir"] / receipt["locator"]
    target = publication_case["project_dir"] / "assets" / "video" / "asset-1.mp4"
    os.link(source, target)

    with pytest.raises(M2PublicationError, match="CANONICAL_PATH_ALIAS"):
        _publisher(publication_case).publish(_agent_command(publication_case))
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()


def test_prerequisite_failure_does_not_persist_command_or_materialize_media(
    publication_case,
):
    scene_checkpoint = publication_case["project_dir"] / "checkpoint_scene_plan.json"
    scene = json.loads(scene_checkpoint.read_text(encoding="utf-8"))
    scene["status"] = "awaiting_human"
    scene["human_approved"] = False
    scene_checkpoint.write_text(json.dumps(scene), encoding="utf-8")

    with pytest.raises(M0ContractError, match="CHECKPOINT_NOT_COMPLETED"):
        _publisher(publication_case).publish(_agent_command(publication_case))
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()
    assert not publication_case["store"].publication_command_path(
        "publish-agent-001"
    ).exists()
    assert not (
        publication_case["project_dir"] / "assets" / "video" / "asset-1.mp4"
    ).exists()


@pytest.mark.parametrize(
    ("boundary", "checkpoint_exists_after_crash"),
    [
        ("publication_command_persisted", False),
        ("publication_asset_materialized", False),
        ("publication_assets_verified", False),
        ("publication_checkpoint_written", True),
        ("publication_checkpoint_verified", True),
    ],
)
def test_publication_crash_boundaries_repair_idempotently(
    publication_case, boundary, checkpoint_exists_after_crash
):
    command = _agent_command(publication_case)

    def crash_once(name, _facts):
        if name == boundary:
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash, match=boundary):
        _publisher(publication_case, crash_hook=crash_once).publish(command)

    assert (
        publication_case["project_dir"] / "checkpoint_assets.json"
    ).exists() is checkpoint_exists_after_crash

    receipt = _publisher(publication_case).publish(command)
    repeated = _publisher(publication_case).publish(command)
    checkpoint = read_checkpoint(
        publication_case["projects_root"], publication_case["project_id"], "assets"
    )
    assert receipt["checkpoint_sha256"] == canonical_sha256(checkpoint)
    assert repeated["checkpoint_sha256"] == receipt["checkpoint_sha256"]
    assert repeated["idempotent"] is True
    history = publication_case["project_dir"] / "history"
    assert not history.exists() or not list(history.glob("checkpoint_assets_*.json"))


def test_immutable_command_partial_publish_recovers_without_final_conflict(
    publication_case,
):
    command = _agent_command(publication_case)

    def interrupt(_final_path: Path, _temporary_path: Path):
        raise InjectedCrash("immutable_publication_command_publish")

    with pytest.raises(InjectedCrash, match="immutable_publication_command_publish"):
        _publisher(publication_case, immutable_publish_hook=interrupt).publish(command)

    receipt = _publisher(publication_case).publish(command)
    command_path = publication_case["project_dir"] / receipt["command_logical_path"]
    assert command_path.exists()
    assert not list(command_path.parent.glob(".*.tmp"))


def test_same_command_id_cannot_be_reauthored_after_immutable_persistence(
    publication_case,
):
    command = _agent_command(publication_case)

    def stop_after_command(name, _facts):
        if name == "publication_command_persisted":
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        _publisher(publication_case, crash_hook=stop_after_command).publish(command)
    changed = deepcopy(command)
    changed["review_evidence"]["review_reference"] = "codex:review:replacement"
    changed = freeze_publication_command(changed)

    with pytest.raises(Exception, match="PUBLICATION_COMMAND_CONFLICT"):
        _publisher(publication_case).publish(changed)
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()


def test_partial_canonical_asset_publish_repairs_before_checkpoint_authority(
    publication_case,
):
    command = _agent_command(publication_case)

    def interrupt(_final_path: Path, _temporary_path: Path):
        raise InjectedCrash("immutable_canonical_asset_publish")

    with pytest.raises(InjectedCrash, match="immutable_canonical_asset_publish"):
        _publisher(publication_case, asset_publish_hook=interrupt).publish(command)
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()
    target = publication_case["project_dir"] / "assets" / "video" / "asset-1.mp4"
    assert not target.exists()
    assert list(target.parent.glob(".asset-1.mp4.batch-v2-publication.*.tmp"))

    _publisher(publication_case).publish(command)
    assert target.exists()
    assert not list(target.parent.glob(".asset-1.mp4.batch-v2-publication.*.tmp"))
    checkpoint = read_checkpoint(
        publication_case["projects_root"], publication_case["project_id"], "assets"
    )
    assert checkpoint["artifacts"]["asset_manifest"] == command["asset_manifest"]


def test_crash_after_first_of_two_assets_leaves_no_authoritative_checkpoint(
    two_item_publication_case,
):
    case = two_item_publication_case
    command = _agent_command(case)

    def stop_after_first_asset(name, facts):
        if (
            name == "publication_asset_materialized"
            and facts["canonical_path"] == "assets/video/asset-1.mp4"
        ):
            raise InjectedCrash("after-first-canonical-asset")

    with pytest.raises(InjectedCrash, match="after-first-canonical-asset"):
        _publisher(case, crash_hook=stop_after_first_asset).publish(command)

    assert (case["project_dir"] / "assets/video/asset-1.mp4").exists()
    assert not (case["project_dir"] / "assets/video/asset-2.mp4").exists()
    assert not (case["project_dir"] / "checkpoint_assets.json").exists()

    _publisher(case).publish(command)
    assert (case["project_dir"] / "assets/video/asset-1.mp4").exists()
    assert (case["project_dir"] / "assets/video/asset-2.mp4").exists()
    assert read_checkpoint(
        case["projects_root"], case["project_id"], "assets"
    )["artifacts"]["asset_manifest"] == command["asset_manifest"]


def test_scoped_publication_suppresses_checkpoint_gcs_hook_and_preserves_legacy(
    publication_case, monkeypatch, tmp_path
):
    import lib.gcs_storage

    scheduled = []
    monkeypatch.setattr(
        lib.gcs_storage.gcs_storage, "is_auto_sync_enabled", lambda: True
    )
    monkeypatch.setattr(
        lib.gcs_storage.gcs_storage,
        "async_sync_project_assets",
        lambda project_dir: scheduled.append(project_dir),
    )
    receipt = _publisher(publication_case).publish(_agent_command(publication_case))
    checkpoint_path = publication_case["project_dir"] / "checkpoint_assets.json"
    returned_bytes = checkpoint_path.read_bytes()
    assert scheduled == []
    assert checkpoint_path.read_bytes() == returned_bytes
    assert receipt["checkpoint_sha256"] == canonical_sha256(
        json.loads(returned_bytes.decode("utf-8"))
    )

    # The legacy hook remains enabled outside the narrowly scoped V2 publisher.
    write_checkpoint(
        publication_case["projects_root"],
        publication_case["project_id"],
        "assets",
        "awaiting_human",
        {"asset_manifest": _agent_command(publication_case)["asset_manifest"]},
        pipeline_type=publication_case["pipeline_type"],
    )
    assert scheduled == [publication_case["project_dir"]]


def test_publication_scope_restores_legacy_hidden_writer_after_exception(
    publication_case, monkeypatch
):
    import lib.gcs_storage

    scheduled = []
    monkeypatch.setattr(
        lib.gcs_storage.gcs_storage, "is_auto_sync_enabled", lambda: True
    )
    monkeypatch.setattr(
        lib.gcs_storage.gcs_storage,
        "async_sync_project_assets",
        lambda project_dir: scheduled.append(project_dir),
    )

    def fail_after_command(name, _facts):
        if name == "publication_command_persisted":
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        _publisher(publication_case, crash_hook=fail_after_command).publish(
            _agent_command(publication_case)
        )
    assert scheduled == []

    write_checkpoint(
        publication_case["projects_root"],
        publication_case["project_id"],
        "assets",
        "awaiting_human",
        {"asset_manifest": _agent_command(publication_case)["asset_manifest"]},
        pipeline_type=publication_case["pipeline_type"],
    )
    assert scheduled == [publication_case["project_dir"]]


def test_publication_scope_suppresses_basetool_writers_and_restores_after_return(
    publication_case, monkeypatch
):
    import lib.events
    import lib.gcs_storage
    from tools.base_tool import BaseTool, ToolResult

    events = []
    uploads = []
    monkeypatch.setattr(lib.events, "PROJECTS_DIR", publication_case["projects_root"])
    monkeypatch.setattr(lib.events, "emit_event", lambda *args: events.append(args))
    monkeypatch.setattr(
        lib.gcs_storage.gcs_storage, "is_auto_sync_enabled", lambda: True
    )
    monkeypatch.setattr(
        lib.gcs_storage.gcs_storage,
        "async_upload_single_asset",
        lambda *args, **kwargs: uploads.append((args, kwargs)),
    )

    class DummyTool(BaseTool):
        name = "m2-hidden-writer-probe"

        def execute(self, inputs):
            Path(inputs["output_path"]).write_bytes(b"probe")
            return ToolResult(success=True, artifacts=[inputs["output_path"]])

    scoped_output = publication_case["project_dir"] / ".batch-v2" / "scope-probe.mp4"
    with publication_execution_scope():
        DummyTool().execute({"output_path": str(scoped_output)})
    assert events == []
    assert uploads == []

    legacy_output = publication_case["project_dir"] / "assets" / "legacy-probe.mp4"
    DummyTool().execute({"output_path": str(legacy_output)})
    assert len(events) == 2
    assert len(uploads) == 2


def test_worker_cannot_enter_canonical_publication_path(publication_case):
    attempt_dir = (
        publication_case["project_dir"]
        / ".batch-v2"
        / "runs"
        / publication_case["request"]["batch_id"]
        / "attempts"
        / "worker-probe"
        / "attempt-probe"
    )
    attempt_dir.mkdir(parents=True)
    with worker_execution_scope(attempt_dir):
        with pytest.raises(WorkerWriteViolation, match="WORKER_PUBLICATION_FORBIDDEN"):
            _publisher(publication_case).publish(_agent_command(publication_case))
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()


def test_publication_is_rejected_while_execution_lock_is_still_held(
    publication_case,
):
    command = _agent_command(publication_case)
    with publication_case["store"].acquire_run_lock():
        with pytest.raises(LocalRunLocked):
            _publisher(publication_case).publish(command)
    assert not (publication_case["project_dir"] / "checkpoint_assets.json").exists()


def test_checkpoint_manifest_overrides_a_stale_loose_backlot_cache(
    publication_case,
):
    command = _agent_command(publication_case)
    _publisher(publication_case).publish(command)
    loose = {
        "version": "1.0",
        "assets": [
            {
                "id": "stale",
                "type": "video",
                "path": "assets/video/stale.mp4",
                "source_tool": "legacy",
                "scene_id": "stale-scene",
            }
        ],
    }
    loose_path = publication_case["project_dir"] / "artifacts" / "asset_manifest.json"
    loose_path.write_text(json.dumps(loose), encoding="utf-8")

    board = load_board_state(publication_case["project_dir"])
    assert board["artifacts"]["asset_manifest"] == command["asset_manifest"]
    assert any(
        entry.get("artifact") == "asset_manifest"
        and entry.get("status") == "cache_mismatch_ignored"
        for entry in board["artifact_diagnostics"]
    )


@pytest.mark.parametrize(
    "metadata_mode", ["absent", "invalid_v2_tag"]
)
def test_non_v2_or_invalid_v2_checkpoint_preserves_legacy_loose_precedence(
    publication_case, metadata_mode
):
    command = _agent_command(publication_case)
    _publisher(publication_case).publish(command)
    checkpoint_path = publication_case["project_dir"] / "checkpoint_assets.json"
    checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    if metadata_mode == "absent":
        checkpoint.pop("metadata")
    else:
        checkpoint["metadata"]["batch_v2_publication"]["kind"] = "untrusted"
    checkpoint_path.write_text(json.dumps(checkpoint), encoding="utf-8")

    loose = {
        "version": "1.0",
        "assets": [
            {
                "id": "legacy-loose",
                "type": "video",
                "path": "assets/video/legacy-loose.mp4",
                "source_tool": "legacy",
                "scene_id": "legacy-scene",
            }
        ],
    }
    loose_path = publication_case["project_dir"] / "artifacts" / "asset_manifest.json"
    loose_path.write_text(json.dumps(loose), encoding="utf-8")

    board = load_board_state(publication_case["project_dir"])
    assert board["artifacts"]["asset_manifest"] == loose
    assert not any(
        entry.get("artifact") == "asset_manifest"
        and entry.get("status") == "cache_mismatch_ignored"
        for entry in board["artifact_diagnostics"]
    )


@pytest.mark.parametrize(
    ("failure_mode", "reason"),
    [
        ("missing", "batch_v2_publication_command_missing"),
        ("corrupt", "batch_v2_publication_command_corrupt"),
        ("mismatched", "batch_v2_publication_command_mismatch"),
    ],
)
def test_recognized_v2_checkpoint_fails_closed_when_command_is_not_exact(
    publication_case, failure_mode, reason
):
    command = _agent_command(publication_case)
    _publisher(publication_case).publish(command)
    checkpoint = read_checkpoint(
        publication_case["projects_root"], publication_case["project_id"], "assets"
    )
    command_path = (
        publication_case["project_dir"]
        / checkpoint["metadata"]["batch_v2_publication"]["command_logical_path"]
    )
    if failure_mode == "missing":
        command_path.unlink()
    elif failure_mode == "corrupt":
        command_path.write_text("{not-json", encoding="utf-8")
    else:
        changed = deepcopy(command)
        changed["review_evidence"]["review_reference"] = "codex:review:mismatch"
        changed = freeze_publication_command(changed)
        command_path.write_bytes(canonical_json_bytes(changed))

    loose = {
        "version": "1.0",
        "assets": [
            {
                "id": "stale-loose",
                "type": "video",
                "path": "assets/video/stale-loose.mp4",
                "source_tool": "legacy",
                "scene_id": "stale-scene",
            }
        ],
    }
    loose_path = publication_case["project_dir"] / "artifacts" / "asset_manifest.json"
    loose_path.write_text(json.dumps(loose), encoding="utf-8")

    board = load_board_state(publication_case["project_dir"])
    assert "asset_manifest" not in board["artifacts"]
    assert {
        "artifact": "asset_manifest",
        "status": "batch_v2_authority_invalid",
        "reason": reason,
    } in board["artifact_diagnostics"]
