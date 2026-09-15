"""Cloud Run identity and trusted execution-status boundaries for M3."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Literal, Mapping, Protocol, Sequence

from .contracts import M0ContractError
from .identity import CLOUD_PLATFORM_SCOPE, CredentialResolver
from .ownership import freeze_execution_status_evidence


_SAFE_RESOURCE_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,127}$")
_SAFE_INVOCATION_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def _safe_resource_component(value: Any) -> bool:
    return isinstance(value, str) and bool(_SAFE_RESOURCE_COMPONENT.fullmatch(value))


@dataclass(frozen=True)
class CloudRunExecutionStatus:
    execution_resource: str
    terminal_state: Literal["terminal", "cancelled"] | None
    observed_at: str


@dataclass(frozen=True)
class CloudInvocationIdentity:
    invocation_id: str
    execution_resource: str
    task_id: str
    mode: Literal["run", "resume"]
    trust_source: Literal["cloud_run_launch_contract"] = "cloud_run_launch_contract"


class CloudRunEnvironmentIdentityResolver:
    """Validate the single-task Cloud Run launch contract from injected env."""

    def __init__(
        self,
        *,
        cloud_project: str,
        location: str,
        job_name: str,
        environment: Mapping[str, str],
    ):
        self._project = cloud_project
        self._location = location
        self._job = job_name
        self._environment = dict(environment)
        if not all(
            _safe_resource_component(value)
            for value in (cloud_project, location, job_name)
        ):
            raise M0ContractError(
                "AUTH_CONFIGURATION",
                "Explicit Cloud Run identity configuration is invalid",
            )

    def resolve(
        self, *, invocation_id: str, mode: Literal["run", "resume"]
    ) -> CloudInvocationIdentity:
        if not isinstance(invocation_id, str) or not _SAFE_INVOCATION_ID.fullmatch(
            invocation_id
        ):
            raise M0ContractError("AUTH_CONFIGURATION", "Unsafe invocation ID")
        environment = self._environment
        if (
            environment.get("CLOUD_RUN_JOB") != self._job
            or environment.get("CLOUD_RUN_TASK_INDEX") != "0"
            or environment.get("CLOUD_RUN_TASK_COUNT") != "1"
            or environment.get("CLOUD_RUN_TASK_ATTEMPT") != "0"
        ):
            raise M0ContractError(
                "AUTH_CONFIGURATION",
                "Cloud Run launch must be task-count=1, task index 0, and attempt 0",
            )
        execution_name = environment.get("CLOUD_RUN_EXECUTION", "")
        if not _safe_resource_component(execution_name):
            raise M0ContractError(
                "AUTH_CONFIGURATION",
                "Cloud Run execution identity is missing or unsafe",
            )
        resource = (
            f"projects/{self._project}/locations/{self._location}/jobs/{self._job}/"
            f"executions/{execution_name}"
        )
        return CloudInvocationIdentity(
            invocation_id=invocation_id,
            execution_resource=resource,
            task_id="0",
            mode=mode,
        )


class CloudRunStatusTransport(Protocol):
    def get_execution_status(
        self, *, credentials: Any, execution_resource: str
    ) -> CloudRunExecutionStatus: ...


class CloudRunADCExecutionStatusVerifier:
    """Prove the exact previous execution stopped through injected ADC transport."""

    verifier_id = "cloud_run_control_plane_adc"

    def __init__(
        self,
        *,
        cloud_project: str,
        location: str,
        job_name: str,
        additional_job_names: Sequence[str] = (),
        credential_resolver: CredentialResolver,
        transport: CloudRunStatusTransport,
    ):
        if not all(
            _safe_resource_component(value)
            for value in (cloud_project, location, job_name, *additional_job_names)
        ):
            raise M0ContractError(
                "AUTH_CONFIGURATION",
                "Explicit Cloud Run project/location/job are required",
            )
        self._execution_prefixes = tuple(
            f"projects/{cloud_project}/locations/{location}/jobs/{name}/executions/"
            for name in (job_name, *additional_job_names)
        )
        self._credential_resolver = credential_resolver
        self._transport = transport

    def verify_stopped(self, recorded_owner: Mapping[str, Any]) -> Mapping[str, Any]:
        execution_resource = recorded_owner.get("execution_id")
        execution_prefix = next(
            (
                prefix
                for prefix in self._execution_prefixes
                if isinstance(execution_resource, str)
                and execution_resource.startswith(prefix)
            ),
            "",
        )
        execution_name = (
            execution_resource[len(execution_prefix) :] if execution_prefix else ""
        )
        if (
            recorded_owner.get("profile") != "cloud_run"
            or not isinstance(execution_resource, str)
            or not execution_prefix
            or not _safe_resource_component(execution_name)
        ):
            raise M0ContractError(
                "TAKEOVER_PROOF_MISMATCH",
                "Recorded owner execution resource is outside the explicit Cloud Run job",
            )
        try:
            adc = self._credential_resolver.resolve(scopes=(CLOUD_PLATFORM_SCOPE,))
        except Exception as exc:
            raise M0ContractError(
                "AUTH_CONFIGURATION", "Cloud Run status ADC resolution failed"
            ) from exc
        if adc.source != "adc" or adc.credentials is None:
            raise M0ContractError(
                "AUTH_CONFIGURATION", "Cloud Run status verification requires ADC"
            )
        status = self._transport.get_execution_status(
            credentials=adc.credentials,
            execution_resource=execution_resource,
        )
        if (
            not isinstance(status, CloudRunExecutionStatus)
            or status.execution_resource != execution_resource
        ):
            raise M0ContractError(
                "TAKEOVER_PROOF_MISMATCH",
                "Control-plane response does not bind the recorded execution resource",
            )
        if status.terminal_state not in {"terminal", "cancelled"}:
            raise M0ContractError(
                "EXECUTION_STATUS_VERIFICATION_FAILED",
                "Recorded Cloud Run execution is not terminal or cancelled",
            )
        evidence_key = hashlib.sha256(
            (
                f"{recorded_owner['batch_id']}\0{execution_resource}\0"
                f"{status.observed_at}\0{status.terminal_state}"
            ).encode("utf-8")
        ).hexdigest()[:24]
        return freeze_execution_status_evidence(
            {
                "version": "1.0",
                "evidence_id": f"cloud-run-status-{evidence_key}",
                "batch_id": recorded_owner["batch_id"],
                "request_digest": recorded_owner["request_digest"],
                "prior_invocation_id": recorded_owner["invocation_id"],
                "prior_execution_id": execution_resource,
                "observed_status": status.terminal_state,
                "observed_at": status.observed_at,
                "verifier": self.verifier_id,
                "execution_resource": execution_resource,
            }
        )


def _rfc3339(value: Any) -> str:
    if hasattr(value, "ToDatetime"):
        value = value.ToDatetime()
    if not isinstance(value, datetime):
        raise M0ContractError(
            "EXECUTION_STATUS_VERIFICATION_FAILED",
            "Cloud Run completion time is not trustworthy",
        )
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class RequestsCloudRunStatusTransport:
    """Narrow Cloud Run v2 REST reader authenticated by injected ADC.

    Construction performs no credential or network access.  The transport does
    not list jobs or executions: it can only GET the exact resource already
    bound into the durable ExecutionOwner.
    """

    def __init__(
        self,
        *,
        session: Any | None = None,
        auth_request_factory: Callable[[], Any] | None = None,
        now: Callable[[], datetime] | None = None,
    ):
        self._injected_session = session
        self._auth_request_factory = auth_request_factory
        self._now = now or (lambda: datetime.now(timezone.utc))

    def _session(self) -> Any:
        if self._injected_session is not None:
            return self._injected_session
        import requests

        return requests

    def _auth_request(self) -> Any:
        if self._auth_request_factory is not None:
            return self._auth_request_factory()
        from google.auth.transport.requests import Request

        return Request()

    @staticmethod
    def _cancelled(document: Mapping[str, Any]) -> bool:
        for condition in document.get("conditions", ()) or ():
            if not isinstance(condition, Mapping):
                continue
            facts = " ".join(
                str(condition.get(field, ""))
                for field in ("type", "state", "reason", "message")
            ).upper()
            if "CANCEL" in facts:
                return True
        return False

    def get_execution_status(
        self, *, credentials: Any, execution_resource: str
    ) -> CloudRunExecutionStatus:
        if not re.fullmatch(
            r"projects/[A-Za-z0-9][A-Za-z0-9-]{0,127}/"
            r"locations/[A-Za-z0-9][A-Za-z0-9-]{0,127}/"
            r"jobs/[A-Za-z0-9][A-Za-z0-9-]{0,127}/"
            r"executions/[A-Za-z0-9][A-Za-z0-9-]{0,127}",
            execution_resource,
        ):
            raise M0ContractError(
                "TAKEOVER_PROOF_MISMATCH", "Unsafe Cloud Run execution resource"
            )
        url = f"https://run.googleapis.com/v2/{execution_resource}"
        headers: dict[str, str] = {"Accept": "application/json"}
        try:
            credentials.before_request(self._auth_request(), "GET", url, headers)
            response = self._session().get(
                url,
                headers=headers,
                timeout=30,
                allow_redirects=False,
            )
        except BaseException as exc:
            raise M0ContractError(
                "EXECUTION_STATUS_VERIFICATION_FAILED",
                f"Cloud Run status transport failed: {type(exc).__name__}",
            ) from exc
        if getattr(response, "status_code", 0) != 200:
            raise M0ContractError(
                "EXECUTION_STATUS_VERIFICATION_FAILED",
                "Cloud Run status lookup did not return an authenticated exact result",
            )
        try:
            document = response.json()
        except (TypeError, ValueError) as exc:
            raise M0ContractError(
                "EXECUTION_STATUS_VERIFICATION_FAILED",
                "Cloud Run status response is not valid JSON",
            ) from exc
        if (
            not isinstance(document, Mapping)
            or document.get("name") != execution_resource
        ):
            raise M0ContractError(
                "TAKEOVER_PROOF_MISMATCH", "Cloud Run returned another execution"
            )
        completion_time = document.get("completionTime")
        if completion_time is None:
            observed_at = _rfc3339(self._now())
            terminal_state = None
        elif not isinstance(completion_time, str):
            raise M0ContractError(
                "EXECUTION_STATUS_VERIFICATION_FAILED",
                "Cloud Run completion time is not trustworthy",
            )
        else:
            try:
                parsed = datetime.fromisoformat(completion_time.replace("Z", "+00:00"))
            except ValueError as exc:
                raise M0ContractError(
                    "EXECUTION_STATUS_VERIFICATION_FAILED",
                    "Cloud Run completion time is not trustworthy",
                ) from exc
            observed_at = _rfc3339(parsed)
            terminal_state = "cancelled" if self._cancelled(document) else "terminal"
        return CloudRunExecutionStatus(
            execution_resource=execution_resource,
            terminal_state=terminal_state,
            observed_at=observed_at,
        )


__all__ = [
    "CloudInvocationIdentity",
    "CloudRunADCExecutionStatusVerifier",
    "CloudRunEnvironmentIdentityResolver",
    "CloudRunExecutionStatus",
    "CloudRunStatusTransport",
    "RequestsCloudRunStatusTransport",
]
