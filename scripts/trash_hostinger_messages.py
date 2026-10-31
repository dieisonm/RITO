#!/usr/bin/env python3
"""
Move Hostinger mailbox messages to Trash (recoverable), selected by IMAP search criteria.

Dry-run by default: prints what would move. Use --apply to move.
Examples:
  python3 -I scripts/trash_hostinger_messages.py --account contato --body Samuelgop --body CarlosIcope --subject "Novo pedido de orçamento"
  python3 -I scripts/trash_hostinger_messages.py --account contato --from roberson@rysolucoes.com.br --apply
"""

from __future__ import annotations

import argparse
import imaplib
import re
import sys
from email.header import decode_header
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from read_hostinger_inbox import load_smtp_php_config  # noqa: E402


def quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def find_trash(conn: imaplib.IMAP4_SSL) -> str:
    status, folders = conn.list()
    if status != "OK":
        raise RuntimeError("Unable to list folders")
    names = []
    for raw in folders or []:
        line = raw.decode("utf-8", errors="replace")
        match = re.search(r'\(([^)]*)\) "[^"]*" "?([^"]+)"?$', line)
        if not match:
            continue
        flags, name = match.group(1), match.group(2)
        if "\\Trash" in flags:
            return name
        names.append(name)
    for candidate in ("INBOX.Trash", "Trash", "Lixeira", "INBOX.Lixeira"):
        if candidate in names:
            return candidate
    raise RuntimeError(f"Trash folder not found. Folders: {names}")


def subject_of(conn: imaplib.IMAP4_SSL, uid: bytes) -> str:
    status, data = conn.uid("FETCH", uid, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM)])")
    if status != "OK" or not data or not isinstance(data[0], tuple):
        return ""
    text = data[0][1].decode("utf-8", errors="replace")
    parts = []
    for line in text.splitlines():
        for chunk, charset in decode_header(line):
            parts.append(chunk.decode(charset or "utf-8", errors="replace") if isinstance(chunk, bytes) else chunk)
    return " ".join(" ".join(parts).split())[:120]


def main() -> int:
    parser = argparse.ArgumentParser(description="Move Hostinger messages to Trash.")
    parser.add_argument("--account", default="contato", choices=["contato", "comercial"])
    parser.add_argument("--mailbox", default="INBOX")
    parser.add_argument("--subject", default="", help="Subject must contain this text (combined with each --body).")
    parser.add_argument("--body", action="append", default=[], help="Body contains this text. Repeatable (OR).")
    parser.add_argument("--from", dest="senders", action="append", default=[], help="Sender address. Repeatable (OR).")
    parser.add_argument("--apply", action="store_true", help="Actually move. Without it, only lists.")
    args = parser.parse_args()
    if not (args.body or args.senders):
        parser.error("Give at least one --body or --from")

    config = load_smtp_php_config(args.account)
    conn = imaplib.IMAP4_SSL(config["imap_host"], int(config["imap_port"]))
    conn.login(config["username"], config["password"])
    try:
        trash = find_trash(conn)
        status, _ = conn.select(args.mailbox, readonly=not args.apply)
        if status != "OK":
            raise RuntimeError(f"Unable to select {args.mailbox}")
        searches = []
        for text in args.body:
            crit = f"BODY {quote(text)}"
            if args.subject:
                crit = f"SUBJECT {quote(args.subject)} {crit}"
            searches.append(crit)
        searches += [f"FROM {quote(addr)}" for addr in args.senders]
        uids: list[bytes] = []
        for crit in searches:
            conn.literal = None
            status, data = conn.uid("SEARCH", "CHARSET", "UTF-8", crit.encode("utf-8"))
            if status != "OK":
                raise RuntimeError(f"Search failed: {crit}")
            for uid in (data[0] or b"").split():
                if uid not in uids:
                    uids.append(uid)
        print(f"{config['username']} {args.mailbox}: {len(uids)} message(s) -> {trash}")
        for uid in uids:
            print(f"  {uid.decode()} | {subject_of(conn, uid)}")
        if not args.apply or not uids:
            print("Dry-run: nothing moved." if not args.apply else "Nothing to move.")
            return 0
        uid_set = b",".join(uids)
        status, _ = conn.uid("MOVE", uid_set, quote(trash))
        if status != "OK":
            conn.uid("COPY", uid_set, quote(trash))
            conn.uid("STORE", uid_set, "+FLAGS", "(\\Deleted)")
            conn.expunge()
        print(f"Moved {len(uids)} message(s) to {trash}.")
    finally:
        try:
            conn.logout()
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
