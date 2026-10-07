# Batch Executor V2 component status

```yaml
component: batch-v2
status: dormant_opt_in
default_enabled: false
production_qualified: false
kj_course_cinematic_supported: false
activation_authority:
  - explicit_user_request
  - explicit_pipeline_manifest_opt_in
```

## Binding routing policy

Batch Executor V2 is dormant. Unless the user explicitly requests Batch V2,
or the selected pipeline manifest explicitly declares a Batch V2 opt-in
execution profile, an Agent must not proactively read, recommend, route to,
invoke, extend, or treat it as an available execution choice.

Incidental search matches, imports, tests, entrypoints, GCS classes, or existing
compatibility consumers do not establish activation or production support.
`kj-course-cinematic` must use and evolve its own current contracts; it must not
be altered to fit Batch V2's frozen provider, operation, storage, concurrency,
or publication assumptions.

## Current evidence boundary

- Batch V2 was merged into `team-main` by `b5d7586` as an opt-in path.
- M0–M4 offline qualification completed.
- M5 real GCS, Cloud Run, IAM, and provider qualification was not performed.
- The legacy execution path remains the default.
- Existing PUP, Backlot, BaseTool, and checkpoint compatibility dependencies
  remain in place; this status does not modify their runtime behavior.

## Deferred physical isolation

Physical extraction is intentionally deferred until `kj-course-cinematic` is
complete. A later, separately approved plan must first identify reusable
storage, receipt, integrity, budget, locking, resume, and publication
primitives; migrate active consumers; run regression tests; and only then
archive the remaining Batch V2 implementation in Git. This document grants no
authority to move, delete, refactor, activate, deploy, or call a provider.
