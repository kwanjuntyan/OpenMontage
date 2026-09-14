#!/usr/bin/env bash

# Dependencies are installed before this script runs. This script fail-closes
# unless it can isolate the test process and every child process in a fresh
# Linux network namespace with no egress interfaces.
set -euo pipefail

repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd "$repository_root"

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "ERROR: the Batch V2 no-egress gate requires Linux" >&2
  exit 64
fi

for required_command in sudo unshare setpriv ip grep; do
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

gate_root="$repository_root/.pytest-tmp/batch-v2-linux"
gate_home="$gate_root/home"
gate_tmp="$gate_root/os-temp"
mkdir -p "$gate_home/.config" "$gate_tmp"

host_uid="$(id -u)"
host_gid="$(id -g)"
python_executable="$repository_root/.venv/bin/python"

sudo -n unshare --net -- bash -ceu '
  ip link set lo up
  if ip route show default | grep -q .; then
    echo "ERROR: isolated test namespace unexpectedly has a default route" >&2
    exit 64
  fi
  if ip -o link show up | grep -vE "^[0-9]+: lo:" | grep -q .; then
    echo "ERROR: isolated test namespace has a non-loopback interface" >&2
    exit 64
  fi
  setpriv --reuid="$1" --regid="$2" --clear-groups \
    env -i \
      HOME="$3" \
      XDG_CONFIG_HOME="$3/.config" \
      TMPDIR="$4" \
      PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
      PYTHONPATH="$6" \
      CI=true \
      OPENMONTAGE_ALLOW_NETWORK=0 \
      PYTHONDONTWRITEBYTECODE=1 \
      PYTHONNOUSERSITE=1 \
      "$5" -B scripts/batch_run_intent_sequences.py --help >/dev/null
  exec setpriv --reuid="$1" --regid="$2" --clear-groups \
    env -i \
      HOME="$3" \
      XDG_CONFIG_HOME="$3/.config" \
      TMPDIR="$4" \
      PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
      PYTHONPATH="$6" \
      CI=true \
      OPENMONTAGE_ALLOW_NETWORK=0 \
      PYTHONDONTWRITEBYTECODE=1 \
      PYTHONNOUSERSITE=1 \
      PYTHONHASHSEED=0 \
      "$5" -m pytest \
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
        -q --basetemp=.pytest-tmp/batch-v2-linux
' batch-v2-no-egress \
  "$host_uid" \
  "$host_gid" \
  "$gate_home" \
  "$gate_tmp" \
  "$python_executable" \
  "$repository_root"
