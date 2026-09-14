from __future__ import annotations

from copy import deepcopy

import pytest

from lib.batch_executor.contracts import (
    canonical_json_bytes,
    canonical_sha256,
    compute_idempotency_digest,
    exact_identity,
    freeze_batch_request,
)
from lib.checkpoint import init_project, read_checkpoint, write_checkpoint
from lib.pipeline_loader import load_pipeline_readonly
from tests.contracts.test_phase0_contracts import sample_artifact


@pytest.fixture()
def authorized_project(tmp_path):
    project_id = "batch-project"
    pipeline_type = "documentary-montage"
    project_dir = init_project(
        project_id,
        title="Batch V2 contract fixture",
        pipeline_type=pipeline_type,
        pipeline_dir=tmp_path,
    )
    write_checkpoint(
        tmp_path,
        project_id,
        "idea",
        "completed",
        {"brief": sample_artifact("brief")},
        pipeline_type=pipeline_type,
        human_approved=True,
    )
    write_checkpoint(
        tmp_path,
        project_id,
        "scene_plan",
        "completed",
        {"scene_plan": sample_artifact("scene_plan")},
        pipeline_type=pipeline_type,
        human_approved=True,
    )
    return {
        "projects_root": tmp_path,
        "project_dir": project_dir,
        "project_id": project_id,
        "pipeline_type": pipeline_type,
    }


@pytest.fixture()
def source_revision():
    return {"kind": "git_commit", "revision": "a" * 40}


@pytest.fixture()
def qualified_adapter_observation():
    return {
        "identity": exact_identity(),
        "route_binding": "explicit_request",
        "credential_mode": "adc",
        "hidden_writers": "disabled",
        "available": True,
    }


@pytest.fixture()
def batch_request(authorized_project, source_revision):
    root = authorized_project["projects_root"]
    project_id = authorized_project["project_id"]
    pipeline_type = authorized_project["pipeline_type"]
    checkpoints = {
        stage: read_checkpoint(root, project_id, stage)
        for stage in ("idea", "scene_plan")
    }
    source_bindings = []
    for binding_id, stage, artifact_name in (
        ("brief-source", "idea", "brief"),
        ("scene-plan-source", "scene_plan", "scene_plan"),
    ):
        checkpoint = checkpoints[stage]
        artifact = checkpoint["artifacts"][artifact_name]
        payload = canonical_json_bytes(artifact)
        source_bindings.append(
            {
                "binding_id": binding_id,
                "source_type": "checkpoint_artifact",
                "logical_path": f"checkpoint_{stage}.json",
                "sha256": canonical_sha256(artifact),
                "size_bytes": len(payload),
                "checkpoint_stage": stage,
                "artifact_name": artifact_name,
                "checkpoint_status": "completed",
                "human_approved": True,
                "storage": {
                    "store_type": "local",
                    "locator": f"checkpoint_{stage}.json",
                },
            }
        )
    request = {
        "version": "1.0",
        "canonical_json": "openmontage-canonical-json-v1",
        "batch_id": "batch-001",
        "created_at": "2026-09-14T08:00:00Z",
        "project_id": project_id,
        "pipeline_type": pipeline_type,
        "stage": "assets",
        "request_digest": "0" * 64,
        "source_revision": deepcopy(source_revision),
        "source_bindings": source_bindings,
        "authorization": {
            "authorization_digest": "0" * 64,
            "manifest_sha256": canonical_sha256(load_pipeline_readonly(pipeline_type)),
            "prerequisite_checkpoints": [
                {
                    "stage": stage,
                    "logical_path": f"checkpoint_{stage}.json",
                    "sha256": canonical_sha256(checkpoints[stage]),
                    "status": "completed",
                    "human_approved": True,
                }
                for stage in ("idea", "scene_plan")
            ],
            "immediate_predecessor_stage": "scene_plan",
            "authorization_basis": "explicit_per_batch",
            "approval_status": "approved",
            "approval_reference": "explicit-per-batch:delegation:batch-v2-m0",
            "approved_budget_usd": 1.0,
            "no_cost": False,
            "decision_refs": [],
            "allowed_identity": exact_identity(),
            "max_total_attempts": 1,
            "max_authorized_spend_usd": 1.0,
            "authorized_at": "2026-09-14T08:00:00Z",
            "scope": "assets_video_batch",
        },
        "execution_policy": {
            "global_worker_cap": 3,
            "provider_concurrency_cap": 1,
            "min_request_spacing_seconds": 0,
            "retry_policy_version": "batch-v2-retry-v1",
            "max_attempts_per_item": 1,
            "max_elapsed_seconds": 3600,
            "max_attempt_cost_usd": 1.0,
            "reuse_policy": "verified_same_request_only",
            "failure_mode": "continue_independent",
            "heartbeat_interval_seconds": 5,
            "storage_profile": "local",
            "cancellation_policy": "stop_new_dispatch",
            "side_effect_policy": {
                "tool_output_mode": "project_scoped_attempt_staging_only",
                "legacy_gcs_auto_sync": False,
                "project_event_writes": False,
                "canonical_writes": False,
            },
        },
        "work_items": [
            {
                "item_id": "item-001",
                "scene_id": "scene-1",
                "asset_id": "asset-1",
                "work_item_digest": "0" * 64,
                "identity": exact_identity(),
                "inputs": {
                    "prompt": "One approved cinematic shot of a clockwork globe.",
                    "operation": "text_to_video",
                    "aspect_ratio": "16:9",
                    "duration": "8s",
                    "store": True,
                },
                "source_binding_ids": ["brief-source", "scene-plan-source"],
                "input_references": [],
                "output_spec": {
                    "output_name": "clip.mp4",
                    "media_kind": "video",
                    "container": "mp4",
                    "allowed_video_codecs": ["h264"],
                    "audio_expected": True,
                    "canonical_destination_intent": "assets/video/asset-1.mp4",
                },
                "estimated_cost_usd": 0.8,
                "estimated_duration_seconds": 60,
                "charged_retry_allowance": 0,
                "dependency_item_ids": [],
            }
        ],
    }
    return freeze_batch_request(request)


@pytest.fixture()
def cloud_owner():
    return {
        "version": "1.0",
        "batch_id": "batch-001",
        "request_digest": "a" * 64,
        "invocation_id": "invocation-old",
        "invocation_mode": "run",
        "profile": "cloud_run",
        "execution_id": "projects/p/locations/r/jobs/j/executions/old",
        "task_id": "0",
        "owner_status": "active",
        "acquired_at": "2026-09-14T08:00:00Z",
        "state_revision": 7,
        "base_state_generation": 21,
    }


def make_paid_running_attempt(*, acceptance="unknown"):
    work_item_digest = "d" * 64
    return {
        "version": "1.0",
        "batch_id": "batch-001",
        "request_digest": "a" * 64,
        "item_id": "item-001",
        "attempt_id": "attempt-001",
        "work_item_digest": work_item_digest,
        "idempotency_digest": compute_idempotency_digest("a" * 64, work_item_digest),
        "identity": exact_identity(),
        "dispatch_sequence": 1,
        "phase": "dispatched",
        "timestamps": {
            "queued_at": "2026-09-14T08:01:00Z",
            "dispatched_at": "2026-09-14T08:01:01Z",
        },
        "acceptance_knowledge": acceptance,
        "billing_mode": "paid",
        "retry_decision": "none",
        "cost": {
            "estimated_usd": 0.8,
            "reserved_usd": 0.8,
            "known_actual_usd": 0,
            "potentially_charged_usd": 0.8,
        },
    }
