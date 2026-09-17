# Backlot Director Workspace Architecture Contract

> **Contract version**: `backlot.workspace.architecture.v1`
> **B0.0 integration baseline**: `team-main @ 661827bee49c57f80b6a5c56b1378bccd7e039f8`; Track A consumer dependency remains pinned separately at `847cda02baa7a166da8f7a71976013765a5f71f2`
> **Status**: full B0.0 governance baseline and B0.1 contract are integrated; the B0.1 integration point is `team-main @ 23b214a`. This contract does not by itself authorize B0.2 product-code changes
> **Roadmap and rationale**: `docs/backlot-director-workspace-plan.md`

## 1. Purpose and precedence

This contract is the short, mandatory boundary for every Agent that designs, implements, reviews, or maintains Backlot／Director Workspace. The roadmap explains why and when; this file states what an implementation **MUST** and **MUST NOT** do.

If this contract conflicts with a current pipeline manifest, schema, official validator, director skill, or `lib/checkpoint.py`, stop and reconcile the documents before coding. A UI or projection implementation may not silently choose a winner.

`MUST`, `MUST NOT`, `SHOULD`, and `MAY` are normative terms. Changing a `MUST`／`MUST NOT` requires the change protocol in section 10.

## 2. Mandatory reading and work classification

Before changing `backlot/`, `backlot/ui/`, `tests/backlot/`, `/api/workspace/*`, or either Backlot architecture document, an Agent MUST read, in order:

1. `AGENT_GUIDE.md`;
2. this contract;
3. `docs/backlot-director-workspace-plan.md`;
4. `backlot/workspace/README.md` and `docs/backlot-workspace-field-source-matrix.v1.{md,json}` for B0.1-or-later work;
5. `schemas/workspace/workspace_projection_v1.schema.json`, `backlot/workspace/projection/{types,contracts}.py`, and `tests/backlot/fixtures/workspace/fixture-matrix.v1.json` for B0.1-or-later work;
6. the relevant current Backlot source and tests, including `tests/backlot/test_workspace_governance.py` and `tests/backlot/test_workspace_contracts.py`.

If the work touches course semantics, Production Units, checkpoints, qualification, or publication authority, the Agent MUST also read the owning skill, schema, validator, and handoff contract. In particular:

- course work: `skills/creative/course-form.md` and the course schemas／validators;
- PUP work: `skills/meta/production-unit-protocol.md`, `docs/production-unit-protocol-implementation-plan.md`, and the relevant execution schemas／validators;
- checkpoint authority: `lib/checkpoint.py` and its contract tests.

The Agent MUST identify the Track B phase, exact base SHA, files in scope, source-of-truth owner, and explicit non-goals before editing. An `OPEN` or `BLOCKED` roadmap item may not be decided implicitly in code.

## 3. Permanent system boundary

Backlot is a projection surface and future intent gateway. It is not a second production control plane.

```text
validated manifests / checkpoints / artifacts / public evidence
                              |
                    official readers + validators
                              |
                  versioned Workspace projections
                              |
                  Backlot / Director Workspace
                              |
             future versioned, digest-bound Agent intent
                              |
                 Agent + pipeline + review + gates
                              |
                    new canonical checkpoint
```

Backlot **MUST** remain observer-only with respect to production truth. Existing operational utilities such as explicit GCS sync do not grant artifact, checkpoint, approval, or publication authority and are outside the B0～B2 Workspace surface.

The tracked Workspace dependency seam **MUST** remain one-way:

```text
backlot/workspace/ui
        |
        v
backlot/workspace/api_v1
        |
        v
backlot/workspace/projection
        |
        v
backlot/workspace/readers
        |
        v
approved official OM readers and validators
```

- Browser code **MUST NOT** read project files, parse producer artifacts, call the legacy project-state API, or construct raw media paths. Workspace UI source remains under `backlot/workspace/ui`, outside the existing wholesale-mounted `backlot/ui` tree, until B0.2 registers the complete surface conditionally; with the default-off flag, UI assets and routes MUST return 404.
- The versioned API layer **MUST NOT** bypass the shared projection layer or decide source precedence／authority itself.
- Projection code **MUST** obtain canonical／legacy source observations through the Workspace reader seam; it **MUST NOT** import the API layer or raw source readers directly. Reader adapters **MUST NOT** import projection or API layers.
- Workspace code **MUST NOT** import provider execution, publisher mutation, approval transition, checkpoint／artifact writer, or producer-private PUP modules. Mixed reader／writer modules require an exact, named, independently reviewed read-only symbol allowlist; importing the whole module is forbidden.
- The Workspace package root **MUST** remain inert, and an unlisted top-level module／subpackage **MUST** fail closed. A new layer requires the section 10 change protocol and matching dependency tests in the same reviewed change.
- The executable boundary is `tests/backlot/test_workspace_governance.py`. Changing an allowlist or dependency direction is an architecture change subject to section 10, not a local test workaround.

## 4. Authority and source-resolution rules

### 4.1 Official readers only

- A canonical／candidate／published badge **MUST** come from an official reader and validator accepted for that artifact family.
- Each projected field group **MUST** identify its owner stage, reader／validator, source kind, lifecycle, absence semantics, and degraded behavior.
- Reading syntactically valid JSON directly does not establish authority.
- Invalid authoritative evidence **MUST** fail closed. It **MUST NOT** fall back to a loose file that looks usable.
- A permitted legacy fallback **MUST** be labeled `display_only + unverified`.
- Every non-`none` `evidence_scope` **MUST** be supported by a compatible source family cited in the same AuthorityDescriptor: manifest, checkpoint, publication, provider request／receipt, binary observation, and human review scopes are not interchangeable. `none` **MUST NOT** cite evidence and is reserved for `authority_state=unavailable + source_kind=unavailable`; every visible authority-bearing field must cite digest-bound evidence.

### 4.2 No private producer state

Workspace code **MUST NOT** scan or interpret producer-private state, including:

- `.production-units/**`;
- `.batch-v2/**` private attempts／receipts;
- coordinator `state.json` or receipt directories;
- opaque `profile_ref` targets;
- arbitrary filesystem paths or unapproved remote URLs.

Missing public contract means `unavailable`, not permission to infer a schema. The M6.0B checkpoint field `metadata.production_units.candidate_handoff`, after official checkpoint validation, is JSON handoff provenance only. It is not unit content, aggregate progress, Human approval, qualification, publication, adoption, or recovery authority.

Each non-empty PUP summary axis **MUST** be backed by an exact source entry also cited by the projection AuthorityDescriptor. Enabled policy requires a project-bound approved proposal checkpoint; qualification requires project-bound profile／matrix content revisions with exact profile identity; execution disposition requires a project-bound `execution-disposition:<value>` content revision whose stage equals the projection authority's source stage. `policy_mode=off` forbids disposition, progress, and candidate handoff.

### 4.3 Revision lifecycle

- Canonical, pending candidate, execution evidence, display-only data, invalid data, and history **MUST** remain distinct.
- An awaiting candidate **MUST NOT** overwrite the presentation of a producer-identified active canonical revision.
- Archived history **MUST NOT** be promoted to active canonical merely because it is the most recent completed entry.
- The current checkpoint writer has no active-canonical pointer during an awaiting rerun. Until a producer-owned pointer exists, `current_canonical` **MUST** be unavailable in that state; the pending candidate and history MAY still be shown.

### 4.4 Deterministic snapshots

Every projection and projected revision **MUST** carry a deterministic source set and composite digest. The complete canonical source entries—including `source_kind` and optional ResourceRef／RevisionRef bindings—form the projection token and ETag. Nested contracts **MUST** be covered by exact source entries in the outer projection; matching only `source_key + sha256` is insufficient. Pagination cursors, future intents, previews, and candidate assignments **MUST** bind to the source snapshot that produced them.

Every non-projection RevisionRef **MUST** occur as the exact `revision_ref` of a source entry whose digest matches it. A source used to establish an authority-bearing field **MUST** also be cited by that field group's AuthorityDescriptor or evidence bucket; merely existing elsewhere in the snapshot is insufficient. `derived_projection` may aggregate producer evidence but **MUST NOT** claim canonical authority; candidate derivations require awaiting-checkpoint evidence, and execution-evidence derivations require at least one explicitly bound non-legacy producer／observation source in their authority evidence. When legacy evidence participates in a validated or active derivation, **each** legacy evidence entry **MUST** have non-legacy corroboration sharing an exact ResourceRef or RevisionRef binding. Corroborating one legacy entry does not corroborate other legacy entries in the same evidence set. A derived entry or unrelated trusted source may not launder legacy-only evidence.

## 5. Versioned narrow-waist contracts

### 5.1 Workspace API

- New read APIs **MUST** use `/api/workspace/v1` and the versioned `WorkspaceProjection` envelope.
- Within one API version, only backward-compatible optional additions are allowed. Changing authority, identity, absence, or lifecycle semantics requires a new API／schema version.
- Known project + missing optional resource returns an `unavailable` projection with reason. Unknown project or invalid／unknown opaque resource key returns 404.
- Media bytes **MUST NOT** be embedded in projection JSON.

Every projection **MUST** expose, as applicable:

- `ResourceRef` and `RevisionRef`;
- `AuthorityDescriptor` and validation state;
- deterministic source snapshot／composite digest;
- explicit capabilities;
- diagnostics and degraded reasons;
- data whose schema matches the declared projection kind／version.

The relation model **MUST** support explicit one-to-many and many-to-many refs. It **MUST NOT** assume every resource has one parent or one target.

### 5.2 MediaRef

A `MediaRef` **MUST** be a typed, authority-aware representation bound to an owning logical ResourceRef／RevisionRef. The v1 owner model MUST support at least `asset`, `clp_entity`, and `render_output`; it MUST NOT coerce a CLP reference or render output into an asset merely to make it viewable. It MUST distinguish thumbnail, detail-quality, original, and preview-proxy purposes; record media kind, availability, safe route, digest／source digest where available, MIME／codec／dimensions／duration, and `browser_playable|preview_proxy_required|unavailable` capability.

`render_output` identity MUST come from a unique producer-declared output key, such as a validated unique `platform_target`, and its owning render-report revision. A path, array position, or “latest file” heuristic is not identity. If no stable unique output key exists, that final render is `unavailable` to Workspace v1 until a producer contract supplies one.

Producer-declared, tool-observed, and human-reviewed metadata **MUST** remain separately labeled and each non-empty bucket **MUST** bind its evidence refs to the owning MediaRef source snapshot. Human-reviewed values require explicit `human_review_record` evidence and never imply approval. The owning logical ResourceRef and exact RevisionRef **MUST** occur together in that snapshot; a shared SHA alone is insufficient. Filesystem paths and URLs are locators, not identity. A preview proxy is disposable server cache, not a canonical asset; its source MediaRef, owner revision, and source-content digest **MUST** be exact and non-dangling. Workspace v1 binds that source representation with a `media-id:<source_media_id>` binary-observation source entry whose digest equals the proxy `source_sha256` and whose ResourceRef／RevisionRef exactly match the proxy owner.

### 5.3 GenerationInstruction

A `GenerationInstruction` **MUST** have a stable ID derived from exact source identity, an owning／creative scope, explicit target refs, a revision／digest, kind, display-safe content, source locator, authority, evidence scope, and unavailable reason. Every non-projection RevisionRef **MUST** be represented exactly in its source snapshot; a source with only the same digest does not bind the instruction revision. A non-null source locator **MUST** select one of the source entries actually cited by the instruction's AuthorityDescriptor; that entry's ResourceRef and RevisionRef **MUST** exactly bind the instruction owner and revision, and its source family **MUST** govern the authority claim. Adding an unrelated same-family, derived, or legacy entry to the evidence list does not launder its content.

Workspace v1 provider-input locators accept only exact `provider_request` or `provider_receipt` evidence and their `evidence_scope` **MUST** match that governing locator family. Other v1 instruction kinds accept exact `approved_checkpoint_artifact`, `awaiting_checkpoint_artifact`, `batch_v2_publication`, or display-only `legacy_loose_file` evidence, with checkpoint, publication, or manifest-only scope respectively. Project markers, pipeline manifests, binary observations, review records, and other generally trusted execution families do not govern instruction content merely because they bind the same logical instruction identity.

Creative specification, shared scene instruction, tile／shot delta, negative prompt, and actual provider input **MUST** remain distinguishable. If a provider received one composite-sheet prompt, Backlot MUST NOT fabricate one provider prompt per tile. Missing provider input is `unavailable`; it MUST NOT be reconstructed from scene descriptions, CLP anchors, Style prefixes, or similar text.

### 5.4 PreviewTimelineProjection

The Preview Player **MUST** consume a versioned, read-only projection produced from validated scene plan, asset manifest, optional valid edit decisions, resolved MediaRefs, and—for `final_render`—a validated render report with stable output identity. Scene／shot refs, Candidate Assignment refs, and final render refs **MUST** be bound by exact ResourceRef-bearing source evidence from their owning lifecycle source. It MUST NOT join raw／loose files in the browser.

Fidelity MUST be explicit:

- `planning_preview`: plan-level approximation;
- `edit_preview`: supported cuts／audio／simple transitions from validated scene-plan, asset-manifest, and edit evidence;
- `final_render`: validated formal output;
- `candidate_preview` (B5): exact Candidate Assignment preview with `authority_state=candidate`, never canonical.

Planning, edit, and candidate previews are not render authority and MUST NOT claim final codec, complex runtime animation, subtitle burn-in, A/V sync, or delivery integrity. Each referenced media resource retains its own AuthorityDescriptor; a preview proxy is only a representation and does not introduce a compound authority state. Source changes MUST stale／invalidate the preview. Long-course playback MUST use bounded preload rather than loading the entire course.

### 5.5 Candidate Set and assignment boundary

Candidate Set persistence and mutation belong to B5, but B0 identity／relation contracts MUST remain forward-compatible with:

- `shot_variations` and scene-level `scene_coverage`;
- scene／continuity creative scope plus optional exact Production Unit execution scope;
- independent assets and composite-sheet-derived tiles with complete crop／digest lineage;
- append-only Candidate Assignment mapping one set to multiple shots／asset slots;
- a single candidate mapped to multiple targets when explicitly requested.

Candidate Set, preferred assignment, and canonical adoption are distinct states. Assignment targets MUST use producer-stable `shot`／`asset_slot` identity. If no such identity exists, Backlot MAY show unassigned scene-level coverage or submit a request for the Agent to create／revise shots; it MUST NOT invent a canonical shot from array order, time overlap, description, filename, or browser-local position.

## 6. Mutation and execution boundary

- B0～B3 Workspace endpoints **MUST** be GET／HEAD only with respect to production state.
- B4 and later **MUST** submit versioned, append-only, idempotent, digest-bound Agent intents; request state and canonical state MUST remain separate.
- Backlot **MUST NOT** call generation providers, select fallback providers, retry ambiguous charges, write canonical artifacts／checkpoints, decide Human Gates, or publish assets／renders.
- A preferred candidate **MUST NOT** become canonical until the Agent follows the existing director, review, cost-disclosure, Human Gate, validator, and checkpoint path.
- Multi-shot assignment intent MUST bind Candidate Set, scene／continuity, Style／CLP context, and every target revision. Any stale binding MUST reject the whole assignment; silent partial adoption is forbidden.

## 7. Compatibility, security, and rollback

- Workspace rollout **MUST** be additive and controlled by a server-side startup flag defaulting to `false`.
- With the flag off, Workspace UI／API return 404 and the existing Board, `/api/projects`, `/api/project/{id}/state`, SSE, media routes, CLI, and ordinary-project behavior remain unchanged.
- Workspace **MUST** support ordinary, non-course, PUP-off, PUP-on／experimental, missing-optional, invalid, and degraded projects without crashing or inventing authority.
- Project IDs, resource keys, cursors, source refs, and media locators are untrusted input and MUST pass containment／schema validation.
- Credentials, provider secrets, private reasoning, and arbitrary local paths MUST NOT be projected to the browser.
- Server-owned thumbnail／projection／preview-proxy cache MAY change during GET requests only when explicitly documented and tested. It MUST remain disposable and separate from canonical project files.
- Rollback MUST require only disabling the feature flag and discarding server cache; no canonical migration may be required.

## 8. Phase ownership

| Phase | Contract boundary |
|---|---|
| B0 | B0.0A document seal plus B0.0B enforcement scaffold; B0.1 versioned schemas and materialized positive／negative domain fixtures; B0.2 read resolver, versioned shell, compatibility and foundation performance evidence |
| B1 | Course, Script, and Style read-only projections |
| B2 | CLP, Scene Assets, GenerationInstruction, MediaRef, lightbox／players, PreviewTimeline |
| B3 | Production Unit detail only after a separate versioned A→B inspection contract |
| B4 | general Agent Intent transport and acknowledgement; no provider execution in Backlot |
| B5 | Candidate Set, Candidate Assignment, 3×3 presentation, multi-shot first-frame assignment, adoption workflow |
| B6 | lenses／history／diff composed from existing projections; no new truth |

B3 being blocked MUST NOT force B4／B5 scene／asset work to read private PUP state. B4／B5 MAY proceed after B2 when their own contracts and gates pass.

## 9. Agent checklists

### 9.1 Startup checklist

Before editing, the implementing Agent MUST report or record:

- [ ] exact base SHA, branch／worktree, and dirty-worktree assessment;
- [ ] Track B phase and explicit user authorization;
- [ ] plan decision IDs／contract clauses being implemented;
- [ ] files owned by this change and files explicitly out of scope;
- [ ] artifact families, official readers／validators, and authority／absence behavior involved;
- [ ] backward-compatibility and feature-flag effect;
- [ ] baseline tests and representative fixtures;
- [ ] unresolved `OPEN`／`BLOCKED` item, if any — implementation stops for that item.

### 9.2 Handoff checklist

Every implementation handoff MUST include:

- [ ] exact base and candidate commit SHA;
- [ ] phase, delivered capability, and non-goals;
- [ ] changed schemas／API versions and compatibility statement;
- [ ] source／authority／degradation mapping;
- [ ] valid, invalid, missing, stale, tampered, legacy, and ordinary-project fixture coverage as applicable;
- [ ] no-write／no-authority-escalation evidence;
- [ ] security／path-containment and privacy assessment;
- [ ] performance evidence for changed hot paths;
- [ ] focused and regression test commands／results;
- [ ] deferred risks and next separately authorized slice;
- [ ] explicit `no merge／no push` unless the user authorized those actions.

## 10. Change protocol

A change to a `MUST`／`MUST NOT`, authority meaning, source precedence, identity, lifecycle, or API wire semantics requires all of:

1. a new decision／supersession entry in the Track B plan;
2. an ADR or equally explicit rationale when the change crosses an existing boundary;
3. updated schemas and positive／negative contract tests;
4. a new API／schema version if existing consumers could interpret the same bytes differently;
5. independent review before merge.

Implementation convenience, UI layout, a newly discovered file, or an Agent's preference is not sufficient authority to change this contract.

B-D032 records the B1C exception: Workspace readers may import only the named
`styles.playbook_loader.load_playbook` catalog reader, after exact playbook-key
validation. It does not permit catalog enumeration, generator access, dynamic
or whole-module imports, style selection, or writes.

## 11. B0 slice entry and exit gates

B0 is deliberately split so that prose is not mistaken for an implemented schema and an implementation Agent is not trapped by a circular startup gate.

### B0.0A documentation seal

B0.0A is complete only when this contract, the Track B plan, the `AGENT_GUIDE.md` route, and the startup／handoff checklist are independently reviewed and integrated together. B0.0A freezes semantics and development boundaries; it does **not** by itself complete B0.0 or claim that schemas, fixtures, API routes, or runtime projections exist.

### B0.0B enforcement scaffold

B0.0B turns the anti-drift boundary into repository structure and tests without implementing the product. It consists only of:

- the tracked `backlot/workspace/{readers,projection,api_v1}` package seams and unserved `backlot/workspace/ui` source seam;
- the one-way dependency and authority-import checks in `tests/backlot/test_workspace_governance.py`;
- the machine-readable coverage inventory in `tests/backlot/fixtures/workspace/fixture-matrix.v1.json`;
- executable checks that reject private-sidecar literals, unsafe layer direction, missing mandatory entry points, stale evidence references, unsafe fixture paths, and false claims that pending consumer fixtures are materialized.

B0.0B **MUST NOT** register a route, provide a Workspace UI, read a project, implement a resolver, define B0.1 wire schemas, call a provider／publisher／writer, or change existing Board runtime behavior. The coverage inventory records baseline evidence and future fixture ownership; it is not a B0.1 consumer golden or a B0.2 performance fixture.

### Full B0.0 exit gate

B0.0 is complete only when all of the following are true:

- [x] B0.0A documents and `AGENT_GUIDE.md` route are reviewed and integrated;
- [x] B0.0B package／UI seams, fixture inventory, and executable tests are reviewed and integrated;
- [x] `tests/backlot/test_workspace_governance.py` passes without skip／xfail;
- [x] the guard demonstrably rejects forbidden authority imports, reversed dependencies, private-source access, unsafe fixture references, and missing mandatory entry points;
- [x] existing Board source and runtime behavior remain unchanged by B0.0B.

### B0.1 schema and fixture materialization

B0.1 MUST NOT start until:

- [x] full B0.0A＋B0.0B is reviewed, merged／available to the implementing worktree, and its governance test passes;
- [x] the user explicitly authorizes B0.1;
- [x] the field/source/reader/validator/authority/degradation/owner matrix scope, template, and source owners are approved;
- [x] feature-flag, versioning, no-write, legacy parity, path-safety, and large-course fixture plans are approved;
- [x] no B0～B2 wire-shape decision required by this v1 contract remains unowned or left for UI inference.

B0.1 completes the field／source authority matrix and materializes ResourceRef, RevisionRef, AuthorityDescriptor, WorkspaceProjection, MediaRef, GenerationInstruction, PreviewTimeline, capability, diagnostic, pagination, and typed-relation schemas plus positive／negative fixtures. Candidate Set／Assignment remains a forward identity／relation boundary; B0.1 MUST NOT add its persistence or mutation. B0.1 is complete only after the matrix, schemas, and fixtures receive independent contract review. It MUST NOT add Workspace runtime routes or UI.

The reviewed B0.1 artifact set is fixed at `docs/backlot-workspace-field-source-matrix.v1.{md,json}`, `schemas/workspace/workspace_projection_v1.schema.json`, `backlot/workspace/projection/{types,contracts}.py`, `tests/backlot/test_workspace_contracts.py`, and the B0.1-owned entries in `tests/backlot/fixtures/workspace/fixture-matrix.v1.json`. Adding a competing schema bundle, authority matrix, or precedence implementation requires the change protocol in this contract.

### B0.2 resolver and Workspace foundation

B0.2 runtime／API work MUST NOT start until the reviewed B0.1 schemas and fixtures are integrated and the user explicitly authorizes B0.2.

B0 is complete only when B0.2 proves:

- [ ] source precedence covers approved, awaiting, in-progress, failed, invalid, matching／mismatched cache, legacy, and missing cases;
- [ ] canonical／candidate／history coexistence and no-active-canonical behavior fail closed correctly;
- [ ] tests prove no private-sidecar reads and no inferred ownership／crosswalk;
- [ ] filesystem snapshots prove GET／HEAD do not change project truth; only explicitly allowed cache may change;
- [ ] common ResourceRef／RevisionRef, authority, snapshot, MediaRef owner／containment, and typed many-to-many relation behavior follows the B0.1 contracts;
- [ ] flag-off／flag-on and all existing Board／ordinary-project API tests remain green;
- [ ] ETag, snapshot-bound pagination, bounded list, and SSE single-flight behavior pass;
- [ ] a representative 40～60 minute fixture has measured budgets for catalog, shell／foundation projections, payload, parse count, requests, base DOM, memory, and event／history behavior;
- [ ] rollback is demonstrated by disabling the flag without canonical migration.

GenerationInstruction rendering／no-fabrication, PreviewTimeline derivation and player behavior, media loading, preview startup／seek, and preview proxies are B2／first-release acceptance gates. Their wire schemas are frozen in B0.1, but B0.2 MUST NOT implement them merely to close B0.
