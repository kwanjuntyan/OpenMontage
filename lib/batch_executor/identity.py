"""Injectable ADC identity boundary for Batch Executor V2 M3."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, Sequence


CLOUD_PLATFORM_SCOPE = "https://www.googleapis.com/auth/cloud-platform"


@dataclass(frozen=True)
class ADCContext:
    """Opaque authentication material plus a non-authoritative project hint."""

    credentials: Any
    detected_project: str | None
    source: str = "adc"


class CredentialResolver(Protocol):
    def resolve(self, *, scopes: Sequence[str]) -> ADCContext: ...


class GoogleADCResolver:
    """Production resolver; imports and accesses ADC only when explicitly called."""

    def resolve(self, *, scopes: Sequence[str]) -> ADCContext:
        import google.auth

        credentials, detected_project = google.auth.default(scopes=list(scopes))
        return ADCContext(
            credentials=credentials,
            detected_project=detected_project,
            source="adc",
        )


__all__ = [
    "ADCContext",
    "CLOUD_PLATFORM_SCOPE",
    "CredentialResolver",
    "GoogleADCResolver",
]
