"""Offline-only Batch V2 coexistence and rollback rehearsal.

Only the verified historical ``main`` AST is compiled to exercise ``--help``
and parser/dispatch wiring. Legacy module top level and production
``process_sequence`` are never executed, so the rehearsal cannot generate
media or write canonical project state.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path
from typing import Any


LEGACY_RUNNER_RELATIVE_PATH = Path("scripts/batch_run_intent_sequences.py")
LEGACY_RUNNER_SHA256 = (
    "1a6d92872ff9f91064b172ebce7e174226ccc4020a261c11b5e31c34f4d4416a"
)


def _compile_legacy_main(source: bytes, filename: str) -> Any:
    """Compile only the verified parser function, never legacy module top level."""
    tree = ast.parse(source.decode("utf-8"), filename=filename)
    matches = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "main"
    ]
    if len(matches) != 1 or isinstance(matches[0], ast.AsyncFunctionDef):
        raise RuntimeError("legacy runner does not have one synchronous main parser")
    parser_module = ast.Module(body=[matches[0]], type_ignores=[])

    def forbidden_dispatch(_sequence: int) -> None:
        raise RuntimeError("production legacy dispatch is disabled in rehearsal")

    namespace: dict[str, Any] = {
        "argparse": argparse,
        "process_sequence": forbidden_dispatch,
    }
    exec(compile(parser_module, filename, "exec"), namespace)
    return namespace["main"]


def _invoke_parser_with_stub(
    main: Any,
    argv: list[str],
) -> tuple[int, list[int], str]:
    calls: list[int] = []

    def process_sequence_stub(sequence: int) -> None:
        calls.append(sequence)

    globals_dict = main.__globals__
    original_process_sequence = globals_dict["process_sequence"]
    original_argv = sys.argv
    output = io.StringIO()
    globals_dict["process_sequence"] = process_sequence_stub
    sys.argv = [str(LEGACY_RUNNER_RELATIVE_PATH), *argv]
    try:
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                main()
            except SystemExit as exc:
                exit_code = int(exc.code or 0)
            else:
                exit_code = 0
    finally:
        sys.argv = original_argv
        globals_dict["process_sequence"] = original_process_sequence
    return exit_code, calls, output.getvalue()


def rehearse_rollback(repository_root: Path) -> dict[str, Any]:
    """Return deterministic proof that V2 remains opt-in beside legacy.

    No sequence body is executed. The only legacy CLI paths exercised are
    parser help and dispatch into an in-memory stub.
    """
    repository_root = repository_root.resolve()
    legacy_runner = repository_root / LEGACY_RUNNER_RELATIVE_PATH
    before = legacy_runner.read_bytes()
    digest = hashlib.sha256(before).hexdigest()
    if digest != LEGACY_RUNNER_SHA256:
        raise RuntimeError("legacy runner differs from the accepted coexistence bytes")

    main = _compile_legacy_main(before, str(LEGACY_RUNNER_RELATIVE_PATH))
    help_exit, help_calls, help_text = _invoke_parser_with_stub(main, ["--help"])
    four_exit, four_calls, _ = _invoke_parser_with_stub(main, ["--seq", "4"])
    all_exit, all_calls, _ = _invoke_parser_with_stub(main, ["--seq", "all"])

    if help_exit != 0 or "--seq" not in help_text or help_calls:
        raise RuntimeError("legacy --help parser rehearsal failed closed")
    if four_exit != 0 or four_calls != [4]:
        raise RuntimeError("legacy single-sequence dispatch stub rehearsal failed")
    if all_exit != 0 or all_calls != [4, 5, 6]:
        raise RuntimeError("legacy all-sequence dispatch stub rehearsal failed")
    if legacy_runner.read_bytes() != before:
        raise RuntimeError("legacy runner changed during the rehearsal")

    legacy_source = before.decode("utf-8")
    v2_entrypoint = repository_root / "scripts" / "batch_execute.py"
    v2_is_opt_in = (
        v2_entrypoint.is_file()
        and "batch_execute" not in legacy_source
        and "batch_executor" not in legacy_source
    )
    if not v2_is_opt_in:
        raise RuntimeError("V2 is not demonstrably separate from the legacy entrypoint")

    return {
        "status": "passed",
        "legacy_runner_sha256": digest,
        "help_exit_code": help_exit,
        "stub_dispatch": {"4": four_calls, "all": all_calls},
        "real_provider_calls": 0,
        "canonical_writes": 0,
        "v2_is_opt_in": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rehearse Batch V2 opt-in rollback without executing media work"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="OpenMontage repository root",
    )
    args = parser.parse_args(argv)
    print(json.dumps(rehearse_rollback(args.repo_root), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
