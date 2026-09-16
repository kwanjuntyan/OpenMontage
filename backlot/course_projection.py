"""Read-only Backlot projection for approved course-form projects."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any, Optional


def _safe_delivery_path(value: Any, prefix: str) -> Optional[str]:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        return None
    if path.parts[0] != prefix:
        return None
    return value


def _validated_unit_progress(value: Any) -> Optional[dict[str, Any]]:
    """Project the typed subset of checkpoint-owned PUP progress metadata."""

    if not isinstance(value, dict):
        return None
    total = value.get("total_units")
    if isinstance(total, bool) or not isinstance(total, int) or total < 0:
        return None

    groups: dict[str, list[str]] = {}
    for key in ("completed_unit_ids", "failed_unit_ids", "stale_unit_ids"):
        items = value.get(key, [])
        if (
            not isinstance(items, list)
            or any(not isinstance(item, str) or not item for item in items)
            or len(items) != len(set(items))
        ):
            return None
        groups[key] = items

    completed = set(groups["completed_unit_ids"])
    failed = set(groups["failed_unit_ids"])
    stale = set(groups["stale_unit_ids"])
    if completed & failed or completed & stale or failed & stale:
        return None
    if len(completed | failed | stale) > total:
        return None

    active = value.get("active_unit_id")
    if active is not None and (not isinstance(active, str) or not active):
        return None
    if active in completed:
        return None

    counts = {}
    for source, target in (
        ("boundary_defect_count", "boundary_defects"),
        ("repair_count", "repairs"),
    ):
        count = value.get(source, 0)
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            return None
        counts[target] = count

    return {
        "total_units": total,
        "completed_units": len(completed),
        "failed_units": len(failed),
        "stale_units": len(stale),
        "active_unit_id": active,
        **counts,
    }


def _course_delivery_projection(
    course: dict[str, Any], checkpoints: dict[str, dict]
) -> dict[str, Any]:
    """Trace declared course deliveries to validated compose/publish checkpoints."""

    from lib.clp_validator import canonical_digest

    requirements = course["delivery_requirements"]
    compose = checkpoints.get("compose") or {}
    compose_artifacts = compose.get("artifacts") or {}
    render_report = (
        compose_artifacts.get("render_report")
        if compose.get("status") == "completed"
        and not compose.get("_checkpoint_invalid")
        else None
    )
    if not isinstance(render_report, dict):
        render_report = None

    render_digest = canonical_digest(render_report) if render_report else None
    outputs = render_report.get("outputs", []) if render_report else []
    master = next(
        (
            item
            for item in outputs
            if isinstance(item, dict)
            and item.get("platform_target") == "course_master"
            and _safe_delivery_path(item.get("path"), "renders") is not None
        ),
        None,
    )
    lesson_outputs = {
        item["platform_target"][len("lesson:") :]: item
        for item in outputs
        if isinstance(item, dict)
        and isinstance(item.get("platform_target"), str)
        and item["platform_target"].startswith("lesson:")
        and item["platform_target"][len("lesson:") :]
        and _safe_delivery_path(item.get("path"), "renders") is not None
    }

    publish = checkpoints.get("publish") or {}
    publish_artifacts = publish.get("artifacts") or {}
    publish_log = (
        publish_artifacts.get("publish_log")
        if publish.get("status") == "completed"
        and not publish.get("_checkpoint_invalid")
        else None
    )
    delivery_trace = None
    if isinstance(publish_log, dict):
        candidate = (publish_log.get("metadata") or {}).get("course_delivery")
        if (
            isinstance(candidate, dict)
            and candidate.get("version") == "1.0"
            and candidate.get("render_report_sha256") == render_digest
        ):
            delivery_trace = candidate

    traced_master = None
    if master and delivery_trace:
        trace_master = delivery_trace.get("full_master")
        if (
            isinstance(trace_master, dict)
            and _safe_delivery_path(trace_master.get("path"), "renders")
            == master.get("path")
        ):
            traced_master = master.get("path")

    traced_lessons: dict[str, str] = {}
    if delivery_trace:
        lesson_trace = delivery_trace.get("lesson_exports", [])
        if isinstance(lesson_trace, list):
            for item in lesson_trace:
                if not isinstance(item, dict):
                    continue
                lesson_id = item.get("lesson_id")
                path = item.get("path")
                output = lesson_outputs.get(lesson_id)
                if (
                    output
                    and _safe_delivery_path(path, "renders") == path
                    and output.get("path") == path
                ):
                    traced_lessons[lesson_id] = path

    def _publish_evidence(key: str) -> Any:
        return delivery_trace.get(key) if delivery_trace else None

    def _file_evidence(key: str, prefix: str) -> Any:
        evidence = _publish_evidence(key)
        if not isinstance(evidence, dict):
            return None
        return (
            evidence
            if _safe_delivery_path(evidence.get("path"), prefix) is not None
            else None
        )

    return {
        "render_report_sha256": render_digest,
        "publish_trace_valid": delivery_trace is not None,
        "full_master": {
            "required": requirements["full_master"],
            "status": (
                "published"
                if traced_master
                else "rendered"
                if master
                else "missing"
                if requirements["full_master"]
                else "not_required"
            ),
            "path": traced_master or (master or {}).get("path"),
        },
        "lesson_exports": [
            {
                "lesson_id": lesson_id,
                "status": (
                    "published"
                    if lesson_id in traced_lessons
                    else "rendered"
                    if lesson_id in lesson_outputs
                    else "missing"
                ),
                "path": traced_lessons.get(lesson_id)
                or (lesson_outputs.get(lesson_id) or {}).get("path"),
            }
            for lesson_id in requirements["lesson_export_ids"]
        ],
        "chapter_markers": {
            "required": requirements["chapter_markers"],
            "status": "published"
            if _file_evidence("chapter_markers", "exports") is not None
            else "missing"
            if requirements["chapter_markers"]
            else "not_required",
            "evidence": _file_evidence("chapter_markers", "exports"),
        },
        "captions": [
            {
                "format": caption_format,
                "status": "published"
                if any(
                    isinstance(item, dict)
                    and item.get("format") == caption_format
                    and _safe_delivery_path(item.get("path"), "exports") is not None
                    for item in (_publish_evidence("captions") or [])
                )
                else "missing",
            }
            for caption_format in requirements["captions"]
        ],
        "bundle": {
            "required": requirements["bundle"],
            "status": "published"
            if _file_evidence("bundle", "exports") is not None
            else "missing"
            if requirements["bundle"]
            else "not_required",
            "evidence": _file_evidence("bundle", "exports"),
        },
    }


def derive_course_projection(
    checkpoints: dict[str, dict],
    stages: list[dict[str, Any]],
    diagnostics: list[dict[str, str]],
    loose_cache: Optional[dict[str, Any]] = None,
) -> Optional[dict[str, Any]]:
    """Return a course view only from the approved proposal checkpoint."""

    proposal_checkpoint = checkpoints.get("proposal") or {}
    authoritative = None
    if (
        not proposal_checkpoint.get("_checkpoint_invalid")
        and proposal_checkpoint.get("status") == "completed"
        and proposal_checkpoint.get("human_approved") is True
    ):
        artifacts = proposal_checkpoint.get("artifacts") or {}
        proposal = artifacts.get("proposal_packet")
        course = artifacts.get("course_manifest")
        if (
            isinstance(proposal, dict)
            and isinstance(course, dict)
            and (proposal.get("production_plan") or {}).get("content_form")
            == "course_form"
        ):
            authoritative = course

    loose = loose_cache
    if authoritative is None:
        if loose is not None:
            diagnostics.append(
                {
                    "artifact": "course_manifest",
                    "status": "untrusted_cache_ignored",
                    "reason": "missing valid approved checkpoint_proposal.json authority",
                }
            )
        return None

    from lib.clp_validator import canonical_digest

    if loose is not None:
        try:
            loose_matches = canonical_digest(loose) == canonical_digest(authoritative)
        except (TypeError, ValueError):
            diagnostics.append(
                {
                    "artifact": "course_manifest",
                    "status": "invalid_cache_ignored",
                    "reason": "standalone cache is not canonical JSON",
                }
            )
        else:
            if not loose_matches:
                diagnostics.append(
                    {
                        "artifact": "course_manifest",
                        "status": "cache_mismatch_ignored",
                        "reason": "approved checkpoint_proposal.json remains authoritative",
                    }
                )

    progress_by_stage = []
    for stage in stages:
        checkpoint = checkpoints.get(stage["name"]) or {}
        if checkpoint.get("_checkpoint_invalid"):
            continue
        metadata = checkpoint.get("metadata")
        partial = metadata.get("partial_progress") if isinstance(metadata, dict) else None
        unit_data = partial.get("production_units") if isinstance(partial, dict) else None
        progress = _validated_unit_progress(unit_data)
        if progress is not None:
            progress_by_stage.append({"stage": stage["name"], **progress})

    active = next(
        (
            item
            for item in reversed(progress_by_stage)
            if item["active_unit_id"] is not None
        ),
        None,
    )
    overall = next(
        (stage for stage in stages if stage["status"] in {"in_progress", "awaiting_human", "failed"}),
        None,
    )
    if overall is None:
        overall = next(
            (stage for stage in reversed(stages) if stage["status"] == "completed"),
            None,
        )

    modules = [
        {
            "id": module["id"],
            "title": module["title"],
            "target_duration_seconds": module["target_duration_seconds"],
            "lessons": [
                {
                    "id": lesson["id"],
                    "title": lesson["title"],
                    "target_duration_seconds": lesson["target_duration_seconds"],
                    "objective_ids": list(lesson["objective_ids"]),
                    "export_required": lesson["export_required"],
                }
                for lesson in module["lessons"]
            ],
        }
        for module in authoritative["modules"]
    ]
    return {
        "is_course": True,
        "manifest_sha256": canonical_digest(authoritative),
        "title": authoritative["title"],
        "target_duration_seconds": authoritative["target_duration_seconds"],
        "objective_count": len(authoritative["objectives"]),
        "module_count": len(modules),
        "lesson_count": sum(len(module["lessons"]) for module in modules),
        "modules": modules,
        "overall_stage": (
            {"name": overall["name"], "status": overall["status"]}
            if overall
            else None
        ),
        "production_units": {
            "by_stage": progress_by_stage,
            "active": (
                {"stage": active["stage"], "unit_id": active["active_unit_id"]}
                if active
                else None
            ),
        },
        "delivery": _course_delivery_projection(authoritative, checkpoints),
    }
