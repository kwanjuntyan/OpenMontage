# OpenMontage Batch Executor V2 — Implementation Plan

> - Status: **Revised — awaiting coordinating main-task acceptance**
> - Planning branch: `codex/batch-v2`
> - Baseline commit: `aa4dbd42e0f0c05b7029198793c2e52041c24a47`
> - Safety tag: `team-main-pre-batch-v2` (annotated tag; peels to the baseline commit)
> - Audit date: 2026-09-14
> - Scope revision: MVP boundary plus workspace and Cloud resume-ownership contracts clarified on 2026-09-14
> - Scope of this commit: planning only; no Batch V2 implementation, deployment, or paid/live API call

## 1. Decision summary

Batch Executor V2 MVP will be one local-first, cloud-ready execution engine with two configuration profiles:

- `local`: durable local project/run storage plus project-scoped, non-canonical attempt staging.
- `cloud-run`: the same engine in one Cloud Run Job task, with GCS as durable storage and a materialized logical `projects/<project-id>/` workspace containing the same project-scoped staging layout.

The MVP is deliberately narrow: it executes only already-approved `assets`-stage work items, in one process, with bounded internal concurrency. The recommended starting point is three global workers, within the approved 2–4 range. A selected provider has its own explicit cap; an unqualified paid provider starts at one in-flight call. Gemini may remain at one for MVP rather than pulling generic thread-safety work into the critical path.

MVP must deliver all of the following as one vertical slice:

- `assets` stage only, initially independent video-generation assets needed by the historical batch use case;
- the same engine under `local` and single-task `cloud-run` profiles;
- exact immutable binding to one approved concrete tool/provider/route/model and all output-affecting inputs;
- per-item durable attempt/state, safe resume, partial-failure reporting, and paid-call ambiguity handling;
- one coordinator writer per invocation; every tool receives an explicit `output_path` under `projects/<project-id>/.batch-v2/runs/<batch-id>/attempts/<item-id>/<attempt-id>/`;
- Cloud ownership records that reject a second active execution and require trusted terminal/cancelled evidence or an explicit prior-invocation-bound human resume authorization before expected GCS generation CAS takeover;
- standard ADC for GCS and, when the selected Google provider route requires it, Vertex;
- synchronous private GCS uploads whose bytes, checksum, size, and object generation are verified before success;
- formal `asset_manifest` validation and official checkpoint validation/writes.

The following are explicitly **post-MVP enhancements** and may not block MVP completion unless an implementation-time failing safety test proves one is unavoidable: distributed leases/fencing or multiple coordinators, Cloud Run array jobs, multi-provider scheduling platforms, broad Backlot redesign, cross-file transactions, global cache/index services, generic storage/event-sourcing frameworks, and support for every media/tool family.

The governing boundary is non-negotiable:

- The **Agent** selects the pipeline and stage, reads the director/provider skills, makes creative choices, selects the exact provider/model, communicates cost, authors immutable work items, self-reviews results, and owns all Human Gates.
- The **executor** validates and mechanically runs only the exact, already-approved work items for one stage. It may schedule, rate-limit, retry when demonstrably safe, resume, cache, stage bytes, persist run state, and report results.
- The executor must never choose the next pipeline stage, generate or rewrite prompts, select a provider through a selector, silently change a provider/model, perform quality review, resolve a gate, or continue into edit/compose.

The executor's successful terminal state is `awaiting_agent_review`, not a pipeline `completed` checkpoint. After the execution process has stopped, the Agent self-reviews and authorizes a sequential single-writer publication through `schemas.artifacts.validate_artifact()` and `lib.checkpoint.write_checkpoint()`. MVP deliberately fails closed to the normal per-gate flow: a gated `assets` stage is written `awaiting_human`, and only a later explicit human reply permits `completed` with `human_approved=true`. Consuming broad/full-run pre-authorization is deferred until its documented `approval_policy` schema mismatch is resolved.

All worker output goes to `projects/<project-id>/.batch-v2/runs/<batch-id>/attempts/<item-id>/<attempt-id>/` or a path with exactly the same project-scoped semantics. This reserved subtree is inside the configured project workspace, but outside `artifacts/`, `assets/`, `renders/`, `history/`, and `checkpoint_<stage>.json`; it is never canonical and Backlot must ignore it. During execution, one coordinator is the only writer of run state, minimal cost state, storage receipts, and checkpoint progress. Publication occurs only after that process has stopped, under a separate sequential single-writer handoff. Existing hidden GCS background writers must be disabled in both execution and publication contexts.

For paid stochastic calls, exactly-once billing cannot be promised unless a provider supplies durable idempotency or recoverable remote job IDs. If a process may have lost contact after provider acceptance, the item becomes `indeterminate` and is not automatically submitted again.

## 2. Audit scope and evidence

The audit was read-only except for a workspace-scoped pytest temporary directory that was removed after the run. No real provider, GCS, or Cloud Run operation was invoked.

### 2.1 Git/worktree baseline

- The independent worktree is on `codex/batch-v2`.
- `HEAD` and `refs/heads/codex/batch-v2` both equal `aa4dbd42e0f0c05b7029198793c2e52041c24a47` before this planning commit.
- The annotated tag object for `team-main-pre-batch-v2` peels to the same baseline commit.
- The worktree was clean and `docs/batch-v2-implementation-plan.md` did not exist before this plan.
- Root `implementation_plan.md` is an existing CLP plan and is intentionally untouched.

### 2.2 Legacy runner findings

Audited file: `scripts/batch_run_intent_sequences.py`.

The runner was appropriate as a one-off production recovery script, but not as a reusable execution engine:

- It hard-codes `D:\kj-openMontage` (`line 21`), project names, Windows paths, sequence mappings, narration files, and direct tool imports.
- It executes generation serially, sleeps a fixed interval, retries broad exceptions with a fixed delay, and exits the whole batch on one terminal item failure.
- Its cache check is only file existence plus a byte-size threshold (`line 129`); it does not bind output to tool, model, inputs, source digests, or media validity.
- It mutates pipeline state and directly serializes artifacts/checkpoints instead of using the formal validation/writer path.
- It combines asset generation, audio timing, edit decisions, scene rendering, master render, GCS sync, and project metadata mutation. That is pipeline orchestration in Python and conflicts with the Agent-Native contract.
- Its artifact shapes do not validate against current `scene_plan`, `asset_manifest`, `edit_decisions`, and `render_report` schemas.
- Its GCS fallback at `line 349` references an undefined `project_id` name.
- No tests target this runner.

The three historical sequence plans contain 40 shots total:

| Sequence | Shots | Planned duration |
|---|---:|---:|
| 4 | 11 | 74.40 s |
| 5 | 15 | 112.48 s |
| 6 | 14 | 99.77 s |
| **Total** | **40** | **286.65 s** |

The provided production baseline is 33.6 minutes wall time, including 30.7 minutes of external generation wait, or about 46 seconds of external wait per shot.

### 2.3 Agent-Native boundary findings

The controlling requirements are explicit in `AGENT_GUIDE.md`:

- `line 80`: Python is tools plus persistence, not orchestration, creative decisions, review logic, or checkpoint policy.
- `lines 181–195`: the Agent owns the pipeline state machine, skills, tool use, self-review, checkpoints, and Human Gates.
- `lines 97–115`: before a paid or consequential call, the Agent announces the exact tool, provider, model/variant, reason, and whether it is a sample or batch.
- `lines 167–176`: provider/model/fallback changes require approval; blocked execution must not silently switch paths.
- `lines 556–570`: each stage has one schema-valid canonical artifact.
- `lines 587–595`: manifest Human Gates are binding and an `awaiting_human` checkpoint ends the Agent turn.

There is one contract inconsistency relevant to future full-run authorization: `AGENT_GUIDE.md:592` and `skills/meta/checkpoint-protocol.md` require full-run pre-authorization to be recorded with `decision_log.category = "approval_policy"`, but `schemas/artifacts/decision_log.schema.json` does not currently allow `approval_policy` in its category enum. The MVP therefore does not consume full-run pre-authorization; it follows the ordinary per-gate flow. Schema reconciliation is post-MVP and does not block implementation of that narrower behavior.

### 2.4 Artifact and checkpoint contract findings

Formal interfaces:

- Artifact registry and validator: `schemas/artifacts/__init__.py::validate_artifact`.
- Checkpoint builder/validator/writer: `lib/checkpoint.py::write_checkpoint`.
- Validating reader: `lib/checkpoint.py::read_checkpoint`.
- Checkpoint envelope schema: `schemas/checkpoints/checkpoint.schema.json`.

Confirmed behavior:

- A terminal `completed` or `awaiting_human` checkpoint must contain the manifest-declared canonical artifact.
- Every artifact supplied to a checkpoint must be registered and schema-valid.
- Manifest Human Gate requirements and terminal-stage prerequisites are enforced by `write_checkpoint`.
- `in_progress` may omit canonical artifacts; partial draft detail belongs in `metadata.partial_progress` unless a complete schema-valid artifact exists.
- The writer deep-copies caller data, validates and serializes before publishing, then uses a local temporary file plus `os.replace` for the current checkpoint.
- Read-time validation catches hand-edited invalid checkpoints.

Required precision: this is **single-file atomic visibility under a single-writer assumption**, not full durability or transactionality.

- Checkpoint and decision-log paths use fixed `.tmp` names and have no process lock, lease, revision, CAS, or fencing token.
- A concurrent writer can cause lost updates or temporary-file collisions.
- The decision log and checkpoint are separate writes; a crash between them can expose a cross-file partial commit.
- Archive writes are best-effort.
- There is no file and parent-directory durability barrier covering sudden power loss.
- Prerequisite enforcement is lifecycle-sensitive: `in_progress` and `failed` are allowed even when terminal prerequisites are not complete. Therefore an `in_progress` write is not proof that paid execution is authorized.
- Legacy compatibility allows a missing `project.json` in some checkpoint paths. Batch V2 must fail closed and require a valid project marker.

Schema observations relevant to V2:

- `scene_plan` describes timed scenes and required assets, but does not freeze an exact concrete tool, provider route, model, complete tool inputs, output digest contract, retry authorization, or budget. The executor must not derive these creative/production decisions from `scene_plan`.
- `asset_manifest` entries require `id`, `type`, `path`, `source_tool`, and `scene_id`; unknown properties are forbidden.
- `render_report` also forbids unknown top-level properties.
- There is no generic canonical loose-artifact writer; publication must validate first and be serialized by the coordinator, while checkpoint publication continues through `write_checkpoint`.
- Backlot currently prefers some loose artifact files over checkpoint-embedded values. Publishing an unreviewed loose draft could show a new artifact beside an old approval state.

### 2.5 Tool registry and BaseTool findings

Audited files: `tools/tool_registry.py` and `tools/base_tool.py`.

- The registry is the correct discovery and capability source of truth. Batch V2 must call discovery, then resolve the exact concrete tool named in the request.
- The executor must not invoke a selector or registry fallback because routing is an Agent decision.
- `BaseTool` exposes `RetryPolicy`, `ResumeSupport`, `idempotency_key_fields`, side effects, resource profile, and `ToolResult` fields.
- Those declarations are metadata only; BaseTool does not execute generic retries or enforce idempotency.
- `BaseTool.get_info()` currently omits at least `retry_policy`, `idempotency_key_fields`, and `progress_schema`, so the support envelope is insufficient for a generic batch scheduler.
- `BaseTool.idempotency_key()` hashes only declared fields and truncates the digest to 16 hex characters. It is not a provider idempotency token and is insufficient as a durable batch cache key.
- Successful tool execution can trigger hidden asynchronous GCS upload through BaseTool instrumentation. Worker-generated events can also write directly to project event files. Both bypass a V2 coordinator unless explicitly disabled or redirected.

MVP does not solve the generic support-envelope problem across all tools. It uses an explicit allowlist of qualified asset-generation adapters and validates the exact observed tool/provider/route/model. A registry-wide batch platform is post-MVP.

### 2.6 GCS findings

Audited file: `lib/gcs_storage.py` and `tests/lib/test_gcs_auto_sync.py`.

Credential conclusion:

- GCS already has an ADC path: `storage.Client(project=...)` and an explicit `google.auth.default()` fallback. Cloud Run service identity can therefore be used for GCS once packaging and IAM are correct.
- `google-cloud-storage` is not declared in `requirements.txt` or `setup.py`, so a clean Cloud image is not currently reproducible.

Durability and correctness gaps:

- `atomic_update_json()` uses a process-local thread lock, file `fsync`, and `os.replace`. It does not provide cross-process exclusion, revisions/CAS, fencing, directory durability, or schema validation.
- Uploads overwrite mutable destination names without `if_generation_match`, a stored object generation, or application-level digest verification.
- Upload errors are collapsed to `None`; callers cannot distinguish retryable, permanent, or ambiguous states.
- Background futures are in memory, `atexit` waits only briefly, and completion is not a durable success barrier. A Cloud Run task can exit after local success but before durable upload.
- Uploads are public by default and return a public-looking URL even when `make_public()` fails.
- The module has upload/sync methods but lacks the read/stat/materialize/conditional-create/CAS operations required for resume.
- Relative paths and project identifiers are not consistently validated through `lib.identity`.
- GCS sync mutates canonical loose JSON after upload by injecting `gcs_url` into artifact shapes that forbid it. This can turn a formerly valid artifact into a schema-invalid one.
- BaseTool success and terminal checkpoint writes each have separate auto-sync paths, creating hidden second writers.

The V2 design must use immutable content-addressed objects, private durable locators, GCS object generation preconditions, structured errors, and a synchronous durability barrier before an item is committed.

### 2.7 Gemini Omni findings

Audited file: `tools/video/gemini_omni_video.py`.

- The tool is stochastic and paid, with an estimate of approximately USD 0.10 per generated second in the current implementation.
- Credential discovery checks API keys, a `GOOGLE_APPLICATION_CREDENTIALS` file, a hard-coded `D:\gcp-keys\...json`, and a repository `.env` file.
- Vertex execution explicitly loads a service-account JSON file. It does not use `google.auth.default()` or the Cloud Run metadata-server identity, so Gemini Vertex is not currently Cloud Run service-identity ready.
- Ambient credential choice also changes the API route and model (`Developer API` versus `Vertex`), violating the need to announce and freeze the exact provider route/model before execution.
- The declared retry policy is not executed by BaseTool. The request itself uses no provider idempotency token.
- The current idempotency fields omit reference content digests, input video digest, duration, `store`, resolved route/model, and tool revision.
- HTTP failures are flattened into strings without typed retryability, `Retry-After`, provider-acceptance phase, or durable remote interaction ID.
- A timeout or crash after provider acceptance but before durable result persistence may have generated and charged for a clip. Blind retry can duplicate spend.
- Output bytes are written directly to the requested final path with no atomic staging, digest, or media probe.
- Vertex execution globally patches DNS resolution and uses an unlocked global credential cache; safe multi-threaded Gemini operation has not been established.

Consequences for the initial profile:

- Gemini's provider cap remains one for MVP. Raising it above one requires later credential/global-state thread-safety qualification and is not an MVP gate.
- The request freezes Developer versus Vertex, project/location, exact model, and auth mode; environment discovery may satisfy credentials but must not alter routing.
- Vertex must adopt ambient ADC for Cloud Run. A service-account file may remain an explicit local-only option; the hard-coded path and hard-coded project fallback must be removed.
- After a possibly accepted paid call, V2 records `indeterminate` and stops automatic replay unless the remote operation can be reconciled safely or the user explicitly re-authorizes it.

### 2.8 Cost and observability findings

- `ToolResult` can report cost, duration, seed, model, artifacts, data, and error, but error and billing semantics are not rich enough for a durable attempt record.
- `tools/cost_tracker.py` performs mutable whole-file reads/writes without coordinator locking, CAS, or atomic publication.
- It persists a top-level `approved_tools` property that is not allowed by `schemas/artifacts/cost_log.schema.json`.
- Backlot consumes checkpoint `metadata.partial_progress` and tool event streams, but ordinary loose artifact precedence can surface unreviewed or stale mixed state.

These remain real canonical-contract gaps, but they do not block the narrowed MVP: MVP does not consume broad/full-run pre-authorization and does not write the existing canonical `cost_log`. It binds an exact per-batch approval/budget in BatchRequest and records estimate/reserved/actual exposure in BatchState/BatchResult. Canonical `approval_policy` and CostTracker migration are post-MVP work; they must not be silently worked around by writing invalid artifacts.

### 2.9 Baseline tests

Two separate categories were verified:

1. **Sandbox harness issue, not a product assertion**
   - Pytest's default `tmp_path` attempted to use `C:\Users\user\AppData\Local\Temp\pytest-of-user`, which this managed sandbox cannot write.
   - This fails during fixture setup before the test body and must not be counted as a Batch/Gemini regression.
   - Supplying a worktree-local `--basetemp` removes this setup failure.

2. **Real product portability/test-isolation failure**
   - With a writable worktree `--basetemp`, the targeted suite produced `39 passed, 1 failed`.
   - The one failure was `test_gemini_omni_status_tracks_google_api_keys`: after environment API keys were removed, the tool still reported `AVAILABLE` because the hard-coded `D:\gcp-keys\...json` exists on this machine.
   - An earlier, broader selected run recorded `67 passed, 1 skipped, 1 failed, 1 subtest passed`, with the same Gemini status assertion as its only product assertion failure. Because its exact file list was not retained, that count is audit context, not the reproducible release baseline.
   - Network permission was not enabled and no provider call occurred.

The repeatable targeted commands were:

```powershell
# Demonstrates the sandbox-only fixture setup failure before the test body.
python -m pytest tests/tools/test_gemini_omni_video.py::test_gemini_omni_inline_data_response_is_handled -q -p no:cacheprovider

# Reproducible product baseline with a writable worktree temp root.
python -m pytest tests/contracts/test_checkpoint_read_gate.py tests/lib/test_checkpoint_prerequisites.py tests/lib/test_checkpoint_noncanonical_stage.py tests/lib/test_gcs_auto_sync.py tests/tools/test_gemini_omni_video.py tests/tools/test_base_tool_dependencies.py --basetemp .pytest_batch_v2_recheck -q
```

The audit shell used Python 3.13.3 and pytest 9.0.2; repository policy currently declares Python 3.10 in `.python-version`. The temp directory was removed after the run. Baseline CI must configure a repository-local pytest temp root, while separately retaining the Gemini credential failure as a product gap until fixed. The release matrix must also run on the repository-declared Python version so the audit interpreter mismatch cannot hide compatibility issues.

### 2.10 Relevant history

- `9d5e22a`: introduced the one-off automated sequence runner.
- `15159f4`: added hybrid Git/GCS media storage to the runner.
- `9cab185`: unified project GCS sync; the runner's undefined `project_id` fallback remains.
- `b970dab`: added GCS ADC fallback.
- `5723386`: added non-blocking GCS auto-sync.
- `a0baea8`: added bounded GCS pool and process-local atomic JSON update.
- `43b66d7`: hardened storage and commit guards.
- `c49d1dd`: documented intra-stage checkpoint progress/resume; it did not add a reusable Batch V2 engine.

The history confirms that legacy behavior should be preserved during migration, then retired by a later ordinary commit only after V2 is proven and merged.

## 3. Goals, scope, and non-goals

### 3.1 Goals

1. Execute an Agent-authored, immutable batch request for exactly one approved pipeline stage.
2. Reduce wall time for I/O-bound provider calls through bounded concurrency without exceeding provider quotas or approved cost.
3. Continue independent items after an item failure and return a complete result inventory.
4. Make interruption and restart safe through durable per-item state, verified same-request result reuse, and explicit ambiguous-call handling.
5. Make local and Cloud Run execution profiles share one code path and one set of contracts.
6. Preserve existing artifact/checkpoint/Human Gate semantics and avoid exposing executor staging as canonical Backlot state, without redesigning Backlot.
7. Support local durable storage and GCS durable storage behind one narrow interface.
8. Provide enough provenance, cost, and structured telemetry for the Agent and user to audit every call.
9. Keep the legacy runner operational until the defined retirement gate.

### 3.2 MVP must complete

MVP is complete only when this bounded slice works end to end:

| MVP area | Required capability | Explicit limit |
|---|---|---|
| Pipeline scope | Execute Agent-authored canonical work items for `assets` only | No stage selection, edit, compose, or cross-stage chaining |
| Initial asset type | Independent video-generation assets needed by the 40-shot use case | Other asset/tool families require an explicit qualified adapter and do not block MVP |
| Process model | One coordinator process with bounded worker threads, default 3 and configured range 1–4 | No multiple executor processes or array jobs |
| Profiles | Same engine under `local` and one Cloud Run Job task | Cloud `task-count=1`, `parallelism=1`, `max-retries=0` |
| Tool identity | Exact concrete tool, provider, API route, model/variant, operation, full inputs, and source digests | One selected provider/route/model per MVP batch; no selector or fallback |
| State/recovery | Durable per-item attempts and `pending/running/staged/committed/failed/indeterminate` state | Resume the same frozen request only; no distributed recovery coordinator |
| Staging/workspace | Tool `output_path` is coordinator-derived under `projects/<project-id>/.batch-v2/runs/<batch-id>/attempts/<item-id>/<attempt-id>/` | Inside configured project root, but outside canonical `artifacts/`, `assets/`, `renders/`, `history/`, and checkpoint paths; Backlot ignores it |
| Writer model | Workers write only their unique project-scoped attempt directory; one coordinator serializes shared state and outputs | Sequential publication only after the execution process stops; no distributed lease system |
| Cloud resume ownership | Durable invocation plus Cloud execution identity; an active owner blocks another execution | Takeover requires trusted prior terminal/cancelled evidence or explicit human resume authorization bound to the prior invocation, then expected-generation CAS |
| Credentials | Standard ADC for GCS and selected Google Cloud provider routes | No hard-coded credential file/project; non-ADC API-key routes must be explicit and secret-injected |
| GCS durability | Synchronous private upload, digest/size/checksum/generation receipt, verified read/head | No background future may satisfy success |
| Canonical state | Complete `asset_manifest` through `validate_artifact`; checkpoint through `write_checkpoint` and validating read | No schema mutation, no automatic Human Gate resolution |
| Safety | Exact approval/budget, typed safe retry, `indeterminate` no replay, secret redaction | No generic provider platform required |
| Packaging | Reproducible non-root container and single Cloud Run Job profile using the same core | No general IaC platform or multi-region support |

The MVP boundary is a release rule: a post-MVP item may become an MVP blocker only when a concrete failing safety/correctness test demonstrates that the bounded design cannot meet an MVP acceptance criterion. Preference for a more general architecture is not sufficient.

### 3.3 Post-MVP enhancements

These are planned follow-on tracks and are not part of MVP Definition of Done:

- renewable distributed leases, fencing tokens, multiple coordinators, Cloud Run array jobs, and multi-region execution;
- cross-file transactions or bundle/current-pointer commits spanning artifact, checkpoint, decision log, and compatibility mirrors;
- broad Backlot UI/state/authority redesign, remote run dashboards, and generalized media resolvers;
- mixed-provider fair scheduling, generic multi-dimensional quota/resource policy, and automatic remote-job reconciliation across providers;
- registry-wide `batch_safe` platform metadata and adapters for every image/audio/video/3D tool;
- cross-batch global cache/index, garbage collection, retention automation, and generalized event sourcing;
- canonical full-run pre-authorization support after `approval_policy` schema reconciliation;
- migration of the existing CostTracker/canonical `cost_log` contract;
- Gemini concurrency above one and provider-wide thread-safety infrastructure;
- reusable IaC, deployment platform, automated SBOM policy, and array-job sharding.

Each follow-on track gets its own approval, tests, and acceptance criteria after MVP. None may be smuggled into MVP through a generic abstraction unless the blocker rule above is met.

### 3.4 Non-goals

- Selecting a pipeline or calculating the next stage.
- Reading a director skill and turning a `scene_plan` into prompts or work items inside Python.
- Creative planning, provider ranking, quality review, or revision decisions.
- Automatic selector use, provider/model fallback, or capability substitution.
- Crossing `assets -> edit -> compose` in one executor invocation.
- Automatically writing terminal pipeline state after execution.
- Distributed scheduling, Cloud Run array jobs, multi-region failover, or Kubernetes.
- Distributed lease renewal/fencing and multi-coordinator ownership.
- Cross-file transactional publication.
- Broad Backlot redesign or a new production dashboard.
- A universal batch platform for every tool/provider/media type.
- Perfect exactly-once semantics for providers that do not expose idempotency/recovery.
- Replacing all existing storage and checkpoint code in the first phase.
- Changing or deleting the legacy runner before migration acceptance.
- Deploying infrastructure or performing paid/live tests without a separate explicit user approval.

## 4. Architectural invariants

These are MVP release-blocking invariants, not preferences:

1. **One stage per batch.** Every request has one `project_id`, `pipeline_type`, and `stage`.
2. **Frozen exact execution.** Every work item names one concrete tool, provider route, model/variant, operation, complete inputs, and output contract.
3. **No creative derivation.** The executor validates; it does not infer missing production choices.
4. **No silent fallback.** A blocked exact tool produces a blocker result.
5. **Authorization before dispatch.** Project identity, checkpoint chain, approval evidence, and cost cap are authenticated before any side effect.
6. **Single coordinator writer.** One process serializes shared execution state; workers never mutate canonical project state or shared control state.
7. **Workspace contract.** Every tool `output_path` stays under the configured `projects/<project-id>/`; attempt staging uses the reserved non-canonical `.batch-v2/runs/.../attempts/...` subtree.
8. **Proven Cloud takeover.** A different Cloud execution cannot dispatch while the recorded owner is active; task topology and elapsed time are not stop evidence. Resume proves stop/authorization before expected-generation CAS.
9. **Durability before success.** Output verification and durable storage receipt precede `committed` state.
10. **Unknown paid outcome is not retryable by default.** Possible acceptance becomes `indeterminate`.
11. **Canonical schemas stay canonical.** Storage locators do not introduce unknown artifact fields.
12. **Human Gates remain human.** Executor completion never implies review or approval.
13. **Profile parity.** Local and single-task Cloud Run differ only in configuration, minimal storage/staging implementations, and identity source.
14. **Legacy coexistence.** V2 writes to a namespaced run area until explicit Agent promotion.

## 5. Responsibility boundary

| Concern | Agent | Batch coordinator | Worker/tool | Human |
|---|---|---|---|---|
| Select pipeline/stage | Owns | Rejects mismatch | None | May direct |
| Read director/provider skills | Owns | None | None | None |
| Create prompts/creative inputs | Owns | Validates presence only | Executes exact input | Reviews at gates |
| Choose tool/provider/model/route | Owns and announces | Resolves exact match; no substitution | Reports actual identity | Approves major changes/cost |
| Build immutable BatchRequest | Owns content | Validates/freezes digest | None | Approval evidence may bind |
| Concurrency/rate scheduling | Sets approved policy bounds | Owns mechanics | Obeys permit | None |
| Retry decision | Defines approved policy and budget | Applies typed safe rules | Returns attempt facts | Re-authorizes ambiguous paid replay |
| Cache/resume | May enable policy | Owns mechanical verification | None | None |
| Technical media validation | Defines output contract | Runs deterministic checks | Produces staged bytes | None |
| Creative/quality review | Owns | Must not perform | Must not perform | Reviews when gated |
| Run journal/storage/cost ledger | Requests | Sole writer | Returns messages only | Audits |
| `in_progress` heartbeat | Authorizes stage run | Sole execution-time physical writer | Never writes | None |
| `awaiting_human` checkpoint | Owns decision after self-review | Sole physical writer of exact Agent command through official writer | None | Reviews |
| `completed/human_approved` | Issues exact command only after a later explicit approval in MVP | Sole physical writer of that command through official writer | None | Supplies gate approval |
| Next pipeline stage | Owns after checkpoint | Must not invoke | None | Gate may allow |

Static and behavioral tests will enforce this table. In particular, the execution engine must not import or call `get_next_stage`, stage director/reviewer logic, selectors, edit/compose render orchestration, or Human Gate decision code. “Agent owns” means the Agent makes and records the semantic decision. During a run, one coordinator process owns all shared writes. After it has durably stopped, publication is a sequential single-writer handoff that persists an exact Agent-authored command; MVP does not implement a renewable distributed lease, fencing token, or concurrent coordinator protocol.

## 6. Proposed architecture

```text
Agent-authored immutable BatchRequest
                |
                v
        Request preflight/authentication
  (schema, project marker, approved checkpoints,
   exact registry identity, budget, input digests)
                |
                v
     Single-process Batch Coordinator  <---->  RunStore / Cost ledger / Events
          |          |          |
          | bounded permits + provider quota
          v          v          v
      Worker 1    Worker 2    Worker 3
          |          |          |
       exact qualified BaseTool adapter
          |          |          |
 project-scoped non-canonical attempt staging only
          \          |          /
           verified result messages
                    |
                    v
     coordinator content-addressed commit
                    |
                    v
       durable BatchResult + storage receipts
                    |
                    v
          status = awaiting_agent_review
                    |
              Agent self-review
                    |
                    v
       immutable PublicationCommand
                    |
                    v
 single publication writer -> validate_artifact + write_checkpoint
                    |
       explicit Human Gate reply, when required
                    |
                    v
 single publication writer -> completed/human_approved=true
```

### 6.1 Proposed implementation layout

No files below are created in this planning phase. The intended layout is:

```text
schemas/execution/
  batch_request.schema.json
  batch_state.schema.json
  batch_result.schema.json
  storage_receipt.schema.json
  execution_owner.schema.json
  execution_status_evidence.schema.json
  resume_authorization.schema.json

lib/batch_executor/
  contracts.py          # schema loading, canonical JSON, digests
  authorization.py      # fail-closed project/checkpoint/approval checks
  engine.py             # coordinator loop only
  scheduler.py          # global + selected-provider bounded permits
  retry.py              # typed classification and approved retry policy
  state.py              # per-item state/attempt persistence and resume
  storage.py            # minimal LocalStore/GCSStore operations
  media_validation.py   # deterministic byte/container checks
  tool_adapter.py       # exact allowlisted adapter and result normalization
  errors.py             # stable error taxonomy
  telemetry.py          # redacted item events and final summary

scripts/batch_execute.py # thin CLI; no planning/orchestration logic
tests/batch_executor/
```

The schema directory is intentionally separate from `schemas/artifacts/`: execution control documents are not pipeline canonical artifacts. Any eventual canonical artifact still uses the existing artifact registry and checkpoint writer.

The MVP layout is intentionally not a generic framework. Multi-provider fairness, generic quota/resource modules, cross-batch cache indexes, append-only event-sourcing infrastructure, distributed coordination, and registry-wide adapter metadata are post-MVP additions only if later requirements justify them.

### 6.2 Execution profiles

| Setting | Local profile | Cloud Run profile |
|---|---|---|
| Engine | Same coordinator package | Same coordinator package |
| Process/task count | 1 process | Cloud Run Job `task-count=1`, `parallelism=1`, `max-retries=0` |
| Default workers | 3 | 3, capped by the exact selected-provider setting |
| Logical project root | Configured projects root plus `<project-id>` (logically `projects/<project-id>/`) | Immutable snapshot materialized as a logical `projects/<project-id>/` workspace under a configured writable job workspace |
| Attempt staging | `<project-root>/.batch-v2/runs/<batch-id>/attempts/<item-id>/<attempt-id>/` | Same logical path inside the materialized Cloud project root; ephemeral bytes are uploaded through GCSStore before commit |
| Durable run store | LocalStore | GCSStore |
| Project source | `OPENMONTAGE_PROJECTS_DIR` plus explicit project ID | Immutable GCS project/request snapshot materialized before preflight |
| GCS identity | ADC or explicit local credential profile | Attached service account via ADC |
| Provider identity | Explicit profile; never hard-coded | Service identity where supported or Secret Manager-injected key |
| Logs | JSONL/file plus console | Structured stdout to Cloud Logging plus durable summary |
| Business behavior | Identical | Identical |

Profiles are declarative configuration. They may constrain limits but cannot change creative inputs, select a provider/model, or alter retry semantics without changing and re-digesting the request.

## 7. Data and contract design

### 7.1 Contract classes

V2 distinguishes three classes of data:

1. **Existing pipeline contracts** — canonical artifacts and checkpoints. Their existing validators remain authoritative.
2. **Execution control contracts** — immutable request, run state, attempt records, result, and storage receipts. These receive dedicated versioned JSON schemas.
3. **Media blobs** — immutable bytes addressed by SHA-256 and referenced by storage receipts.

Execution control records must never be inserted into checkpoint `artifacts` unless they later become a registered canonical artifact. A checkpoint may reference a run by ID/digest inside `metadata`, which the current checkpoint schema permits.

All new execution schemas use a constant version, explicit required fields, `additionalProperties: false` at contract-bearing levels, bounded collections/strings, and semantic validation for relationships JSON Schema cannot express. Unknown fields fail closed rather than becoming implicit behavior.

### 7.2 BatchRequest v1

The Agent authors the semantic content. A persistence helper may validate and serialize it but may not fill creative defaults.

Required fields:

```text
version
batch_id
created_at
project_id
pipeline_type
stage
request_digest
source_revision
source_bindings[]
authorization
execution_policy
work_items[]
```

`source_bindings[]` must include:

- source type and logical path;
- canonical artifact or checkpoint stage/name;
- complete SHA-256 digest;
- checkpoint status and `human_approved` value where relevant;
- CLP binding digest when the pipeline uses CLP;
- immutable storage locator plus generation/version when remote.

`authorization` must include:

- the pipeline-manifest snapshot digest and the complete ordered prerequisite chain for the target stage;
- the immediate predecessor checkpoint plus every applicable human-gated predecessor, each read through the validating checkpoint interface and bound by digest/status/approval evidence (for the initial `assets` scope this includes the approved `scene_plan` chain, not merely the earlier proposal);
- proposal checkpoint/artifact digest and `approval.status` when the selected pipeline has a proposal/cost gate; `approved_with_changes` is valid only when every change is reflected in the frozen request and bindings;
- `approved_budget_usd` or an explicit no-cost declaration;
- applicable decision-log IDs/digests for the exact provider selection and any budget changes;
- one exact allowed tool/provider/route/model identity for the MVP batch;
- maximum total attempts and maximum authorized spend for the batch;
- authorization timestamp and scope.

The executor authenticates this evidence against the current manifest-derived DAG and canonical state. A wrong pipeline DAG, missing/immediate predecessor, unapproved gated predecessor, stale digest, or checkpoint that fails `read_checkpoint` blocks all dispatch. The executor does not create approval evidence. MVP does not interpret broad/full-run pre-authorization; it follows the ordinary per-gate flow and fails closed to `awaiting_human`.

`execution_policy` includes only mechanical controls:

- global worker cap;
- an explicit numeric selected-provider concurrency cap and optional request-spacing/rate bound;
- retry policy version, attempt/time/cost ceilings;
- same-request verified reuse policy;
- failure mode, initially `continue_independent`;
- heartbeat coalescing interval;
- storage profile ID;
- cancellation policy.

Policy cannot name an automatic fallback.

### 7.3 Canonical work item v1

Each work item must include:

- stable `item_id` unique within the batch;
- `scene_id`/asset identity for provenance, not for creative inference;
- exact concrete `tool_name`, tool contract version/revision, provider, route, model/variant, and operation;
- complete normalized tool input object;
- ordered input references with SHA-256, byte size, media type, and immutable locator;
- output specification: logical media kind, expected container/codec constraints, canonical destination intent, and whether audio is expected;
- estimated cost and duration used by budget scheduling;
- explicit safe retry allowance for known charged technical failures, if any;
- optional dependency IDs only for byte dependencies, not pipeline-stage orchestration.

Any omitted output-affecting input is a validation error. The executor does not apply a provider default that could change output invisibly.

The work item may name a canonical destination **intent**, but it cannot supply an arbitrary tool write path. Immediately before execution, the coordinator derives the only permitted tool `output_path` from validated IDs:

```text
projects/<project-id>/.batch-v2/runs/<batch-id>/attempts/<item-id>/<attempt-id>/<output-name>
```

The resolved path must remain beneath the configured and identity-validated project root, after symlink/junction resolution. It must not resolve into `artifacts/`, `assets/`, `renders/`, `history/`, a `checkpoint_<stage>.json` path, the repository root, the process working directory, or a system temp directory. Cloud uses the same logical path after materializing `projects/<project-id>/`; only its physical job-workspace prefix differs.

### 7.4 Digest and identity rules

V2 must not use BaseTool's current 16-hex convenience key as its durable identity.

- Define and version `openmontage-canonical-json-v1` using deterministic UTF-8 JSON, stable object-key order, finite-number rules, and normalized logical paths.
- Compute a full 64-hex SHA-256 work-item digest over all output-affecting fields, tool contract revision, exact route/model, ordered input content digests, source artifact/checkpoint digests, and output validation contract.
- Compute the request digest over the complete request except its own digest field.
- Exclude volatile local materialization paths, signed URLs, access tokens, and timestamps that do not affect output.
- Include `store` or any provider-side persistence setting because it changes side effects/recovery.
- A reused `batch_id` with a different request digest is a hard conflict.
- A tool's observed identity after execution must match the request; mismatch is a contract failure, never silently accepted.

### 7.5 BatchState v1

The MVP state is a revisioned durable snapshot plus per-item attempt records. It contains:

- request identity/digest;
- embedded active ExecutionOwner containing invocation ID, platform execution identity, owner status, state revision, and storage version/generation where applicable;
- the digest/reference of any terminal-execution evidence or human ResumeAuthorization used for ownership handoff;
- lifecycle status/outcome;
- per-item current state and attempt count;
- selected-provider permit/rate summary;
- aggregate estimated/reserved/known actual/indeterminate cost;
- same-request reuse statistics;
- timestamps and last durable attempt sequence;
- links to result and storage receipts.

State must not contain secrets or full prompts by default. A generalized append-only event-sourcing service, renewable distributed ownership lease/fencing token, and global cache index are post-MVP.

### 7.6 Cloud execution ownership and ResumeAuthorization

MVP does not implement a renewable lease, but it does require durable proof that only one Cloud execution may dispatch for a request at a time.

`ExecutionOwner` is embedded in BatchState and contains at least:

- `batch_id` and exact `request_digest`;
- unique executor-generated `invocation_id`;
- trusted Cloud Run execution resource identity/UID plus task identity where available;
- `owner_status`: `active`, `terminal`, or `cancelled`;
- acquisition timestamp and GCS state generation;
- terminal/cancelled evidence digest and observation source when released;
- predecessor owner identity and takeover-proof digest when ownership changed.

An existing `active` owner always blocks a different ordinary `run` invocation. Only an explicitly requested `resume` invocation may attempt the proof-and-CAS handoff below. `task-count=1`, `parallelism=1`, `max-retries=0`, elapsed wall time, missing logs, an old heartbeat, or inability to contact the prior process are **not** proof that the earlier Cloud execution stopped.

Before ownership may move to a new invocation, preflight must validate exactly one of:

1. **Trusted platform evidence:** a minimal ADC-authenticated Cloud Run execution-status verifier identifies the exact recorded prior execution and reports it terminal or cancelled. It persists an immutable, schema-valid `ExecutionStatusEvidence` binding batch ID, request digest, prior invocation ID, execution identity, observed terminal state, observation time, and verifier/source identity. Caller-supplied status JSON without authenticated verification is not trusted evidence.
2. **Explicit human resume authorization:** after the Agent has surfaced the unresolved owner, an immutable `ResumeAuthorization` records the explicit human direction and binds batch ID, request digest, prior invocation ID/execution identity, intended new invocation ID, reason, decision/reply reference, timestamp, and one-time authorization digest.

Only after one proof validates may the explicit resume invocation replace the owner using `save_batch_state(..., expected_generation)`. The successful CAS stores the proof digest and new identity atomically with `owner_status=active`. A failed CAS, mismatched/stale proof, proof for another request/invocation, or unavailable verifier fails closed before any provider dispatch. Normal completion/cancellation changes the application owner record to `terminal`/`cancelled` with expected-generation CAS, but that self-written status alone is not proof that the Cloud Run execution process has stopped; a later execution still needs authenticated control-plane terminal/cancelled evidence or the bound human authorization. This is bounded ownership handoff, not automatic failover, lease expiry, or distributed fencing.

### 7.7 Attempt and error records

Every attempt records:

- batch/item/attempt IDs and idempotency digest;
- exact tool/provider/route/model identity;
- coordinator dispatch sequence;
- timestamps for queued, dispatched, response received, bytes verified, and committed where available;
- acceptance knowledge: `not_accepted`, `accepted`, or `unknown`;
- provider remote operation/interaction ID as soon as it becomes available;
- structured error class, HTTP/provider code, sanitized message, retry-after, and typed retry action;
- estimated, reserved, known actual, and potentially charged amounts;
- output digest/size/probe summary and storage receipt;
- no credential values and no raw provider payload unless explicitly redacted and separately protected.

### 7.8 BatchResult v1

The durable result reports every item, including failures and indeterminate calls. It contains no pipeline approval claim.

Required summary fields:

- request digest and source bindings;
- invocation/execution identity chain and ownership-proof digests used by this run;
- status `awaiting_agent_review` when all safe mechanical work has stopped;
- outcome `all_succeeded`, `partial_failure`, `failed`, `cancelled`, or `indeterminate`;
- successful/cache-hit/failed/blocked/indeterminate/cancelled counts;
- per-item verified storage receipt or structured blocker/error;
- full cost snapshot including retained reserves for indeterminate calls;
- retry/cache/quota statistics;
- Agent-review checklist hints limited to facts, never an automated creative verdict.

### 7.9 StorageReceipt v1

Every committed blob receipt includes:

- `sha256`, byte size, media type, and deterministic probe facts;
- store type;
- local logical path or private `gs://bucket/object` locator;
- GCS object generation and provider checksum when applicable;
- creation time and producing item/attempt IDs;
- encryption/access classification;
- no public or signed URL as durable identity.

### 7.10 Canonical artifact and checkpoint publication

Execution and publication are deliberately separate, sequential single-writer barriers:

1. The coordinator finishes durable media and BatchResult records.
2. The batch enters `awaiting_agent_review`.
3. The Agent inspects outputs using the stage reviewer skill and manifest `review_focus`.
4. The Agent constructs the stage's canonical artifact from reviewed results.
5. The Agent emits an immutable `PublicationCommand` containing the exact `asset_manifest`, review/cost facts, and target `awaiting_human` status for a gated assets stage.
6. Only after the execution process is durably stopped does one publication process take the local run lock or, in Cloud, verify the recorded terminal/cancelled owner evidence and acquire the expected GCS state generation. It enters a scoped V2 context that suppresses every legacy BaseTool/checkpoint background GCS writer.
7. The publication process validates the complete `asset_manifest` with `validate_artifact` and calls `write_checkpoint` with the exact Agent-authorized status. The checkpoint-embedded artifact is the MVP authority.
8. A loose `artifacts/asset_manifest.json` is optional. If compatibility requires it, write it serially after the checkpoint as a digest-identical, rebuildable mirror; startup/resume detects and repairs a mismatched mirror before exposing it.
9. After the later explicit Human Gate reply, the Agent issues a second command and a single publication process writes `completed, human_approved=true` through `write_checkpoint`.

The executor never advances to the next stage. MVP does not claim an atomic transaction across artifact, checkpoint, decision log, or compatibility mirror. It relies on one active writer, official validation, ordered idempotent writes, checkpoint-embedded authority, and restart reconciliation. A transactional bundle/current-pointer protocol and broad Backlot authority redesign are post-MVP.

## 8. Lifecycle and state model

### 8.1 Batch lifecycle

```text
received
   -> validating
   -> ready
   -> running
   -> awaiting_agent_review

validating/ready/running
   -> blocked | cancelled

running
   -> awaiting_agent_review with outcome:
      all_succeeded | partial_failure | failed | indeterminate | cancelled
```

Definitions:

- `received`: bytes exist but are not trusted.
- `validating`: schema, digest, project identity, approval, budget, sources, tool identity, and storage preflight are being checked with no provider side effects.
- `ready`: request is frozen and ownership preflight has succeeded. Local holds the exclusive run lock. Cloud has either conditionally created the first owner or proven the prior owner stopped/was explicitly superseded and then won the expected-generation CAS for the new invocation.
- `running`: at least one item may be queued/dispatched; one coordinator process owns execution writes.
- `blocked`: safe automatic progress is impossible before a configuration, authorization, or ambiguity decision.
- `cancelled`: no new items will dispatch; in-flight calls are reconciled as far as provider semantics permit.
- `awaiting_agent_review`: every item is mechanically terminal and BatchResult is durable. This is not `awaiting_human`.

There is intentionally no executor-owned pipeline `completed` state.

### 8.2 Work-item lifecycle

```text
pending -> eligible -> running
                       |  \
                       |   -> retry_wait -> eligible
                       |   -> indeterminate
                       |   -> failed_terminal
                       v
                succeeded_staged -> committed

verified cache hit ----------------> committed
pending/eligible/retry_wait --------> cancelled
pending/eligible -------------------> blocked_by_dependency
```

- `succeeded_staged` is not durable success; it means worker bytes and facts reached the coordinator.
- `committed` requires media validation, content digest, durable blob receipt, attempt record, and state transition.
- `indeterminate` is terminal for automatic scheduling.
- `blocked_by_dependency` is terminal mechanical non-execution with a structured reason and IDs of failed, cancelled, indeterminate, or already-blocked dependency items; it has no dispatch attempt.
- One item's terminal failure does not cancel independent items.

### 8.3 Attempt phases

Adapters should expose the finest truthful phases possible:

```text
prepared -> dispatched -> provider_accepted -> result_received
         -> bytes_staged -> technically_valid -> durably_committed
```

Not every provider reveals `provider_accepted`. The absence of evidence must not be converted into `not_accepted`. Current synchronous BaseTool providers may require conservative `unknown` classification after dispatch.

### 8.4 Checkpoint progress lifecycle

- Before dispatch, the Agent authorizes a formal `in_progress` assets checkpoint in the immutable request. In the local profile, after full preflight and local run-lock acquisition, the coordinator is the sole process that calls `write_checkpoint` with the `batch_id`/request digest and zero progress.
- In the Cloud profile, a sequential pre-launch publication step writes the official initial `in_progress` checkpoint, then stops before the Cloud task starts. The Cloud task persists per-item progress in GCS BatchState; live remote-to-local checkpoint heartbeat is not an MVP requirement.
- The local coordinator may coalesce item progress into `metadata.partial_progress` through `write_checkpoint`; workers never write it.
- Successful `in_progress` persistence does not replace the separate authorization checks.
- Terminal BatchResult does not itself change checkpoint status. The execution process stops before the later Agent-reviewed publication step begins.
- A storage-aware live Cloud checkpoint backend is a post-MVP enhancement. It must preserve `write_checkpoint` semantics if later added.

## 9. Bounded concurrency and provider quota

### 9.1 Scheduler model

- One coordinator process owns a bounded thread pool for synchronous, I/O-bound tools.
- Initial global default: `max_workers = 3`; valid configured range: 1–4 for the first release.
- MVP batches bind one exact provider/route/model. A work item must acquire the global semaphore, the selected-provider semaphore, and its serialized budget reservation before dispatch.
- Retries re-enter the same queue and do not bypass rate limits.
- Cancellation stops new dispatch and records unresolved in-flight outcomes honestly.
- Process pools, mixed-provider fairness, generic resource permits, and adaptive scheduling are post-MVP.

### 9.2 Provider policy

The MVP selected-provider configuration defines only:

- maximum in-flight calls;
- optional request tokens per interval or minimum spacing when a documented quota is known;
- Retry-After behavior;
- maximum attempts and elapsed time;
- per-attempt and per-batch cost caps;
- whether a durable provider idempotency token or recoverable remote ID exists.

No quota is guessed from historical latency. Unknown paid providers default to one in-flight call and require a reviewed setting before concurrency is raised. Multi-dimensional quota catalogs, adaptive feedback controllers, and multi-provider fairness are post-MVP.

### 9.3 Gemini initial limit

Gemini may remain `max_in_flight = 1` throughout MVP. MVP enablement requires:

1. Developer versus Vertex route/model/auth is explicit and immutable.
2. Vertex, when selected for the Cloud profile, uses ambient ADC without a key file and has explicit project/location.
3. The hard-coded credential path and project fallback are absent.
4. Post-dispatch unknown failures use `indeterminate` and are not replayed.

Raising Gemini to two or three is post-MVP and requires removal of unsafe global DNS/credential mutation, mock concurrency tests, and a separately approved live quota pilot. The global engine may still use three workers when the selected qualified provider permits it.

### 9.4 Future scale

Cloud Run array jobs are considered only after one-task measurements show that one of these is the limiting factor:

- local CPU/memory rather than provider quota;
- more than approximately 100 independent items per batch;
- one-task maximum duration;
- a proven need for multi-provider isolation.

Moving to multiple tasks requires a new distributed lease/fencing and cost-reservation design; it is not a configuration flip.

## 10. Idempotency, cache, and resume

### 10.1 MVP same-request reuse eligibility

A cache hit is accepted only when:

- the full work-item digest matches;
- the tool/provider/route/model and tool contract revision match;
- every input content digest matches;
- the result is in a terminal committed state;
- blob SHA-256 and size match the receipt;
- deterministic technical media probes pass;
- the object generation/version still exists;

File existence or a size threshold is never enough.

For stochastic generation, a reuse hit means reuse of a previously accepted exact result from the same frozen request, not a claim that regeneration would be deterministic. A cross-batch global cache, compatibility catalog, revocation service, and garbage collector are post-MVP.

### 10.2 Content-addressed storage

Local media is first committed beneath the validated project root to an immutable V2 path such as:

```text
projects/<project-id>/.batch-v2/blobs/sha256/<first-two-hex>/<full-sha256>
```

The equivalent private GCS object is namespaced by project and digest. Run/item paths are small references to the blob receipt. Canonical `assets/...` materialization happens only during Agent-approved publication. An existing blob for the same batch/item digest is verified and reused; an existing logical path with a different digest creates a conflict rather than an overwrite. MVP does not build a global cross-project content-addressed service.

### 10.3 Pre-dispatch durability

Before every side-effecting call, the coordinator durably records:

- item and attempt identity;
- exact request digest/tool route/model;
- reserved budget;
- state `running`;
- acceptance knowledge initially `unknown` once dispatch begins.

If this barrier fails, the provider call is not made.

### 10.4 Restart algorithm

On restart, the coordinator:

1. loads and validates the immutable request;
2. creates and records the proposed new `invocation_id`, invocation mode (`run` or explicit `resume`), and, for Cloud, the trusted Cloud Run execution identity;
3. on Local, acquires the exclusive run lock; failure means no dispatch;
4. on Cloud, loads BatchState plus its exact GCS generation and evaluates the current `ExecutionOwner`;
5. if there is no owner, conditionally creates the first `active` owner; if the exact same invocation/execution already owns the state, it may continue only after validating its identity and state generation;
6. if a different owner exists, an ordinary `run` fails closed; only explicit `resume` mode validates trusted terminal/cancelled platform evidence or an explicit human `ResumeAuthorization` bound to that prior owner, this request digest, and the proposed new invocation;
7. only after step 6 succeeds, performs one expected-generation CAS that records the proof digest and makes the new invocation the `active` owner; a CAS loss, missing proof, stale heartbeat alone, elapsed timeout alone, or task topology alone blocks the batch with zero provider calls;
8. verifies the state revision and per-item attempt records;
9. verifies each committed receipt and reconstructs the derived state;
10. requeues `pending`, `eligible`, and expired `retry_wait` items;
11. treats prior `running` attempts according to provider acceptance semantics;
12. reconciles recoverable remote operation IDs before considering a new call;
13. marks possibly accepted paid attempts `indeterminate` when safe reconciliation is unavailable;
14. emits a complete resumed BatchResult without hiding partial failures.

### 10.5 Paid-call ambiguity policy

Automatic replay is allowed only if one of these is proven:

- the failure happened before dispatch;
- the provider explicitly rejected or reported that no operation was accepted;
- the provider honors the same durable idempotency token;
- a durable remote operation ID can be queried and conclusively failed without charge/retry risk.

Otherwise the attempt is `indeterminate`. Its reservation remains in the conservative cost total until reconciled. The Agent explains the state and asks the user before a replacement paid call.

## 11. Retry, backoff, and error taxonomy

### 11.1 Stable error classes

| Error class | Acceptance knowledge | Default action |
|---|---|---|
| `REQUEST_CONTRACT_INVALID` | Not dispatched | Fail item/batch preflight; no retry |
| `PROJECT_IDENTITY_INVALID` | Not dispatched | Block batch; no retry |
| `SOURCE_BINDING_CHANGED` | Not dispatched | Block and require Agent re-plan |
| `APPROVAL_MISSING_OR_STALE` | Not dispatched | Block; no retry |
| `BUDGET_EXCEEDED` | Not dispatched | Block remaining work |
| `TOOL_UNAVAILABLE` | Not dispatched | Block exact item; never fallback |
| `AUTH_CONFIGURATION` | Not dispatched or known rejected | Block provider; no automatic retry |
| `INPUT_MEDIA_INVALID` | Not dispatched | Fail item; no retry |
| `RATE_LIMITED_SUBMIT_REJECTED` | Known rejected before acceptance | Retry a new submit within limits, honoring Retry-After |
| `RATE_LIMITED_REMOTE_POLL` | Accepted with durable remote ID | Retry only the poll/download of that same job; never resubmit generation |
| `RATE_LIMITED_ACCEPTANCE_UNKNOWN` | Unknown | `indeterminate`; do not submit generation again automatically |
| `PROVIDER_TRANSIENT_PRE_ACCEPT` | Known not accepted | Retry within policy |
| `PROVIDER_PERMANENT_REJECT` | Known rejected | Terminal failure |
| `CONTENT_SAFETY_REJECT` | Known rejected | Terminal; Agent decides revision |
| `TIMEOUT_OR_NETWORK_UNKNOWN` | Unknown | `indeterminate`; no automatic replay |
| `REMOTE_JOB_RECOVERABLE` | Accepted | Poll/reconcile same job; do not submit anew |
| `OUTPUT_TECHNICALLY_INVALID` | Accepted/known charged | Retry only if request explicitly authorizes another charged attempt |
| `LOCAL_STORAGE_TRANSIENT` | Provider result already received | Retry storage commit, not generation |
| `GCS_TRANSIENT` | Provider result already received | Retry same blob commit, not generation |
| `GCS_PRECONDITION_CONFLICT` | No new provider call needed | Verify existing object/state; fail closed on digest mismatch |
| `EXECUTION_OWNER_ACTIVE` | Not dispatched | Block the second invocation; no timeout-based takeover |
| `RESUME_OWNERSHIP_PROOF_INVALID` | Not dispatched | Block until exact trusted terminal/cancelled evidence or bound human authorization exists |
| `INTERNAL_BUG` | Depends on phase | Preserve facts; unknown paid phase becomes indeterminate |
| `CANCELLED` | Depends on in-flight state | Stop dispatch; reconcile honestly |

Adapters may add provider codes, but must map them to this stable taxonomy and record the raw sanitized code separately.

### 11.2 Backoff algorithm

- Exponential full jitter: random delay in `[0, min(cap, base * 2^retry_index)]`.
- If the provider supplies `Retry-After`, wait at least that value, bounded by the request's maximum elapsed time. Attempt phase and acceptance knowledge override a generic HTTP class: a post-accept poll/download 429 may retry only the same remote operation, while an acceptance-unknown 429 cannot cause a new generation submit.
- Rate-limit tokens are consumed by every actual attempt.
- Retry ceilings apply simultaneously to attempts, elapsed time, and authorized cost.
- Technical output retries that incur another provider charge require explicit allowance in the immutable request.
- Test code uses an injected fake clock/random source; CI never waits real provider-scale intervals.

Attempt v1 freezes `retry_action` as `none`, `resubmit_generation`, `poll_remote_operation`, `retry_storage_commit`, `reconcile_storage_precondition`, `await_charged_generation_authorization`, `do_not_retry`, or `mark_indeterminate`. `resubmit_generation` is valid only for a known-not-accepted submit. Poll and storage actions can only continue the same remote operation or commit the already-produced bytes. `await_charged_generation_authorization` records a candidate that M1 must still validate against the immutable work-item allowance, attempt ceiling, and budget; it is not dispatch authority. Unknown paid acceptance can only become `mark_indeterminate`.

### 11.3 Failure aggregation

The default batch policy is `continue_independent`:

- terminal failure of one item does not cancel unrelated items;
- dependency-linked items become `blocked_by_dependency` without running;
- systemic authentication, project identity, concurrent-run conflict, storage durability, or budget failures stop new dispatch globally;
- the result enumerates all successes, failures, blockers, and indeterminate attempts.

## 12. Single-writer and commit protocol

### 12.1 Writer ownership

MVP permits exactly one coordinator process per invocation. Local uses an exclusive run lock. Cloud Run fixes `task-count=1`, `parallelism=1`, and `max-retries=0` **within each execution**, but does not treat those settings as protection against another execution of the same request. Cross-execution ownership is enforced by the durable `ExecutionOwner`, validated stop/authorization evidence, and expected-generation CAS described below. MVP has no renewable distributed lease, automatic expiry, heartbeat takeover, or fencing service.

The execution coordinator owns run/progress writes until it durably stops. A later publication invocation begins only after that stop and is the sole writer while persisting the exact Agent-authored command. The Agent owns the semantic decision but does not run a competing writer.

The active coordinator may mutate:

- BatchState and attempt sequence;
- attempt ledger;
- same-request reuse records;
- cost reservations/reconciliation;
- durable storage receipts and logical references;
- canonical media during later publication;
- checkpoint progress;
- canonical artifacts/checkpoints only when authorized by an immutable Agent publication command.

Workers may only:

- read immutable request/materialized inputs;
- write to their unique project-scoped attempt staging directory;
- invoke the exact tool with the coordinator-derived staging `output_path`;
- return immutable result facts/messages to the coordinator.

### 12.2 Cloud ownership acquisition and handoff

The first Cloud invocation conditionally creates BatchState, or fills an owner-null initial state, with its exact `invocation_id`, Cloud Run execution identity, request digest, and `owner_status=active`. A different ordinary `run` execution that observes this owner must fail closed before queueing or dispatching work.

For normal completion or cancellation, the current owner uses expected-generation CAS to persist application status `terminal` or `cancelled` before exiting. A later Cloud execution still verifies that the recorded prior Cloud Run execution itself is terminal/cancelled; the old process's self-written status is not sufficient stop proof. For an abnormal stop that cannot write the transition, the same rule applies. A later invocation cannot infer death from age, missing progress, Cloud task settings, or its own launch. It must be an explicit `resume` and receive one of the Section 7.6 proofs. The minimal authenticated Cloud Run status verifier or the Agent supplies the evidence; the executor only validates the bound facts and mechanically performs the CAS.

The handoff sequence is:

1. load the exact immutable request, BatchState, owner, and GCS generation;
2. require explicit `resume` mode and validate the proposed new invocation/execution identity;
3. verify terminal/cancelled platform evidence for the recorded owner, or validate the one-time human ResumeAuthorization for that owner and proposed successor;
4. reconcile prior in-flight attempt acceptance before allowing any resubmission;
5. CAS the new owner plus proof digest against the previously read generation;
6. re-read and verify that the new owner and generation are durable;
7. only then allow scheduler dispatch.

If two successors race, at most one CAS may win; every loser stops without a provider call. This bounded proof-and-CAS protocol is an MVP safety requirement while renewable leases, fencing tokens, and automated failover remain post-MVP.

### 12.3 Suppressing legacy hidden writers

Every V2 execution **and V2 result-to-artifact/checkpoint publication invocation** must:

- disable legacy `GCS_AUTO_SYNC` behavior even when V2's own GCSStore is configured;
- disable or redirect BaseTool's project event writer and post-success auto-upload in a scoped Batch execution context;
- bypass the terminal `write_checkpoint` legacy async-sync hook for V2 publication metadata, then use the coordinator's synchronous Store commit path instead;
- derive every tool `output_path` beneath `<project-root>/.batch-v2/runs/.../attempts/...`, while keeping it outside canonical directories and checkpoint/history paths;
- prevent workers from calling `write_checkpoint`, `atomic_update_json`, CostTracker persistence, or writing `artifacts/`.

Disabling these behaviors must be scoped to V2 and must not silently break the legacy runner. Integration tests write both `awaiting_human` and `completed` V2 checkpoints and prove that no legacy future is scheduled and no background mutation appears after `write_checkpoint` returns.

### 12.4 Local commit sequence

For one successful attempt:

1. worker closes output in its unique project-scoped attempt directory;
2. coordinator probes media and computes SHA-256/size;
3. coordinator writes an attempt record containing the staged digest;
4. coordinator copies/writes to a unique sibling temporary file beneath the validated project-scoped target filesystem, never system temp;
5. flush and `fsync` the file;
6. verify copied digest;
7. atomically publish with `os.replace` or no-replace semantics as appropriate;
8. `fsync` the parent directory where supported, documenting Windows limitations;
9. persist the storage receipt and state revision;
10. only then set item state `committed`.

Local run ownership uses one OS-level exclusive lock or equivalent; a process-local `threading.Lock` is insufficient. Publication takes the same lock only after execution has stopped. MVP does not implement a renewable lease or fencing token. In Cloud, the durable owner/proof/CAS protocol—not task-count/parallelism/retry settings alone—rejects an accidental second execution and controls resume handoff.

### 12.5 GCS commit sequence

1. upload the content-addressed blob with `if_generation_match=0`;
2. request and verify provider checksum, size, and metadata SHA-256;
3. retain bucket, object name, and immutable generation receipt;
4. write the item attempt record synchronously;
5. update `state.json` with its expected previous GCS generation;
6. only after all durable receipts succeed mark the item committed.

If the blob upload succeeds and the expected-generation state write fails, restart discovers and verifies the blob by digest/generation; it never regenerates merely because the state update failed. This conditional write is an MVP data-integrity mechanism, not a distributed lease service.

### 12.6 Checkpoint publication constraints

- Existing `write_checkpoint` remains the only semantic path for checkpoint construction, schema checks, manifest gates, and prerequisites.
- MVP materializes the project, calls `write_checkpoint`, validates it again with `read_checkpoint`, then synchronously writes/verifies the resulting checkpoint and optional digest-identical artifact mirror through the selected Store. It must not copy gate logic into another implementation.
- The Cloud profile materializes `projects/<project-id>/` first, calls `write_checkpoint` at the normal project checkpoint path, and then performs the synchronous verified GCS write. Calling it in a detached system-temp tree or launching a background upload is not acceptable.
- Terminal artifact/checkpoint status and content remain an Agent decision after review; one sequential publication process is the sole physical writer.
- The checkpoint-embedded `asset_manifest` is MVP authority. A loose file is an optional derived mirror, so two-file atomicity is not claimed.
- MVP crash tests cover the ordered publication boundaries and prove idempotent repair. A transactional bundle/current-pointer spanning checkpoint, decision log, and mirror is post-MVP.

## 13. Security, credentials, and path safety

### 13.1 Identity and containment

- Validate every project ID with `lib.identity.validate_project_id`.
- Resolve local project roots through `resolve_project_dir` and reject symlink/junction aliases or escapes.
- Batch V2 requires an existing, valid `project.json` with matching `project_id` and `pipeline_type`; legacy missing-marker tolerance is not accepted.
- All input/output logical paths are relative, normalized, and checked against their allowed roots.
- Attempt staging and canonical paths are distinct subtrees of the same validated project root. A worker cannot choose its path: the coordinator derives `<project-root>/.batch-v2/runs/<batch-id>/attempts/<item-id>/<attempt-id>/`, and containment is checked after symlink/junction resolution.
- Reject any tool `output_path` outside the configured project root or inside `artifacts/`, `assets/`, `renders/`, `history/`, or checkpoint paths. Only the later Agent-authorized publication step may materialize reviewed media into canonical `assets/`.
- Reject absolute paths, traversal, alternate Windows drive/UNC paths, NULs, and symlink escapes in request-controlled names.
- Subprocess adapters pass argument arrays; no shell interpolation from work-item text.

### 13.2 Credential policy

- No credential path/value is serialized into BatchRequest, logs, state, cache keys, or results.
- Local profile: standard ADC or an explicitly named local credential profile; never a repository or drive-letter fallback.
- Cloud GCS: attached Cloud Run service account through ADC.
- Cloud Vertex/Gemini: `google.auth.default(scopes=...)` plus explicit project/location; no JSON key mounted by default.
- Developer API keys: Secret Manager injection to an environment variable only when that exact route was approved.
- Credential presence may satisfy an approved route, but cannot select or change the route/model.
- Logs redact authorization headers, API keys, signed URLs, raw credential errors, and sensitive prompts.
- CI scans for hard-coded credential paths and likely secrets.

### 13.3 IAM and storage privacy

- Dedicated least-privilege Cloud Run service account.
- Bucket access limited to the selected project/run prefixes where practical.
- The identity performing Cloud resume preflight has only the read permission needed to verify the exact prior Cloud Run execution status, plus the scoped GCS permissions needed for the owner CAS; it cannot accept caller-supplied status as authoritative.
- Private objects by default; no `make_public()` in V2.
- Public delivery, if ever needed, is a separate publish-stage decision.
- Uniform bucket-level access and customer-managed encryption choices are deployment inputs, not hard-coded behavior.
- Object retention/lifecycle rules are documented before a real bucket test.

### 13.4 Supply chain and container

- Pin Python and direct dependencies through a reproducible lock/constraints strategy.
- Explicitly include `google-cloud-storage`; include `ffmpeg`/`ffprobe` only if the technical validator requires them.
- Build from a minimal supported Python base matching repository policy (currently `.python-version` is 3.10).
- Run as a non-root user with read-only application code and one configured writable job workspace containing the materialized logical `projects/<project-id>/`. Worker/tool outputs never use system temp.
- Run the repository's required dependency/security checks before Cloud use. A generalized SBOM/vulnerability-policy pipeline is post-MVP unless existing release policy already mandates it.

## 14. Local/GCS storage abstraction

### 14.1 Store protocol

Both MVP implementations expose the same minimal typed operations:

```text
write_request_if_absent(request_bytes, digest) -> version
load_request(batch_id) -> verified request + version
load_batch_state(batch_id) -> state + version
save_batch_state(state, expected_version) -> new version
put_verified_blob(logical_path, source, sha256, metadata) -> StorageReceipt
get_verified_blob(receipt, destination) -> verified local path
write_result_if_absent(result_bytes, digest) -> version
```

Errors are typed; no method turns a failed durable write into `None` or an empty success.

Generic immutable-record APIs, pointer abstractions, renewable leases, fencing, global indexes, garbage collection, and event-sourcing services are post-MVP.

### 14.2 Proposed namespace

```text
projects/<project-id>/.batch-v2/
  runs/<batch_id>/
    request.json                 # immutable, conditional create
    state.json                   # revisioned owner + item state; GCS generation is the write version
    attempts/<item>/<attempt>/   # tool output_path subtree plus attempt record
    ownership-evidence/<digest>.json
    resume-authorizations/<digest>.json
    outputs/<item>/<sha256>
    result.json                  # immutable terminal executor result
```

The namespace above is relative to the logical project workspace; for GCS it maps to an equivalent private object prefix rather than implying a local filesystem. GCS object names include the validated project ID. LocalStore uses the exact hidden `.batch-v2` subtree inside the configured project root; it does not mirror execution state outside `projects/<project-id>/`.

### 14.3 Durable project/checkpoint integration

Cloud execution starts from an immutable project/request snapshot whose manifest binds all required canonical files and generations. The job first materializes a logical `projects/<project-id>/` beneath its configured writable job workspace, validates its `project.json`, and then derives `.batch-v2/runs/.../attempts/...` inside that project root before dispatch.

The recommended integration path is:

- keep execution-run state in the dedicated V2 store;
- pass every tool an `output_path` inside the materialized project-scoped attempt directory; never use a detached `/tmp`/cwd/repository path;
- have the Agent authorize and sequentially publish the formal initial `in_progress` checkpoint before a Cloud task starts;
- use GCS BatchState, not a new remote checkpoint backend, for Cloud per-item progress during MVP;
- never treat ephemeral local checkpoint bytes as durable success;
- after the job, let the Agent ingest the durable BatchResult and self-review, then issue an exact sequential publication command;
- synchronously upload and verify the validated terminal checkpoint and optional artifact mirror.

A storage-aware live checkpoint backend, distributed current-pointer service, and continuous Backlot progress bridge are post-MVP. They are not required for a real single-task Cloud batch because GCS BatchState is the durable execution record and terminal canonical publication happens after Agent review.

### 14.4 Locator separation

GCS location belongs in `StorageReceipt`/execution provenance, not in current `asset_manifest` or `render_report` unknown fields. Canonical schemas may later add a formally versioned locator field through a deliberate migration, but V2 must not mutate schemas implicitly.

## 15. Cloud Run Job packaging and operation

### 15.1 Image and entrypoint

Proposed dedicated assets:

- `Dockerfile.batch-v2` with pinned Python runtime and dependencies.
- Non-root entrypoint running `python scripts/batch_execute.py run --profile cloud-run --request-uri ...` for first execution or an explicit `resume` command with a proof reference for takeover.
- Image contains no `.env`, credential JSON, project media, or local cache.
- Request URI, bucket, project/location, writable logical-project workspace, worker limit, and selected-provider cap/rate values are supplied as immutable arguments/config.
- The invocation obtains a unique `invocation_id` and a trusted Cloud Run execution identity from the launch contract/platform metadata; neither may be synthesized from batch ID alone.

The CLI remains thin:

1. load profile;
2. establish invocation mode plus unique invocation/Cloud execution identities;
3. resolve request bytes and any explicit resume-proof reference;
4. validate workspace, ownership, request, and provider preflight;
5. invoke the shared engine only after ownership acquisition;
6. return a stable exit code and result locator.

### 15.2 Job shape

- `task-count=1`, `parallelism=1`, `max-retries=0`. These constrain one Cloud Run execution only; they do not authorize a second execution of the same request. Paid-call retry/resume is controlled by durable item state plus the ownership-proof protocol.
- Internal bounded concurrency only.
- Set timeout above the authorized batch worst case, including retry waits.
- Size memory/CPU for the sum of staging buffers, probes, and configured workers.
- Materialize the logical project under one configured writable job-workspace root and create all attempt staging beneath its `.batch-v2/` subtree. Do not pass system-temp paths to tools.
- Attach the dedicated service account.
- Send structured stdout to Cloud Logging.
- On SIGTERM, stop dispatch, persist cancellation intent, reconcile in-flight calls, flush durable state, and exit before the platform deadline where possible.

### 15.3 Preflight

Cloud preflight must fail before provider dispatch when any of these is absent or inconsistent:

- request/schema/digest;
- valid project snapshot and approval/checkpoint bindings;
- a materialized and identity-validated logical `projects/<project-id>/` root plus a derived attempt `output_path` that remains inside `.batch-v2/runs/.../attempts/...` and outside all canonical paths;
- exact qualified adapter/tool version and observed identity contract;
- explicit provider route/model/project/location;
- ambient identity and required scopes;
- bucket access and conditional-write capability;
- storage read-after-write verification;
- a unique invocation ID and trusted Cloud Run execution identity;
- the current `ExecutionOwner` and exact GCS state generation;
- either no prior owner, the exact same valid active owner, or explicit `resume` mode with trusted terminal/cancelled evidence / a schema-valid human ResumeAuthorization bound to the prior owner and proposed successor; an ordinary `run` never takes over;
- successful expected-generation owner acquisition followed by re-read verification; task topology, elapsed time, stale heartbeat, or missing logs alone never satisfies this check;
- budget reservation capacity;
- sufficient capacity in the materialized project-scoped staging workspace;
- disabled legacy background sync/writers.

### 15.4 Stable exit codes

Proposed categories:

- `0`: BatchResult durable; inspect outcome.
- `2`: request/contract/authorization failure before side effects.
- `3`: configuration/auth/storage/ownership preflight blocker.
- `4`: durable result with item failures.
- `5`: durable result with at least one indeterminate paid call.
- `6`: cancellation recorded durably.
- `10`: internal failure; result locator printed if available.

Exit code alone is never the source of truth; the durable BatchResult is.

## 16. Observability and cost governance

### 16.1 Structured telemetry

Every event includes:

- schema version;
- timestamp and monotonic duration where relevant;
- batch, request, item, attempt, project, pipeline, and stage IDs;
- invocation ID, platform execution identity, owner/proof digest, state revision, and attempt sequence;
- exact tool/provider/route/model identifiers;
- lifecycle transition;
- queue wait, provider wait, validation, and storage latency;
- permit/rate-limit state;
- retry class and delay;
- same-request reuse decision;
- estimated/reserved/known actual/potential cost;
- output digest and size, not raw bytes.

Prompts and provider response bodies are omitted from normal logs. A separately protected debug mode may log redacted summaries, never credentials.

### 16.2 Metrics and run summary

MVP minimum metrics:

- total wall time and external wait time;
- active/queued items and maximum observed concurrency;
- throughput for the selected provider/tool;
- per-item/provider/storage latency samples;
- success/failure/indeterminate rates;
- retry and 429 counts;
- same-request reuse hit/miss/corruption counts;
- bytes staged/committed/downloaded;
- estimated versus known actual cost and unreconciled exposure;
- resume count and recovery time.

Local runs write a durable summary plus readable console output. Cloud emits the same event fields to stdout and stores the final summary in GCS.

Cross-run dashboards, generalized p50/p95 aggregation, multi-provider comparisons, and a telemetry platform are post-MVP.

### 16.3 Cost reservation protocol

- The immutable request binds the approved batch cap and per-item estimates.
- Before dispatch, the coordinator serially reserves worst-case authorized cost for the attempt.
- Concurrency cannot oversubscribe the budget because workers never reserve independently.
- On success or known failure, the coordinator reconciles actual cost when reported.
- Indeterminate paid attempts retain conservative reserved exposure.
- Retries consume the same batch cap and explicit attempt allowance.
- Splitting a batch or resuming cannot reset approval or the budget ledger.

MVP keeps this minimal ledger inside BatchState/BatchResult and does not write the existing canonical `cost_log`. Reusing CostTracker requires a later schema-valid migration; the recommended follow-on is to move approval bookkeeping into a defined `metadata` structure or formally version the schema rather than continuing the unknown top-level `approved_tools` property.

### 16.4 Minimal Backlot compatibility

MVP does not add a new Backlot execution dashboard or remote-progress bridge.

- Worker staging and execution drafts live in the reserved project-scoped `.batch-v2/` subtree, outside canonical artifact/media/checkpoint/history paths. Backlot must ignore `.batch-v2/` recursively and must never treat its files as canonical assets or stage artifacts.
- Local runs may continue using existing `metadata.partial_progress`; Cloud per-item progress lives in GCS BatchState until Agent reconciliation.
- The checkpoint-embedded `asset_manifest` is authoritative; an optional loose mirror must be digest-identical or rebuilt before use.
- If an existing loose-manifest precedence rule makes an old manifest override the new Batch V2 checkpoint, the only permitted MVP Backlot change is a narrow assets-specific preference keyed by Batch V2 checkpoint metadata. It must be demonstrated by a failing compatibility test first.
- Showing `awaiting_agent_review`, generalized remote media resolution, new rails, or broad authority refactoring is post-MVP.

## 17. Testing strategy

### 17.1 Test safety policy

Default tests are offline and no-cost:

- keep the existing non-loopback socket guard;
- force a repository/worktree-local pytest `--basetemp` in this managed environment;
- inject clocks, randomness, credentials, registry entries, transports, and storage clients;
- use fake media bytes or tiny locally generated fixtures;
- never read developer machine credential paths;
- mark all external tests and require both an explicit marker/flag and a separate user approval.

Suggested markers:

- `unit` / default: no network.
- `container`: local image only, fake tools.
- `real_gcs`: external writes; user approval required.
- `paid_api`: provider may charge; user approval required.
- `cloud_run`: deploys or runs cloud resources; user approval required.

Existing `live_api` protection remains; subprocess/network tests need an additional explicit no-network environment because Python socket monkeypatching does not constrain child processes.

### 17.2 Mandatory MVP mock/fake, no-paid test matrix

Every test in this table is an MVP gate and must pass without real credentials, GCS, Cloud Run, or provider calls.

| Area | Required scenarios | MVP acceptance |
|---|---|---|
| Request schema/digest | valid/invalid request, unknown fields, key order, paths, full input digests | Stable full SHA-256; fail before tool resolution |
| Request conflict | same `batch_id`, different digest or selected identity | Hard conflict; provider call count zero |
| Project/source identity | traversal, symlink/junction, missing marker, changed checkpoint/artifact/input digest | Rejected before any side effect |
| Workspace/output path | local and Cloud-materialized project roots; absolute/traversal/junction paths; attempts to target repo/cwd/system temp or canonical directories | Every fake tool receives only `<project-root>/.batch-v2/runs/<batch>/attempts/<item>/<attempt>/...`; invalid path yields zero calls |
| Gate/authorization | wrong DAG, unapproved/stale `scene_plan`, invalid checkpoint, stale budget | Complete assets prerequisite chain validates; no dispatch otherwise |
| Exact adapter identity | tool missing/version mismatch, observed provider/route/model mismatch, alternative available | Exact match only; selector/fallback call count zero |
| Worker isolation | fake tool writes only its supplied unique project-scoped attempt path | Worker shared/canonical write count zero; all outputs remain outside `artifacts/`, `assets/`, `renders/`, `history/`, and checkpoints |
| Bounded concurrency | deterministic blocking fake at W=1..4 plus selected-provider cap | Observed calls never exceed either cap |
| Minimal rate control | fake clock, request spacing, submit 429 and Retry-After | Selected-provider limits exact; no real sleep |
| Retry phase | submit-rejected, post-accept poll/download, acceptance-unknown, 5xx/auth/permanent failure | Only safe phase retries; generation submit stays one after acceptance |
| Paid ambiguity | crash/timeout before dispatch, during submit, after remote ID, during download | Unknown acceptance becomes `indeterminate`; no automatic replacement call |
| Partial failure | mixed success/failure/blocked/indeterminate independent items | Remaining independent items continue; result lists every item |
| Budget | concurrent attempts near cap, resume, indeterminate exposure | Serialized reservation never exceeds the exact approved cap |
| Same-request reuse | changed prompt/model/route/duration/store/reference digest; corrupt/missing output | Only exact verified committed result is reused |
| Local persistence | exclusive lock, atomic state replace, corrupt state, restart at key item boundaries | Second local invocation rejected; truthful resume without lost item state |
| Fake GCS | private synchronous upload, `if_generation_match=0`, size/checksum/SHA/generation, transient error | No `committed` before verified receipt; typed failures |
| GCS crash recovery | upload succeeds then state write fails; state generation conflict; corrupt download | Resume reuses verified blob and never regenerates solely for storage failure |
| Cloud first-owner acquisition | two fake Cloud executions start the same request concurrently | Exactly one expected-generation CAS wins; loser records `EXECUTION_OWNER_ACTIVE` and provider call count stays zero |
| Cloud resume ownership proof | ordinary run versus explicit resume; prior owner active/terminal/cancelled; authenticated exact/mismatched platform evidence; untrusted caller JSON; exact/stale/wrong-request human authorization; CAS race | Ordinary run blocks; resume dispatches only after exact stop/authorization proof and successful owner CAS; self-written status/topology/age/heartbeat/log silence never count as stop proof |
| Owner release/recovery | normal terminal/cancelled release, crash before release, proof verifier unavailable | Normal release is generation-bound; crash remains active until trusted evidence or explicit bound authorization; unavailable evidence fails closed |
| Checkpoint progress | formal local `in_progress`; Cloud BatchState progress | Official writer locally; workers never write checkpoints |
| Canonical publication | valid/invalid `asset_manifest`, `awaiting_agent_review`, later gate reply | `validate_artifact` + `write_checkpoint` + validating read; executor never resolves gate |
| Hidden writer suppression | BaseTool and terminal checkpoint legacy auto-sync otherwise enabled | No legacy future and no post-return `gcs_url` mutation |
| Minimal Backlot visibility | `.batch-v2/` staging/draft plus optional old loose manifest | Backlot ignores `.batch-v2/` recursively; narrow fix only if a test proves stale loose precedence |
| ADC/credential isolation | no creds, fake ambient ADC, explicit fake API-key route, hard-coded path probe | No developer path/project leakage; auth cannot alter route/model |
| Output validation | empty/truncated/wrong container/duration/audio facts | Invalid bytes never become committed |
| Redaction | secret-shaped headers/errors/signed URLs/prompt data | No secret in state/result/log output |
| CLI/profile parity | local and cloud-profile fake success/failure/cancel plus Cloud owner-block/explicit-resume; Cloud task retry config zero | Same semantic result and stable exit codes, including ownership preflight blocker |
| Container smoke | Linux non-root/read-only app, writable materialized `projects/<project-id>/`, project-scoped staging, FakeGCS | Same request digest/state/ownership semantics as local; no tool output uses system temp |
| Performance harness | 40 fake 46-second-equivalent waits | Meets bounded-concurrency target without network/cost |

The fake provider exposes counters, barriers, scripted acceptance phases, remote IDs, charges, and key crash points. FakeGCS models object generations, checksums, and precondition failures rather than merely returning URLs.

### 17.3 Post-MVP mock/fake matrix — not an MVP gate

| Follow-on area | Deferred tests |
|---|---|
| Distributed ownership | renewable lease, fencing token, automatic coordinator failover, multi-task/region contention beyond the MVP proof-and-CAS handoff |
| Cross-file transaction | atomic bundle across decision log/artifact/checkpoint/mirror; current-pointer recovery |
| Broad Backlot | new `awaiting_agent_review` UI, remote progress/dashboard, generalized authority rules |
| Generic provider platform | mixed-provider fairness, multi-dimensional quota/resource policies, universal `batch_safe` support envelope |
| Generic storage/cache | cross-batch global index, event sourcing, GC/retention, multi-project deduplication |
| Expanded providers/media | image/audio/3D adapter conformance and provider-independent remote-job reconciliation |
| Gemini parallelism | concurrent ADC refresh/DNS path before raising Gemini above one |
| Full-run authorization/cost log | `approval_policy` schema and canonical CostTracker migration |
| Distributed Cloud | array jobs, multi-region, task retry/failover behavior |

### 17.4 Real tests requiring separate explicit user approval

None of these are authorized by approval of this Plan alone.

| Track | Test | External effect/risk | Required approval payload |
|---|---|---|---|
| MVP qualification | Real GCS integration | Creates/reads cloud objects | Project, bucket, prefix, region, IAM identity, retention/cleanup plan |
| MVP qualification | Cloud image push | Creates registry artifact and may incur storage | Project/region/repository/image tag |
| MVP qualification | Cloud Run fake-tool job | Deploys/runs cloud resources without provider spend | Project/region/service account/resources/max runtime, execution count, exact owner-block/resume-proof scenarios, cleanup |
| MVP qualification | Real provider single sample | May charge and store provider-side data | Exact tool/provider/route/model, prompt/input class, duration, max USD, retention setting |
| MVP qualification | Real provider concurrency pilot | Multiple charges/quota impact | Item count, W1/W2/W3 comparison plan, max attempts, total max USD |
| Optional benchmark | Full 40-shot benchmark | Material spend and time | Exact frozen request, reuse policy, provider quota, total cap, stop conditions |
| Optional combined qualification | Cloud Run real-provider job | Deployment plus paid API and durable data | All Cloud and provider details plus combined max cost |
| Post-MVP only | Public/signed delivery test | Changes access exposure | Exact objects, access duration, audience, rollback |

Approval is obtained immediately before each test tier. A single-sample gate precedes any live batch. A failed or ambiguous live call does not authorize an extra replacement call.

### 17.5 Platform matrix

| Platform | Offline required | External optional with approval |
|---|---|---|
| Windows local | Unit, LocalStore, fake provider, path/junction, resume | Provider/GCS local profile |
| Linux CI | Unit, LocalStore, fake provider, schema/digest parity | None by default |
| Local container | Fake end-to-end, non-root, signal handling | Real GCS only if approved |
| Cloud Run Job | — | Fake job first, then real GCS, then provider; each separately approved |

## 18. Performance baseline and targets

### 18.1 Baseline decomposition

| Metric | Baseline |
|---|---:|
| Items | 40 shots |
| Total wall | 33.6 min / 2,016 s |
| External generation wait | 30.7 min / 1,842 s |
| Other serial overhead | about 2.9 min / 174 s |
| Mean external wait | about 46.05 s/item |
| External-wait share | about 91.4% |

Ignoring quota, skew, and retry, the theoretical lower bounds using the historical external-wait total are:

| Workers | External lower bound | Total with unchanged 174 s overhead | Theoretical total speedup |
|---:|---:|---:|---:|
| 1 | 30.70 min | 33.60 min | 1.00x |
| 2 | 15.35 min | 18.25 min | 1.84x |
| 3 | 10.23 min | 13.13 min | 2.56x |
| 4 | 7.68 min | 10.58 min | 3.18x |

These are capacity bounds, not promises; real provider quota and latency distribution may dominate.

### 18.2 Offline performance acceptance

- 40 fake items with the historical latency distribution or a 46-second-equivalent scaled clock.
- W=3 observed active calls never exceed three or provider limits.
- Scheduler/control overhead adds no more than 5% to fake critical-path time, excluding configured rate waits.
- W=3 achieves at least 2.5x throughput over W=1 in the unthrottled fake benchmark.
- One failed item does not materially delay unrelated items beyond permit/retry policy.
- Resume scans and reconstructs a 40-item run in under 5 seconds on supported local hardware.
- State/event growth remains bounded and no checkpoint write occurs once per worker thread; progress is coalesced by the coordinator.

### 18.3 Approved live performance acceptance

The first approved live pilot compares cold-cache W=1 and qualified bounded concurrency using the same exact provider route/model and comparable inputs.

- Start with a minimal single sample.
- Then use 6–10 items, raising concurrency one step at a time.
- Target at least 1.8x wall-time improvement at the first qualified parallel setting without a higher terminal-error rate or any unapproved cost.
- Record 429/retry/latency/cost data rather than tuning blindly.
- Zero duplicate provider submissions caused by local/GCS state failures.
- A separately approved full 40-shot benchmark has a capacity target of at most 15 minutes at W=3 when provider quota and retry-free conditions permit. It is optional evidence, not an MVP completion gate; if run, publish the measured quota-limited result rather than weakening safety controls.

Correctness, cost safety, and truthful ambiguity handling take precedence over the speed target.

## 19. Phases, milestones, and acceptance criteria

This revision remains planning-only. M0 begins only after the coordinating main task accepts this revision and schedules the offline phase under the user's delegated M0–M4 authority. M0–M4 are the sequential, no-cost gates for an **MVP code-complete** result. M5 contains external qualification tiers that always require fresh, test-specific user approval. Post-MVP tracks are deliberately excluded from every M0–M6 acceptance gate unless a concrete failing MVP safety/correctness test proves one is indispensable.

### M0 — Freeze the MVP contracts and safety specification

Deliverables:

- versioned BatchRequest, BatchState, BatchResult, attempt, storage-receipt, ExecutionOwner, ExecutionStatusEvidence, and ResumeAuthorization schemas for the `assets` video-generation slice;
- canonical digest and exact tool/provider/route/model binding rules;
- an explicit MVP support declaration and allowlisted adapter contract for one selected concrete tool/provider/route/model; no environment-derived route choice;
- a deterministic workspace-path contract that derives tool `output_path` beneath the project-scoped non-canonical `.batch-v2/runs/.../attempts/...` subtree for both profiles;
- Cloud ownership rules that bind invocation/execution identity, trusted terminal/cancelled evidence, one-time human resume authorization, and expected-generation takeover CAS;
- a narrow ADC-authenticated Cloud Run execution-status verifier contract; caller-provided status text is never authoritative;
- test-first Agent-Native, authorization, workspace containment, ownership, hidden-writer, ambiguity, validation, and credential-isolation cases.

Acceptance criteria:

- a fake tool cannot be reached without valid project/source/gate evidence, budget, and exact execution identity;
- an unavailable or mismatched identity fails before dispatch and invokes no fallback;
- the selected MVP adapter identity is recorded before its implementation begins and is not inferred from ambient credentials;
- responsibility tests prove the engine has no stage choice, prompt derivation, creative review, selector, or Human Gate decision behavior;
- schema/semantic validation rejects a tool path outside `projects/<project-id>/`, inside a canonical path, or outside the exact attempt subtree;
- schema/semantic validation rejects an owner takeover without exact prior-owner stop evidence or explicit prior-owner-bound human authorization, before any provider dispatch;
- an ordinary `run` encountering any different recorded owner fails closed; only an explicit `resume` invocation can present takeover proof;
- existing canonical artifact/checkpoint validation remains green;
- no network or real credential is used.

### M1 — Local single-process executor

Deliverables:

- one coordinator process, bounded worker threads with default W=3 and range W=1–4;
- project-scoped non-canonical attempt staging, typed retry/backoff, cancellation, and selected-provider quota controls;
- durable per-item lifecycle, attempt journal, budget reservation, same-request reuse, and resume in LocalStore;
- an OS-level exclusive local run lock and scoped suppression of hidden project/GCS/event writers;
- scripted fake provider and deterministic media validation.

Acceptance criteria:

- a complete fake assets batch runs locally and BatchResult accounts for every item;
- barrier/counter tests prove concurrency never exceeds global or selected-provider limits;
- a second local coordinator is rejected by the run lock;
- every fake tool receives only the coordinator-derived `<project-root>/.batch-v2/runs/<batch-id>/attempts/<item-id>/<attempt-id>/...` output path, with canonical and out-of-project targets rejected;
- crash tests at every local state/output boundary resume the same frozen request without duplicate accepted work;
- an acceptance-ambiguous paid attempt becomes `indeterminate` and is never auto-replayed;
- workers cannot mutate shared state, canonical artifacts, checkpoints, cost files, or event streams;
- the 40-item fake performance targets pass.

### M2 — Canonical assets publication and checkpoint lifecycle

Deliverables:

- an Agent-authored PublicationCommand that binds the exact BatchResult digest and canonical `asset_manifest`;
- sequential single-writer publication after the execution process has stopped;
- `schemas.artifacts.validate_artifact()` and official `write_checkpoint()`/read validation on every canonical write;
- canonical lifecycle integration for official `in_progress`, Agent review, `awaiting_human`, and later explicit-human-approved `completed` states;
- at most a narrow assets-specific Backlot compatibility fix, and only if a failing regression proves it necessary.

Acceptance criteria:

- execution success alone stops at `awaiting_agent_review` in BatchState and cannot publish `awaiting_human` or `completed`;
- after Agent review, a gated assets stage publishes `awaiting_human`; only a later explicit human reply can publish `completed` with `human_approved=true` in MVP;
- every canonical manifest and checkpoint round-trips through existing validators and official readers;
- one publication process owns all canonical mutations and workers/legacy background hooks cannot write after return;
- checkpoint-embedded artifact authority is written before any optional, serial, rebuildable loose mirror;
- ordered idempotent crash repair is proven without claiming a cross-file transaction or redesigning Backlot.

### M3 — Minimal GCS durability and the single-task Cloud profile

Deliverables:

- the minimal GCSStore operations defined in Section 14, using private content-addressed outputs and expected-generation state writes;
- synchronous upload completion plus size, client SHA-256, GCS checksum, object generation, and metadata verification before an item becomes committed;
- one shared engine exposed through Local and Cloud profiles;
- one production assets-video adapter for the M0-selected exact route/model, covered with a fake transport and exact observed-identity assertions;
- a reproducible non-root container and a Cloud Run Job definition/runbook fixed to `task-count=1`, `parallelism=1`, and `max-retries=0`;
- durable Cloud ExecutionOwner acquisition/release plus proof-gated resume takeover using expected GCS generation CAS;
- the minimal ADC-authenticated Cloud Run status verifier used only to prove the exact previous execution is terminal/cancelled;
- a materialized logical `projects/<project-id>/` workspace whose attempt staging uses the same relative path and containment rules as Local;
- service identity/ADC for GCS and Vertex/Gemini; no machine path, implicit project fallback, or baked credential;
- pinned runtime dependency required by the supported Cloud path.

Acceptance criteria:

- FakeGCS generation/checksum/precondition tests and the LocalStore/GCSStore MVP conformance suite pass;
- upload-success/state-write-failure recovery verifies and reuses the existing blob rather than regenerating it;
- a state-generation conflict fails closed and is not treated as a renewable lease/failover protocol;
- an active prior Cloud owner blocks a second ordinary execution; topology, elapsed time, self-written terminal status, stale heartbeat, missing logs, or untrusted status JSON cannot authorize takeover;
- resume dispatch occurs only after exact trusted terminal/cancelled evidence or a one-time human ResumeAuthorization bound to the prior and proposed invocations is validated, the owner CAS wins, and the new owner is re-read successfully;
- concurrent successor tests prove one CAS winner and zero provider calls from every loser or insufficient-evidence invocation;
- success cannot be returned before synchronous GCS verification, and no background upload remains in the success path;
- the local container completes the fake 40-item request with both LocalStore and FakeGCS;
- Local and Cloud profiles produce the same request digest, per-item transitions, result semantics, and exit codes;
- the image contains no secret or bundled project media; at runtime it writes worker/tool output only under the configured materialized project workspace and persists durable records through GCSStore;
- no real deployment, GCS mutation, or provider call is required for this phase.

### M4 — Offline MVP release gate

Deliverables:

- the complete Section 17.2 mock/fake suite on Windows, repository-version Linux CI, and the local container;
- reproducible baseline classification with repository-local writable pytest temp storage;
- implementation diff, Agent-Native self-review, security/cost review, migration runbook, and rollback rehearsal.

Acceptance criteria:

- all mandatory MVP mock/fake tests pass with no expected failure and no network/credential access;
- the earlier sandbox temp-path failures are absent under the documented writable temp root;
- the Gemini hard-coded credential/project/DNS product gap is fixed by injectable ADC-based resolution and is not suppressed;
- no post-MVP capability is used to waive an MVP failure; if one proved indispensable, the Plan records the failing test and a narrowly justified scope amendment first;
- the legacy runner remains unchanged and callable.

### M5 — Separately approved external qualification

Each tier is separately optional until the user supplies its exact approval payload; Plan approval grants none of them:

1. real GCS prefix test;
2. container image push;
3. Cloud Run fake-provider job;
4. one-item real-provider sample;
5. 6–10 item bounded-concurrency pilot;
6. optional full 40-shot or combined Cloud/provider benchmark.

Acceptance criteria for any tier that is authorized:

- the recorded approval fixes project/region/identity/route/model, scope, attempts, retention, cleanup, and cost/time cap as applicable;
- exact announced route/model equals the observed attempt record;
- GCS objects are private, checksummed, generation-bound, synchronously verified, and resumable;
- Cloud uses attached service identity/ADC with `task-count=1`, `parallelism=1`, and `max-retries=0`;
- an approved Cloud fake-provider tier confirms the materialized project-scoped staging path, active-owner rejection across separate executions, authenticated terminal-status verification, and proof-before-CAS resume behavior;
- no storage/retry failure causes a duplicate accepted paid call;
- any indeterminate outcome stops escalation until the Agent reports it and the user gives new direction.

An MVP may be declared **code-complete** and merged opt-in when M0–M4 pass even if the user withholds external-test approval. It may not be called production-qualified for the affected Cloud/provider route, and the legacy runner may not be retired, until the relevant M5 evidence passes.

### M6 — Merge and opt-in coexistence

Deliverables:

- reviewed, phase-aligned implementation commits and final offline evidence;
- opt-in V2 command/profile and migration/rollback documentation;
- normal merge to `team-main` while preserving the legacy runner.

Acceptance criteria:

- Section 22.1 MVP code-complete criteria pass on the candidate commit;
- a post-merge offline/fake run and recovery exercise succeeds;
- any post-merge external execution obtains fresh run-specific approval rather than reusing M5 approval;
- baseline tag and normal Git recovery remain intact;
- retirement is a later, explicit, separate commit and follows Section 22.4.

### Post-MVP enhancement tracks — not M0–M6 gates

1. **Distributed execution:** renewable leases, fencing, coordinator failover, Cloud Run array jobs, multi-region operation, and distributed cost reservation.
2. **Transactional publication:** a bundle/current-pointer transaction across artifact, checkpoint, decision log, and compatibility mirrors.
3. **Broad Backlot evolution:** remote execution progress, new UI states, generalized artifact authority/resolver rules, and wider Backlot refactoring.
4. **Generic executor platform:** mixed-provider fairness, multi-dimensional quotas, universal adapter metadata, all media families, generic storage/event sourcing, global cache/index, GC, and multi-project reuse.
5. **Canonical contract convergence:** full-run `approval_policy` schema support and migration to a schema-valid shared CostTracker/`cost_log` model.
6. **Operational hardening:** expanded dashboards/SLOs, generalized SBOM policy, automated infrastructure lifecycle, and larger live capacity programs.

Each track receives its own proposal, tests, risk review, and approval. Architectural preference or future scale is not evidence that a track blocks the MVP.

## 20. Migration and rollback

### 20.1 Migration sequence

1. Keep `scripts/batch_run_intent_sequences.py` unchanged and available.
2. Introduce V2 behind an explicit command/profile; no default pipeline routing change.
3. Convert the historical 40-shot definitions into schema-valid, no-media test fixtures. Do not rewrite historical project truth in place.
4. Run request validation and fake-tool shadow execution against copied/test project roots.
5. Compare expected item mapping, outputs, costs, and checkpoint progression without provider calls.
6. Complete M0–M4 and merge V2 to `team-main` behind opt-in routing after review; lack of external-test permission does not justify faking production qualification.
7. When separately approved, perform M5 qualification in a new project/run namespace with exact route/model and cost/time caps.
8. Observe at least one offline/fake representative merged V2 run and recovery path. If this observation uses real GCS, Cloud Run, or a provider, obtain a new immediate approval payload for that exact run; an earlier M5 approval is not reusable.
9. Retire the legacy runner by a separate ordinary commit only after the relevant MVP route is production-qualified and the user explicitly confirms retirement.

### 20.2 Rollback

- Disable V2 opt-in routing/configuration.
- Continue using the untouched legacy runner during the coexistence window.
- Preserve V2 run namespaces and receipts for audit; do not mutate canonical artifacts during rollback.
- Revert individual V2 integration commits normally if required; do not rewrite shared history or remove the safety tag.
- If retirement has already merged, restore the legacy runner through a normal revert/cherry-pick from Git history, not a destructive reset.
- GCS rollback disables the V2 profile/configuration; immutable blobs and receipts remain until an approved lifecycle policy removes them.

### 20.3 Compatibility constraints

- Legacy auto-sync stays available outside V2 until separately migrated.
- V2's suppression of legacy writers must be execution-context scoped.
- Existing checkpoint/artifact versions stay readable.
- New MVP control contracts are versioned independently; a breaking revision requires a migration reader before adoption.
- Mixed local/GCS authority for the same batch is forbidden; one profile/store owns a batch ID.
- Post-MVP distributed, transactional, generic-platform, or broad Backlot work is not pulled into a rollback patch unless a demonstrated MVP correctness defect requires a narrowly reviewed fix.

## 21. Risks and mitigations

| Risk | Impact | Mitigation / release gate |
|---|---|---|
| Python drifts into orchestration | Violates core architecture and hidden creative behavior | Static responsibility tests; one-stage immutable request; Agent-only promotion/gates |
| False cache hit | Wrong clip attached to a scene | Full digest, source bindings, media probe, immutable receipt/generation |
| Paid duplicate after timeout/crash | Unexpected spend and duplicate assets | Pre-dispatch journal; accepted/unknown phase; `indeterminate` no-auto-replay |
| Provider quota burst | 429s, bans, low throughput | Global plus selected-provider permits/rate limit, Retry-After, provider-specific qualification |
| Gemini global-state race | Credential/DNS instability | Cap=1 until global mutation removed and concurrency tests/live pilot pass |
| Hidden GCS/event writer | Lost updates and premature publication | Scoped suppression; workers confined to the project-scoped non-canonical attempt subtree; coordinator-only persistence |
| GCS upload acknowledged too late | Cloud task exits with lost result | Synchronous receipt barrier, checksum, generation, no background success path |
| Accidental second Cloud execution | Duplicate paid calls or split ownership | Durable invocation/execution identity; active-owner rejection; trusted stop or bound human authorization; one-winner expected-generation CAS; task settings are defense-in-depth only |
| False Cloud takeover from stale heartbeat/timeout | Live execution is superseded | Neither age nor silence is proof; fail closed until exact trusted terminal/cancelled evidence or explicit prior-owner-bound human authorization exists |
| Schema-invalid `gcs_url` mutation | Checkpoint/read failure and Backlot inconsistency | Locator sidecar; schema validation after every publication |
| Backlot loose-artifact precedence | New artifact shown with old approval | Keep staging outside canonical paths; checkpoint authority; allow only a failing-test-driven assets-specific fix |
| Cost race or invalid canonical cost log | Budget oversubscription or invalid canonical state | Coordinator-owned MVP reservation ledger; do not write canonical `cost_log`; migrate post-MVP |
| Approval evidence mismatch | Spend without valid consent | Fail-closed binding to manifest-derived prerequisite checkpoints, proposal where present, and decision digests |
| `approval_policy` enum mismatch | Broad/full-run approval cannot be consumed canonically | MVP uses normal per-gate human reply; reconcile schema post-MVP |
| Machine-specific credentials | CI and Cloud behave differently | Injectable resolver; standard ADC; remove hard-coded paths/project |
| Missing Cloud dependency | Image fails at runtime | Pinned dependency/container smoke test |
| Path traversal/symlink alias | Read/write outside project | Shared identity resolver and per-path containment tests |
| Provider/model drift | Announced path differs from actual call | Freeze observed route/model; preflight mismatch fails |
| Ordered cross-file publication is interrupted | Optional mirror or decision history may lag checkpoint | One stopped execution process, one publication writer, checkpoint-embedded authority, idempotent restart repair; transactional bundle is post-MVP |
| Performance target conflicts with safety | Unsafe concurrency/retries | Correctness/cost gates precede speed; provider cap raised only with evidence |
| MVP scope expands into a platform rewrite | Delayed delivery and new failure modes | M0–M6 scope gate; require a concrete failing MVP test before promoting any post-MVP capability |

## 22. Definition of Done

### 22.1 MVP code-complete — required for opt-in merge

- [ ] Scope is limited to schema-valid `assets`-stage independent video-generation work items.
- [ ] One shared engine powers Local and single-task Cloud Run profiles; Python does not choose stages, create prompts, review creatively, select fallbacks, or resolve Human Gates.
- [ ] Each immutable BatchRequest binds one exact tool/provider/route/model identity, and the observed adapter identity must match before dispatch.
- [ ] One process provides bounded concurrency (default W=3, supported W=1–4) with selected-provider rate/quota controls.
- [ ] Every item has durable state, attempt phase, receipt, error classification, budget exposure, and restart behavior; acceptance-ambiguous calls become `indeterminate` and are not auto-replayed.
- [ ] Every tool `output_path` is coordinator-derived beneath `projects/<project-id>/.batch-v2/runs/<batch-id>/attempts/<item-id>/<attempt-id>/`; Local and Cloud-materialized workspaces enforce the same post-resolution containment, and workers cannot target canonical paths, the repository/cwd, or system temp.
- [ ] Backlot ignores the `.batch-v2/` subtree and never presents its staging or execution records as canonical.
- [ ] One coordinator serializes shared execution state. Local uses an exclusive run lock. Cloud records exact invocation/execution ownership; `task-count=1`, `parallelism=1`, and `max-retries=0` do not replace cross-execution ownership checks.
- [ ] A second ordinary Cloud execution fails closed while another owner is recorded. Explicit resume requires ADC-authenticated terminal/cancelled evidence for the exact prior Cloud Run execution or one-time explicit human authorization bound to the prior and proposed invocations, then a successful expected-generation owner CAS and re-read, before dispatch; self-written status or caller JSON alone is insufficient.
- [ ] Same-request reuse verifies the full identity digest, media bytes/probe, and storage receipt; no global or cross-project cache service is required.
- [ ] LocalStore and the minimal GCSStore pass the MVP conformance suite.
- [ ] GCS output writes are private, content-addressed, synchronous, generation-bound, and verified by size, client SHA-256, GCS checksum, generation, and metadata before commit.
- [ ] GCS and the supported Vertex/Gemini route use attached service identity/ADC with no hard-coded credential path or implicit project fallback.
- [ ] Canonical `asset_manifest` publication passes `validate_artifact`; checkpoints use the existing official writer/reader and validate after write.
- [ ] Execution success stops at BatchState `awaiting_agent_review`; after Agent review the assets gate uses `awaiting_human`, and only a later explicit human reply permits `completed` with `human_approved=true`.
- [ ] Canonical publication begins only after execution stops and has one writer; hidden legacy/background writers are suppressed in V2 scope and no mutation occurs after return.
- [ ] Interrupted ordered publication is idempotently repairable with the checkpoint-embedded artifact as authority; no cross-file transaction is claimed.
- [ ] The container is reproducible, pinned, non-root, contains no credentials/media, and has stable signal/exit behavior and redacted logs.
- [ ] All Section 17.2 no-cost tests pass on Windows, repository-version Linux CI, and the local container; after checkout/dependency setup, the CI test process and its children run in a fail-closed no-egress environment with no real credential.
- [ ] The writable-temp baseline passes, the Gemini credential portability defect is fixed rather than suppressed, and the 40-item fake performance criteria pass.
- [ ] Migration and rollback are documented/tested, V2 remains opt-in, the legacy runner is untouched, and `team-main-pre-batch-v2` plus normal Git history remain intact.

These criteria require the Cloud profile, GCS implementation, and container to exist and be verified with fakes; they do not silently authorize a real bucket mutation, image push, Cloud Run deployment, or provider charge.

### 22.2 MVP production-qualified — external evidence only when authorized

- [ ] The user has separately approved and the team has passed the applicable real GCS, image-push, Cloud Run fake-job, one-item provider, and bounded-concurrency pilot tiers.
- [ ] Every executed tier stayed within its recorded identity, retention, attempt, time, and cost limits.
- [ ] Observed route/model, ADC identity, GCS verification, resume behavior, paid-call uniqueness, performance, and cost/error evidence are attached to review.
- [ ] No unresolved `indeterminate` result or cleanup/security issue remains for the route being qualified.

If external approval is withheld, Section 22.1 may still support an opt-in merge, but the affected Cloud/provider route is **not production-qualified** and the legacy runner remains available.

### 22.3 Post-MVP enhancements — explicitly not required for MVP Done

The following do not block Sections 22.1 or 22.2 unless a documented failing MVP safety/correctness test proves otherwise: distributed leases/fencing/failover, array jobs, cross-file transactions, broad Backlot redesign, global cache/index/event sourcing, mixed-provider/general quota platforms, all-media adapter coverage, canonical full-run `approval_policy`, and CostTracker/`cost_log` migration.

### 22.4 Legacy retirement gate

- [ ] V2 has merged to `team-main` and remained opt-in during coexistence.
- [ ] The actual route used to replace the legacy runner has passed applicable Section 22.2 qualification and a representative post-merge recovery exercise.
- [ ] Rollback to the legacy runner is still documented and verified.
- [ ] The user explicitly confirms retirement.
- [ ] Removal occurs in a separate focused commit; the annotated safety tag and recoverable Git history remain intact.

## 23. Merge and retirement workflow

1. **Plan commit:** this document only, on `codex/batch-v2`.
2. **Plan review gate:** user approves or requests revisions. No implementation before approval.
3. **MVP implementation commits:** small M0–M4-aligned commits; contracts/tests before behavior, with post-MVP tracks excluded.
4. **Code-complete evidence:** attach the offline matrix, crash tests, container/FakeGCS test, performance evidence, and scope-gate self-review.
5. **Integration review:** verify diff from baseline, Agent-Native self-review, security/cost review, and rollback steps.
6. **Opt-in merge:** when Section 22.1 is green, merge `codex/batch-v2` into `team-main` through the normal review workflow. State clearly whether Section 22.2 production qualification exists.
7. **Post-merge validation:** run an offline/fake representative V2 path and verify resume, canonical checkpoint/artifact publication, and budget state. Any real GCS, Cloud Run, or provider run requires a new immediate approval for that exact execution and cannot inherit an earlier M5 approval.
8. **Qualification and retirement proposal:** complete applicable M5 tiers, then explicitly confirm the coexistence window and rollback readiness. Post-MVP enhancements are not retirement prerequisites unless they are required by the actual replacement route.
9. **Separate retirement-focused commit:** delete `scripts/batch_run_intent_sequences.py` and make only the necessary reference/test/documentation cleanup.
10. **Preserve recovery:** never delete the annotated safety tag or rewrite history.

## 24. Agent-Native self-review of this Plan

| Review question | Result | Evidence in plan |
|---|---|---|
| Does Python select or advance pipeline stages? | No | One-stage invariant; Agent owns next stage |
| Does Python create prompts or creative decisions? | No | Agent-authored complete work items; missing input fails |
| Can the executor select a provider/model/fallback? | No | Exact concrete identity and no-fallback tests |
| Does Python perform creative review? | No | Only deterministic technical media checks; Agent reviewer remains required |
| Can executor success resolve a Human Gate? | No | `awaiting_agent_review` is separate; Agent/human checkpoint flow |
| Are manifest gates binding? | Yes | Terminal publication remains through `write_checkpoint` |
| Are skills still required? | Yes | Agent reads directors/provider skills before authoring/calling |
| Are paid decisions communicated and budget-bound? | Yes | Request authorization plus immediate Agent announcement requirement |
| Are canonical artifacts/checkpoints preserved? | Yes | Existing validator/writer remain authoritative |
| Is resume a persistence concern rather than orchestration? | Yes | Resume only reconstructs the same frozen request/stage |
| Could concurrency change creative semantics? | No | Independent exact items; no selector or re-planning |
| Does Cloud become a second business implementation? | No | Same engine and contracts; storage/profile adapters only |
| Could workers become competing writers? | No | Project-scoped attempt isolation, coordinator-only shared state, and sequential post-execution publication |
| Does staging obey the workspace contract? | Yes | Tool paths are derived inside `projects/<project-id>/.batch-v2/...`, outside canonical subtrees, under identical Local/Cloud logical roots |
| Can task settings or a stale heartbeat steal Cloud ownership? | No | Exact owner identity plus trusted stop/bound human authorization and expected-generation CAS are required before dispatch |
| Is an ambiguous paid outcome represented honestly? | Yes | `indeterminate`, retained cost exposure, explicit re-approval |
| Does the plan preserve the assets Human Gate? | Yes | Agent review, then `awaiting_human`; only a later explicit human reply permits MVP completion |
| Is Cloud a second orchestrator? | No | One engine and contract; Cloud only selects the GCS/ADC/single-task execution profile |
| Do deferred platform features hide inside MVP gates? | No | Section 19 names separate tracks and Section 22.3 makes them non-blocking absent a concrete failing MVP test |

Self-review conclusion: the proposed executor stays within **tools + persistence**. It accelerates and hardens execution of an Agent-authored decision; it does not replace the Agent as orchestrator, creative director, reviewer, or gatekeeper.

## 25. MVP defaults submitted for coordinating main-task acceptance

The coordinating main task has delegated authority to accept or revise the M0–M4 offline development sequence. The following defaults remain binding unless that task records a Plan revision:

1. **Initial scope:** `assets` stage, independent video-generation work items only.
2. **Global concurrency:** default 3, configurable 1–4.
3. **Provider binding:** one exact allowlisted tool/provider/route/model per MVP batch; no fallback or registry-wide platform contract.
4. **Gemini concurrency:** cap the selected Gemini route at 1 for MVP; raising it is post-MVP qualification.
5. **Cloud topology and ownership:** one process in one Cloud Run Job task, `task-count=1`, `parallelism=1`, `max-retries=0`; additionally record invocation/execution identity, reject an active prior owner, and require trusted stop or prior-owner-bound human authorization plus expected-generation CAS before resume. No array jobs or renewable lease.
6. **Cloud identity:** attached service account/ADC for GCS and the supported Vertex/Gemini route; no local credential path or implicit project fallback.
7. **Storage:** private content-addressed GCS objects plus synchronous, checksum- and generation-verified receipts; no public-by-default URL and no undeclared `gcs_url` mutation.
8. **Workspace and resume:** all tool output paths use the project-scoped non-canonical `.batch-v2/runs/.../attempts/...` subtree in both profiles; durable per-item phases and same-request verified reuse apply, while paid acceptance ambiguity is never auto-replayed.
9. **Writer/lifecycle:** one execution coordinator writes shared state; after it stops, one sequential publication process writes validated canonical state. MVP uses normal `awaiting_human` plus a later explicit human reply, not broad pre-authorization.
10. **Deferred scope:** distributed leases/fencing, array jobs, cross-file transactions, broad Backlot work, canonical `approval_policy`/CostTracker migration, and generic platform/cache/provider capabilities are post-MVP unless a concrete failing MVP test proves a blocker.
11. **Live validation:** each real GCS, image push, Cloud Run, and provider tier receives separate exact approval and applicable cost/time cap.

Acceptance of this Plan approves the boundary, not an unnamed execution path. The exact initial tool/provider/route/model must be recorded as an M0 input before its adapter is implemented and must never be inferred from credentials. Cloud project/region, bucket/prefix/retention, and live-test dollar caps remain deferred until the corresponding M5 user approval.

---

**Planning stop condition:** after this document is committed, this task stops and waits for coordinating main-task acceptance. Batch V2 implementation proceeds only when that task schedules an M0–M4 offline phase. Cloud Run deployment, real GCS mutation, container push, and real/paid provider calls remain prohibited without the separate M5 user approvals above.
