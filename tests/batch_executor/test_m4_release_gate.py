"""M4 offline release, migration, and isolation contracts."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

import pytest
import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
LEGACY_RUNNER = REPOSITORY_ROOT / "scripts" / "batch_run_intent_sequences.py"
LEGACY_RUNNER_SHA256 = (
    "1a6d92872ff9f91064b172ebce7e174226ccc4020a261c11b5e31c34f4d4416a"
)


def test_ci_uses_python_310_and_has_fail_closed_linux_no_egress_gate():
    workflow_path = REPOSITORY_ROOT / ".github" / "workflows" / "ci.yml"
    workflow_source = workflow_path.read_text(encoding="utf-8")
    workflow = yaml.safe_load(workflow_source)
    setup_steps = [
        step
        for job in workflow["jobs"].values()
        for step in job["steps"]
        if step.get("uses", "").startswith("actions/setup-python@")
    ]
    assert setup_steps
    assert all(step["with"]["python-version"] == "3.10" for step in setup_steps)
    checkout_steps = [
        step
        for job_definition in workflow["jobs"].values()
        for step in job_definition["steps"]
        if step.get("uses", "").startswith("actions/checkout@")
    ]
    assert checkout_steps
    assert all(
        step.get("with", {}).get("persist-credentials") is False
        for step in checkout_steps
    )
    triggers = yaml.load(workflow_source, Loader=yaml.BaseLoader)["on"]
    assert triggers["pull_request"]["branches"] == ["main", "team-main"]
    assert triggers["push"]["branches"] == ["main", "team-main"]

    job = workflow["jobs"]["batch-v2-linux-offline"]
    assert job["runs-on"] == "ubuntu-latest"
    assert job["timeout-minutes"] == 45
    steps = job["steps"]
    names = [step["name"] for step in steps]
    assert names.index("Install offline-gate dependencies") < names.index(
        "Run Batch V2 test process without egress or credentials"
    )
    resolver_step = next(
        step
        for step in steps
        if step["name"] == "Resolve Batch V2 CPython 3.10 Linux lock"
    )
    assert resolver_step["run"] == (
        "python -B scripts/batch_v2_verify_py310_lock.py resolve"
    )
    assert names.index("Install offline-gate dependencies") < names.index(
        "Resolve Batch V2 CPython 3.10 Linux lock"
    ) < names.index("Run Batch V2 test process without egress or credentials")
    gate_step = steps[
        names.index("Run Batch V2 test process without egress or credentials")
    ]
    assert gate_step["run"] == "bash scripts/run_batch_v2_linux_offline_gate.sh"
    install_step = next(
        step for step in steps if step["name"] == "Install offline-gate dependencies"
    )
    assert "acl" in install_step["run"].split()
    assert "OPENMONTAGE_ALLOW_NETWORK=1" not in workflow_source


def test_linux_gate_is_os_level_fail_closed_and_covers_required_suites():
    gate_path = REPOSITORY_ROOT / "scripts" / "run_batch_v2_linux_offline_gate.sh"
    gate = gate_path.read_text(encoding="utf-8")
    index_entry = subprocess.check_output(
        ["git", "ls-files", "--stage", "--", gate_path.relative_to(REPOSITORY_ROOT)],
        cwd=REPOSITORY_ROOT,
        text=True,
    ).strip()
    assert index_entry.split(maxsplit=1)[0] == "100755"
    for required in (
        "set -euo pipefail",
        "unshare --net",
        "setpriv",
        "setfacl",
        "findmnt",
        "--no-new-privs",
        "--bounding-set=-all",
        "--inh-caps=-all",
        "--ambient-caps=-all",
        "ip link set lo up",
        "ip route show default",
        "ip -o link show up",
        "env -i",
        "OPENMONTAGE_ALLOW_NETWORK=0",
        'gate_uid="65532"',
        'gate_script_index_mode" != "100755"',
        'BATCH_V2_GATE_ROOT',
        'BATCH_V2_GATE_GIT_DIRECTORY',
        'BATCH_V2_GATE_GIT_COMMON_DIRECTORY',
        '[[ -r "$gate_script" && -x "$gate_script" ]]',
        '[[ -r "$python_executable" && -x "$python_executable" ]]',
        '[[ -r "$repository" && -x "$repository" && ! -w "$repository" ]]',
        '[[ -r "$git_directory" && -x "$git_directory" && ! -w "$git_directory" ]]',
        '[[ -r "$git_common_directory" && -x "$git_common_directory" && ! -w "$git_common_directory" ]]',
        'find "$repository" -xdev \\( -type d -o -type f \\) -writable -print -quit',
        '-type f -perm /111',
        '-writable -print0',
        '"$BATCH_V2_GATE_ROOT"|"$BATCH_V2_GATE_ROOT/"*',
        '"$BATCH_V2_GATE_GIT_DIRECTORY/config"',
        'findmnt -rn -o TARGET',
        "nested mounts inside the checkout are unsupported",
        'gate_home="$gate_root/home"',
        'gate_tmp="$gate_root/os-temp"',
        'gate_pytest="$gate_root/pytest"',
        '--basetemp="$BATCH_V2_GATE_PYTEST"',
        "batch_v2_ci_runtime_assert.py",
        "git-metadata",
        "sudo -n true",
        "tests/batch_executor",
        "tests/contracts/test_phase0_contracts.py",
        "tests/contracts/test_checkpoint_read_gate.py",
        "tests/lib/test_checkpoint_prerequisites.py",
        "tests/lib/test_checkpoint_noncanonical_stage.py",
        "tests/tools/test_base_tool_dependencies.py",
        "tests/lib/test_gcs_auto_sync.py",
        "tests/backlot",
        "tests/contracts/test_backlot_contract.py",
        "tests/tools/test_gemini_omni_video.py",
        "tests/tools/test_gemini_omni_portability.py",
    ):
        assert required in gate
    assert "sudo -n unshare --net -- true" in gate
    assert "sensitive credential material exists in the test workspace" in gate
    assert "batch_v2_ci_preflight.py" in gate
    assert "exit 64" in gate
    assert "OPENMONTAGE_ALLOW_NETWORK=1" not in gate
    assert 'default_routes="$(ip route show default 2>&1)"' in gate
    assert 'active_links="$(ip -o link show up 2>&1)"' in gate
    assert "ip route show default |" not in gate
    assert "ip -o link show up |" not in gate
    assert "grep_status=$?" in gate
    assert gate.count("gate-runtime") == 2
    assert "git_metadata_before" in gate
    assert "git_metadata_after" in gate
    assert "Git metadata changed during legacy --help" in gate
    assert "host_uid" not in gate
    namespace_launch = gate.index("sudo -n unshare --net -- bash")
    assert gate.count("--no-new-privs") == 2
    privilege_drop = gate.index("--no-new-privs", namespace_launch)
    dropped_handoff = gate.index(
        '"$7/scripts/run_batch_v2_linux_offline_gate.sh" --dropped-payload'
    )
    legacy_help = gate.index(
        '"$BATCH_V2_GATE_PYTHON" -B scripts/batch_run_intent_sequences.py --help'
    )
    pytest_launch = gate.index('"$BATCH_V2_GATE_PYTHON" -m pytest')
    assert namespace_launch < privilege_drop < dropped_handoff
    assert legacy_help < pytest_launch
    assert "scripts/batch_run_intent_sequences.py --seq" not in gate


@pytest.mark.parametrize(
    "relative_path",
    (
        ".env",
        ".env.local",
        "production.env",
        "private/PRODUCTION.ENV",
        ".youtube-token.json",
        "private/gcp-production.json",
        "private/service-account-prod.json",
        "private/service_account.json",
        "private/credentials-prod.json",
        "private/client-credential.json",
        "private/private-key.pem",
        "private/key.p12",
        "private/auth.key",
    ),
)
def test_ci_workspace_preflight_rejects_credential_names_without_reading_or_leak(
    tmp_path, capsys, monkeypatch, relative_path
):
    from scripts.batch_v2_ci_preflight import main

    allowed = tmp_path / ".env.example"
    allowed.write_text("DOCUMENTATION_ONLY=", encoding="utf-8")
    candidate = tmp_path / relative_path
    candidate.parent.mkdir(parents=True, exist_ok=True)
    secret = "do-not-read-or-print-this-secret"
    candidate.write_text(secret, encoding="utf-8")

    def forbid_content_read(*_args, **_kwargs):
        raise AssertionError("workspace preflight must inspect names only")

    monkeypatch.setattr(Path, "read_text", forbid_content_read)
    monkeypatch.setattr(Path, "read_bytes", forbid_content_read)

    assert main(["--workspace", str(tmp_path)]) == 64
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "sensitive credential material exists in the test workspace" in captured.err
    assert relative_path not in captured.err
    assert secret not in captured.err


def test_ci_workspace_preflight_accepts_documentation_only(tmp_path, monkeypatch):
    from scripts.batch_v2_ci_preflight import main

    (tmp_path / ".env.example").write_text("DOCUMENTATION_ONLY=", encoding="utf-8")
    (tmp_path / "ordinary.json").write_text("{}", encoding="utf-8")

    def forbid_content_read(*_args, **_kwargs):
        raise AssertionError("workspace preflight must inspect names only")

    monkeypatch.setattr(Path, "read_text", forbid_content_read)
    monkeypatch.setattr(Path, "read_bytes", forbid_content_read)
    assert main(["--workspace", str(tmp_path)]) == 0


def test_ci_workspace_preflight_scans_gitignored_untracked_names(tmp_path, capsys):
    from scripts.batch_v2_ci_preflight import main

    (tmp_path / ".gitignore").write_text("ignored/\n", encoding="utf-8")
    candidate = tmp_path / "ignored" / "gcp-production.json"
    candidate.parent.mkdir()
    candidate.write_text("must-not-be-read", encoding="utf-8")

    assert main(["--workspace", str(tmp_path)]) == 64
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "sensitive credential material exists" in captured.err
    assert "gcp-production.json" not in captured.err


def test_ci_workspace_preflight_safely_prunes_test_sandbox(tmp_path):
    from scripts.batch_v2_ci_preflight import main

    sandbox = tmp_path / ".pytest-tmp"
    sandbox.mkdir()
    (sandbox / "gcp-adversarial-fixture.json").write_text(
        "fixture-only", encoding="utf-8"
    )

    assert main(["--workspace", str(tmp_path)]) == 0


def test_ci_workspace_preflight_fails_closed_without_path_disclosure(tmp_path, capsys):
    from scripts.batch_v2_ci_preflight import main

    missing = tmp_path / "private-workspace-must-not-be-printed"
    assert main(["--workspace", str(missing)]) == 64
    captured = capsys.readouterr()
    assert str(missing) not in captured.err
    assert "sensitive credential material exists in the test workspace" in captured.err


def test_ci_runtime_temp_layout_is_dynamically_checked(tmp_path, monkeypatch):
    from scripts.batch_v2_ci_runtime_assert import (
        GateRuntimeContractError,
        assert_repo_local_temp_layout,
    )

    repository = tmp_path / "repository"
    gate = repository / ".pytest-tmp" / "batch-v2-linux.dynamic"
    gate_home = gate / "home"
    gate_tmp = gate / "os-temp"
    gate_pytest = gate / "pytest"
    for directory in (gate_home, gate_tmp, gate_pytest):
        directory.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("HOME", str(gate_home))
    monkeypatch.setenv("TMPDIR", str(gate_tmp))

    assert_repo_local_temp_layout(
        repository=repository,
        home=gate_home,
        os_temp=gate_tmp,
        pytest_basetemp=gate_pytest,
    )
    assert any(gate_tmp.iterdir()) is False

    nested_home = gate_pytest / "nested-home"
    nested_home.mkdir()
    with pytest.raises(GateRuntimeContractError):
        assert_repo_local_temp_layout(
            repository=repository,
            home=nested_home,
            os_temp=gate_tmp,
            pytest_basetemp=gate_pytest,
        )


def test_ci_runtime_failure_reports_only_stable_category(monkeypatch, capsys):
    import scripts.batch_v2_ci_runtime_assert as runtime_assert

    def fail_with_known_category(**_kwargs):
        raise runtime_assert.GateRuntimeContractError(
            runtime_assert.GateFailureCategory.TEMP_WRITE
        )

    monkeypatch.setattr(runtime_assert, "assert_gate_runtime", fail_with_known_category)
    result = runtime_assert.main(
        [
            "gate-runtime",
            "--repository",
            "/sensitive/repository-name",
            "--home",
            "/sensitive/home-name",
            "--os-temp",
            "/sensitive/temp-name",
            "--pytest-basetemp",
            "/sensitive/pytest-name",
        ]
    )

    assert result == 64
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "ERROR: Batch V2 CI assertion failed [temp_write]\n"
    assert "sensitive" not in captured.err


def test_ci_runtime_failure_never_exposes_underlying_exception(monkeypatch, capsys):
    import scripts.batch_v2_ci_runtime_assert as runtime_assert

    def fail_with_secret_bearing_exception(**_kwargs):
        raise OSError("/private/token-path: super-secret-value")

    monkeypatch.setattr(
        runtime_assert, "assert_gate_runtime", fail_with_secret_bearing_exception
    )
    result = runtime_assert.main(
        [
            "gate-runtime",
            "--repository",
            "/repository",
            "--home",
            "/home",
            "--os-temp",
            "/temp",
            "--pytest-basetemp",
            "/pytest",
        ]
    )

    assert result == 64
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "ERROR: Batch V2 CI assertion failed [internal]\n"
    assert "private" not in captured.err
    assert "secret" not in captured.err


@pytest.mark.parametrize(
    ("field", "expected_category"),
    (
        ("CapInh", "cap_inh"),
        ("CapPrm", "cap_prm"),
        ("CapEff", "cap_eff"),
        ("CapBnd", "cap_bnd"),
        ("CapAmb", "cap_amb"),
    ),
)
def test_ci_runtime_capability_failures_have_field_categories(
    monkeypatch, field, expected_category
):
    import scripts.batch_v2_ci_runtime_assert as runtime_assert

    monkeypatch.setattr(runtime_assert.sys, "platform", "linux")
    monkeypatch.setattr(runtime_assert.os, "geteuid", lambda: 65532, raising=False)
    monkeypatch.setattr(runtime_assert.os, "getegid", lambda: 65532, raising=False)
    monkeypatch.setenv("BATCH_V2_GATE_UID", "65532")
    monkeypatch.setenv("BATCH_V2_GATE_GID", "65532")
    privilege_state = {
        "NoNewPrivs": "1",
        "CapInh": "0",
        "CapPrm": "0",
        "CapEff": "0",
        "CapBnd": "0",
        "CapAmb": "0",
    }
    privilege_state[field] = "1"
    monkeypatch.setattr(
        runtime_assert, "_linux_privilege_state", lambda: privilege_state
    )
    monkeypatch.setattr(
        runtime_assert, "assert_repo_local_temp_layout", lambda **_kwargs: None
    )

    with pytest.raises(runtime_assert.GateRuntimeContractError) as failure:
        runtime_assert.assert_gate_runtime(
            repository=Path("repository"),
            home=Path("home"),
            os_temp=Path("temp"),
            pytest_basetemp=Path("pytest"),
        )

    assert failure.value.category.value == expected_category


def test_ci_runtime_missing_capability_field_is_proc_status(monkeypatch):
    import scripts.batch_v2_ci_runtime_assert as runtime_assert

    monkeypatch.setattr(runtime_assert.sys, "platform", "linux")
    monkeypatch.setattr(runtime_assert.os, "geteuid", lambda: 65532, raising=False)
    monkeypatch.setattr(runtime_assert.os, "getegid", lambda: 65532, raising=False)
    monkeypatch.setenv("BATCH_V2_GATE_UID", "65532")
    monkeypatch.setenv("BATCH_V2_GATE_GID", "65532")
    monkeypatch.setattr(
        runtime_assert,
        "_linux_privilege_state",
        lambda: {"NoNewPrivs": "1"},
    )

    with pytest.raises(runtime_assert.GateRuntimeContractError) as failure:
        runtime_assert.assert_gate_runtime(
            repository=Path("repository"),
            home=Path("home"),
            os_temp=Path("temp"),
            pytest_basetemp=Path("pytest"),
        )

    assert failure.value.category is runtime_assert.GateFailureCategory.PROC_STATUS


def test_ci_runtime_proc_parser_ignores_empty_supplementary_groups():
    import scripts.batch_v2_ci_runtime_assert as runtime_assert

    parsed = runtime_assert._parse_linux_privilege_state(
        [
            "Name:\tpython",
            "Groups:\t",
            "NoNewPrivs:\t1",
            "CapInh:\t0000000000000000",
            "CapPrm:\t0000000000000000",
            "CapEff:\t0000000000000000",
            "CapBnd:\t0000000000000000",
            "CapAmb:\t0000000000000000",
        ]
    )

    assert parsed == {
        "NoNewPrivs": "1",
        "CapInh": "0000000000000000",
        "CapPrm": "0000000000000000",
        "CapEff": "0000000000000000",
        "CapBnd": "0000000000000000",
        "CapAmb": "0000000000000000",
    }


@pytest.mark.parametrize(
    "mutate_lines",
    (
        lambda lines: lines[:-1],
        lambda lines: [*lines, lines[-1]],
        lambda lines: [*lines[:-1], "CapAmb:\t"],
    ),
)
def test_ci_runtime_proc_parser_rejects_invalid_required_fields(mutate_lines):
    import scripts.batch_v2_ci_runtime_assert as runtime_assert

    valid_lines = [
        "NoNewPrivs:\t1",
        "CapInh:\t0",
        "CapPrm:\t0",
        "CapEff:\t0",
        "CapBnd:\t0",
        "CapAmb:\t0",
    ]
    with pytest.raises(runtime_assert.GateRuntimeContractError) as failure:
        runtime_assert._parse_linux_privilege_state(mutate_lines(valid_lines))

    assert failure.value.category is runtime_assert.GateFailureCategory.PROC_STATUS


def test_ci_runtime_environment_path_errors_are_categorized(tmp_path, monkeypatch):
    import scripts.batch_v2_ci_runtime_assert as runtime_assert

    repository = tmp_path / "repository"
    gate = repository / ".pytest-tmp" / "batch-v2-linux.dynamic"
    roots = [gate / name for name in ("home", "os-temp", "pytest")]
    for root in roots:
        root.mkdir(parents=True, exist_ok=True)
    invalid_home = tmp_path / "sensitive-home-path"
    monkeypatch.setenv("HOME", str(invalid_home))
    monkeypatch.setenv("TMPDIR", str(roots[1]))
    original_resolve = Path.resolve

    def fail_only_for_configured_home(path, *args, **kwargs):
        if path == invalid_home:
            raise OSError("must not be disclosed")
        return original_resolve(path, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", fail_only_for_configured_home)
    with pytest.raises(runtime_assert.GateRuntimeContractError) as failure:
        runtime_assert.assert_repo_local_temp_layout(
            repository=repository,
            home=roots[0],
            os_temp=roots[1],
            pytest_basetemp=roots[2],
        )

    assert (
        failure.value.category
        is runtime_assert.GateFailureCategory.TEMP_ENVIRONMENT
    )


def test_ci_git_metadata_digest_detects_config_and_hook_mutation(tmp_path):
    from scripts.batch_v2_ci_runtime_assert import git_metadata_digest

    git_dir = tmp_path / ".git"
    hooks = git_dir / "hooks"
    hooks.mkdir(parents=True)
    config = git_dir / "config"
    config.write_text("[core]\n", encoding="utf-8")
    baseline = git_metadata_digest(tmp_path)

    config.write_text("[core]\n\thooksPath = .githooks\n", encoding="utf-8")
    assert git_metadata_digest(tmp_path) != baseline
    config.write_text("[core]\n", encoding="utf-8")
    assert git_metadata_digest(tmp_path) == baseline

    (hooks / "commit-msg").write_text("#!/bin/sh\n", encoding="utf-8")
    assert git_metadata_digest(tmp_path) != baseline


@pytest.mark.skipif(
    os.environ.get("BATCH_V2_LINUX_GATE") != "1",
    reason="dynamic dropped-context proof runs only inside the Linux gate",
)
def test_linux_gate_dynamically_proves_dropped_context_and_temp_layout():
    from scripts.batch_v2_ci_runtime_assert import assert_gate_runtime

    assert_gate_runtime(
        repository=Path(os.environ["BATCH_V2_REPOSITORY_ROOT"]),
        home=Path(os.environ["HOME"]),
        os_temp=Path(os.environ["TMPDIR"]),
        pytest_basetemp=Path(os.environ["BATCH_V2_GATE_PYTEST"]),
    )


def test_clean_install_declares_legacy_imageio_ffmpeg_dependency():
    requirements = (REPOSITORY_ROOT / "requirements.txt").read_text(encoding="utf-8")
    requirement_names = {
        line.split(";", 1)[0].split("[", 1)[0].split("=", 1)[0].split(">", 1)[0]
        .strip()
        .lower()
        for line in requirements.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    assert "imageio-ffmpeg" in requirement_names


def test_gemini_docs_require_explicit_route_project_and_do_not_infer_vertex():
    env_example = (REPOSITORY_ROOT / ".env.example").read_text(encoding="utf-8")
    providers = (REPOSITORY_ROOT / "docs" / "PROVIDERS.md").read_text(
        encoding="utf-8"
    )
    combined = env_example + "\n" + providers
    assert "route=vertex_interactions" in combined
    assert "vertex_project" in combined
    assert "vertex_location" in combined
    assert "credentials alone never select Vertex" in combined


def test_legacy_runner_is_byte_unchanged_and_rehearsal_never_executes_it():
    from scripts.batch_v2_rehearse_rollback import rehearse_rollback

    before = LEGACY_RUNNER.read_bytes()
    assert hashlib.sha256(before).hexdigest() == LEGACY_RUNNER_SHA256

    evidence = rehearse_rollback(REPOSITORY_ROOT)

    assert evidence["status"] == "passed"
    assert evidence["legacy_runner_sha256"] == LEGACY_RUNNER_SHA256
    assert evidence["help_exit_code"] == 0
    assert evidence["stub_dispatch"] == {"4": [4], "all": [4, 5, 6]}
    assert evidence["real_provider_calls"] == 0
    assert evidence["canonical_writes"] == 0
    assert evidence["v2_is_opt_in"] is True
    assert LEGACY_RUNNER.read_bytes() == before


def test_migration_and_evidence_docs_preserve_release_boundaries():
    migration = (
        REPOSITORY_ROOT / "docs" / "batch-v2-migration-rollback.md"
    ).read_text(encoding="utf-8")
    evidence = (
        REPOSITORY_ROOT / "docs" / "batch-v2-m4-offline-evidence.md"
    ).read_text(encoding="utf-8")
    evidence_words = " ".join(evidence.split())
    current_evidence_words = " ".join(
        evidence.split("## Historical Windows M4 evidence", 1)[0].split()
    )
    cloud_run = (
        REPOSITORY_ROOT / "docs" / "batch-v2-cloud-run.md"
    ).read_text(encoding="utf-8")
    for required in (
        "V2 remains opt-in",
        "batch_run_intent_sequences.py",
        "--help",
        "parser/dispatch stubs",
        "git revert",
        "git cherry-pick",
        "team-main-pre-batch-v2",
    ):
        assert required in migration
    assert "--seq 4" not in migration
    assert "--seq all" not in migration

    for required in (
        "M3: completed",
        "M4: completed",
        "c5bc88e2fefa4db22b4e662fa52012d43586eab6",
        "pull/1",
        "run 34931811296",
        "job 104261401724",
        "2589 passed, 12 skipped, 3 xfailed, 1 warning, 1 subtest",
        "job 104261401886",
        "649 passed, 1 skipped, 2 warnings",
        "real CPython 3.10/Linux x86_64 resolver accepted 27 distributions",
        "job 104261401871",
        "b471851eac6ab3bfea399d874e3f6c8116188d8d",
        "sha256:6c16f916ab2b07a53e166022cfbf73b4698520dc6ec14fa8b234b403bb017717",
        "febe67479a3ff3ad75c40385a4829e02eb506158c0b6f50dd0ce8e112b962d42",
        "Config.User `65532:65532`",
        "No broken requirements found",
        "LocalStore",
        "FakeGCS",
        "The final GitHub job observed all of these checks on Linux",
        "test-process isolation",
        "The checkout and dependency installation may use network",
        "reported no P0, P1, or P2 finding",
        "Active-word highlight contrast remains a pre-existing",
        "not production-qualified",
        "legacy runner must not be retired",
        "unique writer",
        "legacy and executor identities have no write permission",
        "recorded generations",
        "latest-head == recorded-generation",
        "qualification remains blocked",
        "threat-model and architecture review",
        "immutable canonical objects plus a generation-CAS pointer",
        "protocol-external mutation invalidates qualification",
        "No production qualification is claimed",
        "rpds-py==2026.5.1",
        "rpds-py==0.30.0",
        "ResolutionImpossible",
    ):
        assert required in evidence_words
    assert "M3: in_progress" not in evidence_words
    assert "M4: in_progress" not in current_evidence_words
    assert "remains pending" not in current_evidence_words
    assert "remain unobserved" not in current_evidence_words
    assert "installing pinned test dependencies" not in cloud_run
    assert "lower-bound test dependencies" in cloud_run
    assert "M3 local-container gate passed at" in cloud_run


def test_ci_gate_temp_artifacts_are_ignored():
    ignore = (REPOSITORY_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".pytest-tmp/" in ignore.splitlines()


def test_m4_release_slice_does_not_modify_forbidden_runtime_surfaces():
    evidence = (
        REPOSITORY_ROOT / "docs" / "batch-v2-m4-offline-evidence.md"
    ).read_text(encoding="utf-8")
    assert "No engine, execution schema, publication, or Cloud Run template change" in evidence
