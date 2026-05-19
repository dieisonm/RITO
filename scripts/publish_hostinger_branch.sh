#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE_URL="$(git -C "$ROOT_DIR" remote get-url origin)"
HOSTINGER_BRANCH="${HOSTINGER_BRANCH:-hostinger}"
SOURCE_SHA="$(git -C "$ROOT_DIR" rev-parse HEAD)"
TMP_DIR="$(mktemp -d)"
PUSH_URL="$REMOTE_URL"

if [[ -n "${GITHUB_TOKEN:-}" && -n "${GITHUB_REPOSITORY:-}" ]]; then
  PUSH_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
fi

cleanup() {
  rm -rf "$TMP_DIR"
}

trap cleanup EXIT

bash "$ROOT_DIR/scripts/build_dist.sh"
python3 "$ROOT_DIR/scripts/validate_dist.py" --dist "$ROOT_DIR/dist"

if git ls-remote --exit-code --heads "$REMOTE_URL" "$HOSTINGER_BRANCH" >/dev/null 2>&1; then
  git clone --branch "$HOSTINGER_BRANCH" --single-branch "$REMOTE_URL" "$TMP_DIR" >/dev/null 2>&1
else
  git -C "$TMP_DIR" init -b "$HOSTINGER_BRANCH" >/dev/null
fi

git -C "$TMP_DIR" config user.name "${GIT_AUTHOR_NAME:-github-actions[bot]}"
git -C "$TMP_DIR" config user.email "${GIT_AUTHOR_EMAIL:-41898282+github-actions[bot]@users.noreply.github.com}"
git -C "$TMP_DIR" remote remove origin >/dev/null 2>&1 || true
git -C "$TMP_DIR" remote add origin "$PUSH_URL"

find "$TMP_DIR" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -R "$ROOT_DIR/dist/." "$TMP_DIR/"

git -C "$TMP_DIR" add --all

if git -C "$TMP_DIR" diff --cached --quiet; then
  echo "Branch $HOSTINGER_BRANCH ja esta atualizada."
  exit 0
fi

git -C "$TMP_DIR" commit -m "Deploy Hostinger site from ${SOURCE_SHA}" >/dev/null
git -C "$TMP_DIR" push origin "$HOSTINGER_BRANCH"

echo "Branch $HOSTINGER_BRANCH publicada com sucesso."
echo "Proximo passo: rode python3 scripts/verify_live_site.py para confirmar se a Hostinger aplicou o deploy."
