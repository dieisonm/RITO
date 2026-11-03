#!/usr/bin/env python3
"""
Consolida a base de prospecção (lotes de outbound de Novo Hamburgo) em uma planilha única.

Fontes (somente leitura): CSVs e JSONs dos lotes, monitores de resposta (.md), resultados de envio
de e-mail (.md), logs de envio do WhatsApp (ops/ai-os/whatsapp/runs) e conversas recebidas
(ops/ai-os/whatsapp/inbox/conversations).

Saída: ops/ai-os/growth/prospecting/base-prospeccao-rito.xlsx (abas Empresas, Contatos, Lotes, Dicionário).
Uso: python3 -I scripts/build_prospect_base.py [--batches DIR] [--out ARQUIVO]
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "ops" / "ai-os"
DEFAULT_BATCHES = ROOT / "_arquivo" / "2026-05-lotes-outbound" / "batches"
DEFAULT_OUT = OPS / "growth" / "prospecting" / "base-prospeccao-rito.xlsx"

COMPANY_FIELDS = [
    "company_id", "company_name", "segment", "city", "state", "website_url", "website_signal", "instagram_url",
    "other_channels", "public_email", "public_phone", "public_whatsapp", "normalized_whatsapp",
    "business_summary", "digital_presence_stage", "observed_signals", "suggested_offer_primary",
    "suggested_offer_secondary", "offer_rationale", "outreach_angle", "confidence_business",
    "confidence_contact", "confidence_offer_fit", "source_primary_url", "source_secondary_urls",
    "source_risk_note", "do_not_contact", "opt_out_received", "last_verified_at",
    "whatsapp_readiness", "primary_contact_channel",
]
CLOSED = {"crust smash": "encerrado: conversou em maio e não quis seguir"}
# Respostas humanas identificadas ao consolidar (2026-10-31), ausentes dos monitores antigos.
HUMAN_REPLIES = {
    "crust smash": ("resposta humana", "perguntou sobre sistema de gestão de pedidos para delivery; o Dieison respondeu e conversou, a empresa não retornou e não quis seguir"),
    "jonas rodas e pneus": ("resposta humana", "respondeu e avisou que o link não abriu"),
    "trate clinica medica": ("resposta humana", "agradeceu depois da réplica curta"),
    "medklinik": ("resposta humana", "disse que não tem interesse no momento"),
}
STATUS_RANK = {"cliente": 7, "sem interesse": 6, "resposta humana": 5, "autoresposta": 4, "bounce": 3, "erro no envio": 2, "enviado": 1, "não contatado": 0}


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def batch_of(filename: str) -> tuple[str, str]:
    if filename == "empresas-novas.csv":
        return "", "prospeccao-continua"
    date = filename[:10]
    match = re.search(r"batch-(\d{3})", filename)
    return date, (f"lote-{match.group(1)}" if match else "fila-whatsapp-sem-site")


def read_csv(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def monitor_mentions(md_path: str) -> dict[str, set[str]]:
    """Nomes entre crases agrupados pela seção do monitor (bounce, autoresposta, resposta humana)."""
    found: dict[str, set[str]] = defaultdict(set)
    section = ""
    for line in open(md_path, encoding="utf-8"):
        if line.startswith("#"):
            section = norm(line)
            continue
        names = re.findall(r"`([^`]+)`", line)
        if not names or not line.lstrip().startswith("-"):
            continue
        name = names[0]
        if "@" in name or name.isdigit():
            continue
        key = norm(line + " " + section)
        if "bounce" in key or "inexistente" in key or "nao encontrado" in key or "quota" in key:
            found["bounce"].add(norm(name))
        elif "autorespost" in key or "automatic" in key:
            found["autoresposta"].add(norm(name))
        elif "resposta humana" in key and "nenhuma" not in key:
            found["resposta humana"].add(norm(name))
    return found


def summary_bullets(md_path: str, limit: int = 8) -> str:
    lines = [line.strip() for line in open(md_path, encoding="utf-8") if line.strip().startswith("- ")]
    return "\n".join(lines[:limit])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batches", default=str(DEFAULT_BATCHES))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    batches = Path(args.batches)

    companies: dict[str, dict] = {}
    company_batches: dict[str, set[str]] = defaultdict(set)
    batch_dates: dict[str, str] = {}

    pilot_files = sorted(glob.glob(str(batches / "*-pilot.csv")))
    # Empresas novas encontradas pelo agente de Prospecção depois da consolidação (fora do Git).
    extra = OPS / "growth" / "prospecting" / "empresas-novas.csv"
    if extra.exists():
        pilot_files.append(str(extra))
    other_csvs = [f for f in sorted(glob.glob(str(batches / "*.csv"))) if f not in pilot_files]
    for path in pilot_files + other_csvs:
        date, batch = batch_of(Path(path).name)
        batch_dates.setdefault(batch, date)
        for row in read_csv(path):
            cid = (row.get("company_id") or "").strip()
            if not cid:
                continue
            record = companies.setdefault(cid, {"company_id": cid})
            for field in COMPANY_FIELDS:
                value = (row.get(field) or "").strip()
                if value and not record.get(field):
                    record[field] = value
            company_batches[cid].add(batch)

    by_name = {norm(c.get("company_name", "")): cid for cid, c in companies.items()}

    contacts: list[dict] = []

    # E-mails: canal final "email" nos JSONs de cada lote, enviado na data do lote.
    for path in sorted(glob.glob(str(batches / "*-outreach-data.json"))):
        date, batch = batch_of(Path(path).name)
        for item in json.load(open(path, encoding="utf-8")):
            channel = item.get("dispatch_channel_final") or item.get("recommended_channel") or ""
            cid = item.get("company_id")
            if channel == "email" and cid in companies:
                contacts.append({"data": date, "company_id": cid, "lote": batch, "canal": "e-mail",
                                 "modelo": item.get("email_subject", ""), "resultado": "enviado",
                                 "fonte": Path(path).name})

    # WhatsApp: logs de envio do WAHA/WhatsApp Web.
    chat_to_company: dict[str, str] = {}
    for path in sorted(glob.glob(str(OPS / "whatsapp" / "runs" / "*.jsonl"))):
        for line in open(path, encoding="utf-8"):
            event = json.loads(line)
            cid = event.get("company_id")
            if cid not in companies:
                continue
            if event.get("chat_id"):
                chat_to_company[event["chat_id"]] = cid
            batch = sorted(company_batches[cid])[0] if company_batches[cid] else ""
            contacts.append({"data": event.get("timestamp", "")[:10], "company_id": cid, "lote": batch,
                             "canal": "WhatsApp", "modelo": event.get("detail", ""),
                             "resultado": "enviado" if event.get("status") == "sent" else "erro no envio",
                             "fonte": Path(path).name})
    for cid, record in companies.items():
        if record.get("normalized_whatsapp"):
            chat_to_company.setdefault(record["normalized_whatsapp"] + "@c.us", cid)

    # Respostas recebidas no WhatsApp (conversas do inbox), sem duplicar o mesmo evento.
    seen_messages: set[tuple] = set()
    for path in sorted(glob.glob(str(OPS / "whatsapp" / "inbox" / "conversations" / "*.jsonl"))):
        for line in open(path, encoding="utf-8"):
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            cid = chat_to_company.get(msg.get("chat_id", ""))
            if not cid or msg.get("from_me") or msg.get("type") not in (None, "chat", "text"):
                continue
            body = " ".join(str(msg.get("body") or "").split())
            if not body or len(body) > 1500:
                continue
            key = (cid, body, str(msg.get("received_at", ""))[:16])
            if key in seen_messages:
                continue
            seen_messages.add(key)
            contacts.append({"data": str(msg.get("received_at", ""))[:10], "company_id": cid,
                             "lote": sorted(company_batches[cid])[0] if company_batches[cid] else "",
                             "canal": "WhatsApp (recebida)", "modelo": "", "resultado": "mensagem recebida",
                             "observacao": body[:300], "fonte": Path(path).name})

    # Resultados citados nos monitores e relatórios (bounce, autoresposta, resposta humana).
    batch_rows = []
    for path in sorted(glob.glob(str(batches / "*.md"))):
        name = Path(path).name
        date, batch = batch_of(name)
        mentions = monitor_mentions(path)
        for outcome, names in mentions.items():
            for company_name in names:
                cid = by_name.get(company_name)
                if cid:
                    contacts.append({"data": date, "company_id": cid, "lote": batch, "canal": "",
                                     "modelo": "", "resultado": outcome, "fonte": name})
        if "monitor" in name or "result" in name or "incident" in name:
            batch_rows.append({"lote": batch, "data": date, "documento": name, "resumo": summary_bullets(path)})

    for company_name, (outcome, note) in HUMAN_REPLIES.items():
        cid = by_name.get(company_name)
        if cid:
            contacts.append({"data": max((c["data"] for c in contacts if c["company_id"] == cid), default=""),
                             "company_id": cid, "lote": sorted(company_batches[cid])[0] if company_batches[cid] else "",
                             "canal": "WhatsApp (recebida)", "modelo": "", "resultado": outcome,
                             "observacao": note, "fonte": "revisão das conversas em 2026-10-31"})
            if company_name == "medklinik":
                companies[cid]["opt_out_received"] = "sim (2026-05, sem interesse)"
            if company_name == "crust smash":
                companies[cid]["proxima_acao_sugerida"] = "encerrado: conversou, não quis seguir (registrado em 2026-10-31)"

    # Contatos registrados depois da consolidação (scripts/registrar_contato.py).
    registered = OPS / "growth" / "prospecting" / "contatos-registrados.jsonl"
    if registered.exists():
        for line in registered.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            entry = json.loads(line)
            key = entry.get("empresa", "")
            cid = key if key in companies else by_name.get(norm(key))
            if not cid:
                cid = "novo-" + norm(key).replace(" ", "-")[:40]
                companies.setdefault(cid, {"company_id": cid, "company_name": key})
            contacts.append({"data": entry.get("data", ""), "company_id": cid,
                             "lote": "", "canal": entry.get("canal", ""), "modelo": "",
                             "resultado": entry.get("resultado", ""), "observacao": entry.get("observacao", ""),
                             "fonte": "contatos-registrados.jsonl"})
            if entry.get("nao_contatar"):
                companies[cid]["do_not_contact"] = "sim"

    # Mesma empresa em listas diferentes (ex.: lote e fila de WhatsApp sem site): fundir pelo nome.
    canonical: dict[str, str] = {}
    alias: dict[str, str] = {}
    for cid in sorted(companies):
        key = norm(companies[cid].get("company_name", ""))
        if key and key in canonical:
            keep = companies[canonical[key]]
            for field, value in companies[cid].items():
                empty = keep.get(field) in (None, "", "false", "False")
                if value and value not in ("false", "False") and empty:
                    keep[field] = value
            keep["ids_antigos"] = ", ".join(filter(None, [keep.get("ids_antigos", ""), cid]))
            company_batches[canonical[key]] |= company_batches[cid]
            alias[cid] = canonical[key]
        elif key:
            canonical[key] = cid
    for cid in alias:
        companies.pop(cid)
    for c in contacts:
        c["company_id"] = alias.get(c["company_id"], c["company_id"])

    # Status atual por empresa = melhor resultado registrado; preparação da próxima rodada.
    offer_words = [("Site Express", ("site", "landing", "presença", "presenca", "página", "pagina")),
                   ("Automação Rápida", ("automa", "agenda", "atendimento", "whatsapp", "lembrete", "triagem", "crm")),
                   ("Painel de Controle", ("dashboard", "painel", "controle", "indicador", "relatório", "relatorio"))]
    for cid, record in companies.items():
        rows = [c for c in contacts if c["company_id"] == cid]
        results = [c["resultado"] for c in rows if c["resultado"] in STATUS_RANK]
        if any(c["resultado"] == "mensagem recebida" for c in rows) and "resposta humana" not in results:
            results.append("autoresposta")
        record["lotes"] = ", ".join(sorted(company_batches[cid]))
        record["status_atual"] = max(results, key=lambda r: STATUS_RANK[r]) if results else "não contatado"
        record["ultimo_contato"] = max((c["data"] for c in rows if c["data"]), default="")
        record["canais_usados"] = ", ".join(sorted({c["canal"] for c in rows if c["canal"]}))
        record["proxima_acao"] = record.pop("proxima_acao_sugerida", "")

        name_key = norm(record.get("company_name", ""))
        blocked = (record.get("do_not_contact") not in ("", None, "false", "False")
                   or record.get("opt_out_received") not in ("", None, "false", "False")
                   or record["status_atual"] in ("sem interesse", "cliente") or name_key in CLOSED)
        bounced = any(c["resultado"] == "bounce" for c in rows)
        if blocked:
            record["elegivel_rodada2"], record["canal_rodada2"], record["prioridade_rodada2"] = "não", "", ""
            record["proxima_acao"] = record["proxima_acao"] or CLOSED.get(name_key, "não contatar")
        else:
            record["elegivel_rodada2"] = "sim"
            if record.get("public_email") and not bounced:
                record["canal_rodada2"] = "e-mail"
            elif record.get("normalized_whatsapp"):
                record["canal_rodada2"] = "WhatsApp (manual)"
            else:
                record["canal_rodada2"] = "buscar contato"
            if record["status_atual"] in ("resposta humana", "autoresposta"):
                record["prioridade_rodada2"] = "A"
            elif record["canal_rodada2"] == "buscar contato" or record["status_atual"] in ("bounce", "erro no envio"):
                record["prioridade_rodada2"] = "C"
            else:
                record["prioridade_rodada2"] = "B"
        text = norm(" ".join(str(record.get(f, "")) for f in ("suggested_offer_primary", "offer_rationale", "outreach_angle")))
        offer = next((name for name, words in offer_words if any(w in text for w in words)), "")
        if not record.get("website_url"):
            offer = "Site Express"
        record["oferta_rodada2"] = offer or "Automação Rápida"

    wb = Workbook()
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="173847")

    def sheet(title: str, columns: list[str], rows: list[dict], first: bool = False):
        ws = wb.active if first else wb.create_sheet()
        ws.title = title
        ws.append(columns)
        for row in rows:
            ws.append([row.get(col, "") for col in columns])
        for cell in ws[1]:
            cell.font, cell.fill = header_font, header_fill
        ws.freeze_panes = "B2"
        ws.auto_filter.ref = ws.dimensions
        for idx, col in enumerate(columns, 1):
            width = min(60, max(12, max(len(str(ws.cell(r, idx).value or "")) for r in range(1, min(ws.max_row, 60) + 1))))
            ws.column_dimensions[ws.cell(1, idx).column_letter].width = width
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(vertical="top", wrap_text=False)
        return ws

    empresa_cols = ["company_id", "company_name", "segment", "city", "status_atual", "ultimo_contato", "canais_usados",
                    "proxima_acao", "elegivel_rodada2", "prioridade_rodada2", "canal_rodada2", "oferta_rodada2", "ids_antigos", "lotes"] + [f for f in COMPANY_FIELDS if f not in ("company_id", "company_name", "segment", "city")]
    sheet("Empresas", empresa_cols, sorted(companies.values(), key=lambda r: r["company_id"]), first=True)
    for c in contacts:
        c["company_name"] = companies[c["company_id"]].get("company_name", "")
    sheet("Contatos", ["data", "company_id", "company_name", "lote", "canal", "resultado", "modelo", "observacao", "fonte"],
          sorted(contacts, key=lambda r: (r["data"], r["company_id"])))
    sheet("Lotes", ["lote", "data", "documento", "resumo"], batch_rows)
    dictionary = [
        {"coluna": "status_atual", "significado": "melhor resultado registrado: não contatado < enviado < erro no envio < bounce < autoresposta < resposta humana"},
        {"coluna": "proxima_acao", "significado": "preenchido à mão ou pelo agente de contato na próxima rodada"},
        {"coluna": "elegivel_rodada2", "significado": "não = pediu para sair, sem interesse, cliente ou conversa encerrada"},
        {"coluna": "prioridade_rodada2", "significado": "A = canal vivo (respondeu ou autoresposta); B = enviado ou não contatado com canal válido; C = bounce, erro ou sem contato"},
        {"coluna": "canal_rodada2", "significado": "e-mail se houver e-mail sem bounce; senão WhatsApp (envio manual); senão buscar contato"},
        {"coluna": "oferta_rodada2", "significado": "sem site → Site Express; senão pela oferta sugerida na prospecção (automação ou painel)"},
        {"coluna": "ids_antigos", "significado": "IDs da mesma empresa em listas antigas, fundidos neste registro"},
        {"coluna": "do_not_contact / opt_out_received", "significado": "não contatar de novo quando preenchido"},
        {"coluna": "Contatos.resultado", "significado": "enviado, erro no envio, bounce, autoresposta, resposta humana, mensagem recebida"},
        {"coluna": "Contatos.fonte", "significado": "arquivo original de onde o registro saiu (arquivado em _arquivo/2026-05-lotes-outbound)"},
        {"coluna": "Observação", "significado": "e-mails dos lotes 001 a 005 foram considerados enviados na data do lote; bounces e autorespostas vêm dos monitores de resposta"},
    ]
    sheet("Dicionário", ["coluna", "significado"], dictionary)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.out)

    counts = defaultdict(int)
    for record in companies.values():
        counts[record["status_atual"]] += 1
    print(f"Empresas: {len(companies)} | Contatos: {len(contacts)} | Lotes/relatórios: {len(batch_rows)}")
    print("Status:", dict(sorted(counts.items(), key=lambda kv: -STATUS_RANK[kv[0]])))
    print("Saída:", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
