# Batch Executor V2 M3 Cloud profile

This is an offline packaging and operations contract for the single-task MVP.
It is not deployment authorization. Building or pushing an image, mutating a
real bucket, starting a Cloud Run Job, resolving real ADC, or invoking Vertex
requires the separate approvals listed under M5 in the implementation plan.

## Frozen execution shape

The Cloud profile is one coordinator process in one task. The job definition
must retain all three controls:

- `taskCount: 1`
- `parallelism: 1`
- `maxRetries: 0`

These settings do not establish cross-execution ownership. The durable
ExecutionOwner and proof-before-generation-CAS protocol remain authoritative.
No age, heartbeat, missing log, retry topology, or caller-authored status JSON
permits takeover.

The only production adapter identity in M3 is:

```text
tool      gemini_omni_video
provider  gemini_omni
route     vertex_interactions
model     gemini-omni-1.1-flash-preview
operation text_to_video
```

The frozen runtime and adapter documents explicitly bind request digest,
project, batch, route, model, Vertex project, and `global` location. ADC only
authenticates GCS, Vertex, and the exact Cloud Run execution lookup. An ambient
ADC project never selects or changes routing, and there is no Developer API or
model fallback. Every production work item also freezes `store: true`; without
that durable Interactions identity the adapter fails preflight before dispatch.

## Image inputs and offline checks

`Dockerfile.batch-v2` intentionally has no default base image. An approved
build must provide a Python 3.10 base by immutable registry digest and an exact
Debian ffmpeg package version. Direct Python dependencies are pinned in
`requirements-batch-v2.txt`; `constraints-batch-v2-py310.txt` freezes the full
Python 3.10 resolution. The Dockerfile itself fails the build before package
installation unless `PYTHON_BASE_IMAGE` ends in an exact lowercase, 64-hex
`@sha256:` digest; a mutable tag alone is never accepted. The build record must
retain the resolver's install report and image digest.

The repository-root `.dockerignore` is a default-deny build context. Only the Dockerfile inputs
(`lib/`, `schemas/`, `pipeline_defs/`, `scripts/batch_execute.py`,
`scripts/batch_publish.py`, and the two pinned dependency files) are explicitly
includable. Secret/environment files,
credentials, project media, generated outputs, caches, test artifacts,
worktrees, and editor/OS noise remain excluded even if they appear below an
otherwise allowed source directory. Builds must use the repository root as
their context so this boundary is effective; preparing a broader or alternate
context requires a separate security review.

The following checks are local and make no external call:

```powershell
python -m pytest tests/batch_executor/test_m3_packaging.py -q --basetemp=.pytest-tmp-m3-packaging
python -m ruff check lib/batch_executor scripts/batch_execute.py tests/batch_executor
```

The M3 container gate remains pending, rather than waived, when the Docker
daemon, digest-pinned base image, or pinned package cache is unavailable. After
an explicit later approval provides those inputs, the reproducible build shape
to qualify is:

```text
docker build --file Dockerfile.batch-v2 \
  --build-arg PYTHON_BASE_IMAGE=python:3.10.18-slim-bookworm@sha256:<approved-digest> \
  --build-arg FFMPEG_APT_VERSION=<approved-bookworm-version> \
  --tag <local-name> .
```

Do not substitute an unqualified base tag in a release record. Do not put
`.env`, service-account JSON, project media, caches, or developer paths in the
build context through additional `COPY` instructions.

## Materialized workspace and inputs

Before process launch, GCS FUSE exposes only an immutable content-addressed
input snapshot at:

```text
/input-snapshot/  (only-dir=batch-v2-input-snapshots/sha256/<full-sha256>)
```

The mount is read-only. It contains `projects/<project-id>/` with the exact
hash-bound project snapshot needed by project/checkpoint/source preflight,
including matching `project.json`, plus the frozen launch config. At startup,
the entrypoint copies that project into the container's non-FUSE, ephemeral,
non-root-writable `/workspace/projects/<project-id>/` tree without overwriting
different bytes. Symlinks, junctions, hard-link aliases, and `.batch-v2` input
state are rejected/ignored as appropriate. The configured snapshot prefix and
the writable project root must be disjoint.

The publication entrypoint additionally omits snapshot `assets/` and
`checkpoint_assets.json` while materializing. Those canonical stage outputs
can appear only after publication proof and ownership CAS, and are restored
from exact GCS publication authority rather than trusted from FUSE input.

This split is a correctness boundary: direct GCSStore publication owns object
names below `projects/<project-id>/...`; no local/FUSE path maps to those object
names. A local canonical write therefore cannot alias the same object later
created and generation/checksum/metadata-verified through the GCS API. The
executor neither discovers a project from ADC nor reconstructs missing
creative state.

The frozen runtime config uses `/workspace/projects` as `projects_root`,
`/input-snapshot/projects` as `input_snapshot_projects_root`, and binds the
full content-addressed `input_snapshot_object_prefix`.
Workers receive only paths under:

```text
/workspace/projects/<project-id>/.batch-v2/runs/<batch-id>/attempts/<item-id>/<attempt-id>/
```

No tool output uses `/tmp`, the repository, or canonical `assets/`,
`artifacts/`, `renders/`, checkpoint, event, or cost paths. GCSStore separately
persists immutable request/result records, generation-CAS state, ownership
proofs, and verified private content-addressed outputs. A successful item waits
for upload completion plus exact generation, byte size, client SHA-256,
provider CRC32C, metadata, and read/head verification. It produces no public or
signed URL.

The config and request locations must be explicit, private, unsigned paths. A
configuration file is self-digested and binds its request URI/digest. The job
template expects the config at `/input-snapshot/config/runtime-config.json`.
The request itself
may be an exact private `gs://` URI in the configured bucket.

For offline LocalStore/FakeGCS equivalence only, a request may freeze
`storage_profile: portable`. That value lets the identical canonical request
bytes and digest pass through either execution profile; the separately frozen
runtime config still selects exactly `local` or `cloud_run`. Production launch
uses its explicit profile and does not treat `portable` as provider, model, or
storage discovery.

Once an image has been built from already available, approved inputs, its fake
40-item qualification uses one prepared host workspace and the same portable
request. No credential or network access is permitted:

```text
docker run --rm --network none \
  --mount type=bind,src=<prepared-workspace>,dst=/workspace \
  <local-image-digest> run --profile local \
  --config /workspace/config/local.json \
  --request-uri /workspace/config/request.json

docker run --rm --network none \
  --env CLOUD_RUN_JOB=batch-v2 \
  --env CLOUD_RUN_EXECUTION=fake-container-execution \
  --env CLOUD_RUN_TASK_INDEX=0 \
  --env CLOUD_RUN_TASK_COUNT=1 \
  --env CLOUD_RUN_TASK_ATTEMPT=0 \
  --mount type=bind,src=<prepared-workspace>,dst=/workspace \
  <local-image-digest> run --profile cloud-run \
  --config /workspace/config/cloud-fake.json \
  --request-uri /workspace/config/request.json
```

Both runtime configs use `transport_mode: offline_fake`. Their results must
have the same request digest, item transitions, accounting, and stable exit
category. M3 records the static container checks when no approved base image is
locally available; it does not pull one merely to run this command.

## First run and resume

First execution:

```text
python /opt/openmontage/scripts/batch_execute.py run \
  --profile cloud-run \
  --config /input-snapshot/config/runtime-config.json \
  --request-uri gs://<private-bucket>/<immutable-request-object>
```

Cloud Run supplies the execution name and task facts. The frozen config supplies
a unique invocation ID. The launch resolver rejects a job-name mismatch, task
index other than zero, task count other than one, or platform attempt other
than zero.

A different active owner blocks ordinary `run`. Resume is explicit and uses
exactly one of these paths:

```text
resume --resume-proof-kind control-plane
resume --resume-proof-kind human-authorization \
  --resume-proof-uri gs://<private-bucket>/<immutable-authorization-object>
```

The first path performs one ADC-authenticated GET for the exact recorded Cloud
Run execution and accepts only terminal/cancelled evidence. The second validates
an immutable, one-time ResumeAuthorization that binds the prior owner, proposed
successor, request, generation, evidence/reply, and timestamp. Only then may a
generation-bound owner CAS occur. The winner is re-read exactly before any
dispatch; every loser makes no provider call. A crashed active owner remains a
blocker without one of those proofs.

## Exit and cancellation contract

The entrypoint emits one redacted JSON summary containing an exit category and,
when known, the durable result locator. It does not print credentials, headers,
signed URLs, prompts, or provider bodies.

- `0`: durable BatchResult; inspect its outcome
- `2`: request/contract/authorization failure before execution side effects
- `3`: configuration/auth/storage/ownership blocker
- `4`: durable item failure result
- `5`: durable indeterminate paid-call result
- `6`: cancellation recorded durably
- `10`: internal failure

SIGINT or SIGTERM sets the shared cancellation event. The coordinator stops new
dispatch, reconciles already returned facts, writes cancellation/ambiguity state
through the same generation CAS path, and exits when safe. Platform timeout must
leave enough termination grace for that bounded reconciliation; a hard-killed
owner remains active and requires proof-gated resume.

Execution stops at `awaiting_agent_review`. This entrypoint cannot choose a
stage/provider/model, issue a PublicationCommand, publish canonical media,
advance a checkpoint, or satisfy an Agent/Human Gate. Those remain the separate
Agent-native publication lifecycle.

After the Agent has reviewed the exact GCS BatchResult and authored and
separately persists a frozen `PublicationCommand`, the dedicated
`scripts/batch_publish.py` composition root invokes the separate
`CloudAssetsPublisher` boundary. The production root constructs the concrete
ADC GCS transport and `CloudRunADCExecutionStatusVerifier`; objects with only a
spoofed public verifier name are not trusted. Its command URI, object
generation, full-byte SHA-256, and command self-digest must all be supplied
separately and match the frozen config. It requires exact
request/state/result object generations and digests, independent terminal or
cancelled execution proof (or one command-bound Human publication
authorization), and a re-read generation-CAS publication claim before any
canonical mutation. It stages only below the materialized project's hidden
`.batch-v2/runs/<batch-id>/publication/` tree, publishes canonical media first,
uses the official checkpoint writer/reader last, and synchronously verifies the
corresponding private workspace GCS objects. The later `completed` transition
still requires a second immutable command bound to an explicit Human Gate reply.
This boundary is intentionally absent from `batch_execute.py` so execution can
never auto-review or auto-publish.

For the Human-authorization proof path, the launch must likewise supply the
exact immutable authorization URI, GCS generation, full-byte SHA-256, and
authorization self-digest. The root never synthesizes that authorization. Its
self-digest proves canonical integrity and binding; it does **not** by itself
authenticate a Human identity. Trust in the explicit Agent/Human approval
workflow and immutable object placement/IAM is a separate launch prerequisite.

The checked-in publication Job template is the control-plane-proof shape. Its
fully bound invocation is:

```text
python /opt/openmontage/scripts/batch_publish.py publish \
  --config /input-snapshot/config/publication-runtime-config.json \
  --command-uri gs://<bucket>/<immutable-command-object> \
  --command-generation <exact-generation> \
  --command-sha256 <full-object-bytes-sha256> \
  --command-digest <command-self-digest>
```

An explicitly reviewed Human-authorization launch adds all four fields; a
partial set fails before publication:

```text
  --authorization-uri gs://<bucket>/<immutable-authorization-object> \
  --authorization-generation <exact-generation> \
  --authorization-sha256 <full-object-bytes-sha256> \
  --authorization-digest <authorization-self-digest>
```

The project/assets publication fence permanently binds the MVP canonical stage
to one batch/request, while the batch-scoped PublicationState records finite
ownership and ordered recovery. Neither is a renewable lease. The official
`checkpoint_assets.json`, written/read through the official checkpoint APIs,
is the canonical lifecycle commit authority. PublicationState is its
ownership/recovery journal: if a process stops after the checkpoint commit but
before the journal CAS, an exact same-command retry verifies/adopts the GCS
checkpoint and repairs the journal; that window is not interpreted as an
uncommitted or bypassed Human Gate.
