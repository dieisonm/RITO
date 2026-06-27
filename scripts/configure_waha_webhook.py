from __future__ import annotations

import argparse
import json

from whatsapp_waha_common import DEFAULT_BASE_URL, DEFAULT_SESSION, load_local_env, waha_request


def build_webhook_payload(url: str, events: list[str]) -> dict:
    env = load_local_env()
    secret = env.get("RITO_WAHA_WEBHOOK_SECRET", "").strip()
    token = env.get("RITO_WAHA_WEBHOOK_TOKEN", "").strip()

    webhook: dict = {
        "url": url,
        "events": events,
        "retries": {
            "policy": "constant",
            "delaySeconds": 2,
            "attempts": 15,
        },
    }
    if secret:
        webhook["hmac"] = {"key": secret}
    if token:
        webhook["customHeaders"] = [
            {
                "name": "X-Rito-Webhook-Token",
                "value": token,
            }
        ]
    return webhook


def main() -> int:
    env = load_local_env()
    parser = argparse.ArgumentParser(description="Configurar webhook do WAHA para a RITO.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--session", default=DEFAULT_SESSION)
    parser.add_argument(
        "--receiver-url",
        default=env.get("RITO_WAHA_RECEIVER_URL", "http://webhook:8787/webhook/waha"),
    )
    parser.add_argument(
        "--events",
        default="session.status,message,message.any,message.ack",
        help="Lista separada por vírgula",
    )
    args = parser.parse_args()

    events = [item.strip() for item in args.events.split(",") if item.strip()]
    payload = {
        "name": args.session,
        "config": {
            "webhooks": [
                build_webhook_payload(args.receiver_url, events),
            ]
        },
    }
    status_code, body = waha_request(
        "PUT",
        f"/api/sessions/{args.session}",
        data=payload,
        base_url=args.base_url,
    )
    print(json.dumps({"http_status": status_code, "body": body}, ensure_ascii=False, indent=2))
    return 0 if 200 <= status_code < 300 else 1


if __name__ == "__main__":
    raise SystemExit(main())
