"""Separate production composition root for Agent-invoked Cloud publication.

This entrypoint consumes an already-authored immutable command.  It cannot
author review/Human evidence, select a stage/provider/model, or execute work.
Construction is injectable for offline FakeGCS qualification; production
always composes concrete ADC-backed transports and the concrete Cloud Run
control-plane verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from .contracts import (
    M0ContractError,
    canonical_json_bytes,
    canonical_sha256,
    validate_publication_authorization,
    validate_publication_command,
)
from .errors import M1ExecutionError, M2PublicationError
from .fake_gcs import FakeGCS
from .gcs_storage import (
    GCSObjectTransport,
    GCSStore,
    GoogleCloudStorageTransport,
    crc32c_base64,
)
from .identity import CLOUD_PLATFORM_SCOPE, CredentialResolver, GoogleADCResolver
from .media_validation import FFprobeMediaValidator, MediaValidator
from .publication import CloudAssetsPublisher
from .runtime import (
    CloudRunADCExecutionStatusVerifier,
    CloudRunEnvironmentIdentityResolver,
    CloudRunStatusTransport,
    RequestsCloudRunStatusTransport,
)
from .workspace import materialize_project_snapshot, validate_snapshot_roots


_SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,127}$")
_SAFE_BUCKET = re.compile(r"^[a-z0-9][a-z0-9._-]{1,220}[a-z0-9]$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_CONFIG_FIELDS = {
    "version",
    "config_digest",
    "profile",
    "transport_mode",
    "projects_root",
    "input_snapshot_projects_root",
    "input_snapshot_object_prefix",
    "bucket",
    "storage_project",
    "cloud_run_project",
    "cloud_run_location",
    "source_cloud_run_job",
    "publication_cloud_run_job",
    "invocation_id",
    "command_ref",
    "proof_kind",
    "authorization_ref",
}


@dataclass
class PublicationRuntimeDependencies:
    """Explicit test seams; production defaults remain ADC-backed/concrete."""

    environment: Mapping[str, str] | None = None
    credential_resolver: CredentialResolver | None = None
    gcs_transport: GCSObjectTransport | None = None
    cloud_status_transport: CloudRunStatusTransport | None = None
    media_validator: MediaValidator | None = None
    allow_offline_fake: bool = False


def _config_digest(config: Mapping[str, Any]) -> str:
    candidate = deepcopy(dict(config))
    candidate.pop("config_digest", None)
    return canonical_sha256(candidate)


def _validate_ref(reference: Any, *, kind: str) -> None:
    if (
        not isinstance(reference, Mapping)
        or set(reference) != {"uri", "generation", "sha256", f"{kind}_digest"}
        or not isinstance(reference.get("uri"), str)
        or not reference["uri"].startswith("gs://")
        or "?" in reference["uri"]
        or isinstance(reference.get("generation"), bool)
        or not isinstance(reference.get("generation"), int)
        or reference["generation"] < 1
        or not _DIGEST.fullmatch(str(reference.get("sha256", "")))
        or not _DIGEST.fullmatch(str(reference.get(f"{kind}_digest", "")))
    ):
        raise M0ContractError(
            "PUBLICATION_RUNTIME_CONFIG_INVALID",
            f"Exact immutable {kind} URI/generation/digests are required",
        )


def validate_publication_runtime_config(config: Mapping[str, Any]) -> None:
    if set(config) != _CONFIG_FIELDS or config.get("version") != "1.0":
        raise M0ContractError(
            "PUBLICATION_RUNTIME_CONFIG_INVALID",
            "Unexpected/missing publication runtime config fields",
        )
    if config.get("profile") != "cloud_run_publication" or config.get(
        "transport_mode"
    ) not in {"gcs_adc", "offline_fake"}:
        raise M0ContractError(
            "PUBLICATION_RUNTIME_CONFIG_INVALID",
            "Only the explicit Cloud publication profile is supported",
        )
    if not _SAFE_BUCKET.fullmatch(str(config.get("bucket", ""))) or not all(
        _SAFE_COMPONENT.fullmatch(str(config.get(field, "")))
        for field in (
            "storage_project",
            "cloud_run_project",
            "cloud_run_location",
            "source_cloud_run_job",
            "publication_cloud_run_job",
            "invocation_id",
        )
    ):
        raise M0ContractError(
            "PUBLICATION_RUNTIME_CONFIG_INVALID",
            "Cloud publication identities must be explicit and safe",
        )
    projects_root = config.get("projects_root")
    snapshot_root = config.get("input_snapshot_projects_root")
    try:
        validate_snapshot_roots(
            projects_root=str(projects_root),
            snapshot_projects_root=str(snapshot_root),
        )
    except (M1ExecutionError, TypeError) as exc:
        raise M0ContractError("PUBLICATION_RUNTIME_CONFIG_INVALID", str(exc)) from exc
    if (
        re.fullmatch(
            r"batch-v2-input-snapshots/sha256/[0-9a-f]{64}",
            str(config.get("input_snapshot_object_prefix", "")),
        )
        is None
    ):
        raise M0ContractError(
            "PUBLICATION_RUNTIME_CONFIG_INVALID",
            "Input snapshot prefix must be immutable and content-addressed",
        )
    _validate_ref(config.get("command_ref"), kind="command")
    proof_kind = config.get("proof_kind")
    authorization = config.get("authorization_ref")
    if proof_kind == "control-plane":
        if authorization is not None:
            raise M0ContractError(
                "PUBLICATION_RUNTIME_CONFIG_INVALID",
                "Control-plane proof cannot carry a Human authorization",
            )
    elif proof_kind == "human-authorization":
        _validate_ref(authorization, kind="authorization")
    else:
        raise M0ContractError(
            "PUBLICATION_RUNTIME_CONFIG_INVALID", "Unknown publication proof kind"
        )
    if config.get("config_digest") != _config_digest(config):
        raise M0ContractError(
            "PUBLICATION_RUNTIME_CONFIG_DIGEST_MISMATCH",
            "Publication runtime config bytes changed",
        )


def freeze_publication_runtime_config(config: Mapping[str, Any]) -> dict[str, Any]:
    frozen = deepcopy(dict(config))
    frozen["config_digest"] = _config_digest(frozen)
    validate_publication_runtime_config(frozen)
    return frozen


def _parse_private_uri(uri: str, *, bucket: str) -> str:
    if not isinstance(uri, str) or not uri.startswith("gs://") or "?" in uri:
        raise M0ContractError(
            "PUBLICATION_INPUT_URI_INVALID", "Expected an unsigned private GCS URI"
        )
    actual_bucket, separator, name = uri[5:].partition("/")
    if not separator or actual_bucket != bucket or not name or name.startswith("/"):
        raise M0ContractError(
            "PUBLICATION_INPUT_URI_INVALID", "Input URI is outside the exact bucket"
        )
    return name


def _load_bound_object(
    *,
    transport: GCSObjectTransport,
    bucket: str,
    reference: Mapping[str, Any],
) -> tuple[bytes, str]:
    name = _parse_private_uri(str(reference["uri"]), bucket=bucket)
    try:
        snapshot = transport.read_object(
            bucket=bucket, name=name, generation=int(reference["generation"])
        )
        head = transport.head_object(
            bucket=bucket, name=name, generation=int(reference["generation"])
        )
    except Exception as exc:
        raise M1ExecutionError(
            "GCS_TRANSIENT", "Exact immutable publication input is unavailable"
        ) from exc
    if snapshot.data is None:
        raise M1ExecutionError("GCS_TRANSIENT", "Publication input returned no bytes")
    payload = bytes(snapshot.data)
    if (
        snapshot.bucket != bucket
        or head.bucket != bucket
        or snapshot.name != name
        or head.name != name
        or snapshot.generation != reference["generation"]
        or head.generation != reference["generation"]
        or snapshot.size_bytes != len(payload)
        or head.size_bytes != len(payload)
        or snapshot.crc32c != crc32c_base64(payload)
        or head.crc32c != crc32c_base64(payload)
        or hashlib.sha256(payload).hexdigest() != reference["sha256"]
        or dict(snapshot.metadata) != dict(head.metadata)
    ):
        raise M1ExecutionError(
            "GCS_VERIFICATION_FAILED", "Publication input object facts changed"
        )
    return payload, name


def _decode(payload: bytes, *, kind: str) -> dict[str, Any]:
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise M0ContractError(
            f"{kind.upper()}_INVALID", f"{kind} is not valid JSON"
        ) from exc
    if not isinstance(value, dict):
        raise M0ContractError(f"{kind.upper()}_INVALID", f"{kind} must be an object")
    return value


def _build_gcs_transport(
    config: Mapping[str, Any], resolver: CredentialResolver
) -> GoogleCloudStorageTransport:
    try:
        adc = resolver.resolve(scopes=(CLOUD_PLATFORM_SCOPE,))
        if adc.source != "adc" or adc.credentials is None:
            raise ValueError("ADC required")
        from google.cloud import storage

        client = storage.Client(
            project=config["storage_project"], credentials=adc.credentials
        )
    except Exception as exc:
        raise M1ExecutionError(
            "AUTH_CONFIGURATION", "Publication GCS transport requires ADC"
        ) from exc
    return GoogleCloudStorageTransport(client)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="batch_publish")
    parser.add_argument("command", choices=("publish",))
    parser.add_argument("--config", required=True)
    parser.add_argument("--command-uri", required=True)
    parser.add_argument("--command-generation", type=int, required=True)
    parser.add_argument("--command-sha256", required=True)
    parser.add_argument("--command-digest", required=True)
    parser.add_argument("--authorization-uri")
    parser.add_argument("--authorization-generation", type=int)
    parser.add_argument("--authorization-sha256")
    parser.add_argument("--authorization-digest")
    return parser


def run_publication_cli(
    argv: Sequence[str],
    *,
    dependencies: PublicationRuntimeDependencies | None = None,
    emit: Callable[[str], None] = print,
) -> int:
    dependencies = dependencies or PublicationRuntimeDependencies()
    try:
        args = _parser().parse_args(list(argv))
        config_path = Path(args.config)
        if not config_path.is_absolute():
            raise M0ContractError(
                "PUBLICATION_RUNTIME_CONFIG_INVALID", "Config path must be absolute"
            )
        config = _decode(config_path.read_bytes(), kind="publication_runtime_config")
        validate_publication_runtime_config(config)
        command_ref = config["command_ref"]
        cli_ref = {
            "uri": args.command_uri,
            "generation": args.command_generation,
            "sha256": args.command_sha256,
            "command_digest": args.command_digest,
        }
        if canonical_json_bytes(cli_ref) != canonical_json_bytes(command_ref):
            raise M0ContractError(
                "PUBLICATION_RUNTIME_CONFIG_MISMATCH",
                "CLI command reference differs from frozen config",
            )
        authorization_ref = config["authorization_ref"]
        cli_authorization = None
        if any(
            value is not None
            for value in (
                args.authorization_uri,
                args.authorization_generation,
                args.authorization_sha256,
                args.authorization_digest,
            )
        ):
            cli_authorization = {
                "uri": args.authorization_uri,
                "generation": args.authorization_generation,
                "sha256": args.authorization_sha256,
                "authorization_digest": args.authorization_digest,
            }
        if canonical_json_bytes(cli_authorization) != canonical_json_bytes(
            authorization_ref
        ):
            raise M0ContractError(
                "PUBLICATION_RUNTIME_CONFIG_MISMATCH",
                "CLI authorization reference differs from frozen config",
            )
        resolver = dependencies.credential_resolver or GoogleADCResolver()
        transport = dependencies.gcs_transport
        if config["transport_mode"] == "offline_fake":
            if not (dependencies.allow_offline_fake and isinstance(transport, FakeGCS)):
                raise M0ContractError(
                    "PUBLICATION_OFFLINE_BOUNDARY_INVALID",
                    "Offline publication requires an explicit injected FakeGCS boundary",
                )
        elif transport is not None:
            raise M0ContractError(
                "PUBLICATION_RUNTIME_CONFIG_INVALID",
                "Production publication cannot replace the ADC GCS transport",
            )
        else:
            transport = _build_gcs_transport(config, resolver)
        assert transport is not None
        command_payload, command_name = _load_bound_object(
            transport=transport,
            bucket=config["bucket"],
            reference=command_ref,
        )
        command = _decode(command_payload, kind="publication_command")
        validate_publication_command(command)
        if command["command_digest"] != command_ref["command_digest"]:
            raise M0ContractError(
                "PUBLICATION_COMMAND_DIGEST_MISMATCH", "Command self-digest differs"
            )
        project_dir = materialize_project_snapshot(
            projects_root=config["projects_root"],
            snapshot_projects_root=config["input_snapshot_projects_root"],
            project_id=command["project_id"],
            exclude_assets_publication_outputs=True,
        )
        store = GCSStore(
            project_dir,
            command["batch_id"],
            bucket=config["bucket"],
            transport=transport,
        )
        expected_command_name = store.publication_command_object_name(
            command["command_id"]
        )
        durable_command, command_generation = store.load_publication_command(
            command["command_id"]
        )
        if (
            command_name != expected_command_name
            or command_generation != command_ref["generation"]
            or canonical_json_bytes(durable_command) != canonical_json_bytes(command)
        ):
            raise M0ContractError(
                "PUBLICATION_COMMAND_BINDING_INVALID",
                "Command URI is not the exact durable command authority",
            )
        identity = CloudRunEnvironmentIdentityResolver(
            cloud_project=config["cloud_run_project"],
            location=config["cloud_run_location"],
            job_name=config["publication_cloud_run_job"],
            environment=(
                dependencies.environment
                if dependencies.environment is not None
                else os.environ
            ),
        ).resolve(invocation_id=config["invocation_id"], mode="run")
        authorization = None
        verifier = None
        if config["proof_kind"] == "human-authorization":
            assert isinstance(authorization_ref, Mapping)
            authorization_payload, authorization_name = _load_bound_object(
                transport=transport,
                bucket=config["bucket"],
                reference=authorization_ref,
            )
            authorization = _decode(
                authorization_payload, kind="publication_authorization"
            )
            validate_publication_authorization(authorization)
            expected_authorization_name = (
                f"projects/{command['project_id']}/.batch-v2/runs/"
                f"{command['batch_id']}/publication/authorizations/"
                f"{authorization['authorization_digest']}.json"
            )
            if (
                authorization_name != expected_authorization_name
                or authorization["authorization_digest"]
                != authorization_ref["authorization_digest"]
            ):
                raise M0ContractError(
                    "PUBLICATION_AUTHORIZATION_BINDING_INVALID",
                    "Authorization URI/digest is not exact durable authority",
                )
            durable_authorization, authorization_generation = (
                store.load_publication_authorization(
                    authorization["authorization_digest"]
                )
            )
            if authorization_generation != authorization_ref[
                "generation"
            ] or canonical_json_bytes(durable_authorization) != canonical_json_bytes(
                authorization
            ):
                raise M0ContractError(
                    "PUBLICATION_AUTHORIZATION_BINDING_INVALID",
                    "Authorization generation/bytes changed",
                )
        else:
            status_transport = (
                dependencies.cloud_status_transport or RequestsCloudRunStatusTransport()
            )
            verifier = CloudRunADCExecutionStatusVerifier(
                cloud_project=config["cloud_run_project"],
                location=config["cloud_run_location"],
                job_name=config["source_cloud_run_job"],
                additional_job_names=(config["publication_cloud_run_job"],),
                credential_resolver=resolver,
                transport=status_transport,
            )
        if config["transport_mode"] == "gcs_adc" and dependencies.media_validator:
            raise M0ContractError(
                "PUBLICATION_RUNTIME_CONFIG_INVALID",
                "Production publication cannot replace the real media validator",
            )
        media_validator = dependencies.media_validator or FFprobeMediaValidator()
        receipt = CloudAssetsPublisher(
            projects_root=config["projects_root"],
            bucket=config["bucket"],
            transport=transport,
            media_validator=media_validator,
            execution_status_verifier=verifier,
        ).publish(
            command,
            trusted_invocation=identity,
            publication_authorization=authorization,
        )
        emit(
            json.dumps(
                {
                    "exit_code": 0,
                    "command_digest": receipt["command_digest"],
                    "checkpoint_generation": receipt["checkpoint_generation"],
                    "status": receipt["status"],
                },
                sort_keys=True,
            )
        )
        return 0
    except BaseException as exc:
        code = getattr(exc, "code", "INTERNAL_FAILURE")
        exit_code = 2 if isinstance(exc, M0ContractError) else 3
        if not isinstance(exc, (M0ContractError, M1ExecutionError, M2PublicationError)):
            exit_code = 10
        emit(json.dumps({"error_code": code, "exit_code": exit_code}, sort_keys=True))
        return exit_code


def main(argv: Sequence[str] | None = None) -> int:
    return run_publication_cli(sys.argv[1:] if argv is None else argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


__all__ = [
    "PublicationRuntimeDependencies",
    "freeze_publication_runtime_config",
    "main",
    "run_publication_cli",
    "validate_publication_runtime_config",
]
