"""Agent-invoked assets publication after an execution has durably stopped.

This module performs no review, approval, stage selection, provider work, or
fallback.  It applies one exact immutable command authored by the Agent (and,
for completion, bound to a later explicit Human Gate reply) through the
repository's official artifact and checkpoint contracts.
"""

from __future__ import annotations

import json
import os
import re
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Mapping

from lib.checkpoint import (
    CheckpointValidationError,
    read_checkpoint,
    validate_checkpoint,
    write_checkpoint,
)
from lib.identity import InvalidProjectIdError, resolve_project_dir
from schemas.artifacts import validate_artifact

from .contracts import (
    CANONICAL_JSON_VERSION,
    M0ContractError,
    canonical_json_bytes,
    canonical_sha256,
    compute_idempotency_digest,
    freeze_publication_authorization,
    validate_contract,
    validate_publication_authorization,
    validate_publication_command,
    validate_publication_state,
)
from .errors import M2PublicationError, StorageConflict
from .gcs_storage import GCSObjectTransport, GCSStore
from .media_validation import MediaValidator
from .ownership import ExecutionStatusVerifier, freeze_execution_status_evidence
from .preflight import validate_frozen_request_authority
from .runtime import CloudInvocationIdentity, CloudRunADCExecutionStatusVerifier
from .side_effects import (
    assert_publication_invocation_allowed,
    publication_execution_scope,
)
from .storage import LocalStore


CrashHook = Callable[[str, Mapping[str, Any]], None]
PublishHook = Callable[[Path, Path], None]


def _latest_attempt(state: Mapping[str, Any], item_id: str) -> Mapping[str, Any] | None:
    attempts = [
        attempt for attempt in state["attempts"] if attempt["item_id"] == item_id
    ]
    return max(attempts, key=lambda attempt: attempt["dispatch_sequence"], default=None)


def _expected_result(
    request: Mapping[str, Any], state: Mapping[str, Any]
) -> dict[str, Any]:
    """Re-derive the complete M1 BatchResult projection from terminal state."""

    receipts = {receipt["receipt_id"]: receipt for receipt in state["storage_receipts"]}
    result_items = []
    for record in state["items"]:
        item_id = record["item_id"]
        item_state = (
            "cache_hit" if record.get("reuse_verified", False) else record["state"]
        )
        result_item: dict[str, Any] = {"item_id": item_id, "state": item_state}
        if item_state in {"committed", "cache_hit"}:
            result_item["storage_receipt"] = deepcopy(
                receipts[record["storage_receipt_id"]]
            )
        elif item_state == "blocked_by_dependency":
            result_item["blocker"] = deepcopy(record["blocker"])
        elif item_state in {"failed_terminal", "indeterminate"}:
            latest = _latest_attempt(state, item_id)
            if latest is not None:
                result_item["error"] = deepcopy(latest["error"])
            else:
                result_item["error"] = {
                    "error_class": record.get("error_class", "INTERNAL_BUG"),
                    "sanitized_message": "Item could not be dispatched within frozen limits.",
                }
        result_items.append(result_item)

    states = [item["state"] for item in result_items]
    counts = {
        "successful": states.count("committed"),
        "cache_hit": states.count("cache_hit"),
        "failed": states.count("failed_terminal"),
        "blocked": states.count("blocked_by_dependency"),
        "indeterminate": states.count("indeterminate"),
        "cancelled": states.count("cancelled"),
    }
    attempted_items = {attempt["item_id"] for attempt in state["attempts"]}
    generation_retries = max(0, len(state["attempts"]) - len(attempted_items))
    operation_retries = sum(
        attempt.get("operation_retry_count", 0) for attempt in state["attempts"]
    )
    return {
        "version": "1.0",
        "batch_id": request["batch_id"],
        "request_digest": request["request_digest"],
        "source_bindings": [
            {"binding_id": binding["binding_id"], "sha256": binding["sha256"]}
            for binding in request["source_bindings"]
        ],
        "invocations": deepcopy(state["invocations"]),
        "ownership_proof_digests": deepcopy(state.get("ownership_proof_digests", [])),
        "status": "awaiting_agent_review",
        "outcome": state["outcome"],
        "counts": counts,
        "items": result_items,
        "cost": deepcopy(state["cost"]),
        "statistics": {
            "attempts": len(state["attempts"]),
            "retries": generation_retries + operation_retries,
            "cache_hits": counts["cache_hit"],
            "rate_limit_wait_seconds": state["rate_limit_wait_seconds"],
        },
        "agent_review_hints": [
            "Review mechanical outputs and receipts before M2 canonical publication."
        ],
        "created_at": state["completed_at"],
    }


def _checkpoint_cost(cost: Mapping[str, Any]) -> dict[str, float]:
    exposure = (
        float(cost["reserved_usd"])
        + float(cost["known_actual_usd"])
        + float(cost["indeterminate_exposure_usd"])
    )
    return {
        "total_spent_usd": float(cost["known_actual_usd"]),
        "total_reserved_usd": float(cost["reserved_usd"])
        + float(cost["indeterminate_exposure_usd"]),
        "budget_remaining_usd": max(0.0, float(cost["authorized_cap_usd"]) - exposure),
    }


def _publication_metadata(command: Mapping[str, Any]) -> dict[str, Any]:
    transition = command["transition"]
    metadata: dict[str, Any] = {
        "version": "1.0",
        "kind": "batch_v2_assets_publication",
        "command_id": command["command_id"],
        "command_digest": command["command_digest"],
        "command_logical_path": (
            f".batch-v2/runs/{command['batch_id']}/publication/commands/"
            f"{command['command_id']}.json"
        ),
        "batch_id": command["batch_id"],
        "request_digest": command["request_digest"],
        "result_sha256": command["result_ref"]["sha256"],
        "result_logical_path": command["result_ref"]["logical_path"],
        "state_sha256": command["state_ref"]["sha256"],
        "state_logical_path": command["state_ref"]["logical_path"],
        "state_revision": command["state_ref"]["revision"],
        "asset_manifest_sha256": command["asset_manifest_sha256"],
        "transition": transition["kind"],
        "target_status": transition["target_status"],
        "agent_review_reference": command["review_evidence"]["review_reference"],
        "execution_owner": {
            "invocation_id": command["execution_owner"]["invocation_id"],
            "execution_id": command["execution_owner"]["execution_id"],
            "profile": command["execution_owner"]["profile"],
            "owner_status": command["execution_owner"]["owner_status"],
        },
    }
    human = transition.get("human_approval_evidence")
    if human is not None:
        metadata["human_approval"] = {
            "approval_id": human["approval_id"],
            "reply_reference": human["reply_reference"],
            "reply_sha256": human["reply_sha256"],
            "approved_at": human["approved_at"],
        }
        metadata["prior_checkpoint_sha256"] = transition["prior_checkpoint_ref"][
            "sha256"
        ]
        metadata["prior_publication_command_digest"] = transition[
            "prior_publication_command_ref"
        ]["sha256"]
    return metadata


def is_exact_v2_publication_checkpoint(
    checkpoint: Mapping[str, Any] | None, command: Mapping[str, Any]
) -> bool:
    """Return whether a checkpoint is the exact output authorized by a command."""

    if checkpoint is None:
        return False
    try:
        validate_publication_command(command)
        return (
            checkpoint.get("project_id") == command["project_id"]
            and checkpoint.get("pipeline_type") == command["pipeline_type"]
            and checkpoint.get("stage") == command["stage"]
            and checkpoint.get("status") == command["transition"]["target_status"]
            and checkpoint.get("human_approval_required") is True
            and checkpoint.get("human_approved")
            is command["transition"]["human_approved"]
            and canonical_json_bytes(
                (checkpoint.get("artifacts") or {}).get("asset_manifest")
            )
            == canonical_json_bytes(command["asset_manifest"])
            and canonical_json_bytes(
                (checkpoint.get("metadata") or {}).get("batch_v2_publication")
            )
            == canonical_json_bytes(_publication_metadata(command))
            and canonical_json_bytes(
                (checkpoint.get("review") or {}).get("batch_v2_agent_review")
            )
            == canonical_json_bytes(command["review_evidence"])
            and canonical_json_bytes(checkpoint.get("cost_snapshot"))
            == canonical_json_bytes(_checkpoint_cost(command["cost_snapshot"]))
        )
    except (KeyError, M0ContractError, TypeError, ValueError):
        return False


def validated_v2_asset_manifest_from_checkpoint(
    project_dir: str | Path, checkpoint: Mapping[str, Any] | None
) -> dict[str, Any] | None:
    """Resolve one validated V2 command/checkpoint pair for Backlot display.

    This intentionally recognizes only the explicit assets publication tag.
    Missing, malformed, path-escaped, or command-mismatched evidence returns
    ``None`` so legacy/non-V2 precedence remains untouched.
    """

    _claimed, manifest, _reason = inspect_v2_asset_manifest_claim(
        project_dir, checkpoint
    )
    return manifest


def inspect_v2_asset_manifest_claim(
    project_dir: str | Path, checkpoint: Mapping[str, Any] | None
) -> tuple[bool, dict[str, Any] | None, str | None]:
    """Classify an explicit V2 assets claim without falling back to loose data."""

    if checkpoint is None or checkpoint.get("_checkpoint_invalid"):
        return False, None, None
    metadata = (checkpoint.get("metadata") or {}).get("batch_v2_publication")
    if not isinstance(metadata, Mapping) or metadata.get("kind") != (
        "batch_v2_assets_publication"
    ):
        return False, None, None
    try:
        root = Path(project_dir).resolve(strict=True)
        validate_checkpoint(dict(checkpoint), pipeline_dir=root.parent)
        if (
            metadata.get("version") != "1.0"
            or not isinstance(metadata.get("batch_id"), str)
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", metadata["batch_id"])
            is None
            or not isinstance(metadata.get("command_id"), str)
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", metadata["command_id"])
            is None
        ):
            return True, None, "batch_v2_publication_command_reference_invalid"
        expected_path = (
            root
            / ".batch-v2"
            / "runs"
            / metadata["batch_id"]
            / "publication"
            / "commands"
            / f"{metadata['command_id']}.json"
        )
        if (
            metadata.get("command_logical_path")
            != expected_path.relative_to(root).as_posix()
        ):
            return True, None, "batch_v2_publication_command_reference_invalid"
        if not expected_path.is_file():
            return True, None, "batch_v2_publication_command_missing"
        resolved_path = expected_path.resolve(strict=True)
        resolved_path.relative_to(root)
        if os.path.normcase(str(resolved_path)) != os.path.normcase(str(expected_path)):
            return True, None, "batch_v2_publication_command_reference_invalid"
        try:
            command = json.loads(resolved_path.read_text(encoding="utf-8"))
            if not isinstance(command, dict):
                raise TypeError("PublicationCommand is not an object")
            validate_publication_command(command)
        except (OSError, json.JSONDecodeError, M0ContractError, TypeError, ValueError):
            return True, None, "batch_v2_publication_command_corrupt"
        if not is_exact_v2_publication_checkpoint(checkpoint, command):
            return True, None, "batch_v2_publication_command_mismatch"
        return True, deepcopy(command["asset_manifest"]), None
    except Exception:
        return True, None, "batch_v2_publication_command_reference_invalid"


class LocalAssetsPublisher:
    """Apply one exact M2 PublicationCommand under the M1 local run lock."""

    def __init__(
        self,
        *,
        projects_root: str | Path,
        media_validator: MediaValidator,
        crash_hook: CrashHook | None = None,
        immutable_publish_hook: PublishHook | None = None,
        asset_publish_hook: PublishHook | None = None,
    ):
        self.projects_root = Path(projects_root).resolve(strict=True)
        self.media_validator = media_validator
        self.crash_hook = crash_hook
        self.immutable_publish_hook = immutable_publish_hook
        self.asset_publish_hook = asset_publish_hook

    def _crash(self, boundary: str, **facts: Any) -> None:
        if self.crash_hook is not None:
            self.crash_hook(boundary, facts)

    @staticmethod
    def _assert_execution_binding(
        command: Mapping[str, Any],
        request: Mapping[str, Any],
        state: Mapping[str, Any],
        result: Mapping[str, Any],
        result_digest: str,
        store: LocalStore,
    ) -> None:
        identity_fields = (
            "batch_id",
            "request_digest",
            "project_id",
            "pipeline_type",
            "stage",
        )
        if any(command[field] != request[field] for field in identity_fields):
            raise M2PublicationError(
                "PUBLICATION_IDENTITY_MISMATCH",
                "PublicationCommand does not bind the durable BatchRequest identity",
            )
        if request["execution_policy"]["storage_profile"] != "local":
            raise M2PublicationError(
                "M2_LOCAL_ONLY", "M2 publisher accepts only the local profile"
            )
        if any(
            canonical_json_bytes(item["identity"])
            != canonical_json_bytes(command["identity"])
            for item in request["work_items"]
        ):
            raise M2PublicationError(
                "PUBLICATION_IDENTITY_MISMATCH",
                "PublicationCommand identity differs from a frozen work item",
            )
        if (
            state["batch_id"] != command["batch_id"]
            or state["request_digest"] != command["request_digest"]
            or state["status"] != "awaiting_agent_review"
            or state["owner"]["owner_status"] not in {"terminal", "cancelled"}
        ):
            raise M2PublicationError(
                "EXECUTION_NOT_STOPPED",
                "BatchState is not a mechanically terminal reviewed-result source",
            )
        if canonical_json_bytes(state["owner"]) != canonical_json_bytes(
            command["execution_owner"]
        ):
            raise M2PublicationError(
                "PUBLICATION_OWNER_IDENTITY_MISMATCH",
                "PublicationCommand owner snapshot differs from durable BatchState",
            )
        expected_state_path = store.state_path.relative_to(store.project_dir).as_posix()
        if (
            command["state_ref"]["logical_path"] != expected_state_path
            or command["state_ref"]["revision"] != state["revision"]
            or command["state_ref"]["sha256"] != canonical_sha256(state)
        ):
            raise M2PublicationError(
                "PUBLICATION_STATE_REF_MISMATCH",
                "PublicationCommand does not bind the exact terminal BatchState",
            )
        expected_result_path = store.result_path.relative_to(
            store.project_dir
        ).as_posix()
        state_result_ref = state.get("result_ref")
        if (
            command["result_ref"]["logical_path"] != expected_result_path
            or command["result_ref"]["sha256"] != result_digest
            or not isinstance(state_result_ref, Mapping)
            or canonical_json_bytes(state_result_ref)
            != canonical_json_bytes(command["result_ref"])
        ):
            raise M2PublicationError(
                "PUBLICATION_RESULT_REF_MISMATCH",
                "PublicationCommand, BatchState, and BatchResult references differ",
            )
        if canonical_json_bytes(result) != canonical_json_bytes(
            _expected_result(request, state)
        ):
            raise M2PublicationError(
                "RESULT_STATE_MISMATCH",
                "BatchResult does not exactly project the durable terminal BatchState",
            )
        if canonical_json_bytes(result["cost"]) != canonical_json_bytes(
            command["cost_snapshot"]
        ):
            raise M2PublicationError(
                "PUBLICATION_COST_MISMATCH",
                "PublicationCommand cost snapshot differs from BatchResult",
            )
        result_created_at = datetime.fromisoformat(
            result["created_at"].replace("Z", "+00:00")
        )
        reviewed_at = datetime.fromisoformat(
            command["review_evidence"]["reviewed_at"].replace("Z", "+00:00")
        )
        command_created_at = datetime.fromisoformat(
            command["created_at"].replace("Z", "+00:00")
        )
        if not result_created_at <= reviewed_at <= command_created_at:
            raise M2PublicationError(
                "PUBLICATION_CHRONOLOGY_INVALID",
                "Publication requires result creation before Agent review before command creation",
            )

    @staticmethod
    def _asset_plan(
        command: Mapping[str, Any],
        request: Mapping[str, Any],
        state: Mapping[str, Any],
        result: Mapping[str, Any],
        *,
        required_store_type: str = "local",
    ) -> list[tuple[Mapping[str, Any], Mapping[str, Any], str]]:
        request_items = {item["item_id"]: item for item in request["work_items"]}
        state_items = {item["item_id"]: item for item in state["items"]}
        result_items = {item["item_id"]: item for item in result["items"]}
        manifest_assets = {
            asset["id"]: asset for asset in command["asset_manifest"]["assets"]
        }
        plan = []
        published_known_cost = Decimal("0")
        for binding in command["asset_bindings"]:
            work_item = request_items.get(binding["item_id"])
            state_item = state_items.get(binding["item_id"])
            result_item = result_items.get(binding["item_id"])
            manifest_asset = manifest_assets.get(binding["asset_id"])
            if (
                work_item is None
                or state_item is None
                or result_item is None
                or manifest_asset is None
                or work_item["asset_id"] != binding["asset_id"]
                or work_item["scene_id"] != manifest_asset["scene_id"]
                or work_item["output_spec"]["canonical_destination_intent"]
                != binding["canonical_path"]
                or manifest_asset["path"] != binding["canonical_path"]
                or manifest_asset["type"] != "video"
                or manifest_asset["source_tool"] != work_item["identity"]["tool_name"]
                or manifest_asset.get("provider") != work_item["identity"]["provider"]
                or manifest_asset.get("model") != work_item["identity"]["model"]
                or manifest_asset.get("prompt") != work_item["inputs"]["prompt"]
                or Decimal(str(manifest_asset.get("duration_seconds", -1)))
                != Decimal(str(work_item["inputs"]["duration"].rstrip("s")))
                or manifest_asset.get("format") != "mp4"
                or state_item["state"] != "committed"
                or result_item["state"] not in {"committed", "cache_hit"}
                or "storage_receipt" not in result_item
            ):
                raise M2PublicationError(
                    "ASSET_RESULT_BINDING_INVALID",
                    "Canonical manifest entry does not bind one exact successful work item",
                )
            receipt = result_item["storage_receipt"]
            latest = _latest_attempt(state, binding["item_id"])
            if (
                receipt["store_type"] != required_store_type
                or state_item.get("storage_receipt_id") != receipt["receipt_id"]
                or binding["storage_receipt_id"] != receipt["receipt_id"]
                or binding["sha256"] != receipt["sha256"]
                or binding["size_bytes"] != receipt["size_bytes"]
                or binding["source_locator"] != receipt["locator"]
                or latest is None
                or latest["phase"] != "durably_committed"
                or latest["work_item_digest"] != work_item["work_item_digest"]
                or canonical_json_bytes(latest["identity"])
                != canonical_json_bytes(work_item["identity"])
                or latest["idempotency_digest"]
                != compute_idempotency_digest(
                    request["request_digest"], work_item["work_item_digest"]
                )
            ):
                raise M2PublicationError(
                    "ASSET_RESULT_BINDING_INVALID",
                    "Publication binding differs from the exact durable receipt/attempt",
                )
            output_spec = dict(work_item["output_spec"])
            output_spec["duration"] = work_item["inputs"]["duration"]
            item_known_cost = Decimal(str(latest["cost"]["known_actual_usd"]))
            if Decimal(str(manifest_asset.get("cost_usd", -1))) != item_known_cost:
                raise M2PublicationError(
                    "ASSET_COST_BINDING_INVALID",
                    "Manifest asset cost differs from its exact durable attempt",
                )
            published_known_cost += item_known_cost
            plan.append((receipt, output_spec, binding["canonical_path"]))
        if Decimal(str(command["asset_manifest"].get("total_cost_usd", -1))) != (
            published_known_cost
        ):
            raise M2PublicationError(
                "ASSET_COST_BINDING_INVALID",
                "Manifest total cost differs from its published durable attempts",
            )
        return plan

    @staticmethod
    def _is_exact_checkpoint(
        checkpoint: Mapping[str, Any] | None, command: Mapping[str, Any]
    ) -> bool:
        return is_exact_v2_publication_checkpoint(checkpoint, command)

    @staticmethod
    def _assert_human_transition(
        command: Mapping[str, Any],
        checkpoint: Mapping[str, Any] | None,
        store: LocalStore,
    ) -> None:
        transition = command["transition"]
        if checkpoint is None:
            raise M2PublicationError(
                "HUMAN_APPROVAL_BINDING_INVALID",
                "Human completion requires the exact prior awaiting_human checkpoint",
            )
        prior_checkpoint = transition["prior_checkpoint_ref"]
        if (
            checkpoint.get("status") != "awaiting_human"
            or checkpoint.get("human_approved") is True
            or canonical_sha256(checkpoint) != prior_checkpoint["sha256"]
            or canonical_sha256(
                (checkpoint.get("artifacts") or {}).get("asset_manifest")
            )
            != command["asset_manifest_sha256"]
        ):
            raise M2PublicationError(
                "HUMAN_APPROVAL_BINDING_INVALID",
                "Current checkpoint is not the exact Agent-reviewed gate state",
            )
        prior_ref = transition["prior_publication_command_ref"]
        prior_command, prior_digest = store.load_publication_command(
            prior_ref["command_id"]
        )
        LocalAssetsPublisher._assert_human_transition_with_prior(
            command,
            checkpoint,
            prior_command=prior_command,
            prior_digest=prior_digest,
            prior_logical_path=store.publication_command_path(prior_ref["command_id"])
            .relative_to(store.project_dir)
            .as_posix(),
        )

    @staticmethod
    def _assert_human_transition_with_prior(
        command: Mapping[str, Any],
        checkpoint: Mapping[str, Any] | None,
        *,
        prior_command: Mapping[str, Any],
        prior_digest: str,
        prior_logical_path: str,
    ) -> None:
        transition = command["transition"]
        if checkpoint is None:
            raise M2PublicationError(
                "HUMAN_APPROVAL_BINDING_INVALID",
                "Human completion requires the exact prior awaiting_human checkpoint",
            )
        prior_checkpoint = transition["prior_checkpoint_ref"]
        if (
            checkpoint.get("status") != "awaiting_human"
            or checkpoint.get("human_approved") is True
            or canonical_sha256(checkpoint) != prior_checkpoint["sha256"]
            or canonical_sha256(
                (checkpoint.get("artifacts") or {}).get("asset_manifest")
            )
            != command["asset_manifest_sha256"]
        ):
            raise M2PublicationError(
                "HUMAN_APPROVAL_BINDING_INVALID",
                "Current checkpoint is not the exact Agent-reviewed gate state",
            )
        prior_ref = transition["prior_publication_command_ref"]
        unchanged_fields = (
            "batch_id",
            "request_digest",
            "project_id",
            "pipeline_type",
            "stage",
            "identity",
            "result_ref",
            "state_ref",
            "execution_owner",
            "asset_manifest",
            "asset_manifest_sha256",
            "asset_bindings",
            "review_evidence",
            "cost_snapshot",
        )
        human = transition["human_approval_evidence"]
        prior_created_at = datetime.fromisoformat(
            prior_command["created_at"].replace("Z", "+00:00")
        )
        approved_at = datetime.fromisoformat(
            human["approved_at"].replace("Z", "+00:00")
        )
        command_created_at = datetime.fromisoformat(
            command["created_at"].replace("Z", "+00:00")
        )
        if (
            prior_digest != prior_ref["sha256"]
            or prior_logical_path != prior_ref["logical_path"]
            or prior_command["transition"]["kind"] != "agent_review_to_awaiting_human"
            or prior_command["command_digest"] != prior_digest
            or any(
                canonical_json_bytes(prior_command[field])
                != canonical_json_bytes(command[field])
                for field in unchanged_fields
            )
            or canonical_json_bytes(prior_command.get("cloud_source"))
            != canonical_json_bytes(command.get("cloud_source"))
            or approved_at <= prior_created_at
            or command_created_at < approved_at
            or (checkpoint.get("metadata") or {})
            .get("batch_v2_publication", {})
            .get("command_digest")
            != prior_digest
        ):
            raise M2PublicationError(
                "HUMAN_APPROVAL_BINDING_INVALID",
                "Prior Agent command/checkpoint chain does not exactly bind this approval",
            )

    @staticmethod
    def _verify_checkpoint(
        checkpoint: Mapping[str, Any] | None, command: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        if checkpoint is None or not LocalAssetsPublisher._is_exact_checkpoint(
            checkpoint, command
        ):
            raise M2PublicationError(
                "CHECKPOINT_ROUNDTRIP_INVALID",
                "Official checkpoint reader did not return the exact authorized publication",
            )
        validate_artifact("asset_manifest", checkpoint["artifacts"]["asset_manifest"])
        return checkpoint

    def publish(self, command: Mapping[str, Any]) -> dict[str, Any]:
        """Publish or idempotently repair one exact local assets transition."""

        assert_publication_invocation_allowed()
        try:
            frozen = deepcopy(dict(command))
            validate_publication_command(frozen)
            if frozen["execution_owner"]["profile"] != "local":
                raise M2PublicationError(
                    "M2_LOCAL_ONLY",
                    "M2 local publisher accepts only local execution authority",
                )
            project_dir = resolve_project_dir(self.projects_root, frozen["project_id"])
        except (M0ContractError, InvalidProjectIdError) as exc:
            if isinstance(exc, M0ContractError):
                raise
            raise M2PublicationError(
                "PUBLICATION_PROJECT_IDENTITY_INVALID", str(exc)
            ) from exc

        store = LocalStore(
            project_dir,
            frozen["batch_id"],
            immutable_publish_hook=self.immutable_publish_hook,
        )
        with (
            store.acquire_publication_lock(),
            store.acquire_run_lock(),
            publication_execution_scope(),
        ):
            request, request_digest = store.load_request()
            validate_frozen_request_authority(request, projects_root=self.projects_root)
            state, _ = store.load_batch_state()
            loaded_result = store.load_result()
            if loaded_result is None:
                raise M2PublicationError(
                    "PUBLICATION_RESULT_MISSING", "Durable BatchResult is missing"
                )
            result, result_digest = loaded_result
            if request_digest != frozen["request_digest"]:
                raise M2PublicationError(
                    "PUBLICATION_REQUEST_MISMATCH",
                    "Durable BatchRequest digest differs from PublicationCommand",
                )
            self._assert_execution_binding(
                frozen, request, state, result, result_digest, store
            )
            asset_plan = self._asset_plan(frozen, request, state, result)

            current = read_checkpoint(
                self.projects_root, frozen["project_id"], "assets"
            )
            exact_checkpoint = self._is_exact_checkpoint(current, frozen)
            if not exact_checkpoint:
                transition_kind = frozen["transition"]["kind"]
                if transition_kind == "agent_review_to_awaiting_human":
                    if current is not None:
                        progress_metadata = current.get("metadata") or {}
                        if (
                            current.get("status") != "in_progress"
                            or progress_metadata.get("batch_id") != frozen["batch_id"]
                            or progress_metadata.get("request_digest")
                            != frozen["request_digest"]
                        ):
                            raise M2PublicationError(
                                "CHECKPOINT_PUBLICATION_CONFLICT",
                                "Agent-reviewed publication may replace only its exact in_progress checkpoint",
                            )
                else:
                    self._assert_human_transition(frozen, current, store)

            # Verify all immutable sources and existing targets before the
            # checkpoint becomes authoritative.  This is read-only and avoids
            # committing a predictably unrepairable manifest.
            for receipt, output_spec, canonical_path in asset_plan:
                store.preflight_canonical_asset(
                    receipt=receipt,
                    canonical_path=canonical_path,
                    validator=self.media_validator,
                    output_spec=output_spec,
                )

            command_path, command_digest = store.write_publication_command_if_absent(
                frozen
            )
            if command_digest != frozen["command_digest"]:
                raise M2PublicationError(
                    "PUBLICATION_COMMAND_DIGEST_MISMATCH",
                    "Durable PublicationCommand digest changed during write",
                )
            self._crash(
                "publication_command_persisted",
                command_id=frozen["command_id"],
                command_digest=command_digest,
            )

            for receipt, output_spec, canonical_path in asset_plan:
                destination, created = store.materialize_canonical_asset(
                    receipt=receipt,
                    canonical_path=canonical_path,
                    validator=self.media_validator,
                    output_spec=output_spec,
                    publish_hook=self.asset_publish_hook,
                )
                self._crash(
                    "publication_asset_materialized",
                    command_id=frozen["command_id"],
                    canonical_path=destination.relative_to(project_dir).as_posix(),
                    created=created,
                )

            for receipt, output_spec, canonical_path in asset_plan:
                store.verify_canonical_asset(
                    receipt=receipt,
                    canonical_path=canonical_path,
                    validator=self.media_validator,
                    output_spec=output_spec,
                )
            self._crash(
                "publication_assets_verified",
                command_id=frozen["command_id"],
            )

            if not exact_checkpoint:
                try:
                    write_checkpoint(
                        self.projects_root,
                        frozen["project_id"],
                        "assets",
                        frozen["transition"]["target_status"],
                        {"asset_manifest": deepcopy(frozen["asset_manifest"])},
                        pipeline_type=frozen["pipeline_type"],
                        checkpoint_policy="guided",
                        human_approval_required=True,
                        human_approved=frozen["transition"]["human_approved"],
                        review={
                            "batch_v2_agent_review": deepcopy(frozen["review_evidence"])
                        },
                        cost_snapshot=_checkpoint_cost(frozen["cost_snapshot"]),
                        metadata={
                            "batch_v2_publication": _publication_metadata(frozen)
                        },
                    )
                except CheckpointValidationError as exc:
                    raise M2PublicationError(
                        "CHECKPOINT_PUBLICATION_FAILED", str(exc)
                    ) from exc
                self._crash(
                    "publication_checkpoint_written",
                    command_id=frozen["command_id"],
                )

            checkpoint = self._verify_checkpoint(
                read_checkpoint(self.projects_root, frozen["project_id"], "assets"),
                frozen,
            )
            self._crash(
                "publication_checkpoint_verified",
                command_id=frozen["command_id"],
            )

            checkpoint_digest = canonical_sha256(checkpoint)
            self._crash(
                "publication_complete",
                command_id=frozen["command_id"],
                checkpoint_sha256=checkpoint_digest,
            )
            return {
                "version": "1.0",
                "command_id": frozen["command_id"],
                "command_digest": frozen["command_digest"],
                "command_logical_path": command_path.relative_to(
                    project_dir
                ).as_posix(),
                "checkpoint_logical_path": "checkpoint_assets.json",
                "checkpoint_sha256": checkpoint_digest,
                "status": checkpoint["status"],
                "human_approved": checkpoint["human_approved"],
                "asset_manifest_sha256": frozen["asset_manifest_sha256"],
                "idempotent": exact_checkpoint,
            }


class CloudAssetsPublisher:
    """Apply one Agent-authored GCS-backed assets publication command.

    This is an explicit publication API, not an execution entrypoint.  It does
    not author review evidence, resolve a Human Gate, or select work/provider
    policy.  A generation-CAS PublicationState grants one process the right to
    perform the sequential canonical writes after independently proving the
    frozen Cloud execution stopped.
    """

    def __init__(
        self,
        *,
        projects_root: str | Path,
        bucket: str,
        transport: GCSObjectTransport,
        media_validator: MediaValidator,
        execution_status_verifier: ExecutionStatusVerifier | None = None,
        crash_hook: CrashHook | None = None,
        immutable_publish_hook: PublishHook | None = None,
        asset_publish_hook: PublishHook | None = None,
        allow_portable_fake: bool = False,
        allow_fake_status_verifier: bool = False,
        now: Callable[[], datetime] | None = None,
    ):
        self.projects_root = Path(projects_root).resolve(strict=True)
        self.bucket = bucket
        self.transport = transport
        self.media_validator = media_validator
        self.execution_status_verifier = execution_status_verifier
        self.crash_hook = crash_hook
        self.immutable_publish_hook = immutable_publish_hook
        self.asset_publish_hook = asset_publish_hook
        self.allow_portable_fake = allow_portable_fake
        self.allow_fake_status_verifier = allow_fake_status_verifier
        self._now_value = now or (lambda: datetime.now(timezone.utc))

    def _now(self) -> str:
        value = self._now_value()
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    def _crash(self, boundary: str, **facts: Any) -> None:
        if self.crash_hook is not None:
            self.crash_hook(boundary, facts)

    @staticmethod
    def _assert_invocation(identity: CloudInvocationIdentity) -> None:
        if (
            not isinstance(identity, CloudInvocationIdentity)
            or identity.trust_source != "cloud_run_launch_contract"
            or identity.task_id != "0"
            or identity.mode not in {"run", "resume"}
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", identity.invocation_id)
            is None
            or re.fullmatch(
                r"projects/[A-Za-z0-9][A-Za-z0-9-]{0,127}/"
                r"locations/[A-Za-z0-9][A-Za-z0-9-]{0,127}/"
                r"jobs/[A-Za-z0-9][A-Za-z0-9-]{0,127}/"
                r"executions/[A-Za-z0-9][A-Za-z0-9-]{0,127}",
                identity.execution_resource,
            )
            is None
        ):
            raise M2PublicationError(
                "PUBLICATION_INVOCATION_INVALID",
                "Cloud publication requires one trusted single-task invocation identity",
            )

    def _assert_cloud_execution_binding(
        self,
        command: Mapping[str, Any],
        request: Mapping[str, Any],
        request_generation: int,
        state: Mapping[str, Any],
        state_generation: int,
        result: Mapping[str, Any],
        result_generation: int,
        store: GCSStore,
    ) -> None:
        identity_fields = (
            "batch_id",
            "request_digest",
            "project_id",
            "pipeline_type",
            "stage",
        )
        if any(command[field] != request[field] for field in identity_fields):
            raise M2PublicationError(
                "PUBLICATION_IDENTITY_MISMATCH",
                "PublicationCommand does not bind the durable GCS BatchRequest identity",
            )
        profile = request["execution_policy"]["storage_profile"]
        if profile == "portable" and self.allow_portable_fake:
            from .fake_gcs import FakeGCS

            portable_fake = isinstance(self.transport, FakeGCS)
        else:
            portable_fake = False
        if profile != "cloud_run" and not (profile == "portable" and portable_fake):
            raise M2PublicationError(
                "CLOUD_PUBLICATION_PROFILE_INVALID",
                "Cloud publisher accepts only cloud_run (or explicit FakeGCS portable qualification)",
            )
        if any(
            canonical_json_bytes(item["identity"])
            != canonical_json_bytes(command["identity"])
            for item in request["work_items"]
        ):
            raise M2PublicationError(
                "PUBLICATION_IDENTITY_MISMATCH",
                "PublicationCommand identity differs from a frozen work item",
            )
        if (
            state["batch_id"] != command["batch_id"]
            or state["request_digest"] != command["request_digest"]
            or state["status"] != "awaiting_agent_review"
            or state["owner"]["profile"] != "cloud_run"
            or state["owner"]["owner_status"] not in {"terminal", "cancelled"}
        ):
            raise M2PublicationError(
                "EXECUTION_NOT_STOPPED",
                "GCS BatchState is not a stopped awaiting_agent_review source",
            )
        if canonical_json_bytes(state["owner"]) != canonical_json_bytes(
            command["execution_owner"]
        ):
            raise M2PublicationError(
                "PUBLICATION_OWNER_IDENTITY_MISMATCH",
                "PublicationCommand owner snapshot differs from durable GCS BatchState",
            )
        cloud = command["cloud_source"]
        if cloud["bucket"] != self.bucket or store.bucket != self.bucket:
            raise M2PublicationError(
                "PUBLICATION_CLOUD_BUCKET_MISMATCH",
                "PublicationCommand names another GCS authority",
            )
        expected = {
            "request": (
                store.request_object_name,
                request_generation,
                canonical_sha256(request),
            ),
            "state": (
                store.state_object_name,
                state_generation,
                canonical_sha256(state),
            ),
            "result": (
                store.result_object_name,
                result_generation,
                canonical_sha256(result),
            ),
        }
        for kind, (name, generation, digest) in expected.items():
            reference = cloud[kind]
            if reference["object_name"] != name:
                raise M2PublicationError(
                    "PUBLICATION_CLOUD_OBJECT_MISMATCH",
                    f"PublicationCommand names another {kind} object",
                )
            if reference["generation"] != generation:
                raise M2PublicationError(
                    "PUBLICATION_CLOUD_GENERATION_MISMATCH",
                    f"PublicationCommand binds a stale {kind} generation",
                )
            if reference["sha256"] != digest:
                raise M2PublicationError(
                    "PUBLICATION_CLOUD_DIGEST_MISMATCH",
                    f"PublicationCommand binds different {kind} bytes",
                )
        if (
            command["state_ref"]["revision"] != state["revision"]
            or command["state_ref"]["sha256"] != canonical_sha256(state)
            or command["result_ref"]["sha256"] != canonical_sha256(result)
        ):
            raise M2PublicationError(
                "PUBLICATION_SOURCE_REF_MISMATCH",
                "PublicationCommand primary refs differ from exact GCS source bytes",
            )
        state_result_ref = state.get("result_ref")
        if not isinstance(state_result_ref, Mapping) or canonical_json_bytes(
            state_result_ref
        ) != canonical_json_bytes(command["result_ref"]):
            raise M2PublicationError(
                "PUBLICATION_RESULT_REF_MISMATCH",
                "GCS BatchState result pointer differs from PublicationCommand",
            )
        if canonical_json_bytes(result) != canonical_json_bytes(
            _expected_result(request, state)
        ):
            raise M2PublicationError(
                "RESULT_STATE_MISMATCH",
                "GCS BatchResult does not exactly project terminal BatchState",
            )
        if canonical_json_bytes(result["cost"]) != canonical_json_bytes(
            command["cost_snapshot"]
        ):
            raise M2PublicationError(
                "PUBLICATION_COST_MISMATCH",
                "PublicationCommand cost snapshot differs from GCS BatchResult",
            )
        result_created_at = datetime.fromisoformat(
            result["created_at"].replace("Z", "+00:00")
        )
        reviewed_at = datetime.fromisoformat(
            command["review_evidence"]["reviewed_at"].replace("Z", "+00:00")
        )
        command_created_at = datetime.fromisoformat(
            command["created_at"].replace("Z", "+00:00")
        )
        if not result_created_at <= reviewed_at <= command_created_at:
            raise M2PublicationError(
                "PUBLICATION_CHRONOLOGY_INVALID",
                "Publication requires result creation before Agent review before command creation",
            )

    @staticmethod
    def _assert_publication_lifecycle(
        command: Mapping[str, Any],
        checkpoint: Mapping[str, Any] | None,
        publication_state: Mapping[str, Any] | None,
        prior_command: Mapping[str, Any] | None,
        prior_command_generation: int | None,
    ) -> None:
        transition = command["transition"]
        if transition["kind"] == "agent_review_to_awaiting_human":
            if (
                publication_state is not None
                and publication_state["completed_commands"]
            ):
                raise M2PublicationError(
                    "CHECKPOINT_PUBLICATION_CONFLICT",
                    "Agent review cannot replace an existing Cloud publication lifecycle",
                )
            if checkpoint is not None:
                progress_metadata = checkpoint.get("metadata") or {}
                if (
                    checkpoint.get("status") != "in_progress"
                    or progress_metadata.get("batch_id") != command["batch_id"]
                    or progress_metadata.get("request_digest")
                    != command["request_digest"]
                ):
                    raise M2PublicationError(
                        "CHECKPOINT_PUBLICATION_CONFLICT",
                        "Agent publication may replace only its exact in_progress checkpoint",
                    )
            return
        if prior_command is None:
            raise M2PublicationError(
                "HUMAN_APPROVAL_BINDING_INVALID",
                "Human completion requires its durable prior GCS command",
            )
        LocalAssetsPublisher._assert_human_transition_with_prior(
            command,
            checkpoint,
            prior_command=prior_command,
            prior_digest=str(prior_command["command_digest"]),
            prior_logical_path=(
                f".batch-v2/runs/{command['batch_id']}/publication/commands/"
                f"{prior_command['command_id']}.json"
            ),
        )
        completed_commands = (
            publication_state["completed_commands"]
            if publication_state is not None
            else []
        )
        is_exact_completed_replay = (
            len(completed_commands) == 2
            and completed_commands[-1]["command_digest"] == command["command_digest"]
        )
        if len(completed_commands) != (2 if is_exact_completed_replay else 1):
            raise M2PublicationError(
                "HUMAN_APPROVAL_BINDING_INVALID",
                "Human completion requires exactly one prior Agent publication completion",
            )
        completion = completed_commands[0]
        prior_ref = transition["prior_publication_command_ref"]
        if (
            completion["command_id"] != prior_ref["command_id"]
            or completion["command_digest"] != prior_ref["sha256"]
            or completion["command_generation"] != prior_ref.get("gcs_generation")
            or prior_command_generation != prior_ref.get("gcs_generation")
            or completion["checkpoint_document_sha256"]
            != transition["prior_checkpoint_ref"]["sha256"]
            or completion["checkpoint"]["generation"]
            != transition["prior_checkpoint_ref"].get("gcs_generation")
        ):
            raise M2PublicationError(
                "HUMAN_APPROVAL_BINDING_INVALID",
                "PublicationState does not bind the prior Agent command/checkpoint",
            )

    def _validate_stop_proof(
        self,
        *,
        command: Mapping[str, Any],
        state: Mapping[str, Any],
        identity: CloudInvocationIdentity,
        publication_state: Mapping[str, Any] | None,
        publication_authorization: Mapping[str, Any] | None,
    ) -> tuple[str, str, str, dict[str, Any]]:
        verifier = self.execution_status_verifier
        if (verifier is None) == (publication_authorization is None):
            raise M2PublicationError(
                "PUBLICATION_STOP_PROOF_REQUIRED",
                "Provide exactly one trusted status verifier or bound Human authorization",
            )
        active_owner = publication_state.get("owner") if publication_state else None
        same_active_process = (
            isinstance(active_owner, Mapping)
            and active_owner.get("owner_status") in {"active", "repairing"}
            and active_owner.get("invocation_id") == identity.invocation_id
            and active_owner.get("execution_id") == identity.execution_resource
            and active_owner.get("task_id") == identity.task_id
            and active_owner.get("command_digest") == command["command_digest"]
        )
        same_completed_process = (
            isinstance(active_owner, Mapping)
            and active_owner.get("owner_status") == "completed"
            and active_owner.get("invocation_id") == identity.invocation_id
            and active_owner.get("execution_id") == identity.execution_resource
            and active_owner.get("task_id") == identity.task_id
            and active_owner.get("command_digest") == command["command_digest"]
        )
        if (
            isinstance(active_owner, Mapping)
            and active_owner.get("owner_status") in {"active", "repairing"}
            and not same_active_process
        ):
            proof_scope = "publication_takeover"
            proof_owner = {
                "version": "1.0",
                "batch_id": command["batch_id"],
                "request_digest": command["request_digest"],
                "invocation_id": active_owner["invocation_id"],
                "invocation_mode": "resume",
                "profile": "cloud_run",
                "execution_id": active_owner["execution_id"],
                "task_id": active_owner["task_id"],
                "owner_status": "active",
                "acquired_at": active_owner["acquired_at"],
                "state_revision": publication_state["revision"],
                "base_state_generation": command["cloud_source"]["state"]["generation"],
            }
            validate_contract("execution_owner", proof_owner)
        else:
            proof_scope = "source_execution"
            proof_owner = state["owner"]
        if publication_authorization is not None:
            try:
                validate_publication_authorization(publication_authorization)
                frozen = freeze_publication_authorization(publication_authorization)
            except M0ContractError as exc:
                raise M2PublicationError(
                    "PUBLICATION_AUTHORIZATION_INVALID", str(exc)
                ) from exc
            digest = str(publication_authorization["authorization_digest"])
            consumed = (
                publication_state.get("consumed_authorization_digests", [])
                if publication_state is not None
                else []
            )
            same_active = (
                same_active_process or same_completed_process
            ) and active_owner.get("proof", {}).get("digest") == digest
            if digest in consumed and not same_active:
                raise M2PublicationError(
                    "PUBLICATION_AUTHORIZATION_REPLAY",
                    "Human publication authorization was already consumed",
                )
            if (
                frozen["authorization_digest"] != digest
                or publication_authorization["scope"] != proof_scope
                or publication_authorization["batch_id"] != command["batch_id"]
                or publication_authorization["request_digest"]
                != command["request_digest"]
                or publication_authorization["prior_invocation_id"]
                != proof_owner["invocation_id"]
                or publication_authorization["prior_execution_id"]
                != proof_owner["execution_id"]
                or publication_authorization["prior_task_id"] != proof_owner["task_id"]
                or publication_authorization["intended_publication_invocation_id"]
                != identity.invocation_id
                or publication_authorization["intended_publication_execution_id"]
                != identity.execution_resource
                or publication_authorization["intended_publication_task_id"]
                != identity.task_id
                or publication_authorization["command_id"] != command["command_id"]
                or publication_authorization["command_digest"]
                != command["command_digest"]
                or publication_authorization["source_state_generation"]
                != command["cloud_source"]["state"]["generation"]
                or publication_authorization["source_state_sha256"]
                != command["state_ref"]["sha256"]
            ):
                raise M2PublicationError(
                    "PUBLICATION_AUTHORIZATION_BINDING_INVALID",
                    "Human authorization does not bind this source, command, and publisher",
                )
            return (
                "human_publication_authorization",
                proof_scope,
                digest,
                deepcopy(frozen),
            )

        assert verifier is not None
        if type(verifier) is not CloudRunADCExecutionStatusVerifier:
            from .fake_gcs import FakeGCS

            explicitly_fake = (
                self.allow_fake_status_verifier
                and isinstance(self.transport, FakeGCS)
                and getattr(verifier, "verifier_id", None)
                == "cloud_run_control_plane_adc"
            )
            if not explicitly_fake:
                raise M2PublicationError(
                    "UNTRUSTED_EXECUTION_EVIDENCE",
                    "Production Cloud publication requires the concrete ADC control-plane verifier",
                )
        if verifier.verifier_id != "cloud_run_control_plane_adc":
            raise M2PublicationError(
                "UNTRUSTED_EXECUTION_EVIDENCE",
                "Cloud publication accepts only the ADC control-plane verifier",
            )
        try:
            evidence = dict(verifier.verify_stopped(proof_owner))
            validate_contract("execution_status_evidence", evidence)
            frozen_evidence = freeze_execution_status_evidence(evidence)
        except Exception as exc:
            raise M2PublicationError(
                "EXECUTION_STATUS_VERIFICATION_FAILED",
                f"Trusted execution status verification failed: {exc}",
            ) from exc
        if (
            frozen_evidence["evidence_digest"] != evidence["evidence_digest"]
            or evidence["batch_id"] != command["batch_id"]
            or evidence["request_digest"] != command["request_digest"]
            or evidence["prior_invocation_id"] != proof_owner["invocation_id"]
            or evidence["prior_execution_id"] != proof_owner["execution_id"]
            or evidence["execution_resource"] != proof_owner["execution_id"]
            or evidence["observed_status"] not in {"terminal", "cancelled"}
        ):
            raise M2PublicationError(
                "PUBLICATION_STOP_PROOF_MISMATCH",
                "Trusted execution evidence does not bind the exact source owner",
            )
        return (
            "trusted_execution_status",
            proof_scope,
            str(evidence["evidence_digest"]),
            deepcopy(evidence),
        )

    @staticmethod
    def _same_active_owner(
        publication_state: Mapping[str, Any],
        command: Mapping[str, Any],
        identity: CloudInvocationIdentity,
        proof_kind: str,
        proof_scope: str,
        proof_digest: str,
    ) -> bool:
        owner = publication_state["owner"]
        return (
            owner["owner_status"] in {"active", "repairing"}
            and owner["invocation_id"] == identity.invocation_id
            and owner["execution_id"] == identity.execution_resource
            and owner["task_id"] == identity.task_id
            and owner["command_id"] == command["command_id"]
            and owner["command_digest"] == command["command_digest"]
            and owner["proof"]["kind"] == proof_kind
            and owner["proof"]["scope"] == proof_scope
            and owner["proof"]["digest"] == proof_digest
        )

    def _acquire_claim(
        self,
        *,
        store: GCSStore,
        command: Mapping[str, Any],
        identity: CloudInvocationIdentity,
        proof_kind: str,
        proof_scope: str,
        proof_digest: str,
        proof_document: Mapping[str, Any],
    ) -> tuple[dict[str, Any], int, bool]:
        loaded = store.load_publication_state()
        repair_claim = False
        if loaded is None:
            if command["transition"]["kind"] != "agent_review_to_awaiting_human":
                raise M2PublicationError(
                    "HUMAN_APPROVAL_BINDING_INVALID",
                    "Human completion cannot initialize publication state",
                )
            state = {
                "version": "1.0",
                "canonical_json": CANONICAL_JSON_VERSION,
                "project_id": command["project_id"],
                "batch_id": command["batch_id"],
                "request_digest": command["request_digest"],
                "revision": 0,
                "source": deepcopy(command["cloud_source"]),
                "owner": {
                    "invocation_id": identity.invocation_id,
                    "execution_id": identity.execution_resource,
                    "task_id": identity.task_id,
                    "owner_status": "active",
                    "command_id": command["command_id"],
                    "command_digest": command["command_digest"],
                    "acquired_at": self._now(),
                    "proof": {
                        "kind": proof_kind,
                        "scope": proof_scope,
                        "digest": proof_digest,
                    },
                },
                "completed_commands": [],
                "consumed_authorization_digests": (
                    [proof_digest]
                    if proof_kind == "human_publication_authorization"
                    else []
                ),
            }
            expected_generation = None
        else:
            prior, prior_generation = loaded
            if (
                prior["project_id"] != command["project_id"]
                or prior["batch_id"] != command["batch_id"]
                or prior["request_digest"] != command["request_digest"]
                or canonical_json_bytes(prior["source"])
                != canonical_json_bytes(command["cloud_source"])
            ):
                raise M2PublicationError(
                    "PUBLICATION_SOURCE_STATE_CONFLICT",
                    "Existing PublicationState names another immutable execution source",
                )
            if self._same_active_owner(
                prior,
                command,
                identity,
                proof_kind,
                proof_scope,
                proof_digest,
            ):
                reread = store.load_publication_state()
                if (
                    reread is None
                    or reread[1] != prior_generation
                    or canonical_json_bytes(reread[0]) != canonical_json_bytes(prior)
                ):
                    raise M2PublicationError(
                        "PUBLICATION_CLAIM_REREAD_FAILED",
                        "Active publication claim changed during exact resume",
                    )
                repair_claim = bool(
                    prior["completed_commands"]
                    and prior["completed_commands"][-1]["command_digest"]
                    == command["command_digest"]
                )
                return prior, prior_generation, repair_claim
            if prior["owner"]["owner_status"] in {"active", "repairing"}:
                repair_claim = bool(
                    prior["completed_commands"]
                    and prior["completed_commands"][-1]["command_digest"]
                    == command["command_digest"]
                )
                if (
                    proof_scope != "publication_takeover"
                    or prior["owner"]["command_id"] != command["command_id"]
                    or prior["owner"]["command_digest"] != command["command_digest"]
                    or prior["owner"]["invocation_id"]
                    != proof_document.get("prior_invocation_id")
                    or prior["owner"]["execution_id"]
                    != proof_document.get("prior_execution_id")
                    or (
                        proof_kind == "human_publication_authorization"
                        and prior["owner"]["task_id"]
                        != proof_document.get("prior_task_id")
                    )
                ):
                    raise M2PublicationError(
                        "PUBLICATION_OWNER_ACTIVE",
                        "Another Cloud publication process owns the active claim",
                    )
                state = deepcopy(prior)
                state["revision"] += 1
                state["owner"] = {
                    "invocation_id": identity.invocation_id,
                    "execution_id": identity.execution_resource,
                    "task_id": identity.task_id,
                    "owner_status": "repairing" if repair_claim else "active",
                    "command_id": command["command_id"],
                    "command_digest": command["command_digest"],
                    "acquired_at": self._now(),
                    "proof": {
                        "kind": proof_kind,
                        "scope": proof_scope,
                        "digest": proof_digest,
                    },
                }
                if proof_kind == "human_publication_authorization":
                    if proof_digest in state["consumed_authorization_digests"]:
                        raise M2PublicationError(
                            "PUBLICATION_AUTHORIZATION_REPLAY",
                            "Human publication authorization was already consumed",
                        )
                    state["consumed_authorization_digests"].append(proof_digest)
                expected_generation = prior_generation
            elif (
                prior["completed_commands"]
                and prior["completed_commands"][-1]["command_digest"]
                == command["command_digest"]
            ):
                owner = prior["owner"]
                if not (
                    owner["invocation_id"] == identity.invocation_id
                    and owner["execution_id"] == identity.execution_resource
                    and owner["task_id"] == identity.task_id
                    and owner["command_id"] == command["command_id"]
                    and owner["proof"]["kind"] == proof_kind
                    and owner["proof"]["scope"] == proof_scope
                    and owner["proof"]["digest"] == proof_digest
                ):
                    raise M2PublicationError(
                        "PUBLICATION_COMPLETION_OWNER_MISMATCH",
                        "A completed publication may be repaired only by its exact owner/proof",
                    )
                state = deepcopy(prior)
                state["revision"] += 1
                state["owner"] = {
                    "invocation_id": identity.invocation_id,
                    "execution_id": identity.execution_resource,
                    "task_id": identity.task_id,
                    "owner_status": "repairing",
                    "command_id": command["command_id"],
                    "command_digest": command["command_digest"],
                    "acquired_at": self._now(),
                    "proof": {
                        "kind": proof_kind,
                        "scope": proof_scope,
                        "digest": proof_digest,
                    },
                }
                state["owner"].pop("completed_at", None)
                repair_claim = True
                expected_generation = prior_generation
            elif (
                command["transition"]["kind"] != "human_approval_to_completed"
                or len(prior["completed_commands"]) != 1
            ):
                raise M2PublicationError(
                    "CHECKPOINT_PUBLICATION_CONFLICT",
                    "Cloud publication lifecycle does not permit this next command",
                )
            else:
                human = command["transition"]["human_approval_evidence"]
                human_digest = canonical_sha256(human)
                if any(
                    completion.get("human_approval_id") == human["approval_id"]
                    or completion.get("human_approval_digest") == human_digest
                    for completion in prior["completed_commands"]
                ):
                    raise M2PublicationError(
                        "HUMAN_APPROVAL_REPLAY",
                        "Human approval evidence was already used by another command",
                    )
                state = deepcopy(prior)
                state["revision"] += 1
                state["owner"] = {
                    "invocation_id": identity.invocation_id,
                    "execution_id": identity.execution_resource,
                    "task_id": identity.task_id,
                    "owner_status": "active",
                    "command_id": command["command_id"],
                    "command_digest": command["command_digest"],
                    "acquired_at": self._now(),
                    "proof": {
                        "kind": proof_kind,
                        "scope": proof_scope,
                        "digest": proof_digest,
                    },
                }
                if proof_kind == "human_publication_authorization":
                    if proof_digest in state["consumed_authorization_digests"]:
                        raise M2PublicationError(
                            "PUBLICATION_AUTHORIZATION_REPLAY",
                            "Human publication authorization was already consumed",
                        )
                    state["consumed_authorization_digests"].append(proof_digest)
                expected_generation = prior_generation
        validate_publication_state(state)
        try:
            generation = store.save_publication_state(
                state, expected_generation=expected_generation
            )
        except Exception as exc:
            if getattr(exc, "code", None) == "GCS_PRECONDITION_CONFLICT":
                raise M2PublicationError(
                    "PUBLICATION_CLAIM_CONFLICT",
                    "Another Cloud publisher won the ownership CAS",
                ) from exc
            raise
        reread = store.load_publication_state()
        if (
            reread is None
            or reread[1] != generation
            or canonical_json_bytes(reread[0]) != canonical_json_bytes(state)
        ):
            raise M2PublicationError(
                "PUBLICATION_CLAIM_REREAD_FAILED",
                "Cloud publication CAS winner could not be re-read exactly",
            )
        return state, generation, repair_claim

    @staticmethod
    def _assert_claim_current(
        *,
        store: GCSStore,
        publication_state: Mapping[str, Any],
        publication_generation: int,
        fence: Mapping[str, Any],
        fence_generation: int,
        require_active: bool = True,
    ) -> None:
        """Fail closed if either batch ownership or project authority changed."""

        store.verify_publication_fence(fence, generation=fence_generation)
        loaded = store.load_publication_state()
        if (
            loaded is None
            or loaded[1] != publication_generation
            or canonical_json_bytes(loaded[0])
            != canonical_json_bytes(publication_state)
            or (
                require_active
                and publication_state["owner"]["owner_status"]
                not in {"active", "repairing"}
            )
        ):
            raise M2PublicationError(
                "PUBLICATION_OWNER_LOST",
                "Publication owner/fence changed before a canonical mutation",
            )

    def _completed_receipt(
        self,
        *,
        command: Mapping[str, Any],
        project_dir: Path,
        publication_state: Mapping[str, Any],
        state_generation: int,
        command_generation: int,
        idempotent: bool,
        local_store: LocalStore,
        gcs_store: GCSStore,
        asset_plan: list[tuple[Mapping[str, Any], Mapping[str, Any], str]],
        publication_fence: Mapping[str, Any],
        fence_generation: int,
    ) -> dict[str, Any]:
        self._assert_claim_current(
            store=gcs_store,
            publication_state=publication_state,
            publication_generation=state_generation,
            fence=publication_fence,
            fence_generation=fence_generation,
            require_active=False,
        )
        if publication_state["owner"]["owner_status"] == "repairing":
            self._crash(
                "cloud_publication_repair_claim_acquired",
                command_id=command["command_id"],
                publication_state_generation=state_generation,
            )
        completion = publication_state["completed_commands"][-1]
        if (
            completion["command_id"] != command["command_id"]
            or publication_state["owner"]["command_id"] != command["command_id"]
            or publication_state["owner"]["command_digest"]
            != command["command_digest"]
            or completion["command_digest"] != command["command_digest"]
            or completion["command_generation"] != command_generation
            or completion["checkpoint"]["logical_path"] != "checkpoint_assets.json"
        ):
            raise M2PublicationError(
                "PUBLICATION_COMPLETION_INVALID",
                "PublicationState completion does not bind the exact checkpoint",
            )
        try:
            prior_command = None
            prior_completion = None
            prior_checkpoint_payload = None
            prior_checkpoint_document = None
            if command["transition"]["kind"] == "human_approval_to_completed":
                prior_id = command["transition"]["prior_publication_command_ref"][
                    "command_id"
                ]
                prior_command, prior_generation = gcs_store.load_publication_command(
                    prior_id
                )
                if (
                    prior_generation
                    != command["transition"]["prior_publication_command_ref"][
                        "gcs_generation"
                    ]
                ):
                    raise ValueError("prior command generation differs")
                if len(publication_state["completed_commands"]) != 2:
                    raise ValueError("completed Human transition has no exact prior")
                prior_completion = publication_state["completed_commands"][0]
                if (
                    prior_completion["command_id"] != prior_command["command_id"]
                    or prior_completion["command_digest"]
                    != prior_command["command_digest"]
                    or prior_completion["command_generation"] != prior_generation
                ):
                    raise ValueError("prior completion differs from durable command")
                _, prior_checkpoint_payload, prior_checkpoint_document = (
                    gcs_store.read_publication_checkpoint_snapshot(
                        command=prior_command,
                        expected_facts=prior_completion["checkpoint_snapshot"],
                        expected_document_sha256=prior_completion[
                            "checkpoint_document_sha256"
                        ],
                        validator=lambda candidate: (
                            LocalAssetsPublisher._verify_checkpoint(
                                candidate, prior_command
                            )
                        ),
                    )
                )
                # The immutable per-command snapshot plus completion journal is
                # the replay authority. Do not require the superseded prior
                # canonical generation: a bucket need not retain old versions.
            asset_objects = {
                record["logical_path"]: record for record in completion["asset_objects"]
            }
            if len(asset_objects) != len(asset_plan):
                raise ValueError("completion asset count differs")
            recovery_plan = []
            for receipt, output_spec, canonical_path in asset_plan:
                self._assert_claim_current(
                    store=gcs_store,
                    publication_state=publication_state,
                    publication_generation=state_generation,
                    fence=publication_fence,
                    fence_generation=fence_generation,
                    require_active=False,
                )
                staging = (
                    local_store.run_dir
                    / "publication"
                    / "recovery"
                    / str(command["command_id"])
                    / str(receipt["item_id"])
                    / "source.mp4"
                )
                gcs_store.materialize_workspace_asset(
                    facts=asset_objects[canonical_path],
                    receipt=receipt,
                    destination=staging,
                )
                local_store.preflight_materialized_canonical_asset(
                    source=staging,
                    receipt=receipt,
                    canonical_path=canonical_path,
                    validator=self.media_validator,
                    output_spec=output_spec,
                )
                recovery_plan.append(
                    (staging, receipt, output_spec, canonical_path)
                )
            _, checkpoint_payload, checkpoint_document = (
                gcs_store.read_publication_checkpoint_snapshot(
                    command=command,
                    expected_facts=completion["checkpoint_snapshot"],
                    expected_document_sha256=completion["checkpoint_document_sha256"],
                    validator=lambda candidate: LocalAssetsPublisher._verify_checkpoint(
                        candidate, command
                    ),
                )
            )
            gcs_store.verify_workspace_checkpoint(
                facts=completion["checkpoint"],
                payload=checkpoint_payload,
                checkpoint=checkpoint_document,
                command=command,
            )
            self._assert_claim_current(
                store=gcs_store,
                publication_state=publication_state,
                publication_generation=state_generation,
                fence=publication_fence,
                fence_generation=fence_generation,
                require_active=False,
            )
            local_store.write_publication_command_if_absent(command)
            if prior_command is not None:
                local_store.write_publication_command_if_absent(prior_command)
            for staging, receipt, output_spec, canonical_path in recovery_plan:
                self._assert_claim_current(
                    store=gcs_store,
                    publication_state=publication_state,
                    publication_generation=state_generation,
                    fence=publication_fence,
                    fence_generation=fence_generation,
                    require_active=False,
                )
                destination, _ = local_store.materialize_from_publication_staging(
                    source=staging,
                    receipt=receipt,
                    canonical_path=canonical_path,
                    validator=self.media_validator,
                    output_spec=output_spec,
                )
                gcs_store.verify_workspace_asset(
                    facts=asset_objects[canonical_path],
                    payload=destination.read_bytes(),
                    receipt=receipt,
                )
            self._crash(
                "cloud_publication_recovery_assets_restored",
                command_id=command["command_id"],
                publication_state_generation=state_generation,
            )
            self._assert_claim_current(
                store=gcs_store,
                publication_state=publication_state,
                publication_generation=state_generation,
                fence=publication_fence,
                fence_generation=fence_generation,
                require_active=False,
            )
            current_checkpoint = read_checkpoint(
                self.projects_root, command["project_id"], "assets"
            )
            if not LocalAssetsPublisher._is_exact_checkpoint(
                current_checkpoint, command
            ):
                if command["transition"]["kind"] == "human_approval_to_completed":
                    assert prior_command is not None
                    assert prior_checkpoint_payload is not None
                    assert prior_checkpoint_document is not None
                    if not LocalAssetsPublisher._is_exact_checkpoint(
                        current_checkpoint, prior_command
                    ):
                        self._assert_claim_current(
                            store=gcs_store,
                            publication_state=publication_state,
                            publication_generation=state_generation,
                            fence=publication_fence,
                            fence_generation=fence_generation,
                            require_active=False,
                        )
                        local_store.adopt_command_bound_checkpoint(
                            payload=prior_checkpoint_payload,
                            validator=lambda candidate: (
                                LocalAssetsPublisher._verify_checkpoint(
                                    candidate, prior_command
                                )
                            ),
                        )
                    restored_prior = LocalAssetsPublisher._verify_checkpoint(
                        read_checkpoint(
                            self.projects_root, command["project_id"], "assets"
                        ),
                        prior_command,
                    )
                    if canonical_json_bytes(restored_prior) != canonical_json_bytes(
                        prior_checkpoint_document
                    ):
                        raise ValueError("local prior checkpoint differs from authority")
                    self._assert_claim_current(
                        store=gcs_store,
                        publication_state=publication_state,
                        publication_generation=state_generation,
                        fence=publication_fence,
                        fence_generation=fence_generation,
                        require_active=False,
                    )
                    write_checkpoint(
                        self.projects_root,
                        command["project_id"],
                        "assets",
                        command["transition"]["target_status"],
                        {"asset_manifest": deepcopy(command["asset_manifest"])},
                        pipeline_type=command["pipeline_type"],
                        checkpoint_policy="guided",
                        human_approval_required=True,
                        human_approved=command["transition"]["human_approved"],
                        review={
                            "batch_v2_agent_review": deepcopy(
                                command["review_evidence"]
                            )
                        },
                        cost_snapshot=_checkpoint_cost(command["cost_snapshot"]),
                        metadata={
                            "batch_v2_publication": _publication_metadata(command)
                        },
                    )
                self._assert_claim_current(
                    store=gcs_store,
                    publication_state=publication_state,
                    publication_generation=state_generation,
                    fence=publication_fence,
                    fence_generation=fence_generation,
                    require_active=False,
                )
                local_store.adopt_command_bound_checkpoint(
                    payload=checkpoint_payload,
                    validator=lambda candidate: (
                        LocalAssetsPublisher._verify_checkpoint(candidate, command)
                    ),
                )
            checkpoint = LocalAssetsPublisher._verify_checkpoint(
                read_checkpoint(self.projects_root, command["project_id"], "assets"),
                command,
            )
            if canonical_json_bytes(checkpoint) != canonical_json_bytes(
                checkpoint_document
            ):
                raise ValueError("official checkpoint reader differs from snapshot")
            gcs_store.verify_workspace_checkpoint(
                facts=completion["checkpoint"],
                payload=checkpoint_payload,
                checkpoint=checkpoint,
                command=command,
            )
            self._crash(
                "cloud_publication_recovery_checkpoint_restored",
                command_id=command["command_id"],
                publication_state_generation=state_generation,
            )
        except Exception as exc:
            if isinstance(exc, M2PublicationError):
                raise
            raise M2PublicationError(
                "PUBLICATION_COMPLETION_INVALID",
                "Completed canonical/GCS publication failed exact re-verification",
            ) from exc
        if publication_state["owner"]["owner_status"] == "repairing":
            repaired_state = deepcopy(publication_state)
            repaired_state["revision"] += 1
            repaired_state["owner"]["owner_status"] = "completed"
            repaired_state["owner"]["completed_at"] = self._now()
            validate_publication_state(repaired_state)
            try:
                repaired_generation = gcs_store.save_publication_state(
                    repaired_state, expected_generation=state_generation
                )
            except Exception as exc:
                if getattr(exc, "code", None) == "GCS_PRECONDITION_CONFLICT":
                    raise M2PublicationError(
                        "PUBLICATION_COMPLETION_CONFLICT",
                        "Publication repair lost its completion CAS",
                    ) from exc
                raise
            reread = gcs_store.load_publication_state()
            if (
                reread is None
                or reread[1] != repaired_generation
                or canonical_json_bytes(reread[0])
                != canonical_json_bytes(repaired_state)
            ):
                raise M2PublicationError(
                    "PUBLICATION_COMPLETION_REREAD_FAILED",
                    "Repaired publication owner did not close durably",
                )
            publication_state = repaired_state
            state_generation = repaired_generation
            self._crash(
                "cloud_publication_repair_completed",
                command_id=command["command_id"],
                publication_state_generation=state_generation,
            )
        self._assert_claim_current(
            store=gcs_store,
            publication_state=publication_state,
            publication_generation=state_generation,
            fence=publication_fence,
            fence_generation=fence_generation,
            require_active=False,
        )
        return {
            "version": "1.0",
            "command_id": command["command_id"],
            "command_digest": command["command_digest"],
            "command_logical_path": (
                f".batch-v2/runs/{command['batch_id']}/publication/commands/"
                f"{command['command_id']}.json"
            ),
            "command_generation": command_generation,
            "checkpoint_logical_path": "checkpoint_assets.json",
            "checkpoint_sha256": canonical_sha256(checkpoint),
            "checkpoint_generation": completion["checkpoint"]["generation"],
            "publication_state_generation": state_generation,
            "status": checkpoint["status"],
            "human_approved": checkpoint["human_approved"],
            "asset_manifest_sha256": command["asset_manifest_sha256"],
            "idempotent": idempotent,
        }

    def publish(
        self,
        command: Mapping[str, Any],
        *,
        trusted_invocation: CloudInvocationIdentity,
        publication_authorization: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Publish or repair one exact Cloud assets transition offline/injected."""

        assert_publication_invocation_allowed()
        self._assert_invocation(trusted_invocation)
        try:
            frozen = deepcopy(dict(command))
            validate_publication_command(frozen)
            project_dir = resolve_project_dir(self.projects_root, frozen["project_id"])
        except (M0ContractError, InvalidProjectIdError) as exc:
            if isinstance(exc, M0ContractError):
                raise
            raise M2PublicationError(
                "PUBLICATION_PROJECT_IDENTITY_INVALID", str(exc)
            ) from exc

        gcs_store = GCSStore(
            project_dir,
            frozen["batch_id"],
            bucket=self.bucket,
            transport=self.transport,
        )
        local_store = LocalStore(
            project_dir,
            frozen["batch_id"],
            immutable_publish_hook=self.immutable_publish_hook,
        )
        with (
            local_store.acquire_publication_lock(),
            local_store.acquire_run_lock(),
            publication_execution_scope(),
        ):
            request, request_generation = gcs_store.load_request()
            validate_frozen_request_authority(request, projects_root=self.projects_root)
            state, state_generation = gcs_store.load_batch_state()
            loaded_result = gcs_store.load_result()
            if loaded_result is None:
                raise M2PublicationError(
                    "PUBLICATION_RESULT_MISSING", "Durable GCS BatchResult is missing"
                )
            result, result_generation = loaded_result
            self._assert_cloud_execution_binding(
                frozen,
                request,
                request_generation,
                state,
                state_generation,
                result,
                result_generation,
                gcs_store,
            )
            asset_plan = LocalAssetsPublisher._asset_plan(
                frozen,
                request,
                state,
                result,
                required_store_type="gcs",
            )
            prior_state_loaded = gcs_store.load_publication_state()
            prior_state = (
                prior_state_loaded[0] if prior_state_loaded is not None else None
            )
            prior_command = None
            prior_command_generation = None
            prior_checkpoint_payload = None
            prior_checkpoint_document = None
            if frozen["transition"]["kind"] == "human_approval_to_completed":
                prior_id = frozen["transition"]["prior_publication_command_ref"][
                    "command_id"
                ]
                prior_command, prior_command_generation = (
                    gcs_store.load_publication_command(prior_id)
                )
                if prior_state is None or not prior_state["completed_commands"]:
                    raise M2PublicationError(
                        "HUMAN_APPROVAL_BINDING_INVALID",
                        "Human completion requires a durable prior publication completion",
                    )
                prior_completion = prior_state["completed_commands"][0]
                _, prior_checkpoint_payload, prior_checkpoint_document = (
                    gcs_store.read_publication_checkpoint_snapshot(
                        command=prior_command,
                        expected_facts=prior_completion["checkpoint_snapshot"],
                        expected_document_sha256=prior_completion[
                            "checkpoint_document_sha256"
                        ],
                        validator=lambda candidate: (
                            LocalAssetsPublisher._verify_checkpoint(
                                candidate, prior_command
                            )
                        ),
                    )
                )
                if (
                    prior_state["owner"]["owner_status"] == "completed"
                    and prior_state["owner"]["command_digest"]
                    == prior_command["command_digest"]
                ):
                    gcs_store.verify_workspace_checkpoint(
                        facts=prior_completion["checkpoint"],
                        payload=prior_checkpoint_payload,
                        checkpoint=prior_checkpoint_document,
                        command=prior_command,
                    )
            current_checkpoint = read_checkpoint(
                self.projects_root, frozen["project_id"], "assets"
            )
            exact_checkpoint = LocalAssetsPublisher._is_exact_checkpoint(
                current_checkpoint, frozen
            )
            state_matches_current = (
                prior_state is not None
                and prior_state["owner"]["command_id"] == frozen["command_id"]
                and prior_state["owner"]["command_digest"] == frozen["command_digest"]
            )
            already_journaled = (
                prior_state is not None
                and bool(prior_state["completed_commands"])
                and prior_state["completed_commands"][-1]["command_digest"]
                == frozen["command_digest"]
            )
            if exact_checkpoint and not state_matches_current:
                code = (
                    "HUMAN_APPROVAL_BINDING_INVALID"
                    if frozen["transition"]["kind"] == "human_approval_to_completed"
                    else "CHECKPOINT_PUBLICATION_CONFLICT"
                )
                raise M2PublicationError(
                    code,
                    "An unjournaled target checkpoint cannot establish publication authority",
                )
            if frozen["transition"]["kind"] == "human_approval_to_completed":
                self._assert_publication_lifecycle(
                    frozen,
                    prior_checkpoint_document,
                    prior_state,
                    prior_command,
                    prior_command_generation,
                )
            elif not exact_checkpoint and not already_journaled:
                self._assert_publication_lifecycle(
                    frozen,
                    current_checkpoint,
                    prior_state,
                    prior_command,
                    prior_command_generation,
                )

            completed_rehydrate = False
            completed_command_generation = None
            if (
                prior_state is not None
                and prior_state["owner"]["owner_status"] == "completed"
                and prior_state["completed_commands"]
            ):
                completion = prior_state["completed_commands"][-1]
                same_command_id = (
                    completion["command_id"] == frozen["command_id"]
                    or prior_state["owner"]["command_id"] == frozen["command_id"]
                )
                if same_command_id and (
                    completion["command_id"] != frozen["command_id"]
                    or completion["command_digest"] != frozen["command_digest"]
                    or prior_state["owner"]["command_id"] != frozen["command_id"]
                    or prior_state["owner"]["command_digest"]
                    != frozen["command_digest"]
                ):
                    raise M2PublicationError(
                        "PUBLICATION_COMPLETION_INVALID",
                        "Completed publication authority names changed command bytes",
                    )
                completed_rehydrate = (
                    completion["command_id"] == frozen["command_id"]
                    and completion["command_digest"] == frozen["command_digest"]
                    and prior_state["owner"]["command_id"] == frozen["command_id"]
                    and prior_state["owner"]["command_digest"]
                    == frozen["command_digest"]
                )
                if completed_rehydrate:
                    durable_command, completed_command_generation = (
                        gcs_store.load_publication_command(frozen["command_id"])
                    )
                    if (
                        canonical_json_bytes(durable_command)
                        != canonical_json_bytes(frozen)
                        or completed_command_generation
                        != completion["command_generation"]
                    ):
                        raise M2PublicationError(
                            "PUBLICATION_COMPLETION_INVALID",
                            "Completed publication does not bind the exact durable command",
                        )
                    publication_fence, fence_generation = (
                        gcs_store.load_publication_fence(frozen)
                    )
                    assert prior_state_loaded is not None
                    return self._completed_receipt(
                        command=frozen,
                        project_dir=project_dir,
                        publication_state=prior_state,
                        state_generation=prior_state_loaded[1],
                        command_generation=completed_command_generation,
                        idempotent=True,
                        local_store=local_store,
                        gcs_store=gcs_store,
                        asset_plan=asset_plan,
                        publication_fence=publication_fence,
                        fence_generation=fence_generation,
                    )
            if prior_state is None:
                gcs_store.preflight_workspace_checkpoint_generation(
                    expected_generation=0
                )
            elif prior_state["owner"]["owner_status"] == "completed":
                gcs_store.preflight_workspace_checkpoint_generation(
                    expected_generation=prior_state["completed_commands"][-1][
                        "checkpoint"
                    ]["generation"]
                )

            # Remote source/target verification is read-only. The only local
            # pre-claim write is rebuildable hidden project staging so media
            # and canonical destinations can be fully preflighted. No durable
            # command/claim or canonical file/checkpoint exists if it fails.
            staged_plan = []
            for receipt, output_spec, canonical_path in asset_plan:
                try:
                    staging = (
                        local_store.run_dir
                        / "publication"
                        / "staging"
                        / frozen["command_id"]
                        / receipt["item_id"]
                        / "source.mp4"
                    )
                    gcs_store.get_verified_blob(receipt, staging)
                    payload = staging.read_bytes()
                    local_store.preflight_materialized_canonical_asset(
                        source=staging,
                        receipt=receipt,
                        canonical_path=canonical_path,
                        validator=self.media_validator,
                        output_spec=output_spec,
                    )
                    gcs_store.preflight_workspace_asset(
                        payload=payload,
                        canonical_path=canonical_path,
                        receipt=receipt,
                    )
                except Exception as exc:
                    if isinstance(exc, (M2PublicationError, StorageConflict)):
                        raise
                    raise M2PublicationError(
                        "GCS_RECEIPT_INVALID",
                        "A publication source receipt/staging failed exact verification",
                    ) from exc
                staged_plan.append((staging, receipt, output_spec, canonical_path))

            proof_kind, proof_scope, proof_digest, proof_document = (
                self._validate_stop_proof(
                    command=frozen,
                    state=state,
                    identity=trusted_invocation,
                    publication_state=prior_state,
                    publication_authorization=publication_authorization,
                )
            )
            if proof_kind == "trusted_execution_status":
                gcs_store.write_ownership_record_if_absent(
                    kind="execution_status",
                    document=proof_document,
                    digest=proof_digest,
                )
            else:
                gcs_store.write_publication_authorization_if_absent(proof_document)
            command_generation, command_digest = (
                gcs_store.write_publication_command_if_absent(frozen)
            )
            if command_digest != frozen["command_digest"]:
                raise M2PublicationError(
                    "PUBLICATION_COMMAND_DIGEST_MISMATCH",
                    "Durable GCS PublicationCommand digest changed",
                )
            try:
                publication_fence, fence_generation = gcs_store.claim_publication_fence(
                    frozen
                )
            except StorageConflict as exc:
                if exc.code == "PROJECT_STAGE_PUBLICATION_CONFLICT":
                    raise M2PublicationError(
                        "PROJECT_STAGE_PUBLICATION_CONFLICT",
                        "Another batch already owns this project/assets canonical authority",
                    ) from exc
                raise
            publication_state, publication_generation, already_completed = (
                self._acquire_claim(
                    store=gcs_store,
                    command=frozen,
                    identity=trusted_invocation,
                    proof_kind=proof_kind,
                    proof_scope=proof_scope,
                    proof_digest=proof_digest,
                    proof_document=proof_document,
                )
            )
            if already_completed:
                return self._completed_receipt(
                    command=frozen,
                    project_dir=project_dir,
                    publication_state=publication_state,
                    state_generation=publication_generation,
                    command_generation=command_generation,
                    idempotent=True,
                    local_store=local_store,
                    gcs_store=gcs_store,
                    asset_plan=asset_plan,
                    publication_fence=publication_fence,
                    fence_generation=fence_generation,
                )
            self._crash(
                "cloud_publication_claim_acquired",
                command_id=frozen["command_id"],
                publication_state_generation=publication_generation,
            )

            # Keep the project-scoped immutable mirror because the existing
            # Backlot V2 authority reader intentionally resolves this exact
            # command path. GCS remains the durable Cloud command authority.
            command_path, local_command_digest = (
                local_store.write_publication_command_if_absent(frozen)
            )
            if local_command_digest != command_digest:
                raise M2PublicationError(
                    "PUBLICATION_COMMAND_DIGEST_MISMATCH",
                    "Local command mirror differs from durable GCS authority",
                )
            if prior_command is not None:
                local_store.write_publication_command_if_absent(prior_command)
            self._crash(
                "cloud_publication_command_mirrored",
                command_id=frozen["command_id"],
            )

            for _staging, receipt, _output_spec, _canonical_path in staged_plan:
                self._crash(
                    "cloud_publication_blob_staged",
                    command_id=frozen["command_id"],
                    item_id=receipt["item_id"],
                )

            for staging, receipt, output_spec, canonical_path in staged_plan:
                self._assert_claim_current(
                    store=gcs_store,
                    publication_state=publication_state,
                    publication_generation=publication_generation,
                    fence=publication_fence,
                    fence_generation=fence_generation,
                )
                destination, created = local_store.materialize_from_publication_staging(
                    source=staging,
                    receipt=receipt,
                    canonical_path=canonical_path,
                    validator=self.media_validator,
                    output_spec=output_spec,
                    publish_hook=self.asset_publish_hook,
                )
                self._crash(
                    "cloud_publication_asset_materialized",
                    command_id=frozen["command_id"],
                    canonical_path=destination.relative_to(project_dir).as_posix(),
                    created=created,
                )

            asset_objects = []
            for staging, receipt, output_spec, canonical_path in staged_plan:
                destination = local_store.verify_materialized_canonical_asset(
                    source=staging,
                    receipt=receipt,
                    canonical_path=canonical_path,
                    validator=self.media_validator,
                    output_spec=output_spec,
                )
                self._assert_claim_current(
                    store=gcs_store,
                    publication_state=publication_state,
                    publication_generation=publication_generation,
                    fence=publication_fence,
                    fence_generation=fence_generation,
                )
                asset_objects.append(
                    gcs_store.publish_workspace_asset(
                        source=destination,
                        canonical_path=canonical_path,
                        receipt=receipt,
                    )
                )
            self._crash(
                "cloud_publication_assets_gcs_verified",
                command_id=frozen["command_id"],
            )

            if prior_command is not None:
                assert prior_checkpoint_payload is not None
                assert prior_checkpoint_document is not None
                checkpoint_before_target = read_checkpoint(
                    self.projects_root, frozen["project_id"], "assets"
                )
                if not LocalAssetsPublisher._is_exact_checkpoint(
                    checkpoint_before_target, frozen
                ):
                    self._assert_claim_current(
                        store=gcs_store,
                        publication_state=publication_state,
                        publication_generation=publication_generation,
                        fence=publication_fence,
                        fence_generation=fence_generation,
                    )
                    local_store.adopt_command_bound_checkpoint(
                        payload=prior_checkpoint_payload,
                        validator=lambda candidate: (
                            LocalAssetsPublisher._verify_checkpoint(
                                candidate, prior_command
                            )
                        ),
                    )
                    restored_prior = LocalAssetsPublisher._verify_checkpoint(
                        read_checkpoint(
                            self.projects_root, frozen["project_id"], "assets"
                        ),
                        prior_command,
                    )
                    if canonical_json_bytes(restored_prior) != canonical_json_bytes(
                        prior_checkpoint_document
                    ):
                        raise M2PublicationError(
                            "CHECKPOINT_RECOVERY_INVALID",
                            "Restored prior Human Gate checkpoint differs from GCS authority",
                        )
                    self._crash(
                        "cloud_publication_prior_checkpoint_restored",
                        command_id=frozen["command_id"],
                    )

            if not exact_checkpoint:
                self._assert_claim_current(
                    store=gcs_store,
                    publication_state=publication_state,
                    publication_generation=publication_generation,
                    fence=publication_fence,
                    fence_generation=fence_generation,
                )
                try:
                    write_checkpoint(
                        self.projects_root,
                        frozen["project_id"],
                        "assets",
                        frozen["transition"]["target_status"],
                        {"asset_manifest": deepcopy(frozen["asset_manifest"])},
                        pipeline_type=frozen["pipeline_type"],
                        checkpoint_policy="guided",
                        human_approval_required=True,
                        human_approved=frozen["transition"]["human_approved"],
                        review={
                            "batch_v2_agent_review": deepcopy(frozen["review_evidence"])
                        },
                        cost_snapshot=_checkpoint_cost(frozen["cost_snapshot"]),
                        metadata={
                            "batch_v2_publication": _publication_metadata(frozen)
                        },
                    )
                except CheckpointValidationError as exc:
                    raise M2PublicationError(
                        "CHECKPOINT_PUBLICATION_FAILED", str(exc)
                    ) from exc
                self._crash(
                    "cloud_publication_checkpoint_written",
                    command_id=frozen["command_id"],
                )

            checkpoint = LocalAssetsPublisher._verify_checkpoint(
                read_checkpoint(self.projects_root, frozen["project_id"], "assets"),
                frozen,
            )
            checkpoint_path = project_dir / "checkpoint_assets.json"
            prior_checkpoint_generation = (
                publication_state["completed_commands"][-1]["checkpoint"]["generation"]
                if publication_state["completed_commands"]
                else 0
            )
            self._assert_claim_current(
                store=gcs_store,
                publication_state=publication_state,
                publication_generation=publication_generation,
                fence=publication_fence,
                fence_generation=fence_generation,
            )
            checkpoint_object, authoritative_payload, authoritative_checkpoint = (
                gcs_store.publish_workspace_checkpoint(
                    source=checkpoint_path,
                    checkpoint=checkpoint,
                    command=frozen,
                    expected_generation=prior_checkpoint_generation,
                    validator=lambda candidate: LocalAssetsPublisher._verify_checkpoint(
                        candidate, frozen
                    ),
                )
            )
            self._assert_claim_current(
                store=gcs_store,
                publication_state=publication_state,
                publication_generation=publication_generation,
                fence=publication_fence,
                fence_generation=fence_generation,
            )
            local_store.adopt_command_bound_checkpoint(
                payload=authoritative_payload,
                validator=lambda candidate: LocalAssetsPublisher._verify_checkpoint(
                    candidate, frozen
                ),
            )
            checkpoint = LocalAssetsPublisher._verify_checkpoint(
                read_checkpoint(self.projects_root, frozen["project_id"], "assets"),
                frozen,
            )
            if canonical_json_bytes(checkpoint) != canonical_json_bytes(
                authoritative_checkpoint
            ):
                raise M2PublicationError(
                    "CHECKPOINT_ROUNDTRIP_INVALID",
                    "Local checkpoint did not converge on GCS command authority",
                )
            checkpoint_snapshot, _, _ = (
                gcs_store.publish_publication_checkpoint_snapshot(
                    source=checkpoint_path,
                    checkpoint=checkpoint,
                    command=frozen,
                    validator=lambda candidate: (
                        LocalAssetsPublisher._verify_checkpoint(candidate, frozen)
                    ),
                )
            )
            self._crash(
                "cloud_publication_checkpoint_gcs_verified",
                command_id=frozen["command_id"],
                generation=checkpoint_object["generation"],
            )

            completed_state = deepcopy(publication_state)
            completed_state["revision"] += 1
            completed_at = self._now()
            completed_state["owner"]["owner_status"] = "completed"
            completed_state["owner"]["completed_at"] = completed_at
            completion = {
                "command_id": frozen["command_id"],
                "command_digest": frozen["command_digest"],
                "command_generation": command_generation,
                "transition": frozen["transition"]["kind"],
                "checkpoint": checkpoint_object,
                "checkpoint_snapshot": checkpoint_snapshot,
                "checkpoint_document_sha256": canonical_sha256(checkpoint),
                "asset_objects": asset_objects,
                "completed_at": completed_at,
            }
            human = frozen["transition"].get("human_approval_evidence")
            if human is not None:
                completion["human_approval_id"] = human["approval_id"]
                completion["human_approval_digest"] = canonical_sha256(human)
            completed_state["completed_commands"].append(completion)
            validate_publication_state(completed_state)
            try:
                completed_generation = gcs_store.save_publication_state(
                    completed_state, expected_generation=publication_generation
                )
            except Exception as exc:
                if getattr(exc, "code", None) == "GCS_PRECONDITION_CONFLICT":
                    raise M2PublicationError(
                        "PUBLICATION_COMPLETION_CONFLICT",
                        "Cloud publication completion lost its generation CAS",
                    ) from exc
                raise
            reread = gcs_store.load_publication_state()
            if (
                reread is None
                or reread[1] != completed_generation
                or canonical_json_bytes(reread[0])
                != canonical_json_bytes(completed_state)
            ):
                raise M2PublicationError(
                    "PUBLICATION_COMPLETION_REREAD_FAILED",
                    "Completed Cloud publication state could not be re-read exactly",
                )
            self._crash(
                "cloud_publication_state_completed",
                command_id=frozen["command_id"],
                publication_state_generation=completed_generation,
            )
            return self._completed_receipt(
                command=frozen,
                project_dir=project_dir,
                publication_state=completed_state,
                state_generation=completed_generation,
                command_generation=command_generation,
                idempotent=exact_checkpoint,
                local_store=local_store,
                gcs_store=gcs_store,
                asset_plan=asset_plan,
                publication_fence=publication_fence,
                fence_generation=fence_generation,
            )


__all__ = [
    "CloudAssetsPublisher",
    "LocalAssetsPublisher",
    "inspect_v2_asset_manifest_claim",
    "is_exact_v2_publication_checkpoint",
    "validated_v2_asset_manifest_from_checkpoint",
]
