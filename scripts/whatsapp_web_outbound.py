from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import quote

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE_FILE = (
    ROOT
    / "operations"
    / "ai-os"
    / "growth"
    / "prospecting"
    / "territories"
    / "novo-hamburgo-rs"
    / "batches"
    / "2026-04-21-batch-001-whatsapp-manual-queue.csv"
)
SESSION_DIR = ROOT / "operations" / "ai-os" / "whatsapp" / ".session" / "chromium-profile"
RUNS_DIR = ROOT / "operations" / "ai-os" / "whatsapp" / "runs"
WHATSAPP_WEB_URL = "https://web.whatsapp.com/"

READY_SELECTORS = [
    "#pane-side",
    "#side",
    "[data-testid='chat-list']",
    "[data-testid='chat-list-search']",
    "[aria-label='Pesquisar ou começar uma nova conversa']",
    "[aria-label='Search or start new chat']",
    "div[title='Nova conversa']",
    "[contenteditable='true'][role='textbox']",
]
QR_SELECTORS = [
    "canvas[aria-label='Scan me!']",
    "[data-testid='qrcode']",
    "canvas",
]
SEND_SELECTORS = [
    "button[aria-label='Enviar']",
    "button[aria-label='Send']",
    "[data-testid='compose-btn-send']",
    "span[data-icon='send']",
]
ERROR_SELECTORS = [
    "text='O número de telefone compartilhado pela url é inválido.'",
    "text='Phone number shared via url is invalid.'",
    "text='Este número não está no WhatsApp.'",
]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ensure_dirs() -> None:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)


def normalize_phone(value: str) -> str:
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        return ""
    if digits.startswith("55"):
        return digits
    if len(digits) in (10, 11):
        return "55" + digits
    return digits


def load_queue_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    cleaned = []
    for row in rows:
        phone = normalize_phone(row.get("normalized_whatsapp", "") or row.get("public_whatsapp", ""))
        if not phone:
            continue
        cleaned.append(
            {
                "company_id": row.get("company_id", "").strip(),
                "company_name": row.get("company_name", "").strip(),
                "phone": phone,
                "message": (row.get("message", "") or "").strip(),
            }
        )
    return cleaned


def append_log(entry: dict) -> None:
    ensure_dirs()
    log_file = RUNS_DIR / f"{datetime.now():%Y-%m-%d}-whatsapp-outbound.jsonl"
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def first_visible_locator(page, selectors: Iterable[str], timeout_ms: int = 1500):
    for selector in selectors:
        locator = page.locator(selector)
        try:
            locator.first.wait_for(state="visible", timeout=timeout_ms)
            return locator.first
        except Exception:
            continue
    return None


def ensure_logged_in(page, timeout_seconds: int = 300) -> None:
    page.goto(WHATSAPP_WEB_URL, wait_until="domcontentloaded")
    ready = first_visible_locator(page, READY_SELECTORS, timeout_ms=5000)
    if ready:
        return

    print("")
    print("WhatsApp Web ainda não autenticado.")
    print("Escaneie o QR code na janela do navegador para continuar.")
    print("")
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        ready = first_visible_locator(page, READY_SELECTORS, timeout_ms=1500)
        if ready:
            print("Autenticação confirmada.")
            return
        time.sleep(1)

    page.wait_for_timeout(3000)
    ready = first_visible_locator(page, READY_SELECTORS, timeout_ms=1000)
    if ready:
        print("Autenticação confirmada.")
        return

    qr = first_visible_locator(page, QR_SELECTORS, timeout_ms=500)
    if qr is None:
        body_text = ""
        try:
            body_text = page.locator("body").inner_text(timeout=2000)
        except Exception:
            body_text = ""
        lowered = body_text.lower()
        if "whatsapp" in page.title().lower() and (
            "conversa" in lowered
            or "chat" in lowered
            or "mensagens" in lowered
            or "message yourself" in lowered
        ):
            print("Autenticação presumida como válida após carregamento visual do WhatsApp Web.")
            return

    raise RuntimeError("Tempo esgotado aguardando autenticação do WhatsApp Web.")


def launch_context(playwright, headed: bool = True):
    ensure_dirs()
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(SESSION_DIR),
        headless=not headed,
        viewport={"width": 1440, "height": 980},
        args=["--start-maximized"],
    )
    page = context.pages[0] if context.pages else context.new_page()
    return context, page


def build_send_url(phone: str, message: str) -> str:
    return f"https://web.whatsapp.com/send?phone={phone}&text={quote(message)}"


def send_message(page, phone: str, message: str, company_id: str = "", company_name: str = "") -> dict:
    url = build_send_url(phone, message)
    page.goto(url, wait_until="domcontentloaded")

    error_locator = first_visible_locator(page, ERROR_SELECTORS, timeout_ms=2500)
    if error_locator:
        return {
            "timestamp": now_iso(),
            "company_id": company_id,
            "company_name": company_name,
            "phone": phone,
            "status": "error",
            "detail": "numero-invalido-ou-nao-encontrado-no-whatsapp",
        }

    send_button = None
    deadline = time.time() + 30
    while time.time() < deadline:
        send_button = first_visible_locator(page, SEND_SELECTORS, timeout_ms=1500)
        if send_button:
            break
        time.sleep(1)

    if not send_button:
        return {
            "timestamp": now_iso(),
            "company_id": company_id,
            "company_name": company_name,
            "phone": phone,
            "status": "error",
            "detail": "botao-enviar-nao-encontrado",
        }

    send_button.click()
    time.sleep(2)
    return {
        "timestamp": now_iso(),
        "company_id": company_id,
        "company_name": company_name,
        "phone": phone,
        "status": "sent",
        "detail": "click-enviar-executado",
    }


def cmd_auth(args) -> int:
    with sync_playwright() as playwright:
        context, page = launch_context(playwright, headed=True)
        try:
            ensure_logged_in(page, timeout_seconds=args.timeout_seconds)
            print(f"Sessão pronta em: {SESSION_DIR}")
            print("Pode fechar a janela quando quiser. A sessão ficará persistida.")
            return 0
        finally:
            context.close()


def cmd_send_test(args) -> int:
    phone = normalize_phone(args.to)
    if not phone:
        print("Número inválido para teste.", file=sys.stderr)
        return 2
    if args.dry_run:
        print("Dry-run:")
        print(phone)
        print(args.message)
        return 0

    with sync_playwright() as playwright:
        context, page = launch_context(playwright, headed=not args.headless)
        try:
            ensure_logged_in(page, timeout_seconds=args.timeout_seconds)
            result = send_message(page, phone, args.message, company_id="test", company_name="Teste manual")
            append_log(result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["status"] == "sent" else 1
        finally:
            context.close()


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
            print(f"- {row['company_id']} | {row['company_name']} | {row['phone']}")
        return 0

    with sync_playwright() as playwright:
        context, page = launch_context(playwright, headed=not args.headless)
        try:
            ensure_logged_in(page, timeout_seconds=args.timeout_seconds)
            for index, row in enumerate(rows, start=1):
                print(f"[{index}/{len(rows)}] Enviando para {row['company_name']} ({row['phone']})")
                result = send_message(
                    page,
                    row["phone"],
                    row["message"],
                    company_id=row["company_id"],
                    company_name=row["company_name"],
                )
                append_log(result)
                print(json.dumps(result, ensure_ascii=False))
                if args.throttle_seconds > 0 and index < len(rows):
                    time.sleep(args.throttle_seconds)
            return 0
        finally:
            context.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Disparo local de WhatsApp Web para a RITO.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    auth = subparsers.add_parser("auth", help="Abrir o WhatsApp Web para autenticar a sessão.")
    auth.add_argument("--timeout-seconds", type=int, default=300)
    auth.set_defaults(func=cmd_auth)

    send_test = subparsers.add_parser("send-test", help="Enviar mensagem de teste para um número.")
    send_test.add_argument("--to", required=True, help="Número em formato livre. Ex.: 5551999999999")
    send_test.add_argument("--message", required=True, help="Mensagem de teste")
    send_test.add_argument("--timeout-seconds", type=int, default=300)
    send_test.add_argument("--dry-run", action="store_true")
    send_test.add_argument("--headless", action="store_true", help="Executa o envio sem abrir a janela do navegador.")
    send_test.set_defaults(func=cmd_send_test)

    send_batch = subparsers.add_parser("send-batch", help="Enviar lote a partir da fila CSV.")
    send_batch.add_argument("--csv", default=str(DEFAULT_QUEUE_FILE))
    send_batch.add_argument("--company-ids", default="")
    send_batch.add_argument("--timeout-seconds", type=int, default=300)
    send_batch.add_argument("--throttle-seconds", type=int, default=45)
    send_batch.add_argument("--apply", action="store_true")
    send_batch.add_argument("--dry-run", action="store_true")
    send_batch.add_argument("--headless", action="store_true", help="Executa o envio sem abrir a janela do navegador.")
    send_batch.set_defaults(func=cmd_send_batch)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
