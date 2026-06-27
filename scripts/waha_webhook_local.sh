#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_DIR="$ROOT/operations/ai-os/whatsapp/runtime"
PID_FILE="$RUNTIME_DIR/waha-webhook.pid"
LOG_FILE="$RUNTIME_DIR/waha-webhook.log"
HEALTH_URL="http://127.0.0.1:8787/health"

mkdir -p "$RUNTIME_DIR"

healthcheck() {
  curl -sf "$HEALTH_URL" >/dev/null 2>&1
}

status() {
  if healthcheck; then
    if [[ -f "$PID_FILE" ]]; then
      echo "running:$(cat "$PID_FILE")"
    else
      echo "running:untracked"
    fi
    return 0
  fi
  if [[ -f "$PID_FILE" ]]; then
    PID="$(cat "$PID_FILE")"
    if kill -0 "$PID" >/dev/null 2>&1; then
      echo "running:$PID"
      return 0
    fi
  fi
  echo "stopped"
  return 1
}

start() {
  if status >/dev/null 2>&1; then
    echo "Webhook receiver já está rodando."
    exit 0
  fi
  cd "$ROOT"
  nohup python3 -u scripts/whatsapp_waha_webhook.py serve >"$LOG_FILE" 2>&1 </dev/null &
  echo $! > "$PID_FILE"
  for _ in 1 2 3 4 5; do
    sleep 1
    if healthcheck; then
      echo "Webhook receiver iniciado com PID $(cat "$PID_FILE")"
      exit 0
    fi
  done
  echo "Falha ao iniciar webhook receiver. Verifique $LOG_FILE" >&2
  exit 1
}

stop() {
  if [[ ! -f "$PID_FILE" ]]; then
    echo "Webhook receiver não está rodando."
    exit 0
  fi
  PID="$(cat "$PID_FILE")"
  if kill -0 "$PID" >/dev/null 2>&1; then
    kill "$PID"
  fi
  rm -f "$PID_FILE"
  echo "Webhook receiver parado."
}

logs() {
  touch "$LOG_FILE"
  tail -n 100 -f "$LOG_FILE"
}

case "${1:-}" in
  start) start ;;
  stop) stop ;;
  status) status ;;
  logs) logs ;;
  *)
    echo "Uso: $0 {start|stop|status|logs}" >&2
    exit 2
    ;;
esac
