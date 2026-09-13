"""Focused CLP hardening checks for Backlot and explainer director contracts."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from backlot.state import (
    _build_stage_rail,
    _read_contained_project_json,
    load_board_state,
)
from lib.clp_validator import canonical_digest
from schemas.artifacts import validate_artifact


PROJECT_ID = "clp-board-hardening"


def _script() -> dict:
    return {
        "version": "1.0",
        "title": "Gate provenance",
        "total_duration_seconds": 5,
        "sections": [
            {
                "id": "section-1",
                "text": "A script with no recurring visual entities.",
                "start_seconds": 0,
                "end_seconds": 5,
            }
        ],
    }


def _manifest() -> dict:
    return {
        "version": "2.0",
        "project_id": PROJECT_ID,
        "characters": [],
        "locations": [],
        "props": [],
    }


def _candidates(script: dict) -> dict:
    return {
        "version": "2.0",
        "project_id": PROJECT_ID,
        "source_script_sha256": canonical_digest(script),
        "candidates": {"characters": [], "locations": [], "props": []},
    }


def _script_checkpoint(script_artifact: object) -> dict:
    return {
        "version": "1.0",
        "project_id": PROJECT_ID,
        "pipeline_type": "animated-explainer",
        "stage": "script",
        "status": "completed",
        "timestamp": "2026-09-13T00:00:00Z",
        "human_approval_required": True,
        "human_approved": True,
        "artifacts": {"script": script_artifact},
    }


def _clp_checkpoint(manifest_artifact: object, candidates_artifact: object) -> dict:
    manifest = _manifest()
    return {
        "version": "1.0",
        "project_id": PROJECT_ID,
        "pipeline_type": "animated-explainer",
        "stage": "clp",
        "status": "completed",
        "timestamp": "2026-09-13T00:00:00Z",
        "human_approval_required": False,
        "human_approved": False,
        "artifacts": {
            "clp_manifest": manifest_artifact,
            "clp_candidates": candidates_artifact,
        },
        "gate_resolution": {
            "mode": "zero_entity_auto",
            "rule_version": "clp_literal_empty_v1",
            "entity_counts": {"characters": 0, "locations": 0, "props": 0},
            "manifest_sha256": canonical_digest(manifest),
            "resolved_at": "2026-09-13T00:00:00Z",
        },
    }


def _pipeline_meta() -> dict:
    return {
        "pipeline_type": "animated-explainer",
        "stages": [
            {"name": "script", "gated": True, "produces": ["script"]},
            {
                "name": "clp",
                "gated": False,
                "produces": ["clp_manifest", "clp_candidates"],
            },
        ],
    }


def _clp_stage(checkpoints: dict, project_dir: Path | None = None) -> dict:
    stages = _build_stage_rail(
        _pipeline_meta(), checkpoints, history={}, project_dir=project_dir
    )
    return next(stage for stage in stages if stage["name"] == "clp")


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_backlot_project_json_reader_rejects_resolved_outside_target(tmp_path):
    project_dir = tmp_path / PROJECT_ID
    project_dir.mkdir()
    outside = tmp_path / "outside.json"
    _write_json(outside, {"project_id": PROJECT_ID})

    assert _read_contained_project_json(project_dir, outside) is None


def test_backlot_resolves_one_project_local_gate_bundle_and_predecessor(tmp_path):
    """The public board verifies the same inline envelope runtime can resume."""
    project_dir = tmp_path / PROJECT_ID
    script = _script()
    manifest = _manifest()
    candidates = _candidates(script)

    _write_json(
        project_dir / "project.json",
        {
            "version": "1.0",
            "project_id": PROJECT_ID,
            "title": "CLP Board Hardening",
            "pipeline_type": "animated-explainer",
        },
    )
    _write_json(project_dir / "artifacts" / "script.json", script)
    _write_json(project_dir / "artifacts" / "clp_manifest.json", manifest)
    _write_json(project_dir / "artifacts" / "clp_candidates.json", candidates)
    _write_json(
        project_dir / "checkpoint_script.json",
        _script_checkpoint(script),
    )
    _write_json(
        project_dir / "checkpoint_clp.json",
        _clp_checkpoint(
            manifest, candidates
        ),
    )

    state = load_board_state(project_dir)
    clp_stage = next(stage for stage in state["stages"] if stage["name"] == "clp")

    assert clp_stage["auto_passed"] is True
    assert clp_stage["gate_skipped"] is False
    assert clp_stage["gate_resolution"]["mode"] == "zero_entity_auto"
    # BoardState's display API remains flat; production directors intentionally
    # consume the separate stage-scoped checkpoint state asserted below.
    assert state["artifacts"]["script"] == script
    assert state["artifacts"]["clp_manifest"] == manifest
    assert state["artifacts"]["clp_candidates"] == candidates


def test_backlot_checkpoint_clp_wins_over_tampered_standalone_cache(tmp_path):
    """Board cabinets and runtime must display the same approved CLP truth."""
    project_dir = tmp_path / PROJECT_ID
    script = _script()
    approved = _manifest()
    candidates = _candidates(script)
    tampered = {
        "version": "2.0",
        "project_id": PROJECT_ID,
        "characters": [
            {
                "id": "injected",
                "name": "Injected Cache Identity",
                "visual_traits": "Must never reach the authoritative cabinet",
                "policy": "text_anchor_only",
                "prompt_anchor": "attacker cache",
            }
        ],
        "locations": [],
        "props": [],
    }
    _write_json(
        project_dir / "project.json",
        {
            "version": "1.0",
            "project_id": PROJECT_ID,
            "title": "CLP Board Hardening",
            "pipeline_type": "animated-explainer",
        },
    )
    _write_json(project_dir / "checkpoint_script.json", _script_checkpoint(script))
    _write_json(
        project_dir / "checkpoint_clp.json",
        _clp_checkpoint(approved, candidates),
    )
    _write_json(project_dir / "artifacts" / "clp_manifest.json", tampered)

    state = load_board_state(project_dir)

    assert state["artifacts"]["clp_manifest"] == approved
    assert state["clp"]["characters"] == []
    assert {
        "artifact": "clp_manifest",
        "status": "cache_mismatch_ignored",
        "reason": "checkpoint_clp.json remains authoritative",
    } in state["artifact_diagnostics"]


def test_backlot_noncanonical_nan_clp_cache_is_diagnostic_not_crash(tmp_path):
    project_dir = tmp_path / PROJECT_ID
    script = _script()
    approved = _manifest()
    candidates = _candidates(script)
    _write_json(
        project_dir / "project.json",
        {
            "version": "1.0",
            "project_id": PROJECT_ID,
            "title": "CLP Board Hardening",
            "pipeline_type": "animated-explainer",
        },
    )
    _write_json(project_dir / "checkpoint_script.json", _script_checkpoint(script))
    _write_json(
        project_dir / "checkpoint_clp.json",
        _clp_checkpoint(approved, candidates),
    )
    malformed_cache = dict(approved)
    malformed_cache["cache_score"] = float("nan")
    _write_json(project_dir / "artifacts" / "clp_manifest.json", malformed_cache)

    state = load_board_state(project_dir)

    assert state["artifacts"]["clp_manifest"] == approved
    assert state["clp"] == {"characters": [], "locations": [], "props": []}
    assert state["artifact_diagnostics"] == [
        {
            "artifact": "clp_manifest",
            "status": "invalid_cache_ignored",
            "reason": "standalone cache is not canonical JSON",
        }
    ]


def test_backlot_standalone_clp_without_checkpoint_is_not_authority(tmp_path):
    project_dir = tmp_path / PROJECT_ID
    standalone = {
        "version": "2.0",
        "project_id": PROJECT_ID,
        "characters": [
            {
                "id": "orphan",
                "name": "Orphan Cache",
                "visual_traits": "No checkpoint authority",
                "policy": "text_anchor_only",
                "prompt_anchor": "orphan",
            }
        ],
        "locations": [],
        "props": [],
    }
    _write_json(project_dir / "artifacts" / "clp_manifest.json", standalone)

    state = load_board_state(project_dir)

    assert "clp_manifest" not in state["artifacts"]
    assert state["clp"] == {"characters": [], "locations": [], "props": []}
    assert state["artifact_diagnostics"][0]["status"] == "untrusted_cache_ignored"


def test_backlot_invokes_one_verifier_with_clean_full_checkpoint_bundle(
    tmp_path, monkeypatch
):
    script = _script()
    script_checkpoint = _script_checkpoint(script)
    clp_checkpoint = _clp_checkpoint(_manifest(), _candidates(script))
    calls = []

    def _capture(current, artifacts=None, predecessor_checkpoint=None, pipeline_dir=None):
        calls.append((current, artifacts, predecessor_checkpoint, pipeline_dir))
        return True, None

    monkeypatch.setattr("lib.checkpoint.verify_gate_resolution", _capture)
    stage = _clp_stage(
        {"script": script_checkpoint, "clp": clp_checkpoint},
        project_dir=tmp_path / PROJECT_ID,
    )

    assert stage["auto_passed"] is True
    assert len(calls) == 1
    current, artifacts, predecessor, pipeline_dir = calls[0]
    assert current["artifacts"] is artifacts
    assert predecessor["stage"] == "script"
    assert predecessor["artifacts"]["script"] == script
    assert pipeline_dir == tmp_path


def test_backlot_binds_gate_identity_to_physical_project_directory(tmp_path):
    """A self-consistent foreign envelope cannot be trusted from another folder."""
    script = _script()
    stage = _clp_stage(
        {
            "script": _script_checkpoint(script),
            "clp": _clp_checkpoint(_manifest(), _candidates(script)),
        },
        project_dir=tmp_path / "different-physical-project",
    )
    assert stage["auto_passed"] is False


@pytest.mark.parametrize(
    "mutation",
    [
        "missing_predecessor",
        "invalid_human_approved_type",
        "invalid_boolean_counts",
        "extra_gate_key",
        "invalid_calendar_time",
        "cross_project_artifacts",
        "extra_artifact",
        "extra_checkpoint_key",
    ],
)
def test_backlot_gate_evidence_variants_fail_closed_without_raising(
    tmp_path, mutation
):
    script = _script()
    checkpoint = _clp_checkpoint(_manifest(), _candidates(script))
    checkpoints = {
        "script": _script_checkpoint(script),
        "clp": checkpoint,
    }

    if mutation == "missing_predecessor":
        checkpoints.pop("script")
    elif mutation == "invalid_human_approved_type":
        checkpoint["human_approved"] = 0
    elif mutation == "invalid_boolean_counts":
        checkpoint["gate_resolution"]["entity_counts"] = {
            "characters": False,
            "locations": False,
            "props": False,
        }
    elif mutation == "extra_gate_key":
        checkpoint["gate_resolution"]["unexpected"] = "must-not-be-trusted"
    elif mutation == "invalid_calendar_time":
        checkpoint["gate_resolution"]["resolved_at"] = (
            "2026-99-99T99:99:99+99:99"
        )
    elif mutation == "cross_project_artifacts":
        checkpoint["artifacts"]["clp_manifest"]["project_id"] = "other-project"
        checkpoint["artifacts"]["clp_candidates"]["project_id"] = "other-project"
    elif mutation == "extra_artifact":
        checkpoint["artifacts"]["typo_artifact"] = {}
    elif mutation == "extra_checkpoint_key":
        checkpoint["_evil"] = "must-reach-schema"

    stage = _clp_stage(checkpoints, project_dir=tmp_path / PROJECT_ID)
    assert stage["auto_passed"] is False


@pytest.mark.parametrize(
    "bad_artifacts",
    [
        None,
        "artifacts/clp.json",
        {"clp_manifest": "../outside.json", "clp_candidates": {}},
        {
            "clp_manifest": "artifacts/missing-manifest.json",
            "clp_candidates": "artifacts/missing-candidates.json",
        },
    ],
)
def test_backlot_malformed_or_unresolved_artifacts_never_raise(
    tmp_path, bad_artifacts
):
    script = _script()
    checkpoint = _clp_checkpoint(_manifest(), _candidates(script))
    checkpoint["artifacts"] = bad_artifacts
    stage = _clp_stage(
        {"script": _script_checkpoint(script), "clp": checkpoint},
        project_dir=tmp_path / PROJECT_ID,
    )
    assert stage["auto_passed"] is False


def test_explainer_directors_use_stage_scoped_artifacts_and_reference_compiler():
    repo_root = Path(__file__).resolve().parents[2]
    scene_text = (repo_root / "skills/pipelines/explainer/scene-director.md").read_text(
        encoding="utf-8"
    )
    asset_text = (repo_root / "skills/pipelines/explainer/asset-director.md").read_text(
        encoding="utf-8"
    )

    for address in (
        'state.artifacts["script"]["script"]',
        'state.artifacts["proposal"]["proposal_packet"]',
        'state.artifacts["clp"]["clp_manifest"]',
    ):
        assert address in scene_text
    for address in (
        'state.artifacts["scene_plan"]["scene_plan"]',
        'state.artifacts["scene_plan"]["clp_shot_bindings"]',
        'state.artifacts["clp"]["clp_manifest"]',
        'state.artifacts["script"]["script"]',
        'state.artifacts["proposal"]["proposal_packet"]',
    ):
        assert address in asset_text
    assert "compile_attached_references" in asset_text
    assert '"operation": "reference_to_video"' in asset_text
    assert '"project_dir": str(project_dir)' in asset_text
    assert '"clp_reference_inputs": clp_reference_inputs' in asset_text
    assert '"auxiliary_reference_images": auxiliary_reference_images' in asset_text
    assert "len(clp_reference_inputs) == strict_count" in asset_text
    assert "matches or exceeds" not in asset_text.lower()


def test_cinematic_directors_use_shared_digest_and_reference_compiler():
    repo_root = Path(__file__).resolve().parents[2]
    scene_text = (repo_root / "skills/pipelines/cinematic/scene-director.md").read_text(
        encoding="utf-8"
    )
    asset_text = (repo_root / "skills/pipelines/cinematic/asset-director.md").read_text(
        encoding="utf-8"
    )

    assert "canonical_digest" in scene_text
    assert "compile_attached_references" in asset_text
    assert '"operation": "reference_to_video"' in asset_text
    assert '"project_dir": str(project_dir)' in asset_text
    assert '"clp_reference_inputs": clp_reference_inputs' in asset_text
    assert '"auxiliary_reference_images": auxiliary_reference_images' in asset_text
    assert "len(clp_reference_inputs) == strict_count" in asset_text
    assert "matches or exceeds" not in asset_text.lower()


def test_clp_directors_share_canonical_source_digest_and_typed_gate_truth():
    repo_root = Path(__file__).resolve().parents[2]
    cinematic = (repo_root / "skills/pipelines/cinematic/clp-director.md").read_text(
        encoding="utf-8"
    )
    explainer = (repo_root / "skills/pipelines/explainer/clp-director.md").read_text(
        encoding="utf-8"
    )

    for text in (cinematic, explainer):
        assert 'state.artifacts["script"]["script"]' in text
        assert "canonical_digest(script)" in text
        assert "policy_bypass" not in text
    assert 'gate_resolution.mode="zero_entity_auto"' in explainer
    assert 'rule_version="clp_literal_empty_v1"' in explainer
    assert "no zero-entity bypass" in cinematic


def test_scene_plan_schema_rejects_empty_scene_id():
    invalid = {
        "version": "1.0",
        "scenes": [
            {
                "id": "",
                "type": "generated",
                "description": "Empty identifiers cannot participate in 1:1 binding.",
                "start_seconds": 0,
                "end_seconds": 1,
            }
        ],
    }
    with pytest.raises(Exception):
        validate_artifact("scene_plan", invalid)
