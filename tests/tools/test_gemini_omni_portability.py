"""Offline portability and exact-route contracts for Gemini Omni."""

from __future__ import annotations

import base64
from pathlib import Path

import pytest

from tools.base_tool import ToolStatus
from tools.video.gemini_omni_video import (
    GeminiOmniVideo,
    GoogleADCVertexTokenResolver,
)


class FakeResponse:
    def __init__(
        self,
        payload,
        *,
        content=b"",
        ok=True,
        status_code=200,
        text="",
    ):
        self._payload = payload
        self.content = content
        self.ok = ok
        self.status_code = status_code
        self.headers = {}
        self.text = text

    def json(self):
        return self._payload

    def raise_for_status(self):
        return None


class RecordingTransport:
    def __init__(self, *, post_response=None, get_response=None):
        self.posts = []
        self.gets = []
        self._post_response = post_response
        self._get_response = get_response

    def post(self, url, **kwargs):
        self.posts.append((url, kwargs))
        if self._post_response is not None:
            return self._post_response
        inline = base64.b64encode(b"offline mp4").decode("ascii")
        return FakeResponse(
            {"id": "offline-interaction", "output_video": {"data": inline}}
        )

    def get(self, url, **kwargs):
        self.gets.append((url, kwargs))
        if self._get_response is not None:
            return self._get_response
        raise AssertionError("inline fake response must not download")


class ForbiddenResolver:
    def __init__(self):
        self.calls = 0

    def resolve_access_token(self, *, scopes):
        self.calls += 1
        raise AssertionError("credential resolution was not authorized")


class FakeResolver:
    def __init__(self):
        self.calls = []

    def resolve_access_token(self, *, scopes):
        self.calls.append(tuple(scopes))
        return "offline-adc-token"


def test_source_has_no_machine_path_repo_env_dns_patch_or_global_credential_cache():
    source = (
        Path(__file__).resolve().parents[2]
        / "tools"
        / "video"
        / "gemini_omni_video.py"
    ).read_text(encoding="utf-8")
    for forbidden in (
        "D:\\gcp-keys",
        ' / ".env"',
        "GOOGLE_GENAI_USE_VERTEXAI",
        "_GLOBAL_VERTEX_CREDS",
        "socket.getaddrinfo",
        'or "prj-vertex-json-key"',
    ):
        assert forbidden not in source


def test_get_status_never_resolves_adc_or_reads_machine_paths(monkeypatch):
    resolver = ForbiddenResolver()
    environment = {
        "GOOGLE_APPLICATION_CREDENTIALS": "Z:/private/service-account.json",
        "GOOGLE_GENAI_USE_VERTEXAI": "true",
        "GOOGLE_CLOUD_PROJECT": "ambient-project",
    }
    tool = GeminiOmniVideo(
        environment=environment,
        credential_resolver=resolver,
        transport=RecordingTransport(),
    )

    def forbid_path_probe(*_args, **_kwargs):
        raise AssertionError("get_status must not inspect credential paths")

    monkeypatch.setattr(Path, "exists", forbid_path_probe)
    monkeypatch.setattr(Path, "read_text", forbid_path_probe)
    assert tool.get_status() == ToolStatus.UNAVAILABLE
    assert resolver.calls == 0

    vertex = GeminiOmniVideo(
        route="vertex_interactions",
        model="gemini-omni-1.1-flash-preview",
        vertex_project="explicit-project",
        vertex_location="global",
        environment=environment,
        credential_resolver=resolver,
        transport=RecordingTransport(),
    )
    assert vertex.get_status() == ToolStatus.AVAILABLE
    assert resolver.calls == 0


def test_ambient_credentials_cannot_switch_developer_default(tmp_path):
    resolver = ForbiddenResolver()
    transport = RecordingTransport()
    tool = GeminiOmniVideo(
        environment={
            "GEMINI_API_KEY": "developer-test-key",
            "GOOGLE_APPLICATION_CREDENTIALS": "Z:/private/key.json",
            "GOOGLE_GENAI_USE_VERTEXAI": "true",
            "GOOGLE_CLOUD_PROJECT": "ambient-project",
            "VERTEX_PROJECT_ID": "ambient-project-two",
        },
        credential_resolver=resolver,
        transport=transport,
    )

    result = tool.execute(
        {"prompt": "offline", "output_path": str(tmp_path / "developer.mp4")}
    )

    assert result.success, result.error
    assert resolver.calls == 0
    assert transport.posts[0][0].endswith("/v1beta/interactions")
    headers = transport.posts[0][1]["headers"]
    assert headers["x-goog-api-key"] == "developer-test-key"
    assert "Authorization" not in headers
    assert result.data["route"] == "developer_api"
    assert result.data["model"] == "gemini-omni-flash-preview"
    assert result.data["observed_identity"]["route"] == "developer_api"


def test_explicit_vertex_route_uses_injected_adc_and_exact_payload(tmp_path):
    resolver = FakeResolver()
    transport = RecordingTransport()
    tool = GeminiOmniVideo(
        environment={"GEMINI_API_KEY": "must-be-ignored"},
        credential_resolver=resolver,
        transport=transport,
    )
    inputs = {
        "prompt": "offline vertex",
        "operation": "text_to_video",
        "route": "vertex_interactions",
        "model": "gemini-omni-1.1-flash-preview",
        "vertex_project": "explicit-project",
        "vertex_location": "global",
        "aspect_ratio": "9:16",
        "output_path": str(tmp_path / "vertex.mp4"),
    }

    result = tool.execute(inputs)

    assert result.success, result.error
    assert resolver.calls == [
        ("https://www.googleapis.com/auth/cloud-platform",)
    ]
    url, call = transport.posts[0]
    assert url == (
        "https://aiplatform.googleapis.com/v1beta1/projects/"
        "explicit-project/locations/global/interactions"
    )
    assert call["headers"] == {
        "Authorization": "Bearer offline-adc-token",
        "X-Goog-User-Project": "explicit-project",
        "Content-Type": "application/json",
    }
    assert call["json"] == {
        "model": "gemini-omni-1.1-flash-preview",
        "input": "offline vertex",
        "response_format": {"type": "video", "aspect_ratio": "9:16"},
    }
    assert result.data["route"] == "vertex_interactions"
    assert result.data["model"] == "gemini-omni-1.1-flash-preview"
    assert result.data["observed_identity"] == {
        "tool_name": "gemini_omni_video",
        "tool_contract_version": "0.2.0",
        "provider": "gemini_omni",
        "route": "vertex_interactions",
        "model": "gemini-omni-1.1-flash-preview",
        "operation": "text_to_video",
    }


def test_vertex_download_allows_only_https_googleapis_and_disables_redirects(
    tmp_path,
):
    uri = "https://storage.googleapis.com/private-output/clip.mp4"
    transport = RecordingTransport(
        post_response=FakeResponse(
            {"id": "offline-interaction", "output_video": {"uri": uri}}
        ),
        get_response=FakeResponse({}, content=b"verified offline mp4"),
    )
    result = GeminiOmniVideo(
        credential_resolver=FakeResolver(),
        transport=transport,
        environment={},
    ).execute(
        {
            "prompt": "offline vertex",
            "route": "vertex_interactions",
            "model": "gemini-omni-1.1-flash-preview",
            "vertex_project": "explicit-project",
            "vertex_location": "global",
            "output_path": str(tmp_path / "trusted.mp4"),
        }
    )

    assert result.success, result.error
    assert transport.gets == [
        (
            uri,
            {
                "headers": {"Authorization": "Bearer offline-adc-token"},
                "timeout": 300,
                "allow_redirects": False,
            },
        )
    ]


@pytest.mark.parametrize(
    "uri",
    [
        "http://storage.googleapis.com/private/clip.mp4",
        "https://attacker.example/private/clip.mp4",
        "https://storage.googleapis.com.attacker.example/private/clip.mp4",
        "https://user@storage.googleapis.com/private/clip.mp4",
        "https://storage.googleapis.com:444/private/clip.mp4",
    ],
)
def test_vertex_download_rejects_untrusted_uri_without_get_or_secret_leak(
    tmp_path, uri
):
    secret = "offline-sensitive-bearer"
    resolver = FakeResolver()
    resolver.resolve_access_token = lambda *, scopes: secret
    transport = RecordingTransport(
        post_response=FakeResponse(
            {"id": "offline-interaction", "output_video": {"uri": uri}}
        )
    )
    result = GeminiOmniVideo(
        credential_resolver=resolver,
        transport=transport,
        environment={},
    ).execute(
        {
            "prompt": "offline vertex",
            "route": "vertex_interactions",
            "model": "gemini-omni-1.1-flash-preview",
            "vertex_project": "explicit-project",
            "vertex_location": "global",
            "output_path": str(tmp_path / "never.mp4"),
        }
    )

    assert not result.success
    assert result.error == "Gemini Omni Vertex request or download failed"
    assert transport.gets == []
    assert uri not in result.error
    assert secret not in result.error


def test_vertex_download_redirect_and_response_body_are_not_followed_or_leaked(
    tmp_path,
):
    secret = "offline-sensitive-bearer"
    trusted_uri = "https://storage.googleapis.com/private-output/clip.mp4"
    hostile_body = f"redirect to https://attacker.example/?token={secret}"
    resolver = FakeResolver()
    resolver.resolve_access_token = lambda *, scopes: secret
    transport = RecordingTransport(
        post_response=FakeResponse(
            {"id": "offline-interaction", "output_video": {"uri": trusted_uri}}
        ),
        get_response=FakeResponse(
            {}, ok=False, status_code=302, text=hostile_body
        ),
    )
    result = GeminiOmniVideo(
        credential_resolver=resolver,
        transport=transport,
        environment={},
    ).execute(
        {
            "prompt": "offline vertex",
            "route": "vertex_interactions",
            "model": "gemini-omni-1.1-flash-preview",
            "vertex_project": "explicit-project",
            "vertex_location": "global",
            "output_path": str(tmp_path / "never.mp4"),
        }
    )

    assert not result.success
    assert result.error == "Gemini Omni Vertex request or download failed"
    assert transport.gets[0][1]["allow_redirects"] is False
    assert trusted_uri not in result.error
    assert hostile_body not in result.error
    assert secret not in result.error


@pytest.mark.parametrize("missing", ["model", "vertex_project", "vertex_location"])
def test_vertex_route_missing_explicit_identity_fails_before_adc_or_transport(
    tmp_path, missing
):
    resolver = ForbiddenResolver()
    transport = RecordingTransport()
    inputs = {
        "prompt": "offline vertex",
        "route": "vertex_interactions",
        "model": "gemini-omni-1.1-flash-preview",
        "vertex_project": "explicit-project",
        "vertex_location": "global",
        "output_path": str(tmp_path / "never.mp4"),
    }
    inputs.pop(missing)

    result = GeminiOmniVideo(
        environment={"GEMINI_API_KEY": "must-not-fallback"},
        credential_resolver=resolver,
        transport=transport,
    ).execute(inputs)

    assert not result.success
    assert missing in result.error
    assert resolver.calls == 0
    assert transport.posts == []


def test_vertex_model_drift_fails_without_fallback(tmp_path):
    resolver = ForbiddenResolver()
    transport = RecordingTransport()
    result = GeminiOmniVideo(
        environment={"GEMINI_API_KEY": "must-not-fallback"},
        credential_resolver=resolver,
        transport=transport,
    ).execute(
        {
            "prompt": "offline vertex",
            "route": "vertex_interactions",
            "model": "another-model",
            "vertex_project": "explicit-project",
            "vertex_location": "global",
            "output_path": str(tmp_path / "never.mp4"),
        }
    )

    assert not result.success
    assert "gemini-omni-1.1-flash-preview" in result.error
    assert resolver.calls == 0
    assert transport.posts == []


def test_standard_adc_resolver_uses_google_auth_default_without_project_selection(
    monkeypatch,
):
    import google.auth

    calls = []

    class Credentials:
        valid = False
        token = None

        def refresh(self, request):
            calls.append(("refresh", request))
            self.valid = True
            self.token = "standard-adc-token"

    credentials = Credentials()

    def fake_default(*, scopes):
        calls.append(("default", tuple(scopes)))
        return credentials, "ambient-project-must-be-ignored"

    monkeypatch.setattr(google.auth, "default", fake_default)
    token = GoogleADCVertexTokenResolver().resolve_access_token(
        scopes=("https://www.googleapis.com/auth/cloud-platform",)
    )

    assert token == "standard-adc-token"
    assert calls[0] == (
        "default",
        ("https://www.googleapis.com/auth/cloud-platform",),
    )
    assert calls[1][0] == "refresh"


def test_gemini_mvp_provider_cap_remains_one():
    assert GeminiOmniVideo.version == "0.2.0"
    assert GeminiOmniVideo.provider_concurrency_cap == 1
