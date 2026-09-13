"""Atlas Cloud video generation with exact, discoverable live-model routes."""

from __future__ import annotations

import mimetypes
import time
from pathlib import Path
from typing import Any

from tools import atlas_client
from tools.atlas_models import VIDEO_MODELS, VIDEO_ROUTES
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

_DEFAULT_MODEL = "bytedance/seedance-2.5/text-to-video"
_DEFAULT_COST_PER_SECOND = 0.10
_OPERATIONS = ("text_to_video", "image_to_video", "reference_to_video", "video_edit")
_ATLAS_RESERVED_EXTRA_PARAM_KEYS = frozenset(
    {
        "model",
        "model_variant",
        "operation",
        "prompt",
        "duration",
        "ratio",
        "aspect_ratio",
        "resolution",
        "image",
        "images",
        "image_url",
        "image_urls",
        "reference_image",
        "reference_images",
        "reference_image_url",
        "reference_image_urls",
        "reference_image_path",
        "reference_image_paths",
        "last_image",
        "last_image_url",
        "end_image",
        "end_image_url",
        "video",
        "videos",
        "video_url",
        "video_clips",
        "reference_video",
        "reference_videos",
        "reference_video_url",
        "reference_audios",
        "refers",
        "clp_manifest",
        "clp_binding",
        "clp_shot_id",
        "clp_shot_bindings",
        "clp_scene_plan",
        "clp_reference_inputs",
        "auxiliary_reference_images",
        "_reference_execution_plan",
        "project_dir",
        "output_path",
        "poll_interval",
        "poll_timeout",
    }
    | {
        field
        for spec in VIDEO_MODELS.values()
        for field in spec.get("optional_fields", ())
    }
    | {str(spec["ratio_key"]) for spec in VIDEO_MODELS.values()}
)


def _is_remote(entry: str) -> bool:
    lowered = str(entry).strip().lower()
    return lowered.startswith(("http://", "https://", "data:", "asset://"))


def _media_type(entry: str) -> str:
    mime, _ = mimetypes.guess_type(str(entry).split("?", 1)[0])
    if mime:
        return mime.split("/", 1)[0]
    suffix = Path(str(entry).split("?", 1)[0]).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".heic", ".heif"}:
        return "image"
    if suffix in {".mp4", ".mov", ".webm", ".mkv"}:
        return "video"
    if suffix in {".mp3", ".wav", ".m4a", ".aac", ".flac"}:
        return "audio"
    raise ValueError(f"Cannot infer Atlas reference media type from {entry!r}; pass `refers` with an explicit type")


class AtlasVideo(BaseTool):
    name = "atlas_video"
    version = "0.2.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "atlascloud"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API
    default_model = _DEFAULT_MODEL
    reference_model_input_key = "model"

    dependencies = ["env:ATLASCLOUD_API_KEY"]
    install_instructions = atlas_client.INSTALL_INSTRUCTIONS
    agent_skills = ["atlas-cloud", "ai-video-gen", "seedance-2-0", "gemini-omni"]

    capabilities = list(_OPERATIONS)
    supports = {
        "text_to_video": True,
        "image_to_video": True,
        "reference_to_video": True,
        "video_edit": True,
        "first_last_frame": True,
        "mixed_media_references": True,
        "native_audio": True,
        "custom_duration": True,
        "aspect_ratio": True,
        "multi_model_gateway": True,
    }
    provider_matrix = {
        family: {key: value for key, value in routes.items()}
        for family, routes in VIDEO_ROUTES.items()
    }
    best_for = [
        "Seedance 2.5/2.0 text, image, and mixed-reference video through Atlas Cloud",
        "Gemini Omni Flash text, image, reference, and video-edit workflows",
        "MiniMax H3 text, start/end image, and mixed-media reference generation up to 2K",
        "one Atlas key with exact per-model request validation and cost estimates",
    ]
    not_good_for = ["offline generation", "clips longer than the selected model permits"]
    fallback_tools = ["seedance_video", "kling_video", "minimax_video", "veo_video"]
    quality_score = 0.86

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "model": {
                "type": "string",
                "default": _DEFAULT_MODEL,
                "enum": sorted(VIDEO_MODELS),
                "description": "Exact live Atlas model id. See provider_matrix in get_info() for supported sibling routes.",
            },
            "operation": {"type": "string", "enum": list(_OPERATIONS), "default": "text_to_video"},
            "model_variant": {
                "type": "string", "enum": ["standard", "developer"], "default": "standard",
                "description": "Select Gemini Omni's developer route when it exists.",
            },
            "duration": {"type": "integer", "default": 10},
            "aspect_ratio": {"type": "string", "default": "16:9"},
            "resolution": {"type": "string"},
            "seed": {"type": "integer"},
            "thinking_level": {"type": "string", "enum": ["default", "high", "low"]},
            "generate_audio": {"type": "boolean"},
            "watermark": {"type": "boolean"},
            "return_last_frame": {"type": "boolean"},
            "output_format": {"type": "string", "enum": ["mp4", "mov"]},
            "bitrate_mode": {"type": "string", "enum": ["standard", "high"]},
            "image_url": {"type": "string"},
            "image_path": {"type": "string"},
            "reference_image_url": {"type": "string"},
            "reference_image_path": {"type": "string"},
            "last_image_url": {"type": "string"},
            "last_image_path": {"type": "string"},
            "end_image_url": {"type": "string"},
            "end_image_path": {"type": "string"},
            "reference_images": {"type": "array", "items": {"type": "string"}},
            "project_dir": {
                "type": "string",
                "description": (
                    "Authoritative CLP project directory; required for strict local "
                    "reference byte/digest verification."
                ),
            },
            "reference_videos": {"type": "array", "items": {"type": "string"}},
            "reference_audios": {"type": "array", "items": {"type": "string"}},
            "video_url": {"type": "string"},
            "video_path": {"type": "string"},
            "reference_video_url": {"type": "string"},
            "reference_video_path": {"type": "string"},
            "video_clips": {"type": "array", "items": {"type": "object"}},
            "refers": {"type": "array", "items": {"type": "object"}},
            "extra_params": {"type": "object"},
            "poll_interval": {"type": "number", "default": 5.0},
            "poll_timeout": {"type": "number", "default": 1200.0},
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=512, disk_mb=500, network_required=True)
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["prompt", "model", "operation", "duration", "aspect_ratio"]
    side_effects = ["writes video file to output_path", "calls Atlas Cloud API"]
    user_visible_verification = ["Watch the generated clip for prompt fidelity, motion coherence, and audio quality"]

    def get_status(self) -> ToolStatus:
        return ToolStatus.AVAILABLE if atlas_client.get_api_key() else ToolStatus.UNAVAILABLE

    def get_info(self) -> dict[str, Any]:
        info = super().get_info()
        info["model_catalog"] = {
            model_id: {
                "family": spec["family"],
                "operation": spec["operation"],
                "variant": spec.get("variant", "standard"),
                "cost_per_second": spec["cost_per_second"],
                "durations": list(spec["durations"]) if spec["durations"] else None,
                "resolutions": list(spec["resolutions"]),
                "media_style": spec["media_style"],
            }
            for model_id, spec in VIDEO_MODELS.items()
        }
        return info

    @staticmethod
    def _family(model: str) -> str:
        spec = VIDEO_MODELS.get(model)
        return spec["family"] if spec else "/".join(model.split("/")[:2])

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        model = self._resolve_model(
            str(inputs.get("model", _DEFAULT_MODEL)),
            str(inputs.get("operation", "text_to_video")),
            str(inputs["model_variant"]) if inputs.get("model_variant") else None,
        )
        rate = VIDEO_MODELS.get(model, {}).get("cost_per_second", _DEFAULT_COST_PER_SECOND)
        duration = int(inputs.get("duration", 10))
        return round(rate * max(duration, 0), 4)

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        return 180.0

    def get_reference_capability(
        self,
        model: str | None = None,
        operation: str | None = None,
        model_variant: str | None = None,
    ) -> dict[str, Any]:
        if model is not None and not isinstance(model, str):
            raise ValueError(f"Atlas model must be a string, got {type(model).__name__}")
        if operation is not None and not isinstance(operation, str):
            raise ValueError(f"Atlas operation must be a string, got {type(operation).__name__}")
        if model_variant is not None and not isinstance(model_variant, str):
            raise ValueError(
                f"Atlas model_variant must be a string, got {type(model_variant).__name__}"
            )
        requested_model = model or _DEFAULT_MODEL
        requested_spec = VIDEO_MODELS.get(requested_model)
        if requested_spec is None:
            raise ValueError(
                f"Unsupported Atlas video model id {requested_model!r} for reference contract"
            )
        op = operation or requested_spec["operation"]
        if op not in _OPERATIONS:
            raise ValueError(f"Unsupported Atlas video operation {op!r}")
        resolved_model = self._resolve_model(requested_model, op, model_variant)
        resolved_spec = VIDEO_MODELS[resolved_model]
        if resolved_spec["operation"] != op:
            raise ValueError(
                f"Atlas capability resolved operation mismatch: requested {op!r}, "
                f"resolved {resolved_spec['operation']!r}"
            )
        media_limits = resolved_spec.get("media_limits", {})
        if op in {"reference_to_video", "video_edit"}:
            max_images = int(media_limits.get("images", 0))
        elif op == "image_to_video":
            max_images = 1
        else:
            max_images = 0
        media_style = str(resolved_spec.get("media_style", "none"))
        payload_key = {
            "seedance_references": "reference_images",
            "gemini_images": "images",
            "h3_refers": "refers",
            "gemini_video_edit": "images",
            "seedance_image": "image",
            "gemini_image": "image",
            "h3_image": "image",
        }.get(media_style, "none")
        canonical_input_key = (
            "reference_images"
            if op in {"reference_to_video", "video_edit"}
            else ("image_path" if op == "image_to_video" else "none")
        )
        accepted_input_keys = {
            "reference_to_video": (
                "reference_images",
                "reference_image_urls",
                "reference_image_paths",
            ),
            "video_edit": (
                "reference_images",
                "reference_image_urls",
                "reference_image_paths",
            ),
            "image_to_video": (
                "image_path",
                "image_url",
                "reference_image_path",
                "reference_image_url",
            ),
            "text_to_video": (),
        }[op]
        return {
            "operation": op,
            "resolved_model": resolved_model,
            "max_image_slots": max_images,
            "strict_clp_supported": op == "reference_to_video" and max_images > 0,
            "canonical_input_key": canonical_input_key,
            "accepted_input_keys": accepted_input_keys,
            "provider_payload_key": payload_key,
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

    def is_operation_available(self, operation: str) -> bool:
        return operation in _OPERATIONS

    def _resolve_model(self, model: str, operation: str, variant: str | None = None) -> str:
        if model not in VIDEO_MODELS:
            raise ValueError(
                f"Unsupported Atlas video model id {model!r}. Use get_info()['model_catalog'] for live routes."
            )
        spec = VIDEO_MODELS[model]
        variant = variant or str(spec.get("variant", "standard"))
        route_key = operation if variant == "standard" else f"{operation}_{variant}"
        resolved = VIDEO_ROUTES.get(spec["family"], {}).get(route_key)
        if not resolved:
            raise ValueError(
                f"{spec['family']} does not expose operation={operation!r}, variant={variant!r} on Atlas Cloud"
            )
        return resolved

    @staticmethod
    def _validate_choice(name: str, value: Any, allowed: tuple[Any, ...] | None) -> Any:
        if allowed and value not in allowed:
            raise ValueError(f"{name}={value!r} is not supported; choose one of {list(allowed)}")
        return value

    @staticmethod
    def _validated_extra_params(value: Any) -> dict[str, Any]:
        """Return extension-only Atlas parameters; reject all owned payload keys."""
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError("extra_params must be an object")
        if any(not isinstance(key, str) or not key for key in value):
            raise ValueError("extra_params keys must be non-empty strings")
        conflicts = sorted(set(value) & _ATLAS_RESERVED_EXTRA_PARAM_KEYS)
        if conflicts:
            raise ValueError(
                f"extra_params cannot override reserved Atlas payload keys: {conflicts}"
            )
        return dict(value)

    def _build_payload(self, inputs: dict[str, Any], model: str) -> dict[str, Any]:
        spec = VIDEO_MODELS[model]
        payload: dict[str, Any] = {"model": model, "prompt": inputs.get("prompt", "")}

        if spec["operation"] != "video_edit":
            duration = int(inputs.get("duration", 10))
            payload["duration"] = self._validate_choice("duration", duration, spec["durations"])
            ratio = inputs.get("aspect_ratio", spec["default_ratio"])
            if ratio == "16:9" and spec["default_ratio"] == "adaptive" and spec["ratios"] == ("adaptive",):
                ratio = "adaptive"
            payload[spec["ratio_key"]] = self._validate_choice("aspect_ratio", ratio, spec["ratios"])

        resolution = inputs.get("resolution", spec["default_resolution"])
        payload["resolution"] = self._validate_choice("resolution", resolution, spec["resolutions"])

        for field in spec.get("optional_fields", ()):
            if inputs.get(field) is not None:
                payload[field] = inputs[field]

        style = spec["media_style"]
        image = inputs.get("image_url") or inputs.get("reference_image_url")
        last_image = inputs.get("last_image_url") or inputs.get("end_image_url")
        images = list(inputs.get("reference_images") or [])
        videos = list(inputs.get("reference_videos") or [])
        audios = list(inputs.get("reference_audios") or [])
        video = inputs.get("video_url") or inputs.get("reference_video_url")

        if style in {"seedance_image", "gemini_image", "h3_image"}:
            if not image:
                raise ValueError("image_to_video requires image_url, image_path, or reference_image_path")
            payload["image"] = image
            if last_image:
                payload["last_image" if style == "seedance_image" else "end_image"] = last_image
        elif style == "gemini_images":
            if image and not images:
                images = [image]
            if not images:
                raise ValueError("This Gemini route requires at least one reference image")
            image_limit = int(spec.get("media_limits", {}).get("images", 0))
            if image_limit and len(images) > image_limit:
                raise ValueError(
                    f"{model} accepts at most {image_limit} reference images; "
                    f"got {len(images)}"
                )
            payload["images"] = images
        elif style == "seedance_references":
            if image and not images:
                images = [image]
            if not (images or videos or (audios and spec["family"] == "bytedance/seedance-2.5")):
                raise ValueError("reference_to_video requires supported reference media for the selected model")
            limits = spec["media_limits"]
            if len(images) > limits["images"] or len(videos) > limits["videos"] or len(audios) > limits["audios"]:
                raise ValueError(
                    f"{model} accepts at most {limits['images']} images, {limits['videos']} videos, "
                    f"and {limits['audios']} audio references"
                )
            if images:
                payload["reference_images"] = images
            if videos:
                payload["reference_videos"] = videos
            if audios:
                payload["reference_audios"] = audios
        elif style == "h3_refers":
            refers = list(inputs.get("refers") or [])
            if not refers:
                refers = [
                    *({"url": value, "type": "image"} for value in images),
                    *({"url": value, "type": "video"} for value in videos),
                    *({"url": value, "type": "audio"} for value in audios),
                ]
                if image:
                    refers.insert(0, {"url": image, "type": "image"})
            if not refers or not any(item.get("type") in {"image", "video"} for item in refers):
                raise ValueError("MiniMax H3 reference_to_video requires at least one image or video in refers")
            payload["refers"] = refers
        elif style == "gemini_video_clips":
            clips = list(inputs.get("video_clips") or [])
            if not clips and video:
                clips = [{"url": video, "start": 0, "ends": min(int(inputs.get("duration", 10)), 10)}]
            if len(clips) != 1:
                raise ValueError("Gemini Omni developer reference_to_video requires exactly one video_clip")
            payload["video_clips"] = clips
            if images:
                payload["images"] = images
        elif style == "gemini_video_edit":
            if not video:
                raise ValueError("video_edit requires video_url, video_path, or reference_video_path")
            payload["video"] = video
            if images:
                if len(images) > spec["media_limits"].get("images", 10):
                    raise ValueError("Gemini Omni video_edit accepts at most 10 reference images")
                payload["images"] = images

        payload.update(self._validated_extra_params(inputs.get("extra_params")))
        return payload

    @staticmethod
    def _upload_value(value: str | None, api_key: str) -> str | None:
        if not value or _is_remote(value):
            return value
        return atlas_client.upload_media(value, api_key)

    def _normalize_media_inputs(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Normalize and type-check media aliases without uploads."""
        resolved = dict(inputs)

        def _media_string(value: Any, context: str) -> str:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Atlas {context} must be a non-empty string")
            if value != value.strip():
                raise ValueError(
                    f"Atlas {context} must not contain surrounding whitespace"
                )
            return value

        def _items(key: str) -> list[str]:
            value = resolved.get(key)
            if value is None:
                return []
            if not isinstance(value, list):
                raise ValueError(f"Atlas {key} must be an array")
            return [
                _media_string(item, f"{key}[{index}]")
                for index, item in enumerate(value)
            ]

        resolved["reference_images"] = [
            *_items("reference_images"),
            *_items("reference_image_urls"),
            *_items("reference_image_paths"),
        ]
        resolved["reference_videos"] = [
            *_items("reference_videos"),
            *_items("reference_video_urls"),
            *_items("reference_video_paths"),
        ]
        resolved["reference_audios"] = [
            *_items("reference_audios"),
            *_items("reference_audio_urls"),
            *_items("reference_audio_paths"),
        ]
        aliases = {
            "image_url": ("image_url", "reference_image_url", "image_path", "reference_image_path"),
            "last_image_url": ("last_image_url", "end_image_url", "last_image_path", "end_image_path"),
            "video_url": ("video_url", "reference_video_url", "video_path", "reference_video_path"),
        }
        for target, sources in aliases.items():
            supplied = []
            for key in sources:
                if key in resolved and resolved[key] is not None:
                    supplied.append(_media_string(resolved[key], key))
            if supplied:
                resolved[target] = supplied[0]

        if resolved.get("refers") is not None:
            if not isinstance(resolved["refers"], list):
                raise ValueError("Atlas refers must be an array")
            normalized = []
            for index, item in enumerate(resolved["refers"]):
                if not isinstance(item, dict):
                    raise ValueError("Each Atlas refers item must be an object")
                entry = dict(item)
                entry["url"] = _media_string(item.get("url"), f"refers[{index}].url")
                if "type" in entry:
                    if entry["type"] not in {"image", "video", "audio"}:
                        raise ValueError(
                            "Each Atlas refers item type must be image, video, or audio"
                        )
                else:
                    entry["type"] = _media_type(entry["url"])
                normalized.append(entry)
            resolved["refers"] = normalized

        if resolved.get("video_clips") is not None:
            if not isinstance(resolved["video_clips"], list):
                raise ValueError("Atlas video_clips must be an array")
            clips = []
            for index, item in enumerate(resolved["video_clips"]):
                if not isinstance(item, dict):
                    raise ValueError("Each Atlas video_clips item must be an object")
                clip = dict(item)
                clip["url"] = _media_string(
                    item.get("url"), f"video_clips[{index}].url"
                )
                clips.append(clip)
            resolved["video_clips"] = clips
        return resolved

    def _resolve_media(self, inputs: dict[str, Any], api_key: str) -> dict[str, Any]:
        resolved = self._normalize_media_inputs(inputs)
        for key in ("image_url", "last_image_url", "video_url"):
            if resolved.get(key):
                resolved[key] = self._upload_value(resolved[key], api_key)

        for key in ("reference_images", "reference_videos", "reference_audios"):
            resolved[key] = [
                self._upload_value(value, api_key)
                for value in resolved.get(key, [])
            ]

        if resolved.get("refers"):
            normalized = []
            for item in resolved["refers"]:
                entry = dict(item)
                entry["url"] = self._upload_value(entry["url"], api_key)
                normalized.append(entry)
            resolved["refers"] = normalized

        if resolved.get("video_clips"):
            clips = []
            for item in resolved["video_clips"]:
                clip = dict(item)
                clip["url"] = self._upload_value(clip["url"], api_key)
                clips.append(clip)
            resolved["video_clips"] = clips
        return resolved

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        try:
            from lib.clp_validator import validate_provider_reference_submission

            def _effective_string(key: str, default: str) -> str:
                if key not in inputs:
                    return default
                value = inputs[key]
                if not isinstance(value, str) or not value:
                    raise ValueError(
                        f"Atlas {key} must be a non-empty string when supplied, "
                        f"got {value!r}"
                    )
                return value

            requested_model = _effective_string("model", _DEFAULT_MODEL)
            requested_operation = _effective_string("operation", "text_to_video")
            requested_variant = (
                _effective_string("model_variant", "standard")
                if "model_variant" in inputs
                else None
            )
            route_contract = self.get_reference_capability(
                model=requested_model,
                operation=requested_operation,
                model_variant=requested_variant,
            )
            self._validated_extra_params(inputs.get("extra_params"))
            validate_provider_reference_submission(self, inputs)
            # Pure shape/cardinality/required-media validation. This produces
            # no network I/O and runs before API-key lookup or media upload.
            preview = self._normalize_media_inputs(inputs)
            self._build_payload(preview, route_contract["resolved_model"])
        except (ValueError, RuntimeError) as exc:
            return ToolResult(success=False, error=f"Provider preflight rejected request: {exc}")

        api_key = atlas_client.get_api_key()
        if not api_key:
            return ToolResult(success=False, error="ATLASCLOUD_API_KEY not set. " + self.install_instructions)

        started = time.time()
        operation = route_contract["operation"]
        try:
            model = route_contract["resolved_model"]
            resolved = self._resolve_media(inputs, api_key)
            payload = self._build_payload(resolved, model)
            prediction_id = atlas_client.submit(atlas_client.GENERATE_VIDEO_ENDPOINT, payload, api_key)
            data = atlas_client.poll(
                prediction_id, api_key,
                interval=float(inputs.get("poll_interval", 5.0)),
                timeout=float(inputs.get("poll_timeout", 1200.0)),
            )
            suffix = str(inputs.get("output_format", "mp4"))
            output_path = Path(inputs.get("output_path") or f"atlas_video.{suffix}")
            atlas_client.download(data["outputs"][0], output_path)
        except (atlas_client.AtlasError, ValueError, KeyError) as exc:
            return ToolResult(success=False, error=f"Atlas Cloud video generation failed: {exc}")
        except Exception as exc:  # noqa: BLE001
            return ToolResult(success=False, error=f"Atlas Cloud video generation failed: {exc}")

        from tools.video._shared import probe_output

        probed = probe_output(output_path)
        cost_inputs = {**inputs, "model": model, "operation": operation}
        return ToolResult(
            success=True,
            data={
                "provider": "atlascloud", "model": model, "prompt": inputs["prompt"],
                "operation": operation, "output": str(output_path), "output_path": str(output_path),
                "prediction_id": prediction_id, "source_url": data["outputs"][0],
                "format": output_path.suffix.lstrip("."), "request_params": payload, **probed,
            },
            artifacts=[str(output_path)], cost_usd=self.estimate_cost(cost_inputs),
            duration_seconds=round(time.time() - started, 2), model=model,
        )
