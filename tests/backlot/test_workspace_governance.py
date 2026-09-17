"""B0.0B anti-drift gates for the future Director Workspace.

These tests intentionally inspect source instead of importing Workspace
modules.  The scaffold has no runtime behavior yet; the checks make the
dependency and authority boundary executable before B0.1/B0.2 add code.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = REPO_ROOT / "backlot" / "workspace"
WORKSPACE_UI_ROOT = WORKSPACE_ROOT / "ui"
LEGACY_UI_WORKSPACE_ROOT = REPO_ROOT / "backlot" / "ui" / "workspace"
FIXTURE_MATRIX = (
    REPO_ROOT
    / "tests"
    / "backlot"
    / "fixtures"
    / "workspace"
    / "fixture-matrix.v1.json"
)

REQUIRED_SCENARIOS = {
    "ordinary-project",
    "course-with-style-and-clp",
    "course-with-assets",
    "pup-disabled",
    "pup-enabled",
    "pending-candidate",
    "missing-or-invalid-artifact",
    "large-course",
}

REQUIRED_VARIANTS = {
    "zero-entity-clp",
    "validated-batch-v2-publication",
    "legacy-asset-manifest",
    "local-browser-playable-media",
    "approved-remote-media",
    "preview-proxy-required-media",
    "missing-media-bytes",
    "failed-progress",
    "stale-progress",
    "completed-delivery",
}

CHECKPOINT_READ_SYMBOLS = {
    "CheckpointValidationError",
    "read_checkpoint",
    "read_project_marker",
    "validate_checkpoint",
}
PIPELINE_READ_SYMBOLS = {"load_pipeline_readonly"}
PUBLIC_BATCH_READ_SYMBOLS = {"inspect_v2_asset_manifest_claim"}
PRIVATE_SOURCE_TOKENS = (".production-units", ".batch-v2")
KNOWN_WORKSPACE_LAYERS = {"root", "readers", "projection", "api_v1"}
BROWSER_SOURCE_SUFFIXES = {".html", ".js", ".jsx", ".mjs", ".ts", ".tsx"}

FORBIDDEN_GLOBAL_IMPORTS = (
    "tools",
    "scripts",
    "lib.providers",
    "lib.production_units",
    "lib.gcs_storage",
    "backlot.server",
    "backlot.ui",
)

FORBIDDEN_LAYER_IMPORTS = {
    "readers": (
        "backlot.workspace.projection",
        "backlot.workspace.api_v1",
    ),
    "projection": (
        "backlot.workspace.api_v1",
        "backlot.state",
        "backlot.course_projection",
        "lib.checkpoint",
        "lib.clp_validator",
        "lib.pipeline_loader",
        "lib.batch_executor",
        "lib.production_units",
    ),
    "api_v1": (
        "backlot.workspace.readers",
        "backlot.state",
        "backlot.course_projection",
        "lib.checkpoint",
        "lib.clp_validator",
        "lib.pipeline_loader",
        "lib.batch_executor",
        "lib.production_units",
    ),
}


def _matches(module: str, prefix: str) -> bool:
    module_key = module.casefold()
    prefix_key = prefix.casefold()
    return module_key == prefix_key or module_key.startswith(f"{prefix_key}.")


def _load_json_without_duplicate_keys(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )


def _assert_safe_repo_relative(value: str) -> Path:
    normalized = value.replace("\\", "/")
    posix_path = PurePosixPath(normalized)
    windows_path = PureWindowsPath(value)
    assert value == normalized
    assert not posix_path.is_absolute()
    assert not windows_path.is_absolute()
    assert not windows_path.drive
    assert not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", normalized)
    assert ".." not in posix_path.parts
    normalized_key = normalized.casefold()
    assert not any(
        token.casefold() in normalized_key for token in PRIVATE_SOURCE_TOKENS
    )
    resolved = (REPO_ROOT / Path(normalized)).resolve()
    resolved.relative_to(REPO_ROOT.resolve())
    return resolved


def _assert_pytest_node_exists(nodeid: str) -> None:
    parts = nodeid.split("::")
    assert len(parts) in {2, 3}, nodeid
    path = _assert_safe_repo_relative(parts[0])
    assert path.is_file(), nodeid
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    if len(parts) == 2:
        assert any(
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == parts[1]
            for node in tree.body
        ), nodeid
        return

    owner = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == parts[1]
        ),
        None,
    )
    assert owner is not None, nodeid
    assert any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == parts[2]
        for node in owner.body
    ), nodeid


def _layer_for(path: Path) -> str:
    relative = path.relative_to(WORKSPACE_ROOT)
    if len(relative.parts) == 1:
        return "root" if relative.name == "__init__.py" else "unknown"
    return relative.parts[0]


def _package_for(path: Path) -> str:
    relative = path.relative_to(REPO_ROOT).with_suffix("")
    parts = list(relative.parts)
    parts.pop()
    return ".".join(parts)


def _import_targets(path: Path, node: ast.Import | ast.ImportFrom) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]

    module = node.module or ""
    if node.level:
        module = importlib.util.resolve_name(
            f"{'.' * node.level}{module}", _package_for(path)
        )
    targets = [module] if module else []
    targets.extend(
        f"{module}.{alias.name}" if module else alias.name for alias in node.names
    )
    return targets


def _source_violations(source: str, *, path: Path, layer: str) -> list[str]:
    tree = ast.parse(source, filename=str(path))
    violations: list[str] = []

    if layer not in KNOWN_WORKSPACE_LAYERS:
        violations.append(f"unknown Workspace layer: {layer}")

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            targets = _import_targets(path, node)

            if layer == "root":
                violations.append("Workspace package root must remain import-free")

            for target in targets:
                if any(_matches(target, prefix) for prefix in FORBIDDEN_GLOBAL_IMPORTS):
                    violations.append(f"forbidden authority import: {target}")
                if any(
                    _matches(target, prefix)
                    for prefix in FORBIDDEN_LAYER_IMPORTS.get(layer, ())
                ):
                    violations.append(f"forbidden {layer} dependency: {target}")

            if any(_matches(target, "lib.checkpoint") for target in targets):
                valid = (
                    isinstance(node, ast.ImportFrom)
                    and node.level == 0
                    and node.module == "lib.checkpoint"
                    and all(
                        alias.name in CHECKPOINT_READ_SYMBOLS for alias in node.names
                    )
                )
                if not valid:
                    violations.append("checkpoint access is not an approved named read")

            if any(_matches(target, "lib.batch_executor") for target in targets):
                valid = (
                    isinstance(node, ast.ImportFrom)
                    and node.level == 0
                    and node.module == "lib.batch_executor.publication"
                    and all(
                        alias.name in PUBLIC_BATCH_READ_SYMBOLS for alias in node.names
                    )
                )
                if not valid:
                    violations.append("batch executor access is not an approved named read")

            if any(_matches(target, "lib.pipeline_loader") for target in targets):
                valid = (
                    isinstance(node, ast.ImportFrom)
                    and node.level == 0
                    and node.module == "lib.pipeline_loader"
                    and all(alias.name in PIPELINE_READ_SYMBOLS for alias in node.names)
                )
                if not valid:
                    violations.append("pipeline access is not an approved named read")

            if any(_matches(target, "importlib") for target in targets):
                violations.append("dynamic module loading is not allowed")

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "__import__":
                violations.append("dynamic module loading is not allowed")
            if (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "importlib"
            ):
                violations.append("dynamic module loading is not allowed")

        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value_key = node.value.casefold()
            for token in PRIVATE_SOURCE_TOKENS:
                if token.casefold() in value_key:
                    violations.append(f"private source token: {token}")

    return sorted(set(violations))


def _browser_source_violations(source: str, *, path: Path) -> list[str]:
    violations: list[str] = []
    source_key = source.casefold()
    for token in (*PRIVATE_SOURCE_TOKENS, "board.js", "library.js"):
        if token.casefold() in source_key:
            violations.append(f"forbidden browser dependency: {token}")

    for legacy_route in ("/api/project/", "/media/", "/thumb/"):
        if legacy_route.casefold() in source_key:
            violations.append(f"forbidden legacy route: {legacy_route}")

    for route in re.findall(r"/api/[A-Za-z0-9_./{}?=&-]+", source):
        if not (
            route == "/api/workspace/v1"
            or route.startswith("/api/workspace/v1/")
            or route.startswith("/api/workspace/v1?")
        ):
            violations.append(f"route is outside Workspace v1: {route}")

    return [f"{path}: {violation}" for violation in sorted(set(violations))]


def test_workspace_scaffold_has_the_frozen_dependency_layers() -> None:
    expected = {
        WORKSPACE_ROOT / "__init__.py",
        WORKSPACE_ROOT / "README.md",
        WORKSPACE_ROOT / "readers" / "__init__.py",
        WORKSPACE_ROOT / "projection" / "__init__.py",
        WORKSPACE_ROOT / "api_v1" / "__init__.py",
        WORKSPACE_UI_ROOT / "README.md",
    }
    assert all(path.is_file() for path in expected)

    root_files = {path.name for path in WORKSPACE_ROOT.iterdir() if path.is_file()}
    root_dirs = {
        path.name
        for path in WORKSPACE_ROOT.iterdir()
        if path.is_dir() and path.name != "__pycache__"
    }
    assert root_files == {"__init__.py", "README.md"}
    assert root_dirs == {"readers", "projection", "api_v1", "ui"}


def test_workspace_runtime_registration_is_server_flag_gated() -> None:
    """B0.2B may register only a default-off, server-side projection route."""
    for relative in (
        "backlot/state.py",
        "backlot/course_projection.py",
    ):
        path = REPO_ROOT / relative
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        imports = [
            target
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for target in _import_targets(path, node)
        ]
        assert not any(_matches(target, "backlot.workspace") for target in imports)

    server_source = (REPO_ROOT / "backlot" / "server.py").read_text(
        encoding="utf-8"
    )
    assert "BACKLOT_WORKSPACE_ENABLED" in server_source
    assert "create_workspace_router" in server_source
    assert not any(
        path.is_file() for path in LEGACY_UI_WORKSPACE_ROOT.rglob("*")
    )
    ui_entries = {
        path.relative_to(WORKSPACE_UI_ROOT).as_posix()
        for path in WORKSPACE_UI_ROOT.rglob("*")
        if path.is_file()
    }
    assert ui_entries == {"README.md"}


def test_b00_workspace_http_surface_is_absent() -> None:
    from fastapi.testclient import TestClient

    from backlot.server import create_app

    client = TestClient(create_app())
    try:
        assert client.get("/api/workspace/v1/catalog").status_code == 404
        assert client.get("/ui/workspace/README.md").status_code == 404
    finally:
        client.close()


def test_workspace_python_obeys_dependency_and_authority_boundaries() -> None:
    violations: list[str] = []
    python_files = sorted(WORKSPACE_ROOT.rglob("*.py"))
    assert python_files

    for path in python_files:
        source = path.read_text(encoding="utf-8")
        for violation in _source_violations(
            source, path=path, layer=_layer_for(path)
        ):
            violations.append(f"{path.relative_to(REPO_ROOT)}: {violation}")

    assert violations == []


@pytest.mark.parametrize(
    "relative",
    ["models.py", "models/__init__.py", "models/resource.py"],
)
def test_unknown_workspace_layers_fail_closed(relative: str) -> None:
    path = WORKSPACE_ROOT / relative
    layer = _layer_for(path)
    violations = _source_violations("VALUE = 1", path=path, layer=layer)
    assert any("unknown Workspace layer" in violation for violation in violations)


@pytest.mark.parametrize(
    ("layer", "source", "expected"),
    [
        ("readers", "from lib.checkpoint import write_checkpoint", "checkpoint"),
        ("readers", "import tools.google_imagen", "authority import"),
        ("readers", "import Tools.google_imagen", "authority import"),
        (
            "projection",
            "from backlot.workspace import api_v1",
            "projection dependency",
        ),
        ("projection", "from .. import api_v1", "projection dependency"),
        (
            "api_v1",
            "from backlot.workspace import readers",
            "api_v1 dependency",
        ),
        (
            "projection",
            "from lib.checkpoint import read_checkpoint",
            "projection dependency",
        ),
        ("readers", "import lib.production_units", "authority import"),
        ("readers", "import importlib", "dynamic module"),
        ("readers", "PRIVATE = '.production-units/state.json'", "private source"),
        ("readers", "PRIVATE = '.PRODUCTION-UNITS/state.json'", "private source"),
    ],
)
def test_boundary_guard_rejects_representative_drift(
    layer: str, source: str, expected: str
) -> None:
    path = WORKSPACE_ROOT / layer / "example.py"
    violations = _source_violations(source, path=path, layer=layer)
    assert any(expected in violation for violation in violations), violations


@pytest.mark.parametrize(
    "source",
    [
        "from lib.checkpoint import read_checkpoint, validate_checkpoint",
        "from lib.checkpoint import read_project_marker",
        "from lib.pipeline_loader import load_pipeline_readonly",
        (
            "from lib.batch_executor.publication import "
            "inspect_v2_asset_manifest_claim"
        ),
        "from backlot.workspace.readers import canonical_course",
    ],
)
def test_reader_guard_keeps_explicit_read_paths_available(source: str) -> None:
    path = WORKSPACE_ROOT / "readers" / "example.py"
    assert _source_violations(source, path=path, layer="readers") == []


def test_reader_allowlist_matches_the_machine_readable_source_matrix() -> None:
    matrix = _load_json_without_duplicate_keys(
        REPO_ROOT / "docs" / "backlot-workspace-field-source-matrix.v1.json"
    )
    expected = {
        *(f"lib.checkpoint.{symbol}" for symbol in CHECKPOINT_READ_SYMBOLS),
        *(f"lib.pipeline_loader.{symbol}" for symbol in PIPELINE_READ_SYMBOLS),
        *(
            f"lib.batch_executor.publication.{symbol}"
            for symbol in PUBLIC_BATCH_READ_SYMBOLS
        ),
    }
    assert set(matrix["reader_boundary"]["currently_approved_workspace_symbols"]) == expected


def test_workspace_browser_code_uses_only_versioned_workspace_routes() -> None:
    violations: list[str] = []
    for path in sorted(WORKSPACE_UI_ROOT.rglob("*")):
        if path.suffix not in BROWSER_SOURCE_SUFFIXES:
            continue
        source = path.read_text(encoding="utf-8")
        violations.extend(
            _browser_source_violations(
                source, path=path.relative_to(REPO_ROOT)
            )
        )

    assert violations == []


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("fetch('/api/project/demo/state')", "legacy route"),
        ("fetch('/api/workspace/v10/catalog')", "outside Workspace v1"),
        ("fetch('/api/workspace/v1evil')", "outside Workspace v1"),
        ("import '/ui/board.js'", "browser dependency"),
        ("const source = '.batch-v2/state.json'", "browser dependency"),
        ("const source = '.BATCH-V2/state.json'", "browser dependency"),
        ("fetch('/media/demo/file.mp4')", "legacy route"),
    ],
)
def test_browser_guard_rejects_representative_drift(
    source: str, expected: str
) -> None:
    violations = _browser_source_violations(
        source, path=Path("backlot/workspace/ui/example.ts")
    )
    assert any(expected in violation for violation in violations), violations


@pytest.mark.parametrize(
    "route",
    [
        "/api/workspace/v1",
        "/api/workspace/v1/catalog",
        "/api/workspace/v1/catalog?limit=20",
        "/api/workspace/v1?health=1",
    ],
)
def test_browser_guard_accepts_exact_workspace_v1_boundary(route: str) -> None:
    source = f"fetch('{route}')"
    assert _browser_source_violations(
        source, path=Path("backlot/workspace/ui/example.ts")
    ) == []


@pytest.mark.parametrize(
    "value",
    [
        "../outside.json",
        "/absolute/path.json",
        "C:/outside.json",
        "C:\\outside.json",
        "C:outside.json",
        "\\\\server\\share\\outside.json",
        "file:/outside.json",
        ".production-units/state.json",
        ".PRODUCTION-UNITS/state.json",
        ".batch-v2/state.json",
        ".BATCH-V2/state.json",
    ],
)
def test_fixture_paths_reject_cross_platform_and_private_locations(
    value: str,
) -> None:
    with pytest.raises((AssertionError, ValueError)):
        _assert_safe_repo_relative(value)


def test_fixture_matrix_is_complete_and_honest_about_materialization() -> None:
    matrix = _load_json_without_duplicate_keys(FIXTURE_MATRIX)
    assert matrix["version"] == "backlot.workspace.fixture-matrix.v1"
    assert matrix["status"] == "b0_1_consumer_fixtures_materialized"
    assert set(matrix["required_variants"]) == REQUIRED_VARIANTS

    scenarios = matrix["scenarios"]
    ids = [scenario["id"] for scenario in scenarios]
    assert len(ids) == len(set(ids))
    assert set(ids) == REQUIRED_SCENARIOS

    for scenario in scenarios:
        evidence = scenario["baseline_evidence"]
        assert evidence["level"] in {
            "exact_source_baseline",
            "partial_source_baseline",
            "none",
        }
        if evidence["level"] == "none":
            assert evidence["pytest_nodeids"] == []
            assert evidence["gap"]
        else:
            assert evidence["pytest_nodeids"]
            for nodeid in evidence["pytest_nodeids"]:
                _assert_pytest_node_exists(nodeid)
            if evidence["level"] == "partial_source_baseline":
                assert evidence["gap"]

        consumer = scenario["consumer_fixture"]
        assert consumer["owner_phase"] in {"B0.1", "B0.2"}
        expected_status = (
            "materialized" if consumer["owner_phase"] == "B0.1" else "pending"
        )
        assert consumer["status"] == expected_status
        fixture_path = _assert_safe_repo_relative(consumer["path"])
        if consumer["status"] == "materialized":
            assert fixture_path.is_dir()
            manifest_path = _assert_safe_repo_relative(consumer["manifest"])
            assert manifest_path.is_file()
            assert manifest_path.parent == fixture_path
            manifest = _load_json_without_duplicate_keys(manifest_path)
            assert manifest["version"] == "backlot.workspace.fixture-set.v1"
            assert manifest["scenario_id"] == scenario["id"]
            case_ids = [case["id"] for case in manifest["cases"]]
            assert case_ids
            assert len(case_ids) == len(set(case_ids))
            fixture_covers: set[str] = set()
            for case in manifest["cases"]:
                assert case["expect"] == "valid"
                assert case["domain_expectation"] in {"positive", "negative", "edge"}
                projection_path = _assert_safe_repo_relative(
                    f"{consumer['path']}/{case['projection']}"
                )
                assert projection_path.is_file()
                assert projection_path.parent == fixture_path
                fixture_covers.update(case["covers"])
            assert set(scenario["variants"]).issubset(fixture_covers)
            assert set(scenario["must_prove"]).issubset(fixture_covers)
        else:
            assert "manifest" not in consumer
            assert not fixture_path.exists()
        assert scenario["runtime_acceptance"]
        assert scenario["must_prove"]

    covered_variants = {
        variant for scenario in scenarios for variant in scenario["variants"]
    }
    assert covered_variants == REQUIRED_VARIANTS


def test_agent_entry_points_name_the_governance_sources_and_test() -> None:
    guide = (REPO_ROOT / "AGENT_GUIDE.md").read_text(encoding="utf-8")
    contract = (
        REPO_ROOT / "docs" / "backlot-workspace-architecture-contract.md"
    ).read_text(encoding="utf-8")

    for required in (
        "docs/backlot-workspace-architecture-contract.md",
        "docs/backlot-director-workspace-plan.md",
        "docs/backlot-workspace-field-source-matrix.v1.md",
        "docs/backlot-workspace-field-source-matrix.v1.json",
        "backlot/workspace/README.md",
        "schemas/workspace/workspace_projection_v1.schema.json",
        "backlot/workspace/projection/contracts.py",
        "backlot/workspace/projection/types.py",
        "tests/backlot/fixtures/workspace/fixture-matrix.v1.json",
        "tests/backlot/test_workspace_governance.py",
        "tests/backlot/test_workspace_contracts.py",
    ):
        assert required in guide

    assert "tests/backlot/fixtures/workspace/fixture-matrix.v1.json" in contract
    assert "tests/backlot/test_workspace_governance.py" in contract
