"""Batch Executor V2 contracts and M1 local execution primitives.

The local executor is deliberately mechanical: it executes only an already
frozen, authorized assets request through one injected exact adapter. Canonical
publication and the production Gemini transport remain later milestones.
"""

from .contracts import (
    CANONICAL_JSON_VERSION,
    INITIAL_ADAPTER_IDENTITY,
    MVP_ADAPTER_SUPPORT,
    M0ContractError,
    canonical_json_bytes,
    canonical_sha256,
    compute_idempotency_digest,
    compute_work_item_digest,
    derive_attempt_output_path,
    freeze_batch_request,
    validate_attempt,
    validate_batch_request,
    validate_batch_result,
    validate_batch_state,
    validate_contract,
    validate_storage_receipt,
)
from .engine import LocalBatchExecutor
from .storage import LocalStore

__all__ = [
    "CANONICAL_JSON_VERSION",
    "INITIAL_ADAPTER_IDENTITY",
    "MVP_ADAPTER_SUPPORT",
    "M0ContractError",
    "LocalBatchExecutor",
    "LocalStore",
    "canonical_json_bytes",
    "canonical_sha256",
    "compute_idempotency_digest",
    "compute_work_item_digest",
    "derive_attempt_output_path",
    "freeze_batch_request",
    "validate_attempt",
    "validate_batch_request",
    "validate_batch_result",
    "validate_batch_state",
    "validate_contract",
    "validate_storage_receipt",
]
