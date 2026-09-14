from __future__ import annotations

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
