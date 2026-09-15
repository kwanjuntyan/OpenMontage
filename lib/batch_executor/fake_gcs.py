"""Deterministic, thread-safe in-memory GCS transport for offline M3 tests."""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Mapping

from .gcs_storage import (
    GCSObjectNotFound,
    GCSObjectSnapshot,
    GCSPreconditionFailed,
    crc32c_base64,
)


@dataclass
class _StoredObject:
    generation: int
    data: bytes
    metadata: dict[str, str]
    content_type: str
    crc32c: str


class FakeGCS:
    """Implements only the conditional object operations required by GCSStore."""

    def __init__(self):
        self._objects: dict[tuple[str, str], _StoredObject] = {}
        self._next_generation = 1
        self._lock = threading.Lock()
        self.write_calls = 0
        self.read_calls = 0
        self.head_calls = 0
        self.successful_creates = 0
        self.background_operations = 0
        self.before_write = None
        self.after_write = None

    @staticmethod
    def _snapshot(
        bucket: str,
        name: str,
        value: _StoredObject,
        *,
        include_data: bool,
    ) -> GCSObjectSnapshot:
        return GCSObjectSnapshot(
            bucket=bucket,
            name=name,
            generation=value.generation,
            size_bytes=len(value.data),
            crc32c=value.crc32c,
            metadata=dict(value.metadata),
            content_type=value.content_type,
            data=bytes(value.data) if include_data else None,
        )

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
        hook = self.before_write
        if hook is not None:
            hook(bucket, name, if_generation_match)
        with self._lock:
            self.write_calls += 1
            key = (bucket, name)
            current = self._objects.get(key)
            current_generation = 0 if current is None else current.generation
            if current_generation != if_generation_match:
                raise GCSPreconditionFailed(
                    f"expected generation {if_generation_match}, found {current_generation}"
                )
            generation = self._next_generation
            self._next_generation += 1
            value = _StoredObject(
                generation=generation,
                data=bytes(data),
                metadata=dict(metadata),
                content_type=content_type,
                crc32c=crc32c_base64(data),
            )
            self._objects[key] = value
            if if_generation_match == 0:
                self.successful_creates += 1
            snapshot = self._snapshot(bucket, name, value, include_data=False)
        hook = self.after_write
        if hook is not None:
            hook(snapshot)
        return snapshot

    def _load(
        self,
        *,
        bucket: str,
        name: str,
        generation: int | None,
        include_data: bool,
    ) -> GCSObjectSnapshot:
        key = (bucket, name)
        value = self._objects.get(key)
        if value is None or (
            generation is not None and value.generation != generation
        ):
            raise GCSObjectNotFound(f"gs://{bucket}/{name}#{generation or 'latest'}")
        return self._snapshot(bucket, name, value, include_data=include_data)

    def read_object(
        self, *, bucket: str, name: str, generation: int | None = None
    ) -> GCSObjectSnapshot:
        with self._lock:
            self.read_calls += 1
            return self._load(
                bucket=bucket,
                name=name,
                generation=generation,
                include_data=True,
            )

    def head_object(
        self, *, bucket: str, name: str, generation: int | None = None
    ) -> GCSObjectSnapshot:
        with self._lock:
            self.head_calls += 1
            return self._load(
                bucket=bucket,
                name=name,
                generation=generation,
                include_data=False,
            )

    @staticmethod
    def _parse_locator(locator: str) -> tuple[str, str]:
        if not locator.startswith("gs://"):
            raise ValueError(locator)
        bucket, separator, name = locator[5:].partition("/")
        if not separator:
            raise ValueError(locator)
        return bucket, name

    def corrupt(self, locator: str, kind: str) -> None:
        """Mutate fake provider facts to exercise fail-closed verification."""

        bucket, name = self._parse_locator(locator)
        with self._lock:
            value = self._objects[(bucket, name)]
            if kind == "bytes":
                value.data += b"-corrupt"
                value.crc32c = crc32c_base64(value.data)
            elif kind == "checksum":
                value.crc32c = "AAAAAA=="
            elif kind == "metadata":
                value.metadata["client_sha256"] = "f" * 64
            else:
                raise ValueError(f"Unsupported corruption: {kind}")

    def object_names(self, bucket: str) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(name for stored_bucket, name in self._objects if stored_bucket == bucket))


__all__ = ["FakeGCS"]
