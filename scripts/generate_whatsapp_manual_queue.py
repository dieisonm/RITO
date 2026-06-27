from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
BATCH_DIR = (
    ROOT
    / "operations"
    / "ai-os"
    / "growth"
    / "prospecting"
    / "territories"
    / "novo-hamburgo-rs"
    / "batches"
)
CSV_FILE = BATCH_DIR / "2026-04-21-batch-001-pilot.csv"
JSON_FILE = BATCH_DIR / "2026-04-21-batch-001-outreach-data.json"
OUT_CSV = BATCH_DIR / "2026-04-21-batch-001-whatsapp-manual-queue.csv"


def digits_only(value: str) -> str:
    return "".join(ch for ch in value if ch.isdigit())


def normalize_br_phone(value: str) -> str:
    digits = digits_only(value)
    if not digits:
        return ""
    if digits.startswith("55"):
        return digits
    if len(digits) in (10, 11):
        return "55" + digits
    return digits


def load_rows():
    with CSV_FILE.open("r", encoding="utf-8") as f:
        csv_rows = {row["company_id"]: row for row in csv.DictReader(f)}
    with JSON_FILE.open("r", encoding="utf-8") as f:
        json_rows = {row["company_id"]: row for row in json.load(f)}
    return csv_rows, json_rows


def main():
    csv_rows, json_rows = load_rows()
    fieldnames = [
        "company_id",
        "company_name",
        "recommended_channel",
        "public_whatsapp",
        "normalized_whatsapp",
        "message",
        "wa_link",
    ]
    rows = []
    for company_id, extra in json_rows.items():
        channel = extra.get("recommended_channel", "")
        if "whatsapp" not in channel:
            continue
        base = csv_rows.get(company_id, {})
        readiness = (base.get("whatsapp_readiness", "") or "").strip().lower()
        if readiness != "confirmed":
            continue
        raw_phone = (base.get("normalized_whatsapp", "") or base.get("public_whatsapp", "")).strip()
        phone = normalize_br_phone(raw_phone)
        if not phone:
            continue
        message = extra.get("whatsapp_body", "").strip()
        wa_link = f"https://wa.me/{phone}?text={quote(message)}" if phone and message else ""
        rows.append(
            {
                "company_id": company_id,
                "company_name": base.get("company_name", company_id),
                "recommended_channel": channel,
                "public_whatsapp": base.get("public_whatsapp", ""),
                "normalized_whatsapp": phone,
                "message": message,
                "wa_link": wa_link,
            }
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(OUT_CSV)


if __name__ == "__main__":
    main()
