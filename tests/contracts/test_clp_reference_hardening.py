from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from lib.clp_validator import (
    CANONICAL_JSON_VERSION,
    CLPValidationError,
    ReferenceSlotOverflowError,
    UnsatisfiedReferenceConstraintsError,
    build_reference_execution_plan,
    canonical_digest,
    canonical_json_bytes,
    compile_attached_references as _compile_attached_references,
    get_tool_reference_capability,
    get_tool_reference_capacity,
    load_authoritative_clp_shot,
    matches_digest,
    structured_reference_inputs,
    validate_provider_reference_submission,
)
from tools.base_tool import ToolResult, ToolStatus
from tools.video.atlas_video import AtlasVideo
from tools.video.seedance_video import SeedanceVideo
from tools.video.video_selector import VideoSelector


def compile_attached_references(binding, manifest, project_dir):
    """Test helper keeps the independent production shot id explicit."""
    return _compile_attached_references(
        binding,
        manifest,
        project_dir,
        expected_shot_id="shot-1",
    )


def _asset_digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _project(tmp_path: Path, *, count: int = 2) -> tuple[Path, dict, dict]:
    project_dir = tmp_path / "reference_test"
    assets_dir = project_dir / "assets"
    assets_dir.mkdir(parents=True)
    characters = []
    for index in range(1, count + 1):
        path = assets_dir / f"c{index}.png"
        path.write_bytes(f"identity-{index}".encode())
        characters.append(
            {
                "id": f"c{index}",
                "name": f"Character {index}",
                "visual_traits": f"Distinctive character {index}",
                "policy": "strict_reference",
                "image": f"assets/c{index}.png",
                "asset_sha256": _asset_digest(path),
            }
        )
    manifest = {
        "version": "2.0",
        "project_id": project_dir.name,
        "characters": characters,
        "locations": [],
        "props": [],
    }
    binding = {
        "shot_id": "shot-1",
        "character_refs": [character["id"] for character in characters],
        "prop_refs": [],
    }
    script = {
        "version": "1.0",
        "title": "Reference test",
        "total_duration_seconds": 1,
        "sections": [
            {
                "id": "s1",
                "text": "The reference characters appear.",
                "start_seconds": 0,
                "end_seconds": 1,
            }
        ],
    }
    scene_plan = {
        "version": "1.0",
        "scenes": [
            {
                "id": "shot-1",
                "type": "generated",
                "description": "Reference test shot",
                "start_seconds": 0,
                "end_seconds": 1,
            }
        ],
    }
    bindings_doc = {
        "version": "2.0",
        "project_id": project_dir.name,
        "source_scene_plan_sha256": canonical_digest(scene_plan),
        "clp_manifest_sha256": canonical_digest(manifest),
        "bindings": [binding],
    }
    candidates = {
        "version": "2.0",
        "project_id": project_dir.name,
        "source_script_sha256": canonical_digest(script),
        "candidates": {
            "characters": [
                {"name": character["name"], "frequency": 1}
                for character in characters
            ],
            "locations": [],
            "props": [],
        },
    }
    marker = {
        "version": "1.0",
        "project_id": project_dir.name,
        "title": "Reference test",
        "pipeline_type": "cinematic",
    }
    envelope = {
        "version": "1.0",
        "project_id": project_dir.name,
        "pipeline_type": "cinematic",
        "status": "completed",
        "timestamp": "2026-09-13T00:00:00Z",
        "human_approval_required": True,
        "human_approved": True,
    }
    persisted = {
        "script": {**envelope, "stage": "script", "artifacts": {"script": script}},
        "clp": {
            **envelope,
            "stage": "clp",
            "artifacts": {"clp_manifest": manifest, "clp_candidates": candidates},
        },
        "scene_plan": {
            **envelope,
            "stage": "scene_plan",
            "artifacts": {
                "scene_plan": scene_plan,
                "clp_manifest": manifest,
                "clp_shot_bindings": bindings_doc,
            },
        },
    }
    (project_dir / "project.json").write_text(json.dumps(marker), encoding="utf-8")
    for stage, checkpoint in persisted.items():
        (project_dir / f"checkpoint_{stage}.json").write_text(
            json.dumps(checkpoint), encoding="utf-8"
        )
    return project_dir, manifest, binding


class _TypedProvider:
    name = "typed_test_video"
    provider = "typed-test"
    reference_model_input_key = "model"
    input_schema = {"properties": {"reference_images": {"type": "array"}}}

    def __init__(self, slots: int = 4):
        self.slots = slots
        self.execute_calls = 0
        self.last_inputs = None

    def get_reference_capability(self, model=None, operation=None, model_variant=None):
        operation = str(operation or "text_to_video")
        return {
            "operation": operation,
            "resolved_model": str(model or "typed-v1") + (
                f"/{model_variant}" if model_variant else ""
            ),
            "max_image_slots": self.slots if operation == "reference_to_video" else 0,
            "strict_clp_supported": operation == "reference_to_video",
            "canonical_input_key": "reference_images",
            "accepted_input_keys": ("reference_images",),
            "provider_payload_key": "provider_reference_images",
        }

    def get_status(self):
        return ToolStatus.AVAILABLE

    def get_info(self):
        return {"agent_skills": [], "best_for": [], "usage_location": "test"}

    def execute(self, inputs):
        validate_provider_reference_submission(self, inputs)
        self.execute_calls += 1
        self.last_inputs = inputs
        return ToolResult(success=True, data={"video_url": "https://example.invalid/video.mp4"})


class _UntypedReferenceProvider:
    """Advertises reference video but has no executable typed CLP contract."""

    name = "untyped_reference_video"
    provider = "untyped-test"
    supports = {"reference_to_video": True}
    input_schema = {"properties": {"reference_image_urls": {"type": "array"}}}

    def __init__(self):
        self.execute_calls = 0

    def get_status(self):
        return ToolStatus.AVAILABLE

    def get_info(self):
        return {"agent_skills": [], "best_for": [], "usage_location": "test"}

    def execute(self, _inputs):
        self.execute_calls += 1
        return ToolResult(success=True, data={"video_url": "https://example.invalid/wrong.mp4"})


def _selector(provider: _TypedProvider) -> VideoSelector:
    selector = VideoSelector()
    selector._providers = MagicMock(return_value=[provider])
    selector._select_best_tool = MagicMock(return_value=(provider, None))
    return selector


def _execute(selector, project_dir, manifest, binding, references, **extra):
    return selector.execute(
        {
            "prompt": "A precise identity test",
            "operation": "reference_to_video",
            "project_dir": str(project_dir),
            "clp_manifest": manifest,
            "clp_binding": binding,
            "clp_shot_id": binding.get("shot_id", "shot-1"),
            "clp_reference_inputs": references,
            **extra,
        }
    )


def test_canonical_digest_has_one_version_and_rejects_legacy_spacing():
    artifact = {"b": 2, "a": 1}
    assert CANONICAL_JSON_VERSION == "openmontage-json-v1"
    assert canonical_json_bytes(artifact) == b'{"a":1,"b":2}'
    digest = canonical_digest(artifact)
    legacy = "sha256:" + hashlib.sha256(
        json.dumps(artifact, sort_keys=True).encode("utf-8")
    ).hexdigest()
    assert matches_digest(digest, artifact)
    assert legacy != digest
    assert not matches_digest(legacy, artifact)


def test_compiler_emits_exact_entity_bound_local_references(tmp_path):
    project_dir, manifest, binding = _project(tmp_path)
    compiled = compile_attached_references(binding, manifest, project_dir)
    assert [entry["entity_id"] for entry in compiled] == ["c1", "c2"]
    assert all(set(entry) == {"entity_id", "asset_sha256", "path"} for entry in compiled)
    assert all(Path(entry["path"]).is_absolute() for entry in compiled)


def test_compiler_rejects_project_root_identity_and_legacy_fields(tmp_path):
    project_dir, manifest, binding = _project(tmp_path)
    wrong_root = tmp_path / "another_project"
    wrong_root.mkdir()
    with pytest.raises(
        (CLPValidationError, ValueError), match="project_id|project_dir|project.json"
    ):
        compile_attached_references(binding, manifest, wrong_root)

    manifest["characters"][0]["strict_lock"] = True
    with pytest.raises(
        Exception, match="Additional properties|strict_lock|authoritative"
    ):
        compile_attached_references(binding, manifest, project_dir)


@pytest.mark.parametrize("mutation", ["legacy_looks", "invalid_policy"])
def test_execution_plan_revalidates_full_manifest_schema(tmp_path, mutation):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    if mutation == "legacy_looks":
        manifest["characters"][0]["looks"] = ["forbidden-variant"]
    else:
        manifest["characters"][0]["policy"] = "strict_referenc"

    with pytest.raises(CLPValidationError):
        build_reference_execution_plan(
            _TypedProvider(),
            "shot-1",
            binding,
            manifest,
            operation="reference_to_video",
            actual_references=compiled,
            project_dir=project_dir,
        )


@pytest.mark.parametrize("mutation", ["missing_shot_id", "extra_field"])
def test_execution_plan_rejects_noncanonical_binding_shape(tmp_path, mutation):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    if mutation == "missing_shot_id":
        binding.pop("shot_id")
    else:
        binding["unexpected"] = "smuggled"

    with pytest.raises(CLPValidationError, match="shot_id|unsupported fields"):
        build_reference_execution_plan(
            _TypedProvider(),
            "shot-1",
            binding,
            manifest,
            operation="reference_to_video",
            actual_references=compiled,
            project_dir=project_dir,
        )


def test_selector_normalizes_to_provider_canonical_key_and_preserves_order(tmp_path):
    project_dir, manifest, binding = _project(tmp_path)
    compiled = compile_attached_references(binding, manifest, project_dir)
    provider = _TypedProvider(slots=3)
    result = _execute(
        _selector(provider),
        project_dir,
        manifest,
        binding,
        compiled,
        auxiliary_reference_images=[{"url": "https://example.invalid/style.png"}],
    )
    assert result.success
    assert provider.execute_calls == 1
    assert provider.last_inputs["operation"] == "reference_to_video"
    assert provider.last_inputs["reference_images"] == [
        compiled[0]["path"],
        compiled[1]["path"],
        "https://example.invalid/style.png",
    ]
    assert "reference_image_paths" not in provider.last_inputs
    plan = provider.last_inputs["_reference_execution_plan"]
    assert plan.strict_entity_ids == ("c1", "c2")
    assert plan.auxiliary_references == ("https://example.invalid/style.png",)


def test_selector_auto_reroutes_from_untyped_to_capable_clp_provider(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    unsupported = _UntypedReferenceProvider()
    capable = _TypedProvider(slots=1)
    selector = VideoSelector()
    selector._providers = MagicMock(return_value=[unsupported, capable])

    def _choose(_inputs, candidates, _context):
        if unsupported in candidates:
            return unsupported, None
        return (candidates[0], None) if candidates else (None, None)

    selector._select_best_tool = MagicMock(side_effect=_choose)
    result = _execute(selector, project_dir, manifest, binding, compiled)

    assert result.success is True
    assert unsupported.execute_calls == 0
    assert capable.execute_calls == 1


@pytest.mark.parametrize(
    ("alias_key", "alias_value"),
    [
        ("image_url", "https://example.invalid/injected.png"),
        (
            "refers",
            [{"url": "https://example.invalid/injected.png", "type": "image"}],
        ),
    ],
)
def test_clp_loose_aliases_fail_before_selection_or_provider_status(
    tmp_path, alias_key, alias_value
):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    provider = _TypedProvider(slots=1)
    provider.get_status = MagicMock(
        side_effect=AssertionError("provider status must not be queried")
    )
    provider.execute = MagicMock(
        side_effect=AssertionError("provider execute must not be called")
    )
    selector = VideoSelector()
    selector._providers = MagicMock(return_value=[provider])
    selector._select_best_tool = MagicMock(
        side_effect=AssertionError("provider selection must not run")
    )

    with pytest.raises(UnsatisfiedReferenceConstraintsError, match="aliases"):
        _execute(
            selector,
            project_dir,
            manifest,
            binding,
            compiled,
            **{alias_key: alias_value},
        )

    selector._select_best_tool.assert_not_called()
    provider.get_status.assert_not_called()
    provider.execute.assert_not_called()


@pytest.mark.parametrize("provider_kind", ["seedance", "atlas"])
def test_zero_reference_clp_collections_do_not_deadlock_real_provider_preflight(
    tmp_path, provider_kind
):
    project_dir, manifest, binding = _project(tmp_path, count=0)
    provider = SeedanceVideo() if provider_kind == "seedance" else AtlasVideo()
    selector = VideoSelector()
    selector._providers = MagicMock(return_value=[provider])
    selector._select_best_tool = MagicMock(return_value=(provider, None))
    payload = {
        "prompt": "No recurring entity appears.",
        "operation": "text_to_video",
        "project_dir": str(project_dir),
        "clp_shot_id": "shot-1",
        "clp_manifest": manifest,
        "clp_binding": binding,
        "clp_reference_inputs": [],
        "auxiliary_reference_images": [],
    }

    if provider_kind == "seedance":
        guard = patch.object(provider, "_get_api_key", return_value=None)
    else:
        guard = patch("tools.atlas_client.get_api_key", return_value=None)
    with guard as key_lookup, patch("requests.post") as http:
        result = selector.execute(payload)

    assert result.success is False
    assert "not set" in result.error
    key_lookup.assert_called_once()
    http.assert_not_called()


def test_selector_routes_public_model_version_to_seedance_25_payload(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    seedance = SeedanceVideo()
    seedance.get_status = MagicMock(return_value=ToolStatus.AVAILABLE)
    selector = VideoSelector()
    selector._providers = MagicMock(return_value=[seedance])
    output_path = project_dir / "renders" / "seedance-25.mp4"

    submit_response = MagicMock()
    submit_response.json.return_value = {
        "status_url": "https://queue.invalid/status",
        "response_url": "https://queue.invalid/result",
    }
    status_response = MagicMock()
    status_response.json.return_value = {"status": "COMPLETED"}
    result_response = MagicMock()
    result_response.json.return_value = {
        "video": {"url": "https://assets.invalid/video.mp4"}
    }
    video_response = MagicMock(content=b"seedance-25-video")

    with patch.object(seedance, "_get_api_key", return_value="key"), patch(
        "tools.video._shared.upload_image_fal",
        return_value="https://assets.invalid/c1.png",
    ), patch("requests.post", return_value=submit_response) as post, patch(
        "requests.get",
        side_effect=[status_response, result_response, video_response],
    ), patch("tools.video.seedance_video.time.sleep"), patch(
        "tools.video._shared.probe_output", return_value={"duration_seconds": 5.0}
    ):
        result = selector.execute(
            {
                "prompt": "Seedance 2.5 exact route",
                "operation": "reference_to_video",
                "model_version": "2.5",
                "project_dir": str(project_dir),
                "clp_shot_id": "shot-1",
                "clp_manifest": manifest,
                "clp_binding": binding,
                "clp_reference_inputs": compiled,
                "output_path": str(output_path),
            }
        )

    assert result.success is True
    assert result.data["model_version"] == "2.5"
    assert post.call_args.args[0].endswith(
        "/bytedance/seedance-2.5/reference-to-video"
    )
    assert post.call_args.kwargs["json"]["image_urls"] == [
        "https://assets.invalid/c1.png"
    ]


@pytest.mark.parametrize(
    "bad_url",
    ["gs://bucket/style.png", "s3://bucket/style.png", " https://example.invalid/style.png"],
)
def test_auxiliary_reference_scheme_and_whitespace_are_fail_closed(tmp_path, bad_url):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    with pytest.raises(UnsatisfiedReferenceConstraintsError):
        build_reference_execution_plan(
            _TypedProvider(slots=2),
            "shot-1",
            binding,
            manifest,
            operation="reference_to_video",
            actual_references=compiled,
            auxiliary_references=[{"url": bad_url}],
            project_dir=project_dir,
        )


def test_selector_requires_explicit_reference_operation_before_provider(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    provider = _TypedProvider()
    with pytest.raises(UnsatisfiedReferenceConstraintsError, match="explicit"):
        _selector(provider).execute(
            {
                "prompt": "no implicit operation upgrade",
                "project_dir": str(project_dir),
                "clp_manifest": manifest,
                "clp_binding": binding,
                "clp_reference_inputs": compiled,
            }
        )
    assert provider.execute_calls == 0


@pytest.mark.parametrize("mutation", ["reverse", "digest", "duplicate", "extra", "remote", "hidden"])
def test_wrong_mapping_shapes_fail_before_all_side_effects(tmp_path, mutation):
    project_dir, manifest, binding = _project(tmp_path)
    compiled = compile_attached_references(binding, manifest, project_dir)
    if mutation == "reverse":
        supplied = list(reversed(compiled))
    elif mutation == "digest":
        supplied = [dict(entry) for entry in compiled]
        supplied[0]["asset_sha256"] = "sha256:" + "0" * 64
    elif mutation == "duplicate":
        supplied = [compiled[0], compiled[0]]
    elif mutation == "extra":
        supplied = [*compiled, dict(compiled[0])]
    elif mutation == "remote":
        supplied = [dict(entry) for entry in compiled]
        supplied[0].pop("path")
        supplied[0]["url"] = "https://example.invalid/wrong.png"
    else:
        supplied = [dict(entry) for entry in compiled]
        supplied[0]["hidden"] = "provider ambiguity"

    provider = _TypedProvider()
    with patch("tools.video._shared.upload_image_fal") as uploader, patch("requests.post") as http:
        with pytest.raises(UnsatisfiedReferenceConstraintsError):
            _execute(_selector(provider), project_dir, manifest, binding, supplied)
    assert provider.execute_calls == 0
    uploader.assert_not_called()
    http.assert_not_called()


def test_wrong_local_bytes_fail_before_all_side_effects(tmp_path):
    project_dir, manifest, binding = _project(tmp_path)
    compiled = compile_attached_references(binding, manifest, project_dir)
    Path(compiled[0]["path"]).write_bytes(b"substituted-identity")
    provider = _TypedProvider()
    with patch("tools.video._shared.upload_image_fal") as uploader, patch("requests.post") as http:
        with pytest.raises(UnsatisfiedReferenceConstraintsError, match="bytes mismatch"):
            _execute(_selector(provider), project_dir, manifest, binding, compiled)
    assert provider.execute_calls == 0
    uploader.assert_not_called()
    http.assert_not_called()


def test_bare_provider_arrays_cannot_satisfy_strict_mapping(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    provider = _TypedProvider()
    selector = _selector(provider)
    with patch("tools.video._shared.upload_image_fal") as uploader, patch("requests.post") as http:
        with pytest.raises(UnsatisfiedReferenceConstraintsError):
            selector.execute(
                {
                    "prompt": "ambiguous",
                    "operation": "reference_to_video",
                    "project_dir": str(project_dir),
                    "clp_manifest": manifest,
                    "clp_binding": binding,
                    "reference_image_paths": [str(project_dir / "assets/c1.png")],
                }
            )
    assert provider.execute_calls == 0
    uploader.assert_not_called()
    http.assert_not_called()


def test_strict_plus_auxiliary_share_one_physical_capacity(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    provider = _TypedProvider(slots=1)
    with pytest.raises(ReferenceSlotOverflowError):
        _execute(
            _selector(provider),
            project_dir,
            manifest,
            binding,
            compiled,
            auxiliary_reference_images=[{"url": "https://example.invalid/style.png"}],
        )
    assert provider.execute_calls == 0


def test_duplicate_binding_and_dangling_ref_fail_before_provider(tmp_path):
    project_dir, manifest, binding = _project(tmp_path)
    compiled = compile_attached_references(binding, manifest, project_dir)
    provider = _TypedProvider()
    duplicate = {**binding, "character_refs": ["c1", "c1"]}
    with pytest.raises(UnsatisfiedReferenceConstraintsError, match="authoritative"):
        _execute(_selector(provider), project_dir, manifest, duplicate, compiled)
    dangling = {**binding, "character_refs": ["c1", "ghost"]}
    with pytest.raises(UnsatisfiedReferenceConstraintsError, match="authoritative"):
        _execute(_selector(provider), project_dir, manifest, dangling, compiled)
    assert provider.execute_calls == 0


def test_structured_refs_require_manifest_and_binding_before_provider(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    provider = _TypedProvider()
    for omitted in ("clp_manifest", "clp_binding"):
        payload = {
            "prompt": "missing context",
            "operation": "reference_to_video",
            "project_dir": str(project_dir),
                "clp_manifest": manifest,
                "clp_binding": binding,
                "clp_shot_id": "shot-1",
                "clp_reference_inputs": compiled,
        }
        payload.pop(omitted)
        with pytest.raises(UnsatisfiedReferenceConstraintsError):
            _selector(provider).execute(payload)
    assert provider.execute_calls == 0


def test_capacity_contract_is_exact_and_unknown_tools_fail_closed():
    seedance = SeedanceVideo()
    assert seedance.get_reference_capacity("2.0", "reference_to_video") == 9
    assert seedance.get_reference_capacity("2.5", "reference_to_video") == 30
    assert seedance.get_reference_capacity("2.5", "text_to_video") == 0
    assert seedance.get_reference_capacity("2.5", "image_to_video") == 1
    seedance_i2v = seedance.get_reference_capability("2.0", "image_to_video")
    assert seedance_i2v["canonical_input_key"] == "image_path"
    assert seedance_i2v["provider_payload_key"] == "image_url"
    with pytest.raises(ValueError):
        seedance.get_reference_capacity("seedance-ish-2.5", "reference_to_video")

    atlas = AtlasVideo()
    assert atlas.get_reference_capacity(
        "bytedance/seedance-2.0/reference-to-video", "reference_to_video"
    ) == 9
    assert atlas.get_reference_capacity(
        "bytedance/seedance-2.5/reference-to-video", "reference_to_video"
    ) == 30
    assert atlas.get_reference_capacity(
        "bytedance/seedance-2.5/text-to-video", "text_to_video"
    ) == 0
    assert atlas.get_reference_capacity(
        "bytedance/seedance-2.5/image-to-video", "image_to_video"
    ) == 1
    standard_gemini = atlas.get_reference_capability(
        "google/gemini-omni-flash/reference-to-video",
        "reference_to_video",
        "standard",
    )
    developer_gemini = atlas.get_reference_capability(
        "google/gemini-omni-flash/reference-to-video",
        "reference_to_video",
        "developer",
    )
    assert standard_gemini["max_image_slots"] == 10
    assert standard_gemini["strict_clp_supported"] is True
    assert developer_gemini["resolved_model"].endswith("reference-to-video-developer")
    assert developer_gemini["max_image_slots"] == 0
    assert developer_gemini["strict_clp_supported"] is False

    class UnknownTool:
        name = "unknown"
        provider = "unknown"

    assert get_tool_reference_capacity(
        UnknownTool(), model="anything", operation="reference_to_video"
    ) == 0

    class ScalarOnlyTool:
        name = "scalar-only"
        provider = "legacy"

        def get_reference_capacity(self, model=None, operation=None, model_variant=None):
            return 99

    scalar_capability = get_tool_reference_capability(
        ScalarOnlyTool(), model="legacy-v1", operation="reference_to_video"
    )
    assert scalar_capability.max_image_slots == 99
    assert scalar_capability.strict_clp_supported is False


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("strict_clp_supported", 1),
        ("accepted_input_keys", "reference_images"),
        ("operation", 7),
        ("unexpected", "field"),
    ],
)
def test_typed_capability_rejects_coercible_or_extra_fields(field, bad_value):
    class MalformedCapabilityTool:
        name = "malformed_capability"
        provider = "test"

        def get_reference_capability(
            self, model=None, operation=None, model_variant=None
        ):
            capability = {
                "operation": operation or "reference_to_video",
                "resolved_model": model or "test/reference-to-video",
                "max_image_slots": 1,
                "strict_clp_supported": True,
                "canonical_input_key": "reference_images",
                "accepted_input_keys": ("reference_images",),
                "provider_payload_key": "reference_images",
            }
            capability[field] = bad_value
            return capability

    with pytest.raises(CLPValidationError):
        get_tool_reference_capability(
            MalformedCapabilityTool(), operation="reference_to_video"
        )


def test_scalar_capacity_cannot_authorize_strict_clp(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)

    class ScalarOnlyTool:
        name = "scalar-only"
        provider = "legacy"

        def get_reference_capacity(self, model=None, operation=None, model_variant=None):
            return 99

    with pytest.raises(UnsatisfiedReferenceConstraintsError, match="does not support"):
        build_reference_execution_plan(
            ScalarOnlyTool(),
            binding["shot_id"],
            binding,
            manifest,
            operation="reference_to_video",
            model="legacy-v1",
            actual_references=compiled,
            project_dir=project_dir,
        )


def test_strict_execution_requires_explicit_project_dir_before_provider_side_effects(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    provider = _TypedProvider()
    with patch("tools.video._shared.upload_image_fal") as uploader, patch("requests.post") as http:
        with pytest.raises(UnsatisfiedReferenceConstraintsError, match="project_dir"):
            _selector(provider).execute(
                {
                    "prompt": "missing authoritative root",
                    "operation": "reference_to_video",
                    "clp_shot_id": "shot-1",
                    "clp_manifest": manifest,
                    "clp_binding": binding,
                    "clp_reference_inputs": compiled,
                }
            )
    assert provider.execute_calls == 0
    uploader.assert_not_called()
    http.assert_not_called()


def test_competing_binding_aliases_are_rejected_at_selector_and_provider(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    provider = _TypedProvider()
    payload = {
        "prompt": "ambiguous binding authority",
        "operation": "reference_to_video",
        "project_dir": str(project_dir),
        "clp_manifest": manifest,
        "clp_binding": binding,
        "binding": dict(binding),
        "clp_reference_inputs": compiled,
    }

    with pytest.raises(UnsatisfiedReferenceConstraintsError, match="exactly one"):
        _selector(provider).execute(payload)
    with pytest.raises(UnsatisfiedReferenceConstraintsError, match="exactly one"):
        validate_provider_reference_submission(provider, payload)
    assert provider.execute_calls == 0


def test_text_anchor_clp_cannot_smuggle_loose_reference_alias(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    manifest["characters"][0]["policy"] = "text_anchor_only"
    manifest["characters"][0]["prompt_anchor"] = "silver-haired astronomer"
    provider = _TypedProvider()
    payload = {
        "prompt": "text-only identity policy",
        "operation": "reference_to_video",
        "project_dir": str(project_dir),
        "clp_manifest": manifest,
        "clp_binding": binding,
        "clp_shot_id": "shot-1",
        "reference_images": [str(project_dir / "assets/c1.png")],
    }
    with pytest.raises(
        UnsatisfiedReferenceConstraintsError, match="authoritative|checkpoint"
    ):
        _selector(provider).execute(payload)
    assert provider.execute_calls == 0

    seedance = SeedanceVideo()
    with patch.object(seedance, "_get_api_key", return_value="key") as key_lookup, patch(
        "tools.video._shared.upload_image_fal"
    ) as uploader, patch("requests.post") as http:
        result = seedance.execute(payload)
    assert not result.success
    key_lookup.assert_not_called()
    uploader.assert_not_called()
    http.assert_not_called()


def test_direct_seedance_cannot_bypass_missing_or_tampered_plan(tmp_path):
    project_dir, manifest, binding = _project(tmp_path)
    compiled = compile_attached_references(binding, manifest, project_dir)
    seedance = SeedanceVideo()
    base = {
        "prompt": "direct bypass",
        "operation": "reference_to_video",
        "model_version": "2.5",
        "project_dir": str(project_dir),
        "clp_manifest": manifest,
        "clp_binding": binding,
        "clp_reference_inputs": compiled,
        "reference_images": [entry["path"] for entry in compiled],
    }
    with patch.object(seedance, "_get_api_key", return_value="key") as key_lookup, patch(
        "tools.video._shared.upload_image_fal"
    ) as uploader, patch("requests.post") as http:
        result = seedance.execute(base)
    assert not result.success
    key_lookup.assert_not_called()
    uploader.assert_not_called()
    http.assert_not_called()

    plan = build_reference_execution_plan(
        seedance,
        binding["shot_id"],
        binding,
        manifest,
        operation="reference_to_video",
        model="2.5",
        actual_references=compiled,
        project_dir=project_dir,
    )
    tampered = {
        **base,
        "_reference_execution_plan": replace(plan, max_slots=999),
    }
    with patch.object(seedance, "_get_api_key", return_value="key") as key_lookup, patch(
        "tools.video._shared.upload_image_fal"
    ) as uploader, patch("requests.post") as http:
        result = seedance.execute(tampered)
    assert not result.success
    key_lookup.assert_not_called()
    uploader.assert_not_called()
    http.assert_not_called()


def test_provider_boundary_rejects_payload_extra_alias(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    seedance = SeedanceVideo()
    context = load_authoritative_clp_shot(project_dir, "shot-1")
    plan = build_reference_execution_plan(
        seedance,
        binding["shot_id"],
        binding,
        manifest,
        operation="reference_to_video",
        model="2.0",
        actual_references=compiled,
        project_dir=project_dir,
        bindings_doc=context.bindings_doc,
        scene_plan=context.scene_plan,
    )
    payload = {
        "prompt": "alias injection",
        "operation": "reference_to_video",
        "model_version": "2.0",
        "project_dir": str(project_dir),
        "clp_manifest": manifest,
        "clp_binding": binding,
        "clp_shot_id": "shot-1",
        "clp_shot_bindings": context.bindings_doc,
        "clp_scene_plan": context.scene_plan,
        "clp_reference_inputs": structured_reference_inputs(plan),
        "_reference_execution_plan": plan,
        "reference_images": [compiled[0]["path"]],
        "reference_image_urls": ["https://example.invalid/extra.png"],
    }
    with pytest.raises(UnsatisfiedReferenceConstraintsError, match="non-canonical"):
        validate_provider_reference_submission(seedance, payload)


def test_direct_atlas_missing_plan_stops_before_upload_or_http(tmp_path):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    atlas = AtlasVideo()
    payload = {
        "prompt": "direct atlas bypass",
        "operation": "reference_to_video",
        "model": "bytedance/seedance-2.5/reference-to-video",
        "project_dir": str(project_dir),
        "clp_manifest": manifest,
        "clp_binding": binding,
        "clp_reference_inputs": compiled,
        "reference_images": [compiled[0]["path"]],
    }
    with patch("tools.atlas_client.get_api_key", return_value="key") as key_lookup, patch(
        "tools.atlas_client.upload_media"
    ) as uploader, patch("tools.atlas_client.submit") as submit, patch("requests.post") as http:
        result = atlas.execute(payload)
    assert not result.success
    key_lookup.assert_not_called()
    uploader.assert_not_called()
    submit.assert_not_called()
    http.assert_not_called()


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("operation", 7),
        ("model_version", 2.5),
        ("model_version", None),
        ("model_version", ""),
        ("model_variant", 1),
        ("model_variant", None),
    ],
)
def test_seedance_route_selectors_reject_coercible_types_before_side_effects(
    field, invalid_value
):
    seedance = SeedanceVideo()
    payload = {
        "prompt": "typed route contract",
        "operation": "reference_to_video",
        "model_version": "2.5",
        "model_variant": "standard",
        "reference_image_urls": ["https://example.invalid/reference.png"],
    }
    payload[field] = invalid_value
    with patch.object(seedance, "_get_api_key", return_value="key") as key_lookup, patch(
        "tools.video._shared.upload_image_fal"
    ) as uploader, patch("requests.post") as http:
        result = seedance.execute(payload)
    assert not result.success
    key_lookup.assert_not_called()
    uploader.assert_not_called()
    http.assert_not_called()


def test_seedance_non_clp_cardinality_preflight_runs_before_upload():
    seedance = SeedanceVideo()
    payload = {
        "prompt": "too many local references",
        "operation": "reference_to_video",
        "model_version": "2.0",
        "reference_image_paths": [f"local-{index}.png" for index in range(10)],
    }
    with patch.object(seedance, "_get_api_key", return_value="key"), patch(
        "tools.video._shared.upload_image_fal"
    ) as uploader, patch("requests.post") as http:
        result = seedance.execute(payload)
    assert result.success is False
    assert "at most 9 reference images" in result.error
    uploader.assert_not_called()
    http.assert_not_called()


def test_seedance_upload_failure_is_normalized_to_tool_result():
    seedance = SeedanceVideo()
    payload = {
        "prompt": "one local reference",
        "operation": "reference_to_video",
        "model_version": "2.0",
        "reference_image_paths": ["missing.png"],
    }
    with patch.object(seedance, "_get_api_key", return_value="key"), patch(
        "tools.video._shared.upload_image_fal", side_effect=FileNotFoundError("missing")
    ), patch("requests.post") as http:
        result = seedance.execute(payload)
    assert result.success is False
    assert "video generation failed" in result.error
    http.assert_not_called()


def test_atlas_non_clp_cardinality_preflight_runs_before_upload():
    atlas = AtlasVideo()
    payload = {
        "prompt": "too many local references",
        "operation": "reference_to_video",
        "model": "bytedance/seedance-2.0/reference-to-video",
        "reference_image_paths": [f"local-{index}.png" for index in range(10)],
    }
    with patch("tools.atlas_client.get_api_key", return_value="key") as key_lookup, patch(
        "tools.atlas_client.upload_media"
    ) as uploader, patch("tools.atlas_client.submit") as submit:
        result = atlas.execute(payload)
    assert result.success is False
    assert "at most 9 images" in result.error
    key_lookup.assert_not_called()
    uploader.assert_not_called()
    submit.assert_not_called()


def test_atlas_explicit_developer_model_does_not_default_to_standard_variant():
    atlas = AtlasVideo()
    original = atlas.get_reference_capability
    resolved_routes = []

    def _capture(**kwargs):
        contract = original(**kwargs)
        resolved_routes.append(contract["resolved_model"])
        return contract

    with patch.object(atlas, "get_reference_capability", side_effect=_capture), patch(
        "tools.atlas_client.get_api_key", return_value=None
    ):
        result = atlas.execute(
            {
                "prompt": "developer route remains exact",
                "operation": "reference_to_video",
                "model": "google/gemini-omni-flash/reference-to-video-developer",
            }
        )
    assert result.success is False
    assert resolved_routes[0].endswith("reference-to-video-developer")


@pytest.mark.parametrize("reserved_key", ["reference_images", "model", "prompt", "refers"])
def test_atlas_extra_params_cannot_override_owned_payload_before_side_effects(
    tmp_path, reserved_key
):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    atlas = AtlasVideo()
    model = "bytedance/seedance-2.5/reference-to-video"
    plan = build_reference_execution_plan(
        atlas,
        binding["shot_id"],
        binding,
        manifest,
        operation="reference_to_video",
        model=model,
        actual_references=compiled,
        project_dir=project_dir,
    )
    payload = {
        "prompt": "locked Atlas payload",
        "operation": "reference_to_video",
        "model": model,
        "project_dir": str(project_dir),
        "clp_manifest": manifest,
        "clp_binding": binding,
        "clp_reference_inputs": structured_reference_inputs(plan),
        "_reference_execution_plan": plan,
        "reference_images": [compiled[0]["path"]],
        "extra_params": {reserved_key: "attacker-controlled"},
    }
    with patch("tools.atlas_client.get_api_key", return_value="key") as key_lookup, patch(
        "tools.atlas_client.upload_media"
    ) as uploader, patch("tools.atlas_client.submit") as submit, patch("requests.post") as http:
        result = atlas.execute(payload)
    assert not result.success
    assert "reserved Atlas payload keys" in result.error
    key_lookup.assert_not_called()
    uploader.assert_not_called()
    submit.assert_not_called()
    http.assert_not_called()


def test_atlas_h3_clp_stays_fail_closed_without_declared_strict_capacity(
    tmp_path,
):
    project_dir, manifest, binding = _project(tmp_path, count=1)
    compiled = compile_attached_references(binding, manifest, project_dir)
    atlas = AtlasVideo()
    selector = VideoSelector()
    selector._providers = MagicMock(return_value=[atlas])
    selector._select_best_tool = MagicMock(return_value=(atlas, None))
    base = {
        "prompt": "The approved signature character enters.",
        "operation": "reference_to_video",
        "model": "minimax/h3/reference-to-video",
        "duration": 4,
        "project_dir": str(project_dir),
        "clp_shot_id": "shot-1",
        "clp_manifest": manifest,
        "clp_binding": binding,
        "clp_reference_inputs": compiled,
        "output_path": str(project_dir / "renders" / "h3.mp4"),
    }

    # Local provider metadata confirms H3 accepts mixed references, but does
    # not publish an exact image-slot ceiling. Strict CLP may not invent one.
    for payload in (
        base,
        {
            **base,
            "refers": [
                {"url": "https://attacker.invalid/substitute.png", "type": "image"}
            ],
        },
    ):
        with patch("tools.atlas_client.get_api_key", return_value="key") as key_lookup, patch(
            "tools.atlas_client.upload_media"
        ) as uploader, patch("tools.atlas_client.submit") as submit:
            with pytest.raises(
                UnsatisfiedReferenceConstraintsError, match="support"
            ):
                selector.execute(payload)
        key_lookup.assert_not_called()
        uploader.assert_not_called()
        submit.assert_not_called()


def test_persisted_checkpoint_state_reaches_real_atlas_payload_and_rejects_mismatch(
    tmp_path,
):
    """Persisted stage truth must survive compiler, selector, and real gateway."""
    from lib.checkpoint import read_checkpoint

    project_id = "persisted-reference-chain"
    project_dir = tmp_path / project_id
    assets_dir = project_dir / "assets"
    assets_dir.mkdir(parents=True)
    identity_path = assets_dir / "hero.png"
    identity_path.write_bytes(b"persisted-signature-look")

    script = {
        "version": "1.0",
        "title": "Persisted reference chain",
        "total_duration_seconds": 4,
        "sections": [
            {
                "id": "section-1",
                "text": "The signature hero enters.",
                "start_seconds": 0,
                "end_seconds": 4,
            }
        ],
    }
    manifest = {
        "version": "2.0",
        "project_id": project_id,
        "characters": [
            {
                "id": "hero",
                "name": "Signature Hero",
                "visual_traits": "One immutable signature appearance",
                "policy": "strict_reference",
                "image": "assets/hero.png",
                "asset_sha256": _asset_digest(identity_path),
            }
        ],
        "locations": [],
        "props": [],
    }
    scene_plan = {
        "version": "1.0",
        "scenes": [
            {
                "id": "shot-1",
                "type": "generated",
                "description": "The signature hero enters the frame.",
                "start_seconds": 0,
                "end_seconds": 4,
            }
        ],
    }
    shot_binding = {
        "shot_id": "shot-1",
        "character_refs": ["hero"],
        "prop_refs": [],
    }
    bindings = {
        "version": "2.0",
        "project_id": project_id,
        "source_scene_plan_sha256": canonical_digest(scene_plan),
        "clp_manifest_sha256": canonical_digest(manifest),
        "bindings": [shot_binding],
    }
    candidates = {
        "version": "2.0",
        "project_id": project_id,
        "source_script_sha256": canonical_digest(script),
        "candidates": {
            "characters": [{"name": "Signature Hero", "frequency": 1}],
            "locations": [],
            "props": [],
        },
    }

    timestamp = "2026-09-13T00:00:00Z"
    checkpoint_base = {
        "version": "1.0",
        "project_id": project_id,
        "pipeline_type": "cinematic",
        "status": "completed",
        "timestamp": timestamp,
        "human_approval_required": True,
        "human_approved": True,
    }
    persisted = {
        "script": {
            **checkpoint_base,
            "stage": "script",
            "artifacts": {"script": script},
        },
        "clp": {
            **checkpoint_base,
            "stage": "clp",
            "artifacts": {
                "clp_manifest": manifest,
                "clp_candidates": candidates,
            },
        },
        "scene_plan": {
            **checkpoint_base,
            "stage": "scene_plan",
            "artifacts": {
                "scene_plan": scene_plan,
                "clp_manifest": manifest,
                "clp_shot_bindings": bindings,
            },
        },
    }
    (project_dir / "project.json").write_text(
        json.dumps(
            {
                "version": "1.0",
                "project_id": project_id,
                "title": "Persisted reference chain",
                "pipeline_type": "cinematic",
            }
        ),
        encoding="utf-8",
    )
    for stage, checkpoint in persisted.items():
        (project_dir / f"checkpoint_{stage}.json").write_text(
            json.dumps(checkpoint), encoding="utf-8"
        )

    # This is the production stage-scoped shape consumed by both directors.
    state = {
        "clp": read_checkpoint(tmp_path, project_id, "clp"),
        "scene_plan": read_checkpoint(tmp_path, project_id, "scene_plan"),
    }
    loaded_manifest = state["clp"]["artifacts"]["clp_manifest"]
    loaded_binding = state["scene_plan"]["artifacts"]["clp_shot_bindings"][
        "bindings"
    ][0]
    compiled = compile_attached_references(
        loaded_binding, loaded_manifest, project_dir
    )

    atlas = AtlasVideo()
    selector = VideoSelector()
    selector._providers = MagicMock(return_value=[atlas])
    selector._select_best_tool = MagicMock(return_value=(atlas, None))
    output_path = project_dir / "renders" / "shot-1.mp4"

    def _download(_url, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"mock-video")

    with patch("tools.atlas_client.get_api_key", return_value="key") as key_lookup, patch(
        "tools.atlas_client.upload_media",
        side_effect=lambda value, _key: f"https://assets.invalid/{Path(value).name}",
    ) as uploader, patch(
        "tools.atlas_client.submit", return_value="prediction-1"
    ) as submit, patch(
        "tools.atlas_client.poll",
        return_value={"outputs": ["https://assets.invalid/shot-1.mp4"]},
    ), patch(
        "tools.atlas_client.download", side_effect=_download
    ), patch(
        "tools.video._shared.probe_output", return_value={"duration_seconds": 4.0}
    ), patch("requests.post") as http:
        result = selector.execute(
            {
                "prompt": scene_plan["scenes"][0]["description"],
                "operation": "reference_to_video",
                "model": "bytedance/seedance-2.5/reference-to-video",
                "project_dir": str(project_dir),
                "clp_manifest": loaded_manifest,
                "clp_binding": loaded_binding,
                "clp_shot_id": "shot-1",
                "clp_reference_inputs": compiled,
                "output_path": str(output_path),
            }
        )

        assert result.success
        key_lookup.assert_called()
        uploader.assert_called_once_with(compiled[0]["path"], "key")
        provider_payload = submit.call_args.args[1]
        assert provider_payload["model"] == (
            "bytedance/seedance-2.5/reference-to-video"
        )
        assert provider_payload["reference_images"] == [
            "https://assets.invalid/hero.png"
        ]
        http.assert_not_called()

        key_lookup.reset_mock()
        uploader.reset_mock()
        submit.reset_mock()
        http.reset_mock()
        mismatched = [dict(compiled[0])]
        mismatched[0]["entity_id"] = "substituted-hero"
        with pytest.raises(UnsatisfiedReferenceConstraintsError, match="identity mismatch"):
            selector.execute(
                {
                    "prompt": "This request must stop before any side effect.",
                    "operation": "reference_to_video",
                    "model": "bytedance/seedance-2.5/reference-to-video",
                    "project_dir": str(project_dir),
                    "clp_manifest": loaded_manifest,
                    "clp_binding": loaded_binding,
                    "clp_shot_id": "shot-1",
                    "clp_reference_inputs": mismatched,
                    "output_path": str(output_path),
                }
            )
        key_lookup.assert_not_called()
        uploader.assert_not_called()
        submit.assert_not_called()
        http.assert_not_called()
