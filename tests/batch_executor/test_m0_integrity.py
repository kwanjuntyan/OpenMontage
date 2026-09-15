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
from tests.batch_executor.test_m0_contracts import (
    _committed_attempt,
    _local_receipt,
    _owner,
)


def _valid_state() -> dict:
    return {
        "version": "1.0",
        "batch_id": "batch-001",
        "request_digest": "a" * 64,
        "revision": 1,
        "owner": _owner(),
        "ownership_proof_digests": [],
        "status": "awaiting_agent_review",
        "outcome": "all_succeeded",
        "items": [
            {
                "item_id": "item-001",
                "state": "committed",
                "attempt_count": 1,
                "storage_receipt_id": "receipt-001",
            }
        ],
        "attempts": [_committed_attempt()],
        "provider_policy": {
            "provider": "gemini_omni",
            "route": "vertex_interactions",
            "model": "gemini-omni-1.1-flash-preview",
            "concurrency_cap": 1,
            "min_request_spacing_seconds": 0,
        },
        "cost": {
            "estimated_usd": 0.8,
            "reserved_usd": 0,
            "known_actual_usd": 0.8,
            "indeterminate_exposure_usd": 0,
            "authorized_cap_usd": 1.0,
        },
        "reuse": {"verified_hits": 0, "misses": 1},
        "created_at": "2026-09-14T08:00:00Z",
        "updated_at": "2026-09-14T08:02:02Z",
        "last_attempt_sequence": 1,
        "storage_receipts": [_local_receipt()],
    }


def _valid_result() -> dict:
    return {
        "version": "1.0",
        "batch_id": "batch-001",
        "request_digest": "a" * 64,
        "source_bindings": [{"binding_id": "scene-plan", "sha256": "d" * 64}],
        "invocations": [
            {
                "invocation_id": "invocation-001",
                "execution_id": "pid-100",
                "profile": "local",
            }
        ],
        "ownership_proof_digests": [],
        "status": "awaiting_agent_review",
        "outcome": "all_succeeded",
        "counts": {
            "successful": 1,
            "cache_hit": 0,
            "failed": 0,
            "blocked": 0,
            "indeterminate": 0,
            "cancelled": 0,
        },
        "items": [
            {
                "item_id": "item-001",
                "state": "committed",
                "storage_receipt": _local_receipt(),
            }
        ],
        "cost": {
            "estimated_usd": 0.8,
            "reserved_usd": 0,
            "known_actual_usd": 0.8,
            "indeterminate_exposure_usd": 0,
            "authorized_cap_usd": 1.0,
        },
        "statistics": {
            "attempts": 1,
            "retries": 0,
            "cache_hits": 0,
            "rate_limit_wait_seconds": 0,
        },
        "agent_review_hints": ["Inspect the verified video receipt."],
        "created_at": "2026-09-14T08:02:03Z",
    }


def test_public_schema_load_isolated_from_caller_mutation():
    schema = load_execution_schema("attempt")
    original = schema["properties"]["version"]["const"]
    try:
        schema["properties"]["version"]["const"] = "caller-mutated"
        fresh = load_execution_schema("attempt")
        assert fresh["properties"]["version"]["const"] == "1.0"
    finally:
        schema["properties"]["version"]["const"] = original


@pytest.mark.parametrize(
    ("mutate", "error_code"),
    [
        (
            lambda attempt: attempt["output"].pop("storage_receipt_id"),
            "INVALID_ATTEMPT_STATE",
        ),
        (
            lambda attempt: attempt.update({"retry_action": "do_not_retry"}),
            "INVALID_ATTEMPT_STATE",
        ),
        (
            lambda attempt: attempt.update(
                {
                    "error": {
                        "error_class": "INTERNAL_BUG",
                        "sanitized_message": "must not coexist with committed output",
                    }
                }
            ),
            "INVALID_ATTEMPT_STATE",
        ),
    ],
)
def test_durably_committed_attempt_requires_one_clean_receipted_terminal_state(
    mutate, error_code
):
    attempt = _committed_attempt()
    mutate(attempt)

    with pytest.raises(M0ContractError, match=error_code):
        validate_attempt(attempt)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda attempt: attempt.update({"phase": "failed", "retry_action": "do_not_retry"}),
        lambda attempt: attempt.update(
            {
                "phase": "failed",
                "retry_action": "do_not_retry",
                "error": {
                    "error_class": "REQUEST_CONTRACT_INVALID",
                    "sanitized_message": "terminal request failure",
                },
            }
        ),
    ],
)
def test_failed_attempt_requires_error_and_cannot_claim_output(mutate):
    attempt = _committed_attempt()
    mutate(attempt)

    with pytest.raises(M0ContractError, match="INVALID_ATTEMPT_STATE"):
        validate_attempt(attempt)


def test_unknown_paid_terminal_attempt_must_remain_indeterminate():
    attempt = _committed_attempt()
    attempt.update(
        {
            "phase": "failed",
            "acceptance_knowledge": "unknown",
            "retry_action": "do_not_retry",
            "error": {
                "error_class": "TIMEOUT_OR_NETWORK_UNKNOWN",
                "sanitized_message": "provider acceptance cannot be established",
            },
        }
    )
    attempt.pop("output")

    with pytest.raises(M0ContractError, match="PAID_AMBIGUITY"):
        validate_attempt(attempt)


def test_noncommitted_attempt_cannot_claim_durable_receipt():
    attempt = _committed_attempt()
    attempt["phase"] = "technically_valid"

    with pytest.raises(M0ContractError, match="INVALID_ATTEMPT_STATE"):
        validate_attempt(attempt)


@pytest.mark.parametrize(
    ("mutate", "error_code"),
    [
        (
            lambda state: state["storage_receipts"][0].update({"generation": 8}),
            "INVALID_STORAGE_RECEIPT",
        ),
        (
            lambda state: state["storage_receipts"].append(
                deepcopy(state["storage_receipts"][0])
            ),
            "DUPLICATE_STORAGE_RECEIPT",
        ),
        (
            lambda state: state["storage_receipts"][0].update({"batch_id": "other-batch"}),
            "STORAGE_RECEIPT_IDENTITY_MISMATCH",
        ),
        (
            lambda state: state["storage_receipts"][0].update({"item_id": "other-item"}),
            "STORAGE_RECEIPT_IDENTITY_MISMATCH",
        ),
        (
            lambda state: state["storage_receipts"][0].update(
                {"attempt_id": "other-attempt"}
            ),
            "STORAGE_RECEIPT_IDENTITY_MISMATCH",
        ),
        (
            lambda state: state["attempts"][0]["output"].update(
                {"storage_receipt_id": "missing-receipt"}
            ),
            "ATTEMPT_RECEIPT_MISMATCH",
        ),
        (
            lambda state: state["storage_receipts"][0].update({"sha256": "e" * 64}),
            "INVALID_STORAGE_RECEIPT",
        ),
        (
            lambda state: state["storage_receipts"][0].update({"size_bytes": 4321}),
            "ATTEMPT_RECEIPT_MISMATCH",
        ),
        (
            lambda state: state["storage_receipts"][0]["probe"].update(
                {"duration_seconds": 7.5}
            ),
            "ATTEMPT_RECEIPT_MISMATCH",
        ),
        (
            lambda state: state["storage_receipts"][0]["probe"].update(
                {"duration_seconds": 8}
            ),
            "ATTEMPT_RECEIPT_MISMATCH",
        ),
        (
            lambda state: state["items"][0].update(
                {"storage_receipt_id": "missing-receipt"}
            ),
            "ITEM_RECEIPT_MISMATCH",
        ),
        (
            lambda state: state.update({"last_attempt_sequence": 2}),
            "ATTEMPT_SEQUENCE_MISMATCH",
        ),
        (
            lambda state: state["cost"].update(
                {
                    "reserved_usd": 0.4,
                    "known_actual_usd": 0.4,
                    "indeterminate_exposure_usd": 0.4,
                }
            ),
            "BUDGET_STATE_INVALID",
        ),
    ],
)
def test_batch_state_rejects_cross_record_corruption(mutate, error_code):
    state = _valid_state()
    mutate(state)

    with pytest.raises(M0ContractError, match=error_code):
        validate_batch_state(state)


def test_batch_state_requires_unique_global_dispatch_sequences():
    state = _valid_state()
    second = deepcopy(state["attempts"][0])
    second["attempt_id"] = "attempt-002"
    second["dispatch_sequence"] = 1
    second["output"]["storage_receipt_id"] = "receipt-002"
    state["attempts"].append(second)
    state["items"][0]["attempt_count"] = 2
    second_receipt = deepcopy(state["storage_receipts"][0])
    second_receipt["receipt_id"] = "receipt-002"
    second_receipt["attempt_id"] = "attempt-002"
    state["storage_receipts"].append(second_receipt)

    with pytest.raises(M0ContractError, match="DUPLICATE_ATTEMPT_SEQUENCE"):
        validate_batch_state(state)


def test_committed_item_requires_durably_committed_attempt_and_receipt():
    state = _valid_state()
    state["attempts"] = []
    state["storage_receipts"] = []
    state["items"][0]["attempt_count"] = 0
    state["items"][0].pop("storage_receipt_id")
    state["last_attempt_sequence"] = 0

    with pytest.raises(M0ContractError, match="COMMITTED_ITEM_INCOMPLETE"):
        validate_batch_state(state)


@pytest.mark.parametrize(
    ("mutate", "error_code"),
    [
        (
            lambda result: result.update({"outcome": "failed"}),
            "RESULT_OUTCOME_MISMATCH",
        ),
        (
            lambda result: result["items"][0]["storage_receipt"].update(
                {"batch_id": "other-batch"}
            ),
            "RESULT_RECEIPT_IDENTITY_MISMATCH",
        ),
        (
            lambda result: result["items"][0]["storage_receipt"].update(
                {"item_id": "other-item"}
            ),
            "RESULT_RECEIPT_IDENTITY_MISMATCH",
        ),
        (
            lambda result: result["cost"].update(
                {
                    "reserved_usd": 0.4,
                    "known_actual_usd": 0.4,
                    "indeterminate_exposure_usd": 0.4,
                }
            ),
            "BUDGET_RESULT_INVALID",
        ),
    ],
)
def test_batch_result_rejects_outcome_receipt_and_cost_corruption(mutate, error_code):
    result = _valid_result()
    mutate(result)

    with pytest.raises(M0ContractError, match=error_code):
        validate_batch_result(result)


def test_batch_result_requires_unique_item_and_receipt_ids():
    result = _valid_result()
    duplicate = deepcopy(result["items"][0])
    result["items"].append(duplicate)
    result["counts"]["successful"] = 2

    with pytest.raises(M0ContractError, match="DUPLICATE_RESULT_ITEM"):
        validate_batch_result(result)

    result = _valid_result()
    duplicate = deepcopy(result["items"][0])
    duplicate["item_id"] = "item-002"
    duplicate["storage_receipt"]["item_id"] = "item-002"
    result["items"].append(duplicate)
    result["counts"]["successful"] = 2

    with pytest.raises(M0ContractError, match="DUPLICATE_STORAGE_RECEIPT"):
        validate_batch_result(result)


def test_failed_result_item_cannot_carry_success_receipt():
    result = _valid_result()
    result["items"][0].update(
        {
            "state": "failed_terminal",
            "error": {
                "error_class": "REQUEST_CONTRACT_INVALID",
                "sanitized_message": "terminal request failure",
            },
        }
    )
    result["counts"].update({"successful": 0, "failed": 1})
    result["outcome"] = "failed"

    with pytest.raises(M0ContractError, match="INVALID_BATCH_RESULT"):
        validate_batch_result(result)
