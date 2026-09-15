from __future__ import annotations

import json
import subprocess
import sys
import threading
from copy import deepcopy
from pathlib import Path

import pytest

from lib.batch_executor.contracts import canonical_json_bytes, freeze_batch_request
from lib.batch_executor.errors import (
    CoordinatorWriterViolation,
    InjectedCrash,
    LocalRunLocked,
    StorageConflict,
)
from lib.batch_executor.media_validation import DeterministicFakeMediaValidator
from lib.batch_executor.storage import LocalStore
from lib.batch_executor.testing import fake_video_bytes
from tests.batch_executor.test_m0_integrity import _valid_result, _valid_state
from tests.batch_executor.test_m0_workspace import _make_directory_link


def _store(authorized_project, batch_id="batch-001") -> LocalStore:
    return LocalStore(authorized_project["project_dir"], batch_id)


def test_local_store_is_revisioned_immutable_and_content_addressed(
    authorized_project, batch_request
):
    store = _store(authorized_project)
    request_version = store.write_request_if_absent(batch_request)
    assert request_version == batch_request["request_digest"]
    loaded, loaded_version = store.load_request()
    assert loaded == batch_request
    assert loaded_version == request_version

    changed = deepcopy(batch_request)
    changed["created_at"] = "2026-09-14T08:00:01Z"
    changed = freeze_batch_request(changed)
    with pytest.raises(StorageConflict, match="REQUEST_CONFLICT"):
        store.write_request_if_absent(changed)

    output = store.attempt_output_path("item-001", "attempt-000001", "clip.mp4")
    output.parent.mkdir(parents=True)
    output.write_bytes(fake_video_bytes(duration_seconds=8, has_audio=True))
    facts = DeterministicFakeMediaValidator().validate(
        output, batch_request["work_items"][0]["output_spec"]
    )
    receipt = store.put_verified_blob(
        source=output,
        logical_path=output.relative_to(authorized_project["project_dir"]).as_posix(),
        batch_id="batch-001",
        item_id="item-001",
        attempt_id="attempt-000001",
        output=facts,
        created_at="2026-09-14T08:00:02Z",
    )
    assert receipt["locator"] == (
        f".batch-v2/blobs/sha256/{facts.sha256[:2]}/{facts.sha256}"
    )
    blob = authorized_project["project_dir"] / Path(receipt["locator"])
    assert blob.read_bytes() == output.read_bytes()
    assert store.verify_receipt(
        receipt,
        validator=DeterministicFakeMediaValidator(),
        output_spec=batch_request["work_items"][0]["output_spec"],
    )


def test_local_state_compare_and_swap_and_coordinator_writer_guard(
    authorized_project, batch_request
):
    store = _store(authorized_project)
    state = _valid_state()
    state["revision"] = 0
    state["owner"]["state_revision"] = 0
    assert store.save_batch_state(state, expected_version=None) == 0
    with pytest.raises(StorageConflict, match="STATE_VERSION_CONFLICT"):
        changed = deepcopy(state)
        changed["revision"] = 1
        changed["owner"]["state_revision"] = 1
        store.save_batch_state(changed, expected_version=None)
    with pytest.raises(StorageConflict, match="STATE_VERSION_CONFLICT"):
        changed = deepcopy(state)
        changed["revision"] = 2
        changed["owner"]["state_revision"] = 2
        store.save_batch_state(changed, expected_version=1)

    caught = []

    def worker():
        try:
            store.write_request_if_absent(batch_request)
        except BaseException as exc:  # pragma: no branch - asserted below
            caught.append(exc)

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()
    assert len(caught) == 1
    assert isinstance(caught[0], CoordinatorWriterViolation)


def test_local_store_rejects_cost_totals_that_disagree_with_attempt_journal(
    authorized_project
):
    store = _store(authorized_project)
    state = _valid_state()
    state["revision"] = 0
    state["owner"]["state_revision"] = 0
    state["cost"]["known_actual_usd"] = 0
    with pytest.raises(Exception, match="COST_LEDGER_MISMATCH"):
        store.save_batch_state(state, expected_version=None)


def test_local_run_lock_is_os_level_and_rejects_another_process(authorized_project):
    store = _store(authorized_project)
    with store.acquire_run_lock():
        with pytest.raises(LocalRunLocked, match="LOCAL_RUN_LOCKED"):
            with store.acquire_run_lock():
                pass

        code = (
            "from pathlib import Path; "
            "from lib.batch_executor.storage import LocalStore; "
            "from lib.batch_executor.errors import LocalRunLocked; "
            f"s=LocalStore(Path({str(authorized_project['project_dir'])!r}), 'batch-001'); "
            "\ntry:\n s.acquire_run_lock().__enter__()\nexcept LocalRunLocked:\n raise SystemExit(23)\n"
        )
        completed = subprocess.run(
            [sys.executable, "-c", code],
            cwd=Path(__file__).resolve().parents[2],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 23, completed.stderr


def test_request_and_result_files_are_canonical_json(authorized_project, batch_request):
    store = _store(authorized_project)
    store.write_request_if_absent(batch_request)
    raw = store.request_path.read_bytes()
    assert raw == canonical_json_bytes(json.loads(raw))


def test_immutable_record_publish_recovers_from_an_orphaned_fsynced_temp(
    authorized_project, batch_request
):
    observed = []

    def interrupt(final_path, temporary_path):
        observed.append((final_path, temporary_path))
        raise InjectedCrash("immutable_temp_fsynced")

    interrupted = LocalStore(
        authorized_project["project_dir"],
        batch_request["batch_id"],
        immutable_publish_hook=interrupt,
    )
    with pytest.raises(InjectedCrash, match="immutable_temp_fsynced"):
        interrupted.write_request_if_absent(batch_request)

    assert len(observed) == 1
    final_path, temporary_path = observed[0]
    assert final_path == interrupted.request_path
    assert not final_path.exists()
    assert temporary_path.is_file()
    assert temporary_path.read_bytes() == canonical_json_bytes(batch_request)

    recovered = _store(authorized_project)
    recovered.write_request_if_absent(batch_request)
    assert recovered.request_path.read_bytes() == canonical_json_bytes(batch_request)
    assert not list(recovered.request_path.parent.glob(".request.json.*.tmp"))


def test_immutable_record_never_overwrites_a_partial_final_file(
    authorized_project, batch_request
):
    store = _store(authorized_project)
    store.request_path.parent.mkdir(parents=True, exist_ok=True)
    store.request_path.write_bytes(b'{"version":')

    with pytest.raises(StorageConflict, match="REQUEST_CONFLICT"):
        store.write_request_if_absent(batch_request)

    assert store.request_path.read_bytes() == b'{"version":'


def test_result_immutable_publish_recovers_from_interrupted_temp(
    authorized_project,
):
    result = _valid_result()

    def interrupt(final_path, temporary_path):
        if final_path.name == "result.json":
            raise InjectedCrash("result_immutable_temp_fsynced")

    interrupted = LocalStore(
        authorized_project["project_dir"],
        result["batch_id"],
        immutable_publish_hook=interrupt,
    )
    with pytest.raises(InjectedCrash, match="result_immutable_temp_fsynced"):
        interrupted.write_result_if_absent(result)
    assert not interrupted.result_path.exists()
    assert list(interrupted.result_path.parent.glob(".result.json.*.tmp"))

    recovered = _store(authorized_project)
    recovered.write_result_if_absent(result)
    assert recovered.load_result()[0] == result
    assert not list(recovered.result_path.parent.glob(".*.tmp"))


def test_attempt_journal_recovers_after_state_wins_then_publish_is_interrupted(
    authorized_project,
):
    state = _valid_state()
    state["revision"] = 0
    state["owner"]["state_revision"] = 0

    def interrupt(final_path, temporary_path):
        if "attempt-journal" in final_path.parts:
            raise InjectedCrash("attempt_journal_temp_fsynced")

    interrupted = LocalStore(
        authorized_project["project_dir"],
        state["batch_id"],
        immutable_publish_hook=interrupt,
    )
    with pytest.raises(InjectedCrash, match="attempt_journal_temp_fsynced"):
        interrupted.save_batch_state(state, expected_version=None)
    loaded, version = interrupted.load_batch_state()
    assert loaded == state
    assert version == 0
    journal_dir = interrupted.run_dir / "attempt-journal" / "item-001" / "attempt-001"
    assert list(journal_dir.glob(".state-00000000.json.*.tmp"))

    recovered = _store(authorized_project)
    next_state = deepcopy(state)
    next_state["revision"] = 1
    next_state["owner"]["state_revision"] = 1
    next_state["updated_at"] = "2026-09-14T08:02:03Z"
    recovered.save_batch_state(next_state, expected_version=0)

    assert not list(journal_dir.glob(".*.tmp"))
    assert (journal_dir / "state-00000001.json").is_file()


def test_local_store_rejects_blob_namespace_symlink_or_junction(
    authorized_project, tmp_path
):
    project = authorized_project["project_dir"]
    batch_root = project / ".batch-v2"
    batch_root.mkdir()
    outside = tmp_path / "outside-blobs"
    outside.mkdir()
    link = batch_root / "blobs"
    is_junction = _make_directory_link(link, outside)
    try:
        with pytest.raises(Exception, match="WORKSPACE_(ALIAS|ESCAPE)"):
            LocalStore(project, "batch-001")
    finally:
        if is_junction and link.exists():
            import os

            os.rmdir(link)
