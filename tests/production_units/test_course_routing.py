from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone

import jsonschema
import pytest

from lib.checkpoint import CheckpointValidationError, validate_checkpoint
from lib.pipeline_loader import list_pipelines, load_pipeline
from schemas.artifacts import validate_artifact
from tests.contracts.test_phase0_contracts import sample_artifact
from tests.production_units.test_course_manifest import course_manifest


def _proposal_checkpoint(*, project_id: str = "course-demo") -> dict:
    proposal = sample_artifact("proposal_packet")
    return {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": "animated-explainer",
        "stage": "proposal",
        "status": "completed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "human_approval_required": True,
        "human_approved": True,
        "artifacts": {
            "proposal_packet": proposal,
            "decision_log": {
                "version": "1.0",
                "project_id": project_id,
                "decisions": [],
            },
        },
    }


def _enable_course(checkpoint: dict) -> None:
    plan = checkpoint["artifacts"]["proposal_packet"]["production_plan"]
    plan["content_form"] = "course_form"
    plan["production_unit_policy"] = {
        "mode": "auto",
        "target_seconds": 180,
        "hard_max_seconds": 480,
        "boundary_priority": "semantic_first",
        "oversize_policy": "allow_with_reason",
        "enabled_stages": [
            "script",
            "clp",
            "scene_plan",
            "assets",
            "edit",
            "compose",
        ],
    }
    checkpoint["artifacts"]["course_manifest"] = course_manifest()


def test_course_form_and_policy_are_additive_to_legacy_proposals() -> None:
    legacy = sample_artifact("proposal_packet")
    validate_artifact("proposal_packet", legacy)

    candidate = deepcopy(legacy)
    candidate["production_plan"].update(
        {
            "content_form": "course_form",
            "production_unit_policy": {
                "mode": "auto",
                "target_seconds": 180,
                "boundary_priority": "semantic_first",
                "oversize_policy": "allow_with_reason",
                "enabled_stages": ["script", "scene_plan"],
            },
        }
    )
    validate_artifact("proposal_packet", candidate)


def test_every_existing_pipeline_manifest_remains_valid() -> None:
    for pipeline_name in list_pipelines():
        load_pipeline(pipeline_name)


def test_approved_course_checkpoint_routes_with_optional_output(tmp_path) -> None:
    checkpoint = _proposal_checkpoint()
    _enable_course(checkpoint)

    validate_checkpoint(checkpoint, pipeline_dir=tmp_path)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda cp: cp["artifacts"]["proposal_packet"]["production_plan"].update(
                content_form="course_form"
            ),
            "requires course_manifest",
        ),
        (
            lambda cp: cp["artifacts"].update(course_manifest=course_manifest()),
            "requires production_plan.content_form",
        ),
    ],
)
def test_course_routing_fails_closed(mutate, message: str, tmp_path) -> None:
    checkpoint = _proposal_checkpoint()
    mutate(checkpoint)

    with pytest.raises(CheckpointValidationError, match=message):
        validate_checkpoint(checkpoint, pipeline_dir=tmp_path)


def test_course_manifest_cannot_be_republished_by_later_stage(tmp_path) -> None:
    checkpoint = _proposal_checkpoint()
    checkpoint.update(stage="script", status="in_progress")
    checkpoint["artifacts"] = {"course_manifest": course_manifest()}

    with pytest.raises(CheckpointValidationError, match="only valid at stage 'proposal'"):
        validate_checkpoint(checkpoint, pipeline_dir=tmp_path)


def test_non_course_pipeline_cannot_claim_course_output(tmp_path) -> None:
    checkpoint = _proposal_checkpoint()
    _enable_course(checkpoint)
    checkpoint["pipeline_type"] = "cinematic"

    with pytest.raises(CheckpointValidationError, match="does not declare"):
        validate_checkpoint(checkpoint, pipeline_dir=tmp_path)


def test_policy_hard_max_cannot_be_smaller_than_target(tmp_path) -> None:
    checkpoint = _proposal_checkpoint()
    _enable_course(checkpoint)
    policy = checkpoint["artifacts"]["proposal_packet"]["production_plan"][
        "production_unit_policy"
    ]
    policy["hard_max_seconds"] = 120

    with pytest.raises(CheckpointValidationError, match="hard_max_seconds"):
        validate_checkpoint(checkpoint, pipeline_dir=tmp_path)


def test_policy_shape_is_typed_and_closed() -> None:
    proposal = sample_artifact("proposal_packet")
    proposal["production_plan"]["production_unit_policy"] = {
        "mode": "auto",
        "target_seconds": 180,
        "boundary_priority": "semantic_first",
        "oversize_policy": "allow_with_reason",
        "enabled_stages": ["script"],
        "secret_switch": True,
    }

    with pytest.raises(jsonschema.ValidationError):
        validate_artifact("proposal_packet", proposal)
