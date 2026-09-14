"""Google Gemini Omni Flash video generation and conversational editing.

Calls the Gemini Interactions API (``POST /v1beta/interactions``) directly with
the project's Google API key — the same key that unlocks Imagen images and
Cloud TTS. Gemini Omni Flash generates 3-10 second 720p/24fps clips with
synthesized audio, and is the only provider in the fleet with stateful
conversational editing: pass ``previous_interaction_id`` and describe only the
delta ("Make the violin invisible. Keep everything else the same.").

Reference images bind to roles via inline prompt tags (``<FIRST_FRAME>``,
``<IMAGE_REF_N>``) and beats can be scheduled with timecode syntax
(``[0-3s] ... [3-6s] ...``). See the Layer 3 skill ``gemini-omni`` for the
authoritative prompting guide — read it before writing prompts.
"""

from __future__ import annotations

import base64
import mimetypes
import os
import time
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence
from urllib.parse import urlsplit

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)

_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
_UPLOAD_URL = "https://generativelanguage.googleapis.com/upload/v1beta/files"
_DEFAULT_MODEL = "gemini-omni-flash-preview"
_DEVELOPER_ROUTE = "developer_api"
_VERTEX_ROUTE = "vertex_interactions"
_VERTEX_MODEL = "gemini-omni-1.1-flash-preview"
_CLOUD_PLATFORM_SCOPE = "https://www.googleapis.com/auth/cloud-platform"
# Billed at 5,792 output tokens per second of 720p video, $17.50/1M tokens
# (ai.google.dev/gemini-api/docs/pricing) — effectively ~$0.10 per second.
_COST_PER_SECOND = 0.10
_DEFAULT_DURATION_SECONDS = 8
_POLL_INTERVAL_SECONDS = 5
_MAX_POLL_SECONDS = 900


class GeminiHTTPTransport(Protocol):
    """Small injectable HTTP boundary used by both Interactions routes."""

    def post(self, url: str, **kwargs: Any) -> Any: ...

    def get(self, url: str, **kwargs: Any) -> Any: ...


class VertexAccessTokenResolver(Protocol):
    """Resolve one access token without choosing any routing identity."""

    def resolve_access_token(self, *, scopes: Sequence[str]) -> str: ...


class RequestsGeminiTransport:
    """Lazy requests adapter; construction and status checks are offline."""

    @staticmethod
    def post(url: str, **kwargs: Any) -> Any:
        import requests

        return requests.post(url, **kwargs)

    @staticmethod
    def get(url: str, **kwargs: Any) -> Any:
        import requests

        return requests.get(url, **kwargs)


class GoogleADCVertexTokenResolver:
    """Use standard ADC/attached identity for a caller-selected Vertex route.

    An explicitly configured ``GOOGLE_APPLICATION_CREDENTIALS`` file remains a
    standard ADC input handled by ``google.auth.default``. This resolver never
    searches for key files and never treats ADC's detected project as routing.
    """

    @staticmethod
    def resolve_access_token(*, scopes: Sequence[str]) -> str:
        import google.auth
        from google.auth.transport.requests import Request

        credentials, _detected_project = google.auth.default(scopes=list(scopes))
        if not credentials.valid or not credentials.token:
            credentials.refresh(Request())
        token = credentials.token
        if not isinstance(token, str) or not token:
            raise RuntimeError("Standard ADC did not provide an access token")
        return token


class GeminiOmniVideo(BaseTool):
    name = "gemini_omni_video"
    version = "0.2.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "gemini_omni"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API
    provider_concurrency_cap = 1

    dependencies = []
    install_instructions = (
        "Set GEMINI_API_KEY or GOOGLE_API_KEY to a Google AI Studio API key.\n"
        "  Get one at https://aistudio.google.com/apikey\n"
        "  Gemini Omni Flash is paid-tier only (no free tier); ~$0.10 per second of video."
    )
    agent_skills = ["gemini-omni", "ai-video-gen"]

    capabilities = ["text_to_video", "image_to_video", "reference_to_video", "edit_video"]
    supports = {
        "text_to_video": True,
        "image_to_video": True,
        "reference_to_video": True,
        "edit_video": True,
        "conversational_editing": True,
        "native_audio": True,
        "text_rendering": True,
        "timecode_control": True,
        # Preview limitations — no sampler controls of any kind.
        "seed": False,
        "negative_prompt": False,
        "first_last_frame_to_video": False,
    }
    best_for = [
        "iterative natural-language video editing (edit a clip without regenerating it)",
        "reference-image-driven clips via <FIRST_FRAME>/<IMAGE_REF_N> prompt tags",
        "fast 3-10s clips with synced audio, rendered text, and timecoded beats from one Google key",
    ]
    not_good_for = [
        "clips longer than 10 seconds or above 720p",
        "seed-reproducible output or negative-prompt control",
        "offline generation",
    ]
    fallback_tools = ["veo_video", "sora_video", "kling_video", "minimax_video"]
    # Conversational editing + native audio are unique in the fleet, but preview
    # output is capped at 720p/10s — below seedance (0.95) and grok/runway (0.9)
    # on raw generation fidelity. Without a quality_score the scorer would only
    # count supports/stability flags and bury the editing capability entirely.
    # See lib/scoring.py.
    quality_score = 0.85

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {
                "type": "string",
                "description": (
                    "Video description, or for edit_video the change to apply. "
                    "Supports <FIRST_FRAME>/<IMAGE_REF_N> tags and [0-3s] timecodes — "
                    "see the gemini-omni skill."
                ),
            },
            "operation": {
                "type": "string",
                "enum": ["text_to_video", "image_to_video", "reference_to_video", "edit_video"],
                "default": "text_to_video",
            },
            "route": {
                "type": "string",
                "enum": [_DEVELOPER_ROUTE, _VERTEX_ROUTE],
                "default": _DEVELOPER_ROUTE,
                "description": (
                    "Explicit API route. Ambient credentials never change this value."
                ),
            },
            "model": {
                "type": "string",
                "description": (
                    "Exact route model. Required for vertex_interactions; the "
                    "Developer API retains its compatibility default."
                ),
            },
            "vertex_project": {
                "type": "string",
                "description": "Explicit billing/routing project for Vertex only.",
            },
            "vertex_location": {
                "type": "string",
                "description": "Explicit Vertex location, such as global.",
            },
            "aspect_ratio": {
                "type": "string",
                "enum": ["16:9", "9:16"],
                "default": "16:9",
            },
            "duration": {
                "type": "string",
                "description": (
                    "Duration hint in seconds (3-10). The model chooses the actual length; "
                    "this only shapes the prompt-independent cost estimate."
                ),
            },
            "reference_image_path": {
                "type": "string",
                "description": "Local reference image (jpg/png) for image_to_video.",
            },
            "reference_image_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Local reference images, bound in the prompt as <IMAGE_REF_0>, <IMAGE_REF_1>, ...",
            },
            "previous_interaction_id": {
                "type": "string",
                "description": (
                    "Interaction id from a prior gemini_omni_video result — edits that video "
                    "in place (edit_video). Requires the prior call to have used store=true."
                ),
            },
            "input_video_path": {
                "type": "string",
                "description": (
                    "Local video to edit (edit_video). Uploaded via the Files API. "
                    "Editing uploaded videos is unavailable in the EEA, Switzerland, and the UK."
                ),
            },
            "store": {
                "type": "boolean",
                "default": True,
                "description": (
                    "Keep the interaction server-side so the result can be edited in later turns "
                    "via previous_interaction_id. Set false only for one-shot generations."
                ),
            },
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=500, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=1, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["prompt", "operation", "aspect_ratio", "previous_interaction_id"]
    side_effects = [
        "writes video file to output_path",
        "calls the Gemini Interactions API",
        "stores the interaction server-side when store=true (enables later edits)",
    ]
    user_visible_verification = [
        "Watch generated clip for visual quality, motion, and prompt adherence",
        "Listen for synthesized audio quality and any requested dialogue/music",
        "After an edit turn, confirm unmentioned elements were preserved",
    ]

    def __init__(
        self,
        *,
        route: str = _DEVELOPER_ROUTE,
        model: str | None = None,
        vertex_project: str | None = None,
        vertex_location: str | None = None,
        credential_resolver: VertexAccessTokenResolver | None = None,
        transport: GeminiHTTPTransport | None = None,
        environment: Mapping[str, str] | None = None,
    ):
        if route not in {_DEVELOPER_ROUTE, _VERTEX_ROUTE}:
            raise ValueError(f"Unsupported Gemini Omni route: {route}")
        self._configured_route = route
        self._configured_model = model
        self._configured_vertex_project = vertex_project
        self._configured_vertex_location = vertex_location
        self._credential_resolver = (
            credential_resolver or GoogleADCVertexTokenResolver()
        )
        self._transport = transport or RequestsGeminiTransport()
        self._environment = environment if environment is not None else os.environ

    def _get_api_key(self) -> str | None:
        return self._environment.get("GEMINI_API_KEY") or self._environment.get(
            "GOOGLE_API_KEY"
        )

    @staticmethod
    def _field_or_configured(
        inputs: Mapping[str, Any], field: str, configured: str | None
    ) -> str | None:
        value = inputs[field] if field in inputs else configured
        return value if isinstance(value, str) and value else None

    def _resolve_route(
        self, inputs: Mapping[str, Any]
    ) -> tuple[str, str, str | None, str | None]:
        route = inputs.get("route", self._configured_route)
        if route not in {_DEVELOPER_ROUTE, _VERTEX_ROUTE}:
            raise ValueError("route must be developer_api or vertex_interactions")
        model = self._field_or_configured(
            inputs, "model", self._configured_model
        )
        if route == _DEVELOPER_ROUTE:
            model = model or _DEFAULT_MODEL
            if model != _DEFAULT_MODEL:
                raise ValueError(
                    f"developer_api model must be exactly {_DEFAULT_MODEL}"
                )
            return route, model, None, None

        if model is None:
            raise ValueError("model is required for vertex_interactions")
        if model != _VERTEX_MODEL:
            raise ValueError(
                f"vertex_interactions model must be exactly {_VERTEX_MODEL}"
            )
        project = self._field_or_configured(
            inputs, "vertex_project", self._configured_vertex_project
        )
        location = self._field_or_configured(
            inputs, "vertex_location", self._configured_vertex_location
        )
        if project is None:
            raise ValueError("vertex_project is required for vertex_interactions")
        if location is None:
            raise ValueError("vertex_location is required for vertex_interactions")
        if not all(character.isalnum() or character == "-" for character in project):
            raise ValueError("vertex_project contains unsupported characters")
        if not all(character.isalnum() or character == "-" for character in location):
            raise ValueError("vertex_location contains unsupported characters")
        return route, model, project, location

    def get_status(self) -> ToolStatus:
        try:
            route, _model, _project, _location = self._resolve_route({})
        except ValueError:
            return ToolStatus.UNAVAILABLE
        if route == _VERTEX_ROUTE:
            return ToolStatus.AVAILABLE
        return ToolStatus.AVAILABLE if self._get_api_key() else ToolStatus.UNAVAILABLE

    @staticmethod
    def _duration_hint(inputs: dict[str, Any]) -> int:
        raw = str(inputs.get("duration") or _DEFAULT_DURATION_SECONDS).strip().lower()
        raw = raw[:-1] if raw.endswith("s") else raw
        try:
            seconds = int(float(raw))
        except ValueError:
            seconds = _DEFAULT_DURATION_SECONDS
        return max(3, min(10, seconds))

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        return _COST_PER_SECOND * self._duration_hint(inputs)

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        return 180.0

    @staticmethod
    def _image_part(path_str: str) -> dict[str, Any]:
        path = Path(path_str)
        if not path.exists():
            raise FileNotFoundError(f"Reference image not found: {path}")
        mime_type, _ = mimetypes.guess_type(path.name)
        if not mime_type or not mime_type.startswith("image/"):
            mime_type = "image/png"
        return {
            "type": "image",
            "data": base64.b64encode(path.read_bytes()).decode("ascii"),
            "mime_type": mime_type,
        }

    def _upload_video_file(self, requests_mod: Any, api_key: str, path_str: str) -> str:
        """Upload a local video via the Files API (resumable) and return its URI."""
        path = Path(path_str)
        if not path.exists():
            raise FileNotFoundError(f"Input video not found: {path}")
        mime_type, _ = mimetypes.guess_type(path.name)
        if not mime_type or not mime_type.startswith("video/"):
            mime_type = "video/mp4"
        video_bytes = path.read_bytes()

        start_resp = requests_mod.post(
            _UPLOAD_URL,
            headers={
                "x-goog-api-key": api_key,
                "X-Goog-Upload-Protocol": "resumable",
                "X-Goog-Upload-Command": "start",
                "X-Goog-Upload-Header-Content-Length": str(len(video_bytes)),
                "X-Goog-Upload-Header-Content-Type": mime_type,
                "Content-Type": "application/json",
            },
            json={"file": {"display_name": path.name}},
            timeout=30,
        )
        start_resp.raise_for_status()
        upload_url = start_resp.headers.get("X-Goog-Upload-URL")
        if not upload_url:
            raise RuntimeError("Files API did not return an upload URL")

        upload_resp = requests_mod.post(
            upload_url,
            headers={
                "X-Goog-Upload-Command": "upload, finalize",
                "X-Goog-Upload-Offset": "0",
                "Content-Length": str(len(video_bytes)),
            },
            data=video_bytes,
            timeout=300,
        )
        upload_resp.raise_for_status()
        file_info = upload_resp.json().get("file", {})

        # Wait until the uploaded video is processed before referencing it.
        deadline = time.time() + _MAX_POLL_SECONDS
        while str(file_info.get("state", "")).upper() == "PROCESSING":
            if time.time() > deadline:
                raise TimeoutError("Uploaded video did not finish processing in time")
            time.sleep(_POLL_INTERVAL_SECONDS)
            status_resp = requests_mod.get(
                f"{_BASE_URL}/{file_info.get('name')}",
                headers={"x-goog-api-key": api_key},
                timeout=15,
            )
            status_resp.raise_for_status()
            file_info = status_resp.json()
        if str(file_info.get("state", "")).upper() == "FAILED":
            raise RuntimeError("Files API failed to process the uploaded video")

        uri = file_info.get("uri")
        if not uri:
            raise RuntimeError(f"Files API response missing uri: {file_info}")
        return uri

    @staticmethod
    def _extract_output_video(data: dict[str, Any]) -> dict[str, Any] | None:
        """Find the output video payload ({'data': b64} or {'uri': files/...})."""
        for key in ("output_video", "outputVideo"):
            video = data.get(key)
            if isinstance(video, dict) and (video.get("data") or video.get("uri")):
                return video
        # REST responses may also carry the video inside steps[].content[].
        for step in data.get("steps") or []:
            for item in step.get("content") or []:
                if isinstance(item, dict) and (item.get("data") or item.get("uri")):
                    if "video" in str(item.get("type", "")).lower() or item.get("mime_type", "").startswith("video/"):
                        return item
                    if item.get("data") or str(item.get("uri", "")).startswith("files/"):
                        return item
        return None

    @staticmethod
    def _file_id_from_uri(uri: str) -> str:
        """Extract the bare file id from any documented URI shape.

        The API may return ``files/<id>``, a full
        ``https://.../v1beta/files/<id>`` resource URI, or a ready-made
        download URL ``.../files/<id>:download?alt=media``. Polling and
        download both need just ``<id>``.
        """
        path = uri.split("?", 1)[0].rstrip("/")
        marker = "files/"
        idx = path.rfind(marker)
        tail = path[idx + len(marker):] if idx != -1 else path.split("/")[-1]
        return tail.split(":", 1)[0]

    def _download_via_uri(self, requests_mod: Any, api_key: str, uri: str) -> bytes:
        """Poll a Files API entry until ACTIVE, then download its bytes."""
        file_id = self._file_id_from_uri(uri)
        headers = {"x-goog-api-key": api_key}
        deadline = time.time() + _MAX_POLL_SECONDS
        while True:
            status_resp = requests_mod.get(
                f"{_BASE_URL}/files/{file_id}", headers=headers, timeout=15
            )
            status_resp.raise_for_status()
            state = str(status_resp.json().get("state", "")).upper()
            if state == "ACTIVE":
                break
            if state == "FAILED":
                raise RuntimeError("Gemini Omni video generation failed during processing")
            if time.time() > deadline:
                raise TimeoutError("Timed out waiting for Gemini Omni video to become ACTIVE")
            time.sleep(_POLL_INTERVAL_SECONDS)

        download_resp = requests_mod.get(
            f"{_BASE_URL}/files/{file_id}:download",
            params={"alt": "media"},
            headers=headers,
            timeout=300,
        )
        download_resp.raise_for_status()
        return download_resp.content

    @staticmethod
    def _validated_vertex_download_uri(uri: str) -> str:
        """Accept only direct HTTPS downloads hosted by Google APIs.

        Vertex response data is untrusted. In particular, a Bearer token must
        never be forwarded to an arbitrary URI or across an HTTP redirect.
        """
        try:
            parsed = urlsplit(uri)
            hostname = (parsed.hostname or "").rstrip(".").lower()
            port = parsed.port
        except (TypeError, ValueError) as exc:
            raise ValueError("Vertex output URI is not trusted") from exc
        googleapis_host = hostname == "googleapis.com" or hostname.endswith(
            ".googleapis.com"
        )
        if (
            parsed.scheme != "https"
            or not googleapis_host
            or parsed.username is not None
            or parsed.password is not None
            or port not in {None, 443}
        ):
            raise ValueError("Vertex output URI is not trusted")
        return uri

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        try:
            route, model_name, project_id, vertex_location = self._resolve_route(
                inputs
            )
        except ValueError as exc:
            return ToolResult(
                success=False,
                error=f"Gemini Omni configuration invalid: {exc}",
            )
        use_vertex = route == _VERTEX_ROUTE
        api_key = self._get_api_key() if not use_vertex else None
        if not use_vertex and not api_key:
            return ToolResult(
                success=False,
                error=(
                    "Neither GEMINI_API_KEY nor GOOGLE_API_KEY is set for the "
                    f"explicit {_DEVELOPER_ROUTE} route. {self.install_instructions}"
                ),
            )

        start = time.time()
        operation = inputs.get("operation", "text_to_video")
        prompt = str(inputs["prompt"]).strip()
        aspect_ratio = inputs.get("aspect_ratio", "16:9")
        previous_interaction_id = inputs.get("previous_interaction_id")

        if operation == "edit_video" and not previous_interaction_id and not inputs.get("input_video_path"):
            return ToolResult(
                success=False,
                error="edit_video requires previous_interaction_id (edit a generated clip) or input_video_path (edit an uploaded clip)",
            )

        reference_paths = list(inputs.get("reference_image_paths") or [])
        if inputs.get("reference_image_path"):
            reference_paths.insert(0, inputs["reference_image_path"])
        if operation in {"image_to_video", "reference_to_video"} and not reference_paths:
            return ToolResult(
                success=False,
                error=f"{operation} requires reference_image_path or reference_image_paths",
            )

        try:
            parts: list[dict[str, Any]] = [self._image_part(p) for p in reference_paths]
            if inputs.get("input_video_path"):
                if use_vertex:
                    raise NotImplementedError("Direct video upload to Vertex Interactions API is not yet supported; use image references or prompt text.")
                video_uri = self._upload_video_file(
                    self._transport, api_key, inputs["input_video_path"]
                )
                parts.append({"type": "document", "uri": video_uri})
        except Exception as e:
            return ToolResult(success=False, error=f"Gemini Omni input preparation failed: {e}")

        if use_vertex:
            try:
                token = self._credential_resolver.resolve_access_token(
                    scopes=(_CLOUD_PLATFORM_SCOPE,)
                )
            except Exception:
                return ToolResult(
                    success=False,
                    error=(
                        "Gemini Omni Vertex authentication failed: standard ADC "
                        "did not provide a usable access token"
                    ),
                )
            if not isinstance(token, str) or not token:
                return ToolResult(
                    success=False,
                    error="Gemini Omni Vertex authentication returned an empty token",
                )
            assert project_id is not None
            assert vertex_location is not None
            endpoint = (
                "https://aiplatform.googleapis.com/v1beta1/projects/"
                f"{project_id}/locations/{vertex_location}/interactions"
            )
            headers = {
                "Authorization": f"Bearer {token}",
                "X-Goog-User-Project": project_id,
                "Content-Type": "application/json",
            }
            payload: dict[str, Any] = {
                "model": model_name,
                "input": prompt if not parts else parts + [{"type": "text", "text": prompt}],
                "response_format": {
                    "type": "video",
                    "aspect_ratio": aspect_ratio,
                },
            }
        else:
            endpoint = f"{_BASE_URL}/interactions"
            headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}
            payload: dict[str, Any] = {
                "model": model_name,
                "input": prompt if not parts else parts + [{"type": "text", "text": prompt}],
                "response_format": {
                    "type": "video",
                    "aspect_ratio": aspect_ratio,
                    "delivery": "uri",
                },
            }

        if previous_interaction_id:
            payload["previous_interaction_id"] = previous_interaction_id
        if inputs.get("store") is False:
            payload["store"] = False

        try:
            resp = self._transport.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=600,
            )
            if not resp.ok:
                if use_vertex:
                    return ToolResult(
                        success=False,
                        error=(
                            "Gemini Omni Vertex interaction failed "
                            f"(HTTP {resp.status_code})"
                        ),
                    )
                detail = resp.text[:1000]
                return ToolResult(
                    success=False,
                    error=f"Gemini Omni interaction failed ({resp.status_code}): {detail}",
                )
            data = resp.json()

            interaction_id = data.get("id")
            video = self._extract_output_video(data)
            if not video:
                if use_vertex:
                    return ToolResult(
                        success=False,
                        error="Gemini Omni Vertex response contained no output video",
                    )
                return ToolResult(
                    success=False,
                    error=f"Gemini Omni response did not include an output video: {str(data)[:1000]}",
                )

            if video.get("data"):
                video_bytes = base64.b64decode(video["data"])
            elif use_vertex:
                uri = self._validated_vertex_download_uri(str(video.get("uri")))
                dl_resp = self._transport.get(
                    uri,
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=300,
                    allow_redirects=False,
                )
                if not 200 <= int(dl_resp.status_code) < 300:
                    raise RuntimeError("Vertex output download was not successful")
                video_bytes = dl_resp.content
            else:
                video_bytes = self._download_via_uri(
                    self._transport, api_key, str(video["uri"])
                )

            output_path = Path(inputs.get("output_path", "gemini_omni_output.mp4"))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(video_bytes)
        except Exception as e:
            if use_vertex:
                return ToolResult(
                    success=False,
                    error="Gemini Omni Vertex request or download failed",
                )
            return ToolResult(success=False, error=f"Gemini Omni video generation failed: {e}")

        editable = inputs.get("store") is not False
        return ToolResult(
            success=True,
            data={
                "provider": self.provider,
                "route": route,
                "model": model_name,
                "prompt": prompt,
                "operation": operation,
                "output": str(output_path),
                "aspect_ratio": aspect_ratio,
                "has_audio": True,
                # Feed this back as previous_interaction_id to edit this clip.
                "interaction_id": interaction_id,
                "editable": editable,
                "observed_identity": {
                    "tool_name": self.name,
                    "tool_contract_version": self.version,
                    "provider": self.provider,
                    "route": route,
                    "model": model_name,
                    "operation": operation,
                },
            },
            artifacts=[str(output_path)],
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            model=model_name,
        )
