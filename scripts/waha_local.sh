#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WAHA_DIR="$ROOT/operations/ai-os/whatsapp/waha"
DOCKER_CONFIG_DIR="$WAHA_DIR/.docker-config"

: "${COLIMA_HOME:=/tmp/rito-colima-home}"
: "${XDG_CACHE_HOME:=/tmp/rito-colima-cache}"
: "${DOCKER_CONFIG:=$DOCKER_CONFIG_DIR}"

if [[ -z "${DOCKER_HOST:-}" && -S "$COLIMA_HOME/docker.sock" ]]; then
  export DOCKER_HOST="unix://$COLIMA_HOME/docker.sock"
fi
export XDG_CACHE_HOME
export DOCKER_CONFIG

if [[ ! -d "$WAHA_DIR" ]]; then
  echo "Diretório do WAHA não encontrado: $WAHA_DIR" >&2
  exit 1
fi

mkdir -p "$WAHA_DIR/.sessions"
mkdir -p "$DOCKER_CONFIG"

if [[ ! -f "$DOCKER_CONFIG/config.json" ]]; then
  cat > "$DOCKER_CONFIG/config.json" <<'EOF'
{
  "cliPluginsExtraDirs": [
    "/opt/homebrew/lib/docker/cli-plugins"
  ]
}
EOF
fi

cd "$WAHA_DIR"
if command -v docker-compose >/dev/null 2>&1; then
  docker-compose "$@"
elif docker compose version >/dev/null 2>&1; then
  docker compose "$@"
else
  echo "Docker Compose não encontrado. Instale docker-compose ou o plugin 'docker compose'." >&2
  exit 1
fi
