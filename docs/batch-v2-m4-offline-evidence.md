# Batch Executor V2 M4 offline evidence

Accepted M3 functional baseline: `9a171db03bdeb52400571d671d259db8e3d8eddc`.
M3 completion was accepted at
`b471851eac6ab3bfea399d874e3f6c8116188d8d` after the real resolver, image,
and dual-profile local-container gates retained as historical evidence below.

Final M4 candidate after the transparent post-qualification security
correction:
`c77b2793876e3ee80f25a5d5233ed3d1f150ea67`.

- Pull request: [kwanjuntyan/OpenMontage#1](https://github.com/kwanjuntyan/OpenMontage/pull/1)
- Final successful workflow: [run 34934501232](https://github.com/kwanjuntyan/OpenMontage/actions/runs/34934501232)
- M3: completed
- M4: completed
- M5: not performed and not authorized
- No production qualification is claimed.

M4 completion covers the repository-version Python 3.10 validation and the
observed Linux namespace/privilege-drop/no-egress test-process gate. It does
not qualify a real provider, attached ADC identity, real GCS bucket, image
push, Cloud Run execution/deployment, or paid operation. Those are M5 actions
and remain outside this evidence. Batch V2 is therefore not production-qualified,
remains opt-in, and the legacy runner must not be retired.

## Final M4 GitHub evidence

All three jobs completed successfully for the exact final candidate and pull
request above:

| Job | GitHub evidence | Accepted result |
|---|---|---|
| Validate Python | [job 104269410842](https://github.com/kwanjuntyan/OpenMontage/actions/runs/34934501232/job/104269410842) | success: 2599 passed, 12 skipped, 3 xfailed, 1 warning, 1 subtest; 427.09s |
| Batch V2 Linux Offline Gate | [job 104269410637](https://github.com/kwanjuntyan/OpenMontage/actions/runs/34934501232/job/104269410637) | success: 659 passed, 1 skipped, 2 warnings; 260.30s; real CPython 3.10/Linux x86_64 resolver accepted 27 distributions |
| Repository Policy & Binary Shield Guard | [job 104269410858](https://github.com/kwanjuntyan/OpenMontage/actions/runs/34934501232/job/104269410858) | success |

The Linux job's dependency setup and real resolver ran before the isolation
boundary. The test process itself then ran under the repository's no-egress,
credential-free namespace and dropped-privilege contract. The successful job
is direct Linux evidence for those dynamic assertions, not an inference from
the historical Windows checks.

### Earlier accepted candidate (historical, superseded)

The earlier accepted M4 candidate was
`c5bc88e2fefa4db22b4e662fa52012d43586eab6`, with successful
[run 34931811296](https://github.com/kwanjuntyan/OpenMontage/actions/runs/34931811296).
It established the Linux isolation and M4 behavior available at that tree, but
it predates the post-qualification security correction below and is not the
exact final-candidate evidence.

| Job | Historical GitHub evidence | Historical result |
|---|---|---|
| Validate Python | [job 104261401724](https://github.com/kwanjuntyan/OpenMontage/actions/runs/34931811296/job/104261401724) | success: 2589 passed, 12 skipped, 3 xfailed, 1 warning, 1 subtest; 366.55s |
| Batch V2 Linux Offline Gate | [job 104261401886](https://github.com/kwanjuntyan/OpenMontage/actions/runs/34931811296/job/104261401886) | success: 649 passed, 1 skipped, 2 warnings; 217.47s; real CPython 3.10/Linux x86_64 resolver accepted 27 distributions |
| Repository Policy & Binary Shield Guard | [job 104261401871](https://github.com/kwanjuntyan/OpenMontage/actions/runs/34931811296/job/104261401871) | success |

### Fail-closed diagnosis chain

The three earlier workflow runs failed closed and were corrected before the
earlier accepted candidate, and their fixes remained covered by the final c77
rerun. None of their failures was skipped, waived, or reclassified as success:

- [Run 34926832790](https://github.com/kwanjuntyan/OpenMontage/actions/runs/34926832790)
  stopped when UID/GID `65532:65532` could not traverse/read the checkout, and
  Validate Python exposed an end-to-end fixture that checkpointed compose
  without the manifest-required real `final_review`. The correction granted
  least-privilege ACL traversal/read only, strengthened non-writable checkout
  and Git-metadata preflight, and exercised high-level render with its returned,
  schema-valid passing `final_review` and exact output-path binding.
- [Run 34928462269](https://github.com/kwanjuntyan/OpenMontage/actions/runs/34928462269)
  reached the dropped runtime assertion and stopped with only a generic exit
  `64`. Offline diagnosis and reproduction identified parsing of the valid
  blank Linux `Groups:` field. The correction then parsed only required
  `/proc/self/status` fields and added stable redacted diagnostic categories
  without exposing paths or values. Validate Python also exposed schema-valid
  `subtitles.style` strings being treated as mappings; the same correction made
  subtitle visual-style resolution compatible with the canonical string
  display mode.
- [Run 34929547674](https://github.com/kwanjuntyan/OpenMontage/actions/runs/34929547674)
  passed Linux isolation but stopped on two non-hermetic legacy GCS unit tests;
  Validate Python stopped on those plus two pre-existing Vox caption-contrast
  regressions. The correction installed test-local fake
  `google.cloud.storage` modules, selected caption bars by actual composited
  contrast, and hardened invalid-background selection with the c5 candidate's
  worst-case black/white maximin rule.

### Transparent post-qualification security correction

An independent full-diff audit after the c5 acceptance found one P2 in the
independently frozen Batch V2 M3 Vertex transport. Although redirects were not
followed, an interaction POST or polling GET returning a 3xx response with an
inline-video JSON body could be parsed as success. Commit
`4f71bb53987cd3cc4bf424838b8699ebaf277676` corrected that fail-open path:
only 2xx responses reach body parsing, and the focused in-memory regressions
cover `199`, `301`, `302`, `307`, and `308` for both submit and poll.
Unsupported `<200` or 3xx POST responses retain unknown provider acceptance as
`TIMEOUT_OR_NETWORK_UNKNOWN` with `mark_indeterminate`, so a possibly accepted
paid request is never automatically submitted again. Polling retains the exact
existing operation identity and uses `REMOTE_JOB_RECOVERABLE` rather than
starting another generation.

The final c77 candidate includes that correction and its tests. Run
34934501232 then passed all three final jobs with the exact results above. A
final independent security/cost/scope re-review of c77 found no remaining P0,
P1, or merge-blocking P2 in the reviewed runtime/security correction. One
non-blocking P2 test-coverage backlog remains: the rollback rehearsal's
automated opt-in guard checks only the legacy runner's direct string
references. A tree-wide audit found no current default V2 route; broadening
that automated guard remains follow-up hardening rather than an observed
runtime defect. Active-word highlight contrast remains a pre-existing,
byte-identical non-regression backlog item: the old and new caption-bar
selection is identical for the affected themes. Neither backlog blocked M4,
and neither was hidden or treated as fixed by this qualification.

## Historical Windows M4 evidence

The original Windows M4 offline matrix was observed on committed parent
`8e298cbb068131452cb82bfc44c66cdca05dbe7a` plus the final local-path
redaction implementation/test blobs below. Those blobs were committed before
the M3 lock correction and remain only as the historical binding for that run;
they are not the final Linux or c77 final-candidate evidence.

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

## Historical M3 CPython 3.10 lock correction and container qualification

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

The completed M4 and final-correction slice is limited to:

- the legacy-facing Gemini Omni credential/routing/download boundary and its
  offline tests;
- Python 3.10 CI configuration and a dedicated Linux test-process isolation
  launcher;
- a fail-closed real CPython 3.10/Linux x86_64 dependency resolver/report gate;
- one missing declared legacy dependency;
- provider configuration documentation;
- opt-in migration/rollback rehearsal and this evidence.

The only Batch V2 runtime modification after the earlier accepted candidate is
the narrow Vertex interaction transport non-2xx response check and its offline
tests. It does not change provider identity, concurrency, budget, or retry
contracts.

No engine, execution schema, publication, or Cloud Run template change is in
that final correction. The accepted legacy runner remains byte-identical and
must remain available; M4 completion does not authorize its retirement.
The change does not add a scheduler, provider selector, generic transport
platform, distributed lease, cross-file transaction, or wider Backlot
behavior.

## Historical Windows test-first and mock/fake evidence

The Gemini and M4 release contracts were added before their implementations.
The initial targeted runs failed on the absent injectable ADC contract and on
all seven missing release-gate deliverables. Qualification uses injected HTTP
transport/token fakes, existing LocalStore/FakeGCS/provider/status fakes,
parser/dispatch stubs, and deterministic fixture media only. No test in this
slice needs or authorizes real credentials, a provider, GCS, Cloud Run, Docker,
or paid work.

The historical Windows handoff attached exact results for these local commands:

```text
python -m pytest tests/tools/test_gemini_omni_video.py tests/tools/test_gemini_omni_portability.py tests/batch_executor/test_m0_contracts.py -q --basetemp=.pytest-tmp/m4-gemini
python -m pytest tests/batch_executor -q --basetemp=.pytest-tmp/m4-batch
python -m pytest tests/contracts/test_phase0_contracts.py tests/contracts/test_checkpoint_read_gate.py tests/lib/test_checkpoint_prerequisites.py tests/lib/test_checkpoint_noncanonical_stage.py -q --basetemp=.pytest-tmp/m4-canonical
python -m pytest tests/tools/test_base_tool_dependencies.py tests/lib/test_gcs_auto_sync.py -q --basetemp=.pytest-tmp/m4-base-gcs
python -m pytest tests/backlot tests/contracts/test_backlot_contract.py -q --basetemp=.pytest-tmp/m4-backlot
python -m pytest tests/batch_executor/test_m4_release_gate.py tests/tools/test_gemini_omni_video.py tests/tools/test_gemini_omni_portability.py -q --basetemp=.pytest-tmp/m4-focused
```

The complete combined command used the union of all paths above (with the
canonical, BaseTool/GCS, Backlot, and both Gemini paths added to
`tests/batch_executor`). Observed in the uncredentialed Windows test process
for the historical tested tree identified above:

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
| Linux gate shell definition | Git Bash syntax passed locally; final dynamic Linux execution is recorded separately above |

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

The successful dedicated Linux workflow installed lower-bound test requirements
first, then invoked `scripts/run_batch_v2_linux_offline_gate.sh`. Those test
requirements are not a resolved dependency lock; the separate real resolver
accepted all 27 exact CPython 3.10/Linux x86_64 distributions. The launcher
contract fail-closes unless `unshare`, `setpriv`, and the required network tools
work; name-scans tracked, untracked, and gitignored workspace content while
safely pruning dependency and test sandboxes; and rejects `.env`, known
credential names, and key material without reading or printing candidate
contents or paths.

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
The final GitHub job observed all of these checks on Linux and completed
successfully with the result bound above.

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
- The independently frozen Batch V2 Vertex transport accepts only 2xx
  interaction responses for body parsing. Unsupported informational/redirect
  responses use fixed redacted error facts; ambiguous paid POST acceptance is
  durable `indeterminate` state and cannot become an automatic generation
  replay.
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

## M4 completion boundary and excluded M5 actions

The historical M3 local-container dual-profile 40-item gate and the final M4
GitHub Linux gate are accepted only within the boundaries recorded above. The
image build used ordinary registry/package dependency access, both historical
M3 qualification containers used `--network none`, and the final M4 test
process used the no-egress namespace boundary. No external provider, attached
ADC credential, real GCS service, Cloud Run execution/deployment, image push,
or paid operation was used or authorized.

M4 is completed, but Batch V2 is still not production-qualified. M5 must
separately qualify the real GCS/IAM, image-push, Cloud Run, ADC, and provider
boundaries under immediate authorization. Until that work succeeds, V2 remains
opt-in and `scripts/batch_run_intent_sequences.py` remains the required legacy
rollback path; it must not be retired.

## M5 publication trust prerequisite

This section is an unexecuted M5 prerequisite, not evidence that M5 occurred.
Nothing in M3 or M4 authorizes real GCS mutation, an image push, Cloud Run, ADC,
or a paid provider call, and none of those actions is production-qualified by
the successful offline/fake gates.

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

Accordingly, M4 completion cannot retire the legacy runner or enable the Batch
V2 production profile. Those transitions require separately authorized and
successful M5 evidence.
