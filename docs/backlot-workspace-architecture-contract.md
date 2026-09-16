# Backlot Director Workspace Architecture Contract

> **Contract version**: `backlot.workspace.architecture.v1`
> **Baseline**: `team-main @ 847cda02baa7a166da8f7a71976013765a5f71f2`
> **Status**: B0.0 normative contract; this document does not by itself authorize product-code changes
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
4. the relevant current Backlot source and tests.

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

## 4. Authority and source-resolution rules

### 4.1 Official readers only

- A canonical／candidate／published badge **MUST** come from an official reader and validator accepted for that artifact family.
- Each projected field group **MUST** identify its owner stage, reader／validator, source kind, lifecycle, absence semantics, and degraded behavior.
- Reading syntactically valid JSON directly does not establish authority.
- Invalid authoritative evidence **MUST** fail closed. It **MUST NOT** fall back to a loose file that looks usable.
- A permitted legacy fallback **MUST** be labeled `display_only + unverified`.

### 4.2 No private producer state

Workspace code **MUST NOT** scan or interpret producer-private state, including:

- `.production-units/**`;
- `.batch-v2/**` private attempts／receipts;
- coordinator `state.json` or receipt directories;
- opaque `profile_ref` targets;
- arbitrary filesystem paths or unapproved remote URLs.

Missing public contract means `unavailable`, not permission to infer a schema. The M6.0B checkpoint field `metadata.production_units.candidate_handoff`, after official checkpoint validation, is JSON handoff provenance only. It is not unit content, aggregate progress, Human approval, qualification, publication, adoption, or recovery authority.

### 4.3 Revision lifecycle

- Canonical, pending candidate, execution evidence, display-only data, invalid data, and history **MUST** remain distinct.
- An awaiting candidate **MUST NOT** overwrite the presentation of a producer-identified active canonical revision.
- Archived history **MUST NOT** be promoted to active canonical merely because it is the most recent completed entry.
- The current checkpoint writer has no active-canonical pointer during an awaiting rerun. Until a producer-owned pointer exists, `current_canonical` **MUST** be unavailable in that state; the pending candidate and history MAY still be shown.

### 4.4 Deterministic snapshots

Every projection and projected revision **MUST** carry a deterministic source set and composite digest. Sorted source identity／digest pairs form the projection token and ETag. Pagination cursors, future intents, previews, and candidate assignments **MUST** bind to the source snapshot that produced them.

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

Producer-declared, tool-observed, and human-reviewed metadata **MUST** remain separately labeled. Filesystem paths and URLs are locators, not identity. A preview proxy is disposable server cache, not a canonical asset.

### 5.3 GenerationInstruction

A `GenerationInstruction` **MUST** have a stable ID derived from exact source identity, an owning／creative scope, explicit target refs, a revision／digest, kind, display-safe content, source locator, authority, evidence scope, and unavailable reason.

Creative specification, shared scene instruction, tile／shot delta, negative prompt, and actual provider input **MUST** remain distinguishable. If a provider received one composite-sheet prompt, Backlot MUST NOT fabricate one provider prompt per tile. Missing provider input is `unavailable`; it MUST NOT be reconstructed from scene descriptions, CLP anchors, Style prefixes, or similar text.

### 5.4 PreviewTimelineProjection

The Preview Player **MUST** consume a versioned, read-only projection produced from validated scene plan, asset manifest, optional valid edit decisions, resolved MediaRefs, and—for `final_render`—a validated render report with stable output identity. It MUST NOT join raw／loose files in the browser.

Fidelity MUST be explicit:

- `planning_preview`: plan-level approximation;
- `edit_preview`: supported cuts／audio／simple transitions from edit evidence;
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
| B0 | B0.0 document seal; B0.1 schema／fixture materialization; B0.2 read resolver, versioned shell, compatibility and foundation performance evidence |
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

## 11. B0 slice entry and exit gates

B0 is deliberately split so that prose is not mistaken for an implemented schema and an implementation Agent is not trapped by a circular startup gate.

### B0.0 document seal — current slice

B0.0 is complete only when this contract, the Track B plan, and the `AGENT_GUIDE.md` route are independently reviewed and committed together. B0.0 freezes semantics and development boundaries; it does **not** claim that schemas, fixtures, API routes, or runtime projections exist.

### B0.1 schema and fixture materialization

B0.1 MUST NOT start until:

- [ ] the B0.0 document seal is merged／available to the implementing worktree;
- [ ] the user explicitly authorizes B0.1;
- [ ] the field/source/reader/validator/authority/degradation/owner matrix scope, template, and source owners are approved;
- [ ] feature-flag, versioning, no-write, legacy parity, path-safety, and large-course fixture plans are approved;
- [ ] no B0～B2 wire-shape decision remains unowned or left for UI inference.

B0.1 completes the field／source authority matrix and materializes ResourceRef, RevisionRef, AuthorityDescriptor, WorkspaceProjection, MediaRef, GenerationInstruction, PreviewTimeline, capability, diagnostic, pagination, and typed-relation schemas plus positive／negative fixtures. Candidate Set／Assignment remains a forward identity／relation boundary; B0.1 MUST NOT add its persistence or mutation. B0.1 is complete only after the matrix, schemas, and fixtures receive independent contract review. It MUST NOT add Workspace runtime routes or UI.

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
