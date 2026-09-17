# Backlot Workspace v1 Field／Source Authority Matrix

> **Contract version**: `backlot.workspace.field-source-matrix.v1`
> **Phase**: B0.1 consumer contract
> **Status**: integrated at `team-main @ 23b214a`; normative B0.1 consumer contract
> **Machine-readable source**: `docs/backlot-workspace-field-source-matrix.v1.json`
> **Wire schema**: `schemas/workspace/workspace_projection_v1.schema.json`
> **Runtime status**: no resolver, route, UI, preview engine, or mutation is authorized by this document

## 1. Purpose

This matrix fixes the source, owner, reader, validator, authority, lifecycle,
absence, and degradation meaning of each Workspace v1 field group before B0.2
implements any project reader or resolver. It exists to prevent a later Agent
from treating a useful-looking file, path, URL, checkpoint, cache, or private
sidecar as production truth.

The JSON companion is the complete machine-readable matrix. This Markdown file
is the human review surface. If they disagree, stop and repair both in the same
reviewed change; do not choose one in adapter or UI code.

This contract is subordinate to producer-owned schemas, validators, pipeline
manifests, director skills, and `lib/checkpoint.py`, and to
`docs/backlot-workspace-architecture-contract.md`. It does not create new
producer authority.

## 2. Frozen consumer vocabulary

Workspace v1 uses these authority states only:

- `canonical`
- `candidate`
- `execution_evidence`
- `display_only`
- `unavailable`

Validation is separately one of `validated|invalid|unverified`. Evidence depth
is separately one of `none|manifest_only|checkpoint_validated|publication_validated|provider_request|provider_receipt|binary_observed|human_reviewed`.
Each non-`none` scope requires at least one compatible cited SourceEntry: manifest
scope uses project／pipeline／style／legacy manifest-like sources; checkpoint
scope uses checkpoint-derived, PUP-contract, or render-report sources;
publication, provider request／receipt, binary observation, and human review
each require their matching source family. `none` requires an empty evidence
set and is reserved for `authority_state=unavailable + source_kind=unavailable`;
visible authority-bearing data always cites evidence. The JSON companion
freezes the complete compatibility table.

The exact `source_kind` tokens are:

```text
project_marker
pipeline_manifest
approved_checkpoint_artifact
awaiting_checkpoint_artifact
working_checkpoint_artifact
failed_checkpoint_artifact
checkpoint_partial_progress
checkpoint_candidate_handoff
production_unit_qualification_profile
production_unit_capability_matrix
production_unit_execution_contract
batch_v2_publication
style_catalog_current
legacy_loose_file
legacy_scan
render_report_output
provider_request
provider_receipt
binary_observation
human_review_record
derived_projection
unavailable
```

The PUP axes remain independent:

| Axis | Tokens／absence rule |
|---|---|
| Approved policy | `off|auto|fixed`; missing policy is exactly `off` |
| Execution disposition | `compare_only|publish_candidate|null`; `off` requires `null` |
| Manifest support | `true|false|null`; it describes implementation support only |
| Qualification | `unknown|unsupported|experimental|code_complete|beta_qualified|production_qualified|disabled|invalid` |
| Checkpoint lifecycle | `completed|awaiting_human|in_progress|failed|absent|null` |
| Human Gate | exact checkpoint fields; never inferred from the other axes |

`profile_id + profile_version + profile_sha256` is the qualification identity
when a trusted, exact profile/matrix pair is available. Missing trusted
resolution produces `qualification_status=unknown` and a null identity.

Media availability is `browser_playable|preview_proxy_required|unavailable`.
Preview fidelity is
`planning_preview|edit_preview|final_render|candidate_preview`; those values are
not authority states.

`workspace_catalog` is the reserved non-project service scope
`backlot-workspace/catalog`. Every catalog item retains its own project-scoped
source snapshot, authority, and diagnostics. Every non-null media metadata
bucket carries evidence refs bound to its MediaRef snapshot; human-reviewed
quality scores are allowed only as separately labeled review evidence.

`source_snapshot.algorithm=canonical-source-entries-v1` means: reject duplicate
source keys; sort complete source entries by `source_key`; encode the array as
UTF-8 JSON with object keys sorted and no insignificant whitespace; then SHA-256
the resulting bytes and prefix the lowercase hex digest with `sha256:`.
`source_kind` and optional ResourceRef／RevisionRef bindings are therefore part
of the token, so authority or identity metadata cannot co-drift behind an
unchanged ETag.

Nested source coverage compares the same complete source entries. Media owners
and every non-projection revision require exact identity plus revision binding,
not a coincidentally equal SHA. `derived_projection` cannot claim canonical
authority and must cite the awaiting or non-legacy producer／observation evidence
that supports a candidate or execution-evidence result. Preview proxies additionally bind their
source representation using `media-id:<source_media_id>` with the exact source
content digest, owner ResourceRef, and owner RevisionRef. Human review metadata
requires a separate `human_review_record` source.

## 3. Resolution order

Every artifact family follows the same fail-closed sequence:

1. Resolve the producer-declared owner stage from a validated pipeline
   manifest.
2. Read the checkpoint using the official `read_checkpoint` and
   `validate_checkpoint` path.
3. Keep completed, awaiting, in-progress, failed, invalid, missing, and history
   distinct.
4. Validate the artifact with its official schema and semantic validator and
   compute its canonical digest.
5. Compare loose cache bytes only for diagnostics.
6. Use an explicitly permitted legacy fallback only as
   `display_only + unverified` when no modern authoritative claim exists.
7. If an authoritative claim is invalid, fail closed; never recover authority
   from a loose file.
8. Never promote history to current canonical without a producer-owned
   active-canonical pointer.

The current checkpoint writer has no active-canonical pointer during an
awaiting rerun. In that state Workspace may show pending candidates and
history, but `revision_set.current_canonical` must be unavailable with
`not_identifiable_from_current_contract`.

## 4. Current Workspace reader boundary

B0.2A currently permits only these named producer reads:

- `CheckpointValidationError`, `read_checkpoint`, `read_project_marker`, and
  `validate_checkpoint` from `lib.checkpoint`;
- `load_pipeline_readonly` from `lib.pipeline_loader`;
- `inspect_v2_asset_manifest_claim` from
  `lib.batch_executor.publication`.

Several existing producer utilities appear in this matrix because they are the
correct prospective reader or validator, but they are not approved imports for
`backlot/workspace/readers`. Later B0.2/B1 work must add each narrow capability
and matching governance tests through the Architecture Contract change protocol.
Naming a utility here is not runtime authorization.

## 5. Field-group matrix

The table is a compact index. The JSON companion contains the full source,
absence, invalid/degraded, and forbidden-inference text for every row.

| Field group | Producer source and official validation | Authority／absence／degradation | Wire types | Implementation owner |
|---|---|---|---|---|
| Project identity | contained `project.json` through public `lib.checkpoint.read_project_marker` | Missing/invalid/mismatched marker is omitted from B0.2A catalog; directory or route name is not identity | `ResourceRef`, catalog, shell | B0.2 |
| Catalog project summary | authenticated project marker + selected manifest validated by `load_pipeline_readonly` | Reserved workspace service scope outside items; each item has its own project snapshot, authority, and diagnostics. B0.2A leaves classification unavailable because course/candidate evidence is deferred | catalog item, snapshot | B0.2A |
| Pipeline stage rail and gates | selected pipeline manifest; schema + `load_pipeline_readonly` | B0.2A admits the named read seam for catalog validation only. Shell/stage rail remains deferred; invalid/missing manifest fails closed with no fixed-tab fallback | `ShellData`, `StageSummary`, snapshot | B0.2 |
| Approved course | completed, human-approved proposal checkpoint containing valid `proposal_packet` + `course_manifest` and `content_form=course_form` | The only canonical course truth. Loose course file never creates authority | revision set, projected revision | B1 |
| Course candidate/history | validated proposal candidates and separately classified checkpoint history | Awaiting is candidate; working/failed are display snapshots; history is not current | revision set | B0.2/B1 |
| Script revisions | owner checkpoint + artifact schema | Completed/gated revision may be canonical; awaiting is candidate. Missing/invalid is unavailable. No unsupported semantic timing claims | revision set, resource/revision refs | B1 |
| Legacy script | contained loose script only under explicit legacy fallback | Always `display_only + unverified`; invalid authoritative evidence blocks fallback | projected revision | B0.2/B1 |
| Proposal style | selected proposal fields from validated proposal revision | Follows proposal lifecycle; suggested playbook is only a recommendation | projected revision, snapshot | B1 |
| Course style intent | exact `course_manifest.style_intent` | Follows course revision; remains distinct from playbook content | projected revision, snapshot | B1 |
| Project/checkpoint style identity | authenticated marker and validated checkpoint playbook names | Missing corroboration is not conflict. Real drift makes resolved style unavailable | projected revision, diagnostic | B0.2/B1 |
| Current style catalog | strict `styles.playbook_loader` result | Valid current content, but `historically_frozen=false` unless producer evidence binds exact old bytes | projected revision, snapshot | B0.2/B1 |
| Downstream style observation | validated `scene_plan.style_playbook` | Corroboration/drift evidence only; never overwrites proposal style | projected revision, diagnostic | B1 |
| CLP manifest | validated CLP owner checkpoint and semantic validator | Completed/gated or valid zero-entity completion is canonical; candidate/working/failed stay distinct | revision set, entity refs, media refs | B2 |
| Zero-entity CLP | exact verified `zero_entity_auto` gate resolution | Canonical CLP plus `verification_mode`; not a new authority state. Missing empty file is not success | projected revision, diagnostic | B2 |
| CLP shot bindings | validated scene-plan checkpoint bound to exact scene-plan and CLP digests | Exact typed relations only; missing/dangling/mismatched bindings are unavailable | `TypedRelation`, refs | B2 |
| Legacy CLP display | bounded legacy observations when no modern CLP claim exists | Always `display_only + unverified`; filenames never create strict-reference authority | projected revision, media refs | B2 |
| Ordinary checkpoint assets | validated owner checkpoint and `asset_manifest` | Lifecycle-aware manifest authority. Invalid claim blocks loose fallback | revision set, media refs, instructions | B0.2/B2 |
| Batch V2 assets | `inspect_v2_asset_manifest_claim` | Exact validated publication claim is canonical. Private Batch records are forbidden | projected revision, media refs | B0.2/B2 |
| Legacy assets | contained loose manifest only under explicit fallback | Always `display_only + unverified` | projected revision, media refs, instructions | B0.2/B2 |
| Local media | locator declared by exact owner and contained under project | Authority follows `asset|clp_entity|render_output` owner. Missing/unsafe bytes make the representation unavailable | `MediaRef` | B2 |
| Approved remote media | exact remote locator from same authoritative owner plus approved HTTPS policy | Remote reachability does not create authority. Unknown scheme/host/credentials fail closed | `MediaRef` | B2 |
| Preview proxy | disposable cache derived from exact source MediaRef | Derived representation only; stale digest invalidates it and it never creates canonical media | `MediaRef` | B2 |
| Missing/unreadable bytes | logical owner may remain valid while binary observation fails | `availability=unavailable`, `locator=null`; declared and observed metadata stay separate | `MediaRef`, diagnostic | B2 |
| Media metadata evidence | owning artifact, bounded probe, or explicit review evidence | Declared, observed, and human-reviewed buckets remain separate and each binds evidence refs; quality score is not approval | `MediaRef`, metadata, evidence ref | B2 |
| Creative specification and other declarative instruction kinds | exact mapped producer field, initially asset manifest prompt | Its locator must be an AuthorityDescriptor evidence entry exactly bound to the instruction owner/revision and use one of the v1 governing families: approved／awaiting checkpoint artifact, batch-v2 publication, or display-only legacy loose file; scope must respectively be checkpoint-validated, publication-validated, or manifest-only. General project／observation evidence cannot govern instruction text; missing text is never reconstructed | `GenerationInstruction` | B2 |
| Actual provider input | exact public provider request/receipt only | Request and receipt evidence/scopes are not interchangeable. Missing provider evidence is unavailable. One composite request does not become nine invented prompts | `GenerationInstruction` | producer contract/B2 |
| Render output | validated completed compose checkpoint + render report + unique producer output key | Identity is unique `platform_target` + report revision. Missing/duplicate key, unsafe path, or invalid report is unavailable | render-output ref, media ref | producer gap/B0.2/B2 |
| Delivery trace | digest-bound valid compose/publish checkpoint evidence | Evidence trace does not prove bytes, playback, or content quality; digest/path mismatch degrades only that trace | projected revision, diagnostic | B2 |
| Preview timeline | derived from validated scene plan, assets, optional edit, MediaRefs, and stable render output for final | Fidelity is explicit; edit preview requires scene-plan + asset-manifest + edit evidence. Source change stales it. Planning/edit/candidate never imply render parity or adoption | `PreviewTimelineData` | B2; B5 candidate mode |
| PUP approved policy | AuthorityDescriptor-cited, exact project-bound validated, human-approved proposal checkpoint policy (`revision_kind=checkpoint`, `stage=proposal`) | Missing equals `off`; no disposition. Wrong-stage evidence and legacy helper aliases are non-authoritative | PUP summary | B0.2 |
| PUP manifest support | actual selected manifest bytes | Separate from policy and qualification. Matrix `manifest_supported` is not a trusted manifest reader | PUP summary | B0.2 |
| PUP qualification | AuthorityDescriptor-cited, exact project-bound trusted profile/matrix pair with content revisions; profile revision ID is `profile_id:profile_version` | M6.0A validates supplied shape/bindings only. No trusted discovery means `unknown` | PUP summary, qualification identity | Track A then Track B |
| PUP disposition | AuthorityDescriptor-cited, exact project-bound public execution content revision identified as `execution-disposition:<value>` with revision stage equal to projection `source_stage` | Stage-internal intent, never publication; absent is null | PUP summary | Track A/B0.2 |
| PUP aggregate progress | validated checkpoint + current bounded consumer validation | `progress_by_stage[]`; execution evidence only. Invalid counts degrade progress without hiding a valid course | PUP summary/progress | B0.2; stronger schema Track A |
| PUP candidate handoff | official checkpoint validation including durable handoff validation | JSON provenance/execution evidence only. Absence is normal; tamper invalidates checkpoint | PUP summary/handoff provenance | B0.2 |
| PUP unit detail | no public source yet | Always unavailable with `b3_inspection_contract_unavailable`; no private fallback | PUP summary | Track A then B3 |
| Decisions | existing loose/root decision context | B0–B2 only `display_only + unverified`; canonical history/provenance normalization is deferred | projected revision, diagnostic | B6 |

## 6. Required no-inference behavior

The following are contract failures, not UI polish issues:

- using path, URL, array position, filename, title, time overlap, or “latest” as
  logical identity;
- treating JSON parse success as authority;
- making a candidate replace a canonical revision;
- promoting archived history to current canonical;
- showing loose or legacy data as validated/canonical;
- resolving a style conflict by similarity or fallback;
- equating `strict_reference` with human-selected or digest-locked media;
- turning asset-manifest order into selected take;
- reconstructing provider input from creative specification, scene text, CLP
  anchors, Style prefixes, or one composite-sheet request;
- treating preview/proxy availability as render, publication, selection, or
  adoption authority;
- collapsing PUP policy, manifest support, disposition, qualification,
  checkpoint, and Human Gate into one effective-state badge;
- deriving unit details, ownership crosswalk, attempt selection, epoch,
  recovery, or qualification from aggregate progress or M6.0B handoff
  provenance;
- reading `.production-units/**`, `.batch-v2/**`, coordinator state, attempts,
  receipts, or opaque `profile_ref` targets.

## 7. Known contract gaps carried into later phases

The matrix intentionally preserves these gaps instead of resolving them in
B0.1:

1. B0.2A closes the narrow public Workspace read seams for the authenticated
   project marker and selected pipeline manifest, with governance allowlist
   tests. The strict style catalog loader remains a later B0.2/B1 gap.
2. B0.2 must implement one lifecycle/source resolver for generic script,
   scene, asset, edit, render, loose-cache, and history cases.
3. The producer render schema does not require unique `platform_target` values.
   Workspace v1 therefore marks missing or duplicate output keys unavailable;
   it must not invent identity.
4. B2 owns local/remote/proxy/binary media resolution, GenerationInstruction
   rendering, and PreviewTimeline runtime behavior.
5. Actual provider input remains unavailable without a public exact
   request/receipt contract.
6. Track A still owns trusted qualification discovery/evidence authentication.
   M6.0A supplied-document validation is not that resolver.
7. Production Unit details stay blocked until a separately versioned,
   sanitized A→B inspection contract, validator, and fixtures are integrated.

These gaps do not block schema-valid B0.1 consumer fixtures. They do block any
claim that live B0.2/B1/B2/B3 behavior already exists.
