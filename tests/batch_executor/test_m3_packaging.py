from __future__ import annotations

import ast
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
    assert all(line.count("==") == 1 and not line.endswith("==") for line in requirement_lines)
    assert all("google-cloud-run" not in line.lower() for line in requirement_lines)
    constraints = [
        line.strip()
        for line in (REPOSITORY_ROOT / "constraints-batch-v2-py310.txt")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert all(line.count("==") == 1 and not line.endswith("==") for line in constraints)
    constrained_names = {line.split("==", 1)[0].lower() for line in constraints}
    assert {line.split("==", 1)[0].lower() for line in requirement_lines} <= constrained_names
    assert len(constrained_names) == len(constraints)


def test_dedicated_container_requires_immutable_base_and_runs_non_root():
    dockerfile = (REPOSITORY_ROOT / "Dockerfile.batch-v2").read_text(
        encoding="utf-8"
    )
    assert "ARG PYTHON_BASE_IMAGE\nFROM ${PYTHON_BASE_IMAGE}" in dockerfile
    assert "ARG FFMPEG_APT_VERSION" in dockerfile
    assert '"ffmpeg=${FFMPEG_APT_VERSION}"' in dockerfile
    assert "USER 65532:65532" in dockerfile
    assert "chmod --recursive a-w /opt/openmontage" in dockerfile
    assert "mkdir --parents /workspace/projects" in dockerfile
    assert "--constraint constraints-batch-v2-py310.txt" in dockerfile
    assert 'PYTHONPATH=/opt/openmontage' in dockerfile
    assert (
        'ENTRYPOINT ["python", "/opt/openmontage/scripts/batch_execute.py"]'
        in dockerfile
    )
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
    assert container["volumeMounts"] == [
        {"name": "materialized-project-workspace", "mountPath": "/workspace"}
    ]
    assert task["serviceAccountName"] == "${BATCH_V2_SERVICE_ACCOUNT}"


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
