"""Batch Executor V2 contracts, M1 local execution, and M2 publication.

The local executor is deliberately mechanical: it executes only an already
frozen, authorized assets request through one injected exact adapter. M2 then
applies an immutable Agent-authored command through the official checkpoint
contracts. The production Gemini transport remains an M3 milestone.
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
    freeze_publication_command,
    portable_canonical_asset_identity,
    validate_attempt,
    validate_batch_request,
    validate_batch_result,
    validate_batch_state,
    validate_canonical_asset_path,
    validate_contract,
    validate_publication_command,
    validate_storage_receipt,
)
from .engine import LocalBatchExecutor
from .publication import LocalAssetsPublisher
from .storage import LocalStore

__all__ = [
    "CANONICAL_JSON_VERSION",
    "INITIAL_ADAPTER_IDENTITY",
    "MVP_ADAPTER_SUPPORT",
    "M0ContractError",
    "LocalBatchExecutor",
    "LocalAssetsPublisher",
    "LocalStore",
    "canonical_json_bytes",
    "canonical_sha256",
    "compute_idempotency_digest",
    "compute_work_item_digest",
    "derive_attempt_output_path",
    "freeze_batch_request",
    "freeze_publication_command",
    "portable_canonical_asset_identity",
    "validate_attempt",
    "validate_batch_request",
    "validate_batch_result",
    "validate_batch_state",
    "validate_canonical_asset_path",
    "validate_contract",
    "validate_publication_command",
    "validate_storage_receipt",
]
