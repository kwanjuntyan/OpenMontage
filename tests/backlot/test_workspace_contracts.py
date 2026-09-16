"""B0.1 versioned Workspace wire-contract and consumer-fixture gates."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import NotRequired, get_args, get_origin, get_type_hints

import jsonschema
import pytest

from backlot.workspace.projection import types as workspace_types
from backlot.workspace.projection.contracts import (
    WORKSPACE_V1_DEFINITIONS,
    WorkspaceContractError,
    build_source_snapshot,
    source_snapshot_digest,
    validate_workspace_contract,
    validate_workspace_projection,
    workspace_contract_schema,
)
from schemas.workspace import (
    load_workspace_v1_schema,
    validate_workspace_v1,
    workspace_v1_validator,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = REPO_ROOT / "tests" / "backlot" / "fixtures" / "workspace"
MATRIX_PATH = FIXTURE_ROOT / "fixture-matrix.v1.json"
AUTHORITY_MATRIX_PATH = (
    REPO_ROOT / "docs" / "backlot-workspace-field-source-matrix.v1.json"
)


def _load_json(path: Path) -> dict:
    def reject_duplicates(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key: {key}")
            value[key] = item
        return value

    return json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )


def _fixture_projections() -> list[tuple[Path, dict]]:
    return [
        (path, _load_json(path)) for path in sorted(FIXTURE_ROOT.glob("*/*.valid.json"))
    ]


def _snapshot_digest(sources: list[dict]) -> str:
    ordered = sorted(sources, key=lambda source: source["source_key"])
    encoded = json.dumps(
        ordered,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _refresh_snapshot(snapshot: dict) -> None:
    snapshot["sources"].sort(key=lambda source: source["source_key"])
    snapshot["composite_sha256"] = _snapshot_digest(snapshot["sources"])


def _refresh_projection_snapshot(projection: dict) -> None:
    _refresh_snapshot(projection["source_snapshot"])
    revision = projection["revision_ref"]
    if revision is not None and revision["revision_kind"] == "projection":
        revision["sha256"] = projection["source_snapshot"]["composite_sha256"]


def _sync_nested_source(projection: dict, child: dict, source_key: str) -> None:
    nested_source = next(
        source
        for source in child["source_snapshot"]["sources"]
        if source["source_key"] == source_key
    )
    outer_sources = projection["source_snapshot"]["sources"]
    outer_sources[:] = [
        source for source in outer_sources if source["source_key"] != source_key
    ]
    outer_sources.append(deepcopy(nested_source))
    _refresh_snapshot(child["source_snapshot"])
    _refresh_projection_snapshot(projection)


def _walk_values(value):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_values(child)


def _ordinary_shell() -> dict:
    return _load_json(FIXTURE_ROOT / "ordinary-project" / "ordinary-shell.valid.json")


def _media_collection() -> dict:
    return _load_json(
        FIXTURE_ROOT / "course-with-assets" / "mixed-media-authority.valid.json"
    )


def _generation_instructions() -> dict:
    return _load_json(
        FIXTURE_ROOT / "course-with-assets" / "generation-instructions.valid.json"
    )


def test_workspace_schema_bundle_is_draft_2020_12_closed_and_offline() -> None:
    schema = load_workspace_v1_schema()
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    jsonschema.Draft202012Validator.check_schema(schema)
    assert "workspace_projection" in schema["$defs"]
    assert "candidate_handoff_provenance" in schema["$defs"]

    stable_objects = {
        "resource_identity",
        "resource_ref",
        "revision_ref",
        "authority_descriptor",
        "source_entry",
        "source_snapshot",
        "typed_relation",
        "media_ref",
        "generation_instruction",
        "preview_timeline_data",
        "workspace_projection",
    }
    for name in stable_objects:
        assert schema["$defs"][name]["additionalProperties"] is False

    external_refs = [
        value["$ref"]
        for value in _walk_values(schema)
        if isinstance(value, dict)
        and "$ref" in value
        and not value["$ref"].startswith("#/")
    ]
    assert external_refs == []


def test_schema_and_typed_contracts_keep_executable_shape_and_enum_parity() -> None:
    schema = load_workspace_v1_schema()
    definitions = schema["$defs"]
    typed_objects = {
        "resource_identity": workspace_types.ResourceIdentity,
        "revision_ref": workspace_types.RevisionRef,
        "evidence_ref": workspace_types.EvidenceRef,
        "authority_descriptor": workspace_types.AuthorityDescriptor,
        "source_entry": workspace_types.SourceEntry,
        "source_snapshot": workspace_types.SourceSnapshot,
        "typed_relation": workspace_types.TypedRelation,
        "resource_ref": workspace_types.ResourceRef,
        "capability_entry": workspace_types.CapabilityEntry,
        "diagnostic": workspace_types.Diagnostic,
        "pagination_cursor": workspace_types.PaginationCursor,
        "pagination": workspace_types.Pagination,
        "media_metadata": workspace_types.MediaMetadata,
        "media_locator": workspace_types.MediaLocator,
        "media_ref": workspace_types.MediaRef,
        "instruction_source_locator": workspace_types.InstructionSourceLocator,
        "generation_instruction": workspace_types.GenerationInstruction,
        "resource_summary_data": workspace_types.ResourceSummaryData,
        "projected_revision": workspace_types.ProjectedRevision,
        "revision_set_data": workspace_types.RevisionSetData,
        "catalog_item": workspace_types.CatalogItem,
        "catalog_data": workspace_types.CatalogData,
        "stage_summary": workspace_types.StageSummary,
        "shell_data": workspace_types.ShellData,
        "media_collection_data": workspace_types.MediaCollectionData,
        "generation_instruction_collection_data": (
            workspace_types.GenerationInstructionCollectionData
        ),
        "qualification_identity": workspace_types.QualificationIdentity,
        "candidate_handoff_provenance": (workspace_types.CandidateHandoffProvenance),
        "production_unit_progress": workspace_types.ProductionUnitProgress,
        "production_unit_summary_data": workspace_types.ProductionUnitSummaryData,
        "timeline_segment": workspace_types.TimelineSegment,
        "audio_track": workspace_types.AudioTrack,
        "preview_timeline_data": workspace_types.PreviewTimelineData,
    }
    for definition, typed_contract in typed_objects.items():
        wire = definitions[definition]
        hints = get_type_hints(typed_contract, include_extras=True)
        required_keys = {
            key for key, hint in hints.items() if get_origin(hint) is not NotRequired
        }
        assert set(wire["required"]) == required_keys
        assert set(wire["properties"]) == set(hints)

    assert set(get_args(workspace_types.ResourceKind)) == set(
        definitions["resource_kind"]["enum"]
    )
    assert set(get_args(workspace_types.SourceKind)) == set(
        definitions["authority_descriptor"]["properties"]["source_kind"]["enum"]
    )
    assert set(get_args(workspace_types.ProjectionKind)) == set(
        definitions["workspace_projection"]["properties"]["projection_kind"]["enum"]
    )

    projection_types = {
        "catalog": workspace_types.CatalogProjection,
        "shell": workspace_types.ShellProjection,
        "resource_summary": workspace_types.ResourceSummaryProjection,
        "revision_set": workspace_types.RevisionSetProjection,
        "media_collection": workspace_types.MediaCollectionProjection,
        "generation_instruction_collection": (
            workspace_types.GenerationInstructionCollectionProjection
        ),
        "production_unit_summary": workspace_types.ProductionUnitSummaryProjection,
        "preview_timeline": workspace_types.PreviewTimelineProjection,
    }
    workspace_required = set(definitions["workspace_projection"]["required"])
    workspace_properties = set(definitions["workspace_projection"]["properties"])
    for projection_kind, typed_contract in projection_types.items():
        hints = get_type_hints(typed_contract, include_extras=True)
        required_keys = {
            key for key, hint in hints.items() if get_origin(hint) is not NotRequired
        }
        assert required_keys == workspace_required
        assert set(hints) == workspace_properties
        assert get_args(hints["projection_kind"]) == (projection_kind,)

    required_exports = {
        typed_contract.__name__ for typed_contract in typed_objects.values()
    } | {typed_contract.__name__ for typed_contract in projection_types.values()}
    required_exports |= {
        "CandidateAssignmentIdentity",
        "CandidateHandoffControlChain",
        "GenerationInstructionResourceRef",
        "MediaOwnerRef",
        "ProjectResourceRef",
        "RenderOutputIdentity",
        "WorkspaceData",
    }
    assert required_exports.issubset(set(workspace_types.__all__))

    media_hints = get_type_hints(workspace_types.MediaRef)
    assert media_hints["owner_ref"] is workspace_types.MediaOwnerRef
    assert set(get_args(get_type_hints(workspace_types.MediaOwnerRef)["kind"])) == {
        "asset",
        "clp_entity",
        "render_output",
    }
    instruction_hints = get_type_hints(workspace_types.GenerationInstruction)
    assert (
        instruction_hints["resource_ref"]
        is workspace_types.GenerationInstructionResourceRef
    )
    assert get_args(
        get_type_hints(workspace_types.GenerationInstructionResourceRef)["kind"]
    ) == ("generation_instruction",)
    catalog_hints = get_type_hints(workspace_types.CatalogItem)
    assert catalog_hints["project_ref"] is workspace_types.ProjectResourceRef
    assert get_args(get_type_hints(workspace_types.ProjectResourceRef)["kind"]) == (
        "project",
    )
    preview_hints = get_type_hints(workspace_types.PreviewTimelineData)
    assert workspace_types.RenderOutputIdentity in get_args(
        preview_hints["final_render_ref"]
    )
    assert workspace_types.CandidateAssignmentIdentity in get_args(
        preview_hints["candidate_assignment_ref"]
    )

    chain_wire = definitions["candidate_handoff_provenance"]["properties"][
        "control_chain"
    ]
    chain_hints = get_type_hints(workspace_types.CandidateHandoffControlChain)
    assert set(chain_wire["required"]) == set(chain_hints)
    assert set(chain_wire["properties"]) == set(chain_hints)


def test_schema_loader_returns_caller_owned_copy_and_rejects_unknown_definition() -> (
    None
):
    first = load_workspace_v1_schema()
    first["$defs"].clear()
    assert load_workspace_v1_schema()["$defs"]
    with pytest.raises(KeyError, match="unknown Workspace v1 definition"):
        workspace_v1_validator("not_a_contract")
    validate_workspace_v1("valid_identifier", definition="identifier")


def test_all_materialized_consumer_fixtures_validate_and_cover_matrix() -> None:
    matrix = _load_json(MATRIX_PATH)
    discovered = _fixture_projections()
    assert len(discovered) == 14

    covered_variants: set[str] = set()
    domain_expectations: set[str] = set()
    for scenario in matrix["scenarios"]:
        consumer = scenario["consumer_fixture"]
        if consumer["owner_phase"] == "B0.2":
            assert consumer["status"] == "pending"
            continue

        assert consumer["status"] == "materialized"
        manifest = _load_json(REPO_ROOT / consumer["manifest"])
        assert manifest["scenario_id"] == scenario["id"]
        scenario_coverage: set[str] = set()
        for case in manifest["cases"]:
            projection = _load_json(REPO_ROOT / consumer["path"] / case["projection"])
            validate_workspace_v1(projection)
            validate_workspace_projection(projection)
            covered_variants.update(case["covers"])
            scenario_coverage.update(case["covers"])
            domain_expectations.add(case["domain_expectation"])
        assert set(scenario["must_prove"]).issubset(scenario_coverage)

    assert set(matrix["required_variants"]).issubset(covered_variants)
    assert {"positive", "negative", "edge"}.issubset(domain_expectations)


def test_fixture_source_snapshots_are_sorted_unique_and_digest_bound() -> None:
    snapshots = []
    for _, projection in _fixture_projections():
        snapshots.extend(
            value
            for value in _walk_values(projection)
            if isinstance(value, dict)
            and value.get("algorithm") == "canonical-source-entries-v1"
        )

    assert snapshots
    for snapshot in snapshots:
        keys = [source["source_key"] for source in snapshot["sources"]]
        assert keys == sorted(keys)
        assert len(keys) == len(set(keys))
        assert snapshot["composite_sha256"] == _snapshot_digest(snapshot["sources"])
        assert snapshot["composite_sha256"] == source_snapshot_digest(
            snapshot["sources"]
        )


def test_public_contract_registry_is_explicit_complete_and_caller_owned() -> None:
    schema = load_workspace_v1_schema()
    assert WORKSPACE_V1_DEFINITIONS == frozenset(schema["$defs"])
    rooted = workspace_contract_schema("media_ref")
    assert rooted["$ref"] == "#/$defs/media_ref"
    rooted["$defs"].clear()
    assert workspace_contract_schema("media_ref")["$defs"]
    with pytest.raises(KeyError, match="not public"):
        workspace_contract_schema("future_unreviewed_contract")


def test_source_snapshot_builder_sorts_copies_and_binds_digest() -> None:
    sources = [
        {
            "source_key": "z:last",
            "source_kind": "pipeline_manifest",
            "sha256": f"sha256:{'2' * 64}",
        },
        {
            "source_key": "a:first",
            "source_kind": "project_marker",
            "sha256": f"sha256:{'1' * 64}",
        },
    ]
    snapshot = build_source_snapshot(sources)
    assert [source["source_key"] for source in snapshot["sources"]] == [
        "a:first",
        "z:last",
    ]
    sources[0]["source_key"] = "changed"
    snapshot["sources"][0]["source_key"] = "caller-change"
    assert (
        build_source_snapshot(
            [
                {
                    "source_key": "a:first",
                    "source_kind": "project_marker",
                    "sha256": f"sha256:{'1' * 64}",
                }
            ]
        )["sources"][0]["source_key"]
        == "a:first"
    )


def test_source_snapshot_digest_binds_kind_resource_and_revision_metadata() -> None:
    source = {
        "source_key": "artifact:script",
        "source_kind": "approved_checkpoint_artifact",
        "sha256": f"sha256:{'a' * 64}",
        "resource_ref": {
            "project_id": "digest-fixture",
            "kind": "stage",
            "stage": "script",
            "local_id": "script",
            "resource_key": "stage_script_01",
        },
        "revision_ref": {
            "revision_kind": "artifact",
            "revision_id": "script-approved-001",
            "sha256": f"sha256:{'a' * 64}",
            "stage": "script",
            "artifact_name": "script",
        },
    }
    baseline = source_snapshot_digest([source])

    for mutation in ("source_kind", "resource_ref", "revision_ref"):
        changed = deepcopy(source)
        if mutation == "source_kind":
            changed[mutation] = "legacy_loose_file"
        elif mutation == "resource_ref":
            changed[mutation]["local_id"] = "different-script"
        else:
            changed[mutation]["revision_id"] = "script-approved-002"
        assert source_snapshot_digest([changed]) != baseline

    unknown_field = deepcopy(source)
    unknown_field["unreviewed_metadata"] = "must not enter a projection token"
    with pytest.raises(WorkspaceContractError) as error:
        source_snapshot_digest([unknown_field])
    assert error.value.code == "schema_validation_failed"


@pytest.mark.parametrize(
    "evidence_scope",
    [
        "checkpoint_validated",
        "publication_validated",
        "provider_request",
        "provider_receipt",
        "binary_observed",
        "human_reviewed",
    ],
)
def test_evidence_scope_requires_compatible_cited_source(
    evidence_scope: str,
) -> None:
    projection = _ordinary_shell()
    projection["authority"]["evidence_scope"] = evidence_scope
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(projection)
    assert error.value.code == "unsupported_evidence_scope"

    none_with_evidence = _ordinary_shell()
    none_with_evidence["authority"]["evidence_scope"] = "none"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(none_with_evidence)
    assert error.value.code == "none_scope_with_evidence"

    visible_without_evidence = _ordinary_shell()
    visible_without_evidence["authority"].update(
        {
            "authority_state": "display_only",
            "validation_state": "unverified",
            "evidence_scope": "none",
            "evidence_refs": [],
        }
    )
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(visible_without_evidence)
    assert error.value.code == "none_scope_requires_unavailable"


def test_derived_authority_cannot_be_canonical_or_launder_legacy_evidence() -> None:
    canonical = _ordinary_shell()
    canonical["authority"]["source_kind"] = "derived_projection"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(canonical)
    assert error.value.code == "derived_canonical_authority"

    legacy_only = _ordinary_shell()
    legacy_only["authority"]["authority_state"] = "execution_evidence"
    legacy_only["authority"]["source_kind"] = "derived_projection"
    for source in legacy_only["source_snapshot"]["sources"]:
        source["source_kind"] = "legacy_loose_file"
    _refresh_projection_snapshot(legacy_only)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(legacy_only)
    assert error.value.code == "derived_execution_without_trusted_evidence"

    unrelated_trust = _ordinary_shell()
    legacy_source = next(
        source
        for source in unrelated_trust["source_snapshot"]["sources"]
        if source["source_kind"] == "pipeline_manifest"
    )
    legacy_source["source_kind"] = "legacy_loose_file"
    unrelated_source = {
        "source_key": "asset:unrelated-observation",
        "source_kind": "binary_observation",
        "sha256": f"sha256:{'e' * 64}",
        "resource_ref": {
            "project_id": "ordinary-project",
            "kind": "asset",
            "stage": None,
            "local_id": "unrelated-asset",
            "resource_key": "asset_unrelated_01",
        },
        "revision_ref": {
            "revision_kind": "content",
            "revision_id": "unrelated-observation-001",
            "sha256": f"sha256:{'e' * 64}",
        },
    }
    unrelated_trust["source_snapshot"]["sources"].append(unrelated_source)
    unrelated_trust["authority"].update(
        {
            "authority_state": "execution_evidence",
            "validation_state": "validated",
            "source_kind": "derived_projection",
            "evidence_scope": "binary_observed",
            "evidence_refs": [
                {
                    "source_key": legacy_source["source_key"],
                    "sha256": legacy_source["sha256"],
                },
                {
                    "source_key": unrelated_source["source_key"],
                    "sha256": unrelated_source["sha256"],
                },
            ],
        }
    )
    _refresh_projection_snapshot(unrelated_trust)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(unrelated_trust)
    assert error.value.code == "derived_unrelated_evidence"


def test_semantic_validator_rejects_snapshot_evidence_cursor_and_revision_drift() -> (
    None
):
    unsorted = _media_collection()
    unsorted["source_snapshot"]["sources"].reverse()
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(unsorted)
    assert error.value.code == "unsorted_source_snapshot"

    digest_drift = _ordinary_shell()
    digest_drift["source_snapshot"]["composite_sha256"] = f"sha256:{'0' * 64}"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(digest_drift)
    assert error.value.code == "source_snapshot_digest_mismatch"

    cursor_drift = _media_collection()
    cursor_drift["data"]["pagination"] = {
        "limit": 2,
        "has_more": True,
        "next_cursor": {
            "version": "backlot.workspace.cursor.v1",
            "snapshot_sha256": f"sha256:{'0' * 64}",
            "sort_key": "resource_key",
            "last_resource_key": "asset_scene01_frame_01",
            "direction": "forward",
        },
    }
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(cursor_drift)
    assert error.value.code == "cursor_snapshot_mismatch"

    mixed_identity = _load_json(
        FIXTURE_ROOT / "pending-candidate" / "awaiting-with-history.valid.json"
    )
    mixed_identity["data"]["historical_revisions"][0]["resource_ref"][
        "resource_key"
    ] = "different_resource_01"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(mixed_identity)
    assert error.value.code == "mixed_revision_resource"


def test_resource_ref_supports_explicit_many_to_many_relations() -> None:
    source = {
        "source_key": "candidate:scene-coverage-01",
        "source_kind": "awaiting_checkpoint_artifact",
        "sha256": f"sha256:{'d' * 64}",
    }
    source_snapshot = build_source_snapshot([source])

    def identity(kind: str, local_id: str, key: str) -> dict:
        return {
            "project_id": "relation-fixture",
            "kind": kind,
            "stage": None,
            "local_id": local_id,
            "resource_key": key,
        }

    relation = {
        "relation_id": "scene-coverage-01",
        "relation_type": "covers",
        "source_refs": [identity("candidate", "candidate-01", "candidate_0001")],
        "target_refs": [
            identity("shot", "shot-01", "shot_relation_01"),
            identity("shot", "shot-02", "shot_relation_02"),
        ],
        "authority": {
            "authority_state": "candidate",
            "validation_state": "validated",
            "source_kind": "derived_projection",
            "evidence_scope": "checkpoint_validated",
            "source_stage": None,
            "checkpoint_status": "awaiting_human",
            "human_approved": None,
            "historically_frozen": False,
            "evidence_refs": [
                {"source_key": source["source_key"], "sha256": source["sha256"]}
            ],
            "degraded_reasons": [],
        },
        "source_snapshot": source_snapshot,
    }
    validate_workspace_v1(relation, definition="typed_relation")
    validate_workspace_contract(relation, definition="typed_relation")


def test_nested_relation_evidence_must_be_covered_by_projection_snapshot() -> None:
    projection = _ordinary_shell()
    project_ref = {
        key: projection["resource_ref"][key]
        for key in ("project_id", "kind", "stage", "local_id", "resource_key")
    }
    target_ref = {
        "project_id": "ordinary-project",
        "kind": "stage",
        "stage": "script",
        "local_id": "script",
        "resource_key": "stage_script_ordinary_01",
    }
    source = {
        "source_key": "relation:project-script",
        "source_kind": "approved_checkpoint_artifact",
        "sha256": f"sha256:{'c' * 64}",
    }
    projection["resource_ref"]["relation_refs"] = [
        {
            "relation_id": "project-owns-script",
            "relation_type": "owns",
            "source_refs": [project_ref],
            "target_refs": [target_ref],
            "authority": {
                "authority_state": "execution_evidence",
                "validation_state": "validated",
                "source_kind": "derived_projection",
                "evidence_scope": "checkpoint_validated",
                "source_stage": "script",
                "checkpoint_status": "completed",
                "human_approved": None,
                "historically_frozen": False,
                "evidence_refs": [
                    {"source_key": source["source_key"], "sha256": source["sha256"]}
                ],
                "degraded_reasons": [],
            },
            "source_snapshot": build_source_snapshot([source]),
        }
    ]
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(projection)
    assert error.value.code == "nested_source_not_in_projection_snapshot"


def test_revision_set_keeps_candidate_and_history_without_promoting_history() -> None:
    projection = _load_json(
        FIXTURE_ROOT / "pending-candidate" / "awaiting-with-history.valid.json"
    )
    revisions = projection["data"]
    assert revisions["current_canonical"] is None
    assert revisions["current_canonical_unavailable_reason"] == (
        "not_identifiable_from_current_contract"
    )
    assert (
        revisions["pending_candidates"][0]["authority"]["authority_state"]
        == "candidate"
    )
    assert (
        revisions["historical_revisions"][0]["authority"]["authority_state"]
        == "display_only"
    )


def test_pup_axes_remain_distinct_and_b3_details_remain_unavailable() -> None:
    disabled = _load_json(
        FIXTURE_ROOT / "pup-disabled" / "approved-policy-off.valid.json"
    )["data"]
    enabled = _load_json(
        FIXTURE_ROOT / "pup-enabled" / "experimental-summary.valid.json"
    )["data"]
    assert disabled["policy_mode"] == "off"
    assert disabled["execution_disposition"] is None
    assert disabled["qualification_status"] == "unknown"
    assert enabled["policy_mode"] == "auto"
    assert enabled["execution_disposition"] is None
    assert enabled["manifest_supported"] is None
    assert enabled["qualification_status"] == "unknown"
    assert enabled["qualification_identity"] is None
    assert enabled["progress_by_stage"][0]["stage"] == "script"
    assert enabled["unit_details_available"] is False
    assert enabled["candidate_handoff"]["authority"] == "pup_json_merge"


def test_media_fixture_separates_authority_availability_metadata_and_lineage() -> None:
    items = {item["media_id"]: item for item in _media_collection()["data"]["items"]}
    assert (
        items["image-local-001"]["authority"]["source_kind"] == "batch_v2_publication"
    )
    assert items["audio-legacy-001"]["authority"]["authority_state"] == "display_only"
    assert items["audio-remote-001"]["locator"]["kind"] == "approved_remote"
    assert items["video-original-001"]["availability"] == "preview_proxy_required"
    assert items["video-proxy-001"]["proxy_source_media_id"] == "video-original-001"
    assert items["missing-image-001"]["locator"] is None
    assert items["missing-image-001"]["unavailable_reason"] == "media_bytes_missing"
    assert items["render-youtube-001"]["owner_ref"]["local_id"] == "youtube"


def test_provider_input_is_not_fabricated_from_creative_specification() -> None:
    instructions = {
        item["instruction_id"]: item
        for item in _generation_instructions()["data"]["items"]
    }
    creative = instructions["scene-01-shared-creative-spec"]
    provider = instructions["scene-01-provider-input-missing"]
    recorded = instructions["scene-01-provider-input-recorded"]
    assert creative["instruction_kind"] == "creative_specification"
    assert creative["display_content"]
    assert provider["instruction_kind"] == "provider_input"
    assert provider["display_content"] is None
    assert provider["source_locator"] is None
    assert provider["unavailable_reason"] == "provider_input_not_recorded"
    assert recorded["authority"]["evidence_scope"] == "provider_request"
    assert recorded["display_content"]


@pytest.mark.parametrize(
    "mutator",
    [
        lambda value: value["authority"].update(validation_state="unverified"),
        lambda value: value.update(data_schema="backlot.workspace.catalog.v1"),
        lambda value: value.update(unexpected=True),
    ],
)
def test_projection_schema_rejects_authority_version_and_shape_drift(mutator) -> None:
    projection = _ordinary_shell()
    mutator(projection)
    with pytest.raises(jsonschema.ValidationError):
        validate_workspace_v1(projection)


def test_schema_rejects_legacy_promotion_and_missing_production_unit_stage() -> None:
    legacy = _media_collection()["data"]["items"][1]
    promoted = deepcopy(legacy)
    promoted["authority"]["authority_state"] = "canonical"
    promoted["authority"]["validation_state"] = "validated"
    with pytest.raises(jsonschema.ValidationError):
        validate_workspace_v1(promoted, definition="media_ref")

    unit_ref = deepcopy(_ordinary_shell()["resource_ref"])
    unit_ref["kind"] = "production_unit"
    unit_ref.pop("stage")
    with pytest.raises(jsonschema.ValidationError):
        validate_workspace_v1(unit_ref, definition="resource_ref")


def test_schema_rejects_unsafe_media_and_metadata_evidence_drift() -> None:
    media = _media_collection()["data"]["items"][0]

    wrong_owner = deepcopy(media)
    wrong_owner["owner_ref"]["kind"] = "shot"
    with pytest.raises(jsonschema.ValidationError):
        validate_workspace_v1(wrong_owner, definition="media_ref")

    raw_path = deepcopy(media)
    raw_path["locator"]["href"] = "C:/project/output.png"
    with pytest.raises(jsonschema.ValidationError):
        validate_workspace_v1(raw_path, definition="media_ref")

    metadata_drift = deepcopy(media)
    metadata_drift["declared_metadata"]["evidence_kind"] = "human_reviewed"
    with pytest.raises(jsonschema.ValidationError):
        validate_workspace_v1(metadata_drift, definition="media_ref")

    assert media["review_metadata"]["quality_score"] == 4.5
    validate_workspace_v1(media, definition="media_ref")
    validate_workspace_contract(media, definition="media_ref")

    unsupported_human_score = deepcopy(media)
    unsupported_human_score["review_metadata"]["evidence_refs"] = [
        {
            "source_key": "assets:publication",
            "sha256": f"sha256:{'5' * 64}",
        }
    ]
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(unsupported_human_score, definition="media_ref")
    assert error.value.code == "invalid_human_review_source"

    missing_reason = deepcopy(
        next(
            item
            for item in _media_collection()["data"]["items"]
            if item["media_id"] == "missing-image-001"
        )
    )
    missing_reason["unavailable_reason"] = None
    with pytest.raises(jsonschema.ValidationError):
        validate_workspace_v1(missing_reason, definition="media_ref")


def test_schema_rejects_manifest_text_claimed_as_provider_input() -> None:
    provider = deepcopy(_generation_instructions()["data"]["items"][1])
    provider["display_content"] = (
        "Reconstructed text that the provider may never have received."
    )
    provider["source_locator"] = {
        "source_key": "assets:publication",
        "field_pointer": "/assets/0/generation_spec",
    }
    provider["unavailable_reason"] = None
    provider["authority"] = deepcopy(
        _generation_instructions()["data"]["items"][0]["authority"]
    )
    with pytest.raises(jsonschema.ValidationError):
        validate_workspace_v1(provider, definition="generation_instruction")


def test_generation_instruction_revision_requires_exact_source_binding() -> None:
    instruction = deepcopy(_generation_instructions()["data"]["items"][0])
    instruction["revision_ref"]["revision_id"] = "creative-spec-v2"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(instruction, definition="generation_instruction")
    assert error.value.code == "unbound_instruction_revision"


def test_generation_instruction_locator_must_be_authority_evidence() -> None:
    instruction = deepcopy(_generation_instructions()["data"]["items"][0])
    instruction["source_snapshot"]["sources"].append(
        {
            "source_key": "legacy:creative-copy",
            "source_kind": "legacy_loose_file",
            "sha256": f"sha256:{'f' * 64}",
        }
    )
    instruction["source_locator"] = {
        "source_key": "legacy:creative-copy",
        "field_pointer": "/prompt",
    }
    _refresh_snapshot(instruction["source_snapshot"])
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(instruction, definition="generation_instruction")
    assert error.value.code == "instruction_locator_not_authority_evidence"

    laundered = deepcopy(instruction)
    laundered["authority"]["evidence_refs"].append(
        {
            "source_key": "legacy:creative-copy",
            "sha256": f"sha256:{'f' * 64}",
        }
    )
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(laundered, definition="generation_instruction")
    assert error.value.code == "instruction_locator_not_owner_bound"

    same_family = deepcopy(_generation_instructions()["data"]["items"][0])
    same_family_source = {
        "source_key": "assets:unrelated-publication",
        "source_kind": "batch_v2_publication",
        "sha256": f"sha256:{'d' * 64}",
        "resource_ref": {
            "project_id": "course-assets",
            "kind": "asset",
            "stage": None,
            "local_id": "unrelated-asset",
            "resource_key": "asset_unrelated_02",
        },
        "revision_ref": {
            "revision_kind": "content",
            "revision_id": "unrelated-publication-v1",
            "sha256": f"sha256:{'d' * 64}",
        },
    }
    same_family["source_snapshot"]["sources"].append(same_family_source)
    same_family["source_snapshot"]["sources"].sort(key=lambda item: item["source_key"])
    same_family["authority"]["evidence_refs"].append(
        {
            "source_key": same_family_source["source_key"],
            "sha256": same_family_source["sha256"],
        }
    )
    same_family["source_locator"] = {
        "source_key": same_family_source["source_key"],
        "field_pointer": "/assets/999/prompt",
    }
    _refresh_snapshot(same_family["source_snapshot"])
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(same_family, definition="generation_instruction")
    assert error.value.code == "instruction_locator_not_owner_bound"

    derived = deepcopy(_generation_instructions()["data"]["items"][0])
    derived_source = {
        "source_key": "project:unrelated-marker",
        "source_kind": "project_marker",
        "sha256": f"sha256:{'b' * 64}",
        "resource_ref": {
            "project_id": "course-assets",
            "kind": "project",
            "stage": None,
            "local_id": "course-assets",
            "resource_key": "project_course_assets",
        },
        "revision_ref": {
            "revision_kind": "content",
            "revision_id": "unrelated-project-marker-v1",
            "sha256": f"sha256:{'b' * 64}",
        },
    }
    derived["source_snapshot"]["sources"].append(derived_source)
    derived["source_snapshot"]["sources"].sort(key=lambda item: item["source_key"])
    derived["authority"].update(
        {
            "source_kind": "derived_projection",
            "evidence_scope": "manifest_only",
            "evidence_refs": [
                {
                    "source_key": derived_source["source_key"],
                    "sha256": derived_source["sha256"],
                }
            ],
        }
    )
    derived["source_locator"] = {
        "source_key": derived_source["source_key"],
        "field_pointer": "/prompt",
    }
    _refresh_snapshot(derived["source_snapshot"])
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(derived, definition="generation_instruction")
    assert error.value.code == "instruction_locator_not_owner_bound"

    wrong_family = deepcopy(_generation_instructions()["data"]["items"][0])
    locator_key = wrong_family["source_locator"]["source_key"]
    locator_source = next(
        source
        for source in wrong_family["source_snapshot"]["sources"]
        if source["source_key"] == locator_key
    )
    locator_source["source_kind"] = "project_marker"
    wrong_family["authority"]["source_kind"] = "derived_projection"
    wrong_family["authority"]["evidence_scope"] = "manifest_only"
    _refresh_snapshot(wrong_family["source_snapshot"])
    wrong_family["authority"]["evidence_refs"][0]["sha256"] = locator_source[
        "sha256"
    ]
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(wrong_family, definition="generation_instruction")
    assert error.value.code == "instruction_locator_source_family_mismatch"

    scope_laundering = deepcopy(_generation_instructions()["data"]["items"][2])
    receipt_source = {
        "source_key": "provider:receipt:scene-01-shot-02",
        "source_kind": "provider_receipt",
        "sha256": f"sha256:{'a' * 64}",
    }
    scope_laundering["source_snapshot"]["sources"].append(receipt_source)
    scope_laundering["source_snapshot"]["sources"].sort(
        key=lambda item: item["source_key"]
    )
    scope_laundering["authority"]["evidence_refs"].append(
        {
            "source_key": receipt_source["source_key"],
            "sha256": receipt_source["sha256"],
        }
    )
    scope_laundering["authority"]["evidence_scope"] = "provider_receipt"
    _refresh_snapshot(scope_laundering["source_snapshot"])
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(
            scope_laundering, definition="generation_instruction"
        )
    assert error.value.code == "instruction_evidence_scope_mismatch"


def test_each_legacy_evidence_source_requires_exact_corroboration() -> None:
    projection = _ordinary_shell()
    bound_legacy = next(
        source
        for source in projection["source_snapshot"]["sources"]
        if source["source_kind"] == "pipeline_manifest"
    )
    bound_legacy["source_kind"] = "legacy_loose_file"
    bound_legacy["resource_ref"] = {
        "project_id": "ordinary-project",
        "kind": "project",
        "stage": None,
        "local_id": "ordinary-project",
        "resource_key": "project_ordinary_project",
    }
    trusted = deepcopy(bound_legacy)
    trusted.update(
        {
            "source_key": "manifest:trusted-observation",
            "source_kind": "binary_observation",
            "sha256": f"sha256:{'c' * 64}",
        }
    )
    unbound_legacy = {
        "source_key": "legacy:unbound-second-source",
        "source_kind": "legacy_loose_file",
        "sha256": f"sha256:{'d' * 64}",
    }
    projection["source_snapshot"]["sources"].extend([trusted, unbound_legacy])
    projection["source_snapshot"]["sources"].sort(key=lambda item: item["source_key"])
    projection["authority"].update(
        {
            "authority_state": "execution_evidence",
            "validation_state": "validated",
            "source_kind": "derived_projection",
            "evidence_scope": "manifest_only",
            "evidence_refs": [
                {
                    "source_key": bound_legacy["source_key"],
                    "sha256": bound_legacy["sha256"],
                },
                {
                    "source_key": trusted["source_key"],
                    "sha256": trusted["sha256"],
                },
                {
                    "source_key": unbound_legacy["source_key"],
                    "sha256": unbound_legacy["sha256"],
                },
            ],
        }
    )
    _refresh_projection_snapshot(projection)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(projection)
    assert error.value.code == "derived_unrelated_evidence"


def test_schema_rejects_candidate_preview_with_canonical_authority() -> None:
    projection = _load_json(
        FIXTURE_ROOT / "course-with-assets" / "completed-delivery.valid.json"
    )
    projection["data"]["fidelity"] = "candidate_preview"
    projection["data"]["final_render_ref"] = None
    projection["data"]["candidate_assignment_ref"] = {
        "project_id": "course-assets",
        "kind": "candidate_assignment",
        "stage": None,
        "local_id": "assignment-001",
        "resource_key": "assignment_0001",
    }
    with pytest.raises(jsonschema.ValidationError):
        validate_workspace_v1(projection)


def test_semantic_validator_rejects_execution_and_collection_identity_escalation() -> (
    None
):
    handoff_as_canonical = _ordinary_shell()
    handoff_as_canonical["authority"]["source_kind"] = "checkpoint_candidate_handoff"
    handoff_as_canonical["authority"]["evidence_scope"] = "checkpoint_validated"
    handoff_as_canonical["source_snapshot"]["sources"][0]["source_kind"] = (
        "checkpoint_candidate_handoff"
    )
    _refresh_projection_snapshot(handoff_as_canonical)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(handoff_as_canonical)
    assert error.value.code == "execution_evidence_authority_escalation"

    style_as_historical = _load_json(
        FIXTURE_ROOT / "course-with-style-and-clp" / "current-style.valid.json"
    )
    style_as_historical["authority"]["historically_frozen"] = True
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(style_as_historical)
    assert error.value.code == "current_style_claimed_historical"

    duplicate_media = _media_collection()
    second = deepcopy(duplicate_media["data"]["items"][0])
    second["purpose"] = "detail"
    duplicate_media["data"]["items"].append(second)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(duplicate_media)
    assert error.value.code == "duplicate_media_id"

    duplicate_media_data = deepcopy(_media_collection()["data"])
    duplicate_media_data["items"].append(deepcopy(duplicate_media_data["items"][0]))
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(
            duplicate_media_data,
            definition="media_collection_data",
        )
    assert error.value.code == "duplicate_media_id"

    duplicate_instruction_data = deepcopy(_generation_instructions()["data"])
    duplicate_instruction_data["items"].append(
        deepcopy(duplicate_instruction_data["items"][0])
    )
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(
            duplicate_instruction_data,
            definition="generation_instruction_collection_data",
        )
    assert error.value.code == "duplicate_instruction_id"

    self_proxy = _media_collection()
    proxy = next(
        item
        for item in self_proxy["data"]["items"]
        if item["media_id"] == "video-proxy-001"
    )
    proxy["proxy_source_media_id"] = proxy["media_id"]
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(self_proxy)
    assert error.value.code == "self_referential_preview_proxy"


def test_catalog_items_are_bound_and_catalog_scope_is_reserved() -> None:
    catalog = _load_json(FIXTURE_ROOT / "ordinary-project" / "catalog.valid.json")
    validate_workspace_projection(catalog)

    missing_item_snapshot = deepcopy(catalog)
    missing_item_snapshot["data"]["items"][0].pop("source_snapshot")
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(missing_item_snapshot)
    assert error.value.code == "schema_validation_failed"

    wrong_scope = deepcopy(catalog)
    wrong_scope["resource_ref"]["kind"] = "project"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(wrong_scope)
    assert error.value.code == "invalid_workspace_catalog_scope"


def test_revision_lifecycle_and_nested_projection_digests_fail_closed() -> None:
    projection = _load_json(
        FIXTURE_ROOT / "pending-candidate" / "awaiting-with-history.valid.json"
    )

    promoted_history = deepcopy(projection)
    promoted_history["data"]["historical_revisions"][0]["authority"][
        "authority_state"
    ] = "canonical"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(promoted_history)
    assert error.value.code == "historical_revision_authority_escalation"

    stale_nested_projection = deepcopy(projection)
    stale_nested_projection["data"]["pending_candidates"][0]["revision_ref"][
        "revision_kind"
    ] = "projection"
    stale_nested_projection["data"]["pending_candidates"][0]["revision_ref"][
        "sha256"
    ] = f"sha256:{'0' * 64}"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(stale_nested_projection)
    assert error.value.code == "projected_revision_digest_mismatch"

    nonprojection_top = _load_json(
        FIXTURE_ROOT / "course-with-assets" / "completed-delivery.valid.json"
    )
    nonprojection_top["revision_ref"]["revision_id"] = "render-report-002"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(nonprojection_top)
    assert error.value.code == "unbound_projection_revision"

    nonprojection_nested = deepcopy(projection)
    nonprojection_nested["data"]["pending_candidates"][0]["revision_ref"][
        "revision_id"
    ] = "script-awaiting-003"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(nonprojection_nested)
    assert error.value.code == "unbound_projected_revision"


def test_media_owner_metadata_remote_and_proxy_lineage_are_digest_bound() -> None:
    collection = _media_collection()
    items = {item["media_id"]: item for item in collection["data"]["items"]}

    unbound_owner = deepcopy(items["image-local-001"])
    unbound_owner["owner_revision"]["sha256"] = f"sha256:{'c' * 64}"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(unbound_owner, definition="media_ref")
    assert error.value.code == "unbound_media_owner_revision"

    identity_drift = deepcopy(items["image-local-001"])
    identity_drift["owner_revision"]["artifact_name"] = "different_manifest"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(identity_drift, definition="media_ref")
    assert error.value.code == "unbound_media_owner_revision"

    unbound_review = deepcopy(items["image-local-001"])
    unbound_review["review_metadata"] = {
        "evidence_kind": "human_reviewed",
        "evidence_refs": [
            {"source_key": "review:missing", "sha256": f"sha256:{'c' * 64}"}
        ],
        "quality_score": 4.5,
    }
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(unbound_review, definition="media_ref")
    assert error.value.code == "media_metadata_source_not_in_snapshot"

    remote_legacy = deepcopy(items["audio-legacy-001"])
    remote_legacy["locator"] = {
        "kind": "approved_remote",
        "href": "https://media.example.test/untrusted.mp3",
    }
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(remote_legacy, definition="media_ref")
    assert error.value.code == "unapproved_remote_media"

    derived_legacy = deepcopy(items["audio-legacy-001"])
    derived_legacy["authority"]["source_kind"] = "derived_projection"
    derived_legacy["authority"]["validation_state"] = "validated"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(derived_legacy, definition="media_ref")
    assert error.value.code == "derived_legacy_authority_escalation"

    unrelated_trust = deepcopy(items["audio-legacy-001"])
    unrelated_trust["authority"].update(
        {
            "authority_state": "execution_evidence",
            "validation_state": "validated",
            "source_kind": "derived_projection",
            "evidence_scope": "manifest_only",
        }
    )
    legacy_owner_source = next(
        source
        for source in unrelated_trust["source_snapshot"]["sources"]
        if source["source_key"] == "owner:audio-legacy-001"
    )
    unrelated_trust["source_snapshot"]["sources"].append(
        {
            "source_key": "project:unrelated-marker",
            "source_kind": "project_marker",
            "sha256": f"sha256:{'b' * 64}",
        }
    )
    unrelated_trust["authority"]["evidence_refs"] = [
        {
            "source_key": legacy_owner_source["source_key"],
            "sha256": legacy_owner_source["sha256"],
        },
        {
            "source_key": "project:unrelated-marker",
            "sha256": f"sha256:{'b' * 64}",
        },
    ]
    _refresh_snapshot(unrelated_trust["source_snapshot"])
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(unrelated_trust, definition="media_ref")
    assert error.value.code == "derived_unrelated_evidence"

    dangling = deepcopy(collection)
    dangling_proxy = next(
        item
        for item in dangling["data"]["items"]
        if item["media_id"] == "video-proxy-001"
    )
    dangling["data"]["items"] = [
        item
        for item in dangling["data"]["items"]
        if item["media_id"] != dangling_proxy["proxy_source_media_id"]
    ]
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(dangling)
    assert error.value.code == "dangling_preview_proxy_source"

    unbound_lineage = deepcopy(items["video-proxy-001"])
    unbound_lineage["proxy_source_media_id"] = "missing-original"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(unbound_lineage, definition="media_ref")
    assert error.value.code == "unbound_preview_proxy_source"

    bare_lineage = deepcopy(items["video-proxy-001"])
    lineage_source = next(
        source
        for source in bare_lineage["source_snapshot"]["sources"]
        if source["source_key"] == "media-id:video-original-001"
    )
    lineage_source.pop("resource_ref")
    lineage_source.pop("revision_ref")
    _refresh_snapshot(bare_lineage["source_snapshot"])
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(bare_lineage, definition="media_ref")
    assert error.value.code == "unbound_preview_proxy_source"

    digest_mismatch = deepcopy(collection)
    mismatched_proxy = next(
        item
        for item in digest_mismatch["data"]["items"]
        if item["media_id"] == "video-proxy-001"
    )
    mismatched_proxy["source_sha256"] = f"sha256:{'5' * 64}"
    lineage = next(
        source
        for source in mismatched_proxy["source_snapshot"]["sources"]
        if source["source_key"] == "media-id:video-original-001"
    )
    lineage["sha256"] = mismatched_proxy["source_sha256"]
    proxy_lineage_evidence = next(
        evidence
        for evidence in mismatched_proxy["authority"]["evidence_refs"]
        if evidence["source_key"] == "media-id:video-original-001"
    )
    proxy_lineage_evidence["sha256"] = mismatched_proxy["source_sha256"]
    _sync_nested_source(
        digest_mismatch,
        mismatched_proxy,
        "media-id:video-original-001",
    )
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(digest_mismatch)
    assert error.value.code == "preview_proxy_digest_mismatch"

    owner_mismatch = deepcopy(collection)
    mismatched_owner = next(
        item
        for item in owner_mismatch["data"]["items"]
        if item["media_id"] == "video-proxy-001"
    )
    mismatched_owner["owner_ref"]["local_id"] = "different-owner"
    mismatched_owner["owner_ref"]["resource_key"] = "asset_different_owner_01"
    owner_source = next(
        source
        for source in mismatched_owner["source_snapshot"]["sources"]
        if source["source_key"] == "owner:video-proxy-001"
    )
    owner_source["resource_ref"]["local_id"] = "different-owner"
    owner_source["resource_ref"]["resource_key"] = "asset_different_owner_01"
    owner_lineage = next(
        source
        for source in mismatched_owner["source_snapshot"]["sources"]
        if source["source_key"] == "media-id:video-original-001"
    )
    owner_lineage["resource_ref"]["local_id"] = "different-owner"
    owner_lineage["resource_ref"]["resource_key"] = "asset_different_owner_01"
    _sync_nested_source(
        owner_mismatch,
        mismatched_owner,
        "owner:video-proxy-001",
    )
    _sync_nested_source(
        owner_mismatch,
        mismatched_owner,
        "media-id:video-original-001",
    )
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(owner_mismatch)
    assert error.value.code == "preview_proxy_owner_mismatch"


def test_preview_nested_media_and_render_authority_are_bounded() -> None:
    planning = _load_json(
        FIXTURE_ROOT / "course-with-assets" / "planning-preview.valid.json"
    )
    cross_project = deepcopy(planning)
    cross_project["data"]["segments"][0]["visual_media"]["owner_ref"]["project_id"] = (
        "another-project"
    )
    cross_project_media = cross_project["data"]["segments"][0]["visual_media"]
    for source in cross_project_media["source_snapshot"]["sources"]:
        if source.get("resource_ref") is not None:
            source["resource_ref"]["project_id"] = "another-project"
    _refresh_snapshot(cross_project_media["source_snapshot"])
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(cross_project)
    assert error.value.code == "cross_project_preview_media"

    stale_timeline = deepcopy(planning)
    nested = stale_timeline["data"]["segments"][0]["visual_media"]["source_snapshot"]
    nested["sources"].append(
        {
            "source_key": "media:untracked",
            "source_kind": "binary_observation",
            "sha256": f"sha256:{'c' * 64}",
        }
    )
    _refresh_snapshot(nested)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(stale_timeline)
    assert error.value.code == "preview_media_source_not_in_timeline_snapshot"

    source_kind_drift = deepcopy(planning)
    nested = source_kind_drift["data"]["segments"][0]["visual_media"]
    owner_source = next(
        source
        for source in nested["source_snapshot"]["sources"]
        if source["source_key"] == "owner:planning-image-001"
    )
    owner_source["source_kind"] = "derived_projection"
    _refresh_snapshot(nested["source_snapshot"])
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(source_kind_drift)
    assert error.value.code == "preview_media_source_not_in_timeline_snapshot"

    proxy_timeline = deepcopy(planning)
    proxy = deepcopy(
        next(
            item
            for item in _media_collection()["data"]["items"]
            if item["media_id"] == "video-proxy-001"
        )
    )
    proxy_timeline["data"]["segments"][0]["visual_media"] = proxy
    for source in proxy["source_snapshot"]["sources"]:
        outer_sources = proxy_timeline["source_snapshot"]["sources"]
        outer_sources[:] = [
            existing
            for existing in outer_sources
            if existing["source_key"] != source["source_key"]
        ]
        outer_sources.append(deepcopy(source))
    _refresh_projection_snapshot(proxy_timeline)
    validate_workspace_projection(proxy_timeline)
    proxy_timeline["data"]["segments"][0]["visual_media"]["proxy_source_media_id"] = (
        "unbound-source"
    )
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(proxy_timeline)
    assert error.value.code == "unbound_preview_proxy_source"

    missing_scene_plan = deepcopy(planning)
    missing_scene_plan["source_snapshot"]["sources"] = [
        source
        for source in missing_scene_plan["source_snapshot"]["sources"]
        if not source["source_key"].startswith("scene-plan:")
    ]
    missing_scene_plan["authority"]["evidence_refs"] = [
        evidence
        for evidence in missing_scene_plan["authority"]["evidence_refs"]
        if not evidence["source_key"].startswith("scene-plan:")
    ]
    _refresh_projection_snapshot(missing_scene_plan)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(missing_scene_plan)
    assert error.value.code == "planning_preview_without_scene_plan"

    final_render = _load_json(
        FIXTURE_ROOT / "course-with-assets" / "completed-delivery.valid.json"
    )
    final_render["authority"]["checkpoint_status"] = "in_progress"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(final_render)
    assert error.value.code == "invalid_render_output_authority"

    final_identity_drift = _load_json(
        FIXTURE_ROOT / "course-with-assets" / "completed-delivery.valid.json"
    )
    final_identity_drift["data"]["final_render_ref"]["local_id"] = "vimeo"
    final_identity_drift["data"]["final_render_ref"]["resource_key"] = "render_vimeo_01"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(final_identity_drift)
    assert error.value.code == "unbound_final_render_ref"

    candidate_identity_drift = _load_json(
        FIXTURE_ROOT / "course-with-assets" / "candidate-preview.valid.json"
    )
    candidate_identity_drift["data"]["candidate_assignment_ref"]["local_id"] = (
        "assignment-002"
    )
    candidate_identity_drift["data"]["candidate_assignment_ref"]["resource_key"] = (
        "assignment_0002"
    )
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(candidate_identity_drift)
    assert error.value.code == "unbound_candidate_assignment_ref"


def test_edit_preview_requires_scene_plan_assets_and_edit_evidence() -> None:
    edit_preview = _load_json(
        FIXTURE_ROOT / "course-with-assets" / "edit-preview.valid.json"
    )
    validate_workspace_projection(edit_preview)
    assert edit_preview["data"]["segments"]
    assert edit_preview["data"]["segments"][0]["visual_media"] is not None
    assert edit_preview["data"]["audio_tracks"]
    source_kinds = {
        source["source_kind"] for source in edit_preview["source_snapshot"]["sources"]
    }
    assert "approved_checkpoint_artifact" in source_kinds
    assert "batch_v2_publication" in source_kinds

    missing_scene_plan = deepcopy(edit_preview)
    missing_scene_plan["source_snapshot"]["sources"] = [
        source
        for source in missing_scene_plan["source_snapshot"]["sources"]
        if source.get("revision_ref", {}).get("stage") != "scene_plan"
    ]
    missing_scene_plan["authority"]["evidence_refs"] = [
        evidence
        for evidence in missing_scene_plan["authority"]["evidence_refs"]
        if not evidence["source_key"].startswith("scene-plan:")
    ]
    _refresh_projection_snapshot(missing_scene_plan)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(missing_scene_plan)
    assert error.value.code == "edit_preview_without_scene_plan"

    missing_assets = deepcopy(edit_preview)
    missing_assets["source_snapshot"]["sources"] = [
        source
        for source in missing_assets["source_snapshot"]["sources"]
        if source["source_kind"] != "batch_v2_publication"
    ]
    missing_assets["authority"]["evidence_refs"] = [
        evidence
        for evidence in missing_assets["authority"]["evidence_refs"]
        if evidence["source_key"] != "assets:publication"
    ]
    missing_assets["authority"]["evidence_scope"] = "checkpoint_validated"
    _refresh_projection_snapshot(missing_assets)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(missing_assets)
    assert error.value.code == "edit_preview_without_assets"

    missing_edit = deepcopy(edit_preview)
    missing_edit["source_snapshot"]["sources"] = [
        source
        for source in missing_edit["source_snapshot"]["sources"]
        if source.get("revision_ref", {}).get("stage") != "edit"
    ]
    missing_edit["authority"]["evidence_refs"] = [
        evidence
        for evidence in missing_edit["authority"]["evidence_refs"]
        if evidence["source_key"] != "edit:checkpoint"
    ]
    missing_edit["revision_ref"] = None
    _refresh_projection_snapshot(missing_edit)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(missing_edit)
    assert error.value.code == "edit_preview_without_edit_checkpoint"


def test_pup_axes_require_their_exact_public_evidence() -> None:
    enabled = _load_json(
        FIXTURE_ROOT / "pup-enabled" / "experimental-summary.valid.json"
    )

    unbound_manifest = deepcopy(enabled)
    unbound_manifest["data"]["manifest_supported"] = True
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(unbound_manifest)
    assert error.value.code == "unbound_pup_manifest_support"

    unbound_disposition = deepcopy(enabled)
    unbound_disposition["data"]["execution_disposition"] = "compare_only"
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(unbound_disposition)
    assert error.value.code == "unbound_pup_execution_disposition"

    unbound_qualification = deepcopy(enabled)
    unbound_qualification["data"]["qualification_status"] = "experimental"
    unbound_qualification["data"]["qualification_identity"] = {
        "profile_id": "course-h264-1080p",
        "profile_version": "1.0.0",
        "profile_sha256": f"sha256:{'c' * 64}",
    }
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(unbound_qualification)
    assert error.value.code == "unbound_pup_qualification"

    uncited_policy = deepcopy(enabled)
    uncited_policy["authority"]["evidence_refs"] = [
        evidence
        for evidence in uncited_policy["authority"]["evidence_refs"]
        if evidence["source_key"] != "proposal:checkpoint"
    ]
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(uncited_policy)
    assert error.value.code == "unbound_pup_policy"

    unbound_handoff = deepcopy(enabled)
    source = next(
        source
        for source in unbound_handoff["source_snapshot"]["sources"]
        if source["source_key"] == "script:candidate-handoff"
    )
    source["source_kind"] = "checkpoint_partial_progress"
    _refresh_projection_snapshot(unbound_handoff)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(unbound_handoff)
    assert error.value.code == "unbound_pup_candidate_handoff"

    wrong_policy = deepcopy(enabled)
    wrong_policy["data"]["candidate_handoff"]["policy_checkpoint_sha256"] = (
        f"sha256:{'e' * 64}"
    )
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(wrong_policy)
    assert error.value.code == "pup_handoff_policy_digest_mismatch"

    wrong_policy_stage = deepcopy(enabled)
    policy_source = next(
        source
        for source in wrong_policy_stage["source_snapshot"]["sources"]
        if source["source_key"] == "proposal:checkpoint"
    )
    policy_source["revision_ref"]["stage"] = "edit"
    _refresh_projection_snapshot(wrong_policy_stage)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(wrong_policy_stage)
    assert error.value.code == "unbound_pup_policy"

    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_contract(
            enabled["data"],
            definition="production_unit_summary_data",
        )
    assert error.value.code == "pup_evidence_context_required"

    disabled_with_handoff = deepcopy(enabled)
    disabled_with_handoff["data"]["policy_mode"] = "off"
    disabled_with_handoff["data"]["progress_by_stage"] = []
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(disabled_with_handoff)
    assert error.value.code == "disabled_pup_has_candidate_handoff"

    magic_prefixes = deepcopy(enabled)
    magic_prefixes["data"]["qualification_status"] = "experimental"
    magic_prefixes["data"]["qualification_identity"] = {
        "profile_id": "course-h264-1080p",
        "profile_version": "1.0.0",
        "profile_sha256": f"sha256:{'c' * 64}",
    }
    magic_prefixes["source_snapshot"]["sources"].extend(
        [
            {
                "source_key": "pup:qualification-profile",
                "source_kind": "derived_projection",
                "sha256": f"sha256:{'c' * 64}",
            },
            {
                "source_key": "pup:capability-matrix",
                "source_kind": "derived_projection",
                "sha256": f"sha256:{'d' * 64}",
            },
        ]
    )
    _refresh_projection_snapshot(magic_prefixes)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(magic_prefixes)
    assert error.value.code == "unbound_pup_qualification"

    magic_disposition = deepcopy(enabled)
    magic_disposition["data"]["execution_disposition"] = "compare_only"
    magic_disposition["source_snapshot"]["sources"].append(
        {
            "source_key": "pup:execution-contract",
            "source_kind": "derived_projection",
            "sha256": f"sha256:{'e' * 64}",
        }
    )
    _refresh_projection_snapshot(magic_disposition)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(magic_disposition)
    assert error.value.code == "unbound_pup_execution_disposition"

    explicit_contracts = deepcopy(enabled)
    explicit_contracts["data"]["qualification_status"] = "experimental"
    explicit_contracts["data"]["qualification_identity"] = {
        "profile_id": "course-h264-1080p",
        "profile_version": "1.0.0",
        "profile_sha256": f"sha256:{'c' * 64}",
    }
    explicit_contracts["data"]["execution_disposition"] = "compare_only"
    project_identity = {
        key: explicit_contracts["resource_ref"][key]
        for key in ("project_id", "kind", "stage", "local_id", "resource_key")
    }
    explicit_contracts["source_snapshot"]["sources"].extend(
        [
            {
                "source_key": "qualification:profile",
                "source_kind": "production_unit_qualification_profile",
                "sha256": f"sha256:{'c' * 64}",
                "resource_ref": deepcopy(project_identity),
                "revision_ref": {
                    "revision_kind": "content",
                    "revision_id": "course-h264-1080p:1.0.0",
                    "sha256": f"sha256:{'c' * 64}",
                },
            },
            {
                "source_key": "qualification:matrix",
                "source_kind": "production_unit_capability_matrix",
                "sha256": f"sha256:{'d' * 64}",
                "resource_ref": deepcopy(project_identity),
                "revision_ref": {
                    "revision_kind": "content",
                    "revision_id": "capability-matrix:v1",
                    "sha256": f"sha256:{'d' * 64}",
                },
            },
            {
                "source_key": "execution:contract",
                "source_kind": "production_unit_execution_contract",
                "sha256": f"sha256:{'e' * 64}",
                "resource_ref": deepcopy(project_identity),
                "revision_ref": {
                    "revision_kind": "content",
                    "revision_id": "execution-disposition:compare_only",
                    "sha256": f"sha256:{'e' * 64}",
                    "stage": "script",
                },
            },
        ]
    )
    explicit_contracts["authority"]["evidence_refs"].extend(
        [
            {
                "source_key": "qualification:profile",
                "sha256": f"sha256:{'c' * 64}",
            },
            {
                "source_key": "qualification:matrix",
                "sha256": f"sha256:{'d' * 64}",
            },
            {
                "source_key": "execution:contract",
                "sha256": f"sha256:{'e' * 64}",
            },
        ]
    )
    _refresh_projection_snapshot(explicit_contracts)
    validate_workspace_projection(explicit_contracts)

    wrong_profile_revision = deepcopy(explicit_contracts)
    profile_source = next(
        source
        for source in wrong_profile_revision["source_snapshot"]["sources"]
        if source["source_key"] == "qualification:profile"
    )
    profile_source["revision_ref"]["revision_id"] = "other-profile:1.0.0"
    _refresh_projection_snapshot(wrong_profile_revision)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(wrong_profile_revision)
    assert error.value.code == "unbound_pup_qualification"

    uncited_profile = deepcopy(explicit_contracts)
    uncited_profile["authority"]["evidence_refs"] = [
        evidence
        for evidence in uncited_profile["authority"]["evidence_refs"]
        if evidence["source_key"] != "qualification:profile"
    ]
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(uncited_profile)
    assert error.value.code == "unbound_pup_qualification"

    wrong_disposition_stage = deepcopy(explicit_contracts)
    disposition_source = next(
        source
        for source in wrong_disposition_stage["source_snapshot"]["sources"]
        if source["source_key"] == "execution:contract"
    )
    disposition_source["revision_ref"]["stage"] = "edit"
    _refresh_projection_snapshot(wrong_disposition_stage)
    with pytest.raises(WorkspaceContractError) as error:
        validate_workspace_projection(wrong_disposition_stage)
    assert error.value.code == "unbound_pup_execution_disposition"


def test_authority_matrix_matches_frozen_schema_vocabulary_and_records_gaps() -> None:
    matrix = _load_json(AUTHORITY_MATRIX_PATH)
    schema = load_workspace_v1_schema()
    assert matrix["status"] == "b0.1_review_ready"
    assert (
        matrix["frozen_vocabulary"]["source_snapshot_algorithm"]["name"]
        == "canonical-source-entries-v1"
    )
    schema_kinds = set(
        schema["$defs"]["authority_descriptor"]["properties"]["source_kind"]["enum"]
    )
    assert set(matrix["frozen_vocabulary"]["source_kind"]) == schema_kinds
    resource_kinds = set(schema["$defs"]["resource_kind"]["enum"])
    assert set(matrix["frozen_vocabulary"]["resource_kind"]) == resource_kinds
    assert "workspace_catalog" in resource_kinds
    assert len(matrix["rows"]) >= 30
    assert any(
        row["official_reader_validator"]["resolution_status"].endswith("_gap")
        for row in matrix["rows"]
    )
    assert any(row["field_group"] == "pup.unit_details" for row in matrix["rows"])


def test_fixture_corpus_never_contains_private_sidecar_or_raw_local_path() -> None:
    forbidden = (".production-units", ".batch-v2", "file://", "c:/", "d:/", "\\\\")
    for path, projection in _fixture_projections():
        text = json.dumps(projection, ensure_ascii=False).casefold()
        assert not any(token.casefold() in text for token in forbidden), path
