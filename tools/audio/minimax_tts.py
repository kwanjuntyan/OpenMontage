"""MiniMax international Speech 2.6 HD with existing system or cloned voices."""

import json
import os
from pathlib import Path

import requests
from jsonschema import validate

from tools.base_tool import BaseTool, ResourceProfile, ToolResult, ToolRuntime, ToolStability, ToolTier
from tools.provider_pricing import PriceQuoteRequired


class MiniMaxTTS(BaseTool):
    name = "minimax_tts"
    provider = "minimax"
    capability = "tts"
    tier = ToolTier.VOICE
    runtime = ToolRuntime.API
    stability = ToolStability.BETA
    dependencies = ["env:MINIMAX_API_KEY", "python:requests"]
    install_instructions = "Set MINIMAX_API_KEY from the international platform.minimax.io account."
    capabilities = ["text_to_speech", "list_voices"]
    supports = {"cloned_voices": True, "multilingual": True, "emotion_control": True}
    best_for = ["MiniMax Speech 2.6 HD narration using existing cloned Voice IDs"]
    resource_profile = ResourceProfile(network_required=True)
    idempotency_key_fields = [
        "operation", "voice_type", "text", "voice_id", "model_id", "speed", "voice_baseline",
        "volume", "pitch", "emotion", "language_boost", "output_format",
    ]
    input_schema = {
        "type": "object",
        "properties": {
            "operation": {"type": "string", "enum": ["generate", "list_voices"], "default": "generate"},
            "voice_type": {"type": "string", "enum": ["all", "system", "voice_cloning", "voice_generation"]},
            "text": {"type": "string", "minLength": 1, "maxLength": 9999},
            "voice_id": {"type": "string", "minLength": 1},
            "voice_baseline": {"type": "string", "description": "Alias in config/minimax_voice_baselines.json, e.g. amy."},
            "model_id": {"type": "string", "enum": ["speech-2.6-hd"], "default": "speech-2.6-hd"},
            "speed": {"type": "number", "minimum": 0.5, "maximum": 2, "default": 1},
            "volume": {"type": "number", "exclusiveMinimum": 0, "maximum": 10, "default": 1},
            "pitch": {"type": "integer", "minimum": -12, "maximum": 12, "default": 0},
            "emotion": {"type": "string", "enum": [
                "happy", "sad", "angry", "fearful", "disgusted", "surprised", "calm", "fluent", "whisper",
            ]},
            "language_boost": {"type": "string", "default": "auto"},
            "output_format": {"type": "string", "enum": ["wav", "mp3"], "default": "wav"},
            "output_path": {"type": "string"},
        },
    }

    def estimate_cost(self, inputs):
        if inputs.get("operation") == "list_voices":
            return 0.0
        raise PriceQuoteRequired("Quote MiniMax Speech 2.6 HD usage and any first-use voice fee before synthesis")

    def resolve_baseline(self, inputs):
        inputs = dict(inputs)
        if inputs.get("voice_baseline") and inputs.get("operation") != "list_voices":
            path = Path(__file__).resolve().parents[2] / "config/minimax_voice_baselines.json"
            catalog = json.loads(path.read_text(encoding="utf-8"))
            if catalog["provider"] != self.provider:
                raise ValueError("Voice baseline provider must be minimax")
            voice = catalog["voices"][inputs["voice_baseline"].lower()]
            inputs.setdefault("model_id", catalog["model_id"])
            inputs.setdefault("voice_id", voice["voice_id"])
            if inputs["model_id"] == catalog["model_id"] and inputs["voice_id"] == voice["voice_id"]:
                inputs.setdefault("speed", voice["speed"])
        return inputs

    def execute(self, inputs):
        inputs = self.resolve_baseline(inputs)
        validate(inputs, self.input_schema)
        listing = inputs.get("operation") == "list_voices"
        if listing:
            endpoint = "get_voice"
            payload = {"voice_type": inputs.get("voice_type", "all")}
        else:
            endpoint = "t2a_v2"
            output_format = inputs.get("output_format", "wav")
            path = Path(inputs.get("output_path", f"minimax_tts.{output_format}"))
            if path.suffix.lower() != f".{output_format}":
                raise ValueError("output_path extension must match output_format")
            voice = {
                "voice_id": inputs["voice_id"], "speed": inputs.get("speed", 1),
                "vol": inputs.get("volume", 1), "pitch": inputs.get("pitch", 0),
            }
            if "emotion" in inputs:
                voice["emotion"] = inputs["emotion"]
            payload = {
                "model": inputs.get("model_id", "speech-2.6-hd"), "text": inputs["text"],
                "stream": False, "output_format": "hex", "voice_setting": voice,
                "language_boost": inputs.get("language_boost", "auto"),
                "audio_setting": {"format": output_format, "sample_rate": 32000, "channel": 1},
            }
        response = requests.post(
            f"https://api.minimax.io/v1/{endpoint}",
            headers={"Authorization": f"Bearer {os.environ['MINIMAX_API_KEY']}"},
            json=payload, timeout=180,
        )
        response.raise_for_status()
        result = response.json()
        status = result["base_resp"]
        if status["status_code"] != 0:
            raise RuntimeError(f"MiniMax API error {status['status_code']}: {status['status_msg']}")
        if listing:
            return ToolResult(success=True, data=result, cost_usd=0.0)
        audio = bytes.fromhex(result["data"]["audio"])
        if not audio:
            raise ValueError("MiniMax returned no audio")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(audio)
        return ToolResult(
            success=True,
            data={
                "provider": self.provider, "model": payload["model"], "output": str(path),
                "voice_setting": voice, "format": output_format,
                "extra_info": result.get("extra_info", {}), "cost_status": "unquoted",
            },
            artifacts=[str(path)], model=payload["model"], cost_usd=None,
        )
