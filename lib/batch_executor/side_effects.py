"""Scoped hidden-writer suppression and V2 worker filesystem confinement."""

from __future__ import annotations

import contextlib
import contextvars
import _thread
import os
import stat
import sys
import threading
from pathlib import Path
from typing import Iterator

from .errors import WorkerWriteViolation


_WORKER_WRITE_ROOT: contextvars.ContextVar[Path | None] = contextvars.ContextVar(
    "batch_v2_worker_write_root", default=None
)
_HIDDEN_WRITERS_SUPPRESSED: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "batch_v2_hidden_writers_suppressed", default=False
)
_PUBLICATION_SCOPE_ACTIVE: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "batch_v2_publication_scope_active", default=False
)


def hidden_writers_suppressed() -> bool:
    """Return whether the current call is inside a scoped V2 invocation."""

    return _HIDDEN_WRITERS_SUPPRESSED.get()


def assert_publication_invocation_allowed() -> None:
    """Reject canonical publication from a provider worker or nested publisher."""

    if _WORKER_WRITE_ROOT.get() is not None:
        raise WorkerWriteViolation(
            "WORKER_PUBLICATION_FORBIDDEN",
            "Provider workers cannot enter the canonical publication path",
        )
    if _PUBLICATION_SCOPE_ACTIVE.get():
        raise WorkerWriteViolation(
            "NESTED_PUBLICATION_FORBIDDEN",
            "Canonical publication invocations cannot be nested",
        )


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
    lexical = Path(os.path.abspath(candidate))
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise WorkerWriteViolation(
            "WORKER_WRITE_FORBIDDEN",
            f"Worker may write only inside {root}; rejected {resolved}",
        ) from exc
    if os.path.normcase(str(resolved)) != os.path.normcase(str(lexical)):
        raise WorkerWriteViolation(
            "WORKER_ALIAS_FORBIDDEN",
            "Worker write targets may not traverse a symlink or junction",
        )
    if lexical.exists():
        try:
            target_stat = lexical.stat(follow_symlinks=False)
        except OSError as exc:
            raise WorkerWriteViolation(
                "WORKER_WRITE_FORBIDDEN", "Worker write target could not be inspected"
            ) from exc
        if stat.S_ISLNK(target_stat.st_mode):
            raise WorkerWriteViolation(
                "WORKER_SYMLINK_FORBIDDEN", "Worker may not write through a symlink"
            )
        if stat.S_ISREG(target_stat.st_mode) and target_stat.st_nlink > 1:
            raise WorkerWriteViolation(
                "WORKER_HARDLINK_FORBIDDEN",
                "Worker may not write a multiply-linked file",
            )


def _assert_attempt_tree_has_no_aliases(root: Path) -> None:
    """Reject aliases planted in staging before a worker receives control."""

    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            entries = list(os.scandir(directory))
        except OSError as exc:
            raise WorkerWriteViolation(
                "WORKER_ALIAS_FORBIDDEN",
                "Worker attempt staging could not be inspected",
            ) from exc
        for directory_entry in entries:
            entry = Path(directory_entry.path)
            try:
                entry_stat = directory_entry.stat(follow_symlinks=False)
                resolved = entry.resolve(strict=True)
            except OSError as exc:
                raise WorkerWriteViolation(
                    "WORKER_ALIAS_FORBIDDEN",
                    "Worker attempt staging contains an unreadable filesystem alias",
                ) from exc
            lexical = Path(os.path.abspath(entry))
            if stat.S_ISLNK(entry_stat.st_mode) or os.path.normcase(
                str(resolved)
            ) != os.path.normcase(str(lexical)):
                raise WorkerWriteViolation(
                    "WORKER_SYMLINK_FORBIDDEN",
                    "Worker attempt staging may not contain symlinks or junctions",
                )
            if stat.S_ISREG(entry_stat.st_mode) and entry_stat.st_nlink > 1:
                raise WorkerWriteViolation(
                    "WORKER_HARDLINK_FORBIDDEN",
                    "Worker attempt staging contains a multiply-linked file",
                )
            if stat.S_ISDIR(entry_stat.st_mode):
                pending.append(entry)


def _worker_audit_hook(event: str, args: tuple[object, ...]) -> None:
    root = _WORKER_WRITE_ROOT.get()
    if root is None:
        return
    if event == "open" and len(args) >= 3 and _is_write_open(args[1], args[2]):
        _assert_worker_path(args[0], root)
        return
    if event == "os.link":
        raise WorkerWriteViolation(
            "WORKER_HARDLINK_FORBIDDEN",
            "M1 provider workers may not create hard links",
        )
    if event == "os.symlink":
        raise WorkerWriteViolation(
            "WORKER_SYMLINK_FORBIDDEN",
            "M1 provider workers may not create symbolic links or junction aliases",
        )
    if event in {"os.mknod", "os.mkfifo"}:
        raise WorkerWriteViolation(
            "WORKER_SPECIAL_FILE_FORBIDDEN",
            "M1 provider workers may not create special filesystem entries",
        )
    path_positions = {
        "os.remove": (0,),
        "os.rename": (0, 1),
        "os.rmdir": (0,),
        "os.mkdir": (0,),
        "os.chmod": (0,),
        "os.truncate": (0,),
        "os.utime": (0,),
        "os.chown": (0,),
        "os.setxattr": (0,),
        "os.removexattr": (0,),
    }
    for position in path_positions.get(event, ()):
        if position < len(args):
            _assert_worker_path(args[position], root)
    if event in {"subprocess.Popen", "os.system"}:
        raise WorkerWriteViolation(
            "WORKER_WRITE_FORBIDDEN",
            "M1 provider workers may not launch an unconfined subprocess",
        )


sys.addaudithook(_worker_audit_hook)


_ORIGINAL_THREAD_START = threading.Thread.start
_ORIGINAL_LOW_LEVEL_THREAD_START = _thread.start_new_thread


def _guarded_thread_start(thread: threading.Thread, *args, **kwargs):
    if _WORKER_WRITE_ROOT.get() is not None:
        raise WorkerWriteViolation(
            "WORKER_NESTED_THREAD_FORBIDDEN",
            "M1 provider workers may not start nested or helper threads",
        )
    return _ORIGINAL_THREAD_START(thread, *args, **kwargs)


def _guarded_low_level_thread_start(function, args, kwargs=None):
    if _WORKER_WRITE_ROOT.get() is not None:
        raise WorkerWriteViolation(
            "WORKER_NESTED_THREAD_FORBIDDEN",
            "M1 provider workers may not start low-level helper threads",
        )
    if kwargs is None:
        return _ORIGINAL_LOW_LEVEL_THREAD_START(function, args)
    return _ORIGINAL_LOW_LEVEL_THREAD_START(function, args, kwargs)


threading.Thread.start = _guarded_thread_start
_thread.start_new_thread = _guarded_low_level_thread_start
threading._start_new_thread = _guarded_low_level_thread_start


@contextlib.contextmanager
def worker_execution_scope(attempt_dir: str | Path) -> Iterator[None]:
    """Suppress hidden writers and confine this worker to one attempt directory."""

    root = Path(attempt_dir).resolve(strict=True)
    _assert_attempt_tree_has_no_aliases(root)
    root_token = _WORKER_WRITE_ROOT.set(root)
    hidden_token = _HIDDEN_WRITERS_SUPPRESSED.set(True)
    try:
        yield
    finally:
        _HIDDEN_WRITERS_SUPPRESSED.reset(hidden_token)
        _WORKER_WRITE_ROOT.reset(root_token)


@contextlib.contextmanager
def publication_execution_scope() -> Iterator[None]:
    """Suppress legacy writers only for one sequential V2 publication call."""

    assert_publication_invocation_allowed()
    publication_token = _PUBLICATION_SCOPE_ACTIVE.set(True)
    hidden_token = _HIDDEN_WRITERS_SUPPRESSED.set(True)
    try:
        yield
    finally:
        _HIDDEN_WRITERS_SUPPRESSED.reset(hidden_token)
        _PUBLICATION_SCOPE_ACTIVE.reset(publication_token)


__all__ = [
    "assert_publication_invocation_allowed",
    "hidden_writers_suppressed",
    "publication_execution_scope",
    "worker_execution_scope",
]
