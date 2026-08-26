#!/usr/bin/env bash
set -euo pipefail

APP_NAME="moveo-fintech"
PACKAGE_NAME="moveo-fintech-tools"
INSTALL_SPEC="${MFT_INSTALL_SPEC:-git+https://github.com/yaronhorsky/mtf.git}"
MIN_PYTHON="3.11"

info() {
  printf '\033[1;36m%s\033[0m\n' "$1" >&2
}

warn() {
  printf '\033[1;33m%s\033[0m\n' "$1" >&2
}

fail() {
  printf '\033[1;31m%s\033[0m\n' "$1" >&2
  exit 1
}

python_ok() {
  "$1" - "$MIN_PYTHON" <<'PY'
import sys

minimum = tuple(int(part) for part in sys.argv[1].split("."))
raise SystemExit(0 if sys.version_info[:2] >= minimum else 1)
PY
}

find_python() {
  if command -v python3 >/dev/null 2>&1 && python_ok "$(command -v python3)"; then
    command -v python3
    return 0
  fi

  if command -v python >/dev/null 2>&1 && python_ok "$(command -v python)"; then
    command -v python
    return 0
  fi

  return 1
}

install_python() {
  info "Python ${MIN_PYTHON}+ was not found. Preparing Python..."

  if command -v mise >/dev/null 2>&1; then
    mise install python@latest
    mise use -g python@latest
    return 0
  fi

  if command -v brew >/dev/null 2>&1; then
    brew install python
    return 0
  fi

  if [[ "$(uname -s)" == "Darwin" ]]; then
    info "Installing mise so Python can be prepared consistently..."
    curl https://mise.run | sh
    export PATH="$HOME/.local/bin:$PATH"
    mise install python@latest
    mise use -g python@latest
    return 0
  fi

  fail "Python ${MIN_PYTHON}+ is required. Install Python and rerun this script."
}

ensure_python() {
  local python_bin

  if python_bin="$(find_python)"; then
    printf '%s\n' "$python_bin"
    return 0
  fi

  install_python

  if python_bin="$(find_python)"; then
    printf '%s\n' "$python_bin"
    return 0
  fi

  fail "Could not prepare Python ${MIN_PYTHON}+."
}

ensure_pipx() {
  local python_bin="$1"

  if "$python_bin" -m pipx --version >/dev/null 2>&1; then
    return 0
  fi

  info "Preparing pipx..."
  "$python_bin" -m pip install --user --upgrade pipx
}

resolve_app() {
  local python_bin="$1"
  local pipx_bin_dir

  pipx_bin_dir="${PIPX_BIN_DIR:-}"
  if [[ -z "$pipx_bin_dir" ]]; then
    pipx_bin_dir="$($python_bin -m pipx environment --value PIPX_BIN_DIR 2>/dev/null || true)"
  fi

  if [[ -n "$pipx_bin_dir" && -x "$pipx_bin_dir/$APP_NAME" ]]; then
    printf '%s\n' "$pipx_bin_dir/$APP_NAME"
    return 0
  fi

  if [[ -x "$HOME/.local/bin/$APP_NAME" ]]; then
    printf '%s\n' "$HOME/.local/bin/$APP_NAME"
    return 0
  fi

  if command -v "$APP_NAME" >/dev/null 2>&1; then
    command -v "$APP_NAME"
    return 0
  fi

  return 1
}

resolve_app_python() {
  local python_bin="$1"
  local pipx_home

  pipx_home="${PIPX_HOME:-}"
  if [[ -z "$pipx_home" ]]; then
    pipx_home="$($python_bin -m pipx environment --value PIPX_HOME 2>/dev/null || true)"
  fi

  if [[ -n "$pipx_home" && -x "$pipx_home/venvs/$PACKAGE_NAME/bin/python" ]]; then
    printf '%s\n' "$pipx_home/venvs/$PACKAGE_NAME/bin/python"
    return 0
  fi

  return 1
}

app_python() {
  local app_path="$1"
  local resolved_path="$app_path"
  local shebang
  local second_line

  while [[ -L "$resolved_path" ]]; do
    local target
    target="$(readlink "$resolved_path")"
    if [[ "$target" == /* ]]; then
      resolved_path="$target"
    else
      resolved_path="$(dirname "$resolved_path")/$target"
    fi
  done

  IFS= read -r shebang < "$resolved_path" || return 1
  second_line="$(sed -n '2p' "$resolved_path")"
  shebang="${shebang#\#!}"

  if [[ "$shebang" == "/bin/sh" && "$second_line" == *"exec"*"python"* ]]; then
    local shim_python
    shim_python="$(printf '%s\n' "$second_line" | sed -n "s/.*exec' '\([^']*\)'.*/\1/p")"
    if [[ -x "$shim_python" ]]; then
      printf '%s\n' "$shim_python"
      return 0
    fi
  fi

  if [[ "$shebang" == /usr/bin/env\ python* ]]; then
    local env_python
    env_python="${shebang#/usr/bin/env }"
    if command -v "$env_python" >/dev/null 2>&1; then
      command -v "$env_python"
      return 0
    fi
  fi

  if [[ -x "$shebang" ]]; then
    printf '%s\n' "$shebang"
    return 0
  fi

  return 1
}

completion_script() {
  local python_bin="$1"
  local shell_name="$2"

  "$python_bin" - "$APP_NAME" "_MOVEO_FINTECH_COMPLETE" "$shell_name" <<'PY'
import sys
from typer.completion import get_completion_script

prog_name, complete_var, shell = sys.argv[1:]
print(get_completion_script(prog_name=prog_name, complete_var=complete_var, shell=shell))
PY
}

append_managed_block() {
  local rc_file="$1"
  local block="$2"

  mkdir -p "$(dirname "$rc_file")"
  touch "$rc_file"

  if grep -q "MOVEO FINTECH COMPLETION START" "$rc_file"; then
    return 0
  fi

  {
    printf '\n# MOVEO FINTECH COMPLETION START\n'
    printf '%b\n' "$block"
    printf '# MOVEO FINTECH COMPLETION END\n'
  } >> "$rc_file"
}

install_completion() {
  local app_path="$1"
  local installer_python_bin="$2"
  local shell_path="${SHELL:-}"
  local shell_name
  local python_bin

  shell_name="$(basename "$shell_path")"
  python_bin="$(resolve_app_python "$installer_python_bin")" || python_bin="$(app_python "$app_path")" || return 1

  case "$shell_name" in
    zsh)
      local completion_dir="$HOME/.zfunc"
      mkdir -p "$completion_dir"
      completion_script "$python_bin" "zsh" > "$completion_dir/_$APP_NAME"
      append_managed_block "$HOME/.zshrc" "fpath=(\"$completion_dir\" \$fpath)\nautoload -Uz compinit\ncompinit"
      ;;
    bash)
      local completion_dir="$HOME/.local/share/bash-completion/completions"
      mkdir -p "$completion_dir"
      completion_script "$python_bin" "bash" > "$completion_dir/$APP_NAME"
      append_managed_block "$HOME/.bashrc" "source \"$completion_dir/$APP_NAME\""
      ;;
    fish)
      local completion_dir="$HOME/.config/fish/completions"
      mkdir -p "$completion_dir"
      completion_script "$python_bin" "fish" > "$completion_dir/$APP_NAME.fish"
      ;;
    *)
      "$app_path" --install-completion >/dev/null
      ;;
  esac
}

main() {
  info "Installing Moveo Fintech Tools..."

  local python_bin
  python_bin="$(ensure_python)"

  ensure_pipx "$python_bin"
  "$python_bin" -m pipx ensurepath >/dev/null || true

  info "Installing ${APP_NAME}..."
  "$python_bin" -m pipx install "$INSTALL_SPEC" --force

  local app_path
  app_path="$(resolve_app "$python_bin")" || fail "Installed ${APP_NAME}, but could not resolve its executable path."

  info "Installing shell autocomplete..."
  install_completion "$app_path" "$python_bin" || warn "Autocomplete could not be installed automatically. Run: ${APP_NAME} --install-completion"

  if [[ "${MFT_SKIP_SETUP:-0}" != "1" ]]; then
    "$app_path" setup
  fi

  info "Moveo Fintech Tools is ready."
  warn "If your current shell does not see ${APP_NAME} or tab completion yet, open a new terminal or run: rehash"
}

main "$@"
