# CLP Director - Animated Explainer Pipeline

## When To Use

You are extracting and establishing Character, Location, and Prop (CLP) visual consistency specifications for an animated explainer video.

## Explainer-Specific Strategy: Zero-Entity vs Hero Assets

Unlike narrative cinematic films which almost always require characters and locations, animated explainers fall into two distinct categories:

1. **Pure Topic / Abstract / Kinetic Explainers (Zero-Entity Path)**:
   - Concepts are explained via motion typography, abstract geometry, charts, or standard Remotion scene cards.
   - **Action**: Emit empty arrays for `characters: []`, `locations: []`, `props: []`.
   - **Gate Policy**: Write `status="completed"`, `human_approved=false`; the
     checkpoint writer emits and validates the top-level typed evidence
     `gate_resolution.mode="zero_entity_auto"`,
     `rule_version="clp_literal_empty_v1"`, exact zero counts, canonical
     manifest hash, and timezone-aware `resolved_at`. Do not hand-author or
     place this evidence under `metadata`.

2. **Mascot / Product / Architecture Explainers (Hero Asset Path)**:
   - Contains a recurring mascot character, specific system architecture diagrams, or tangible hardware devices.
   - **Action**: Extract candidates into `clp_candidates.json` sidecar, generate master visual reference images, assemble `clp_manifest.json`.
   - **Gate Policy**: Mandates human approval before proceeding to scene plan and asset generation.

## Artifact Contract

- Produces: `clp_manifest` (validates against `schemas/artifacts/clp_manifest.schema.json`).
- Sidecar: `clp_candidates` (validates against `schemas/artifacts/clp_candidates.schema.json`).
- Exact predecessor: load `state.artifacts["script"]["script"]`.
- Referential integrity: set `source_script_sha256` exclusively with
  `lib.clp_validator.canonical_digest(script)`; never hash pretty-printed file
  bytes or use another JSON serialization convention.

For an approved course-form proposal with explicit Production Unit mode, read
`skills/meta/production-unit-protocol.md`. Extract candidates only from the
assigned script-unit capsule and return the unchanged capsule digest. After
deterministic aggregation, the Agent must resolve every digest-bound local
candidate to a same-category final entity or explicitly ignore it. Duplicate
mentions may resolve to one entity; workers never resolve conflicts or publish
per-unit CLP manifests. The result is still exactly one course-wide
`clp_candidates` plus one canonical `clp_manifest`, reviewed and published by
the existing CLP checkpoint/Human Gate rules (including the unchanged literal
zero-entity auto path).

## Quality Bar

- Zero-entity explainers must emit schema-valid empty arrays (never omitting required fields).
- Hero assets must adopt **One Signature Look per Character/Prop** to guarantee visual continuity.
- No silent downgrades: entities with `policy: "strict_reference"` must have verified master images.
