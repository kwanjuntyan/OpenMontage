"""Google tools use the configured service-account JSON, never API-key fallback."""

from __future__ import annotations

import os
from typing import Any

# Broad scope that covers Cloud Text-to-Speech and Vertex AI prediction.
CLOUD_PLATFORM_SCOPE = "https://www.googleapis.com/auth/cloud-platform"


def resolve_google_location(location: str | None = None) -> str:
    """Return a Vertex location, treating blank env values as unset."""

    return location or os.environ.get("GOOGLE_CLOUD_LOCATION") or "us-central1"

# Shared constants for long-running Google/Vertex AI generation calls (e.g. music, video)
GOOGLE_API_TIMEOUT_SECONDS = 600
GOOGLE_API_TIMEOUT_MS = GOOGLE_API_TIMEOUT_SECONDS * 1000


def service_account_configured() -> bool:
    """True when GOOGLE_APPLICATION_CREDENTIALS points to an existing file."""
    path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    return bool(path and os.path.exists(path))


def has_google_credentials() -> bool:
    """Report JSON configuration only; this does not verify model entitlement."""
    return service_account_configured()


def get_genai_client(
    http_options: Any | None = None,
    location: str | None = None,
) -> Any:
    """Create a Vertex client with explicit JSON credentials and optional region."""
    from google import genai
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"], scopes=[CLOUD_PLATFORM_SCOPE]
    )
    return genai.Client(
        enterprise=True,
        credentials=credentials,
        project=resolve_project_id(credentials.project_id),
        location=resolve_google_location(location),
        http_options=http_options,
    )


def resolve_project_id(creds_project_id: str | None = None) -> str | None:
    """Resolve the GCP project id from env vars, falling back to the key file's.

    Vertex AI needs an explicit project id; TTS does not. We prefer an explicit
    env override so users can target a project other than the key's own.
    """
    return (
        os.environ.get("GOOGLE_CLOUD_PROJECT")
        or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        or os.environ.get("GCLOUD_PROJECT")
        or creds_project_id
    )


def get_access_token(scopes: list[str] | None = None) -> tuple[str, str | None]:
    """Mint an OAuth access token from the service-account JSON.

    Returns ``(access_token, project_id)``. ``project_id`` is the one embedded
    in the key file (callers should still prefer :func:`resolve_project_id`).

    Raises:
        RuntimeError: if ``google-auth`` is missing or the credentials cannot
            be loaded/refreshed — with a message the agent can surface verbatim.
    """
    if scopes is None:
        scopes = [CLOUD_PLATFORM_SCOPE]

    try:
        from google.auth.transport.requests import Request
        from google.oauth2 import service_account
    except ImportError as exc:  # pragma: no cover - depends on optional dep
        raise RuntimeError(
            "Service-account auth requires the 'google-auth' package. "
            "Install it with: pip install google-auth"
        ) from exc

    path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not path or not os.path.exists(path):
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS is not set or points to a missing "
            "file; cannot use service-account authentication."
        )

    try:
        creds = service_account.Credentials.from_service_account_file(
            path, scopes=scopes
        )
        creds.refresh(Request())
    except Exception as exc:  # noqa: BLE001 - re-raised as actionable message
        raise RuntimeError(
            f"Failed to load/refresh service-account credentials from {path}: {exc}"
        ) from exc

    token = creds.token
    if not token or not isinstance(token, str):
        raise RuntimeError(
            "Service-account credentials did not yield a valid access token."
        )

    project_id = getattr(creds, "project_id", None)
    ret_project_id = str(project_id) if project_id is not None else None
    return token, ret_project_id
