"""Gemini 3.8 TTS via Vertex generateContent, separate from Cloud TTS."""

from __future__ import annotations
from pathlib import Path
from tools.provider_pricing import PriceQuoteRequired

from tools.base_tool import (
    BaseTool,
    ToolTier,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolResult,
    ResourceProfile,
)


class GeminiTTS(BaseTool):
    name = "gemini_tts"
    capability = "tts"
    provider = "gemini"
    hosting_provider = "google"
    tier = ToolTier.VOICE
    runtime = ToolRuntime.API
    stability = ToolStability.BETA
    agent_skills = ["provider-model-refresh"]
    install_instructions = "Set GOOGLE_APPLICATION_CREDENTIALS to a service-account JSON; use google-genai >= 2.25.0."
    capabilities = ["text_to_speech", "multi_speaker"]
    supports = {"multi_speaker": True, "style_control": True}
    best_for = ["Expressive single-speaker narration and directed dialogue"]
    resource_profile = ResourceProfile(network_required=True)
    idempotency_key_fields = [
        "model_id",
        "text",
        "voice_id",
        "style",
        "turns",
        "speakers",
        "output_format",
    ]
    input_schema = {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["generate", "list_voices"],
                "default": "generate",
            },
            "model_id": {
                "type": "string",
                "enum": ["gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts"],
                "default": "gemini-3.8-flash-tts",
            },
            "text": {"type": "string", "minLength": 1},
            "voice_id": {"type": "string", "default": "Kore"},
            "style": {"type": "string"},
            "output_format": {"type": "string", "enum": ["wav"], "default": "wav"},
            "turns": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["speaker", "text"],
                    "properties": {
                        "speaker": {"type": "string"},
                        "text": {"type": "string", "minLength": 1},
                        "style": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
            },
            "speakers": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "items": {
                    "type": "object",
                    "required": ["speaker", "voice"],
                    "properties": {
                        "speaker": {"type": "string"},
                        "voice": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
            },
            "output_path": {"type": "string"},
        },
    }

    def get_status(self):
        from tools.google_credentials import has_google_credentials

        return (
            ToolStatus.AVAILABLE if has_google_credentials() else ToolStatus.UNAVAILABLE
        )

    def estimate_cost(self, inputs):
        if inputs.get("operation") == "list_voices":
            return 0.0
        raise PriceQuoteRequired(
            "Gemini TTS requires a current token-based price quote"
        )

    def build_request(self, inputs):
        from jsonschema import validate

        validate(inputs, self.input_schema)
        if bool(inputs.get("text")) == bool(inputs.get("turns")):
            raise ValueError("Provide text or turns, exclusively")
        if inputs.get("turns"):
            speakers = inputs.get("speakers", [])
            names = [s["speaker"] for s in speakers]
            if len(set(names)) != len(names) or any(
                t["speaker"] not in names for t in inputs["turns"]
            ):
                raise ValueError(
                    "Every turn requires a unique configured speaker voice"
                )
            turns = inputs["turns"]
            speech = {"multi_speaker_voice_config": {"speaker_voice_configs": [
                {"speaker": s["speaker"], "voice_config": {"voice": s["voice"]}} for s in speakers
            ]}}
        else:
            turns = [{"text": inputs["text"], "style": inputs.get("style", "")}]
            speech = {"voice_config": {"voice": inputs.get("voice_id", "Kore")}}
        content = []
        for turn in turns:
            metadata = {k: turn[k] for k in ("speaker", "style") if turn.get(k)}
            content.append(
                {"text": turn["text"], "speech_metadata": metadata}
            )
        audio_format = {"audio": {"mimeType": "AUDIO_WAV"}}
        return {
            "model": inputs.get("model_id", "gemini-3.8-flash-tts"),
            "contents": [{"role": "user", "parts": content}],
            "config": {
                "response_modalities": ["AUDIO"], "speech_config": speech,
                "http_options": {"extra_body": {"generationConfig": {"responseFormat": [audio_format]}}},
            },
        }

    def execute(self, inputs):
        from tools.google_credentials import get_genai_client, GOOGLE_API_TIMEOUT_MS

        try:
            if inputs.get("operation") == "list_voices":
                with get_genai_client(location="global") as client:
                    voices = client.voices.list()
                return ToolResult(success=True, data=voices.model_dump(mode="json", exclude_none=True), cost_usd=0.0)
            path = Path(inputs.get("output_path", "gemini_tts.wav"))
            if path.suffix.lower() != ".wav":
                raise ValueError("output_path must use .wav")
            request = self.build_request(inputs)
            with get_genai_client(location="global", http_options={"timeout": GOOGLE_API_TIMEOUT_MS}) as client:
                result = client.models.generate_content(**request)
            data = b"".join(
                p.inline_data.data for c in (result.candidates or [])
                for p in (c.content.parts if c.content else [])
                if p.inline_data and p.inline_data.data
            )
            if not data:
                raise ValueError("Gemini returned no audio")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            return ToolResult(
                success=True,
                data={
                    "provider": self.provider,
                    "model": request["model"],
                    "output": str(path),
                    "format": "wav",
                    "sample_rate": 24000,
                    "channels": 1,
                    "cost_status": "unquoted",
                },
                artifacts=[str(path)],
                cost_usd=None,
                model=request["model"],
            )
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))
