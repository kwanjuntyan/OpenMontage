# Production Unit Protocol M6 qualification record

> Current status (2026-09-16): **M6.0A review-ready candidate**. This record
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
`execution_disposition`, the complete digest-bound `execution_contract`, and
`execution_contract_sha256`; the old report
`mode` key is retained temporarily as an execution-disposition alias. New
callers must use the canonical two-axis arguments.

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

Synthetic interface fixtures (not qualification evidence):

- `tests/fixtures/production_units/m6_0a_qualification_profile.fixture.json`
- `tests/fixtures/production_units/m6_0a_capability_matrix.fixture.json`

## Evidence snapshot

Base commit: `bdce618f7554468ee3a652a84724ba1bd9ae173b`

Baseline in the clean M6 worktree:

- `python -m pytest tests/production_units -q`: 80 passed
- `python -m pytest tests/backlot/test_course_projection.py -q`: 7 passed

M6.0A candidate:

- `python -m pytest tests/production_units -q`: 106 passed
- checkpoint/pipeline offline regression (pipeline catalog and manifest,
  checkpoint read/prerequisite, canonical-stage compatibility): 70 passed
- Backlot course projection regression: 7 passed

All tests used explicit short `--basetemp` paths under
`D:\kj-openMontage\.pytest-tmp`. No provider, network, deployment, GCS,
media-generation, push, or merge action was performed.

## Capability claim boundary

M6.0A may claim:

- canonical vocabulary closure with a backward-compatible helper seam;
- strict default-off and fail-closed mapping tests;
- versioned qualification/profile matrix shapes and exact digest binding;
- no change to canonical artifacts, checkpoint chain, Human Gates, Batch V2
  ownership, or Backlot writer authority.

M6.0A may not claim:

- durable candidate-to-checkpoint handoff/recovery qualification (M6.0B);
- physical media qualification (M6.0C);
- 3/8/15/30/60 offline matrix completion (M6.1);
- a real provider-backed 60-minute beta profile (M6.2);
- production qualification or rollout (M6.3);
- general proof that 180 seconds is optimal.

## Interface handoff for GPT B

GPT B may project the synthetic fixtures after the review commit, but must
remain observer-only.

- approved policy mode: `off|auto|fixed`;
- execution disposition: `compare_only|publish_candidate`;
- qualification status: the eight-value safe status vocabulary above;
- support signal: `manifest_supported` is independent of qualification;
- exact authority: `profile_id + profile_version + profile_sha256`;
- selector: pipeline, content form, stages, runtime, composition mode, asset
  route, provider, model, and media profile;
- diagnostics: use the matrix `reason`; do not infer success from
  `supported: true`;
- backward-compatible default: no profile/matrix means `unknown`; missing PUP
  policy still means disabled/off;
- unstable until M6.0B review: durable coordinator state, candidate handoff,
  aggregate stage/unit progress, recovery/epoch fields, and checkpoint
  provenance references.

## Next review-gated slice

M6.0B should define and fault-test the canonical candidate handoff and minimum
durable recovery seam. It must not revive the old mega-RFC wholesale, add a
second publisher/approval system, modify Backlot ownership, call providers, or
perform a merge without separate approval.
