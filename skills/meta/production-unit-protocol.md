# Production Unit Protocol — Lean M2–M5 experimental profile

Status: experimental and opt-in. Planning, editing, and render preparation
remain in-memory candidates whose only publisher is the existing checkpoint
workflow. Render commands require an explicitly injected executor and do not
grant media, provider, filesystem, checkpoint, or publication authority.

This protocol provides bounded candidate paths for course script, CLP, scene
planning, Batch V2 assets, edit/render preparation, and read-only Backlot
projection without changing OpenMontage's canonical pipeline. It does not
claim that 180 seconds is optimal, establish 60-minute production
qualification, or authorize publication.

## Hard boundary

The scene-plan M2a slice consumes:

- the approved canonical `script` from its completed checkpoint;
- the canonical `clp_manifest` from its completed checkpoint;
- an exact digest-bound projection of the already approved proposal/style
  context used by the normal scene stage;
- a separately generated, schema-valid monolithic scene-plan baseline when a
  completed comparison is requested.

For an approved `content_form=course_form` proposal, M2b may additionally:

- build script units from complete, approved lesson boundaries in the
  proposal checkpoint's canonical `course_manifest`;
- merge script fragments only after exact lesson/section ownership, timing,
  stable IDs, source digests, and global voice-performance agreement pass;
- extract CLP candidates per inherited script unit and require one
  Agent-authored resolution map bound to the exact combined candidate digest;
- merge that resolution into the one existing course-wide `clp_manifest`.

No PUP helper runs Backlot, providers, or media by itself. A Production Unit is
never a lesson, checkpoint, or nested project.

## M3 Batch V2 asset boundary

The first asset route is `batch_v2_owned` for the exact qualified generated-
video identity only. PUP may group the validated global scene timeline, check
100% coverage of video requirements assigned to this route, and compile
Agent-authored immutable specs into a normal frozen Batch V2 request. It must
preserve every authenticated source binding, existing budget/attempt limits,
and exact scene-plan-to-CLP-binding digest.

Batch V2 remains the sole owner of dispatch, retry, ambiguous-charge handling,
storage receipts, resume, review state, cost accounting, PublicationCommand,
and canonical asset publication. PUP may bind an exact BatchResult for later
review; it never publishes an `asset_manifest`. Unsupported asset/provider
routes stay unsupported until separately qualified.

## M4 edit and render boundary

PUP may derive edit units from the approved global scene timeline and merge
validated fragments into one ordinary `edit_decisions` candidate. Global
timestamps remain authoritative. Every primary cut must remain inside its unit,
reference an asset owned by that unit, and cover the unit without gaps or
overlap. Global audio/subtitle configuration and the proposal-locked
`renderer_family`, `render_runtime`, and `composition_mode` are supplied once;
unit workers cannot replace or silently swap them.

After normal edit review, PUP may freeze one unit-render command per edit unit.
An executor must return a content digest, byte size, and complete probe evidence.
Duration, resolution, fps, codecs, required audio, sample rate, A/V sync,
decode-to-null, and timestamp monotonicity are hard gates. Only exact unit
receipts may form the deterministic assembly command; the assembled master must
pass the same profile before PUP can return an ordinary `render_report`
candidate. Failed or stale units can be regenerated independently, but neither
receipts nor candidates are canonical artifacts until the existing director,
checkpoint writer, final review, and Human Gate accept them.

## Two-axis execution vocabulary

Never use one `mode` field for both policy and execution intent.

| Axis | Values | Authority |
|---|---|---|
| Approved proposal policy | `off`, `auto`, `fixed` | `proposal_packet.production_plan.production_unit_policy.mode` |
| Stage-internal execution disposition | `compare_only`, `publish_candidate` | The bounded helper call/unit execution contract |

Legal mappings are deliberately small: `off` has no execution disposition and
is a strict no-op; `auto` or `fixed` may request `compare_only` or
`publish_candidate` only for a stage listed in the approved policy. An absent
policy is `off`. A disposition without an approved non-off policy, a stage not
listed in `enabled_stages`, mixed legacy/canonical arguments, or a disposition
unsupported by that helper fails closed.

M2-M5 Python helpers temporarily retain their old `mode="compare_only"` /
`mode="publish_candidate"` keyword as a compatibility alias. New code must pass
`production_unit_policy=...` and `execution_disposition=...`; the compatibility
alias is not a proposal mode and must not appear in proposal artifacts.

## Policy modes

### `off` (default)

Missing policy and explicit `off` mean the same thing. Follow the existing
scene-director process unchanged. Do not import or call Production Unit
helpers, create `.production-units/`, alter artifacts, add checkpoint
metadata, or change the Human Gate.

### `auto`

The approved semantic boundaries are derived using the configured soft target.
This selects PUP policy, but does not by itself select an execution disposition
or grant publication authority.

### `fixed`

The approved boundary configuration is fixed for the run. It still requires a
separate execution disposition and carries no publication authority.

## Execution dispositions

### `compare_only`

The user must explicitly opt in. Read the approved predecessor artifacts
through the checkpoint API, then use
`lib.production_units.scene_plan_merge.run_scene_plan_compare` in memory.
The helper only returns a candidate/report and always reports
`publish_allowed: false`.

Script and CLP use `run_script_units` and `run_clp_units`. They accept the same
default-off contract. Their `publish_candidate` disposition only returns a
validated in-memory candidate; it grants no checkpoint, gate, provider, or
filesystem authority. The normal stage director must still review and pass the
candidate to the existing checkpoint writer.

### `publish_candidate`

This disposition permits a helper to return a validated candidate to the
owning director. It is not canonical publication. The director, reviewer,
canonical validator, checkpoint writer, and existing Human Gate remain the
only handoff path. Asset and render adapters may still report
`publish_allowed: false` because Batch V2 and the existing render/checkpoint
contracts retain their separate authority.

## Qualification profile and capability matrix

`schemas/execution/production_unit_qualification_profile.schema.json` binds a
claim to exact Git, pipeline manifest, schemas, adapters, pipeline/content
form/stages, runtime/composition mode, provider/model/asset route, media
profile, OS/runtime/hardware, evidence digests, and requalification triggers.
`schemas/execution/production_unit_capability_matrix.schema.json` projects
those exact profiles for consumers. The safe status vocabulary is `unknown`,
`unsupported`, `experimental`, `code_complete`, `beta_qualified`,
`production_qualified`, `disabled`, and `invalid`.

`pipeline_manifest.extensions.production_units.supported: true` means only
that the pipeline implements an opt-in route. It never upgrades a profile's
qualification status. Only exact versioned evidence may do that.

For script, every approved lesson is owned once, every narration section maps
to exactly one owned lesson, global timestamps remain authoritative, and legal
non-narration gaps are preserved. For CLP, worker completion order is ignored;
every local candidate is either mapped to a same-category final entity or
explicitly ignored, and every final entity must be sourced by a candidate.

1. Treat script sections as narration intervals, not as proof that every
   second contains narration. Derive a complete ordered timeline from those
   intervals plus explicit `visual_only` spans for legal head, inter-section,
   and tail gaps. Build units only at those derived boundaries. Unit size is
   configurable; 180 seconds is only the experimental default.
2. Give each planning invocation only its `context_capsule`. The capsule
   contains the assigned timeline spans and narration sections, compact
   previous/next span hints, and the canonical CLP with source digests.
3. Return the exact `context_capsule_sha256`, one version 1.0 scene-plan
   fragment using the approved style playbook, and CLP binding rows for that
   unit. Scenes inside narration spans must carry the matching
   `script_section_id`; scenes inside `visual_only` spans must omit it and are
   owned by their time range. A stale result or a unit claiming another
   unit's span is rejected.
4. Merge by authoritative unit ordinal, never by completion order.
5. Require exact narration-section and complete visual-timeline coverage,
   unique scene IDs, resolvable CLP references, exact binding coverage, and
   deterministic canonical digests.
6. Validate the independent monolithic baseline by the same coverage, style,
   schema, and CLP rules. Record both digests, scene counts, count delta, and
   whether scene IDs/order match.
7. Present the comparison result as experimental evidence only.

Production Unit helpers never call `write_checkpoint`, replace artifacts,
update checkpoint status, or advance a Human Gate. Publication candidates can
become canonical only through the existing stage director, schema/semantic
validation, checkpoint writer, and original Human Gate.

## Fail closed

Stop the compare-only attempt when:

- a derived narration or visual-only span exceeds the configured hard max;
- a context capsule exceeds its byte limit;
- source or capsule digests are stale;
- a unit result is missing, duplicated, or owns foreign content;
- a scene crosses a span boundary, claims a mismatched narration section, or
  scene timings have a gap, overlap, invalid order, or incomplete coverage;
- scene IDs, bindings, or CLP references are missing, duplicated, or dangling;
- unit style playbooks disagree.

Failure of this experiment never changes the approved canonical artifacts.
The operator may continue through the existing monolithic scene process only
as an explicit production decision under the normal Human Gate.

## Interpretation

Passing deterministic fixtures proves bounded plumbing, merge integrity, CLP
sharing, and repair isolation. It does not by itself prove better Agent
attention.

One frozen 30-minute `off` versus `auto@180s` paired benchmark has now passed
its mechanical gates and blind semantic threshold; see
`docs/production-unit-benchmark-30m.md`. It supports superiority for that
course/profile only. It does not prove that 180 seconds is a universal optimum
or satisfy M6 qualification.

Treat `longest_same_type_run` as a coarse diagnostic only. `scene.type` does
not encode setting, framing, movement, overlays, character action, or semantic
variation, so a longer run must not by itself trigger a repair or fail a unit.
Use semantic review and richer repetition telemetry to judge perceived visual
redundancy.
