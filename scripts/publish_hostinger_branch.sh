#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE_URL="$(git -C "$ROOT_DIR" remote get-url origin)"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}

trap cleanup EXIT

bash "$ROOT_DIR/scripts/build_dist.sh"

cp -R "$ROOT_DIR/dist/." "$TMP_DIR/"

git -C "$TMP_DIR" init -b hostinger >/dev/null
git -C "$TMP_DIR" remote add origin "$REMOTE_URL"
git -C "$TMP_DIR" add .
git -C "$TMP_DIR" commit -m "Deploy Hostinger site" >/dev/null
git -C "$TMP_DIR" push -f origin hostinger

echo "Branch hostinger publicada com sucesso."
