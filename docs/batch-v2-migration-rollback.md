# Batch Executor V2 migration and rollback

Status: M4 offline rehearsal only. This document does not authorize a provider
call, credential lookup, GCS mutation, image build/push, Cloud Run execution,
deployment, merge, or legacy retirement.

## Coexistence invariant

V2 remains opt-in. It runs only when an operator explicitly invokes
`scripts/batch_execute.py` or the separate Agent publication entrypoint with a
frozen request/config. No existing pipeline or legacy command routes to V2 by
default. The legacy `scripts/batch_run_intent_sequences.py` remains present at
its accepted SHA-256
`1a6d92872ff9f91064b172ebce7e174226ccc4020a261c11b5e31c34f4d4416a`.
The annotated `team-main-pre-batch-v2` tag and ordinary Git history remain the
recovery baseline.

## Offline migration rehearsal

Run only this safe rehearsal in an uncredentialed offline workspace:

```text
python -m scripts.batch_v2_rehearse_rollback
```

It verifies the historical bytes, exercises the legacy `--help` parser, and
tests the single/all parser/dispatch stubs after replacing
`process_sequence`. It reports zero provider calls and zero canonical writes.
It never executes a sequence body. CI and release rehearsal must not invoke a
real sequence selector because doing so generates paid media and mutates
canonical project data.

The dedicated Linux gate additionally launches the real legacy entrypoint once
with only its help flag. That import/argument-parser smoke runs after `env -i`
inside the same OS no-egress namespace as pytest, uses `-B`, and must exit zero;
it never supplies a sequence selector. The AST rehearsal remains the safe test
of dispatch mapping without entering any production sequence body.

The rehearsal also confirms that V2 has a separate explicit entrypoint. It is
not evidence for the still-pending Linux or local-container 40-item gates and
is not production qualification.

## Opt-in migration sequence

1. Review the phase-aligned M0–M4 commits and their offline evidence.
2. Keep every V2 profile disabled in default/legacy routing.
3. Run the no-credential fake suites and the safe rehearsal above on copied or
   generated fixtures only.
4. Complete the repository-version Linux and local-container gates before
   claiming M4 complete. Do not waive unavailable infrastructure.
5. Merge only through the normal `team-main` review flow after Section 22.1 is
   satisfied. A merge still does not authorize M5 external qualification.
6. Keep the legacy runner through the opt-in coexistence window. Retirement is
   a later user-approved commit after the applicable M5 evidence passes.

## Rollback procedure

1. Disable the explicit V2 command/profile in the invoking automation. Do not
   alter retained V2 blobs, receipts, execution state, or canonical artifacts.
2. Continue using the untouched legacy entrypoint only under its normal paid
   execution approvals; use the offline rehearsal above for CI/readiness.
3. Reverse a faulty V2 integration with a normal `git revert
   <reviewed-integration-commit>` and review the generated commit. Never rewrite
   shared history or use a destructive reset.
4. If a reviewed rollback/restoration commit already exists on another branch,
   apply that exact commit with `git cherry-pick <reviewed-restoration-commit>`.
5. If a future legacy-retirement commit has landed, restore it by reverting
   that retirement commit. The safety tag can be inspected to verify the
   historical content, but it must not be moved or deleted.
6. Run the parser/dispatch stub rehearsal and offline contract suites again,
   then record the new commit IDs and result. External cleanup requires a
   separate, narrowly scoped authorization.

Rollback disables new dispatch; it does not pretend that accepted or
indeterminate paid attempts never happened. Such state remains durable and is
reported to the Agent/user rather than replayed.
