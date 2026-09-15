"""Narrow mechanical adapter boundary consumed by the M1 executor."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from threading import Event
from typing import Any, Literal, Mapping, Protocol

from .errors import M1ExecutionError


@dataclass(frozen=True)
class ProviderCall:
    """One exact submit or same-operation poll instruction."""

    kind: Literal["submit", "poll"]
    item_id: str
    attempt_id: str
    identity: Mapping[str, str]
    inputs: Mapping[str, Any]
    output_path: Path
    idempotency_digest: str
    provider_operation_id: str | None = None


@dataclass(frozen=True)
class ProviderFacts:
    """Facts returned by a worker; never a request to mutate shared state."""

    success: bool
    acceptance: Literal["not_accepted", "accepted", "unknown"]
    known_actual_usd: float = 0.0
    potentially_charged_usd: float = 0.0
    provider_operation_id: str | None = None
    error_class: str | None = None
    retry_action: str = "none"
    sanitized_message: str | None = None
    retry_after_seconds: float = 0.0


class ProviderAdapter(Protocol):
    """No selector or fallback: one prequalified exact provider adapter."""

    def invoke(self, call: ProviderCall, cancellation: Event) -> ProviderFacts: ...


def validate_provider_facts(
    facts: ProviderFacts,
    *,
    billing_mode: Literal["paid", "no_cost"],
    call_kind: Literal["submit", "poll"],
) -> None:
    """Validate worker facts before they can change durable cost or retry state."""

    numeric_facts = {
        "known_actual_usd": facts.known_actual_usd,
        "potentially_charged_usd": facts.potentially_charged_usd,
        "retry_after_seconds": facts.retry_after_seconds,
    }
    for field, value in numeric_facts.items():
        try:
            numeric = float(value)
        except (TypeError, ValueError) as exc:
            raise M1ExecutionError(
                "INVALID_PROVIDER_FACTS", f"Provider {field} must be numeric"
            ) from exc
        if not math.isfinite(numeric) or numeric < 0:
            raise M1ExecutionError(
                "INVALID_PROVIDER_FACTS",
                f"Provider {field} must be finite and non-negative",
            )
    if billing_mode == "no_cost" and (
        float(facts.known_actual_usd) != 0
        or float(facts.potentially_charged_usd) != 0
    ):
        raise M1ExecutionError(
            "INVALID_PROVIDER_FACTS", "No-cost work cannot report monetary exposure"
        )
    if facts.success:
        if (
            facts.acceptance != "accepted"
            or facts.retry_action != "none"
            or facts.error_class is not None
        ):
            raise M1ExecutionError(
                "INVALID_PROVIDER_FACTS",
                "Provider success requires accepted/none with no error class",
            )
        return
    if facts.error_class is None or facts.retry_action == "none":
        raise M1ExecutionError(
            "INVALID_PROVIDER_FACTS",
            "Provider failure requires a stable error class and typed action",
        )
    if facts.acceptance == "not_accepted" and (
        float(facts.known_actual_usd) != 0
        or float(facts.potentially_charged_usd) != 0
    ):
        raise M1ExecutionError(
            "INVALID_PROVIDER_FACTS", "Known rejection cannot report charge exposure"
        )
    if facts.retry_action == "resubmit_generation" and (
        facts.acceptance != "not_accepted" or call_kind != "submit"
    ):
        raise M1ExecutionError(
            "INVALID_PROVIDER_FACTS",
            "Generation resubmission requires a known-not-accepted submit",
        )
    if facts.retry_action == "poll_remote_operation" and (
        facts.acceptance != "accepted" or not facts.provider_operation_id
    ):
        raise M1ExecutionError(
            "INVALID_PROVIDER_FACTS",
            "Remote polling requires accepted work and a durable operation ID",
        )
    if facts.retry_action == "mark_indeterminate" and not (
        facts.acceptance == "unknown"
        or (facts.acceptance == "accepted" and facts.provider_operation_id)
    ):
        raise M1ExecutionError(
            "INVALID_PROVIDER_FACTS",
            "Indeterminate facts require unknown acceptance or an accepted remote operation",
        )
    if facts.acceptance == "unknown" and facts.retry_action != "mark_indeterminate":
        raise M1ExecutionError(
            "INVALID_PROVIDER_FACTS",
            "Unknown acceptance can only become indeterminate",
        )
    if facts.retry_action in {
        "retry_storage_commit",
        "reconcile_storage_precondition",
        "await_charged_generation_authorization",
    }:
        raise M1ExecutionError(
            "INVALID_PROVIDER_FACTS",
            "Provider workers cannot authorize storage or charged-generation actions",
        )


__all__ = [
    "ProviderAdapter",
    "ProviderCall",
    "ProviderFacts",
    "validate_provider_facts",
]
