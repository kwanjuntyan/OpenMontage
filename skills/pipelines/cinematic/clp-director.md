# CLP Director Skill (Character, Location, Prop)

```yaml
name: clp-director
stage: clp
pipeline: cinematic
produces:
  - clp_manifest
  - clp_candidates
tools_used:
  - image_selector
```

## Overview
The **CLP Director** acts as the Production Designer and Head of the Art Department. Operating immediately after the `script` stage and before `scene_plan`, the CLP Director locks the physical appearance of all core entities to guarantee visual consistency across the entire project.

### Core Policy: One Signature Look per Episode
To prevent multi-costume combinatorial explosion and reference slot confusion, each character in this project/episode is defined by **one signature composite appearance master** (Face + Costume unified in a single reference image).

---

## Workflow

### 1. Script Entity Extraction (Sidecar Protocol)
- Read the exact predecessor artifact from
  `state.artifacts["script"]["script"]`. Do NOT mutate `script.json`.
- Set `source_script_sha256` with
  `lib.clp_validator.canonical_digest(script)`. Never hash pretty-printed file
  bytes or use a second JSON serialization convention.
- Extract all mentioned:
  - **Characters**: Hero characters, recurring figures, speaking roles.
  - **Locations**: Environments, architecture, lighting, time of day.
  - **Props**: Critical narrative devices, contracts, hero items, product models, diagrams.
- Write Sidecar artifact `projects/<project-id>/artifacts/clp_candidates.json` compliant with `clp_candidates.schema.json`.

### 2. Reference Allocation & Policy Assignment
For each entity, determine the `policy`:
- `strict_reference`: Hero characters, primary environments, plot-driving props. Mandatory composite image generated; bound to model reference slots.
- `text_anchor_only`: Ambient characters, secondary backgrounds. No reference image generated; concise keywords injected into prompt.
- `ignore`: Incidental background extras.

### 3. Master Image Generation
For every entity with `policy: "strict_reference"`:
- Call `image_selector` (using FLUX.1-dev or Google Imagen 3):
  - **Character Prompt**: Clear eye-level portrait with full signature wardrobe on a neutral studio background. E.g.:  
    `"Medium studio shot of 55yo British male executive Harrison Sterling, sharp jawline, silver-templed grey hair, piercing blue eyes, wearing bespoke dark navy double-breasted suit, crisp white collar, burgundy silk tie. Clean neutral grey studio background, diffused studio lighting, 8k, cinematic."`
  - **Location Prompt**: Establishing wide-angle empty plate capturing architecture and palette.
  - **Prop Prompt**: Isolated product-grade detail shot capturing surface material and distinctive marks.
- Save images locally under:
  - `projects/<project-id>/assets/clp/characters/<id>.png`
  - `projects/<project-id>/assets/clp/locations/<id>.png`
  - `projects/<project-id>/assets/clp/props/<id>.png`
- Compute the SHA-256 digest of each image binary for CAS (Content-Addressable Storage) validation.

### 4. Manifest Assembly
- Assemble `projects/<project-id>/artifacts/clp_manifest.json` complying with `clp_manifest.schema.json`.
- Populate `asset_sha256`, `prompt_anchor`, `visual_traits`, and local `image` paths.

### 5. Checkpoint & Gate Protocol
- **Case A: Pipeline with `human_approval_default: true` (e.g. `cinematic`)**:
  - Write checkpoint with status `awaiting_human`.
  - Present entity summary and Backlot board link to the user.
  - **END YOUR TURN**. Do not proceed to `scene_plan` until the user approves in chat or on the Backlot board.
- Cinematic has no zero-entity bypass. Even an empty cinematic CLP manifest
  remains subject to its manifest-declared human gate.
