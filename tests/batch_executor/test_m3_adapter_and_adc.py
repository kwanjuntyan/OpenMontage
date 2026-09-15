from __future__ import annotations

import base64
import socket
import threading
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from lib.batch_executor.contracts import exact_identity
from lib.batch_executor.engine import LocalBatchExecutor
from lib.batch_executor.errors import M1ExecutionError
from lib.batch_executor.gemini_adapter import (
    GeminiOmniVertexAdapter,
    RequestsVertexInteractionsTransport,
    VertexInteractionResponse,
    VertexTransportError,
    freeze_vertex_adapter_config,
)
from lib.batch_executor.identity import ADCContext
from lib.batch_executor.media_validation import (
    DeterministicFakeMediaValidator,
    FFprobeMediaValidator,
)
from lib.batch_executor.runtime import (
    CloudRunADCExecutionStatusVerifier,
    CloudRunEnvironmentIdentityResolver,
    CloudRunExecutionStatus,
    RequestsCloudRunStatusTransport,
)
from lib.batch_executor.storage import LocalStore
from lib.batch_executor.testing import FakeClock, fake_video_bytes
from lib.batch_executor.tool_adapter import ProviderCall, validate_provider_facts


class FakeADCResolver:
    def __init__(self, *, detected_project="ambient-project-that-must-be-ignored"):
        self.context = ADCContext(
            credentials=object(), detected_project=detected_project, source="adc"
        )
        self.calls = []

    def resolve(self, *, scopes):
        self.calls.append(tuple(scopes))
        return self.context


class FakeVertexTransport:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def submit(self, **kwargs):
        self.calls.append(("submit", kwargs))
        if isinstance(self.response, BaseException):
            raise self.response
        return self.response

    def poll(self, **kwargs):
        self.calls.append(("poll", kwargs))
        if isinstance(self.response, BaseException):
            raise self.response
        return self.response


def _config(batch_request, authorized_project, **overrides):
    document = {
        "version": "1.0",
        "config_digest": "0" * 64,
        "request_digest": batch_request["request_digest"],
        "batch_id": batch_request["batch_id"],
        "project_id": authorized_project["project_id"],
        "identity": exact_identity(),
        "vertex_project": "explicit-vertex-project",
        "vertex_location": "global",
    }
    document.update(overrides)
    return freeze_vertex_adapter_config(document)


def _call(store, batch_request, *, kind="submit", operation_id=None, identity=None):
    output = store.attempt_output_path(
        "item-001", "attempt-000001", "clip.mp4"
    )
    store.prepare_attempt_directory(output)
    return ProviderCall(
        kind=kind,
        item_id="item-001",
        attempt_id="attempt-000001",
        identity=identity or exact_identity(),
        inputs=deepcopy(batch_request["work_items"][0]["inputs"]),
        output_path=output,
        idempotency_digest="a" * 64,
        provider_operation_id=operation_id,
    )


def test_exact_vertex_adapter_uses_explicit_project_location_model_and_fake_adc(
    batch_request, authorized_project, monkeypatch
):
    store = LocalStore(authorized_project["project_dir"], batch_request["batch_id"])
    response = VertexInteractionResponse(
        disposition="succeeded",
        observed_identity=exact_identity(),
        output_bytes=b"OPENMONTAGE_FAKE_VIDEO_V1\n"
        b'{"container":"mp4","duration_seconds":8.0,"has_audio":true,"video_codec":"h264"}'
        b"\nFAKE-MEDIA-BYTES",
        provider_operation_id="interaction-001",
        known_actual_usd=0.8,
    )
    transport = FakeVertexTransport(response)
    resolver = FakeADCResolver()
    adapter = GeminiOmniVertexAdapter(
        config=_config(batch_request, authorized_project),
        project_dir=authorized_project["project_dir"],
        credential_resolver=resolver,
        transport=transport,
    )
    monkeypatch.setattr(
        socket,
        "create_connection",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("network forbidden")),
    )

    call = _call(store, batch_request)
    facts = adapter.invoke(call, threading.Event())
    validate_provider_facts(facts, billing_mode="paid", call_kind="submit")
    assert facts.success is True
    assert call.output_path.is_file()
    assert adapter.observation == {
        "identity": exact_identity(),
        "route_binding": "explicit_request",
        "credential_mode": "adc",
        "hidden_writers": "disabled",
        "available": True,
    }
    assert len(resolver.calls) == 1
    kind, kwargs = transport.calls[0]
    assert kind == "submit"
    assert kwargs["project"] == "explicit-vertex-project"
    assert kwargs["location"] == "global"
    assert kwargs["model"] == "gemini-omni-1.1-flash-preview"
    assert kwargs["route"] == "vertex_interactions"
    assert kwargs["credentials"] is resolver.context.credentials
    assert "ambient-project-that-must-be-ignored" not in repr(kwargs)


def test_exact_adapter_fake_transport_runs_only_as_mechanical_shared_engine_worker(
    batch_request,
    authorized_project,
    source_revision,
):
    resolver = FakeADCResolver()
    transport = FakeVertexTransport(
        VertexInteractionResponse(
            disposition="succeeded",
            observed_identity=exact_identity(),
            output_bytes=fake_video_bytes(),
            provider_operation_id="interaction-engine-001",
            known_actual_usd=0.8,
        )
    )
    adapter = GeminiOmniVertexAdapter(
        config=_config(batch_request, authorized_project),
        project_dir=authorized_project["project_dir"],
        credential_resolver=resolver,
        transport=transport,
    )
    result = LocalBatchExecutor(
        projects_root=authorized_project["projects_root"],
        provider=adapter,
        media_validator=DeterministicFakeMediaValidator(),
        clock=FakeClock(),
    ).run(
        batch_request,
        observed_source_revision=source_revision,
        adapter_observation=adapter.observation,
        invocation_id="exact-adapter-engine",
    )
    assert result["outcome"] == "all_succeeded"
    assert result["status"] == "awaiting_agent_review"
    assert len(transport.calls) == 1
    output_path = (
        authorized_project["project_dir"]
        / ".batch-v2"
        / "runs"
        / batch_request["batch_id"]
        / "attempts"
        / "item-001"
        / "attempt-000001"
        / "clip.mp4"
    )
    assert output_path.is_file()
    assert not (authorized_project["project_dir"] / "assets" / "video" / "clip.mp4").exists()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("vertex_project", ""),
        ("vertex_location", "us-central1"),
        ("identity", {**exact_identity(), "model": "fallback-model"}),
        ("identity", {**exact_identity(), "route": "developer_api"}),
    ],
)
def test_adapter_config_rejects_missing_or_drifted_route_before_adc(
    field, value, batch_request, authorized_project
):
    resolver = FakeADCResolver()
    with pytest.raises(Exception):
        GeminiOmniVertexAdapter(
            config=_config(batch_request, authorized_project, **{field: value}),
            project_dir=authorized_project["project_dir"],
            credential_resolver=resolver,
            transport=FakeVertexTransport(None),
        )
    assert resolver.calls == []


def test_adapter_rejects_another_frozen_request_before_resolving_adc(
    batch_request, authorized_project
):
    resolver = FakeADCResolver()
    adapter = GeminiOmniVertexAdapter(
        config=_config(batch_request, authorized_project),
        project_dir=authorized_project["project_dir"],
        credential_resolver=resolver,
        transport=FakeVertexTransport(None),
    )
    changed = deepcopy(batch_request)
    changed["request_digest"] = "f" * 64
    with pytest.raises(Exception, match="ADAPTER_CONFIG_DIGEST_MISMATCH"):
        adapter.qualify_request(changed)
    assert resolver.calls == []


def test_adapter_requires_stored_interaction_for_durable_resume_before_adc(
    batch_request, authorized_project
):
    resolver = FakeADCResolver()
    adapter = GeminiOmniVertexAdapter(
        config=_config(batch_request, authorized_project),
        project_dir=authorized_project["project_dir"],
        credential_resolver=resolver,
        transport=FakeVertexTransport(None),
    )
    changed = deepcopy(batch_request)
    changed["work_items"][0]["inputs"]["store"] = False
    with pytest.raises(Exception, match="store=true"):
        adapter.qualify_request(changed)
    assert resolver.calls == []


def test_adc_resolution_or_refresh_failure_is_known_pre_submit_auth_configuration(
    batch_request, authorized_project
):
    class BrokenResolver:
        def resolve(self, *, scopes):
            raise OSError("local credential details must not escape")

    adapter = GeminiOmniVertexAdapter(
        config=_config(batch_request, authorized_project),
        project_dir=authorized_project["project_dir"],
        credential_resolver=BrokenResolver(),
        transport=FakeVertexTransport(None),
    )
    with pytest.raises(Exception, match="AUTH_CONFIGURATION"):
        adapter.qualify_request(batch_request)

    class BrokenRefreshCredentials:
        valid = False
        token = None

        def refresh(self, _request):
            raise OSError("refresh failed before HTTP transmission")

    kwargs = _vertex_transport_kwargs(batch_request)
    kwargs["credentials"] = BrokenRefreshCredentials()
    transport = RequestsVertexInteractionsTransport()
    with pytest.raises(VertexTransportError) as raised:
        transport.submit(**kwargs)
    assert raised.value.acceptance == "not_accepted"
    assert raised.value.error_class == "AUTH_CONFIGURATION"


def test_observed_model_drift_fails_closed_and_never_writes_output(
    batch_request, authorized_project
):
    store = LocalStore(authorized_project["project_dir"], batch_request["batch_id"])
    response = VertexInteractionResponse(
        disposition="succeeded",
        observed_identity={**exact_identity(), "model": "another-model"},
        output_bytes=b"bytes-that-must-not-be-written",
        provider_operation_id="interaction-001",
        known_actual_usd=0.8,
    )
    resolver = FakeADCResolver()
    adapter = GeminiOmniVertexAdapter(
        config=_config(batch_request, authorized_project),
        project_dir=authorized_project["project_dir"],
        credential_resolver=resolver,
        transport=FakeVertexTransport(response),
    )
    call = _call(store, batch_request)
    with pytest.raises(Exception, match="EXACT_IDENTITY_MISMATCH"):
        adapter.invoke(call, threading.Event())
    assert not call.output_path.exists()


def test_remote_operation_poll_and_unknown_submit_have_non_replayable_typed_actions(
    batch_request, authorized_project
):
    store = LocalStore(authorized_project["project_dir"], batch_request["batch_id"])
    resolver = FakeADCResolver()
    remote = VertexInteractionResponse(
        disposition="remote_pending",
        observed_identity=exact_identity(),
        provider_operation_id="interaction-remote",
        error_class="REMOTE_JOB_RECOVERABLE",
    )
    adapter = GeminiOmniVertexAdapter(
        config=_config(batch_request, authorized_project),
        project_dir=authorized_project["project_dir"],
        credential_resolver=resolver,
        transport=FakeVertexTransport(remote),
    )
    facts = adapter.invoke(_call(store, batch_request), threading.Event())
    assert facts.acceptance == "accepted"
    assert facts.retry_action == "poll_remote_operation"
    assert facts.provider_operation_id == "interaction-remote"

    unknown_adapter = GeminiOmniVertexAdapter(
        config=_config(batch_request, authorized_project),
        project_dir=authorized_project["project_dir"],
        credential_resolver=FakeADCResolver(),
        transport=FakeVertexTransport(
            VertexTransportError(
                "connection ended after request transmission", acceptance="unknown"
            )
        ),
    )
    unknown = unknown_adapter.invoke(_call(store, batch_request), threading.Event())
    assert unknown.acceptance == "unknown"
    assert unknown.retry_action == "mark_indeterminate"
    assert unknown.error_class == "TIMEOUT_OR_NETWORK_UNKNOWN"


def test_adapter_rejects_any_output_path_outside_exact_materialized_attempt(
    batch_request, authorized_project
):
    resolver = FakeADCResolver()
    transport = FakeVertexTransport(
        VertexInteractionResponse(
            disposition="succeeded",
            observed_identity=exact_identity(),
            output_bytes=b"unused",
            provider_operation_id="interaction-001",
        )
    )
    adapter = GeminiOmniVertexAdapter(
        config=_config(batch_request, authorized_project),
        project_dir=authorized_project["project_dir"],
        credential_resolver=resolver,
        transport=transport,
    )
    store = LocalStore(authorized_project["project_dir"], batch_request["batch_id"])
    call = _call(store, batch_request)
    outside = authorized_project["project_dir"] / "assets" / "forbidden.mp4"
    call = ProviderCall(**{**call.__dict__, "output_path": outside})
    with pytest.raises(Exception, match="INVALID_OUTPUT_PATH"):
        adapter.invoke(call, threading.Event())
    assert transport.calls == []
    assert not outside.exists()


class FakeBearerCredentials:
    valid = True
    token = "fake-vertex-adc-token"


class FakeVertexHTTPResponse:
    def __init__(self, status_code, document, *, content=b""):
        self.status_code = status_code
        self.document = document
        self.content = content
        self.headers = {}

    def json(self):
        return deepcopy(self.document)

    def raise_for_status(self):
        if self.status_code >= 400:
            raise OSError("fake HTTP failure")


class FakeVertexHTTPSession:
    def __init__(self, response, *, download=None):
        self.response = response
        self.download = download
        self.calls = []

    def request(self, method, url, *, headers, json, timeout, allow_redirects):
        self.calls.append(
            (
                "interaction",
                method,
                url,
                dict(headers),
                json,
                timeout,
                allow_redirects,
            )
        )
        return self.response

    def get(self, url, *, headers, timeout, allow_redirects=False):
        self.calls.append(
            ("download", url, dict(headers), timeout, allow_redirects)
        )
        if self.download is None:
            raise AssertionError("unexpected media download")
        return self.download


def _vertex_transport_kwargs(batch_request):
    return {
        "credentials": FakeBearerCredentials(),
        "project": "explicit-vertex-project",
        "location": "global",
        "route": "vertex_interactions",
        "model": "gemini-omni-1.1-flash-preview",
        "operation": "text_to_video",
        "inputs": deepcopy(batch_request["work_items"][0]["inputs"]),
        "idempotency_digest": "a" * 64,
        "provider_operation_id": None,
    }


def test_vertex_http_transport_parses_realistic_output_video_without_route_fallback(
    batch_request,
):
    output = b"fake-video"
    response = FakeVertexHTTPResponse(
        200,
        {
            "id": "interaction-001",
            "model": "gemini-omni-1.1-flash-preview",
            "outputVideo": {"data": base64.b64encode(output).decode("ascii")},
        },
    )
    session = FakeVertexHTTPSession(response)
    transport = RequestsVertexInteractionsTransport()
    transport._session = lambda: session
    request_kwargs = _vertex_transport_kwargs(batch_request)
    request_kwargs["inputs"]["duration"] = "7s"
    normalized = transport.submit(**request_kwargs)
    assert normalized.output_bytes == output
    assert normalized.provider_operation_id == "interaction-001"
    assert normalized.observed_identity == exact_identity()
    _, method, url, headers, payload, timeout, allow_redirects = session.calls[0]
    assert method == "POST"
    assert url == (
        "https://aiplatform.googleapis.com/v1beta1/projects/"
        "explicit-vertex-project/locations/global/interactions"
    )
    assert headers["Authorization"] == "Bearer fake-vertex-adc-token"
    assert payload == {
        "model": "gemini-omni-1.1-flash-preview",
        "input": batch_request["work_items"][0]["inputs"]["prompt"],
        "response_format": {
            "type": "video",
            "aspect_ratio": "16:9",
            "duration": "7s",
        },
        "store": True,
    }
    assert timeout == 600
    assert allow_redirects is False


@pytest.mark.parametrize("status_code", [199, 301, 302, 307, 308])
def test_vertex_submit_non_success_with_inline_video_fails_closed(
    status_code, batch_request
):
    response = FakeVertexHTTPResponse(
        status_code,
        {
            "id": "redirect-body-must-not-be-trusted",
            "output_video": {
                "data": base64.b64encode(b"redirect-video-must-not-be-used").decode(
                    "ascii"
                )
            },
        },
    )
    session = FakeVertexHTTPSession(response)
    transport = RequestsVertexInteractionsTransport()
    transport._session = lambda: session

    with pytest.raises(VertexTransportError) as raised:
        transport.submit(**_vertex_transport_kwargs(batch_request))

    assert str(raised.value) == "Vertex returned an unsupported non-2xx response"
    assert raised.value.acceptance == "unknown"
    assert raised.value.error_class == "TIMEOUT_OR_NETWORK_UNKNOWN"
    assert raised.value.provider_operation_id is None
    assert [call[0] for call in session.calls] == ["interaction"]
    assert session.calls[0][-1] is False


@pytest.mark.parametrize("status_code", [199, 301, 302, 307, 308])
def test_vertex_poll_non_success_with_inline_video_preserves_remote_identity(
    status_code, batch_request
):
    response = FakeVertexHTTPResponse(
        status_code,
        {
            "id": "redirect-body-must-not-replace-operation",
            "output_video": {
                "data": base64.b64encode(b"redirect-video-must-not-be-used").decode(
                    "ascii"
                )
            },
        },
    )
    session = FakeVertexHTTPSession(response)
    transport = RequestsVertexInteractionsTransport()
    transport._session = lambda: session
    kwargs = _vertex_transport_kwargs(batch_request)
    kwargs["provider_operation_id"] = "interaction-existing"

    with pytest.raises(VertexTransportError) as raised:
        transport.poll(**kwargs)

    assert str(raised.value) == "Vertex returned an unsupported non-2xx response"
    assert raised.value.acceptance == "accepted"
    assert raised.value.error_class == "REMOTE_JOB_RECOVERABLE"
    assert raised.value.provider_operation_id == "interaction-existing"
    assert [call[0] for call in session.calls] == ["interaction"]
    assert session.calls[0][-1] is False


def test_vertex_http_transport_never_defaults_a_missing_frozen_duration(
    batch_request,
):
    session = FakeVertexHTTPSession(FakeVertexHTTPResponse(500, {}))
    transport = RequestsVertexInteractionsTransport()
    transport._session = lambda: session
    request_kwargs = _vertex_transport_kwargs(batch_request)
    del request_kwargs["inputs"]["duration"]

    with pytest.raises(KeyError, match="duration"):
        transport.submit(**request_kwargs)

    assert session.calls == []


def test_vertex_adapter_rejects_unsafe_remote_operation_identity(
    batch_request, authorized_project
):
    config = _config(batch_request, authorized_project)
    adapter = GeminiOmniVertexAdapter(
        config=config,
        project_dir=authorized_project["project_dir"],
        credential_resolver=FakeADCResolver(),
        transport=FakeVertexTransport(
            VertexInteractionResponse(
                disposition="remote_pending",
                observed_identity=exact_identity(),
                provider_operation_id="interactions/escape?alt=media",
            )
        ),
    )
    store = LocalStore(authorized_project["project_dir"], batch_request["batch_id"])
    call = _call(store, batch_request)
    with pytest.raises(M1ExecutionError, match="unsafe or ambiguous"):
        adapter.invoke(call, threading.Event())

    unsafe_poll = replace(
        call,
        kind="poll",
        provider_operation_id="../another-interaction",
    )
    with pytest.raises(Exception, match="single-segment"):
        adapter.invoke(unsafe_poll, threading.Event())


def test_vertex_media_locator_is_host_restricted_and_preserves_remote_identity(
    batch_request,
):
    response = FakeVertexHTTPResponse(
        200,
        {
            "id": "interaction-accepted",
            "output_video": {"uri": "https://attacker.invalid/steal-token"},
        },
    )
    session = FakeVertexHTTPSession(response)
    transport = RequestsVertexInteractionsTransport()
    transport._session = lambda: session
    with pytest.raises(VertexTransportError) as raised:
        transport.submit(**_vertex_transport_kwargs(batch_request))
    assert raised.value.acceptance == "accepted"
    assert raised.value.provider_operation_id == "interaction-accepted"
    assert [call[0] for call in session.calls] == ["interaction"]


def test_vertex_media_download_is_google_host_bound_and_refuses_redirects(
    batch_request,
):
    response = FakeVertexHTTPResponse(
        200,
        {
            "id": "interaction-download",
            "output_video": {
                "uri": "https://storage.googleapis.com/private/output.mp4"
            },
        },
    )
    session = FakeVertexHTTPSession(
        response,
        download=FakeVertexHTTPResponse(200, {}, content=b"downloaded-video"),
    )
    transport = RequestsVertexInteractionsTransport()
    transport._session = lambda: session
    normalized = transport.submit(**_vertex_transport_kwargs(batch_request))
    assert normalized.output_bytes == b"downloaded-video"
    download = session.calls[1]
    assert download[0] == "download"
    assert download[1] == "https://storage.googleapis.com/private/output.mp4"
    assert download[-1] is False


@pytest.mark.parametrize("status_code", [401, 404, 408, 503])
def test_vertex_poll_http_failures_preserve_accepted_remote_operation(
    status_code, batch_request
):
    response = FakeVertexHTTPResponse(status_code, {})
    session = FakeVertexHTTPSession(response)
    transport = RequestsVertexInteractionsTransport()
    transport._session = lambda: session
    kwargs = _vertex_transport_kwargs(batch_request)
    kwargs["provider_operation_id"] = "interaction-existing"
    with pytest.raises(VertexTransportError) as raised:
        transport.poll(**kwargs)
    assert raised.value.acceptance == "accepted"
    assert raised.value.provider_operation_id == "interaction-existing"


def test_vertex_submit_timeout_is_paid_ambiguous_not_a_generation_retry(
    batch_request,
):
    session = FakeVertexHTTPSession(FakeVertexHTTPResponse(408, {}))
    transport = RequestsVertexInteractionsTransport()
    transport._session = lambda: session
    with pytest.raises(VertexTransportError) as raised:
        transport.submit(**_vertex_transport_kwargs(batch_request))
    assert raised.value.acceptance == "unknown"
    assert raised.value.error_class == "TIMEOUT_OR_NETWORK_UNKNOWN"


def test_ffprobe_validator_uses_argument_array_and_freezes_technical_facts(
    batch_request, tmp_path, monkeypatch
):
    output = tmp_path / "provider-output.mp4"
    output.write_bytes(b"deterministic-real-mp4-placeholder")
    calls = []

    def fake_run(arguments, **kwargs):
        calls.append((arguments, kwargs))
        return SimpleNamespace(
            returncode=0,
            stdout=(
                '{"streams":[{"codec_type":"video","codec_name":"h264"},'
                '{"codec_type":"audio","codec_name":"aac"}],'
                '"format":{"format_name":"mov,mp4,m4a,3gp,3g2,mj2",'
                '"duration":"8.000000"}}'
            ),
        )

    monkeypatch.setattr("lib.batch_executor.media_validation.subprocess.run", fake_run)
    output_spec = batch_request["work_items"][0]["output_spec"] | {"duration": "8s"}
    facts = FFprobeMediaValidator(ffprobe_binary="/opt/ffmpeg/bin/ffprobe").validate(
        output, output_spec
    )
    assert facts.size_bytes == len(output.read_bytes())
    assert facts.probe == {
        "container": "mp4",
        "duration_seconds": 8.0,
        "video_codec": "h264",
        "has_audio": True,
    }
    arguments, kwargs = calls[0]
    assert arguments == [
        "/opt/ffmpeg/bin/ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(output),
    ]
    assert kwargs == {
        "check": False,
        "capture_output": True,
        "text": True,
        "timeout": 30,
    }


def test_ffprobe_validator_fails_closed_on_probe_or_contract_drift(
    batch_request, tmp_path, monkeypatch
):
    output = tmp_path / "provider-output.mp4"
    output.write_bytes(b"bytes")

    def fake_run(_arguments, **_kwargs):
        return SimpleNamespace(
            returncode=0,
            stdout=(
                '{"streams":[{"codec_type":"video","codec_name":"vp9"}],'
                '"format":{"format_name":"webm","duration":"8.0"}}'
            ),
        )

    monkeypatch.setattr("lib.batch_executor.media_validation.subprocess.run", fake_run)
    output_spec = batch_request["work_items"][0]["output_spec"] | {"duration": "8s"}
    with pytest.raises(Exception, match="OUTPUT_TECHNICALLY_INVALID"):
        FFprobeMediaValidator().validate(output, output_spec)


class FakeCloudRunStatusTransport:
    def __init__(self, status):
        self.status = status
        self.calls = []

    def get_execution_status(self, **kwargs):
        self.calls.append(kwargs)
        return self.status


def test_cloud_run_status_verifier_uses_adc_and_exact_recorded_resource(cloud_owner):
    resolver = FakeADCResolver(detected_project="wrong-ambient-project")
    status = CloudRunExecutionStatus(
        execution_resource=cloud_owner["execution_id"],
        terminal_state="terminal",
        observed_at="2026-09-15T00:20:00Z",
    )
    transport = FakeCloudRunStatusTransport(status)
    verifier = CloudRunADCExecutionStatusVerifier(
        cloud_project="p",
        location="r",
        job_name="j",
        credential_resolver=resolver,
        transport=transport,
    )
    evidence = verifier.verify_stopped(cloud_owner)
    assert evidence["execution_resource"] == cloud_owner["execution_id"]
    assert evidence["observed_status"] == "terminal"
    assert transport.calls == [
        {
            "credentials": resolver.context.credentials,
            "execution_resource": cloud_owner["execution_id"],
        }
    ]
    assert "wrong-ambient-project" not in repr(transport.calls)


def test_cloud_status_verifier_fails_closed_on_wrong_resource_or_nonterminal(cloud_owner):
    resolver = FakeADCResolver()
    wrong = deepcopy(cloud_owner)
    wrong["execution_id"] = "projects/other/locations/r/jobs/j/executions/old"
    verifier = CloudRunADCExecutionStatusVerifier(
        cloud_project="p",
        location="r",
        job_name="j",
        credential_resolver=resolver,
        transport=FakeCloudRunStatusTransport(None),
    )
    with pytest.raises(Exception, match="execution resource"):
        verifier.verify_stopped(wrong)
    assert resolver.calls == []

    nonterminal_transport = FakeCloudRunStatusTransport(
        CloudRunExecutionStatus(
            execution_resource=cloud_owner["execution_id"],
            terminal_state=None,
            observed_at="2026-09-15T00:20:00Z",
        )
    )
    verifier = CloudRunADCExecutionStatusVerifier(
        cloud_project="p",
        location="r",
        job_name="j",
        credential_resolver=resolver,
        transport=nonterminal_transport,
    )
    with pytest.raises(Exception, match="not terminal"):
        verifier.verify_stopped(cloud_owner)


def test_cloud_launch_identity_requires_exact_single_task_zero_retry_shape():
    environment = {
        "CLOUD_RUN_JOB": "j",
        "CLOUD_RUN_EXECUTION": "execution-001",
        "CLOUD_RUN_TASK_INDEX": "0",
        "CLOUD_RUN_TASK_COUNT": "1",
        "CLOUD_RUN_TASK_ATTEMPT": "0",
    }
    resolver = CloudRunEnvironmentIdentityResolver(
        cloud_project="p",
        location="r",
        job_name="j",
        environment=environment,
    )
    identity = resolver.resolve(invocation_id="invocation-001", mode="run")
    assert identity.execution_resource == (
        "projects/p/locations/r/jobs/j/executions/execution-001"
    )
    assert identity.task_id == "0"

    for field, invalid in (
        ("CLOUD_RUN_TASK_COUNT", "2"),
        ("CLOUD_RUN_TASK_INDEX", "1"),
        ("CLOUD_RUN_TASK_ATTEMPT", "1"),
        ("CLOUD_RUN_JOB", "other"),
    ):
        changed = {**environment, field: invalid}
        rejected = CloudRunEnvironmentIdentityResolver(
            cloud_project="p",
            location="r",
            job_name="j",
            environment=changed,
        )
        with pytest.raises(Exception, match="task-count=1"):
            rejected.resolve(invocation_id="invocation-001", mode="run")


class FakeRESTCredentials:
    def __init__(self):
        self.calls = []

    def before_request(self, request, method, url, headers):
        self.calls.append((request, method, url))
        headers["Authorization"] = "Bearer fake-adc-token"


class FakeRESTResponse:
    status_code = 200

    def __init__(self, document):
        self.document = document

    def json(self):
        return deepcopy(self.document)


class FakeRESTSession:
    def __init__(self, document):
        self.document = document
        self.calls = []

    def get(self, url, *, headers, timeout, allow_redirects):
        self.calls.append((url, dict(headers), timeout, allow_redirects))
        return FakeRESTResponse(self.document)


def test_cloud_run_rest_transport_only_reads_exact_bound_resource_with_adc(cloud_owner):
    credentials = FakeRESTCredentials()
    session = FakeRESTSession(
        {
            "name": cloud_owner["execution_id"],
            "completionTime": "2026-09-15T00:19:59.125Z",
            "conditions": [{"reason": "Cancelled", "message": "user cancelled"}],
        }
    )
    auth_request = object()
    transport = RequestsCloudRunStatusTransport(
        session=session,
        auth_request_factory=lambda: auth_request,
    )
    status = transport.get_execution_status(
        credentials=credentials,
        execution_resource=cloud_owner["execution_id"],
    )
    expected_url = f"https://run.googleapis.com/v2/{cloud_owner['execution_id']}"
    assert status == CloudRunExecutionStatus(
        execution_resource=cloud_owner["execution_id"],
        terminal_state="cancelled",
        observed_at="2026-09-15T00:19:59.125000Z",
    )
    assert credentials.calls == [(auth_request, "GET", expected_url)]
    assert session.calls == [
        (
            expected_url,
            {"Accept": "application/json", "Authorization": "Bearer fake-adc-token"},
            30,
            False,
        )
    ]


def test_cloud_run_rest_transport_fails_closed_on_wrong_or_nonterminal_resource(
    cloud_owner,
):
    credentials = FakeRESTCredentials()
    wrong = FakeRESTSession(
        {"name": f"{cloud_owner['execution_id']}-other", "completionTime": "2026-09-15T00:20:00Z"}
    )
    with pytest.raises(Exception, match="another execution"):
        RequestsCloudRunStatusTransport(
            session=wrong,
            auth_request_factory=object,
        ).get_execution_status(
            credentials=credentials,
            execution_resource=cloud_owner["execution_id"],
        )

    running = FakeRESTSession({"name": cloud_owner["execution_id"]})
    status = RequestsCloudRunStatusTransport(
        session=running,
        auth_request_factory=object,
        now=lambda: datetime(2026, 9, 15, 0, 20, tzinfo=timezone.utc),
    ).get_execution_status(
        credentials=credentials,
        execution_resource=cloud_owner["execution_id"],
    )
    assert status.terminal_state is None
    assert status.observed_at == "2026-09-15T00:20:00Z"
