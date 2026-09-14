"""Project-scoped durable LocalStore for the M1 executor."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import threading
from decimal import Decimal
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

from .contracts import (
    M0ContractError,
    canonical_json_bytes,
    canonical_sha256,
    derive_attempt_output_path,
    validate_batch_request,
    validate_batch_result,
    validate_batch_state,
    validate_storage_receipt,
)
from .errors import (
    CoordinatorWriterViolation,
    LocalRunLocked,
    M1ExecutionError,
    StorageConflict,
)
from .media_validation import MediaValidator, OutputFacts


def _digest_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        _fsync_directory(path.parent)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _write_immutable(path: Path, payload: bytes, *, conflict_code: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        if path.read_bytes() != payload:
            raise StorageConflict(conflict_code, f"Immutable record differs: {path}")
        return
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    _fsync_directory(path.parent)


class LocalRunLock:
    """A non-blocking OS-level exclusive lock held for the whole local run."""

    def __init__(self, path: Path):
        self.path = path
        self._handle = None

    def __enter__(self) -> "LocalRunLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle = self.path.open("a+b")
        try:
            if os.name == "nt":
                import msvcrt

                handle.seek(0, os.SEEK_END)
                if handle.tell() == 0:
                    handle.write(b"\0")
                    handle.flush()
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, BlockingIOError) as exc:
            handle.close()
            raise LocalRunLocked(
                "LOCAL_RUN_LOCKED", f"Another coordinator owns {self.path}"
            ) from exc
        self._handle = handle
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        handle = self._handle
        self._handle = None
        if handle is None:
            return
        try:
            if os.name == "nt":
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        finally:
            handle.close()


class LocalStore:
    """Minimal M1 store; every mutating method is coordinator-thread-only."""

    def __init__(self, project_dir: str | Path, batch_id: str):
        self.project_dir = Path(project_dir).resolve(strict=True)
        self.batch_id = batch_id
        self.run_dir = self.project_dir / ".batch-v2" / "runs" / batch_id
        self.blob_root = self.project_dir / ".batch-v2" / "blobs" / "sha256"
        self.request_path = self.run_dir / "request.json"
        self.state_path = self.run_dir / "state.json"
        self.result_path = self.run_dir / "result.json"
        self.lock_path = self.run_dir / "run.lock"
        self._writer_thread_id = threading.get_ident()
        self._journal_digests: dict[str, str] = {}
        self._assert_project_scoped_path(self.run_dir)
        self._assert_project_scoped_path(self.blob_root)

    def _assert_project_scoped_path(self, path: Path) -> Path:
        resolved = path.resolve(strict=False)
        try:
            resolved.relative_to(self.project_dir)
        except ValueError as exc:
            raise M1ExecutionError(
                "WORKSPACE_ESCAPE", f"Batch V2 path escapes project root: {path}"
            ) from exc
        if os.path.normcase(str(resolved)) != os.path.normcase(str(path)):
            raise M1ExecutionError(
                "WORKSPACE_ALIAS", f"Batch V2 path changes identity through an alias: {path}"
            )
        return resolved

    def _assert_writer(self) -> None:
        if threading.get_ident() != self._writer_thread_id:
            raise CoordinatorWriterViolation(
                "COORDINATOR_WRITER_REQUIRED",
                "Only the coordinator thread may mutate LocalStore",
            )

    def acquire_run_lock(self) -> LocalRunLock:
        self._assert_writer()
        return LocalRunLock(self.lock_path)

    def attempt_output_path(
        self, item_id: str, attempt_id: str, output_name: str
    ) -> Path:
        projects_root = self.project_dir.parent
        return derive_attempt_output_path(
            projects_root,
            self.project_dir.name,
            self.batch_id,
            item_id,
            attempt_id,
            output_name,
        )

    def prepare_attempt_directory(self, output_path: Path) -> None:
        self._assert_writer()
        resolved = self._assert_project_scoped_path(output_path.parent)
        expected = self.run_dir / "attempts" / output_path.parent.parent.name / output_path.parent.name
        if os.path.normcase(str(resolved)) != os.path.normcase(str(expected)):
            raise M1ExecutionError(
                "WORKSPACE_ALIAS", "Attempt directory changes identity through an alias"
            )
        output_path.parent.mkdir(parents=True, exist_ok=True)

    def write_request_if_absent(self, request: Mapping[str, Any]) -> str:
        self._assert_writer()
        validate_batch_request(request)
        payload = canonical_json_bytes(request)
        digest = str(request["request_digest"])
        self.run_dir.mkdir(parents=True, exist_ok=True)
        _write_immutable(
            self.request_path, payload, conflict_code="REQUEST_CONFLICT"
        )
        return digest

    def load_request(self) -> tuple[dict[str, Any], str]:
        try:
            request = json.loads(self.request_path.read_text(encoding="utf-8"))
            validate_batch_request(request)
        except (OSError, json.JSONDecodeError, M0ContractError) as exc:
            raise M1ExecutionError(
                "REQUEST_RECORD_INVALID", "Durable BatchRequest is missing or corrupt"
            ) from exc
        return request, str(request["request_digest"])

    def _save_raw_state(
        self, state: Mapping[str, Any], *, expected_version: int | None
    ) -> int:
        self._assert_writer()
        revision = int(state["revision"])
        if self.state_path.exists():
            try:
                current = json.loads(self.state_path.read_text(encoding="utf-8"))
                current_revision = int(current["revision"])
            except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
                raise M1ExecutionError(
                    "STATE_RECORD_INVALID", "Existing BatchState is corrupt"
                ) from exc
            if expected_version is None or current_revision != expected_version:
                raise StorageConflict(
                    "STATE_VERSION_CONFLICT",
                    f"Expected revision {expected_version}, found {current_revision}",
                )
            if revision != expected_version + 1:
                raise StorageConflict(
                    "STATE_VERSION_CONFLICT", "New revision must increment exactly once"
                )
        elif expected_version is not None or revision != 0:
            raise StorageConflict(
                "STATE_VERSION_CONFLICT", "Initial state must be revision zero"
            )
        _atomic_write(self.state_path, canonical_json_bytes(state))
        return revision

    def save_batch_state(
        self, state: Mapping[str, Any], *, expected_version: int | None
    ) -> int:
        self._assert_writer()
        validate_batch_state(state)
        reserved = sum(
            (Decimal(str(attempt["cost"]["reserved_usd"])) for attempt in state["attempts"]),
            Decimal("0"),
        )
        known = sum(
            (Decimal(str(attempt["cost"]["known_actual_usd"])) for attempt in state["attempts"]),
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
        expected = state["cost"]
        if (
            reserved != Decimal(str(expected["reserved_usd"]))
            or known != Decimal(str(expected["known_actual_usd"]))
            or indeterminate != Decimal(str(expected["indeterminate_exposure_usd"]))
        ):
            raise M1ExecutionError(
                "COST_LEDGER_MISMATCH",
                "BatchState cost totals do not equal the durable attempt ledger",
            )
        revision = self._save_raw_state(state, expected_version=expected_version)
        # These immutable files are a rebuildable attempt journal. state.json
        # is the sole authoritative ledger and is always published first.
        for attempt in state["attempts"]:
            attempt_payload = canonical_json_bytes(attempt)
            attempt_digest = hashlib.sha256(attempt_payload).hexdigest()
            if self._journal_digests.get(attempt["attempt_id"]) == attempt_digest:
                continue
            journal_path = (
                self.run_dir
                / "attempt-journal"
                / attempt["item_id"]
                / attempt["attempt_id"]
                / f"state-{revision:08d}.json"
            )
            _write_immutable(
                journal_path,
                attempt_payload,
                conflict_code="ATTEMPT_JOURNAL_CONFLICT",
            )
            self._journal_digests[attempt["attempt_id"]] = attempt_digest
        return revision

    def load_batch_state(self) -> tuple[dict[str, Any], int]:
        try:
            state = json.loads(self.state_path.read_text(encoding="utf-8"))
            validate_batch_state(state)
        except (OSError, json.JSONDecodeError, M0ContractError) as exc:
            raise M1ExecutionError(
                "STATE_RECORD_INVALID", "Durable BatchState is missing or corrupt"
            ) from exc
        return state, int(state["revision"])

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
        actual_sha, actual_size = _digest_file(source)
        if actual_sha != output.sha256 or actual_size != output.size_bytes:
            raise M1ExecutionError(
                "LOCAL_STORAGE_TRANSIENT", "Staged bytes changed before durable commit"
            )
        destination = self.blob_root / output.sha256[:2] / output.sha256
        self._assert_project_scoped_path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            stored_sha, stored_size = _digest_file(destination)
            if stored_sha != output.sha256 or stored_size != output.size_bytes:
                raise StorageConflict(
                    "BLOB_DIGEST_CONFLICT", "Existing content-addressed blob is corrupt"
                )
        else:
            descriptor, temporary = tempfile.mkstemp(
                prefix=f".{output.sha256}.", suffix=".tmp", dir=destination.parent
            )
            os.close(descriptor)
            temporary_path = Path(temporary)
            try:
                with source.open("rb") as source_handle, temporary_path.open("wb") as target:
                    shutil.copyfileobj(source_handle, target)
                    target.flush()
                    os.fsync(target.fileno())
                copied_sha, copied_size = _digest_file(temporary_path)
                if copied_sha != output.sha256 or copied_size != output.size_bytes:
                    raise M1ExecutionError(
                        "LOCAL_STORAGE_TRANSIENT", "Copied blob failed digest verification"
                    )
                os.replace(temporary_path, destination)
                _fsync_directory(destination.parent)
            finally:
                if temporary_path.exists():
                    temporary_path.unlink()
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
            "store_type": "local",
            "logical_path": logical_path,
            "locator": destination.relative_to(self.project_dir).as_posix(),
            "created_at": created_at,
            "verification": {
                "completed_at": created_at,
                "write_mode": "synchronous",
                "sha256_verified": True,
                "size_verified": True,
                "provider_checksum_verified": False,
                "generation_verified": False,
            },
            "access": "private",
            "encryption": "provider_managed",
        }
        validate_storage_receipt(receipt)
        return receipt

    def verify_receipt(
        self,
        receipt: Mapping[str, Any],
        *,
        validator: MediaValidator,
        output_spec: Mapping[str, Any],
    ) -> bool:
        try:
            validate_storage_receipt(receipt)
            relative = PurePosixPath(receipt["locator"])
            expected = PurePosixPath(
                ".batch-v2",
                "blobs",
                "sha256",
                receipt["sha256"][:2],
                receipt["sha256"],
            )
            if relative != expected:
                raise ValueError("receipt locator is not the exact local CAS path")
            blob = (self.project_dir / Path(*relative.parts)).resolve(strict=True)
            blob.relative_to(self.project_dir)
            lexical_blob = self.project_dir / Path(*relative.parts)
            if os.path.normcase(str(blob)) != os.path.normcase(str(lexical_blob)):
                raise ValueError("receipt locator changes identity through an alias")
            digest, size = _digest_file(blob)
            facts = validator.validate(blob, output_spec)
            if (
                digest != receipt["sha256"]
                or size != receipt["size_bytes"]
                or facts.sha256 != receipt["sha256"]
                or facts.size_bytes != receipt["size_bytes"]
                or canonical_json_bytes(facts.probe)
                != canonical_json_bytes(receipt["probe"])
            ):
                raise ValueError("receipt digest, size, or probe differs")
        except (M0ContractError, M1ExecutionError, OSError, ValueError) as exc:
            raise M1ExecutionError(
                "REUSE_RECEIPT_INVALID", "Committed local receipt failed verification"
            ) from exc
        return True

    def write_result_if_absent(self, result: Mapping[str, Any]) -> str:
        self._assert_writer()
        validate_batch_result(result)
        payload = canonical_json_bytes(result)
        digest = canonical_sha256(result)
        _write_immutable(self.result_path, payload, conflict_code="RESULT_CONFLICT")
        return digest

    def load_result(self) -> tuple[dict[str, Any], str] | None:
        if not self.result_path.exists():
            return None
        try:
            result = json.loads(self.result_path.read_text(encoding="utf-8"))
            validate_batch_result(result)
        except (OSError, json.JSONDecodeError, M0ContractError) as exc:
            raise M1ExecutionError(
                "RESULT_RECORD_INVALID", "Durable BatchResult is corrupt"
            ) from exc
        return result, canonical_sha256(result)


__all__ = ["LocalRunLock", "LocalStore"]
