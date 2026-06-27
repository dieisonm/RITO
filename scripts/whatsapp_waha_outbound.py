from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from whatsapp_waha_common import (
    DEFAULT_BASE_URL,
    DEFAULT_QUEUE_FILE,
    DEFAULT_SESSION,
    append_outbound_log,
    load_queue_rows,
    now_iso,
    normalize_phone,
    resolve_chat_id_for_phone,
    waha_request,
)


def send_text(
    session: str,
    chat_id: str,
    text: str,
    *,
    reply_to: str | None = None,
    base_url: str = DEFAULT_BASE_URL,
) -> dict:
    payload = {
        "session": session,
        "chatId": chat_id,
        "text": text,
    }
    if reply_to:
        payload["reply_to"] = reply_to
    status_code, body = waha_request(
        "POST",
        "/api/sendText",
        data=payload,
        base_url=base_url,
    )
    ok = 200 <= status_code < 300
    return {
        "timestamp": now_iso(),
        "status": "sent" if ok else "error",
        "http_status": status_code,
        "response": body,
    }


def send_seen(session: str, chat_id: str, *, message_ids: list[str] | None = None, base_url: str = DEFAULT_BASE_URL) -> dict:
    payload = {
        "session": session,
        "chatId": chat_id,
    }
    if message_ids:
        payload["messageIds"] = message_ids
    status_code, body = waha_request(
        "POST",
        "/api/sendSeen",
        data=payload,
        base_url=base_url,
    )
    ok = 200 <= status_code < 300
    return {
        "timestamp": now_iso(),
        "status": "seen" if ok else "error",
        "http_status": status_code,
        "response": body,
    }


def cmd_session_status(args) -> int:
    status_code, body = waha_request("GET", f"/api/sessions/{args.session}", base_url=args.base_url)
    print(json.dumps({"http_status": status_code, "body": body}, ensure_ascii=False, indent=2))
    return 0 if status_code == 200 else 1


def cmd_session_start(args) -> int:
    status_code, body = waha_request(
        "POST",
        f"/api/sessions/{args.session}/start",
        data={},
        base_url=args.base_url,
    )
    print(json.dumps({"http_status": status_code, "body": body}, ensure_ascii=False, indent=2))
    return 0 if status_code in (200, 201) else 1


def cmd_send_test(args) -> int:
    phone = normalize_phone(args.to)
    if not phone:
        print("Número inválido para teste.", file=sys.stderr)
        return 2
    chat_id = resolve_chat_id_for_phone(phone, session=args.session, base_url=args.base_url)
    if args.dry_run or not args.apply:
        print("Dry-run:")
        print(json.dumps({"phone": phone, "chat_id": chat_id, "message": args.message}, ensure_ascii=False, indent=2))
        return 0

    result = send_text(args.session, chat_id, args.message, base_url=args.base_url)
    result.update(
        {
            "company_id": "test",
            "company_name": "Teste manual",
            "phone": phone,
            "chat_id": chat_id,
            "detail": "waha-sendText",
        }
    )
    append_outbound_log(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "sent" else 1


def cmd_send_batch(args) -> int:
    csv_path = Path(args.csv).resolve()
    rows = load_queue_rows(csv_path)
    if args.company_ids:
        allowed = {item.strip() for item in args.company_ids.split(",") if item.strip()}
        rows = [row for row in rows if row["company_id"] in allowed]

    if not rows:
        print("Nenhuma linha elegível para envio.")
        return 0

    if args.dry_run or not args.apply:
        print(f"Dry-run de {len(rows)} mensagens.")
        for row in rows:
            print(f"- {row['company_id']} | {row['company_name']} | {row['chat_id']}")
        return 0

    exit_code = 0
    for index, row in enumerate(rows, start=1):
        resolved_chat_id = resolve_chat_id_for_phone(row["phone"], session=args.session, base_url=args.base_url)
        print(f"[{index}/{len(rows)}] Enviando para {row['company_name']} ({resolved_chat_id})")
        result = send_text(args.session, resolved_chat_id, row["message"], base_url=args.base_url)
        result.update(
            {
                "company_id": row["company_id"],
                "company_name": row["company_name"],
                "phone": row["phone"],
                "chat_id": resolved_chat_id,
                "detail": "waha-sendText",
            }
        )
        append_outbound_log(result)
        print(json.dumps(result, ensure_ascii=False))
        if result["status"] != "sent":
            exit_code = 1
        if args.throttle_seconds > 0 and index < len(rows):
            time.sleep(args.throttle_seconds)
    return exit_code


def cmd_send_reply(args) -> int:
    result = send_text(
        args.session,
        args.chat_id,
        args.message,
        reply_to=args.reply_to or None,
        base_url=args.base_url,
    )
    result.update(
        {
            "chat_id": args.chat_id,
            "detail": "waha-sendText-reply" if args.reply_to else "waha-sendText",
            "reply_to": args.reply_to or None,
        }
    )
    append_outbound_log(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "sent" else 1


def cmd_send_seen(args) -> int:
    message_ids = [item.strip() for item in args.message_ids.split(",") if item.strip()] if args.message_ids else None
    result = send_seen(args.session, args.chat_id, message_ids=message_ids, base_url=args.base_url)
    result.update(
        {
            "chat_id": args.chat_id,
            "detail": "waha-sendSeen",
            "message_ids": message_ids or [],
        }
    )
    append_outbound_log(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "seen" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Disparo local de WhatsApp via WAHA para a RITO.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--session", default=DEFAULT_SESSION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    session_status = subparsers.add_parser("session-status", help="Mostrar o estado da sessão no WAHA.")
    session_status.set_defaults(func=cmd_session_status)

    session_start = subparsers.add_parser("session-start", help="Iniciar a sessão no WAHA.")
    session_start.set_defaults(func=cmd_session_start)

    send_test = subparsers.add_parser("send-test", help="Enviar mensagem de teste para um número.")
    send_test.add_argument("--to", required=True, help="Número em formato livre. Ex.: 5551999999999")
    send_test.add_argument("--message", required=True, help="Mensagem de teste")
    send_test.add_argument("--apply", action="store_true")
    send_test.add_argument("--dry-run", action="store_true")
    send_test.set_defaults(func=cmd_send_test)

    send_batch = subparsers.add_parser("send-batch", help="Enviar lote a partir da fila CSV.")
    send_batch.add_argument("--csv", default=str(DEFAULT_QUEUE_FILE))
    send_batch.add_argument("--company-ids", default="")
    send_batch.add_argument("--throttle-seconds", type=int, default=45)
    send_batch.add_argument("--apply", action="store_true")
    send_batch.add_argument("--dry-run", action="store_true")
    send_batch.set_defaults(func=cmd_send_batch)

    send_reply = subparsers.add_parser("send-reply", help="Responder uma conversa já existente.")
    send_reply.add_argument("--chat-id", required=True, help="Ex.: 5551999999999@c.us")
    send_reply.add_argument("--message", required=True)
    send_reply.add_argument("--reply-to", default="", help="ID da mensagem para responder, se quiser encadear.")
    send_reply.set_defaults(func=cmd_send_reply)

    send_seen_cmd = subparsers.add_parser("send-seen", help="Marcar mensagens como lidas em um chat.")
    send_seen_cmd.add_argument("--chat-id", required=True, help="Ex.: 5551999999999@c.us")
    send_seen_cmd.add_argument("--message-ids", default="", help="IDs separados por vírgula; opcional.")
    send_seen_cmd.set_defaults(func=cmd_send_seen)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
