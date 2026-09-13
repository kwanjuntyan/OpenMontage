"""Fail-closed CLP project-root and predecessor provenance contracts."""

from __future__ import annotations

import json
from copy import deepcopy

import jsonschema
import pytest

import lib.checkpoint as checkpoint_lib
from lib.checkpoint import (
    CheckpointValidationError,
    _checkpoint_path,
    _stage_requires_approval,
    get_latest_checkpoint,
    get_pipeline_stages,
    init_project,
    read_checkpoint,
    validate_checkpoint,
    verify_gate_resolution,
    write_checkpoint,
)
from lib.clp_validator import canonical_digest
from schemas.artifacts import validate_artifact


NOW = "2026-09-13T00:00:00Z"
PIPELINE = "animated-explainer"


def _script() -> dict:
    return {
        "version": "1.0",
        "title": "Provenance fixture",
        "total_duration_seconds": 1,
        "sections": [
            {"id": "s1", "text": "Hello.", "start_seconds": 0, "end_seconds": 1}
        ],
    }


def _manifest(project_id: str = "p") -> dict:
    return {
        "version": "2.0",
        "project_id": project_id,
        "characters": [],
        "locations": [],
        "props": [],
    }


def _candidates(script: dict, project_id: str = "p") -> dict:
    return {
        "version": "2.0",
        "project_id": project_id,
        "source_script_sha256": canonical_digest(script),
        "candidates": {"characters": [], "locations": [], "props": []},
    }


def _script_checkpoint(project_id: str = "p") -> dict:
    return {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": PIPELINE,
        "stage": "script",
        "status": "completed",
        "timestamp": NOW,
        "human_approved": True,
        "artifacts": {"script": _script()},
    }


def _clp_checkpoint(project_id: str = "p", *, approved: bool = True) -> dict:
    script = _script()
    return {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": PIPELINE,
        "stage": "clp",
        "status": "completed",
        "timestamp": NOW,
        "human_approved": approved,
        "artifacts": {
            "clp_manifest": _manifest(project_id),
            "clp_candidates": _candidates(script, project_id),
        },
    }


def _scene_plan() -> dict:
    return {
        "version": "1.0",
        "scenes": [
            {
                "id": "shot-1",
                "type": "generated",
                "description": "A shot.",
                "start_seconds": 0,
                "end_seconds": 1,
            }
        ],
    }


def _scene_checkpoint(manifest: dict, *, include_local_manifest: bool = False) -> dict:
    scene_plan = _scene_plan()
    artifacts = {
        "scene_plan": scene_plan,
        "clp_shot_bindings": {
            "version": "2.0",
            "project_id": "p",
            "source_scene_plan_sha256": canonical_digest(scene_plan),
            "clp_manifest_sha256": canonical_digest(manifest),
            "bindings": [{"shot_id": "shot-1"}],
        },
    }
    if include_local_manifest:
        artifacts["clp_manifest"] = manifest
    return {
        "version": "1.0",
        "project_id": "p",
        "pipeline_type": PIPELINE,
        "stage": "scene_plan",
        "status": "completed",
        "timestamp": NOW,
        "human_approved": True,
        "artifacts": artifacts,
    }


def _write_checkpoint_file(root, checkpoint: dict) -> None:
    project_dir = root / checkpoint["project_id"]
    project_dir.mkdir(parents=True, exist_ok=True)
    stage = checkpoint["stage"]
    (project_dir / f"checkpoint_{stage}.json").write_text(
        json.dumps(checkpoint), encoding="utf-8"
    )


@pytest.mark.parametrize("artifact_name", ["clp_candidates", "clp_shot_bindings"])
def test_all_clp_sidecars_reject_path_like_project_id(artifact_name):
    script = _script()
    data = _candidates(script, "..")
    if artifact_name == "clp_shot_bindings":
        scene = _scene_plan()
        data = {
            "version": "2.0",
            "project_id": "..",
            "source_scene_plan_sha256": canonical_digest(scene),
            "clp_manifest_sha256": canonical_digest(_manifest()),
            "bindings": [{"shot_id": "shot-1"}],
        }
    with pytest.raises(jsonschema.ValidationError):
        validate_artifact(artifact_name, data)


def test_checkpoint_project_id_is_rejected_before_path_join(tmp_path):
    checkpoint = {
        "version": "1.0",
        "project_id": "..",
        "pipeline_type": "unknown",
        "stage": "script",
        "status": "in_progress",
        "timestamp": NOW,
        "artifacts": {},
    }
    with pytest.raises(CheckpointValidationError, match="Invalid project_id"):
        validate_checkpoint(checkpoint, pipeline_dir=tmp_path)
    with pytest.raises(CheckpointValidationError, match="Invalid project_id"):
        _checkpoint_path(tmp_path, "..", "script")


def test_checkpoint_stage_is_rejected_before_filename_join(tmp_path):
    with pytest.raises(CheckpointValidationError, match="stage path component"):
        _checkpoint_path(tmp_path, "p", "../script")


def test_write_checkpoint_rejects_project_escape_without_creating_outside(tmp_path):
    outside_name = f"{tmp_path.name}-escaped"
    outside = tmp_path.parent / outside_name
    assert not outside.exists()
    with pytest.raises(CheckpointValidationError, match="Invalid project_id"):
        write_checkpoint(
            tmp_path,
            f"../{outside_name}",
            "research",
            "in_progress",
            {},
        )
    assert not outside.exists()


@pytest.mark.parametrize("pipeline_type", ["unknown", "pipeline-does-not-exist"])
def test_init_project_rejects_invalid_pipeline_before_creating_directory(
    tmp_path, pipeline_type
):
    with pytest.raises(CheckpointValidationError):
        init_project(
            "must-not-exist",
            title="Invalid pipeline",
            pipeline_type=pipeline_type,
            pipeline_dir=tmp_path,
        )
    assert not (tmp_path / "must-not-exist").exists()


@pytest.mark.parametrize(
    "marker",
    [
        {"project_id": "other", "pipeline_type": "framework-smoke"},
        {"project_id": "p", "pipeline_type": "cinematic"},
    ],
)
def test_lifecycle_write_rejects_marker_identity_mismatch(tmp_path, marker):
    project_dir = tmp_path / "p"
    project_dir.mkdir()
    (project_dir / "project.json").write_text(json.dumps(marker), encoding="utf-8")
    with pytest.raises(CheckpointValidationError, match="marker .*mismatch"):
        write_checkpoint(
            tmp_path,
            "p",
            "research",
            "completed",
            {"research_brief": {}},
            pipeline_type="framework-smoke",
            human_approved=True,
        )
    assert not (project_dir / "checkpoint_research.json").exists()


def test_lifecycle_write_rejects_corrupt_marker(tmp_path):
    project_dir = tmp_path / "p"
    project_dir.mkdir()
    (project_dir / "project.json").write_text("{not-json", encoding="utf-8")
    with pytest.raises(CheckpointValidationError, match="corrupt project marker"):
        write_checkpoint(
            tmp_path,
            "p",
            "research",
            "completed",
            {"research_brief": {}},
            pipeline_type="framework-smoke",
            human_approved=True,
        )
    assert not (project_dir / "checkpoint_research.json").exists()


def test_completed_clp_rejects_missing_script_predecessor(tmp_path):
    checkpoint = _clp_checkpoint()
    with pytest.raises(CheckpointValidationError, match="checkpoint_script.json not found"):
        validate_checkpoint(checkpoint, pipeline_dir=tmp_path)


def test_zero_entity_autopass_rejects_missing_script_predecessor(tmp_path):
    checkpoint = _clp_checkpoint(approved=False)
    manifest = checkpoint["artifacts"]["clp_manifest"]
    checkpoint["gate_resolution"] = {
        "mode": "zero_entity_auto",
        "rule_version": "clp_literal_empty_v1",
        "entity_counts": {"characters": 0, "locations": 0, "props": 0},
        "manifest_sha256": canonical_digest(manifest),
        "resolved_at": NOW,
    }
    with pytest.raises(CheckpointValidationError, match="checkpoint_script.json not found"):
        validate_checkpoint(checkpoint, pipeline_dir=tmp_path)


def test_zero_entity_verifier_requires_full_authenticated_predecessor(tmp_path):
    checkpoint = _clp_checkpoint(approved=False)
    manifest = checkpoint["artifacts"]["clp_manifest"]
    checkpoint["gate_resolution"] = {
        "mode": "zero_entity_auto",
        "rule_version": "clp_literal_empty_v1",
        "entity_counts": {"characters": 0, "locations": 0, "props": 0},
        "manifest_sha256": canonical_digest(manifest),
        "resolved_at": NOW,
    }

    valid, reason = verify_gate_resolution(
        checkpoint,
        predecessor_checkpoint=_script(),
        pipeline_dir=tmp_path,
    )
    assert valid is False
    assert "checkpoint schema validation" in reason

    valid, reason = verify_gate_resolution(
        checkpoint,
        predecessor_checkpoint=_script_checkpoint(),
        pipeline_dir=tmp_path,
    )
    assert (valid, reason) == (True, None)


@pytest.mark.parametrize(
    ("target", "mutation"),
    [
        ("current", {"unexpected": True}),
        ("current", {"timestamp": "2026-99-99T99:99:99Z"}),
        ("predecessor", {"unexpected": True}),
        ("predecessor", {"timestamp": "2026-99-99T99:99:99Z"}),
    ],
)
def test_gate_verifier_validates_full_checkpoint_envelopes(tmp_path, target, mutation):
    checkpoint = _clp_checkpoint(approved=False)
    manifest = checkpoint["artifacts"]["clp_manifest"]
    checkpoint["gate_resolution"] = {
        "mode": "zero_entity_auto",
        "rule_version": "clp_literal_empty_v1",
        "entity_counts": {"characters": 0, "locations": 0, "props": 0},
        "manifest_sha256": canonical_digest(manifest),
        "resolved_at": NOW,
    }
    predecessor = _script_checkpoint()
    if target == "current":
        checkpoint.update(mutation)
    else:
        predecessor.update(mutation)

    valid, reason = verify_gate_resolution(
        checkpoint,
        predecessor_checkpoint=predecessor,
        pipeline_dir=tmp_path,
    )
    assert valid is False
    assert "schema validation" in reason


def test_completed_clp_accepts_only_matching_approved_script(tmp_path):
    script_checkpoint = _script_checkpoint()
    _write_checkpoint_file(tmp_path, script_checkpoint)
    validate_checkpoint(_clp_checkpoint(), pipeline_dir=tmp_path)

    stale = _clp_checkpoint()
    stale["artifacts"]["clp_candidates"]["source_script_sha256"] = "sha256:" + "0" * 64
    with pytest.raises(CheckpointValidationError, match="source_script_sha256 mismatch"):
        validate_checkpoint(stale, pipeline_dir=tmp_path)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ({"project_id": "other"}, "project_id"),
        ({"pipeline_type": "cinematic"}, "pipeline_type"),
        ({"stage": "proposal"}, "stage"),
        ({"status": "failed"}, "status"),
        ({"human_approved": False}, "human approval"),
    ],
)
def test_script_predecessor_identity_status_and_approval_are_checked(
    tmp_path, mutation, message
):
    predecessor = _script_checkpoint()
    predecessor.update(mutation)
    project_dir = tmp_path / "p"
    project_dir.mkdir()
    (project_dir / "checkpoint_script.json").write_text(
        json.dumps(predecessor), encoding="utf-8"
    )
    with pytest.raises(CheckpointValidationError, match=message):
        validate_checkpoint(_clp_checkpoint(), pipeline_dir=tmp_path)


def test_explicit_pipeline_root_never_falls_back_to_global_projects(tmp_path, monkeypatch):
    authoritative = tmp_path / "authoritative"
    fallback = tmp_path / "fallback"
    _write_checkpoint_file(fallback, _script_checkpoint())
    monkeypatch.setattr(checkpoint_lib, "PROJECTS_DIR", fallback)
    with pytest.raises(CheckpointValidationError, match="checkpoint_script.json not found"):
        validate_checkpoint(_clp_checkpoint(), pipeline_dir=authoritative)


def test_scene_rejects_local_manifest_without_exact_clp_predecessor(tmp_path):
    manifest = _manifest()
    with pytest.raises(CheckpointValidationError, match="checkpoint_clp.json not found"):
        validate_checkpoint(
            _scene_checkpoint(manifest, include_local_manifest=True), pipeline_dir=tmp_path
        )


def test_scene_rejects_unapproved_clp_predecessor(tmp_path):
    _write_checkpoint_file(tmp_path, _script_checkpoint())
    predecessor = _clp_checkpoint(approved=False)
    _write_checkpoint_file(tmp_path, predecessor)
    with pytest.raises(CheckpointValidationError, match="GATE VIOLATION"):
        validate_checkpoint(_scene_checkpoint(_manifest()), pipeline_dir=tmp_path)


def test_scene_rejects_manifest_shadow_and_accepts_identical_cache(tmp_path):
    _write_checkpoint_file(tmp_path, _script_checkpoint())
    _write_checkpoint_file(tmp_path, _clp_checkpoint())

    approved = _manifest()
    validate_checkpoint(
        _scene_checkpoint(approved, include_local_manifest=True), pipeline_dir=tmp_path
    )

    rogue = deepcopy(approved)
    rogue["characters"] = [
        {
            "id": "rogue",
            "name": "Rogue",
            "visual_traits": "Unapproved",
            "policy": "text_anchor_only",
            "prompt_anchor": "rogue",
        }
    ]
    with pytest.raises(CheckpointValidationError, match="shadows approved predecessor"):
        validate_checkpoint(
            _scene_checkpoint(rogue, include_local_manifest=True), pipeline_dir=tmp_path
        )


def test_clp_checkpoint_cannot_smuggle_scene_bindings_or_recurse(tmp_path):
    checkpoint = _clp_checkpoint()
    checkpoint["artifacts"]["clp_shot_bindings"] = {}
    with pytest.raises(CheckpointValidationError, match="only valid at stage 'scene_plan'"):
        validate_checkpoint(checkpoint, pipeline_dir=tmp_path)


@pytest.mark.parametrize("pipeline_type", ["unknown", "cinematic-typo"])
def test_provided_unknown_pipeline_never_falls_back_to_canonical_stages(pipeline_type):
    with pytest.raises(
        CheckpointValidationError,
        match=r"Unknown pipeline_type",
    ):
        get_pipeline_stages(pipeline_type)


@pytest.mark.parametrize("status", ["completed", "in_progress", "failed"])
def test_unknown_pipeline_is_rejected_for_every_status(status):
    checkpoint = _script_checkpoint()
    checkpoint["pipeline_type"] = "unknown"
    checkpoint["status"] = status
    with pytest.raises(CheckpointValidationError, match="concrete, schema-valid pipeline_type"):
        validate_checkpoint(checkpoint)


@pytest.mark.parametrize("reader", ["exact", "latest"])
def test_checkpoint_reader_binds_envelope_to_physical_path(tmp_path, reader):
    project_dir = tmp_path / "p"
    project_dir.mkdir()
    checkpoint = _script_checkpoint()
    checkpoint["project_id"] = "other-project"
    (project_dir / "checkpoint_script.json").write_text(
        json.dumps(checkpoint), encoding="utf-8"
    )

    with pytest.raises(CheckpointValidationError, match="path identity mismatch"):
        if reader == "exact":
            read_checkpoint(tmp_path, "p", "script")
        else:
            get_latest_checkpoint(tmp_path, "p")


def test_corrupt_pipeline_manifest_helpers_fail_closed(monkeypatch):
    import lib.pipeline_loader as pipeline_loader

    def corrupt_manifest(_pipeline_type):
        raise ValueError("corrupt manifest probe")

    monkeypatch.setattr(pipeline_loader, "load_pipeline_readonly", corrupt_manifest)
    with pytest.raises(CheckpointValidationError, match="corrupt manifest probe"):
        get_pipeline_stages("cinematic")
    with pytest.raises(CheckpointValidationError, match="corrupt manifest probe"):
        _stage_requires_approval("cinematic", "clp")
