from __future__ import annotations

import csv
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WAHA_ENV_FILE = ROOT / "operations" / "ai-os" / "whatsapp" / "waha" / ".env"
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
RUNS_DIR = ROOT / "operations" / "ai-os" / "whatsapp" / "runs"
INBOX_DIR = ROOT / "operations" / "ai-os" / "whatsapp" / "inbox"
RAW_DIR = INBOX_DIR / "raw"
CONVERSATIONS_DIR = INBOX_DIR / "conversations"
PENDING_DIR = INBOX_DIR / "pending"
DEFAULT_BASE_URL = "http://127.0.0.1:3000"
DEFAULT_SESSION = "default"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ensure_dirs() -> None:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
    PENDING_DIR.mkdir(parents=True, exist_ok=True)


def load_local_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if WAHA_ENV_FILE.exists():
        for line in WAHA_ENV_FILE.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            values[key.strip()] = value.strip()
    for key in (
        "WAHA_API_KEY",
        "RITO_WAHA_RECEIVER_URL",
        "RITO_WAHA_WEBHOOK_SECRET",
        "RITO_WAHA_WEBHOOK_TOKEN",
        "RITO_WAHA_WEBHOOK_PORT",
        "RITO_WAHA_WEBHOOK_HOST",
    ):
        if os.getenv(key):
            values[key] = os.getenv(key, "")
    return values


def sanitize_chat_id(chat_id: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_", ".") else "_" for ch in chat_id)
    return safe.strip("_") or "unknown-chat"


def normalize_phone(value: str) -> str:
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        return ""
    if digits.startswith("55"):
        return digits
    if len(digits) in (10, 11):
        return "55" + digits
    return digits


def chat_id_for_phone(value: str) -> str:
    phone = normalize_phone(value)
    return f"{phone}@c.us" if phone else ""


def resolve_chat_id_for_phone(
    value: str,
    *,
    session: str = DEFAULT_SESSION,
    base_url: str = DEFAULT_BASE_URL,
) -> str:
    phone = normalize_phone(value)
    if not phone:
        return ""

    status_code, body = waha_request(
        "GET",
        f"/api/contacts/check-exists?session={urllib.parse.quote(session)}&phone={urllib.parse.quote(phone)}",
        base_url=base_url,
    )
    if status_code == 200 and isinstance(body, dict):
        chat_id = (body.get("chatId") or "").strip()
        if chat_id:
            return chat_id
    return chat_id_for_phone(phone)


def append_jsonl(path: Path, entry: dict) -> None:
    ensure_dirs()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def append_outbound_log(entry: dict) -> None:
    log_file = RUNS_DIR / f"{datetime.now():%Y-%m-%d}-whatsapp-outbound.jsonl"
    append_jsonl(log_file, entry)


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
                "chat_id": chat_id_for_phone(phone),
                "message": (row.get("message", "") or "").strip(),
            }
        )
    return cleaned


def waha_request(
    method: str,
    path: str,
    *,
    data: dict | None = None,
    base_url: str = DEFAULT_BASE_URL,
) -> tuple[int, dict | list | str]:
    env = load_local_env()
    api_key = env.get("WAHA_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(f"WAHA_API_KEY ausente em {WAHA_ENV_FILE}")

    url = f"{base_url.rstrip('/')}{path}"
    headers = {
        "X-Api-Key": api_key,
        "Accept": "application/json",
    }
    payload = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        payload = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(url, data=payload, method=method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type and raw:
                return response.status, json.loads(raw)
            return response.status, raw
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            return exc.code, json.loads(raw)
        except Exception:
            return exc.code, raw
