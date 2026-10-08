"""Gemini Omni 1.1 video generation and editing through Vertex Interactions."""

from __future__ import annotations

import base64
import mimetypes
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlparse
from tools.google_credentials import get_access_token, has_google_credentials, resolve_project_id

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)

_DEFAULT_MODEL = "gemini-omni-1.1-flash-preview"
# Vertex video output tokens/sec at $17.50 per million, checked 2026-10-08.
_VIDEO_TOKENS = {"360p": 1931, "720p": 5792, "1080p": 8688, "4k": 17376}

class GeminiOmniVideo(BaseTool):
    name = "gemini_omni_video"
    version = "0.2.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "gemini_omni"
    hosting_provider = "google"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = []
    install_instructions = (
        "Set GOOGLE_APPLICATION_CREDENTIALS to a Vertex AI service-account JSON. "
        "Omni 1.1 uses global; the project needs model access and billing."
    )
    agent_skills = ["gemini-omni", "ai-video-gen"]

    capabilities = ["text_to_video", "image_to_video", "reference_to_video", "first_last_frame_to_video", "edit_video", "extend_video"]
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
        "first_last_frame_to_video": True,
        "extend_video": True,
    }
    best_for = [
        "iterative natural-language video editing (edit a clip without regenerating it)",
        "reference-image-driven clips via <FIRST_FRAME>/<IMAGE_REF_N> prompt tags",
        "fast 3-10s clips with synced audio, rendered text, and timecoded beats via Vertex",
    ]
    not_good_for = [
        "single generations longer than 10 seconds",
        "seed-reproducible output or negative-prompt control",
        "offline generation",
    ]
    fallback_tools = []
    quality_score = 0.85

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "model": {"type": "string", "enum": [_DEFAULT_MODEL], "default": _DEFAULT_MODEL},
            "resolution": {"type": "string", "enum": list(_VIDEO_TOKENS), "default": "720p"},
            "last_image_path": {"type": "string", "description": "Last frame: local path or gs:// URI."},
            "reference_video_paths": {"type": "array", "items": {"type": "string"}, "description": "Reference videos: local paths or gs:// URIs."},
            "gcs_uri": {"type": "string", "description": "Optional gs:// output; otherwise inline bytes."},
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
                "enum": ["text_to_video", "image_to_video", "reference_to_video", "first_last_frame_to_video", "edit_video", "extend_video"],
                "default": "text_to_video",
            },
            "aspect_ratio": {
                "type": "string",
                "enum": ["16:9", "9:16"],
                "default": "16:9",
            },
            "duration": {
                "type": ["integer", "string"], "default": 8,
                "description": "3-10 whole seconds; legacy '5'/'5s' accepted. Sent to the API.",
            },
            "reference_image_path": {
                "type": "string",
                "description": "Reference image (jpg/png): local path or gs:// URI for image_to_video.",
            },
            "reference_image_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Reference images: local paths or gs:// URIs, bound as <IMAGE_REF_0>, <IMAGE_REF_1>, ...",
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
                "description": "Source video for edit/extend; local path or gs:// URI.",
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
    idempotency_key_fields = [
        "prompt", "model", "operation", "aspect_ratio", "resolution", "duration",
        "reference_image_path", "reference_image_paths", "last_image_path",
        "input_video_path", "reference_video_paths",
        "previous_interaction_id", "store", "gcs_uri",
    ]
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

    def get_status(self) -> ToolStatus:
        return ToolStatus.AVAILABLE if has_google_credentials() else ToolStatus.UNAVAILABLE

    @staticmethod
    def _duration_hint(inputs: dict[str, Any]) -> int:
        raw = str(inputs.get("duration", 8)).strip().removesuffix("s")
        if not raw.isdecimal() or not 3 <= int(raw) <= 10:
            raise ValueError("Omni duration must be a whole number of seconds from 3 to 10")
        return int(raw)

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        """Video output only; input and reasoning tokens are additional charges."""
        tokens = _VIDEO_TOKENS[inputs.get("resolution", "720p")]
        return round(tokens * self._duration_hint(inputs) * 17.5 / 1_000_000, 6)

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        return 180.0

    @staticmethod
    def _media_part(source: str, kind: str) -> dict[str, Any]:
        mime = mimetypes.guess_type(urlparse(source).path)[0] or {"image": "image/png", "video": "video/mp4"}[kind]
        part = {"type": kind, "mime_type": mime}
        if source.startswith("gs://"):
            part["uri"] = source
        else:
            part["data"] = base64.b64encode(Path(source).read_bytes()).decode("ascii")
        return part

    def build_request(self, inputs: dict[str, Any]) -> dict[str, Any]:
        from jsonschema import validate

        validate(inputs, self.input_schema)
        operation = inputs.get("operation", "text_to_video")
        images = list(inputs.get("reference_image_paths") or [])
        first = inputs.get("reference_image_path")
        if first:
            images.insert(0, first)
        last = inputs.get("last_image_path")
        if last or operation == "first_last_frame_to_video":
            if len(images) != 1 or not last or operation not in {"image_to_video", "first_last_frame_to_video"}:
                raise ValueError("First/last generation requires one first frame, one last frame and image_to_video operation")
            images.append(last)
            operation = "image_to_video"
        videos = list(inputs.get("reference_video_paths") or [])
        source = inputs.get("input_video_path")
        if source:
            videos.insert(0, source)
        previous = inputs.get("previous_interaction_id")
        if operation == "image_to_video" and not images:
            raise ValueError("image_to_video requires a first frame")
        if operation == "reference_to_video" and not (images or videos):
            raise ValueError("reference_to_video requires image or video references")
        if operation in {"edit_video", "extend_video"} and not (previous or videos):
            raise ValueError("Editing/extending requires a source video or previous_interaction_id")
        parts = [self._media_part(p, "image") for p in images]
        parts += [self._media_part(p, "video") for p in videos]
        parts.append({"type": "text", "text": inputs["prompt"]})
        video_format = {
            "type": "video", "delivery": "inline",
            "aspect_ratio": inputs.get("aspect_ratio", "16:9"),
            "resolution": inputs.get("resolution", "720p"),
            "duration": f"{self._duration_hint(inputs)}s",
        }
        if inputs.get("gcs_uri"):
            video_format.update(delivery="uri", gcs_uri=inputs["gcs_uri"])
        task = {"edit_video": "edit", "extend_video": "extend"}.get(operation, operation)
        payload = {
            "model": inputs.get("model", _DEFAULT_MODEL), "input": parts,
            "response_format": [video_format], "store": inputs.get("store", True),
            "generation_config": {"video_config": {"task": task}},
        }
        if previous:
            payload["previous_interaction_id"] = previous
        return payload

    @staticmethod
    def _extract_output_video(data: dict[str, Any]) -> dict[str, Any] | None:
        for key in ("output_video", "outputVideo"):
            if data.get(key):
                return data[key]
        for step in data.get("steps") or []:
            for item in step.get("content") or []:
                if item.get("type") == "video":
                    return item
        return None

    @staticmethod
    def _download_via_uri(requests_mod: Any, token: str, uri: str) -> bytes:
        headers = {}
        if uri.startswith("gs://"):
            bucket, object_name = uri[5:].split("/", 1)
            uri = f"https://storage.googleapis.com/storage/v1/b/{bucket}/o/{quote(object_name, safe='')}?alt=media"
            headers = {"Authorization": f"Bearer {token}"}
        elif urlparse(uri).hostname == "aiplatform.googleapis.com":
            headers = {"Authorization": f"Bearer {token}"}
        response = requests_mod.get(uri, headers=headers, timeout=300)
        response.raise_for_status()
        return response.content

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        import requests

        start = time.time()
        try:
            payload = self.build_request(inputs)
            token, credential_project = get_access_token()
            project = resolve_project_id(credential_project)
            url = f"https://aiplatform.googleapis.com/v1beta1/projects/{project}/locations/global/interactions"
            response = requests.post(
                url, headers={"Authorization": f"Bearer {token}"}, json=payload, timeout=600
            )
            response.raise_for_status()
            data = response.json()
            video = self._extract_output_video(data)
            if not video:
                raise RuntimeError(f"Omni returned no video: {data}")
            video_bytes = (base64.b64decode(video["data"]) if video.get("data")
                           else self._download_via_uri(requests, token, video["uri"]))
            output_path = Path(inputs.get("output_path", "gemini_omni_output.mp4"))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(video_bytes)
            return ToolResult(
                success=True,
                data={
                    "provider": self.provider, "hosting_provider": "google",
                    "model": payload["model"], "output": str(output_path),
                    "operation": inputs.get("operation", "text_to_video"),
                    "aspect_ratio": inputs.get("aspect_ratio", "16:9"),
                    "resolution": inputs.get("resolution", "720p"),
                    "requested_duration": self._duration_hint(inputs), "has_audio": True,
                    "interaction_id": data.get("id"), "editable": payload["store"],
                    "usage": data.get("usage"), "cost_status": "video_output_estimate_only",
                },
                artifacts=[str(output_path)], cost_usd=self.estimate_cost(inputs),
                duration_seconds=round(time.time() - start, 2), model=payload["model"],
            )
        except requests.HTTPError as exc:
            return ToolResult(success=False, error=f"Vertex Omni HTTP {exc.response.status_code}: {exc.response.text}")
        except Exception as exc:
            return ToolResult(success=False, error=f"Vertex Omni generation failed: {exc}")
