# Director Workspace module boundary

This directory contains the tracked B0.0B enforcement seam, the B0.1 common
projection contract, and the B0.2A read-only catalog foundation. It registers
no route, changes no existing Board behavior, and grants no production write
authority.

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

B0.2A adds only `readers/catalog.py` and `projection/catalog.py`: contained
direct-child marker authentication, validation through the public
`load_pipeline_readonly` seam, and a bounded snapshot-bound catalog resolver.
It intentionally does not add shell/stage-rail projections, checkpoints,
course classification, API/feature-flag/UI work, media, or private-sidecar
reads. Missing, invalid, or unusable marker/title evidence is omitted rather
than inferred from a directory, route, filename, or latest checkpoint. An
authenticated marker with a missing or invalid selected manifest remains a
degraded, unavailable catalog item with marker-scoped diagnostics.

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
`lib.batch_executor.publication`. Adding or widening an exception requires the
Architecture Contract change protocol and independent review. Whole-module,
star, dynamic, provider, writer, and private Production Unit imports are
rejected by the governance test.

`tests/backlot/test_workspace_governance.py` enforces this direction and the
forbidden authority imports. `tests/backlot/test_workspace_contracts.py`
enforces the B0.1 schema and semantic contract.
`tests/backlot/fixtures/workspace/fixture-matrix.v1.json` distinguishes the
materialized B0.1 consumer goldens from the still-pending B0.2 large-course
runtime fixture. The normative product boundary remains
`docs/backlot-workspace-architecture-contract.md`.
