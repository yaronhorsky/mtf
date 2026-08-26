#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$TMP_DIR/home" "$TMP_DIR/pipx-home" "$TMP_DIR/pipx-bin"

HOME="$TMP_DIR/home" \
PIPX_HOME="$TMP_DIR/pipx-home" \
PIPX_BIN_DIR="$TMP_DIR/pipx-bin" \
SHELL="/bin/bash" \
MFT_INSTALL_SPEC="$ROOT_DIR" \
MFT_SKIP_SETUP=1 \
bash "$ROOT_DIR/scripts/install.sh"

"$TMP_DIR/pipx-bin/moveo-fintech" --version
"$TMP_DIR/pipx-bin/moveo-fintech" --help >/dev/null

test -f "$TMP_DIR/home/.local/share/bash-completion/completions/moveo-fintech"
test -f "$TMP_DIR/home/.bashrc"

echo "installer test passed"
