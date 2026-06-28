from __future__ import annotations

import argparse
import hmac
import json
from datetime import datetime
from hashlib import sha512
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from whatsapp_waha_common import (
    CONVERSATIONS_DIR,
    DEFAULT_SESSION,
    INBOX_DIR,
    PENDING_DIR,
    RAW_DIR,
    append_jsonl,
    ensure_dirs,
    load_local_env,
    now_iso,
    sanitize_chat_id,
)


SESSION_EVENTS_FILE = INBOX_DIR / "session-events.jsonl"
PENDING_REPLIES_FILE = PENDING_DIR / "pending-replies.jsonl"


def verify_hmac(raw_body: bytes, provided_hmac: str, secret: str) -> bool:
    computed = hmac.new(secret.encode("utf-8"), raw_body, sha512).hexdigest()
    return hmac.compare_digest(computed, provided_hmac)


def pending_reply_exists(message_id: str) -> bool:
    if not message_id or not PENDING_REPLIES_FILE.exists():
        return False
    for line in PENDING_REPLIES_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if item.get("message_id") == message_id:
            return True
    return False


def should_enqueue_pending(message_entry: dict) -> bool:
    if message_entry["from_me"]:
        return False

    body = (message_entry.get("body") or "").strip()
    msg_type = (message_entry.get("type") or "").strip().lower()

    if not body:
        return False
    if msg_type in {"biz_content_placeholder", "e2e_notification", "notification_template"}:
        return False
    if pending_reply_exists(message_entry.get("message_id", "")):
        return False
    return True


def normalize_event(payload: dict) -> tuple[dict, dict | None]:
    event = payload.get("event", "")
    session = payload.get("session", "")
    event_payload = payload.get("payload", {}) or {}
    raw_data = event_payload.get("_data", {}) or {}
    chat_id = (
        event_payload.get("chatId")
        or event_payload.get("from")
        or event_payload.get("to")
        or "unknown-chat"
    )
    message_entry = {
        "received_at": now_iso(),
        "event": event,
        "session": session,
        "chat_id": chat_id,
        "message_id": event_payload.get("id") or event_payload.get("_data", {}).get("id", {}).get("_serialized"),
        "timestamp": event_payload.get("timestamp"),
        "from": event_payload.get("from"),
        "to": event_payload.get("to"),
        "from_me": bool(event_payload.get("fromMe", False)),
        "ack": event_payload.get("ack"),
        "body": event_payload.get("body"),
        "type": event_payload.get("type") or raw_data.get("type"),
        "has_media": bool(event_payload.get("hasMedia", False)),
        "media": event_payload.get("media"),
        "raw_payload": event_payload,
    }

    pending_entry = None
    if event in {"message", "message.any"} and should_enqueue_pending(message_entry):
        pending_entry = {
            "received_at": message_entry["received_at"],
            "status": "new",
            "session": session or DEFAULT_SESSION,
            "chat_id": chat_id,
            "message_id": message_entry["message_id"],
            "from": message_entry["from"],
            "body": message_entry["body"],
            "type": message_entry["type"],
            "has_media": message_entry["has_media"],
        }
    return message_entry, pending_entry


class WahaWebhookHandler(BaseHTTPRequestHandler):
    server_version = "RitoWahaWebhook/1.0"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._json_response(200, {"status": "ok", "time": now_iso()})
            return
        self._json_response(404, {"error": "not-found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/webhook/waha":
            self._json_response(404, {"error": "not-found"})
            return

        content_length = int(self.headers.get("Content-Length", "0") or "0")
        raw_body = self.rfile.read(content_length)
        env = load_local_env()
        expected_token = env.get("RITO_WAHA_WEBHOOK_TOKEN", "")
        expected_secret = env.get("RITO_WAHA_WEBHOOK_SECRET", "")

        if expected_token:
            provided_token = self.headers.get("X-Rito-Webhook-Token", "")
            if provided_token != expected_token:
                self._json_response(401, {"error": "invalid-token"})
                return

        provided_hmac = self.headers.get("X-Webhook-Hmac", "")
        algorithm = self.headers.get("X-Webhook-Hmac-Algorithm", "")
        if expected_secret and provided_hmac:
            if algorithm.lower() != "sha512":
                self._json_response(401, {"error": "invalid-hmac-algorithm"})
                return
            if not verify_hmac(raw_body, provided_hmac, expected_secret):
                self._json_response(401, {"error": "invalid-hmac"})
                return

        try:
            body = json.loads(raw_body.decode("utf-8"))
        except Exception as exc:
            self._json_response(400, {"error": "invalid-json", "detail": str(exc)})
            return

        ensure_dirs()
        raw_file = RAW_DIR / f"{datetime.now():%Y-%m-%d}-waha-events.jsonl"
        append_jsonl(
            raw_file,
            {
                "received_at": now_iso(),
                "headers": {
                    "X-Webhook-Request-Id": self.headers.get("X-Webhook-Request-Id"),
                    "X-Webhook-Timestamp": self.headers.get("X-Webhook-Timestamp"),
                    "X-Webhook-Hmac-Algorithm": self.headers.get("X-Webhook-Hmac-Algorithm"),
                    "X-Rito-Webhook-Token": self.headers.get("X-Rito-Webhook-Token"),
                },
                "body": body,
            },
        )

        event = body.get("event", "")
        if event == "session.status":
            append_jsonl(
                SESSION_EVENTS_FILE,
                {
                    "received_at": now_iso(),
                    "session": body.get("session"),
                    "payload": body.get("payload"),
                },
            )
        else:
            message_entry, pending_entry = normalize_event(body)
            convo_file = CONVERSATIONS_DIR / f"{sanitize_chat_id(message_entry['chat_id'])}.jsonl"
            append_jsonl(convo_file, message_entry)
            if pending_entry:
                append_jsonl(PENDING_REPLIES_FILE, pending_entry)

        self._json_response(200, {"status": "ok"})

    def log_message(self, format: str, *args) -> None:
        return

    def _json_response(self, status_code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def cmd_serve(args) -> int:
    ensure_dirs()
    server = ThreadingHTTPServer((args.host, args.port), WahaWebhookHandler)
    print(f"Webhook WAHA ouvindo em http://{args.host}:{args.port}/webhook/waha")
    print(f"Health check: http://{args.host}:{args.port}/health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Webhook receiver local do WAHA para a RITO.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve = subparsers.add_parser("serve", help="Iniciar o servidor local de webhook.")
    serve.add_argument("--host", default=load_local_env().get("RITO_WAHA_WEBHOOK_HOST", "0.0.0.0"))
    serve.add_argument("--port", type=int, default=int(load_local_env().get("RITO_WAHA_WEBHOOK_PORT", "8787")))
    serve.set_defaults(func=cmd_serve)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
