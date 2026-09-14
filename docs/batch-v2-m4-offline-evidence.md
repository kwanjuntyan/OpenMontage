# Batch Executor V2 M4 offline evidence

Candidate baseline: `9a171db03bdeb52400571d671d259db8e3d8eddc`.

- M3: in_progress
- M4: in_progress
- No production qualification is claimed.

This record covers only offline code preparation. Linux CI and the actual
dual-profile 40-item local-container run have not yet executed, so neither M3
nor M4 is complete or code-complete under the approved Plan.

## Implementation-diff review

The M4 slice is limited to:

- the legacy-facing Gemini Omni credential/routing/download boundary and its
  offline tests;
- Python 3.10 CI configuration and a dedicated Linux test-process isolation
  launcher;
- one missing declared legacy dependency;
- provider configuration documentation;
- opt-in migration/rollback rehearsal and this evidence.

No engine, execution schema, publication, or Cloud Run template change is in
scope. The accepted legacy runner remains byte-identical. The change does not
add a scheduler, provider selector, generic transport platform, distributed
lease, cross-file transaction, or wider Backlot behavior.

## Test-first and mock/fake evidence

The Gemini and M4 release contracts were added before their implementations.
The initial targeted runs failed on the absent injectable ADC contract and on
all seven missing release-gate deliverables. Qualification uses injected HTTP
transport/token fakes, existing LocalStore/FakeGCS/provider/status fakes,
parser/dispatch stubs, and deterministic fixture media only. No test in this
slice needs or authorizes real credentials, a provider, GCS, Cloud Run, Docker,
or paid work.

The handoff must attach exact results for these local commands:

```text
python -m pytest tests/tools/test_gemini_omni_video.py tests/tools/test_gemini_omni_portability.py tests/batch_executor/test_m0_contracts.py -q --basetemp=.pytest-tmp/m4-gemini
python -m pytest tests/batch_executor -q --basetemp=.pytest-tmp/m4-batch
python -m pytest tests/batch_executor tests/contracts/test_phase0_contracts.py tests/contracts/test_checkpoint_read_gate.py tests/lib/test_checkpoint_prerequisites.py tests/lib/test_checkpoint_noncanonical_stage.py -q --basetemp=.pytest-tmp/m4-canonical
python -m pytest tests/tools/test_base_tool_dependencies.py tests/lib/test_gcs_auto_sync.py -q --basetemp=.pytest-tmp/m4-base-gcs
python -m pytest tests/backlot tests/contracts/test_backlot_contract.py -q --basetemp=.pytest-tmp/m4-backlot
```

Observed in the uncredentialed Windows test process for this candidate:

| Gate | Result |
|---|---:|
| Complete final combined offline matrix above, plus both Gemini test files | 605 passed, 4 platform-permission skips |
| Earlier isolated `tests/batch_executor` harness classification | 453 passed, 3 platform-permission skips; final coverage repeated in the combined gate |
| Canonical checkpoint/artifact regression | 48 passed |
| BaseTool/GCS legacy regression | 12 passed |
| Backlot regression | 57 passed, 1 platform-permission skip |
| Gemini tool + portability + M0 contracts | 55 passed |
| Final M4 release + Gemini focused slice | 52 passed |
| Ruff on all touched Python | passed |
| Execution schemas, Draft 2020-12 | 11 passed meta-validation |
| Repository Git policy tree scan | passed |
| Rollback parser/dispatch stub rehearsal | passed; zero provider/canonical calls |
| Linux gate shell definition | syntax passed locally; namespace execution pending Linux CI |

The first full Batch V2 attempt used a nested `--basetemp` before its
repository-local parent existed. Pytest reported 144 passes and 312 setup
errors, all the same Windows `WinError 3` parent-path failure and no product
assertion failure. After explicitly creating `.pytest-tmp`, the unchanged test
set produced 453 passes and three platform link-permission skips. This is a
test-harness path issue, not a waived product failure. The combined run removed
all provider credential names declared by `.env.example`, removed known Google
route/project aliases, set `OPENMONTAGE_ALLOW_NETWORK=0`, and ran under the
repository pytest socket guard.

The dedicated Linux workflow installs lower-bound test requirements first,
then invokes `scripts/run_batch_v2_linux_offline_gate.sh`. Those requirements
are not a resolved dependency lock. The launcher contract fail-closes unless
`unshare`, `setpriv`, and the required network tools work; name-scans tracked,
untracked, and gitignored workspace content while safely pruning dependency and
test sandboxes; and rejects `.env`, known credential names, and key material
without reading or printing candidate contents or paths.

The isolated test process uses dedicated UID/GID `65532:65532`,
`no_new_privs`, and empty bounding/inheritable/permitted/effective/ambient
capability sets. It dynamically requires `sudo -n true` to fail. Route and
interface commands must themselves succeed before their captured output is
evaluated. `HOME`, `TMPDIR`, and pytest basetemp are separately created sibling
directories beneath one fresh repository-local gate root, and a real tempfile
plus before/after runtime checks prove pytest cannot prune the other two.
Before pytest the dropped process hashes Git config/hook state around the
actual legacy `-B ... --help` invocation and fails on mutation; `-B` is not
claimed to suppress non-bytecode side effects. This test-process isolation is
inherited by subprocesses. The checkout and dependency installation may use
network; the repository does not claim the complete CI lifecycle is offline.
All Linux namespace/drop assertions remain unobserved until the GitHub Linux
job runs, so M4 remains in progress.

## Agent-Native responsibility review

- The Agent still authors the canonical request, chooses the pipeline/stage,
  performs creative review, and presents Human Gates.
- Python accepts only the caller's explicit route/model/project/location. ADC
  authenticates an already-selected Vertex route and cannot select it.
- The tool does deterministic request/response handling only. It cannot choose
  a fallback, advance a stage, publish a checkpoint, or approve a result.
- Execution/publication separation and the exact provider concurrency cap of
  one are unchanged.
- The rollback rehearsal invokes only parser/dispatch stubs and therefore does
  not disguise generation or canonical publication as a test.

## Security and cost review

- `GeminiOmniVideo` contract version `0.2.0` exposes the new exact route/model
  identity. Developer API remains the explicit default.
- Vertex requires explicit model, project, and location; its lazy injectable
  resolver uses standard ADC without an implicit project or key-file search.
- `get_status()` performs no ADC lookup, network operation, or private-path
  probe. No module mutates global DNS/socket state or caches credentials.
- A Vertex Bearer token is sent only to the explicit interaction endpoint or a
  validated HTTPS `googleapis.com` download host. Redirects are explicitly
  disabled for both the initial POST and output GET, and response
  URI/token/body data is redacted from failures. Malicious URI tests assert
  zero download calls.
- Developer API key and local-video calls also disable redirects and require an
  explicit 2xx response. The resumable upload URL is accepted only as HTTPS on
  a `googleapis.com` host with no userinfo and no non-443 port before any local
  bytes are sent. Remote response bodies, payload data, URIs, and exception
  text are mapped to redacted route/operation errors.
- The Gemini provider concurrency cap remains one. No charged request ran, and
  no budget/cost semantics changed.
- CI checkout does not persist Git credentials; the isolated test process
  inherits neither credentials nor a user configuration home.

The registered legacy-facing `GeminiOmniVideo` minor version is intentionally
distinct from Batch V2's independently frozen M0/M3 adapter contract. The
executor uses `GeminiOmniVertexAdapter` and its schema-bound `0.1.0` identity;
this M4 slice does not rewrite execution schemas or silently migrate frozen
requests. Any future convergence requires an explicit versioned request/schema
migration rather than reporting the new legacy-tool behavior under `0.1.0`.

## Pending environment evidence

The current Windows environment can establish offline unit/fake evidence but
cannot establish the repository-version Linux namespace result or the required
local-container dual-profile 40-item result. Those gates remain pending, not
waived. No Docker daemon, image dependency, external service, or credential was
probed during this slice.

## M5 publication trust prerequisite

Production IAM/topology must make the publication identity the unique writer
for the canonical asset/checkpoint, publication fence, and publication-state
namespaces. The legacy and executor identities have no write permission to those
namespaces. Recorded generations needed by the approved recovery window must
remain available under the bucket's versioning/retention policy.

Any protocol-external mutation invalidates qualification evidence. If the
deployment cannot guarantee unique-writer IAM, qualification remains blocked
pending a new threat-model and architecture review. Exact
`latest-head == recorded-generation` checks at every relevant publication
mutation/return boundary are a minimum detection requirement, not sufficient
protection against another identity that retains canonical write permission.
That topology must first adopt immutable canonical objects plus a
generation-CAS pointer, or a separately reviewed protocol proven equivalent,
and then repeat qualification. Recorded-generation retention remains a
separate prerequisite: the recorded generations required by the recovery
window must remain readable. These are external M5 prerequisites, not blockers
attributable to the accepted M3 commit, and M4 does not implement them.
