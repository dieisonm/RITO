#!/usr/bin/env python3
"""
Read Hostinger inbox via IMAP using the same mailbox credentials as the SMTP setup.
"""

from __future__ import annotations

import argparse
import email
import imaplib
import json
import re
import sys
from datetime import datetime, timezone
from email.header import decode_header
from email.message import Message
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


ROOT = Path(__file__).resolve().parents[1]
SMTP_CONFIG_PATH = ROOT / "rito-smtp.php"


def load_smtp_php_config() -> Dict[str, str]:
    text = SMTP_CONFIG_PATH.read_text(encoding="utf-8")

    def pick(key: str) -> str:
        pattern = rf"'{re.escape(key)}'\s*=>\s*'([^']*)'"
        match = re.search(pattern, text)
        if not match:
            raise RuntimeError(f"Config key not found in rito-smtp.php: {key}")
        return match.group(1)

    return {
        "username": pick("username"),
        "password": pick("password"),
        "imap_host": "imap.hostinger.com",
        "imap_port": "993",
    }


def decode_mime_header(value: Optional[str]) -> str:
    if not value:
        return ""
    parts = []
    for chunk, charset in decode_header(value):
        if isinstance(chunk, bytes):
            encoding = (charset or "utf-8").strip().lower()
            if encoding in {"unknown-8bit", "unknown", "x-unknown"}:
                encoding = "utf-8"
            try:
                parts.append(chunk.decode(encoding, errors="replace"))
            except LookupError:
                parts.append(chunk.decode("utf-8", errors="replace"))
        else:
            parts.append(chunk)
    return "".join(parts).strip()


def extract_text_body(message: Message) -> str:
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            disposition = (part.get("Content-Disposition") or "").lower()
            if content_type == "text/plain" and "attachment" not in disposition:
                payload = part.get_payload(decode=True)
                if payload is None:
                    continue
                charset = (part.get_content_charset() or "utf-8").strip().lower()
                if charset in {"unknown-8bit", "unknown", "x-unknown"}:
                    charset = "utf-8"
                try:
                    return payload.decode(charset, errors="replace").strip()
                except LookupError:
                    return payload.decode("utf-8", errors="replace").strip()
        return ""

    payload = message.get_payload(decode=True)
    if payload is None:
        return ""
    charset = (message.get_content_charset() or "utf-8").strip().lower()
    if charset in {"unknown-8bit", "unknown", "x-unknown"}:
        charset = "utf-8"
    try:
        return payload.decode(charset, errors="replace").strip()
    except LookupError:
        return payload.decode("utf-8", errors="replace").strip()


def compact_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def body_preview(message: Message, limit: int) -> str:
    preview = compact_whitespace(extract_text_body(message))
    if len(preview) <= limit:
        return preview
    return preview[: limit - 1].rstrip() + "…"


def parse_internal_date(raw_date: Any) -> str:
    if isinstance(raw_date, bytes):
        raw_date = raw_date.decode("utf-8", errors="replace")
    if not raw_date:
        return ""
    cleaned = str(raw_date).strip('"')
    try:
        dt = datetime.strptime(cleaned, "%d-%b-%Y %H:%M:%S %z")
        return dt.astimezone(timezone.utc).isoformat()
    except ValueError:
        return cleaned


def fetch_ids(conn: imaplib.IMAP4_SSL, mailbox: str, unseen_only: bool) -> List[bytes]:
    status, _ = conn.select(mailbox, readonly=True)
    if status != "OK":
        raise RuntimeError(f"Unable to select mailbox: {mailbox}")
    criterion = "UNSEEN" if unseen_only else "ALL"
    status, data = conn.search(None, criterion)
    if status != "OK":
        raise RuntimeError(f"Search failed for {criterion}")
    if not data or not data[0]:
        return []
    ids = data[0].split()
    ids.reverse()
    return ids


def fetch_messages(
    conn: imaplib.IMAP4_SSL,
    ids: Sequence[bytes],
    limit: int,
    preview_limit: int,
    include_body: bool,
) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for msg_id in ids[:limit]:
        status, data = conn.fetch(msg_id, "(RFC822 INTERNALDATE)")
        if status != "OK" or not data:
            continue
        metadata = None
        raw_email = None
        for item in data:
            if not isinstance(item, tuple):
                continue
            metadata = item[0]
            raw_email = item[1]
            break
        if raw_email is None:
            continue
        message = email.message_from_bytes(raw_email)
        metadata_text = metadata.decode("utf-8", errors="replace") if metadata else ""
        internal_match = re.search(r'INTERNALDATE "([^"]+)"', metadata_text)
        internal_date = parse_internal_date(internal_match.group(1) if internal_match else "")
        records.append(
            {
                "id": msg_id.decode("utf-8", errors="replace"),
                "internal_date": internal_date,
                "from": decode_mime_header(message.get("From")),
                "to": decode_mime_header(message.get("To")),
                "subject": decode_mime_header(message.get("Subject")),
                "date_header": decode_mime_header(message.get("Date")),
                "message_id": decode_mime_header(message.get("Message-ID")),
                "preview": body_preview(message, preview_limit),
                **({"body": extract_text_body(message)} if include_body else {}),
            }
        )
    return records


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Read Hostinger inbox via IMAP.")
    parser.add_argument("--mailbox", default="INBOX", help="Mailbox to inspect. Default: INBOX")
    parser.add_argument("--limit", type=int, default=10, help="Max messages to return. Default: 10")
    parser.add_argument("--unseen", action="store_true", help="Only fetch unread messages.")
    parser.add_argument(
        "--preview-limit",
        type=int,
        default=220,
        help="Body preview max characters. Default: 220",
    )
    parser.add_argument(
        "--ids",
        default="",
        help="Lista de IDs IMAP separados por vírgula para buscar mensagens específicas.",
    )
    parser.add_argument(
        "--include-body",
        action="store_true",
        help="Inclui o corpo de texto completo da mensagem no JSON de saída.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)

    config = load_smtp_php_config()
    conn = imaplib.IMAP4_SSL(config["imap_host"], int(config["imap_port"]))
    try:
        conn.login(config["username"], config["password"])
        status, _ = conn.select(args.mailbox, readonly=True)
        if status != "OK":
            raise RuntimeError(f"Unable to select mailbox: {args.mailbox}")
        if args.ids.strip():
            message_ids = [item.strip().encode("utf-8") for item in args.ids.split(",") if item.strip()]
        else:
            message_ids = fetch_ids(conn, args.mailbox, args.unseen)
        messages = fetch_messages(conn, message_ids, args.limit, args.preview_limit, args.include_body)
    finally:
        try:
            conn.logout()
        except Exception:
            pass

    payload = {
        "mailbox": args.mailbox,
        "unseen_only": args.unseen,
        "returned": len(messages),
        "messages": messages,
    }
    if args.pretty:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    else:
        json.dump(payload, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
