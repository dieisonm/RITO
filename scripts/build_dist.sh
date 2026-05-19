#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

cp -R "$ROOT_DIR/site/." "$DIST_DIR/"
rm -rf "$DIST_DIR/logos"
cp -R "$ROOT_DIR/logos" "$DIST_DIR/logos"
find "$DIST_DIR" -name .DS_Store -delete
find "$DIST_DIR/storage" -type f -name '*.jsonl' -delete 2>/dev/null || true

SOURCE_SHA="unknown"
SOURCE_SHORT_SHA="unknown"
SOURCE_BRANCH="unknown"
SOURCE_COMMITTED_AT=""
SOURCE_DIRTY="unknown"

if git -C "$ROOT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  SOURCE_SHA="$(git -C "$ROOT_DIR" rev-parse HEAD 2>/dev/null || echo unknown)"
  SOURCE_SHORT_SHA="$(git -C "$ROOT_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
  SOURCE_BRANCH="$(git -C "$ROOT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
  SOURCE_COMMITTED_AT="$(git -C "$ROOT_DIR" show -s --format=%cI HEAD 2>/dev/null || echo "")"
  if [[ -n "$(git -C "$ROOT_DIR" status --porcelain -- site logos scripts/build_dist.sh 2>/dev/null || true)" ]]; then
    SOURCE_DIRTY="true"
  else
    SOURCE_DIRTY="false"
  fi
fi

ASSET_VERSION="$(
  find "$DIST_DIR" -type f \
    ! -name 'deploy-info.json' \
    ! -name '*.jsonl' \
    ! -path "$DIST_DIR/storage/*" \
    -exec shasum -a 256 {} + \
    | sort \
    | shasum -a 256 \
    | awk '{print substr($1, 1, 12)}'
)"
BUILT_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

cat > "$DIST_DIR/deploy-info.json" <<EOF
{
  "source_sha": "$SOURCE_SHA",
  "source_short_sha": "$SOURCE_SHORT_SHA",
  "source_branch": "$SOURCE_BRANCH",
  "source_committed_at": "$SOURCE_COMMITTED_AT",
  "source_dirty": $SOURCE_DIRTY,
  "asset_version": "$ASSET_VERSION",
  "built_at": "$BUILT_AT"
}
EOF

ASSET_VERSION="$ASSET_VERSION" find "$DIST_DIR" -name '*.html' -exec perl -0pi -e 's/__ASSET_VERSION__/$ENV{ASSET_VERSION}/g' {} +

echo "Dist gerado em: $DIST_DIR"
echo "Asset version: $ASSET_VERSION"
