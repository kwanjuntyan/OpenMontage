from __future__ import annotations

import _thread
import os
from pathlib import Path
import threading

import pytest

from lib.batch_executor.errors import WorkerWriteViolation
from lib.batch_executor.side_effects import worker_execution_scope
from lib.batch_executor.tool_adapter import ProviderCall


def test_worker_scope_allows_only_attempt_staging_writes(authorized_project):
    project = authorized_project["project_dir"]
    allowed = project / ".batch-v2" / "runs" / "batch-001" / "attempts" / "item-001" / "attempt-001"
    allowed.mkdir(parents=True)
    with worker_execution_scope(allowed):
        (allowed / "clip.mp4").write_bytes(b"allowed")
        with pytest.raises(WorkerWriteViolation, match="WORKER_WRITE_FORBIDDEN"):
            (project / "checkpoint_assets.json").write_text("forbidden", encoding="utf-8")
        with pytest.raises(WorkerWriteViolation, match="WORKER_WRITE_FORBIDDEN"):
            (project / "events.jsonl").write_text("forbidden", encoding="utf-8")
        with pytest.raises(WorkerWriteViolation, match="WORKER_WRITE_FORBIDDEN"):
            (
                project
                / ".batch-v2"
                / "runs"
                / "batch-001"
                / "attempt-journal"
                / "item-001.json"
            ).write_text("forbidden", encoding="utf-8")
        with pytest.raises(WorkerWriteViolation, match="WORKER_WRITE_FORBIDDEN"):
            (project / "assets" / "video.mp4").write_bytes(b"forbidden")
    assert not (project / "checkpoint_assets.json").exists()
    assert not (project / "events.jsonl").exists()


def test_basetool_event_and_gcs_hidden_writers_are_suppressed_only_in_worker_scope(
    monkeypatch, authorized_project
):
    from tools.base_tool import BaseTool, ToolResult
    import lib.events
    import lib.gcs_storage

    project = authorized_project["project_dir"]
    output = project / ".batch-v2" / "runs" / "batch-001" / "attempts" / "item-001" / "attempt-001" / "clip.mp4"
    output.parent.mkdir(parents=True)
    events = []
    uploads = []
    monkeypatch.setattr(lib.events, "emit_event", lambda *args: events.append(args))
    monkeypatch.setattr(lib.gcs_storage.gcs_storage, "is_auto_sync_enabled", lambda: True)
    monkeypatch.setattr(
        lib.gcs_storage.gcs_storage,
        "async_upload_single_asset",
        lambda *args, **kwargs: uploads.append((args, kwargs)),
    )

    class DummyTool(BaseTool):
        name = "dummy"

        def execute(self, inputs):
            Path(inputs["output_path"]).write_bytes(b"video")
            return ToolResult(success=True, artifacts=[inputs["output_path"]])

    with worker_execution_scope(output.parent):
        DummyTool().execute({"output_path": str(output)})
    assert events == []
    assert uploads == []


def test_provider_adapter_cannot_escape_staging_even_when_it_tries(
    authorized_project, batch_request
):
    project = authorized_project["project_dir"]
    output = (
        project
        / ".batch-v2"
        / "runs"
        / "batch-001"
        / "attempts"
        / "item-001"
        / "attempt-001"
        / "clip.mp4"
    )
    output.parent.mkdir(parents=True)
    call = ProviderCall(
        kind="submit",
        item_id="item-001",
        attempt_id="attempt-001",
        identity=batch_request["work_items"][0]["identity"],
        inputs=batch_request["work_items"][0]["inputs"],
        output_path=output,
        idempotency_digest="a" * 64,
    )

    class EscapingAdapter:
        def invoke(self, provider_call, cancellation):
            (project / "checkpoint_assets.json").write_text("escape", encoding="utf-8")

    with worker_execution_scope(output.parent):
        with pytest.raises(WorkerWriteViolation, match="WORKER_WRITE_FORBIDDEN"):
            EscapingAdapter().invoke(call, threading.Event())
    assert not (project / "checkpoint_assets.json").exists()


@pytest.mark.parametrize(
    "protected_relative_path",
    [
        "checkpoint_assets.json",
        "artifacts/asset_manifest.json",
        ".batch-v2/runs/batch-001/state.json",
        "events.jsonl",
        "artifacts/cost_log.json",
    ],
)
def test_worker_cannot_cross_bind_protected_files_with_hardlinks(
    authorized_project, protected_relative_path
):
    project = authorized_project["project_dir"]
    allowed = (
        project
        / ".batch-v2"
        / "runs"
        / "batch-001"
        / "attempts"
        / "item-001"
        / "attempt-001"
    )
    allowed.mkdir(parents=True, exist_ok=True)
    protected = project / protected_relative_path
    protected.parent.mkdir(parents=True, exist_ok=True)
    protected.write_text("safe", encoding="utf-8")

    with worker_execution_scope(allowed):
        with pytest.raises(WorkerWriteViolation, match="WORKER_HARDLINK_FORBIDDEN"):
            os.link(protected, allowed / "alias.json")

    assert protected.read_text(encoding="utf-8") == "safe"
    assert not (allowed / "alias.json").exists()


def test_worker_scope_rejects_a_preexisting_hardlink_alias(authorized_project):
    project = authorized_project["project_dir"]
    allowed = (
        project
        / ".batch-v2"
        / "runs"
        / "batch-001"
        / "attempts"
        / "item-001"
        / "attempt-001"
    )
    allowed.mkdir(parents=True, exist_ok=True)
    checkpoint = project / "checkpoint_assets.json"
    checkpoint.write_text("safe", encoding="utf-8")
    alias = allowed / "preexisting-alias.json"
    os.link(checkpoint, alias)

    with pytest.raises(WorkerWriteViolation, match="WORKER_HARDLINK_FORBIDDEN"):
        with worker_execution_scope(allowed):
            alias.write_text("modified", encoding="utf-8")

    assert checkpoint.read_text(encoding="utf-8") == "safe"


def test_worker_cannot_create_symlink_entries(authorized_project):
    project = authorized_project["project_dir"]
    allowed = (
        project
        / ".batch-v2"
        / "runs"
        / "batch-001"
        / "attempts"
        / "item-001"
        / "attempt-001"
    )
    allowed.mkdir(parents=True, exist_ok=True)
    checkpoint = project / "checkpoint_assets.json"
    checkpoint.write_text("safe", encoding="utf-8")

    with worker_execution_scope(allowed):
        with pytest.raises(WorkerWriteViolation, match="WORKER_SYMLINK_FORBIDDEN"):
            os.symlink(checkpoint, allowed / "alias.json")

    assert checkpoint.read_text(encoding="utf-8") == "safe"
    assert not (allowed / "alias.json").exists()


def test_worker_scope_rejects_a_preexisting_symlink_alias(authorized_project):
    project = authorized_project["project_dir"]
    allowed = (
        project
        / ".batch-v2"
        / "runs"
        / "batch-001"
        / "attempts"
        / "item-001"
        / "attempt-001"
    )
    allowed.mkdir(parents=True, exist_ok=True)
    checkpoint = project / "checkpoint_assets.json"
    checkpoint.write_text("safe", encoding="utf-8")
    alias = allowed / "preexisting-symlink.json"
    try:
        os.symlink(checkpoint, alias)
    except OSError as exc:
        pytest.skip(f"Symlink creation is unavailable on this platform: {exc}")

    with pytest.raises(WorkerWriteViolation, match="WORKER_SYMLINK_FORBIDDEN"):
        with worker_execution_scope(allowed):
            alias.write_text("modified", encoding="utf-8")

    assert checkpoint.read_text(encoding="utf-8") == "safe"


def test_worker_cannot_start_a_nested_thread_to_escape_confinement(
    authorized_project,
):
    project = authorized_project["project_dir"]
    allowed = (
        project
        / ".batch-v2"
        / "runs"
        / "batch-001"
        / "attempts"
        / "item-001"
        / "attempt-001"
    )
    allowed.mkdir(parents=True, exist_ok=True)
    checkpoint = project / "checkpoint_assets.json"
    checkpoint.write_text("safe", encoding="utf-8")
    child = threading.Thread(
        target=lambda: checkpoint.write_text("modified", encoding="utf-8")
    )

    with worker_execution_scope(allowed):
        with pytest.raises(
            WorkerWriteViolation, match="WORKER_NESTED_THREAD_FORBIDDEN"
        ):
            child.start()

    assert checkpoint.read_text(encoding="utf-8") == "safe"
    assert not child.is_alive()


def test_worker_cannot_start_a_low_level_helper_thread(authorized_project):
    project = authorized_project["project_dir"]
    allowed = (
        project
        / ".batch-v2"
        / "runs"
        / "batch-001"
        / "attempts"
        / "item-001"
        / "attempt-001"
    )
    allowed.mkdir(parents=True, exist_ok=True)
    checkpoint = project / "checkpoint_assets.json"
    checkpoint.write_text("safe", encoding="utf-8")

    with worker_execution_scope(allowed):
        with pytest.raises(
            WorkerWriteViolation, match="WORKER_NESTED_THREAD_FORBIDDEN"
        ):
            _thread.start_new_thread(
                lambda: checkpoint.write_text("modified", encoding="utf-8"), ()
            )

    assert checkpoint.read_text(encoding="utf-8") == "safe"


def test_worker_guards_are_scoped_and_do_not_break_unscoped_threads(
    authorized_project,
):
    target = authorized_project["project_dir"] / "unscoped-helper-output.txt"
    child = threading.Thread(target=lambda: target.write_text("ok", encoding="utf-8"))
    child.start()
    child.join(timeout=5)

    assert not child.is_alive()
    assert target.read_text(encoding="utf-8") == "ok"
