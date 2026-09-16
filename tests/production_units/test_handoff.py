from __future__ import annotations

from copy import deepcopy
import inspect
import json
from pathlib import Path
import threading

import pytest

from lib.checkpoint import (
    CheckpointValidationError,
    init_project,
    read_checkpoint,
    write_checkpoint,
)
from lib.clp_validator import canonical_digest
from lib.production_units.handoff import (
    ProductionUnitHandoffCoordinator,
    ProductionUnitHandoffError,
)
from tests.contracts.test_phase0_contracts import sample_artifact


POLICY = {
    "mode": "auto",
    "target_seconds": 180,
    "hard_max_seconds": 480,
    "boundary_priority": "semantic_first",
    "oversize_policy": "allow_with_reason",
    "enabled_stages": ["script"],
}
CONTROL = {
    "chain_id": "control-0001",
    "event_sequence": 0,
    "sha256": "sha256:" + "c" * 64,
}
PLAN = {"version": "1.0", "unit_ids": ["unit-0001"]}
MERGE = {
    "version": "1.0",
    "selected_result_sha256s": ["sha256:" + "a" * 64],
}


class InjectedCrash(RuntimeError):
    pass


def _proposal(*, policy: dict | None) -> dict:
    packet = sample_artifact("proposal_packet")
    if policy is not None:
        packet["production_plan"]["production_unit_policy"] = deepcopy(policy)
    return packet


def _setup_project(
    tmp_path: Path,
    *,
    project_id: str = "pup-handoff",
    policy: dict | None = POLICY,
) -> ProductionUnitHandoffCoordinator:
    init_project(
        project_id,
        title="PUP handoff",
        pipeline_type="animated-explainer",
        pipeline_dir=tmp_path,
    )
    write_checkpoint(
        tmp_path,
        project_id,
        "research",
        "completed",
        {"research_brief": sample_artifact("research_brief")},
        pipeline_type="animated-explainer",
    )
    write_checkpoint(
        tmp_path,
        project_id,
        "proposal",
        "completed",
        {"proposal_packet": _proposal(policy=policy)},
        pipeline_type="animated-explainer",
        human_approved=True,
    )
    return ProductionUnitHandoffCoordinator(tmp_path, project_id, "script-candidate-001")


def _prepare(
    coordinator: ProductionUnitHandoffCoordinator,
    *,
    crash_hook=None,
) -> dict:
    result = coordinator.prepare_candidate(
        run_id="run-0001",
        stage="script",
        execution_epoch=0,
        control_chain=CONTROL,
        plan=PLAN,
        artifacts={"script": sample_artifact("script")},
        merge_evidence=MERGE,
        crash_hook=crash_hook,
    )
    assert result is not None
    return result


def _validated(
    tmp_path: Path,
    *,
    project_id: str = "pup-handoff",
) -> ProductionUnitHandoffCoordinator:
    coordinator = _setup_project(tmp_path, project_id=project_id)
    _prepare(coordinator)
    coordinator.record_review(
        decision="accepted",
        review_evidence={"reviewer": "agent-reviewer", "critical_findings": 0},
    )
    coordinator.validate_candidate()
    return coordinator


def _stage_documents(project_id: str) -> dict[str, dict]:
    script = sample_artifact("script")
    clp_manifest = sample_artifact("clp_manifest")
    clp_manifest["project_id"] = project_id
    clp_candidates = sample_artifact("clp_candidates")
    clp_candidates["project_id"] = project_id
    clp_candidates["source_script_sha256"] = canonical_digest(script)
    scene_plan = sample_artifact("scene_plan")
    clp_shot_bindings = sample_artifact("clp_shot_bindings")
    clp_shot_bindings["project_id"] = project_id
    clp_shot_bindings["source_scene_plan_sha256"] = canonical_digest(scene_plan)
    clp_shot_bindings["clp_manifest_sha256"] = canonical_digest(clp_manifest)
    edit_decisions = sample_artifact("edit_decisions")
    edit_decisions["render_runtime"] = "remotion"
    return {
        "script": script,
        "clp_manifest": clp_manifest,
        "clp_candidates": clp_candidates,
        "scene_plan": scene_plan,
        "clp_shot_bindings": clp_shot_bindings,
        "asset_manifest": sample_artifact("asset_manifest"),
        "edit_decisions": edit_decisions,
    }


def _stage_candidate(
    tmp_path: Path,
    stage: str,
    *,
    project_id: str | None = None,
    handoff_id: str | None = None,
) -> tuple[ProductionUnitHandoffCoordinator, dict[str, dict]]:
    project_id = project_id or f"pup-{stage.replace('_', '-')}"
    policy = deepcopy(POLICY)
    policy["enabled_stages"] = [stage]
    _setup_project(tmp_path, project_id=project_id, policy=policy)
    docs = _stage_documents(project_id)
    stages = ["script", "clp", "scene_plan", "assets", "edit"]
    stage_artifacts = {
        "script": {"script": docs["script"]},
        "clp": {
            "clp_manifest": docs["clp_manifest"],
            "clp_candidates": docs["clp_candidates"],
        },
        "scene_plan": {
            "scene_plan": docs["scene_plan"],
            "clp_shot_bindings": docs["clp_shot_bindings"],
        },
        "assets": {"asset_manifest": docs["asset_manifest"]},
        "edit": {"edit_decisions": docs["edit_decisions"]},
    }
    for predecessor in stages[: stages.index(stage)]:
        write_checkpoint(
            tmp_path,
            project_id,
            predecessor,
            "completed",
            stage_artifacts[predecessor],
            pipeline_type="animated-explainer",
            human_approved=True,
        )
    coordinator = ProductionUnitHandoffCoordinator(
        tmp_path,
        project_id,
        handoff_id or f"{stage}-candidate-001",
    )
    return coordinator, stage_artifacts[stage]


def _prepare_review_validate(
    coordinator: ProductionUnitHandoffCoordinator,
    stage: str,
    artifacts: dict[str, dict],
) -> None:
    assert coordinator.prepare_candidate(
        run_id="run-0001",
        stage=stage,
        execution_epoch=0,
        control_chain=CONTROL,
        plan=PLAN,
        artifacts=artifacts,
        merge_evidence=MERGE,
    ) is not None
    coordinator.record_review(
        decision="accepted", review_evidence={"reviewer": "agent-reviewer"}
    )
    coordinator.validate_candidate()


def _frozen_awaiting_checkpoint(
    tmp_path: Path,
) -> tuple[ProductionUnitHandoffCoordinator, dict]:
    coordinator = _validated(tmp_path)
    coordinator.submit_checkpoint(
        cost_snapshot={"total_usd": 1.25, "currency": "USD"},
        metadata={"consumer_context": {"label": "frozen"}},
    )
    awaiting = read_checkpoint(tmp_path, "pup-handoff", "script")
    assert awaiting is not None
    return coordinator, awaiting


def _write_human_approval(
    tmp_path: Path,
    awaiting: dict,
    **overrides,
) -> None:
    arguments = {
        "pipeline_type": awaiting["pipeline_type"],
        "style_playbook": awaiting.get("style_playbook"),
        "checkpoint_policy": awaiting["checkpoint_policy"],
        "human_approval_required": awaiting["human_approval_required"],
        "human_approved": True,
        "review": deepcopy(awaiting.get("review")),
        "cost_snapshot": deepcopy(awaiting.get("cost_snapshot")),
        "error": awaiting.get("error"),
        "metadata": deepcopy(awaiting.get("metadata")),
    }
    arguments.update(overrides)
    write_checkpoint(
        tmp_path,
        awaiting["project_id"],
        awaiting["stage"],
        "completed",
        deepcopy(awaiting["artifacts"]),
        **arguments,
    )


def _resign(document: dict, field: str = "record_sha256") -> dict:
    value = deepcopy(document)
    value.pop(field, None)
    value[field] = canonical_digest(value)
    return value


def _rewrite(path: Path, document: dict) -> None:
    path.write_text(json.dumps(document), encoding="utf-8")


def test_normal_candidate_review_validation_and_checkpoint_handoff(tmp_path) -> None:
    coordinator = _validated(tmp_path)
    assert read_checkpoint(tmp_path, "pup-handoff", "script") is None

    result = coordinator.submit_checkpoint()

    assert result["idempotent"] is False
    checkpoint = read_checkpoint(tmp_path, "pup-handoff", "script")
    assert checkpoint["status"] == "awaiting_human"
    assert checkpoint["human_approved"] is False
    provenance = checkpoint["metadata"]["production_units"]["candidate_handoff"]
    assert provenance["authority"] == "pup_json_merge"
    assert provenance["execution_epoch"] == 0
    assert provenance["control_chain"] == CONTROL
    assert result["receipt"]["checkpoint"]["sha256"] == canonical_digest(checkpoint)

    again = coordinator.resume_checkpoint()
    assert again["idempotent"] is True
    assert again["receipt"] == result["receipt"]


@pytest.mark.parametrize("stage", ["clp", "scene_plan", "edit"])
def test_other_json_stages_complete_basic_coordinator_handoff(tmp_path, stage) -> None:
    coordinator, artifacts = _stage_candidate(tmp_path, stage)
    _prepare_review_validate(coordinator, stage, artifacts)

    result = coordinator.submit_checkpoint()

    checkpoint = read_checkpoint(tmp_path, coordinator.project_id, stage)
    assert result["idempotent"] is False
    assert checkpoint["artifacts"] == artifacts
    expected_status = "awaiting_human" if stage == "scene_plan" else "completed"
    assert checkpoint["status"] == expected_status
    assert checkpoint["metadata"]["production_units"]["candidate_handoff"][
        "authority"
    ] == "pup_json_merge"


@pytest.mark.parametrize(
    ("stage", "foreign_name"),
    [
        ("script", "asset_manifest"),
        ("clp", "script"),
        ("scene_plan", "edit_decisions"),
        ("edit", "asset_manifest"),
    ],
)
def test_stage_artifact_allowlist_rejects_cross_stage_authority(
    tmp_path, stage, foreign_name
) -> None:
    project_id = f"pup-authority-{stage.replace('_', '-')}"
    policy = deepcopy(POLICY)
    policy["enabled_stages"] = [stage]
    coordinator = _setup_project(tmp_path, project_id=project_id, policy=policy)
    docs = _stage_documents(project_id)
    primary = {
        "script": "script",
        "clp": "clp_manifest",
        "scene_plan": "scene_plan",
        "edit": "edit_decisions",
    }[stage]

    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.prepare_candidate(
            run_id="run-0001",
            stage=stage,
            execution_epoch=0,
            control_chain=CONTROL,
            plan=PLAN,
            artifacts={
                primary: docs[primary],
                foreign_name: docs[foreign_name],
            },
            merge_evidence=MERGE,
        )

    assert exc.value.code == "STAGE_ARTIFACT_AUTHORITY_VIOLATION"
    assert not (tmp_path / project_id / ".production-units").exists()


def test_original_human_gate_is_not_bypassed(tmp_path) -> None:
    coordinator = _validated(tmp_path)
    coordinator.submit_checkpoint()
    checkpoint = read_checkpoint(tmp_path, "pup-handoff", "script")
    assert checkpoint["status"] == "awaiting_human"
    assert "human_approved" not in inspect.signature(
        coordinator.submit_checkpoint
    ).parameters

    with pytest.raises(CheckpointValidationError, match="GATE VIOLATION"):
        write_checkpoint(
            tmp_path,
            "pup-handoff",
            "script",
            "completed",
            checkpoint["artifacts"],
            pipeline_type="animated-explainer",
            human_approved=False,
            metadata=checkpoint["metadata"],
        )


def test_original_human_gate_transition_preserves_full_frozen_envelope(
    tmp_path,
) -> None:
    _, awaiting = _frozen_awaiting_checkpoint(tmp_path)

    _write_human_approval(tmp_path, awaiting)

    completed = read_checkpoint(tmp_path, "pup-handoff", "script")
    assert completed["status"] == "completed"
    assert completed["human_approved"] is True
    normalized_awaiting = deepcopy(awaiting)
    normalized_completed = deepcopy(completed)
    for field in ("status", "human_approved", "timestamp"):
        normalized_awaiting.pop(field)
        normalized_completed.pop(field)
    assert normalized_completed == normalized_awaiting


@pytest.mark.parametrize("attack", ["replace", "add"])
def test_human_gate_rejects_review_replacement_or_addition(
    tmp_path, attack
) -> None:
    _, awaiting = _frozen_awaiting_checkpoint(tmp_path)
    if attack == "replace":
        changed_review = {"reviewer": "attacker", "critical_findings": 0}
    else:
        changed_review = deepcopy(awaiting["review"])
        changed_review["post_approval_note"] = "not part of reviewed envelope"

    with pytest.raises(CheckpointValidationError, match="checkpoint envelope is frozen"):
        _write_human_approval(tmp_path, awaiting, review=changed_review)

    assert read_checkpoint(tmp_path, "pup-handoff", "script") == awaiting


def test_human_gate_rejects_cost_snapshot_mutation(tmp_path) -> None:
    _, awaiting = _frozen_awaiting_checkpoint(tmp_path)
    changed_cost = deepcopy(awaiting["cost_snapshot"])
    changed_cost["total_usd"] = 999.0

    with pytest.raises(CheckpointValidationError, match="checkpoint envelope is frozen"):
        _write_human_approval(tmp_path, awaiting, cost_snapshot=changed_cost)

    assert read_checkpoint(tmp_path, "pup-handoff", "script") == awaiting


@pytest.mark.parametrize("attack", ["modify", "add", "remove"])
def test_human_gate_rejects_metadata_sibling_mutation_addition_or_removal(
    tmp_path, attack
) -> None:
    _, awaiting = _frozen_awaiting_checkpoint(tmp_path)
    changed_metadata = deepcopy(awaiting["metadata"])
    if attack == "modify":
        changed_metadata["consumer_context"]["label"] = "changed"
    elif attack == "add":
        changed_metadata["unreviewed_sibling"] = {"accepted": False}
    else:
        changed_metadata.pop("consumer_context")
    assert (
        changed_metadata["production_units"]
        == awaiting["metadata"]["production_units"]
    )

    with pytest.raises(CheckpointValidationError, match="checkpoint envelope is frozen"):
        _write_human_approval(tmp_path, awaiting, metadata=changed_metadata)

    assert read_checkpoint(tmp_path, "pup-handoff", "script") == awaiting


def test_human_gate_cannot_complete_from_intent_without_awaiting_receipt(
    tmp_path,
) -> None:
    coordinator = _validated(tmp_path)

    def crash(name: str) -> None:
        if name == "checkpoint_intent_persisted":
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        coordinator.submit_checkpoint(crash_hook=crash)
    records = coordinator._load_chain()
    metadata = coordinator._expected_checkpoint_metadata(
        records["candidate"],
        records["review"],
        records["validation"],
        records["checkpoint_intent"],
    )

    with pytest.raises(CheckpointValidationError, match="PUP HUMAN GATE VIOLATION"):
        write_checkpoint(
            tmp_path,
            "pup-handoff",
            "script",
            "completed",
            records["candidate"]["artifacts"],
            pipeline_type="animated-explainer",
            human_approved=True,
            metadata=metadata,
        )
    assert read_checkpoint(tmp_path, "pup-handoff", "script") is None


def test_human_gate_cannot_drop_provenance_replace_artifacts_or_mix_authority(
    tmp_path,
) -> None:
    coordinator = _validated(tmp_path)
    coordinator.submit_checkpoint()
    awaiting = read_checkpoint(tmp_path, "pup-handoff", "script")

    with pytest.raises(CheckpointValidationError, match="PUP HUMAN GATE VIOLATION"):
        write_checkpoint(
            tmp_path,
            "pup-handoff",
            "script",
            "completed",
            awaiting["artifacts"],
            pipeline_type="animated-explainer",
            human_approved=True,
        )

    changed_artifacts = deepcopy(awaiting["artifacts"])
    changed_artifacts["script"]["title"] = "substituted after review"
    with pytest.raises(CheckpointValidationError, match="PUP HUMAN GATE VIOLATION"):
        write_checkpoint(
            tmp_path,
            "pup-handoff",
            "script",
            "completed",
            changed_artifacts,
            pipeline_type="animated-explainer",
            human_approved=True,
            metadata=awaiting["metadata"],
        )

    hybrid_metadata = deepcopy(awaiting["metadata"])
    hybrid_metadata["batch_v2_publication"] = {
        "command_digest": "sha256:" + "a" * 64
    }
    with pytest.raises(CheckpointValidationError, match="checkpoint envelope is frozen"):
        _write_human_approval(tmp_path, awaiting, metadata=hybrid_metadata)

    assert read_checkpoint(tmp_path, "pup-handoff", "script") == awaiting


def test_official_reader_rejects_checkpoint_provenance_tamper(tmp_path) -> None:
    coordinator = _validated(tmp_path)
    coordinator.submit_checkpoint()
    checkpoint_path = tmp_path / "pup-handoff" / "checkpoint_script.json"
    checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    checkpoint["metadata"]["production_units"]["candidate_handoff"][
        "control_chain"
    ]["sha256"] = "sha256:" + "1" * 64
    _rewrite(checkpoint_path, checkpoint)

    with pytest.raises(CheckpointValidationError, match="provenance"):
        read_checkpoint(tmp_path, "pup-handoff", "script")


@pytest.mark.parametrize(
    "boundary",
    [
        "candidate_persisted",
        "checkpoint_intent_persisted",
        "checkpoint_written",
        "checkpoint_receipt_persisted",
    ],
)
def test_crash_boundaries_restart_deterministically(tmp_path, boundary) -> None:
    coordinator = _setup_project(tmp_path)

    def crash(name: str) -> None:
        if name == boundary:
            raise InjectedCrash(name)

    if boundary == "candidate_persisted":
        with pytest.raises(InjectedCrash):
            _prepare(coordinator, crash_hook=crash)
        _prepare(coordinator)
        coordinator.record_review(
            decision="accepted", review_evidence={"reviewer": "r"}
        )
        coordinator.validate_candidate()
        result = coordinator.submit_checkpoint()
    else:
        _prepare(coordinator)
        coordinator.record_review(
            decision="accepted", review_evidence={"reviewer": "r"}
        )
        coordinator.validate_candidate()
        with pytest.raises(InjectedCrash):
            coordinator.submit_checkpoint(crash_hook=crash)
        result = coordinator.resume_checkpoint()

    checkpoint = read_checkpoint(tmp_path, "pup-handoff", "script")
    assert checkpoint["status"] == "awaiting_human"
    assert result["receipt"]["checkpoint"]["sha256"] == canonical_digest(checkpoint)


def test_crash_after_writer_repairs_receipt_without_rewriting_checkpoint(tmp_path) -> None:
    coordinator = _validated(tmp_path)

    def crash(name: str) -> None:
        if name == "checkpoint_written":
            raise InjectedCrash(name)

    with pytest.raises(InjectedCrash):
        coordinator.submit_checkpoint(crash_hook=crash)
    checkpoint_path = tmp_path / "pup-handoff" / "checkpoint_script.json"
    before = checkpoint_path.read_bytes()

    result = coordinator.resume_checkpoint()

    assert result["idempotent"] is False
    assert checkpoint_path.read_bytes() == before
    history = tmp_path / "pup-handoff" / "history"
    assert not history.exists() or not list(history.glob("checkpoint_script_*.json"))


def test_policy_drift_blocks_review_and_publication(tmp_path) -> None:
    coordinator = _setup_project(tmp_path)
    _prepare(coordinator)
    changed = deepcopy(POLICY)
    changed["target_seconds"] = 240
    write_checkpoint(
        tmp_path,
        "pup-handoff",
        "proposal",
        "completed",
        {"proposal_packet": _proposal(policy=changed)},
        pipeline_type="animated-explainer",
        human_approved=True,
    )

    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.record_review(decision="accepted", review_evidence={"reviewer": "r"})
    assert exc.value.code in {"STALE_SOURCE_CHECKPOINT", "STALE_POLICY"}
    assert read_checkpoint(tmp_path, "pup-handoff", "script") is None


def test_source_checkpoint_drift_blocks_review(tmp_path) -> None:
    coordinator = _setup_project(tmp_path)
    _prepare(coordinator)
    research = sample_artifact("research_brief")
    research["topic"] = "Changed source"
    write_checkpoint(
        tmp_path,
        "pup-handoff",
        "research",
        "completed",
        {"research_brief": research},
        pipeline_type="animated-explainer",
    )

    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.record_review(decision="accepted", review_evidence={"reviewer": "r"})
    assert exc.value.code == "STALE_SOURCE_CHECKPOINT"


def test_target_checkpoint_drift_blocks_commit(tmp_path) -> None:
    coordinator = _validated(tmp_path)
    write_checkpoint(
        tmp_path,
        "pup-handoff",
        "script",
        "in_progress",
        {},
        pipeline_type="animated-explainer",
    )

    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.submit_checkpoint()
    assert exc.value.code == "STALE_CHECKPOINT"
    assert read_checkpoint(tmp_path, "pup-handoff", "script")["status"] == "in_progress"


def test_candidate_and_plan_tamper_fail_closed(tmp_path) -> None:
    coordinator = _setup_project(tmp_path)
    _prepare(coordinator)
    candidate_path = coordinator.handoff_dir / "candidate.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate["artifacts"]["script"]["title"] = "tampered"
    _rewrite(candidate_path, candidate)

    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.record_review(decision="accepted", review_evidence={"reviewer": "r"})
    assert exc.value.code == "HANDOFF_RECORD_TAMPERED"

    coordinator = _setup_project(tmp_path, project_id="pup-plan-tamper")
    _prepare(coordinator)
    plan_path = coordinator.handoff_dir / "plan.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan["plan"]["unit_ids"] = ["unit-other"]
    _rewrite(plan_path, _resign(plan))
    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.record_review(decision="accepted", review_evidence={"reviewer": "r"})
    assert exc.value.code == "STALE_PLAN"


def test_state_tamper_and_control_chain_drift_fail_closed(tmp_path) -> None:
    coordinator = _setup_project(tmp_path)
    _prepare(coordinator)
    state = json.loads(coordinator.state_path.read_text(encoding="utf-8"))
    state["execution_epoch"] = 1
    _rewrite(coordinator.state_path, _resign(state, "state_sha256"))

    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.record_review(decision="accepted", review_evidence={"reviewer": "r"})
    assert exc.value.code == "HANDOFF_STATE_STALE"

    coordinator = _setup_project(tmp_path, project_id="pup-control-tamper")
    _prepare(coordinator)
    candidate_path = coordinator.handoff_dir / "candidate.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate["identity"]["control_chain"]["sha256"] = "sha256:" + "d" * 64
    _rewrite(candidate_path, _resign(candidate))
    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.record_review(decision="accepted", review_evidence={"reviewer": "r"})
    assert exc.value.code == "HANDOFF_IDENTITY_MISMATCH"


def test_review_receipt_and_authority_tamper_fail_closed(tmp_path) -> None:
    coordinator = _setup_project(tmp_path)
    _prepare(coordinator)
    coordinator.record_review(
        decision="accepted", review_evidence={"reviewer": "r", "critical": 0}
    )
    review_path = coordinator.handoff_dir / "review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review["review_evidence"]["critical"] = 1
    _rewrite(review_path, review)
    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.validate_candidate()
    assert exc.value.code == "HANDOFF_RECORD_TAMPERED"

    coordinator = _setup_project(tmp_path, project_id="pup-authority-tamper")
    _prepare(coordinator)
    candidate_path = coordinator.handoff_dir / "candidate.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate["batch_publication_command_sha256"] = "sha256:" + "e" * 64
    _rewrite(candidate_path, _resign(candidate))
    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.record_review(decision="accepted", review_evidence={"reviewer": "r"})
    assert exc.value.code == "INVALID_HANDOFF_RECORD"


def test_checkpoint_metadata_cannot_mix_batch_or_render_authority(tmp_path) -> None:
    coordinator = _validated(tmp_path)
    for metadata in (
        {"batch_v2_publication": {"command_digest": "sha256:" + "a" * 64}},
        {"pup_render_publication": {"receipt": "sha256:" + "b" * 64}},
        {"production_units": {"candidate_handoff": {}}},
    ):
        with pytest.raises(ProductionUnitHandoffError) as exc:
            coordinator.submit_checkpoint(metadata=metadata)
        assert exc.value.code == "HYBRID_PUBLICATION_AUTHORITY"
    assert read_checkpoint(tmp_path, "pup-handoff", "script") is None


def test_cross_epoch_replay_and_adoption_are_not_accepted(tmp_path) -> None:
    coordinator = _setup_project(tmp_path)
    _prepare(coordinator)
    candidate_path = coordinator.handoff_dir / "candidate.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate["identity"]["execution_epoch"] = 1
    _rewrite(candidate_path, _resign(candidate))
    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.record_review(decision="accepted", review_evidence={"reviewer": "r"})
    assert exc.value.code == "HANDOFF_IDENTITY_MISMATCH"

    coordinator = _setup_project(tmp_path, project_id="pup-illegal-adoption")
    _prepare(coordinator)
    candidate_path = coordinator.handoff_dir / "candidate.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate["adopted_from_epoch"] = 0
    _rewrite(candidate_path, _resign(candidate))
    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.record_review(decision="accepted", review_evidence={"reviewer": "r"})
    assert exc.value.code == "INVALID_HANDOFF_RECORD"


def test_ambiguous_charged_attempt_is_not_retried_or_persisted(tmp_path) -> None:
    coordinator = _setup_project(tmp_path)
    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.prepare_candidate(
            run_id="run-0001",
            stage="script",
            execution_epoch=0,
            control_chain=CONTROL,
            plan=PLAN,
            artifacts={"script": sample_artifact("script")},
            merge_evidence=MERGE,
            provider_charge_state="ambiguous",
        )
    assert exc.value.code == "AMBIGUOUS_CHARGED_ATTEMPT"
    assert not (tmp_path / "pup-handoff" / ".production-units").exists()


def test_concurrent_coordinator_is_rejected_and_retry_is_idempotent(tmp_path) -> None:
    coordinator = _validated(tmp_path)
    entered = threading.Event()
    release = threading.Event()
    errors: list[BaseException] = []

    def block(name: str) -> None:
        if name == "checkpoint_intent_persisted":
            entered.set()
            assert release.wait(timeout=10)

    def first() -> None:
        try:
            coordinator.submit_checkpoint(crash_hook=block)
        except BaseException as exc:  # pragma: no cover - assertion surfaced below
            errors.append(exc)

    thread = threading.Thread(target=first)
    thread.start()
    assert entered.wait(timeout=10)
    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.resume_checkpoint()
    assert exc.value.code == "HANDOFF_COORDINATOR_BUSY"
    release.set()
    thread.join(timeout=10)
    assert not thread.is_alive()
    assert errors == []
    assert coordinator.resume_checkpoint()["idempotent"] is True


def test_different_handoffs_serialize_one_project_stage_commit(tmp_path) -> None:
    first, artifacts = _stage_candidate(
        tmp_path, "script", project_id="pup-shared-stage", handoff_id="handoff-a"
    )
    second = ProductionUnitHandoffCoordinator(
        tmp_path, "pup-shared-stage", "handoff-b"
    )
    _prepare_review_validate(first, "script", artifacts)
    _prepare_review_validate(second, "script", artifacts)
    entered = threading.Event()
    release = threading.Event()
    errors: list[BaseException] = []

    def block(name: str) -> None:
        if name == "checkpoint_written":
            entered.set()
            assert release.wait(timeout=10)

    def commit_first() -> None:
        try:
            first.submit_checkpoint(crash_hook=block)
        except BaseException as exc:  # pragma: no cover - assertion surfaced below
            errors.append(exc)

    thread = threading.Thread(target=commit_first)
    thread.start()
    assert entered.wait(timeout=10)
    with pytest.raises(ProductionUnitHandoffError) as exc:
        second.submit_checkpoint()
    assert exc.value.code == "CHECKPOINT_STAGE_BUSY"
    release.set()
    thread.join(timeout=10)
    assert not thread.is_alive()
    assert errors == []

    checkpoint = read_checkpoint(tmp_path, "pup-shared-stage", "script")
    assert checkpoint["metadata"]["production_units"]["candidate_handoff"][
        "handoff_id"
    ] == "handoff-a"
    with pytest.raises(ProductionUnitHandoffError) as exc:
        second.resume_checkpoint()
    assert exc.value.code == "STALE_CHECKPOINT"


def test_ordinary_writer_cannot_race_pup_stage_commit(tmp_path) -> None:
    coordinator = _validated(tmp_path)
    entered = threading.Event()
    release = threading.Event()
    errors: list[BaseException] = []

    def block(name: str) -> None:
        if name == "checkpoint_written":
            entered.set()
            assert release.wait(timeout=10)

    def commit_candidate() -> None:
        try:
            coordinator.submit_checkpoint(crash_hook=block)
        except BaseException as exc:  # pragma: no cover - assertion surfaced below
            errors.append(exc)

    thread = threading.Thread(target=commit_candidate)
    thread.start()
    assert entered.wait(timeout=10)
    for competing_stage in ("script", "proposal"):
        with pytest.raises(CheckpointValidationError, match="CHECKPOINT_STAGE_BUSY"):
            write_checkpoint(
                tmp_path,
                "pup-handoff",
                competing_stage,
                "in_progress",
                {},
                pipeline_type="animated-explainer",
            )
    release.set()
    thread.join(timeout=10)
    assert not thread.is_alive()
    assert errors == []
    assert read_checkpoint(tmp_path, "pup-handoff", "script")["status"] == "awaiting_human"


@pytest.mark.parametrize("policy", [None, {"mode": "off"}])
def test_missing_or_off_policy_is_strict_noop(tmp_path, policy) -> None:
    coordinator = _setup_project(tmp_path, policy=policy)
    result = coordinator.prepare_candidate(
        run_id="run-0001",
        stage="script",
        execution_epoch=0,
        control_chain=CONTROL,
        plan=PLAN,
        artifacts={"script": {"not": "inspected while off"}},
        merge_evidence={},
    )
    assert result is None
    assert not (tmp_path / "pup-handoff" / ".production-units").exists()


def test_off_policy_is_noop_even_for_separately_owned_stage(tmp_path) -> None:
    coordinator = _setup_project(tmp_path, policy={"mode": "off"})
    assert coordinator.prepare_candidate(
        run_id="run-0001",
        stage="assets",
        execution_epoch=0,
        control_chain=CONTROL,
        plan={},
        artifacts={},
        merge_evidence={},
    ) is None
    assert not (tmp_path / "pup-handoff" / ".production-units").exists()


def test_ordinary_project_without_proposal_remains_unchanged(tmp_path) -> None:
    init_project(
        "ordinary",
        title="Ordinary",
        pipeline_type="framework-smoke",
        pipeline_dir=tmp_path,
    )
    coordinator = ProductionUnitHandoffCoordinator(
        tmp_path, "ordinary", "ordinary-script"
    )
    assert coordinator.prepare_candidate(
        run_id="run-ordinary",
        stage="script",
        execution_epoch=0,
        control_chain=CONTROL,
        plan={"ignored": True},
        artifacts={"script": {"ignored": True}},
        merge_evidence={},
    ) is None
    assert not (tmp_path / "ordinary" / ".production-units").exists()


@pytest.mark.parametrize(
    ("stage", "code"),
    [
        ("assets", "BATCH_V2_AUTHORITY_REQUIRED"),
        ("compose", "RENDER_AUTHORITY_NOT_QUALIFIED"),
    ],
)
def test_non_json_publication_authorities_cannot_use_handoff(tmp_path, stage, code) -> None:
    policy = deepcopy(POLICY)
    policy["enabled_stages"] = [stage]
    coordinator = _setup_project(tmp_path, policy=policy)
    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.prepare_candidate(
            run_id="run-0001",
            stage=stage,
            execution_epoch=0,
            control_chain=CONTROL,
            plan=PLAN,
            artifacts={},
            merge_evidence={},
        )
    assert exc.value.code == code


def test_checkpoint_receipt_tamper_is_rejected(tmp_path) -> None:
    coordinator = _validated(tmp_path)
    coordinator.submit_checkpoint()
    receipt_path = coordinator.handoff_dir / "checkpoint-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["candidate_sha256"] = "sha256:" + "f" * 64
    _rewrite(receipt_path, _resign(receipt))

    with pytest.raises(CheckpointValidationError, match="provenance"):
        read_checkpoint(tmp_path, "pup-handoff", "script")
    with pytest.raises(ProductionUnitHandoffError) as exc:
        coordinator.resume_checkpoint()
    assert exc.value.code == "CHECKPOINT_RECEIPT_TAMPERED"
