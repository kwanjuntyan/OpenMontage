"""Exact Vertex Interactions adapter for the one M3 production identity.

Configuration, credentials, and transport are separate inputs.  ADC can
authenticate a call but can never choose the project, location, route, model,
operation, or fallback.
"""

from __future__ import annotations

import base64
import math
import os
import re
import threading
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Mapping, Protocol
from urllib.parse import urlparse

from .contracts import (
    M0ContractError,
    canonical_sha256,
    exact_identity,
    validate_exact_identity,
)
from .errors import M1ExecutionError
from .identity import ADCContext, CLOUD_PLATFORM_SCOPE, CredentialResolver
from .tool_adapter import ProviderCall, ProviderFacts, validate_provider_facts


_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_SAFE_OPERATION_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,255}$")
_VERTEX_PROJECT = re.compile(r"^[a-z][a-z0-9-]{4,62}[a-z0-9]$")
_CONFIG_FIELDS = {
    "version",
    "config_digest",
    "request_digest",
    "batch_id",
    "project_id",
    "identity",
    "vertex_project",
    "vertex_location",
}


@dataclass(frozen=True)
class VertexInteractionResponse:
    """Normalized facts observed by an injected Vertex transport."""

    disposition: Literal["succeeded", "remote_pending", "rejected"]
    observed_identity: Mapping[str, str]
    output_bytes: bytes | None = None
    provider_operation_id: str | None = None
    known_actual_usd: float = 0.0
    potentially_charged_usd: float = 0.0
    error_class: str | None = None
    sanitized_message: str | None = None
    retry_after_seconds: float = 0.0


class VertexTransportError(RuntimeError):
    """Transport failure with explicit provider-acceptance knowledge."""

    def __init__(
        self,
        message: str,
        *,
        acceptance: Literal["not_accepted", "accepted", "unknown"],
        error_class: str | None = None,
        provider_operation_id: str | None = None,
        retry_after_seconds: float = 0.0,
        potentially_charged_usd: float = 0.0,
    ):
        self.acceptance = acceptance
        self.error_class = error_class
        self.provider_operation_id = provider_operation_id
        self.retry_after_seconds = retry_after_seconds
        self.potentially_charged_usd = potentially_charged_usd
        super().__init__(message)


class VertexInteractionsTransport(Protocol):
    def submit(self, **kwargs: Any) -> VertexInteractionResponse: ...

    def poll(self, **kwargs: Any) -> VertexInteractionResponse: ...


def _config_digest(document: Mapping[str, Any]) -> str:
    candidate = deepcopy(dict(document))
    candidate.pop("config_digest", None)
    return canonical_sha256(candidate)


def validate_vertex_adapter_config(document: Mapping[str, Any]) -> None:
    if set(document) != _CONFIG_FIELDS:
        raise M0ContractError(
            "ADAPTER_CONFIG_INVALID",
            f"Exact adapter config fields required; got {sorted(document)}",
        )
    if document.get("version") != "1.0":
        raise M0ContractError("ADAPTER_CONFIG_INVALID", "Unsupported adapter config version")
    for field in ("batch_id", "project_id"):
        value = document.get(field)
        if not isinstance(value, str) or not _SAFE_ID.fullmatch(value):
            raise M0ContractError("ADAPTER_CONFIG_INVALID", f"Unsafe {field}")
    digest = document.get("request_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise M0ContractError("ADAPTER_CONFIG_INVALID", "Invalid request digest")
    identity = document.get("identity")
    if not isinstance(identity, Mapping):
        raise M0ContractError("ADAPTER_CONFIG_INVALID", "Exact identity is required")
    validate_exact_identity(identity, field="Vertex adapter configuration")
    vertex_project = document.get("vertex_project")
    if not isinstance(vertex_project, str) or not _VERTEX_PROJECT.fullmatch(vertex_project):
        raise M0ContractError(
            "ADAPTER_CONFIG_INVALID", "Explicit valid Vertex project is required"
        )
    if document.get("vertex_location") != "global":
        raise M0ContractError(
            "ADAPTER_CONFIG_INVALID",
            "The frozen vertex_interactions MVP route requires explicit location=global",
        )
    config_digest = document.get("config_digest")
    if config_digest != _config_digest(document):
        raise M0ContractError("ADAPTER_CONFIG_DIGEST_MISMATCH", "Adapter config changed")


def freeze_vertex_adapter_config(document: Mapping[str, Any]) -> dict[str, Any]:
    frozen = deepcopy(dict(document))
    frozen["config_digest"] = _config_digest(frozen)
    validate_vertex_adapter_config(frozen)
    return frozen


def _finite_non_negative(value: float, field: str) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise M1ExecutionError(
            "INVALID_PROVIDER_FACTS", f"Vertex {field} must be numeric"
        ) from exc
    if not math.isfinite(numeric) or numeric < 0:
        raise M1ExecutionError(
            "INVALID_PROVIDER_FACTS", f"Vertex {field} must be finite and non-negative"
        )
    return numeric


class GeminiOmniVertexAdapter:
    """Mechanical adapter for only INITIAL_ADAPTER_IDENTITY."""

    def __init__(
        self,
        *,
        config: Mapping[str, Any],
        project_dir: str | Path,
        credential_resolver: CredentialResolver,
        transport: VertexInteractionsTransport,
    ):
        validate_vertex_adapter_config(config)
        self.config = deepcopy(dict(config))
        self.project_dir = Path(project_dir).resolve(strict=True)
        if self.project_dir.name != self.config["project_id"]:
            raise M0ContractError(
                "PROJECT_IDENTITY_INVALID",
                "Materialized project root does not match adapter configuration",
            )
        self._transport = transport
        self._credential_resolver = credential_resolver
        self._adc: ADCContext | None = None
        self.observation = {
            "identity": exact_identity(),
            "route_binding": "explicit_request",
            "credential_mode": "adc",
            "hidden_writers": "disabled",
            "available": True,
        }

    def _ensure_adc(self) -> ADCContext:
        if self._adc is None:
            # This is the only credential boundary.  The detected ADC project
            # is intentionally ignored for all routing decisions.
            try:
                adc = self._credential_resolver.resolve(
                    scopes=(CLOUD_PLATFORM_SCOPE,)
                )
            except M1ExecutionError:
                raise
            except Exception as exc:
                raise M1ExecutionError(
                    "AUTH_CONFIGURATION", "ADC resolution failed"
                ) from exc
            if adc.source != "adc" or adc.credentials is None:
                raise M1ExecutionError(
                    "AUTH_CONFIGURATION",
                    "Vertex adapter requires an injected ADC identity",
                )
            self._adc = adc
        return self._adc

    def qualify_request(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        """Bind config to one frozen request and resolve ADC after that check."""

        if (
            request.get("request_digest") != self.config["request_digest"]
            or request.get("batch_id") != self.config["batch_id"]
            or request.get("project_id") != self.config["project_id"]
            or request.get("stage") != "assets"
        ):
            raise M0ContractError(
                "ADAPTER_CONFIG_DIGEST_MISMATCH",
                "Adapter config does not bind the exact frozen assets request",
            )
        work_items = request.get("work_items")
        if not isinstance(work_items, list) or not work_items:
            raise M0ContractError("ADAPTER_CONFIG_INVALID", "Request has no work items")
        for item in work_items:
            identity = item.get("identity") if isinstance(item, Mapping) else None
            if not isinstance(identity, Mapping):
                raise M0ContractError("EXACT_IDENTITY_MISMATCH", "Work item identity missing")
            validate_exact_identity(identity, field="work item identity")
            if dict(identity) != dict(self.config["identity"]):
                raise M0ContractError(
                    "EXACT_IDENTITY_MISMATCH",
                    "Work item identity differs from adapter configuration",
                )
            if item.get("inputs", {}).get("store") is not True:
                raise M0ContractError(
                    "ADAPTER_CONFIG_INVALID",
                    "The Vertex Interactions MVP route requires store=true for durable reconciliation",
                )
        self._ensure_adc()
        return deepcopy(self.observation)

    def _validate_call(self, call: ProviderCall) -> None:
        validate_exact_identity(call.identity, field="provider call identity")
        if dict(call.identity) != dict(self.config["identity"]):
            raise M0ContractError(
                "EXACT_IDENTITY_MISMATCH", "Call differs from frozen adapter identity"
            )
        if call.inputs.get("operation") != "text_to_video":
            raise M0ContractError(
                "EXACT_IDENTITY_MISMATCH", "M3 adapter supports only text_to_video"
            )
        expected_parent = (
            self.project_dir
            / ".batch-v2"
            / "runs"
            / self.config["batch_id"]
            / "attempts"
            / call.item_id
            / call.attempt_id
        )
        lexical = Path(os.path.abspath(call.output_path))
        resolved = call.output_path.resolve(strict=False)
        if (
            not call.output_path.is_absolute()
            or resolved.parent != expected_parent
            or os.path.normcase(str(resolved)) != os.path.normcase(str(lexical))
            or call.output_path.suffix.lower() != ".mp4"
        ):
            raise M0ContractError(
                "INVALID_OUTPUT_PATH",
                "Vertex worker output must be the exact materialized attempt staging path",
            )
        if call.kind == "poll" and (
            not isinstance(call.provider_operation_id, str)
            or not _SAFE_OPERATION_ID.fullmatch(call.provider_operation_id)
        ):
            raise M0ContractError(
                "PROVIDER_OPERATION_ID_REQUIRED",
                "Poll requires a safe exact single-segment operation ID",
            )
        if call.kind == "submit" and call.provider_operation_id is not None:
            raise M0ContractError(
                "INVALID_RETRY_ACTION", "Submit cannot reuse a remote operation ID"
            )

    def _transport_kwargs(self, call: ProviderCall) -> dict[str, Any]:
        adc = self._ensure_adc()
        return {
            "credentials": adc.credentials,
            "project": self.config["vertex_project"],
            "location": self.config["vertex_location"],
            "route": self.config["identity"]["route"],
            "model": self.config["identity"]["model"],
            "operation": self.config["identity"]["operation"],
            "inputs": deepcopy(dict(call.inputs)),
            "idempotency_digest": call.idempotency_digest,
            "provider_operation_id": call.provider_operation_id,
        }

    @staticmethod
    def _transport_failure(
        call: ProviderCall, exc: VertexTransportError
    ) -> ProviderFacts:
        retry_after = _finite_non_negative(
            exc.retry_after_seconds, "retry_after_seconds"
        )
        potential = _finite_non_negative(
            exc.potentially_charged_usd, "potentially_charged_usd"
        )
        message = str(exc)[:4096] or "Vertex transport failed"
        if exc.acceptance == "unknown":
            return ProviderFacts(
                success=False,
                acceptance="unknown",
                potentially_charged_usd=potential,
                provider_operation_id=exc.provider_operation_id,
                error_class="TIMEOUT_OR_NETWORK_UNKNOWN",
                retry_action="mark_indeterminate",
                sanitized_message=message,
                retry_after_seconds=retry_after,
            )
        if exc.acceptance == "accepted":
            if not exc.provider_operation_id:
                return ProviderFacts(
                    success=False,
                    acceptance="unknown",
                    potentially_charged_usd=potential,
                    error_class="TIMEOUT_OR_NETWORK_UNKNOWN",
                    retry_action="mark_indeterminate",
                    sanitized_message=message,
                    retry_after_seconds=retry_after,
                )
            return ProviderFacts(
                success=False,
                acceptance="accepted",
                potentially_charged_usd=potential,
                provider_operation_id=exc.provider_operation_id,
                error_class=(
                    exc.error_class
                    if exc.error_class
                    in {"RATE_LIMITED_REMOTE_POLL", "REMOTE_JOB_RECOVERABLE"}
                    else "REMOTE_JOB_RECOVERABLE"
                ),
                retry_action="poll_remote_operation",
                sanitized_message=message,
                retry_after_seconds=retry_after,
            )
        error_class = exc.error_class or "PROVIDER_TRANSIENT_PRE_ACCEPT"
        action = (
            "resubmit_generation"
            if error_class
            in {"RATE_LIMITED_SUBMIT_REJECTED", "PROVIDER_TRANSIENT_PRE_ACCEPT"}
            else "do_not_retry"
        )
        return ProviderFacts(
            success=False,
            acceptance="not_accepted",
            error_class=error_class,
            retry_action=action,
            sanitized_message=message,
            retry_after_seconds=retry_after,
        )

    def _normalize_response(
        self, call: ProviderCall, response: VertexInteractionResponse
    ) -> ProviderFacts:
        validate_exact_identity(
            response.observed_identity, field="observed Vertex response identity"
        )
        if dict(response.observed_identity) != dict(self.config["identity"]):
            raise M0ContractError(
                "EXACT_IDENTITY_MISMATCH", "Vertex response identity drifted"
            )
        known = _finite_non_negative(response.known_actual_usd, "known_actual_usd")
        potential = _finite_non_negative(
            response.potentially_charged_usd, "potentially_charged_usd"
        )
        retry_after = _finite_non_negative(
            response.retry_after_seconds, "retry_after_seconds"
        )
        if response.provider_operation_id is not None and (
            not isinstance(response.provider_operation_id, str)
            or not _SAFE_OPERATION_ID.fullmatch(response.provider_operation_id)
        ):
            raise M1ExecutionError(
                "INVALID_PROVIDER_FACTS",
                "Vertex returned an unsafe or ambiguous remote-operation ID",
            )
        if response.disposition == "succeeded":
            if not response.output_bytes or not response.provider_operation_id:
                raise M1ExecutionError(
                    "INVALID_PROVIDER_FACTS",
                    "Successful Vertex interaction requires bytes and durable interaction ID",
                )
            try:
                with call.output_path.open("xb") as output:
                    output.write(response.output_bytes)
                    output.flush()
                    os.fsync(output.fileno())
            except FileExistsError as exc:
                raise M1ExecutionError(
                    "OUTPUT_PATH_CONFLICT", "Provider output path already exists"
                ) from exc
            return ProviderFacts(
                success=True,
                acceptance="accepted",
                known_actual_usd=known,
                potentially_charged_usd=potential,
                provider_operation_id=response.provider_operation_id,
            )
        if response.disposition == "remote_pending":
            if not response.provider_operation_id:
                raise M1ExecutionError(
                    "INVALID_PROVIDER_FACTS",
                    "Remote continuation requires a durable interaction ID",
                )
            error_class = response.error_class or "REMOTE_JOB_RECOVERABLE"
            if error_class not in {"RATE_LIMITED_REMOTE_POLL", "REMOTE_JOB_RECOVERABLE"}:
                raise M1ExecutionError(
                    "INVALID_PROVIDER_FACTS", "Remote continuation has an unsafe error class"
                )
            return ProviderFacts(
                success=False,
                acceptance="accepted",
                known_actual_usd=known,
                potentially_charged_usd=potential,
                provider_operation_id=response.provider_operation_id,
                error_class=error_class,
                retry_action="poll_remote_operation",
                sanitized_message=(
                    response.sanitized_message or "Vertex interaction remains active"
                )[:4096],
                retry_after_seconds=retry_after,
            )
        error_class = response.error_class or "PROVIDER_PERMANENT_REJECT"
        action = (
            "resubmit_generation"
            if error_class
            in {"RATE_LIMITED_SUBMIT_REJECTED", "PROVIDER_TRANSIENT_PRE_ACCEPT"}
            else "do_not_retry"
        )
        return ProviderFacts(
            success=False,
            acceptance="not_accepted",
            error_class=error_class,
            retry_action=action,
            sanitized_message=(
                response.sanitized_message or "Vertex interaction was rejected"
            )[:4096],
            retry_after_seconds=retry_after,
        )

    def invoke(
        self, call: ProviderCall, cancellation: threading.Event
    ) -> ProviderFacts:
        self._validate_call(call)
        if cancellation.is_set():
            return ProviderFacts(
                success=False,
                acceptance="not_accepted",
                error_class="CANCELLED",
                retry_action="do_not_retry",
                sanitized_message="Cancelled before Vertex dispatch.",
            )
        try:
            if call.kind == "submit":
                response = self._transport.submit(**self._transport_kwargs(call))
            else:
                response = self._transport.poll(**self._transport_kwargs(call))
        except VertexTransportError as exc:
            facts = self._transport_failure(call, exc)
        except BaseException as exc:
            facts = ProviderFacts(
                success=False,
                acceptance="unknown" if call.kind == "submit" else "accepted",
                provider_operation_id=call.provider_operation_id,
                error_class=(
                    "TIMEOUT_OR_NETWORK_UNKNOWN"
                    if call.kind == "submit"
                    else "REMOTE_JOB_RECOVERABLE"
                ),
                retry_action=(
                    "mark_indeterminate"
                    if call.kind == "submit"
                    else "poll_remote_operation"
                ),
                sanitized_message=f"Vertex transport failed: {type(exc).__name__}"[:4096],
            )
        else:
            facts = self._normalize_response(call, response)
        validate_provider_facts(
            facts,
            billing_mode="paid",
            call_kind=call.kind,
        )
        return facts


class RequestsVertexInteractionsTransport:
    """Synchronous production HTTP transport; no route or model selection."""

    @staticmethod
    def _session() -> Any:
        import requests

        return requests

    @staticmethod
    def _bearer(credentials: Any) -> str:
        try:
            if not getattr(credentials, "valid", False) or not getattr(
                credentials, "token", None
            ):
                from google.auth.transport.requests import Request

                credentials.refresh(Request())
        except Exception as exc:
            raise VertexTransportError(
                "ADC token refresh failed",
                acceptance="not_accepted",
                error_class="AUTH_CONFIGURATION",
            ) from exc
        token = getattr(credentials, "token", None)
        if not token:
            raise VertexTransportError(
                "ADC produced no access token",
                acceptance="not_accepted",
                error_class="AUTH_CONFIGURATION",
            )
        return str(token)

    @staticmethod
    def _endpoint(project: str, location: str) -> str:
        return (
            "https://aiplatform.googleapis.com/v1beta1/"
            f"projects/{project}/locations/{location}/interactions"
        )

    @staticmethod
    def _identity(model: str, route: str, operation: str) -> dict[str, str]:
        identity = exact_identity()
        identity.update({"model": model, "route": route, "operation": operation})
        return identity

    @staticmethod
    def _retry_after(response: Any) -> float:
        try:
            return max(0.0, float(response.headers.get("Retry-After", 0)))
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _output_video(document: Mapping[str, Any]) -> Mapping[str, Any] | None:
        for field in ("output_video", "outputVideo"):
            video = document.get(field)
            if isinstance(video, Mapping) and (video.get("data") or video.get("uri")):
                return video
        for step in document.get("steps", ()) or ():
            if not isinstance(step, Mapping):
                continue
            for content in step.get("content", ()) or ():
                if not isinstance(content, Mapping):
                    continue
                media_type = str(content.get("mime_type", "")).lower()
                kind = str(content.get("type", "")).lower()
                if ("video" in kind or media_type.startswith("video/")) and (
                    content.get("data") or content.get("uri")
                ):
                    return content
        outputs = document.get("outputs", ()) or ()
        for output in outputs:
            if not isinstance(output, Mapping):
                continue
            video = output.get("video")
            if isinstance(video, Mapping) and (video.get("data") or video.get("uri")):
                return video
        return None

    @staticmethod
    def _trusted_media_uri(uri: str) -> bool:
        parsed = urlparse(uri)
        hostname = (parsed.hostname or "").lower()
        return (
            parsed.scheme == "https"
            and not parsed.username
            and not parsed.password
            and bool(hostname)
            and (hostname == "googleapis.com" or hostname.endswith(".googleapis.com"))
        )

    def _request(self, *, method: str, **kwargs: Any) -> VertexInteractionResponse:
        credentials = kwargs["credentials"]
        project = kwargs["project"]
        location = kwargs["location"]
        route = kwargs["route"]
        model = kwargs["model"]
        operation = kwargs["operation"]
        inputs = kwargs["inputs"]
        operation_id = kwargs.get("provider_operation_id")
        endpoint = self._endpoint(project, location)
        url = endpoint if method == "POST" else f"{endpoint}/{operation_id}"
        headers = {
            "Authorization": f"Bearer {self._bearer(credentials)}",
            "X-Goog-User-Project": project,
            "Content-Type": "application/json",
        }
        payload = None
        if method == "POST":
            payload = {
                "model": model,
                "input": inputs["prompt"],
                "response_format": {
                    "type": "video",
                    "aspect_ratio": inputs["aspect_ratio"],
                },
                "store": bool(inputs["store"]),
            }
        try:
            response = self._session().request(
                method,
                url,
                headers=headers,
                json=payload,
                timeout=600,
                allow_redirects=False,
            )
        except BaseException as exc:
            raise VertexTransportError(
                f"Vertex request transport failed: {type(exc).__name__}",
                acceptance="unknown" if method == "POST" else "accepted",
                provider_operation_id=operation_id,
            ) from exc
        retry_after = self._retry_after(response)
        if response.status_code in {401, 403}:
            raise VertexTransportError(
                "Vertex ADC authorization failed",
                acceptance="not_accepted" if method == "POST" else "accepted",
                error_class=(
                    "AUTH_CONFIGURATION"
                    if method == "POST"
                    else "REMOTE_JOB_RECOVERABLE"
                ),
                provider_operation_id=operation_id,
            )
        if response.status_code == 429:
            raise VertexTransportError(
                "Vertex rate limit",
                acceptance="not_accepted" if method == "POST" else "accepted",
                error_class=(
                    "RATE_LIMITED_SUBMIT_REJECTED"
                    if method == "POST"
                    else "RATE_LIMITED_REMOTE_POLL"
                ),
                provider_operation_id=operation_id,
                retry_after_seconds=retry_after,
            )
        if response.status_code == 408:
            raise VertexTransportError(
                "Vertex request timeout left acceptance unresolved",
                acceptance="unknown" if method == "POST" else "accepted",
                error_class=(
                    "TIMEOUT_OR_NETWORK_UNKNOWN"
                    if method == "POST"
                    else "REMOTE_JOB_RECOVERABLE"
                ),
                provider_operation_id=operation_id,
            )
        if response.status_code >= 500:
            raise VertexTransportError(
                "Vertex service failed after request transmission",
                acceptance="unknown" if method == "POST" else "accepted",
                provider_operation_id=operation_id,
            )
        if response.status_code >= 400:
            raise VertexTransportError(
                "Vertex rejected the request or remote-operation lookup",
                acceptance="not_accepted" if method == "POST" else "accepted",
                error_class=(
                    "PROVIDER_PERMANENT_REJECT"
                    if method == "POST"
                    else "REMOTE_JOB_RECOVERABLE"
                ),
                provider_operation_id=operation_id,
            )
        try:
            data = response.json()
        except (TypeError, ValueError) as exc:
            raise VertexTransportError(
                "Vertex returned invalid JSON after accepting the request",
                acceptance="unknown" if method == "POST" else "accepted",
                provider_operation_id=operation_id,
            ) from exc
        if not isinstance(data, Mapping):
            raise VertexTransportError(
                "Vertex returned a non-object response",
                acceptance="unknown" if method == "POST" else "accepted",
                provider_operation_id=operation_id,
            )
        interaction_id = data.get("id") or operation_id
        observed = self._identity(
            str(data.get("model", model)),
            str(data.get("route", route)),
            str(data.get("operation", operation)),
        )
        if response.status_code == 202 or str(data.get("status", "")).upper() in {
            "PENDING",
            "RUNNING",
        }:
            return VertexInteractionResponse(
                disposition="remote_pending",
                observed_identity=observed,
                provider_operation_id=interaction_id,
                error_class="REMOTE_JOB_RECOVERABLE",
                retry_after_seconds=retry_after,
            )
        video = self._output_video(data)
        if not video:
            raise VertexTransportError(
                "Vertex response omitted video facts",
                acceptance="accepted",
                provider_operation_id=interaction_id,
            )
        if video.get("data"):
            try:
                output_bytes = base64.b64decode(video["data"], validate=True)
            except (TypeError, ValueError) as exc:
                raise VertexTransportError(
                    "Vertex returned invalid inline video bytes",
                    acceptance="accepted",
                    provider_operation_id=interaction_id,
                ) from exc
        elif video.get("uri"):
            uri = str(video["uri"])
            if not self._trusted_media_uri(uri):
                raise VertexTransportError(
                    "Vertex returned an untrusted media locator",
                    acceptance="accepted",
                    provider_operation_id=interaction_id,
                )
            try:
                download = self._session().get(
                    uri,
                    headers=headers,
                    timeout=300,
                    allow_redirects=False,
                )
                if download.status_code != 200:
                    raise OSError("media download did not return exact bytes")
                output_bytes = bytes(download.content)
            except BaseException as exc:
                raise VertexTransportError(
                    "Vertex media download requires same-operation reconciliation",
                    acceptance="accepted",
                    provider_operation_id=interaction_id,
                ) from exc
        else:
            raise VertexTransportError(
                "Vertex video locator was empty",
                acceptance="accepted",
                provider_operation_id=interaction_id,
            )
        return VertexInteractionResponse(
            disposition="succeeded",
            observed_identity=observed,
            output_bytes=output_bytes,
            provider_operation_id=interaction_id,
        )

    def submit(self, **kwargs: Any) -> VertexInteractionResponse:
        return self._request(method="POST", **kwargs)

    def poll(self, **kwargs: Any) -> VertexInteractionResponse:
        return self._request(method="GET", **kwargs)


__all__ = [
    "GeminiOmniVertexAdapter",
    "RequestsVertexInteractionsTransport",
    "VertexInteractionResponse",
    "VertexInteractionsTransport",
    "VertexTransportError",
    "freeze_vertex_adapter_config",
    "validate_vertex_adapter_config",
]
