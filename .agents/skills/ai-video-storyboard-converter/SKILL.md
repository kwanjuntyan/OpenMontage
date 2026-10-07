---
name: ai-video-storyboard-converter
description: Convert a located script excerpt plus project requirements into approximately 15-second AI video storyboard prompts with strict dialogue fidelity, timing, visual style, performance, shot-level spatial and prop continuity, and QA. Use when Codex needs to generate, continue, revise, or inspect numbered storyboard segments for a specified episode, scene, paragraph, page, or excerpt. Do not use to summarize full scripts, build project context files, or answer broad plot, character, or worldbuilding questions.
---

# AI Video Storyboard Converter

## Overview

Use this skill only to convert an explicitly located script range into approximately 15-second AI video storyboard prompts.

It consumes the original script excerpt, project requirements, and any existing project-local context. It does not build project context, summarize long scripts, or create project notes.

Keep concrete client projects, scripts, character names, palettes, and output examples out of this skill. Store project-specific material in the user's project folder.

## Preflight Gate

Complete this gate before reading any large converter reference.

1. Decide whether the request belongs to this skill.
   - Use this skill for a located excerpt that must be generated, continued, locally revised, or checked as an approximately 15-second numbered storyboard segment.
   - Route long-script reading, project-library work, project notes, indexing, and broad plot, character, relationship, setting, worldbuilding, or project-wide continuity questions to `$ai-video-project-context`; do not read converter references merely to make that handoff.
   - For a mixed request, finish and verify project-context work first, then handle only an explicitly located script range here.
2. Confirm the minimum source material for the requested operation.
   - Formal generation, continuation, content-affecting revision, and dialogue-fidelity checking require a locatable original script range.
   - Continuation also requires the previous segment's complete storyboard, especially its final shot and ending state.
   - Revision requires the current segment and its `[Context Lock - Do Not Render]`; if dialogue or story content may change, the original script range is also required.
   - A supplied storyboard may be inspected for format, timing, camera, performance, or continuity within the available evidence. Without the original script, do not claim dialogue/source fidelity or generate missing story content.
3. If required material is missing, request the exact excerpt, range, previous segment, current segment, or Context Lock and stop. Do not load large references only to refuse or request material.

## Conditional Resource Map

After the Preflight Gate passes, read only the references required by the task:

- `references/main-converter-rules.md` (`main`): source scope, priorities, dialogue fidelity, segment capacity, and conversion boundaries.
- `references/camera-performance-rules.md` (`camera`): shot action, blocking, performance, continuity staging, and camera geometry.
- `references/output-format-qa.md` (`output`): exact output shell, field responsibilities, timing, dialogue coverage, continuity checks, and delivery QA.
- `references/anti-contamination-rules.md` (`anti`): specialized cross-project contamination, old-format rollback, sample-leakage, and rule-inheritance audits.
- `references/seedance-2.0-rules.md` (`seedance`): additive rules only for an explicitly specified Seedance 2.0 task.

| Task | Required references |
| --- | --- |
| Formal new segment | `main` + `camera` + `output` |
| Continue the next segment | `main` + `camera` + `output` |
| Local format, dialogue, or timing revision | `main` + `output`; add `camera` if shot structure, blocking, performance, props, Context Lock, or continuity can change |
| Format, dialogue, or timing QA only | `main` + `output` |
| Camera, performance, blocking, or geometry QA only | `main` + `camera`; add `output` when checking Context Lock, props, full continuity, or returning a revised formal segment |
| Contamination or old-format audit | `main` + `output` + `anti`; add `camera` only when the audit includes shot or performance contamination |
| Seedance 2.0 | Add `seedance` to the corresponding route above |
| Skill maintenance | Read `SKILL.md` and only the references whose routing or rules may change; read `seedance` only when maintaining its adapter |

The ordinary production safety contract remains authoritative in `SKILL.md`, `main`, `camera`, and `output`. Do not load `anti` for routine production after its core checks have been confirmed in those files. Every delivered formal storyboard must load `output` and pass its applicable internal QA. A camera-only audit that only lists issues may omit `output`; add it before returning a revised formal storyboard.

## Storyboard Conversion Workflow

1. Complete the Preflight Gate, then load the route selected from the Conditional Resource Map.
2. Read relevant project-local context when available. Accept Chinese-first and legacy English project-context filenames by role, do not rename or update them here, and never let them override the original script.
3. Apply the priority order in `main`, generate only the requested range, and preserve original dialogue exactly in `「」`.
4. Use approximately 15-second numbered shots with integer durations whose sum equals the title duration; use a natural shorter duration only when `main` permits it.
5. Preserve the exact formal shell and `[Context Lock - Do Not Render]` defined by `output`.
6. Run the QA required by the selected route before delivery. Do not print an internal checklist unless the user asks.

## Formal Delivery Gate

Before returning a formal segment, inspect the final answer itself and confirm that these top-level fields appear once and in this order: title, `【约束铁律】`, `整体视频采用`, `场景设定`, `角色`, `空间站位备忘`, `道具设定`, `[Context Lock - Do Not Render]`, then one or more numbered shots.

For every numbered shot, require `时间长度`, `景别`, `构图`, `机位运动`, `画面内容`, and `台词`. Do not deliver until all required fields are present, dialogue matches the located source, and integer shot durations equal the title duration. Repair the draft before responding if any check fails.

Do not state an internal rule-file version unless the user asks. Git release metadata is authoritative; reference headings are not version declarations.

## Hard Boundaries

- Never build or update project briefs, script overviews, character bibles, worldbuilding glossaries, episode indexes, style-rule files, or continuity-note files.
- Never answer broad script-analysis questions from this skill; route them to `$ai-video-project-context`.
- Never write storyboard prompts from memory, summaries, or guessed dialogue when the original script text is unavailable.
- Never add plot events, dialogue, props, color values, character facts, or worldbuilding unsupported by the current script or project materials.
- Never treat a sample project, previous conversation, old output, or one client preference as a universal rule.
- Never put specific project content into this skill during maintenance.
- Never replace `[Context Lock - Do Not Render]` with another field name.
- Never omit numbered shot fields or integer shot durations in formal storyboard output.

## Maintenance Guidance

When improving this skill:

- Put workflow-level routing and hard boundaries in `SKILL.md`.
- Put conversion boundaries and priority changes in `references/main-converter-rules.md`.
- Put cinematic shot, blocking, performance, dialogue reaction, action, suspense, power dynamics, continuity staging, and camera geometry in `references/camera-performance-rules.md`.
- Put output shell, field responsibilities, timing checks, dialogue coverage, continuity checks, and delivery QA in `references/output-format-qa.md`.
- Put cross-project contamination, old-format rollback, sample leakage, and rule-inheritance risks in `references/anti-contamination-rules.md`.
- Do not add long-script understanding, project-context building, project-file schemas, or broad script-Q&A rules to this skill.

After significant changes, validate the skill structure and test at least one short dialogue conversion and one continuity-sensitive storyboard revision.
