#!/usr/bin/env python3
"""
Envia um e-mail pela caixa da RITO na Hostinger (contato@ ou comercial@), com cópia na pasta Enviados.

Simulação por padrão: mostra o e-mail exatamente como sairá. Só envia com --apply, depois da aprovação
do Dieison para aquele texto. Para responder a uma mensagem da caixa, use --responder-id <id IMAP>
(o assunto ganha "Re:" e a resposta entra na mesma conversa).

Uso:
  python3 -I scripts/enviar_email.py --account comercial --para cliente@x.com --assunto "..." --texto arquivo.txt
  python3 -I scripts/enviar_email.py --account contato --responder-id 123 --texto resposta.txt --apply
"""

from __future__ import annotations

import argparse
import email
import imaplib
import smtplib
import ssl
import sys
import time
from email.message import EmailMessage
from email.utils import formataddr, make_msgid, parseaddr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from read_hostinger_inbox import decode_mime_header, load_smtp_php_config  # noqa: E402

SMTP_HOST, SMTP_PORT = "smtp.hostinger.com", 465
SIGNATURE = "\n\n--\nRITO Sistemas · ritosistemas.com\nWhatsApp (51) 99659-9049 · Novo Hamburgo/RS"


def original_headers(config, msg_id: str) -> dict:
    conn = imaplib.IMAP4_SSL(config["imap_host"], int(config["imap_port"]))
    try:
        conn.login(config["username"], config["password"])
        conn.select("INBOX", readonly=True)
        status, data = conn.fetch(msg_id.encode(), "(BODY.PEEK[HEADER])")
        if status != "OK" or not data or not isinstance(data[0], tuple):
            raise RuntimeError(f"Mensagem {msg_id} não encontrada")
        head = email.message_from_bytes(data[0][1])
        return {"from": head.get("Reply-To") or head.get("From", ""), "subject": decode_mime_header(head.get("Subject", "")),
                "message_id": head.get("Message-ID", ""), "references": head.get("References", "")}
    finally:
        conn.logout()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", default="comercial", choices=["contato", "comercial"])
    parser.add_argument("--para", default="", help="destinatário (obrigatório sem --responder-id)")
    parser.add_argument("--assunto", default="")
    parser.add_argument("--texto", required=True, help="arquivo .txt com o corpo do e-mail")
    parser.add_argument("--responder-id", default="", help="id IMAP da mensagem a responder")
    parser.add_argument("--sem-assinatura", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    config = load_smtp_php_config(args.account)
    body = Path(args.texto).read_text(encoding="utf-8").strip() + ("" if args.sem_assinatura else SIGNATURE)
    msg = EmailMessage()
    msg["From"] = formataddr(("RITO Sistemas", config["username"]))
    if args.responder_id:
        orig = original_headers(config, args.responder_id)
        msg["To"] = orig["from"]
        subject = orig["subject"]
        msg["Subject"] = subject if subject.lower().startswith("re:") else f"Re: {subject}"
        if orig["message_id"]:
            msg["In-Reply-To"] = orig["message_id"]
            msg["References"] = (orig["references"] + " " + orig["message_id"]).strip()
    else:
        if not args.para or not args.assunto:
            parser.error("--para e --assunto são obrigatórios sem --responder-id")
        msg["To"] = args.para
        msg["Subject"] = args.assunto
    msg["Message-ID"] = make_msgid(domain="ritosistemas.com")
    msg.set_content(body)

    print("=" * 60)
    print(f"De: {msg['From']}\nPara: {msg['To']}\nAssunto: {msg['Subject']}\n")
    print(body)
    print("=" * 60)
    if not parseaddr(str(msg["To"]))[1]:
        raise SystemExit("Destinatário inválido.")
    if not args.apply:
        print("Simulação: nada foi enviado. Use --apply depois da aprovação.")
        return 0

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ssl.create_default_context()) as smtp:
        smtp.login(config["username"], config["password"])
        smtp.send_message(msg)
    try:
        conn = imaplib.IMAP4_SSL(config["imap_host"], int(config["imap_port"]))
        conn.login(config["username"], config["password"])
        for folder in ("INBOX.Sent", "Sent", "INBOX.Enviados"):
            if conn.select(folder)[0] == "OK":
                conn.append(folder, "\\Seen", imaplib.Time2Internaldate(time.time()), msg.as_bytes())
                break
        conn.logout()
    except Exception as exc:  # cópia em Enviados é conveniência; o envio já aconteceu
        print(f"Aviso: enviado, mas sem cópia em Enviados ({exc})")
    print(f"Enviado para {msg['To']}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
