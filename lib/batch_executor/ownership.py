"""Offline ownership proof and paid-ambiguity rules for Batch V2 M0."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Protocol

from .contracts import (
    M0ContractError,
    freeze_self_digest,
    validate_attempt,
    validate_contract,
)


@dataclass(frozen=True)
class TakeoverPlan:
    """Proof-validated input to a future expected-generation CAS.

    Producing this value does not perform or imply that CAS.  M3 must write the
    candidate with ``expected_generation`` and then re-read the winning owner.
    """

    expected_generation: int
    new_owner: dict[str, Any]
    proof_kind: str
    proof_digest: str
    indeterminate_item_ids: tuple[str, ...]


class ExecutionStatusVerifier(Protocol):
    """Trust boundary implemented by the ADC Cloud Run control-plane adapter in M3."""

    verifier_id: str

    def verify_stopped(
        self, recorded_owner: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        """Return immutable evidence for the exact owner or raise."""
        ...


def freeze_execution_status_evidence(document: Mapping[str, Any]) -> dict[str, Any]:
    return freeze_self_digest(
        document,
        schema_name="execution_status_evidence",
        digest_field="evidence_digest",
    )


def freeze_resume_authorization(document: Mapping[str, Any]) -> dict[str, Any]:
    return freeze_self_digest(
        document,
        schema_name="resume_authorization",
        digest_field="authorization_digest",
    )


def assert_dispatch_owner(
    recorded_owner: Mapping[str, Any],
    *,
    invocation_id: str,
    execution_id: str,
    invocation_mode: str,
) -> None:
    """Allow only the same active owner; a different owner fails closed."""

    validate_contract("execution_owner", recorded_owner)
    same_owner = (
        recorded_owner["invocation_id"] == invocation_id
        and recorded_owner["execution_id"] == execution_id
    )
    if same_owner and recorded_owner["owner_status"] == "active":
        return
    if invocation_mode == "run":
        raise M0ContractError(
            "ACTIVE_OWNER_CONFLICT",
            "An ordinary run cannot replace any different recorded owner",
        )
    raise M0ContractError(
        "TAKEOVER_PROOF_REQUIRED",
        "Resume must complete proof-before-CAS ownership planning before dispatch",
    )


def _binds_prior_owner(proof: Mapping[str, Any], owner: Mapping[str, Any]) -> bool:
    return (
        proof.get("batch_id") == owner.get("batch_id")
        and proof.get("request_digest") == owner.get("request_digest")
        and proof.get("prior_invocation_id") == owner.get("invocation_id")
        and proof.get("prior_execution_id") == owner.get("execution_id")
    )


def resumed_item_state(attempt: Mapping[str, Any]) -> str:
    """Classify one last attempt without making a provider call.

    Human forced takeover changes execution ownership only.  It never converts
    a possibly accepted paid operation into permission to submit a replacement.
    """

    validate_attempt(attempt)
    phase = attempt["phase"]
    terminal_states = {
        "durably_committed": "committed",
        "failed": "failed_terminal",
        "indeterminate": "indeterminate",
        "cancelled": "cancelled",
    }
    if phase in terminal_states:
        return terminal_states[phase]
    if attempt["billing_mode"] == "paid" and (
        phase != "prepared" or attempt["acceptance_knowledge"] in {"accepted", "unknown"}
    ):
        return "indeterminate"
    if attempt["acceptance_knowledge"] == "accepted":
        return "indeterminate"
    return "pending"


def _indeterminate_items(attempts: Iterable[Mapping[str, Any]]) -> tuple[str, ...]:
    by_item: dict[str, Mapping[str, Any]] = {}
    for attempt in attempts:
        validate_attempt(attempt)
        item_id = attempt["item_id"]
        previous = by_item.get(item_id)
        if previous is None or attempt["dispatch_sequence"] > previous["dispatch_sequence"]:
            by_item[item_id] = attempt
    return tuple(
        sorted(item_id for item_id, attempt in by_item.items() if resumed_item_state(attempt) == "indeterminate")
    )


def prepare_cloud_takeover(
    recorded_owner: Mapping[str, Any],
    *,
    current_state_generation: int,
    new_invocation_id: str,
    new_execution_id: str,
    new_task_id: str,
    acquired_at: str,
    prior_attempts: Iterable[Mapping[str, Any]] = (),
    execution_status_verifier: ExecutionStatusVerifier | None = None,
    resume_authorization: Mapping[str, Any] | None = None,
) -> TakeoverPlan:
    """Validate one exact proof and build, but do not write, the CAS candidate."""

    validate_contract("execution_owner", recorded_owner)
    if recorded_owner["profile"] != "cloud_run":
        raise M0ContractError("CLOUD_OWNER_REQUIRED", "Cloud takeover requires a Cloud owner")
    if current_state_generation < 1:
        raise M0ContractError("INVALID_STATE_GENERATION", "Expected GCS generation must be positive")
    if new_invocation_id == recorded_owner["invocation_id"]:
        raise M0ContractError("INVALID_SUCCESSOR", "Takeover requires a new invocation ID")
    proof_count = int(execution_status_verifier is not None) + int(resume_authorization is not None)
    if proof_count != 1:
        raise M0ContractError("TAKEOVER_PROOF_REQUIRED", "Provide exactly one takeover proof")

    proof_kind: str
    proof_digest: str
    if execution_status_verifier is not None:
        if execution_status_verifier.verifier_id != "cloud_run_control_plane_adc":
            raise M0ContractError(
                "UNTRUSTED_EXECUTION_EVIDENCE",
                "Only the ADC Cloud Run control-plane verifier may attest execution status",
            )
        try:
            execution_status_evidence = execution_status_verifier.verify_stopped(recorded_owner)
        except Exception as exc:
            raise M0ContractError(
                "EXECUTION_STATUS_VERIFICATION_FAILED", f"Trusted verifier failed: {exc}"
            ) from exc
        if not isinstance(execution_status_evidence, Mapping):
            raise M0ContractError(
                "EXECUTION_STATUS_VERIFICATION_FAILED", "Verifier returned no evidence object"
            )
        validate_contract("execution_status_evidence", execution_status_evidence)
        if not _binds_prior_owner(execution_status_evidence, recorded_owner):
            raise M0ContractError(
                "TAKEOVER_PROOF_MISMATCH", "Execution evidence does not bind the recorded owner"
            )
        if execution_status_evidence["execution_resource"] != recorded_owner["execution_id"]:
            raise M0ContractError(
                "TAKEOVER_PROOF_MISMATCH", "Verified resource is not the recorded execution"
            )
        frozen = freeze_execution_status_evidence(execution_status_evidence)
        if frozen["evidence_digest"] != execution_status_evidence["evidence_digest"]:
            raise M0ContractError("TAKEOVER_PROOF_DIGEST_MISMATCH", "Evidence was changed")
        proof_kind = "trusted_execution_status"
        proof_digest = execution_status_evidence["evidence_digest"]
    else:
        assert resume_authorization is not None
        validate_contract("resume_authorization", resume_authorization)
        if not _binds_prior_owner(resume_authorization, recorded_owner):
            raise M0ContractError(
                "TAKEOVER_PROOF_MISMATCH", "ResumeAuthorization does not bind the recorded owner"
            )
        if resume_authorization["intended_new_invocation_id"] != new_invocation_id:
            raise M0ContractError(
                "TAKEOVER_PROOF_MISMATCH", "ResumeAuthorization names another successor"
            )
        if resume_authorization["expected_state_generation"] != current_state_generation:
            raise M0ContractError(
                "TAKEOVER_PROOF_MISMATCH", "ResumeAuthorization is stale for this generation"
            )
        frozen = freeze_resume_authorization(resume_authorization)
        if frozen["authorization_digest"] != resume_authorization["authorization_digest"]:
            raise M0ContractError("TAKEOVER_PROOF_DIGEST_MISMATCH", "Authorization was changed")
        proof_kind = "human_resume_authorization"
        proof_digest = resume_authorization["authorization_digest"]

    new_owner = {
        "version": "1.0",
        "batch_id": recorded_owner["batch_id"],
        "request_digest": recorded_owner["request_digest"],
        "invocation_id": new_invocation_id,
        "invocation_mode": "resume",
        "profile": "cloud_run",
        "execution_id": new_execution_id,
        "task_id": new_task_id,
        "owner_status": "active",
        "acquired_at": acquired_at,
        "state_revision": recorded_owner["state_revision"] + 1,
        "base_state_generation": current_state_generation,
        "predecessor": {
            "invocation_id": recorded_owner["invocation_id"],
            "execution_id": recorded_owner["execution_id"],
        },
        "takeover_proof": {"kind": proof_kind, "digest": proof_digest},
    }
    validate_contract("execution_owner", new_owner)
    return TakeoverPlan(
        expected_generation=current_state_generation,
        new_owner=deepcopy(new_owner),
        proof_kind=proof_kind,
        proof_digest=proof_digest,
        indeterminate_item_ids=_indeterminate_items(prior_attempts),
    )


__all__ = [
    "ExecutionStatusVerifier",
    "TakeoverPlan",
    "assert_dispatch_owner",
    "freeze_execution_status_evidence",
    "freeze_resume_authorization",
    "prepare_cloud_takeover",
    "resumed_item_state",
]
