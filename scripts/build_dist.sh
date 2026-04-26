#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

cp -R "$ROOT_DIR/site/." "$DIST_DIR/"
cp -R "$ROOT_DIR/logos" "$DIST_DIR/logos"
find "$DIST_DIR" -name .DS_Store -delete

SOURCE_SHA="unknown"
SOURCE_SHORT_SHA="unknown"
SOURCE_BRANCH="unknown"
SOURCE_COMMITTED_AT=""

if git -C "$ROOT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  SOURCE_SHA="$(git -C "$ROOT_DIR" rev-parse HEAD 2>/dev/null || echo unknown)"
  SOURCE_SHORT_SHA="$(git -C "$ROOT_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
  SOURCE_BRANCH="$(git -C "$ROOT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
  SOURCE_COMMITTED_AT="$(git -C "$ROOT_DIR" show -s --format=%cI HEAD 2>/dev/null || echo "")"
fi

cat > "$DIST_DIR/deploy-info.json" <<EOF
{
  "source_sha": "$SOURCE_SHA",
  "source_short_sha": "$SOURCE_SHORT_SHA",
  "source_branch": "$SOURCE_BRANCH",
  "source_committed_at": "$SOURCE_COMMITTED_AT"
}
EOF

echo "Dist gerado em: $DIST_DIR"
