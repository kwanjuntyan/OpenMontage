---
name: gemini-omni
description: Generate, edit, and extend Gemini Omni 1.1 clips through Vertex AI with service-account JSON; supports references, first/last frames, integer duration and resolution.
allowed-tools: Bash, Read, Write
metadata:
  openclaw:
    requires:
      env_any:
        - GOOGLE_APPLICATION_CREDENTIALS
---

# Gemini Omni 1.1 Flash on Vertex AI

Use `gemini_omni_video`, model `gemini-omni-1.1-flash-preview`, in `global`.
Authentication is always `GOOGLE_APPLICATION_CREDENTIALS` service-account JSON.
Do not switch to API keys or gateway tools automatically. Use the project `.venv`.

Route generation, editing and extension through `video_selector` with
`preferred_tool="gemini_omni_video"`; the selector passes interaction state through.
A JSON credential indicates configuration, not verified account entitlement.

## Parameters

- `operation`: `text_to_video`, `image_to_video`, `reference_to_video`,
  `first_last_frame_to_video`, `edit_video` (alias `video_edit`), `extend_video`.
- `duration`: integer 3-10 seconds; legacy `"5"` / `"5s"` accepted, sent as `"5s"`.
- `resolution`: `360p`, `720p` (default), `1080p`, `4k`; aspect `16:9` / `9:16`.
- First frame: `reference_image_path`; final frame: `last_image_path`.
  Use exactly one of each with `first_last_frame_to_video` or `image_to_video`.
- References: `reference_image_paths`, `reference_video_paths`; URL counterparts
  also accepted. Local media goes inline; `gs://` media can be referenced directly.
- Editing/extension: `input_video_path` (aliases `video_path` / `video_url`),
  or `previous_interaction_id`. Prior interaction must have used `store=true`.
- `store` defaults true. Output defaults to inline MP4 bytes saved at `output_path`.
  Optional `gcs_uri` requests Cloud Storage output and downloads it using JSON auth.
- No streaming/background job layer is implemented. Do not resubmit a timed-out
  generation blindly; the provider might already have accepted it.

Cost estimate covers video output only: about $0.034 / $0.101 / $0.152 / $0.304
per second at 360p / 720p / 1080p / 4k. Input and reasoning tokens cost extra.

## When to pick it (and when not)

| Use it for | Prefer another provider for |
|---|---|
| Iterative refinement — generate, review, then edit the same clip in layers | One-shot cinematic hero clips (→ Seedance 2.0, see `seedance-2-0`) |
| Editing an existing/uploaded clip (restyle, add/remove objects, change text) | Single generations longer than 10s |
| On-screen rendered text and word-by-word text beats | Seed-reproducible generations (no seed support) |
| Reference-image-bound subjects/styles, first/last frames | Exact seed reproducibility |
| Timecode-scheduled multi-beat clips from one prompt | Non-English narration (English only fully supported) |

Use the registry and `video_selector` for all supported operations, including editing and extension.

## Generation prompting

Describe **scene + camera + lighting + motion + audio**. Official example:

> Continuous, unbroken handheld shot of a fluffy tabby cat sitting on a sunny windowsill, looking out into a leafy garden. The cat's tail twitches slowly, and its ears rotate slightly toward ambient noises. Sunbeams illuminate dust motes in the air.

- **Force a single shot** explicitly: "In a single continuous shot," / "No scene cuts." Otherwise the model may cut between scenes.
- **Negatives go in prose** — there is no `negative_prompt` parameter: "No dialogue," "No extra sound effects."
- **No sampler controls**: system instructions, temperature, top_p, and seeds are all unsupported. The prompt is the only lever.
- **Meta-prompt for quality**: "Consider micro-detail, expression and timing to create a very rich, detailed but entirely natural scene."

### Timecode syntax

Schedule beats with bracketed ranges or natural language — this maps directly onto OpenMontage scene-plan timings:

```
[0-3s] A person is walking [3-6s] They stop and turn around
```

> "After 3 seconds, a woman enters the scene." / "At 5s the chorus starts in the background audio."

### Audio and on-screen text

Audio is synthesized automatically; direct it in the prompt: "Include calm background music," "The audio is a low tinny radio broadcast in the background." Rendered text works and can be timed:

> One word on the screen at a time: 'did, you, know, that, Omni, can, do, awesome, text?' Each word appears for 1s.

## Reference images (`<FIRST_FRAME>` / `<IMAGE_REF_N>` tags)

Pass local images via `reference_image_paths` (they are sent in order), then bind them to roles **inside the prompt** with tags. `<IMAGE_REF_N>` indexes from 0 in the order supplied:

```
in the style of <IMAGE_REF_0> a woman <IMAGE_REF_1> is walking
```

```
[0-3s] A studio fashion sequence. Starting with woman <IMAGE_REF_0>, she is
holding <IMAGE_REF_1> [3-6s] Then we see the man <IMAGE_REF_2> holding <IMAGE_REF_3>
```

- `<FIRST_FRAME>` makes an image the opening frame: `<FIRST_FRAME> a woman is walking`.
- Use high-resolution images; describe the intended motion specifically rather than "make it move."
- Say what each image *is* (product / character / style / background reference) — the model decides usage from context.

## Conversational editing (the differentiator)

**Editing prompts are the opposite of generation prompts: short and surgical.** Overly descriptive edit prompts cause unintended changes.

1. Generate the base clip (subject + scene + motion). The tool returns `interaction_id` in its result data.
2. Pass it back as `previous_interaction_id` with `operation="edit_video"` and describe **only the delta**.
3. Append **"Keep everything else the same."** to pin unmentioned elements.
4. Refine in layers — one turn for lighting, one for camera, one for action, one for audio.

Official good/bad pairs:

| Avoid | Instead |
|---|---|
| "In the video of the man sitting on the sofa, please add a small black cat..." | "Add a cat that jumps onto his lap, he begins to pet it. Keep everything else the same." |
| "Please remove the cell phone... and fill in the background so it looks like..." | "Make the phone invisible. Keep everything else the same." |

Other working edit prompts: "Make this video anime" / "Put a fashionable hat on this person" / "Change the lighting to be more dramatic" / "Change the text on the sign to say 'Omni Flash'".

**Gotcha — `store`:** editing via `previous_interaction_id` only works if the *prior* call kept the interaction server-side (`store` defaults to true in `gemini_omni_video`). Set `store=false` only for one-shot generations you will never edit.

**Editing local videos:** pass `input_video_path` instead of `previous_interaction_id`; the tool sends inline video data to Vertex. Unavailable in the EEA, Switzerland, and the UK (editing *generated* videos works everywhere).

## Hard limitations (preview)

- Output: 3-10s per generation, 360p/720p/1080p/4k, MP4 with audio; aspect ratio `16:9` or `9:16`. All output carries an invisible SynthID watermark.
- No seed, negative prompt, temperature, top_p, or system instructions.
- Extension and first/last-frame generation are supported by Omni 1.1.
- Standalone audio reference input is unsupported; native dialogue/music/SFX are prompted in text.
- Up to 10 images and 3 videos per prompt; follow model limits for each operation.
- English fully supported; other languages untested.
- Images of minors (EEA/CH/UK) and certain recognizable people are blocked for upload/editing.

## Sources

- Vertex model: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/omni-1-1-flash
- First/last frames: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-first-and-last-frames
- Interactions: https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/interactions-api
- Pricing: https://cloud.google.com/vertex-ai/generative-ai/pricing
