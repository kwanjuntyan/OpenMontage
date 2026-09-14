from __future__ import annotations

import ast
import fnmatch
import re
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_batch_v2_runtime_dependencies_are_narrow_and_exactly_pinned():
    requirement_lines = [
        line.strip()
        for line in (REPOSITORY_ROOT / "requirements-batch-v2.txt")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert {line.split("==", 1)[0].lower() for line in requirement_lines} == {
        "google-auth",
        "google-cloud-storage",
        "google-crc32c",
        "jsonschema",
        "pyyaml",
        "requests",
    }
    assert all(
        line.count("==") == 1 and not line.endswith("==") for line in requirement_lines
    )
    assert all("google-cloud-run" not in line.lower() for line in requirement_lines)
    constraints = [
        line.strip()
        for line in (REPOSITORY_ROOT / "constraints-batch-v2-py310.txt")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert all(
        line.count("==") == 1 and not line.endswith("==") for line in constraints
    )
    constrained_names = {line.split("==", 1)[0].lower() for line in constraints}
    assert {
        line.split("==", 1)[0].lower() for line in requirement_lines
    } <= constrained_names
    assert len(constrained_names) == len(constraints)


def test_dedicated_container_requires_immutable_base_and_runs_non_root():
    dockerfile = (REPOSITORY_ROOT / "Dockerfile.batch-v2").read_text(encoding="utf-8")
    assert "ARG PYTHON_BASE_IMAGE\nFROM ${PYTHON_BASE_IMAGE}" in dockerfile
    digest_guard = re.search(r"re\.fullmatch\(r'([^']+)', sys\.argv\[1\]\)", dockerfile)
    assert digest_guard is not None
    digest_pattern = re.compile(digest_guard.group(1))
    assert digest_pattern.fullmatch("python:3.10.18-slim-bookworm@sha256:" + "a" * 64)
    for mutable_or_malformed in (
        "python:3.10.18-slim-bookworm",
        "python:latest",
        "python@sha256:" + "a" * 63,
        "python@sha256:" + "g" * 64,
        "python@sha512:" + "a" * 64,
        "python@sha256:" + "a" * 64 + "-suffix",
    ):
        assert digest_pattern.fullmatch(mutable_or_malformed) is None
    assert dockerfile.index("re.fullmatch") < dockerfile.index("apt-get update")
    assert "ARG FFMPEG_APT_VERSION" in dockerfile
    assert '"ffmpeg=${FFMPEG_APT_VERSION}"' in dockerfile
    assert "USER 65532:65532" in dockerfile
    assert "chmod --recursive a-w /opt/openmontage" in dockerfile
    assert "mkdir --parents /workspace/projects" in dockerfile
    assert "--constraint constraints-batch-v2-py310.txt" in dockerfile
    assert "PYTHONPATH=/opt/openmontage" in dockerfile
    assert (
        'ENTRYPOINT ["python", "/opt/openmontage/scripts/batch_execute.py"]'
        in dockerfile
    )
    assert "COPY scripts/batch_publish.py ./scripts/batch_publish.py" in dockerfile
    assert "COPY . " not in dockerfile
    assert "COPY .\n" not in dockerfile
    for forbidden in (
        ".env",
        "credentials.json",
        "service-account.json",
        "projects ./projects",
        "assets ./assets",
        "COPY cache",
    ):
        assert forbidden not in dockerfile


def test_cloud_run_job_template_is_exactly_one_zero_retry_task():
    template_path = (
        REPOSITORY_ROOT / "deploy" / "batch-v2" / "cloud-run-job.template.yaml"
    )
    document = yaml.safe_load(template_path.read_text(encoding="utf-8"))
    execution = document["spec"]["template"]["spec"]
    task = execution["template"]["spec"]
    assert execution["taskCount"] == 1
    assert execution["parallelism"] == 1
    assert task["maxRetries"] == 0
    assert len(task["containers"]) == 1
    container = task["containers"][0]
    assert container["image"] == "${BATCH_V2_IMAGE_DIGEST}"
    assert container["args"][:3] == ["run", "--profile", "cloud-run"]
    assert container["args"][4] == "/input-snapshot/config/runtime-config.json"
    assert container["volumeMounts"] == [
        {
            "name": "immutable-input-snapshot",
            "mountPath": "/input-snapshot",
            "readOnly": True,
        }
    ]
    assert all(
        mount["mountPath"] != "/workspace" for mount in container["volumeMounts"]
    )
    dockerfile = (REPOSITORY_ROOT / "Dockerfile.batch-v2").read_text(encoding="utf-8")
    user_match = re.search(r"(?m)^USER (\d+):(\d+)$", dockerfile)
    assert user_match is not None
    assert len(task["volumes"]) == 1
    snapshot_volume = task["volumes"][0]
    assert snapshot_volume["name"] == "immutable-input-snapshot"
    assert snapshot_volume["csi"]["readOnly"] is True
    assert snapshot_volume["csi"]["volumeAttributes"]["mountOptions"] == (
        "only-dir=batch-v2-input-snapshots/sha256/${INPUT_SNAPSHOT_SHA256},"
        f"uid={user_match.group(1)},gid={user_match.group(2)}"
    )
    assert not snapshot_volume["csi"]["volumeAttributes"]["mountOptions"].startswith(
        "only-dir=projects"
    )
    assert task["serviceAccountName"] == "${BATCH_V2_SERVICE_ACCOUNT}"
    assert "--offline-qualification" not in container["args"]


def test_cloud_publication_job_uses_separate_root_and_disjoint_read_only_snapshot():
    template_path = (
        REPOSITORY_ROOT
        / "deploy"
        / "batch-v2"
        / "cloud-run-publication-job.template.yaml"
    )
    document = yaml.safe_load(template_path.read_text(encoding="utf-8"))
    execution = document["spec"]["template"]["spec"]
    task = execution["template"]["spec"]
    assert execution["taskCount"] == execution["parallelism"] == 1
    assert task["maxRetries"] == 0
    container = task["containers"][0]
    assert container["command"] == [
        "python",
        "/opt/openmontage/scripts/batch_publish.py",
    ]
    assert container["args"][:2] == ["publish", "--config"]
    assert "/input-snapshot/config/publication-runtime-config.json" in container["args"]
    assert container["volumeMounts"] == [
        {
            "name": "immutable-input-snapshot",
            "mountPath": "/input-snapshot",
            "readOnly": True,
        }
    ]
    assert all(
        mount["mountPath"] != "/workspace" for mount in container["volumeMounts"]
    )
    snapshot = task["volumes"][0]["csi"]
    assert snapshot["readOnly"] is True
    dockerfile = (REPOSITORY_ROOT / "Dockerfile.batch-v2").read_text(
        encoding="utf-8"
    )
    user_match = re.search(r"(?m)^USER (\d+):(\d+)$", dockerfile)
    assert user_match is not None
    assert snapshot["volumeAttributes"]["mountOptions"] == (
        "only-dir=batch-v2-input-snapshots/sha256/${INPUT_SNAPSHOT_SHA256},"
        f"uid={user_match.group(1)},gid={user_match.group(2)}"
    )
    assert "--offline-qualification" not in container["args"]


def _docker_context_includes(rules: list[str], path: str) -> bool:
    included = True
    for raw_rule in rules:
        negated = raw_rule.startswith("!")
        pattern = raw_rule[1:] if negated else raw_rule
        if pattern.endswith("/"):
            matched = path.rstrip("/") == pattern.rstrip("/")
        else:
            matched = fnmatch.fnmatchcase(path, pattern)
        if matched:
            included = negated
    return included


def test_docker_build_context_is_default_deny_with_only_runtime_inputs_allowed():
    rules = [
        line.strip()
        for line in (REPOSITORY_ROOT / ".dockerignore")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert rules[0] == "**"

    required_inputs = (
        "Dockerfile.batch-v2",
        ".dockerignore",
        "requirements-batch-v2.txt",
        "constraints-batch-v2-py310.txt",
        "lib/batch_executor/cli.py",
        "schemas/execution/batch_request.schema.json",
        "pipeline_defs/documentary-montage.yaml",
        "scripts/batch_execute.py",
        "scripts/batch_publish.py",
    )
    for path in required_inputs:
        assert _docker_context_includes(rules, path), path

    forbidden_context = (
        ".git/config",
        ".env.production",
        "projects/private/assets/video.mp4",
        "lib/service-account.json",
        "lib/credentials-prod.json",
        "lib/__pycache__/runtime.cpython-310.pyc",
        "node_modules/example/index.js",
        ".pytest-tmp-packaging/result.xml",
        "tests/output.xml",
        "worktrees/another-checkout/file.py",
        ".vscode/settings.json",
        "Thumbs.db",
        "generated/preview.mp4",
        "unrelated-source.txt",
        "scripts/not-a-runtime-entrypoint.py",
    )
    for path in forbidden_context:
        assert not _docker_context_includes(rules, path), path


def test_cloud_entrypoint_exposes_no_pipeline_review_or_identity_selector():
    cli_path = REPOSITORY_ROOT / "lib" / "batch_executor" / "cli.py"
    tree = ast.parse(cli_path.read_text(encoding="utf-8"))
    parser_arguments = []
    imported_modules = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "add_argument" and node.args:
                value = node.args[0]
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    parser_arguments.append(value.value)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.append(node.module)
    assert set(parser_arguments) == {
        "command",
        "--profile",
        "--config",
        "--request-uri",
        "--resume-proof-uri",
        "--resume-proof-kind",
        "--offline-qualification",
    }
    assert all(
        selector not in parser_arguments
        for selector in (
            "--pipeline",
            "--stage",
            "--provider",
            "--route",
            "--model",
            "--approve",
            "--publish",
        )
    )
    assert "lib.checkpoint" not in imported_modules
    assert not any(module.endswith("publication") for module in imported_modules)


def test_publication_entrypoint_is_separate_and_composes_only_frozen_authority():
    script = (REPOSITORY_ROOT / "scripts" / "batch_publish.py").read_text(
        encoding="utf-8"
    )
    assert "lib.batch_executor.publication_cli" in script
    source = (
        REPOSITORY_ROOT / "lib" / "batch_executor" / "publication_cli.py"
    ).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert "lib.batch_executor.publication" not in imported
    assert ".publication" in imported or "publication" in imported
    assert "CloudAssetsPublisher" in source
    assert "CloudRunADCExecutionStatusVerifier" in source
    for forbidden in (
        "CloudBatchExecutor",
        "LocalBatchExecutor",
        "get_next_stage",
        "provider_selector",
        "freeze_publication_command",
        "freeze_publication_authorization",
    ):
        assert forbidden not in source


def test_m3_runtime_sources_contain_no_key_path_or_ambient_project_fallback():
    runtime_sources = "\n".join(
        (REPOSITORY_ROOT / "lib" / "batch_executor" / filename).read_text(
            encoding="utf-8"
        )
        for filename in (
            "cli.py",
            "gcs_storage.py",
            "gemini_adapter.py",
            "identity.py",
            "runtime.py",
            "publication_cli.py",
            "workspace.py",
        )
    )
    for forbidden in (
        "GOOGLE_APPLICATION_CREDENTIALS",
        "from_service_account_file",
        "service-account.json",
        "developer_api",
        "make_public",
        "generate_signed_url",
    ):
        assert forbidden not in runtime_sources


def test_runbook_keeps_external_actions_behind_m5_and_project_scoped_workspace():
    runbook = (REPOSITORY_ROOT / "docs" / "batch-v2-cloud-run.md").read_text(
        encoding="utf-8"
    )
    assert "not deployment authorization" in runbook
    assert "separate approvals listed under M5" in runbook
    assert "taskCount: 1" in runbook
    assert "parallelism: 1" in runbook
    assert "maxRetries: 0" in runbook
    assert "/workspace/projects/<project-id>/.batch-v2/runs/" in runbook
    assert "No tool output uses `/tmp`" in runbook
    assert "awaiting_agent_review" in runbook
    assert "cannot choose a\nstage/provider/model" in runbook
    assert "default-deny build context" in runbook
    assert "Only the Dockerfile inputs" in runbook
    assert "container gate remains pending, rather than waived" in runbook
    assert "not part of M3 acceptance" not in runbook
    assert "dst=/input-snapshot,readonly" in runbook
    assert "<prepared-local-workspace>" in runbook
    assert "<prepared-cloud-workspace>" in runbook
    assert "--offline-qualification" in runbook
    assert "does not compute a Merkle digest" in runbook
    assert "python -m scripts.batch_v2_prepare_offline_qualification" in runbook


def test_offline_qualification_fixture_prepares_forty_portable_items(tmp_path):
    from scripts.batch_v2_prepare_offline_qualification import (
        prepare_offline_qualification,
    )

    root = tmp_path / "offline-qualification"
    summary = prepare_offline_qualification(root)
    snapshot = root / "input-snapshot"
    request = yaml.safe_load(
        (snapshot / "config" / "request.json").read_text(encoding="utf-8")
    )
    assert len(request["work_items"]) == 40
    assert request["execution_policy"]["storage_profile"] == "portable"
    assert summary["request_digest"] == request["request_digest"]
    assert (snapshot / "projects" / request["project_id"] / "project.json").is_file()
    assert (root / "local-workspace" / "projects" / request["project_id"]).is_dir()
    assert (root / "cloud-workspace" / "projects").is_dir()
    for name, profile in (
        ("local-runtime-config.json", "local"),
        ("cloud-runtime-config.json", "cloud_run"),
    ):
        config = yaml.safe_load(
            (snapshot / "config" / name).read_text(encoding="utf-8")
        )
        assert config["profile"] == profile
        assert config["transport_mode"] == "offline_fake"
        assert config["request_digest"] == request["request_digest"]

    second_root = tmp_path / "offline-qualification-second"
    second = prepare_offline_qualification(second_root)
    assert second["request_digest"] == summary["request_digest"]
    for relative in (
        "config/request.json",
        f"projects/{request['project_id']}/project.json",
        f"projects/{request['project_id']}/checkpoint_idea.json",
        f"projects/{request['project_id']}/checkpoint_scene_plan.json",
    ):
        assert (second_root / "input-snapshot" / relative).read_bytes() == (
            snapshot / relative
        ).read_bytes()
