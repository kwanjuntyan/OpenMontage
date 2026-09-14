"""Batch Executor V2 contracts and the shared Local/Cloud execution core.

The executor is deliberately mechanical: it executes only an already frozen,
authorized assets request through one injected exact adapter. M2 applies an
immutable Agent-authored command through the official checkpoint contracts.
M3 adds a generation-CAS GCS Store and the one exact Vertex adapter without
giving Python responsibility for pipeline, review, or Human Gate decisions.
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
from .engine import BatchExecutor, CloudBatchExecutor, LocalBatchExecutor
from .gcs_storage import GCSStore
from .publication import LocalAssetsPublisher
from .storage import ExecutionStore, LocalStore

__all__ = [
    "CANONICAL_JSON_VERSION",
    "INITIAL_ADAPTER_IDENTITY",
    "MVP_ADAPTER_SUPPORT",
    "M0ContractError",
    "BatchExecutor",
    "CloudBatchExecutor",
    "ExecutionStore",
    "GCSStore",
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
