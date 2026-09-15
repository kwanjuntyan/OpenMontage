# Production Unit Protocol — Lean M2a

Status: experimental, opt-in, scene-plan compare-only proof.

This protocol tests whether a long approved script can be planned in bounded
units without changing OpenMontage's canonical pipeline. It does not claim
that 180 seconds is optimal, enable long-course production, or authorize
publication.

## Hard boundary

Lean M2a applies only to `scene_plan` and consumes:

- the approved canonical `script` from its completed checkpoint;
- the canonical `clp_manifest` from its completed checkpoint;
- an exact digest-bound projection of the already approved proposal/style
  context used by the normal scene stage;
- a separately generated, schema-valid monolithic scene-plan baseline when a
  completed comparison is requested.

It does not segment script or CLP creation. It does not run assets, edit,
compose, Backlot, provider calls, or media generation.

## Modes

### `off` (default)

Missing policy and explicit `off` mean the same thing. Follow the existing
scene-director process unchanged. Do not import or call Production Unit
helpers, create `.production-units/`, alter artifacts, add checkpoint
metadata, or change the Human Gate.

### `compare_only`

The user must explicitly opt in. Read the approved predecessor artifacts
through the checkpoint API, then use
`lib.production_units.scene_plan_merge.run_scene_plan_compare` in memory.
The helper only returns a candidate/report and always reports
`publish_allowed: false`.

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

Do not call `write_checkpoint`, replace `scene_plan.json`, update checkpoint
status, or advance the scene-plan Human Gate from this path. A future reviewed
milestone must add an explicit publication contract before candidates can
become canonical artifacts.

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
attention. That requires later paired live-Agent benchmarks and is outside
Lean M2a.
