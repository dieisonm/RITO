#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

cp -R "$ROOT_DIR/site/." "$DIST_DIR/"
mkdir -p "$DIST_DIR/assets/brand"
find "$ROOT_DIR/assets/brand/logos/site" -maxdepth 1 -type f ! -name 'README.md' -exec cp {} "$DIST_DIR/assets/brand/" \;
find "$DIST_DIR" -name .DS_Store -delete
find "$DIST_DIR/storage" -type f -name '*.jsonl' -delete 2>/dev/null || true

SOURCE_SHA="unknown"
SOURCE_SHORT_SHA="unknown"
SOURCE_BRANCH="unknown"
SOURCE_COMMITTED_AT=""
SOURCE_DIRTY="unknown"

git_with_timeout() {
  local timeout_seconds="${GIT_METADATA_TIMEOUT_SECONDS:-4}"
  local tmp_file pid watcher status

  tmp_file="$(mktemp)"
  (GIT_OPTIONAL_LOCKS=0 git -C "$ROOT_DIR" "$@" >"$tmp_file" 2>/dev/null) &
  pid="$!"
  (sleep "$timeout_seconds"; kill "$pid" 2>/dev/null || true) &
  watcher="$!"

  if wait "$pid"; then
    status=0
  else
    status="$?"
  fi

  kill "$watcher" 2>/dev/null || true
  wait "$watcher" 2>/dev/null || true

  if [[ "$status" -eq 0 ]]; then
    cat "$tmp_file"
  fi

  rm -f "$tmp_file"
  return "$status"
}

if [[ "${SKIP_GIT_METADATA:-0}" != "1" ]] && git_with_timeout rev-parse --is-inside-work-tree >/dev/null; then
  SOURCE_SHA="$(git_with_timeout rev-parse HEAD || echo unknown)"
  SOURCE_SHORT_SHA="$(git_with_timeout rev-parse --short HEAD || echo unknown)"
  SOURCE_BRANCH="$(git_with_timeout rev-parse --abbrev-ref HEAD || echo unknown)"
  SOURCE_COMMITTED_AT="$(git_with_timeout show -s --format=%cI HEAD || echo "")"
  if [[ -n "$(git_with_timeout status --porcelain -- site scripts/build_dist.sh || true)" ]]; then
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
