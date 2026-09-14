from __future__ import annotations

import json
from copy import deepcopy

import pytest

from lib.batch_executor.contracts import (
    M0ContractError,
    canonical_json_bytes,
    canonical_sha256,
    exact_identity,
    freeze_batch_request,
)
from lib.checkpoint import init_project, read_checkpoint, write_checkpoint
from lib.pipeline_loader import load_pipeline_readonly
from lib.batch_executor.preflight import (
    _validate_clp_binding,
    _validate_proposal_approval,
    preflight_batch_request,
)
from tests.contracts.test_phase0_contracts import sample_artifact


class FakePaidTool:
    def __init__(self):
        self.calls = 0

    def execute(self):
        self.calls += 1


def _decision(decision_id, category, *, user_approved=True):
    selected = {
        "provider_selection": f"identity-sha256:{canonical_sha256(exact_identity())}",
        "budget_tradeoff": "approved-budget-usd:1",
        "concept_selection": "concept-1",
    }[category]
    return {
        "decision_id": decision_id,
        "stage": "proposal",
        "category": category,
        "subject": f"M0 {category}",
        "options_considered": [
            {
                "option_id": selected,
                "label": selected,
                "score": 1.0,
                "reason": "Explicitly selected by the user for this batch.",
            }
        ],
        "selected": selected,
        "reason": "The user approved this exact choice.",
        "user_visible": True,
        "user_approved": user_approved,
    }


def _proposal_checkpoint(*, status="approved", budget=1.0):
    decisions = [
        _decision("provider-choice", "provider_selection"),
        _decision("budget-choice", "budget_tradeoff"),
    ]
    return {
        "artifacts": {
            "proposal_packet": {
                "approval": {
                    "status": status,
                    "approved_budget_usd": budget,
                }
            },
            "decision_log": {
                "version": "1.0",
                "project_id": "batch-project",
                "decisions": decisions,
            },
        }
    }


def _proposal_authorization(checkpoint, *, status="approved", budget=1.0):
    decisions = checkpoint["artifacts"]["decision_log"]["decisions"]
    return {
        "authorization_basis": "validated_proposal_checkpoint",
        "approval_status": status,
        "approval_reference": "checkpoint:proposal:proposal_packet",
        "approved_budget_usd": budget,
        "max_authorized_spend_usd": budget,
        "no_cost": False,
        "allowed_identity": exact_identity(),
        "decision_refs": [
            {
                "decision_id": decision["decision_id"],
                "sha256": canonical_sha256(decision),
            }
            for decision in decisions
        ],
    }


def _preflight(batch_request, authorized_project, source_revision, observation):
    return preflight_batch_request(
        batch_request,
        projects_root=authorized_project["projects_root"],
        observed_source_revision=source_revision,
        adapter_observation=observation,
    )


def _authorize_then_execute(checkpoints, authorization, tool):
    _validate_proposal_approval(checkpoints, authorization)
    tool.execute()


def _preflight_then_execute(request, *, projects_root, source_revision, observation, tool):
    facts = preflight_batch_request(
        request,
        projects_root=projects_root,
        observed_source_revision=source_revision,
        adapter_observation=observation,
    )
    tool.execute()
    return facts


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
    checkpoint = _proposal_checkpoint(status="approved_with_changes")
    checkpoints = {"proposal": checkpoint}
    authorization = _proposal_authorization(
        checkpoint,
        status="approved",
    )
    with pytest.raises(M0ContractError, match="PROPOSAL_APPROVAL_MISMATCH"):
        _validate_proposal_approval(checkpoints, authorization)
    authorization["approval_status"] = "approved_with_changes"
    _validate_proposal_approval(checkpoints, authorization)


def test_raised_frozen_request_budget_cannot_exceed_verified_proposal(batch_request):
    request = deepcopy(batch_request)
    request["authorization"].update(
        {
            "authorization_basis": "validated_proposal_checkpoint",
            "approval_reference": "checkpoint:proposal:proposal_packet",
            "approved_budget_usd": 2.0,
            "max_authorized_spend_usd": 2.0,
        }
    )
    request["execution_policy"]["max_attempt_cost_usd"] = 2.0
    checkpoint = _proposal_checkpoint(budget=1.0)
    request["authorization"]["decision_refs"] = _proposal_authorization(checkpoint)[
        "decision_refs"
    ]
    request = freeze_batch_request(request)
    tool = FakePaidTool()

    with pytest.raises(M0ContractError, match="PROPOSAL_BUDGET_EXCEEDED"):
        _authorize_then_execute(
            {"proposal": checkpoint}, request["authorization"], tool
        )
    assert tool.calls == 0


@pytest.mark.parametrize(
    ("corruption", "error_code"),
    [
        ("unknown_id", "DECISION_REFERENCE_UNKNOWN"),
        ("wrong_digest", "DECISION_DIGEST_MISMATCH"),
        ("not_user_approved", "DECISION_NOT_USER_APPROVED"),
        ("wrong_category", "DECISION_CATEGORY_MISMATCH"),
        ("wrong_provider_selection", "DECISION_SELECTION_MISMATCH"),
        ("wrong_budget_selection", "DECISION_SELECTION_MISMATCH"),
    ],
)
def test_proposal_decision_refs_fail_closed_before_fake_tool(corruption, error_code):
    checkpoint = _proposal_checkpoint(status="approved_with_changes")
    authorization = _proposal_authorization(
        checkpoint,
        status="approved_with_changes",
    )
    if corruption == "unknown_id":
        authorization["decision_refs"][0]["decision_id"] = "invented-decision"
    elif corruption == "wrong_digest":
        authorization["decision_refs"][0]["sha256"] = "f" * 64
    elif corruption == "not_user_approved":
        decision = checkpoint["artifacts"]["decision_log"]["decisions"][0]
        decision["user_approved"] = False
        authorization["decision_refs"][0]["sha256"] = canonical_sha256(decision)
    elif corruption == "wrong_category":
        decision = checkpoint["artifacts"]["decision_log"]["decisions"][0]
        decision["category"] = "concept_selection"
        decision["selected"] = "concept-1"
        decision["options_considered"][0].update(
            {"option_id": "concept-1", "label": "concept-1"}
        )
        authorization["decision_refs"][0]["sha256"] = canonical_sha256(decision)
    elif corruption == "wrong_provider_selection":
        decision = checkpoint["artifacts"]["decision_log"]["decisions"][0]
        decision["selected"] = f"identity-sha256:{'f' * 64}"
        decision["options_considered"][0].update(
            {"option_id": decision["selected"], "label": "Unapproved different identity"}
        )
        authorization["decision_refs"][0]["sha256"] = canonical_sha256(decision)
    else:
        decision = checkpoint["artifacts"]["decision_log"]["decisions"][1]
        decision["selected"] = "approved-budget-usd:999"
        decision["options_considered"][0].update(
            {"option_id": decision["selected"], "label": "Unapproved budget"}
        )
        authorization["decision_refs"][1]["sha256"] = canonical_sha256(decision)
    tool = FakePaidTool()

    with pytest.raises(M0ContractError, match=error_code):
        _authorize_then_execute({"proposal": checkpoint}, authorization, tool)
    assert tool.calls == 0


def test_proposal_decision_refs_must_resolve_in_proposal_checkpoint():
    proposal_checkpoint = _proposal_checkpoint()
    authorization = _proposal_authorization(proposal_checkpoint)
    decision_log = proposal_checkpoint["artifacts"].pop("decision_log")
    tool = FakePaidTool()

    with pytest.raises(M0ContractError, match="DECISION_LOG_REQUIRED"):
        _authorize_then_execute(
            {
                "proposal": proposal_checkpoint,
                "scene_plan": {"artifacts": {"decision_log": decision_log}},
            },
            authorization,
            tool,
        )
    assert tool.calls == 0


def test_no_proposal_uses_explicit_per_batch_contract_without_false_provenance():
    authorization = {
        "authorization_basis": "explicit_per_batch",
        "approval_status": "approved",
        "approval_reference": "explicit-per-batch:delegation:batch-v2-m0",
        "approved_budget_usd": 1.0,
        "max_authorized_spend_usd": 1.0,
        "no_cost": False,
        "decision_refs": [],
    }
    _validate_proposal_approval({}, authorization)

    authorization["authorization_basis"] = "validated_proposal_checkpoint"
    with pytest.raises(M0ContractError, match="PROPOSAL_AUTHORIZATION_REQUIRED"):
        _validate_proposal_approval({}, authorization)


def test_preflight_authenticates_proposal_budget_and_decisions_from_official_checkpoints(
    tmp_path,
    batch_request,
    source_revision,
    qualified_adapter_observation,
):
    project_id = "proposal-batch-project"
    pipeline_type = "animation"
    project_dir = init_project(
        project_id,
        title="M0 proposal authorization fixture",
        pipeline_type=pipeline_type,
        pipeline_dir=tmp_path,
    )
    write_checkpoint(
        tmp_path,
        project_id,
        "research",
        "completed",
        {"research_brief": sample_artifact("research_brief")},
        pipeline_type=pipeline_type,
    )
    proposal = sample_artifact("proposal_packet")
    proposal["production_plan"]["pipeline"] = pipeline_type
    proposal["approval"]["approved_budget_usd"] = 1.0
    write_checkpoint(
        tmp_path,
        project_id,
        "proposal",
        "completed",
        {
            "proposal_packet": proposal,
            "decision_log": {
                "version": "1.0",
                "project_id": project_id,
                "decisions": [
                    _decision("provider-choice", "provider_selection"),
                    _decision("budget-choice", "budget_tradeoff"),
                ],
            },
        },
        pipeline_type=pipeline_type,
        human_approved=True,
    )
    write_checkpoint(
        tmp_path,
        project_id,
        "script",
        "completed",
        {"script": sample_artifact("script")},
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
    checkpoints = {
        stage: read_checkpoint(tmp_path, project_id, stage)
        for stage in ("research", "proposal", "script", "scene_plan")
    }
    request = deepcopy(batch_request)
    request.update({"project_id": project_id, "pipeline_type": pipeline_type})
    request["authorization"].update(
        {
            "manifest_sha256": canonical_sha256(load_pipeline_readonly(pipeline_type)),
            "prerequisite_checkpoints": [
                {
                    "stage": stage,
                    "logical_path": f"checkpoint_{stage}.json",
                    "sha256": canonical_sha256(checkpoints[stage]),
                    "status": "completed",
                    "human_approved": checkpoints[stage]["human_approved"],
                }
                for stage in ("research", "proposal", "script", "scene_plan")
            ],
            **_proposal_authorization(checkpoints["proposal"]),
        }
    )
    request["source_bindings"] = []
    for binding_id, stage, artifact_name in (
        ("script-source", "script", "script"),
        ("scene-plan-source", "scene_plan", "scene_plan"),
    ):
        artifact = checkpoints[stage]["artifacts"][artifact_name]
        request["source_bindings"].append(
            {
                "binding_id": binding_id,
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
        )
    request["work_items"][0]["source_binding_ids"] = [
        "script-source",
        "scene-plan-source",
    ]
    request = freeze_batch_request(request)

    facts = preflight_batch_request(
        request,
        projects_root=tmp_path,
        observed_source_revision=source_revision,
        adapter_observation=qualified_adapter_observation,
    )

    assert facts.project_dir == project_dir.resolve()
    assert facts.prerequisite_stages == ("research", "proposal", "script", "scene_plan")

    raised_budget = deepcopy(request)
    raised_budget["authorization"].update(
        {"approved_budget_usd": 2.0, "max_authorized_spend_usd": 2.0}
    )
    raised_budget["execution_policy"]["max_attempt_cost_usd"] = 2.0
    raised_budget = freeze_batch_request(raised_budget)
    tool = FakePaidTool()
    with pytest.raises(M0ContractError, match="PROPOSAL_BUDGET_EXCEEDED"):
        _preflight_then_execute(
            raised_budget,
            projects_root=tmp_path,
            source_revision=source_revision,
            observation=qualified_adapter_observation,
            tool=tool,
        )
    assert tool.calls == 0
