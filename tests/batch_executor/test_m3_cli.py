from __future__ import annotations

import json
import signal
import shutil
import socket
import threading
from copy import deepcopy
from pathlib import Path

import pytest

from lib.batch_executor.cli import RuntimeDependencies, freeze_runtime_config, run_cli
from lib.batch_executor.contracts import canonical_json_bytes, freeze_batch_request
from lib.batch_executor.fake_gcs import FakeGCS
from lib.batch_executor.gcs_storage import GCSObjectSnapshot
from lib.batch_executor.gemini_adapter import freeze_vertex_adapter_config
from lib.batch_executor.identity import ADCContext
from lib.batch_executor.runtime import CloudRunExecutionStatus
from lib.batch_executor.testing import FakeProviderStep, ScriptedFakeProvider


def _request_file(tmp_path, request):
    path = (tmp_path / "request.json").resolve()
    path.write_bytes(canonical_json_bytes(request))
    return str(path)


def _config(
    request,
    authorized_project,
    request_uri,
    *,
    profile="local",
    mode="run",
    invocation_id="cli-invocation-001",
):
    adapter = freeze_vertex_adapter_config(
        {
            "version": "1.0",
            "config_digest": "0" * 64,
            "request_digest": request["request_digest"],
            "batch_id": request["batch_id"],
            "project_id": request["project_id"],
            "identity": deepcopy(request["work_items"][0]["identity"]),
            "vertex_project": "explicit-vertex-project",
            "vertex_location": "global",
        }
    )
    config = {
        "version": "1.0",
        "config_digest": "0" * 64,
        "profile": profile,
        "transport_mode": "offline_fake",
        "projects_root": str(authorized_project["projects_root"].resolve()),
        "request_uri": request_uri,
        "request_digest": request["request_digest"],
        "observed_source_revision": deepcopy(request["source_revision"]),
        "invocation_id": invocation_id,
        "invocation_mode": mode,
        "adapter_config": adapter,
    }
    if profile == "cloud_run":
        snapshot_projects_root = (
            authorized_project["projects_root"].parent
            / f"{authorized_project['projects_root'].name}-input-snapshot-projects"
        ).resolve()
        snapshot_project = snapshot_projects_root / request["project_id"]
        if not snapshot_project.exists():
            shutil.copytree(
                authorized_project["project_dir"],
                snapshot_project,
                ignore=shutil.ignore_patterns(".batch-v2"),
            )
        config["cloud"] = {
            "bucket": "private-batch-bucket",
            "storage_project": "explicit-storage-project",
            "cloud_run_project": "cloud-project",
            "cloud_run_location": "us-central1",
            "cloud_run_job": "batch-v2",
            "input_snapshot_projects_root": str(snapshot_projects_root),
            "input_snapshot_object_prefix": (
                "batch-v2-input-snapshots/sha256/" + "a" * 64
            ),
        }
    return freeze_runtime_config(config)


def _write_config(tmp_path, config):
    path = (tmp_path / "runtime-config.json").resolve()
    path.write_bytes(canonical_json_bytes(config))
    return str(path)


def _cloud_environment(*, execution="execution-001"):
    return {
        "CLOUD_RUN_JOB": "batch-v2",
        "CLOUD_RUN_EXECUTION": execution,
        "CLOUD_RUN_TASK_INDEX": "0",
        "CLOUD_RUN_TASK_COUNT": "1",
        "CLOUD_RUN_TASK_ATTEMPT": "0",
    }


def test_thin_local_fake_cli_completes_and_emits_stable_result_locator(
    batch_request, authorized_project, tmp_path
):
    request_uri = _request_file(tmp_path, batch_request)
    config_path = _write_config(
        tmp_path, _config(batch_request, authorized_project, request_uri)
    )
    emitted = []
    exit_code = run_cli(
        [
            "run",
            "--profile",
            "local",
            "--config",
            config_path,
            "--request-uri",
            request_uri,
        ],
        emit=emitted.append,
    )
    assert exit_code == 0
    summary = json.loads(emitted[-1])
    assert summary["outcome"] == "all_succeeded"
    assert Path(summary["result_locator"]).parts[-5:] == (
        "batch-project",
        ".batch-v2",
        "runs",
        "batch-001",
        "result.json",
    )
    assert (
        authorized_project["project_dir"]
        / ".batch-v2"
        / "runs"
        / "batch-001"
        / "attempts"
        / "item-001"
        / "attempt-000001"
        / "clip.mp4"
    ).is_file()


def test_single_task_cloud_fake_cli_uses_injected_gcs_and_never_resolves_adc_or_network(
    batch_request, authorized_project, tmp_path, monkeypatch
):
    request = deepcopy(batch_request)
    request["execution_policy"]["storage_profile"] = "cloud_run"
    request = freeze_batch_request(request)
    request_uri = _request_file(tmp_path, request)
    config_path = _write_config(
        tmp_path,
        _config(request, authorized_project, request_uri, profile="cloud_run"),
    )
    transport = FakeGCS()

    class ForbiddenADC:
        def resolve(self, *, scopes):
            raise AssertionError("offline fake CLI must not access credentials")

    monkeypatch.setattr(
        socket,
        "create_connection",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("offline fake CLI attempted network access")
        ),
    )

    emitted = []
    exit_code = run_cli(
        [
            "run",
            "--profile",
            "cloud-run",
            "--config",
            config_path,
            "--request-uri",
            request_uri,
        ],
        dependencies=RuntimeDependencies(
            environment=_cloud_environment(),
            credential_resolver=ForbiddenADC(),
            gcs_transport=transport,
        ),
        emit=emitted.append,
    )
    assert exit_code == 0
    summary = json.loads(emitted[-1])
    assert summary == {
        "exit_code": 0,
        "outcome": "all_succeeded",
        "result_locator": (
            "gs://private-batch-bucket/projects/batch-project/.batch-v2/"
            "runs/batch-001/result.json"
        ),
    }
    assert any(
        name.endswith("/result.json")
        for name in transport.object_names("private-batch-bucket")
    )
    assert transport.background_operations == 0


@pytest.mark.parametrize(
    ("provider_step", "cancelled", "expected_exit"),
    [
        (
            FakeProviderStep.error(
                "PROVIDER_PERMANENT_REJECT",
                acceptance="not_accepted",
                retry_action="do_not_retry",
            ),
            False,
            4,
        ),
        (
            FakeProviderStep.error(
                "TIMEOUT_OR_NETWORK_UNKNOWN",
                acceptance="unknown",
                retry_action="mark_indeterminate",
            ),
            False,
            5,
        ),
        (None, True, 6),
    ],
)
def test_cli_maps_durable_failure_indeterminate_and_cancellation_exit_codes(
    provider_step,
    cancelled,
    expected_exit,
    batch_request,
    authorized_project,
    tmp_path,
):
    request_uri = _request_file(tmp_path, batch_request)
    config_path = _write_config(
        tmp_path, _config(batch_request, authorized_project, request_uri)
    )
    provider = ScriptedFakeProvider(
        scripts={"item-001": [provider_step]} if provider_step is not None else None
    )
    cancellation = threading.Event()
    if cancelled:
        cancellation.set()
    emitted = []
    exit_code = run_cli(
        [
            "run",
            "--profile",
            "local",
            "--config",
            config_path,
            "--request-uri",
            request_uri,
        ],
        dependencies=RuntimeDependencies(fake_provider_factory=lambda: provider),
        cancellation=cancellation,
        emit=emitted.append,
    )
    assert exit_code == expected_exit
    assert json.loads(emitted[-1])["exit_code"] == expected_exit
    if cancelled:
        assert provider.calls == []


def test_cli_config_or_command_tamper_fails_before_provider(
    batch_request, authorized_project, tmp_path
):
    request_uri = _request_file(tmp_path, batch_request)
    config = _config(batch_request, authorized_project, request_uri)
    config["request_digest"] = "f" * 64
    config_path = _write_config(tmp_path, config)
    provider = ScriptedFakeProvider()
    emitted = []
    exit_code = run_cli(
        [
            "run",
            "--profile",
            "local",
            "--config",
            config_path,
            "--request-uri",
            request_uri,
        ],
        dependencies=RuntimeDependencies(fake_provider_factory=lambda: provider),
        emit=emitted.append,
    )
    assert exit_code == 2
    assert provider.calls == []
    assert json.loads(emitted[-1])["error_code"] == "ADAPTER_CONFIG_DIGEST_MISMATCH"
    assert str(authorized_project["projects_root"]) not in emitted[-1]


def test_runtime_configuration_digest_failure_uses_preflight_blocker_exit_three(
    batch_request, authorized_project, tmp_path
):
    request_uri = _request_file(tmp_path, batch_request)
    config = _config(batch_request, authorized_project, request_uri)
    config["projects_root"] = str((tmp_path / "different-root").resolve())
    config_path = _write_config(tmp_path, config)
    provider = ScriptedFakeProvider()
    emitted = []
    assert (
        run_cli(
            [
                "run",
                "--profile",
                "local",
                "--config",
                config_path,
                "--request-uri",
                request_uri,
            ],
            dependencies=RuntimeDependencies(fake_provider_factory=lambda: provider),
            emit=emitted.append,
        )
        == 3
    )
    assert provider.calls == []
    assert json.loads(emitted[-1]) == {
        "error_code": "RUNTIME_CONFIG_DIGEST_MISMATCH",
        "exit_code": 3,
    }


def test_portable_request_cannot_be_used_as_a_production_transport_profile(
    batch_request, authorized_project, tmp_path
):
    request = deepcopy(batch_request)
    request["execution_policy"]["storage_profile"] = "portable"
    request = freeze_batch_request(request)
    request_uri = _request_file(tmp_path, request)
    config = _config(request, authorized_project, request_uri)
    config["transport_mode"] = "vertex"
    config = freeze_runtime_config(config)
    config_path = _write_config(tmp_path, config)

    class ForbiddenADC:
        def resolve(self, *, scopes):
            raise AssertionError("portable production request reached credentials")

    emitted = []
    assert (
        run_cli(
            [
                "run",
                "--profile",
                "local",
                "--config",
                config_path,
                "--request-uri",
                request_uri,
            ],
            dependencies=RuntimeDependencies(credential_resolver=ForbiddenADC()),
            emit=emitted.append,
        )
        == 2
    )
    assert json.loads(emitted[-1])["error_code"] == "INVALID_STORAGE_PROFILE"


def test_main_installs_and_restores_signal_handlers_around_shared_cancellation(
    monkeypatch,
):
    installed = {}
    restored = []
    previous = {signal.SIGINT: object(), signal.SIGTERM: object()}

    monkeypatch.setattr(signal, "getsignal", lambda number: previous[number])

    def fake_signal(number, handler):
        if handler is previous[number]:
            restored.append(number)
        else:
            installed[number] = handler

    monkeypatch.setattr(signal, "signal", fake_signal)

    def fake_run_cli(_argv, *, cancellation):
        assert not cancellation.is_set()
        installed[signal.SIGTERM](signal.SIGTERM, None)
        assert cancellation.is_set()
        return 6

    monkeypatch.setattr("lib.batch_executor.cli.run_cli", fake_run_cli)
    from lib.batch_executor.cli import main

    assert main([]) == 6
    assert set(installed) == {signal.SIGINT, signal.SIGTERM}
    assert restored == [signal.SIGINT, signal.SIGTERM]


def test_invalid_cli_shape_uses_contract_exit_without_provider(capsys):
    emitted = []
    assert run_cli([], emit=emitted.append) == 2
    assert json.loads(emitted[-1]) == {
        "error_code": "CLI_ARGUMENT_INVALID",
        "exit_code": 2,
    }
    assert "required" in capsys.readouterr().err


def test_cloud_cli_active_owner_blocks_run_then_control_plane_resume_takes_over(
    batch_request, authorized_project, tmp_path
):
    request = deepcopy(batch_request)
    request["execution_policy"]["storage_profile"] = "cloud_run"
    request = freeze_batch_request(request)
    request_uri = _request_file(tmp_path, request)
    transport = FakeGCS()
    provider = ScriptedFakeProvider()
    injected = False

    def fail_after_initial_state(snapshot: GCSObjectSnapshot):
        nonlocal injected
        if snapshot.name.endswith("/state.json") and not injected:
            injected = True
            raise OSError("process stopped after durable initial owner")

    transport.after_write = fail_after_initial_state
    first_config_path = _write_config(
        tmp_path,
        _config(
            request,
            authorized_project,
            request_uri,
            profile="cloud_run",
            invocation_id="cli-owner-old",
        ),
    )
    first_exit = run_cli(
        [
            "run",
            "--profile",
            "cloud-run",
            "--config",
            first_config_path,
            "--request-uri",
            request_uri,
        ],
        dependencies=RuntimeDependencies(
            environment=_cloud_environment(execution="execution-old"),
            gcs_transport=transport,
            fake_provider_factory=lambda: provider,
        ),
        emit=lambda _line: None,
    )
    assert first_exit == 3
    assert provider.calls == []
    transport.after_write = None

    ordinary_config = _config(
        request,
        authorized_project,
        request_uri,
        profile="cloud_run",
        invocation_id="cli-owner-other",
    )
    ordinary_path = tmp_path / "ordinary-config.json"
    ordinary_path.write_bytes(canonical_json_bytes(ordinary_config))
    ordinary_provider = ScriptedFakeProvider()
    assert (
        run_cli(
            [
                "run",
                "--profile",
                "cloud-run",
                "--config",
                str(ordinary_path.resolve()),
                "--request-uri",
                request_uri,
            ],
            dependencies=RuntimeDependencies(
                environment=_cloud_environment(execution="execution-other"),
                gcs_transport=transport,
                fake_provider_factory=lambda: ordinary_provider,
            ),
            emit=lambda _line: None,
        )
        == 3
    )
    assert ordinary_provider.calls == []

    old_resource = (
        "projects/cloud-project/locations/us-central1/jobs/batch-v2/"
        "executions/execution-old"
    )

    class FakeADC:
        def resolve(self, *, scopes):
            return ADCContext(credentials=object(), detected_project="ignored")

    class FakeStatus:
        def get_execution_status(self, *, credentials, execution_resource):
            assert credentials is not None
            assert execution_resource == old_resource
            return CloudRunExecutionStatus(
                execution_resource=execution_resource,
                terminal_state="terminal",
                observed_at="2026-09-15T01:00:00Z",
            )

    resume_config = _config(
        request,
        authorized_project,
        request_uri,
        profile="cloud_run",
        mode="resume",
        invocation_id="cli-owner-successor",
    )
    resume_path = tmp_path / "resume-config.json"
    resume_path.write_bytes(canonical_json_bytes(resume_config))
    resume_provider = ScriptedFakeProvider()
    resume_emitted = []
    resume_exit = run_cli(
        [
            "resume",
            "--profile",
            "cloud-run",
            "--config",
            str(resume_path.resolve()),
            "--request-uri",
            request_uri,
            "--resume-proof-kind",
            "control-plane",
        ],
        dependencies=RuntimeDependencies(
            environment=_cloud_environment(execution="execution-successor"),
            credential_resolver=FakeADC(),
            gcs_transport=transport,
            cloud_status_transport=FakeStatus(),
            fake_provider_factory=lambda: resume_provider,
        ),
        emit=resume_emitted.append,
    )
    assert resume_exit == 0, resume_emitted
    assert resume_provider.submit_calls == 1
