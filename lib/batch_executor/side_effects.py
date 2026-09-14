"""Thread-scoped suppression and filesystem confinement for V2 workers."""

from __future__ import annotations

import contextlib
import contextvars
import os
import sys
from pathlib import Path
from typing import Iterator

from .errors import WorkerWriteViolation


_WORKER_WRITE_ROOT: contextvars.ContextVar[Path | None] = contextvars.ContextVar(
    "batch_v2_worker_write_root", default=None
)
_HIDDEN_WRITERS_SUPPRESSED: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "batch_v2_hidden_writers_suppressed", default=False
)


def hidden_writers_suppressed() -> bool:
    """Return whether the current call is inside a V2 worker execution scope."""

    return _HIDDEN_WRITERS_SUPPRESSED.get()


def _is_write_open(mode: object, flags: object) -> bool:
    if isinstance(mode, str) and any(marker in mode for marker in "wax+"):
        return True
    if isinstance(flags, int):
        write_flags = os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC
        return bool(flags & write_flags)
    return False


def _assert_worker_path(path_like: object, root: Path) -> None:
    if isinstance(path_like, int):
        raise WorkerWriteViolation(
            "WORKER_WRITE_FORBIDDEN", "Worker descriptor writes are not permitted"
        )
    try:
        candidate = Path(os.fsdecode(path_like))
    except (TypeError, ValueError, OSError) as exc:
        raise WorkerWriteViolation(
            "WORKER_WRITE_FORBIDDEN", "Worker write target is not a valid path"
        ) from exc
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise WorkerWriteViolation(
            "WORKER_WRITE_FORBIDDEN",
            f"Worker may write only inside {root}; rejected {resolved}",
        ) from exc


def _worker_audit_hook(event: str, args: tuple[object, ...]) -> None:
    root = _WORKER_WRITE_ROOT.get()
    if root is None:
        return
    if event == "open" and len(args) >= 3 and _is_write_open(args[1], args[2]):
        _assert_worker_path(args[0], root)
        return
    path_positions = {
        "os.remove": (0,),
        "os.rename": (0, 1),
        "os.rmdir": (0,),
        "os.mkdir": (0,),
        "os.chmod": (0,),
        "os.truncate": (0,),
        "os.utime": (0,),
    }
    for position in path_positions.get(event, ()):
        if position < len(args):
            _assert_worker_path(args[position], root)
    if event == "subprocess.Popen":
        raise WorkerWriteViolation(
            "WORKER_WRITE_FORBIDDEN",
            "M1 provider workers may not launch an unconfined subprocess",
        )


sys.addaudithook(_worker_audit_hook)


@contextlib.contextmanager
def worker_execution_scope(attempt_dir: str | Path) -> Iterator[None]:
    """Suppress hidden writers and confine this worker to one attempt directory."""

    root = Path(attempt_dir).resolve(strict=True)
    root_token = _WORKER_WRITE_ROOT.set(root)
    hidden_token = _HIDDEN_WRITERS_SUPPRESSED.set(True)
    try:
        yield
    finally:
        _HIDDEN_WRITERS_SUPPRESSED.reset(hidden_token)
        _WORKER_WRITE_ROOT.reset(root_token)


__all__ = ["hidden_writers_suppressed", "worker_execution_scope"]
