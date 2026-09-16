# Director Workspace module boundary

This directory is the tracked B0.0B enforcement seam. It is deliberately a
non-runtime scaffold: it registers no route, reads no project, defines no wire
schema, and changes no existing Board behavior.

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
capability-level, not package-level. The initial read allowlist is limited to
`read_checkpoint`, `validate_checkpoint`, and `CheckpointValidationError` from
`lib.checkpoint`, plus `inspect_v2_asset_manifest_claim` from
`lib.batch_executor.publication`. Adding or widening an exception requires the
Architecture Contract change protocol and independent review. Whole-module,
star, dynamic, provider, writer, and private Production Unit imports are
rejected by the governance test.

`tests/backlot/test_workspace_governance.py` enforces this direction and the
forbidden authority imports. `tests/backlot/fixtures/workspace/fixture-matrix.v1.json`
tracks the compatibility scenarios that later phases must materialize. The
normative product boundary remains
`docs/backlot-workspace-architecture-contract.md`.
