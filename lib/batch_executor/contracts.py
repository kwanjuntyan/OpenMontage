"""Versioned, offline-only Batch Executor V2 M0 contracts.

This module validates frozen work authored and approved by the Agent/user.  It
does not choose a stage, create prompts, select/fallback providers, review
media, resolve Human Gates, dispatch work, or write canonical project state.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal
from functools import lru_cache
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from lib.identity import InvalidProjectIdError, resolve_project_dir


CANONICAL_JSON_VERSION = "openmontage-canonical-json-v1"
SCHEMAS_DIR = Path(__file__).resolve().parents[2] / "schemas" / "execution"
SCHEMA_NAMES = frozenset(
    {
        "batch_request",
        "batch_state",
        "batch_result",
        "attempt",
        "storage_receipt",
        "execution_owner",
        "execution_status_evidence",
        "resume_authorization",
    }
)

# ``vertex_interactions`` is the stable OpenMontage route identifier for the
# Vertex AI global Interactions resource family.  It never denotes the Gemini
# Developer API and must never be selected by inspecting ambient credentials.
_INITIAL_IDENTITY = {
    "tool_name": "gemini_omni_video",
    "tool_contract_version": "0.1.0",
    "provider": "gemini_omni",
    "route": "vertex_interactions",
    "model": "gemini-omni-1.1-flash-preview",
    "operation": "text_to_video",
}
INITIAL_ADAPTER_IDENTITY: Mapping[str, str] = MappingProxyType(_INITIAL_IDENTITY)

# This freezes the support target without claiming that the current production
# adapter implements it.  M3 must satisfy every declaration before a real call.
MVP_ADAPTER_SUPPORT: Mapping[str, Any] = MappingProxyType(
    {
        "contract_version": "batch-v2-gemini-vertex-v1",
        "identity": INITIAL_ADAPTER_IDENTITY,
        "route_binding": "explicit_request",
        "credential_mode": "adc",
        "maximum_qualified_concurrency": 1,
        "hidden_writers": "disabled",
        "implementation_status": "contract_only_until_m3",
    }
)

_SAFE_COMPONENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:")
_SENSITIVE_KEYS = frozenset(
    {
        "api_key",
        "access_token",
        "refresh_token",
        "client_secret",
        "credentials",
        "credential_path",
        "google_application_credentials",
        "service_account",
        "service_account_json",
        "authorization_header",
        "signed_url",
    }
)


class M0ContractError(ValueError):
    """A fail-closed M0 contract violation with a stable machine code."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


@lru_cache(maxsize=None)
def _load_execution_schema_cached(name: str) -> dict[str, Any]:
    """Load one allowlisted execution schema for internal read-only use."""

    if name not in SCHEMA_NAMES:
        raise M0ContractError("UNKNOWN_SCHEMA", f"Unknown execution schema {name!r}")
    path = SCHEMAS_DIR / f"{name}.schema.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise M0ContractError("SCHEMA_LOAD_FAILED", f"Cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise M0ContractError("SCHEMA_LOAD_FAILED", f"Schema {path} is not an object")
    return value


def load_execution_schema(name: str) -> dict[str, Any]:
    """Return a caller-owned copy of one allowlisted execution schema."""

    return deepcopy(_load_execution_schema_cached(name))


@lru_cache(maxsize=1)
def _schema_registry() -> Registry:
    resources = []
    for name in sorted(SCHEMA_NAMES):
        schema = _load_execution_schema_cached(name)
        Draft202012Validator.check_schema(schema)
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


@lru_cache(maxsize=None)
def _validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(
        _load_execution_schema_cached(name),
        registry=_schema_registry(),
        format_checker=FormatChecker(),
    )


def validate_contract(name: str, document: Mapping[str, Any]) -> None:
    """Validate one document against its versioned JSON Schema."""

    errors = sorted(_validator(name).iter_errors(document), key=lambda error: list(error.path))
    if not errors:
        return
    error = errors[0]
    location = ".".join(str(part) for part in error.absolute_path) or "<root>"
    raise M0ContractError(
        "SCHEMA_VALIDATION_FAILED",
        f"{name} at {location}: {error.message}",
    )


def _validate_json_value(value: Any, location: str = "<root>") -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise M0ContractError("NON_CANONICAL_JSON", f"Non-finite number at {location}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_value(item, f"{location}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise M0ContractError(
                    "NON_CANONICAL_JSON", f"Non-string object key at {location}: {key!r}"
                )
            _validate_json_value(item, f"{location}.{key}")
        return
    raise M0ContractError(
        "NON_CANONICAL_JSON",
        f"Unsupported JSON value {type(value).__name__} at {location}",
    )


def canonical_json_bytes(document: Any) -> bytes:
    """Serialize deterministic UTF-8 JSON under the v1 canonical rules.

    V1 keeps JSON numeric spelling significant (``1`` and ``1.0`` differ),
    rejects non-finite/non-JSON values, sorts object keys, emits no insignificant
    whitespace, and never ASCII-escapes Unicode.
    """

    _validate_json_value(document)
    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(document: Any) -> str:
    """Return the complete lowercase 64-hex SHA-256 canonical digest."""

    return hashlib.sha256(canonical_json_bytes(document)).hexdigest()


def _digest_without(document: Mapping[str, Any], field: str) -> str:
    candidate = deepcopy(dict(document))
    candidate.pop(field, None)
    return canonical_sha256(candidate)


def freeze_batch_request(document: Mapping[str, Any]) -> dict[str, Any]:
    """Compute integrity digests without inventing creative or policy defaults."""

    frozen = deepcopy(dict(document))
    source_bindings = frozen.get("source_bindings")
    if not isinstance(source_bindings, list):
        raise M0ContractError("INVALID_REQUEST", "source_bindings must be an array")
    binding_by_id = {
        binding.get("binding_id"): binding
        for binding in source_bindings
        if isinstance(binding, dict)
    }
    work_items = frozen.get("work_items")
    if not isinstance(work_items, list):
        raise M0ContractError("INVALID_REQUEST", "work_items must be an array")
    for item in work_items:
        if not isinstance(item, dict):
            raise M0ContractError("INVALID_REQUEST", "Every work item must be an object")
        item["work_item_digest"] = compute_work_item_digest(item, binding_by_id)
    authorization = frozen.get("authorization")
    if not isinstance(authorization, dict):
        raise M0ContractError("INVALID_REQUEST", "authorization must be an object")
    authorization["authorization_digest"] = _digest_without(
        authorization, "authorization_digest"
    )
    frozen["request_digest"] = _digest_without(frozen, "request_digest")
    validate_batch_request(frozen)
    return frozen


def freeze_self_digest(
    document: Mapping[str, Any], *, schema_name: str, digest_field: str
) -> dict[str, Any]:
    """Freeze a self-digesting evidence document and validate its schema."""

    frozen = deepcopy(dict(document))
    frozen[digest_field] = _digest_without(frozen, digest_field)
    validate_contract(schema_name, frozen)
    _assert_no_sensitive_values(frozen)
    return frozen


def compute_work_item_digest(
    item: Mapping[str, Any], source_bindings: Mapping[str, Mapping[str, Any]]
) -> str:
    """Bind an item to its exact ordered source content, not merely source IDs."""

    candidate = deepcopy(dict(item))
    candidate.pop("work_item_digest", None)
    binding_digests = []
    source_ids = candidate.get("source_binding_ids")
    if not isinstance(source_ids, list):
        raise M0ContractError("INVALID_REQUEST", "source_binding_ids must be an array")
    for binding_id in source_ids:
        binding = source_bindings.get(binding_id)
        if not isinstance(binding, Mapping):
            raise M0ContractError(
                "UNKNOWN_SOURCE_BINDING", f"Cannot digest unknown source binding {binding_id!r}"
            )
        binding_digests.append(
            {
                "binding_id": binding_id,
                "sha256": binding.get("sha256"),
                "size_bytes": binding.get("size_bytes"),
            }
        )
    return canonical_sha256(
        {
            "digest_contract": "openmontage-work-item-digest-v1",
            "work_item": candidate,
            "ordered_source_bindings": binding_digests,
        }
    )


def compute_idempotency_digest(request_digest: str, work_item_digest: str) -> str:
    """Return the full stable same-request idempotency identity for one item."""

    return canonical_sha256(
        {
            "digest_contract": "openmontage-batch-idempotency-v1",
            "request_digest": request_digest,
            "work_item_digest": work_item_digest,
        }
    )


def validate_logical_path(value: Any, *, field: str) -> str:
    """Require one normalized, project-relative POSIX logical path."""

    if not isinstance(value, str) or not value:
        raise M0ContractError("INVALID_LOGICAL_PATH", f"{field} must be non-empty text")
    if "\\" in value or "\x00" in value or "?" in value:
        raise M0ContractError("INVALID_LOGICAL_PATH", f"{field} is not a durable logical path")
    if _WINDOWS_DRIVE_RE.match(value) or "://" in value:
        raise M0ContractError("INVALID_LOGICAL_PATH", f"{field} must be project-relative")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise M0ContractError("INVALID_LOGICAL_PATH", f"{field} escapes or is not normalized")
    normalized = path.as_posix()
    if normalized != value or "//" in value:
        raise M0ContractError(
            "INVALID_LOGICAL_PATH", f"{field} must use normalized POSIX spelling"
        )
    return normalized


def _safe_component(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not _SAFE_COMPONENT_RE.fullmatch(value):
        raise M0ContractError("INVALID_PATH_COMPONENT", f"Unsafe {field}: {value!r}")
    if value in {".", ".."}:
        raise M0ContractError("INVALID_PATH_COMPONENT", f"Unsafe {field}: {value!r}")
    return value


def _paths_equal(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left)) == os.path.normcase(str(right))


def _resolve_without_alias(path: Path, *, root: Path, field: str) -> Path:
    expected = path
    resolved = path.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise M0ContractError("WORKSPACE_ESCAPE", f"{field} escapes project root") from exc
    if not _paths_equal(resolved, expected):
        raise M0ContractError(
            "WORKSPACE_ALIAS",
            f"{field} changes identity through a symlink or junction: {expected} -> {resolved}",
        )
    return resolved


def derive_attempt_output_path(
    projects_root: str | Path,
    project_id: str,
    batch_id: str,
    item_id: str,
    attempt_id: str,
    output_name: str,
) -> Path:
    """Derive the only M0-permitted tool output path for both profiles."""

    try:
        project_dir = resolve_project_dir(projects_root, project_id)
    except InvalidProjectIdError as exc:
        raise M0ContractError("INVALID_PROJECT", str(exc)) from exc
    if not project_dir.is_dir():
        raise M0ContractError("INVALID_PROJECT", f"Project directory does not exist: {project_dir}")
    safe_batch = _safe_component(batch_id, field="batch_id")
    safe_item = _safe_component(item_id, field="item_id")
    safe_attempt = _safe_component(attempt_id, field="attempt_id")
    safe_output = _safe_component(output_name, field="output_name")
    if not safe_output.lower().endswith(".mp4"):
        raise M0ContractError("INVALID_OUTPUT_PATH", "MVP output_name must end in .mp4")
    target = project_dir.joinpath(
        ".batch-v2",
        "runs",
        safe_batch,
        "attempts",
        safe_item,
        safe_attempt,
        safe_output,
    )
    return _resolve_without_alias(target, root=project_dir, field="output_path")


def validate_attempt_output_path(
    candidate: str | Path,
    *,
    projects_root: str | Path,
    project_id: str,
    batch_id: str,
    item_id: str,
    attempt_id: str,
    output_name: str,
) -> Path:
    """Reject arbitrary, traversal, aliased, temp, or canonical tool paths."""

    raw = str(candidate)
    lexical_parts = raw.replace("\\", "/").split("/")
    if any(part in {".", ".."} for part in lexical_parts):
        raise M0ContractError("INVALID_OUTPUT_PATH", "output_path contains traversal")
    candidate_path = Path(candidate)
    if not candidate_path.is_absolute():
        raise M0ContractError("INVALID_OUTPUT_PATH", "output_path must be absolute")
    expected = derive_attempt_output_path(
        projects_root, project_id, batch_id, item_id, attempt_id, output_name
    )
    project_dir = resolve_project_dir(projects_root, project_id)
    resolved = _resolve_without_alias(candidate_path, root=project_dir, field="output_path")
    if not _paths_equal(resolved, expected):
        raise M0ContractError(
            "INVALID_OUTPUT_PATH", f"Expected coordinator-derived path {expected}, got {candidate}"
        )
    return resolved


def _normalized_sensitive_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")


def _assert_no_sensitive_values(value: Any, location: str = "<root>") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = _normalized_sensitive_key(str(key))
            if normalized in _SENSITIVE_KEYS:
                raise M0ContractError(
                    "CREDENTIAL_MATERIAL_FORBIDDEN",
                    f"Credential-bearing field {key!r} is forbidden at {location}",
                )
            _assert_no_sensitive_values(item, f"{location}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _assert_no_sensitive_values(item, f"{location}[{index}]")


def exact_identity() -> dict[str, str]:
    """Return a mutable copy suitable for a request or attempt record."""

    return dict(INITIAL_ADAPTER_IDENTITY)


def validate_exact_identity(identity: Mapping[str, Any], *, field: str = "identity") -> None:
    actual = dict(identity)
    expected = dict(INITIAL_ADAPTER_IDENTITY)
    if actual != expected:
        mismatches = [
            f"{key}={actual.get(key)!r} (expected {expected[key]!r})"
            for key in expected
            if actual.get(key) != expected[key]
        ]
        extras = sorted(set(actual) - set(expected))
        if extras:
            mismatches.append(f"unexpected fields={extras}")
        raise M0ContractError(
            "EXACT_IDENTITY_MISMATCH", f"{field}: " + "; ".join(mismatches)
        )


def adapter_observation_blockers(observation: Mapping[str, Any]) -> tuple[str, ...]:
    """Return offline qualification blockers; never inspect credentials/env."""

    blockers: list[str] = []
    allowed_fields = {
        "identity",
        "route_binding",
        "credential_mode",
        "hidden_writers",
        "available",
    }
    normalized_keys = {_normalized_sensitive_key(str(key)) for key in observation}
    if normalized_keys.intersection(_SENSITIVE_KEYS):
        blockers.append("CREDENTIAL_MATERIAL_FORBIDDEN")
    if "fallback" in observation or "fallback_tools" in observation:
        blockers.append("FALLBACK_FORBIDDEN")
    if set(observation) - allowed_fields:
        blockers.append("UNSUPPORTED_ADAPTER_OBSERVATION")
    identity = observation.get("identity")
    try:
        if not isinstance(identity, Mapping):
            raise M0ContractError("EXACT_IDENTITY_MISMATCH", "identity is missing")
        validate_exact_identity(identity, field="observed adapter identity")
    except M0ContractError as exc:
        blockers.append(exc.code)
    if observation.get("route_binding") != "explicit_request":
        blockers.append("ROUTE_NOT_EXPLICIT")
    if observation.get("credential_mode") != "adc":
        blockers.append("ADC_REQUIRED")
    if observation.get("hidden_writers") != "disabled":
        blockers.append("HIDDEN_WRITERS_NOT_DISABLED")
    if observation.get("available") is not True:
        blockers.append("ADAPTER_UNAVAILABLE")
    return tuple(dict.fromkeys(blockers))


def validate_adapter_observation(observation: Mapping[str, Any]) -> None:
    blockers = adapter_observation_blockers(observation)
    if blockers:
        raise M0ContractError(
            "ADAPTER_NOT_QUALIFIED", f"Adapter support blockers: {', '.join(blockers)}"
        )


def _validate_dependency_graph(work_items: list[Mapping[str, Any]]) -> None:
    graph = {str(item["item_id"]): list(item["dependency_item_ids"]) for item in work_items}
    known = set(graph)
    for item_id, dependencies in graph.items():
        unknown = sorted(set(dependencies) - known)
        if unknown:
            raise M0ContractError(
                "UNKNOWN_ITEM_DEPENDENCY", f"{item_id} depends on unknown items {unknown}"
            )
        if item_id in dependencies:
            raise M0ContractError("CYCLIC_ITEM_DEPENDENCY", f"{item_id} depends on itself")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(item_id: str) -> None:
        if item_id in visiting:
            raise M0ContractError("CYCLIC_ITEM_DEPENDENCY", f"Cycle reaches {item_id}")
        if item_id in visited:
            return
        visiting.add(item_id)
        for dependency in graph[item_id]:
            visit(dependency)
        visiting.remove(item_id)
        visited.add(item_id)

    for item_id in graph:
        visit(item_id)


def _decimal(value: Any) -> Decimal:
    return Decimal(str(value))


def validate_batch_request(document: Mapping[str, Any]) -> None:
    """Apply schema plus relationships that JSON Schema cannot express."""

    validate_contract("batch_request", document)
    _assert_no_sensitive_values(document)
    if document["canonical_json"] != CANONICAL_JSON_VERSION:
        raise M0ContractError("CANONICAL_VERSION_MISMATCH", "Unsupported canonical JSON version")

    source_bindings = list(document["source_bindings"])
    binding_ids = [binding["binding_id"] for binding in source_bindings]
    if len(binding_ids) != len(set(binding_ids)):
        raise M0ContractError("DUPLICATE_SOURCE_BINDING", "source binding IDs must be unique")
    binding_by_id = {binding["binding_id"]: binding for binding in source_bindings}
    for binding in source_bindings:
        validate_logical_path(binding["logical_path"], field="source_bindings.logical_path")
        source_type = binding["source_type"]
        checkpoint_fields = {
            "checkpoint_stage",
            "checkpoint_status",
            "human_approved",
        }
        if source_type in {"checkpoint", "checkpoint_artifact"}:
            missing = checkpoint_fields - set(binding)
            if missing:
                raise M0ContractError(
                    "INVALID_SOURCE_BINDING", f"{binding['binding_id']} missing {sorted(missing)}"
                )
            if source_type == "checkpoint_artifact" and "artifact_name" not in binding:
                raise M0ContractError(
                    "INVALID_SOURCE_BINDING", "checkpoint_artifact requires artifact_name"
                )
        elif checkpoint_fields.intersection(binding) or "artifact_name" in binding:
            raise M0ContractError(
                "INVALID_SOURCE_BINDING", "project_file cannot carry checkpoint fields"
            )
        storage = binding.get("storage")
        if storage:
            locator = storage["locator"]
            if "?" in locator:
                raise M0ContractError("SIGNED_URL_FORBIDDEN", "Source locator cannot be signed")
            if storage["store_type"] == "gcs":
                if not locator.startswith("gs://") or "generation" not in storage:
                    raise M0ContractError(
                        "INVALID_STORAGE_BINDING", "GCS binding requires gs:// locator and generation"
                    )
            elif locator != binding["logical_path"]:
                raise M0ContractError(
                    "INVALID_STORAGE_BINDING", "Local locator must equal normalized logical_path"
                )

    authorization = document["authorization"]
    validate_exact_identity(authorization["allowed_identity"], field="authorization.allowed_identity")
    expected_authorization_digest = _digest_without(authorization, "authorization_digest")
    if authorization["authorization_digest"] != expected_authorization_digest:
        raise M0ContractError("AUTHORIZATION_DIGEST_MISMATCH", "Authorization was changed")
    checkpoint_stages = [entry["stage"] for entry in authorization["prerequisite_checkpoints"]]
    if len(checkpoint_stages) != len(set(checkpoint_stages)):
        raise M0ContractError("DUPLICATE_CHECKPOINT_EVIDENCE", "Checkpoint stages must be unique")
    for evidence in authorization["prerequisite_checkpoints"]:
        expected_path = f"checkpoint_{evidence['stage']}.json"
        if validate_logical_path(evidence["logical_path"], field="checkpoint evidence path") != expected_path:
            raise M0ContractError(
                "CHECKPOINT_PATH_MISMATCH",
                f"Stage {evidence['stage']!r} must bind {expected_path!r}",
            )

    work_items = list(document["work_items"])
    item_ids = [item["item_id"] for item in work_items]
    asset_ids = [item["asset_id"] for item in work_items]
    if len(item_ids) != len(set(item_ids)):
        raise M0ContractError("DUPLICATE_WORK_ITEM", "item_id values must be unique")
    if len(asset_ids) != len(set(asset_ids)):
        raise M0ContractError("DUPLICATE_ASSET_ID", "asset_id values must be unique")
    _validate_dependency_graph(work_items)

    required_attempts = 0
    worst_case_cost = Decimal("0")
    used_binding_ids: set[str] = set()
    for item in work_items:
        validate_exact_identity(item["identity"], field=f"work_items.{item['item_id']}.identity")
        if item["inputs"]["operation"] != item["identity"]["operation"]:
            raise M0ContractError("OPERATION_MISMATCH", f"Operation mismatch for {item['item_id']}")
        destination = validate_logical_path(
            item["output_spec"]["canonical_destination_intent"],
            field=f"work_items.{item['item_id']}.canonical_destination_intent",
        )
        if PurePosixPath(destination).parts[0] != "assets":
            raise M0ContractError(
                "INVALID_DESTINATION_INTENT", "MVP canonical destination intent must be under assets/"
            )
        if destination.startswith(".batch-v2/"):
            raise M0ContractError(
                "INVALID_DESTINATION_INTENT", "Canonical intent cannot use attempt staging"
            )
        for binding_id in item["source_binding_ids"]:
            if binding_id not in binding_by_id:
                raise M0ContractError(
                    "UNKNOWN_SOURCE_BINDING", f"{item['item_id']} references {binding_id!r}"
                )
            used_binding_ids.add(binding_id)
        for reference in item["input_references"]:
            binding = binding_by_id.get(reference["binding_id"])
            if binding is None:
                raise M0ContractError(
                    "UNKNOWN_SOURCE_BINDING", f"Input reference uses {reference['binding_id']!r}"
                )
            if reference["sha256"] != binding["sha256"] or reference["size_bytes"] != binding["size_bytes"]:
                raise M0ContractError(
                    "INPUT_REFERENCE_MISMATCH", f"Input reference differs from {reference['binding_id']}"
                )
            expected_locator = (binding.get("storage") or {}).get(
                "locator", binding["logical_path"]
            )
            if reference["locator"] != expected_locator:
                raise M0ContractError(
                    "INPUT_REFERENCE_MISMATCH", f"Locator differs from {reference['binding_id']}"
                )
        if item["work_item_digest"] != compute_work_item_digest(item, binding_by_id):
            raise M0ContractError(
                "WORK_ITEM_DIGEST_MISMATCH", f"Work item {item['item_id']} was changed"
            )
        attempts = 1 + item["charged_retry_allowance"]
        if attempts > document["execution_policy"]["max_attempts_per_item"]:
            raise M0ContractError(
                "RETRY_NOT_AUTHORIZED", f"{item['item_id']} exceeds max_attempts_per_item"
            )
        required_attempts += attempts
        attempt_cost = _decimal(item["estimated_cost_usd"])
        if attempt_cost > _decimal(document["execution_policy"]["max_attempt_cost_usd"]):
            raise M0ContractError(
                "ATTEMPT_COST_NOT_AUTHORIZED", f"{item['item_id']} exceeds per-attempt cap"
            )
        worst_case_cost += attempt_cost * attempts

    if used_binding_ids != set(binding_ids):
        unused = sorted(set(binding_ids) - used_binding_ids)
        raise M0ContractError("UNUSED_SOURCE_BINDING", f"Unused source bindings: {unused}")
    if required_attempts > authorization["max_total_attempts"]:
        raise M0ContractError("ATTEMPT_BUDGET_EXCEEDED", "Requested attempts exceed authorization")
    approved = _decimal(authorization["approved_budget_usd"])
    cap = _decimal(authorization["max_authorized_spend_usd"])
    if cap > approved:
        raise M0ContractError("BUDGET_AUTHORIZATION_INVALID", "Spend cap exceeds approved budget")
    if authorization["no_cost"]:
        if approved != 0 or cap != 0 or worst_case_cost != 0:
            raise M0ContractError("BUDGET_AUTHORIZATION_INVALID", "no_cost requires zero exposure")
    elif cap <= 0:
        raise M0ContractError("BUDGET_AUTHORIZATION_INVALID", "Paid batch requires a positive cap")
    if worst_case_cost > cap:
        raise M0ContractError(
            "BUDGET_AUTHORIZATION_EXCEEDED",
            f"Worst-case authorized attempts cost {worst_case_cost} > {cap}",
        )
    if document["request_digest"] != _digest_without(document, "request_digest"):
        raise M0ContractError("REQUEST_DIGEST_MISMATCH", "BatchRequest was changed")


def validate_storage_receipt(document: Mapping[str, Any]) -> None:
    validate_contract("storage_receipt", document)
    _assert_no_sensitive_values(document)
    logical_path = validate_logical_path(
        document["logical_path"], field="StorageReceipt.logical_path"
    )
    logical_parts = PurePosixPath(logical_path).parts
    if logical_parts[:2] != (".batch-v2", "runs"):
        raise M0ContractError(
            "INVALID_STORAGE_RECEIPT",
            "MVP execution receipt logical_path must remain in .batch-v2/runs staging",
        )
    expected_prefix = (
        ".batch-v2",
        "runs",
        document["batch_id"],
        "attempts",
        document["item_id"],
        document["attempt_id"],
    )
    if logical_parts[:6] != expected_prefix or len(logical_parts) < 7:
        raise M0ContractError(
            "INVALID_STORAGE_RECEIPT",
            "StorageReceipt path must bind its batch, item, and attempt identity",
        )
    locator = document["locator"]
    if "?" in locator:
        raise M0ContractError("SIGNED_URL_FORBIDDEN", "StorageReceipt locator cannot be signed")
    if document["store_type"] == "gcs":
        if not locator.startswith("gs://"):
            raise M0ContractError("INVALID_STORAGE_RECEIPT", "GCS locator must start gs://")
        if document["sha256"] not in locator:
            raise M0ContractError(
                "INVALID_STORAGE_RECEIPT", "GCS blob locator must be content-addressed by SHA-256"
            )
        if "generation" not in document or "provider_checksum" not in document:
            raise M0ContractError(
                "INVALID_STORAGE_RECEIPT", "GCS receipt requires generation and CRC32C"
            )
        if (
            document["verification"]["provider_checksum_verified"] is not True
            or document["verification"]["generation_verified"] is not True
        ):
            raise M0ContractError(
                "INVALID_STORAGE_RECEIPT",
                "GCS success requires synchronous checksum and generation verification",
            )
    else:
        locator_path = validate_logical_path(
            locator, field="StorageReceipt.locator"
        )
        expected_locator = PurePosixPath(
            ".batch-v2",
            "blobs",
            "sha256",
            document["sha256"][:2],
            document["sha256"],
        )
        if PurePosixPath(locator_path) != expected_locator:
            raise M0ContractError(
                "INVALID_STORAGE_RECEIPT",
                "Local locator must be the exact project-scoped SHA-256 CAS path",
            )
        if "generation" in document or "provider_checksum" in document:
            raise M0ContractError(
                "INVALID_STORAGE_RECEIPT", "Local receipt cannot claim GCS verification"
            )
        if (
            document["verification"]["provider_checksum_verified"] is not False
            or document["verification"]["generation_verified"] is not False
        ):
            raise M0ContractError(
                "INVALID_STORAGE_RECEIPT", "Local receipt cannot claim GCS-only verification"
            )


_GENERATION_RESUBMIT_ERRORS = frozenset(
    {"RATE_LIMITED_SUBMIT_REJECTED", "PROVIDER_TRANSIENT_PRE_ACCEPT"}
)
_REMOTE_POLL_ERRORS = frozenset({"RATE_LIMITED_REMOTE_POLL", "REMOTE_JOB_RECOVERABLE"})
_STORAGE_RETRY_ERRORS = frozenset({"LOCAL_STORAGE_TRANSIENT", "GCS_TRANSIENT"})
_UNKNOWN_ACCEPTANCE_ERRORS = frozenset(
    {"RATE_LIMITED_ACCEPTANCE_UNKNOWN", "TIMEOUT_OR_NETWORK_UNKNOWN"}
)
_NOT_ACCEPTED_TERMINAL_ERRORS = frozenset(
    {
        "REQUEST_CONTRACT_INVALID",
        "PROJECT_IDENTITY_INVALID",
        "SOURCE_BINDING_CHANGED",
        "APPROVAL_MISSING_OR_STALE",
        "BUDGET_EXCEEDED",
        "TOOL_UNAVAILABLE",
        "AUTH_CONFIGURATION",
        "INPUT_MEDIA_INVALID",
        "PROVIDER_PERMANENT_REJECT",
        "CONTENT_SAFETY_REJECT",
        "EXECUTION_OWNER_ACTIVE",
        "RESUME_OWNERSHIP_PROOF_INVALID",
    }
)


@dataclass(frozen=True)
class _AttemptActionRule:
    action: str
    error_classes: frozenset[str]
    phase: str
    acceptance: str
    output_requirement: str
    provider_operation_requirement: str = "optional"


_ATTEMPT_ACTION_RULES = (
    _AttemptActionRule(
        "resubmit_generation",
        _GENERATION_RESUBMIT_ERRORS,
        "failed",
        "not_accepted",
        "forbidden",
        "forbidden",
    ),
    _AttemptActionRule(
        "poll_remote_operation",
        _REMOTE_POLL_ERRORS,
        "provider_accepted",
        "accepted",
        "forbidden",
        "required",
    ),
    _AttemptActionRule(
        "retry_storage_commit",
        _STORAGE_RETRY_ERRORS,
        "technically_valid",
        "accepted",
        "required",
    ),
    _AttemptActionRule(
        "reconcile_storage_precondition",
        frozenset({"GCS_PRECONDITION_CONFLICT"}),
        "technically_valid",
        "accepted",
        "required",
    ),
    _AttemptActionRule(
        "await_charged_generation_authorization",
        frozenset({"OUTPUT_TECHNICALLY_INVALID"}),
        "failed",
        "accepted",
        "forbidden",
    ),
    _AttemptActionRule(
        "do_not_retry",
        _NOT_ACCEPTED_TERMINAL_ERRORS | _GENERATION_RESUBMIT_ERRORS,
        "failed",
        "not_accepted",
        "forbidden",
        "forbidden",
    ),
    _AttemptActionRule(
        "do_not_retry",
        frozenset({"OUTPUT_TECHNICALLY_INVALID"}),
        "failed",
        "accepted",
        "forbidden",
    ),
    _AttemptActionRule(
        "do_not_retry",
        _STORAGE_RETRY_ERRORS | {"GCS_PRECONDITION_CONFLICT"},
        "failed",
        "accepted",
        "required",
    ),
    _AttemptActionRule(
        "do_not_retry", frozenset({"INTERNAL_BUG"}), "failed", "not_accepted", "forbidden"
    ),
    _AttemptActionRule(
        "do_not_retry", frozenset({"INTERNAL_BUG"}), "failed", "accepted", "optional"
    ),
    _AttemptActionRule(
        "do_not_retry", frozenset({"CANCELLED"}), "cancelled", "not_accepted", "forbidden"
    ),
    _AttemptActionRule(
        "do_not_retry", frozenset({"CANCELLED"}), "cancelled", "accepted", "forbidden"
    ),
    _AttemptActionRule(
        "mark_indeterminate",
        _UNKNOWN_ACCEPTANCE_ERRORS | {"INTERNAL_BUG", "CANCELLED"},
        "indeterminate",
        "unknown",
        "forbidden",
    ),
    _AttemptActionRule(
        "mark_indeterminate",
        _REMOTE_POLL_ERRORS,
        "indeterminate",
        "accepted",
        "forbidden",
        "required",
    ),
)


def _require_attempt_shape(document: Mapping[str, Any], rule: _AttemptActionRule) -> None:
    if document["phase"] != rule.phase:
        raise M0ContractError(
            "INVALID_RETRY_ACTION",
            f"{rule.action} requires phase={rule.phase} for {document['error']['error_class']}",
        )
    actual_output = document.get("output")
    if rule.output_requirement == "forbidden" and actual_output is not None:
        raise M0ContractError(
            "INVALID_ATTEMPT_STATE",
            f"{rule.action} cannot carry an output",
        )
    if rule.output_requirement == "required" and not isinstance(actual_output, Mapping):
        raise M0ContractError(
            "INVALID_ATTEMPT_STATE",
            f"{rule.action} requires the already-produced output",
        )
    operation_id = document.get("provider_operation_id")
    if rule.provider_operation_requirement == "required" and not operation_id:
        raise M0ContractError(
            "PROVIDER_OPERATION_ID_REQUIRED",
            f"{rule.action} requires a durable provider operation ID",
        )
    if rule.provider_operation_requirement == "forbidden" and operation_id is not None:
        raise M0ContractError(
            "INVALID_RETRY_ACTION",
            f"{rule.action} cannot reuse a provider operation ID",
        )


def _validate_charged_retry_facts(document: Mapping[str, Any]) -> None:
    if (
        document["billing_mode"] != "paid"
        or _decimal(document["cost"]["known_actual_usd"]) <= 0
    ):
        raise M0ContractError(
            "CHARGED_RETRY_FACTS_REQUIRED",
            "Technical retry candidacy requires an accepted, known-charged paid attempt",
        )


def _validate_generation_resubmit_cost(document: Mapping[str, Any]) -> None:
    cost = document["cost"]
    if (
        _decimal(cost["known_actual_usd"]) != 0
        or _decimal(cost["potentially_charged_usd"]) != 0
    ):
        raise M0ContractError(
            "RETRY_COST_FACTS_INVALID",
            "Known-not-accepted generation resubmission cannot carry actual or possible charge",
        )


def validate_attempt(document: Mapping[str, Any]) -> None:
    validate_contract("attempt", document)
    _assert_no_sensitive_values(document)
    validate_exact_identity(document["identity"], field="attempt.identity")
    phase = document["phase"]
    acceptance = document["acceptance_knowledge"]
    retry_action = document["retry_action"]
    expected_idempotency = compute_idempotency_digest(
        document["request_digest"], document["work_item_digest"]
    )
    if document["idempotency_digest"] != expected_idempotency:
        raise M0ContractError("IDEMPOTENCY_DIGEST_MISMATCH", "Attempt identity was changed")
    output = document.get("output")
    error = document.get("error")
    if (
        isinstance(output, Mapping)
        and output.get("storage_receipt_id") is not None
        and phase != "durably_committed"
    ):
        raise M0ContractError(
            "INVALID_ATTEMPT_STATE",
            "Only a durably committed attempt may claim a StorageReceipt",
        )
    if phase == "durably_committed":
        if (
            acceptance != "accepted"
            or not isinstance(output, Mapping)
            or not output.get("storage_receipt_id")
            or retry_action != "none"
            or error is not None
        ):
            raise M0ContractError(
                "INVALID_ATTEMPT_STATE",
                "Committed attempt requires one accepted, receipted output with no error or retry",
            )
    if acceptance == "unknown" and document["billing_mode"] == "paid" and error is not None and (
        phase != "indeterminate" or retry_action != "mark_indeterminate"
    ):
        raise M0ContractError(
            "PAID_AMBIGUITY",
            "Unknown paid acceptance must remain indeterminate and cannot be retried",
        )
    if acceptance == "unknown" and document["billing_mode"] == "paid" and (
        _decimal(document["cost"]["known_actual_usd"])
        + _decimal(document["cost"]["potentially_charged_usd"])
        <= 0
    ):
        raise M0ContractError(
            "PAID_AMBIGUITY",
            "Unknown paid acceptance must retain a non-zero known or potential charge",
        )

    if retry_action == "none":
        if error is not None or phase in {"failed", "indeterminate", "cancelled"}:
            raise M0ContractError(
                "INVALID_ATTEMPT_STATE",
                "An error or terminal non-success attempt requires a typed retry action",
            )
        return
    if not isinstance(error, Mapping):
        raise M0ContractError(
            "INVALID_ATTEMPT_STATE", "A typed retry action requires a structured error"
        )
    error_class = error["error_class"]
    class_rules = [
        rule
        for rule in _ATTEMPT_ACTION_RULES
        if rule.action == retry_action and error_class in rule.error_classes
    ]
    if not class_rules:
        raise M0ContractError(
            "INVALID_RETRY_ACTION",
            f"{error_class} cannot use {retry_action}",
        )
    rule = next(
        (rule for rule in class_rules if rule.acceptance == acceptance),
        None,
    )
    if rule is None:
        raise M0ContractError(
            "INVALID_RETRY_ACTION",
            f"{error_class}/{retry_action} cannot use acceptance={acceptance}",
        )
    _require_attempt_shape(document, rule)
    if retry_action == "resubmit_generation":
        _validate_generation_resubmit_cost(document)
    if error_class == "OUTPUT_TECHNICALLY_INVALID":
        _validate_charged_retry_facts(document)


def _validate_cost_exposure(cost: Mapping[str, Any], *, code: str) -> None:
    exposure = (
        _decimal(cost["reserved_usd"])
        + _decimal(cost["known_actual_usd"])
        + _decimal(cost["indeterminate_exposure_usd"])
    )
    if exposure > _decimal(cost["authorized_cap_usd"]):
        raise M0ContractError(
            code,
            "Reserved, known-actual, and indeterminate exposure exceeds the authorized cap",
        )


def _mechanical_outcome(states: list[str]) -> str:
    if "indeterminate" in states:
        return "indeterminate"
    successful = sum(state in {"committed", "cache_hit"} for state in states)
    if successful == len(states):
        return "all_succeeded"
    if states and all(state == "cancelled" for state in states):
        return "cancelled"
    if successful:
        return "partial_failure"
    return "failed"


def _validate_dependency_blockers(
    items: list[Mapping[str, Any]],
    *,
    attempts_for_item: Mapping[str, list[Mapping[str, Any]]] | None = None,
) -> None:
    items_by_id = {item["item_id"]: item for item in items}
    blocking_states = {
        "failed_terminal",
        "blocked_by_dependency",
        "indeterminate",
        "cancelled",
    }
    for item in items:
        blocker = item.get("blocker")
        if item["state"] != "blocked_by_dependency":
            if blocker is not None:
                raise M0ContractError(
                    "DEPENDENCY_BLOCKER_INVALID",
                    f"Non-blocked item {item['item_id']} cannot claim a dependency blocker",
                )
            continue
        if not isinstance(blocker, Mapping):
            raise M0ContractError(
                "DEPENDENCY_BLOCKER_INVALID",
                f"Blocked item {item['item_id']} requires a structured blocker",
            )
        if attempts_for_item is not None and attempts_for_item[item["item_id"]]:
            raise M0ContractError(
                "DEPENDENCY_BLOCKER_INVALID",
                f"Dependency-blocked item {item['item_id']} must not have been dispatched",
            )
        if item.get("storage_receipt_id") is not None or item.get("error_class") is not None:
            raise M0ContractError(
                "DEPENDENCY_BLOCKER_INVALID",
                f"Dependency-blocked item {item['item_id']} cannot masquerade as provider work",
            )
        for dependency_id in blocker["dependency_item_ids"]:
            dependency = items_by_id.get(dependency_id)
            if (
                dependency is None
                or dependency_id == item["item_id"]
                or dependency["state"] not in blocking_states
            ):
                raise M0ContractError(
                    "DEPENDENCY_BLOCKER_INVALID",
                    f"Blocked item {item['item_id']} names no valid blocking item {dependency_id}",
                )


def _validate_terminal_item_latest_attempt(
    item: Mapping[str, Any], attempts: list[Mapping[str, Any]]
) -> Mapping[str, Any] | None:
    if not attempts:
        if item["state"] == "committed":
            raise M0ContractError(
                "COMMITTED_ITEM_INCOMPLETE",
                f"Committed item {item['item_id']} has no durable attempt",
            )
        return None
    latest = max(attempts, key=lambda attempt: attempt["dispatch_sequence"])
    expected = {
        "committed": ("durably_committed", "none"),
        "failed_terminal": ("failed", "do_not_retry"),
        "indeterminate": ("indeterminate", "mark_indeterminate"),
        "cancelled": ("cancelled", "do_not_retry"),
    }.get(item["state"])
    if expected is not None and (latest["phase"], latest["retry_action"]) != expected:
        raise M0ContractError(
            "ITEM_LATEST_ATTEMPT_MISMATCH",
            f"{item['state']} item {item['item_id']} is not supported by its latest attempt",
        )
    if item["state"] == "cancelled" and any(
        attempt["phase"] == "indeterminate"
        or (
            attempt["billing_mode"] == "paid"
            and attempt["acceptance_knowledge"] == "unknown"
        )
        for attempt in attempts
    ):
        raise M0ContractError(
            "ITEM_LATEST_ATTEMPT_MISMATCH",
            f"Cancelled item {item['item_id']} cannot hide a paid or indeterminate ambiguity",
        )
    if item.get("error_class") is not None and latest.get("error", {}).get(
        "error_class"
    ) != item["error_class"]:
        raise M0ContractError(
            "ITEM_LATEST_ATTEMPT_MISMATCH",
            f"Item {item['item_id']} error class differs from its latest attempt",
        )
    return latest


def validate_batch_state(document: Mapping[str, Any]) -> None:
    validate_contract("batch_state", document)
    _assert_no_sensitive_values(document)
    owner = document["owner"]
    if owner["batch_id"] != document["batch_id"] or owner["request_digest"] != document["request_digest"]:
        raise M0ContractError("OWNER_IDENTITY_MISMATCH", "Owner does not bind this BatchState")
    invocations = document.get("invocations")
    if invocations is not None:
        invocation_ids = [entry["invocation_id"] for entry in invocations]
        if len(invocation_ids) != len(set(invocation_ids)):
            raise M0ContractError(
                "DUPLICATE_INVOCATION", "BatchState invocation IDs must be unique"
            )
        latest_invocation = invocations[-1]
        if (
            latest_invocation["invocation_id"] != owner["invocation_id"]
            or latest_invocation["execution_id"] != owner["execution_id"]
            or latest_invocation["profile"] != owner["profile"]
        ):
            raise M0ContractError(
                "INVOCATION_OWNER_MISMATCH",
                "Latest BatchState invocation must bind the active/current owner",
            )
    item_ids = [item["item_id"] for item in document["items"]]
    if len(item_ids) != len(set(item_ids)):
        raise M0ContractError("DUPLICATE_WORK_ITEM", "BatchState item IDs must be unique")
    receipts_by_id: dict[str, Mapping[str, Any]] = {}
    known_item_ids = set(item_ids)
    for receipt in document["storage_receipts"]:
        receipt_id = receipt["receipt_id"]
        if receipt_id in receipts_by_id:
            raise M0ContractError(
                "DUPLICATE_STORAGE_RECEIPT", "StorageReceipt IDs must be unique"
            )
        if receipt["batch_id"] != document["batch_id"] or receipt["item_id"] not in known_item_ids:
            raise M0ContractError(
                "STORAGE_RECEIPT_IDENTITY_MISMATCH",
                "StorageReceipt does not bind this batch and a known item",
            )
        receipts_by_id[receipt_id] = receipt

    attempt_ids: set[str] = set()
    dispatch_sequences: set[int] = set()
    attempts_by_id: dict[str, Mapping[str, Any]] = {}
    attempts_for_item: dict[str, list[Mapping[str, Any]]] = {
        item_id: [] for item_id in item_ids
    }
    attempts_by_item: dict[str, int] = {item_id: 0 for item_id in item_ids}
    for attempt in document["attempts"]:
        validate_attempt(attempt)
        if attempt["batch_id"] != document["batch_id"] or attempt["request_digest"] != document["request_digest"]:
            raise M0ContractError("ATTEMPT_IDENTITY_MISMATCH", "Attempt does not bind this state")
        if attempt["attempt_id"] in attempt_ids:
            raise M0ContractError("DUPLICATE_ATTEMPT", "Attempt IDs must be unique")
        attempt_ids.add(attempt["attempt_id"])
        sequence = attempt["dispatch_sequence"]
        if sequence in dispatch_sequences:
            raise M0ContractError(
                "DUPLICATE_ATTEMPT_SEQUENCE", "dispatch_sequence values must be globally unique"
            )
        dispatch_sequences.add(sequence)
        if attempt["item_id"] not in attempts_by_item:
            raise M0ContractError("UNKNOWN_ATTEMPT_ITEM", "Attempt references unknown item")
        attempts_by_id[attempt["attempt_id"]] = attempt
        attempts_for_item[attempt["item_id"]].append(attempt)
        attempts_by_item[attempt["item_id"]] += 1

    dispatch_blocker = document.get("dispatch_blocker")
    if dispatch_blocker is not None:
        source_item_id = dispatch_blocker["source_item_id"]
        if source_item_id not in known_item_ids:
            raise M0ContractError(
                "DISPATCH_BLOCKER_IDENTITY_MISMATCH",
                "Durable dispatch blocker references an unknown source item",
            )
        source_attempt_id = dispatch_blocker.get("source_attempt_id")
        if source_attempt_id is not None:
            source_attempt = attempts_by_id.get(source_attempt_id)
            if source_attempt is None or source_attempt["item_id"] != source_item_id:
                raise M0ContractError(
                    "DISPATCH_BLOCKER_IDENTITY_MISMATCH",
                    "Durable dispatch blocker attempt does not bind its source item",
                )

    expected_last_sequence = max(dispatch_sequences, default=0)
    if document["last_attempt_sequence"] != expected_last_sequence:
        raise M0ContractError(
            "ATTEMPT_SEQUENCE_MISMATCH",
            f"last_attempt_sequence must equal {expected_last_sequence}",
        )

    for receipt in receipts_by_id.values():
        attempt = attempts_by_id.get(receipt["attempt_id"])
        if attempt is None or attempt["item_id"] != receipt["item_id"]:
            raise M0ContractError(
                "STORAGE_RECEIPT_IDENTITY_MISMATCH",
                "StorageReceipt does not bind a known attempt for its item",
            )
        validate_storage_receipt(receipt)

    referenced_receipt_ids: set[str] = set()
    for attempt_id, attempt in attempts_by_id.items():
        output = attempt.get("output")
        if not isinstance(output, Mapping) or "storage_receipt_id" not in output:
            continue
        receipt_id = output["storage_receipt_id"]
        receipt = receipts_by_id.get(receipt_id)
        if receipt is None:
            raise M0ContractError(
                "ATTEMPT_RECEIPT_MISMATCH", f"Attempt {attempt_id} references no durable receipt"
            )
        if (
            receipt["batch_id"] != attempt["batch_id"]
            or receipt["item_id"] != attempt["item_id"]
            or receipt["attempt_id"] != attempt_id
            or receipt["sha256"] != output["sha256"]
            or receipt["size_bytes"] != output["size_bytes"]
            or canonical_json_bytes(receipt["probe"])
            != canonical_json_bytes(output["probe"])
        ):
            raise M0ContractError(
                "ATTEMPT_RECEIPT_MISMATCH",
                f"Attempt {attempt_id} output differs from its StorageReceipt",
            )
        referenced_receipt_ids.add(receipt_id)

    for receipt_id, receipt in receipts_by_id.items():
        attempt = attempts_by_id.get(receipt["attempt_id"])
        if attempt is None or receipt_id not in referenced_receipt_ids:
            raise M0ContractError(
                "STORAGE_RECEIPT_IDENTITY_MISMATCH",
                f"StorageReceipt {receipt_id} is not bound by its attempt output",
            )

    _validate_dependency_blockers(
        document["items"], attempts_for_item=attempts_for_item
    )
    for item in document["items"]:
        if item["attempt_count"] != attempts_by_item[item["item_id"]]:
            raise M0ContractError("ATTEMPT_COUNT_MISMATCH", f"Wrong count for {item['item_id']}")
        if item["state"] == "retry_wait":
            if "next_eligible_at" not in item:
                raise M0ContractError(
                    "RETRY_DEADLINE_REQUIRED",
                    f"Retry-wait item {item['item_id']} requires a durable deadline",
                )
        elif "next_eligible_at" in item:
            raise M0ContractError(
                "INVALID_RETRY_DEADLINE",
                f"Non-waiting item {item['item_id']} cannot retain a retry deadline",
            )
        latest_attempt = _validate_terminal_item_latest_attempt(
            item, attempts_for_item[item["item_id"]]
        )
        receipt_id = item.get("storage_receipt_id")
        if item["state"] == "committed":
            receipt = receipts_by_id.get(receipt_id)
            if receipt_id is None:
                raise M0ContractError(
                    "COMMITTED_ITEM_INCOMPLETE",
                    f"Committed item {item['item_id']} lacks a StorageReceipt ID",
                )
            if receipt is None or receipt["item_id"] != item["item_id"]:
                raise M0ContractError(
                    "ITEM_RECEIPT_MISMATCH",
                    f"Item {item['item_id']} references no matching StorageReceipt",
                )
            if latest_attempt is None or latest_attempt.get("output", {}).get(
                "storage_receipt_id"
            ) != receipt_id:
                raise M0ContractError(
                    "COMMITTED_ITEM_INCOMPLETE",
                    f"Committed item {item['item_id']} latest attempt lacks its durable receipt",
                )
        elif receipt_id is not None:
            raise M0ContractError(
                "ITEM_RECEIPT_MISMATCH",
                f"Non-committed item {item['item_id']} cannot claim a committed receipt",
            )
    reuse_flags_present = any("reuse_verified" in item for item in document["items"])
    if reuse_flags_present:
        if any("reuse_verified" not in item for item in document["items"]):
            raise M0ContractError(
                "REUSE_ACCOUNTING_MISMATCH",
                "M1 reuse provenance must be present for every item or none",
            )
        verified_hits = sum(bool(item["reuse_verified"]) for item in document["items"])
        if any(
            item["reuse_verified"] and item["state"] != "committed"
            for item in document["items"]
        ):
            raise M0ContractError(
                "REUSE_ACCOUNTING_MISMATCH",
                "Only a verified committed item may be marked as reused",
            )
        if (
            document["reuse"]["verified_hits"] != verified_hits
            or document["reuse"]["misses"] != len(document["items"]) - verified_hits
        ):
            raise M0ContractError(
                "REUSE_ACCOUNTING_MISMATCH",
                "BatchState reuse totals differ from per-item provenance",
            )
    _validate_cost_exposure(document["cost"], code="BUDGET_STATE_INVALID")
    if document["status"] == "awaiting_agent_review" and "outcome" not in document:
        raise M0ContractError("INVALID_BATCH_STATE", "Terminal mechanical state requires outcome")
    if document["status"] == "awaiting_agent_review":
        expected_outcome = _mechanical_outcome([item["state"] for item in document["items"]])
        if document["outcome"] != expected_outcome:
            raise M0ContractError(
                "INVALID_BATCH_STATE",
                f"Terminal state outcome must be {expected_outcome}",
            )
    if invocations is not None:
        if "rate_limit_wait_seconds" not in document:
            raise M0ContractError(
                "M1_STATE_PROVENANCE_INCOMPLETE",
                "M1 BatchState requires durable rate-limit accounting",
            )
        if document["status"] == "awaiting_agent_review" and "completed_at" not in document:
            raise M0ContractError(
                "M1_STATE_PROVENANCE_INCOMPLETE",
                "Terminal M1 BatchState requires a stable completion timestamp",
            )
        if document["status"] != "awaiting_agent_review" and "completed_at" in document:
            raise M0ContractError(
                "M1_STATE_PROVENANCE_INCOMPLETE",
                "Non-terminal M1 BatchState cannot claim completion",
            )
    if "result_ref" in document and document["status"] != "awaiting_agent_review":
        raise M0ContractError(
            "INVALID_RESULT_REFERENCE",
            "Only terminal mechanical state may reference BatchResult",
        )


def validate_batch_result(document: Mapping[str, Any]) -> None:
    validate_contract("batch_result", document)
    _assert_no_sensitive_values(document)
    item_ids = [item["item_id"] for item in document["items"]]
    if len(item_ids) != len(set(item_ids)):
        raise M0ContractError("DUPLICATE_RESULT_ITEM", "BatchResult item IDs must be unique")
    invocation_ids = [entry["invocation_id"] for entry in document["invocations"]]
    if len(invocation_ids) != len(set(invocation_ids)):
        raise M0ContractError(
            "DUPLICATE_INVOCATION", "BatchResult invocation IDs must be unique"
        )
    states = [item["state"] for item in document["items"]]
    expected = {
        "successful": states.count("committed"),
        "cache_hit": states.count("cache_hit"),
        "failed": states.count("failed_terminal"),
        "blocked": states.count("blocked_by_dependency"),
        "indeterminate": states.count("indeterminate"),
        "cancelled": states.count("cancelled"),
    }
    if dict(document["counts"]) != expected:
        raise M0ContractError("RESULT_COUNT_MISMATCH", f"Expected counts {expected}")
    expected_outcome = _mechanical_outcome(states)
    if document["outcome"] != expected_outcome:
        raise M0ContractError(
            "RESULT_OUTCOME_MISMATCH", f"Outcome must be {expected_outcome} for item states"
        )
    _validate_dependency_blockers(document["items"])
    receipt_ids: set[str] = set()
    for item in document["items"]:
        if item["state"] in {"committed", "cache_hit"}:
            if "storage_receipt" not in item:
                raise M0ContractError(
                    "INVALID_BATCH_RESULT", f"{item['item_id']} lacks a storage receipt"
                )
            receipt = item["storage_receipt"]
            if receipt["receipt_id"] in receipt_ids:
                raise M0ContractError(
                    "DUPLICATE_STORAGE_RECEIPT", "BatchResult receipt IDs must be unique"
                )
            if receipt["batch_id"] != document["batch_id"] or receipt["item_id"] != item[
                "item_id"
            ]:
                raise M0ContractError(
                    "RESULT_RECEIPT_IDENTITY_MISMATCH",
                    f"Receipt does not bind result item {item['item_id']}",
                )
            validate_storage_receipt(receipt)
            receipt_ids.add(receipt["receipt_id"])
            if "error" in item:
                raise M0ContractError(
                    "INVALID_BATCH_RESULT", f"Successful item {item['item_id']} cannot carry an error"
                )
        else:
            if "storage_receipt" in item:
                raise M0ContractError(
                    "INVALID_BATCH_RESULT",
                    f"Non-success item {item['item_id']} cannot carry a success receipt",
                )
            if item["state"] in {"failed_terminal", "indeterminate"} and "error" not in item:
                raise M0ContractError(
                    "INVALID_BATCH_RESULT", f"{item['item_id']} lacks a structured error"
                )
            if item["state"] == "blocked_by_dependency" and "error" in item:
                raise M0ContractError(
                    "DEPENDENCY_BLOCKER_INVALID",
                    f"Blocked item {item['item_id']} cannot claim a provider error",
                )
    _validate_cost_exposure(document["cost"], code="BUDGET_RESULT_INVALID")


__all__ = [
    "CANONICAL_JSON_VERSION",
    "INITIAL_ADAPTER_IDENTITY",
    "MVP_ADAPTER_SUPPORT",
    "M0ContractError",
    "SCHEMA_NAMES",
    "adapter_observation_blockers",
    "canonical_json_bytes",
    "canonical_sha256",
    "compute_idempotency_digest",
    "compute_work_item_digest",
    "derive_attempt_output_path",
    "exact_identity",
    "freeze_batch_request",
    "freeze_self_digest",
    "load_execution_schema",
    "validate_adapter_observation",
    "validate_attempt",
    "validate_attempt_output_path",
    "validate_batch_request",
    "validate_batch_result",
    "validate_batch_state",
    "validate_contract",
    "validate_exact_identity",
    "validate_logical_path",
    "validate_storage_receipt",
]
