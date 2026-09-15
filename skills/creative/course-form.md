# Course Form

## When to use

Use this skill when the requested result is a learning experience with explicit
learner outcomes, prerequisite structure, teaching practice, and assessment.
Duration alone does not select course form. A long documentary, podcast, event,
or montage remains its own form; a concise lesson may still be course-form.

At proposal time, set `production_plan.content_form="course_form"` only after
this pedagogical intent is clear. Read `creative/long-form.md` as an additional
retention and chapter-design resource when useful, but do not copy its
15-minute narrative shape into every course.

## Responsibility boundary

This skill owns curriculum design and a `course_manifest` candidate. It does
not define model attention limits, Production Unit sizing, folders, retries,
resume, rendering, checkpoint transitions, or publication. For bounded stage
execution, read `skills/meta/production-unit-protocol.md`. Production Units are
not lessons, modules, chapters, projects, or checkpoints.

The proposal director remains responsible for production choices, costs,
runtime/provider locks, approval, and writing the proposal checkpoint. This
skill never publishes or approves an artifact.

## Inputs

- learner and use context;
- desired post-course capability and observable success evidence;
- research brief and authenticated sources;
- entry knowledge, constraints, target duration, language, and accessibility;
- delivery needs such as a full master, lesson exports, chapters, captions, or
  an export bundle.

If the learner, capability, or success evidence is unknown, resolve that before
expanding modules or writing a script.

## Design process

### 1. Write one course promise

State who the learner is, what they will be able to do, where they will use it,
and what evidence will prove success. Avoid promises such as “understand” that
cannot be observed.

### 2. Define assessable objectives

Give every objective a stable ID, observable verb, object, success evidence,
and source references. Each objective must be taught and assessed. Prefer the
smallest set that fully supports the course promise.

### 3. Build the dependency graph

Order concepts and skills by prerequisite, not by source order. Record lesson
and objective prerequisites explicitly. A prerequisite must appear earlier and
every reference must resolve.

### 4. Design modules and lessons

Each module delivers an intermediate capability and ends with synthesis or a
bridge. Each lesson records:

- its stable ID, title, target duration, and expected learner outcome;
- objective and prerequisite references;
- sources, glossary terms, and notation introduced or reused;
- teaching beats such as activation, explanation, model, worked example,
  demonstration, practice, recap, assessment, and bridge;
- whether it must be exported as an independent deliverable.

Lesson duration is a pedagogical budget. It is not a Production Unit size.

### 5. Place assessment and retrieval

Use diagnostic checks where entry knowledge matters, formative checks while a
skill is being built, and summative evidence for the final capability. Revisit
important earlier objectives through application or retrieval instead of
merely repeating their explanation.

### 6. Freeze shared language and style intent

Record preferred terms, definitions, forbidden aliases, notation, and first-use
rules. Record the course-wide tone and visual intent. These become inputs to the
one course-wide CLP and later stage contexts; do not create a second CLP here.

### 7. Declare delivery requirements

Choose whether the course needs a full master, which lessons need independent
exports, chapter markers, caption formats, and an export bundle. Requirements
are declarations, not claims that files already exist.

## Output contract

Return one schema-valid `course_manifest` candidate conforming to
`schemas/artifacts/course_manifest.schema.json`. It must:

- use `content_form="course_form"` and the same `project_id` as the project;
- have exact course/module/lesson duration totals;
- use globally unique stable IDs and resolvable references;
- cover every objective in teaching and assessment;
- make lesson export flags exactly match delivery requirements;
- contain only static learning design, never progress, attempts, unit state,
  costs, credentials, CLP copies, render paths, or publish outcomes.

The proposal checkpoint must contain this manifest beside the proposal packet.
Later stages consume that approved predecessor and must not republish a modified
copy.

## Review gate

Before handoff, confirm:

- the course promise is observable and realistic for the duration;
- objective, lesson, prerequisite, source, glossary, notation, assessment, and
  delivery references all resolve;
- examples and practice progress from modeled to independent performance;
- each assessment captures the evidence named by its objective;
- terminology and notation are introduced before dependent use;
- the sequence has purposeful bridges and a final synthesis;
- no Production Unit or runtime state leaked into the course manifest.

