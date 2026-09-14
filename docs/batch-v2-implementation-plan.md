# OpenMontage Batch Executor V2 — Implementation Plan

> - Status: **Proposed — awaiting user approval**
> - Planning branch: `codex/batch-v2`
> - Baseline commit: `aa4dbd42e0f0c05b7029198793c2e52041c24a47`
> - Safety tag: `team-main-pre-batch-v2` (annotated tag; peels to the baseline commit)
> - Audit date: 2026-09-14
> - Scope of this commit: planning only; no Batch V2 implementation, deployment, or paid/live API call

## 1. Decision summary

Batch Executor V2 will be one local-first, cloud-ready execution engine with two configuration profiles:

- `local`: durable local project/run storage plus isolated local scratch space.
- `cloud-run`: the same engine in one Cloud Run Job task, with GCS as durable storage and local ephemeral scratch space.

The initial engine will use one process and bounded internal concurrency. The recommended starting point is three global workers, within the approved 2–4 range. Provider-specific limits are stricter: an unqualified paid provider starts at one in-flight call, and Gemini Omni remains at one until its credential routing and thread-safety gates pass. Array jobs and distributed scheduling are intentionally deferred.

The governing boundary is non-negotiable:

- The **Agent** selects the pipeline and stage, reads the director/provider skills, makes creative choices, selects the exact provider/model, communicates cost, authors immutable work items, self-reviews results, and owns all Human Gates.
- The **executor** validates and mechanically runs only the exact, already-approved work items for one stage. It may schedule, rate-limit, retry when demonstrably safe, resume, cache, stage bytes, persist run state, and report results.
- The executor must never choose the next pipeline stage, generate or rewrite prompts, select a provider through a selector, silently change a provider/model, perform quality review, resolve a gate, or continue into edit/compose.

The executor's successful terminal state is `awaiting_agent_review`, not a pipeline `completed` checkpoint. After Agent review, the Agent authorizes canonical publication and a fenced commit coordinator persists it through `schemas.artifacts.validate_artifact()` and `lib.checkpoint.write_checkpoint()`. A gated stage is written `awaiting_human` unless a still-valid, explicitly recorded full-run pre-authorization covers that gate. `completed` with `human_approved=true` always requires human approval evidence for that gate; the Agent, never the executor, determines whether a new reply or an in-scope pre-authorization supplies that evidence.

All worker output goes to isolated per-attempt staging. A single coordinator is the only writer of run state, cache indexes, cost state, storage receipts, canonical media promotion, and checkpoint progress. Existing hidden GCS background writers must be disabled in the V2 execution context.

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

There is one contract inconsistency to resolve before implementation: `AGENT_GUIDE.md:592` and `skills/meta/checkpoint-protocol.md` require full-run pre-authorization to be recorded with `decision_log.category = "approval_policy"`, but `schemas/artifacts/decision_log.schema.json` does not currently allow `approval_policy` in its category enum.

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

- Gemini's provider cap remains one until credential routing, global state, typed failures, and concurrency tests pass.
- The request freezes Developer versus Vertex, project/location, exact model, and auth mode; environment discovery may satisfy credentials but must not alter routing.
- Vertex must adopt ambient ADC for Cloud Run. A service-account file may remain an explicit local-only option; the hard-coded path and hard-coded project fallback must be removed.
- After a possibly accepted paid call, V2 records `indeterminate` and stops automatic replay unless the remote operation can be reconciled safely or the user explicitly re-authorizes it.

### 2.8 Cost and observability findings

- `ToolResult` can report cost, duration, seed, model, artifacts, data, and error, but error and billing semantics are not rich enough for a durable attempt record.
- `tools/cost_tracker.py` performs mutable whole-file reads/writes without coordinator locking, CAS, or atomic publication.
- It persists a top-level `approved_tools` property that is not allowed by `schemas/artifacts/cost_log.schema.json`.
- Backlot consumes checkpoint `metadata.partial_progress` and tool event streams, but ordinary loose artifact precedence can surface unreviewed or stale mixed state.

The cost schema mismatch and decision-log `approval_policy` mismatch are Phase 0 contract blockers, not issues to work around inside the executor.

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
4. Make interruption and restart safe through durable run state, verified cache entries, and explicit ambiguous-call handling.
5. Make local and Cloud Run execution profiles share one code path and one set of contracts.
6. Preserve existing artifact/checkpoint/Human Gate semantics and Backlot truthfulness.
7. Support local durable storage and GCS durable storage behind one narrow interface.
8. Provide enough provenance, cost, and structured telemetry for the Agent and user to audit every call.
9. Keep the legacy runner operational until the defined retirement gate.

### 3.2 Initial functional scope

The recommended first production scope is the `assets` stage, beginning with independent video-generation work items. This is where historical wait time is concentrated and where concurrency has the clearest benefit.

The core contracts should be media-neutral so image, audio, and other independently executable assets can be added after their tool adapters pass the same batch-safety contract. Initial implementation should not claim a tool type is supported merely because it inherits `BaseTool`.

### 3.3 Non-goals

- Selecting a pipeline or calculating the next stage.
- Reading a director skill and turning a `scene_plan` into prompts or work items inside Python.
- Creative planning, provider ranking, quality review, or revision decisions.
- Automatic selector use, provider/model fallback, or capability substitution.
- Crossing `assets -> edit -> compose` in one executor invocation.
- Automatically writing terminal pipeline state after execution.
- Distributed scheduling, Cloud Run array jobs, multi-region failover, or Kubernetes.
- Perfect exactly-once semantics for providers that do not expose idempotency/recovery.
- Replacing all existing storage and checkpoint code in the first phase.
- Changing or deleting the legacy runner before migration acceptance.
- Deploying infrastructure or performing paid/live tests without a separate explicit user approval.

## 4. Architectural invariants

These are release-blocking invariants, not preferences:

1. **One stage per batch.** Every request has one `project_id`, `pipeline_type`, and `stage`.
2. **Frozen exact execution.** Every work item names one concrete tool, provider route, model/variant, operation, complete inputs, and output contract.
3. **No creative derivation.** The executor validates; it does not infer missing production choices.
4. **No silent fallback.** A blocked exact tool produces a blocker result.
5. **Authorization before dispatch.** Project identity, checkpoint chain, approval evidence, and cost cap are authenticated before any side effect.
6. **Single coordinator writer.** Workers never mutate canonical project state or shared control state.
7. **Durability before success.** Output verification and durable storage receipt precede `committed` state.
8. **Unknown paid outcome is not retryable by default.** Possible acceptance becomes `indeterminate`.
9. **Canonical schemas stay canonical.** Storage locators do not introduce unknown artifact fields.
10. **Human Gates remain human.** Executor completion never implies review or approval.
11. **Profile parity.** Local and Cloud Run differ only in configuration, storage/scratch implementations, and identity source.
12. **Legacy coexistence.** V2 writes to a namespaced run area until explicit Agent promotion.

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
| `in_progress` heartbeat | Authorizes stage run | Sole physical writer in the active fenced epoch | Never writes | None |
| `awaiting_human` checkpoint | Owns decision after self-review | Sole physical writer of exact Agent command through official writer | None | Reviews |
| `completed/human_approved` | Determines whether valid human evidence covers the gate and issues exact command | Sole physical writer of that command through official writer | None | Supplies new or recorded in-scope approval |
| Next pipeline stage | Owns after checkpoint | Must not invoke | None | Gate may allow |

Static and behavioral tests will enforce this table. In particular, the execution engine must not import or call `get_next_stage`, stage director/reviewer logic, selectors, edit/compose render orchestration, or Human Gate decision code. “Agent owns” means the Agent makes and records the semantic decision; it does not create a second physical writer. A leased/fenced coordinator epoch is the only process allowed to persist shared project/run state. After an execution coordinator releases its epoch, a commit-only coordinator may acquire a new epoch and persist an exact Agent-authored publication command.

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
       exact concrete BaseTool adapters
          |          |          |
       isolated per-attempt scratch only
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
 fenced commit coordinator -> validate_artifact + write_checkpoint
                    |
       Human Gate evidence, when required
          (new reply or valid recorded policy)
                    |
                    v
 fenced commit coordinator -> completed/human_approved=true
```

### 6.1 Proposed implementation layout

No files below are created in this planning phase. The intended layout is:

```text
schemas/execution/
  batch_request.schema.json
  batch_state.schema.json
  batch_result.schema.json
  storage_receipt.schema.json

lib/batch_executor/
  contracts.py          # schema loading, canonical JSON, digests
  authorization.py      # fail-closed project/checkpoint/approval checks
  engine.py             # coordinator loop only
  scheduler.py          # bounded permits and fairness
  quota.py              # provider token buckets / Retry-After feedback
  retry.py              # typed classification and approved retry policy
  journal.py            # coordinator-only state/event persistence
  cache.py              # verified result index
  storage.py            # Store protocol, LocalStore, GCSStore
  media_validation.py   # deterministic byte/container checks
  tool_adapter.py       # exact registry resolution and result normalization
  errors.py             # stable error taxonomy
  telemetry.py          # redacted structured events and summaries

scripts/batch_execute.py # thin CLI; no planning/orchestration logic
tests/batch_executor/
```

The schema directory is intentionally separate from `schemas/artifacts/`: execution control documents are not pipeline canonical artifacts. Any eventual canonical artifact still uses the existing artifact registry and checkpoint writer.

### 6.2 Execution profiles

| Setting | Local profile | Cloud Run profile |
|---|---|---|
| Engine | Same coordinator package | Same coordinator package |
| Process/task count | 1 process | Cloud Run Job `task-count=1`, `parallelism=1` |
| Default workers | 3 | 3, subject to CPU/memory/provider profile |
| Scratch | Configured local temp outside canonical project tree | `/tmp/openmontage/...` ephemeral |
| Durable run store | LocalStore | GCSStore |
| Project source | `OPENMONTAGE_PROJECTS_DIR` plus explicit project ID | Immutable GCS project/request snapshot |
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
- applicable decision-log IDs/digests for provider selection, budget changes, fallback decisions, and any valid full-run pre-authorization;
- exact allowed tool/provider/route/model set, normally one identity per item;
- maximum total attempts and maximum authorized spend for the batch;
- authorization timestamp and scope.

The executor authenticates this evidence against the current manifest-derived DAG and canonical state. A wrong pipeline DAG, missing/immediate predecessor, unapproved gated predecessor, stale digest, or checkpoint that fails `read_checkpoint` blocks all dispatch. The executor does not create approval evidence or decide whether a broad approval semantically covers a later Human Gate; the Agent records that conclusion in the exact publication command.

`execution_policy` includes only mechanical controls:

- global worker cap;
- provider/tool quota policy IDs and explicit numeric bounds;
- retry policy version, attempt/time/cost ceilings;
- cache policy;
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

The state snapshot is derived from an append-only event/attempt history and contains:

- request identity/digest;
- coordinator owner/fencing token and state revision;
- lifecycle status/outcome;
- per-item current state and attempt count;
- provider permit/rate summary;
- aggregate estimated/reserved/known actual/indeterminate cost;
- cache statistics;
- timestamps and last durable event sequence;
- links to result and storage receipts.

State must not contain secrets or full prompts by default.

### 7.6 Attempt and error records

Every attempt records:

- batch/item/attempt IDs and idempotency digest;
- exact tool/provider/route/model identity;
- coordinator dispatch sequence;
- timestamps for queued, dispatched, response received, bytes verified, and committed where available;
- acceptance knowledge: `not_accepted`, `accepted`, or `unknown`;
- provider remote operation/interaction ID as soon as it becomes available;
- structured error class, HTTP/provider code, sanitized message, retry-after, and retry decision;
- estimated, reserved, known actual, and potentially charged amounts;
- output digest/size/probe summary and storage receipt;
- no credential values and no raw provider payload unless explicitly redacted and separately protected.

### 7.7 BatchResult v1

The durable result reports every item, including failures and indeterminate calls. It contains no pipeline approval claim.

Required summary fields:

- request digest and source bindings;
- status `awaiting_agent_review` when all safe mechanical work has stopped;
- outcome `all_succeeded`, `partial_failure`, `failed`, `cancelled`, or `indeterminate`;
- successful/cache-hit/failed/indeterminate counts;
- per-item verified storage receipt or structured blocker/error;
- full cost snapshot including retained reserves for indeterminate calls;
- retry/cache/quota statistics;
- Agent-review checklist hints limited to facts, never an automated creative verdict.

### 7.8 StorageReceipt v1

Every committed blob receipt includes:

- `sha256`, byte size, media type, and deterministic probe facts;
- store type;
- local logical path or private `gs://bucket/object` locator;
- GCS object generation and provider checksum when applicable;
- creation time and producing item/attempt IDs;
- encryption/access classification;
- no public or signed URL as durable identity.

### 7.9 Canonical artifact and checkpoint publication

Execution and publication are deliberately separate barriers:

1. The coordinator finishes durable media and BatchResult records.
2. The batch enters `awaiting_agent_review`.
3. The Agent inspects outputs using the stage reviewer skill and manifest `review_focus`.
4. The Agent constructs the stage's canonical artifact from reviewed results.
5. The Agent emits an immutable `PublicationCommand` containing the exact artifact, target checkpoint status, review/cost facts, and approval evidence. If a gate lacks a still-valid recorded full-run pre-authorization, the target is `awaiting_human` and the Agent ends the turn. If a valid pre-authorization explicitly covers the gate, the Agent may target `completed` with its decision reference and `human_approved=true` after self-review.
6. A commit-only coordinator acquires the project/stage writer lease after the execution coordinator has released its epoch. It enters a scoped V2 publication context that suppresses all legacy BaseTool/checkpoint GCS background writers.
7. The coordinator validates the artifact with `validate_artifact` and calls `write_checkpoint` with the exact Agent-authorized status. The checkpoint-embedded artifact is the V2 canonical authority.
8. Backlot recognizes V2 publication metadata and prefers the validated checkpoint authority. Only after that checkpoint/current pointer is durable may the coordinator write a digest-identical loose artifact as a compatibility cache.
9. If a new human reply is needed, the Agent later emits a second immutable command and a new fenced commit-only epoch writes `completed, human_approved=true` with that approval evidence.

For non-gated stages, the Agent still performs self-review before an exact terminal checkpoint command. The executor never advances to the next stage.

Two local files are not claimed to be a transaction. Safety comes from one explicit authority: the checkpoint/current pointer is published first and Backlot/downstream V2 readers ignore a missing or stale loose cache. A loose canonical artifact, when retained for compatibility, must be bit-equivalent to that authority. A crash before the derived cache update therefore cannot expose a new-artifact/old-approval state.

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
- `ready`: request is frozen and coordinator lease acquired.
- `running`: at least one item may be queued/dispatched; durable run ownership exists.
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
```

- `succeeded_staged` is not durable success; it means worker bytes and facts reached the coordinator.
- `committed` requires media validation, content digest, durable blob receipt, attempt record, and state transition.
- `indeterminate` is terminal for automatic scheduling.
- One item's terminal failure does not cancel independent items.

### 8.3 Attempt phases

Adapters should expose the finest truthful phases possible:

```text
prepared -> dispatched -> provider_accepted -> result_received
         -> bytes_staged -> technically_valid -> durably_committed
```

Not every provider reveals `provider_accepted`. The absence of evidence must not be converted into `not_accepted`. Current synchronous BaseTool providers may require conservative `unknown` classification after dispatch.

### 8.4 Checkpoint progress lifecycle

- Before dispatch, the Agent authorizes a formal `in_progress` stage checkpoint in the immutable request. After full preflight and writer-lease acquisition, the execution coordinator is the sole process that calls `write_checkpoint` with the `batch_id`/request digest and zero progress.
- The same fenced coordinator epoch may coalesce item progress into `metadata.partial_progress` through `write_checkpoint`; workers never write it.
- Successful `in_progress` persistence does not replace the separate authorization checks.
- Terminal BatchResult does not itself change checkpoint status. The execution coordinator releases its lease before any later commit-only publication epoch begins.
- Any Cloud profile checkpoint backend must preserve `write_checkpoint`'s semantic validation rather than reimplementing gate policy.

## 9. Bounded concurrency and provider quota

### 9.1 Scheduler model

- One coordinator process owns a bounded thread pool for synchronous, I/O-bound tools.
- Initial global default: `max_workers = 3`; valid configured range: 1–4 for the first release.
- CPU/GPU-local tools may advertise stricter resource permits; process pools are not part of the first release.
- A work item must acquire all applicable permits before dispatch: global, provider, tool, resource, and budget reservation.
- Retries re-enter the same queue and do not bypass rate limits.
- A fair queue prevents a throttled provider from starving work for another provider.
- Cancellation stops new dispatch and records unresolved in-flight outcomes honestly.

### 9.2 Provider policy

Each versioned provider profile can define:

- maximum in-flight calls;
- request tokens per interval;
- generated-seconds or other provider-specific quota units per interval;
- burst capacity;
- minimum spacing;
- Retry-After behavior;
- maximum attempts and elapsed time;
- per-attempt and per-batch cost caps;
- recoverability/idempotency capability;
- declared thread-safety level.

No quota is guessed from historical latency. Unknown paid providers default to one in-flight call and require a reviewed profile before concurrency is raised.

### 9.3 Gemini initial limit

Gemini remains `max_in_flight = 1` until all of the following pass:

1. Developer versus Vertex route/model/auth is explicit and immutable.
2. Vertex uses ambient ADC without a key file in the Cloud profile.
3. DNS and credential caching no longer mutate unprotected global state per call.
4. Mock concurrency tests show no credential-refresh or route races.
5. A separately approved live pilot establishes a safe provider quota.

After those gates, raise to two first; three requires measured evidence. The global engine can still default to three for other independently qualified tools/providers.

### 9.4 Future scale

Cloud Run array jobs are considered only after one-task measurements show that one of these is the limiting factor:

- local CPU/memory rather than provider quota;
- more than approximately 100 independent items per batch;
- one-task maximum duration;
- a proven need for multi-provider isolation.

Moving to multiple tasks requires a new distributed lease/fencing and cost-reservation design; it is not a configuration flip.

## 10. Idempotency, cache, and resume

### 10.1 Cache eligibility

A cache hit is accepted only when:

- the full work-item digest matches;
- the tool/provider/route/model and tool contract revision match;
- every input content digest matches;
- the result is in a terminal committed state;
- blob SHA-256 and size match the receipt;
- deterministic technical media probes pass;
- the object generation/version still exists;
- the cache entry is not marked revoked or incompatible.

File existence or a size threshold is never enough.

For stochastic generation, a cache hit means reuse of a previously accepted exact result, not a claim that regeneration would be deterministic.

### 10.2 Content-addressed storage

Media is first committed to an immutable path such as:

```text
blobs/sha256/<first-two-hex>/<full-sha256>
```

Run/item paths are small references to the blob receipt. Canonical project materialization happens only during Agent-approved publication. An existing blob with the same digest is verified and reused; an existing logical path with a different digest creates a conflict rather than an overwrite.

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
2. acquires a new lease/fencing token;
3. verifies the event/state revision chain;
4. verifies each committed receipt and reconstructs the derived state;
5. requeues `pending`, `eligible`, and expired `retry_wait` items;
6. treats stale `running` attempts according to provider semantics;
7. reconciles recoverable remote operation IDs before considering a new call;
8. marks possibly accepted paid attempts `indeterminate` when safe reconciliation is unavailable;
9. emits a complete resumed BatchResult without hiding partial failures.

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

### 11.3 Failure aggregation

The default batch policy is `continue_independent`:

- terminal failure of one item does not cancel unrelated items;
- dependency-linked items become `blocked_by_dependency` without running;
- systemic authentication, project identity, lease, storage durability, or budget failures stop new dispatch globally;
- the result enumerates all successes, failures, blockers, and indeterminate attempts.

## 12. Single-writer and commit protocol

### 12.1 Writer ownership

Only one leased/fenced coordinator epoch may mutate shared state. An execution epoch owns run/progress writes; after it durably finishes and releases the lease, a commit-only epoch may persist an exact Agent-authored publication command. The Agent owns the decision but is not a competing filesystem/object-store writer.

The active coordinator may mutate:

- BatchState and event sequence;
- attempt ledger;
- cache index;
- cost reservations/reconciliation;
- durable storage receipts and logical references;
- canonical media during later publication;
- checkpoint progress;
- canonical artifacts/checkpoints only when authorized by an immutable Agent publication command.

Workers may only:

- read immutable request/materialized inputs;
- write to their unique attempt scratch directory;
- invoke the exact tool with a staging output path;
- return immutable result facts/messages to the coordinator.

### 12.2 Suppressing legacy hidden writers

Every V2 execution **and V2 result-to-artifact/checkpoint publication epoch** must:

- disable legacy `GCS_AUTO_SYNC` behavior even when V2's own GCSStore is configured;
- disable or redirect BaseTool's project event writer and post-success auto-upload in a scoped Batch execution context;
- bypass the terminal `write_checkpoint` legacy async-sync hook for V2 publication metadata, then use the coordinator's synchronous Store commit path instead;
- keep attempt scratch outside the canonical project tree so legacy path inference cannot mistake it for canonical output;
- prevent workers from calling `write_checkpoint`, `atomic_update_json`, CostTracker persistence, or writing `artifacts/`.

Disabling these behaviors must be scoped to V2 and must not silently break the legacy runner. Integration tests write both `awaiting_human` and `completed` V2 checkpoints and prove that no legacy future is scheduled and no background mutation appears after `write_checkpoint` returns.

### 12.3 Local commit sequence

For one successful attempt:

1. worker closes output in unique scratch;
2. coordinator probes media and computes SHA-256/size;
3. coordinator writes an attempt record containing the staged digest;
4. coordinator copies/writes to a unique temporary file in the target filesystem;
5. flush and `fsync` the file;
6. verify copied digest;
7. atomically publish with `os.replace` or no-replace semantics as appropriate;
8. `fsync` the parent directory where supported, documenting Windows limitations;
9. persist the storage receipt and state revision;
10. only then set item state `committed`.

Run ownership uses an OS-level exclusive lease or equivalent, and canonical publication additionally uses a project/stage lease. A second process opening the same batch or publishing the same project/stage must be rejected or fenced; a process-local `threading.Lock` is insufficient.

### 12.4 GCS commit sequence

1. upload the content-addressed blob with `if_generation_match=0`;
2. request and verify provider checksum, size, and metadata SHA-256;
3. retain bucket, object name, and immutable generation receipt;
4. write immutable attempt/event records;
5. update the current state pointer with an expected generation/CAS;
6. only after all durable receipts succeed mark the item committed.

If the blob upload succeeds and state CAS fails, restart discovers and verifies the orphan/previous blob by digest; it never regenerates merely because the state update failed.

### 12.5 Checkpoint publication constraints

- Existing `write_checkpoint` remains the only semantic path for checkpoint construction, schema checks, manifest gates, and prerequisites.
- V2 may extend its persistence backend or wrap its validated bytes for GCS, but must not copy its gate logic into a second implementation.
- Cloud durable checkpoint publication needs conditional generation and a current-pointer protocol; merely calling local `write_checkpoint` in ephemeral `/tmp` and launching background upload is not acceptable.
- Terminal artifact/checkpoint status and content remain an Agent decision after review; the active commit-only coordinator is the sole physical writer.
- For V2, checkpoint-embedded artifacts/current pointers are authoritative. Loose files are derived caches written later, so two-file atomicity is neither assumed nor required for reader correctness.
- Crash-injection tests cover the decision-log/checkpoint cross-file boundary until a transactional bundle/current-pointer protocol exists.

## 13. Security, credentials, and path safety

### 13.1 Identity and containment

- Validate every project ID with `lib.identity.validate_project_id`.
- Resolve local project roots through `resolve_project_dir` and reject symlink/junction aliases or escapes.
- Batch V2 requires an existing, valid `project.json` with matching `project_id` and `pipeline_type`; legacy missing-marker tolerance is not accepted.
- All input/output logical paths are relative, normalized, and checked against their allowed roots.
- Scratch and canonical roots are distinct. A worker cannot choose a canonical path.
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
- Private objects by default; no `make_public()` in V2.
- Public delivery, if ever needed, is a separate publish-stage decision.
- Uniform bucket-level access and customer-managed encryption choices are deployment inputs, not hard-coded behavior.
- Object retention/lifecycle rules are documented before a real bucket test.

### 13.4 Supply chain and container

- Pin Python and direct dependencies through a reproducible lock/constraints strategy.
- Explicitly include `google-cloud-storage`; include `ffmpeg`/`ffprobe` only if the technical validator requires them.
- Build from a minimal supported Python base matching repository policy (currently `.python-version` is 3.10).
- Run as a non-root user with read-only application code and writable `/tmp` only.
- Emit an SBOM/vulnerability scan in CI before Cloud deployment.

## 14. Local/GCS storage abstraction

### 14.1 Store protocol

Both implementations expose the same typed operations:

```text
put_blob_if_absent(bytes/path, sha256, metadata) -> StorageReceipt
head_blob(receipt_or_digest) -> BlobStat
get_blob(receipt_or_digest, destination) -> verified local path
materialize_input(receipt, scratch_path) -> verified local path
put_immutable_record(key, bytes, digest) -> RecordReceipt
read_record(key_or_receipt) -> bytes + version
compare_and_swap_pointer(key, expected_version, new_receipt) -> new version
acquire_or_renew_lease(batch_id, owner, expected_fence) -> fence
release_lease(batch_id, owner, fence)
```

Errors are typed; no method turns a failed durable write into `None` or an empty success.

### 14.2 Proposed namespace

```text
projects/<project_id>/batch-v2/
  requests/<request_digest>.json
  runs/<batch_id>/
    current.json                 # versioned pointer/CAS target
    events/<sequence>.json       # immutable in GCS; JSONL may be a local view
    attempts/<item>/<attempt>.json
    results/<result_digest>.json
    items/<item_id>.json         # logical receipt reference
  blobs/sha256/<prefix>/<digest>
```

GCS object names include the validated project ID. LocalStore mirrors the logical layout under an explicitly configured durable root.

### 14.3 Durable project/checkpoint integration

Cloud execution starts from an immutable project/request snapshot whose manifest binds all required canonical files and generations. The job materializes and validates that snapshot before dispatch.

The recommended integration path is:

- keep execution-run state in the dedicated V2 store;
- have the Agent authorize the formal initial `in_progress` checkpoint in the frozen request, then let the leased execution coordinator persist it after preflight and before dispatch;
- add a storage-aware backend beneath the existing checkpoint semantic builder for cloud progress, using generation preconditions;
- never treat ephemeral local checkpoint bytes as durable success;
- after the job, let the Agent ingest the durable BatchResult and self-review, then issue an exact publication command for a new commit-only coordinator epoch.

If a storage-aware checkpoint backend is not ready, the Cloud profile may run fake-tool packaging tests but is not production-ready for a real provider batch.

### 14.4 Locator separation

GCS location belongs in `StorageReceipt`/execution provenance, not in current `asset_manifest` or `render_report` unknown fields. Canonical schemas may later add a formally versioned locator field through a deliberate migration, but V2 must not mutate schemas implicitly.

## 15. Cloud Run Job packaging and operation

### 15.1 Image and entrypoint

Proposed dedicated assets:

- `Dockerfile.batch-v2` with pinned Python runtime and dependencies.
- Non-root entrypoint running `python scripts/batch_execute.py run --profile cloud-run --request-uri ...`.
- Image contains no `.env`, credential JSON, project media, or local cache.
- Request URI, bucket, project/location, worker limit, and quota profile are supplied as immutable arguments/config.

The CLI remains thin:

1. load profile;
2. resolve request bytes;
3. validate/preflight;
4. invoke the shared engine;
5. return a stable exit code and result locator.

### 15.2 Job shape

- `task-count=1`, `parallelism=1`.
- Internal bounded concurrency only.
- Set timeout above the authorized batch worst case, including retry waits.
- Size memory/CPU for the sum of staging buffers, probes, and configured workers.
- Use ephemeral `/tmp` only for recoverable scratch.
- Attach the dedicated service account.
- Send structured stdout to Cloud Logging.
- On SIGTERM, stop dispatch, persist cancellation intent, reconcile in-flight calls, flush durable state, and exit before the platform deadline where possible.

### 15.3 Preflight

Cloud preflight must fail before provider dispatch when any of these is absent or inconsistent:

- request/schema/digest;
- valid project snapshot and approval/checkpoint bindings;
- exact tool version and batch-safe declaration;
- explicit provider route/model/project/location;
- ambient identity and required scopes;
- bucket access and conditional-write capability;
- storage read-after-write verification;
- budget reservation capacity;
- sufficient scratch capacity;
- disabled legacy background sync/writers.

### 15.4 Stable exit codes

Proposed categories:

- `0`: BatchResult durable; inspect outcome.
- `2`: request/contract/authorization failure before side effects.
- `3`: configuration/auth/storage preflight blocker.
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
- coordinator owner/fence and event sequence;
- exact tool/provider/route/model identifiers;
- lifecycle transition;
- queue wait, provider wait, validation, and storage latency;
- permit/rate-limit state;
- retry class and delay;
- cache decision;
- estimated/reserved/known actual/potential cost;
- output digest and size, not raw bytes.

Prompts and provider response bodies are omitted from normal logs. A separately protected debug mode may log redacted summaries, never credentials.

### 16.2 Metrics and run summary

Minimum metrics:

- total wall time and external wait time;
- active/queued items and maximum observed concurrency;
- throughput per provider/tool;
- p50/p95 item and storage latency;
- success/failure/indeterminate rates;
- retry and 429 counts;
- cache hit/miss/corruption counts;
- bytes staged/committed/downloaded;
- estimated versus known actual cost and unreconciled exposure;
- resume count and recovery time.

Local runs write a durable summary plus readable console output. Cloud emits the same event fields to stdout and stores the final summary in GCS.

### 16.3 Cost reservation protocol

- The immutable request binds the approved batch cap and per-item estimates.
- Before dispatch, the coordinator serially reserves worst-case authorized cost for the attempt.
- Concurrency cannot oversubscribe the budget because workers never reserve independently.
- On success or known failure, the coordinator reconciles actual cost when reported.
- Indeterminate paid attempts retain conservative reserved exposure.
- Retries consume the same batch cap and explicit attempt allowance.
- Splitting a batch or resuming cannot reset approval or the budget ledger.

Before reuse, CostTracker must be hardened for atomic coordinator publication and made schema-valid. The recommended schema-compatible fix is to move approval bookkeeping into a defined `metadata` structure or formally version the schema, rather than continuing the unknown top-level `approved_tools` property.

### 16.4 Backlot behavior

- `metadata.partial_progress` can link to V2 run state and show factual counts.
- Worker scratch and execution drafts are never treated as canonical artifacts.
- Backlot must show `awaiting_agent_review` as execution state distinct from `awaiting_human`.
- On promotion, loose artifact and checkpoint-embedded artifact digests must match.
- A crash cannot leave Backlot showing new assets under an old approval badge.
- Any remote media access uses an authenticated resolver or short-lived signed URL generated at view time; durable records keep private locators.

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

### 17.2 Mandatory mock/fake, no-paid test matrix

All tests in this table must pass without real credentials, GCS, Cloud Run, or provider calls.

| Area | Required scenarios | Acceptance |
|---|---|---|
| Request schema | valid request, missing fields, unknown fields, invalid enum/path/number | Fail closed before tool resolution |
| Canonical digest | key order, Unicode, numbers, logical path normalization, self-digest exclusion | Same semantic request yields same full SHA-256 on Windows/Linux |
| Request conflict | same `batch_id`, different digest | Hard conflict; no call |
| Project identity | traversal, absolute/UNC/drive path, symlink/junction alias, missing/corrupt marker | Rejected before any side effect |
| Source binding | changed artifact/checkpoint/input digest, changed GCS generation | Rejected before any call |
| Gate/authorization | wrong manifest/DAG, missing or unapproved immediate predecessor, unapproved/stale `scene_plan`, hand-edited invalid checkpoint, unapproved proposal where present, stale budget, missing decision, invalid full-run authorization | Complete manifest-derived chain is read/validated; rejected before any paid call |
| Decision schema | `approval_policy` contract after reconciliation | Documentation, schema, validator, and tests agree |
| Exact registry routing | fake concrete tool present/missing/version mismatch | Exact match only; no selector/fallback |
| Tool support envelope | batch-safe/thread-safe/recovery/retry/idempotency metadata | Missing mandatory metadata fails preflight |
| Worker isolation | fake tool writes only supplied staging path | No worker write in project/artifacts/checkpoints/run state |
| Bounded concurrency | deterministic blocking fake tool at W=1..4 | Observed concurrency never exceeds every active cap |
| Provider quota | fake clock/token bucket, bursts, multiple providers | Rate windows and fairness exact; no real sleep |
| Retry | submit-rejected 429, post-accept poll/download 429, acceptance-unknown 429, Retry-After, 5xx pre-accept, permanent reject, auth failure | Only safe phase retries; post-accept poll keeps generation submit count at one; full jitter bounded |
| Paid ambiguity | timeout/crash before dispatch, during POST, after accepted ID, during download | Unknown acceptance becomes `indeterminate`; no duplicate fake call |
| No fallback | exact provider blocked while an alternative fake provider is available | Blocker returned; alternative call count remains zero |
| Failure aggregation | mixed success/failure/blocked/indeterminate items | Independent items continue; complete result inventory |
| Cost reservation | concurrent fake paid items near cap | No oversubscription; attempts/resume share one ledger |
| Cost schema | save/reload/reconcile/indeterminate reserve | `validate_artifact("cost_log", ...)` passes |
| Cache key | prompt/model/route/duration/store/reference-digest/tool-revision changes | Every output-affecting change misses cache |
| Cache verification | missing/truncated/corrupt/wrong generation/wrong media blob | Reject cache and follow safe retry policy |
| LocalStore | conditional create, CAS conflict, batch and project/stage lease conflict, writer-epoch handoff, digest verification | No lost update; second coordinator fenced; commit-only epoch starts only after execution epoch ends |
| FakeGCSStore | generation preconditions, checksum mismatch, transient error, CAS conflict | Typed errors and deterministic recovery |
| Commit crash matrix | crash before/after blob, attempt, state pointer, cost, checkpoint, decision log | Resume has one truthful authority and no unnecessary provider replay |
| Checkpoint progress | official `in_progress` + partial progress | Uses `write_checkpoint`; artifacts empty unless schema-valid |
| Terminal gate | execution success; Agent command with no broad approval; valid/invalid full-run pre-authorization; later human reply | Executor alone never emits terminal pipeline state; Agent evidence determines awaiting versus completed |
| Artifact validation | generated draft with unknown `gcs_url`, missing provenance, bad path | Validator rejects; no canonical publication |
| Terminal sync suppression | V2 `awaiting_human` and `completed` publication with legacy auto-sync otherwise enabled | No legacy future scheduled and no post-return artifact mutation |
| Backlot | staging, progress, promotion, restart, old approval | No new-artifact/old-approval mixed display |
| Credential resolver | no creds, fake API key, explicit local key file, fake ambient ADC | Deterministic; no `D:\` or developer state leakage |
| Gemini route | fake Developer vs Vertex resolution | Route/model stays request-bound despite ambient credentials |
| Gemini thread safety | concurrent fake ADC refresh/DNS path | No global mutation/race before raising cap |
| Output validation | empty/truncated/wrong container/duration/audio facts | Never committed as success |
| Security/redaction | secret-shaped inputs/errors/headers/signed URLs | No secret in events/result/cache |
| CLI | dry/fake success, contract failure, partial failure, cancellation | Stable exit codes and durable result pointer |
| Container smoke | Linux image, non-root, read-only app, fake batch | Same request digest and result semantics as local |
| Performance harness | 40 fake 46-second-equivalent waits with fake/scaled clock | Meets scheduler target without network/cost |

An in-memory fake provider must expose counters, barriers, scripted errors, remote IDs, charges, and deliberate crash points. A FakeGCS client must model object generations and precondition failures rather than merely returning URLs.

### 17.3 Real tests requiring separate explicit user approval

None of these are authorized by approval of this Plan alone.

| Test | External effect/risk | Required approval payload |
|---|---|---|
| Real provider single sample | May charge and store provider-side data | Exact tool/provider/route/model, prompt/input class, duration, max USD, retention setting |
| Real provider concurrency pilot | Multiple charges/quota impact | Item count, W1/W2/W3 comparison plan, max attempts, total max USD |
| Full 40-shot benchmark | Material spend and time | Exact frozen request, cache policy, provider quota, total cap, stop conditions |
| Real GCS integration | Creates/reads cloud objects | Project, bucket, prefix, region, IAM identity, retention/cleanup plan |
| Cloud image push | Creates registry artifact and may incur storage | Project/region/repository/image tag |
| Cloud Run fake-tool job | Deploys/runs cloud resource without provider spend | Project/region/service account/resources/max runtime/cleanup |
| Cloud Run real-provider job | Deployment plus paid API and durable data | All Cloud and provider details plus combined max cost |
| Public/signed delivery test | Changes access exposure | Exact objects, access duration, audience, rollback |

Approval is obtained immediately before each test tier. A single-sample gate precedes any live batch. A failed or ambiguous live call does not authorize an extra replacement call.

### 17.4 Platform matrix

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
- A full 40-shot capacity target is at most 15 minutes at W=3 when provider quota and retry-free conditions permit; if not, publish the measured quota-limited result and revise the target before release.

Correctness, cost safety, and truthful ambiguity handling take precedence over the speed target.

## 19. Phases, milestones, and acceptance criteria

No implementation phase, including Phase 0, begins until this Plan is approved or revised by the user. Phases are sequential hard gates: every prior phase's acceptance criteria must be green before the next phase begins. Phase 6 additionally requires the entire mandatory offline/mock matrix and Phases 0–5 to be green before requesting any external-test approval.

### Phase 0 — Contract decisions and executable safety specification

Deliverables:

- approve this Plan and record open decisions;
- reconcile `decision_log.category="approval_policy"` with its schema/protocol;
- reconcile CostTracker's `approved_tools` persistence with `cost_log` schema;
- write execution schemas and canonical digest specification;
- define tool batch-safety/support-envelope additions;
- add test-first regression cases for Agent-Native boundaries, hidden writers, ambiguity, schema mutation, and credential isolation. They may be red in an intermediate implementation commit, but the minimum contract/preflight code required to make the Phase 0 suite green is part of this phase.

Acceptance criteria:

- documentation and schemas agree on approval evidence;
- current canonical artifact/checkpoint validation remains green;
- every new Phase 0 regression is green; no expected failure is carried into Phase 1;
- a request cannot reach a fake tool without valid marker, source chain, approval, budget, and exact tool identity;
- responsibility tests prove the engine has no pipeline-stage, review, selector, or fallback behavior;
- no real credentials or network are used.

### Phase 1 — Local contracts, fake adapter, and coordinator skeleton

Deliverables:

- request/state/result/receipt validators;
- exact ToolRegistry resolver and explicit `batch_safe` contract;
- in-memory scripted fake tool;
- single-process coordinator, global/provider permits, event model, and thin CLI;
- scoped suppression/redirection of BaseTool hidden event/GCS writers.

Acceptance criteria:

- end-to-end fake batch runs entirely offline;
- global and provider concurrency limits are proven by barriers/counters;
- exact unavailable tool blocks with zero alternative-provider calls;
- all worker writes remain in isolated scratch;
- BatchResult enumerates every item;
- executor terminal state is only `awaiting_agent_review`.

### Phase 2 — Local durability, cache, retry, resume, and cost

Deliverables:

- LocalStore, exclusive lease/fencing, immutable blobs, CAS state;
- typed error classification, fake clock full-jitter retry, cancellation;
- verified cache and restart reconstruction;
- coordinator cost reservation/reconciliation with schema-valid persistence;
- deterministic media probes and crash-injection harness.

Acceptance criteria:

- all cache corruption and request-conflict tests fail closed;
- second coordinator is rejected/fenced;
- crash at every defined local commit boundary resumes without lost state;
- no paid-ambiguous fake call is automatically repeated;
- concurrent reservations never exceed the approved cap;
- 40-item fake performance targets pass.

### Phase 3 — Canonical publication, checkpoints, and Backlot

Deliverables:

- coordinator-only validated artifact publication helper;
- formal `in_progress` checkpoint heartbeat integration;
- Agent-controlled result-to-artifact promotion flow;
- Backlot execution-state/progress linkage and authority consistency;
- history/decision-log crash behavior hardened or explicitly bundled.

Acceptance criteria:

- all checkpoint writes go through `write_checkpoint` and validate on read;
- fenced execution/commit-only writer epochs are mutually exclusive; workers cannot write artifacts/checkpoints/events/cost state;
- execution success alone cannot produce `awaiting_human` or `completed`;
- after Agent review, a gate without valid broad approval produces `awaiting_human`; `completed` requires either a new human reply or a still-in-scope recorded `approval_policy`, with the Agent supplying the decision evidence;
- terminal V2 publication suppresses the legacy checkpoint GCS hook; no background writer mutates the artifact after return;
- no unknown storage fields enter canonical artifacts;
- checkpoint/current-pointer authority is published before any derived loose cache, and Backlot never shows a staged draft or new-artifact/old-approval mix.

### Phase 4 — GCS durable store

Deliverables:

- GCSStore with conditional create, stat/get/materialize, CAS, leases, checksums, and typed errors;
- immutable namespace and private receipts;
- explicit dependency pinning;
- storage-aware checkpoint persistence design implemented without duplicating gate logic;
- fake/emulator GCS parity tests.

Acceptance criteria:

- success is impossible before a verified object generation receipt;
- upload-success/state-failure restart reuses the blob and does not regenerate;
- generation conflicts fail closed on digest mismatch;
- no background upload is part of the success path;
- no canonical schema mutation or public-by-default object behavior;
- local and GCS backends pass one conformance suite;
- no real GCS is required for this phase's default CI.

### Phase 5 — Cloud Run packaging, still fake-only

Deliverables:

- reproducible non-root Batch V2 container;
- signal handling and stable exit codes;
- Cloud profile preflight and explicit ADC/Secret Manager routing;
- infrastructure runbook/templates, but no automatic deployment.

Acceptance criteria:

- local container executes a full fake 40-item batch with LocalStore and FakeGCS;
- image contains no credential/project media and runs read-only except scratch;
- Windows/local-container digest and result semantics match;
- Gemini Vertex ambient ADC path is unit-tested with fake credentials;
- Cloud Run real deployment remains blocked pending explicit user approval.

### Phase 6 — User-approved external validation

Sequence:

1. approved real GCS prefix test;
2. approved Cloud Run fake-tool job;
3. approved one-item real provider sample;
4. approved 6–10 item concurrency pilot;
5. optional separately approved 40-shot benchmark.

Acceptance criteria:

- every tier has a recorded approval payload and hard cost/attempt stop;
- exact announced route/model equals the observed attempt record;
- GCS objects are private, checksummed, generation-bound, and resumable;
- Cloud job uses service identity/ADC where supported;
- no duplicate paid call due to retry or storage failure;
- measured performance/cost/error data is attached to the implementation review;
- any indeterminate outcome stops escalation to the next tier until resolved.

### Phase 7 — Merge, rollout, and legacy retirement

Deliverables:

- opt-in V2 rollout and migration documentation;
- final test/performance evidence;
- merge to `team-main` after review;
- later, separate legacy-runner retirement commit.

Acceptance criteria:

- all Definition of Done items pass on the merged commit;
- V2 has completed an offline/fake representative post-merge run and resume exercise; any new real GCS, Cloud Run, or provider execution has a fresh, run-specific approval payload;
- rollback to legacy remains documented and tested before retirement;
- legacy runner is not deleted in the V2 merge commit;
- retirement occurs only after the merged V2 acceptance window and explicit confirmation;
- baseline tag and Git history remain intact.

## 20. Migration and rollback

### 20.1 Migration sequence

1. Keep `scripts/batch_run_intent_sequences.py` unchanged and available.
2. Introduce V2 behind an explicit command/profile; no default pipeline routing change.
3. Convert the historical 40-shot definitions into schema-valid, no-media test fixtures. Do not rewrite historical project truth in place.
4. Run request validation and fake-tool shadow execution against copied/test project roots.
5. Compare expected item mapping, outputs, costs, and checkpoint progression without provider calls.
6. Perform approved live validation in a new project/run namespace.
7. Merge V2 to `team-main` only after review and acceptance.
8. Observe at least one offline/fake representative merged V2 run and recovery path. If this observation uses real GCS, Cloud Run, or a provider, obtain a new immediate approval payload and cost cap for that exact run; Phase 6 approval is not reusable.
9. Retire the legacy runner by a separate ordinary commit only after explicit confirmation.

### 20.2 Rollback

- Disable V2 opt-in routing/configuration.
- Continue using the untouched legacy runner during the coexistence window.
- Preserve V2 run namespaces and receipts for audit; do not mutate canonical artifacts during rollback.
- Revert individual V2 integration commits normally if required; do not rewrite shared history or remove the safety tag.
- If retirement has already merged, restore the legacy runner through a normal revert/cherry-pick from Git history, not a destructive reset.
- GCS rollback changes only current pointers/config; immutable blobs remain until the approved lifecycle policy removes them.

### 20.3 Compatibility constraints

- Legacy auto-sync stays available outside V2 until separately migrated.
- V2's suppression of legacy writers must be execution-context scoped.
- Existing checkpoint/artifact versions stay readable.
- New control contracts are versioned independently and have migration readers before any breaking change.
- Mixed local/GCS authority for the same batch is forbidden; one profile/store owns a batch ID.

## 21. Risks and mitigations

| Risk | Impact | Mitigation / release gate |
|---|---|---|
| Python drifts into orchestration | Violates core architecture and hidden creative behavior | Static responsibility tests; one-stage immutable request; Agent-only promotion/gates |
| False cache hit | Wrong clip attached to a scene | Full digest, source bindings, media probe, immutable receipt/generation |
| Paid duplicate after timeout/crash | Unexpected spend and duplicate assets | Pre-dispatch journal; accepted/unknown phase; `indeterminate` no-auto-replay |
| Provider quota burst | 429s, bans, low throughput | Hierarchical permits/token buckets, Retry-After, provider-specific qualification |
| Gemini global-state race | Credential/DNS instability | Cap=1 until global mutation removed and concurrency tests/live pilot pass |
| Hidden GCS/event writer | Lost updates and premature publication | Scoped suppression; workers outside project tree; coordinator-only persistence |
| GCS upload acknowledged too late | Cloud task exits with lost result | Synchronous receipt barrier, checksum, generation, no background success path |
| GCS overwrite/split brain | Stale or mixed results | Immutable blobs plus CAS pointer/lease/fencing |
| Schema-invalid `gcs_url` mutation | Checkpoint/read failure and Backlot inconsistency | Locator sidecar; schema validation after every publication |
| Backlot loose-artifact precedence | New artifact shown with old approval | Staging namespace; digest-equal promotion; authority/commit marker tests |
| Cost race/invalid cost_log | Budget oversubscription or invalid canonical state | Coordinator reservation; schema reconciliation; crash tests |
| Approval evidence mismatch | Spend without valid consent | Fail-closed binding to manifest-derived prerequisite checkpoints, proposal where present, and decision digests |
| `approval_policy` enum mismatch | Full-run approval cannot be canonical | Phase 0 schema/protocol reconciliation |
| Machine-specific credentials | CI and Cloud behave differently | Injectable resolver; standard ADC; remove hard-coded paths/project |
| Missing Cloud dependency | Image fails at runtime | Pinned dependency/container smoke test |
| Path traversal/symlink alias | Read/write outside project | Shared identity resolver and per-path containment tests |
| Provider/model drift | Announced path differs from actual call | Freeze observed route/model; preflight mismatch fails |
| Incomplete checkpoint transaction | Decision/checkpoint split | Single coordinator, crash matrix, eventual bundle/current-pointer protocol |
| Performance target conflicts with safety | Unsafe concurrency/retries | Correctness/cost gates precede speed; provider cap raised only with evidence |

## 22. Definition of Done

Batch Executor V2 is done only when all statements are true:

### Architecture and contracts

- [ ] One shared engine powers local and Cloud Run profiles.
- [ ] Executor accepts only immutable, schema-valid, full-digest BatchRequests for one stage.
- [ ] Agent-Native responsibility tests prohibit DAG/stage choice, prompt derivation, review, selector/fallback, and gate decisions in Python.
- [ ] Exact tool/provider/route/model observed at runtime matches what the Agent announced and the request binds.
- [ ] `approval_policy` and cost-log schema inconsistencies are resolved canonically.

### Correctness and durability

- [ ] Workers only write isolated attempt scratch and return messages.
- [ ] One fenced coordinator epoch at a time owns every shared/canonical mutation, including Agent-authorized terminal publication.
- [ ] LocalStore and GCSStore pass a shared conformance suite.
- [ ] Item success requires digest/probe/storage receipt and durable state.
- [ ] GCS uses immutable private objects, verified checksums, generations, and conditional writes.
- [ ] Cache hits verify complete identity and bytes.
- [ ] Crash/restart tests pass at every commit boundary.
- [ ] Possibly accepted paid calls become `indeterminate` and are never auto-replayed.

### Pipeline integrity

- [ ] Canonical artifacts validate through `validate_artifact`.
- [ ] Checkpoints are written/read through official interfaces.
- [ ] `in_progress` uses coordinator-coalesced `metadata.partial_progress`.
- [ ] Execution success stops at `awaiting_agent_review`.
- [ ] Agent review precedes terminal publication; gate-specific human evidence—either a new reply or a valid recorded full-run policy—precedes `completed`.
- [ ] V2 terminal publication suppresses legacy background sync and leaves no post-return artifact mutation.
- [ ] Backlot prefers V2 checkpoint/current-pointer authority and never displays staged/unreviewed artifacts or a new-artifact/old-approval mix as canonical state.
- [ ] No storage locator is injected into a schema that does not declare it.

### Security and operations

- [ ] No machine-specific credential path or project fallback remains in supported V2 providers.
- [ ] Cloud GCS and Vertex use attached service identity/ADC where supported.
- [ ] API-key routes use explicitly approved Secret Manager injection.
- [ ] Container is reproducible, pinned, non-root, and contains no secrets/media.
- [ ] Logs/results pass redaction tests.
- [ ] Stable exit codes, signal handling, cost accounting, and runbooks exist.

### Tests and performance

- [ ] All mandatory no-cost mock/fake tests pass on Windows, Linux CI, and the local container.
- [ ] Baseline test harness uses writable temp storage; the Gemini portability failure is fixed, not suppressed.
- [ ] 40-item fake benchmark meets concurrency/overhead/speedup targets.
- [ ] Separately approved real GCS, Cloud fake-job, single-provider sample, and concurrency pilot evidence pass.
- [ ] No unapproved external call, deployment, or spend occurs in CI.

### Rollout

- [ ] V2 remains opt-in until representative validation completes.
- [ ] Rollback is tested and documented.
- [ ] V2 is reviewed and merged to `team-main` before legacy retirement.
- [ ] The legacy runner is removed only in a separate confirmed commit.
- [ ] `team-main-pre-batch-v2` and normal Git recovery remain intact.

## 23. Merge and retirement workflow

1. **Plan commit:** this document only, on `codex/batch-v2`.
2. **Plan review gate:** user approves or requests revisions. No implementation before approval.
3. **Implementation commits:** small, phase-aligned commits; contracts/tests before behavior.
4. **Audit evidence:** attach offline matrix, crash tests, container test, and any separately approved external evidence.
5. **Integration review:** verify diff from baseline, Agent-Native self-review, security/cost review, and rollback steps.
6. **Merge:** merge `codex/batch-v2` into `team-main` through the repository's normal review workflow.
7. **Post-merge validation:** run an offline/fake representative V2 path and verify resume/Backlot/cost state. Any real GCS, Cloud Run, or provider run requires a new, immediate approval for that exact execution and cannot inherit a Phase 6 approval.
8. **Retirement proposal:** explicitly confirm the acceptance window and rollback readiness.
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
| Could workers become competing writers? | No | Coordinator-only mutation and fencing acceptance gates |
| Is an ambiguous paid outcome represented honestly? | Yes | `indeterminate`, retained cost exposure, explicit re-approval |
| Does the plan preserve the assets Human Gate? | Yes | Agent review; then either `awaiting_human` or Agent-authenticated in-scope full-run approval, never executor judgment |

Self-review conclusion: the proposed executor stays within **tools + persistence**. It accelerates and hardens execution of an Agent-authored decision; it does not replace the Agent as orchestrator, creative director, reviewer, or gatekeeper.

## 25. Decisions requested from the user

Approval of the overall Plan is requested before implementation. The following defaults are recommended; changes can be recorded as Plan revisions:

1. **Initial scope:** `assets` stage, independent video-generation work items only.
2. **Global concurrency:** default 3, configurable 1–4.
3. **Gemini concurrency:** 1 until credential/thread-safety qualification, then raise to 2 before considering 3.
4. **Cloud topology:** one process in one Cloud Run Job task; no array jobs.
5. **Cloud identity:** attached service account/ADC for GCS and Vertex; API keys only for an explicitly selected Developer route.
6. **Storage:** private content-addressed GCS objects plus generation-bound receipts; no public-by-default URLs and no `gcs_url` schema mutation.
7. **Paid ambiguity:** no automatic replay when provider acceptance is unknown.
8. **Lifecycle:** execution ends at `awaiting_agent_review`; the Agent owns terminal status/approval decisions and one fenced commit coordinator physically writes them.
9. **Contract fixes:** add canonical support for `approval_policy` and make CostTracker output schema-valid before V2 relies on them.
10. **Live validation:** each real GCS, Cloud Run, and provider tier receives a separate exact approval and cost cap.

Cloud project/region, bucket/prefix/retention, exact initial provider route/model, and live-test dollar caps are intentionally deferred until the corresponding external phase and must not be inferred by implementation code.

---

**Planning stop condition:** after this document is committed, work stops. Batch V2 implementation, Cloud Run deployment, real GCS mutation, and real/paid provider calls require subsequent user approval under the phase gates above.
