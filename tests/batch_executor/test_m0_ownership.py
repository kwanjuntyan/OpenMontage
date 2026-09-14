from __future__ import annotations

from copy import deepcopy

import pytest

from lib.batch_executor.contracts import M0ContractError
from lib.batch_executor.ownership import (
    assert_dispatch_owner,
    freeze_execution_status_evidence,
    freeze_resume_authorization,
    prepare_cloud_takeover,
    resumed_item_state,
)
from tests.batch_executor.conftest import make_paid_running_attempt


def _evidence(owner):
    return freeze_execution_status_evidence(
        {
            "version": "1.0",
            "evidence_id": "evidence-001",
            "batch_id": owner["batch_id"],
            "request_digest": owner["request_digest"],
            "prior_invocation_id": owner["invocation_id"],
            "prior_execution_id": owner["execution_id"],
            "observed_status": "terminal",
            "observed_at": "2026-09-14T08:30:00Z",
            "verifier": "cloud_run_control_plane_adc",
            "execution_resource": owner["execution_id"],
        }
    )


def _authorization(owner, *, successor="invocation-new", generation=22):
    return freeze_resume_authorization(
        {
            "version": "1.0",
            "authorization_id": "resume-001",
            "batch_id": owner["batch_id"],
            "request_digest": owner["request_digest"],
            "prior_invocation_id": owner["invocation_id"],
            "prior_execution_id": owner["execution_id"],
            "intended_new_invocation_id": successor,
            "expected_state_generation": generation,
            "reason": "Operator verified the prior execution cannot continue and forces ownership only.",
            "decision_reference": "user-reply:resume-001",
            "authorized_at": "2026-09-14T08:31:00Z",
        }
    )


class FakeADCExecutionStatusVerifier:
    verifier_id = "cloud_run_control_plane_adc"

    def __init__(self, evidence):
        self.evidence = evidence
        self.calls = 0

    def verify_stopped(self, recorded_owner):
        self.calls += 1
        return self.evidence


class CallerSuppliedStatusVerifier(FakeADCExecutionStatusVerifier):
    verifier_id = "caller_supplied_json"


def _takeover(owner, **overrides):
    kwargs = {
        "current_state_generation": 22,
        "new_invocation_id": "invocation-new",
        "new_execution_id": "projects/p/locations/r/jobs/j/executions/new",
        "new_task_id": "0",
        "acquired_at": "2026-09-14T08:32:00Z",
    }
    kwargs.update(overrides)
    return prepare_cloud_takeover(owner, **kwargs)


def test_same_active_owner_may_dispatch_but_different_ordinary_run_fails_closed(cloud_owner):
    assert_dispatch_owner(
        cloud_owner,
        invocation_id=cloud_owner["invocation_id"],
        execution_id=cloud_owner["execution_id"],
        invocation_mode="run",
    )
    with pytest.raises(M0ContractError, match="ACTIVE_OWNER_CONFLICT"):
        assert_dispatch_owner(
            cloud_owner,
            invocation_id="invocation-new",
            execution_id="execution-new",
            invocation_mode="run",
        )


def test_self_written_terminal_owner_is_not_stop_proof_for_another_run(cloud_owner):
    terminal = deepcopy(cloud_owner)
    terminal["owner_status"] = "terminal"
    terminal["release_evidence_digest"] = "c" * 64
    terminal["release_observation_source"] = "self"
    with pytest.raises(M0ContractError, match="ACTIVE_OWNER_CONFLICT"):
        assert_dispatch_owner(
            terminal,
            invocation_id="invocation-new",
            execution_id="execution-new",
            invocation_mode="run",
        )
    with pytest.raises(M0ContractError, match="TAKEOVER_PROOF_REQUIRED"):
        assert_dispatch_owner(
            terminal,
            invocation_id="invocation-new",
            execution_id="execution-new",
            invocation_mode="resume",
        )


def test_caller_supplied_terminal_json_is_not_trusted_without_adc_verification(cloud_owner):
    evidence = _evidence(cloud_owner)
    with pytest.raises(M0ContractError, match="UNTRUSTED_EXECUTION_EVIDENCE"):
        _takeover(
            cloud_owner,
            execution_status_verifier=CallerSuppliedStatusVerifier(evidence),
        )


def test_trusted_exact_terminal_evidence_produces_proof_before_cas_plan(cloud_owner):
    evidence = _evidence(cloud_owner)
    verifier = FakeADCExecutionStatusVerifier(evidence)
    plan = _takeover(
        cloud_owner,
        execution_status_verifier=verifier,
    )
    assert verifier.calls == 1
    assert plan.expected_generation == 22
    assert plan.proof_kind == "trusted_execution_status"
    assert plan.proof_digest == evidence["evidence_digest"]
    assert plan.new_owner["invocation_mode"] == "resume"
    assert plan.new_owner["owner_status"] == "active"
    assert plan.new_owner["base_state_generation"] == 22
    assert plan.new_owner["predecessor"] == {
        "invocation_id": cloud_owner["invocation_id"],
        "execution_id": cloud_owner["execution_id"],
    }


def test_terminal_evidence_for_another_execution_is_rejected(cloud_owner):
    evidence = _evidence(cloud_owner)
    evidence["prior_execution_id"] = "another-execution"
    evidence = freeze_execution_status_evidence(evidence)
    with pytest.raises(M0ContractError, match="TAKEOVER_PROOF_MISMATCH"):
        _takeover(
            cloud_owner,
            execution_status_verifier=FakeADCExecutionStatusVerifier(evidence),
        )


def test_human_resume_authorization_is_bound_to_prior_successor_and_generation(cloud_owner):
    authorization = _authorization(cloud_owner)
    plan = _takeover(cloud_owner, resume_authorization=authorization)
    assert plan.proof_kind == "human_resume_authorization"
    assert plan.proof_digest == authorization["authorization_digest"]

    with pytest.raises(M0ContractError, match="TAKEOVER_PROOF_MISMATCH"):
        _takeover(
            cloud_owner,
            current_state_generation=23,
            resume_authorization=authorization,
        )
    with pytest.raises(M0ContractError, match="TAKEOVER_PROOF_MISMATCH"):
        _takeover(
            cloud_owner,
            new_invocation_id="another-successor",
            resume_authorization=authorization,
        )


def test_exactly_one_takeover_proof_is_required(cloud_owner):
    with pytest.raises(M0ContractError, match="TAKEOVER_PROOF_REQUIRED"):
        _takeover(cloud_owner)
    with pytest.raises(M0ContractError, match="TAKEOVER_PROOF_REQUIRED"):
        _takeover(
            cloud_owner,
            execution_status_verifier=FakeADCExecutionStatusVerifier(_evidence(cloud_owner)),
            resume_authorization=_authorization(cloud_owner),
        )


@pytest.mark.parametrize("acceptance", ["unknown", "accepted"])
def test_paid_running_or_possibly_accepted_attempt_is_indeterminate_not_replayed(acceptance):
    attempt = make_paid_running_attempt(acceptance=acceptance)
    assert resumed_item_state(attempt) == "indeterminate"


def test_forced_human_takeover_does_not_authorize_paid_ambiguous_replay(cloud_owner):
    attempt = make_paid_running_attempt(acceptance="unknown")
    plan = _takeover(
        cloud_owner,
        resume_authorization=_authorization(cloud_owner),
        prior_attempts=[attempt],
    )
    assert plan.indeterminate_item_ids == ("item-001",)


def test_stale_or_modified_proof_digest_fails_closed(cloud_owner):
    authorization = _authorization(cloud_owner)
    authorization["reason"] = "Changed after authorization"
    with pytest.raises(M0ContractError, match="TAKEOVER_PROOF_DIGEST_MISMATCH"):
        _takeover(cloud_owner, resume_authorization=authorization)
