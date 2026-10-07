---
name: ai-video-asset-designer
description: Plan, design, and maintain reusable visual assets for AI-video projects from project-local context and authorized source materials. Use after project-context initialization to inventory and prioritize characters, environments, props, costumes, vehicles, creatures, graphics, style references, and variants; decide which need images, text-only definitions, or temporary descriptions; assign stable internal keys and human-readable asset IDs; create or update asset plans and production lists; write or revise copy-ready prompts for ChatGPT Image 2 or Nano Banana Pro; diagnose generated results; and generate images only when the user explicitly asks and a callable image tool is available. Do not use to build project context, write storyboard prompts, or write video-motion prompts.
---

# AI Video Asset Designer

## Overview

Use this Skill as one independent asset workflow for an AI-video project. It combines asset planning, production-list maintenance, copy-ready visual-asset Prompt writing, and Prompt revision. The normal upstream is an initialized project library from `ai-video-project-context`; exact facts still require the original script or client source.

The Skill writes only two project-local Markdown files:

- `visual-assets/资产规划.md`
- `visual-assets/资产生产清单.md`

Full Prompt text remains in the conversation and is never written to those files by default.

## Resource Map

Read references progressively:

1. Always read `references/project-input-contract.md` before locating project inputs.
2. Read `references/asset-planning-rules.md` for planning, ID assignment, variant design, or production-list updates.
3. Read `references/asset-prompt-rules.md` and `references/output-format-qa.md` for Prompt writing or revision.
4. Read `references/chatgpt-image-2-adapter.md` for the default ChatGPT Image 2 output.
5. Read `references/nano-banana-pro-adapter.md` only when the user explicitly specifies Nano Banana Pro.

Do not load unrelated project files, old workflow state, archived material, or other projects.

## Task Selection

Use the planning workflow when the user asks to:

- identify or organize characters, environments, props, costumes, vehicles, creatures, graphics, or style assets;
- decide which assets must be designed first;
- create or revise `资产规划.md` or `资产生产清单.md`;
- map recurring assets, variants, states, reference images, or continuity requirements.

Use the Prompt workflow when the user asks to:

- write a character, scene, prop, costume, vehicle, creature, graphic, style-reference, or asset-editing Prompt;
- produce the next approved batch of asset-image Prompts;
- revise a Prompt from a generated-image problem or reference image.

Use the explicit-generation branch only when the user clearly asks to generate an image and a callable image-generation tool is available. A Prompt-only request never triggers image generation.

Do not build the project library, write storyboard-frame Prompts, write video-motion Prompts, rewrite the script, or change upstream project-context files in this Skill. For project-library work, direct the user to `$ai-video-project-context`.

## Core Workflow

### 1. Locate and preflight

1. Resolve the project root from an explicit user path, the current project directory, or the nearest directory containing the project-context file roles. Apply the Chinese-primary filename map and legacy-English fallback in references/project-input-contract.md.
2. Read a present project `AGENTS.md` and obey it, but do not require the 11-Skill `_project_state.md`.
3. Read only the project-context files selected by that filename map and the original source ranges needed for the requested scope. Preserve the actual filenames in source references.
4. Read existing `visual-assets/资产规划.md` and `visual-assets/资产生产清单.md` before updating them.
5. Classify every important input as source fact, confirmed design, proposed visual design, or unknown/conflict.

If the request is project-wide and the project library is missing, do not rebuild it here. Explain the missing input and direct the user to `$ai-video-project-context`. A bounded single-asset request may proceed only when the user supplies enough explicit, confirmed asset information.

### 2. Plan assets

1. Extract reusable or continuity-critical assets.
2. Separate image-reference assets, text-only definitions, and one-off elements that can remain inline in a later scene Prompt.
3. Assign P0, P1, or P2 production priority.
4. Assign an immutable internal key such as `A0001` and a human-readable asset ID.
5. Keep base identity separate from episode, day/night, costume, injury, wetness, damage, lighting, or other variants.
6. Record narrative/visual function, required views and states, reference roles and priority, source ranges, consistency relationships, approval needs, and missing decisions.
7. When visual details are missing, propose a clearly marked design direction instead of presenting it as canon.
8. Write or update the two project Markdown files with the planning scope and current status `待确认`.
9. Show the planning summary and production list in the conversation. Do not write formal Prompts until the user confirms the relevant scope.

### 3. Produce Prompt batches

After the user confirms all information that blocks the selected assets, or explicitly supplies and confirms a bounded single-asset specification:

1. Read the confirmed asset rows and only the source material needed for them.
2. Build an internal platform-neutral Prompt specification.
3. Adapt it to ChatGPT Image 2 by default, or to Nano Banana Pro only when explicitly requested.
4. Run the Prompt QA rules.
5. Process at most five assets per batch, in P0 to P1 to P2 order.
6. Give each asset a Prompt ID such as `A0002-P01` and a batch ID such as `B001`.
7. Update only Prompt metadata and status in `资产生产清单.md`; never write the full Prompt.
8. Output one complete, independent Prompt per asset in its own `text` code block.
9. End with the delivered Prompt IDs and ask whether to continue the next batch or revise the current batch.

The code block must contain only text intended for the image model. Put explanations, assumptions, model labels, Prompt IDs, and QA notes outside the block. Do not use “same as above”; every Prompt must work when copied alone.

### 4. Revise

When a user reports a generated-image problem:

1. Identify the smallest cause: identity drift, state drift, reference-role confusion, material error, composition error, unwanted element, or style mismatch.
2. Separate what must remain unchanged from what may change.
3. Make a local revision when possible and increment the Prompt version.
4. Output the complete revised Prompt in a fresh copyable code block.
5. Update the production-list metadata without saving the Prompt body.

### 5. Generate only on explicit request

When explicitly asked to generate an image:

1. Confirm the target asset, model, references, and requested output.
2. Submit only the current asset Prompt and user-selected reference images to the available image tool.
3. Never submit the complete script or project library.
4. If the requested model is unavailable, say so instead of substituting silently.
5. Report the actual result and write a result path only when one exists.
6. If the tool returns only a conversation image, mark the item `已生成，待用户保存/命名`.

## Source and Safety Boundaries

- Original scripts, client materials, explicit user decisions, and confirmed project rules outrank project-library summaries.
- Never invent canon, relationships, colors, materials, or continuity facts.
- Never convert a proposed design into a source fact without user confirmation.
- Never read another project, `旧版/`, archived material, or another task's chat history.
- Never put project-specific facts, client names, complete scripts, private references, or generated assets inside this Skill repository.
- Never modify project-context files, old 11-Skill state files, or installed Skill copies.
- Never create duplicate Chinese and English project-context files; if both names exist for one role, stop that role and request an authority decision.
- Never generate storyboard-frame Prompts, numbered shots, durations, camera movement, performance direction, or video-motion Prompts.
- Never call a generation API or image tool without an explicit user request.

## Maintenance

Keep workflow routing and hard boundaries in this file. Keep schemas, asset-planning rules, Prompt construction, model adapters, and QA in the directly linked references. When model documentation changes, update only the relevant adapter and record its verification date; do not change the platform-neutral asset data model.
