"""Shared vocabulary and qualification contracts for Production Units.

The approved proposal policy and the stage-internal execution intent are two
different axes.  This module is the single executable boundary between them.
It performs no I/O other than loading versioned JSON schemas for explicit
qualification validation.
"""

from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import jsonschema

from lib.clp_validator import canonical_digest


POLICY_MODES = frozenset({"off", "auto", "fixed"})
EXECUTION_DISPOSITIONS = frozenset({"compare_only", "publish_candidate"})
PUP_STAGES = frozenset({"script", "clp", "scene_plan", "assets", "edit", "compose"})
QUALIFICATION_STATUSES = frozenset(
    {
        "unknown",
        "unsupported",
        "experimental",
        "code_complete",
        "beta_qualified",
        "production_qualified",
        "disabled",
        "invalid",
    }
)

_POLICY_KEYS = {
    "mode",
    "target_seconds",
    "hard_max_seconds",
    "boundary_priority",
    "oversize_policy",
    "enabled_stages",
}
_SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "schemas" / "execution"


class ProductionUnitContractError(ValueError):
    """Fail-closed PUP vocabulary or qualification contract error."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _fail(code: str, message: str) -> None:
    raise ProductionUnitContractError(code, message)


def _positive_number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail("INVALID_POLICY", f"{field} must be a finite positive number")
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        _fail("INVALID_POLICY", f"{field} must be a finite positive number")
    return result


def _validate_policy(policy: Mapping[str, Any]) -> dict[str, Any]:
    value = deepcopy(dict(policy))
    unknown = set(value) - _POLICY_KEYS
    if unknown:
        _fail("INVALID_POLICY", f"unknown production-unit policy fields: {sorted(unknown)}")
    mode = value.get("mode")
    if mode not in POLICY_MODES:
        _fail("INVALID_POLICY_MODE", f"unsupported approved policy mode {mode!r}")
    if mode == "off":
        return value

    required = {
        "target_seconds",
        "boundary_priority",
        "oversize_policy",
        "enabled_stages",
    }
    missing = required - set(value)
    if missing:
        _fail("INVALID_POLICY", f"enabled policy is missing fields: {sorted(missing)}")
    target = _positive_number(value["target_seconds"], "target_seconds")
    hard_max = value.get("hard_max_seconds")
    if hard_max is not None and _positive_number(hard_max, "hard_max_seconds") < target:
        _fail("INVALID_POLICY", "hard_max_seconds must be >= target_seconds")
    if value["boundary_priority"] != "semantic_first":
        _fail("INVALID_POLICY", "boundary_priority must be 'semantic_first'")
    if value["oversize_policy"] not in {"allow_with_reason", "fail"}:
        _fail("INVALID_POLICY", "oversize_policy is unsupported")
    enabled = value["enabled_stages"]
    if not isinstance(enabled, list) or not enabled or any(
        not isinstance(stage, str) or stage not in PUP_STAGES for stage in enabled
    ):
        _fail("INVALID_POLICY", "enabled_stages must be unique supported PUP stages")
    if len(enabled) != len(set(enabled)):
        _fail("INVALID_POLICY", "enabled_stages must be unique supported PUP stages")
    return value


def resolve_execution_contract(
    *,
    stage: str,
    production_unit_policy: Mapping[str, Any] | None = None,
    execution_disposition: str | None = None,
    legacy_mode: str | None = None,
    allowed_dispositions: Iterable[str] = EXECUTION_DISPOSITIONS,
    helper_target_seconds: float = 180.0,
    helper_hard_max_seconds: float = 480.0,
) -> dict[str, Any] | None:
    """Resolve approved policy plus execution intent into one bounded call.

    ``legacy_mode`` preserves the M2-M5 helper API.  It is deliberately kept
    separate from the canonical arguments: mixed old/new vocabulary fails
    closed instead of guessing.  Missing policy and explicit ``off`` return
    before any stage input is inspected by the caller.
    """

    if stage not in PUP_STAGES:
        _fail("UNSUPPORTED_STAGE", f"unsupported Production Unit stage {stage!r}")
    allowed = frozenset(allowed_dispositions)
    if not allowed or not allowed.issubset(EXECUTION_DISPOSITIONS):
        _fail("INVALID_EXECUTION_CONTRACT", "allowed dispositions are invalid")

    canonical_supplied = (
        production_unit_policy is not None or execution_disposition is not None
    )
    if legacy_mode is not None and canonical_supplied:
        _fail(
            "MIXED_EXECUTION_VOCABULARY",
            "use production_unit_policy + execution_disposition or legacy mode, not both",
        )

    # Preserve the original default-off guarantee before touching any helper
    # duration or stage payload. The policy object itself remains validated
    # when explicitly supplied.
    if legacy_mode == "off":
        return None
    if legacy_mode is None and production_unit_policy is None:
        if execution_disposition is None:
            return None
        _fail(
            "DISPOSITION_WITHOUT_POLICY",
            "execution_disposition requires an approved non-off production_unit_policy",
        )
    if legacy_mode is None and production_unit_policy is not None:
        if not isinstance(production_unit_policy, Mapping):
            _fail("INVALID_POLICY", "production_unit_policy must be an object")
        early_policy = _validate_policy(production_unit_policy)
        if early_policy["mode"] == "off":
            if execution_disposition is not None:
                _fail(
                    "DISPOSITION_WITH_OFF_POLICY",
                    "off policy cannot carry an execution disposition",
                )
            return None

    helper_target = _positive_number(helper_target_seconds, "helper_target_seconds")
    helper_hard_max = _positive_number(
        helper_hard_max_seconds, "helper_hard_max_seconds"
    )
    if helper_hard_max < helper_target:
        _fail("INVALID_POLICY", "helper hard max must be >= helper target")

    legacy_used = legacy_mode is not None
    if legacy_used:
        if legacy_mode not in EXECUTION_DISPOSITIONS:
            _fail("UNSUPPORTED_LEGACY_MODE", f"unsupported legacy helper mode {legacy_mode!r}")
        policy = {
            "mode": "auto",
            "target_seconds": helper_target,
            "hard_max_seconds": helper_hard_max,
            "boundary_priority": "semantic_first",
            "oversize_policy": "allow_with_reason",
            "enabled_stages": [stage],
        }
        disposition = legacy_mode
    else:
        policy = _validate_policy(production_unit_policy)
        disposition = execution_disposition

    if disposition not in EXECUTION_DISPOSITIONS:
        _fail(
            "INVALID_EXECUTION_DISPOSITION",
            f"unsupported execution disposition {disposition!r}",
        )
    if disposition not in allowed:
        _fail(
            "UNSUPPORTED_EXECUTION_DISPOSITION",
            f"stage {stage!r} does not support {disposition!r}",
        )
    if stage not in policy["enabled_stages"]:
        _fail(
            "STAGE_NOT_ENABLED",
            f"approved policy does not enable Production Units for {stage!r}",
        )

    effective_target = float(policy["target_seconds"])
    effective_hard_max = float(
        policy.get("hard_max_seconds", max(helper_hard_max, effective_target))
    )
    if effective_hard_max < effective_target:
        _fail("INVALID_POLICY", "effective hard max must be >= target_seconds")
    contract = {
        "version": "1.0",
        "policy_mode": policy["mode"],
        "execution_disposition": disposition,
        "stage": stage,
        "target_seconds": effective_target,
        "hard_max_seconds": effective_hard_max,
        "legacy_mode_alias_used": legacy_used,
    }
    contract["contract_sha256"] = canonical_digest(contract)
    return contract


def execution_report_fields(contract: Mapping[str, Any]) -> dict[str, Any]:
    """Return additive report fields while retaining the M2-M5 alias."""

    disposition = contract["execution_disposition"]
    return {
        "execution_contract": deepcopy(dict(contract)),
        "policy_mode": contract["policy_mode"],
        "execution_disposition": disposition,
        # Deprecated M2-M5 compatibility alias.  This is not a proposal mode.
        "mode": disposition,
        "execution_contract_sha256": contract["contract_sha256"],
    }


def _load_execution_schema(name: str) -> dict[str, Any]:
    path = _SCHEMA_ROOT / f"{name}.schema.json"
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        _fail("QUALIFICATION_SCHEMA_UNAVAILABLE", f"cannot load {path}: {exc}")


def _validate_schema(name: str, value: Mapping[str, Any]) -> dict[str, Any]:
    candidate = deepcopy(dict(value))
    try:
        jsonschema.validate(
            instance=candidate,
            schema=_load_execution_schema(name),
            format_checker=jsonschema.FormatChecker(),
        )
    except jsonschema.ValidationError as exc:
        _fail("INVALID_QUALIFICATION_CONTRACT", f"{name}: {exc.message}")
    return candidate


def validate_qualification_profile(
    profile: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one exact, versioned qualification profile and its evidence."""

    candidate = _validate_schema("production_unit_qualification_profile", profile)
    status = candidate["qualification_status"]
    evidence_kinds = {item["kind"] for item in candidate["evidence"]}
    if status in {"beta_qualified", "production_qualified"} and not candidate.get(
        "qualified_at"
    ):
        _fail(
            "INSUFFICIENT_QUALIFICATION_EVIDENCE",
            f"{status} requires qualified_at",
        )
    if status == "beta_qualified" and "beta_e2e" not in evidence_kinds:
        _fail("INSUFFICIENT_QUALIFICATION_EVIDENCE", "beta_qualified requires beta_e2e evidence")
    if status == "production_qualified" and not {
        "beta_e2e",
        "production_sample",
    }.issubset(evidence_kinds):
        _fail(
            "INSUFFICIENT_QUALIFICATION_EVIDENCE",
            "production_qualified requires beta_e2e and production_sample evidence",
        )
    return candidate


def _profile_selector(profile: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "pipeline": profile["pipeline"],
        "content_form": profile["content_form"],
        "supported_stages": profile["supported_stages"],
        "render_runtime": profile["render"]["runtime"],
        "composition_mode": profile["render"]["composition_mode"],
        "asset_route": profile["asset_route"]["route"],
        "provider": profile["asset_route"]["provider"],
        "model": profile["asset_route"]["model"],
        "media_profile": profile["media_profile"]["name"],
    }


def validate_capability_matrix(
    matrix: Mapping[str, Any],
    profiles: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Bind matrix rows to exact profiles; manifest support never upgrades status."""

    candidate = _validate_schema("production_unit_capability_matrix", matrix)
    validated = [validate_qualification_profile(profile) for profile in profiles]
    by_id = {
        (profile["profile_id"], profile["profile_version"]): profile
        for profile in validated
    }
    if len(by_id) != len(validated):
        _fail("DUPLICATE_QUALIFICATION_PROFILE", "profile IDs and versions must be unique")
    seen_entries: set[tuple[str, str]] = set()
    for entry in candidate["entries"]:
        key = (entry["profile_id"], entry["profile_version"])
        if key in seen_entries:
            _fail("DUPLICATE_CAPABILITY_ENTRY", f"duplicate matrix entry {key!r}")
        seen_entries.add(key)
        profile = by_id.get(key)
        if profile is None:
            _fail("UNKNOWN_QUALIFICATION_PROFILE", f"matrix entry {key!r} has no profile")
        if entry["profile_sha256"] != canonical_digest(profile):
            _fail("STALE_QUALIFICATION_PROFILE", f"matrix entry {key!r} binds a stale profile")
        if entry["qualification_status"] != profile["qualification_status"]:
            _fail("QUALIFICATION_STATUS_DRIFT", f"matrix entry {key!r} changed status")
        if entry["selector"] != _profile_selector(profile):
            _fail("QUALIFICATION_SELECTOR_DRIFT", f"matrix entry {key!r} changed selectors")
        if not entry["manifest_supported"] and entry["qualification_status"] in {
            "beta_qualified",
            "production_qualified",
        }:
            _fail(
                "UNSUPPORTED_QUALIFICATION_CLAIM",
                f"matrix entry {key!r} cannot be qualified when manifest support is false",
            )
    return candidate
