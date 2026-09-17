"""Static Python mirrors of the Backlot Workspace v1 wire contracts.

The JSON Schema bundle in :mod:`schemas.workspace` remains normative.  These
types exist only to make projection producers and consumers easier to review;
they grant no project-read or production authority.
"""

from __future__ import annotations

from typing import TypeAlias, Union

from typing_extensions import NotRequired, TypedDict
from typing import Literal


JSONScalar: TypeAlias = Union[None, bool, int, float, str]
JSONValue: TypeAlias = Union[
    JSONScalar,
    list["JSONValue"],
    dict[str, "JSONValue"],
]

ResourceKind: TypeAlias = Literal[
    "workspace_catalog",
    "project",
    "stage",
    "course",
    "module",
    "lesson",
    "script_section",
    "clp_entity",
    "continuity_group",
    "scene",
    "shot",
    "asset_slot",
    "asset",
    "render_output",
    "generation_instruction",
    "production_unit",
    "candidate_set",
    "candidate",
    "candidate_assignment",
    "preview_timeline",
]
AuthorityState: TypeAlias = Literal[
    "canonical",
    "candidate",
    "execution_evidence",
    "display_only",
    "unavailable",
]
ValidationState: TypeAlias = Literal["validated", "invalid", "unverified"]
SourceKind: TypeAlias = Literal[
    "project_marker",
    "pipeline_manifest",
    "approved_checkpoint_artifact",
    "awaiting_checkpoint_artifact",
    "working_checkpoint_artifact",
    "failed_checkpoint_artifact",
    "checkpoint_partial_progress",
    "checkpoint_candidate_handoff",
    "production_unit_qualification_profile",
    "production_unit_capability_matrix",
    "production_unit_execution_contract",
    "batch_v2_publication",
    "style_catalog_current",
    "legacy_loose_file",
    "legacy_scan",
    "render_report_output",
    "provider_request",
    "provider_receipt",
    "binary_observation",
    "human_review_record",
    "derived_projection",
    "unavailable",
]
EvidenceScope: TypeAlias = Literal[
    "none",
    "manifest_only",
    "checkpoint_validated",
    "publication_validated",
    "provider_request",
    "provider_receipt",
    "binary_observed",
    "human_reviewed",
]
ProjectionKind: TypeAlias = Literal[
    "catalog",
    "shell",
    "resource_summary",
    "revision_set",
    "media_collection",
    "generation_instruction_collection",
    "production_unit_summary",
    "preview_timeline",
]


class ResourceIdentity(TypedDict):
    project_id: str
    kind: ResourceKind
    local_id: str
    resource_key: str
    stage: NotRequired[str | None]


class RevisionRef(TypedDict):
    revision_kind: Literal[
        "checkpoint", "artifact", "content", "projection", "execution_epoch"
    ]
    revision_id: str
    sha256: str
    stage: NotRequired[str]
    artifact_name: NotRequired[str]
    execution_epoch: NotRequired[int]
    timestamp: NotRequired[str]


class EvidenceRef(TypedDict):
    source_key: str
    sha256: str


class AuthorityDescriptor(TypedDict):
    authority_state: AuthorityState
    validation_state: ValidationState
    source_kind: SourceKind
    evidence_scope: EvidenceScope
    evidence_refs: list[EvidenceRef]
    degraded_reasons: list[str]
    source_stage: NotRequired[str | None]
    checkpoint_status: NotRequired[
        Literal["completed", "awaiting_human", "in_progress", "failed", "absent"] | None
    ]
    human_approved: NotRequired[bool | None]
    historically_frozen: NotRequired[bool | None]


class SourceEntry(TypedDict):
    source_key: str
    source_kind: SourceKind
    sha256: str
    resource_ref: NotRequired[ResourceIdentity]
    revision_ref: NotRequired[RevisionRef]


class SourceSnapshot(TypedDict):
    algorithm: Literal["canonical-source-entries-v1"]
    sources: list[SourceEntry]
    composite_sha256: str


class TypedRelation(TypedDict):
    relation_id: str
    relation_type: Literal[
        "owns",
        "targets",
        "uses",
        "references",
        "covers",
        "derived_from",
        "creative_scope",
        "execution_scope",
        "assigned_to",
        "corroborates",
    ]
    source_refs: list[ResourceIdentity]
    target_refs: list[ResourceIdentity]
    authority: AuthorityDescriptor
    source_snapshot: SourceSnapshot


class ResourceRef(ResourceIdentity):
    parent_refs: list[ResourceIdentity]
    relation_refs: list[TypedRelation]


class MediaOwnerRef(TypedDict):
    project_id: str
    kind: Literal["asset", "clp_entity", "render_output"]
    local_id: str
    resource_key: str
    stage: NotRequired[str | None]
    parent_refs: list[ResourceIdentity]
    relation_refs: list[TypedRelation]


class GenerationInstructionResourceRef(TypedDict):
    project_id: str
    kind: Literal["generation_instruction"]
    local_id: str
    resource_key: str
    stage: NotRequired[str | None]
    parent_refs: list[ResourceIdentity]
    relation_refs: list[TypedRelation]


class ProjectResourceRef(TypedDict):
    project_id: str
    kind: Literal["project"]
    local_id: str
    resource_key: str
    stage: NotRequired[str | None]
    parent_refs: list[ResourceIdentity]
    relation_refs: list[TypedRelation]


class RenderOutputIdentity(TypedDict):
    project_id: str
    kind: Literal["render_output"]
    local_id: str
    resource_key: str
    stage: NotRequired[str | None]


class CandidateAssignmentIdentity(TypedDict):
    project_id: str
    kind: Literal["candidate_assignment"]
    local_id: str
    resource_key: str
    stage: NotRequired[str | None]


class CapabilityEntry(TypedDict):
    available: bool
    reason: str | None


CapabilityMap: TypeAlias = dict[str, CapabilityEntry]


class Diagnostic(TypedDict):
    code: str
    severity: Literal["info", "warning", "error"]
    message: str
    source_keys: list[str]
    resource_refs: list[ResourceIdentity]


class PaginationCursor(TypedDict):
    version: Literal["backlot.workspace.cursor.v1"]
    snapshot_sha256: str
    sort_key: str
    last_resource_key: str
    direction: Literal["forward"]


class Pagination(TypedDict):
    limit: int
    has_more: bool
    next_cursor: PaginationCursor | None


class MediaMetadata(TypedDict):
    evidence_kind: Literal["producer_declared", "tool_observed", "human_reviewed"]
    evidence_refs: list[EvidenceRef]
    sha256: NotRequired[str]
    mime_type: NotRequired[str]
    format: NotRequired[str]
    codec: NotRequired[str]
    width: NotRequired[int]
    height: NotRequired[int]
    duration_seconds: NotRequired[float]
    quality_score: NotRequired[float]
    observed_at: NotRequired[str]


class MediaLocator(TypedDict):
    kind: Literal["workspace_route", "approved_remote"]
    href: str


class MediaRef(TypedDict):
    media_id: str
    owner_ref: MediaOwnerRef
    owner_revision: RevisionRef
    media_kind: Literal["image", "audio", "video"]
    purpose: Literal["thumbnail", "detail", "original", "preview_proxy"]
    availability: Literal["browser_playable", "preview_proxy_required", "unavailable"]
    locator: MediaLocator | None
    unavailable_reason: str | None
    proxy_source_media_id: str | None
    content_sha256: str | None
    source_sha256: str | None
    declared_metadata: MediaMetadata | None
    observed_metadata: MediaMetadata | None
    review_metadata: MediaMetadata | None
    authority: AuthorityDescriptor
    source_snapshot: SourceSnapshot
    diagnostics: list[Diagnostic]


class InstructionSourceLocator(TypedDict):
    source_key: str
    field_pointer: str


class GenerationInstruction(TypedDict):
    instruction_id: str
    resource_ref: GenerationInstructionResourceRef
    creative_scope_ref: ResourceIdentity
    target_refs: list[ResourceIdentity]
    revision_ref: RevisionRef
    instruction_kind: Literal[
        "creative_specification",
        "provider_input",
        "negative_prompt",
        "narration_text",
        "delivery_contract",
        "music_intent",
        "sfx_intent",
        "search_query",
    ]
    application_scope: Literal[
        "single_target", "shared_scene", "per_target_delta", "composite_sheet"
    ]
    display_content: str | None
    source_locator: InstructionSourceLocator | None
    authority: AuthorityDescriptor
    source_snapshot: SourceSnapshot
    unavailable_reason: str | None


class CoursePromise(TypedDict):
    learner: str
    capability: str
    use_context: str
    success_evidence: str


class CourseObjective(TypedDict):
    id: str
    actor: str
    observable_verb: str
    object: str
    success_evidence: str
    source_refs: list[str]
    conditions: NotRequired[str]


class CourseTeachingBeat(TypedDict):
    kind: Literal[
        "activation",
        "hook",
        "explanation",
        "model",
        "worked_example",
        "demonstration",
        "practice",
        "recap",
        "assessment",
        "bridge",
    ]
    intent: str
    objective_ids: NotRequired[list[str]]


class CourseLesson(TypedDict):
    id: str
    title: str
    target_duration_seconds: float
    objective_ids: list[str]
    prerequisite_lesson_ids: list[str]
    prerequisite_objective_ids: list[str]
    expected_outcome: str
    source_refs: list[str]
    teaching_beats: list[CourseTeachingBeat]
    glossary_ids: list[str]
    notation_ids: list[str]
    export_required: bool


class CourseModule(TypedDict):
    id: str
    title: str
    intermediate_capability: str
    target_duration_seconds: float
    objective_ids: list[str]
    lessons: list[CourseLesson]
    recap_intent: str


class CourseAssessment(TypedDict):
    id: str
    type: Literal["diagnostic", "formative", "summative"]
    objective_ids: list[str]
    prompt_intent: str
    expected_evidence: str
    pass_criteria: str
    lesson_id: NotRequired[str]


class CourseSource(TypedDict):
    id: str
    uri: str
    title: NotRequired[str]
    locator: NotRequired[str]
    digest: NotRequired[str]


class CourseGlossaryEntry(TypedDict):
    id: str
    preferred_term: str
    definition: str
    aliases: list[str]
    forbidden_aliases: list[str]


class CourseNotationEntry(TypedDict):
    id: str
    symbol: str
    meaning: str
    first_lesson_id: NotRequired[str]
    units: NotRequired[str]


class CourseStyleIntent(TypedDict):
    tone: str
    visual_intent: str


class CourseDeliveryRequirements(TypedDict):
    full_master: bool
    lesson_export_ids: list[str]
    chapter_markers: bool
    captions: list[Literal["srt", "vtt", "burned_in"]]
    bundle: bool


class CourseDesign(TypedDict):
    version: Literal["1.0"]
    project_id: str
    content_form: Literal["course_form"]
    title: str
    target_duration_seconds: float
    course_promise: CoursePromise
    audience: list[str]
    entry_requirements: list[str]
    objectives: list[CourseObjective]
    modules: list[CourseModule]
    assessments: list[CourseAssessment]
    sources: list[CourseSource]
    glossary: list[CourseGlossaryEntry]
    notation: list[CourseNotationEntry]
    style_intent: CourseStyleIntent
    delivery_requirements: CourseDeliveryRequirements


class ResourceSummaryData(TypedDict):
    version: Literal["backlot.workspace.resource-summary.v1"]
    label: str
    availability: Literal["available", "display_only", "invalid", "unavailable"]
    description: NotRequired[str]
    course_design: NotRequired[CourseDesign]


class ProjectedRevision(TypedDict):
    resource_ref: ResourceRef
    revision_ref: RevisionRef
    source_snapshot: SourceSnapshot
    authority: AuthorityDescriptor
    capabilities: CapabilityMap
    diagnostics: list[Diagnostic]
    data: ResourceSummaryData


class RevisionSetData(TypedDict):
    version: Literal["backlot.workspace.revision-set.v1"]
    current_canonical: ProjectedRevision | None
    current_canonical_unavailable_reason: str | None
    pending_candidates: list[ProjectedRevision]
    historical_revisions: list[ProjectedRevision]


class CatalogItem(TypedDict):
    project_ref: ProjectResourceRef
    title: str
    classification: Literal[
        "ordinary",
        "approved_course",
        "awaiting_course_candidate",
        "legacy",
        "invalid",
        "unavailable",
    ]
    pipeline_type: str
    revision_ref: RevisionRef | None
    source_snapshot: SourceSnapshot
    authority: AuthorityDescriptor
    capabilities: CapabilityMap
    diagnostics: list[Diagnostic]


class CatalogData(TypedDict):
    version: Literal["backlot.workspace.catalog.v1"]
    items: list[CatalogItem]
    pagination: Pagination


class StageSummary(TypedDict):
    name: str
    status: Literal[
        "pending", "in_progress", "awaiting_human", "completed", "failed", "invalid"
    ]
    human_approval_default: bool


class ShellData(TypedDict):
    version: Literal["backlot.workspace.shell.v1"]
    pipeline_type: str
    classification: Literal[
        "ordinary",
        "approved_course",
        "awaiting_course_candidate",
        "legacy",
        "invalid",
        "unavailable",
    ]
    stages: list[StageSummary]
    current_stage: str | None
    gate_state: Literal[
        "none", "awaiting_human", "approved", "failed", "invalid", "unavailable"
    ]


class MediaCollectionData(TypedDict):
    version: Literal["backlot.workspace.media-collection.v1"]
    items: list[MediaRef]
    pagination: Pagination


class GenerationInstructionCollectionData(TypedDict):
    version: Literal["backlot.workspace.generation-instruction-collection.v1"]
    items: list[GenerationInstruction]
    pagination: Pagination


class QualificationIdentity(TypedDict):
    profile_id: str
    profile_version: str
    profile_sha256: str


class CandidateHandoffControlChain(TypedDict):
    chain_id: str
    event_sequence: int
    sha256: str


class CandidateHandoffProvenance(TypedDict):
    version: Literal["1.0"]
    authority: Literal["pup_json_merge"]
    handoff_id: str
    run_id: str
    execution_epoch: int
    control_chain: CandidateHandoffControlChain
    policy_checkpoint_sha256: str
    policy_sha256: str
    plan_record_sha256: str
    candidate_record_sha256: str
    candidate_sha256: str
    review_record_sha256: str
    validation_record_sha256: str
    checkpoint_intent_sha256: str


class ProductionUnitProgress(TypedDict):
    stage: str
    total_units: int
    completed_units: int
    failed_units: int
    stale_units: int
    active_unit_id: str | None
    boundary_defects: int
    repairs: int


class ProductionUnitSummaryData(TypedDict):
    version: Literal["backlot.workspace.production-unit-summary.v1"]
    policy_mode: Literal["off", "auto", "fixed"]
    execution_disposition: Literal["compare_only", "publish_candidate"] | None
    manifest_supported: bool | None
    qualification_status: Literal[
        "unknown",
        "unsupported",
        "experimental",
        "code_complete",
        "beta_qualified",
        "production_qualified",
        "disabled",
        "invalid",
    ]
    qualification_identity: QualificationIdentity | None
    progress_by_stage: list[ProductionUnitProgress]
    candidate_handoff: CandidateHandoffProvenance | None
    unit_details_available: Literal[False]
    unit_details_unavailable_reason: Literal["b3_inspection_contract_unavailable"]


class TimelineSegment(TypedDict):
    segment_id: str
    scene_ref: ResourceIdentity
    shot_ref: ResourceIdentity | None
    start_seconds: float
    end_seconds: float
    visual_media: MediaRef | None
    availability: Literal["available", "degraded", "unavailable"]
    degraded_reasons: list[str]


class AudioTrack(TypedDict):
    track_id: str
    kind: Literal["narration", "dialogue", "music", "sfx"]
    media_ref: MediaRef
    start_seconds: float
    end_seconds: float
    gain_db: float


class PreviewTimelineData(TypedDict):
    version: Literal["backlot.workspace.preview-timeline.v1"]
    fidelity: Literal[
        "planning_preview", "edit_preview", "final_render", "candidate_preview"
    ]
    duration_seconds: float
    segments: list[TimelineSegment]
    audio_tracks: list[AudioTrack]
    unsupported_effects: list[str]
    preload_ahead_segments: int
    final_render_ref: RenderOutputIdentity | None
    candidate_assignment_ref: CandidateAssignmentIdentity | None


WorkspaceData: TypeAlias = Union[
    CatalogData,
    ShellData,
    ResourceSummaryData,
    RevisionSetData,
    MediaCollectionData,
    GenerationInstructionCollectionData,
    ProductionUnitSummaryData,
    PreviewTimelineData,
]


class _WorkspaceProjectionBase(TypedDict):
    projection_version: Literal["backlot.workspace.v1"]
    resource_ref: ResourceRef
    revision_ref: RevisionRef | None
    source_snapshot: SourceSnapshot
    authority: AuthorityDescriptor
    capabilities: CapabilityMap
    diagnostics: list[Diagnostic]


class CatalogProjection(_WorkspaceProjectionBase):
    projection_kind: Literal["catalog"]
    data_schema: Literal["backlot.workspace.catalog.v1"]
    data: CatalogData


class ShellProjection(_WorkspaceProjectionBase):
    projection_kind: Literal["shell"]
    data_schema: Literal["backlot.workspace.shell.v1"]
    data: ShellData


class ResourceSummaryProjection(_WorkspaceProjectionBase):
    projection_kind: Literal["resource_summary"]
    data_schema: Literal["backlot.workspace.resource-summary.v1"]
    data: ResourceSummaryData


class RevisionSetProjection(_WorkspaceProjectionBase):
    projection_kind: Literal["revision_set"]
    data_schema: Literal["backlot.workspace.revision-set.v1"]
    data: RevisionSetData


class MediaCollectionProjection(_WorkspaceProjectionBase):
    projection_kind: Literal["media_collection"]
    data_schema: Literal["backlot.workspace.media-collection.v1"]
    data: MediaCollectionData


class GenerationInstructionCollectionProjection(_WorkspaceProjectionBase):
    projection_kind: Literal["generation_instruction_collection"]
    data_schema: Literal["backlot.workspace.generation-instruction-collection.v1"]
    data: GenerationInstructionCollectionData


class ProductionUnitSummaryProjection(_WorkspaceProjectionBase):
    projection_kind: Literal["production_unit_summary"]
    data_schema: Literal["backlot.workspace.production-unit-summary.v1"]
    data: ProductionUnitSummaryData


class PreviewTimelineProjection(_WorkspaceProjectionBase):
    projection_kind: Literal["preview_timeline"]
    data_schema: Literal["backlot.workspace.preview-timeline.v1"]
    data: PreviewTimelineData


WorkspaceProjection: TypeAlias = Union[
    CatalogProjection,
    ShellProjection,
    ResourceSummaryProjection,
    RevisionSetProjection,
    MediaCollectionProjection,
    GenerationInstructionCollectionProjection,
    ProductionUnitSummaryProjection,
    PreviewTimelineProjection,
]


__all__ = [
    "AudioTrack",
    "AuthorityDescriptor",
    "AuthorityState",
    "CandidateAssignmentIdentity",
    "CandidateHandoffProvenance",
    "CandidateHandoffControlChain",
    "CatalogData",
    "CatalogItem",
    "CatalogProjection",
    "CourseAssessment",
    "CourseDeliveryRequirements",
    "CourseDesign",
    "CourseGlossaryEntry",
    "CourseLesson",
    "CourseModule",
    "CourseNotationEntry",
    "CourseObjective",
    "CoursePromise",
    "CourseSource",
    "CourseStyleIntent",
    "CourseTeachingBeat",
    "CapabilityEntry",
    "CapabilityMap",
    "Diagnostic",
    "EvidenceRef",
    "EvidenceScope",
    "GenerationInstruction",
    "GenerationInstructionCollectionData",
    "GenerationInstructionCollectionProjection",
    "GenerationInstructionResourceRef",
    "InstructionSourceLocator",
    "JSONScalar",
    "JSONValue",
    "MediaCollectionData",
    "MediaCollectionProjection",
    "MediaLocator",
    "MediaMetadata",
    "MediaOwnerRef",
    "MediaRef",
    "Pagination",
    "PaginationCursor",
    "PreviewTimelineData",
    "PreviewTimelineProjection",
    "ProjectedRevision",
    "ProjectionKind",
    "QualificationIdentity",
    "ProductionUnitSummaryProjection",
    "ProductionUnitProgress",
    "ProductionUnitSummaryData",
    "ProjectResourceRef",
    "ResourceIdentity",
    "ResourceKind",
    "ResourceRef",
    "ResourceSummaryData",
    "ResourceSummaryProjection",
    "RevisionRef",
    "RevisionSetData",
    "RevisionSetProjection",
    "RenderOutputIdentity",
    "ShellProjection",
    "ShellData",
    "SourceEntry",
    "SourceKind",
    "SourceSnapshot",
    "StageSummary",
    "TimelineSegment",
    "TypedRelation",
    "ValidationState",
    "WorkspaceData",
    "WorkspaceProjection",
]
