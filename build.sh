#!/usr/bin/env bash
# Build a self-contained executable for the Subtitles Translator CLI.
#
# Usage:
#   ./build.sh
#
# The resulting binary is written to dist/subtitles-translator and runs on the
# host platform (here: macOS). Build on Windows/Linux to target those systems.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON="${PYTHON:-$ROOT_DIR/.venv/bin/python}"

echo "==> Using Python: $($PYTHON --version)"
echo "==> Ensuring build dependencies are installed"
"$PYTHON" -m pip install --quiet --upgrade pip pyinstaller requests

echo "==> Cleaning previous build artifacts"
rm -rf build dist

echo "==> Building executable"
"$PYTHON" -m PyInstaller --clean --noconfirm subtitles-translator.spec

echo "==> Done. Binary available at: dist/subtitles-translator"
