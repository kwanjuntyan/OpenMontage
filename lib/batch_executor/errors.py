"""Typed failures for the local Batch Executor V2 milestones."""

from __future__ import annotations


class M1ExecutionError(RuntimeError):
    """Base error carrying a stable machine-readable code."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"{code}: {message}")


class StorageConflict(M1ExecutionError):
    """An immutable record or compare-and-swap precondition was violated."""


class LocalRunLocked(M1ExecutionError):
    """Another coordinator process owns the local batch run lock."""


class CoordinatorWriterViolation(M1ExecutionError):
    """A non-coordinator thread attempted a shared durable write."""


class WorkerWriteViolation(M1ExecutionError):
    """A worker attempted to write outside its unique attempt directory."""


class M2PublicationError(M1ExecutionError):
    """A fail-closed canonical publication contract or lifecycle violation."""


class InjectedCrash(M1ExecutionError):
    """Offline crash-injection signal used at durable M1 boundaries."""

    def __init__(self, boundary: str):
        self.boundary = boundary
        super().__init__("INJECTED_CRASH", boundary)


__all__ = [
    "CoordinatorWriterViolation",
    "InjectedCrash",
    "LocalRunLocked",
    "M1ExecutionError",
    "M2PublicationError",
    "StorageConflict",
    "WorkerWriteViolation",
]
