# -*- coding: utf-8 -*-
"""CLP Semantic and Referential Integrity Validator for OpenMontage."""

from __future__ import annotations

import hashlib
import hmac
import json
import re
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from lib.identity import resolve_project_dir, validate_project_id

SHA256_REGEX = re.compile(r"^sha256:[0-9a-f]{64}$")
_REMOTE_REFERENCE_PREFIXES = ("http://", "https://", "data:", "asset://")
_IMAGE_REFERENCE_ALIASES = frozenset(
    {
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
        # Atlas H3's provider-native mixed-media envelope can otherwise
        # override the verified canonical strict image collection.
        "refers",
    }
)
CANONICAL_JSON_VERSION = "openmontage-json-v1"


def present_image_reference_aliases(
    inputs: dict[str, Any],
    *,
    allowed: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Return caller-supplied provider image aliases outside an allow-list.

    Presence, rather than truthiness, is authoritative: an explicit empty or
    malformed alias must not create a second interpretation of a CLP request.
    Selector and final provider gateways share this helper so alias injection
    is rejected consistently on both sides of the execution plan.
    """
    if not isinstance(inputs, dict):
        raise UnsatisfiedReferenceConstraintsError(
            "Reference submission inputs must be an object"
        )
    return tuple(
        sorted(
            key
            for key in _IMAGE_REFERENCE_ALIASES - set(allowed)
            if key in inputs
        )
    )


class CLPValidationError(ValueError):
    """Raised when CLP manifest or sidecar bindings violate semantic constraints."""
    pass


class UnsatisfiedReferenceConstraintsError(RuntimeError):
    """Raised when strict reference count exceeds the provider's physical slot limit."""
    pass


class ReferenceSlotOverflowError(UnsatisfiedReferenceConstraintsError):
    """Raised when materialized references exceed a provider's declared capacity."""
    pass


def canonical_json_bytes(obj: Any) -> bytes:
    """Produce the one canonical artifact representation used for provenance.

    Version ``openmontage-json-v1`` is intentionally a single compact encoding.
    Accepting both pretty and
    compact JSON hashes makes the provenance boundary ambiguous and permits two
    digests for the same logical artifact.
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_digest(obj: Any) -> str:
    """Produce a deterministic digest of compact canonical JSON."""
    return f"sha256:{hashlib.sha256(canonical_json_bytes(obj)).hexdigest()}"


def matches_digest(expected: str, obj: Any) -> bool:
    """Verify *only* the canonical compact-JSON digest of ``obj``."""
    if not isinstance(expected, str) or not SHA256_REGEX.fullmatch(expected):
        return False
    return hmac.compare_digest(canonical_digest(obj), expected)


@dataclass(frozen=True)
class ReferenceCapability:
    """Exact provider/model/operation contract for strict image references."""

    provider: str
    tool_name: str
    operation: str
    resolved_model: str
    max_image_slots: int
    strict_clp_supported: bool
    canonical_input_key: str = "reference_images"
    accepted_input_keys: tuple[str, ...] = ("reference_images",)
    provider_payload_key: str = "reference_images"

    @property
    def supported(self) -> bool:
        """Compatibility alias for strict CLP support, not raw slot capacity."""
        return self.strict_clp_supported


@dataclass(frozen=True)
class ReferenceSlotMapping:
    """Explicit mapping from bound strict entity to physical provider slot and input."""
    entity_id: str
    slot_index: int
    asset_sha256: str
    materialized_input: str
    source_kind: str = "path"


@dataclass(frozen=True)
class ReferenceExecutionPlan:
    """Rigid execution plan constructed before making any media upload or API calls."""
    provider: str
    tool_name: str
    operation: str
    model: str
    max_slots: int
    strict_count: int
    strict_entity_ids: tuple[str, ...]
    ordered_digests: tuple[str, ...]
    slot_mappings: tuple[ReferenceSlotMapping, ...]
    binding_sha256: str
    canonical_input_key: str = "reference_images"
    provider_payload_key: str = "reference_images"
    auxiliary_references: tuple[str, ...] = ()
    shot_id: str = ""
    project_id: str = ""
    manifest_sha256: str = ""
    bindings_sha256: str = ""
    scene_plan_sha256: str = ""


@dataclass(frozen=True)
class AuthoritativeCLPShot:
    """One shot resolved from the exact persisted CLP checkpoint chain."""

    project_id: str
    pipeline_type: str
    shot_id: str
    manifest: dict[str, Any]
    bindings_doc: dict[str, Any]
    scene_plan: dict[str, Any]
    binding: dict[str, Any]


_SHOT_BINDING_KEYS = frozenset(
    {"shot_id", "location_ref", "character_refs", "prop_refs", "focal_entity"}
)


def _validate_single_shot_binding_contract(
    binding: Any,
    *,
    shot_id: str,
    manifest: dict[str, Any],
) -> None:
    """Validate the exact executable subset of one shot-binding sidecar row."""
    if not isinstance(binding, dict):
        raise CLPValidationError("Shot binding must be a JSON object")
    extra_keys = set(binding) - _SHOT_BINDING_KEYS
    if extra_keys:
        raise CLPValidationError(
            f"Shot binding contains unsupported fields: {sorted(map(str, extra_keys))}"
        )
    bound_shot_id = binding.get("shot_id")
    if not isinstance(bound_shot_id, str) or not bound_shot_id:
        raise CLPValidationError("Shot binding requires a non-empty string shot_id")
    if bound_shot_id != shot_id:
        raise CLPValidationError(
            f"Shot binding identity mismatch: expected shot_id={shot_id!r}, "
            f"got {bound_shot_id!r}"
        )
    errors = validate_clp_shot_bindings_semantics(
        {"bindings": [binding]}, manifest=manifest
    )
    if errors:
        raise CLPValidationError("; ".join(errors))


def resolve_and_validate_strict_asset(
    item: dict[str, Any],
    cat: str,
    project_root: Path,
) -> list[str]:
    """Validate that a strict_reference asset image exists, is a regular file within project_root, and matches its SHA-256.

    Enforces:
    1. Rejects absolute paths, drive letters, leading slashes or backslashes.
    2. Rejects path traversal components like '..'.
    3. Resolves strictly relative to project_root without fallback to repo root or cwd.
    4. Prohibits symlink / junction escapes outside project_root.
    5. Checks regular file existence and binary SHA-256 match.
    """
    errors: list[str] = []
    item_id = item.get("id", "unknown")
    raw_path = item.get("image")
    expected_sha256 = item.get("asset_sha256")

    if not raw_path:
        errors.append(f"{cat}['{item_id}']: policy='strict_reference' requires 'image'")
        return errors
    if not expected_sha256:
        errors.append(f"{cat}['{item_id}']: policy='strict_reference' requires 'asset_sha256'")
        return errors

    if not isinstance(raw_path, str) or not raw_path.strip():
        errors.append(f"{cat}['{item_id}']: policy='strict_reference' requires non-empty string 'image'")
        return errors

    # Check for absolute paths, drive letters, and leading slashes/backslashes
    if (
        raw_path.startswith("/")
        or raw_path.startswith("\\")
        or (len(raw_path) > 1 and raw_path[1] == ":")
        or Path(raw_path).is_absolute()
    ):
        errors.append(f"{cat}['{item_id}']: absolute path forbidden in image path: {raw_path!r}")
        return errors

    # Check for path traversal attempts like '..'
    path_obj = Path(raw_path)
    if ".." in path_obj.parts or ".." in raw_path.replace("\\", "/").split("/"):
        errors.append(f"{cat}['{item_id}']: path traversal forbidden in image path: {raw_path!r}")
        return errors

    # Strict project root containment
    resolved_root = project_root.resolve()
    target_path = resolved_root / path_obj
    try:
        resolved_target = target_path.resolve()
    except OSError as e:
        errors.append(f"{cat}['{item_id}']: failed to resolve asset path {raw_path!r}: {e}")
        return errors

    # Check containment - strictly prevents symlink / junction escape outside project root
    try:
        resolved_target.relative_to(resolved_root)
    except ValueError:
        errors.append(
            f"{cat}['{item_id}']: asset path escapes project root: {raw_path!r} -> {resolved_target}"
        )
        return errors

    # Check that target is a regular file
    if not resolved_target.is_file():
        errors.append(
            f"{cat}['{item_id}']: strict_reference image file not found in project root: {raw_path!r}"
        )
        return errors

    # Verify regular file binary SHA-256
    try:
        data = resolved_target.read_bytes()
        actual_hash = f"sha256:{hashlib.sha256(data).hexdigest()}"
        if actual_hash != expected_sha256:
            errors.append(
                f"{cat}['{item_id}']: strict_reference bytes mismatch; asset_sha256 "
                f"(expected {expected_sha256!r}, got {actual_hash!r})"
            )
    except OSError as e:
        errors.append(f"{cat}['{item_id}']: failed to read asset file {resolved_target}: {e}")

    return errors


def validate_clp_manifest_semantics(
    manifest: dict[str, Any],
    project_dir: Optional[Path] = None,
) -> list[str]:
    """Validate semantic rules of a CLP manifest beyond basic JSON Schema.

    Rules:
    1. Character, Location, and Prop IDs must be globally unique across all categories.
    2. Entities with policy='strict_reference' must provide image and asset_sha256,
       and the image must safely resolve to an existing regular file matching asset_sha256 within project_root.
    3. Entities with policy='text_anchor_only' must provide prompt_anchor.
    ``policy`` is the sole runtime source of truth.  Legacy ``strict_lock`` is
    deliberately ignored here so two fields can never disagree at execution time.
    """
    errors: list[str] = []

    project_id = manifest.get("project_id")
    resolved_project_root: Optional[Path] = None
    if project_dir:
        try:
            project_id = validate_project_id(project_id)
        except ValueError:
            errors.append(f"Invalid project_id format: {project_id!r}")
        else:
            candidate_root = Path(project_dir).resolve()
            if candidate_root.name != project_id:
                errors.append(
                    f"manifest.project_id {project_id!r} does not match "
                    f"project_dir name {candidate_root.name!r}"
                )
            else:
                resolved_project_root = candidate_root
    elif project_id:
        try:
            validate_project_id(project_id)
        except ValueError:
            errors.append(f"Invalid project_id format: {project_id!r}")

    seen_all_ids: dict[str, str] = {}  # id -> category

    for cat in ("characters", "locations", "props"):
        for idx, item in enumerate(manifest.get(cat, [])):
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            if not item_id:
                errors.append(f"{cat}[{idx}]: missing id")
                continue
            if item_id in seen_all_ids:
                errors.append(
                    f"{cat}[{idx}]: duplicate id '{item_id}' (already defined in '{seen_all_ids[item_id]}')"
                )
            else:
                seen_all_ids[item_id] = cat

            policy = item.get("policy", "strict_reference")
            if policy == "strict_reference":
                if not item.get("image"):
                    errors.append(f"{cat}['{item_id}']: policy='strict_reference' requires 'image'")
                if not item.get("asset_sha256"):
                    errors.append(f"{cat}['{item_id}']: policy='strict_reference' requires 'asset_sha256'")
                if item.get("image") and item.get("asset_sha256"):
                    if not resolved_project_root:
                        errors.append(
                            f"{cat}['{item_id}']: cannot resolve strict asset without an "
                            "explicit project_dir matching manifest.project_id"
                        )
                    else:
                        asset_errs = resolve_and_validate_strict_asset(
                            item,
                            cat,
                            project_root=resolved_project_root,
                        )
                        errors.extend(asset_errs)
            elif policy == "text_anchor_only":
                if not item.get("prompt_anchor"):
                    errors.append(f"{cat}['{item_id}']: policy='text_anchor_only' requires 'prompt_anchor'")

    return errors


def validate_clp_manifest_or_raise(
    manifest: dict[str, Any],
    project_dir: Optional[Path] = None,
) -> None:
    """Validate CLP manifest semantics and raise CLPValidationError if any violation exists."""
    errors = validate_clp_manifest_semantics(manifest, project_dir=project_dir)
    if errors:
        raise CLPValidationError(f"CLP Manifest semantic validation failed: {'; '.join(errors)}")


def validate_clp_shot_bindings_semantics(
    bindings_doc: dict[str, Any],
    manifest: Optional[dict[str, Any]] = None,
    scene_plan: Optional[dict[str, Any]] = None,
) -> list[str]:
    """Validate that shot bindings do not contain dangling references or duplicate shot bindings.

    Rules:
    1. Each shot_id in bindings must be unique (no duplicate bindings for the same shot).
    2. character_refs must exist in manifest.characters.
    3. location_ref must exist in manifest.locations.
    4. prop_refs must exist in manifest.props.
    5. focal_entity must be in the bound entities for that shot.
    6. Exact coverage: if scene_plan is provided, every scene in scene_plan must have
       exactly one binding in bindings_doc, and no unexpected shot_ids may exist.
    7. Digest cross-checks: verified against canonical digests of manifest and scene_plan.
    """
    errors: list[str] = []

    valid_char_ids = set()
    valid_loc_ids = set()
    valid_prop_ids = set()
    if manifest:
        valid_char_ids = {c["id"] for c in manifest.get("characters", []) if isinstance(c, dict) and "id" in c}
        valid_loc_ids = {
            location["id"]
            for location in manifest.get("locations", [])
            if isinstance(location, dict) and "id" in location
        }
        valid_prop_ids = {p["id"] for p in manifest.get("props", []) if isinstance(p, dict) and "id" in p}

    valid_shot_ids: Optional[set[str]] = None
    if scene_plan and isinstance(scene_plan.get("scenes"), list):
        seen_sp_scenes: set[str] = set()
        for s in scene_plan["scenes"]:
            if isinstance(s, dict):
                sid = s.get("id") or s.get("scene_id") or s.get("name")
                if sid:
                    if sid in seen_sp_scenes:
                        errors.append(f"scene_plan contains duplicate scene ID: {sid!r}")
                    seen_sp_scenes.add(sid)
        valid_shot_ids = seen_sp_scenes

    # Digest cross-checks using canonical digest
    if manifest and isinstance(manifest, dict):
        bound_m_hash = bindings_doc.get("clp_manifest_sha256")
        if bound_m_hash and not matches_digest(bound_m_hash, manifest):
            expected_m_hash = canonical_digest(manifest)
            errors.append(
                f"clp_manifest_sha256 mismatch (expected {expected_m_hash}, got {bound_m_hash})"
            )

    if scene_plan and isinstance(scene_plan, dict):
        bound_sp_hash = bindings_doc.get("source_scene_plan_sha256")
        if bound_sp_hash and not matches_digest(bound_sp_hash, scene_plan):
            expected_sp_hash = canonical_digest(scene_plan)
            errors.append(
                f"source_scene_plan_sha256 mismatch (expected {expected_sp_hash}, got {bound_sp_hash})"
            )

    bindings_list = bindings_doc.get("bindings")
    if not isinstance(bindings_list, list) or len(bindings_list) == 0:
        if valid_shot_ids:
            errors.append(f"Bindings list is empty, but scene_plan expects shots: {sorted(valid_shot_ids)}")
        seen_shot_ids: set[str] = set()
    else:
        seen_shot_ids = set()
        for idx, b in enumerate(bindings_list):
            if not isinstance(b, dict):
                errors.append(f"Shot binding at index {idx} must be a JSON object")
                continue
            shot_id = b.get("shot_id") or f"index_{idx}"
            if shot_id in seen_shot_ids:
                errors.append(f"Duplicate shot binding for shot_id '{shot_id}'")
            seen_shot_ids.add(shot_id)

            if valid_shot_ids is not None and shot_id not in valid_shot_ids:
                errors.append(f"Shot binding '{shot_id}': shot_id not found in scene_plan")

            if manifest:
                loc_ref = b.get("location_ref")
                if loc_ref is not None and (
                    not isinstance(loc_ref, str) or not loc_ref
                ):
                    errors.append(
                        f"Shot '{shot_id}': location_ref must be a non-empty string"
                    )
                    loc_ref = None
                elif loc_ref and loc_ref not in valid_loc_ids:
                    errors.append(f"Shot '{shot_id}': dangling location_ref '{loc_ref}'")

                char_refs = b.get("character_refs") or []
                if not isinstance(char_refs, list) or any(
                    not isinstance(ref, str) or not ref for ref in char_refs
                ):
                    errors.append(
                        f"Shot '{shot_id}': character_refs must be an array of non-empty strings"
                    )
                    char_refs = []
                else:
                    if len(char_refs) != len(set(char_refs)):
                        errors.append(f"Shot '{shot_id}': duplicate character_refs are forbidden")
                    for cr in char_refs:
                        if cr not in valid_char_ids:
                            errors.append(f"Shot '{shot_id}': dangling character_ref '{cr}'")

                prop_refs = b.get("prop_refs") or []
                if not isinstance(prop_refs, list) or any(
                    not isinstance(ref, str) or not ref for ref in prop_refs
                ):
                    errors.append(
                        f"Shot '{shot_id}': prop_refs must be an array of non-empty strings"
                    )
                    prop_refs = []
                else:
                    if len(prop_refs) != len(set(prop_refs)):
                        errors.append(f"Shot '{shot_id}': duplicate prop_refs are forbidden")
                    for pr in prop_refs:
                        if pr not in valid_prop_ids:
                            errors.append(f"Shot '{shot_id}': dangling prop_ref '{pr}'")

                focal = b.get("focal_entity")
                if focal is not None and (
                    not isinstance(focal, str) or not focal
                ):
                    errors.append(
                        f"Shot '{shot_id}': focal_entity must be a non-empty string"
                    )
                elif focal:
                    bound_all = set(char_refs) | set(prop_refs)
                    if loc_ref:
                        bound_all.add(loc_ref)
                    if focal not in bound_all:
                        errors.append(f"Shot '{shot_id}': focal_entity '{focal}' is not bound to this shot")

    # Exact coverage check against scene_plan
    if valid_shot_ids is not None:
        missing_shots = valid_shot_ids - seen_shot_ids
        if missing_shots:
            errors.append(f"Missing shot bindings for scene-plan scenes: {sorted(missing_shots)}")
        unexpected_shots = seen_shot_ids - valid_shot_ids
        if unexpected_shots:
            errors.append(f"Unexpected shot bindings not in scene_plan: {sorted(unexpected_shots)}")

    return errors


def validate_clp_shot_bindings_or_raise(
    bindings_doc: dict[str, Any],
    manifest: Optional[dict[str, Any]] = None,
    scene_plan: Optional[dict[str, Any]] = None,
) -> None:
    """Validate CLP shot bindings semantics and raise CLPValidationError if violations exist."""
    errors = validate_clp_shot_bindings_semantics(bindings_doc, manifest, scene_plan)
    if errors:
        raise CLPValidationError(f"CLP Shot Bindings semantic validation failed: {'; '.join(errors)}")


def validate_clp_bundle_or_raise(
    artifacts: dict[str, Any],
    project_dir: Optional[Path] = None,
) -> None:
    """Entrypoint for checkpoint validation: verifies CLP manifest, candidates, and shot bindings."""
    manifest = artifacts.get("clp_manifest")
    bindings = artifacts.get("clp_shot_bindings")
    candidates = artifacts.get("clp_candidates")
    scene_plan = artifacts.get("scene_plan")

    if manifest and isinstance(manifest, dict):
        validate_clp_manifest_or_raise(manifest, project_dir=project_dir)

    if bindings and isinstance(bindings, dict):
        validate_clp_shot_bindings_or_raise(
            bindings,
            manifest=manifest if isinstance(manifest, dict) else None,
            scene_plan=scene_plan if isinstance(scene_plan, dict) else None,
        )

    # Cross-check project_ids
    project_ids = []
    for art in (manifest, bindings, candidates, scene_plan):
        if isinstance(art, dict) and art.get("project_id"):
            project_ids.append(art["project_id"])
    if len(set(project_ids)) > 1:
        raise CLPValidationError(
            f"CLP bundle project_id mismatch across artifacts: {project_ids}"
        )


def _declared_method(tool: Any, name: str) -> Any:
    """Return a method explicitly declared by a tool, never a mock child."""
    for cls in type(tool).__mro__:
        if name in cls.__dict__:
            method = getattr(tool, name)
            return method if callable(method) else None
    method = vars(tool).get(name)
    return method if callable(method) else None


def _declared_attribute(tool: Any, name: str) -> Any:
    """Return a real adapter attribute without accepting synthetic mock children."""
    for cls in type(tool).__mro__:
        if name in cls.__dict__:
            return getattr(tool, name)
    return vars(tool).get(name)


def resolve_tool_reference_model_input(
    tool: Any,
    inputs: dict[str, Any],
) -> Optional[str]:
    """Resolve the adapter's one authoritative model selector without aliases.

    Adapters should declare ``reference_model_input_key`` as either ``model`` or
    ``model_version``. Undeclared adapters retain a narrow compatibility path,
    but competing selectors are always rejected.
    """
    declared_key = _declared_attribute(tool, "reference_model_input_key")
    if declared_key is not None and declared_key not in {"model", "model_version"}:
        raise CLPValidationError(
            f"{getattr(tool, 'name', 'tool')} declared invalid reference_model_input_key "
            f"{declared_key!r}"
        )
    present = [
        key for key in ("model", "model_version") if inputs.get(key) is not None
    ]
    if declared_key is not None:
        foreign = [key for key in present if key != declared_key]
        if foreign:
            raise UnsatisfiedReferenceConstraintsError(
                f"{getattr(tool, 'name', 'tool')} accepts model selection only through "
                f"{declared_key!r}; competing selectors are forbidden: {foreign}"
            )
        value = inputs.get(declared_key)
    else:
        if len(present) > 1:
            raise UnsatisfiedReferenceConstraintsError(
                f"Ambiguous model selectors for {getattr(tool, 'name', 'tool')}: {present}"
            )
        value = inputs.get(present[0]) if present else None
    if value is not None and not isinstance(value, str):
        raise UnsatisfiedReferenceConstraintsError(
            f"Model selector must be a string, got {type(value).__name__}"
        )
    return value


def _validated_capacity(value: Any, *, context: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise CLPValidationError(f"{context} returned invalid reference capacity: {value!r}")
    return value


def _validate_reference_capability(
    capability: ReferenceCapability,
    *,
    requested_operation: str,
) -> ReferenceCapability:
    """Validate every field of an adapter capability without coercion."""
    context = capability.tool_name if isinstance(capability.tool_name, str) else "tool"
    for field_name in ("provider", "tool_name", "operation", "resolved_model"):
        value = getattr(capability, field_name)
        if not isinstance(value, str) or not value:
            raise CLPValidationError(
                f"{context} capability {field_name} must be a non-empty string"
            )
    if capability.operation != requested_operation:
        raise CLPValidationError(
            f"{context} capability operation mismatch: requested "
            f"{requested_operation!r}, got {capability.operation!r}"
        )
    _validated_capacity(
        capability.max_image_slots,
        context=f"{context}.get_reference_capability",
    )
    if type(capability.strict_clp_supported) is not bool:
        raise CLPValidationError(
            f"{context} capability strict_clp_supported must be boolean"
        )
    if not isinstance(capability.canonical_input_key, str) or not capability.canonical_input_key:
        raise CLPValidationError(
            f"{context} declared an empty canonical reference input key"
        )
    if not isinstance(capability.provider_payload_key, str) or not capability.provider_payload_key:
        raise CLPValidationError(f"{context} declared an empty provider payload key")
    if not isinstance(capability.accepted_input_keys, tuple) or not all(
        isinstance(key, str) and key for key in capability.accepted_input_keys
    ):
        raise CLPValidationError(
            f"{context} declared invalid accepted reference input keys"
        )
    if len(set(capability.accepted_input_keys)) != len(capability.accepted_input_keys):
        raise CLPValidationError(
            f"{context} declared duplicate accepted reference input keys"
        )
    if (
        capability.max_image_slots > 0
        and capability.canonical_input_key not in capability.accepted_input_keys
    ):
        raise CLPValidationError(
            f"{context} canonical reference key {capability.canonical_input_key!r} "
            "is absent from accepted_input_keys"
        )
    if capability.strict_clp_supported and capability.max_image_slots == 0:
        raise CLPValidationError(
            f"{context} cannot support strict CLP with zero image slots"
        )
    return capability


def get_tool_reference_capability(
    tool: Any,
    model: Optional[str] = None,
    operation: str = "text_to_video",
    model_variant: Optional[str] = None,
) -> ReferenceCapability:
    """Resolve an exact typed capability without provider-name heuristics.

    Production adapters implement ``get_reference_capability`` or an exact
    ``get_reference_capacity(model, operation)`` contract. Adapter errors
    propagate so unknown models cannot fall through to guessed capacity.
    """
    provider = str(getattr(tool, "provider", "unknown"))
    tool_name = str(getattr(tool, "name", "unknown"))
    capability_method = _declared_method(tool, "get_reference_capability")
    if capability_method is not None:
        raw = capability_method(
            model=model,
            operation=operation,
            model_variant=model_variant,
        )
        if isinstance(raw, ReferenceCapability):
            capability = raw
        elif isinstance(raw, dict):
            required_fields = {
                "operation",
                "resolved_model",
                "max_image_slots",
                "strict_clp_supported",
                "canonical_input_key",
                "accepted_input_keys",
                "provider_payload_key",
            }
            if set(raw) != required_fields:
                raise CLPValidationError(
                    f"{tool_name}.get_reference_capability must return exactly "
                    f"{sorted(required_fields)}, got {sorted(map(str, raw))}"
                )
            for field_name in (
                "operation",
                "resolved_model",
                "canonical_input_key",
                "provider_payload_key",
            ):
                if not isinstance(raw[field_name], str) or not raw[field_name]:
                    raise CLPValidationError(
                        f"{tool_name}.get_reference_capability field {field_name} "
                        "must be a non-empty string"
                    )
            if type(raw["strict_clp_supported"]) is not bool:
                raise CLPValidationError(
                    f"{tool_name}.get_reference_capability field "
                    "strict_clp_supported must be boolean"
                )
            accepted_keys = raw["accepted_input_keys"]
            if not isinstance(accepted_keys, (list, tuple)):
                raise CLPValidationError(
                    f"{tool_name}.get_reference_capability field "
                    "accepted_input_keys must be an array"
                )
            capability = ReferenceCapability(
                provider=provider,
                tool_name=tool_name,
                operation=raw["operation"],
                resolved_model=raw["resolved_model"],
                max_image_slots=_validated_capacity(
                    raw["max_image_slots"],
                    context=f"{tool_name}.get_reference_capability",
                ),
                strict_clp_supported=raw["strict_clp_supported"],
                canonical_input_key=raw["canonical_input_key"],
                accepted_input_keys=tuple(accepted_keys),
                provider_payload_key=raw["provider_payload_key"],
            )
        else:
            raise CLPValidationError(
                f"{tool_name}.get_reference_capability must return ReferenceCapability or dict, "
                f"got {type(raw).__name__}"
            )
        return _validate_reference_capability(
            capability,
            requested_operation=operation,
        )

    capacity_method = _declared_method(tool, "get_reference_capacity")
    if capacity_method is not None:
        capacity = _validated_capacity(
            capacity_method(
                model=model,
                operation=operation,
                model_variant=model_variant,
            ),
            context=f"{tool_name}.get_reference_capacity",
        )
    else:
        capacity = 0
    return ReferenceCapability(
        provider=provider,
        tool_name=tool_name,
        operation=operation,
        resolved_model=str(model or getattr(tool, "default_model", None) or "default"),
        max_image_slots=capacity,
        strict_clp_supported=False,
    )


def get_tool_reference_capacity(
    tool: Any,
    model: Optional[str] = None,
    operation: str = "text_to_video",
    model_variant: Optional[str] = None,
) -> int:
    """Return exact image-slot capacity for ``tool/model/operation``."""
    return get_tool_reference_capability(
        tool,
        model=model,
        operation=operation,
        model_variant=model_variant,
    ).max_image_slots


def _entity_indexes(manifest: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    indexes: dict[str, dict[str, dict[str, Any]]] = {}
    globally_seen: dict[str, str] = {}
    for category in ("characters", "locations", "props"):
        index: dict[str, dict[str, Any]] = {}
        values = manifest.get(category, [])
        if not isinstance(values, list):
            raise CLPValidationError(f"clp_manifest.{category} must be an array")
        for item in values:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                raise CLPValidationError(
                    f"clp_manifest.{category} contains an entity without a string id"
                )
            entity_id = item["id"]
            if entity_id in globally_seen:
                raise CLPValidationError(
                    f"Duplicate entity id {entity_id!r} in {category} and {globally_seen[entity_id]}"
                )
            globally_seen[entity_id] = category
            index[entity_id] = item
        indexes[category] = index
    return indexes


def _bound_strict_entities(
    shot_id: str,
    binding: dict[str, Any],
    manifest: dict[str, Any],
) -> list[tuple[str, dict[str, Any]]]:
    indexes = _entity_indexes(manifest)
    ordered: list[tuple[str, dict[str, Any]]] = []

    def add_many(key: str, category: str) -> None:
        refs = binding.get(key) or []
        if not isinstance(refs, list) or any(
            not isinstance(ref, str) or not ref for ref in refs
        ):
            raise CLPValidationError(
                f"Shot {shot_id!r} {key} must be an array of non-empty strings"
            )
        if len(refs) != len(set(refs)):
            raise CLPValidationError(
                f"Shot {shot_id!r} contains duplicate entity IDs in {key}: {refs}"
            )
        for entity_id in refs:
            entity = indexes[category].get(entity_id)
            if entity is None:
                raise CLPValidationError(
                    f"Shot {shot_id!r} has dangling {key} entity {entity_id!r}"
                )
            if entity.get("policy", "strict_reference") == "strict_reference":
                ordered.append((entity_id, entity))

    add_many("character_refs", "characters")
    location_id = binding.get("location_ref")
    if location_id is not None:
        if not isinstance(location_id, str) or not location_id:
            raise CLPValidationError(
                f"Shot {shot_id!r} location_ref must be a non-empty string"
            )
        location = indexes["locations"].get(location_id)
        if location is None:
            raise CLPValidationError(
                f"Shot {shot_id!r} has dangling location_ref {location_id!r}"
            )
        if location.get("policy", "strict_reference") == "strict_reference":
            ordered.append((location_id, location))
    add_many("prop_refs", "props")

    for entity_id, entity in ordered:
        digest = entity.get("asset_sha256")
        if not isinstance(digest, str) or not SHA256_REGEX.fullmatch(digest):
            raise CLPValidationError(
                f"Strict entity {entity_id!r} requires a lowercase sha256 asset_sha256"
            )
    return ordered


def check_strict_reference_budget(
    shot_id: str,
    binding: dict[str, Any],
    manifest: dict[str, Any],
    max_slots: int,
) -> int:
    """Check exact strict entity count against non-negative physical capacity."""
    max_slots = _validated_capacity(max_slots, context="reference capacity")
    strict_count = len(_bound_strict_entities(shot_id, binding, manifest))
    if strict_count > max_slots:
        raise ReferenceSlotOverflowError(
            f"Shot {shot_id!r} requires {strict_count} strict reference images, "
            f"exceeding downstream model slot capacity ({max_slots}); "
            "aborting before side effects"
        )
    return strict_count


def _reference_is_remote(value: str) -> bool:
    return value.lower().startswith(_REMOTE_REFERENCE_PREFIXES)


def _project_root(
    manifest: dict[str, Any],
    project_dir: Optional[Path],
) -> Path:
    project_id = validate_project_id(manifest.get("project_id"))
    if project_dir is None:
        raise UnsatisfiedReferenceConstraintsError(
            "CLP reference execution requires an explicit project_dir; global project "
            "directory fallback is forbidden at the provider boundary"
        )
    root = Path(project_dir).resolve()
    if root.name != project_id:
        raise CLPValidationError(
            f"manifest.project_id {project_id!r} does not match project_dir name {root.name!r}"
        )
    return root


def _resolve_local_reference(
    value: str,
    *,
    manifest: dict[str, Any],
    project_dir: Optional[Path],
) -> Path:
    source = Path(value)
    root = _project_root(manifest, project_dir)
    if not source.is_absolute():
        source = root / source
    try:
        resolved = source.resolve(strict=True)
    except OSError as exc:
        raise UnsatisfiedReferenceConstraintsError(
            f"Strict reference file cannot be resolved: {value!r}: {exc}"
        ) from exc
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise UnsatisfiedReferenceConstraintsError(
            f"Strict reference path escapes project root: {value!r} -> {resolved}"
        ) from exc
    if not resolved.is_file():
        raise UnsatisfiedReferenceConstraintsError(
            f"Strict reference is not a regular file: {resolved}"
        )
    return resolved


def _file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise UnsatisfiedReferenceConstraintsError(
            f"Cannot read strict reference {path}: {exc}"
        ) from exc
    return f"sha256:{digest.hexdigest()}"


def _materialize_reference_mappings(
    *,
    shot_id: str,
    strict_entities: list[tuple[str, dict[str, Any]]],
    actual_references: Optional[list[Any]],
    manifest: dict[str, Any],
    project_dir: Optional[Path],
) -> tuple[ReferenceSlotMapping, ...]:
    references = [] if actual_references is None else actual_references
    if not isinstance(references, list):
        raise UnsatisfiedReferenceConstraintsError("clp_reference_inputs must be an array")
    if len(references) != len(strict_entities):
        raise UnsatisfiedReferenceConstraintsError(
            f"Shot {shot_id!r} requires exactly {len(strict_entities)} entity-bound "
            f"strict references; received {len(references)}. Extra references must "
            "use auxiliary_reference_images."
        )

    mappings: list[ReferenceSlotMapping] = []
    seen_entity_ids: set[str] = set()
    seen_sources: set[str] = set()
    for slot_index, ((expected_id, entity), supplied) in enumerate(
        zip(strict_entities, references)
    ):
        expected_digest = entity["asset_sha256"]
        if not isinstance(supplied, dict) or set(supplied) != {
            "entity_id", "asset_sha256", "path"
        }:
            raise UnsatisfiedReferenceConstraintsError(
                f"Strict reference {slot_index} must contain exactly "
                "entity_id, asset_sha256, and path; remote/bare strict inputs are forbidden"
            )
        entity_id = supplied.get("entity_id")
        declared_digest = supplied.get("asset_sha256")
        raw_source = supplied.get("path")
        if not isinstance(raw_source, str) or not raw_source:
            raise UnsatisfiedReferenceConstraintsError(
                f"Strict reference path at slot {slot_index} must be a non-empty string"
            )
        if entity_id != expected_id:
            raise UnsatisfiedReferenceConstraintsError(
                f"Strict reference order/identity mismatch at slot {slot_index}: "
                f"expected {expected_id!r}, got {entity_id!r}"
            )
        if declared_digest != expected_digest:
            raise UnsatisfiedReferenceConstraintsError(
                f"Strict reference digest mismatch for {expected_id!r}: "
                f"expected {expected_digest!r}, got {declared_digest!r}"
            )
        source_kind = "path"

        if entity_id in seen_entity_ids:
            raise UnsatisfiedReferenceConstraintsError(
                f"Duplicate strict reference entity_id: {entity_id!r}"
            )
        seen_entity_ids.add(entity_id)
        path = _resolve_local_reference(
            raw_source,
            manifest=manifest,
            project_dir=project_dir,
        )
        actual_digest = _file_digest(path)
        if not hmac.compare_digest(actual_digest, expected_digest):
            raise UnsatisfiedReferenceConstraintsError(
                f"Strict reference bytes mismatch for {entity_id!r}: "
                f"expected {expected_digest!r}, got {actual_digest!r}"
            )
        materialized = str(path)
        if materialized in seen_sources:
            raise UnsatisfiedReferenceConstraintsError(
                f"Duplicate strict reference source is not allowed: {materialized!r}"
            )
        seen_sources.add(materialized)
        mappings.append(
            ReferenceSlotMapping(
                entity_id=expected_id,
                slot_index=slot_index,
                asset_sha256=expected_digest,
                materialized_input=materialized,
                source_kind=source_kind,
            )
        )
    return tuple(mappings)


def _normalize_auxiliary_references(
    values: Optional[list[Any]],
    *,
    manifest: dict[str, Any],
    project_dir: Optional[Path],
    strict_sources: set[str],
) -> tuple[str, ...]:
    if values is None:
        return ()
    if not isinstance(values, list):
        raise UnsatisfiedReferenceConstraintsError(
            "auxiliary_reference_images must be an array"
        )
    normalized: list[str] = []
    seen = set(strict_sources)
    for index, value in enumerate(values):
        if not isinstance(value, dict) or set(value) not in ({"path"}, {"url"}):
            raise UnsatisfiedReferenceConstraintsError(
                f"Auxiliary reference {index} must be exactly {{'path': ...}} "
                "or {'url': ...}"
            )
        source_kind = "path" if "path" in value else "url"
        raw = value[source_kind]
        if not isinstance(raw, str) or not raw:
            raise UnsatisfiedReferenceConstraintsError(
                f"Auxiliary reference {index} source must be a non-empty string"
            )
        if raw != raw.strip():
            raise UnsatisfiedReferenceConstraintsError(
                f"Auxiliary reference {index} source must not contain surrounding whitespace"
            )
        if source_kind == "path":
            materialized = str(
                _resolve_local_reference(
                    raw,
                    manifest=manifest,
                    project_dir=project_dir,
                )
            )
        else:
            if not _reference_is_remote(raw):
                raise UnsatisfiedReferenceConstraintsError(
                    f"Invalid auxiliary reference URL: {raw!r}"
                )
            materialized = raw
        if materialized in seen:
            raise UnsatisfiedReferenceConstraintsError(
                f"Duplicate reference source: {materialized!r}"
            )
        seen.add(materialized)
        normalized.append(materialized)
    return tuple(normalized)


def normalize_auxiliary_reference_inputs(
    values: Optional[list[Any]],
    *,
    manifest: dict[str, Any],
    project_dir: Path,
    strict_references: list[dict[str, str]],
) -> tuple[str, ...]:
    """Provider-independent validation for auxiliary image references.

    Selectors call this before provider status/scoring so malformed paths,
    schemes, whitespace, and collisions fail before any status endpoint or
    generation-side effect is touched.
    """
    strict_sources = {
        entry["path"]
        for entry in strict_references
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }
    return _normalize_auxiliary_references(
        values,
        manifest=manifest,
        project_dir=project_dir,
        strict_sources=strict_sources,
    )


def load_authoritative_clp_shot(
    project_dir: Path,
    expected_shot_id: str,
) -> AuthoritativeCLPShot:
    """Load one shot only from authenticated, completed stage checkpoints.

    Caller-supplied manifest or binding fragments are never authority here.
    The project marker fixes project/pipeline identity; ``read_checkpoint``
    revalidates approval gates, predecessor provenance, artifact schemas, and
    the scene-plan/manifest digests before this function selects exactly one
    row by the independently supplied shot id.
    """
    if not isinstance(expected_shot_id, str) or not expected_shot_id:
        raise CLPValidationError("CLP execution requires a non-empty independent shot id")

    raw_project_dir = Path(project_dir)
    project_id = validate_project_id(raw_project_dir.name)
    try:
        resolved_project_dir = resolve_project_dir(
            raw_project_dir.parent,
            project_id,
        )
    except ValueError as exc:
        raise CLPValidationError(f"Invalid authoritative project directory: {exc}") from exc
    if resolved_project_dir != raw_project_dir.resolve():
        raise CLPValidationError(
            f"Project directory identity mismatch: expected {resolved_project_dir}, "
            f"got {raw_project_dir.resolve()}"
        )

    marker_path = resolved_project_dir / "project.json"
    try:
        resolved_marker = marker_path.resolve(strict=True)
    except OSError as exc:
        raise CLPValidationError(
            f"Authoritative CLP execution requires project.json: {exc}"
        ) from exc
    if (
        resolved_marker.parent != resolved_project_dir
        or resolved_marker.name != "project.json"
        or not resolved_marker.is_file()
    ):
        raise CLPValidationError(
            f"project.json must be a direct regular file in {resolved_project_dir}"
        )
    try:
        marker = json.loads(resolved_marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CLPValidationError(f"Cannot read authoritative project.json: {exc}") from exc
    if not isinstance(marker, dict) or marker.get("project_id") != project_id:
        raise CLPValidationError(
            "project.json identity does not match the authoritative project directory"
        )
    pipeline_type = marker.get("pipeline_type")
    if not isinstance(pipeline_type, str) or not pipeline_type:
        raise CLPValidationError("project.json requires a concrete pipeline_type")

    # Import lazily: checkpoint validation calls this module for CLP semantics.
    from lib.checkpoint import CheckpointValidationError, read_checkpoint

    try:
        clp_checkpoint = read_checkpoint(
            resolved_project_dir.parent, project_id, "clp"
        )
        scene_checkpoint = read_checkpoint(
            resolved_project_dir.parent, project_id, "scene_plan"
        )
    except CheckpointValidationError as exc:
        raise CLPValidationError(
            f"Authoritative CLP checkpoint chain failed validation: {exc}"
        ) from exc
    if clp_checkpoint is None or scene_checkpoint is None:
        raise CLPValidationError(
            "Authoritative CLP execution requires checkpoint_clp.json and "
            "checkpoint_scene_plan.json"
        )
    for name, checkpoint in (
        ("clp", clp_checkpoint),
        ("scene_plan", scene_checkpoint),
    ):
        if checkpoint.get("status") != "completed":
            raise CLPValidationError(
                f"Authoritative {name} checkpoint must be completed"
            )
        if checkpoint.get("pipeline_type") != pipeline_type:
            raise CLPValidationError(
                f"{name} checkpoint pipeline does not match project.json"
            )

    clp_artifacts = clp_checkpoint.get("artifacts")
    scene_artifacts = scene_checkpoint.get("artifacts")
    if not isinstance(clp_artifacts, dict) or not isinstance(scene_artifacts, dict):
        raise CLPValidationError("Authoritative CLP checkpoints require artifact objects")
    manifest = clp_artifacts.get("clp_manifest")
    bindings_doc = scene_artifacts.get("clp_shot_bindings")
    scene_plan = scene_artifacts.get("scene_plan")
    if not all(isinstance(value, dict) for value in (manifest, bindings_doc, scene_plan)):
        raise CLPValidationError(
            "Authoritative checkpoint chain is missing clp_manifest, "
            "clp_shot_bindings, or scene_plan"
        )

    from schemas.artifacts import validate_artifact

    try:
        validate_artifact(
            "clp_manifest", manifest, project_dir=resolved_project_dir
        )
        validate_artifact("clp_shot_bindings", bindings_doc)
        validate_artifact("scene_plan", scene_plan)
        validate_clp_shot_bindings_or_raise(
            bindings_doc,
            manifest=manifest,
            scene_plan=scene_plan,
        )
    except Exception as exc:
        if isinstance(exc, CLPValidationError):
            raise
        raise CLPValidationError(
            f"Authoritative CLP artifacts failed validation: {exc}"
        ) from exc

    selected = [
        row
        for row in bindings_doc.get("bindings", [])
        if isinstance(row, dict) and row.get("shot_id") == expected_shot_id
    ]
    if len(selected) != 1:
        raise CLPValidationError(
            f"Expected exactly one authoritative binding for shot "
            f"{expected_shot_id!r}, found {len(selected)}"
        )

    return AuthoritativeCLPShot(
        project_id=project_id,
        pipeline_type=pipeline_type,
        shot_id=expected_shot_id,
        manifest=deepcopy(manifest),
        bindings_doc=deepcopy(bindings_doc),
        scene_plan=deepcopy(scene_plan),
        binding=deepcopy(selected[0]),
    )


def _require_authoritative_cache_match(
    *,
    context: AuthoritativeCLPShot,
    manifest: Any,
    binding: Any,
) -> None:
    """Allow detached values only as exact caches of persisted authority."""
    if not isinstance(manifest, dict) or not hmac.compare_digest(
        canonical_digest(manifest), canonical_digest(context.manifest)
    ):
        raise CLPValidationError(
            "Caller clp_manifest does not match authoritative checkpoint_clp.json"
        )
    if not isinstance(binding, dict) or not hmac.compare_digest(
        canonical_digest(binding), canonical_digest(context.binding)
    ):
        raise CLPValidationError(
            f"Caller binding does not match authoritative binding for shot "
            f"{context.shot_id!r}"
        )


def compile_attached_references(
    binding: dict[str, Any],
    manifest: dict[str, Any],
    project_dir: Path,
    *,
    expected_shot_id: str,
) -> list[dict[str, str]]:
    """Compile manifest assets into verified entity-bound reference inputs.

    Runtime directors supply an independent shot id.  Both detached arguments
    are treated only as caches and must byte-canonically match the exact
    completed checkpoint chain resolved from ``project_dir``.
    """
    from schemas.artifacts import validate_artifact

    context = load_authoritative_clp_shot(Path(project_dir), expected_shot_id)
    _require_authoritative_cache_match(
        context=context,
        manifest=manifest,
        binding=binding,
    )
    # Use freshly loaded authority after the cache comparison so a caller can
    # never control policy, identity, or slot composition.
    manifest = context.manifest
    binding = context.binding
    _project_root(manifest, Path(project_dir))
    validate_artifact("clp_manifest", manifest, project_dir=Path(project_dir))
    bound_shot_id = binding.get("shot_id") if isinstance(binding, dict) else None
    _validate_single_shot_binding_contract(
        binding,
        shot_id=bound_shot_id if isinstance(bound_shot_id, str) else "",
        manifest=manifest,
    )
    shot_id = expected_shot_id
    strict_entities = _bound_strict_entities(shot_id, binding, manifest)
    compiled_inputs: list[dict[str, str]] = []
    for entity_id, entity in strict_entities:
        image = entity.get("image")
        if not isinstance(image, str) or not image:
            raise UnsatisfiedReferenceConstraintsError(
                f"Strict entity {entity_id!r} has no local manifest image to compile"
            )
        compiled_inputs.append(
            {
                "entity_id": entity_id,
                "asset_sha256": entity["asset_sha256"],
                "path": image,
            }
        )
    mappings = _materialize_reference_mappings(
        shot_id=shot_id,
        strict_entities=strict_entities,
        actual_references=compiled_inputs,
        manifest=manifest,
        project_dir=Path(project_dir),
    )
    return [
        {
            "entity_id": mapping.entity_id,
            "asset_sha256": mapping.asset_sha256,
            "path": mapping.materialized_input,
        }
        for mapping in mappings
    ]


def build_reference_execution_plan(
    tool: Any,
    shot_id: str,
    binding: dict[str, Any],
    manifest: dict[str, Any],
    operation: str = "text_to_video",
    model: Optional[str] = None,
    actual_references: Optional[list[Any]] = None,
    *,
    model_variant: Optional[str] = None,
    auxiliary_references: Optional[list[Any]] = None,
    project_dir: Optional[Path] = None,
    bindings_doc: Optional[dict[str, Any]] = None,
    scene_plan: Optional[dict[str, Any]] = None,
) -> ReferenceExecutionPlan:
    """Build and fully verify a strict-reference plan before any side effects."""
    if not isinstance(shot_id, str) or not shot_id:
        raise CLPValidationError("Reference execution requires a non-empty shot_id")
    try:
        from schemas.artifacts import validate_artifact

        validate_artifact(
            "clp_manifest",
            manifest,
            project_dir=Path(project_dir) if project_dir is not None else None,
        )
    except Exception as exc:
        if isinstance(exc, CLPValidationError):
            raise
        raise CLPValidationError(
            f"CLP manifest failed executable schema validation: {exc}"
        ) from exc
    _validate_single_shot_binding_contract(
        binding,
        shot_id=shot_id,
        manifest=manifest,
    )
    if (bindings_doc is None) != (scene_plan is None):
        raise CLPValidationError(
            "Reference provenance requires both clp_shot_bindings and scene_plan"
        )
    if bindings_doc is not None and scene_plan is not None:
        try:
            validate_artifact("clp_shot_bindings", bindings_doc)
            validate_artifact("scene_plan", scene_plan)
            validate_clp_shot_bindings_or_raise(
                bindings_doc,
                manifest=manifest,
                scene_plan=scene_plan,
            )
        except Exception as exc:
            if isinstance(exc, CLPValidationError):
                raise
            raise CLPValidationError(
                f"CLP reference provenance failed schema validation: {exc}"
            ) from exc
        selected = [
            row
            for row in bindings_doc.get("bindings", [])
            if isinstance(row, dict) and row.get("shot_id") == shot_id
        ]
        if len(selected) != 1 or canonical_digest(selected[0]) != canonical_digest(binding):
            raise CLPValidationError(
                f"Detached binding is not the unique sidecar row for shot {shot_id!r}"
            )
    capability = get_tool_reference_capability(
        tool,
        model=model,
        operation=operation,
        model_variant=model_variant,
    )
    strict_entities = _bound_strict_entities(shot_id, binding, manifest)
    strict_count = len(strict_entities)
    if strict_count and not capability.supported:
        raise UnsatisfiedReferenceConstraintsError(
            f"{capability.tool_name}/{capability.resolved_model} does not support "
            f"strict references for operation={operation!r}"
        )
    check_strict_reference_budget(
        shot_id,
        binding,
        manifest,
        max_slots=capability.max_image_slots,
    )
    mappings = _materialize_reference_mappings(
        shot_id=shot_id,
        strict_entities=strict_entities,
        actual_references=actual_references,
        manifest=manifest,
        project_dir=project_dir,
    )
    auxiliary = _normalize_auxiliary_references(
        auxiliary_references,
        manifest=manifest,
        project_dir=project_dir,
        strict_sources={mapping.materialized_input for mapping in mappings},
    )
    if len(mappings) + len(auxiliary) > capability.max_image_slots:
        raise ReferenceSlotOverflowError(
            f"Shot {shot_id!r} materializes {len(mappings)} strict + "
            f"{len(auxiliary)} auxiliary image references, exceeding "
            f"{capability.max_image_slots} slots"
        )
    return ReferenceExecutionPlan(
        provider=capability.provider,
        tool_name=capability.tool_name,
        operation=operation,
        model=capability.resolved_model,
        max_slots=capability.max_image_slots,
        strict_count=strict_count,
        strict_entity_ids=tuple(entity_id for entity_id, _ in strict_entities),
        ordered_digests=tuple(entity["asset_sha256"] for _, entity in strict_entities),
        slot_mappings=mappings,
        binding_sha256=canonical_digest(binding),
        canonical_input_key=capability.canonical_input_key,
        provider_payload_key=capability.provider_payload_key,
        auxiliary_references=auxiliary,
        shot_id=shot_id,
        project_id=str(manifest.get("project_id") or ""),
        manifest_sha256=canonical_digest(manifest),
        bindings_sha256=(
            canonical_digest(bindings_doc) if bindings_doc is not None else ""
        ),
        scene_plan_sha256=(
            canonical_digest(scene_plan) if scene_plan is not None else ""
        ),
    )


def structured_reference_inputs(plan: ReferenceExecutionPlan) -> list[dict[str, str]]:
    """Serialize verified strict mappings for replay at the provider boundary."""
    return [
        {
            "entity_id": mapping.entity_id,
            "asset_sha256": mapping.asset_sha256,
            mapping.source_kind: mapping.materialized_input,
        }
        for mapping in plan.slot_mappings
    ]


def _plan_value(plan: Any, name: str) -> Any:
    if isinstance(plan, ReferenceExecutionPlan):
        return getattr(plan, name)
    if isinstance(plan, dict):
        return plan.get(name)
    return None


def validate_provider_reference_submission(
    tool: Any,
    inputs: dict[str, Any],
) -> Optional[ReferenceExecutionPlan]:
    """Revalidate a selector plan at the final pre-upload/provider boundary.

    Non-CLP direct calls remain compatible.  A call carrying CLP context must
    reproduce the exact entity identities, digests, local bytes, ordering, model,
    operation, capacity, and canonical provider payload from the selector plan.
    """
    if "clp_binding" in inputs and "binding" in inputs:
        raise UnsatisfiedReferenceConstraintsError(
            "CLP provider submission accepts exactly one binding key; do not "
            "provide both clp_binding and legacy binding"
        )
    binding = (
        inputs.get("clp_binding")
        if "clp_binding" in inputs
        else inputs.get("binding")
    )
    manifest = inputs.get("clp_manifest")
    bindings_doc = inputs.get("clp_shot_bindings")
    scene_plan = inputs.get("clp_scene_plan")
    expected_shot_id = inputs.get("clp_shot_id")
    plan = inputs.get("_reference_execution_plan")
    structured = inputs.get("clp_reference_inputs")
    auxiliary = inputs.get("auxiliary_reference_images")
    if not any(
        value is not None
        for value in (
            binding,
            manifest,
            bindings_doc,
            scene_plan,
            expected_shot_id,
            plan,
            structured,
            auxiliary,
        )
    ):
        return None
    if (
        not isinstance(binding, dict)
        or not isinstance(manifest, dict)
        or not isinstance(bindings_doc, dict)
        or not isinstance(scene_plan, dict)
    ):
        raise UnsatisfiedReferenceConstraintsError(
            "CLP provider submission requires clp_binding, clp_manifest, "
            "clp_shot_bindings, and clp_scene_plan"
        )
    if not isinstance(expected_shot_id, str) or not expected_shot_id:
        raise UnsatisfiedReferenceConstraintsError(
            "CLP provider submission requires an independent non-empty clp_shot_id"
        )
    project_dir_value = inputs.get("project_dir")
    if not isinstance(project_dir_value, str) or not project_dir_value:
        raise UnsatisfiedReferenceConstraintsError(
            "CLP provider submission requires authoritative project_dir"
        )
    try:
        from schemas.artifacts import validate_artifact

        context = load_authoritative_clp_shot(
            Path(project_dir_value), expected_shot_id
        )
        _require_authoritative_cache_match(
            context=context,
            manifest=manifest,
            binding=binding,
        )
        if canonical_digest(bindings_doc) != canonical_digest(context.bindings_doc):
            raise CLPValidationError(
                "Caller clp_shot_bindings does not match checkpoint_scene_plan.json"
            )
        if canonical_digest(scene_plan) != canonical_digest(context.scene_plan):
            raise CLPValidationError(
                "Caller clp_scene_plan does not match checkpoint_scene_plan.json"
            )
        manifest = context.manifest
        binding = context.binding
        bindings_doc = context.bindings_doc
        scene_plan = context.scene_plan
        shot_id = context.shot_id
        validate_artifact(
            "clp_manifest",
            manifest,
            project_dir=Path(project_dir_value),
        )
        _validate_single_shot_binding_contract(
            binding,
            shot_id=shot_id,
            manifest=manifest,
        )
    except Exception as exc:
        if isinstance(exc, UnsatisfiedReferenceConstraintsError):
            raise
        raise UnsatisfiedReferenceConstraintsError(
            f"CLP provider schema/binding validation failed: {exc}"
        ) from exc
    strict_entities = _bound_strict_entities(shot_id, binding, manifest)
    loose_aliases = present_image_reference_aliases(inputs)
    if plan is None and loose_aliases:
        raise UnsatisfiedReferenceConstraintsError(
            "CLP provider submissions cannot carry loose image aliases; use "
            "clp_reference_inputs for strict identity references or "
            "auxiliary_reference_images for non-identity references"
        )
    if not strict_entities and plan is None and structured is None and auxiliary is None:
        return None
    if plan is None or not isinstance(plan, (ReferenceExecutionPlan, dict)):
        raise UnsatisfiedReferenceConstraintsError(
            "CLP strict provider submission is missing _reference_execution_plan"
        )
    if not isinstance(structured, list):
        raise UnsatisfiedReferenceConstraintsError(
            "CLP strict provider submission is missing structured clp_reference_inputs"
        )
    operation_value = inputs.get("operation", "text_to_video")
    if not isinstance(operation_value, str):
        raise UnsatisfiedReferenceConstraintsError(
            f"operation must be a string, got {type(operation_value).__name__}"
        )
    operation = operation_value
    if operation != "reference_to_video":
        raise UnsatisfiedReferenceConstraintsError(
            "Strict CLP references require operation='reference_to_video', "
            f"got {operation!r}"
        )
    model = resolve_tool_reference_model_input(tool, inputs)
    model_variant = inputs.get("model_variant")
    if model_variant is not None and not isinstance(model_variant, str):
        raise UnsatisfiedReferenceConstraintsError(
            f"model_variant must be a string, got {type(model_variant).__name__}"
        )
    rebuilt = build_reference_execution_plan(
        tool=tool,
        shot_id=shot_id,
        binding=binding,
        manifest=manifest,
        operation=operation,
        model=model,
        model_variant=model_variant,
        actual_references=structured,
        auxiliary_references=inputs.get("auxiliary_reference_images"),
        project_dir=Path(project_dir_value),
        bindings_doc=bindings_doc,
        scene_plan=scene_plan,
    )
    comparable_fields = (
        "provider",
        "tool_name",
        "operation",
        "model",
        "max_slots",
        "strict_count",
        "strict_entity_ids",
        "ordered_digests",
        "slot_mappings",
        "binding_sha256",
        "canonical_input_key",
        "provider_payload_key",
        "auxiliary_references",
        "shot_id",
        "project_id",
        "manifest_sha256",
        "bindings_sha256",
        "scene_plan_sha256",
    )
    for field_name in comparable_fields:
        if _plan_value(plan, field_name) != getattr(rebuilt, field_name):
            raise UnsatisfiedReferenceConstraintsError(
                f"Reference execution plan mismatch at {field_name}"
            )
    conflicting_aliases = present_image_reference_aliases(
        inputs,
        allowed=(rebuilt.canonical_input_key,),
    )
    if conflicting_aliases:
        raise UnsatisfiedReferenceConstraintsError(
            f"Provider payload contains non-canonical reference aliases: {conflicting_aliases}"
        )
    canonical_values = inputs.get(rebuilt.canonical_input_key)
    expected_values = [
        *(mapping.materialized_input for mapping in rebuilt.slot_mappings),
        *rebuilt.auxiliary_references,
    ]
    if canonical_values != expected_values:
        raise UnsatisfiedReferenceConstraintsError(
            f"Provider canonical payload {rebuilt.canonical_input_key!r} does not "
            "exactly match execution plan"
        )
    return rebuilt
