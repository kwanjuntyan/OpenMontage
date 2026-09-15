"""Minimal synchronous GCS durability adapter for Batch Executor V2 M3.

The store contains no scheduler or ownership policy.  It accepts an injected
object transport, performs conditional writes, and turns durable GCS facts into
the same execution contracts consumed by the LocalStore-backed engine.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import struct
import threading
from contextlib import nullcontext
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, ContextManager, Mapping, Protocol

from .contracts import (
    CANONICAL_JSON_VERSION,
    M0ContractError,
    canonical_json_bytes,
    canonical_sha256,
    derive_attempt_output_path,
    validate_canonical_asset_path,
    validate_batch_request,
    validate_batch_result,
    validate_batch_state,
    validate_publication_authorization,
    validate_publication_command,
    validate_publication_state,
    validate_storage_receipt,
)
from .errors import CoordinatorWriterViolation, M1ExecutionError, StorageConflict
from .media_validation import MediaValidator, OutputFacts
from .storage import _atomic_write, _digest_file, _validate_ownership_record


_GCS_BUCKET = re.compile(r"^[a-z0-9][a-z0-9._-]{1,220}[a-z0-9]$")
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class GCSObjectNotFound(RuntimeError):
    """The injected transport could not find an exact object/generation."""


class GCSPreconditionFailed(RuntimeError):
    """An injected transport rejected an expected-generation write."""


@dataclass(frozen=True)
class GCSObjectSnapshot:
    """Trusted facts returned synchronously by an object transport."""

    bucket: str
    name: str
    generation: int
    size_bytes: int
    crc32c: str
    metadata: Mapping[str, str]
    content_type: str
    data: bytes | None = None


class GCSObjectTransport(Protocol):
    """Small injected boundary used by GCSStore and its FakeGCS double."""

    def write_object(
        self,
        *,
        bucket: str,
        name: str,
        data: bytes,
        metadata: Mapping[str, str],
        content_type: str,
        if_generation_match: int,
    ) -> GCSObjectSnapshot: ...

    def read_object(
        self, *, bucket: str, name: str, generation: int | None = None
    ) -> GCSObjectSnapshot: ...

    def head_object(
        self, *, bucket: str, name: str, generation: int | None = None
    ) -> GCSObjectSnapshot: ...


def crc32c_base64(payload: bytes) -> str:
    """Return the GCS/HTTP base64 big-endian CRC32C representation."""

    crc = 0xFFFFFFFF
    polynomial = 0x82F63B78
    for octet in payload:
        crc ^= octet
        for _ in range(8):
            crc = (crc >> 1) ^ (polynomial if crc & 1 else 0)
    value = (~crc) & 0xFFFFFFFF
    return base64.b64encode(struct.pack(">I", value)).decode("ascii")


def _http_status(exception: BaseException) -> int | None:
    for name in ("code", "status_code"):
        value = getattr(exception, name, None)
        if callable(value):
            value = value()
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


class GoogleCloudStorageTransport:
    """Thin adapter over an explicitly constructed google-cloud-storage client.

    The client is injected after ADC resolution with an explicit billing/client
    project.  Constructing this class performs no credential or network access.
    """

    def __init__(self, client: Any):
        self._client = client

    @staticmethod
    def _snapshot(blob: Any, *, data: bytes | None) -> GCSObjectSnapshot:
        return GCSObjectSnapshot(
            bucket=str(blob.bucket.name),
            name=str(blob.name),
            generation=int(blob.generation),
            size_bytes=int(blob.size),
            crc32c=str(blob.crc32c),
            metadata=dict(blob.metadata or {}),
            content_type=str(blob.content_type or "application/octet-stream"),
            data=data,
        )

    @staticmethod
    def _translate(exc: BaseException) -> BaseException:
        status = _http_status(exc)
        if status == 404:
            return GCSObjectNotFound(str(exc))
        if status == 412:
            return GCSPreconditionFailed(str(exc))
        return exc

    def write_object(
        self,
        *,
        bucket: str,
        name: str,
        data: bytes,
        metadata: Mapping[str, str],
        content_type: str,
        if_generation_match: int,
    ) -> GCSObjectSnapshot:
        blob = self._client.bucket(bucket).blob(name)
        blob.metadata = dict(metadata)
        try:
            blob.upload_from_string(
                data,
                content_type=content_type,
                if_generation_match=if_generation_match,
                checksum="crc32c",
            )
            written_generation = int(blob.generation)
            blob = self._client.bucket(bucket).blob(name, generation=written_generation)
            blob.reload(if_generation_match=written_generation)
        except BaseException as exc:
            translated = self._translate(exc)
            if translated is exc:
                raise
            raise translated from exc
        return self._snapshot(blob, data=None)

    def read_object(
        self, *, bucket: str, name: str, generation: int | None = None
    ) -> GCSObjectSnapshot:
        blob = self._client.bucket(bucket).blob(name, generation=generation)
        try:
            blob.reload()
            data = blob.download_as_bytes(
                if_generation_match=int(blob.generation), checksum="crc32c"
            )
        except BaseException as exc:
            translated = self._translate(exc)
            if translated is exc:
                raise
            raise translated from exc
        return self._snapshot(blob, data=data)

    def head_object(
        self, *, bucket: str, name: str, generation: int | None = None
    ) -> GCSObjectSnapshot:
        blob = self._client.bucket(bucket).blob(name, generation=generation)
        try:
            blob.reload()
        except BaseException as exc:
            translated = self._translate(exc)
            if translated is exc:
                raise
            raise translated from exc
        return self._snapshot(blob, data=None)


class GCSStore:
    """Private, generation-bound Store implementation with synchronous checks."""

    def __init__(
        self,
        project_dir: str | Path,
        batch_id: str,
        *,
        bucket: str,
        transport: GCSObjectTransport,
    ):
        self.project_dir = Path(project_dir).resolve(strict=True)
        self.project_id = self.project_dir.name
        self.batch_id = batch_id
        if not isinstance(bucket, str) or not _GCS_BUCKET.fullmatch(bucket):
            raise M1ExecutionError(
                "GCS_CONFIGURATION_INVALID", "Invalid private bucket name"
            )
        self.bucket = bucket
        self.transport = transport
        self.run_dir = self.project_dir / ".batch-v2" / "runs" / batch_id
        self._prefix = f"projects/{self.project_id}/.batch-v2/runs/{batch_id}"
        self._request_name = f"{self._prefix}/request.json"
        self._state_name = f"{self._prefix}/state.json"
        self._result_name = f"{self._prefix}/result.json"
        self._writer_thread_id = threading.get_ident()
        self._assert_project_scoped_path(self.run_dir)

    @property
    def result_logical_path(self) -> str:
        return f".batch-v2/runs/{self.batch_id}/result.json"

    @property
    def request_object_name(self) -> str:
        return self._request_name

    @property
    def state_object_name(self) -> str:
        return self._state_name

    @property
    def result_object_name(self) -> str:
        return self._result_name

    @property
    def publication_state_object_name(self) -> str:
        return f"{self._prefix}/publication/state.json"

    @property
    def publication_fence_object_name(self) -> str:
        """Project/stage authority guard shared by every assets batch."""

        return f"projects/{self.project_id}/.batch-v2/publication/assets/fence.json"

    def publication_command_object_name(self, command_id: str) -> str:
        if not isinstance(command_id, str) or not _SAFE_ID.fullmatch(command_id):
            raise M1ExecutionError(
                "PUBLICATION_COMMAND_ID_INVALID", "Unsafe publication command ID"
            )
        return f"{self._prefix}/publication/commands/{command_id}.json"

    def _publication_fence(self, command: Mapping[str, Any]) -> dict[str, Any]:
        validate_publication_command(command)
        return {
            "version": "1.0",
            "canonical_json": CANONICAL_JSON_VERSION,
            "project_id": self.project_id,
            "stage": "assets",
            "batch_id": self.batch_id,
            "request_digest": str(command["request_digest"]),
            "source_state": dict(command["cloud_source"]["state"]),
        }

    def claim_publication_fence(
        self, command: Mapping[str, Any]
    ) -> tuple[dict[str, Any], int]:
        """Permanently bind one project/assets authority to one frozen batch.

        This is a finite CAS guard, not a lease.  Later lifecycle transitions
        for the same batch reuse the byte-identical guard; another batch fails
        closed before any canonical mutation.
        """

        self._assert_writer()
        fence = self._publication_fence(command)
        payload = canonical_json_bytes(fence)
        generation = self._write_immutable(
            name=self.publication_fence_object_name,
            payload=payload,
            metadata=self._record_metadata(
                "publication_fence",
                hashlib.sha256(payload).hexdigest(),
                stage="assets",
                request_digest=str(command["request_digest"]),
            ),
            content_type="application/json",
            conflict_code="PROJECT_STAGE_PUBLICATION_CONFLICT",
        )
        return fence, generation

    def verify_publication_fence(
        self, fence: Mapping[str, Any], *, generation: int
    ) -> None:
        """Re-read the exact project/stage guard before canonical writes."""

        self._assert_writer()
        if (
            set(fence)
            != {
                "version",
                "canonical_json",
                "project_id",
                "stage",
                "batch_id",
                "request_digest",
                "source_state",
            }
            or fence.get("version") != "1.0"
            or fence.get("canonical_json") != CANONICAL_JSON_VERSION
            or fence.get("project_id") != self.project_id
            or fence.get("stage") != "assets"
            or fence.get("batch_id") != self.batch_id
            or not re.fullmatch(r"[0-9a-f]{64}", str(fence.get("request_digest", "")))
            or not isinstance(fence.get("source_state"), Mapping)
        ):
            raise StorageConflict(
                "PROJECT_STAGE_PUBLICATION_CONFLICT",
                "Project/assets publication fence is malformed or names another batch",
            )
        payload = canonical_json_bytes(fence)
        self._read_and_verify(
            name=self.publication_fence_object_name,
            payload=payload,
            metadata=self._record_metadata(
                "publication_fence",
                hashlib.sha256(payload).hexdigest(),
                stage="assets",
                request_digest=str(fence["request_digest"]),
            ),
            content_type="application/json",
            generation=generation,
        )

    def load_publication_fence(
        self, command: Mapping[str, Any]
    ) -> tuple[dict[str, Any], int]:
        """Load the exact immutable project/assets guard without creating it."""

        self._assert_writer()
        fence = self._publication_fence(command)
        payload = canonical_json_bytes(fence)
        try:
            generation = self._read_and_verify(
                name=self.publication_fence_object_name,
                payload=payload,
                metadata=self._record_metadata(
                    "publication_fence",
                    hashlib.sha256(payload).hexdigest(),
                    stage="assets",
                    request_digest=str(command["request_digest"]),
                ),
                content_type="application/json",
            )
        except M1ExecutionError as exc:
            if exc.code in {"GCS_TRANSIENT", "AUTH_CONFIGURATION"}:
                raise
            raise StorageConflict(
                "PROJECT_STAGE_PUBLICATION_CONFLICT",
                "Project/assets publication fence is missing or differs",
            ) from exc
        except (GCSObjectNotFound, GCSPreconditionFailed) as exc:
            raise StorageConflict(
                "PROJECT_STAGE_PUBLICATION_CONFLICT",
                "Project/assets publication fence is missing or differs",
            ) from exc
        return fence, generation

    def _assert_writer(self) -> None:
        if threading.get_ident() != self._writer_thread_id:
            raise CoordinatorWriterViolation(
                "COORDINATOR_WRITER_REQUIRED",
                "Only the coordinator thread may mutate GCSStore",
            )

    def _assert_project_scoped_path(self, path: Path) -> Path:
        lexical = Path(os.path.abspath(path))
        resolved = path.resolve(strict=False)
        try:
            relative = resolved.relative_to(self.project_dir)
        except ValueError as exc:
            raise M1ExecutionError(
                "WORKSPACE_ESCAPE", f"Batch V2 path escapes project root: {path}"
            ) from exc
        if os.path.normcase(str(resolved)) != os.path.normcase(str(lexical)):
            raise M1ExecutionError(
                "WORKSPACE_ALIAS",
                f"Batch V2 path changes identity through an alias: {path}",
            )
        if relative.parts and relative.parts[0] != ".batch-v2":
            raise M1ExecutionError(
                "WORKSPACE_ESCAPE", "Cloud execution writes must remain under .batch-v2"
            )
        return resolved

    def acquire_run_lock(self) -> ContextManager[object]:
        self._assert_writer()
        # Cross-execution exclusion is the durable owner/proof/CAS protocol.
        # Within this one process the engine has exactly one coordinator.
        return nullcontext(self)

    def batch_state_exists(self) -> bool:
        try:
            self.transport.head_object(bucket=self.bucket, name=self._state_name)
        except GCSObjectNotFound:
            return False
        except Exception as exc:
            raise self._transport_error(
                exc, "BatchState existence check failed"
            ) from exc
        return True

    def attempt_output_path(
        self, item_id: str, attempt_id: str, output_name: str
    ) -> Path:
        return derive_attempt_output_path(
            self.project_dir.parent,
            self.project_id,
            self.batch_id,
            item_id,
            attempt_id,
            output_name,
        )

    def prepare_attempt_directory(self, output_path: Path) -> None:
        self._assert_writer()
        resolved = self._assert_project_scoped_path(output_path.parent)
        expected = (
            self.run_dir
            / "attempts"
            / output_path.parent.parent.name
            / output_path.parent.name
        )
        if os.path.normcase(str(resolved)) != os.path.normcase(str(expected)):
            raise M1ExecutionError(
                "WORKSPACE_ALIAS", "Attempt directory changes identity through an alias"
            )
        output_path.parent.mkdir(parents=True, exist_ok=True)

    def _record_metadata(
        self, record_type: str, digest: str, **extra: str
    ) -> dict[str, str]:
        return {
            "openmontage_schema": "batch-v2-v1",
            "record_type": record_type,
            "project_id": self.project_id,
            "batch_id": self.batch_id,
            "canonical_sha256": digest,
            **extra,
        }

    @staticmethod
    def _transport_error(exc: Exception, message: str) -> M1ExecutionError:
        code = (
            "AUTH_CONFIGURATION" if _http_status(exc) in {401, 403} else "GCS_TRANSIENT"
        )
        return M1ExecutionError(code, message)

    def _verify_exact_object(
        self,
        snapshot: GCSObjectSnapshot,
        head: GCSObjectSnapshot,
        *,
        name: str,
        payload: bytes,
        metadata: Mapping[str, str],
        content_type: str,
        expected_generation: int | None = None,
    ) -> None:
        digest = hashlib.sha256(payload).hexdigest()
        expected_crc32c = crc32c_base64(payload)
        if snapshot.data is None:
            raise M1ExecutionError(
                "GCS_VERIFICATION_FAILED", "GCS re-read returned no bytes"
            )
        if (
            snapshot.bucket != self.bucket
            or snapshot.name != name
            or head.bucket != self.bucket
            or head.name != name
            or snapshot.generation != head.generation
            or (
                expected_generation is not None
                and snapshot.generation != expected_generation
            )
            or snapshot.size_bytes != len(payload)
            or head.size_bytes != len(payload)
            or snapshot.data != payload
            or hashlib.sha256(snapshot.data).hexdigest() != digest
            or snapshot.crc32c != expected_crc32c
            or head.crc32c != expected_crc32c
            or dict(snapshot.metadata) != dict(metadata)
            or dict(head.metadata) != dict(metadata)
            or snapshot.content_type != content_type
            or head.content_type != content_type
        ):
            raise M1ExecutionError(
                "GCS_VERIFICATION_FAILED",
                f"GCS object identity/checksum/metadata mismatch for {name}",
            )

    def _read_and_verify(
        self,
        *,
        name: str,
        payload: bytes,
        metadata: Mapping[str, str],
        content_type: str,
        generation: int | None = None,
    ) -> int:
        try:
            snapshot = self.transport.read_object(
                bucket=self.bucket, name=name, generation=generation
            )
            head = self.transport.head_object(
                bucket=self.bucket, name=name, generation=snapshot.generation
            )
        except (GCSObjectNotFound, GCSPreconditionFailed, M1ExecutionError):
            raise
        except Exception as exc:
            raise self._transport_error(
                exc, f"GCS re-read/head failed for {name}"
            ) from exc
        self._verify_exact_object(
            snapshot,
            head,
            name=name,
            payload=payload,
            metadata=metadata,
            content_type=content_type,
            expected_generation=generation,
        )
        return snapshot.generation

    def _write_immutable(
        self,
        *,
        name: str,
        payload: bytes,
        metadata: Mapping[str, str],
        content_type: str,
        conflict_code: str,
    ) -> int:
        self._assert_writer()
        try:
            created = self.transport.write_object(
                bucket=self.bucket,
                name=name,
                data=payload,
                metadata=metadata,
                content_type=content_type,
                if_generation_match=0,
            )
            generation = created.generation
        except GCSPreconditionFailed:
            try:
                existing = self.transport.read_object(bucket=self.bucket, name=name)
                generation = existing.generation
            except GCSObjectNotFound as exc:
                raise StorageConflict(
                    "GCS_PRECONDITION_CONFLICT",
                    "Conditional create lost but no winner can be verified",
                ) from exc
        except M1ExecutionError:
            raise
        except Exception as exc:
            raise self._transport_error(
                exc, f"GCS immutable create failed for {name}"
            ) from exc
        try:
            return self._read_and_verify(
                name=name,
                payload=payload,
                metadata=metadata,
                content_type=content_type,
                generation=generation,
            )
        except M1ExecutionError as exc:
            if exc.code in {"GCS_TRANSIENT", "AUTH_CONFIGURATION"}:
                raise
            raise StorageConflict(
                conflict_code, f"Immutable GCS record differs: {name}"
            ) from exc
        except GCSObjectNotFound as exc:
            raise StorageConflict(
                conflict_code, f"Immutable GCS record differs: {name}"
            ) from exc

    def write_request_if_absent(self, request: Mapping[str, Any]) -> int:
        validate_batch_request(request)
        payload = canonical_json_bytes(request)
        metadata = self._record_metadata(
            "batch_request",
            canonical_sha256(request),
            request_digest=str(request["request_digest"]),
        )
        return self._write_immutable(
            name=self._request_name,
            payload=payload,
            metadata=metadata,
            content_type="application/json",
            conflict_code="REQUEST_CONFLICT",
        )

    def load_request(self) -> tuple[dict[str, Any], int]:
        try:
            snapshot = self.transport.read_object(
                bucket=self.bucket, name=self._request_name
            )
            if snapshot.data is None:
                raise ValueError("missing request bytes")
            request = json.loads(snapshot.data.decode("utf-8"))
            validate_batch_request(request)
            metadata = self._record_metadata(
                "batch_request",
                canonical_sha256(request),
                request_digest=str(request["request_digest"]),
            )
            self._read_and_verify(
                name=self._request_name,
                payload=canonical_json_bytes(request),
                metadata=metadata,
                content_type="application/json",
                generation=snapshot.generation,
            )
        except M1ExecutionError as exc:
            if exc.code in {"GCS_TRANSIENT", "AUTH_CONFIGURATION"}:
                raise
            raise M1ExecutionError(
                "REQUEST_RECORD_INVALID",
                "Durable GCS BatchRequest is missing or corrupt",
            ) from exc
        except (
            GCSObjectNotFound,
            GCSPreconditionFailed,
            M0ContractError,
            ValueError,
            UnicodeError,
        ) as exc:
            raise M1ExecutionError(
                "REQUEST_RECORD_INVALID",
                "Durable GCS BatchRequest is missing or corrupt",
            ) from exc
        except Exception as exc:
            raise self._transport_error(
                exc, "Durable GCS BatchRequest read failed"
            ) from exc
        return request, snapshot.generation

    @staticmethod
    def _validate_cost_ledger(state: Mapping[str, Any]) -> None:
        reserved = sum(
            (
                Decimal(str(attempt["cost"]["reserved_usd"]))
                for attempt in state["attempts"]
            ),
            Decimal("0"),
        )
        known = sum(
            (
                Decimal(str(attempt["cost"]["known_actual_usd"]))
                for attempt in state["attempts"]
            ),
            Decimal("0"),
        )
        indeterminate = sum(
            (
                Decimal(str(attempt["cost"]["potentially_charged_usd"]))
                for attempt in state["attempts"]
                if attempt["phase"] == "indeterminate"
            ),
            Decimal("0"),
        )
        cost = state["cost"]
        if (
            reserved != Decimal(str(cost["reserved_usd"]))
            or known != Decimal(str(cost["known_actual_usd"]))
            or indeterminate != Decimal(str(cost["indeterminate_exposure_usd"]))
        ):
            raise M1ExecutionError(
                "COST_LEDGER_MISMATCH",
                "BatchState cost totals do not equal the durable attempt ledger",
            )

    def save_batch_state(
        self, state: Mapping[str, Any], *, expected_version: str | int | None
    ) -> int:
        self._assert_writer()
        validate_batch_state(state)
        self._validate_cost_ledger(state)
        if expected_version is not None and (
            isinstance(expected_version, bool) or not isinstance(expected_version, int)
        ):
            raise StorageConflict(
                "GCS_PRECONDITION_CONFLICT",
                "GCS state version must be an object generation",
            )
        payload = canonical_json_bytes(state)
        digest = hashlib.sha256(payload).hexdigest()
        metadata = self._record_metadata(
            "batch_state",
            digest,
            request_digest=str(state["request_digest"]),
            logical_revision=str(state["revision"]),
        )
        precondition = 0 if expected_version is None else expected_version
        try:
            written = self.transport.write_object(
                bucket=self.bucket,
                name=self._state_name,
                data=payload,
                metadata=metadata,
                content_type="application/json",
                if_generation_match=precondition,
            )
        except GCSPreconditionFailed as exc:
            raise StorageConflict(
                "GCS_PRECONDITION_CONFLICT",
                f"BatchState generation no longer equals {precondition}",
            ) from exc
        except Exception as exc:
            raise self._transport_error(
                exc, "BatchState conditional write failed"
            ) from exc
        try:
            return self._read_and_verify(
                name=self._state_name,
                payload=payload,
                metadata=metadata,
                content_type="application/json",
                generation=written.generation,
            )
        except M1ExecutionError as exc:
            if exc.code == "AUTH_CONFIGURATION":
                raise
            raise M1ExecutionError(
                "GCS_TRANSIENT", "BatchState write could not be synchronously verified"
            ) from exc
        except (GCSObjectNotFound, GCSPreconditionFailed) as exc:
            raise M1ExecutionError(
                "GCS_TRANSIENT", "BatchState write could not be synchronously verified"
            ) from exc

    def load_batch_state(self) -> tuple[dict[str, Any], int]:
        try:
            snapshot = self.transport.read_object(
                bucket=self.bucket, name=self._state_name
            )
            if snapshot.data is None:
                raise ValueError("missing state bytes")
            state = json.loads(snapshot.data.decode("utf-8"))
            validate_batch_state(state)
            self._validate_cost_ledger(state)
            payload = canonical_json_bytes(state)
            metadata = self._record_metadata(
                "batch_state",
                hashlib.sha256(payload).hexdigest(),
                request_digest=str(state["request_digest"]),
                logical_revision=str(state["revision"]),
            )
            self._read_and_verify(
                name=self._state_name,
                payload=payload,
                metadata=metadata,
                content_type="application/json",
                generation=snapshot.generation,
            )
        except M1ExecutionError as exc:
            if exc.code in {"GCS_TRANSIENT", "AUTH_CONFIGURATION"}:
                raise
            raise M1ExecutionError(
                "STATE_RECORD_INVALID", "Durable GCS BatchState is missing or corrupt"
            ) from exc
        except (
            GCSObjectNotFound,
            GCSPreconditionFailed,
            M0ContractError,
            ValueError,
            UnicodeError,
        ) as exc:
            raise M1ExecutionError(
                "STATE_RECORD_INVALID", "Durable GCS BatchState is missing or corrupt"
            ) from exc
        except Exception as exc:
            raise self._transport_error(
                exc, "Durable GCS BatchState read failed"
            ) from exc
        return state, snapshot.generation

    def _blob_name(self, item_id: str, digest: str) -> str:
        return f"{self._prefix}/outputs/{item_id}/{digest}"

    def _blob_metadata(
        self, *, item_id: str, digest: str, size_bytes: int
    ) -> dict[str, str]:
        return {
            "openmontage_schema": "batch-v2-v1",
            "record_type": "content_addressed_blob",
            "project_id": self.project_id,
            "batch_id": self.batch_id,
            "item_id": item_id,
            "client_sha256": digest,
            "size_bytes": str(size_bytes),
            "media_type": "video/mp4",
        }

    def _parse_locator(self, locator: str) -> tuple[str, str]:
        prefix = "gs://"
        if not locator.startswith(prefix) or "?" in locator:
            raise M1ExecutionError(
                "REUSE_RECEIPT_INVALID", "Invalid private GCS locator"
            )
        remainder = locator[len(prefix) :]
        bucket, separator, name = remainder.partition("/")
        if not separator or not name:
            raise M1ExecutionError("REUSE_RECEIPT_INVALID", "Incomplete GCS locator")
        return bucket, name

    def _verified_blob_snapshot(self, receipt: Mapping[str, Any]) -> GCSObjectSnapshot:
        validate_storage_receipt(receipt)
        if receipt["store_type"] != "gcs":
            raise M1ExecutionError(
                "REUSE_RECEIPT_INVALID", "Receipt is not a GCS receipt"
            )
        bucket, name = self._parse_locator(str(receipt["locator"]))
        expected_name = self._blob_name(str(receipt["item_id"]), str(receipt["sha256"]))
        if bucket != self.bucket or name != expected_name:
            raise M1ExecutionError(
                "REUSE_RECEIPT_INVALID",
                "GCS receipt locator is outside the exact batch namespace",
            )
        generation = int(receipt["generation"])
        try:
            snapshot = self.transport.read_object(
                bucket=bucket, name=name, generation=generation
            )
            head = self.transport.head_object(
                bucket=bucket, name=name, generation=generation
            )
        except (GCSObjectNotFound, GCSPreconditionFailed) as exc:
            raise M1ExecutionError(
                "REUSE_RECEIPT_INVALID", "The exact GCS blob generation is unavailable"
            ) from exc
        except M1ExecutionError:
            raise
        except Exception as exc:
            raise self._transport_error(
                exc, "GCS blob verification transport failed"
            ) from exc
        if snapshot.data is None:
            raise M1ExecutionError("REUSE_RECEIPT_INVALID", "GCS blob has no bytes")
        metadata = self._blob_metadata(
            item_id=str(receipt["item_id"]),
            digest=str(receipt["sha256"]),
            size_bytes=int(receipt["size_bytes"]),
        )
        try:
            self._verify_exact_object(
                snapshot,
                head,
                name=name,
                payload=snapshot.data,
                metadata=metadata,
                content_type="video/mp4",
                expected_generation=generation,
            )
        except M1ExecutionError as exc:
            raise M1ExecutionError(
                "REUSE_RECEIPT_INVALID", "GCS object facts differ from the receipt"
            ) from exc
        if (
            hashlib.sha256(snapshot.data).hexdigest() != receipt["sha256"]
            or len(snapshot.data) != receipt["size_bytes"]
            or snapshot.crc32c != receipt["provider_checksum"]["value"]
        ):
            raise M1ExecutionError(
                "REUSE_RECEIPT_INVALID",
                "GCS digest, size, or provider checksum changed",
            )
        return snapshot

    def put_verified_blob(
        self,
        *,
        source: Path,
        logical_path: str,
        batch_id: str,
        item_id: str,
        attempt_id: str,
        output: OutputFacts,
        created_at: str,
    ) -> dict[str, Any]:
        self._assert_writer()
        if batch_id != self.batch_id:
            raise M1ExecutionError("GCS_BLOB_CONFLICT", "Blob batch identity changed")
        actual_digest, actual_size = _digest_file(source)
        if actual_digest != output.sha256 or actual_size != output.size_bytes:
            raise M1ExecutionError(
                "GCS_TRANSIENT", "Staged output changed before synchronous upload"
            )
        payload = source.read_bytes()
        name = self._blob_name(item_id, output.sha256)
        metadata = self._blob_metadata(
            item_id=item_id, digest=output.sha256, size_bytes=output.size_bytes
        )
        try:
            written = self.transport.write_object(
                bucket=self.bucket,
                name=name,
                data=payload,
                metadata=metadata,
                content_type="video/mp4",
                if_generation_match=0,
            )
            generation = written.generation
        except GCSPreconditionFailed:
            try:
                existing = self.transport.read_object(bucket=self.bucket, name=name)
                generation = existing.generation
            except GCSObjectNotFound as exc:
                raise StorageConflict(
                    "GCS_PRECONDITION_CONFLICT",
                    "Blob create race has no verifiable winner",
                ) from exc
        except M1ExecutionError:
            raise
        except Exception as exc:
            raise self._transport_error(exc, "GCS blob upload failed") from exc
        try:
            verified_generation = self._read_and_verify(
                name=name,
                payload=payload,
                metadata=metadata,
                content_type="video/mp4",
                generation=generation,
            )
        except M1ExecutionError as exc:
            if exc.code in {"GCS_TRANSIENT", "AUTH_CONFIGURATION"}:
                raise
            raise StorageConflict(
                "GCS_PRECONDITION_CONFLICT",
                "Existing GCS CAS object differs from staged bytes",
            ) from exc
        except (GCSObjectNotFound, GCSPreconditionFailed) as exc:
            raise StorageConflict(
                "GCS_PRECONDITION_CONFLICT",
                "Existing GCS CAS object differs from staged bytes",
            ) from exc
        receipt = {
            "version": "1.0",
            "receipt_id": f"receipt-{attempt_id}",
            "batch_id": batch_id,
            "item_id": item_id,
            "attempt_id": attempt_id,
            "sha256": output.sha256,
            "size_bytes": output.size_bytes,
            "media_type": "video/mp4",
            "probe": dict(output.probe),
            "store_type": "gcs",
            "logical_path": logical_path,
            "locator": f"gs://{self.bucket}/{name}",
            "generation": verified_generation,
            "provider_checksum": {
                "algorithm": "crc32c",
                "value": crc32c_base64(payload),
            },
            "created_at": created_at,
            "verification": {
                "completed_at": created_at,
                "write_mode": "synchronous",
                "sha256_verified": True,
                "size_verified": True,
                "provider_checksum_verified": True,
                "generation_verified": True,
            },
            "access": "private",
            "encryption": "provider_managed",
        }
        validate_storage_receipt(receipt)
        return receipt

    def get_verified_blob(self, receipt: Mapping[str, Any], destination: Path) -> Path:
        self._assert_writer()
        destination = self._assert_project_scoped_path(Path(destination))
        snapshot = self._verified_blob_snapshot(receipt)
        assert snapshot.data is not None
        try:
            _atomic_write(destination, snapshot.data)
        except OSError as exc:
            raise M1ExecutionError(
                "LOCAL_STORAGE_TRANSIENT",
                "Verified GCS bytes could not be materialized in the project workspace",
            ) from exc
        digest, size = _digest_file(destination)
        if digest != receipt["sha256"] or size != receipt["size_bytes"]:
            raise M1ExecutionError(
                "REUSE_RECEIPT_INVALID", "Downloaded GCS blob failed local verification"
            )
        return destination

    def restore_staged_blob(
        self,
        *,
        destination: Path,
        batch_id: str,
        item_id: str,
        output: OutputFacts,
    ) -> bool:
        """Recover a blob uploaded before a failed state CAS.

        The deterministic object name and the already durable technical-output
        facts are sufficient to discover the object without trusting a loose
        listing or replaying the provider operation.
        """

        self._assert_writer()
        destination = self._assert_project_scoped_path(Path(destination))
        if batch_id != self.batch_id:
            raise M1ExecutionError(
                "REUSE_RECEIPT_INVALID", "Provisional GCS blob batch changed"
            )
        name = self._blob_name(item_id, output.sha256)
        metadata = self._blob_metadata(
            item_id=item_id,
            digest=output.sha256,
            size_bytes=output.size_bytes,
        )
        try:
            snapshot = self.transport.read_object(bucket=self.bucket, name=name)
        except GCSObjectNotFound:
            return False
        except Exception as exc:
            raise self._transport_error(
                exc, "Provisional GCS blob lookup failed"
            ) from exc
        try:
            head = self.transport.head_object(
                bucket=self.bucket,
                name=name,
                generation=snapshot.generation,
            )
            if snapshot.data is None:
                raise M1ExecutionError(
                    "GCS_VERIFICATION_FAILED", "Provisional GCS blob has no bytes"
                )
            self._verify_exact_object(
                snapshot,
                head,
                name=name,
                payload=snapshot.data,
                metadata=metadata,
                content_type="video/mp4",
                expected_generation=snapshot.generation,
            )
            if (
                hashlib.sha256(snapshot.data).hexdigest() != output.sha256
                or len(snapshot.data) != output.size_bytes
            ):
                raise M1ExecutionError(
                    "GCS_VERIFICATION_FAILED",
                    "Provisional GCS blob differs from durable attempt facts",
                )
        except (GCSObjectNotFound, M1ExecutionError) as exc:
            raise StorageConflict(
                "GCS_PRECONDITION_CONFLICT",
                "Provisional content-addressed GCS object is not exactly reusable",
            ) from exc
        except Exception as exc:
            raise self._transport_error(
                exc, "Provisional GCS blob verification failed"
            ) from exc
        try:
            _atomic_write(destination, snapshot.data)
        except OSError as exc:
            raise M1ExecutionError(
                "LOCAL_STORAGE_TRANSIENT",
                "Provisional GCS blob could not be restored to project staging",
            ) from exc
        digest, size = _digest_file(destination)
        if digest != output.sha256 or size != output.size_bytes:
            raise M1ExecutionError(
                "LOCAL_STORAGE_TRANSIENT",
                "Restored project staging bytes failed exact verification",
            )
        return True

    def verify_receipt(
        self,
        receipt: Mapping[str, Any],
        *,
        validator: MediaValidator,
        output_spec: Mapping[str, Any],
    ) -> bool:
        try:
            # Keep the local verification cache deliberately short for Windows
            # MAX_PATH parity; identity remains bound by the full receipt.
            destination = self.run_dir / "verified" / f"{receipt['sha256'][:16]}.mp4"
            self.get_verified_blob(receipt, destination)
            facts = validator.validate(destination, output_spec)
            if (
                facts.sha256 != receipt["sha256"]
                or facts.size_bytes != receipt["size_bytes"]
                or canonical_json_bytes(facts.probe)
                != canonical_json_bytes(receipt["probe"])
            ):
                raise ValueError("media probe changed")
        except M1ExecutionError as exc:
            if exc.code in {
                "GCS_TRANSIENT",
                "AUTH_CONFIGURATION",
                "LOCAL_STORAGE_TRANSIENT",
            }:
                raise
            raise M1ExecutionError(
                "REUSE_RECEIPT_INVALID", "Committed GCS receipt failed verification"
            ) from exc
        except (GCSObjectNotFound, M0ContractError, OSError, ValueError) as exc:
            raise M1ExecutionError(
                "REUSE_RECEIPT_INVALID", "Committed GCS receipt failed verification"
            ) from exc
        return True

    def write_result_if_absent(self, result: Mapping[str, Any]) -> int:
        validate_batch_result(result)
        payload = canonical_json_bytes(result)
        digest = canonical_sha256(result)
        metadata = self._record_metadata(
            "batch_result", digest, request_digest=str(result["request_digest"])
        )
        return self._write_immutable(
            name=self._result_name,
            payload=payload,
            metadata=metadata,
            content_type="application/json",
            conflict_code="RESULT_CONFLICT",
        )

    def load_result(self) -> tuple[dict[str, Any], int] | None:
        try:
            snapshot = self.transport.read_object(
                bucket=self.bucket, name=self._result_name
            )
        except GCSObjectNotFound:
            return None
        except Exception as exc:
            raise self._transport_error(
                exc, "Durable GCS BatchResult read failed"
            ) from exc
        try:
            if snapshot.data is None:
                raise ValueError("missing result bytes")
            result = json.loads(snapshot.data.decode("utf-8"))
            validate_batch_result(result)
            payload = canonical_json_bytes(result)
            metadata = self._record_metadata(
                "batch_result",
                canonical_sha256(result),
                request_digest=str(result["request_digest"]),
            )
            self._read_and_verify(
                name=self._result_name,
                payload=payload,
                metadata=metadata,
                content_type="application/json",
                generation=snapshot.generation,
            )
        except M1ExecutionError as exc:
            if exc.code in {"GCS_TRANSIENT", "AUTH_CONFIGURATION"}:
                raise
            raise M1ExecutionError(
                "RESULT_RECORD_INVALID", "Durable GCS BatchResult is corrupt"
            ) from exc
        except (
            GCSObjectNotFound,
            GCSPreconditionFailed,
            M0ContractError,
            ValueError,
            UnicodeError,
        ) as exc:
            raise M1ExecutionError(
                "RESULT_RECORD_INVALID", "Durable GCS BatchResult is corrupt"
            ) from exc
        return result, snapshot.generation

    def write_ownership_record_if_absent(
        self,
        *,
        kind: str,
        document: Mapping[str, Any],
        digest: str,
    ) -> int:
        self._assert_writer()
        _validate_ownership_record(kind, document, digest)
        directories = {
            "execution_status": "ownership-evidence",
            "resume_authorization": "resume-authorizations",
        }
        directory = directories[kind]
        return self._write_immutable(
            name=f"{self._prefix}/{directory}/{digest}.json",
            payload=canonical_json_bytes(document),
            metadata=self._record_metadata(
                kind, canonical_sha256(document), proof_digest=digest
            ),
            content_type="application/json",
            conflict_code="OWNERSHIP_RECORD_CONFLICT",
        )

    def write_publication_authorization_if_absent(
        self, authorization: Mapping[str, Any]
    ) -> int:
        """Persist one command-bound Human proof before publication claiming."""

        self._assert_writer()
        validate_publication_authorization(authorization)
        digest = str(authorization["authorization_digest"])
        return self._write_immutable(
            name=f"{self._prefix}/publication/authorizations/{digest}.json",
            payload=canonical_json_bytes(authorization),
            metadata=self._record_metadata(
                "publication_authorization",
                canonical_sha256(authorization),
                authorization_digest=digest,
                command_digest=str(authorization["command_digest"]),
            ),
            content_type="application/json",
            conflict_code="PUBLICATION_AUTHORIZATION_CONFLICT",
        )

    def load_publication_authorization(
        self, authorization_digest: str
    ) -> tuple[dict[str, Any], int]:
        """Read one exact immutable publication authorization record."""

        if not isinstance(authorization_digest, str) or not re.fullmatch(
            r"[0-9a-f]{64}", authorization_digest
        ):
            raise M1ExecutionError(
                "PUBLICATION_AUTHORIZATION_INVALID", "Unsafe authorization digest"
            )
        name = f"{self._prefix}/publication/authorizations/{authorization_digest}.json"
        try:
            snapshot = self.transport.read_object(bucket=self.bucket, name=name)
            if snapshot.data is None:
                raise ValueError("missing authorization bytes")
            authorization = json.loads(snapshot.data.decode("utf-8"))
            validate_publication_authorization(authorization)
            if authorization["authorization_digest"] != authorization_digest:
                raise ValueError("authorization digest differs")
            payload = canonical_json_bytes(authorization)
            metadata = self._record_metadata(
                "publication_authorization",
                canonical_sha256(authorization),
                authorization_digest=authorization_digest,
                command_digest=str(authorization["command_digest"]),
            )
            self._read_and_verify(
                name=name,
                payload=payload,
                metadata=metadata,
                content_type="application/json",
                generation=snapshot.generation,
            )
        except (
            GCSObjectNotFound,
            GCSPreconditionFailed,
            M0ContractError,
            ValueError,
        ) as exc:
            raise M1ExecutionError(
                "PUBLICATION_AUTHORIZATION_INVALID",
                "Immutable publication authorization is missing or corrupt",
            ) from exc
        return authorization, snapshot.generation

    def write_publication_command_if_absent(
        self, command: Mapping[str, Any]
    ) -> tuple[int, str]:
        """Create and synchronously verify the immutable Agent command in GCS."""

        self._assert_writer()
        validate_publication_command(command)
        cloud_source = command.get("cloud_source")
        if (
            not isinstance(cloud_source, Mapping)
            or cloud_source.get("bucket") != self.bucket
            or command.get("batch_id") != self.batch_id
            or command.get("project_id") != self.project_id
        ):
            raise M1ExecutionError(
                "PUBLICATION_GCS_AUTHORITY_MISMATCH",
                "PublicationCommand does not bind this exact GCS store",
            )
        payload = canonical_json_bytes(command)
        digest = str(command["command_digest"])
        generation = self._write_immutable(
            name=self.publication_command_object_name(str(command["command_id"])),
            payload=payload,
            metadata=self._record_metadata(
                "publication_command",
                hashlib.sha256(payload).hexdigest(),
                command_digest=digest,
            ),
            content_type="application/json",
            conflict_code="PUBLICATION_COMMAND_CONFLICT",
        )
        return generation, digest

    def load_publication_command(self, command_id: str) -> tuple[dict[str, Any], int]:
        name = self.publication_command_object_name(command_id)
        try:
            snapshot = self.transport.read_object(bucket=self.bucket, name=name)
            if snapshot.data is None:
                raise ValueError("missing publication command bytes")
            command = json.loads(snapshot.data.decode("utf-8"))
            validate_publication_command(command)
            payload = canonical_json_bytes(command)
            metadata = self._record_metadata(
                "publication_command",
                hashlib.sha256(payload).hexdigest(),
                command_digest=str(command["command_digest"]),
            )
            self._read_and_verify(
                name=name,
                payload=payload,
                metadata=metadata,
                content_type="application/json",
                generation=snapshot.generation,
            )
        except M1ExecutionError as exc:
            if exc.code in {"GCS_TRANSIENT", "AUTH_CONFIGURATION"}:
                raise
            raise M1ExecutionError(
                "PUBLICATION_COMMAND_RECORD_INVALID",
                "Durable GCS PublicationCommand is missing or corrupt",
            ) from exc
        except (
            GCSObjectNotFound,
            GCSPreconditionFailed,
            M0ContractError,
            UnicodeError,
            ValueError,
            json.JSONDecodeError,
        ) as exc:
            raise M1ExecutionError(
                "PUBLICATION_COMMAND_RECORD_INVALID",
                "Durable GCS PublicationCommand is missing or corrupt",
            ) from exc
        return command, snapshot.generation

    def load_publication_state(self) -> tuple[dict[str, Any], int] | None:
        name = self.publication_state_object_name
        try:
            snapshot = self.transport.read_object(bucket=self.bucket, name=name)
        except GCSObjectNotFound:
            return None
        except Exception as exc:
            raise self._transport_error(
                exc, "Durable Cloud PublicationState read failed"
            ) from exc
        try:
            if snapshot.data is None:
                raise ValueError("missing publication state bytes")
            state = json.loads(snapshot.data.decode("utf-8"))
            validate_publication_state(state)
            payload = canonical_json_bytes(state)
            metadata = self._record_metadata(
                "publication_state",
                hashlib.sha256(payload).hexdigest(),
                request_digest=str(state["request_digest"]),
                logical_revision=str(state["revision"]),
            )
            self._read_and_verify(
                name=name,
                payload=payload,
                metadata=metadata,
                content_type="application/json",
                generation=snapshot.generation,
            )
        except M1ExecutionError as exc:
            if exc.code in {"GCS_TRANSIENT", "AUTH_CONFIGURATION"}:
                raise
            raise M1ExecutionError(
                "PUBLICATION_STATE_INVALID",
                "Durable Cloud PublicationState is corrupt",
            ) from exc
        except (
            GCSObjectNotFound,
            GCSPreconditionFailed,
            M0ContractError,
            UnicodeError,
            ValueError,
            json.JSONDecodeError,
        ) as exc:
            raise M1ExecutionError(
                "PUBLICATION_STATE_INVALID",
                "Durable Cloud PublicationState is corrupt",
            ) from exc
        return state, snapshot.generation

    def save_publication_state(
        self,
        state: Mapping[str, Any],
        *,
        expected_generation: int | None,
    ) -> int:
        """Generation-CAS one publication owner/state and verify the winner."""

        self._assert_writer()
        validate_publication_state(state)
        if (
            state["project_id"] != self.project_id
            or state["batch_id"] != self.batch_id
            or state["source"]["bucket"] != self.bucket
        ):
            raise M1ExecutionError(
                "PUBLICATION_GCS_AUTHORITY_MISMATCH",
                "PublicationState does not bind this exact GCS store",
            )
        if expected_generation is None:
            if state["revision"] != 0:
                raise StorageConflict(
                    "GCS_PRECONDITION_CONFLICT",
                    "Initial PublicationState must use revision zero",
                )
            precondition = 0
        else:
            if isinstance(expected_generation, bool) or expected_generation < 1:
                raise StorageConflict(
                    "GCS_PRECONDITION_CONFLICT",
                    "PublicationState expected generation must be positive",
                )
            loaded = self.load_publication_state()
            if loaded is None or loaded[1] != expected_generation:
                raise StorageConflict(
                    "GCS_PRECONDITION_CONFLICT",
                    "PublicationState generation changed before CAS",
                )
            if state["revision"] != loaded[0]["revision"] + 1:
                raise StorageConflict(
                    "GCS_PRECONDITION_CONFLICT",
                    "PublicationState revision must increment exactly once",
                )
            precondition = expected_generation
        payload = canonical_json_bytes(state)
        metadata = self._record_metadata(
            "publication_state",
            hashlib.sha256(payload).hexdigest(),
            request_digest=str(state["request_digest"]),
            logical_revision=str(state["revision"]),
        )
        try:
            written = self.transport.write_object(
                bucket=self.bucket,
                name=self.publication_state_object_name,
                data=payload,
                metadata=metadata,
                content_type="application/json",
                if_generation_match=precondition,
            )
        except GCSPreconditionFailed as exc:
            raise StorageConflict(
                "GCS_PRECONDITION_CONFLICT",
                "Cloud publication ownership claim lost its generation CAS",
            ) from exc
        except Exception as exc:
            raise self._transport_error(
                exc, "PublicationState conditional write failed"
            ) from exc
        try:
            return self._read_and_verify(
                name=self.publication_state_object_name,
                payload=payload,
                metadata=metadata,
                content_type="application/json",
                generation=written.generation,
            )
        except (GCSObjectNotFound, GCSPreconditionFailed, M1ExecutionError) as exc:
            raise M1ExecutionError(
                "GCS_TRANSIENT",
                "PublicationState CAS winner could not be synchronously re-read",
            ) from exc

    def read_verified_blob_bytes(self, receipt: Mapping[str, Any]) -> bytes:
        """Read one exact private GCS receipt without touching local canonical state."""

        self._assert_writer()
        snapshot = self._verified_blob_snapshot(receipt)
        if snapshot.data is None:  # pragma: no cover - enforced by helper
            raise M1ExecutionError(
                "GCS_VERIFICATION_FAILED", "Verified GCS receipt returned no bytes"
            )
        return bytes(snapshot.data)

    @staticmethod
    def _workspace_facts(
        *, logical_path: str, name: str, generation: int, payload: bytes
    ) -> dict[str, Any]:
        return {
            "logical_path": logical_path,
            "object_name": name,
            "generation": generation,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "size_bytes": len(payload),
            "crc32c": crc32c_base64(payload),
        }

    def read_workspace_asset_bytes(
        self,
        *,
        facts: Mapping[str, Any],
        receipt: Mapping[str, Any],
    ) -> bytes:
        """Download one completed canonical asset by exact immutable facts."""

        self._assert_writer()
        validate_storage_receipt(receipt)
        logical_path = validate_canonical_asset_path(
            str(facts.get("logical_path", "")), field="publication asset"
        )
        name = f"projects/{self.project_id}/{logical_path}"
        try:
            snapshot = self.transport.read_object(
                bucket=self.bucket,
                name=name,
                generation=int(facts["generation"]),
            )
        except Exception as exc:
            raise self._transport_error(
                exc, "Completed canonical GCS asset download failed"
            ) from exc
        if snapshot.data is None:
            raise M1ExecutionError(
                "GCS_VERIFICATION_FAILED", "Canonical GCS asset returned no bytes"
            )
        payload = bytes(snapshot.data)
        self.verify_workspace_asset(facts=facts, payload=payload, receipt=receipt)
        return payload

    def materialize_workspace_asset(
        self,
        *,
        facts: Mapping[str, Any],
        receipt: Mapping[str, Any],
        destination: Path,
    ) -> Path:
        """Restore verified canonical GCS bytes only into hidden project staging."""

        self._assert_writer()
        destination = self._assert_project_scoped_path(Path(destination))
        relative = destination.relative_to(self.project_dir)
        if not relative.parts or relative.parts[0] != ".batch-v2":
            raise M1ExecutionError(
                "WORKSPACE_ESCAPE",
                "Cloud recovery download must remain in hidden project staging",
            )
        payload = self.read_workspace_asset_bytes(facts=facts, receipt=receipt)
        destination.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write(destination, payload)
        if _digest_file(destination) != (receipt["sha256"], receipt["size_bytes"]):
            raise M1ExecutionError(
                "GCS_VERIFICATION_FAILED",
                "Recovered canonical asset staging bytes changed",
            )
        return destination

    def publication_checkpoint_snapshot_object_name(self, command_digest: str) -> str:
        if not isinstance(command_digest, str) or not re.fullmatch(
            r"[0-9a-f]{64}", command_digest
        ):
            raise M1ExecutionError(
                "PUBLICATION_COMMAND_DIGEST_MISMATCH",
                "Unsafe publication command digest",
            )
        return f"{self._prefix}/publication/checkpoints/{command_digest}.json"

    def _checkpoint_object_metadata(
        self,
        *,
        record_type: str,
        payload: bytes,
        checkpoint: Mapping[str, Any],
        command: Mapping[str, Any],
        logical_path: str,
    ) -> dict[str, str]:
        return self._record_metadata(
            record_type,
            hashlib.sha256(payload).hexdigest(),
            client_sha256=hashlib.sha256(payload).hexdigest(),
            logical_path=logical_path,
            command_digest=str(command["command_digest"]),
            checkpoint_sha256=canonical_sha256(checkpoint),
            status=str(checkpoint["status"]),
        )

    def _read_command_bound_checkpoint(
        self,
        *,
        name: str,
        generation: int | None,
        record_type: str,
        logical_path: str,
        command: Mapping[str, Any],
        validator: Callable[[Mapping[str, Any]], Any],
    ) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
        try:
            snapshot = self.transport.read_object(
                bucket=self.bucket, name=name, generation=generation
            )
            if snapshot.data is None:
                raise ValueError("missing checkpoint bytes")
            payload = bytes(snapshot.data)
            checkpoint = json.loads(payload.decode("utf-8"))
            validator(checkpoint)
            metadata = self._checkpoint_object_metadata(
                record_type=record_type,
                payload=payload,
                checkpoint=checkpoint,
                command=command,
                logical_path=logical_path,
            )
            self._read_and_verify(
                name=name,
                payload=payload,
                metadata=metadata,
                content_type="application/json",
                generation=snapshot.generation,
            )
        except (GCSObjectNotFound, GCSPreconditionFailed, M1ExecutionError):
            raise
        except Exception as exc:
            raise M1ExecutionError(
                "GCS_VERIFICATION_FAILED",
                "Command-bound checkpoint object is missing, corrupt, or mismatched",
            ) from exc
        return (
            self._workspace_facts(
                logical_path=logical_path,
                name=name,
                generation=snapshot.generation,
                payload=payload,
            ),
            payload,
            checkpoint,
        )

    def publish_publication_checkpoint_snapshot(
        self,
        *,
        source: Path,
        checkpoint: Mapping[str, Any],
        command: Mapping[str, Any],
        validator: Callable[[Mapping[str, Any]], Any],
    ) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
        """Freeze one per-command checkpoint image for recovery/convergence."""

        self._assert_writer()
        payload = Path(source).read_bytes()
        validator(checkpoint)
        name = self.publication_checkpoint_snapshot_object_name(
            str(command["command_digest"])
        )
        logical_path = (
            f".batch-v2/runs/{self.batch_id}/publication/checkpoints/"
            f"{command['command_digest']}.json"
        )
        metadata = self._checkpoint_object_metadata(
            record_type="publication_checkpoint_snapshot",
            payload=payload,
            checkpoint=checkpoint,
            command=command,
            logical_path=logical_path,
        )
        try:
            written = self.transport.write_object(
                bucket=self.bucket,
                name=name,
                data=payload,
                metadata=metadata,
                content_type="application/json",
                if_generation_match=0,
            )
            generation = written.generation
        except GCSPreconditionFailed:
            generation = None
        except Exception as exc:
            raise self._transport_error(
                exc, "Publication checkpoint snapshot create failed"
            ) from exc
        return self._read_command_bound_checkpoint(
            name=name,
            generation=generation,
            record_type="publication_checkpoint_snapshot",
            logical_path=logical_path,
            command=command,
            validator=validator,
        )

    def read_publication_checkpoint_snapshot(
        self,
        *,
        command: Mapping[str, Any],
        expected_facts: Mapping[str, Any],
        expected_document_sha256: str,
        validator: Callable[[Mapping[str, Any]], Any],
    ) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
        """Read a completed transition's immutable checkpoint image exactly."""

        self._assert_writer()
        name = self.publication_checkpoint_snapshot_object_name(
            str(command["command_digest"])
        )
        logical_path = (
            f".batch-v2/runs/{self.batch_id}/publication/checkpoints/"
            f"{command['command_digest']}.json"
        )
        facts, payload, checkpoint = self._read_command_bound_checkpoint(
            name=name,
            generation=int(expected_facts["generation"]),
            record_type="publication_checkpoint_snapshot",
            logical_path=logical_path,
            command=command,
            validator=validator,
        )
        if (
            canonical_sha256(checkpoint) != expected_document_sha256
            or dict(facts) != dict(expected_facts)
        ):
            raise M1ExecutionError(
                "GCS_VERIFICATION_FAILED",
                "Checkpoint snapshot differs from completed publication facts",
            )
        return facts, payload, checkpoint

    def publish_workspace_asset(
        self,
        *,
        source: Path,
        canonical_path: str,
        receipt: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Conditionally create and synchronously verify one canonical GCS asset."""

        self._assert_writer()
        canonical_path = validate_canonical_asset_path(
            canonical_path, field="canonical_path"
        )
        validate_storage_receipt(receipt)
        if receipt["store_type"] != "gcs":
            raise M1ExecutionError(
                "PUBLICATION_GCS_AUTHORITY_MISMATCH",
                "Canonical GCS publication requires a GCS source receipt",
            )
        expected_source = self.project_dir / Path(*canonical_path.split("/"))
        try:
            resolved_source = Path(source).resolve(strict=True)
        except OSError as exc:
            raise M1ExecutionError(
                "WORKSPACE_ESCAPE", "Canonical GCS source is missing"
            ) from exc
        if os.path.normcase(str(resolved_source)) != os.path.normcase(
            str(expected_source)
        ) or os.path.normcase(str(resolved_source)) != os.path.normcase(
            str(Path(os.path.abspath(source)))
        ):
            raise M1ExecutionError(
                "WORKSPACE_ESCAPE",
                "Canonical GCS source must be the exact unaliased project destination",
            )
        payload = resolved_source.read_bytes()
        if (
            hashlib.sha256(payload).hexdigest() != receipt["sha256"]
            or len(payload) != receipt["size_bytes"]
        ):
            raise M1ExecutionError(
                "GCS_VERIFICATION_FAILED",
                "Canonical source bytes differ from their verified receipt",
            )
        name = f"projects/{self.project_id}/{canonical_path}"
        metadata = self._record_metadata(
            "canonical_asset",
            receipt["sha256"],
            client_sha256=str(receipt["sha256"]),
            logical_path=canonical_path,
            source_receipt_id=str(receipt["receipt_id"]),
            source_generation=str(receipt["generation"]),
        )
        generation = self._write_immutable(
            name=name,
            payload=payload,
            metadata=metadata,
            content_type="video/mp4",
            conflict_code="GCS_PRECONDITION_CONFLICT",
        )
        return self._workspace_facts(
            logical_path=canonical_path,
            name=name,
            generation=generation,
            payload=payload,
        )

    def preflight_workspace_asset(
        self,
        *,
        payload: bytes,
        canonical_path: str,
        receipt: Mapping[str, Any],
    ) -> None:
        """Read-only check that a canonical GCS destination is absent or exact."""

        self._assert_writer()
        canonical_path = validate_canonical_asset_path(
            canonical_path, field="canonical_path"
        )
        validate_storage_receipt(receipt)
        if (
            receipt["store_type"] != "gcs"
            or hashlib.sha256(payload).hexdigest() != receipt["sha256"]
            or len(payload) != receipt["size_bytes"]
        ):
            raise M1ExecutionError(
                "PUBLICATION_GCS_AUTHORITY_MISMATCH",
                "Canonical preflight source differs from its GCS receipt",
            )
        name = f"projects/{self.project_id}/{canonical_path}"
        metadata = self._record_metadata(
            "canonical_asset",
            str(receipt["sha256"]),
            client_sha256=str(receipt["sha256"]),
            logical_path=canonical_path,
            source_receipt_id=str(receipt["receipt_id"]),
            source_generation=str(receipt["generation"]),
        )
        try:
            existing = self.transport.head_object(bucket=self.bucket, name=name)
        except GCSObjectNotFound:
            return
        except Exception as exc:
            raise self._transport_error(
                exc, "Canonical GCS asset preflight failed"
            ) from exc
        try:
            self._read_and_verify(
                name=name,
                payload=payload,
                metadata=metadata,
                content_type="video/mp4",
                generation=existing.generation,
            )
        except (GCSObjectNotFound, GCSPreconditionFailed, M1ExecutionError) as exc:
            raise StorageConflict(
                "GCS_PRECONDITION_CONFLICT",
                "Canonical GCS asset destination already differs",
            ) from exc

    def verify_workspace_asset(
        self,
        *,
        facts: Mapping[str, Any],
        payload: bytes,
        receipt: Mapping[str, Any],
    ) -> None:
        """Re-read an already completed private canonical asset exactly."""

        self._assert_writer()
        validate_storage_receipt(receipt)
        expected_name = f"projects/{self.project_id}/{facts['logical_path']}"
        expected_facts = self._workspace_facts(
            logical_path=str(facts["logical_path"]),
            name=expected_name,
            generation=int(facts["generation"]),
            payload=payload,
        )
        if dict(facts) != expected_facts:
            raise M1ExecutionError(
                "GCS_VERIFICATION_FAILED",
                "Completed canonical asset facts differ from local bytes",
            )
        metadata = self._record_metadata(
            "canonical_asset",
            str(receipt["sha256"]),
            client_sha256=str(receipt["sha256"]),
            logical_path=str(facts["logical_path"]),
            source_receipt_id=str(receipt["receipt_id"]),
            source_generation=str(receipt["generation"]),
        )
        self._read_and_verify(
            name=expected_name,
            payload=payload,
            metadata=metadata,
            content_type="video/mp4",
            generation=int(facts["generation"]),
        )

    def publish_workspace_checkpoint(
        self,
        *,
        source: Path,
        checkpoint: Mapping[str, Any],
        command: Mapping[str, Any],
        expected_generation: int,
        validator: Callable[[Mapping[str, Any]], Any],
    ) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
        """Generation-CAS the official checkpoint, adopting a same-command winner."""

        self._assert_writer()
        if isinstance(expected_generation, bool) or expected_generation < 0:
            raise StorageConflict(
                "GCS_PRECONDITION_CONFLICT", "Invalid checkpoint expected generation"
            )
        expected_source = self.project_dir / "checkpoint_assets.json"
        try:
            resolved_source = Path(source).resolve(strict=True)
        except OSError as exc:
            raise M1ExecutionError(
                "WORKSPACE_ESCAPE", "Canonical checkpoint source is missing"
            ) from exc
        if os.path.normcase(str(resolved_source)) != os.path.normcase(
            str(expected_source)
        ) or os.path.normcase(str(resolved_source)) != os.path.normcase(
            str(Path(os.path.abspath(source)))
        ):
            raise M1ExecutionError(
                "WORKSPACE_ESCAPE",
                "GCS checkpoint source must be the exact unaliased project checkpoint",
            )
        payload = resolved_source.read_bytes()
        name = f"projects/{self.project_id}/checkpoint_assets.json"
        validator(checkpoint)
        metadata = self._checkpoint_object_metadata(
            record_type="canonical_checkpoint",
            payload=payload,
            checkpoint=checkpoint,
            command=command,
            logical_path="checkpoint_assets.json",
        )
        try:
            written = self.transport.write_object(
                bucket=self.bucket,
                name=name,
                data=payload,
                metadata=metadata,
                content_type="application/json",
                if_generation_match=expected_generation,
            )
            generation = written.generation
        except GCSPreconditionFailed:
            generation = None
        except Exception as exc:
            raise self._transport_error(
                exc, "Canonical checkpoint conditional write failed"
            ) from exc
        return self._read_command_bound_checkpoint(
            name=name,
            generation=generation,
            record_type="canonical_checkpoint",
            logical_path="checkpoint_assets.json",
            command=command,
            validator=validator,
        )

    def preflight_workspace_checkpoint_generation(
        self, *, expected_generation: int
    ) -> None:
        """Read-only validation of the next canonical checkpoint CAS base."""

        self._assert_writer()
        if isinstance(expected_generation, bool) or expected_generation < 0:
            raise StorageConflict(
                "GCS_PRECONDITION_CONFLICT", "Invalid checkpoint preflight generation"
            )
        name = f"projects/{self.project_id}/checkpoint_assets.json"
        try:
            current = self.transport.head_object(bucket=self.bucket, name=name)
        except GCSObjectNotFound:
            if expected_generation == 0:
                return
            raise StorageConflict(
                "GCS_PRECONDITION_CONFLICT",
                "Expected canonical GCS checkpoint generation is missing",
            ) from None
        except Exception as exc:
            raise self._transport_error(
                exc, "Canonical GCS checkpoint preflight failed"
            ) from exc
        if expected_generation == 0 or current.generation != expected_generation:
            raise StorageConflict(
                "GCS_PRECONDITION_CONFLICT",
                "Canonical GCS checkpoint generation differs before publication",
            )

    def verify_workspace_checkpoint(
        self,
        *,
        facts: Mapping[str, Any],
        payload: bytes,
        checkpoint: Mapping[str, Any],
        command: Mapping[str, Any],
    ) -> None:
        """Re-read an already completed private canonical checkpoint exactly."""

        self._assert_writer()
        name = f"projects/{self.project_id}/checkpoint_assets.json"
        expected_facts = self._workspace_facts(
            logical_path="checkpoint_assets.json",
            name=name,
            generation=int(facts["generation"]),
            payload=payload,
        )
        if dict(facts) != expected_facts:
            raise M1ExecutionError(
                "GCS_VERIFICATION_FAILED",
                "Completed canonical checkpoint facts differ from local bytes",
            )
        metadata = self._record_metadata(
            "canonical_checkpoint",
            hashlib.sha256(payload).hexdigest(),
            client_sha256=hashlib.sha256(payload).hexdigest(),
            logical_path="checkpoint_assets.json",
            command_digest=str(command["command_digest"]),
            checkpoint_sha256=canonical_sha256(checkpoint),
            status=str(checkpoint["status"]),
        )
        self._read_and_verify(
            name=name,
            payload=payload,
            metadata=metadata,
            content_type="application/json",
            generation=int(facts["generation"]),
        )


__all__ = [
    "GCSObjectNotFound",
    "GCSObjectSnapshot",
    "GCSObjectTransport",
    "GCSPreconditionFailed",
    "GCSStore",
    "GoogleCloudStorageTransport",
    "crc32c_base64",
]
