"""Narrow mechanical adapter boundary consumed by the M1 executor."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Event
from typing import Any, Literal, Mapping, Protocol


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


__all__ = ["ProviderAdapter", "ProviderCall", "ProviderFacts"]
