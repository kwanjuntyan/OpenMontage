from __future__ import annotations

from copy import deepcopy

import pytest

from lib.batch_executor.contracts import (
    M0ContractError,
    load_execution_schema,
    validate_attempt,
    validate_batch_result,
    validate_batch_state,
)
from tests.batch_executor.test_m0_contracts import _committed_attempt
from tests.batch_executor.test_m0_integrity import _valid_result, _valid_state


STABLE_ERROR_CLASSES = {
    "REQUEST_CONTRACT_INVALID",
    "PROJECT_IDENTITY_INVALID",
    "SOURCE_BINDING_CHANGED",
    "APPROVAL_MISSING_OR_STALE",
    "BUDGET_EXCEEDED",
    "TOOL_UNAVAILABLE",
    "AUTH_CONFIGURATION",
    "INPUT_MEDIA_INVALID",
    "RATE_LIMITED_SUBMIT_REJECTED",
    "RATE_LIMITED_REMOTE_POLL",
    "RATE_LIMITED_ACCEPTANCE_UNKNOWN",
    "PROVIDER_TRANSIENT_PRE_ACCEPT",
    "PROVIDER_PERMANENT_REJECT",
    "CONTENT_SAFETY_REJECT",
    "TIMEOUT_OR_NETWORK_UNKNOWN",
    "REMOTE_JOB_RECOVERABLE",
    "OUTPUT_TECHNICALLY_INVALID",
    "LOCAL_STORAGE_TRANSIENT",
    "GCS_TRANSIENT",
    "GCS_PRECONDITION_CONFLICT",
    "EXECUTION_OWNER_ACTIVE",
    "RESUME_OWNERSHIP_PROOF_INVALID",
    "INTERNAL_BUG",
    "CANCELLED",
}

RETRY_ACTIONS = {
    "none",
    "resubmit_generation",
    "poll_remote_operation",
    "retry_storage_commit",
    "reconcile_storage_precondition",
    "await_charged_generation_authorization",
    "do_not_retry",
    "mark_indeterminate",
}

NOT_ACCEPTED_TERMINAL_ERRORS = {
    "REQUEST_CONTRACT_INVALID",
    "PROJECT_IDENTITY_INVALID",
    "SOURCE_BINDING_CHANGED",
    "APPROVAL_MISSING_OR_STALE",
    "BUDGET_EXCEEDED",
    "TOOL_UNAVAILABLE",
    "AUTH_CONFIGURATION",
    "INPUT_MEDIA_INVALID",
    "PROVIDER_PERMANENT_REJECT",
    "CONTENT_SAFETY_REJECT",
    "EXECUTION_OWNER_ACTIVE",
    "RESUME_OWNERSHIP_PROOF_INVALID",
}


def _retry_attempt(error_class: str, action: str) -> dict:
    cases = {
        "resubmit_generation": ("failed", "not_accepted", False, False),
        "poll_remote_operation": ("provider_accepted", "accepted", True, False),
        "retry_storage_commit": ("technically_valid", "accepted", True, True),
        "reconcile_storage_precondition": (
            "technically_valid",
            "accepted",
            True,
            True,
        ),
        "await_charged_generation_authorization": (
            "failed",
            "accepted",
            True,
            False,
        ),
        "do_not_retry": ("failed", "not_accepted", False, False),
        "mark_indeterminate": ("indeterminate", "unknown", False, False),
    }
    phase, acceptance, keep_operation, keep_output = cases[action]
    attempt = _committed_attempt()
    attempt.update(
        {
            "phase": phase,
            "acceptance_knowledge": acceptance,
            "retry_action": action,
            "error": {
                "error_class": error_class,
                "sanitized_message": "typed M0 retry fixture",
            },
        }
    )
    if not keep_operation:
        attempt.pop("provider_operation_id", None)
    if keep_output:
        attempt["output"].pop("storage_receipt_id")
    else:
        attempt.pop("output")
    if acceptance == "not_accepted":
        attempt["cost"].update(
            {"reserved_usd": 0, "known_actual_usd": 0, "potentially_charged_usd": 0}
        )
    elif acceptance == "unknown":
        attempt["cost"].update(
            {
                "reserved_usd": 0.8,
                "known_actual_usd": 0,
                "potentially_charged_usd": 0.8,
            }
        )
    return attempt


def _terminal_state(item_state: str, attempt: dict | None) -> dict:
    state = _valid_state()
    state["storage_receipts"] = []
    state["items"][0].pop("storage_receipt_id")
    state["items"][0]["state"] = item_state
    state["items"][0]["attempt_count"] = int(attempt is not None)
    state["attempts"] = [] if attempt is None else [attempt]
    state["last_attempt_sequence"] = 0 if attempt is None else attempt["dispatch_sequence"]
    state["outcome"] = {
        "failed_terminal": "failed",
        "indeterminate": "indeterminate",
        "cancelled": "cancelled",
    }[item_state]
    state["cost"].update(
        {
            "reserved_usd": 0,
            "known_actual_usd": 0,
            "indeterminate_exposure_usd": 0,
        }
    )
    return state


def _dependency_blocker() -> dict:
    return {
        "kind": "dependency_failure",
        "dependency_item_ids": ["item-001"],
        "reason": "Upstream item failed before this item could run.",
    }


def _dependency_state() -> dict:
    state = _terminal_state(
        "failed_terminal",
        _retry_attempt("PROVIDER_PERMANENT_REJECT", "do_not_retry"),
    )
    state["items"][0]["error_class"] = "PROVIDER_PERMANENT_REJECT"
    state["items"].append(
        {
            "item_id": "item-002",
            "state": "blocked_by_dependency",
            "attempt_count": 0,
            "blocker": _dependency_blocker(),
        }
    )
    return state


def _dependency_result() -> dict:
    result = _valid_result()
    result.update(
        {
            "outcome": "failed",
            "counts": {
                "successful": 0,
                "cache_hit": 0,
                "failed": 1,
                "blocked": 1,
                "indeterminate": 0,
                "cancelled": 0,
            },
            "items": [
                {
                    "item_id": "item-001",
                    "state": "failed_terminal",
                    "error": {
                        "error_class": "PROVIDER_PERMANENT_REJECT",
                        "sanitized_message": "Provider rejected the upstream item.",
                    },
                },
                {
                    "item_id": "item-002",
                    "state": "blocked_by_dependency",
                    "blocker": _dependency_blocker(),
                },
            ],
        }
    )
    result["cost"].update(
        {
            "reserved_usd": 0,
            "known_actual_usd": 0,
            "indeterminate_exposure_usd": 0,
        }
    )
    return result


def test_attempt_schema_freezes_plan_error_taxonomy_and_typed_retry_actions():
    schema = load_execution_schema("attempt")

    assert set(schema["$defs"]["error_class"]["enum"]) == STABLE_ERROR_CLASSES
    assert set(schema["properties"]["retry_action"]["enum"]) == RETRY_ACTIONS
    assert "never authorizes dispatch" in schema["properties"]["retry_action"][
        "description"
    ]
    assert "retry_decision" not in schema["properties"]


@pytest.mark.parametrize(
    ("error_class", "action"),
    [
        ("RATE_LIMITED_SUBMIT_REJECTED", "resubmit_generation"),
        ("PROVIDER_TRANSIENT_PRE_ACCEPT", "resubmit_generation"),
        ("RATE_LIMITED_REMOTE_POLL", "poll_remote_operation"),
        ("REMOTE_JOB_RECOVERABLE", "poll_remote_operation"),
        ("LOCAL_STORAGE_TRANSIENT", "retry_storage_commit"),
        ("GCS_TRANSIENT", "retry_storage_commit"),
        ("GCS_PRECONDITION_CONFLICT", "reconcile_storage_precondition"),
        (
            "OUTPUT_TECHNICALLY_INVALID",
            "await_charged_generation_authorization",
        ),
        ("PROVIDER_PERMANENT_REJECT", "do_not_retry"),
        ("TIMEOUT_OR_NETWORK_UNKNOWN", "mark_indeterminate"),
    ],
)
def test_positive_error_acceptance_operation_and_retry_action_matrix(
    error_class, action
):
    validate_attempt(_retry_attempt(error_class, action))


@pytest.mark.parametrize("error_class", sorted(NOT_ACCEPTED_TERMINAL_ERRORS))
def test_non_retryable_error_taxonomy_is_known_not_accepted_and_terminal(error_class):
    validate_attempt(_retry_attempt(error_class, "do_not_retry"))


def test_internal_bug_preserves_known_or_unknown_acceptance_facts():
    known = _retry_attempt("PROVIDER_PERMANENT_REJECT", "do_not_retry")
    known["error"]["error_class"] = "INTERNAL_BUG"
    validate_attempt(known)

    unknown = _retry_attempt("TIMEOUT_OR_NETWORK_UNKNOWN", "mark_indeterminate")
    unknown["error"]["error_class"] = "INTERNAL_BUG"
    validate_attempt(unknown)


@pytest.mark.parametrize(
    ("error_class", "original_action", "unsafe_action", "error_code"),
    [
        (
            "RATE_LIMITED_REMOTE_POLL",
            "poll_remote_operation",
            "resubmit_generation",
            "INVALID_RETRY_ACTION",
        ),
        (
            "REMOTE_JOB_RECOVERABLE",
            "poll_remote_operation",
            "resubmit_generation",
            "INVALID_RETRY_ACTION",
        ),
        (
            "LOCAL_STORAGE_TRANSIENT",
            "retry_storage_commit",
            "resubmit_generation",
            "INVALID_RETRY_ACTION",
        ),
        (
            "GCS_TRANSIENT",
            "retry_storage_commit",
            "resubmit_generation",
            "INVALID_RETRY_ACTION",
        ),
        (
            "OUTPUT_TECHNICALLY_INVALID",
            "await_charged_generation_authorization",
            "resubmit_generation",
            "INVALID_RETRY_ACTION",
        ),
    ],
)
def test_poll_storage_and_charged_retry_cannot_become_generation_replay(
    error_class, original_action, unsafe_action, error_code
):
    attempt = _retry_attempt(error_class, original_action)
    attempt["retry_action"] = unsafe_action

    with pytest.raises(M0ContractError, match=error_code):
        validate_attempt(attempt)


def test_remote_poll_requires_durable_provider_operation_id():
    attempt = _retry_attempt("REMOTE_JOB_RECOVERABLE", "poll_remote_operation")
    attempt.pop("provider_operation_id")

    with pytest.raises(M0ContractError, match="PROVIDER_OPERATION_ID_REQUIRED"):
        validate_attempt(attempt)


@pytest.mark.parametrize(
    ("error_class", "action", "wrong_acceptance"),
    [
        ("RATE_LIMITED_SUBMIT_REJECTED", "resubmit_generation", "accepted"),
        ("REMOTE_JOB_RECOVERABLE", "poll_remote_operation", "not_accepted"),
        ("LOCAL_STORAGE_TRANSIENT", "retry_storage_commit", "not_accepted"),
        (
            "OUTPUT_TECHNICALLY_INVALID",
            "await_charged_generation_authorization",
            "not_accepted",
        ),
        ("TIMEOUT_OR_NETWORK_UNKNOWN", "mark_indeterminate", "not_accepted"),
    ],
)
def test_retry_action_rejects_acceptance_mismatch(
    error_class, action, wrong_acceptance
):
    attempt = _retry_attempt(error_class, action)
    attempt["acceptance_knowledge"] = wrong_acceptance

    with pytest.raises(M0ContractError, match="INVALID_RETRY_ACTION"):
        validate_attempt(attempt)


def test_generation_resubmit_cannot_reuse_a_remote_operation():
    attempt = _retry_attempt("PROVIDER_TRANSIENT_PRE_ACCEPT", "resubmit_generation")
    attempt["provider_operation_id"] = "existing-operation"

    with pytest.raises(M0ContractError, match="INVALID_RETRY_ACTION"):
        validate_attempt(attempt)


def test_generation_resubmit_requires_charge_free_not_accepted_facts():
    attempt = _retry_attempt("PROVIDER_TRANSIENT_PRE_ACCEPT", "resubmit_generation")
    attempt["cost"]["known_actual_usd"] = 0.1

    with pytest.raises(M0ContractError, match="RETRY_COST_FACTS_INVALID"):
        validate_attempt(attempt)


@pytest.mark.parametrize(
    ("error_class", "action"),
    [
        ("LOCAL_STORAGE_TRANSIENT", "retry_storage_commit"),
        ("GCS_TRANSIENT", "retry_storage_commit"),
        ("GCS_PRECONDITION_CONFLICT", "reconcile_storage_precondition"),
    ],
)
def test_storage_actions_require_already_produced_bytes(error_class, action):
    attempt = _retry_attempt(error_class, action)
    attempt.pop("output")

    with pytest.raises(M0ContractError, match="INVALID_ATTEMPT_STATE"):
        validate_attempt(attempt)


def test_accepted_remote_operation_may_be_marked_indeterminate_but_not_replayed():
    attempt = _retry_attempt("REMOTE_JOB_RECOVERABLE", "poll_remote_operation")
    attempt.update({"phase": "indeterminate", "retry_action": "mark_indeterminate"})
    validate_attempt(attempt)


def test_unknown_paid_acceptance_can_only_be_marked_indeterminate():
    attempt = _retry_attempt("TIMEOUT_OR_NETWORK_UNKNOWN", "mark_indeterminate")
    attempt.update({"phase": "failed", "retry_action": "do_not_retry"})

    with pytest.raises(M0ContractError, match="PAID_AMBIGUITY"):
        validate_attempt(attempt)

    attempt = _retry_attempt("TIMEOUT_OR_NETWORK_UNKNOWN", "mark_indeterminate")
    attempt["cost"].update({"known_actual_usd": 0, "potentially_charged_usd": 0})
    with pytest.raises(M0ContractError, match="PAID_AMBIGUITY"):
        validate_attempt(attempt)


def test_charged_technical_retry_is_only_an_authorization_candidate():
    attempt = _retry_attempt(
        "OUTPUT_TECHNICALLY_INVALID",
        "await_charged_generation_authorization",
    )
    validate_attempt(attempt)
    assert attempt["retry_action"] == "await_charged_generation_authorization"
    assert attempt["retry_action"] != "resubmit_generation"

    attempt["cost"]["known_actual_usd"] = 0
    with pytest.raises(M0ContractError, match="CHARGED_RETRY_FACTS_REQUIRED"):
        validate_attempt(attempt)


def test_dependency_blocker_is_explicit_in_state_and_result():
    validate_batch_state(_dependency_state())
    validate_batch_result(_dependency_result())


@pytest.mark.parametrize("document_factory", [_dependency_state, _dependency_result])
def test_dependency_blocker_must_name_a_known_failed_or_blocked_item(document_factory):
    document = document_factory()
    document["items"][-1]["blocker"]["dependency_item_ids"] = ["invented-item"]

    validator = validate_batch_state if "attempts" in document else validate_batch_result
    with pytest.raises(M0ContractError, match="DEPENDENCY_BLOCKER_INVALID"):
        validator(document)


def test_blocked_item_cannot_hide_a_dispatch_attempt():
    state = _dependency_state()
    attempt = _retry_attempt("PROVIDER_PERMANENT_REJECT", "do_not_retry")
    attempt.update(
        {
            "attempt_id": "attempt-002",
            "item_id": "item-002",
            "dispatch_sequence": 2,
        }
    )
    state["attempts"].append(attempt)
    state["items"][-1]["attempt_count"] = 1
    state["last_attempt_sequence"] = 2

    with pytest.raises(M0ContractError, match="DEPENDENCY_BLOCKER_INVALID"):
        validate_batch_state(state)


def test_result_outcome_and_counts_include_dependency_blockers():
    result = _dependency_result()
    result["outcome"] = "partial_failure"
    with pytest.raises(M0ContractError, match="RESULT_OUTCOME_MISMATCH"):
        validate_batch_result(result)

    result = _dependency_result()
    result["counts"]["blocked"] = 0
    with pytest.raises(M0ContractError, match="RESULT_COUNT_MISMATCH"):
        validate_batch_result(result)


def test_committed_item_must_be_supported_by_latest_attempt():
    state = _valid_state()
    later = _retry_attempt("PROVIDER_PERMANENT_REJECT", "do_not_retry")
    later.update({"attempt_id": "attempt-002", "dispatch_sequence": 2})
    state["attempts"].append(later)
    state["items"][0]["attempt_count"] = 2
    state["last_attempt_sequence"] = 2

    with pytest.raises(M0ContractError, match="ITEM_LATEST_ATTEMPT_MISMATCH"):
        validate_batch_state(state)


def test_terminal_item_states_are_supported_by_latest_attempt_or_no_dispatch_cancel():
    failed = _terminal_state(
        "failed_terminal",
        _retry_attempt("PROVIDER_PERMANENT_REJECT", "do_not_retry"),
    )
    indeterminate = _terminal_state(
        "indeterminate",
        _retry_attempt("TIMEOUT_OR_NETWORK_UNKNOWN", "mark_indeterminate"),
    )
    cancelled = _terminal_state("cancelled", None)
    cancelled_after_dispatch = _retry_attempt("PROVIDER_PERMANENT_REJECT", "do_not_retry")
    cancelled_after_dispatch.update(
        {
            "phase": "cancelled",
            "error": {
                "error_class": "CANCELLED",
                "sanitized_message": "Cancelled before provider acceptance.",
            },
        }
    )

    validate_batch_state(failed)
    validate_batch_state(indeterminate)
    validate_batch_state(cancelled)
    validate_batch_state(_terminal_state("cancelled", cancelled_after_dispatch))


@pytest.mark.parametrize(
    ("item_state", "attempt"),
    [
        (
            "failed_terminal",
            _retry_attempt("PROVIDER_TRANSIENT_PRE_ACCEPT", "resubmit_generation"),
        ),
        (
            "indeterminate",
            _retry_attempt("PROVIDER_PERMANENT_REJECT", "do_not_retry"),
        ),
        (
            "cancelled",
            _retry_attempt("TIMEOUT_OR_NETWORK_UNKNOWN", "mark_indeterminate"),
        ),
    ],
)
def test_terminal_item_state_cannot_hide_latest_attempt_facts(item_state, attempt):
    state = _terminal_state(item_state, deepcopy(attempt))

    with pytest.raises(M0ContractError, match="ITEM_LATEST_ATTEMPT_MISMATCH"):
        validate_batch_state(state)
