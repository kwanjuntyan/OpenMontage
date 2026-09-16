# Production Unit Protocol M6 qualification record

> Current status (2026-09-16): **M6.0A follow-up review-ready candidate**. This record
> describes contract closure only. It is not beta or production qualification.

## Scope completed in M6.0A

M6.0A separates two previously conflated axes:

| Axis | Canonical values | Location |
|---|---|---|
| Approved project policy | `off`, `auto`, `fixed` | `proposal_packet.production_plan.production_unit_policy.mode` |
| Stage execution disposition | `compare_only`, `publish_candidate` | bounded PUP helper execution contract |

The legal mapping is:

- missing policy or `mode=off` → strict no-op, no disposition;
- `auto|fixed` + a stage in `enabled_stages` → an explicitly selected
  `compare_only|publish_candidate` disposition supported by that helper;
- missing policy with a disposition, `off` with a disposition, mixed legacy
  and canonical arguments, disabled stages, and unsupported dispositions fail
  closed;
- `publish_candidate` means only “return a validated candidate to the owning
  director.” It grants no checkpoint, Human Gate, provider, filesystem,
  Batch V2, render, or external publication authority.

The M2-M5 helper keyword `mode="compare_only|publish_candidate"` remains a
deprecated compatibility alias. Reports now add `policy_mode`,
`policy_mode_authority`, `execution_disposition`, the complete digest-bound
`execution_contract`, and `execution_contract_sha256`; the old report `mode`
key is retained temporarily as an execution-disposition alias. New callers
must use the canonical two-axis arguments.

The legacy alias synthesizes `policy_mode="auto"` only to preserve M2-M5 helper
behavior. Its report is explicitly marked
`policy_mode_authority="none_legacy_diagnostic"` and
`legacy_mode_alias_used=true`; neither its synthesized mode nor disposition is
approved/effective policy. The canonical helper path reports
`policy_mode_authority="validated_proposal_checkpoint_required"`, which is a
requirement, not proof: the resolver validates shape but does not read a
checkpoint. The only trusted approved-policy source is the validated,
human-approved proposal checkpoint.

## Qualification contracts

The versioned producer-side contracts are:

- `schemas/execution/production_unit_qualification_profile.schema.json`
- `schemas/execution/production_unit_capability_matrix.schema.json`

A profile binds the exact Git commit, pipeline manifest, schemas, adapters,
pipeline/content form/stages, runtime/composition mode, provider/model/asset
route, media profile, OS/runtime/hardware, evidence digests, status, and
requalification triggers. The safe status vocabulary is:

- `unknown`
- `unsupported`
- `experimental`
- `code_complete`
- `beta_qualified`
- `production_qualified`
- `disabled`
- `invalid`

The capability matrix is only a digest-bound projection of exact profiles.
`pipeline_manifest.extensions.production_units.supported: true` remains an
implementation-capability declaration and never upgrades qualification.

M6.0A validators operate only on caller-supplied in-memory documents. They do
not provide canonical discovery, dereference `profile_ref`, select a winning
profile, bind `manifest_supported` to an actual validated manifest, read
evidence bytes, authenticate evidence digests, or replay M6 gates. Therefore a
validated `beta_qualified`/`production_qualified` shape is still a
producer-authored assertion until the later trust-root and qualification
harness verify it.

Synthetic interface fixtures (not qualification evidence):

- `tests/fixtures/production_units/m6_0a_qualification_profile.fixture.json`
- `tests/fixtures/production_units/m6_0a_capability_matrix.fixture.json`

Reusable invalid consumer fixtures:

- `invalid/m6_0a_stale_profile_digest.fixture.json`
- `invalid/m6_0a_selector_drift.fixture.json`
- `invalid/m6_0a_status_drift.fixture.json`
- `invalid/m6_0a_beta_insufficient_evidence.fixture.json`

All paths above are below `tests/fixtures/production_units/`. The matrix
fixtures intentionally exercise the current supplied-document validator; they
do not imply that `profile_ref` is safe to dereference.

## Consumer-review follow-up disposition

| GPT B finding | M6.0A follow-up decision | Owner / target | Capability claim now |
|---|---|---|---|
| Canonical discovery location, loader, resolver | Deferred | Track A / M6.1 before live qualification projection | Schema/fixture-driven integration only; no live discovery |
| `profile_ref` containment, traversal, symlink trust | Deferred with loader | Track A / M6.1 | Opaque display reference only; consumers must not dereference |
| Multiple selector matches | Deferred with resolver | Track A / M6.1 | No effective-profile selection claim |
| Missing profile/matrix → `unknown` executable result | Deferred with resolver | Track A / M6.1 | Consumer presentation default only |
| Evidence bytes/digest/gate-result verification | Deferred | Track A / M6.1 offline qualification harness | Shape and required-kind validation only; no authenticity claim |
| Actual manifest binding for `manifest_supported` | Deferred with resolver | Track A / M6.1 | Matrix boolean is non-authoritative without validated manifest |
| Shared invalid fixtures | Fixed in this follow-up | Track A / M6.0A | Stale digest, selector/status drift, and insufficient beta evidence are reusable |
| Canonical source for each live selector field | Deferred with resolver | Track A / M6.1 | No live selector matching claim |
| Operational policy `off` vs profile status `disabled` presentation | Deferred presentation policy | Track B / D2-D4 | They remain separate axes and must not share an effective-state badge |

Track B owns presentation policy for these degraded/unknown states. It does
not own producer discovery, trust, selection, evidence verification, or
manifest binding.

## Evidence snapshot

Base commit: `bdce618f7554468ee3a652a84724ba1bd9ae173b`

Baseline in the clean M6 worktree:

- `python -m pytest tests/production_units -q`: 80 passed
- `python -m pytest tests/backlot/test_course_projection.py -q`: 7 passed

M6.0A initial candidate (`6478309`):

- `python -m pytest tests/production_units -q`: 106 passed
- checkpoint/pipeline offline regression (pipeline catalog and manifest,
  checkpoint read/prerequisite, canonical-stage compatibility): 70 passed
- Backlot course projection regression: 7 passed

M6.0A consumer-review follow-up candidate:

- focused contract/script/course-routing tests: 50 passed
- `python -m pytest tests/production_units -q`: 110 passed
- `python -m pytest tests/backlot/test_course_projection.py -q`: 7 passed

All tests used explicit short `--basetemp` paths under
`D:\kj-openMontage\.pytest-tmp`. No provider, network, deployment, GCS,
media-generation, push, or merge action was performed.

## Capability claim boundary

M6.0A may claim:

- canonical vocabulary closure with a backward-compatible helper seam;
- strict default-off and fail-closed mapping tests;
- versioned qualification/profile matrix shapes and exact binding for
  caller-supplied trusted documents;
- no change to canonical artifacts, checkpoint chain, Human Gates, Batch V2
  ownership, or Backlot writer authority.

M6.0A may not claim:

- durable candidate-to-checkpoint handoff/recovery qualification (M6.0B);
- physical media qualification (M6.0C);
- 3/8/15/30/60 offline matrix completion (M6.1);
- a real provider-backed 60-minute beta profile (M6.2);
- production qualification or rollout (M6.3);
- general proof that 180 seconds is optimal.
- canonical profile/matrix discovery, trusted `profile_ref` dereference,
  effective profile selection, evidence authenticity, replayed gate results,
  or actual-manifest binding.

## Interface handoff for GPT B

GPT B may project the synthetic fixtures after the review commit, but must
remain observer-only.

- approved policy mode: `off|auto|fixed`, read only from the validated approved
  proposal checkpoint;
- execution disposition: `compare_only|publish_candidate`, safe for consumer
  projection only from the canonical resolver path with
  `legacy_mode_alias_used=false`;
- legacy helper reports: diagnostic only when
  `policy_mode_authority="none_legacy_diagnostic"`; never establish an
  approved/effective policy badge;
- qualification status: the eight-value safe status vocabulary above;
- project policy `off` and qualification status `disabled` are different
  axes; consumers must not collapse them into one badge;
- support signal: `manifest_supported` is independent of qualification;
- supplied-document identity binding: `profile_id + profile_version +
  profile_sha256`; it is not live discovery authority;
- selector: pipeline, content form, stages, runtime, composition mode, asset
  route, provider, model, and media profile;
- diagnostics: use the matrix `reason`; do not infer success from
  `supported: true`;
- backward-compatible presentation default: no profile/matrix means `unknown`;
  M6.0A has no executable resolver for that rule. Missing approved PUP policy
  still means disabled/off on the canonical path;
- `profile_ref` is opaque; Backlot must not dereference it;
- qualification status and `manifest_supported` are producer assertions until
  later evidence/manifest trust binding;
- unstable until M6.0B review: durable coordinator state, candidate handoff,
  aggregate stage/unit progress, recovery/epoch fields, and checkpoint
  provenance references.

## Next review-gated slice

M6.0B should define and fault-test the canonical candidate handoff and minimum
durable recovery seam. It must not revive the old mega-RFC wholesale, add a
second publisher/approval system, modify Backlot ownership, call providers, or
perform a merge without separate approval.
