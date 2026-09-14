"""M2 local assets publication after an execution has durably stopped.

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
from datetime import datetime
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
    M0ContractError,
    canonical_json_bytes,
    canonical_sha256,
    compute_idempotency_digest,
    validate_publication_command,
)
from .errors import M2PublicationError
from .media_validation import MediaValidator
from .preflight import validate_frozen_request_authority
from .side_effects import assert_publication_invocation_allowed, publication_execution_scope
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

    receipts = {
        receipt["receipt_id"]: receipt for receipt in state["storage_receipts"]
    }
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
        "ownership_proof_digests": deepcopy(
            state.get("ownership_proof_digests", [])
        ),
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
        metadata["prior_checkpoint_sha256"] = transition[
            "prior_checkpoint_ref"
        ]["sha256"]
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
            or re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", metadata["batch_id"]
            )
            is None
            or not isinstance(metadata.get("command_id"), str)
            or re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", metadata["command_id"]
            )
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
        if metadata.get("command_logical_path") != expected_path.relative_to(
            root
        ).as_posix():
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
                or manifest_asset["source_tool"]
                != work_item["identity"]["tool_name"]
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
                receipt["store_type"] != "local"
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
            or canonical_sha256((checkpoint.get("artifacts") or {}).get("asset_manifest"))
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
        approved_at = datetime.fromisoformat(human["approved_at"].replace("Z", "+00:00"))
        command_created_at = datetime.fromisoformat(
            command["created_at"].replace("Z", "+00:00")
        )
        if (
            prior_digest != prior_ref["sha256"]
            or store.publication_command_path(prior_ref["command_id"]).relative_to(
                store.project_dir
            ).as_posix()
            != prior_ref["logical_path"]
            or prior_command["transition"]["kind"]
            != "agent_review_to_awaiting_human"
            or prior_command["command_digest"] != prior_digest
            or any(
                canonical_json_bytes(prior_command[field])
                != canonical_json_bytes(command[field])
                for field in unchanged_fields
            )
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
            project_dir = resolve_project_dir(
                self.projects_root, frozen["project_id"]
            )
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
            validate_frozen_request_authority(
                request, projects_root=self.projects_root
            )
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
                            "batch_v2_agent_review": deepcopy(
                                frozen["review_evidence"]
                            )
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
                read_checkpoint(
                    self.projects_root, frozen["project_id"], "assets"
                ),
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
                "command_logical_path": command_path.relative_to(project_dir).as_posix(),
                "checkpoint_logical_path": "checkpoint_assets.json",
                "checkpoint_sha256": checkpoint_digest,
                "status": checkpoint["status"],
                "human_approved": checkpoint["human_approved"],
                "asset_manifest_sha256": frozen["asset_manifest_sha256"],
                "idempotent": exact_checkpoint,
            }


__all__ = [
    "LocalAssetsPublisher",
    "inspect_v2_asset_manifest_claim",
    "is_exact_v2_publication_checkpoint",
    "validated_v2_asset_manifest_from_checkpoint",
]
