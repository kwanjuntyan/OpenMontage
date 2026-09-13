"""Capability-level video selector that routes between generation and stock providers.

Provider discovery is automatic — any BaseTool with capability="video_generation"
is picked up from the registry.  Adding a new video provider requires only creating
the tool file in tools/video/; no changes to this selector are needed.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from tools.base_tool import BaseTool, ToolResult, ToolRuntime, ToolStability, ToolStatus, ToolTier


class VideoSelector(BaseTool):
    name = "video_selector"
    version = "0.3.1"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "selector"
    stability = ToolStability.BETA
    runtime = ToolRuntime.HYBRID
    agent_skills = ["ai-video-gen", "create-video", "ltx2", "gemini-omni", "atlas-cloud"]

    # Operations that REQUIRE motion: an image-only tool (image_selector) is not
    # an acceptable last-resort fallback for these, so fallback_tools_for() drops it.
    MOTION_REQUIRED_OPERATIONS = frozenset({"image_to_video", "reference_to_video", "video_edit"})
    # Default score gap for the preferred_provider override (see input_schema).
    PREFERRED_PROVIDER_GAP = 0.15

    capabilities = [
        "text_to_video", "image_to_video", "reference_to_video", "video_edit", "stock_video",
        "provider_selection", "search_video", "download_video",
    ]
    supports = {
        "user_preference_routing": True,
        "offline_fallback": True,
        "reference_image": True,
        "stock_fallback": True,
    }
    best_for = [
        "preflight routing",
        "user-facing recommendation flows",
        "switching between cloud, local, and stock video tools",
    ]

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "preferred_provider": {
                "type": "string",
                "description": "Provider name or 'auto'. Valid values are discovered at runtime from the registry.",
                "default": "auto",
            },
            "preferred_provider_gap": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "default": 0.15,
                "description": (
                    "Max weighted-score gap (0-1) within which an explicit preferred_provider "
                    "overrides the top-ranked provider. If the preferred provider's best score "
                    "falls more than this far below the overall top, the preference is ignored "
                    "and the top-ranked provider wins. Default 0.15 — honors a preference unless "
                    "it would drag selection to a drastically worse provider."
                ),
            },
            "allowed_providers": {"type": "array", "items": {"type": "string"}},
            "operation": {
                "type": "string",
                "enum": ["text_to_video", "image_to_video", "reference_to_video", "video_edit", "rank"],
                "default": "text_to_video",
            },
            "target_operation": {
                "type": "string",
                "enum": ["text_to_video", "image_to_video", "reference_to_video", "video_edit"],
                "description": "Operation to score when operation='rank'.",
                "default": "text_to_video",
            },
            "aspect_ratio": {
                "type": "string",
                "enum": ["16:9", "9:16", "1:1"],
                "default": "16:9",
                "description": "Video aspect ratio. Passed through to the selected provider.",
            },
            "duration": {
                "type": "string",
                "description": "Duration hint (e.g., '5', '10'). Passed through to the selected provider.",
            },
            "reference_image_path": {
                "type": "string",
                "description": "Local path to a reference image for image_to_video. Auto-uploaded if the provider requires a URL.",
            },
            "reference_image_url": {
                "type": "string",
                "description": "URL of a reference image for image_to_video.",
            },
            "reference_image_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Reference image URLs for providers that support reference-conditioned video.",
            },
            "reference_image_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Local reference image paths for providers that support reference-conditioned video.",
            },
            "clp_reference_inputs": {
                "type": "array",
                "description": (
                    "Exact strict CLP mapping. Each entry must contain only entity_id, "
                    "asset_sha256, and a project-contained local path."
                ),
                "items": {
                    "type": "object",
                    "required": ["entity_id", "asset_sha256", "path"],
                    "additionalProperties": False,
                    "properties": {
                        "entity_id": {"type": "string", "minLength": 1},
                        "asset_sha256": {
                            "type": "string",
                            "pattern": "^sha256:[0-9a-f]{64}$",
                        },
                        "path": {"type": "string", "minLength": 1},
                    },
                },
            },
            "clp_shot_id": {
                "type": "string",
                "minLength": 1,
                "description": (
                    "Independent current shot identity used to select exactly one "
                    "row from the authenticated persisted CLP sidecar."
                ),
            },
            "clp_manifest": {
                "type": "object",
                "description": "Optional exact cache of checkpoint_clp.json authority.",
            },
            "clp_binding": {
                "type": "object",
                "description": "Optional exact cache of the selected persisted sidecar row.",
            },
            "clp_shot_bindings": {
                "type": "object",
                "description": "Optional exact cache of checkpoint_scene_plan sidecar authority.",
            },
            "clp_scene_plan": {
                "type": "object",
                "description": "Optional exact cache of the persisted scene_plan artifact.",
            },
            "auxiliary_reference_images": {
                "type": "array",
                "description": (
                    "Non-identity style references, kept separate from strict CLP mappings "
                    "but charged against the same physical image-slot capacity."
                ),
                "items": {
                    "oneOf": [
                        {
                            "type": "object",
                            "required": ["path"],
                            "additionalProperties": False,
                            "properties": {"path": {"type": "string", "minLength": 1}},
                        },
                        {
                            "type": "object",
                            "required": ["url"],
                            "additionalProperties": False,
                            "properties": {"url": {"type": "string", "minLength": 1}},
                        },
                    ]
                },
            },
            "project_dir": {
                "type": "string",
                "description": (
                    "Authoritative local project directory. Its basename must exactly "
                    "match project.json and the persisted checkpoint identities."
                ),
            },
            "reference_video_url": {
                "type": "string",
                "description": "Reference video URL for providers that support video-conditioned generation.",
            },
            "reference_video_path": {
                "type": "string",
                "description": "Local reference video path. Providers that require URLs should reject this clearly.",
            },
            "reference_video_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Reference video URLs for mixed-media generation.",
            },
            "reference_video_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Local reference video paths for mixed-media generation.",
            },
            "reference_audio_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Reference audio URLs for mixed-media generation.",
            },
            "reference_audio_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Local reference audio paths for mixed-media generation.",
            },
            "last_image_url": {"type": "string", "description": "Optional final frame for first/last-frame generation."},
            "last_image_path": {"type": "string", "description": "Optional local final frame."},
            "video_url": {"type": "string", "description": "Source video URL for video editing."},
            "video_path": {"type": "string", "description": "Local source video for video editing."},
            "video_clips": {"type": "array", "items": {"type": "object"}},
            "refers": {"type": "array", "items": {"type": "object"}},
            "image_list": {
                "type": "array",
                "description": "Provider-specific list of image references, e.g. Kling Official Video Omni.",
            },
            "video_list": {
                "type": "array",
                "description": "Provider-specific list of video references, e.g. Kling Official Video Omni.",
            },
            "element_list": {
                "type": "array",
                "description": "Provider-specific element references, e.g. Kling Official element_id objects.",
            },
            "multi_shot": {
                "type": "boolean",
                "description": "Provider-specific multi-shot mode.",
            },
            "shot_type": {
                "type": "string",
                "description": "Provider-specific multi-shot type.",
            },
            "multi_prompt": {
                "type": "array",
                "description": "Structured multi-shot prompts; not inferred from prose.",
            },
            "image_url": {
                "type": "string",
                "description": "Alias for reference_image_url (used by some providers like Kling via fal.ai).",
            },
            "resolution": {
                "type": "string",
                "description": "Resolution hint for providers that support named output resolutions.",
            },
            "api_family": {
                "type": "string",
                "description": "Provider-specific API family hint passed through when supported, e.g. classic/turbo/omni.",
            },
            "model_name": {
                "type": "string",
                "description": "Provider-specific model name passed through when supported.",
            },
            "model": {
                "type": "string",
                "description": "Exact provider model id, e.g. an Atlas Cloud live model route.",
            },
            "model_version": {
                "type": "string",
                "enum": ["2.0", "2.5"],
                "description": (
                    "Seedance direct-adapter version selector. Mutually exclusive "
                    "with the exact provider `model` selector."
                ),
            },
            "model_variant": {
                "type": "string",
                "description": "Provider route variant, e.g. standard or developer.",
            },
            "mode": {
                "type": "string",
                "description": "Provider-specific quality mode passed through when supported.",
            },
            "sound": {
                "type": "string",
                "description": "Provider-specific native audio toggle passed through when supported.",
            },
            "watermark": {
                "type": "boolean",
                "description": "Provider-specific watermark toggle passed through when supported.",
            },
            "callback_url": {
                "type": "string",
                "description": "Provider-specific callback URL. Current OpenMontage providers still poll by default.",
            },
            "external_task_id": {
                "type": "string",
                "description": "Provider-specific idempotency/provenance task id.",
            },
            "workflow_json": {
                "type": "string",
                "description": (
                    "Optional full ComfyUI workflow JSON. Routes to a custom-workflow-capable "
                    "provider (e.g. comfyui_video) based on server availability, not bundled "
                    "model readiness. Requires output_node."
                ),
            },
            "workflow_path": {
                "type": "string",
                "description": (
                    "Optional path to a ComfyUI workflow JSON file. Routes to a custom-workflow-"
                    "capable provider based on server availability. Requires output_node."
                ),
            },
            "output_node": {
                "type": "string",
                "description": "ComfyUI output node ID for a custom workflow_json/workflow_path.",
            },
            "workflow_name": {
                "type": "string",
                "description": "Optional human-readable provenance label for a custom workflow.",
            },
            "workflow_model": {
                "type": "string",
                "description": "Optional model/provenance label for a custom workflow.",
            },
            "workflow_model_stack": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Optional provenance metadata for custom workflow dependencies.",
            },
            "output_path": {"type": "string"},
        },
    }

    def _providers(self) -> list[BaseTool]:
        """Auto-discover video generation providers from the registry."""
        from tools.tool_registry import registry
        registry.ensure_discovered()
        return [t for t in registry.get_by_capability("video_generation")
                if t.name != self.name]

    @property
    def fallback_tools(self) -> list[str]:
        """Static (input-agnostic) fallback list for external consumers / contracts.

        See :meth:`fallback_tools_for` for the input-aware form used during
        routing, which drops ``image_selector`` for motion-required briefs.
        """
        return [t.name for t in self._providers()] + ["image_selector"]

    def fallback_tools_for(self, inputs: dict[str, object]) -> list[str]:
        """Input-aware fallback list used during routing.

        ``image_selector`` is a legitimate degraded last-resort for a still-image
        brief (text_to_video with no motion requirement), but for motion-required
        operations (image_to_video / reference_to_video) an image-only fallback
        silently defeats the brief. Gate it here at the selector layer so a direct
        caller — with no director skill enforcing the prohibition — still cannot
        fall back to an image tool when motion was requested.
        """
        tools = [t.name for t in self._providers()]
        operation = inputs.get("operation", "text_to_video")
        if operation in self.MOTION_REQUIRED_OPERATIONS:
            return tools
        return tools + ["image_selector"]

    @property
    def provider_matrix(self) -> dict[str, dict[str, str]]:
        """Built at runtime from each provider's best_for field."""
        matrix = {}
        for tool in self._providers():
            strength = ", ".join(tool.best_for) if tool.best_for else tool.name
            matrix[tool.provider] = {"tool": tool.name, "strength": strength}
        return matrix

    def get_status(self) -> ToolStatus:
        if any(tool.get_status() == ToolStatus.AVAILABLE for tool in self._providers()):
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, object]) -> float:
        candidates = self._filter_candidates(inputs, self._providers())
        if not candidates:
            return 0.0
        tool, _ = self._select_best_tool(inputs, candidates, self._prepare_task_context(inputs))
        return tool.estimate_cost(inputs) if tool else 0.0

    def estimate_runtime(self, inputs: dict[str, object]) -> float:
        candidates = self._providers()
        if not candidates:
            return 0.0
        tool, _ = self._select_best_tool(inputs, candidates, self._prepare_task_context(inputs))
        return tool.estimate_runtime(inputs) if tool else 0.0

    def execute(self, inputs: dict[str, object]) -> ToolResult:
        from lib.scoring import rank_providers

        candidates = self._providers()

        # Rank mode — return scored provider rankings without generating
        if inputs.get("operation") == "rank":
            rank_inputs = self._rank_inputs(inputs)
            task_context = self._prepare_task_context(rank_inputs)
            candidates = self._filter_candidates(rank_inputs, candidates)
            rankings = rank_providers(candidates, task_context)
            return ToolResult(
                success=True,
                data={
                    "rankings": self._serialize_rankings(candidates, rankings),
                    "explanation": "\n".join(r.explain() for r in rankings[:5]),
                    "normalized_task_context": task_context,
                },
            )

        # Normal generation — strict/auxiliary reference semantics are explicit.
        adapted = dict(inputs)
        present_model_keys = [
            key for key in ("model", "model_version") if key in adapted
        ]
        invalid_model_keys = [
            key
            for key in present_model_keys
            if not isinstance(adapted[key], str) or not adapted[key]
        ]
        if invalid_model_keys:
            return ToolResult(
                success=False,
                error=(
                    "Selector preflight rejected non-empty string contract for: "
                    f"{invalid_model_keys}"
                ),
            )
        if len(present_model_keys) > 1:
            return ToolResult(
                success=False,
                error="Selector preflight rejects competing model and model_version selectors",
            )
        # `_reference_execution_plan` is an internal capability proof.  A
        # caller-supplied value is never authoritative and must not survive to
        # a provider. Canonical empty collections mean "no references" rather
        # than forcing a reference route or a zero-plan provider deadlock.
        adapted.pop("_reference_execution_plan", None)
        for collection_key in (
            "clp_reference_inputs",
            "auxiliary_reference_images",
        ):
            if adapted.get(collection_key) == []:
                adapted.pop(collection_key, None)
        if "clp_binding" in adapted and "binding" in adapted:
            from lib.clp_validator import UnsatisfiedReferenceConstraintsError

            raise UnsatisfiedReferenceConstraintsError(
                "CLP execution accepts exactly one binding key; do not provide both "
                "clp_binding and legacy binding"
            )
        if (
            adapted.get("clp_reference_inputs")
            or adapted.get("auxiliary_reference_images")
        ) and adapted.get("operation") != "reference_to_video":
            from lib.clp_validator import UnsatisfiedReferenceConstraintsError

            raise UnsatisfiedReferenceConstraintsError(
                "Structured CLP/auxiliary references require explicit "
                "operation='reference_to_video'"
            )

        # Authenticate and materialize the provider-independent CLP contract
        # before scoring providers. Some status probes perform real local HTTP
        # I/O (for example ComfyUI /system_stats); malformed provenance, wrong
        # bytes, missing references, or an all-provider slot overflow must stop
        # even before those probes.
        early_has_clp_context = any(
            key in adapted
            for key in (
                "clp_binding",
                "binding",
                "clp_manifest",
                "clp_shot_bindings",
                "clp_scene_plan",
                "clp_shot_id",
                "clp_reference_inputs",
                "auxiliary_reference_images",
            )
        )
        if early_has_clp_context:
            from lib.clp_validator import (
                canonical_digest,
                CLPValidationError,
                compile_attached_references,
                get_tool_reference_capability,
                load_authoritative_clp_shot,
                normalize_auxiliary_reference_inputs,
                present_image_reference_aliases,
                ReferenceSlotOverflowError,
                resolve_tool_reference_model_input,
                UnsatisfiedReferenceConstraintsError,
            )

            early_shot_id = adapted.get("clp_shot_id")
            early_project_dir = adapted.get("project_dir")
            if not isinstance(early_shot_id, str) or not early_shot_id:
                raise UnsatisfiedReferenceConstraintsError(
                    "CLP execution requires an independent non-empty clp_shot_id"
                )
            if not isinstance(early_project_dir, str) or not early_project_dir:
                raise UnsatisfiedReferenceConstraintsError(
                    "CLP execution requires authoritative project_dir"
                )
            loose_aliases = present_image_reference_aliases(adapted)
            if loose_aliases:
                raise UnsatisfiedReferenceConstraintsError(
                    "authoritative CLP execution: caller-supplied provider reference "
                    f"aliases are forbidden/unsupported before selection: {list(loose_aliases)}; use "
                    "clp_reference_inputs or auxiliary_reference_images"
                )
            early_binding = (
                adapted.get("clp_binding")
                if "clp_binding" in adapted
                else adapted.get("binding")
            )
            early_manifest = adapted.get("clp_manifest")
            if (early_binding is None) != (early_manifest is None):
                raise UnsatisfiedReferenceConstraintsError(
                    "Detached CLP caches must provide both clp_binding and clp_manifest"
                )
            try:
                early_context = load_authoritative_clp_shot(
                    early_project_dir, early_shot_id
                )
                cache_pairs = (
                    ("binding", early_binding, early_context.binding),
                    ("manifest", early_manifest, early_context.manifest),
                    (
                        "clp_shot_bindings",
                        adapted.get("clp_shot_bindings"),
                        early_context.bindings_doc,
                    ),
                    (
                        "clp_scene_plan",
                        adapted.get("clp_scene_plan"),
                        early_context.scene_plan,
                    ),
                )
                for label, supplied, authoritative in cache_pairs:
                    if supplied is not None and (
                        not isinstance(supplied, dict)
                        or canonical_digest(supplied) != canonical_digest(authoritative)
                    ):
                        raise CLPValidationError(
                            f"Caller {label} differs from authoritative persisted checkpoint"
                        )
                expected_strict_inputs = compile_attached_references(
                    early_context.binding,
                    early_context.manifest,
                    early_project_dir,
                    expected_shot_id=early_shot_id,
                )
                supplied_strict_inputs = adapted.get("clp_reference_inputs")
                if expected_strict_inputs:
                    if not isinstance(supplied_strict_inputs, list) or canonical_digest(
                        supplied_strict_inputs
                    ) != canonical_digest(expected_strict_inputs):
                        received_count = (
                            len(supplied_strict_inputs)
                            if isinstance(supplied_strict_inputs, list)
                            else 0
                        )
                        raise UnsatisfiedReferenceConstraintsError(
                            f"Shot {early_shot_id!r} requires exactly "
                            f"{len(expected_strict_inputs)} entity-bound strict references; "
                            f"received {received_count}; strict reference identity mismatch "
                            "with the materialized authoritative mapping"
                        )
                elif supplied_strict_inputs is not None:
                    raise UnsatisfiedReferenceConstraintsError(
                        "Shot has no strict entities but caller supplied strict references"
                    )
                normalized_auxiliary = normalize_auxiliary_reference_inputs(
                    adapted.get("auxiliary_reference_images"),
                    manifest=early_context.manifest,
                    project_dir=Path(early_project_dir),
                    strict_references=expected_strict_inputs,
                )
            except UnsatisfiedReferenceConstraintsError:
                raise
            except Exception as exc:
                raise UnsatisfiedReferenceConstraintsError(
                    f"CLP provenance validation failed before provider selection: {exc}"
                ) from exc

            adapted.pop("binding", None)
            adapted["clp_binding"] = early_context.binding
            adapted["clp_manifest"] = early_context.manifest
            adapted["clp_shot_bindings"] = early_context.bindings_doc
            adapted["clp_scene_plan"] = early_context.scene_plan
            required_slots = len(expected_strict_inputs) + len(normalized_auxiliary)
            if required_slots:
                routing_candidates = list(candidates)
                allowed = set(adapted.get("allowed_providers") or [])
                if allowed:
                    routing_candidates = [
                        candidate
                        for candidate in routing_candidates
                        if candidate.provider in allowed
                    ]
                preferred = adapted.get("preferred_provider", "auto")
                if preferred not in (None, "auto"):
                    routing_candidates = [
                        candidate
                        for candidate in routing_candidates
                        if candidate.provider == preferred
                    ]
                routing_candidates = self._filter_candidates(
                    adapted, routing_candidates
                )
                eligible = []
                resolved_capabilities = []
                for candidate in routing_candidates:
                    try:
                        candidate_model = resolve_tool_reference_model_input(
                            candidate, adapted
                        )
                        capability = get_tool_reference_capability(
                            candidate,
                            model=candidate_model,
                            operation=str(adapted.get("operation", "text_to_video")),
                            model_variant=adapted.get("model_variant"),
                        )
                    except Exception:
                        continue
                    resolved_capabilities.append(capability)
                    if (
                        (not expected_strict_inputs or capability.supported)
                        and capability.max_image_slots >= required_slots
                    ):
                        eligible.append(candidate)
                if not eligible:
                    capacity_candidates = [
                        capability
                        for capability in resolved_capabilities
                        if not expected_strict_inputs or capability.supported
                    ]
                    if capacity_candidates:
                        maximum_slots = max(
                            capability.max_image_slots
                            for capability in capacity_candidates
                        )
                        if maximum_slots < required_slots:
                            raise ReferenceSlotOverflowError(
                                f"Authenticated references require {required_slots} image slots, "
                                f"exceeding every eligible provider/model capacity ({maximum_slots}); "
                                "aborting before provider selection or side effects"
                            )
                    raise UnsatisfiedReferenceConstraintsError(
                        "Selected routing constraints do not expose a provider/model "
                        f"that supports all {required_slots} authenticated reference slots"
                    )
                candidates = eligible

        task_context = self._prepare_task_context(adapted)
        tool, score = self._select_best_tool(adapted, candidates, task_context)
        if tool is None:
            return ToolResult(success=False, error="No video generation provider available.")

        # Adapt input keys: stock tools use 'query' while generators use 'prompt'
        if hasattr(tool, 'input_schema'):
            required = tool.input_schema.get("properties", {})
            if "query" in required and "query" not in adapted:
                adapted["query"] = adapted.get("prompt", "")

        # CLP Strict Reference Capacity Preflight (fail-closed before upload or
        # provider execution).  Detached manifest/binding values are caches
        # only: authority is reloaded from the exact persisted checkpoints by
        # project_dir + an independently supplied clp_shot_id.
        clp_binding = (
            adapted.get("clp_binding")
            if "clp_binding" in adapted
            else adapted.get("binding")
        )
        clp_manifest = adapted.get("clp_manifest")
        has_clp_context = any(
            key in adapted
            for key in (
                "clp_binding",
                "binding",
                "clp_manifest",
                "clp_shot_bindings",
                "clp_scene_plan",
                "clp_shot_id",
                "clp_reference_inputs",
                "auxiliary_reference_images",
            )
        )

        if has_clp_context:
            from lib.clp_validator import (
                build_reference_execution_plan,
                canonical_digest,
                check_strict_reference_budget,
                CLPValidationError,
                get_tool_reference_capability,
                load_authoritative_clp_shot,
                resolve_tool_reference_model_input,
                structured_reference_inputs,
                UnsatisfiedReferenceConstraintsError,
            )

            shot_id = adapted.get("clp_shot_id")
            project_dir = adapted.get("project_dir")
            if not isinstance(shot_id, str) or not shot_id:
                raise UnsatisfiedReferenceConstraintsError(
                    "CLP execution requires an independent non-empty clp_shot_id"
                )
            if not isinstance(project_dir, str) or not project_dir:
                raise UnsatisfiedReferenceConstraintsError(
                    "CLP execution requires authoritative project_dir"
                )
            if (clp_binding is None) != (clp_manifest is None):
                raise UnsatisfiedReferenceConstraintsError(
                    "Detached CLP caches must provide both clp_binding and clp_manifest"
                )

            try:
                context = load_authoritative_clp_shot(project_dir, shot_id)
                if clp_binding is not None:
                    if not isinstance(clp_binding, dict) or canonical_digest(
                        clp_binding
                    ) != canonical_digest(context.binding):
                        raise CLPValidationError(
                            "Caller binding differs from the authoritative shot binding"
                        )
                    if not isinstance(clp_manifest, dict) or canonical_digest(
                        clp_manifest
                    ) != canonical_digest(context.manifest):
                        raise CLPValidationError(
                            "Caller manifest differs from checkpoint_clp.json"
                        )
                supplied_bindings = adapted.get("clp_shot_bindings")
                if supplied_bindings is not None and (
                    not isinstance(supplied_bindings, dict)
                    or canonical_digest(supplied_bindings)
                    != canonical_digest(context.bindings_doc)
                ):
                    raise CLPValidationError(
                        "Caller clp_shot_bindings differs from checkpoint_scene_plan.json"
                    )
                supplied_scene_plan = adapted.get("clp_scene_plan")
                if supplied_scene_plan is not None and (
                    not isinstance(supplied_scene_plan, dict)
                    or canonical_digest(supplied_scene_plan)
                    != canonical_digest(context.scene_plan)
                ):
                    raise CLPValidationError(
                        "Caller clp_scene_plan differs from checkpoint_scene_plan.json"
                    )
            except UnsatisfiedReferenceConstraintsError:
                raise
            except Exception as exc:
                raise UnsatisfiedReferenceConstraintsError(
                    "Strict CLP provenance validation failed before provider "
                    f"execution: {exc}"
                ) from exc

            clp_binding = context.binding
            clp_manifest = context.manifest
            adapted.pop("binding", None)
            adapted["clp_binding"] = clp_binding
            adapted["clp_manifest"] = clp_manifest
            adapted["clp_shot_bindings"] = context.bindings_doc
            adapted["clp_scene_plan"] = context.scene_plan

            # Auto-routing must consider the authenticated hard-set before it
            # commits to an adapter. A generic tool can advertise a broad
            # reference operation without implementing the typed CLP contract;
            # prefer a capable candidate when routing is automatic, while an
            # explicit provider/model choice remains fail-closed.
            bound_slot_count = (
                len(clp_binding.get("character_refs") or [])
                + (1 if clp_binding.get("location_ref") else 0)
                + len(clp_binding.get("prop_refs") or [])
            )
            strict_count = check_strict_reference_budget(
                shot_id,
                clp_binding,
                clp_manifest,
                max_slots=bound_slot_count,
            )
            auxiliary_value = adapted.get("auxiliary_reference_images")
            auxiliary_count = len(auxiliary_value) if isinstance(auxiliary_value, list) else 0
            required_reference_slots = strict_count + auxiliary_count
            if strict_count and adapted.get("operation") != "reference_to_video":
                raise UnsatisfiedReferenceConstraintsError(
                    "Persisted strict CLP entities require operation='reference_to_video'"
                )

            def _candidate_fits_reference_contract(candidate: BaseTool) -> bool:
                try:
                    candidate_model = resolve_tool_reference_model_input(candidate, adapted)
                    capability = get_tool_reference_capability(
                        candidate,
                        model=candidate_model,
                        operation=str(adapted.get("operation", "text_to_video")),
                        model_variant=adapted.get("model_variant"),
                    )
                except Exception:
                    return False
                return (
                    (not strict_count or capability.supported)
                    and capability.max_image_slots >= required_reference_slots
                )

            if required_reference_slots and not _candidate_fits_reference_contract(tool):
                preferred = adapted.get("preferred_provider", "auto")
                explicit_route = (
                    preferred not in (None, "auto")
                    or adapted.get("model") is not None
                    or adapted.get("model_version") is not None
                )
                if not explicit_route:
                    eligible = [
                        candidate
                        for candidate in candidates
                        if _candidate_fits_reference_contract(candidate)
                    ]
                    rerouted, reroute_score = self._select_best_tool(
                        adapted, eligible, task_context
                    )
                    if rerouted in eligible:
                        tool, score = rerouted, reroute_score

            # Strict references have one authoritative shape. Provider aliases
            # are rejected here and populated only after the plan is verified.
            structured_references = adapted.get("clp_reference_inputs")
            loose_references = self._extract_actual_references(adapted)
            if loose_references:
                raise UnsatisfiedReferenceConstraintsError(
                    "Provider reference aliases are forbidden whenever CLP context is "
                    "present; use clp_reference_inputs for identity references or "
                    "auxiliary_reference_images for non-identity references"
                )
            model_param = resolve_tool_reference_model_input(tool, adapted)

            try:
                plan = build_reference_execution_plan(
                    tool=tool,
                    shot_id=shot_id,
                    binding=clp_binding,
                    manifest=clp_manifest,
                    operation=adapted.get("operation", "text_to_video"),
                    model=model_param,
                    actual_references=structured_references,
                    model_variant=adapted.get("model_variant"),
                    auxiliary_references=adapted.get("auxiliary_reference_images"),
                    project_dir=project_dir,
                    bindings_doc=context.bindings_doc,
                    scene_plan=context.scene_plan,
                )
            except UnsatisfiedReferenceConstraintsError:
                raise
            except Exception as exc:
                # The selector is an executable provider boundary.  Normalize
                # schema/semantic failures into the same operational error as
                # missing or over-budget strict references, while retaining the
                # precise diagnostic and guaranteeing no upload/API side effect.
                raise UnsatisfiedReferenceConstraintsError(
                    f"Strict CLP reference validation failed before provider execution: {exc}"
                ) from exc
            if plan.strict_count or plan.auxiliary_references:
                self._clear_image_reference_aliases(adapted)
                adapted[plan.canonical_input_key] = [
                    *(mapping.materialized_input for mapping in plan.slot_mappings),
                    *plan.auxiliary_references,
                ]
                adapted["clp_reference_inputs"] = structured_reference_inputs(plan)
                adapted["_reference_execution_plan"] = plan

        # Auto-resolve reference_image_path to a URL for providers that need it
        if adapted.get("operation") == "image_to_video" and adapted.get("reference_image_path"):
            tool_props = getattr(tool, "input_schema", {}).get("properties", {})
            # If the provider uses image_url (not reference_image_path), upload and convert
            if "image_url" in tool_props and "image_url" not in adapted:
                try:
                    from tools.video._shared import upload_image_fal
                    adapted["image_url"] = upload_image_fal(adapted["reference_image_path"])
                except Exception as e:
                    return ToolResult(success=False, error=f"Failed to upload reference image: {e}")

        result = tool.execute(adapted)
        if result.success:
            result.data.setdefault("selected_tool", tool.name)
            result.data["selected_provider"] = tool.provider
            result.data["selection_reason"] = score.explain() if score else f"Selected {tool.provider} ({tool.name})"
            if score:
                result.data["provider_score"] = score.to_dict()
            result.data.update(self._tool_context_payload(tool))
            result.data["alternatives_considered"] = [
                t.name for t in candidates
                if t.name != tool.name and t.get_status().value == "available"
            ]
            # Input-aware fallback list (drops image_selector for motion-required briefs).
            result.data.setdefault("fallback_tools", self.fallback_tools_for(adapted))
        return result

    @staticmethod
    def _clear_image_reference_aliases(inputs: dict[str, object]) -> None:
        """Remove ambiguous aliases before writing the adapter's canonical key."""
        for key in (
            "reference_image_path",
            "image_path",
            "image_url",
            "reference_image_url",
            "first_frame_path",
            "start_image_url",
            "image",
            "reference_image_paths",
            "reference_image_urls",
            "image_paths",
            "image_urls",
            "reference_images",
        ):
            inputs.pop(key, None)

    @staticmethod
    def _extract_actual_references(inputs: dict[str, Any]) -> list[str]:
        """Normalize all provider reference input keys into an ordered list of reference inputs."""
        refs: list[str] = []
        # 1. Singular path/URL keys
        for k in (
            "reference_image_path",
            "image_path",
            "image_url",
            "reference_image_url",
            "first_frame_path",
            "start_image_url",
            "image",
        ):
            v = inputs.get(k)
            if isinstance(v, str) and v.strip() and v not in refs:
                refs.append(v.strip())

        # 2. Plural path/URL lists
        for k in (
            "reference_image_paths",
            "reference_image_urls",
            "image_paths",
            "image_urls",
        ):
            v_list = inputs.get(k)
            if isinstance(v_list, list):
                for item in v_list:
                    if isinstance(item, str) and item.strip() and item not in refs:
                        refs.append(item.strip())

        # 3. reference_images structured objects or strings
        ref_imgs = inputs.get("reference_images")
        if isinstance(ref_imgs, list):
            for item in ref_imgs:
                if isinstance(item, str) and item.strip() and item not in refs:
                    refs.append(item.strip())
                elif isinstance(item, dict):
                    path_or_url = item.get("path") or item.get("url") or item.get("image")
                    if isinstance(path_or_url, str) and path_or_url.strip() and path_or_url not in refs:
                        refs.append(path_or_url.strip())

        return refs

    def _select_best_tool(
        self,
        inputs: dict[str, object],
        candidates: list[BaseTool],
        task_context: dict[str, object],
    ) -> tuple[BaseTool | None, object]:
        """Select the best provider using scored ranking.

        Respects preferred_provider and environment hints as tie-breakers,
        but the scoring engine drives the primary selection.
        """
        from lib.scoring import rank_providers

        preferred = inputs.get("preferred_provider", "auto")
        allowed = set(inputs.get("allowed_providers") or [])
        if allowed:
            candidates = [tool for tool in candidates if tool.provider in allowed]
        candidates = self._filter_candidates(inputs, candidates)

        env_hint = os.environ.get("VIDEO_GEN_LOCAL_MODEL", "").lower()
        env_map = {
            "wan2.2-ti2v-5b": "wan",
            "wan2.2-t2v-a14b": "wan",
            "wan2.2-i2v-a14b": "wan",
            "wan2.1-1.3b": "wan",
            "wan2.1-14b": "wan",
            "hunyuan-1.5": "hunyuan",
            "ltx2-local": "ltx",
            "cogvideo-5b": "cogvideo",
            "cogvideo-2b": "cogvideo",
        }
        if preferred == "auto" and env_hint in env_map:
            preferred = env_map[env_hint]

        rankings = rank_providers(candidates, task_context)

        # Selectable tools, keyed by NAME (not provider). Keying by provider
        # string shadowed one of two tools that legitimately share a provider —
        # e.g. seedance_video (fal) and seedance_replicate both have
        # provider="seedance", so only the first-registered was ever reachable.
        # Keying by name keeps every backend selectable; ranking picks the best.
        selectable_by_name: dict[str, BaseTool] = {
            tool.name: tool for tool in candidates if self._tool_selectable(tool, inputs)
        }

        def _tool_for(score: object) -> BaseTool | None:
            return selectable_by_name.get(getattr(score, "tool_name", None))

        # If a preferred provider is explicitly requested, honor it ONLY when its
        # best ranked tool is within a configurable score gap of the overall top.
        # The prior code returned the preferred provider on the first ranking
        # match regardless of how far below the top it scored (the comment
        # claimed "unless drastically worse" but no gate enforced it).
        if preferred != "auto" and rankings:
            try:
                gap = float(inputs.get("preferred_provider_gap", self.PREFERRED_PROVIDER_GAP))
            except (TypeError, ValueError):
                gap = self.PREFERRED_PROVIDER_GAP
            top_score = rankings[0].weighted_score
            preferred_score = next(
                (s for s in rankings if s.provider == preferred and _tool_for(s) is not None),
                None,
            )
            if preferred_score is not None and preferred_score.weighted_score >= top_score - gap:
                return _tool_for(preferred_score), preferred_score

        # Return the highest-scored selectable provider
        for score in rankings:
            tool = _tool_for(score)
            if tool is not None:
                return tool, score

        return None, None

    def _prepare_task_context(self, inputs: dict[str, object]) -> dict[str, object]:
        from lib.scoring import normalize_task_context

        return normalize_task_context(
            inputs.get("task_context", {}),
            prompt=str(inputs.get("prompt", "")),
            capability=self.capability,
            operation=str(inputs.get("operation", "text_to_video")),
        )

    @staticmethod
    def _rank_inputs(inputs: dict[str, object]) -> dict[str, object]:
        rank_inputs = dict(inputs)
        rank_inputs["operation"] = inputs.get("target_operation", "text_to_video")
        return rank_inputs

    @staticmethod
    def _tool_context_payload(tool: BaseTool) -> dict[str, object]:
        info = tool.get_info()
        return {
            "selected_tool_agent_skills": info.get("agent_skills", []),
            "required_agent_skills": info.get("agent_skills", []),
            "selected_tool_usage_location": info.get("usage_location"),
            "selected_tool_best_for": info.get("best_for", []),
        }

    def _serialize_rankings(self, candidates: list[BaseTool], rankings: list[object]) -> list[dict[str, object]]:
        tool_by_name = {tool.name: tool for tool in candidates}
        serialized: list[dict[str, object]] = []
        for score in rankings:
            item = score.to_dict()
            tool = tool_by_name.get(score.tool_name)
            if tool:
                info = tool.get_info()
                item["agent_skills"] = info.get("agent_skills", [])
                item["usage_location"] = info.get("usage_location")
                item["best_for"] = info.get("best_for", [])
                item["supports"] = info.get("supports", {})
                item["status"] = str(tool.get_status())
            serialized.append(item)
        return serialized

    def _filter_candidates(
        self,
        inputs: dict[str, object],
        candidates: list[BaseTool],
    ) -> list[BaseTool]:
        exact_model = inputs.get("model")
        exact_version = inputs.get("model_version")
        if exact_model is not None and exact_version is not None:
            return []
        if exact_version is not None:
            version_matches = [
                tool
                for tool in candidates
                if getattr(tool, "reference_model_input_key", None) == "model_version"
                and exact_version
                in getattr(tool, "input_schema", {})
                .get("properties", {})
                .get("model_version", {})
                .get("enum", [])
            ]
            if not version_matches:
                return []
            candidates = version_matches
        if exact_model:
            model_matches = [
                tool for tool in candidates
                if exact_model in getattr(tool, "input_schema", {}).get("properties", {}).get("model", {}).get("enum", [])
                or exact_model in tool.get_info().get("model_catalog", {})
            ]
            if model_matches:
                candidates = model_matches
            else:
                return []

        # A caller-supplied custom workflow is provider-specific (ComfyUI graph
        # JSON). Route it only to custom-workflow-capable providers whose server
        # is reachable — bundled-model readiness is irrelevant in that case.
        if self._has_custom_workflow(inputs):
            return [t for t in candidates if self._custom_workflow_eligible(t, inputs)]

        operation = inputs.get("operation", "text_to_video")
        if operation == "rank":
            operation = inputs.get("target_operation", "text_to_video")

        filtered: list[BaseTool] = []
        matched_operation = False
        for tool in candidates:
            supports = getattr(tool, "supports", {})
            props = getattr(tool, "input_schema", {}).get("properties", {})

            if operation == "image_to_video":
                if supports.get("image_to_video") or "image_url" in props or "reference_image_url" in props:
                    matched_operation = True
                    if self._operation_ready(tool, "image_to_video"):
                        filtered.append(tool)
                continue

            if operation == "reference_to_video":
                has_typed_reference_contract = any(
                    callable(cls.__dict__.get("get_reference_capability"))
                    or callable(cls.__dict__.get("get_reference_capacity"))
                    for cls in type(tool).__mro__
                )
                if (
                    supports.get("reference_to_video")
                    or "reference_image_urls" in props
                    or has_typed_reference_contract
                ):
                    matched_operation = True
                    filtered.append(tool)
                continue

            matched_operation = True
            if self._operation_ready(tool, str(operation)):
                filtered.append(tool)

        return filtered if matched_operation else candidates

    @staticmethod
    def _operation_ready(tool: BaseTool, operation: str) -> bool:
        checker = getattr(tool, "is_operation_available", None)
        if not callable(checker):
            return True
        return bool(checker(operation))

    @staticmethod
    def _has_custom_workflow(inputs: dict[str, object]) -> bool:
        return bool(inputs.get("workflow_json") or inputs.get("workflow_path"))

    def _custom_workflow_eligible(self, tool: BaseTool, inputs: dict[str, object]) -> bool:
        """Whether a tool can run the caller-supplied custom workflow.

        Eligibility is based on server availability, not bundled-model readiness:
        a provider qualifies when it advertises ``custom_workflow`` support, an
        ``output_node`` is supplied, and its backend is reachable (status is not
        UNAVAILABLE).
        """
        if not self._has_custom_workflow(inputs):
            return False
        if not inputs.get("output_node"):
            return False
        supports = getattr(tool, "supports", {})
        if not supports.get("custom_workflow"):
            return False
        return tool.get_status() != ToolStatus.UNAVAILABLE

    def _tool_selectable(self, tool: BaseTool, inputs: dict[str, object]) -> bool:
        """A provider is selectable if it is AVAILABLE, or if it can serve a
        caller-supplied custom workflow even while bundled models report DEGRADED."""
        if tool.get_status() == ToolStatus.AVAILABLE:
            return True
        return self._custom_workflow_eligible(tool, inputs)
