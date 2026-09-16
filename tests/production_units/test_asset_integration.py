from __future__ import annotations

from copy import deepcopy

import pytest

from lib.batch_executor.contracts import (
    canonical_json_bytes,
    canonical_sha256,
    exact_identity,
    freeze_batch_request,
)
from lib.batch_executor.engine import LocalBatchExecutor
from lib.batch_executor.media_validation import DeterministicFakeMediaValidator
from lib.batch_executor.testing import FakeClock, ScriptedFakeProvider
from lib.checkpoint import init_project, read_checkpoint, write_checkpoint
from lib.clp_validator import canonical_digest
from lib.pipeline_loader import load_pipeline_readonly
from lib.production_units.assets import (
    AssetBatchIntegrationError,
    bind_batch_result,
    build_asset_units,
    compile_asset_batch_request,
    run_asset_units,
)
from tests.contracts.test_phase0_contracts import sample_artifact
from tests.batch_executor import conftest as batch_fixtures


@pytest.fixture
def authorized_project(tmp_path):
    return batch_fixtures.authorized_project.__wrapped__(tmp_path)


@pytest.fixture
def source_revision():
    return batch_fixtures.source_revision.__wrapped__()


@pytest.fixture
def qualified_adapter_observation():
    return batch_fixtures.qualified_adapter_observation.__wrapped__()


@pytest.fixture
def batch_request(authorized_project, source_revision):
    return batch_fixtures.batch_request.__wrapped__(authorized_project, source_revision)


def _asset_sources(project_id: str):
    scene_plan = {
        "version": "1.0",
        "style_playbook": "explainer-teacher",
        "scenes": [
            {
                "id": "scene-1",
                "type": "generated",
                "description": "Animated request key moving through a service",
                "start_seconds": 0,
                "end_seconds": 8,
                "required_assets": [
                    {
                        "type": "video",
                        "description": "request key animation",
                        "source": "generate",
                    }
                ],
            }
        ],
    }
    clp_manifest = {
        "version": "2.0",
        "project_id": project_id,
        "characters": [],
        "locations": [],
        "props": [],
    }
    bindings = {
        "version": "2.0",
        "project_id": project_id,
        "source_scene_plan_sha256": canonical_digest(scene_plan),
        "clp_manifest_sha256": canonical_digest(clp_manifest),
        "bindings": [{"shot_id": "scene-1"}],
    }
    return scene_plan, clp_manifest, bindings


def _animated_base_request(tmp_path, batch_request, scene_plan, clp_manifest, bindings):
    root = tmp_path
    project_id = "pup-asset-course"
    pipeline_type = "animated-explainer"
    init_project(
        project_id,
        title="PUP asset integration",
        pipeline_type=pipeline_type,
        pipeline_dir=root,
    )
    research = sample_artifact("research_brief")
    proposal = sample_artifact("proposal_packet")
    proposal["approval"]["approved_budget_usd"] = 1.0
    script = {
        "version": "1.0",
        "title": "PUP asset integration",
        "total_duration_seconds": 8,
        "sections": [
            {
                "id": "section-1",
                "text": "A stable key makes the retry safe.",
                "start_seconds": 0,
                "end_seconds": 8,
            }
        ],
    }
    provider_selection = f"identity-sha256:{canonical_sha256(exact_identity())}"
    decisions = {
        "version": "1.0",
        "project_id": project_id,
        "decisions": [
            {
                "decision_id": "decision-provider",
                "stage": "proposal",
                "category": "provider_selection",
                "subject": "Batch V2 video provider",
                "options_considered": [
                    {
                        "option_id": provider_selection,
                        "label": "Frozen Batch V2 identity",
                        "score": 1.0,
                        "reason": "Exact qualified route",
                    }
                ],
                "selected": provider_selection,
                "reason": "Exact qualified route",
                "user_approved": True,
            },
            {
                "decision_id": "decision-budget",
                "stage": "proposal",
                "category": "budget_tradeoff",
                "subject": "Batch budget",
                "options_considered": [
                    {
                        "option_id": "approved-budget-usd:1",
                        "label": "One dollar",
                        "score": 1.0,
                        "reason": "Covers the single fake work item",
                    }
                ],
                "selected": "approved-budget-usd:1",
                "reason": "Covers the single fake work item",
                "user_approved": True,
            },
        ],
    }
    write_checkpoint(
        root,
        project_id,
        "research",
        "completed",
        {"research_brief": research},
        pipeline_type=pipeline_type,
        human_approved=False,
    )
    write_checkpoint(
        root,
        project_id,
        "proposal",
        "completed",
        {"proposal_packet": proposal, "decision_log": decisions},
        pipeline_type=pipeline_type,
        human_approved=True,
    )
    write_checkpoint(
        root,
        project_id,
        "script",
        "completed",
        {"script": script},
        pipeline_type=pipeline_type,
        human_approved=True,
    )
    candidates = {
        "version": "2.0",
        "project_id": project_id,
        "source_script_sha256": canonical_digest(script),
        "candidates": {"characters": [], "locations": [], "props": []},
    }
    write_checkpoint(
        root,
        project_id,
        "clp",
        "completed",
        {"clp_manifest": clp_manifest, "clp_candidates": candidates},
        pipeline_type=pipeline_type,
        human_approved=True,
    )
    write_checkpoint(
        root,
        project_id,
        "scene_plan",
        "completed",
        {"scene_plan": scene_plan, "clp_shot_bindings": bindings},
        pipeline_type=pipeline_type,
        human_approved=True,
    )
    request = deepcopy(batch_request)
    request.update(project_id=project_id, pipeline_type=pipeline_type)
    artifact_sources = [
        ("script-source", "script", "script", script, True),
        ("clp-manifest-source", "clp", "clp_manifest", clp_manifest, True),
        ("scene-plan-source", "scene_plan", "scene_plan", scene_plan, True),
        (
            "clp-shot-binding-source",
            "scene_plan",
            "clp_shot_bindings",
            bindings,
            True,
        ),
    ]
    request["source_bindings"] = []
    for binding_id, stage, artifact_name, artifact, approved in artifact_sources:
        payload = canonical_json_bytes(artifact)
        entry = {
            "binding_id": binding_id,
            "source_type": "checkpoint_artifact",
            "logical_path": f"checkpoint_{stage}.json",
            "sha256": canonical_sha256(artifact),
            "size_bytes": len(payload),
            "checkpoint_stage": stage,
            "artifact_name": artifact_name,
            "checkpoint_status": "completed",
            "human_approved": approved,
            "storage": {
                "store_type": "local",
                "locator": f"checkpoint_{stage}.json",
            },
        }
        if artifact_name == "scene_plan":
            entry["clp_binding_digest"] = canonical_sha256(bindings)
        request["source_bindings"].append(entry)
    checkpoints = [
        read_checkpoint(root, project_id, stage)
        for stage in ("research", "proposal", "script", "clp", "scene_plan")
    ]
    decision_log = checkpoints[1]["artifacts"]["decision_log"]
    request["authorization"].update(
        manifest_sha256=canonical_sha256(load_pipeline_readonly(pipeline_type)),
        prerequisite_checkpoints=[
            {
                "stage": checkpoint["stage"],
                "logical_path": f"checkpoint_{checkpoint['stage']}.json",
                "sha256": canonical_sha256(checkpoint),
                "status": "completed",
                "human_approved": checkpoint.get("human_approved", False),
            }
            for checkpoint in checkpoints
        ],
        immediate_predecessor_stage="scene_plan",
        authorization_basis="validated_proposal_checkpoint",
        approval_status="approved",
        approval_reference="checkpoint:proposal:proposal_packet",
        approved_budget_usd=1.0,
        max_authorized_spend_usd=1.0,
        decision_refs=[
            {
                "decision_id": decision["decision_id"],
                "sha256": canonical_sha256(decision),
            }
            for decision in decision_log["decisions"]
        ],
    )
    request["work_items"][0]["source_binding_ids"] = [
        item[0] for item in artifact_sources
    ]
    return freeze_batch_request(request), {
        "projects_root": root,
        "project_id": project_id,
        "project_dir": root / project_id,
        "pipeline_type": pipeline_type,
    }


def _spec(unit_id: str):
    return {
        "item_id": "course-video-001",
        "asset_id": "asset-course-video-001",
        "scene_id": "scene-1",
        "required_asset_index": 0,
        "unit_id": unit_id,
        "inputs": {
            "prompt": "Animated blue request key K moving through one service boundary.",
            "operation": "text_to_video",
            "aspect_ratio": "16:9",
            "duration": "8s",
            "store": True,
        },
        "output_spec": {
            "output_name": "course-video-001.mp4",
            "media_kind": "video",
            "container": "mp4",
            "allowed_video_codecs": ["h264"],
            "audio_expected": True,
            "canonical_destination_intent": "assets/video/asset-course-video-001.mp4",
        },
        "estimated_cost_usd": 0.8,
        "estimated_duration_seconds": 60,
        "charged_retry_allowance": 0,
        "dependency_asset_ids": [],
    }


def _compilation(tmp_path, batch_request):
    scene, clp, bindings = _asset_sources("pup-asset-course")
    base, project = _animated_base_request(
        tmp_path, batch_request, scene, clp, bindings
    )
    units = build_asset_units(scene, clp, bindings)
    compiled = compile_asset_batch_request(
        base,
        scene_plan=scene,
        clp_manifest=clp,
        clp_shot_bindings=bindings,
        units=units,
        asset_specs=[_spec(units[0]["unit_id"])],
    )
    return scene, clp, bindings, units, compiled, project


def test_compiler_reuses_exact_batch_contract_without_publication(
    tmp_path, batch_request
) -> None:
    _, _, _, units, compilation, _ = _compilation(tmp_path, batch_request)
    request = compilation["batch_request"]
    receipt = compilation["adapter_receipt"]
    assert request["work_items"][0]["identity"]["provider"] == "gemini_omni"
    assert request["work_items"][0]["source_binding_ids"] == [
        "script-source",
        "clp-manifest-source",
        "scene-plan-source",
        "clp-shot-binding-source",
    ]
    assert receipt["unit_plan_sha256"] == canonical_digest(units)
    assert receipt["batch_request_digest"] == request["request_digest"]
    assert "publication_command" not in compilation


def test_compiled_request_runs_end_to_end_with_no_network_fake(
    batch_request,
    tmp_path,
    source_revision,
    qualified_adapter_observation,
) -> None:
    _, _, _, _, compilation, project = _compilation(tmp_path, batch_request)
    provider = ScriptedFakeProvider()
    executor = LocalBatchExecutor(
        projects_root=project["projects_root"],
        provider=provider,
        media_validator=DeterministicFakeMediaValidator(),
        clock=FakeClock(),
    )
    result = executor.run(
        compilation["batch_request"],
        observed_source_revision=source_revision,
        adapter_observation=qualified_adapter_observation,
        invocation_id="pup-m3-offline",
    )
    bound = bind_batch_result(compilation, result)
    assert result["outcome"] == "all_succeeded"
    assert provider.submit_calls == 1
    assert bound["publication_authority"] == "batch_v2_only"
    assert bound["selected_results"][0]["state"] == "committed"


@pytest.mark.parametrize(
    ("mutate", "code"),
    [
        (
            lambda base, units, specs: base["source_bindings"][1].update(
                clp_binding_digest="0" * 64
            ),
            "INVALID_BASE_BATCH_REQUEST",
        ),
        (lambda base, units, specs: specs.clear(), "ASSET_COVERAGE"),
        (
            lambda base, units, specs: specs[0].update(unit_id="asset-unit-9999"),
            "UNIT_OWNERSHIP_VIOLATION",
        ),
    ],
)
def test_compiler_fails_closed_before_batch_execution(
    tmp_path, batch_request, mutate, code: str
) -> None:
    scene, clp, bindings = _asset_sources("pup-asset-course")
    base, _ = _animated_base_request(
        tmp_path, batch_request, scene, clp, bindings
    )
    units = build_asset_units(scene, clp, bindings)
    specs = [_spec(units[0]["unit_id"])]
    mutate(base, units, specs)
    with pytest.raises(AssetBatchIntegrationError) as caught:
        compile_asset_batch_request(
            base,
            scene_plan=scene,
            clp_manifest=clp,
            clp_shot_bindings=bindings,
            units=units,
            asset_specs=specs,
        )
    assert caught.value.code == code


def test_batch_result_must_bind_exact_request(
    batch_request,
    tmp_path,
    source_revision,
    qualified_adapter_observation,
) -> None:
    _, _, _, _, compilation, project = _compilation(tmp_path, batch_request)
    executor = LocalBatchExecutor(
        projects_root=project["projects_root"],
        provider=ScriptedFakeProvider(),
        media_validator=DeterministicFakeMediaValidator(),
        clock=FakeClock(),
    )
    result = executor.run(
        compilation["batch_request"],
        observed_source_revision=source_revision,
        adapter_observation=qualified_adapter_observation,
        invocation_id="pup-m3-tamper",
    )
    changed = deepcopy(result)
    changed["request_digest"] = "0" * 64
    with pytest.raises(AssetBatchIntegrationError) as caught:
        bind_batch_result(compilation, changed)
    assert caught.value.code == "STALE_BATCH_RESULT"


def test_asset_mode_off_is_strict_noop() -> None:
    assert run_asset_units(mode="off", scene_plan={"bad": object()}) is None
