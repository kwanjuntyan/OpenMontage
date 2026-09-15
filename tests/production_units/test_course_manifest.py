from __future__ import annotations

from copy import deepcopy

import jsonschema
import pytest

from lib.production_units.course import CourseManifestError
from schemas.artifacts import ARTIFACT_NAMES, validate_artifact


def course_manifest() -> dict:
    return {
        "version": "1.0",
        "project_id": "course-demo",
        "content_form": "course_form",
        "title": "Reliable Systems",
        "target_duration_seconds": 600,
        "course_promise": {
            "learner": "software engineers",
            "capability": "diagnose a retry boundary",
            "use_context": "a production incident",
            "success_evidence": "a justified recovery plan",
        },
        "audience": ["software engineers"],
        "entry_requirements": ["basic HTTP knowledge"],
        "objectives": [
            {
                "id": "obj-diagnose",
                "actor": "learner",
                "observable_verb": "diagnose",
                "object": "an ambiguous retry",
                "success_evidence": "classifies the attempt and selects a safe action",
                "source_refs": ["src-retries"],
            },
            {
                "id": "obj-design",
                "actor": "learner",
                "observable_verb": "design",
                "object": "an idempotent request boundary",
                "success_evidence": "produces a complete boundary sketch",
                "source_refs": ["src-retries"],
            },
        ],
        "modules": [
            {
                "id": "mod-foundations",
                "title": "Foundations",
                "intermediate_capability": "reason about retry safety",
                "target_duration_seconds": 600,
                "objective_ids": ["obj-diagnose", "obj-design"],
                "lessons": [
                    {
                        "id": "lesson-diagnose",
                        "title": "Diagnose",
                        "target_duration_seconds": 240,
                        "objective_ids": ["obj-diagnose"],
                        "prerequisite_lesson_ids": [],
                        "prerequisite_objective_ids": [],
                        "expected_outcome": "classify one retry",
                        "source_refs": ["src-retries"],
                        "teaching_beats": [
                            {
                                "kind": "worked_example",
                                "intent": "classify a timeout",
                                "objective_ids": ["obj-diagnose"],
                            }
                        ],
                        "glossary_ids": ["term-idempotent"],
                        "notation_ids": [],
                        "export_required": False,
                    },
                    {
                        "id": "lesson-design",
                        "title": "Design",
                        "target_duration_seconds": 360,
                        "objective_ids": ["obj-design"],
                        "prerequisite_lesson_ids": ["lesson-diagnose"],
                        "prerequisite_objective_ids": ["obj-diagnose"],
                        "expected_outcome": "design one safe request boundary",
                        "source_refs": ["src-retries"],
                        "teaching_beats": [
                            {
                                "kind": "practice",
                                "intent": "sketch an idempotency key flow",
                                "objective_ids": ["obj-design"],
                            }
                        ],
                        "glossary_ids": ["term-idempotent"],
                        "notation_ids": ["notation-key"],
                        "export_required": True,
                    },
                ],
                "recap_intent": "connect diagnosis to safe design",
            }
        ],
        "assessments": [
            {
                "id": "assessment-diagnose",
                "type": "formative",
                "objective_ids": ["obj-diagnose"],
                "lesson_id": "lesson-diagnose",
                "prompt_intent": "classify a timeout",
                "expected_evidence": "classification and reason",
                "pass_criteria": "states whether replay is safe",
            },
            {
                "id": "assessment-design",
                "type": "summative",
                "objective_ids": ["obj-design"],
                "lesson_id": "lesson-design",
                "prompt_intent": "design a boundary",
                "expected_evidence": "request and receipt sketch",
                "pass_criteria": "prevents ambiguous duplicate effects",
            },
        ],
        "sources": [{"id": "src-retries", "uri": "https://example.test/retries"}],
        "glossary": [
            {
                "id": "term-idempotent",
                "preferred_term": "idempotent",
                "definition": "repetition preserves the intended effect",
                "aliases": [],
                "forbidden_aliases": [],
            }
        ],
        "notation": [
            {
                "id": "notation-key",
                "symbol": "K",
                "meaning": "idempotency key",
                "first_lesson_id": "lesson-design",
            }
        ],
        "style_intent": {
            "tone": "precise and calm",
            "visual_intent": "state-machine diagrams",
        },
        "delivery_requirements": {
            "full_master": True,
            "lesson_export_ids": ["lesson-design"],
            "chapter_markers": True,
            "captions": ["vtt"],
            "bundle": True,
        },
    }


def test_course_manifest_is_registered_and_valid() -> None:
    assert "course_manifest" in ARTIFACT_NAMES
    validate_artifact("course_manifest", course_manifest())


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda value: value["modules"][0].update(target_duration_seconds=601),
            "duration",
        ),
        (
            lambda value: value["modules"][0]["lessons"][1][
                "prerequisite_lesson_ids"
            ].append("lesson-design"),
            "not earlier",
        ),
        (
            lambda value: value["assessments"].pop(),
            "not assessed",
        ),
        (
            lambda value: value["delivery_requirements"].update(
                lesson_export_ids=[]
            ),
            "exports",
        ),
        (
            lambda value: value["objectives"][0].update(
                observable_verb="understand"
            ),
            "observable verb",
        ),
    ],
)
def test_course_manifest_semantic_failures(mutate, message: str) -> None:
    value = deepcopy(course_manifest())
    mutate(value)
    with pytest.raises(CourseManifestError, match=message):
        validate_artifact("course_manifest", value)


def test_course_manifest_rejects_runtime_state_and_unknown_fields() -> None:
    value = course_manifest()
    value["status"] = "in_progress"
    with pytest.raises(jsonschema.ValidationError):
        validate_artifact("course_manifest", value)
