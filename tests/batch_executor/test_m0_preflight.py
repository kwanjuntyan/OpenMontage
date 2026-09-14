from __future__ import annotations

import json
from copy import deepcopy

import pytest

from lib.batch_executor.contracts import M0ContractError, freeze_batch_request
from lib.batch_executor.preflight import (
    _validate_clp_binding,
    _validate_proposal_approval,
    preflight_batch_request,
)


class FakePaidTool:
    def __init__(self):
        self.calls = 0

    def execute(self):
        self.calls += 1


def _preflight(batch_request, authorized_project, source_revision, observation):
    return preflight_batch_request(
        batch_request,
        projects_root=authorized_project["projects_root"],
        observed_source_revision=source_revision,
        adapter_observation=observation,
    )


def test_valid_project_source_gate_budget_and_exact_identity_preflight(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    facts = _preflight(
        batch_request,
        authorized_project,
        source_revision,
        qualified_adapter_observation,
    )
    assert facts.project_dir == authorized_project["project_dir"].resolve()
    assert facts.prerequisite_stages == ("idea", "scene_plan")
    assert facts.source_binding_ids == ("brief-source", "scene-plan-source")
    assert facts.work_item_ids == ("item-001",)
    assert facts.request_digest == batch_request["request_digest"]


@pytest.mark.parametrize(
    ("mutate", "error_code"),
    [
        (
            lambda request: request["authorization"].update(
                {"manifest_sha256": "f" * 64}
            ),
            "PIPELINE_MANIFEST_MISMATCH",
        ),
        (
            lambda request: request["authorization"].update(
                {"immediate_predecessor_stage": "idea"}
            ),
            "IMMEDIATE_PREDECESSOR_MISMATCH",
        ),
        (
            lambda request: request["authorization"]["prerequisite_checkpoints"].reverse(),
            "PREREQUISITE_CHAIN_MISMATCH",
        ),
        (
            lambda request: request["authorization"].update(
                {"approval_status": "approved_with_changes"}
            ),
            "APPROVAL_CHANGE_UNBOUND",
        ),
    ],
)
def test_stale_or_incomplete_authorization_blocks_before_fake_tool(
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
    mutate,
    error_code,
):
    request = deepcopy(batch_request)
    mutate(request)
    request = freeze_batch_request(request)
    tool = FakePaidTool()
    with pytest.raises(M0ContractError, match=error_code):
        _preflight(request, authorized_project, source_revision, qualified_adapter_observation)
    assert tool.calls == 0


def test_stale_source_digest_blocks_before_fake_tool(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    request = deepcopy(batch_request)
    request["source_bindings"][1]["sha256"] = "f" * 64
    request = freeze_batch_request(request)
    tool = FakePaidTool()
    with pytest.raises(M0ContractError, match="SOURCE_BINDING_MISMATCH"):
        _preflight(request, authorized_project, source_revision, qualified_adapter_observation)
    assert tool.calls == 0


def test_tampered_human_gate_fails_official_checkpoint_validation(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    checkpoint_path = authorized_project["project_dir"] / "checkpoint_scene_plan.json"
    checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    checkpoint["human_approved"] = False
    checkpoint_path.write_text(json.dumps(checkpoint), encoding="utf-8")

    with pytest.raises(M0ContractError, match="CHECKPOINT_VALIDATION_FAILED"):
        _preflight(
            batch_request,
            authorized_project,
            source_revision,
            qualified_adapter_observation,
        )


def test_source_revision_mismatch_blocks_before_adapter_or_tool(
    batch_request, authorized_project, qualified_adapter_observation
):
    with pytest.raises(M0ContractError, match="SOURCE_REVISION_MISMATCH"):
        _preflight(
            batch_request,
            authorized_project,
            {"kind": "git_commit", "revision": "b" * 40},
            qualified_adapter_observation,
        )


def test_adapter_route_or_adc_mismatch_blocks_without_fallback(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    observation = deepcopy(qualified_adapter_observation)
    observation["identity"]["route"] = "developer_interactions"
    observation["credential_mode"] = "api_key"
    observation["fallback"] = "some_other_model"
    with pytest.raises(M0ContractError, match="ADAPTER_NOT_QUALIFIED") as caught:
        _preflight(batch_request, authorized_project, source_revision, observation)
    assert "EXACT_IDENTITY_MISMATCH" in str(caught.value)
    assert "ADC_REQUIRED" in str(caught.value)


def test_budget_overrun_is_rejected_during_request_freeze_before_any_call(batch_request):
    request = deepcopy(batch_request)
    request["authorization"]["approved_budget_usd"] = 0.5
    request["authorization"]["max_authorized_spend_usd"] = 0.5
    tool = FakePaidTool()
    with pytest.raises(M0ContractError, match="BUDGET_AUTHORIZATION_EXCEEDED"):
        freeze_batch_request(request)
    assert tool.calls == 0


def test_preflight_ignores_ambient_api_keys_and_never_derives_route(
    monkeypatch,
    batch_request,
    authorized_project,
    source_revision,
    qualified_adapter_observation,
):
    monkeypatch.setenv("GEMINI_API_KEY", "ambient-developer-key-must-not-select-route")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "C:/ambient/key.json")
    facts = _preflight(
        batch_request,
        authorized_project,
        source_revision,
        qualified_adapter_observation,
    )
    assert facts.request_digest == batch_request["request_digest"]


def test_project_marker_is_mandatory_and_exact(
    batch_request, authorized_project, source_revision, qualified_adapter_observation
):
    marker = authorized_project["project_dir"] / "project.json"
    data = json.loads(marker.read_text(encoding="utf-8"))
    data["project_id"] = "other-project"
    marker.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(M0ContractError, match="PROJECT_MARKER_MISMATCH"):
        _preflight(
            batch_request,
            authorized_project,
            source_revision,
            qualified_adapter_observation,
        )


def test_pipeline_using_clp_requires_exact_scene_plan_to_shot_binding_digest():
    bindings = [
        {
            "source_type": "checkpoint_artifact",
            "artifact_name": "scene_plan",
            "sha256": "a" * 64,
        },
        {
            "source_type": "checkpoint_artifact",
            "artifact_name": "clp_shot_bindings",
            "sha256": "b" * 64,
        },
    ]
    with pytest.raises(M0ContractError, match="CLP_BINDING_MISMATCH"):
        _validate_clp_binding({"scene_plan", "clp_shot_bindings"}, bindings)
    bindings[0]["clp_binding_digest"] = "b" * 64
    _validate_clp_binding({"scene_plan", "clp_shot_bindings"}, bindings)


def test_proposal_cost_gate_must_match_frozen_approval_and_bind_changes():
    checkpoints = {
        "proposal": {
            "artifacts": {
                "proposal_packet": {"approval": {"status": "approved_with_changes"}}
            }
        }
    }
    authorization = {"approval_status": "approved", "decision_refs": []}
    with pytest.raises(M0ContractError, match="PROPOSAL_APPROVAL_MISMATCH"):
        _validate_proposal_approval(checkpoints, authorization)
    authorization["approval_status"] = "approved_with_changes"
    with pytest.raises(M0ContractError, match="APPROVAL_CHANGE_UNBOUND"):
        _validate_proposal_approval(checkpoints, authorization)
    authorization["decision_refs"] = [{"decision_id": "change-1", "sha256": "c" * 64}]
    _validate_proposal_approval(checkpoints, authorization)
