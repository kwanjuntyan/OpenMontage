"""Prepare deterministic host fixtures for the offline Batch V2 container gate.

This helper authors no creative decisions and invokes no executor, provider, cloud,
credential, or network boundary.  It only freezes a 40-item portable request and
the two explicit runtime profiles used by the documented no-network smoke test.
"""

from __future__ import annotations

import argparse
import json
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping, Sequence

from lib.batch_executor.contracts import (
    canonical_json_bytes,
    canonical_sha256,
    exact_identity,
    freeze_batch_request,
)
from lib.batch_executor.gemini_adapter import freeze_vertex_adapter_config
from lib.checkpoint import (
    init_project,
    read_checkpoint,
    validate_checkpoint,
    write_checkpoint,
)
from lib.pipeline_loader import load_pipeline_readonly


_PROJECT_ID = "batch-v2-offline-qualification"
_PIPELINE_TYPE = "documentary-montage"
_REQUEST_CONTAINER_PATH = "/input-snapshot/config/request.json"
_PROJECTS_CONTAINER_PATH = "/workspace/projects"
_SNAPSHOT_PROJECTS_CONTAINER_PATH = "/input-snapshot/projects"
_FIXED_TIMESTAMP = "2026-09-15T00:00:00Z"


def _brief() -> dict[str, Any]:
    return {
        "version": "1.0",
        "title": "Batch V2 offline qualification",
        "hook": "A deterministic fake-only executor qualification.",
        "key_points": ["Exercise bounded concurrency and durable state semantics."],
        "tone": "casual",
        "style": "clean-professional",
        "target_platform": "youtube",
        "target_duration_seconds": 320,
    }


def _scene_plan() -> dict[str, Any]:
    return {
        "version": "1.0",
        "scenes": [
            {
                "id": "scene-1",
                "type": "talking_head",
                "description": "Deterministic offline qualification scene",
                "start_seconds": 0,
                "end_seconds": 320,
            }
        ],
    }


def _source_binding(
    *, checkpoint: Mapping[str, Any], stage: str, artifact_name: str
) -> dict[str, Any]:
    artifact = checkpoint["artifacts"][artifact_name]
    return {
        "binding_id": f"{artifact_name.replace('_', '-')}-source",
        "source_type": "checkpoint_artifact",
        "logical_path": f"checkpoint_{stage}.json",
        "sha256": canonical_sha256(artifact),
        "size_bytes": len(canonical_json_bytes(artifact)),
        "checkpoint_stage": stage,
        "artifact_name": artifact_name,
        "checkpoint_status": "completed",
        "human_approved": True,
        "storage": {
            "store_type": "local",
            "locator": f"checkpoint_{stage}.json",
        },
    }


def _runtime_config_digest(config: Mapping[str, Any]) -> str:
    candidate = deepcopy(dict(config))
    candidate.pop("config_digest", None)
    return canonical_sha256(candidate)


def _freeze_checkpoint_timestamp(
    *, projects_root: Path, project_id: str, stage: str
) -> None:
    checkpoint = read_checkpoint(projects_root, project_id, stage)
    if checkpoint is None:
        raise RuntimeError(f"Qualification checkpoint {stage!r} is missing")
    checkpoint["timestamp"] = _FIXED_TIMESTAMP
    validate_checkpoint(checkpoint, pipeline_dir=projects_root)
    (projects_root / project_id / f"checkpoint_{stage}.json").write_bytes(
        canonical_json_bytes(checkpoint)
    )


def _runtime_config(
    *, request: Mapping[str, Any], profile: str, invocation_id: str
) -> dict[str, Any]:
    adapter = freeze_vertex_adapter_config(
        {
            "version": "1.0",
            "config_digest": "0" * 64,
            "request_digest": request["request_digest"],
            "batch_id": request["batch_id"],
            "project_id": request["project_id"],
            "identity": exact_identity(),
            "vertex_project": "offline-qualification-not-a-real-project",
            "vertex_location": "global",
        }
    )
    config: dict[str, Any] = {
        "version": "1.0",
        "config_digest": "0" * 64,
        "profile": profile,
        "transport_mode": "offline_fake",
        "projects_root": _PROJECTS_CONTAINER_PATH,
        "request_uri": _REQUEST_CONTAINER_PATH,
        "request_digest": request["request_digest"],
        "observed_source_revision": deepcopy(request["source_revision"]),
        "invocation_id": invocation_id,
        "invocation_mode": "run",
        "adapter_config": adapter,
    }
    if profile == "cloud_run":
        config["cloud"] = {
            "bucket": "offline-qualification-private-bucket",
            "storage_project": "offline-qualification-storage",
            "cloud_run_project": "offline-qualification-runtime",
            "cloud_run_location": "us-central1",
            "cloud_run_job": "batch-v2",
            "input_snapshot_projects_root": _SNAPSHOT_PROJECTS_CONTAINER_PATH,
            "input_snapshot_object_prefix": (
                "batch-v2-input-snapshots/sha256/" + request["request_digest"]
            ),
        }
    config["config_digest"] = _runtime_config_digest(config)
    return config


def prepare_offline_qualification(output_root: str | Path) -> dict[str, Any]:
    """Create one deterministic, explicit, fake-only 40-item fixture tree."""

    root = Path(output_root).resolve()
    if root.exists() and any(root.iterdir()):
        raise FileExistsError("Offline qualification output root must be empty")
    root.mkdir(parents=True, exist_ok=True)
    snapshot_root = root / "input-snapshot"
    snapshot_projects = snapshot_root / "projects"
    project_dir = init_project(
        _PROJECT_ID,
        title="Batch V2 offline qualification",
        pipeline_type=_PIPELINE_TYPE,
        pipeline_dir=snapshot_projects,
    )
    marker_path = project_dir / "project.json"
    marker = json.loads(marker_path.read_text(encoding="utf-8"))
    marker["created_at"] = _FIXED_TIMESTAMP
    marker_path.write_bytes(canonical_json_bytes(marker))
    write_checkpoint(
        snapshot_projects,
        _PROJECT_ID,
        "idea",
        "completed",
        {"brief": _brief()},
        pipeline_type=_PIPELINE_TYPE,
        human_approved=True,
    )
    _freeze_checkpoint_timestamp(
        projects_root=snapshot_projects,
        project_id=_PROJECT_ID,
        stage="idea",
    )
    write_checkpoint(
        snapshot_projects,
        _PROJECT_ID,
        "scene_plan",
        "completed",
        {"scene_plan": _scene_plan()},
        pipeline_type=_PIPELINE_TYPE,
        human_approved=True,
    )
    _freeze_checkpoint_timestamp(
        projects_root=snapshot_projects,
        project_id=_PROJECT_ID,
        stage="scene_plan",
    )
    checkpoints = {
        stage: read_checkpoint(snapshot_projects, _PROJECT_ID, stage)
        for stage in ("idea", "scene_plan")
    }
    if any(checkpoint is None for checkpoint in checkpoints.values()):
        raise RuntimeError("Qualification checkpoints did not round-trip")
    typed_checkpoints = {
        stage: checkpoint
        for stage, checkpoint in checkpoints.items()
        if checkpoint is not None
    }
    bindings = [
        _source_binding(
            checkpoint=typed_checkpoints["idea"],
            stage="idea",
            artifact_name="brief",
        ),
        _source_binding(
            checkpoint=typed_checkpoints["scene_plan"],
            stage="scene_plan",
            artifact_name="scene_plan",
        ),
    ]
    estimated_cost = 0.8
    item_count = 40
    authorized_budget = estimated_cost * item_count
    request = freeze_batch_request(
        {
            "version": "1.0",
            "canonical_json": "openmontage-canonical-json-v1",
            "batch_id": "batch-v2-offline-qualification-40",
            "created_at": "2026-09-15T00:00:00Z",
            "project_id": _PROJECT_ID,
            "pipeline_type": _PIPELINE_TYPE,
            "stage": "assets",
            "request_digest": "0" * 64,
            "source_revision": {
                "kind": "content_snapshot",
                "revision": "offline-qualification-v1",
            },
            "source_bindings": bindings,
            "authorization": {
                "authorization_digest": "0" * 64,
                "manifest_sha256": canonical_sha256(
                    load_pipeline_readonly(_PIPELINE_TYPE)
                ),
                "prerequisite_checkpoints": [
                    {
                        "stage": stage,
                        "logical_path": f"checkpoint_{stage}.json",
                        "sha256": canonical_sha256(typed_checkpoints[stage]),
                        "status": "completed",
                        "human_approved": True,
                    }
                    for stage in ("idea", "scene_plan")
                ],
                "immediate_predecessor_stage": "scene_plan",
                "authorization_basis": "explicit_per_batch",
                "approval_status": "approved",
                "approval_reference": (
                    "explicit-per-batch:offline-qualification-fixture-v1"
                ),
                "approved_budget_usd": authorized_budget,
                "no_cost": False,
                "decision_refs": [],
                "allowed_identity": exact_identity(),
                "max_total_attempts": item_count,
                "max_authorized_spend_usd": authorized_budget,
                "authorized_at": "2026-09-15T00:00:00Z",
                "scope": "assets_video_batch",
            },
            "execution_policy": {
                "global_worker_cap": 3,
                "provider_concurrency_cap": 1,
                "min_request_spacing_seconds": 0,
                "retry_policy_version": "batch-v2-retry-v1",
                "max_attempts_per_item": 1,
                "max_elapsed_seconds": 3600,
                "max_attempt_cost_usd": estimated_cost,
                "reuse_policy": "verified_same_request_only",
                "failure_mode": "continue_independent",
                "heartbeat_interval_seconds": 5,
                "storage_profile": "portable",
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
                    "item_id": f"item-{index:03d}",
                    "scene_id": "scene-1",
                    "asset_id": f"asset-{index:03d}",
                    "work_item_digest": "0" * 64,
                    "identity": exact_identity(),
                    "inputs": {
                        "prompt": f"Deterministic fake qualification clip {index:03d}.",
                        "operation": "text_to_video",
                        "aspect_ratio": "16:9",
                        "duration": "8s",
                        "store": True,
                    },
                    "source_binding_ids": [
                        "brief-source",
                        "scene-plan-source",
                    ],
                    "input_references": [],
                    "output_spec": {
                        "output_name": "clip.mp4",
                        "media_kind": "video",
                        "container": "mp4",
                        "allowed_video_codecs": ["h264"],
                        "audio_expected": True,
                        "canonical_destination_intent": (
                            f"assets/video/asset-{index:03d}.mp4"
                        ),
                    },
                    "estimated_cost_usd": estimated_cost,
                    "estimated_duration_seconds": 60,
                    "charged_retry_allowance": 0,
                    "dependency_item_ids": [],
                }
                for index in range(1, item_count + 1)
            ],
        }
    )

    config_dir = snapshot_root / "config"
    config_dir.mkdir(parents=True)
    (config_dir / "request.json").write_bytes(canonical_json_bytes(request))
    for filename, profile, invocation_id in (
        ("local-runtime-config.json", "local", "offline-local-qualification"),
        ("cloud-runtime-config.json", "cloud_run", "offline-cloud-qualification"),
    ):
        (config_dir / filename).write_bytes(
            canonical_json_bytes(
                _runtime_config(
                    request=request,
                    profile=profile,
                    invocation_id=invocation_id,
                )
            )
        )

    local_project = root / "local-workspace" / "projects" / _PROJECT_ID
    shutil.copytree(project_dir, local_project)
    (root / "cloud-workspace" / "projects").mkdir(parents=True)
    return {
        "version": "1.0",
        "mode": "offline_fake_non_production",
        "item_count": item_count,
        "request_digest": request["request_digest"],
        "input_snapshot": str(snapshot_root),
        "local_workspace": str(root / "local-workspace"),
        "cloud_workspace": str(root / "cloud-workspace"),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="batch_v2_prepare_offline_qualification")
    parser.add_argument("command", choices=("prepare",))
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args(argv)
    summary = prepare_offline_qualification(args.output_root)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


__all__ = ["main", "prepare_offline_qualification"]
