from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest
import yaml

from lib.production_units.contracts import (
    EXECUTION_DISPOSITIONS,
    POLICY_MODES,
    QUALIFICATION_STATUSES,
    ProductionUnitContractError,
    resolve_execution_contract,
    validate_capability_matrix,
    validate_qualification_profile,
)
from lib.clp_validator import canonical_digest


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = ROOT / "tests/fixtures/production_units"


def _policy(mode: str = "auto", *, stages=None) -> dict:
    return {
        "mode": mode,
        "target_seconds": 180,
        "hard_max_seconds": 480,
        "boundary_priority": "semantic_first",
        "oversize_policy": "allow_with_reason",
        "enabled_stages": stages or ["script", "scene_plan"],
    }


def _profile(*, status: str = "code_complete") -> dict:
    digest = "sha256:" + "a" * 64
    return {
        "version": "1.0",
        "profile_id": "animated-explainer-course-remotion-batch-v2",
        "profile_version": "0.1.0",
        "source": {
            "git_commit": "b" * 40,
            "pipeline_manifest": {
                "name": "animated-explainer",
                "version": "2.0",
                "sha256": digest,
            },
            "schemas": [
                {"name": "proposal_packet", "version": "1.0", "sha256": digest}
            ],
            "adapters": [
                {"name": "batch_v2_owned", "version": "1.0", "sha256": digest}
            ],
        },
        "pipeline": "animated-explainer",
        "content_form": "course_form",
        "supported_stages": ["script", "clp", "scene_plan", "assets", "edit", "compose"],
        "render": {"runtime": "remotion", "composition_mode": "templated"},
        "asset_route": {
            "route": "batch_v2_owned",
            "provider": "gemini_omni",
            "model": "gemini-omni-flash-preview",
            "adapter_version": "1.0",
        },
        "media_profile": {
            "name": "course-h264-1080p",
            "version": "1.0",
            "sha256": digest,
        },
        "qualification_status": status,
        "environment": {
            "os": "windows",
            "os_version": "11",
            "runtime": "python",
            "runtime_version": "3.13",
            "hardware": {
                "cpu": "offline-fixture",
                "ram_bytes": 17179869184,
                "gpu": None,
                "vram_bytes": None,
            },
        },
        "evidence": [
            {
                "evidence_id": "m6-0a-contract-tests",
                "kind": "contract_tests",
                "ref": "tests/production_units/test_contracts.py",
                "sha256": digest,
            }
        ],
        "requalification_triggers": [
            "git_commit_changed",
            "pipeline_manifest_changed",
            "schema_changed",
            "adapter_changed",
            "provider_or_model_changed",
            "runtime_changed",
            "media_profile_changed",
            "os_or_hardware_changed"
        ],
    }


def _matrix(profile: dict) -> dict:
    validated = validate_qualification_profile(profile)
    return {
        "version": "1.0",
        "matrix_id": "pup-m6-fixture",
        "matrix_version": "0.1.0",
        "generated_at": "2026-09-16T00:00:00+08:00",
        "entries": [
            {
                "profile_id": profile["profile_id"],
                "profile_version": profile["profile_version"],
                "profile_ref": "tests/fixtures/production_units/profile.json",
                "profile_sha256": canonical_digest(validated),
                "selector": {
                    "pipeline": profile["pipeline"],
                    "content_form": profile["content_form"],
                    "supported_stages": profile["supported_stages"],
                    "render_runtime": profile["render"]["runtime"],
                    "composition_mode": profile["render"]["composition_mode"],
                    "asset_route": profile["asset_route"]["route"],
                    "provider": profile["asset_route"]["provider"],
                    "model": profile["asset_route"]["model"],
                    "media_profile": profile["media_profile"]["name"],
                },
                "manifest_supported": True,
                "qualification_status": profile["qualification_status"],
                "reason": "M6.0A contract fixture; no beta or production claim.",
            }
        ],
    }


def test_proposal_policy_mode_is_not_execution_disposition() -> None:
    schema = json.loads(
        (ROOT / "schemas/artifacts/proposal_packet.schema.json").read_text(encoding="utf-8")
    )
    schema_modes = set(
        schema["properties"]["production_plan"]["properties"]
        ["production_unit_policy"]["properties"]["mode"]["enum"]
    )
    assert schema_modes == POLICY_MODES
    assert schema_modes.isdisjoint(EXECUTION_DISPOSITIONS)


def test_qualification_status_vocabulary_is_shared_by_both_schemas() -> None:
    profile_schema = json.loads(
        (ROOT / "schemas/execution/production_unit_qualification_profile.schema.json")
        .read_text(encoding="utf-8")
    )
    matrix_schema = json.loads(
        (ROOT / "schemas/execution/production_unit_capability_matrix.schema.json")
        .read_text(encoding="utf-8")
    )
    assert set(profile_schema["$defs"]["status"]["enum"]) == QUALIFICATION_STATUSES
    assert set(matrix_schema["$defs"]["status"]["enum"]) == QUALIFICATION_STATUSES


@pytest.mark.parametrize("policy_mode", ["auto", "fixed"])
@pytest.mark.parametrize("disposition", ["compare_only", "publish_candidate"])
def test_approved_policy_and_execution_disposition_are_independent(
    policy_mode: str, disposition: str
) -> None:
    contract = resolve_execution_contract(
        stage="script",
        production_unit_policy=_policy(policy_mode),
        execution_disposition=disposition,
    )
    assert contract is not None
    assert contract["policy_mode"] == policy_mode
    assert (
        contract["policy_mode_authority"]
        == "validated_proposal_checkpoint_required"
    )
    assert contract["legacy_mode_alias_used"] is False
    assert contract["execution_disposition"] == disposition


def test_missing_or_off_policy_is_strict_noop() -> None:
    assert resolve_execution_contract(
        stage="script", helper_target_seconds=float("nan")
    ) is None
    assert resolve_execution_contract(
        stage="script",
        production_unit_policy={"mode": "off"},
        helper_hard_max_seconds=-1,
    ) is None


@pytest.mark.parametrize(
    ("kwargs", "code"),
    [
        (
            {"production_unit_policy": _policy(), "execution_disposition": "compare_only", "legacy_mode": "compare_only"},
            "MIXED_EXECUTION_VOCABULARY",
        ),
        (
            {"production_unit_policy": {"mode": "off"}, "execution_disposition": "compare_only"},
            "DISPOSITION_WITH_OFF_POLICY",
        ),
        (
            {"production_unit_policy": _policy(stages=["script"]), "execution_disposition": "compare_only", "stage": "scene_plan"},
            "STAGE_NOT_ENABLED",
        ),
        (
            {"production_unit_policy": _policy(), "execution_disposition": "publish_candidate", "allowed_dispositions": {"compare_only"}},
            "UNSUPPORTED_EXECUTION_DISPOSITION",
        ),
    ],
)
def test_invalid_or_unsupported_mapping_fails_closed(kwargs, code: str) -> None:
    arguments = {"stage": "script", **kwargs}
    with pytest.raises(ProductionUnitContractError) as caught:
        resolve_execution_contract(**arguments)
    assert caught.value.code == code


def test_legacy_execution_mode_is_explicit_compatibility_only() -> None:
    contract = resolve_execution_contract(
        stage="script",
        legacy_mode="compare_only",
        helper_target_seconds=300,
        helper_hard_max_seconds=480,
    )
    assert contract is not None
    assert contract["policy_mode"] == "auto"
    assert contract["execution_disposition"] == "compare_only"
    assert contract["target_seconds"] == 300
    assert contract["legacy_mode_alias_used"] is True
    assert contract["policy_mode_authority"] == "none_legacy_diagnostic"


def test_qualification_profile_and_matrix_bind_exact_selectors() -> None:
    profile = _profile()
    validated_profile = validate_qualification_profile(profile)
    validated_matrix = validate_capability_matrix(_matrix(profile), [profile])
    assert canonical_digest(validated_profile).startswith("sha256:")
    assert canonical_digest(validated_matrix).startswith("sha256:")
    assert validated_matrix["entries"][0]["qualification_status"] == "code_complete"


@pytest.mark.parametrize(
    ("route", "provider", "model"),
    [
        ("batch_v2_owned", None, "gemini-omni-flash-preview"),
        ("batch_v2_owned", "gemini_omni", ""),
        ("none", "gemini_omni", None),
        ("none", None, "gemini-omni-flash-preview"),
    ],
)
def test_qualification_profile_rejects_contradictory_asset_route(
    route: str, provider: str | None, model: str | None
) -> None:
    profile = _profile()
    profile["asset_route"].update(
        {"route": route, "provider": provider, "model": model}
    )

    with pytest.raises(ProductionUnitContractError) as caught:
        validate_qualification_profile(profile)
    assert caught.value.code == "INVALID_QUALIFICATION_CONTRACT"


def test_local_only_asset_route_allows_no_model() -> None:
    profile = _profile()
    profile["asset_route"].update(
        {"route": "local_only", "provider": "ffmpeg", "model": None}
    )
    assert validate_qualification_profile(profile)["asset_route"]["model"] is None


def test_handoff_fixtures_are_exactly_bound_and_experimental() -> None:
    profile = json.loads(
        (FIXTURE_ROOT / "m6_0a_qualification_profile.fixture.json").read_text(
            encoding="utf-8"
        )
    )
    matrix = json.loads(
        (FIXTURE_ROOT / "m6_0a_capability_matrix.fixture.json").read_text(
            encoding="utf-8"
        )
    )
    validated = validate_capability_matrix(matrix, [profile])
    status = validated["entries"][0]["qualification_status"]
    assert status == "experimental"
    assert status not in {"beta_qualified", "production_qualified"}


@pytest.mark.parametrize(
    ("fixture_name", "expected_code"),
    [
        (
            "invalid/m6_0a_stale_profile_digest.fixture.json",
            "STALE_QUALIFICATION_PROFILE",
        ),
        (
            "invalid/m6_0a_selector_drift.fixture.json",
            "QUALIFICATION_SELECTOR_DRIFT",
        ),
        (
            "invalid/m6_0a_status_drift.fixture.json",
            "QUALIFICATION_STATUS_DRIFT",
        ),
    ],
)
def test_shared_invalid_matrix_fixtures_fail_closed(
    fixture_name: str, expected_code: str
) -> None:
    profile = json.loads(
        (FIXTURE_ROOT / "m6_0a_qualification_profile.fixture.json").read_text(
            encoding="utf-8"
        )
    )
    matrix = json.loads((FIXTURE_ROOT / fixture_name).read_text(encoding="utf-8"))

    with pytest.raises(ProductionUnitContractError) as caught:
        validate_capability_matrix(matrix, [profile])
    assert caught.value.code == expected_code


def test_shared_beta_insufficient_evidence_fixture_fails_closed() -> None:
    profile = json.loads(
        (
            FIXTURE_ROOT
            / "invalid/m6_0a_beta_insufficient_evidence.fixture.json"
        ).read_text(encoding="utf-8")
    )

    with pytest.raises(ProductionUnitContractError) as caught:
        validate_qualification_profile(profile)
    assert caught.value.code == "INSUFFICIENT_QUALIFICATION_EVIDENCE"


def test_manifest_support_never_upgrades_qualification() -> None:
    manifest = yaml.safe_load(
        (ROOT / "pipeline_defs/animated-explainer.yaml").read_text(encoding="utf-8")
    )
    assert manifest["extensions"]["production_units"]["supported"] is True
    profile = _profile(status="experimental")
    matrix = validate_capability_matrix(_matrix(profile), [profile])
    assert matrix["entries"][0]["manifest_supported"] is True
    assert matrix["entries"][0]["qualification_status"] == "experimental"


def test_stale_matrix_profile_digest_fails_closed() -> None:
    profile = _profile()
    matrix = _matrix(profile)
    matrix["entries"][0]["profile_sha256"] = "sha256:" + "0" * 64
    with pytest.raises(ProductionUnitContractError) as caught:
        validate_capability_matrix(matrix, [profile])
    assert caught.value.code == "STALE_QUALIFICATION_PROFILE"


def test_beta_claim_requires_beta_e2e_evidence() -> None:
    profile = _profile(status="beta_qualified")
    with pytest.raises(ProductionUnitContractError) as caught:
        validate_qualification_profile(profile)
    assert caught.value.code == "INSUFFICIENT_QUALIFICATION_EVIDENCE"
