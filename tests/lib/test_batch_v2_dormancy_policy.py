"""Zero-side-effect policy checks for the dormant Batch V2 component."""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GUIDE = REPO_ROOT / "AGENT_GUIDE.md"
STATUS = REPO_ROOT / "docs" / "batch-v2-status.md"
IMPLEMENTATION_PLAN = REPO_ROOT / "docs" / "batch-v2-implementation-plan.md"
MIGRATION = REPO_ROOT / "docs" / "batch-v2-migration-rollback.md"
PIPELINE_DEFS = REPO_ROOT / "pipeline_defs"

_ROUTING_TOKENS = (
    "dormant_opt_in",
    "not production-qualified",
    "not supported by kj-course-cinematic",
    "explicitly requests Batch V2",
    "explicitly declares a Batch V2 opt-in execution profile",
)
_BATCH_ROUTE_REFERENCES = (
    "batch_v2",
    "batch-v2",
    "lib.batch_executor",
    "scripts/batch_execute.py",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_agent_guide_declares_binding_batch_v2_dormancy_policy():
    guide = _read(GUIDE)
    for token in _ROUTING_TOKENS:
        assert token in guide
    assert "`kj-course-cinematic` must evolve from its own current contracts" in guide


def test_status_document_freezes_nonproduction_non_kj_boundary():
    status = _read(STATUS)
    assert "status: dormant_opt_in" in status
    assert "default_enabled: false" in status
    assert "production_qualified: false" in status
    assert "kj_course_cinematic_supported: false" in status
    assert "This document grants no" in status


def test_batch_documents_point_to_current_status_authority():
    assert "docs/batch-v2-status.md" in _read(IMPLEMENTATION_PLAN)
    migration = _read(MIGRATION)
    assert "docs/batch-v2-status.md" in migration
    assert "`dormant_opt_in`" in migration


def test_no_current_pipeline_manifest_routes_to_batch_v2():
    offenders: list[str] = []
    for manifest in sorted(PIPELINE_DEFS.rglob("*.yaml")):
        content = _read(manifest).lower()
        if any(token in content for token in _BATCH_ROUTE_REFERENCES):
            offenders.append(manifest.relative_to(REPO_ROOT).as_posix())
    assert offenders == []


def test_kj_course_cinematic_manifest_does_not_route_to_batch_v2():
    manifest = PIPELINE_DEFS / "kj-course-cinematic.yaml"
    if not manifest.exists():
        return
    content = _read(manifest).lower()
    for token in _BATCH_ROUTE_REFERENCES:
        assert token not in content
