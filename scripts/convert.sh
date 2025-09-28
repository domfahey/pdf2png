#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: $0 --pdf PATH [--out DIR] [--prefix NAME] [--overwrite]

Convert a scanned PDF to lossless PNG images using the repository CLI.
Run 'uv run make install' beforehand to ensure dependencies are available.
If --out is omitted, PNGs are written to the current directory.
USAGE
}

CALLER_PWD="$(pwd)"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
cd "$REPO_ROOT"

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: 'uv' command not found. Install uv before running this script." >&2
  exit 1
fi

if [ ! -x .venv/bin/python ]; then
  echo "Error: .venv/bin/python not found. Run 'uv run make install' first." >&2
  exit 1
fi

PDF=""
OUT=""
PREFIX=""
OVERWRITE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pdf)
      PDF="$2"
      shift 2
      ;;
    --out)
      OUT="$2"
      shift 2
      ;;
    --prefix)
      PREFIX="$2"
      shift 2
      ;;
    --overwrite)
      OVERWRITE=true
      shift 1
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$PDF" ]]; then
  echo "Error: --pdf is required." >&2
  usage
  exit 1
fi

if [[ -z "$OUT" ]]; then
  OUT="$CALLER_PWD"
fi

cmd=(uv run --python .venv/bin/python pdf2png.py "$PDF" "$OUT")

if [[ -n "$PREFIX" ]]; then
  cmd+=(--prefix "$PREFIX")
fi

if [[ "$OVERWRITE" == true ]]; then
  cmd+=(--overwrite)
fi

"${cmd[@]}"
