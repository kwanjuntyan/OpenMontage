---
name: vox-paper-collage
description: >
  Prompt writing and visual direction for Vox-style paper-collage explainer video,
  tactile stop-motion collage animation, and clean documentary motion design.
  Features Model-Aware Dynamic Grammar Dispatch: generates 6-dimension structured
  timestamped prompts for Gemini Omni Flash (Part A) or continuous multi-shot prose
  for ByteDance Seedance 2.0 (Part B). Enforces Audio-First timing and strict keyword constraints.
allowed-tools: Read, Write
metadata:
  openclaw:
    requires:
      env_any:
        - GEMINI_API_KEY
        - GOOGLE_API_KEY
        - GOOGLE_APPLICATION_CREDENTIALS
        - FAL_KEY
---

# Vox Paper Collage Motion Design — Dynamic Engine Skill
### Gemini Omni Flash (Part A) & Seedance 2.0 (Part B)

This skill guides the Scene Planner and Asset Director in writing high-precision, engine-correct prompts for Vox-style paper-collage explainer videos.

---

## 1. Dynamic Grammar Dispatch (Model-Aware Routing)

In OpenMontage, prompts are automatically tailored to the target video provider declared in the pipeline/proposal:

| Target Video Tool / Model | Prompt Engine | Grammar Syntax |
| :--- | :--- | :--- |
| `gemini_omni_video` (`gemini-omni-1.1-flash-preview` / `gemini-omni-flash-preview`) | **Part A: Omni 6-Dimension Schema** | Structured blocks (`SHOT`, `STYLE`, `LIGHTING`, `LOCATION`, `ACTION`, `TEXT`, `AUDIO`, `NEGATIVE`) with timestamped action intervals. |
| `seedance_video` / `seedance_ark` (`seedance-2-0` / `seedance-2-5`) | **Part B: Seedance Multi-Shot Prose** | Dense cinematic prose with explicit `Cut to:` transitions, camera lens designations, and sound design sentences. |
| Dual-Engine Evaluation Mode | **Both Part A & Part B** | Output both formats into `artifacts/scene_plan.json` under `prompts.gemini_omni` and `prompts.seedance` for A/B quality testing. |

---

## 2. PART 0 — Shared Creative Language (Engine-Agnostic)

### 2.1 The Vox Aesthetic Checklist
Every prompt in this style must incorporate the tactile ingredients of documentary paper collage:
1. **Aged Newsprint / Grid-Paper Backdrop**: Off-white, textured paper (`#F5F4EF`), subtle grid lines, photocopy artifacts, soft vignette.
2. **Halftone Cut-Outs**: Archival photos, portraits, and engravings rendered with a visible duotone or monochrome print dot pattern.
3. **Physical Drop Shadows**: Every cutout element has crisp scissor-cut edges and a visible physical drop shadow, reading as a layered tabletop object.
4. **Self-Assembling Frames**: The frame builds itself in motion. Never ask for a static pan over a flat image. Start from empty backdrop; cutouts slide in from the edges and snap into place sequentially.
5. **Hand-Drawn Scribbles & Arrows**: Real-time vector-style annotations (arrows, circles, highlights) drawing themselves onto the paper to point at spoken concepts.
6. **Visual Density Rhythm**: Something physical must enter, move, or transform every **1.5 to 2.0 seconds**.
7. **Stop-Motion Register**: **12 FPS cadence**, zero motion blur, crisp frame-by-frame repositioning.

### 2.2 Strict On-Screen Text Rules
AI video generators cannot reliably render full sentences.
* **Never let the AI video model generate running subtitles or sentences.**
* **Restrict in-frame text to 1 or 2 uppercase, high-impact keywords** (e.g. `TEXT: "JAPAN 1950"` or `TEXT: "CRISIS"`).
* Full subtitles, captions, and stats cards are added in post-production by `video_compose` (Remotion/FFmpeg), not prompted into the diffusion model.

### 2.3 Audio-First Timing Protocol (Mandatory)
Before authoring `ACTION` intervals, the actual narration audio line must be generated (via TTS) and its exact duration measured:
1. Script section text $\to$ TTS $\to$ `probe_duration(line.mp3)` (e.g., `5.2s`).
2. Map the measured duration into the action interval:
   - `0.0 - 1.5s`: Initial element slides in.
   - `1.5 - 3.5s`: Arrow draws itself toward keyword.
   - `3.5 - 5.2s`: Highlighter box pops into place.

---

## 3. PART A — Gemini Omni Flash Prompt Grammar

When `gemini_omni_video` is the active tool, write prompts using the 6-dimension schema:

```text
SHOT: Tabletop collage / extreme close-up, 12 FPS stop-motion, static camera with subtle punch-in.
STYLE: Vox paper-collage documentary. Aged newsprint background, halftone dot cut-outs, crisp scissor-cut edges, physical drop shadows. Zero motion blur.
LIGHTING: Warm diffused archival desk lamp, casting soft directional shadows under paper edges.
LOCATION: Tabletop with aged yellowed grid paper, subtle paper grain and light pencil guidelines.
ACTION:
  - 0.0-1.5s: Frame starts on empty grid paper. A black-and-white halftone cut-out of [Subject] slides in rapidly from the left and snaps into place with a subtle paper jitter.
  - 1.5-3.5s: A hand-drawn red ink arrow draws itself from the tip, circling [Key element].
  - 3.5-[END]s: A bright yellow highlighter rectangular block pops in under the text label.
TEXT: "[1-2 UPPERCASE KEYWORDS]"
AUDIO: Subtle paper rustle, mechanical click, vintage projector hum. No spoken words, no dialogue.
NEGATIVE: smooth digital CGI, glossy 3D render, motion blur, rainbow colors, blurry text.
```

---

## 4. PART B — Seedance 2.0 Prompt Grammar

When `seedance_video` is the active tool, write prompts using Seedance prose syntax:

```text
Tabletop paper-collage documentary in Vox motion-design aesthetic, 12 FPS stop-motion feel with zero motion blur. On an aged newsprint and off-white grid paper backdrop, a crisp black-and-white halftone cutout of [Subject] slides into frame and settles with a tactile drop shadow.

Cut to: Tight macro insert as a hand-drawn red marker arrow sketches itself across the paper in rapid strokes, pointing toward [Key concept]. A bold paper label stamped with "[KEYWORD]" drops into place with physical bounce.

Ambient sound design: faint tape-recorder hiss, tactile paper rustling, and typewriter key impact. No spoken dialogue.
```

---

## 5. Talking Head & Lip-Sync Behavior

When an on-screen character (e.g. Dr. Deming) must speak:
1. **Paper Cutout Flap (Vox Stylized)**:
   Specify: *"A halftone cutout of [Character], his cutout paper jaw flaps open and shut in snappy 12 FPS rhythm as if speaking urgently."*
2. **Realistic Lip-Sync (High-Fidelity Dubbing)**:
   Allow the character to speak naturally in the video. In post-production, OpenMontage's `audio_mixer` separates the ambient sound effects, and `lip_sync` (Wav2Lip / Kling LipSync) retargets the mouth to the exact Mandarin TTS audio.
