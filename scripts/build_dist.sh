#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

cp -R "$ROOT_DIR/site/." "$DIST_DIR/"
cp -R "$ROOT_DIR/logos" "$DIST_DIR/logos"

echo "Dist gerado em: $DIST_DIR"
