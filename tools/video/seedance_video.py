"""Seedance 2.0 and 2.5 (ByteDance) video generation via fal.ai API.

Best for cinematic clips with native audio, director-level camera control,
and lip-sync from quoted dialogue in prompts.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

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


class SeedanceVideo(BaseTool):
    name = "seedance_video"
    version = "0.3.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "seedance"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API
    default_model = "2.0"
    reference_model_input_key = "model_version"

    dependencies = []
    install_instructions = (
        "Set FAL_KEY to your fal.ai API key.\n"
        "  Get one at https://fal.ai/dashboard/keys"
    )
    agent_skills = ["seedance-2-0", "seedance-2-5", "ai-video-gen"]

    capabilities = ["text_to_video", "image_to_video", "reference_to_video"]
    supports = {
        "text_to_video": True,
        "image_to_video": True,
        "reference_to_video": True,
        "multiple_reference_images": True,
        "reference_image": True,
        "native_audio": True,
        "cinematic_quality": True,
        "camera_direction": True,
        "lip_sync": True,
        "multi_shot": True,
        "aspect_ratio": True,
        "seed": True,
    }
    best_for = [
        "preferred premium video gen when FAL_KEY is available",
        "cinematic trailers, teasers, and high-fidelity clips with native synchronized audio",
        "director-level camera control and multi-shot editing in a single generation",
        "lip-sync from quoted dialogue in prompts",
        "Seedance 2.5 reference generation (up to 30 images + 10 video + 10 audio clips)",
        "consistent character identity across shots",
    ]
    not_good_for = ["offline generation", "budget-constrained projects"]
    fallback_tools = ["veo_video", "kling_video", "minimax_video"]
    # Premium model — beat out "experimental stability" baseline. The scoring
    # engine reads quality_score directly when present (see lib/scoring.py).
    quality_score = 0.95

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "operation": {
                "type": "string",
                "enum": ["text_to_video", "image_to_video", "reference_to_video"],
                "default": "text_to_video",
            },
            "model_variant": {
                "type": "string",
                "enum": ["standard", "fast"],
                "default": "standard",
                "description": "standard = highest quality, fast = lower latency and cost",
            },
            "model_version": {
                "type": "string",
                "enum": ["2.0", "2.5"],
                "default": "2.0",
                "description": "Seedance 2.5 is the current high-quality model; 2.0 retains fast-tier access.",
            },
            "duration": {
                "type": "string",
                "enum": [
                    "auto",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                ],
                "default": "5",
                "description": "Duration in seconds. 'auto' lets the model decide.",
            },
            "aspect_ratio": {
                "type": "string",
                "enum": ["auto", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"],
                "default": "16:9",
            },
            "resolution": {
                "type": "string",
                "enum": ["480p", "720p"],
                "default": "720p",
            },
            "generate_audio": {
                "type": "boolean",
                "default": True,
                "description": "Generate synchronized audio (speech, SFX, ambient)",
            },
            "image_url": {
                "type": "string",
                "description": "Start frame image URL for image_to_video (jpg, png, webp)",
            },
            "image_path": {
                "type": "string",
                "description": "Local start-frame path for image_to_video. Auto-uploaded to fal.ai storage.",
            },
            "end_image_url": {
                "type": "string",
                "description": "Optional end frame URL for image_to_video",
            },
            "reference_image_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Up to 9 reference image URLs for reference_to_video (identity / wardrobe / setting / style anchors).",
            },
            "reference_image_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Local reference image paths for reference_to_video. Auto-uploaded to fal.ai storage.",
            },
            "reference_images": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Canonical ordered image inputs for reference_to_video; local paths are uploaded in place.",
            },
            "project_dir": {
                "type": "string",
                "description": (
                    "Authoritative CLP project directory; required for strict local "
                    "reference byte/digest verification."
                ),
            },
            "reference_video_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Up to 3 reference video clip URLs for reference_to_video (motion / camera / pacing anchors).",
            },
            "reference_audio_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Up to 3 reference audio clip URLs for reference_to_video (voice / music / ambience anchors).",
            },
            "seed": {
                "type": "integer",
                "description": "Optional seed for reproducibility",
            },
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=500, network_required=True
    )
    retry_policy = RetryPolicy(
        max_retries=2, retryable_errors=["rate_limit", "timeout"]
    )
    idempotency_key_fields = [
        "prompt",
        "model_version",
        "model_variant",
        "operation",
        "duration",
        "seed",
    ]
    side_effects = ["writes video file to output_path", "calls fal.ai API"]
    user_visible_verification = [
        "Watch generated clip for motion coherence, audio sync, and visual quality"
    ]

    def _get_api_key(self) -> str | None:
        return os.environ.get("FAL_KEY") or os.environ.get("FAL_AI_API_KEY")

    def get_status(self) -> ToolStatus:
        if self._get_api_key():
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        if inputs.get("model_version", "2.0") == "2.5":
            return round(
                0.30
                * (
                    5
                    if inputs.get("duration", "5") == "auto"
                    else int(inputs.get("duration", "5"))
                ),
                2,
            )
        variant = inputs.get("model_variant", "standard")
        duration = inputs.get("duration", "5")
        secs = 5 if duration == "auto" else int(duration)
        rate = 0.2419 if variant == "fast" else 0.3034
        return round(rate * secs, 2)

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        if inputs.get("model_version", "2.0") == "2.5":
            return 150.0
        variant = inputs.get("model_variant", "standard")
        return 60.0 if variant == "fast" else 120.0

    def get_reference_capability(
        self,
        model: str | None = None,
        operation: str | None = None,
        model_variant: str | None = None,
    ) -> dict[str, Any]:
        if model is not None and not isinstance(model, str):
            raise ValueError(f"Seedance model_version must be a string, got {type(model).__name__}")
        if operation is not None and not isinstance(operation, str):
            raise ValueError(f"Seedance operation must be a string, got {type(operation).__name__}")
        if model_variant is not None and not isinstance(model_variant, str):
            raise ValueError(
                f"Seedance model_variant must be a string, got {type(model_variant).__name__}"
            )
        ver = model or "2.0"
        if ver not in {"2.0", "2.5"}:
            raise ValueError(f"Unsupported Seedance model_version for reference contract: {ver!r}")
        op = operation or "reference_to_video"
        if op not in {"text_to_video", "image_to_video", "reference_to_video"}:
            raise ValueError(f"Unsupported Seedance operation for reference contract: {op!r}")
        variant = model_variant or "standard"
        if variant not in {"standard", "fast"}:
            raise ValueError(f"Unsupported Seedance model_variant: {variant!r}")
        if ver == "2.5" and variant == "fast":
            raise ValueError("Seedance 2.5 has no fast route")
        operation_path = op.replace("_", "-")
        resolved_model = (
            f"bytedance/seedance-{ver}/fast/{operation_path}"
            if variant == "fast"
            else f"bytedance/seedance-{ver}/{operation_path}"
        )
        canonical_input_key = (
            "reference_images"
            if op == "reference_to_video"
            else ("image_path" if op == "image_to_video" else "none")
        )
        return {
            "operation": op,
            "resolved_model": resolved_model,
            "max_image_slots": (
                (30 if ver == "2.5" else 9)
                if op == "reference_to_video"
                else (1 if op == "image_to_video" else 0)
            ),
            "strict_clp_supported": op == "reference_to_video",
            "canonical_input_key": canonical_input_key,
            "accepted_input_keys": (
                ("reference_images", "reference_image_urls", "reference_image_paths")
                if op == "reference_to_video"
                else (("image_url", "image_path") if op == "image_to_video" else ())
            ),
            "provider_payload_key": (
                ("image_urls" if ver == "2.5" else "reference_image_urls")
                if op == "reference_to_video"
                else ("image_url" if op == "image_to_video" else "none")
            ),
        }

    def get_reference_capacity(
        self,
        model: str | None = None,
        operation: str | None = None,
        model_variant: str | None = None,
    ) -> int:
        """Backward-compatible scalar view of the exact typed capability."""
        return int(
            self.get_reference_capability(
                model=model,
                operation=operation,
                model_variant=model_variant,
            )["max_image_slots"]
        )

    def _build_request_payload(
        self,
        inputs: dict[str, Any],
        *,
        operation: str,
        model_version: str,
        variant: str,
    ) -> dict[str, Any]:
        """Validate media cardinality, then materialize provider inputs.

        All count/type checks run before the first upload. Any upload failure is
        propagated to ``execute`` and normalized into a ToolResult.
        """
        prompt = inputs.get("prompt")
        if not isinstance(prompt, str) or not prompt:
            raise ValueError("Seedance prompt must be a non-empty string")
        payload: dict[str, Any] = {"prompt": prompt}

        if inputs.get("duration"):
            payload["duration"] = inputs["duration"]
        if inputs.get("aspect_ratio"):
            payload["aspect_ratio"] = inputs["aspect_ratio"]
        if inputs.get("resolution"):
            payload["resolution"] = inputs["resolution"]
        if "generate_audio" in inputs:
            payload["generate_audio"] = inputs["generate_audio"]
        if inputs.get("seed") is not None:
            payload["seed"] = inputs["seed"]

        if operation == "image_to_video":
            if inputs.get("image_url"):
                payload["image_url"] = inputs["image_url"]
            elif inputs.get("image_path"):
                from tools.video._shared import upload_image_fal

                payload["image_url"] = upload_image_fal(inputs["image_path"])
            else:
                raise ValueError("Seedance image_to_video requires image_url or image_path")
            if inputs.get("end_image_url"):
                payload["end_image_url"] = inputs["end_image_url"]
            if model_version == "2.5":
                payload["aspect_ratio"] = "auto"

        if operation == "reference_to_video":
            def _string_list(key: str) -> list[str]:
                value = inputs.get(key)
                if value is None:
                    return []
                if not isinstance(value, list) or not all(
                    isinstance(item, str) and item for item in value
                ):
                    raise ValueError(f"Seedance {key} must be an array of non-empty strings")
                return list(value)

            canonical_images = inputs.get("reference_images")
            if canonical_images is not None:
                if not isinstance(canonical_images, list) or not all(
                    isinstance(item, str) and item for item in canonical_images
                ):
                    raise ValueError(
                        "Seedance reference_images must be an array of non-empty strings"
                    )
                raw_images = list(canonical_images)
            else:
                raw_images = [
                    *_string_list("reference_image_urls"),
                    *_string_list("reference_image_paths"),
                ]
            ref_video_urls = _string_list("reference_video_urls")
            ref_audio_urls = _string_list("reference_audio_urls")
            max_images = self.get_reference_capacity(
                model=model_version,
                operation="reference_to_video",
                model_variant=variant,
            )
            max_videos = 10 if model_version == "2.5" else 3
            max_audios = 10 if model_version == "2.5" else 3
            for label, count, maximum in (
                ("reference images", len(raw_images), max_images),
                ("reference videos", len(ref_video_urls), max_videos),
                ("reference audio clips", len(ref_audio_urls), max_audios),
            ):
                if count > maximum:
                    raise ValueError(
                        f"Seedance {model_version} reference_to_video accepts at most "
                        f"{maximum} {label}; got {count}"
                    )
            if not (raw_images or ref_video_urls or ref_audio_urls):
                raise ValueError(
                    "Seedance reference_to_video requires at least one reference input"
                )

            ref_image_urls: list[str] = []
            for value in raw_images:
                if value.lower().startswith(
                    ("http://", "https://", "gs://", "s3://", "data:", "asset://")
                ):
                    ref_image_urls.append(value)
                else:
                    from tools.video._shared import upload_image_fal

                    ref_image_urls.append(upload_image_fal(value))
            if ref_image_urls:
                payload[
                    "image_urls" if model_version == "2.5" else "reference_image_urls"
                ] = ref_image_urls
            if ref_video_urls:
                payload[
                    "video_urls" if model_version == "2.5" else "reference_video_urls"
                ] = ref_video_urls
            if ref_audio_urls:
                payload[
                    "audio_urls" if model_version == "2.5" else "reference_audio_urls"
                ] = ref_audio_urls
        return payload

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        try:
            from lib.clp_validator import validate_provider_reference_submission

            def _effective_string(key: str, default: str) -> str:
                if key not in inputs:
                    return default
                value = inputs[key]
                if not isinstance(value, str) or not value:
                    raise ValueError(
                        f"Seedance {key} must be a non-empty string when supplied, "
                        f"got {value!r}"
                    )
                return value

            operation = _effective_string("operation", "text_to_video")
            model_version = _effective_string("model_version", "2.0")
            variant = _effective_string("model_variant", "standard")
            route_contract = self.get_reference_capability(
                model=model_version,
                operation=operation,
                model_variant=variant,
            )
            validate_provider_reference_submission(self, inputs)
        except (ValueError, RuntimeError) as exc:
            return ToolResult(success=False, error=f"Provider preflight rejected request: {exc}")

        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(
                success=False,
                error="FAL_KEY not set. " + self.install_instructions,
            )

        import requests

        start = time.time()
        operation = route_contract["operation"]
        model_path = route_contract["resolved_model"]

        try:
            payload = self._build_request_payload(
                inputs,
                operation=operation,
                model_version=model_version,
                variant=variant,
            )
        except Exception as exc:  # noqa: BLE001 - normalize adapter/media failures
            return ToolResult(
                success=False,
                error=f"Seedance {model_version} video generation failed: {exc}",
            )

        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        }

        try:
            submit_resp = requests.post(
                f"https://queue.fal.run/{model_path}",
                headers=headers,
                json=payload,
                timeout=30,
            )
            submit_resp.raise_for_status()
            queue_data = submit_resp.json()
            status_url = queue_data["status_url"]
            response_url = queue_data["response_url"]

            while True:
                time.sleep(5)
                status_resp = requests.get(status_url, headers=headers, timeout=15)
                status_resp.raise_for_status()
                status = status_resp.json().get("status", "UNKNOWN")
                if status == "COMPLETED":
                    break
                if status in ("FAILED", "CANCELLED"):
                    return ToolResult(
                        success=False,
                        error=f"Seedance {model_version} video generation {status.lower()}",
                    )

            result_resp = requests.get(response_url, headers=headers, timeout=30)
            result_resp.raise_for_status()
            data = result_resp.json()

            video_url = data["video"]["url"]
            video_response = requests.get(video_url, timeout=120)
            video_response.raise_for_status()

            output_path = Path(inputs.get("output_path", "seedance_output.mp4"))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(video_response.content)

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Seedance {model_version} video generation failed: {e}",
            )

        from tools.video._shared import probe_output

        probed = probe_output(output_path)
        return ToolResult(
            success=True,
            data={
                "provider": "seedance",
                "model": model_path,
                "prompt": inputs["prompt"],
                "operation": operation,
                "variant": variant,
                "model_version": model_version,
                "aspect_ratio": inputs.get("aspect_ratio", "16:9"),
                "resolution": inputs.get("resolution", "720p"),
                "generate_audio": inputs.get("generate_audio", True),
                "seed": data.get("seed"),
                "output": str(output_path),
                "output_path": str(output_path),
                "format": "mp4",
                **probed,
            },
            artifacts=[str(output_path)],
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            model=model_path,
        )
