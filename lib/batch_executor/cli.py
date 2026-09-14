"""Thin Batch Executor V2 M3 CLI for Local and single-task Cloud profiles."""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import sys
import threading
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from urllib.parse import unquote, urlparse

from .contracts import (
    M0ContractError,
    canonical_sha256,
    exact_identity,
    validate_batch_request,
)
from .engine import CloudBatchExecutor, LocalBatchExecutor
from .errors import M1ExecutionError
from .fake_gcs import FakeGCS
from .gcs_storage import (
    GCSObjectTransport,
    GCSStore,
    GoogleCloudStorageTransport,
)
from .gemini_adapter import (
    GeminiOmniVertexAdapter,
    RequestsVertexInteractionsTransport,
    validate_vertex_adapter_config,
)
from .identity import CLOUD_PLATFORM_SCOPE, CredentialResolver, GoogleADCResolver
from .media_validation import DeterministicFakeMediaValidator, FFprobeMediaValidator
from .ownership import ExecutionStatusVerifier
from .runtime import (
    CloudRunADCExecutionStatusVerifier,
    CloudRunEnvironmentIdentityResolver,
    CloudRunStatusTransport,
    RequestsCloudRunStatusTransport,
)
from .testing import ScriptedFakeProvider
from .tool_adapter import ProviderAdapter
from .workspace import materialize_project_snapshot, validate_snapshot_roots


_BASE_CONFIG_FIELDS = {
    "version",
    "config_digest",
    "profile",
    "transport_mode",
    "projects_root",
    "request_uri",
    "request_digest",
    "observed_source_revision",
    "invocation_id",
    "invocation_mode",
    "adapter_config",
}
_CLOUD_FIELDS = {
    "bucket",
    "storage_project",
    "cloud_run_project",
    "cloud_run_location",
    "cloud_run_job",
    "input_snapshot_projects_root",
    "input_snapshot_object_prefix",
}
_SAFE_CLOUD_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,127}$")
_SAFE_BUCKET = re.compile(r"^[a-z0-9][a-z0-9._-]{1,220}[a-z0-9]$")
_REQUEST_FAILURE_CODES = {
    "ADAPTER_CONFIG_DIGEST_MISMATCH",
    "ADAPTER_CONFIG_INVALID",
    "APPROVAL_MISSING_OR_STALE",
    "BUDGET_AUTHORIZATION_EXCEEDED",
    "BUDGET_AUTHORIZATION_INVALID",
    "EXACT_IDENTITY_MISMATCH",
    "INVALID_STORAGE_PROFILE",
    "PROJECT_IDENTITY_INVALID",
    "REQUEST_CONFLICT",
    "REQUEST_CONTRACT_INVALID",
    "SOURCE_BINDING_CHANGED",
}
_CONFIGURATION_FAILURE_CODES = {
    "AUTH_CONFIGURATION",
    "OFFLINE_QUALIFICATION_REQUIRED",
    "REQUEST_URI_INVALID",
    "RUNTIME_CONFIG_DIGEST_MISMATCH",
    "RUNTIME_CONFIG_INVALID",
    "RUNTIME_CONFIG_MISMATCH",
}


@dataclass
class RuntimeDependencies:
    """Injectable external boundaries; defaults are constructed lazily."""

    environment: Mapping[str, str] | None = None
    credential_resolver: CredentialResolver | None = None
    gcs_transport: GCSObjectTransport | None = None
    vertex_transport: Any | None = None
    cloud_status_transport: CloudRunStatusTransport | None = None
    fake_provider_factory: Callable[[], ProviderAdapter] | None = None


def _runtime_config_digest(config: Mapping[str, Any]) -> str:
    candidate = deepcopy(dict(config))
    candidate.pop("config_digest", None)
    return canonical_sha256(candidate)


def validate_runtime_config(config: Mapping[str, Any]) -> None:
    profile = config.get("profile")
    expected_fields = set(_BASE_CONFIG_FIELDS)
    if profile == "cloud_run":
        expected_fields.add("cloud")
    if set(config) != expected_fields:
        raise M0ContractError(
            "RUNTIME_CONFIG_INVALID",
            f"Unexpected or missing runtime config fields: {sorted(set(config) ^ expected_fields)}",
        )
    if config.get("version") != "1.0" or profile not in {"local", "cloud_run"}:
        raise M0ContractError(
            "RUNTIME_CONFIG_INVALID", "Unsupported profile/config version"
        )
    if config.get("transport_mode") not in {"offline_fake", "vertex"}:
        raise M0ContractError(
            "RUNTIME_CONFIG_INVALID", "Transport mode must be offline_fake or vertex"
        )
    projects_root = config.get("projects_root")
    if not isinstance(projects_root, str) or not Path(projects_root).is_absolute():
        raise M0ContractError(
            "RUNTIME_CONFIG_INVALID", "projects_root must be an explicit absolute path"
        )
    if not isinstance(config.get("request_uri"), str) or "?" in config["request_uri"]:
        raise M0ContractError(
            "RUNTIME_CONFIG_INVALID", "Request URI must be explicit and unsigned"
        )
    if not re.fullmatch(r"[0-9a-f]{64}", str(config.get("request_digest", ""))):
        raise M0ContractError("RUNTIME_CONFIG_INVALID", "Request digest is invalid")
    source = config.get("observed_source_revision")
    if (
        not isinstance(source, Mapping)
        or set(source) != {"kind", "revision"}
        or source.get("kind") not in {"git_commit", "content_snapshot"}
        or not isinstance(source.get("revision"), str)
        or not source["revision"]
    ):
        raise M0ContractError(
            "RUNTIME_CONFIG_INVALID", "Observed source revision must be explicit"
        )
    if not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", str(config.get("invocation_id", ""))
    ):
        raise M0ContractError("RUNTIME_CONFIG_INVALID", "Invocation ID is unsafe")
    mode = config.get("invocation_mode")
    if mode not in {"run", "resume"} or (profile == "local" and mode != "run"):
        raise M0ContractError(
            "RUNTIME_CONFIG_INVALID", "Invalid invocation mode/profile"
        )
    adapter = config.get("adapter_config")
    if not isinstance(adapter, Mapping):
        raise M0ContractError("RUNTIME_CONFIG_INVALID", "Adapter config is required")
    validate_vertex_adapter_config(adapter)
    if (
        adapter["request_digest"] != config["request_digest"]
        or adapter["identity"] != exact_identity()
    ):
        raise M0ContractError(
            "ADAPTER_CONFIG_DIGEST_MISMATCH",
            "Runtime and adapter configs do not bind the same request/identity",
        )
    if profile == "cloud_run":
        cloud = config.get("cloud")
        if not isinstance(cloud, Mapping) or set(cloud) != _CLOUD_FIELDS:
            raise M0ContractError(
                "RUNTIME_CONFIG_INVALID", "Exact Cloud profile settings are required"
            )
        if (
            not isinstance(cloud.get("bucket"), str)
            or not _SAFE_BUCKET.fullmatch(cloud["bucket"])
            or not all(
                isinstance(cloud.get(field), str)
                and bool(_SAFE_CLOUD_COMPONENT.fullmatch(cloud[field]))
                for field in _CLOUD_FIELDS
                - {
                    "bucket",
                    "input_snapshot_projects_root",
                    "input_snapshot_object_prefix",
                }
            )
        ):
            raise M0ContractError(
                "RUNTIME_CONFIG_INVALID", "Cloud profile values must be explicit"
            )
        snapshot_root = cloud.get("input_snapshot_projects_root")
        snapshot_prefix = cloud.get("input_snapshot_object_prefix")
        if (
            not isinstance(snapshot_root, str)
            or not Path(snapshot_root).is_absolute()
            or not isinstance(snapshot_prefix, str)
            or re.fullmatch(
                r"batch-v2-input-snapshots/sha256/[0-9a-f]{64}", snapshot_prefix
            )
            is None
        ):
            raise M0ContractError(
                "RUNTIME_CONFIG_INVALID",
                "Cloud input snapshot root/prefix must be explicit and immutable",
            )
        try:
            validate_snapshot_roots(
                projects_root=projects_root,
                snapshot_projects_root=snapshot_root,
            )
        except M1ExecutionError as exc:
            raise M0ContractError("RUNTIME_CONFIG_INVALID", str(exc)) from exc
    if config.get("config_digest") != _runtime_config_digest(config):
        raise M0ContractError(
            "RUNTIME_CONFIG_DIGEST_MISMATCH", "Runtime config changed"
        )


def freeze_runtime_config(config: Mapping[str, Any]) -> dict[str, Any]:
    frozen = deepcopy(dict(config))
    frozen["config_digest"] = _runtime_config_digest(frozen)
    validate_runtime_config(frozen)
    return frozen


def _load_local_bytes(uri: str) -> bytes:
    direct_path = Path(uri)
    if direct_path.is_absolute():
        path = direct_path
    else:
        parsed = urlparse(uri)
        if parsed.scheme and parsed.scheme != "file":
            raise M0ContractError("REQUEST_URI_INVALID", "Expected a local file URI")
        if parsed.scheme == "file":
            raw_path = unquote(parsed.path)
            if os.name == "nt" and re.match(r"^/[A-Za-z]:", raw_path):
                raw_path = raw_path[1:]
            path = Path(raw_path)
        else:
            path = direct_path
    if not path.is_absolute():
        raise M0ContractError("REQUEST_URI_INVALID", "Local URI must be absolute")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise M0ContractError(
            "REQUEST_URI_INVALID", "Local JSON input is unreadable"
        ) from exc


def _decode_json(payload: bytes, *, kind: str) -> dict[str, Any]:
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise M0ContractError(
            f"{kind.upper()}_INVALID", f"{kind} is not valid JSON"
        ) from exc
    if not isinstance(value, dict):
        raise M0ContractError(f"{kind.upper()}_INVALID", f"{kind} must be an object")
    return value


def _build_google_gcs_transport(
    config: Mapping[str, Any], resolver: CredentialResolver
) -> GoogleCloudStorageTransport:
    try:
        adc = resolver.resolve(scopes=(CLOUD_PLATFORM_SCOPE,))
    except Exception as exc:
        raise M1ExecutionError(
            "AUTH_CONFIGURATION", "GCS ADC resolution failed"
        ) from exc
    if adc.source != "adc" or adc.credentials is None:
        raise M1ExecutionError("AUTH_CONFIGURATION", "GCS requires ADC")
    try:
        from google.cloud import storage

        client = storage.Client(
            project=config["cloud"]["storage_project"], credentials=adc.credentials
        )
    except Exception as exc:
        raise M1ExecutionError(
            "AUTH_CONFIGURATION", "GCS client construction failed"
        ) from exc
    return GoogleCloudStorageTransport(client)


def _load_uri(
    uri: str,
    *,
    config: Mapping[str, Any],
    gcs_transport: GCSObjectTransport | None,
) -> bytes:
    if not uri.startswith("gs://"):
        return _load_local_bytes(uri)
    if "?" in uri or gcs_transport is None:
        raise M0ContractError(
            "REQUEST_URI_INVALID", "Private GCS transport is required"
        )
    bucket, separator, name = uri[5:].partition("/")
    if not separator or bucket != config["cloud"]["bucket"]:
        raise M0ContractError(
            "REQUEST_URI_INVALID", "GCS URI is outside the explicit private bucket"
        )
    try:
        snapshot = gcs_transport.read_object(bucket=bucket, name=name)
    except Exception as exc:
        raise M1ExecutionError(
            "GCS_TRANSIENT", "Failed to read immutable GCS input"
        ) from exc
    if snapshot.data is None:
        raise M1ExecutionError("GCS_TRANSIENT", "GCS input returned no bytes")
    return snapshot.data


def _exit_for_result(result: Mapping[str, Any]) -> int:
    if result["outcome"] == "all_succeeded":
        return 0
    if result["outcome"] == "indeterminate":
        return 5
    if result["outcome"] == "cancelled":
        return 6
    return 4


def _exit_for_exception(exc: BaseException) -> int:
    if isinstance(exc, SystemExit):
        return 0 if exc.code in {None, 0} else 2
    if isinstance(exc, M0ContractError):
        return 3 if exc.code in _CONFIGURATION_FAILURE_CODES else 2
    if isinstance(exc, M1ExecutionError):
        return 2 if exc.code in _REQUEST_FAILURE_CODES else 3
    return 10


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="batch_execute")
    parser.add_argument("command", choices=("run", "resume"))
    parser.add_argument("--profile", choices=("local", "cloud-run"), required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--request-uri", required=True)
    parser.add_argument("--resume-proof-uri")
    parser.add_argument(
        "--resume-proof-kind", choices=("control-plane", "human-authorization")
    )
    parser.add_argument(
        "--offline-qualification",
        action="store_true",
        help="Authorize the explicit no-network portable FakeGCS qualification path",
    )
    return parser


def run_cli(
    argv: Sequence[str],
    *,
    dependencies: RuntimeDependencies | None = None,
    cancellation: threading.Event | None = None,
    emit: Callable[[str], None] = print,
) -> int:
    dependencies = dependencies or RuntimeDependencies()
    cancellation = cancellation or threading.Event()
    result_locator: str | None = None
    try:
        args = _parser().parse_args(list(argv))
        config = _decode_json(_load_local_bytes(args.config), kind="runtime_config")
        validate_runtime_config(config)
        profile = "cloud_run" if args.profile == "cloud-run" else "local"
        if (
            config["profile"] != profile
            or config["invocation_mode"] != args.command
            or config["request_uri"] != args.request_uri
        ):
            raise M0ContractError(
                "RUNTIME_CONFIG_MISMATCH",
                "CLI command/profile/request URI differs from frozen runtime config",
            )
        offline_qualification = bool(args.offline_qualification)
        if (
            profile == "cloud_run"
            and config["transport_mode"] == "offline_fake"
            and not offline_qualification
        ):
            raise M0ContractError(
                "OFFLINE_QUALIFICATION_REQUIRED",
                "Cloud FakeGCS execution requires the explicit test-only qualification flag",
            )
        if offline_qualification and config["transport_mode"] != "offline_fake":
            raise M0ContractError(
                "RUNTIME_CONFIG_MISMATCH",
                "Offline qualification cannot authorize a production transport",
            )
        resolver = dependencies.credential_resolver or GoogleADCResolver()
        gcs_transport = dependencies.gcs_transport
        if profile == "cloud_run" and gcs_transport is None:
            gcs_transport = (
                FakeGCS()
                if config["transport_mode"] == "offline_fake"
                else _build_google_gcs_transport(config, resolver)
            )
        request = _decode_json(
            _load_uri(args.request_uri, config=config, gcs_transport=gcs_transport),
            kind="batch_request",
        )
        validate_batch_request(request)
        if request["request_digest"] != config["request_digest"]:
            raise M0ContractError(
                "RUNTIME_CONFIG_MISMATCH", "Runtime config binds another request"
            )
        if offline_qualification and request["execution_policy"][
            "storage_profile"
        ] != "portable":
            raise M0ContractError(
                "INVALID_STORAGE_PROFILE",
                "Offline qualification requires the explicit portable storage profile",
            )
        if (
            request["execution_policy"]["storage_profile"] == "portable"
            and config["transport_mode"] != "offline_fake"
        ):
            raise M0ContractError(
                "INVALID_STORAGE_PROFILE",
                "portable storage profile is reserved for offline parity qualification",
            )
        project_dir = Path(config["projects_root"]) / request["project_id"]
        if profile == "cloud_run":
            project_dir = materialize_project_snapshot(
                projects_root=config["projects_root"],
                snapshot_projects_root=config["cloud"]["input_snapshot_projects_root"],
                project_id=request["project_id"],
            )
        if config["transport_mode"] == "offline_fake":
            provider = (
                dependencies.fake_provider_factory()
                if dependencies.fake_provider_factory is not None
                else ScriptedFakeProvider()
            )
            media_validator = DeterministicFakeMediaValidator()
            adapter_observation = {
                "identity": exact_identity(),
                "route_binding": "explicit_request",
                "credential_mode": "adc",
                "hidden_writers": "disabled",
                "available": True,
            }
        else:
            provider = GeminiOmniVertexAdapter(
                config=config["adapter_config"],
                project_dir=project_dir,
                credential_resolver=resolver,
                transport=(
                    dependencies.vertex_transport
                    or RequestsVertexInteractionsTransport()
                ),
            )
            media_validator = FFprobeMediaValidator()
            adapter_observation = provider.observation

        if profile == "local":
            if args.resume_proof_uri or args.resume_proof_kind:
                raise M0ContractError(
                    "RUNTIME_CONFIG_MISMATCH", "Local run cannot carry Cloud proof"
                )
            executor = LocalBatchExecutor(
                projects_root=config["projects_root"],
                provider=provider,
                media_validator=media_validator,
            )
            result = executor.run(
                request,
                observed_source_revision=config["observed_source_revision"],
                adapter_observation=adapter_observation,
                invocation_id=config["invocation_id"],
                cancellation=cancellation,
            )
            result_locator = str(
                project_dir / ".batch-v2" / "runs" / request["batch_id"] / "result.json"
            )
        else:
            assert gcs_transport is not None
            cloud = config["cloud"]
            identity = CloudRunEnvironmentIdentityResolver(
                cloud_project=cloud["cloud_run_project"],
                location=cloud["cloud_run_location"],
                job_name=cloud["cloud_run_job"],
                environment=(
                    dependencies.environment
                    if dependencies.environment is not None
                    else os.environ
                ),
            ).resolve(
                invocation_id=config["invocation_id"],
                mode=config["invocation_mode"],
            )
            status_verifier: ExecutionStatusVerifier | None = None
            resume_authorization: Mapping[str, Any] | None = None
            if args.command == "resume":
                if (
                    args.resume_proof_kind == "control-plane"
                    and not args.resume_proof_uri
                ):
                    status_transport = dependencies.cloud_status_transport
                    if status_transport is None:
                        status_transport = RequestsCloudRunStatusTransport()
                    status_verifier = CloudRunADCExecutionStatusVerifier(
                        cloud_project=cloud["cloud_run_project"],
                        location=cloud["cloud_run_location"],
                        job_name=cloud["cloud_run_job"],
                        credential_resolver=resolver,
                        transport=status_transport,
                    )
                elif (
                    args.resume_proof_kind == "human-authorization"
                    and args.resume_proof_uri
                ):
                    resume_authorization = _decode_json(
                        _load_uri(
                            args.resume_proof_uri,
                            config=config,
                            gcs_transport=gcs_transport,
                        ),
                        kind="resume_authorization",
                    )
                else:
                    raise M0ContractError(
                        "TAKEOVER_PROOF_REQUIRED",
                        "Resume requires exactly one proof source",
                    )
            elif args.resume_proof_uri or args.resume_proof_kind:
                raise M0ContractError(
                    "RUNTIME_CONFIG_MISMATCH",
                    "Ordinary run cannot carry takeover proof",
                )
            executor = CloudBatchExecutor(
                projects_root=config["projects_root"],
                provider=provider,
                media_validator=media_validator,
                store_factory=lambda exact_project_dir, batch_id: GCSStore(
                    exact_project_dir,
                    batch_id,
                    bucket=cloud["bucket"],
                    transport=gcs_transport,
                ),
            )
            result = executor.run(
                request,
                observed_source_revision=config["observed_source_revision"],
                adapter_observation=adapter_observation,
                trusted_invocation=identity,
                cancellation=cancellation,
                execution_status_verifier=status_verifier,
                resume_authorization=resume_authorization,
            )
            result_locator = (
                f"gs://{cloud['bucket']}/projects/{request['project_id']}/.batch-v2/"
                f"runs/{request['batch_id']}/result.json"
            )
        qualification = None
        if offline_qualification:
            result_locator = None
            qualification = {
                "mode": "offline_fake_non_production",
                "durability": (
                    "process_memory" if profile == "cloud_run" else "local_workspace"
                ),
                "semantics": {
                    "batch_id": result["batch_id"],
                    "request_digest": result["request_digest"],
                    "status": result["status"],
                    "outcome": result["outcome"],
                    "counts": deepcopy(result["counts"]),
                    "items": [
                        {"item_id": item["item_id"], "state": item["state"]}
                        for item in result["items"]
                    ],
                    "cost": deepcopy(result["cost"]),
                    "statistics": deepcopy(result["statistics"]),
                },
            }
        exit_code = _exit_for_result(result)
        summary = {
            "exit_code": exit_code,
            "outcome": result["outcome"],
            "result_locator": result_locator,
        }
        if qualification is not None:
            summary["qualification"] = qualification
        emit(json.dumps(summary, sort_keys=True))
        return exit_code
    except BaseException as exc:
        if isinstance(exc, KeyboardInterrupt):
            cancellation.set()
        exit_code = _exit_for_exception(exc)
        payload = {
            "error_code": (
                "CLI_ARGUMENT_INVALID"
                if isinstance(exc, SystemExit)
                else getattr(exc, "code", "INTERNAL_FAILURE")
            ),
            "exit_code": exit_code,
        }
        if result_locator is not None:
            payload["result_locator"] = result_locator
        emit(json.dumps(payload, sort_keys=True))
        return exit_code


def main(argv: Sequence[str] | None = None) -> int:
    cancellation = threading.Event()
    previous_handlers: dict[int, Any] = {}

    def cancel(_signum: int, _frame: Any) -> None:
        cancellation.set()

    for signal_number in (signal.SIGINT, signal.SIGTERM):
        previous_handlers[signal_number] = signal.getsignal(signal_number)
        signal.signal(signal_number, cancel)
    try:
        return run_cli(
            sys.argv[1:] if argv is None else argv,
            cancellation=cancellation,
        )
    finally:
        for signal_number, handler in previous_handlers.items():
            signal.signal(signal_number, handler)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


__all__ = [
    "RuntimeDependencies",
    "freeze_runtime_config",
    "main",
    "run_cli",
    "validate_runtime_config",
]
