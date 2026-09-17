"""Pure validators and deterministic helpers for Workspace v1 contracts.

This module is intentionally limited to JSON-shaped values.  It does not read
projects, resolve producer authority, register routes, or mutate production
state.  JSON Schema defines the wire shape; the checks here cover cross-field
semantics that JSON Schema cannot express safely.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from hashlib import sha256
import json
import re
from typing import Any
from urllib.parse import unquote, urlsplit

from jsonschema import ValidationError

from schemas.workspace import load_workspace_v1_schema, workspace_v1_validator
from schemas.artifacts import validate_artifact

from .types import SourceSnapshot, WorkspaceProjection


SOURCE_SNAPSHOT_ALGORITHM = "canonical-source-entries-v1"

# Definitions are an explicit API.  Adding a new schema definition does not
# silently make it consumable through this module.
WORKSPACE_V1_DEFINITIONS = frozenset(
    {
        "identifier",
        "local_id",
        "resource_key",
        "digest",
        "resource_kind",
        "resource_identity",
        "revision_ref",
        "evidence_ref",
        "authority_descriptor",
        "source_entry",
        "source_snapshot",
        "typed_relation",
        "resource_ref",
        "capability_entry",
        "capability_map",
        "diagnostic",
        "pagination_cursor",
        "pagination",
        "media_metadata",
        "media_locator",
        "media_ref",
        "instruction_source_locator",
        "generation_instruction",
        "resource_summary_data",
        "script_display",
        "script_voice_performance",
        "script_section",
        "script_delivery_cues",
        "script_enhancement_cue",
        "script_pronunciation_guide",
        "style_display",
        "style_proposal",
        "style_selected_concept",
        "style_observation",
        "style_checkpoint_observation",
        "style_observations",
        "style_resolved",
        "style_catalog",
        "style_identity",
        "style_visual_language",
        "style_color_palette",
        "style_font_spec",
        "style_typography",
        "style_motion",
        "style_audio",
        "style_asset_generation",
        "style_taste_profile",
        "course_design",
        "course_id",
        "course_id_array",
        "course_promise",
        "course_objective",
        "course_teaching_beat",
        "course_lesson",
        "course_module",
        "course_assessment",
        "course_source",
        "course_glossary",
        "course_notation",
        "course_style_intent",
        "course_delivery_requirements",
        "projected_revision",
        "revision_set_data",
        "catalog_item",
        "catalog_data",
        "stage_summary",
        "shell_data",
        "media_collection_data",
        "generation_instruction_collection_data",
        "qualification_identity",
        "candidate_handoff_provenance",
        "production_unit_progress",
        "production_unit_summary_data",
        "timeline_segment",
        "audio_track",
        "preview_timeline_data",
        "workspace_projection",
    }
)

_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_SOURCE_KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,255}$")
_ACTIVE_AUTHORITY_STATES = {"canonical", "candidate", "execution_evidence"}
_LEGACY_SOURCE_KINDS = {"legacy_loose_file", "legacy_scan"}
_EXECUTION_EVIDENCE_SOURCE_KINDS = {
    "project_marker",
    "pipeline_manifest",
    "approved_checkpoint_artifact",
    "checkpoint_partial_progress",
    "checkpoint_candidate_handoff",
    "production_unit_qualification_profile",
    "production_unit_capability_matrix",
    "production_unit_execution_contract",
    "batch_v2_publication",
    "style_catalog_current",
    "render_report_output",
    "provider_request",
    "provider_receipt",
    "binary_observation",
    "human_review_record",
}
_CREATIVE_INSTRUCTION_SOURCE_KINDS = {
    "approved_checkpoint_artifact",
    "awaiting_checkpoint_artifact",
    "batch_v2_publication",
    "legacy_loose_file",
}
_INSTRUCTION_SOURCE_KINDS_BY_KIND = {
    "creative_specification": _CREATIVE_INSTRUCTION_SOURCE_KINDS,
    "provider_input": {"provider_request", "provider_receipt"},
    "negative_prompt": _CREATIVE_INSTRUCTION_SOURCE_KINDS,
    "narration_text": _CREATIVE_INSTRUCTION_SOURCE_KINDS,
    "delivery_contract": _CREATIVE_INSTRUCTION_SOURCE_KINDS,
    "music_intent": _CREATIVE_INSTRUCTION_SOURCE_KINDS,
    "sfx_intent": _CREATIVE_INSTRUCTION_SOURCE_KINDS,
    "search_query": _CREATIVE_INSTRUCTION_SOURCE_KINDS,
}
_EVIDENCE_SCOPE_SOURCE_KINDS = {
    "manifest_only": {
        "project_marker",
        "pipeline_manifest",
        "style_catalog_current",
        "legacy_loose_file",
        "legacy_scan",
    },
    "checkpoint_validated": {
        "approved_checkpoint_artifact",
        "awaiting_checkpoint_artifact",
        "working_checkpoint_artifact",
        "failed_checkpoint_artifact",
        "checkpoint_partial_progress",
        "checkpoint_candidate_handoff",
        "production_unit_qualification_profile",
        "production_unit_capability_matrix",
        "production_unit_execution_contract",
        "render_report_output",
    },
    "publication_validated": {"batch_v2_publication"},
    "provider_request": {"provider_request"},
    "provider_receipt": {"provider_receipt"},
    "binary_observed": {"binary_observation"},
    "human_reviewed": {"human_review_record"},
}
_INSTRUCTION_EVIDENCE_SCOPE_BY_SOURCE_KIND = {
    "approved_checkpoint_artifact": "checkpoint_validated",
    "awaiting_checkpoint_artifact": "checkpoint_validated",
    "batch_v2_publication": "publication_validated",
    "legacy_loose_file": "manifest_only",
    "provider_request": "provider_request",
    "provider_receipt": "provider_receipt",
}
_QUALIFIED_STATUSES = {
    "unsupported",
    "experimental",
    "code_complete",
    "beta_qualified",
    "production_qualified",
}


class WorkspaceContractError(ValueError):
    """A schema or semantic violation in a Workspace wire value."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        path: Sequence[str | int] = (),
    ) -> None:
        self.code = code
        self.path = tuple(path)
        location = "$" + "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}" for part in self.path
        )
        super().__init__(f"{code} at {location}: {message}")


def _require_definition(definition: str) -> None:
    if definition not in WORKSPACE_V1_DEFINITIONS:
        raise KeyError(f"Workspace v1 definition is not public: {definition}")


def workspace_contract_schema(
    definition: str = "workspace_projection",
) -> dict[str, Any]:
    """Return a caller-owned schema bundle rooted at one public definition."""

    _require_definition(definition)
    schema = load_workspace_v1_schema()
    schema["$ref"] = f"#/$defs/{definition}"
    return deepcopy(schema)


def _schema_validate(value: Any, definition: str) -> None:
    _require_definition(definition)
    try:
        workspace_v1_validator(definition).validate(value)
    except ValidationError as exc:
        raise WorkspaceContractError(
            "schema_validation_failed",
            exc.message,
            path=tuple(exc.absolute_path),
        ) from exc


def _fail(
    code: str,
    message: str,
    path: Sequence[str | int],
) -> None:
    raise WorkspaceContractError(code, message, path=path)


def _source_pairs(
    sources: Iterable[Mapping[str, Any]],
) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, Mapping):
            _fail("invalid_source_entry", "source must be an object", (index,))
        source_key = source.get("source_key")
        digest = source.get("sha256")
        if not isinstance(source_key, str) or not _SOURCE_KEY_RE.fullmatch(source_key):
            _fail(
                "invalid_source_key",
                "source_key is not a Workspace identifier",
                (index, "source_key"),
            )
        if not isinstance(digest, str) or not _DIGEST_RE.fullmatch(digest):
            _fail(
                "invalid_source_digest",
                "sha256 must use the sha256:<lowercase-hex> form",
                (index, "sha256"),
            )
        if source_key in seen:
            _fail(
                "duplicate_source_key",
                f"source_key {source_key!r} occurs more than once",
                (index, "source_key"),
            )
        seen.add(source_key)
        pairs.append((source_key, digest))
    return pairs


def _digest_sources(sources: Iterable[Mapping[str, Any]]) -> str:
    canonical_sources = sorted(
        (deepcopy(dict(source)) for source in sources),
        key=lambda source: source["source_key"],
    )
    payload = json.dumps(
        canonical_sources,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{sha256(payload).hexdigest()}"


def source_snapshot_digest(sources: Iterable[Mapping[str, Any]]) -> str:
    """Hash complete source entries sorted by ``source_key`` as canonical JSON."""

    entries = deepcopy(list(sources))
    for entry in entries:
        _schema_validate(entry, "source_entry")
    _source_pairs(entries)
    return _digest_sources(entries)


def build_source_snapshot(sources: Iterable[Mapping[str, Any]]) -> SourceSnapshot:
    """Build and validate a sorted, caller-owned source snapshot."""

    entries = deepcopy(list(sources))
    for entry in entries:
        _schema_validate(entry, "source_entry")
    _source_pairs(entries)
    entries.sort(key=lambda entry: entry["source_key"])
    snapshot: SourceSnapshot = {
        "algorithm": SOURCE_SNAPSHOT_ALGORITHM,
        "sources": entries,  # type: ignore[typeddict-item]
        "composite_sha256": _digest_sources(entries),
    }
    _schema_validate(snapshot, "source_snapshot")
    _validate_source_snapshot(snapshot, ())
    return deepcopy(snapshot)


def _validate_source_snapshot(
    snapshot: Mapping[str, Any], path: Sequence[str | int]
) -> None:
    sources = snapshot["sources"]
    pairs = _source_pairs(sources)
    keys = [source_key for source_key, _ in pairs]
    if keys != sorted(keys):
        _fail(
            "unsorted_source_snapshot",
            "sources must be ordered by source_key",
            (*path, "sources"),
        )
    expected = _digest_sources(sources)
    if snapshot["composite_sha256"] != expected:
        _fail(
            "source_snapshot_digest_mismatch",
            f"expected {expected}",
            (*path, "composite_sha256"),
        )


def _validate_authority(
    authority: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    path: Sequence[str | int],
) -> None:
    state = authority["authority_state"]
    validation = authority["validation_state"]
    source_kind = authority["source_kind"]
    source_by_key = {
        source["source_key"]: source["sha256"] for source in snapshot["sources"]
    }
    source_kind_by_key = {
        source["source_key"]: source["source_kind"] for source in snapshot["sources"]
    }
    source_entry_by_key = {
        source["source_key"]: source for source in snapshot["sources"]
    }

    evidence_keys: set[str] = set()
    for index, evidence in enumerate(authority["evidence_refs"]):
        key = evidence["source_key"]
        if key in evidence_keys:
            _fail(
                "duplicate_evidence_source",
                f"evidence source {key!r} occurs more than once",
                (*path, "evidence_refs", index, "source_key"),
            )
        evidence_keys.add(key)
        if key not in source_by_key:
            _fail(
                "evidence_source_not_in_snapshot",
                f"evidence source {key!r} is absent from the source snapshot",
                (*path, "evidence_refs", index, "source_key"),
            )
        if evidence["sha256"] != source_by_key[key]:
            _fail(
                "evidence_digest_mismatch",
                f"evidence digest for {key!r} differs from the source snapshot",
                (*path, "evidence_refs", index, "sha256"),
            )

    evidence_scope = authority["evidence_scope"]
    evidence_kinds = {source_kind_by_key[key] for key in evidence_keys}
    if evidence_scope == "none":
        if evidence_keys:
            _fail(
                "none_scope_with_evidence",
                "evidence_scope 'none' cannot cite evidence sources",
                (*path, "evidence_scope"),
            )
        if state != "unavailable" or source_kind != "unavailable":
            _fail(
                "none_scope_requires_unavailable",
                "evidence_scope 'none' is reserved for unavailable authority with no claimed source family",
                (*path, "evidence_scope"),
            )
    elif not (evidence_kinds & _EVIDENCE_SCOPE_SOURCE_KINDS[evidence_scope]):
        _fail(
            "unsupported_evidence_scope",
            f"evidence_scope {evidence_scope!r} requires a compatible cited evidence source",
            (*path, "evidence_scope"),
        )

    if source_kind not in {"derived_projection", "unavailable"} and not any(
        source_kind_by_key[key] == source_kind for key in evidence_keys
    ):
        _fail(
            "authority_source_kind_mismatch",
            "authority source_kind is not present in its bound evidence sources",
            (*path, "source_kind"),
        )

    if source_kind == "derived_projection" and state != "unavailable":
        evidence_sources = [source_entry_by_key[key] for key in evidence_keys]
        if not evidence_kinds:
            _fail(
                "derived_authority_without_evidence",
                "a visible derived projection requires explicit bound evidence",
                (*path, "evidence_refs"),
            )
        if state == "canonical":
            _fail(
                "derived_canonical_authority",
                "a derived projection may reflect producer authority but cannot itself become canonical",
                (*path, "authority_state"),
            )
        if (
            state == "candidate"
            and "awaiting_checkpoint_artifact" not in evidence_kinds
        ):
            _fail(
                "derived_candidate_without_awaiting_evidence",
                "derived candidate authority requires awaiting-checkpoint evidence",
                (*path, "evidence_refs"),
            )
        if state == "execution_evidence" and not (
            evidence_kinds & _EXECUTION_EVIDENCE_SOURCE_KINDS
        ):
            _fail(
                "derived_execution_without_trusted_evidence",
                "derived execution evidence requires at least one non-legacy validated source family",
                (*path, "evidence_refs"),
            )
        if evidence_kinds <= _LEGACY_SOURCE_KINDS and (
            state != "display_only" or validation != "unverified"
        ):
            _fail(
                "derived_legacy_authority_escalation",
                "legacy-only evidence remains display_only and unverified after derivation",
                path,
            )
        legacy_evidence = [
            source
            for source in evidence_sources
            if source["source_kind"] in _LEGACY_SOURCE_KINDS
        ]
        if legacy_evidence and (
            state in _ACTIVE_AUTHORITY_STATES or validation == "validated"
        ):
            if state == "execution_evidence":
                corroborating_evidence = [
                    source
                    for source in evidence_sources
                    if source["source_kind"] in _EXECUTION_EVIDENCE_SOURCE_KINDS
                ]
            elif state == "candidate":
                corroborating_evidence = [
                    source
                    for source in evidence_sources
                    if source["source_kind"] == "awaiting_checkpoint_artifact"
                ]
            else:
                corroborating_evidence = [
                    source
                    for source in evidence_sources
                    if source["source_kind"]
                    not in {*_LEGACY_SOURCE_KINDS, "derived_projection", "unavailable"}
                ]

            def shares_binding(
                legacy: Mapping[str, Any], corroborating: Mapping[str, Any]
            ) -> bool:
                legacy_resource = legacy.get("resource_ref")
                corroborating_resource = corroborating.get("resource_ref")
                if (
                    legacy_resource is not None
                    and corroborating_resource is not None
                    and _identity_key(legacy_resource)
                    == _identity_key(corroborating_resource)
                ):
                    return True
                legacy_revision = legacy.get("revision_ref")
                corroborating_revision = corroborating.get("revision_ref")
                return (
                    legacy_revision is not None
                    and corroborating_revision is not None
                    and legacy_revision == corroborating_revision
                )

            if any(
                not any(
                    shares_binding(legacy, corroborating)
                    for corroborating in corroborating_evidence
                )
                for legacy in legacy_evidence
            ):
                _fail(
                    "derived_unrelated_evidence",
                    "every legacy evidence source must share an exact resource or revision binding with non-legacy corroboration",
                    (*path, "evidence_refs"),
                )

    if state in _ACTIVE_AUTHORITY_STATES:
        if validation != "validated":
            _fail(
                "unvalidated_active_authority",
                f"{state} authority requires validated evidence",
                (*path, "validation_state"),
            )
        if not authority["evidence_refs"] or not snapshot["sources"]:
            _fail(
                "active_authority_without_evidence",
                f"{state} authority requires a non-empty bound source set",
                (*path, "evidence_refs"),
            )

    if validation == "invalid" and state != "unavailable":
        _fail(
            "invalid_authority_escalation",
            "invalid evidence may only produce unavailable authority",
            (*path, "authority_state"),
        )
    if validation == "unverified" and state not in {"display_only", "unavailable"}:
        _fail(
            "unverified_authority_escalation",
            "unverified evidence may only be display-only or unavailable",
            (*path, "authority_state"),
        )

    if source_kind in {"legacy_loose_file", "legacy_scan"} and state != "unavailable":
        if state != "display_only" or validation != "unverified":
            _fail(
                "legacy_authority_escalation",
                "legacy evidence must remain display_only and unverified",
                path,
            )
    if source_kind == "awaiting_checkpoint_artifact" and state != "unavailable":
        if (
            state != "candidate"
            or validation != "validated"
            or authority.get("checkpoint_status") != "awaiting_human"
        ):
            _fail(
                "invalid_awaiting_authority",
                "awaiting checkpoint evidence must remain a validated candidate",
                path,
            )
    if source_kind == "working_checkpoint_artifact" and state != "unavailable":
        if (
            state != "display_only"
            or authority.get("checkpoint_status") != "in_progress"
        ):
            _fail(
                "working_authority_escalation",
                "working checkpoint evidence must remain an in-progress display snapshot",
                path,
            )
    if source_kind == "failed_checkpoint_artifact" and state != "unavailable":
        if state != "display_only" or authority.get("checkpoint_status") != "failed":
            _fail(
                "failed_authority_escalation",
                "failed checkpoint evidence must remain a failed display snapshot",
                path,
            )
    if source_kind == "approved_checkpoint_artifact" and state != "unavailable":
        if (
            state not in {"canonical", "display_only"}
            or validation != "validated"
            or authority.get("checkpoint_status") != "completed"
        ):
            _fail(
                "invalid_approved_authority",
                "approved checkpoint evidence must be completed validated evidence; history remains display-only",
                path,
            )
    if source_kind == "batch_v2_publication" and state != "unavailable":
        if (
            state not in {"canonical", "execution_evidence"}
            or validation != "validated"
        ):
            _fail(
                "publication_authority_escalation",
                "Batch V2 data must remain validated canonical or bounded execution evidence",
                path,
            )
    if source_kind == "render_report_output" and state != "unavailable":
        if (
            state not in {"canonical", "execution_evidence"}
            or validation != "validated"
            or authority.get("checkpoint_status") != "completed"
        ):
            _fail(
                "invalid_render_output_authority",
                "render-report output requires completed validated evidence",
                path,
            )
    if source_kind in {
        "checkpoint_partial_progress",
        "checkpoint_candidate_handoff",
        "production_unit_qualification_profile",
        "production_unit_capability_matrix",
        "production_unit_execution_contract",
        "provider_request",
        "provider_receipt",
        "binary_observation",
        "human_review_record",
    } and state not in {"execution_evidence", "unavailable"}:
        _fail(
            "execution_evidence_authority_escalation",
            f"{source_kind} may only be bounded execution evidence",
            (*path, "authority_state"),
        )
    if (
        source_kind == "style_catalog_current"
        and authority.get("historically_frozen") is True
    ):
        _fail(
            "current_style_claimed_historical",
            "the current Style catalog does not prove historically frozen bytes",
            (*path, "historically_frozen"),
        )
    if source_kind == "unavailable" and validation == "validated":
        _fail(
            "fabricated_unavailable_validation",
            "an unavailable source cannot claim validated evidence",
            (*path, "validation_state"),
        )


def _identity_key(resource: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        resource.get("project_id"),
        resource.get("kind"),
        resource.get("stage"),
        resource.get("local_id"),
        resource.get("resource_key"),
    )


def _validate_resource_ref(
    resource: Mapping[str, Any], path: Sequence[str | int]
) -> None:
    project_id = resource["project_id"]
    for index, parent in enumerate(resource["parent_refs"]):
        if parent["project_id"] != project_id:
            _fail(
                "cross_project_parent",
                "a parent ref must belong to the same direct-child project",
                (*path, "parent_refs", index),
            )

    relation_ids: set[str] = set()
    own_identity = _identity_key(resource)
    for index, relation in enumerate(resource["relation_refs"]):
        relation_path = (*path, "relation_refs", index)
        relation_id = relation["relation_id"]
        if relation_id in relation_ids:
            _fail(
                "duplicate_relation_id",
                f"relation_id {relation_id!r} occurs more than once",
                (*relation_path, "relation_id"),
            )
        relation_ids.add(relation_id)
        related = [*relation["source_refs"], *relation["target_refs"]]
        if any(ref["project_id"] != project_id for ref in related):
            _fail(
                "cross_project_relation",
                "relation refs must belong to the same direct-child project",
                relation_path,
            )
        if own_identity not in {_identity_key(ref) for ref in related}:
            _fail(
                "unbound_resource_relation",
                "a ResourceRef relation must include that resource",
                relation_path,
            )


def _validate_diagnostics(
    diagnostics: Sequence[Mapping[str, Any]],
    snapshot: Mapping[str, Any],
    project_id: str,
    path: Sequence[str | int],
) -> None:
    source_keys = {source["source_key"] for source in snapshot["sources"]}
    for index, diagnostic in enumerate(diagnostics):
        for key in diagnostic["source_keys"]:
            if key not in source_keys:
                _fail(
                    "diagnostic_source_not_in_snapshot",
                    f"diagnostic source {key!r} is absent from the bound snapshot",
                    (*path, index, "source_keys"),
                )
        if any(ref["project_id"] != project_id for ref in diagnostic["resource_refs"]):
            _fail(
                "cross_project_diagnostic",
                "diagnostic resource refs must belong to the projection project",
                (*path, index, "resource_refs"),
            )


def _validate_snapshot_project(
    snapshot: Mapping[str, Any],
    project_id: str,
    path: Sequence[str | int],
) -> None:
    for index, source in enumerate(snapshot["sources"]):
        source_resource = source.get("resource_ref")
        if source_resource is not None and source_resource["project_id"] != project_id:
            _fail(
                "cross_project_snapshot_source",
                "source resource belongs to a different project",
                (*path, "sources", index, "resource_ref"),
            )


def _validate_snapshot_covered(
    child_snapshot: Mapping[str, Any],
    parent_snapshot: Mapping[str, Any],
    path: Sequence[str | int],
) -> None:
    parent_sources = {
        json.dumps(source, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for source in parent_snapshot["sources"]
    }
    child_sources = {
        json.dumps(source, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for source in child_snapshot["sources"]
    }
    if not child_sources.issubset(parent_sources):
        _fail(
            "nested_source_not_in_projection_snapshot",
            "nested source evidence must be included in the projection snapshot",
            path,
        )


def _validate_revision_bound(
    revision: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    path: Sequence[str | int],
    *,
    projection_error: str,
    unbound_error: str,
    subject: str,
) -> None:
    if revision["revision_kind"] == "projection":
        if revision["sha256"] != snapshot["composite_sha256"]:
            _fail(
                projection_error,
                f"projection revision must equal the {subject} source snapshot digest",
                (*path, "sha256"),
            )
        return

    if not any(
        source["sha256"] == revision["sha256"]
        and source.get("revision_ref") == revision
        for source in snapshot["sources"]
    ):
        _fail(
            unbound_error,
            f"exact non-projection {subject} RevisionRef must be represented in its source snapshot",
            path,
        )


def _validate_typed_relation(
    relation: Mapping[str, Any], path: Sequence[str | int]
) -> None:
    refs = [*relation["source_refs"], *relation["target_refs"]]
    project_ids = {ref["project_id"] for ref in refs}
    if len(project_ids) != 1:
        _fail(
            "cross_project_relation",
            "all relation endpoints must belong to one direct-child project",
            path,
        )
    _validate_snapshot_project(
        relation["source_snapshot"],
        refs[0]["project_id"],
        (*path, "source_snapshot"),
    )


def _validate_locator(locator: Mapping[str, Any], path: Sequence[str | int]) -> None:
    href = locator["href"]
    if locator["kind"] == "approved_remote":
        parsed = urlsplit(href)
        if (
            parsed.scheme != "https"
            or not parsed.netloc
            or parsed.username
            or parsed.password
        ):
            _fail(
                "unsafe_remote_locator",
                "approved remote media requires credential-free HTTPS authority",
                (*path, "href"),
            )
        return

    parsed = urlsplit(href)
    if (
        parsed.scheme
        or parsed.netloc
        or parsed.fragment
        or "\\" in href
        or "\x00" in href
    ):
        _fail(
            "unsafe_workspace_locator",
            "workspace media locators must be local versioned API routes",
            (*path, "href"),
        )
    decoded = href
    for _ in range(3):
        expanded = unquote(decoded)
        if expanded == decoded:
            break
        decoded = expanded
    decoded_path = urlsplit(decoded).path
    if (
        "\\" in decoded
        or "\x00" in decoded
        or any(part in {".", ".."} for part in decoded_path.split("/"))
    ):
        _fail(
            "unsafe_workspace_locator",
            "workspace media locator contains an unsafe path segment",
            (*path, "href"),
        )
    if not decoded_path.startswith("/api/workspace/v1/"):
        _fail(
            "unversioned_workspace_locator",
            "workspace media locator is outside /api/workspace/v1",
            (*path, "href"),
        )


def _validate_media_ref(media: Mapping[str, Any], path: Sequence[str | int]) -> None:
    owner = media["owner_ref"]
    snapshot = media["source_snapshot"]
    _validate_snapshot_project(
        snapshot,
        owner["project_id"],
        (*path, "source_snapshot"),
    )
    snapshot_by_key = {
        source["source_key"]: source["sha256"] for source in snapshot["sources"]
    }
    source_kind_by_key = {
        source["source_key"]: source["source_kind"] for source in snapshot["sources"]
    }
    snapshot_digests = set(snapshot_by_key.values())
    owner_revision_sources = [
        source
        for source in snapshot["sources"]
        if source["sha256"] == media["owner_revision"]["sha256"]
        and source.get("revision_ref") == media["owner_revision"]
        and source.get("resource_ref") is not None
        and _identity_key(source["resource_ref"]) == _identity_key(owner)
    ]
    if not owner_revision_sources:
        _fail(
            "unbound_media_owner_revision",
            "exact owner ResourceRef and RevisionRef must be represented in the media source snapshot",
            (*path, "owner_revision"),
        )
    if media["proxy_source_media_id"] == media["media_id"]:
        _fail(
            "self_referential_preview_proxy",
            "a preview proxy must identify a distinct source media representation",
            (*path, "proxy_source_media_id"),
        )
    if media["purpose"] == "preview_proxy":
        lineage_key = f"media-id:{media['proxy_source_media_id']}"
        lineage_sources = [
            source
            for source in snapshot["sources"]
            if source["source_key"] == lineage_key
            and source["source_kind"] == "binary_observation"
            and source["sha256"] == media["source_sha256"]
            and source.get("resource_ref") is not None
            and _identity_key(source["resource_ref"]) == _identity_key(owner)
            and source.get("revision_ref") == media["owner_revision"]
        ]
        if not lineage_sources:
            _fail(
                "unbound_preview_proxy_source",
                "preview proxy source identity, owner, revision, and digest must be bound by a binary media-id:<id> source entry",
                (*path, "proxy_source_media_id"),
            )
    authority = media["authority"]
    if (
        authority["source_kind"] == "derived_projection"
        and authority["authority_state"] != "unavailable"
    ):
        evidence = {
            (item["source_key"], item["sha256"]) for item in authority["evidence_refs"]
        }
        owner_evidence = [
            source
            for source in snapshot["sources"]
            if (source["source_key"], source["sha256"]) in evidence
            and source.get("resource_ref") is not None
            and _identity_key(source["resource_ref"]) == _identity_key(owner)
            and source.get("revision_ref") == media["owner_revision"]
        ]
        if not owner_evidence:
            _fail(
                "derived_media_without_owner_evidence",
                "derived media authority must cite evidence bound to its exact owner revision",
                (*path, "authority", "evidence_refs"),
            )
        owner_evidence_kinds = {source["source_kind"] for source in owner_evidence}
        if authority["authority_state"] == "candidate" and (
            "awaiting_checkpoint_artifact" not in owner_evidence_kinds
        ):
            _fail(
                "derived_media_candidate_without_owner_evidence",
                "derived candidate media requires owner-bound awaiting-checkpoint evidence",
                (*path, "authority", "evidence_refs"),
            )
        if authority["authority_state"] == "execution_evidence" and not (
            owner_evidence_kinds & _EXECUTION_EVIDENCE_SOURCE_KINDS
        ):
            _fail(
                "derived_media_execution_without_owner_evidence",
                "derived execution media requires owner-bound non-legacy producer or observation evidence",
                (*path, "authority", "evidence_refs"),
            )
        if owner_evidence_kinds <= _LEGACY_SOURCE_KINDS and (
            authority["authority_state"] != "display_only"
            or authority["validation_state"] != "unverified"
        ):
            _fail(
                "derived_media_legacy_escalation",
                "derived legacy media remains display_only and unverified",
                (*path, "authority"),
            )
    if (
        media["source_sha256"] is not None
        and media["source_sha256"] not in snapshot_digests
    ):
        _fail(
            "unbound_media_source_digest",
            "source_sha256 must be represented in the media source snapshot",
            (*path, "source_sha256"),
        )
    if media["locator"] is not None:
        _validate_locator(media["locator"], (*path, "locator"))
        if media["locator"]["kind"] == "approved_remote":
            allowed_remote_sources = {
                "approved_checkpoint_artifact",
                "batch_v2_publication",
                "render_report_output",
            }
            if (
                authority["source_kind"] not in allowed_remote_sources
                or authority["validation_state"] != "validated"
                or authority["authority_state"]
                not in {"canonical", "execution_evidence"}
            ):
                _fail(
                    "unapproved_remote_media",
                    "remote media requires validated approved publication evidence",
                    (*path, "locator", "kind"),
                )
    if media["purpose"] == "preview_proxy" and media["locator"] is not None:
        if media["locator"]["kind"] != "workspace_route":
            _fail(
                "external_preview_proxy",
                "preview proxies must use the disposable Workspace route boundary",
                (*path, "locator", "kind"),
            )
    metadata_fields = {
        "declared_metadata": "producer_declared",
        "observed_metadata": "tool_observed",
        "review_metadata": "human_reviewed",
    }
    for field, expected in metadata_fields.items():
        metadata = media[field]
        if metadata is not None:
            if metadata["evidence_kind"] != expected:
                _fail(
                    "misclassified_media_evidence",
                    f"{field} must use evidence_kind={expected}",
                    (*path, field, "evidence_kind"),
                )
            evidence_keys: set[str] = set()
            for index, evidence in enumerate(metadata["evidence_refs"]):
                key = evidence["source_key"]
                if key in evidence_keys:
                    _fail(
                        "duplicate_media_metadata_evidence",
                        f"metadata evidence source {key!r} occurs more than once",
                        (*path, field, "evidence_refs", index, "source_key"),
                    )
                evidence_keys.add(key)
                if key not in snapshot_by_key:
                    _fail(
                        "media_metadata_source_not_in_snapshot",
                        f"metadata evidence source {key!r} is absent from the media snapshot",
                        (*path, field, "evidence_refs", index, "source_key"),
                    )
                if evidence["sha256"] != snapshot_by_key[key]:
                    _fail(
                        "media_metadata_digest_mismatch",
                        f"metadata evidence digest for {key!r} differs from the media snapshot",
                        (*path, field, "evidence_refs", index, "sha256"),
                    )
                source_kind = source_kind_by_key[key]
                if expected == "tool_observed" and source_kind != "binary_observation":
                    _fail(
                        "invalid_observed_metadata_source",
                        "tool-observed metadata requires binary_observation evidence",
                        (*path, field, "evidence_refs", index, "source_key"),
                    )
                if (
                    expected == "human_reviewed"
                    and source_kind != "human_review_record"
                ):
                    _fail(
                        "invalid_human_review_source",
                        "human-reviewed metadata requires human_review_record evidence",
                        (*path, field, "evidence_refs", index, "source_key"),
                    )
                if expected == "producer_declared" and source_kind in {
                    "binary_observation",
                    "human_review_record",
                }:
                    _fail(
                        "invalid_declared_metadata_source",
                        "producer-declared metadata requires producer-owned source evidence",
                        (*path, field, "evidence_refs", index, "source_key"),
                    )

    if media["availability"] == "unavailable":
        if not media["diagnostics"] and not media["authority"]["degraded_reasons"]:
            _fail(
                "unexplained_media_unavailability",
                "unavailable media requires an explicit diagnostic or degraded reason",
                (*path, "availability"),
            )
    _validate_diagnostics(
        media["diagnostics"],
        media["source_snapshot"],
        owner["project_id"],
        (*path, "diagnostics"),
    )


def _validate_generation_instruction(
    instruction: Mapping[str, Any], path: Sequence[str | int]
) -> None:
    project_id = instruction["resource_ref"]["project_id"]
    _validate_snapshot_project(
        instruction["source_snapshot"],
        project_id,
        (*path, "source_snapshot"),
    )
    _validate_revision_bound(
        instruction["revision_ref"],
        instruction["source_snapshot"],
        (*path, "revision_ref"),
        projection_error="instruction_projection_digest_mismatch",
        unbound_error="unbound_instruction_revision",
        subject="instruction",
    )
    related = [instruction["creative_scope_ref"], *instruction["target_refs"]]
    if any(ref["project_id"] != project_id for ref in related):
        _fail(
            "cross_project_instruction",
            "instruction scope and targets must belong to the same project",
            path,
        )

    locator = instruction["source_locator"]
    if locator is not None:
        source_key = locator["source_key"]
        snapshot_sources = {
            source["source_key"]: source
            for source in instruction["source_snapshot"]["sources"]
        }
        if source_key not in snapshot_sources:
            _fail(
                "instruction_source_not_in_snapshot",
                f"instruction source {source_key!r} is absent from the bound snapshot",
                (*path, "source_locator", "source_key"),
            )
        authority_evidence_keys = {
            evidence["source_key"]
            for evidence in instruction["authority"]["evidence_refs"]
        }
        if source_key not in authority_evidence_keys:
            _fail(
                "instruction_locator_not_authority_evidence",
                "instruction source locator must identify evidence used by its authority descriptor",
                (*path, "source_locator", "source_key"),
            )
        locator_source = snapshot_sources[source_key]
        locator_resource = locator_source.get("resource_ref")
        locator_revision = locator_source.get("revision_ref")
        if (
            locator_resource is None
            or _identity_key(locator_resource)
            != _identity_key(instruction["resource_ref"])
            or locator_revision != instruction["revision_ref"]
            or locator_source["sha256"] != instruction["revision_ref"]["sha256"]
        ):
            _fail(
                "instruction_locator_not_owner_bound",
                "instruction source locator must select evidence bound to the exact instruction ResourceRef and RevisionRef",
                (*path, "source_locator", "source_key"),
            )
        locator_kind = locator_source["source_kind"]
        allowed_locator_kinds = _INSTRUCTION_SOURCE_KINDS_BY_KIND[
            instruction["instruction_kind"]
        ]
        if locator_kind not in allowed_locator_kinds:
            _fail(
                "instruction_locator_source_family_mismatch",
                f"{locator_kind!r} cannot govern {instruction['instruction_kind']!r} instruction content",
                (*path, "source_locator", "source_key"),
            )
        authority = instruction["authority"]
        expected_scope = _INSTRUCTION_EVIDENCE_SCOPE_BY_SOURCE_KIND[locator_kind]
        if authority["evidence_scope"] != expected_scope:
            _fail(
                "instruction_evidence_scope_mismatch",
                f"{locator_kind!r} instruction evidence requires {expected_scope!r} scope",
                (*path, "authority", "evidence_scope"),
            )
        authority_kind = authority["source_kind"]
        if authority_kind not in {"derived_projection", "unavailable"}:
            if locator_kind != authority_kind:
                _fail(
                    "instruction_locator_authority_mismatch",
                    "instruction source locator must identify the exact source family that owns the authority claim",
                    (*path, "source_locator", "source_key"),
                )
        elif authority_kind == "derived_projection":
            state = authority["authority_state"]
            validation = authority["validation_state"]
            valid_derived_locator = (
                state == "candidate" and locator_kind == "awaiting_checkpoint_artifact"
            ) or (
                state == "execution_evidence"
                and locator_kind in _EXECUTION_EVIDENCE_SOURCE_KINDS
            )
            valid_legacy_locator = (
                state == "display_only"
                and validation == "unverified"
                and locator_kind in _LEGACY_SOURCE_KINDS
            )
            if not (valid_derived_locator or valid_legacy_locator):
                _fail(
                    "instruction_locator_authority_mismatch",
                    "derived instruction content must locate its governing awaiting, non-legacy execution, or unverified legacy evidence",
                    (*path, "source_locator", "source_key"),
                )

    target_count = len(instruction["target_refs"])
    if instruction["application_scope"] in {"single_target", "per_target_delta"}:
        if target_count != 1:
            _fail(
                "invalid_instruction_target_cardinality",
                f"{instruction['application_scope']} requires exactly one target",
                (*path, "target_refs"),
            )

    content = instruction["display_content"]
    authority = instruction["authority"]
    if content is None and authority["authority_state"] != "unavailable":
        _fail(
            "missing_instruction_claimed_available",
            "an unrecorded instruction must remain unavailable",
            (*path, "authority", "authority_state"),
        )
    if content is not None and authority["authority_state"] == "unavailable":
        _fail(
            "unavailable_instruction_has_content",
            "unavailable instruction content must not be projected",
            (*path, "display_content"),
        )
    if instruction["instruction_kind"] == "provider_input" and content is not None:
        if authority["evidence_scope"] not in {"provider_request", "provider_receipt"}:
            _fail(
                "fabricated_provider_input",
                "provider input content requires provider request or receipt evidence",
                (*path, "authority", "evidence_scope"),
            )


def _revision_signature(revision: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        revision["revision_ref"]["revision_kind"],
        revision["revision_ref"]["revision_id"],
        revision["revision_ref"]["sha256"],
    )


def _validate_course_design(
    course_design: Mapping[str, Any],
    resource: Mapping[str, Any],
    path: Sequence[str | int],
) -> None:
    """Keep the embedded Course declaration bound wherever the v1 wire permits it."""
    try:
        validate_artifact("course_manifest", dict(course_design))
    except Exception:
        _fail(
            "invalid_course_design",
            "course_design must pass the official Course manifest validator",
            path,
        )
    if (
        resource["kind"] != "course"
        or course_design["project_id"] != resource["project_id"]
    ):
        _fail(
            "course_design_project_mismatch",
            "course_design requires a Course ResourceRef with an exact project_id binding",
            (*path, "project_id"),
        )


def _validate_script_display(
    script: Mapping[str, Any],
    resource: Mapping[str, Any],
    revision: Mapping[str, Any] | None,
    snapshot: Mapping[str, Any],
    authority: Mapping[str, Any],
    path: Sequence[str | int],
) -> None:
    """Validate the original Script contract before accepting its closed display copy."""
    try:
        validate_artifact("script", dict(script))
    except Exception:
        _fail(
            "invalid_script_display",
            "script must pass the official Script validator",
            path,
        )
    if resource["kind"] != "stage" or resource["stage"] != resource["local_id"]:
        _fail(
            "script_resource_identity_mismatch",
            "script requires its manifest owner Stage ResourceRef",
            path,
        )
    if (
        revision is None
        or revision.get("revision_kind") != "checkpoint"
        or not isinstance(revision.get("stage"), str)
    ):
        _fail(
            "script_checkpoint_revision_required",
            "script requires an exact checkpoint Stage RevisionRef",
            path,
        )
    if revision.get("stage") != resource["stage"]:
        _fail(
            "script_revision_stage_mismatch",
            "script revision stage must match its Stage ResourceRef",
            path,
        )
    cited_evidence = {
        (evidence["source_key"], evidence["sha256"])
        for evidence in authority["evidence_refs"]
    }
    if not any(
        source.get("resource_ref") is not None
        and _identity_key(source["resource_ref"]) == _identity_key(resource)
        and source.get("revision_ref") == revision
        and source["sha256"] == revision["sha256"]
        and (source["source_key"], source["sha256"]) in cited_evidence
        for source in snapshot["sources"]
    ):
        _fail(
            "script_evidence_identity_mismatch",
            "script requires exact checkpoint evidence bound to its ResourceRef and RevisionRef",
            path,
        )


def _validate_style_display(
    style: Mapping[str, Any],
    resource: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    authority: Mapping[str, Any],
    path: Sequence[str | int],
) -> None:
    """Style is a project-scoped, multi-source read projection, never a raw catalog copy."""
    if resource["kind"] != "project" or resource["local_id"] != resource["project_id"]:
        _fail(
            "style_resource_identity_mismatch",
            "Style requires an exact project ResourceRef",
            path,
        )
    _validate_authority(
        style["proposal_authority"], snapshot, (*path, "proposal_authority")
    )
    availability = style["proposal"]["availability"]
    proposal_state = style["proposal_authority"]["authority_state"]
    if (
        (availability == "available" and proposal_state != "canonical")
        or (availability == "candidate" and proposal_state != "candidate")
        or (availability == "unavailable" and proposal_state != "unavailable")
    ):
        _fail(
            "style_proposal_lifecycle_mismatch",
            "proposal availability must match its field authority lifecycle",
            (*path, "proposal"),
        )
    if ("course_style_intent" in style) != ("course_authority" in style):
        _fail(
            "style_course_authority_pairing",
            "course Style intent and its authority must occur together",
            path,
        )
    if "course_authority" in style:
        _validate_authority(
            style["course_authority"], snapshot, (*path, "course_authority")
        )
    observations = style["observations"]
    for name, observation in observations.items():
        if observation["state"] == "present" and not isinstance(
            observation["value"], str
        ):
            _fail(
                "style_observation_value_invalid",
                "present Style observations require a string value",
                (*path, "observations", name),
            )
        if observation["state"] != "present" and observation["value"] is not None:
            _fail(
                "style_observation_value_invalid",
                "non-present Style observations require null values",
                (*path, "observations", name),
            )
    selection = observations["proposal_selection"]
    requires_selection = (
        style["proposal"]["availability"] in {"available", "candidate"}
        or style.get("resolved_style") is not None
    )
    if requires_selection and selection["state"] != "present":
        _fail(
            "style_proposal_selection_missing",
            "Style requires an exact selected proposal playbook",
            (*path, "observations", "proposal_selection"),
        )
    source_by_stage = {
        source.get("revision_ref", {}).get("stage"): source
        for source in snapshot["sources"]
        if source.get("revision_ref", {}).get("revision_kind") == "checkpoint"
    }
    for name in ("proposal_authority", "course_authority"):
        field_authority = style.get(name)
        if field_authority is None or field_authority["authority_state"] == "unavailable":
            continue
        source = source_by_stage.get(field_authority.get("source_stage"))
        cited = {
            (entry["source_key"], entry["sha256"])
            for entry in field_authority["evidence_refs"]
        }
        if source is None or (source["source_key"], source["sha256"]) not in cited:
            _fail(
                "style_field_authority_unbound",
                "Style proposal and course field authorities must cite their exact checkpoint source",
                (*path, name),
            )
    stages: set[str] = set()
    for index, observation in enumerate(style["checkpoint_observations"]):
        if observation["stage"] in stages:
            _fail(
                "duplicate_style_checkpoint_observation",
                "checkpoint style observation stages must be unique",
                (*path, "checkpoint_observations", index, "stage"),
            )
        stages.add(observation["stage"])
        _validate_authority(
            observation["authority"],
            snapshot,
            (*path, "checkpoint_observations", index, "authority"),
        )
        source = source_by_stage.get(observation["stage"])
        if observation["state"] == "present":
            if not isinstance(observation["value"], str) or source is None:
                _fail(
                    "style_checkpoint_observation_unbound",
                    "present checkpoint observations require their exact checkpoint source",
                    (*path, "checkpoint_observations", index),
                )
            cited = {
                (entry["source_key"], entry["sha256"])
                for entry in observation["authority"]["evidence_refs"]
            }
            if (source["source_key"], source["sha256"]) not in cited:
                _fail(
                    "style_checkpoint_observation_unbound",
                    "checkpoint observation authority must cite its stage source",
                    (*path, "checkpoint_observations", index, "authority"),
                )
        elif (
            observation["value"] is not None
            or observation["authority"]["authority_state"] != "unavailable"
        ):
            _fail(
                "style_checkpoint_observation_invalid",
                "invalid checkpoint observations require null values and unavailable authority",
                (*path, "checkpoint_observations", index),
            )
    resolved = style.get("resolved_style")
    if resolved is not None and not any(
        source["source_kind"] == "style_catalog_current"
        for source in snapshot["sources"]
    ):
        _fail(
            "style_catalog_evidence_missing",
            "resolved Style requires a bound current catalog source",
            path,
        )
    if resolved is None:
        return
    if style["proposal_authority"]["authority_state"] != "canonical":
        _fail(
            "style_resolved_without_canonical_proposal",
            "resolved Style requires canonical proposal field authority",
            (*path, "proposal_authority"),
        )
    if authority["authority_state"] != "canonical":
        _fail(
            "style_resolved_without_canonical_proposal",
            "resolved Style requires canonical proposal authority",
            path,
        )
    if resolved["playbook"] != selection["value"]:
        _fail(
            "style_resolved_selection_mismatch",
            "resolved playbook must equal the selected proposal key",
            (*path, "resolved_style", "playbook"),
        )
    present = [
        item["value"] for item in observations.values() if item["state"] == "present"
    ]
    present.extend(
        item["value"]
        for item in style["checkpoint_observations"]
        if item["state"] == "present"
    )
    if any(item["state"] == "invalid" for item in observations.values()) or any(
        item["state"] == "invalid" for item in style["checkpoint_observations"]
    ):
        _fail(
            "style_resolved_with_invalid_observation",
            "invalid Style evidence cannot resolve current Style",
            path,
        )
    if any(value != resolved["playbook"] for value in present):
        _fail(
            "style_resolved_observation_conflict",
            "every present Style observation must match resolved playbook",
            path,
        )
    cited = {
        (entry["source_key"], entry["sha256"]) for entry in authority["evidence_refs"]
    }
    for observation in style["checkpoint_observations"]:
        if observation["state"] == "present":
            source = source_by_stage[observation["stage"]]
            if (source["source_key"], source["sha256"]) not in cited:
                _fail(
                    "style_observation_evidence_missing",
                    "resolved Style must cite every present checkpoint observation",
                    path,
                )
    if observations["project_marker"]["state"] == "present" and not any(
        source["source_kind"] == "project_marker"
        and (source["source_key"], source["sha256"]) in cited
        for source in snapshot["sources"]
    ):
        _fail(
            "style_observation_evidence_missing",
            "resolved Style must cite a present marker observation",
            path,
        )
    if not any(
        source["source_kind"] == "style_catalog_current"
        and (source["source_key"], source["sha256"]) in cited
        for source in snapshot["sources"]
    ):
        _fail(
            "style_catalog_evidence_missing",
            "resolved Style authority must cite the current catalog",
            path,
        )
    if not any(
        source.get("revision_ref", {}).get("stage") == authority.get("source_stage")
        and source["source_kind"] == "approved_checkpoint_artifact"
        and (source["source_key"], source["sha256"]) in cited
        for source in snapshot["sources"]
    ):
        _fail(
            "style_proposal_evidence_missing",
            "resolved Style authority must cite approved proposal evidence",
            path,
        )


def _validate_revision_set(
    data: Mapping[str, Any],
    path: Sequence[str | int],
    outer_resource: Mapping[str, Any] | None = None,
) -> None:
    current = data["current_canonical"]
    candidates = data["pending_candidates"]
    history = data["historical_revisions"]
    revisions = [item for item in [current, *candidates, *history] if item is not None]

    if current is not None and current["authority"]["authority_state"] != "canonical":
        _fail(
            "noncanonical_current_revision",
            "current_canonical must carry canonical authority",
            (*path, "current_canonical", "authority", "authority_state"),
        )
    for index, candidate in enumerate(candidates):
        if candidate["authority"]["authority_state"] != "candidate":
            _fail(
                "noncandidate_pending_revision",
                "pending_candidates must carry candidate authority",
                (*path, "pending_candidates", index, "authority", "authority_state"),
            )
    for index, historical in enumerate(history):
        if historical["authority"]["authority_state"] != "display_only":
            _fail(
                "historical_revision_authority_escalation",
                "historical revisions must remain display_only",
                (*path, "historical_revisions", index, "authority", "authority_state"),
            )

    signatures: set[tuple[Any, ...]] = set()
    for index, revision in enumerate(revisions):
        _validate_revision_bound(
            revision["revision_ref"],
            revision["source_snapshot"],
            (*path, "revisions", index, "revision_ref"),
            projection_error="projected_revision_digest_mismatch",
            unbound_error="unbound_projected_revision",
            subject="projected revision",
        )
        signature = _revision_signature(revision)
        if signature in signatures:
            _fail(
                "duplicate_revision",
                "one revision cannot occupy multiple lifecycle slots",
                (*path, "revisions", index),
            )
        signatures.add(signature)
        if outer_resource is not None and _identity_key(
            revision["resource_ref"]
        ) != _identity_key(outer_resource):
            _fail(
                "mixed_revision_resource",
                "every revision-set member must describe the same logical resource",
                (*path, "revisions", index, "resource_ref"),
            )
        course_design = revision["data"].get("course_design")
        if course_design is not None:
            _validate_course_design(
                course_design,
                revision["resource_ref"],
                (*path, "revisions", index, "data", "course_design"),
            )
        script = revision["data"].get("script")
        if script is not None:
            _validate_script_display(
                script,
                revision["resource_ref"],
                revision["revision_ref"],
                revision["source_snapshot"],
                revision["authority"],
                (*path, "revisions", index, "data", "script"),
            )


def _validate_production_unit_summary(
    data: Mapping[str, Any],
    path: Sequence[str | int],
    snapshot: Mapping[str, Any] | None = None,
    resource: Mapping[str, Any] | None = None,
    authority: Mapping[str, Any] | None = None,
) -> None:
    policy = data["policy_mode"]
    disposition = data["execution_disposition"]
    progress_by_stage = data["progress_by_stage"]
    if policy == "off":
        if disposition is not None:
            _fail(
                "disabled_pup_has_disposition",
                "missing or off PUP policy has no execution disposition",
                (*path, "execution_disposition"),
            )
        if progress_by_stage:
            _fail(
                "disabled_pup_has_progress",
                "missing or off PUP policy cannot claim execution progress",
                (*path, "progress_by_stage"),
            )
        if data["candidate_handoff"] is not None:
            _fail(
                "disabled_pup_has_candidate_handoff",
                "missing or off PUP policy cannot claim a candidate handoff",
                (*path, "candidate_handoff"),
            )

    qualification = data["qualification_status"]
    identity = data["qualification_identity"]
    if qualification in _QUALIFIED_STATUSES and identity is None:
        _fail(
            "qualification_without_identity",
            f"{qualification} requires profile id, version, and digest",
            (*path, "qualification_identity"),
        )

    requires_evidence_context = (
        policy != "off"
        or disposition is not None
        or data["manifest_supported"] is not None
        or qualification in _QUALIFIED_STATUSES
        or bool(progress_by_stage)
        or data["candidate_handoff"] is not None
    )
    if snapshot is None and requires_evidence_context:
        _fail(
            "pup_evidence_context_required",
            "authority-bearing PUP data must be validated inside a Workspace projection",
            path,
        )

    if snapshot is not None:
        sources_by_kind: dict[str, list[Mapping[str, Any]]] = {}
        for source in snapshot["sources"]:
            sources_by_kind.setdefault(source["source_kind"], []).append(source)
        authority_evidence = (
            {
                (evidence["source_key"], evidence["sha256"])
                for evidence in authority["evidence_refs"]
            }
            if authority is not None
            else set()
        )

        def cited_by_authority(source: Mapping[str, Any]) -> bool:
            return (source["source_key"], source["sha256"]) in authority_evidence

        def bound_sources(source_kind: str) -> list[Mapping[str, Any]]:
            if resource is None:
                return []
            return [
                source
                for source in sources_by_kind.get(source_kind, [])
                if cited_by_authority(source)
                and source.get("resource_ref") is not None
                and _identity_key(source["resource_ref"]) == _identity_key(resource)
                and source.get("revision_ref") is not None
                and source["sha256"] == source["revision_ref"]["sha256"]
            ]

        policy_sources = [
            source
            for source in bound_sources("approved_checkpoint_artifact")
            if source["revision_ref"]["revision_kind"] == "checkpoint"
            and source["revision_ref"].get("stage") == "proposal"
        ]
        if policy != "off" and not policy_sources:
            _fail(
                "unbound_pup_policy",
                "enabled PUP policy requires an exact project-bound approved proposal checkpoint",
                (*path, "policy_mode"),
            )
        if data["manifest_supported"] is not None and not any(
            cited_by_authority(source)
            for source in sources_by_kind.get("pipeline_manifest", [])
        ):
            _fail(
                "unbound_pup_manifest_support",
                "manifest_supported requires actual validated pipeline-manifest bytes",
                (*path, "manifest_supported"),
            )
        if qualification in _QUALIFIED_STATUSES:
            profile_sources = bound_sources("production_unit_qualification_profile")
            has_profile = identity is not None and any(
                source["sha256"] == identity["profile_sha256"]
                and source["revision_ref"]["revision_kind"] == "content"
                and source["revision_ref"]["revision_id"]
                == f"{identity['profile_id']}:{identity['profile_version']}"
                for source in profile_sources
            )
            has_matrix = any(
                source["revision_ref"]["revision_kind"] == "content"
                for source in bound_sources("production_unit_capability_matrix")
            )
            if not has_profile or not has_matrix:
                _fail(
                    "unbound_pup_qualification",
                    "qualified status requires an exact validated profile/matrix pair in the source snapshot",
                    (*path, "qualification_identity"),
                )
        if disposition is not None:
            disposition_stage = authority.get("source_stage") if authority else None
            has_execution_contract = any(
                source["revision_ref"]["revision_kind"] == "content"
                and source["revision_ref"]["revision_id"]
                == f"execution-disposition:{disposition}"
                and disposition_stage is not None
                and source["revision_ref"].get("stage") == disposition_stage
                for source in bound_sources("production_unit_execution_contract")
            )
            if not policy_sources or not has_execution_contract:
                _fail(
                    "unbound_pup_execution_disposition",
                    "execution disposition requires exact project-bound policy and execution-contract evidence",
                    (*path, "execution_disposition"),
                )
        if progress_by_stage and not any(
            cited_by_authority(source)
            for source in sources_by_kind.get("checkpoint_partial_progress", [])
        ):
            _fail(
                "unbound_pup_progress",
                "PUP progress requires public checkpoint partial-progress evidence",
                (*path, "progress_by_stage"),
            )
        handoff = data["candidate_handoff"]
        if handoff is not None:
            if not any(
                cited_by_authority(source)
                for source in sources_by_kind.get("checkpoint_candidate_handoff", [])
            ):
                _fail(
                    "unbound_pup_candidate_handoff",
                    "candidate handoff requires official checkpoint handoff evidence",
                    (*path, "candidate_handoff"),
                )
            approved_digests = {source["sha256"] for source in policy_sources}
            if handoff["policy_checkpoint_sha256"] not in approved_digests:
                _fail(
                    "pup_handoff_policy_digest_mismatch",
                    "candidate handoff policy checkpoint must match the approved policy source",
                    (*path, "candidate_handoff", "policy_checkpoint_sha256"),
                )

    stages: set[str] = set()
    for index, progress in enumerate(progress_by_stage):
        progress_path = (*path, "progress_by_stage", index)
        if progress["stage"] in stages:
            _fail(
                "duplicate_pup_progress_stage",
                f"progress for stage {progress['stage']!r} occurs more than once",
                (*progress_path, "stage"),
            )
        stages.add(progress["stage"])
        terminal = (
            progress["completed_units"]
            + progress["failed_units"]
            + progress["stale_units"]
        )
        if terminal > progress["total_units"]:
            _fail(
                "pup_progress_exceeds_total",
                "completed, failed, and stale counts cannot exceed total units",
                progress_path,
            )
        if (
            progress["active_unit_id"] is not None
            and terminal >= progress["total_units"]
        ):
            _fail(
                "terminal_pup_has_active_unit",
                "fully terminal progress cannot also claim an active unit",
                (*progress_path, "active_unit_id"),
            )


def _validate_preview_timeline(
    data: Mapping[str, Any],
    path: Sequence[str | int],
    *,
    authority: Mapping[str, Any] | None = None,
    project_id: str | None = None,
    source_snapshot: Mapping[str, Any] | None = None,
) -> None:
    fidelity = data["fidelity"]
    snapshot_sources = source_snapshot["sources"] if source_snapshot is not None else []

    def source_binds(ref: Mapping[str, Any], *source_kinds: str) -> bool:
        return any(
            source.get("resource_ref") is not None
            and _identity_key(source["resource_ref"]) == _identity_key(ref)
            and source.get("revision_ref") is not None
            and source["sha256"] == source["revision_ref"]["sha256"]
            and (not source_kinds or source["source_kind"] in source_kinds)
            for source in snapshot_sources
        )

    def has_stage_source(stage: str, *source_kinds: str) -> bool:
        return any(
            source["source_kind"] in source_kinds
            and source.get("revision_ref", {}).get("stage") == stage
            for source in snapshot_sources
        )

    def has_asset_source() -> bool:
        return any(
            source["source_kind"] == "batch_v2_publication"
            or (
                source["source_kind"]
                in {"approved_checkpoint_artifact", "awaiting_checkpoint_artifact"}
                and source.get("revision_ref", {}).get("artifact_name")
                == "asset_manifest"
            )
            for source in snapshot_sources
        )

    if fidelity != "final_render" and data["final_render_ref"] is not None:
        _fail(
            "nonfinal_preview_claims_render",
            "only final_render fidelity may carry final_render_ref",
            (*path, "final_render_ref"),
        )
    if fidelity != "candidate_preview" and data["candidate_assignment_ref"] is not None:
        _fail(
            "noncandidate_preview_claims_assignment",
            "only candidate_preview may carry candidate_assignment_ref",
            (*path, "candidate_assignment_ref"),
        )
    if authority is not None:
        if fidelity == "final_render" and authority["authority_state"] != "canonical":
            _fail(
                "noncanonical_final_preview",
                "final_render preview requires canonical authority",
                (*path, "fidelity"),
            )
        if (
            fidelity == "final_render"
            and authority["source_kind"] != "render_report_output"
        ):
            _fail(
                "final_preview_without_render_report",
                "final_render preview requires completed render-report authority",
                (*path, "fidelity"),
            )
        if (
            fidelity == "candidate_preview"
            and authority["authority_state"] != "candidate"
        ):
            _fail(
                "noncandidate_candidate_preview",
                "candidate_preview requires candidate authority",
                (*path, "fidelity"),
            )
    if fidelity == "final_render" and data["unsupported_effects"]:
        _fail(
            "final_render_has_preview_limitations",
            "direct final-render playback cannot claim unsupported preview effects",
            (*path, "unsupported_effects"),
        )

    if project_id is not None:
        for field in ("final_render_ref", "candidate_assignment_ref"):
            ref = data[field]
            if ref is not None and ref["project_id"] != project_id:
                _fail(
                    "cross_project_preview_ref",
                    f"{field} must belong to the preview project",
                    (*path, field),
                )
        final_ref = data["final_render_ref"]
        if final_ref is not None and not source_binds(
            final_ref, "render_report_output"
        ):
            _fail(
                "unbound_final_render_ref",
                "final_render_ref must be bound by render-report source evidence",
                (*path, "final_render_ref"),
            )
        candidate_ref = data["candidate_assignment_ref"]
        if candidate_ref is not None and not source_binds(
            candidate_ref, "awaiting_checkpoint_artifact"
        ):
            _fail(
                "unbound_candidate_assignment_ref",
                "candidate_assignment_ref must be bound by awaiting checkpoint evidence",
                (*path, "candidate_assignment_ref"),
            )

    if source_snapshot is not None:
        if fidelity in {"planning_preview", "edit_preview"}:
            if not has_stage_source("scene_plan", "approved_checkpoint_artifact"):
                _fail(
                    f"{fidelity.removesuffix('_preview')}_preview_without_scene_plan",
                    f"{fidelity} requires validated scene-plan source evidence",
                    (*path, "fidelity"),
                )
            if not has_asset_source():
                _fail(
                    f"{fidelity.removesuffix('_preview')}_preview_without_assets",
                    f"{fidelity} requires validated asset-manifest evidence",
                    (*path, "fidelity"),
                )
        if fidelity == "edit_preview" and not has_stage_source(
            "edit", "approved_checkpoint_artifact"
        ):
            _fail(
                "edit_preview_without_edit_checkpoint",
                "edit preview requires validated edit source evidence",
                (*path, "fidelity"),
            )

    duration = data["duration_seconds"]
    segment_ids: set[str] = set()
    previous_start = -1.0
    for index, segment in enumerate(data["segments"]):
        segment_path = (*path, "segments", index)
        if segment["segment_id"] in segment_ids:
            _fail(
                "duplicate_preview_segment",
                f"segment_id {segment['segment_id']!r} occurs more than once",
                (*segment_path, "segment_id"),
            )
        segment_ids.add(segment["segment_id"])
        if segment["start_seconds"] >= segment["end_seconds"]:
            _fail(
                "invalid_preview_segment_range",
                "segment start must precede segment end",
                segment_path,
            )
        if segment["end_seconds"] > duration:
            _fail(
                "preview_segment_out_of_bounds",
                "segment end exceeds timeline duration",
                (*segment_path, "end_seconds"),
            )
        if segment["start_seconds"] < previous_start:
            _fail(
                "unordered_preview_segments",
                "segments must be ordered by start_seconds",
                (*segment_path, "start_seconds"),
            )
        previous_start = segment["start_seconds"]
        if segment["scene_ref"]["kind"] != "scene":
            _fail(
                "invalid_preview_scene_ref",
                "scene_ref must identify a scene",
                (*segment_path, "scene_ref", "kind"),
            )
        if segment["shot_ref"] is not None and segment["shot_ref"]["kind"] != "shot":
            _fail(
                "invalid_preview_shot_ref",
                "shot_ref must identify a shot",
                (*segment_path, "shot_ref", "kind"),
            )
        if project_id is not None:
            refs = [segment["scene_ref"]]
            if segment["shot_ref"] is not None:
                refs.append(segment["shot_ref"])
            if any(ref["project_id"] != project_id for ref in refs):
                _fail(
                    "cross_project_preview_segment",
                    "segment refs must belong to the preview project",
                    segment_path,
                )
            for field in ("scene_ref", "shot_ref"):
                ref = segment[field]
                if ref is not None and not source_binds(
                    ref,
                    "approved_checkpoint_artifact",
                    "awaiting_checkpoint_artifact",
                ):
                    _fail(
                        "unbound_preview_segment_ref",
                        f"{field} must be bound by scene-plan checkpoint evidence",
                        (*segment_path, field),
                    )
            media = segment["visual_media"]
            if media is not None and media["owner_ref"]["project_id"] != project_id:
                _fail(
                    "cross_project_preview_media",
                    "visual media must belong to the preview project",
                    (*segment_path, "visual_media", "owner_ref"),
                )
        if segment["availability"] == "available":
            media = segment["visual_media"]
            if media is None or media["availability"] != "browser_playable":
                _fail(
                    "fabricated_playable_segment",
                    "available segment requires browser-playable visual media",
                    (*segment_path, "visual_media"),
                )
        elif not segment["degraded_reasons"]:
            _fail(
                "unexplained_preview_degradation",
                "degraded or unavailable segments require an explicit reason",
                (*segment_path, "degraded_reasons"),
            )

    track_ids: set[str] = set()
    for index, track in enumerate(data["audio_tracks"]):
        track_path = (*path, "audio_tracks", index)
        if track["track_id"] in track_ids:
            _fail(
                "duplicate_preview_audio_track",
                f"track_id {track['track_id']!r} occurs more than once",
                (*track_path, "track_id"),
            )
        track_ids.add(track["track_id"])
        if track["start_seconds"] >= track["end_seconds"]:
            _fail(
                "invalid_preview_audio_range",
                "audio start must precede audio end",
                track_path,
            )
        if track["end_seconds"] > duration:
            _fail(
                "preview_audio_out_of_bounds",
                "audio end exceeds timeline duration",
                (*track_path, "end_seconds"),
            )
        if track["media_ref"]["media_kind"] != "audio":
            _fail(
                "non_audio_preview_track",
                "audio track must reference audio media",
                (*track_path, "media_ref", "media_kind"),
            )
        if (
            project_id is not None
            and track["media_ref"]["owner_ref"]["project_id"] != project_id
        ):
            _fail(
                "cross_project_preview_media",
                "audio media must belong to the preview project",
                (*track_path, "media_ref", "owner_ref"),
            )

    if source_snapshot is not None:
        timeline_sources = {
            json.dumps(
                source, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
            for source in source_snapshot["sources"]
        }
        nested_media = [
            segment["visual_media"]
            for segment in data["segments"]
            if segment["visual_media"] is not None
        ] + [track["media_ref"] for track in data["audio_tracks"]]
        for index, media in enumerate(nested_media):
            media_sources = {
                json.dumps(
                    source,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                for source in media["source_snapshot"]["sources"]
            }
            if not media_sources.issubset(timeline_sources):
                _fail(
                    "preview_media_source_not_in_timeline_snapshot",
                    "nested media evidence must be included in the timeline snapshot",
                    (*path, "nested_media", index, "source_snapshot"),
                )


def _walk(
    value: Any, path: tuple[str | int, ...] = ()
) -> Iterable[tuple[tuple[str | int, ...], Mapping[str, Any]]]:
    if isinstance(value, Mapping):
        yield path, value
        for key, child in value.items():
            yield from _walk(child, (*path, str(key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, (*path, index))


def _run_nested_semantics(value: Any) -> None:
    for path, node in _walk(value):
        keys = node.keys()
        if {"algorithm", "sources", "composite_sha256"} <= keys:
            _validate_source_snapshot(node, path)
        if {"authority", "source_snapshot"} <= keys:
            _validate_authority(
                node["authority"], node["source_snapshot"], (*path, "authority")
            )
        if {
            "project_id",
            "kind",
            "local_id",
            "resource_key",
            "parent_refs",
            "relation_refs",
        } <= keys:
            _validate_resource_ref(node, path)
        if {
            "relation_id",
            "relation_type",
            "source_refs",
            "target_refs",
            "authority",
            "source_snapshot",
        } <= keys:
            _validate_typed_relation(node, path)
        if {"diagnostics", "source_snapshot", "resource_ref"} <= keys:
            _validate_diagnostics(
                node["diagnostics"],
                node["source_snapshot"],
                node["resource_ref"]["project_id"],
                (*path, "diagnostics"),
            )
            if node.get("projection_kind") != "catalog":
                _validate_snapshot_project(
                    node["source_snapshot"],
                    node["resource_ref"]["project_id"],
                    (*path, "source_snapshot"),
                )
        if {"media_id", "owner_ref", "owner_revision", "media_kind", "purpose"} <= keys:
            _validate_media_ref(node, path)
        if {
            "instruction_id",
            "instruction_kind",
            "source_locator",
            "target_refs",
        } <= keys:
            _validate_generation_instruction(node, path)


def _validate_media_collection(
    data: Mapping[str, Any],
    path: Sequence[str | int],
    *,
    project_id: str | None = None,
    parent_snapshot: Mapping[str, Any] | None = None,
) -> None:
    media_ids: set[str] = set()
    media_by_id: dict[str, Mapping[str, Any]] = {}
    for index, media in enumerate(data["items"]):
        item_path = (*path, "items", index)
        if media["media_id"] in media_ids:
            _fail(
                "duplicate_media_id",
                f"media_id {media['media_id']!r} occurs more than once",
                (*item_path, "media_id"),
            )
        media_ids.add(media["media_id"])
        media_by_id[media["media_id"]] = media
        if parent_snapshot is not None:
            _validate_snapshot_covered(
                media["source_snapshot"],
                parent_snapshot,
                (*item_path, "source_snapshot"),
            )
        if project_id is not None and media["owner_ref"]["project_id"] != project_id:
            _fail(
                "cross_project_media_collection",
                "media owner belongs to a different project",
                (*item_path, "owner_ref"),
            )

    for index, media in enumerate(data["items"]):
        if media["purpose"] != "preview_proxy":
            continue
        item_path = (*path, "items", index)
        source_id = media["proxy_source_media_id"]
        source = media_by_id.get(source_id)
        if source is None:
            _fail(
                "dangling_preview_proxy_source",
                "preview proxy source must be colocated in the media collection",
                (*item_path, "proxy_source_media_id"),
            )
        if source["purpose"] == "preview_proxy":
            _fail(
                "chained_preview_proxy",
                "a preview proxy must point directly to a non-proxy representation",
                (*item_path, "proxy_source_media_id"),
            )
        if (
            _identity_key(media["owner_ref"]) != _identity_key(source["owner_ref"])
            or media["owner_revision"] != source["owner_revision"]
        ):
            _fail(
                "preview_proxy_owner_mismatch",
                "preview proxy and source must share one logical owner revision",
                (*item_path, "owner_ref"),
            )
        if (
            source["content_sha256"] is None
            or media["source_sha256"] != source["content_sha256"]
        ):
            _fail(
                "preview_proxy_digest_mismatch",
                "preview proxy source_sha256 must equal source content_sha256",
                (*item_path, "source_sha256"),
            )


def _validate_generation_instruction_collection(
    data: Mapping[str, Any],
    path: Sequence[str | int],
    *,
    project_id: str | None = None,
    parent_snapshot: Mapping[str, Any] | None = None,
) -> None:
    instruction_ids: set[str] = set()
    for index, instruction in enumerate(data["items"]):
        item_path = (*path, "items", index)
        if instruction["instruction_id"] in instruction_ids:
            _fail(
                "duplicate_instruction_id",
                f"instruction_id {instruction['instruction_id']!r} occurs more than once",
                (*item_path, "instruction_id"),
            )
        instruction_ids.add(instruction["instruction_id"])
        if parent_snapshot is not None:
            _validate_snapshot_covered(
                instruction["source_snapshot"],
                parent_snapshot,
                (*item_path, "source_snapshot"),
            )
        if (
            project_id is not None
            and instruction["resource_ref"]["project_id"] != project_id
        ):
            _fail(
                "cross_project_instruction_collection",
                "instruction belongs to a different project",
                (*item_path, "resource_ref"),
            )


def _validate_workspace_projection(projection: Mapping[str, Any]) -> None:
    resource = projection["resource_ref"]
    snapshot = projection["source_snapshot"]
    project_id = resource["project_id"]
    kind = projection["projection_kind"]
    revision = projection["revision_ref"]
    if revision is not None:
        _validate_revision_bound(
            revision,
            snapshot,
            ("revision_ref",),
            projection_error="projection_revision_digest_mismatch",
            unbound_error="unbound_projection_revision",
            subject="Workspace projection",
        )

    for index, source in enumerate(snapshot["sources"]):
        source_resource = source.get("resource_ref")
        if (
            kind != "catalog"
            and source_resource is not None
            and source_resource["project_id"] != project_id
        ):
            _fail(
                "cross_project_projection_source",
                "source resource belongs to a different project",
                ("source_snapshot", "sources", index, "resource_ref"),
            )

    _validate_diagnostics(
        projection["diagnostics"], snapshot, project_id, ("diagnostics",)
    )

    data = projection["data"]
    if kind == "resource_summary" and data.get("course_design") is not None:
        _validate_course_design(
            data["course_design"], resource, ("data", "course_design")
        )
    if kind == "resource_summary" and data.get("script") is not None:
        _validate_script_display(
            data["script"],
            resource,
            projection["revision_ref"],
            snapshot,
            projection["authority"],
            ("data", "script"),
        )
    if kind == "resource_summary" and data.get("style") is not None:
        _validate_style_display(
            data["style"],
            resource,
            snapshot,
            projection["authority"],
            ("data", "style"),
        )
    pagination = data.get("pagination")
    if pagination is not None and pagination["next_cursor"] is not None:
        if pagination["next_cursor"]["snapshot_sha256"] != snapshot["composite_sha256"]:
            _fail(
                "cursor_snapshot_mismatch",
                "pagination cursor must bind to the projection source snapshot",
                ("data", "pagination", "next_cursor", "snapshot_sha256"),
            )

    if kind == "catalog":
        if (
            resource["kind"] != "workspace_catalog"
            or resource["project_id"] != "backlot-workspace"
            or resource["local_id"] != "catalog"
            or resource["parent_refs"]
            or resource["relation_refs"]
        ):
            _fail(
                "invalid_workspace_catalog_scope",
                "catalog projections require the reserved backlot-workspace/catalog service scope",
                ("resource_ref",),
            )
        project_keys: set[str] = set()
        for index, item in enumerate(data["items"]):
            item_path = ("data", "items", index)
            project_ref = item["project_ref"]
            if project_ref["resource_key"] in project_keys:
                _fail(
                    "duplicate_catalog_project",
                    "catalog project resource_key occurs more than once",
                    (*item_path, "project_ref", "resource_key"),
                )
            project_keys.add(project_ref["resource_key"])
            _validate_snapshot_project(
                item["source_snapshot"],
                project_ref["project_id"],
                (*item_path, "source_snapshot"),
            )
            _validate_snapshot_covered(
                item["source_snapshot"],
                snapshot,
                (*item_path, "source_snapshot"),
            )
            _validate_diagnostics(
                item["diagnostics"],
                item["source_snapshot"],
                project_ref["project_id"],
                (*item_path, "diagnostics"),
            )
            revision = item["revision_ref"]
            if revision is not None:
                _validate_revision_bound(
                    revision,
                    item["source_snapshot"],
                    (*item_path, "revision_ref"),
                    projection_error="catalog_item_revision_digest_mismatch",
                    unbound_error="unbound_catalog_item_revision",
                    subject="catalog item",
                )
    elif kind == "revision_set":
        _validate_revision_set(data, ("data",), resource)
        nested_revisions = [
            item
            for item in [
                data["current_canonical"],
                *data["pending_candidates"],
                *data["historical_revisions"],
            ]
            if item is not None
        ]
        for index, revision in enumerate(nested_revisions):
            _validate_snapshot_covered(
                revision["source_snapshot"],
                snapshot,
                ("data", "revisions", index, "source_snapshot"),
            )
    elif kind == "media_collection":
        _validate_media_collection(
            data,
            ("data",),
            project_id=project_id,
            parent_snapshot=snapshot,
        )
    elif kind == "generation_instruction_collection":
        _validate_generation_instruction_collection(
            data,
            ("data",),
            project_id=project_id,
            parent_snapshot=snapshot,
        )
    elif kind == "production_unit_summary":
        _validate_production_unit_summary(
            data,
            ("data",),
            snapshot,
            resource,
            projection["authority"],
        )
    elif kind == "preview_timeline":
        if resource["kind"] != "preview_timeline":
            _fail(
                "invalid_preview_resource",
                "preview_timeline projection requires a preview_timeline ResourceRef",
                ("resource_ref", "kind"),
            )
        _validate_preview_timeline(
            data,
            ("data",),
            authority=projection["authority"],
            project_id=project_id,
            source_snapshot=snapshot,
        )

    for nested_path, node in _walk(projection):
        if nested_path == ("source_snapshot",):
            continue
        if {"algorithm", "sources", "composite_sha256"} <= node.keys():
            _validate_snapshot_covered(node, snapshot, nested_path)


def validate_workspace_contract(
    value: Any, definition: str = "workspace_projection"
) -> Any:
    """Validate and return an isolated Workspace v1 JSON-shaped value.

    Validation never normalizes or fills producer data.  Schema-invalid or
    semantically ambiguous values fail closed with :class:`WorkspaceContractError`.
    """

    candidate = deepcopy(value)
    _schema_validate(candidate, definition)
    _run_nested_semantics(candidate)

    if definition == "revision_set_data":
        _validate_revision_set(candidate, ())
    elif definition == "media_collection_data":
        _validate_media_collection(candidate, ())
    elif definition == "generation_instruction_collection_data":
        _validate_generation_instruction_collection(candidate, ())
    elif definition == "production_unit_summary_data":
        _validate_production_unit_summary(candidate, ())
    elif definition == "preview_timeline_data":
        _validate_preview_timeline(candidate, ())
    elif definition == "workspace_projection":
        _validate_workspace_projection(candidate)

    return deepcopy(candidate)


def validate_workspace_projection(
    value: Mapping[str, Any],
) -> WorkspaceProjection:
    """Validate one WorkspaceProjection and return a caller-owned copy."""

    return validate_workspace_contract(value, "workspace_projection")


__all__ = [
    "SOURCE_SNAPSHOT_ALGORITHM",
    "WORKSPACE_V1_DEFINITIONS",
    "WorkspaceContractError",
    "build_source_snapshot",
    "source_snapshot_digest",
    "validate_workspace_contract",
    "validate_workspace_projection",
    "workspace_contract_schema",
]
