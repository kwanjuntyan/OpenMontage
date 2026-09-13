"""Contract tests for clp_manifest and related Sidecar artifact schemas, including fail-closed validation and negative red-team test cases."""

import json
import hashlib
import pytest
import jsonschema
from schemas.artifacts import validate_artifact, load_schema
from lib.clp_validator import (
    validate_clp_manifest_semantics,
    validate_clp_shot_bindings_semantics,
    check_strict_reference_budget,
    CLPValidationError,
    UnsatisfiedReferenceConstraintsError,
)
from lib.checkpoint import validate_checkpoint, CheckpointValidationError, write_checkpoint


_VALID_TIMESTAMP = "2026-09-13T00:00:00Z"


def _valid_script(title="CLP predecessor"):
    return {
        "version": "1.0",
        "title": title,
        "total_duration_seconds": 1,
        "sections": [
            {
                "id": "s1",
                "text": "A valid predecessor script.",
                "start_seconds": 0,
                "end_seconds": 1,
            }
        ],
    }


def _write_exact_script_predecessor(projects_root, project_id, pipeline_type, script=None):
    project_dir = projects_root / project_id
    project_dir.mkdir(parents=True, exist_ok=True)
    script = script or _valid_script()
    checkpoint = {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": pipeline_type,
        "stage": "script",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approval_required": True,
        "human_approved": True,
        "artifacts": {"script": script},
    }
    (project_dir / "checkpoint_script.json").write_text(
        json.dumps(checkpoint), encoding="utf-8"
    )
    return script, checkpoint


def _write_exact_clp_predecessor(projects_root, project_id, pipeline_type, manifest):
    from lib.clp_validator import canonical_digest

    script, _ = _write_exact_script_predecessor(
        projects_root, project_id, pipeline_type
    )
    project_dir = projects_root / project_id
    checkpoint = {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": pipeline_type,
        "stage": "clp",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approval_required": pipeline_type == "cinematic",
        "human_approved": True,
        "artifacts": {
            "clp_manifest": manifest,
            "clp_candidates": {
                "version": "2.0",
                "project_id": project_id,
                "source_script_sha256": canonical_digest(script),
                "candidates": {"characters": [], "locations": [], "props": []},
            },
        },
    }
    (project_dir / "checkpoint_clp.json").write_text(
        json.dumps(checkpoint), encoding="utf-8"
    )
    return checkpoint


def _persist_reference_runtime(
    project_dir, manifest, binding, *, pipeline_type="cinematic", scene_plan=None
):
    """Persist the exact approved chain required by the executable compiler."""
    from lib.clp_validator import canonical_digest

    project_dir.mkdir(parents=True, exist_ok=True)
    project_id = project_dir.name
    script = _valid_script("Reference runtime")
    if scene_plan is None:
        scene_plan = {
            "version": "1.0",
            "scenes": [
                {
                    "id": binding["shot_id"],
                    "type": "generated",
                    "description": "Reference runtime shot",
                    "start_seconds": 0,
                    "end_seconds": 1,
                }
            ],
        }
    bindings_doc = {
        "version": "2.0",
        "project_id": project_id,
        "source_scene_plan_sha256": canonical_digest(scene_plan),
        "clp_manifest_sha256": canonical_digest(manifest),
        "bindings": [binding],
    }
    candidates = {
        "version": "2.0",
        "project_id": project_id,
        "source_script_sha256": canonical_digest(script),
        "candidates": {"characters": [], "locations": [], "props": []},
    }
    marker = {
        "version": "1.0",
        "project_id": project_id,
        "title": "Reference runtime",
        "pipeline_type": pipeline_type,
    }
    envelope = {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": pipeline_type,
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approval_required": True,
        "human_approved": True,
    }
    scene_artifacts = {
        "scene_plan": scene_plan,
        "clp_shot_bindings": bindings_doc,
    }
    if pipeline_type == "cinematic":
        scene_artifacts["clp_manifest"] = manifest
    persisted = {
        "project.json": marker,
        "checkpoint_script.json": {
            **envelope,
            "stage": "script",
            "artifacts": {"script": script},
        },
        "checkpoint_clp.json": {
            **envelope,
            "stage": "clp",
            "artifacts": {
                "clp_manifest": manifest,
                "clp_candidates": candidates,
            },
        },
        "checkpoint_scene_plan.json": {
            **envelope,
            "stage": "scene_plan",
            "artifacts": scene_artifacts,
        },
    }
    for filename, payload in persisted.items():
        (project_dir / filename).write_text(json.dumps(payload), encoding="utf-8")
    return scene_plan, bindings_doc


def test_clp_manifest_schema_loads():
    """Verify clp_manifest schema is registered and can be loaded."""
    schema = load_schema("clp_manifest")
    assert schema["title"] == "CLP Manifest"
    assert "characters" in schema["properties"]
    assert "locations" in schema["properties"]
    assert "props" in schema["properties"]


def test_clp_manifest_valid_full(tmp_path):
    """Verify a complete CLP manifest passes validation with signature composite appearance."""
    import hashlib

    project_dir = tmp_path / "esg-pilot-episode"
    project_dir.mkdir()
    img_char = project_dir / "harrison.png"
    img_char.write_bytes(b"char-bytes-12345")
    hash_char = f"sha256:{hashlib.sha256(img_char.read_bytes()).hexdigest()}"

    img_loc = project_dir / "boardroom.png"
    img_loc.write_bytes(b"loc-bytes-67890")
    hash_loc = f"sha256:{hashlib.sha256(img_loc.read_bytes()).hexdigest()}"

    img_prop = project_dir / "contract.png"
    img_prop.write_bytes(b"prop-bytes-abcdef")
    hash_prop = f"sha256:{hashlib.sha256(img_prop.read_bytes()).hexdigest()}"

    data = {
        "version": "2.0",
        "project_id": "esg-pilot-episode",
        "characters": [
            {
                "id": "char_harrison",
                "name": "Harrison Sterling",
                "role": "Chief Auditor",
                "age": 55,
                "gender": "male",
                "visual_traits": "Bespoke navy suit, silver-templed grey hair, stern piercing eyes",
                "costume": "Double-breasted Italian wool suit, burgundy silk tie",
                "image": "harrison.png",
                "asset_sha256": hash_char,
                "gcs_url": "https://storage.googleapis.com/om-assets/clp/harrison.png",
                "prompt_anchor": "55yo British male executive, sharp jawline, silver hair, bespoke dark navy suit",
                "policy": "strict_reference",
            }
        ],
        "locations": [
            {
                "id": "loc_boardroom",
                "name": "London Executive Boardroom",
                "environment_description": "High-rise minimalist boardroom overlooking London skyline with floor-to-ceiling windows",
                "lighting": "Cool overcast daylight diffusing through sheer blinds",
                "palette": ["#1A2530", "#A0AAB2", "#D8E2DC"],
                "interior_exterior": "interior",
                "image": "boardroom.png",
                "asset_sha256": hash_loc,
                "prompt_anchor": "modern London corporate boardroom, glass skyscraper window, rainy overcast light",
                "policy": "strict_reference",
            }
        ],
        "props": [
            {
                "id": "prop_audit_contract",
                "name": "ESG Audit Dossier",
                "category": "hero_prop",
                "description": "Thick black leather-bound binder stamped with gold foil ESG seal",
                "material": "Full grain black leather, brass corner guards, gilded paper edges",
                "image": "contract.png",
                "asset_sha256": hash_prop,
                "prompt_anchor": "heavy black leather binder folder with gold stamped seal",
                "policy": "strict_reference",
            }
        ]
    }
    validate_artifact("clp_manifest", data, project_dir=project_dir)


def test_clp_manifest_empty_arrays_for_zero_entity_explainer():
    """Verify empty arrays pass validation (Approach 2: Zero-entity auto-bypass)."""
    data = {
        "version": "2.0",
        "project_id": "clean-motion-explainer",
        "characters": [],
        "locations": [],
        "props": []
    }
    validate_artifact("clp_manifest", data)


def test_strict_manifest_requires_explicit_matching_project_root(tmp_path):
    project_dir = tmp_path / "root-bound-project"
    project_dir.mkdir()
    image = project_dir / "hero.png"
    image.write_bytes(b"root-bound-hero")
    digest = "sha256:" + hashlib.sha256(image.read_bytes()).hexdigest()
    manifest = {
        "version": "2.0",
        "project_id": project_dir.name,
        "characters": [
            {
                "id": "hero",
                "name": "Hero",
                "visual_traits": "Signature look",
                "policy": "strict_reference",
                "image": image.name,
                "asset_sha256": digest,
            }
        ],
        "locations": [],
        "props": [],
    }

    with pytest.raises(CLPValidationError, match="explicit project_dir"):
        validate_artifact("clp_manifest", manifest)
    with pytest.raises(CLPValidationError, match="does not match project_dir"):
        validate_artifact("clp_manifest", manifest, project_dir=tmp_path)
    validate_artifact("clp_manifest", manifest, project_dir=project_dir)


def test_clp_manifest_rejects_additional_properties_looks():
    """Red-team: Reject attempts to inject multi-look arrays or unexpected properties."""
    data = {
        "version": "2.0",
        "project_id": "esg-pilot-episode",
        "characters": [
            {
                "id": "char_amy",
                "name": "Amy",
                "visual_traits": "Casual lab coat, dark brown hair",
                "policy": "strict_reference",
                "looks": ["lab_coat", "gala_dress"]  # Illegal property!
            }
        ],
        "locations": [],
        "props": []
    }
    with pytest.raises(jsonschema.ValidationError) as exc:
        validate_artifact("clp_manifest", data)
    assert "Additional properties are not allowed" in str(exc.value)


def test_clp_manifest_rejects_invalid_hash_format():
    """Red-team: Reject invalid asset_sha256 strings (must match regex pattern)."""
    data = {
        "version": "2.0",
        "project_id": "esg-pilot-episode",
        "characters": [
            {
                "id": "char_amy",
                "name": "Amy",
                "visual_traits": "Casual lab coat",
                "policy": "strict_reference",
                "image": "assets/amy.png",
                "asset_sha256": "not-a-hash"  # Invalid pattern!
            }
        ],
        "locations": [],
        "props": []
    }
    with pytest.raises(jsonschema.ValidationError):
        validate_artifact("clp_manifest", data)


def test_clp_candidates_sidecar_valid():
    """Verify clp_candidates sidecar schema passes validation."""
    data = {
        "version": "2.0",
        "project_id": "mole-stargazer",
        "source_script_sha256": "sha256:fedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321",
        "extracted_by": "gemini-2.5-flash",
        "candidates": {
            "characters": [{"name": "鼴鼠", "frequency": 12, "suggested_role": "主角"}],
            "locations": [{"name": "星空草地", "frequency": 8}],
            "props": [{"name": "天文望遠鏡", "frequency": 5}]
        }
    }
    validate_artifact("clp_candidates", data)


def test_clp_shot_bindings_sidecar_valid():
    """Verify clp_shot_bindings sidecar schema passes validation."""
    data = {
        "version": "2.0",
        "project_id": "mole-stargazer",
        "source_scene_plan_sha256": "sha256:1111222233334444555566667777888811112222333344445555666677778888",
        "clp_manifest_sha256": "sha256:9999888877776666555544443333222299998888777766665555444433332222",
        "bindings": [
            {
                "shot_id": "shot_01",
                "location_ref": "loc_grassland",
                "character_refs": ["char_mole"],
                "prop_refs": ["prop_telescope"],
                "focal_entity": "char_mole"
            }
        ]
    }
    validate_artifact("clp_shot_bindings", data)


def test_clp_validator_semantic_duplicate_ids():
    """Verify semantic validator detects duplicate entity IDs."""
    manifest = {
        "characters": [
            {"id": "char_mole", "name": "Mole 1", "visual_traits": "T1", "policy": "strict_reference", "image": "a.png", "asset_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000"},
            {"id": "char_mole", "name": "Mole 2", "visual_traits": "T2", "policy": "text_anchor_only", "prompt_anchor": "mole"},
        ],
        "locations": [],
        "props": []
    }
    errors = validate_clp_manifest_semantics(manifest)
    assert any("duplicate id 'char_mole'" in err for err in errors)


def test_clp_validator_semantic_dangling_references():
    """Verify semantic validator catches dangling references in shot bindings."""
    manifest = {
        "characters": [{"id": "char_mole", "name": "Mole", "visual_traits": "T1", "policy": "text_anchor_only", "prompt_anchor": "m"}],
        "locations": [],
        "props": []
    }
    bindings = {
        "bindings": [
            {
                "shot_id": "shot_01",
                "character_refs": ["char_nonexistent"],
                "location_ref": "loc_ghost",
            }
        ]
    }
    errors = validate_clp_shot_bindings_semantics(bindings, manifest)
    assert any("dangling character_ref 'char_nonexistent'" in err for err in errors)
    assert any("dangling location_ref 'loc_ghost'" in err for err in errors)


def test_strict_reference_budget_overflow_raises_error():
    """Verify that exceeding physical slots raises UnsatisfiedReferenceConstraintsError without network calls."""
    manifest = {
        "characters": [
            {"id": "c1", "policy": "strict_reference", "asset_sha256": "sha256:" + "1" * 64},
            {"id": "c2", "policy": "strict_reference", "asset_sha256": "sha256:" + "2" * 64},
            {"id": "c3", "policy": "strict_reference", "asset_sha256": "sha256:" + "3" * 64},
        ],
        "locations": [
            {"id": "loc_bg", "policy": "strict_reference", "asset_sha256": "sha256:" + "4" * 64}
        ],
        "props": []
    }
    binding = {
        "shot_id": "shot_climax",
        "character_refs": ["c1", "c2", "c3"],
        "location_ref": "loc_bg"
    }
    # Max slots = 2, but binding has 4 strict references!
    with pytest.raises(UnsatisfiedReferenceConstraintsError) as exc:
        check_strict_reference_budget("shot_climax", binding, manifest, max_slots=2)
    assert "exceeding downstream model slot capacity" in str(exc.value)


def test_checkpoint_validation_rejects_unknown_artifact():
    """Red-team P0-1: Checkpoint must fail closed if an unknown or misspelled artifact is present."""
    cp = {
        "version": "1.0",
        "project_id": "test-p",
        "pipeline_type": "animated-explainer",
        "stage": "research",
        "status": "in_progress",
        "human_approved": True,
        "artifacts": {
            "typo_artifact": {"some": "data"}  # Unknown artifact!
        }
    }
    with pytest.raises(CheckpointValidationError) as exc:
        validate_checkpoint(cp)
    assert "Unknown artifact 'typo_artifact'" in str(exc.value)


def test_checkpoint_explainer_clp_blocks_nonempty_without_approval(tmp_path):
    """Red-team P0-2: Animated explainer with non-empty CLP entities MUST block if human_approved is false."""
    project_id = "test-explainer-gate"
    artifacts = {
        "clp_manifest": {
            "version": "2.0",
            "project_id": project_id,
            "characters": [
                {
                    "id": "char_hero",
                    "name": "Hero",
                    "visual_traits": "Cartoon hero",
                    "policy": "text_anchor_only",
                    "prompt_anchor": "hero"
                }
            ],
            "locations": [],
            "props": []
        }
    }
    # Attempting to write completed without human_approved for non-empty entities must raise GATE VIOLATION
    with pytest.raises(CheckpointValidationError) as exc:
        write_checkpoint(
            pipeline_dir=tmp_path,
            project_id=project_id,
            stage="clp",
            status="completed",
            artifacts=artifacts,
            pipeline_type="animated-explainer",
            human_approved=False
        )
    assert "GATE VIOLATION" in str(exc.value)
    assert "Human approval is mandatory when entities exist" in str(exc.value)


def test_backlot_clp_explicit_empty_manifest_authoritative(tmp_path):
    """Verify that an explicit empty clp_manifest is authoritative and does NOT fall back to legacy."""
    from backlot.state import _derive_clp
    artifacts = {
        "clp_manifest": {
            "version": "2.0",
            "project_id": "test-zero",
            "characters": [],
            "locations": [],
            "props": []
        },
        "character_design": {
            "characters": [{"id": "legacy_char", "name": "Legacy Amy"}]
        }
    }
    result = _derive_clp(tmp_path, artifacts)
    # Must be strictly empty because clp_manifest is authoritative!
    assert result["characters"] == []
    assert result["locations"] == []
    assert result["props"] == []


def test_clp_manifest_cross_category_duplicate_id_rejected():
    """Red-team: Cross-category ID duplicate (e.g. character and prop both named 'shared') must be rejected."""
    data = {
        "version": "2.0",
        "project_id": "test-cross-dup",
        "characters": [
            {
                "id": "shared_hero",
                "name": "Hero",
                "visual_traits": "Hero person",
                "policy": "text_anchor_only",
                "prompt_anchor": "hero"
            }
        ],
        "locations": [],
        "props": [
            {
                "id": "shared_hero",  # Collision across categories!
                "name": "Hero Sword",
                "description": "Sword of hero",
                "policy": "text_anchor_only",
                "prompt_anchor": "sword"
            }
        ]
    }
    from lib.clp_validator import CLPValidationError
    with pytest.raises(CLPValidationError) as exc:
        validate_artifact("clp_manifest", data)
    assert "duplicate id 'shared_hero'" in str(exc.value)


def test_validate_checkpoint_catches_semantic_and_gate_violations():
    """Red-team P0-A & P0-D: validate_checkpoint() must reject semantic errors and unapproved non-empty explainer on read path."""
    from lib.clp_validator import CLPValidationError
    # 1. Semantic error in checkpoint artifact
    cp_semantic_error = {
        "version": "1.0",
        "project_id": "test-read-gate",
        "pipeline_type": "cinematic",
        "stage": "clp",
        "status": "in_progress",
        "human_approved": True,
        "artifacts": {
            "clp_manifest": {
                "version": "2.0",
                "project_id": "test-read-gate",
                "characters": [
                    {"id": "c1", "name": "A", "visual_traits": "V1", "policy": "text_anchor_only", "prompt_anchor": "a"},
                    {"id": "c1", "name": "B", "visual_traits": "V2", "policy": "text_anchor_only", "prompt_anchor": "b"},
                ],
                "locations": [],
                "props": []
            }
        }
    }
    with pytest.raises(CheckpointValidationError) as exc:
        validate_checkpoint(cp_semantic_error)
    assert "duplicate id 'c1'" in str(exc.value)

    # 2. Unapproved non-empty explainer on read path
    cp_unapproved_explainer = {
        "version": "1.0",
        "project_id": "test-read-gate",
        "stage": "clp",
        "pipeline_type": "animated-explainer",
        "status": "completed",
        "human_approved": False,
        "artifacts": {
            "clp_manifest": {
                "version": "2.0",
                "project_id": "test-read-gate",
                "characters": [
                    {"id": "c1", "name": "A", "visual_traits": "V1", "policy": "text_anchor_only", "prompt_anchor": "a"}
                ],
                "locations": [],
                "props": []
            }
        }
    }
    with pytest.raises(CheckpointValidationError) as exc:
        validate_checkpoint(cp_unapproved_explainer)
    assert "GATE VIOLATION" in str(exc.value)


def test_video_selector_enforces_slot_overflow_with_zero_api_calls(tmp_path):
    """Red-team P0-B: video_selector must raise UnsatisfiedReferenceConstraintsError with ZERO calls to provider."""
    from unittest.mock import MagicMock
    from tools.video.video_selector import VideoSelector
    from lib.clp_validator import UnsatisfiedReferenceConstraintsError

    selector = VideoSelector()

    class OneSlotTool:
        name = "fake_generator"
        provider = "fake"

        def __init__(self):
            self.execute = MagicMock()

        def get_reference_capability(
            self, *, model=None, operation="text_to_video", model_variant=None
        ):
            return {
                "operation": operation,
                "resolved_model": model or "fake-reference-model",
                "max_image_slots": 1,
                "strict_clp_supported": True,
                "canonical_input_key": "reference_images",
                "accepted_input_keys": ("reference_images",),
                "provider_payload_key": "reference_images",
            }

    fake_tool = OneSlotTool()

    project_dir = tmp_path / "test-selector-overflow"
    asset_dir = project_dir / "assets"
    asset_dir.mkdir(parents=True)
    image_paths = []
    image_digests = []
    for name in ("c1.png", "c2.png"):
        path = asset_dir / name
        path.write_bytes(name.encode("utf-8"))
        image_paths.append(f"assets/{name}")
        image_digests.append(
            "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        )

    binding = {
        "shot_id": "shot_01",
        "character_refs": ["c1", "c2"],  # 2 strict references!
    }
    manifest = {
        "version": "2.0",
        "project_id": "test-selector-overflow",
        "characters": [
            {
                "id": "c1",
                "name": "First duelist",
                "visual_traits": "First duelist signature look",
                "policy": "strict_reference",
                "image": image_paths[0],
                "asset_sha256": image_digests[0],
            },
            {
                "id": "c2",
                "name": "Second duelist",
                "visual_traits": "Second duelist signature look",
                "policy": "strict_reference",
                "image": image_paths[1],
                "asset_sha256": image_digests[1],
            },
        ],
        "locations": [],
        "props": []
    }

    inputs = {
        "prompt": "Epic duel",
        "operation": "reference_to_video",
        "project_dir": str(project_dir),
        "clp_binding": binding,
        "clp_manifest": manifest,
    }

    # Monkeypatch _select_best_tool to return fake_tool
    selector._select_best_tool = MagicMock(return_value=(fake_tool, MagicMock()))

    with pytest.raises(UnsatisfiedReferenceConstraintsError):
        selector.execute(inputs)

    # CRITICAL: Verify that the provider was NEVER called!
    fake_tool.execute.assert_not_called()


def test_cinematic_dag_requires_declared_produces_and_dependencies():
    """Red-team P0-C: Cinematic pipeline requires complete declared produces collection."""
    from lib.checkpoint import validate_checkpoint, CheckpointValidationError

    # 1. Stage 'clp' in cinematic without clp_candidates must fail
    cp_clp_missing_cand = {
        "version": "1.0",
        "project_id": "test-dag",
        "pipeline_type": "cinematic",
        "stage": "clp",
        "status": "completed",
        "human_approved": True,
        "artifacts": {
            "clp_manifest": {
                "version": "2.0",
                "project_id": "test-dag",
                "characters": [],
                "locations": [],
                "props": []
            }
        }
    }
    with pytest.raises(CheckpointValidationError) as exc:
        validate_checkpoint(cp_clp_missing_cand)
    assert "Stage 'clp' with status 'completed' in pipeline 'cinematic' must include declared produced artifact 'clp_candidates'" in str(exc.value)

    # 2. Stage 'scene_plan' in cinematic without clp_shot_bindings must fail
    cp_scene_missing_bindings = {
        "version": "1.0",
        "project_id": "test-dag",
        "pipeline_type": "cinematic",
        "stage": "scene_plan",
        "status": "completed",
        "human_approved": True,
        "artifacts": {
            "scene_plan": {
                "version": "1.0",
                "scenes": []
            }
        }
    }
    with pytest.raises(CheckpointValidationError) as exc:
        validate_checkpoint(cp_scene_missing_bindings)
    assert "Stage 'scene_plan' with status 'completed' in pipeline 'cinematic' must include declared produced artifact 'clp_shot_bindings'" in str(exc.value)


def test_nonempty_candidates_plus_empty_manifest_rejected_without_approval():
    """Red-team P0-D: Evasion attempt (candidates found entities, but manifest emptied to bypass gate) is rejected."""
    from lib.checkpoint import validate_checkpoint, CheckpointValidationError

    cp = {
        "version": "1.0",
        "project_id": "test-cand-bypass",
        "pipeline_type": "animated-explainer",
        "stage": "clp",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approved": False,
        "artifacts": {
            "clp_manifest": {
                "version": "2.0",
                "project_id": "test-cand-bypass",
                "characters": [],
                "locations": [],
                "props": []
            },
            "clp_candidates": {
                "version": "2.0",
                "project_id": "test-cand-bypass",
                "source_script_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
                "candidates": {
                    "characters": [{"name": "Hero", "frequency": 5}],
                    "locations": [],
                    "props": [],
                }
            }
        }
    }
    with pytest.raises(CheckpointValidationError) as exc:
        validate_checkpoint(cp)
    assert "GATE VIOLATION: stage 'clp' candidates contains 1 extracted entities" in str(exc.value)


def test_binding_exact_coverage_rejected_when_mismatched():
    """Red-team P0-C & P1: Shot bindings must have exact 1:1 coverage with scene-plan scenes."""
    from lib.clp_validator import validate_clp_shot_bindings_or_raise, CLPValidationError

    scene_plan = {
        "version": "1.0",
        "scenes": [
            {"id": "scene_01"},
            {"id": "scene_02"}
        ]
    }
    # Missing scene_02
    bindings_missing = {
        "version": "2.0",
        "project_id": "test-p",
        "source_scene_plan_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
        "clp_manifest_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
        "bindings": [
            {"shot_id": "scene_01", "character_refs": [], "prop_refs": []}
        ]
    }
    with pytest.raises(CLPValidationError) as exc:
        validate_clp_shot_bindings_or_raise(bindings_missing, scene_plan=scene_plan)
    assert "Missing shot bindings for scene-plan scenes: ['scene_02']" in str(exc.value)

    # Duplicate scene_01
    bindings_dup = {
        "version": "2.0",
        "project_id": "test-p",
        "source_scene_plan_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
        "clp_manifest_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
        "bindings": [
            {"shot_id": "scene_01", "character_refs": [], "prop_refs": []},
            {"shot_id": "scene_01", "character_refs": [], "prop_refs": []},
            {"shot_id": "scene_02", "character_refs": [], "prop_refs": []},
        ]
    }
    with pytest.raises(CLPValidationError) as exc:
        validate_clp_shot_bindings_or_raise(bindings_dup, scene_plan=scene_plan)
    assert "Duplicate shot binding for shot_id 'scene_01'" in str(exc.value)


def test_strict_count_with_max_slots_0_and_cross_category():
    """Red-team P0-B: Cross-category collision can NEVER overwrite strict entity to bypass slot limits."""
    from lib.clp_validator import check_strict_reference_budget, CLPValidationError, UnsatisfiedReferenceConstraintsError

    manifest = {
        "characters": [
            {"id": "shared", "policy": "strict_reference", "image": "c.png", "asset_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000"}
        ],
        "locations": [],
        "props": [
            {"id": "shared", "policy": "ignore"}
        ]
    }
    binding = {
        "shot_id": "shot_climax",
        "character_refs": ["shared"],
    }
    # Must raise either CLPValidationError (for cross-category collision) or UnsatisfiedReferenceConstraintsError.
    # It must NEVER return 0 or pass quietly!
    with pytest.raises((CLPValidationError, UnsatisfiedReferenceConstraintsError)):
        check_strict_reference_budget("shot_climax", binding, manifest, max_slots=0)


def test_legacy_strict_lock_field_rejected():
    """P1: ``policy`` is the only persisted reference-control truth."""
    from schemas.artifacts import validate_artifact

    data = {
        "version": "2.0",
        "project_id": "test-proj",
        "characters": [
            {
                "id": "c1",
                "name": "Amy",
                "visual_traits": "Lab coat",
                "policy": "text_anchor_only",
                "prompt_anchor": "amy in coat",
                "strict_lock": True,
            }
        ],
        "locations": [],
        "props": []
    }
    with pytest.raises(jsonschema.ValidationError, match="strict_lock"):
        validate_artifact("clp_manifest", data)


# ==============================================================================
# SECTION 4.18 PROBE VERIFICATION SUITE (ALL 6 PROBES FLIPPED TO PASS/REJECTED)
# ==============================================================================

def test_section_418_probe_1_missing_file_rejected(tmp_path):
    """Probe 1: validate_artifact rejects non-existent strict image despite valid hex digest."""
    data = {
        "version": "2.0",
        "project_id": "probe-1-proj",
        "characters": [
            {
                "id": "char_missing",
                "name": "Ghost",
                "visual_traits": "Invisible",
                "policy": "strict_reference",
                "image": "definitely/missing.png",
                "asset_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
            }
        ],
        "locations": [],
        "props": [],
    }
    project_dir = tmp_path / "probe-1-proj"
    project_dir.mkdir()
    with pytest.raises(CLPValidationError) as exc:
        validate_artifact("clp_manifest", data, project_dir=project_dir)
    assert "strict_reference image file not found" in str(exc.value)


def test_section_418_probe_2_cinematic_scene_plan_dangling_ref_and_mismatches_rejected(tmp_path):
    """Probe 2: validate_checkpoint rejects cinematic scene_plan with ghost ref, project mismatch, or fake digest."""
    from lib.clp_validator import canonical_digest

    proj_dir = tmp_path / "probe-2-proj"
    proj_dir.mkdir(parents=True, exist_ok=True)

    approved_manifest = {
        "version": "2.0",
        "project_id": "probe-2-proj",
        "characters": [
            {
                "id": "char_hero",
                "name": "Hero",
                "visual_traits": "Cape",
                "policy": "text_anchor_only",
                "prompt_anchor": "hero in cape",
            }
        ],
        "locations": [],
        "props": [],
    }
    approved_m_hash = canonical_digest(approved_manifest)

    _write_exact_clp_predecessor(
        tmp_path, "probe-2-proj", "cinematic", approved_manifest
    )

    scene_plan = {
        "version": "1.0",
        "project_id": "probe-2-proj",
        "scenes": [{"id": "scene_01", "name": "Opening", "start_seconds": 0, "end_seconds": 5}],
    }
    sp_hash = canonical_digest(scene_plan)

    # 1. Ghost ref in bindings (references non-existent 'ghost' character)
    cp_ghost = {
        "version": "1.0",
        "project_id": "probe-2-proj",
        "pipeline_type": "cinematic",
        "stage": "scene_plan",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approved": True,
        "artifacts": {
            "scene_plan": scene_plan,
            "clp_shot_bindings": {
                "version": "2.0",
                "project_id": "probe-2-proj",
                "source_scene_plan_sha256": sp_hash,
                "clp_manifest_sha256": approved_m_hash,
                "bindings": [
                    {"shot_id": "scene_01", "character_refs": ["ghost"], "prop_refs": []}
                ],
            },
        },
    }
    with pytest.raises(CheckpointValidationError) as exc_ghost:
        validate_checkpoint(cp_ghost, pipeline_dir=tmp_path)
    assert "dangling character_ref 'ghost'" in str(exc_ghost.value)

    # 2. Project ID mismatch
    cp_mismatch = {
        "version": "1.0",
        "project_id": "probe-2-proj",
        "pipeline_type": "cinematic",
        "stage": "scene_plan",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approved": True,
        "artifacts": {
            "scene_plan": {
                "version": "1.0",
                "project_id": "wrong-proj",
                "scenes": [{"id": "scene_01", "name": "Opening", "start_seconds": 0, "end_seconds": 5}],
            },
        },
    }
    with pytest.raises(CheckpointValidationError) as exc:
        validate_checkpoint(cp_mismatch, pipeline_dir=tmp_path)
    assert "Project ID mismatch" in str(exc.value)

    # 3. Mismatched manifest digest in bindings
    cp_bad_m_hash = {
        "version": "1.0",
        "project_id": "probe-2-proj",
        "pipeline_type": "cinematic",
        "stage": "scene_plan",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approved": True,
        "artifacts": {
            "scene_plan": scene_plan,
            "clp_shot_bindings": {
                "version": "2.0",
                "project_id": "probe-2-proj",
                "source_scene_plan_sha256": sp_hash,
                "clp_manifest_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
                "bindings": [
                    {"shot_id": "scene_01", "character_refs": ["char_hero"], "prop_refs": []}
                ],
            },
        },
    }
    with pytest.raises(CheckpointValidationError) as exc_m_hash:
        validate_checkpoint(cp_bad_m_hash, pipeline_dir=tmp_path)
    assert "clp_manifest_sha256 mismatch" in str(exc_m_hash.value)


def test_section_418_probe_3_cinematic_empty_clp_unapproved_rejected():
    """Probe 3: validate_checkpoint rejects cinematic empty CLP without human approval."""
    cp = {
        "version": "1.0",
        "project_id": "probe-3-proj",
        "pipeline_type": "cinematic",
        "stage": "clp",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approved": False,
        "gate_resolution": {
            "mode": "policy_bypass",
            "entity_counts": {"characters": 0, "locations": 0, "props": 0},
        },
        "artifacts": {
            "clp_manifest": {
                "version": "2.0",
                "project_id": "probe-3-proj",
                "characters": [],
                "locations": [],
                "props": [],
            },
            "clp_candidates": {
                "version": "2.0",
                "project_id": "probe-3-proj",
                "source_script_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
                "candidates": {"characters": [], "locations": [], "props": []},
            },
        },
    }
    with pytest.raises(CheckpointValidationError) as exc:
        validate_checkpoint(cp)
    assert "GATE VIOLATION" in str(exc.value)


def test_section_418_probe_4_strict_entity_zero_reference_inputs_rejected(tmp_path):
    """Probe 4: VideoSelector.execute with 1 strict entity and 0 actual reference inputs raises error with 0 provider calls."""
    from unittest.mock import MagicMock
    from tools.video.video_selector import VideoSelector
    from tools.video.seedance_video import SeedanceVideo
    from lib.clp_validator import UnsatisfiedReferenceConstraintsError

    selector = VideoSelector()
    fake_tool = SeedanceVideo()
    provider_execute = MagicMock()
    fake_tool.execute = provider_execute

    project_dir = tmp_path / "probe-4-proj"
    asset_dir = project_dir / "assets"
    asset_dir.mkdir(parents=True)
    character_image = asset_dir / "char.png"
    character_image.write_bytes(b"strict-character")
    character_digest = "sha256:" + hashlib.sha256(
        character_image.read_bytes()
    ).hexdigest()

    binding = {
        "shot_id": "shot_01",
        "character_refs": ["char_strict"],
    }
    manifest = {
        "version": "2.0",
        "project_id": "probe-4-proj",
        "characters": [
                {
                    "id": "char_strict",
                    "name": "Strict Char",
                    "visual_traits": "Single immutable signature look",
                    "policy": "strict_reference",
                "image": "assets/char.png",
                "asset_sha256": character_digest,
            }
        ],
        "locations": [],
        "props": [],
    }
    _persist_reference_runtime(project_dir, manifest, binding)
    inputs = {
        "prompt": "Strict hero walks in",
        "operation": "reference_to_video",
        "binding": binding,
        "clp_manifest": manifest,
        "project_dir": str(project_dir),
        "clp_shot_id": "shot_01",
    }

    selector._select_best_tool = MagicMock(return_value=(fake_tool, MagicMock()))

    with pytest.raises(UnsatisfiedReferenceConstraintsError) as exc:
        selector.execute(inputs)
    assert "requires exactly 1 entity-bound strict references; received 0" in str(exc.value)
    provider_execute.assert_not_called()


def test_section_418_probe_5_explainer_clp_verified_auto_passed(tmp_path):
    """Probe 5: auto-pass requires an exact approved script predecessor."""
    from backlot.state import _build_stage_rail
    from lib.clp_validator import canonical_digest

    project_id = "probe-5-proj"
    project_dir = tmp_path / project_id
    project_dir.mkdir()
    script = {
        "version": "1.0",
        "title": "Zero-entity explainer",
        "total_duration_seconds": 1,
        "sections": [
            {
                "id": "s1",
                "text": "A purely abstract explanation.",
                "start_seconds": 0,
                "end_seconds": 1,
            }
        ],
    }
    script_cp = {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": "animated-explainer",
        "stage": "script",
        "status": "completed",
        "timestamp": "2026-09-13T00:00:00Z",
        "human_approval_required": True,
        "human_approved": True,
        "artifacts": {"script": script},
    }
    manifest = {
        "version": "2.0",
        "project_id": project_id,
        "characters": [],
        "locations": [],
        "props": [],
    }
    m_hash = canonical_digest(manifest)

    cp = {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": "animated-explainer",
        "stage": "clp",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approved": False,
        "gate_resolution": {
            "mode": "zero_entity_auto",
            "rule_version": "clp_literal_empty_v1",
            "entity_counts": {"characters": 0, "locations": 0, "props": 0},
            "manifest_sha256": m_hash,
            "resolved_at": "2026-09-13T00:00:00Z",
        },
        "artifacts": {
            "clp_manifest": manifest,
            "clp_candidates": {
                "version": "2.0",
                "project_id": project_id,
                "source_script_sha256": canonical_digest(script),
                "candidates": {"characters": [], "locations": [], "props": []},
            },
        },
    }

    pipeline_meta = {
        "pipeline_type": "animated-explainer",
        "stages": [{"name": "clp", "gated": False, "produces": ["clp_manifest", "clp_candidates"]}],
    }
    (project_dir / "checkpoint_script.json").write_text(
        json.dumps(script_cp), encoding="utf-8"
    )
    (project_dir / "checkpoint_clp.json").write_text(
        json.dumps(cp), encoding="utf-8"
    )
    checkpoints = {"script": script_cp, "clp": cp}
    rail = _build_stage_rail(
        pipeline_meta, checkpoints, history={}, project_dir=project_dir
    )
    clp_entry = next(s for s in rail if s["name"] == "clp")
    assert clp_entry.get("auto_passed") is True
    assert clp_entry.get("gate_skipped") is False


def test_section_418_probe_6_gated_script_with_policy_bypass_gate_skipped_not_auto_passed():
    """Probe 6: Backlot flags gated script with {mode: 'policy_bypass'} as gate_skipped=True and auto_passed=False."""
    from backlot.state import _build_stage_rail

    cp = {
        "version": "1.0",
        "project_id": "probe-6-proj",
        "pipeline_type": "animated-explainer",
        "stage": "script",
        "status": "completed",
        "human_approved": False,
        "gate_resolution": {
            "mode": "policy_bypass",
            "rule_version": "clp_literal_empty_v1",
            "entity_counts": {"characters": 0, "locations": 0, "props": 0},
            "manifest_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
            "resolved_at": "2026-09-13T00:00:00Z",
        },
        "artifacts": {"script": {"version": "1.0", "project_id": "probe-6-proj"}},
    }

    pipeline_meta = {
        "pipeline_type": "animated-explainer",
        "stages": [{"name": "script", "gated": True, "produces": ["script"]}],
    }
    checkpoints = {"script": cp}
    rail = _build_stage_rail(pipeline_meta, checkpoints, history={})
    script_entry = next(s for s in rail if s["name"] == "script")
    assert script_entry.get("gate_skipped") is True
    assert script_entry.get("auto_passed") is False


# ==============================================================================
# SECTION 4.20 CLOSURE TEST SUITE (ALL P0 GROUPS AND GOTCHAS RIGIDLY VERIFIED)
# ==============================================================================

def test_section_420_probe_a1_absolute_image_path_rejected(tmp_path):
    """P0-A: Schema and runtime reject absolute path (e.g. C:\\Windows\\win.ini)."""
    data = {
        "version": "2.0",
        "project_id": "probe-a1-proj",
        "characters": [
            {
                "id": "char_win",
                "name": "Win",
                "visual_traits": "System file",
                "policy": "strict_reference",
                "image": "C:\\Windows\\win.ini",
                "asset_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
            }
        ],
        "locations": [],
        "props": [],
    }
    with pytest.raises((jsonschema.ValidationError, CLPValidationError)):
        validate_artifact("clp_manifest", data, project_dir=tmp_path)


def test_section_420_probe_a2_symlink_escape_rejected(tmp_path):
    """P0-A: Symlink or junction escaping project_root is strictly rejected."""
    import hashlib
    import os
    import subprocess
    import sys
    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    outside_file = outside_dir / "secret.png"
    outside_file.write_bytes(b"secret-data-outside")
    outside_hash = f"sha256:{hashlib.sha256(outside_file.read_bytes()).hexdigest()}"

    proj_dir = tmp_path / "project_root"
    proj_dir.mkdir()
    symlink_file = proj_dir / "escaped.png"
    image_path = "escaped.png"
    junction = None
    try:
        symlink_file.symlink_to(outside_file)
    except OSError:
        if sys.platform != "win32":
            pytest.skip("Symlink creation not permitted in this test environment")
        # Windows directory junctions do not require Developer Mode/admin and
        # exercise the same post-resolve containment invariant as symlinks.
        junction = proj_dir / "escaped-junction"
        created = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(junction), str(outside_dir)],
            capture_output=True,
            text=True,
            check=False,
        )
        if created.returncode != 0:
            pytest.fail(f"Could not create Windows junction probe: {created.stderr or created.stdout}")
        image_path = "escaped-junction/secret.png"

    data = {
        "version": "2.0",
        "project_id": proj_dir.name,
        "characters": [
            {
                "id": "char_esc",
                "name": "Esc",
                "visual_traits": "Escaped",
                "policy": "strict_reference",
                "image": image_path,
                "asset_sha256": outside_hash,
            }
        ],
        "locations": [],
        "props": [],
    }
    try:
        with pytest.raises(CLPValidationError) as exc:
            validate_artifact("clp_manifest", data, project_dir=proj_dir)
        assert "asset path escapes project root" in str(exc.value)
    finally:
        if junction is not None and junction.exists():
            os.rmdir(junction)


def test_section_420_probe_a3_stale_candidate_source_script_hash_rejected(tmp_path):
    """P0-A: validate_checkpoint rejects CLP candidates with stale source_script_sha256."""
    from lib.clp_validator import canonical_digest

    proj_dir = tmp_path / "probe-a3-proj"
    proj_dir.mkdir(parents=True, exist_ok=True)

    real_script = _valid_script("Stale candidate source")
    _write_exact_script_predecessor(
        tmp_path,
        "probe-a3-proj",
        "animated-explainer",
        script=real_script,
    )

    # CLP checkpoint with fake/stale candidate source_script_sha256
    clp_cp = {
        "version": "1.0",
        "project_id": "probe-a3-proj",
        "pipeline_type": "animated-explainer",
        "stage": "clp",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approved": True,
        "artifacts": {
            "clp_manifest": {"version": "2.0", "project_id": "probe-a3-proj", "characters": [], "locations": [], "props": []},
            "clp_candidates": {
                "version": "2.0",
                "project_id": "probe-a3-proj",
                "source_script_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",  # STALE!
                "candidates": {"characters": [], "locations": [], "props": []},
            },
        },
    }
    with pytest.raises(CheckpointValidationError) as exc:
        validate_checkpoint(clp_cp, pipeline_dir=tmp_path)
    assert "source_script_sha256 mismatch with predecessor checkpoint_script.json" in str(exc.value)


def test_section_420_probe_a4_scene_local_manifest_shadowing_rejected(tmp_path):
    """P0-A: scene_plan checkpoint cannot shadow approved predecessor checkpoint_clp.json with altered manifest."""
    from lib.clp_validator import canonical_digest

    proj_dir = tmp_path / "probe-a4-proj"
    proj_dir.mkdir(parents=True, exist_ok=True)

    approved_manifest = {
        "version": "2.0",
        "project_id": "probe-a4-proj",
        "characters": [
            {"id": "char_hero", "name": "Approved Hero", "visual_traits": "Gold Suit", "policy": "text_anchor_only", "prompt_anchor": "hero"}
        ],
        "locations": [],
        "props": [],
    }
    _write_exact_clp_predecessor(
        tmp_path, "probe-a4-proj", "animated-explainer", approved_manifest
    )

    # Rogue local manifest inside scene_plan artifacts attempting to override approved predecessor
    rogue_manifest = {
        "version": "2.0",
        "project_id": "probe-a4-proj",
        "characters": [
            {"id": "char_rogue", "name": "Rogue Override", "visual_traits": "Black Suit", "policy": "text_anchor_only", "prompt_anchor": "rogue"}
        ],
        "locations": [],
        "props": [],
    }

    scene_plan = {
        "version": "1.0",
        "project_id": "probe-a4-proj",
        "scenes": [{"id": "s1"}],
    }
    bindings = {
        "version": "2.0",
        "project_id": "probe-a4-proj",
        "source_scene_plan_sha256": canonical_digest(scene_plan),
        "clp_manifest_sha256": canonical_digest(rogue_manifest),
        "bindings": [{"shot_id": "s1", "character_refs": ["char_rogue"], "prop_refs": []}],
    }

    scene_cp = {
        "version": "1.0",
        "project_id": "probe-a4-proj",
        "pipeline_type": "animated-explainer",
        "stage": "scene_plan",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approved": True,
        "artifacts": {
            "scene_plan": scene_plan,
            "clp_manifest": rogue_manifest,  # Rogue shadow!
            "clp_shot_bindings": bindings,
        },
    }
    with pytest.raises(CheckpointValidationError) as exc:
        validate_checkpoint(scene_cp, pipeline_dir=tmp_path)
    assert "Local clp_manifest shadows approved predecessor checkpoint_clp.json with different content" in str(exc.value)


def test_section_420_probe_b1_under_coverage_2_strict_1_ref_rejected(tmp_path):
    """P0-B: 2 strict entities + 1 structured ref fails with zero provider calls."""
    from unittest.mock import MagicMock
    from tools.video.video_selector import VideoSelector
    from tools.video.seedance_video import SeedanceVideo
    from lib.clp_validator import UnsatisfiedReferenceConstraintsError

    selector = VideoSelector()
    fake_tool = SeedanceVideo()
    provider_execute = MagicMock()
    fake_tool.execute = provider_execute

    project_dir = tmp_path / "probe-b1-proj"
    project_dir.mkdir()
    c1 = project_dir / "c1.png"
    c2 = project_dir / "c2.png"
    c1.write_bytes(b"character-one")
    c2.write_bytes(b"character-two")
    digest1 = "sha256:" + hashlib.sha256(c1.read_bytes()).hexdigest()
    digest2 = "sha256:" + hashlib.sha256(c2.read_bytes()).hexdigest()

    binding = {
        "shot_id": "shot_dual",
        "character_refs": ["char_1", "char_2"],
    }
    manifest = {
        "version": "2.0",
        "project_id": "probe-b1-proj",
        "characters": [
            {"id": "char_1", "name": "Char 1", "visual_traits": "One", "policy": "strict_reference", "image": "c1.png", "asset_sha256": digest1},
            {"id": "char_2", "name": "Char 2", "visual_traits": "Two", "policy": "strict_reference", "image": "c2.png", "asset_sha256": digest2},
        ],
        "locations": [],
        "props": [],
    }
    _persist_reference_runtime(project_dir, manifest, binding)
    # Only one exact entity-bound input is provided for two strict entities.
    inputs = {
        "prompt": "Two heroes meet",
        "operation": "reference_to_video",
        "binding": binding,
        "clp_manifest": manifest,
        "project_dir": str(project_dir),
        "clp_shot_id": "shot_dual",
        "clp_reference_inputs": [
            {"entity_id": "char_1", "asset_sha256": digest1, "path": "c1.png"}
        ],
    }
    selector._select_best_tool = MagicMock(return_value=(fake_tool, MagicMock()))

    with pytest.raises(UnsatisfiedReferenceConstraintsError) as exc:
        selector.execute(inputs)
    assert "requires exactly 2 entity-bound strict references; received 1" in str(exc.value)
    provider_execute.assert_not_called()


def test_section_420_probe_b2_dangling_character_ref_zero_provider_calls(tmp_path):
    """P0-B: Dangling character_ref='ghost' raises error with 0 provider calls."""
    from unittest.mock import MagicMock
    from tools.video.video_selector import VideoSelector
    from lib.clp_validator import UnsatisfiedReferenceConstraintsError

    selector = VideoSelector()
    fake_tool = MagicMock()
    selector._select_best_tool = MagicMock(return_value=(fake_tool, MagicMock()))

    binding = {
        "shot_id": "shot_ghost",
        "character_refs": ["ghost"],
    }
    manifest = {
        "version": "2.0",
        "project_id": "probe-b2-proj",
        "characters": [
            {
                "id": "char_real",
                "name": "Real",
                "visual_traits": "Real recurring presenter",
                "policy": "text_anchor_only",
                "prompt_anchor": "real",
            }
        ],
        "locations": [],
        "props": [],
    }
    project_dir = tmp_path / "probe-b2-proj"
    _persist_reference_runtime(project_dir, manifest, binding)
    inputs = {
        "prompt": "Ghost appears",
        "operation": "reference_to_video",
        "binding": binding,
        "clp_manifest": manifest,
        "project_dir": str(project_dir),
        "clp_shot_id": "shot_ghost",
    }

    with pytest.raises(UnsatisfiedReferenceConstraintsError) as exc:
        selector.execute(inputs)
    assert "dangling character_ref 'ghost'" in str(exc.value)
    fake_tool.execute.assert_not_called()


def test_section_420_probe_b3_manifest_binding_xor_rejected(tmp_path):
    """P0-B: Strict manifest without binding, or binding with refs without manifest, raises error with 0 provider calls."""
    from unittest.mock import MagicMock
    from tools.video.video_selector import VideoSelector
    from lib.clp_validator import UnsatisfiedReferenceConstraintsError

    selector = VideoSelector()
    fake_tool = MagicMock()
    selector._select_best_tool = MagicMock(return_value=(fake_tool, MagicMock()))

    # 1. Strict manifest without binding
    manifest = {
        "version": "2.0",
        "project_id": "probe-b3-proj",
        "characters": [
            {
                "id": "c1",
                "name": "C1",
                "visual_traits": "One signature look",
                "policy": "text_anchor_only",
                "prompt_anchor": "C1",
            }
        ],
        "locations": [],
        "props": [],
    }
    project_dir = tmp_path / "probe-b3-proj"
    binding = {"shot_id": "s1", "character_refs": ["c1"]}
    _persist_reference_runtime(project_dir, manifest, binding)
    with pytest.raises(UnsatisfiedReferenceConstraintsError) as exc1:
        selector.execute({
            "prompt": "No binding",
            "operation": "reference_to_video",
            "project_dir": str(project_dir),
            "clp_shot_id": "s1",
            "clp_manifest": manifest,
        })
    assert "both clp_binding and clp_manifest" in str(exc1.value)

    # 2. Binding with refs without manifest
    with pytest.raises(UnsatisfiedReferenceConstraintsError) as exc2:
        selector.execute({
            "prompt": "No manifest",
            "operation": "reference_to_video",
            "project_dir": str(project_dir),
            "clp_shot_id": "s1",
            "binding": binding,
        })
    assert "both clp_binding and clp_manifest" in str(exc2.value)

    fake_tool.execute.assert_not_called()


def test_section_420_probe_b4_loose_plural_reference_keys_rejected(tmp_path):
    """P0-B: legacy plural URL aliases cannot impersonate exact strict assets."""
    from unittest.mock import MagicMock
    from tools.video.video_selector import VideoSelector
    from tools.video.seedance_video import SeedanceVideo
    from lib.clp_validator import UnsatisfiedReferenceConstraintsError

    selector = VideoSelector()
    fake_tool = SeedanceVideo()
    provider_execute = MagicMock()
    fake_tool.execute = provider_execute

    binding = {"shot_id": "shot_plural", "character_refs": ["c1", "c2"]}
    project_dir = tmp_path / "probe-b4-proj"
    project_dir.mkdir()
    c1_path = project_dir / "c1.png"
    c2_path = project_dir / "c2.png"
    c1_path.write_bytes(b"plural-one")
    c2_path.write_bytes(b"plural-two")
    manifest = {
        "version": "2.0",
        "project_id": "probe-b4-proj",
        "characters": [
            {"id": "c1", "name": "C1", "visual_traits": "One", "policy": "strict_reference", "image": "c1.png", "asset_sha256": "sha256:" + hashlib.sha256(c1_path.read_bytes()).hexdigest()},
            {"id": "c2", "name": "C2", "visual_traits": "Two", "policy": "strict_reference", "image": "c2.png", "asset_sha256": "sha256:" + hashlib.sha256(c2_path.read_bytes()).hexdigest()},
        ],
        "locations": [],
        "props": [],
    }
    _persist_reference_runtime(project_dir, manifest, binding)
    inputs = {
        "prompt": "Two heroes in action",
        "operation": "reference_to_video",
        "binding": binding,
        "clp_manifest": manifest,
        "project_dir": str(project_dir),
        "clp_shot_id": "shot_plural",
        "reference_image_urls": ["https://example.com/ref1.png", "https://example.com/ref2.png"],
    }
    selector._select_best_tool = MagicMock(return_value=(fake_tool, None))

    with pytest.raises(UnsatisfiedReferenceConstraintsError, match="aliases are forbidden"):
        selector.execute(inputs)
    provider_execute.assert_not_called()


def test_section_420_probe_b5_seedance_and_atlas_typed_capacities():
    """P0-B: capacities are exact model-by-operation contracts."""
    from tools.video.seedance_video import SeedanceVideo
    from tools.video.atlas_video import AtlasVideo

    sv = SeedanceVideo()
    assert sv.get_reference_capacity(model="2.0", operation="reference_to_video") == 9
    assert sv.get_reference_capacity(model="2.5", operation="reference_to_video") == 30
    assert sv.get_reference_capacity(model="2.5", operation="image_to_video") == 1
    assert sv.get_reference_capacity(model="2.5", operation="text_to_video") == 0

    av = AtlasVideo()
    assert av.get_reference_capacity(
        model="bytedance/seedance-2.0/reference-to-video",
        operation="reference_to_video",
    ) == 9
    assert av.get_reference_capacity(
        model="bytedance/seedance-2.5/reference-to-video",
        operation="reference_to_video",
    ) == 30
    assert av.get_reference_capacity(
        model="bytedance/seedance-2.5/image-to-video",
        operation="image_to_video",
    ) == 1
    assert av.get_reference_capacity(
        model="bytedance/seedance-2.5/text-to-video",
        operation="text_to_video",
    ) == 0


def test_section_420_probe_c1_verify_gate_resolution_rejects_missing_explicit_false():
    """P0-C: verify_gate_resolution strictly rejects missing or non-boolean human_approved."""
    from lib.checkpoint import verify_gate_resolution

    cp = {
        "pipeline_type": "animated-explainer",
        "stage": "clp",
        "status": "completed",
        # human_approved is missing!
        "gate_resolution": {"mode": "zero_entity_auto"},
        "artifacts": {
            "clp_manifest": {"characters": [], "locations": [], "props": []},
            "clp_candidates": {
                "source_script_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
                "candidates": {"characters": [], "locations": [], "props": []},
            },
        },
    }
    is_valid, reason = verify_gate_resolution(cp)
    assert is_valid is False
    assert "human_approved must be explicitly boolean False" in reason


def test_section_420_probe_c2_verify_gate_resolution_rejects_date_only():
    """P0-C: verify_gate_resolution strictly rejects date-only resolved_at (requires ISO-8601 with tz)."""
    from lib.checkpoint import verify_gate_resolution
    from lib.clp_validator import canonical_digest

    project_id = "probe-c2-proj"
    manifest = {
        "version": "2.0",
        "project_id": project_id,
        "characters": [],
        "locations": [],
        "props": [],
    }
    m_hash = canonical_digest(manifest)

    script = _valid_script("Probe C2 predecessor")
    script_digest = canonical_digest(script)
    cp = {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": "animated-explainer",
        "stage": "clp",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approved": False,
        "gate_resolution": {
            "mode": "zero_entity_auto",
            "rule_version": "clp_literal_empty_v1",
            "entity_counts": {"characters": 0, "locations": 0, "props": 0},
            "manifest_sha256": m_hash,
            "resolved_at": "2026-09-13",  # DATE ONLY!
        },
        "artifacts": {
            "clp_manifest": manifest,
            "clp_candidates": {
                "version": "2.0",
                "project_id": project_id,
                "source_script_sha256": script_digest,
                "candidates": {"characters": [], "locations": [], "props": []},
            },
        },
    }
    predecessor = {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": "animated-explainer",
        "stage": "script",
        "status": "completed",
        "timestamp": _VALID_TIMESTAMP,
        "human_approval_required": True,
        "human_approved": True,
        "artifacts": {"script": script},
    }
    is_valid, reason = verify_gate_resolution(
        cp, predecessor_checkpoint=predecessor
    )
    assert is_valid is False
    assert "date-time" in reason or "ISO-8601 timestamp" in reason


def test_section_420_probe_c3_malformed_artifacts_never_raises_in_backlot():
    """P0-C: Backlot _build_stage_rail never raises on path-backed or malformed artifacts; marks auto_passed=False."""
    from backlot.state import _build_stage_rail

    malformed_cp = {
        "version": "1.0",
        "project_id": "malformed-proj",
        "pipeline_type": "animated-explainer",
        "stage": "clp",
        "status": "completed",
        "human_approved": False,
        "gate_resolution": {
            "mode": "zero_entity_auto",
            "rule_version": "clp_literal_empty_v1",
            "entity_counts": {"characters": 0, "locations": 0, "props": 0},
            "manifest_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
            "resolved_at": "2026-09-13T00:00:00Z",
        },
        "artifacts": "path/to/artifacts.json",  # Not a dict!
    }
    pipeline_meta = {
        "pipeline_type": "animated-explainer",
        "stages": [{"name": "clp", "gated": False, "produces": ["clp_manifest", "clp_candidates"]}],
    }
    rail = _build_stage_rail(pipeline_meta, {"clp": malformed_cp}, history={})
    clp_entry = next(s for s in rail if s["name"] == "clp")
    assert clp_entry.get("auto_passed") is False


def test_section_420_probe_d1_explainer_director_contract_integration(tmp_path):
    """P0-D: Explainer scene director contract produces bindings with exact digests and passes to selector."""
    from unittest.mock import MagicMock
    from tools.video.video_selector import VideoSelector
    from tools.video.seedance_video import SeedanceVideo
    from tools.base_tool import ToolResult
    from lib.clp_validator import canonical_digest, compile_attached_references

    project_dir = tmp_path / "explainer-prod"
    asset_dir = project_dir / "assets"
    asset_dir.mkdir(parents=True)
    professor_image = asset_dir / "prof.png"
    professor_image.write_bytes(b"approved-professor-composite")
    professor_digest = "sha256:" + hashlib.sha256(
        professor_image.read_bytes()
    ).hexdigest()

    scene_plan = {
        "version": "1.0",
        "scenes": [
            {
                "id": "scene_01",
                "type": "generated",
                "description": "Professor explains quantum physics",
                "start_seconds": 0,
                "end_seconds": 5,
            }
        ],
    }
    manifest = {
        "version": "2.0",
        "project_id": "explainer-prod",
        "characters": [
            {
                "id": "char_prof",
                "name": "Professor",
                "visual_traits": "Tweed jacket, glasses",
                "policy": "strict_reference",
                "image": "assets/prof.png",
                "asset_sha256": professor_digest,
            }
        ],
        "locations": [],
        "props": [],
    }
    # Scene Director produces bindings
    bindings_doc = {
        "version": "2.0",
        "project_id": "explainer-prod",
        "source_scene_plan_sha256": canonical_digest(scene_plan),
        "clp_manifest_sha256": canonical_digest(manifest),
        "bindings": [
            {"shot_id": "scene_01", "character_refs": ["char_prof"], "prop_refs": []}
        ],
    }
    validate_artifact("clp_shot_bindings", bindings_doc)
    _persist_reference_runtime(
        project_dir,
        manifest,
        bindings_doc["bindings"][0],
        pipeline_type="animated-explainer",
        scene_plan=scene_plan,
    )

    # Asset Director invokes VideoSelector with exact binding and reference
    selector = VideoSelector()
    fake_tool = SeedanceVideo()
    provider_execute = MagicMock(
        return_value=ToolResult(
            success=True, data={"video_url": "https://example.com/scene1.mp4"}
        )
    )
    fake_tool.execute = provider_execute
    selector._select_best_tool = MagicMock(return_value=(fake_tool, None))

    shot_binding = bindings_doc["bindings"][0]
    compiled = compile_attached_references(
        shot_binding,
        manifest,
        project_dir,
        expected_shot_id="scene_01",
    )
    result = selector.execute({
        "prompt": scene_plan["scenes"][0]["description"],
        "operation": "reference_to_video",
        "clp_binding": shot_binding,
        "clp_shot_id": "scene_01",
        "clp_manifest": manifest,
        "clp_reference_inputs": compiled,
        "project_dir": str(project_dir),
        "model_version": "2.5",
    })
    assert result.success is True
    provider_execute.assert_called_once()
    plan = provider_execute.call_args[0][0]["_reference_execution_plan"]
    assert plan.strict_count == 1
    assert plan.max_slots == 30  # Seedance 2.5 typed capacity!
    assert plan.slot_mappings[0].entity_id == "char_prof"
    assert plan.slot_mappings[0].materialized_input == str(professor_image.resolve())


def test_section_420_probe_p1_typo_pipeline_type_fails_closed():
    """P1: Pipeline manifest loader fails closed on typo pipeline_type (e.g. 'cinematic-typo')."""
    cp = {
        "version": "1.0",
        "project_id": "test-typo",
        "pipeline_type": "cinematic-typo",  # Typo!
        "stage": "scene_plan",
        "status": "completed",
        "human_approved": True,
        "artifacts": {
            "scene_plan": {"version": "1.0", "project_id": "test-typo", "scenes": []}
        },
    }
    with pytest.raises(CheckpointValidationError) as exc:
        validate_checkpoint(cp)
    assert "Unknown pipeline_type or invalid manifest 'cinematic-typo'" in str(exc.value)


def test_section_420_probe_p2_canonical_digest_deterministic():
    """P1: canonical_digest produces exact, deterministic SHA-256 digests across types."""
    from lib.clp_validator import canonical_digest, matches_digest

    obj1 = {"b": 2, "a": 1}
    obj2 = {"a": 1, "b": 2}
    digest1 = canonical_digest(obj1)
    digest2 = canonical_digest(obj2)
    assert digest1 == digest2
    assert matches_digest(digest1, obj1)
    assert matches_digest(digest1, obj2)
