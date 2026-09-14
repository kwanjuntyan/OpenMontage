#!/usr/bin/env bash

# Dependencies are installed before this script runs. This script fail-closes
# unless it can isolate the test process and every child process in a fresh
# Linux network namespace with no egress interfaces.
set -euo pipefail

repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd "$repository_root"

if [[ "${1:-}" == "--dropped-payload" ]]; then
  for required_variable in \
    BATCH_V2_GATE_HOME \
    BATCH_V2_GATE_TMP \
    BATCH_V2_GATE_PYTEST \
    BATCH_V2_GATE_PYTHON \
    BATCH_V2_REPOSITORY_ROOT; do
    if [[ -z "${!required_variable:-}" ]]; then
      echo "ERROR: isolated gate launch contract is incomplete" >&2
      exit 64
    fi
  done

  # no_new_privs must make the runner's passwordless sudo rule unusable by
  # this process and every child. Capabilities are independently checked by
  # the dynamic Python assertion below.
  if sudo -n true >/dev/null 2>&1; then
    echo "ERROR: isolated gate process retained sudo elevation" >&2
    exit 64
  fi

  "$BATCH_V2_GATE_PYTHON" -B scripts/batch_v2_ci_runtime_assert.py \
    gate-runtime \
    --repository "$BATCH_V2_REPOSITORY_ROOT" \
    --home "$BATCH_V2_GATE_HOME" \
    --os-temp "$BATCH_V2_GATE_TMP" \
    --pytest-basetemp "$BATCH_V2_GATE_PYTEST"

  git_metadata_before="$(
    "$BATCH_V2_GATE_PYTHON" -B scripts/batch_v2_ci_runtime_assert.py \
      git-metadata --workspace "$BATCH_V2_REPOSITORY_ROOT"
  )"
  "$BATCH_V2_GATE_PYTHON" -B scripts/batch_run_intent_sequences.py --help \
    >/dev/null
  git_metadata_after="$(
    "$BATCH_V2_GATE_PYTHON" -B scripts/batch_v2_ci_runtime_assert.py \
      git-metadata --workspace "$BATCH_V2_REPOSITORY_ROOT"
  )"
  if [[ "$git_metadata_before" != "$git_metadata_after" ]]; then
    echo "ERROR: Git metadata changed during legacy --help" >&2
    exit 64
  fi

  "$BATCH_V2_GATE_PYTHON" -m pytest \
    tests/batch_executor \
    tests/contracts/test_phase0_contracts.py \
    tests/contracts/test_checkpoint_read_gate.py \
    tests/lib/test_checkpoint_prerequisites.py \
    tests/lib/test_checkpoint_noncanonical_stage.py \
    tests/tools/test_base_tool_dependencies.py \
    tests/lib/test_gcs_auto_sync.py \
    tests/backlot \
    tests/contracts/test_backlot_contract.py \
    tests/tools/test_gemini_omni_video.py \
    tests/tools/test_gemini_omni_portability.py \
    -q --basetemp="$BATCH_V2_GATE_PYTEST"

  "$BATCH_V2_GATE_PYTHON" -B scripts/batch_v2_ci_runtime_assert.py \
    gate-runtime \
    --repository "$BATCH_V2_REPOSITORY_ROOT" \
    --home "$BATCH_V2_GATE_HOME" \
    --os-temp "$BATCH_V2_GATE_TMP" \
    --pytest-basetemp "$BATCH_V2_GATE_PYTEST"
  exit 0
fi

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "ERROR: the Batch V2 no-egress gate requires Linux" >&2
  exit 64
fi

for required_command in sudo unshare setpriv ip grep mktemp; do
  if ! command -v "$required_command" >/dev/null 2>&1; then
    echo "ERROR: required isolation command is unavailable: $required_command" >&2
    exit 64
  fi
done

if [[ ! -x "$repository_root/.venv/bin/python" ]]; then
  echo "ERROR: install dependencies into .venv before running this gate" >&2
  exit 64
fi

# `env -i` prevents inherited credential variables. This name-only preflight
# prevents BaseTool or an SDK from discovering .env.example-adjacent secrets
# such as *service-account*.json or *credentials*.json in the checkout.
if ! "$repository_root/.venv/bin/python" \
  "$repository_root/scripts/batch_v2_ci_preflight.py" \
  --workspace "$repository_root"; then
  echo "ERROR: sensitive credential material exists in the test workspace" >&2
  exit 64
fi

if ! sudo -n true >/dev/null 2>&1; then
  echo "ERROR: passwordless sudo is required for the no-egress namespace" >&2
  exit 64
fi
if ! sudo -n unshare --net -- true >/dev/null 2>&1; then
  echo "ERROR: network namespaces are unavailable; refusing an unisolated test run" >&2
  exit 64
fi

mkdir -p "$repository_root/.pytest-tmp"
gate_root="$(mktemp -d "$repository_root/.pytest-tmp/batch-v2-linux.XXXXXX")"
gate_home="$gate_root/home"
gate_tmp="$gate_root/os-temp"
gate_pytest="$gate_root/pytest"
mkdir -p "$gate_home/.config" "$gate_tmp" "$gate_pytest"

case "$gate_root" in
  "$repository_root"/.pytest-tmp/batch-v2-linux.*) ;;
  *)
    echo "ERROR: unsafe Batch V2 gate temp root" >&2
    exit 64
    ;;
esac

cleanup_gate_root() {
  sudo -n rm -rf -- "$gate_root" >/dev/null 2>&1 || true
}
trap cleanup_gate_root EXIT

gate_uid="65532"
gate_gid="65532"
python_executable="$repository_root/.venv/bin/python"
if ! sudo -n chown -R "$gate_uid:$gate_gid" "$gate_root"; then
  echo "ERROR: unable to prepare the isolated gate temp root" >&2
  exit 64
fi

sudo -n unshare --net -- bash -ceu '
  if ! ip link set lo up >/dev/null 2>&1; then
    echo "ERROR: unable to enable isolated loopback" >&2
    exit 64
  fi
  if ! default_routes="$(ip route show default 2>&1)"; then
    echo "ERROR: unable to inspect isolated routes" >&2
    exit 64
  fi
  if [[ -n "$default_routes" ]]; then
    echo "ERROR: isolated test namespace unexpectedly has a default route" >&2
    exit 64
  fi
  if ! active_links="$(ip -o link show up 2>&1)"; then
    echo "ERROR: unable to inspect isolated interfaces" >&2
    exit 64
  fi
  set +e
  non_loopback_links="$(grep -vE "^[0-9]+: lo:" <<<"$active_links")"
  grep_status=$?
  set -e
  if [[ "$grep_status" -gt 1 ]]; then
    echo "ERROR: unable to validate isolated interfaces" >&2
    exit 64
  fi
  if [[ -n "$non_loopback_links" ]]; then
    echo "ERROR: isolated test namespace has a non-loopback interface" >&2
    exit 64
  fi
  exec setpriv \
    --reuid="$1" \
    --regid="$2" \
    --clear-groups \
    --no-new-privs \
    --bounding-set=-all \
    --inh-caps=-all \
    --ambient-caps=-all \
    -- \
    env -i \
      HOME="$3" \
      XDG_CONFIG_HOME="$3/.config" \
      TMPDIR="$4" \
      BATCH_V2_GATE_HOME="$3" \
      BATCH_V2_GATE_TMP="$4" \
      BATCH_V2_GATE_PYTEST="$5" \
      BATCH_V2_GATE_PYTHON="$6" \
      BATCH_V2_REPOSITORY_ROOT="$7" \
      BATCH_V2_GATE_UID="$1" \
      BATCH_V2_GATE_GID="$2" \
      BATCH_V2_LINUX_GATE=1 \
      GIT_CONFIG_COUNT=1 \
      GIT_CONFIG_KEY_0=safe.directory \
      GIT_CONFIG_VALUE_0="$7" \
      PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
      PYTHONPATH="$7" \
      CI=true \
      OPENMONTAGE_ALLOW_NETWORK=0 \
      PYTHONDONTWRITEBYTECODE=1 \
      PYTHONNOUSERSITE=1 \
      PYTHONHASHSEED=0 \
      bash "$7/scripts/run_batch_v2_linux_offline_gate.sh" --dropped-payload
' batch-v2-no-egress \
  "$gate_uid" \
  "$gate_gid" \
  "$gate_home" \
  "$gate_tmp" \
  "$gate_pytest" \
  "$python_executable" \
  "$repository_root"
