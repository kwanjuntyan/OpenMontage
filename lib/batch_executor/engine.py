"""M1 Local-first, single-coordinator Batch Executor."""

from __future__ import annotations

import os
import random
import threading
import time
import uuid
from concurrent.futures import FIRST_COMPLETED, Future, wait
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Mapping

from .contracts import (
    canonical_json_bytes,
    compute_idempotency_digest,
    validate_attempt,
    validate_attempt_output_path,
)
from .errors import M1ExecutionError
from .media_validation import MediaValidator, OutputFacts
from .preflight import preflight_batch_request
from .retry import RandomSource, full_jitter_delay
from .scheduler import BoundedScheduler, Clock
from .side_effects import worker_execution_scope
from .storage import LocalStore
from .tool_adapter import ProviderAdapter, ProviderCall, ProviderFacts


TERMINAL_ITEM_STATES = {
    "committed",
    "failed_terminal",
    "blocked_by_dependency",
    "indeterminate",
    "cancelled",
}


def _money(value: float | int | str | Decimal) -> float:
    return float(Decimal(str(value)).quantize(Decimal("0.000001")))


def _money_sum(*values: float | int | str | Decimal) -> float:
    return _money(sum((Decimal(str(value)) for value in values), Decimal("0")))


class RealClock:
    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    def monotonic(self) -> float:
        return time.monotonic()

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


class LocalBatchExecutor:
    """Execute approved assets work items without owning pipeline decisions."""

    def __init__(
        self,
        *,
        projects_root: str | Path,
        provider: ProviderAdapter,
        media_validator: MediaValidator,
        clock: Clock | None = None,
        random_source: RandomSource | None = None,
        crash_hook: Callable[[str, Mapping[str, Any]], None] | None = None,
    ):
        self.projects_root = Path(projects_root)
        self.provider = provider
        self.media_validator = media_validator
        self.clock = clock or RealClock()
        self.random_source = random_source or random.Random()
        self.crash_hook = crash_hook
        self._store: LocalStore | None = None
        self._state: dict[str, Any] | None = None
        self._state_version: int | None = None
        self._request: dict[str, Any] | None = None
        self._work_items: dict[str, dict[str, Any]] = {}
        self._reused_item_ids: set[str] = set()
        self._rate_limit_wait_seconds = 0.0
        self._cancellation = threading.Event()

    def _now(self) -> str:
        now_method = getattr(self.clock, "now", None)
        value = now_method() if callable(now_method) else datetime.now(timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    def _elapsed_seconds(self) -> float:
        assert self._state is not None
        created = datetime.fromisoformat(self._state["created_at"].replace("Z", "+00:00"))
        now_method = getattr(self.clock, "now", None)
        now = now_method() if callable(now_method) else datetime.now(timezone.utc)
        return max(0.0, (now - created).total_seconds())

    def _retry_deadline(self, delay_seconds: float) -> str:
        now_method = getattr(self.clock, "now", None)
        now = now_method() if callable(now_method) else datetime.now(timezone.utc)
        return (now + timedelta(seconds=delay_seconds)).astimezone(timezone.utc).isoformat().replace(
            "+00:00", "Z"
        )

    def _wait_for_retry_deadline(self, record: Mapping[str, Any]) -> None:
        deadline = datetime.fromisoformat(
            str(record["next_eligible_at"]).replace("Z", "+00:00")
        )
        now_method = getattr(self.clock, "now", None)
        now = now_method() if callable(now_method) else datetime.now(timezone.utc)
        remaining = max(0.0, (deadline - now).total_seconds())
        if remaining and not self._cancellation.is_set():
            self.clock.sleep(remaining)

    def _crash(self, boundary: str, **facts: Any) -> None:
        if self.crash_hook is not None:
            self.crash_hook(boundary, facts)

    def _save_state(self) -> None:
        assert self._store is not None and self._state is not None
        expected = self._state_version
        next_revision = 0 if expected is None else expected + 1
        self._state["revision"] = next_revision
        self._state["updated_at"] = self._now()
        self._state["owner"]["state_revision"] = next_revision
        self._state_version = self._store.save_batch_state(
            self._state, expected_version=expected
        )

    def _initial_state(self, request: Mapping[str, Any], invocation_id: str) -> dict[str, Any]:
        created_at = self._now()
        identity = request["work_items"][0]["identity"]
        return {
            "version": "1.0",
            "batch_id": request["batch_id"],
            "request_digest": request["request_digest"],
            "revision": 0,
            "owner": {
                "version": "1.0",
                "batch_id": request["batch_id"],
                "request_digest": request["request_digest"],
                "invocation_id": invocation_id,
                "invocation_mode": "run",
                "profile": "local",
                "execution_id": f"pid-{os.getpid()}",
                "task_id": "main",
                "owner_status": "active",
                "acquired_at": created_at,
                "state_revision": 0,
                "base_state_generation": 0,
            },
            "ownership_proof_digests": [],
            "status": "ready",
            "items": [
                {"item_id": item["item_id"], "state": "pending", "attempt_count": 0}
                for item in request["work_items"]
            ],
            "attempts": [],
            "provider_policy": {
                "provider": identity["provider"],
                "route": identity["route"],
                "model": identity["model"],
                "concurrency_cap": request["execution_policy"][
                    "provider_concurrency_cap"
                ],
                "min_request_spacing_seconds": request["execution_policy"][
                    "min_request_spacing_seconds"
                ],
            },
            "cost": {
                "estimated_usd": _money_sum(
                    *(item["estimated_cost_usd"] for item in request["work_items"])
                ),
                "reserved_usd": 0.0,
                "known_actual_usd": 0.0,
                "indeterminate_exposure_usd": 0.0,
                "authorized_cap_usd": request["authorization"][
                    "max_authorized_spend_usd"
                ],
            },
            "reuse": {"verified_hits": 0, "misses": len(request["work_items"])},
            "created_at": created_at,
            "updated_at": created_at,
            "last_attempt_sequence": 0,
            "storage_receipts": [],
        }

    def _item_record(self, item_id: str) -> dict[str, Any]:
        assert self._state is not None
        return next(item for item in self._state["items"] if item["item_id"] == item_id)

    def _item_attempts(self, item_id: str) -> list[dict[str, Any]]:
        assert self._state is not None
        return sorted(
            [attempt for attempt in self._state["attempts"] if attempt["item_id"] == item_id],
            key=lambda attempt: attempt["dispatch_sequence"],
        )

    def _latest_attempt(self, item_id: str) -> dict[str, Any] | None:
        attempts = self._item_attempts(item_id)
        return attempts[-1] if attempts else None

    def _receipt(self, receipt_id: str) -> dict[str, Any]:
        assert self._state is not None
        return next(
            receipt
            for receipt in self._state["storage_receipts"]
            if receipt["receipt_id"] == receipt_id
        )

    def _output_spec(self, item: Mapping[str, Any]) -> dict[str, Any]:
        output_spec = dict(item["output_spec"])
        output_spec["duration"] = item["inputs"]["duration"]
        return output_spec

    def _verify_result_receipts(self, result: Mapping[str, Any]) -> None:
        assert self._store is not None and self._state is not None and self._request is not None
        for result_item in result["items"]:
            if result_item["state"] not in {"committed", "cache_hit"}:
                continue
            work_item = self._work_items[result_item["item_id"]]
            receipt = result_item["storage_receipt"]
            state_item = self._item_record(result_item["item_id"])
            latest = self._latest_attempt(result_item["item_id"])
            state_receipt = (
                self._receipt(state_item["storage_receipt_id"])
                if state_item.get("storage_receipt_id")
                else None
            )
            if (
                state_item["state"] != "committed"
                or latest is None
                or latest["phase"] != "durably_committed"
                or latest["work_item_digest"] != work_item["work_item_digest"]
                or latest["identity"] != work_item["identity"]
                or latest["idempotency_digest"]
                != compute_idempotency_digest(
                    self._request["request_digest"], work_item["work_item_digest"]
                )
                or receipt["batch_id"] != self._request["batch_id"]
                or state_receipt is None
                or canonical_json_bytes(receipt) != canonical_json_bytes(state_receipt)
            ):
                raise M1ExecutionError(
                    "REUSE_RECEIPT_INVALID",
                    "Committed reuse facts do not bind the exact request, item, attempt, and receipt",
                )
            self._store.verify_receipt(
                receipt,
                validator=self.media_validator,
                output_spec=self._output_spec(work_item),
            )

    def _take_local_ownership(self, invocation_id: str) -> None:
        assert self._state is not None and self._request is not None
        previous = self._state["owner"]
        acquired_at = self._now()
        self._state["owner"] = {
            "version": "1.0",
            "batch_id": self._request["batch_id"],
            "request_digest": self._request["request_digest"],
            "invocation_id": invocation_id,
            "invocation_mode": "resume",
            "profile": "local",
            "execution_id": f"pid-{os.getpid()}",
            "task_id": "main",
            "owner_status": "active",
            "acquired_at": acquired_at,
            "state_revision": self._state["revision"],
            "base_state_generation": self._state["revision"],
            "predecessor": {
                "invocation_id": previous["invocation_id"],
                "execution_id": previous["execution_id"],
            },
        }
        self._state.pop("result_ref", None)
        self._state.pop("outcome", None)
        self._state["status"] = "running"
        self._save_state()

    def _mark_indeterminate(self, attempt: dict[str, Any], message: str) -> None:
        assert self._state is not None
        reserved = float(attempt["cost"]["reserved_usd"])
        potential = max(
            float(attempt["cost"]["potentially_charged_usd"]),
            reserved,
            float(attempt["cost"]["estimated_usd"]),
        )
        self._state["cost"]["reserved_usd"] = _money_sum(
            self._state["cost"]["reserved_usd"], -reserved
        )
        self._state["cost"]["indeterminate_exposure_usd"] = _money_sum(
            self._state["cost"]["indeterminate_exposure_usd"], potential
        )
        attempt["phase"] = "indeterminate"
        attempt["acceptance_knowledge"] = "unknown"
        attempt["retry_action"] = "mark_indeterminate"
        attempt["cost"]["reserved_usd"] = 0.0
        attempt["cost"]["potentially_charged_usd"] = potential
        attempt["error"] = {
            "error_class": "TIMEOUT_OR_NETWORK_UNKNOWN",
            "sanitized_message": message,
        }
        record = self._item_record(attempt["item_id"])
        record.pop("next_eligible_at", None)
        record.update({"state": "indeterminate", "error_class": attempt["error"]["error_class"]})

    def _recover_state(self) -> None:
        assert self._state is not None and self._store is not None
        changed = False
        for item_id, work_item in self._work_items.items():
            record = self._item_record(item_id)
            latest = self._latest_attempt(item_id)
            if record["state"] == "committed":
                if (
                    latest is None
                    or latest["work_item_digest"] != work_item["work_item_digest"]
                    or latest["identity"] != work_item["identity"]
                    or latest["idempotency_digest"]
                    != compute_idempotency_digest(
                        self._request["request_digest"], work_item["work_item_digest"]
                    )
                ):
                    raise M1ExecutionError(
                        "REUSE_RECEIPT_INVALID",
                        "Committed attempt does not bind the exact frozen work item",
                    )
                receipt = self._receipt(record["storage_receipt_id"])
                self._store.verify_receipt(
                    receipt,
                    validator=self.media_validator,
                    output_spec=self._output_spec(work_item),
                )
                self._reused_item_ids.add(item_id)
                continue
            if record["state"] in TERMINAL_ITEM_STATES:
                continue
            if latest is None:
                record["state"] = "eligible"
                record.pop("next_eligible_at", None)
                changed = True
                continue
            phase = latest["phase"]
            latest.setdefault("operation_retry_count", 0)
            if phase == "prepared":
                record["state"] = "eligible"
                record.pop("next_eligible_at", None)
                changed = True
            elif phase == "dispatched":
                if latest["billing_mode"] == "paid":
                    self._mark_indeterminate(
                        latest,
                        "Prior local process stopped after dispatch; provider acceptance is unknown",
                    )
                else:
                    latest.update(
                        {
                            "phase": "failed",
                            "acceptance_knowledge": "not_accepted",
                            "retry_action": "resubmit_generation",
                            "error": {
                                "error_class": "PROVIDER_TRANSIENT_PRE_ACCEPT",
                                "sanitized_message": "No-cost dispatch interrupted before response",
                            },
                        }
                    )
                    record["state"] = "retry_wait"
                    record["next_eligible_at"] = self._now()
                changed = True
            elif phase in {"result_received", "bytes_staged", "technically_valid"}:
                output_path = self._store.attempt_output_path(
                    item_id, latest["attempt_id"], work_item["output_spec"]["output_name"]
                )
                if output_path.is_file():
                    record["state"] = "succeeded_staged"
                    record.pop("next_eligible_at", None)
                elif latest.get("provider_operation_id"):
                    latest.update(
                        {
                            "phase": "provider_accepted",
                            "retry_action": "poll_remote_operation",
                            "error": {
                                "error_class": "REMOTE_JOB_RECOVERABLE",
                                "sanitized_message": "Resume must reconcile the accepted operation",
                            },
                        }
                    )
                    record["state"] = "retry_wait"
                    record["next_eligible_at"] = self._now()
                else:
                    latest["acceptance_knowledge"] = "unknown"
                    self._mark_indeterminate(
                        latest, "Accepted output is missing and cannot be reconciled"
                    )
                changed = True
            elif phase == "provider_accepted":
                if latest.get("provider_operation_id"):
                    latest["retry_action"] = "poll_remote_operation"
                    latest["error"] = {
                        "error_class": "REMOTE_JOB_RECOVERABLE",
                        "sanitized_message": "Resume will poll the same accepted operation",
                    }
                    record["state"] = "retry_wait"
                    record["next_eligible_at"] = self._now()
                else:
                    latest["acceptance_knowledge"] = "unknown"
                    self._mark_indeterminate(
                        latest, "Accepted operation lacks a durable provider operation ID"
                    )
                changed = True
            elif latest["retry_action"] in {
                "resubmit_generation",
                "poll_remote_operation",
                "retry_storage_commit",
                "reconcile_storage_precondition",
                "await_charged_generation_authorization",
            }:
                record["state"] = "retry_wait"
                record.setdefault("next_eligible_at", self._now())
                changed = True
        verified_hits = len(self._reused_item_ids)
        if (
            self._state["reuse"]["verified_hits"] != verified_hits
            or self._state["reuse"]["misses"]
            != len(self._work_items) - verified_hits
        ):
            self._state["reuse"] = {
                "verified_hits": verified_hits,
                "misses": len(self._work_items) - verified_hits,
            }
            changed = True
        if changed:
            self._save_state()

    def _settle_cancellation(self) -> bool:
        """Stop new dispatch without hiding accepted or prior failure facts."""

        changed = False
        for item_id, item in self._work_items.items():
            record = self._item_record(item_id)
            if record["state"] == "succeeded_staged":
                latest = self._latest_attempt(item_id)
                self._commit_staged(item, latest)
                changed = True
                continue
            if record["state"] not in {"pending", "eligible", "retry_wait"}:
                continue
            latest = self._latest_attempt(item_id)
            if latest is None:
                record["state"] = "cancelled"
            elif latest["phase"] == "prepared":
                reserved = float(latest["cost"]["reserved_usd"])
                self._state["cost"]["reserved_usd"] = _money_sum(
                    self._state["cost"]["reserved_usd"], -reserved
                )
                latest.update(
                    {
                        "phase": "cancelled",
                        "acceptance_knowledge": "not_accepted",
                        "retry_action": "do_not_retry",
                        "error": {
                            "error_class": "CANCELLED",
                            "sanitized_message": "Cancelled before provider dispatch.",
                        },
                    }
                )
                latest["cost"].update(
                    {"reserved_usd": 0.0, "potentially_charged_usd": 0.0}
                )
                record["state"] = "cancelled"
            elif latest["retry_action"] == "poll_remote_operation":
                latest.update(
                    {"phase": "indeterminate", "retry_action": "mark_indeterminate"}
                )
                record.update(
                    {
                        "state": "indeterminate",
                        "error_class": latest["error"]["error_class"],
                    }
                )
            elif latest["retry_action"] in {
                "resubmit_generation",
                "await_charged_generation_authorization",
            }:
                latest["retry_action"] = "do_not_retry"
                record.update(
                    {
                        "state": "failed_terminal",
                        "error_class": latest["error"]["error_class"],
                    }
                )
            elif latest["retry_action"] in {
                "retry_storage_commit",
                "reconcile_storage_precondition",
            }:
                latest.update({"phase": "failed", "retry_action": "do_not_retry"})
                record.update(
                    {
                        "state": "failed_terminal",
                        "error_class": latest["error"]["error_class"],
                    }
                )
            else:
                raise M1ExecutionError(
                    "INVALID_CANCELLATION_STATE",
                    f"Cannot safely cancel {item_id} from {latest['phase']}/{latest['retry_action']}",
                )
            record.pop("next_eligible_at", None)
            changed = True
        return changed

    def _dependency_blocked_or_waiting(self, item: Mapping[str, Any]) -> str:
        dependencies = item["dependency_item_ids"]
        if not dependencies:
            return "ready"
        records = [self._item_record(dependency) for dependency in dependencies]
        failed = [record["item_id"] for record in records if record["state"] in TERMINAL_ITEM_STATES - {"committed"}]
        if failed:
            record = self._item_record(item["item_id"])
            record["state"] = "blocked_by_dependency"
            record["blocker"] = {
                "kind": "dependency_failure",
                "dependency_item_ids": failed,
                "reason": "One or more required work items did not commit.",
            }
            return "blocked"
        if any(record["state"] != "committed" for record in records):
            return "waiting"
        return "ready"

    def _can_start_attempt(self, item: Mapping[str, Any], *, charged_retry: bool) -> bool:
        assert self._state is not None and self._request is not None
        policy = self._request["execution_policy"]
        attempts = self._item_attempts(item["item_id"])
        if len(attempts) >= policy["max_attempts_per_item"]:
            return False
        if len(self._state["attempts"]) >= self._request["authorization"]["max_total_attempts"]:
            return False
        if self._elapsed_seconds() >= policy["max_elapsed_seconds"]:
            return False
        if charged_retry:
            charged_failures = sum(
                attempt.get("error", {}).get("error_class")
                == "OUTPUT_TECHNICALLY_INVALID"
                for attempt in attempts
            )
            if charged_failures > item["charged_retry_allowance"]:
                return False
        exposure = (
            float(self._state["cost"]["reserved_usd"])
            + float(self._state["cost"]["known_actual_usd"])
            + float(self._state["cost"]["indeterminate_exposure_usd"])
            + float(item["estimated_cost_usd"])
        )
        return exposure <= float(self._state["cost"]["authorized_cap_usd"]) + 1e-9

    def _fail_retry_candidate(self, record: dict[str, Any], latest: dict[str, Any] | None) -> None:
        record.pop("next_eligible_at", None)
        record["state"] = "failed_terminal"
        if latest is None:
            record["error_class"] = "BUDGET_EXCEEDED"
            return
        latest["retry_action"] = "do_not_retry"
        record["error_class"] = latest["error"]["error_class"]

    def _prepare_attempt(self, item: Mapping[str, Any]) -> dict[str, Any] | None:
        assert self._state is not None and self._request is not None
        record = self._item_record(item["item_id"])
        latest = self._latest_attempt(item["item_id"])
        charged_retry = bool(
            latest
            and latest.get("retry_action") == "await_charged_generation_authorization"
        )
        if not self._can_start_attempt(item, charged_retry=charged_retry):
            self._fail_retry_candidate(record, latest)
            self._save_state()
            return None
        sequence = self._state["last_attempt_sequence"] + 1
        attempt_id = f"attempt-{sequence:06d}"
        estimated = float(item["estimated_cost_usd"])
        attempt = {
            "version": "1.0",
            "batch_id": self._request["batch_id"],
            "request_digest": self._request["request_digest"],
            "item_id": item["item_id"],
            "attempt_id": attempt_id,
            "work_item_digest": item["work_item_digest"],
            "idempotency_digest": compute_idempotency_digest(
                self._request["request_digest"], item["work_item_digest"]
            ),
            "identity": dict(item["identity"]),
            "dispatch_sequence": sequence,
            "phase": "prepared",
            "timestamps": {"queued_at": self._now()},
            "acceptance_knowledge": "not_accepted",
            "billing_mode": "no_cost" if self._request["authorization"]["no_cost"] else "paid",
            "retry_action": "none",
            "operation_retry_count": 0,
            "cost": {
                "estimated_usd": estimated,
                "reserved_usd": estimated,
                "known_actual_usd": 0.0,
                "potentially_charged_usd": 0.0,
            },
        }
        validate_attempt(attempt)
        self._state["attempts"].append(attempt)
        self._state["last_attempt_sequence"] = sequence
        self._state["cost"]["reserved_usd"] = _money_sum(
            self._state["cost"]["reserved_usd"], estimated
        )
        record.update({"state": "running", "attempt_count": record["attempt_count"] + 1})
        record.pop("next_eligible_at", None)
        record.pop("error_class", None)
        self._save_state()
        self._crash("attempt_reserved", item_id=item["item_id"], attempt_id=attempt_id)
        return attempt

    def _dispatch_attempt(self, item: Mapping[str, Any], attempt: dict[str, Any]) -> ProviderCall:
        assert self._store is not None and self._request is not None
        output_path = self._store.attempt_output_path(
            item["item_id"], attempt["attempt_id"], item["output_spec"]["output_name"]
        )
        validate_attempt_output_path(
            output_path,
            projects_root=self.projects_root,
            project_id=self._request["project_id"],
            batch_id=self._request["batch_id"],
            item_id=item["item_id"],
            attempt_id=attempt["attempt_id"],
            output_name=item["output_spec"]["output_name"],
        )
        self._store.prepare_attempt_directory(output_path)
        attempt["phase"] = "dispatched"
        attempt["acceptance_knowledge"] = "unknown"
        attempt["timestamps"]["dispatched_at"] = self._now()
        attempt["cost"]["potentially_charged_usd"] = attempt["cost"]["estimated_usd"]
        self._save_state()
        self._crash("dispatch_recorded", item_id=item["item_id"], attempt_id=attempt["attempt_id"])
        return ProviderCall(
            kind="submit",
            item_id=item["item_id"],
            attempt_id=attempt["attempt_id"],
            identity=deepcopy(item["identity"]),
            inputs=deepcopy(item["inputs"]),
            output_path=output_path,
            idempotency_digest=attempt["idempotency_digest"],
        )

    def _poll_call(self, item: Mapping[str, Any], attempt: dict[str, Any]) -> ProviderCall:
        assert self._store is not None
        output_path = self._store.attempt_output_path(
            item["item_id"], attempt["attempt_id"], item["output_spec"]["output_name"]
        )
        self._store.prepare_attempt_directory(output_path)
        return ProviderCall(
            kind="poll",
            item_id=item["item_id"],
            attempt_id=attempt["attempt_id"],
            identity=deepcopy(item["identity"]),
            inputs=deepcopy(item["inputs"]),
            output_path=output_path,
            idempotency_digest=attempt["idempotency_digest"],
            provider_operation_id=attempt["provider_operation_id"],
        )

    def _worker(self, call: ProviderCall, cancellation: threading.Event) -> ProviderFacts:
        with worker_execution_scope(call.output_path.parent):
            return self.provider.invoke(call, cancellation)

    def _reconcile_cost(self, attempt: dict[str, Any], facts: ProviderFacts) -> None:
        assert self._state is not None
        prior_reserved = float(attempt["cost"]["reserved_usd"])
        prior_known = float(attempt["cost"]["known_actual_usd"])
        known = max(prior_known, float(facts.known_actual_usd))
        if facts.acceptance == "not_accepted" or (
            facts.acceptance == "accepted" and known > 0
        ):
            potential = 0.0
        else:
            potential = max(
                float(attempt["cost"]["potentially_charged_usd"]),
                float(facts.potentially_charged_usd),
            )
        self._state["cost"]["reserved_usd"] = _money_sum(
            self._state["cost"]["reserved_usd"], -prior_reserved
        )
        self._state["cost"]["known_actual_usd"] = _money_sum(
            self._state["cost"]["known_actual_usd"], known, -prior_known
        )
        attempt["cost"].update(
            {
                "reserved_usd": 0.0,
                "known_actual_usd": known,
                "potentially_charged_usd": potential,
            }
        )

    def _record_worker_failure(
        self, item: Mapping[str, Any], attempt: dict[str, Any], facts: ProviderFacts
    ) -> None:
        assert self._state is not None
        self._reconcile_cost(attempt, facts)
        record = self._item_record(item["item_id"])
        error_class = facts.error_class or "INTERNAL_BUG"
        message = facts.sanitized_message or "Provider adapter returned no error details"
        if facts.acceptance == "unknown" and attempt["billing_mode"] == "paid":
            potential = max(
                float(attempt["cost"]["potentially_charged_usd"]),
                float(attempt["cost"]["estimated_usd"]),
            )
            self._state["cost"]["indeterminate_exposure_usd"] = _money_sum(
                self._state["cost"]["indeterminate_exposure_usd"], potential
            )
            attempt.update(
                {
                    "phase": "indeterminate",
                    "acceptance_knowledge": "unknown",
                    "retry_action": "mark_indeterminate",
                    "error": {
                        "error_class": error_class
                        if error_class
                        in {"RATE_LIMITED_ACCEPTANCE_UNKNOWN", "TIMEOUT_OR_NETWORK_UNKNOWN", "INTERNAL_BUG", "CANCELLED"}
                        else "INTERNAL_BUG",
                        "sanitized_message": message,
                    },
                }
            )
            attempt["cost"]["potentially_charged_usd"] = potential
            record.update(
                {"state": "indeterminate", "error_class": attempt["error"]["error_class"]}
            )
            record.pop("next_eligible_at", None)
        else:
            attempt["acceptance_knowledge"] = facts.acceptance
            attempt["retry_action"] = facts.retry_action
            attempt["error"] = {
                "error_class": error_class,
                "sanitized_message": message,
            }
            if facts.retry_after_seconds:
                attempt["error"]["retry_after_seconds"] = facts.retry_after_seconds
            if facts.provider_operation_id:
                attempt["provider_operation_id"] = facts.provider_operation_id
            if facts.retry_action == "poll_remote_operation":
                attempt["phase"] = "provider_accepted"
                record["state"] = "retry_wait"
            elif facts.retry_action == "resubmit_generation":
                attempt["phase"] = "failed"
                record["state"] = "retry_wait"
            elif facts.retry_action == "do_not_retry":
                attempt["phase"] = "failed"
                record["state"] = "failed_terminal"
                record["error_class"] = error_class
                record.pop("next_eligible_at", None)
            elif facts.retry_action == "mark_indeterminate":
                attempt["phase"] = "indeterminate"
                record["state"] = "indeterminate"
                record["error_class"] = error_class
                record.pop("next_eligible_at", None)
            else:
                raise M1ExecutionError(
                    "INVALID_PROVIDER_FACTS",
                    f"Provider failure supplied unsafe action {facts.retry_action}",
                )
        if record["state"] == "retry_wait":
            if facts.retry_action == "poll_remote_operation":
                continuation_count = attempt.get("operation_retry_count", 0) + 1
                attempt["operation_retry_count"] = continuation_count
                if continuation_count >= 3:
                    attempt.update(
                        {"phase": "indeterminate", "retry_action": "mark_indeterminate"}
                    )
                    record.update(
                        {"state": "indeterminate", "error_class": error_class}
                    )
                    record.pop("next_eligible_at", None)
                    validate_attempt(attempt)
                    self._save_state()
                    return
            retry_index = max(0, record["attempt_count"] - 1)
            delay = full_jitter_delay(
                retry_index,
                base_seconds=1.0,
                cap_seconds=30.0,
                random_source=self.random_source,
                retry_after_seconds=facts.retry_after_seconds,
            )
            if self._elapsed_seconds() + delay >= self._request["execution_policy"]["max_elapsed_seconds"]:
                if facts.retry_action == "poll_remote_operation":
                    attempt.update(
                        {"phase": "indeterminate", "retry_action": "mark_indeterminate"}
                    )
                    record.update(
                        {"state": "indeterminate", "error_class": error_class}
                    )
                    record.pop("next_eligible_at", None)
                else:
                    self._fail_retry_candidate(record, attempt)
            else:
                record["next_eligible_at"] = self._retry_deadline(delay)
        validate_attempt(attempt)
        self._save_state()
        if record["state"] == "retry_wait":
            self._crash(
                "retry_wait_persisted",
                item_id=item["item_id"],
                attempt_id=attempt["attempt_id"],
            )
            self._wait_for_retry_deadline(record)

    def _record_provider_success(
        self, item: Mapping[str, Any], attempt: dict[str, Any], facts: ProviderFacts
    ) -> None:
        self._reconcile_cost(attempt, facts)
        attempt.update(
            {
                "phase": "result_received",
                "acceptance_knowledge": "accepted",
                "retry_action": "none",
            }
        )
        attempt.pop("error", None)
        if facts.provider_operation_id:
            attempt["provider_operation_id"] = facts.provider_operation_id
        attempt["timestamps"]["response_received_at"] = self._now()
        self._save_state()
        self._crash(
            "provider_result_recorded",
            item_id=item["item_id"],
            attempt_id=attempt["attempt_id"],
        )
        self._validate_and_commit(item, attempt)

    def _validate_and_commit(self, item: Mapping[str, Any], attempt: dict[str, Any]) -> None:
        assert self._store is not None and self._state is not None
        output_path = self._store.attempt_output_path(
            item["item_id"], attempt["attempt_id"], item["output_spec"]["output_name"]
        )
        try:
            facts = self.media_validator.validate(output_path, self._output_spec(item))
        except M1ExecutionError as exc:
            attempt.update(
                {
                    "phase": "failed",
                    "acceptance_knowledge": "accepted",
                    "retry_action": "await_charged_generation_authorization",
                    "error": {
                        "error_class": "OUTPUT_TECHNICALLY_INVALID",
                        "sanitized_message": str(exc)[:4096],
                    },
                }
            )
            attempt.pop("output", None)
            record = self._item_record(item["item_id"])
            if self._can_start_attempt(item, charged_retry=True):
                record["state"] = "retry_wait"
                record["next_eligible_at"] = self._now()
            else:
                attempt["retry_action"] = "do_not_retry"
                record.update(
                    {"state": "failed_terminal", "error_class": "OUTPUT_TECHNICALLY_INVALID"}
                )
                record.pop("next_eligible_at", None)
            validate_attempt(attempt)
            self._save_state()
            return
        attempt.update(
            {
                "phase": "technically_valid",
                "retry_action": "none",
                "output": {
                    "sha256": facts.sha256,
                    "size_bytes": facts.size_bytes,
                    "probe": dict(facts.probe),
                },
            }
        )
        attempt.pop("error", None)
        attempt["timestamps"]["bytes_verified_at"] = self._now()
        record = self._item_record(item["item_id"])
        record["state"] = "succeeded_staged"
        record.pop("next_eligible_at", None)
        self._save_state()
        self._crash("media_validated", item_id=item["item_id"], attempt_id=attempt["attempt_id"])
        self._commit_staged(item, attempt, facts)

    def _commit_staged(
        self,
        item: Mapping[str, Any],
        attempt: dict[str, Any],
        facts: OutputFacts | None = None,
    ) -> None:
        assert self._store is not None and self._state is not None
        output_path = self._store.attempt_output_path(
            item["item_id"], attempt["attempt_id"], item["output_spec"]["output_name"]
        )
        if facts is None:
            facts = self.media_validator.validate(output_path, self._output_spec(item))
            recorded = attempt.get("output")
            if recorded and (
                recorded["sha256"] != facts.sha256
                or recorded["size_bytes"] != facts.size_bytes
                or canonical_json_bytes(recorded["probe"])
                != canonical_json_bytes(facts.probe)
            ):
                raise M1ExecutionError(
                    "REUSE_RECEIPT_INVALID", "Staged bytes changed after validation"
                )
            attempt["output"] = {
                "sha256": facts.sha256,
                "size_bytes": facts.size_bytes,
                "probe": dict(facts.probe),
            }
        try:
            receipt = self._store.put_verified_blob(
                source=output_path,
                logical_path=output_path.relative_to(self._store.project_dir).as_posix(),
                batch_id=self._request["batch_id"],
                item_id=item["item_id"],
                attempt_id=attempt["attempt_id"],
                output=facts,
                created_at=self._now(),
            )
        except M1ExecutionError as exc:
            if exc.code != "LOCAL_STORAGE_TRANSIENT":
                raise
            continuation_count = attempt.get("operation_retry_count", 0) + 1
            attempt["operation_retry_count"] = continuation_count
            attempt.update(
                {
                    "phase": "technically_valid",
                    "retry_action": "retry_storage_commit",
                    "error": {
                        "error_class": "LOCAL_STORAGE_TRANSIENT",
                        "sanitized_message": str(exc)[:4096],
                    },
                }
            )
            record = self._item_record(item["item_id"])
            record["state"] = "retry_wait"
            if (
                continuation_count >= 3
                or self._elapsed_seconds()
                >= self._request["execution_policy"]["max_elapsed_seconds"]
            ):
                attempt.update({"phase": "failed", "retry_action": "do_not_retry"})
                record.update(
                    {"state": "failed_terminal", "error_class": "LOCAL_STORAGE_TRANSIENT"}
                )
                record.pop("next_eligible_at", None)
            else:
                delay = full_jitter_delay(
                    continuation_count - 1,
                    base_seconds=0.25,
                    cap_seconds=5.0,
                    random_source=self.random_source,
                )
                record["next_eligible_at"] = self._retry_deadline(delay)
            self._save_state()
            if record["state"] == "retry_wait":
                self._crash(
                    "retry_wait_persisted",
                    item_id=item["item_id"],
                    attempt_id=attempt["attempt_id"],
                )
                self._wait_for_retry_deadline(record)
            return
        self._crash("blob_committed", item_id=item["item_id"], attempt_id=attempt["attempt_id"])
        attempt["phase"] = "durably_committed"
        attempt["retry_action"] = "none"
        attempt.pop("error", None)
        attempt["output"]["storage_receipt_id"] = receipt["receipt_id"]
        attempt["timestamps"]["committed_at"] = self._now()
        if not any(
            existing["receipt_id"] == receipt["receipt_id"]
            for existing in self._state["storage_receipts"]
        ):
            self._state["storage_receipts"].append(receipt)
        record = self._item_record(item["item_id"])
        record.update(
            {
                "state": "committed",
                "storage_receipt_id": receipt["receipt_id"],
            }
        )
        record.pop("error_class", None)
        record.pop("next_eligible_at", None)
        self._save_state()
        self._crash("item_committed", item_id=item["item_id"], attempt_id=attempt["attempt_id"])

    def _handle_future(
        self,
        call: ProviderCall,
        attempt: dict[str, Any],
        future: Future[ProviderFacts],
    ) -> None:
        item = self._work_items[call.item_id]
        try:
            facts = future.result()
        except BaseException as exc:
            facts = ProviderFacts(
                success=False,
                acceptance="unknown",
                potentially_charged_usd=float(attempt["cost"]["estimated_usd"]),
                error_class="INTERNAL_BUG",
                retry_action="mark_indeterminate",
                sanitized_message=f"Worker failed after dispatch: {type(exc).__name__}",
            )
        if facts.success:
            if facts.acceptance != "accepted":
                raise M1ExecutionError(
                    "INVALID_PROVIDER_FACTS", "Successful provider result must be accepted"
                )
            self._record_provider_success(item, attempt, facts)
        else:
            self._record_worker_failure(item, attempt, facts)

    def _final_outcome(self) -> str:
        assert self._state is not None
        states = [item["state"] for item in self._state["items"]]
        if "indeterminate" in states:
            return "indeterminate"
        successful = sum(state == "committed" for state in states)
        if successful == len(states):
            return "all_succeeded"
        if states and all(state == "cancelled" for state in states):
            return "cancelled"
        if successful:
            return "partial_failure"
        return "failed"

    def _terminalize(self, invocation_id: str, cancellation: threading.Event) -> dict[str, Any]:
        assert self._state is not None and self._request is not None and self._store is not None
        self._state["status"] = "awaiting_agent_review"
        self._state["outcome"] = self._final_outcome()
        self._state["owner"]["owner_status"] = (
            "cancelled" if cancellation.is_set() else "terminal"
        )
        self._save_state()

        result_items = []
        for record in self._state["items"]:
            item_id = record["item_id"]
            state = "cache_hit" if item_id in self._reused_item_ids else record["state"]
            result_item: dict[str, Any] = {"item_id": item_id, "state": state}
            if state in {"committed", "cache_hit"}:
                result_item["storage_receipt"] = deepcopy(
                    self._receipt(record["storage_receipt_id"])
                )
            elif state == "blocked_by_dependency":
                result_item["blocker"] = deepcopy(record["blocker"])
            elif state in {"failed_terminal", "indeterminate"}:
                latest = self._latest_attempt(item_id)
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
        outcome = (
            "indeterminate"
            if counts["indeterminate"]
            else "all_succeeded"
            if counts["successful"] + counts["cache_hit"] == len(states)
            else "cancelled"
            if counts["cancelled"] == len(states)
            else "partial_failure"
            if counts["successful"] + counts["cache_hit"]
            else "failed"
        )
        attempted_items = {attempt["item_id"] for attempt in self._state["attempts"]}
        generation_retries = max(
            0, len(self._state["attempts"]) - len(attempted_items)
        )
        operation_retries = sum(
            attempt.get("operation_retry_count", 0)
            for attempt in self._state["attempts"]
        )
        result = {
            "version": "1.0",
            "batch_id": self._request["batch_id"],
            "request_digest": self._request["request_digest"],
            "source_bindings": [
                {"binding_id": binding["binding_id"], "sha256": binding["sha256"]}
                for binding in self._request["source_bindings"]
            ],
            "invocations": [
                {
                    "invocation_id": invocation_id,
                    "execution_id": self._state["owner"]["execution_id"],
                    "profile": "local",
                }
            ],
            "ownership_proof_digests": [],
            "status": "awaiting_agent_review",
            "outcome": outcome,
            "counts": counts,
            "items": result_items,
            "cost": deepcopy(self._state["cost"]),
            "statistics": {
                "attempts": len(self._state["attempts"]),
                "retries": generation_retries + operation_retries,
                "cache_hits": counts["cache_hit"],
                "rate_limit_wait_seconds": self._rate_limit_wait_seconds,
            },
            "agent_review_hints": [
                "Review mechanical outputs and receipts before M2 canonical publication."
            ],
            "created_at": self._now(),
        }
        digest = self._store.write_result_if_absent(result)
        self._crash("result_written", result_digest=digest)
        self._state["result_ref"] = {
            "logical_path": self._store.result_path.relative_to(
                self._store.project_dir
            ).as_posix(),
            "sha256": digest,
        }
        self._save_state()
        return result

    def _run_locked(
        self,
        invocation_id: str,
        cancellation: threading.Event,
    ) -> dict[str, Any]:
        assert self._store is not None and self._request is not None
        self._store.write_request_if_absent(self._request)
        self._crash("request_persisted", request_digest=self._request["request_digest"])
        durable_request, durable_digest = self._store.load_request()
        if durable_digest != self._request["request_digest"] or durable_request != self._request:
            raise M1ExecutionError(
                "REQUEST_CONFLICT", "Durable request differs from the preflight request"
            )

        if self._store.state_path.exists():
            self._state, self._state_version = self._store.load_batch_state()
            if self._state["request_digest"] != self._request["request_digest"]:
                raise M1ExecutionError(
                    "REQUEST_CONFLICT", "BatchState binds another request digest"
                )
            existing_result = self._store.load_result()
            if existing_result is not None:
                result, _ = existing_result
                if result["request_digest"] != self._request["request_digest"]:
                    raise M1ExecutionError(
                        "REQUEST_CONFLICT", "BatchResult binds another request digest"
                    )
                self._verify_result_receipts(result)
                return result
            self._take_local_ownership(invocation_id)
            self._recover_state()
        else:
            self._state = self._initial_state(self._request, invocation_id)
            self._state_version = None
            self._save_state()
            self._crash("state_initialized", invocation_id=invocation_id)

        policy = self._request["execution_policy"]
        provider = self._request["work_items"][0]["identity"]["provider"]
        with BoundedScheduler(
            max_workers=policy["global_worker_cap"],
            provider_caps={provider: policy["provider_concurrency_cap"]},
            provider_spacing_seconds={
                provider: policy["min_request_spacing_seconds"]
            },
            clock=self.clock,
        ) as scheduler:
            inflight: dict[Future[ProviderFacts], tuple[ProviderCall, dict[str, Any]]] = {}
            while True:
                state_changed = False
                if cancellation.is_set():
                    state_changed = self._settle_cancellation()
                    if state_changed:
                        self._save_state()

                capacity = policy["provider_concurrency_cap"] - len(inflight)
                if not cancellation.is_set() and capacity > 0:
                    for item_id, item in self._work_items.items():
                        if capacity <= 0:
                            break
                        record = self._item_record(item_id)
                        if record["state"] in TERMINAL_ITEM_STATES or record["state"] == "running":
                            continue
                        dependency = self._dependency_blocked_or_waiting(item)
                        if dependency == "blocked":
                            state_changed = True
                            continue
                        if dependency == "waiting":
                            continue
                        latest = self._latest_attempt(item_id)
                        if record["state"] == "retry_wait":
                            self._wait_for_retry_deadline(record)
                            if cancellation.is_set():
                                continue
                        if record["state"] == "succeeded_staged" or (
                            latest
                            and latest["retry_action"]
                            in {"retry_storage_commit", "reconcile_storage_precondition"}
                        ):
                            self._commit_staged(item, latest)
                            state_changed = True
                            continue
                        if latest and latest["retry_action"] == "poll_remote_operation":
                            call = self._poll_call(item, latest)
                            record["state"] = "running"
                            record.pop("next_eligible_at", None)
                            self._save_state()
                            future = scheduler.submit(
                                provider,
                                lambda call=call: self._worker(call, cancellation),
                            )
                            inflight[future] = (call, latest)
                            capacity -= 1
                            continue
                        if latest and latest["phase"] == "prepared":
                            attempt = latest
                        else:
                            attempt = self._prepare_attempt(item)
                        if attempt is None:
                            state_changed = True
                            continue
                        call = self._dispatch_attempt(item, attempt)
                        future = scheduler.submit(
                            provider,
                            lambda call=call: self._worker(call, cancellation),
                        )
                        inflight[future] = (call, attempt)
                        capacity -= 1

                if state_changed:
                    self._save_state()
                if inflight:
                    done, _ = wait(tuple(inflight), return_when=FIRST_COMPLETED)
                    for future in done:
                        call, attempt = inflight.pop(future)
                        self._handle_future(call, attempt, future)
                    continue
                if all(
                    record["state"] in TERMINAL_ITEM_STATES
                    for record in self._state["items"]
                ):
                    break
                # No in-flight or mechanically ready item means frozen dependencies
                # or limits left the state inconsistent. Fail closed without calls.
                unresolved = [
                    record
                    for record in self._state["items"]
                    if record["state"] not in TERMINAL_ITEM_STATES
                ]
                if unresolved:
                    for record in unresolved:
                        record.update(
                            {"state": "failed_terminal", "error_class": "INTERNAL_BUG"}
                        )
                    self._save_state()
                    break
            self._rate_limit_wait_seconds = scheduler.rate_limit_wait_seconds
        return self._terminalize(invocation_id, cancellation)

    def run(
        self,
        request: Mapping[str, Any],
        *,
        observed_source_revision: Mapping[str, Any],
        adapter_observation: Mapping[str, Any],
        invocation_id: str | None = None,
        cancellation: threading.Event | None = None,
    ) -> dict[str, Any]:
        """Preflight and execute one immutable local assets BatchRequest."""

        self._state = None
        self._state_version = None
        self._reused_item_ids = set()
        self._rate_limit_wait_seconds = 0.0
        frozen = deepcopy(dict(request))
        facts = preflight_batch_request(
            frozen,
            projects_root=self.projects_root,
            observed_source_revision=observed_source_revision,
            adapter_observation=adapter_observation,
        )
        if frozen["execution_policy"]["storage_profile"] != "local":
            raise M1ExecutionError(
                "INVALID_STORAGE_PROFILE", "M1 LocalBatchExecutor accepts only local profile"
            )
        if frozen["execution_policy"]["provider_concurrency_cap"] != 1:
            raise M1ExecutionError(
                "INVALID_PROVIDER_CAP", "Selected Gemini provider cap must remain one"
            )
        self._request = frozen
        self._work_items = {item["item_id"]: item for item in frozen["work_items"]}
        self._store = LocalStore(facts.project_dir, frozen["batch_id"])
        invocation = invocation_id or f"local-{uuid.uuid4().hex}"
        cancellation_event = cancellation or threading.Event()
        self._cancellation = cancellation_event
        with self._store.acquire_run_lock():
            return self._run_locked(invocation, cancellation_event)


__all__ = ["LocalBatchExecutor", "RealClock"]
