# Batch Executor V2 M4 offline evidence

Accepted M3 functional baseline: `9a171db03bdeb52400571d671d259db8e3d8eddc`.
M3 completion was accepted at
`b471851eac6ab3bfea399d874e3f6c8116188d8d` after the real resolver, image,
and dual-profile local-container gates described below.

The original Windows M4 offline matrix was observed on committed parent
`8e298cbb068131452cb82bfc44c66cdca05dbe7a` plus the final local-path
redaction implementation/test blobs below. Those blobs were committed before
the M3 lock correction and remain as the historical binding for that run.

```text
tools/video/gemini_omni_video.py
  SHA-256 035c8b3b6fa6d7516acc5686876c2a285226699a4690fe7b69ecef7c41c405a5
tests/tools/test_gemini_omni_portability.py
  SHA-256 54a87a2b0d7d79103caff4691663f17bec5976cafa863594261cb499188f5692
scripts/batch_v2_ci_preflight.py
  SHA-256 fc7de69166986b99dead01f9fb36e9f4e73a3210111f43b031f039d2fc3f7123
tests/batch_executor/test_m4_release_gate.py
  SHA-256 fe725fa327132a0a2a2745d2c4ff0836daa1c3c8c6f28a83d73b969d093f5a5c
```

- M3: completed
- M4: in_progress
- No production qualification is claimed.

M3 completion covers the reviewed code plus local, fake-only container
qualification. M4 remains `in_progress`: the GitHub Linux namespace/drop gate
remains pending. Nothing here qualifies a real provider, ADC identity, GCS
bucket, Cloud Run deployment, image push, or paid operation.

### M3 CPython 3.10 lock correction and completed container qualification

The coordinating root performed the first real M3 image build from committed
`2f9beca81d20a432dc5a1f0102c10b35f63b8047` with these frozen inputs:

```text
python:3.10.18-slim-bookworm@sha256:445b9efb2c047a7ccdb30d293fd6b1aa0f62a55062dc2b69051df91e10848749
linux/amd64 manifest sha256:b4d66d07136c546f1765eae2bfcce9a64fa95f37c717c02bedd06d0476d1dbbd
ffmpeg 7:5.1.9-0+deb12u1
```

The base and ffmpeg steps succeeded, but pip stopped with
`ResolutionImpossible`: `jsonschema==4.26.0` requires `rpds-py>=0.25.0`, while
the original `rpds-py==2026.5.1` pin requires Python 3.11 or newer. Git history
shows that the constraint file was introduced in `ec03ce8` without a generator
or retained resolver report. Its complete 27-package set matches the current
Python 3.13 development environment, so that host freeze was not valid Python
3.10 provenance.

A marker/dependency-closure audit of all exact pins found the other 26 pins
compatible with Python 3.10 and no missing or incompatible runtime dependency.
In a separate real dry-run without constraints on the same CPython 3.10/Linux
amd64 base, pip selected the available `rpds-py==0.30.0` cp310 manylinux wheel.
The correction candidate pins that version and adds a CI setup command that
runs pip's real
`--no-cache-dir --dry-run --ignore-installed --only-binary=:all:` resolver,
then validates the complete exact report and every artifact SHA-256. This
network-enabled dependency-resolution gate precedes, and is distinct from, the
later no-egress pytest process. Offline tests validate the report checker and
workflow contract; they do not claim current package-index availability.

At `b471851eac6ab3bfea399d874e3f6c8116188d8d`, the coordinating root reran
the hardened verifier with real package-index access in the digest-pinned
CPython 3.10.18/Linux amd64 container. The exact command included
`--no-cache-dir`; it completed with
`Batch V2 lock resolved ...: 27 distributions`, and all 27 selected artifacts
were binary wheels.

The corrected image then built successfully with these observed facts:

| Image/build fact | Accepted observation |
|---|---|
| Base index digest | `sha256:445b9efb2c047a7ccdb30d293fd6b1aa0f62a55062dc2b69051df91e10848749` |
| Linux amd64 base manifest | `sha256:b4d66d07136c546f1765eae2bfcce9a64fa95f37c717c02bedd06d0476d1dbbd` |
| ffmpeg build argument and container dpkg version | `7:5.1.9-0+deb12u1` |
| Local image ID / RepoDigest binding | `sha256:6c16f916ab2b07a53e166022cfbf73b4698520dc6ec14fa8b234b403bb017717` |
| Runtime platform | `linux/amd64` |
| Declared user | Config.User `65532:65532` |
| Dynamic identity | UID/GID `65532:65532` |
| Entrypoint | `batch_execute.py` |
| Python dependency health | `pip check`: `No broken requirements found.` |
| Docker build context | `7.11 kB` |

The image filename inventory contained no credential or environment files,
project media, or project assets. The `7.11 kB` application build-context
payload contained only the allowed `lib/`, `schemas/`, `pipeline_defs/`,
`batch_execute.py`, `batch_publish.py`, and the two Batch V2 dependency files.

The deterministic qualification fixture contained 40 items and request digest
`febe67479a3ff3ad75c40385a4829e02eb506158c0b6f50dd0ce8e112b962d42`.
Both container runs used `--network none`:

- LocalStore exited `0` with `all_succeeded`: 40 successful, zero failed,
  blocked, or indeterminate items; 40 attempts, zero retries; every item was
  `committed`; status was `awaiting_agent_review`; durability was
  `local_workspace`.
- The FakeGCS Cloud profile exited `0` with the same request digest, counts,
  cost facts, transitions, outcome, and stable exit semantics. Its deliberate
  qualification-only durability was `process_memory` and `result_locator` was
  null. It was rerun once with the same fixture solely to capture stdout; both
  runs used no real external resource.

This completes M3's approved local-container qualification boundary. The
package/image build may use registry and package-index network, but the two
runtime qualifications had no network. No provider, ADC, real GCS, Cloud Run,
or paid action was involved, and the user's `team-main` changes remained
untouched.

## Implementation-diff review

The M4 slice is limited to:

- the legacy-facing Gemini Omni credential/routing/download boundary and its
  offline tests;
- Python 3.10 CI configuration and a dedicated Linux test-process isolation
  launcher;
- a fail-closed real CPython 3.10/Linux x86_64 dependency resolver/report gate;
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

The handoff attaches exact results for these local commands:

```text
python -m pytest tests/tools/test_gemini_omni_video.py tests/tools/test_gemini_omni_portability.py tests/batch_executor/test_m0_contracts.py -q --basetemp=.pytest-tmp/m4-gemini
python -m pytest tests/batch_executor -q --basetemp=.pytest-tmp/m4-batch
python -m pytest tests/contracts/test_phase0_contracts.py tests/contracts/test_checkpoint_read_gate.py tests/lib/test_checkpoint_prerequisites.py tests/lib/test_checkpoint_noncanonical_stage.py -q --basetemp=.pytest-tmp/m4-canonical
python -m pytest tests/tools/test_base_tool_dependencies.py tests/lib/test_gcs_auto_sync.py -q --basetemp=.pytest-tmp/m4-base-gcs
python -m pytest tests/backlot tests/contracts/test_backlot_contract.py -q --basetemp=.pytest-tmp/m4-backlot
python -m pytest tests/batch_executor/test_m4_release_gate.py tests/tools/test_gemini_omni_video.py tests/tools/test_gemini_omni_portability.py -q --basetemp=.pytest-tmp/m4-focused
```

The complete combined command uses the union of all paths above (with the
canonical, BaseTool/GCS, Backlot, and both Gemini paths added to
`tests/batch_executor`). Observed in the uncredentialed Windows test process
for the tested tree identified above:

| Gate | Result |
|---|---:|
| Complete final combined offline matrix | 625 passed, 5 platform/environment skips |
| Isolated `tests/batch_executor` | 463 passed, 4 platform/environment skips |
| Canonical checkpoint/artifact regression | 48 passed |
| BaseTool/GCS legacy regression | 12 passed |
| Backlot regression | 57 passed, 1 platform-permission skip |
| Gemini tool + portability + M0 contracts | 66 passed |
| Final M4 release + Gemini focused slice | 72 passed, 1 Linux-gate-only skip |
| Ruff on all touched Python | passed |
| Execution schemas, Draft 2020-12 | 11 passed meta-validation |
| Repository Git policy tree scan | passed |
| Rollback parser/dispatch stub rehearsal | passed; zero provider/canonical calls |
| Linux gate shell definition | Git Bash syntax passed locally; namespace/drop execution pending Linux CI |

Immediately before adding the two case-insensitive `*.env` name-only
regressions, the same candidate boundary produced 623 passed and 5 skips in
the complete matrix, 461 passed and 4 skips for `tests/batch_executor`, and 70
passed with 1 skip in the M4/Gemini slice. The final rows above supersede those
intermediate counts and include both new tests; they are not Linux CI evidence.

An earlier candidate's nested `--basetemp` run failed only because its
repository-local parent did not exist. The current commands explicitly created
that parent and completed without setup errors; the earlier condition remains
classified as a Windows harness-path issue, not a waived product failure. The
combined run removed all provider credential names declared by `.env.example`,
removed known Google route/project aliases, set
`OPENMONTAGE_ALLOW_NETWORK=0`, and ran under the repository pytest socket
guard.

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
- Missing or unreadable local video/reference inputs are also mapped to a fixed
  local-input validation category; caller filesystem paths and underlying
  exception text are not returned in `ToolResult.error`.
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

The M3 local-container dual-profile 40-item gate is now accepted as recorded
above. The GitHub Linux namespace/drop gate remains pending, not waived; the
current Windows environment cannot establish that repository-version Linux
isolation result. The image build used ordinary registry/package dependency
access, while both qualification containers used `--network none`. No external
provider, ADC credential, real GCS service, Cloud Run deployment, image push,
or paid operation was used.

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
