# Director Workspace module boundary

This directory contains the tracked B0.0B enforcement seam, the B0.1 common
projection contract, the B0.2A catalog foundation, and the B0.2B projection
API foundation.  B0.2B registers only server-flagged, read-only v1 routes;
with `BACKLOT_WORKSPACE_ENABLED` absent or false they return 404 and existing
Board behavior remains unchanged.  It grants no production write authority.

The B0.1 contract surface is intentionally narrow:

- `schemas/workspace/workspace_projection_v1.schema.json` is the normative
  closed JSON wire-schema bundle;
- `projection/types.py` mirrors those shapes for static Python consumers;
- `projection/contracts.py` adds pure, no-I/O semantic checks for authority,
  source snapshots, lifecycle, media, prompt, PUP, pagination, and preview
  invariants;
- `docs/backlot-workspace-field-source-matrix.v1.{md,json}` records producer
  ownership, approved readers／validators, degradation, and B0.2 gaps;
- `tests/backlot/fixtures/workspace/` contains B0.1 consumer wire goldens, not
  canonical project trees or runtime fixtures.

B0.2A adds contained direct-child marker authentication, validation through the
public `load_pipeline_readonly` seam, and a bounded snapshot-bound catalog
resolver. B0.2B adds `readers/shell.py`, `projection/shell.py`, and
`api_v1/router.py`: the manifest-driven stage rail may observe only official
`read_checkpoint` results. Missing or invalid checkpoints remain explicit
stage states; no loose fallback is consulted. B0.2C adds the separately served
shell source. B0.2D adds quoted ETags derived only from the validated
projection source snapshot, conditional GET, coarse Workspace SSE invalidation,
and a bounded app-memory projection cache. The cache stores validated response
JSON only, is invalidated by project changes, and is disposable on restart or
flag-off; it never writes under a project root. SSE carries only a change type
and project id, never a path, source snapshot, or producer payload.
B1A adds one separately scoped Course read seam: `readers/course.py` observes
only the authenticated project's manifest-declared `proposal` checkpoint via
`read_checkpoint`.  A Course becomes canonical only when that checkpoint is
`completed` and `human_approved`, and its `proposal_packet` and
`course_manifest` both pass their official schema and semantic validators with
an exact `project_id` binding. Awaiting-human evidence remains a candidate;
history, loose artifacts, PUP/Batch sidecars, delivery/publication and all
writers remain out of scope. The proposal-stage Inspector lazy-loads this
revision set and presents structured learning-design declarations only.

Course/candidate classification, media, and private-sidecar reads remain out
of scope.
Missing, invalid, or unusable marker/title evidence is omitted rather than
inferred from a directory, route, filename, or latest checkpoint.

B1B adds the same narrowly scoped Script seam. It resolves exactly one
manifest-declared stage whose `produces` contains `script`, observes only that
stage via `read_checkpoint`, and validates the embedded artifact with
`validate_artifact("script")`. A completed checkpoint is canonical only after
its manifest Human Gate is approved; awaiting-human is a candidate. Working
and failed snapshots have no v1 RevisionSet display slot and are unavailable.
Loose `artifacts/script.json` remains the recorded `b0.2_contained_reader_gap`:
it is not read or displayed by B1B, and invalid modern evidence blocks any
fallback. The Script endpoint and Inspector are read-only and stage-lazy.

B1C adds a project-scoped, multi-source Style projection. It validates the
manifest-declared proposal owner and selected concept, then calls only the
governed named `styles.playbook_loader.load_playbook` reader with the exact
producer-declared key. Marker, proposal, and scene-plan names remain distinct
observations; a missing scene plan is not a conflict. The current catalog is
not historically frozen, and no `style.json`, catalog enumeration, generator
loader, provider, or write path is used.

The allowed dependency direction is:

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

- `readers/` is the only Workspace layer that may adapt canonical sources.
  It may use only explicitly approved, read-only public contracts.
- `projection/` owns common identity, authority, provenance, capability, and
  degradation semantics. It obtains observations through `readers/` and may
  not import raw source readers, API, or UI code.
- `api_v1/` is the future `/api/workspace/v1` transport boundary. It may not
  bypass projections to reinterpret files or authority.
- `ui/` is the future browser-source surface. It stays outside the existing
  wholesale-mounted `backlot/ui/` tree until B0.2 can register it behind the
  default-off flag. It may consume only versioned Workspace responses and safe
  media routes supplied by them.
- A future Agent Intent gateway is a separately authorized B4 boundary. It is
  not part of this scaffold and will not grant Backlot provider, checkpoint,
  approval, or publication authority.

The package root is inert, and unlisted top-level modules or subpackages fail
closed. Adding another layer (including future shared models or the B4 intent
gateway) requires the Architecture Contract change protocol, its dependency
direction, and matching governance tests in the same reviewed change.

Because some existing modules mix read and write capabilities, imports are
capability-level, not package-level. The explicit read allowlist is limited to
`read_checkpoint`, `read_project_marker`, `validate_checkpoint`, and
`CheckpointValidationError` from `lib.checkpoint`; `load_pipeline_readonly`
from `lib.pipeline_loader`; and `inspect_v2_asset_manifest_claim` from
`lib.batch_executor.publication`; and `load_playbook` from
`styles.playbook_loader`. Adding or widening an exception requires the
Architecture Contract change protocol and independent review. Whole-module,
star, dynamic, provider, writer, and private Production Unit imports are
rejected by the governance test.

`tests/backlot/test_workspace_governance.py` enforces this direction and the
forbidden authority imports. `tests/backlot/test_workspace_contracts.py`
enforces the B0.1 schema and semantic contract.
`tests/backlot/fixtures/workspace/fixture-matrix.v1.json` distinguishes the
materialized B0.1 consumer goldens from the still-pending B0.2 large-course
runtime fixture. B0.2D's generated, foundation-only 100-project performance
evidence is recorded separately in
`docs/backlot-workspace-b02d-foundation-baseline.v1.json`; it does not upgrade
that fixture into Course authority. The normative product boundary remains
`docs/backlot-workspace-architecture-contract.md`.
