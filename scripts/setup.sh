#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
cd "$REPO_ROOT"

require() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: missing required command '$1'." >&2
    exit 1
  fi
}

require uv
require make

if [ ! -d ".venv" ]; then
  echo "Creating uv virtual environment (.venv)…"
  uv venv .venv
else
  echo "Virtual environment already exists (.venv)."
fi

echo "Installing development dependencies via uv…"
uv pip install -r requirements-dev.txt

declare -a TARGETS=("format" "lint" "type-check" "test")
for target in "${TARGETS[@]}"; do
  echo "Running make ${target}…"
  uv run make "${target}"
  echo
done

echo "Setup complete. Activate with: source .venv/bin/activate"
