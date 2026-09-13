"""Read-time approval enforcement for persisted checkpoint envelopes."""

from __future__ import annotations

import json

import pytest

from lib.checkpoint import CheckpointValidationError, read_checkpoint, validate_checkpoint


def _script_checkpoint(*, approved: bool, required: bool = True) -> dict:
    return {
        "version": "1.0",
        "project_id": "read-gate",
        "pipeline_type": "cinematic",
        "stage": "script",
        "status": "completed",
        "timestamp": "2026-09-13T00:00:00Z",
        "human_approval_required": required,
        "human_approved": approved,
        "artifacts": {
            "script": {
                "version": "1.0",
                "title": "Read gate probe",
                "total_duration_seconds": 1,
                "sections": [
                    {
                        "id": "s1",
                        "text": "A persisted checkpoint cannot forge approval.",
                        "start_seconds": 0,
                        "end_seconds": 1,
                    }
                ],
            }
        },
    }


def test_validate_checkpoint_rejects_unapproved_manifest_gate_on_read(tmp_path) -> None:
    checkpoint = _script_checkpoint(approved=False, required=False)
    with pytest.raises(CheckpointValidationError, match="GATE VIOLATION"):
        validate_checkpoint(checkpoint, pipeline_dir=tmp_path)


def test_read_checkpoint_rejects_hand_edited_unapproved_gate(tmp_path) -> None:
    project = tmp_path / "read-gate"
    project.mkdir()
    path = project / "checkpoint_script.json"
    path.write_text(json.dumps(_script_checkpoint(approved=False)), encoding="utf-8")
    with pytest.raises(CheckpointValidationError, match="GATE VIOLATION"):
        read_checkpoint(tmp_path, "read-gate", "script")
