"""Semantic checks for the immutable course-form design artifact."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Iterable, Mapping


class CourseManifestError(ValueError):
    """Raised when a schema-valid course manifest is semantically unsafe."""


_FORBIDDEN_KEYS = {
    "active_stage",
    "active_unit",
    "attempts",
    "authorization",
    "clp_manifest",
    "control_chain_digest",
    "cost",
    "cost_usd",
    "credentials",
    "dispatch",
    "execution_epoch",
    "master_clp",
    "percentage_complete",
    "production_units",
    "provider_receipt",
    "publish_outcome",
    "render_outputs",
    "render_path",
    "repairs",
    "retries",
    "status",
    "telemetry",
}
_UNOBSERVABLE_ONLY = {"appreciate", "be aware", "know", "learn", "understand"}


def _decimal(value: Any) -> Decimal:
    return Decimal(str(value))


def _refs(values: Iterable[str], known: set[str], field: str) -> None:
    unknown = set(values) - known
    if unknown:
        raise CourseManifestError(f"{field} has unresolved references: {sorted(unknown)}")


def _reject_runtime_state(value: Any, path: str = "course_manifest") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key in _FORBIDDEN_KEYS:
                raise CourseManifestError(f"{path}.{key} is execution/runtime state")
            _reject_runtime_state(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_runtime_state(child, f"{path}[{index}]")


def validate_course_manifest_or_raise(manifest: Mapping[str, Any]) -> None:
    """Validate cross-reference, curriculum, duration, and authority invariants.

    JSON shape is validated by :func:`schemas.artifacts.validate_artifact`
    before this function is called. This function deliberately performs no I/O.
    """

    _reject_runtime_state(manifest)
    objectives = list(manifest["objectives"])
    modules = list(manifest["modules"])
    assessments = list(manifest["assessments"])
    sources = list(manifest["sources"])
    glossary = list(manifest["glossary"])
    notation = list(manifest["notation"])
    lessons = [lesson for module in modules for lesson in module["lessons"]]

    collections = {
        "objective": objectives,
        "module": modules,
        "lesson": lessons,
        "assessment": assessments,
        "source": sources,
        "glossary": glossary,
        "notation": notation,
    }
    all_ids: set[str] = set()
    for namespace, items in collections.items():
        ids = [item["id"] for item in items]
        if len(ids) != len(set(ids)):
            raise CourseManifestError(f"duplicate {namespace} id")
        overlap = all_ids.intersection(ids)
        if overlap:
            raise CourseManifestError(f"IDs must be globally unique: {sorted(overlap)}")
        all_ids.update(ids)

    objective_ids = {item["id"] for item in objectives}
    lesson_ids = {item["id"] for item in lessons}
    source_ids = {item["id"] for item in sources}
    glossary_ids = {item["id"] for item in glossary}
    notation_ids = {item["id"] for item in notation}
    lesson_order = {lesson["id"]: index for index, lesson in enumerate(lessons)}

    for objective in objectives:
        if objective["observable_verb"].strip().casefold() in _UNOBSERVABLE_ONLY:
            raise CourseManifestError(
                f"objective {objective['id']!r} needs an observable verb"
            )
        _refs(objective["source_refs"], source_ids, f"objective {objective['id']} source_refs")

    taught: set[str] = set()
    for module in modules:
        module_lessons = module["lessons"]
        expected = sum((_decimal(item["target_duration_seconds"]) for item in module_lessons), Decimal(0))
        if _decimal(module["target_duration_seconds"]) != expected:
            raise CourseManifestError(f"module {module['id']!r} duration does not equal its lessons")
        _refs(module["objective_ids"], objective_ids, f"module {module['id']} objective_ids")
        module_taught = {oid for item in module_lessons for oid in item["objective_ids"]}
        if set(module["objective_ids"]) != module_taught:
            raise CourseManifestError(
                f"module {module['id']!r} objective_ids must exactly describe its lessons"
            )

    for lesson in lessons:
        lesson_id = lesson["id"]
        if not lesson["objective_ids"]:
            raise CourseManifestError(f"lesson {lesson_id!r} must teach at least one objective")
        _refs(lesson["objective_ids"], objective_ids, f"lesson {lesson_id} objective_ids")
        _refs(lesson["source_refs"], source_ids, f"lesson {lesson_id} source_refs")
        _refs(lesson["glossary_ids"], glossary_ids, f"lesson {lesson_id} glossary_ids")
        _refs(lesson["notation_ids"], notation_ids, f"lesson {lesson_id} notation_ids")
        _refs(
            lesson["prerequisite_objective_ids"],
            objective_ids,
            f"lesson {lesson_id} prerequisite_objective_ids",
        )
        _refs(
            lesson["prerequisite_lesson_ids"],
            lesson_ids,
            f"lesson {lesson_id} prerequisite_lesson_ids",
        )
        for predecessor in lesson["prerequisite_lesson_ids"]:
            if lesson_order[predecessor] >= lesson_order[lesson_id]:
                raise CourseManifestError(
                    f"lesson {lesson_id!r} prerequisite {predecessor!r} is not earlier"
                )
        for beat in lesson["teaching_beats"]:
            _refs(
                beat.get("objective_ids", []),
                set(lesson["objective_ids"]),
                f"lesson {lesson_id} teaching beat objective_ids",
            )
        taught.update(lesson["objective_ids"])

    assessed: set[str] = set()
    for assessment in assessments:
        assessment_id = assessment["id"]
        if not assessment["objective_ids"]:
            raise CourseManifestError(
                f"assessment {assessment_id!r} must check at least one objective"
            )
        _refs(
            assessment["objective_ids"],
            objective_ids,
            f"assessment {assessment_id} objective_ids",
        )
        if "lesson_id" in assessment:
            _refs([assessment["lesson_id"]], lesson_ids, f"assessment {assessment_id} lesson_id")
        assessed.update(assessment["objective_ids"])

    if taught != objective_ids:
        raise CourseManifestError(f"objectives not taught exactly once-or-more: {sorted(objective_ids - taught)}")
    if assessed != objective_ids:
        raise CourseManifestError(f"objectives not assessed: {sorted(objective_ids - assessed)}")

    course_duration = sum(
        (_decimal(module["target_duration_seconds"]) for module in modules), Decimal(0)
    )
    if _decimal(manifest["target_duration_seconds"]) != course_duration:
        raise CourseManifestError("course duration does not equal its modules")

    for entry in notation:
        if "first_lesson_id" in entry:
            _refs([entry["first_lesson_id"]], lesson_ids, f"notation {entry['id']} first_lesson_id")
    preferred_terms = [entry["preferred_term"].strip().casefold() for entry in glossary]
    if len(preferred_terms) != len(set(preferred_terms)):
        raise CourseManifestError("glossary preferred terms must be unique")

    exports = set(manifest["delivery_requirements"]["lesson_export_ids"])
    _refs(exports, lesson_ids, "delivery_requirements.lesson_export_ids")
    declared_exports = {lesson["id"] for lesson in lessons if lesson["export_required"]}
    if exports != declared_exports:
        raise CourseManifestError("delivery lesson exports must match lesson export_required flags")
