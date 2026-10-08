"""Explicit tool/host/model constraints shared by capability selectors."""

from __future__ import annotations


def filter_explicit_route(inputs, candidates):
    tool_name = inputs.get("preferred_tool")
    host = inputs.get("hosting_provider")
    model = inputs.get("model") or inputs.get("model_id") or inputs.get("model_name")
    # Google model requests default to our direct JSON-authenticated adapters.
    if not tool_name and not host and model:
        if model.startswith("gemini-omni"):
            tool_name = "gemini_omni_video"
        elif model.startswith("gemini-") and "tts" in model:
            tool_name = "gemini_tts"
        elif model.startswith(("imagen-", "gemini-nano-banana-")) or (model.startswith("gemini-") and "image" in model):
            tool_name = "google_imagen"
        elif model.startswith("veo"):
            tool_name = "veo_video"
        elif model.startswith("lyria"):
            tool_name = "google_music"
    selected = []
    for tool in candidates:
        if not tool_name and not host and tool.name in {"gemini_fal_image", "gemini_replicate_image", "gemini_omni_fal"}:
            continue
        if tool_name and tool.name != tool_name:
            continue
        if host and getattr(tool, "hosting_provider", tool.provider) != host:
            continue
        if model:
            props = tool.input_schema.get("properties", {})
            models = set()
            for field in ("model", "model_id", "model_name"):
                models.update(props.get(field, {}).get("enum", []))
            models.update(getattr(tool, "_MODELS", {}))
            models.update(getattr(tool, "_MODEL_ALIASES", {}))
            models.update(tool.get_info().get("model_catalog", {}))
            if model not in models:
                continue
        operation = inputs.get("generation_mode") or inputs.get("operation")
        routes = getattr(tool, "routes", None) or getattr(tool, "models", None)
        if isinstance(routes, dict) and operation and operation != "rank":
            model_routes = (
                routes.get(model, {}) if model else next(iter(routes.values()), {})
            )
            normalized = (
                "text_to_video"
                if operation == "generate" and tool.capability == "video_generation"
                else operation
            )
            if normalized not in model_routes:
                continue
        if tool.capability == "image_generation":
            props = tool.input_schema.get("properties", {})
            if any(inputs.get(k) and k not in props for k in ("mask_path", "mask_url")):
                continue
            if any(
                inputs.get(k) and k not in props and "images" not in props
                for k in ("image_path", "image_paths", "image_url", "image_urls")
            ):
                continue
            if operation == "precise_edit" and not (
                getattr(tool, "supports", {}).get("precise_edit")
                or isinstance(routes, dict)
                and any("precise_edit" in r for r in routes.values())
            ):
                continue
        selected.append(tool)
    return selected
