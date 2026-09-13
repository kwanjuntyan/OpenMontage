"""Every shipped pipeline manifest must actually load.

`lib.checkpoint` must fail closed when a named manifest cannot be parsed.
Falling back to the canonical stage list or to a caller-supplied gate flag
would run against the wrong DAG and could silently disable approval gates.

Existing manifest coverage names individual pipelines (talking-head,
framework-smoke, animated-explainer, documentary-montage), so a manifest that
no test happens to name is never loaded. These tests iterate the directory.
"""

from pathlib import Path

import pytest
import yaml

from lib.checkpoint import _stage_requires_approval, get_next_stage, get_pipeline_stages
from lib.pipeline_loader import load_pipeline

REPO_ROOT = Path(__file__).resolve().parents[2]
PIPELINE_DEFS = REPO_ROOT / "pipeline_defs"

PIPELINE_NAMES = sorted(p.stem for p in PIPELINE_DEFS.glob("*.yaml"))


def _declared_stages(name: str) -> list[str]:
    raw = yaml.safe_load((PIPELINE_DEFS / f"{name}.yaml").read_text(encoding="utf-8"))
    return [stage["name"] for stage in raw["stages"]]


def test_catalog_is_not_empty() -> None:
    assert PIPELINE_NAMES, "no pipeline manifests found"


@pytest.mark.parametrize("name", ["../cinematic", "subdir/cinematic", "C:\\cinematic"])
def test_pipeline_name_cannot_escape_manifest_root(name: str) -> None:
    with pytest.raises(ValueError, match="Invalid pipeline name"):
        load_pipeline(name)


@pytest.mark.parametrize("name", PIPELINE_NAMES)
def test_shipped_manifest_validates(name: str) -> None:
    """Regression: screen-demo.yaml carried a `production_modes` block the
    manifest schema did not allow, so the whole manifest failed to load."""
    manifest = load_pipeline(name)
    assert manifest["stages"]


@pytest.mark.parametrize("name", PIPELINE_NAMES)
def test_effective_stage_order_is_the_declared_one(name: str) -> None:
    """A manifest that silently falls back gets the canonical stage list.

    For screen-demo that inserted `research` and `proposal` ahead of its real
    first stage, so the prerequisite check rejected the opening checkpoint of
    every run with PREREQUISITE VIOLATION.
    """
    assert get_pipeline_stages(name) == _declared_stages(name)


@pytest.mark.parametrize("name", PIPELINE_NAMES)
def test_declared_approval_gates_are_enforceable(name: str) -> None:
    """AGENT_GUIDE.md: the manifest's human_approval_default is binding.

    `_stage_requires_approval` returning None means the caller's own flag wins,
    which is exactly the fail-open the gate is supposed to prevent.
    """
    raw = yaml.safe_load((PIPELINE_DEFS / f"{name}.yaml").read_text(encoding="utf-8"))

    for stage in raw["stages"]:
        if "human_approval_default" not in stage:
            continue
        resolved = _stage_requires_approval(name, stage["name"])
        assert resolved == stage["human_approval_default"], (
            f"{name}.{stage['name']}: manifest declares "
            f"{stage['human_approval_default']} but the checkpoint writer "
            f"resolves {resolved}"
        )


def test_animated_explainer_required_research_artifact_is_durable() -> None:
    """A required artifact cannot live only in transient Agent state."""
    manifest = load_pipeline("animated-explainer")
    stages = {stage["name"]: stage for stage in manifest["stages"]}

    assert "research_brief" in stages["proposal"]["required_artifacts_in"]
    assert "research_brief" in stages["research"]["produces"]
    assert stages["research"].get("checkpoint_required", True) is True


@pytest.mark.parametrize("name", PIPELINE_NAMES)
def test_required_inputs_are_produced_by_durable_earlier_stages(name: str) -> None:
    """No required DAG input may disappear with a non-persisted producer."""
    manifest = load_pipeline(name)
    producers: dict[str, dict] = {}
    for stage in manifest["stages"]:
        for required in stage.get("required_artifacts_in") or []:
            assert required in producers, (
                f"{name}.{stage['name']} requires {required!r} without an earlier producer"
            )
            assert producers[required].get("checkpoint_required", True) is True, (
                f"{name}.{stage['name']} requires {required!r}, but producer "
                f"{producers[required]['name']} is non-durable"
            )
        for produced in stage.get("produces") or []:
            producers[produced] = stage


def test_get_next_stage_skips_missing_optional_but_resumes_started_optional(
    tmp_path, monkeypatch
) -> None:
    """checkpoint_required:false means optional only until that stage starts."""
    from lib import checkpoint as checkpoint_module

    manifest = {
        "stages": [
            {"name": "research", "checkpoint_required": False},
            {"name": "proposal", "checkpoint_required": True},
        ]
    }
    monkeypatch.setattr(
        "lib.pipeline_loader.load_pipeline_readonly", lambda _name: manifest
    )
    monkeypatch.setattr(
        checkpoint_module,
        "get_pipeline_stages",
        lambda _name: ["research", "proposal"],
    )
    monkeypatch.setattr(checkpoint_module, "read_checkpoint", lambda *_args: None)
    assert get_next_stage(tmp_path, "optional-probe", "probe") == "proposal"

    def _started(_root, _project, stage):
        return (
            {"status": "in_progress", "pipeline_type": "probe"}
            if stage == "research"
            else None
        )

    monkeypatch.setattr(checkpoint_module, "read_checkpoint", _started)
    assert get_next_stage(tmp_path, "optional-probe", "probe") == "research"
