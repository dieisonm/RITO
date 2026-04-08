#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RELEASE_DIR="$ROOT_DIR/release"
ZIP_PATH="$RELEASE_DIR/ritosistemas-hostinger.zip"

bash "$ROOT_DIR/scripts/build_dist.sh"

rm -rf "$RELEASE_DIR"
mkdir -p "$RELEASE_DIR"

cd "$ROOT_DIR/dist"
zip -qr "$ZIP_PATH" .

echo "Pacote gerado em: $ZIP_PATH"
