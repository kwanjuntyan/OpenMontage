from __future__ import annotations

import inspect
from copy import deepcopy

import pytest

from lib.batch_executor.contracts import (
    INITIAL_ADAPTER_IDENTITY,
    MVP_ADAPTER_SUPPORT,
    M0ContractError,
    SCHEMA_NAMES,
    adapter_observation_blockers,
    canonical_json_bytes,
    canonical_sha256,
    compute_idempotency_digest,
    exact_identity,
    freeze_self_digest,
    load_execution_schema,
    validate_adapter_observation,
    validate_attempt,
    validate_batch_request,
    validate_batch_result,
    validate_batch_state,
    validate_storage_receipt,
)


def _local_receipt():
    return {
        "version": "1.0",
        "receipt_id": "receipt-001",
        "batch_id": "batch-001",
        "item_id": "item-001",
        "attempt_id": "attempt-001",
        "sha256": "c" * 64,
        "size_bytes": 1234,
        "media_type": "video/mp4",
        "probe": {
            "container": "mp4",
            "duration_seconds": 8.0,
            "video_codec": "h264",
            "has_audio": True,
        },
        "store_type": "local",
        "logical_path": ".batch-v2/runs/batch-001/attempts/item-001/attempt-001/clip.mp4",
        "locator": ".batch-v2/blobs/sha256/cc/" + "c" * 64,
        "created_at": "2026-09-14T08:02:00Z",
        "verification": {
            "completed_at": "2026-09-14T08:02:00Z",
            "write_mode": "synchronous",
            "sha256_verified": True,
            "size_verified": True,
            "provider_checksum_verified": False,
            "generation_verified": False,
        },
        "access": "private",
        "encryption": "provider_managed",
    }


def _committed_attempt():
    work_item_digest = "d" * 64
    return {
        "version": "1.0",
        "batch_id": "batch-001",
        "request_digest": "a" * 64,
        "item_id": "item-001",
        "attempt_id": "attempt-001",
        "work_item_digest": work_item_digest,
        "idempotency_digest": compute_idempotency_digest("a" * 64, work_item_digest),
        "identity": exact_identity(),
        "dispatch_sequence": 1,
        "phase": "durably_committed",
        "timestamps": {
            "queued_at": "2026-09-14T08:01:00Z",
            "dispatched_at": "2026-09-14T08:01:01Z",
            "response_received_at": "2026-09-14T08:02:00Z",
            "bytes_verified_at": "2026-09-14T08:02:01Z",
            "committed_at": "2026-09-14T08:02:02Z",
        },
        "acceptance_knowledge": "accepted",
        "billing_mode": "paid",
        "provider_operation_id": "interaction-123",
        "retry_action": "none",
        "cost": {
            "estimated_usd": 0.8,
            "reserved_usd": 0,
            "known_actual_usd": 0.8,
            "potentially_charged_usd": 0,
        },
        "output": {
            "sha256": "c" * 64,
            "size_bytes": 1234,
            "probe": {
                "container": "mp4",
                "duration_seconds": 8.0,
                "video_codec": "h264",
                "has_audio": True,
            },
            "storage_receipt_id": "receipt-001",
        },
    }


def _owner():
    return {
        "version": "1.0",
        "batch_id": "batch-001",
        "request_digest": "a" * 64,
        "invocation_id": "invocation-001",
        "invocation_mode": "run",
        "profile": "local",
        "execution_id": "pid-100",
        "task_id": "main",
        "owner_status": "active",
        "acquired_at": "2026-09-14T08:00:00Z",
        "state_revision": 1,
        "base_state_generation": 0,
    }


def test_all_nine_execution_schemas_are_valid_draft_2020_12():
    assert SCHEMA_NAMES == {
        "batch_request",
        "batch_state",
        "batch_result",
        "attempt",
        "storage_receipt",
        "execution_owner",
        "execution_status_evidence",
        "resume_authorization",
        "publication_command",
    }
    for name in SCHEMA_NAMES:
        schema = load_execution_schema(name)
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["additionalProperties"] is False


def test_canonical_json_is_stable_utf8_finite_and_full_sha256():
    left = {"z": "時鐘", "a": [1, 1.0, True, None]}
    right = {"a": [1, 1.0, True, None], "z": "時鐘"}
    assert canonical_json_bytes(left) == canonical_json_bytes(right)
    assert b" " not in canonical_json_bytes(left)
    digest = canonical_sha256(left)
    assert len(digest) == 64
    assert digest == canonical_sha256(right)
    with pytest.raises(M0ContractError, match="NON_CANONICAL_JSON"):
        canonical_sha256({"bad": float("nan")})


def test_versioned_state_attempt_receipt_and_result_contracts_resolve_refs():
    receipt = _local_receipt()
    attempt = _committed_attempt()
    owner = _owner()
    validate_storage_receipt(receipt)
    validate_attempt(attempt)

    state = {
        "version": "1.0",
        "batch_id": "batch-001",
        "request_digest": "a" * 64,
        "revision": 1,
        "owner": owner,
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
        "attempts": [attempt],
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
        "storage_receipts": [receipt],
    }
    validate_batch_state(state)

    result = {
        "version": "1.0",
        "batch_id": "batch-001",
        "request_digest": "a" * 64,
        "source_bindings": [{"binding_id": "scene-plan", "sha256": "d" * 64}],
        "invocations": [
            {"invocation_id": "invocation-001", "execution_id": "pid-100", "profile": "local"}
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
        "items": [{"item_id": "item-001", "state": "committed", "storage_receipt": receipt}],
        "cost": state["cost"],
        "statistics": {"attempts": 1, "retries": 0, "cache_hits": 0, "rate_limit_wait_seconds": 0},
        "agent_review_hints": ["Inspect the verified video receipt."],
        "created_at": "2026-09-14T08:02:03Z",
    }
    validate_batch_result(result)


@pytest.mark.parametrize(
    ("location", "field", "value"),
    [
        ("root", "next_stage", "edit"),
        ("root", "gate_decision", "approved"),
        ("item", "fallback_tools", ["another_tool"]),
        ("item", "selector", "best_available"),
        ("item", "quality_review", {"auto_approve": True}),
    ],
)
def test_agent_native_contract_rejects_orchestration_and_creative_fields(
    batch_request, location, field, value
):
    request = deepcopy(batch_request)
    target = request if location == "root" else request["work_items"][0]
    target[field] = value
    with pytest.raises(M0ContractError, match="SCHEMA_VALIDATION_FAILED"):
        validate_batch_request(request)


def test_hidden_writer_policy_is_mandatory_and_canonical_writes_are_forbidden(batch_request):
    request = deepcopy(batch_request)
    request["execution_policy"]["side_effect_policy"]["legacy_gcs_auto_sync"] = True
    with pytest.raises(M0ContractError, match="SCHEMA_VALIDATION_FAILED"):
        validate_batch_request(request)
    request = deepcopy(batch_request)
    request["execution_policy"]["side_effect_policy"]["project_event_writes"] = True
    with pytest.raises(M0ContractError, match="SCHEMA_VALIDATION_FAILED"):
        validate_batch_request(request)
    request = deepcopy(batch_request)
    request["execution_policy"]["side_effect_policy"]["canonical_writes"] = True
    with pytest.raises(M0ContractError, match="SCHEMA_VALIDATION_FAILED"):
        validate_batch_request(request)


def test_output_affecting_store_setting_is_digest_bound(batch_request):
    request = deepcopy(batch_request)
    request["work_items"][0]["inputs"]["store"] = False
    with pytest.raises(M0ContractError, match="WORK_ITEM_DIGEST_MISMATCH"):
        validate_batch_request(request)


def test_work_item_digest_directly_binds_ordered_source_content(batch_request):
    request = deepcopy(batch_request)
    request["source_bindings"][0]["sha256"] = "e" * 64
    with pytest.raises(M0ContractError, match="WORK_ITEM_DIGEST_MISMATCH"):
        validate_batch_request(request)


def test_attempt_uses_full_same_request_idempotency_digest():
    attempt = _committed_attempt()
    assert len(attempt["idempotency_digest"]) == 64
    attempt["idempotency_digest"] = "0" * 64
    with pytest.raises(M0ContractError, match="IDEMPOTENCY_DIGEST_MISMATCH"):
        validate_attempt(attempt)


def test_gcs_receipt_requires_synchronous_generation_and_checksum_verification():
    receipt = _local_receipt()
    receipt.update(
        {
            "store_type": "gcs",
            "locator": "gs://private-bucket/sha256/cc/" + "c" * 64,
            "generation": 42,
            "provider_checksum": {"algorithm": "crc32c", "value": "AAAAAA=="},
        }
    )
    receipt["verification"]["provider_checksum_verified"] = True
    receipt["verification"]["generation_verified"] = True
    validate_storage_receipt(receipt)
    receipt["locator"] = "gs://private-bucket/mutable/latest.mp4"
    with pytest.raises(M0ContractError, match="content-addressed"):
        validate_storage_receipt(receipt)
    receipt["locator"] = "gs://private-bucket/sha256/cc/" + "c" * 64
    receipt["verification"]["generation_verified"] = False
    with pytest.raises(M0ContractError, match="INVALID_STORAGE_RECEIPT"):
        validate_storage_receipt(receipt)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("route", "developer_interactions"),
        ("model", "gemini-omni-flash-preview"),
        ("provider", "google_ai_studio"),
        ("operation", "image_to_video"),
    ],
)
def test_exact_route_model_provider_operation_mismatch_fails_closed(batch_request, field, value):
    request = deepcopy(batch_request)
    request["work_items"][0]["identity"][field] = value
    with pytest.raises(M0ContractError, match="SCHEMA_VALIDATION_FAILED"):
        validate_batch_request(request)


def test_credentials_cannot_be_serialized_in_frozen_request(batch_request):
    request = deepcopy(batch_request)
    request["work_items"][0]["inputs"]["api_key"] = "not-a-real-secret"
    with pytest.raises(M0ContractError, match="SCHEMA_VALIDATION_FAILED"):
        validate_batch_request(request)


def test_mvp_support_declaration_freezes_vertex_identity_and_adc(qualified_adapter_observation):
    assert dict(INITIAL_ADAPTER_IDENTITY) == {
        "tool_name": "gemini_omni_video",
        "tool_contract_version": "0.1.0",
        "provider": "gemini_omni",
        "route": "vertex_interactions",
        "model": "gemini-omni-1.1-flash-preview",
        "operation": "text_to_video",
    }
    assert MVP_ADAPTER_SUPPORT["credential_mode"] == "adc"
    assert MVP_ADAPTER_SUPPORT["route_binding"] == "explicit_request"
    assert MVP_ADAPTER_SUPPORT["implementation_status"] == "contract_only_until_m3"
    validate_adapter_observation(qualified_adapter_observation)


def test_current_gemini_adapter_is_explicitly_not_m0_production_qualified():
    from tools.video import gemini_omni_video as current

    source = inspect.getsource(current.GeminiOmniVideo.execute)
    assert "use_vertex = bool" in source
    assert "GOOGLE_GENAI_USE_VERTEXAI" in source
    assert current._DEFAULT_MODEL == "gemini-omni-flash-preview"

    observed_current_behavior = {
        "identity": {
            "tool_name": current.GeminiOmniVideo.name,
            "tool_contract_version": current.GeminiOmniVideo.version,
            "provider": current.GeminiOmniVideo.provider,
            "route": "ambient_credential_selected",
            "model": current._DEFAULT_MODEL,
            "operation": "text_to_video",
        },
        "route_binding": "ambient_credentials",
        "credential_mode": "api_key_or_service_account_file",
        "hidden_writers": "enabled_by_base_tool",
        "available": True,
    }
    blockers = adapter_observation_blockers(observed_current_behavior)
    assert "EXACT_IDENTITY_MISMATCH" in blockers
    assert "ROUTE_NOT_EXPLICIT" in blockers
    assert "ADC_REQUIRED" in blockers
    assert "HIDDEN_WRITERS_NOT_DISABLED" in blockers
    assert "FALLBACK_FORBIDDEN" not in blockers


def test_evidence_schema_rejects_unversioned_or_nonterminal_claim():
    evidence = {
        "version": "1.0",
        "evidence_id": "evidence-001",
        "batch_id": "batch-001",
        "request_digest": "a" * 64,
        "prior_invocation_id": "invocation-old",
        "prior_execution_id": "execution-old",
        "observed_status": "running",
        "observed_at": "2026-09-14T08:30:00Z",
        "verifier": "cloud_run_control_plane_adc",
        "execution_resource": "projects/p/locations/r/jobs/j/executions/old",
    }
    with pytest.raises(M0ContractError, match="SCHEMA_VALIDATION_FAILED"):
        freeze_self_digest(
            evidence,
            schema_name="execution_status_evidence",
            digest_field="evidence_digest",
        )
