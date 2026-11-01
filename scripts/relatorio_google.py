#!/usr/bin/env python3
"""
Relatório do Google para o site da RITO: Search Console (buscas e indexação) e GA4 (visitas e eventos).

Credencial: google-service-account.local.json na raiz da pasta RITO (conta de serviço só de leitura,
fora do Git). A conta precisa estar como usuária no Search Console e como Leitor no GA4.

Uso:
  python3 scripts/relatorio_google.py [--dias 28] [--salvar]
Com --salvar, grava o Markdown em ops/ai-os/growth/relatorios/AAAA-MM-DD-google.md (fora do Git).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import warnings
from pathlib import Path
from urllib.parse import quote

warnings.filterwarnings("ignore")

from google.auth.transport.requests import AuthorizedSession  # noqa: E402
from google.oauth2 import service_account  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
KEY = ROOT / "google-service-account.local.json"
SITE = "sc-domain:ritosistemas.com"
GA4_PROPERTY = "538384859"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly", "https://www.googleapis.com/auth/analytics.readonly"]
LEAD_EVENTS = ["generate_lead_form", "click_whatsapp", "click_offers_page", "click_email"]


def session() -> AuthorizedSession:
    info = json.loads(KEY.read_text(encoding="utf-8"))
    return AuthorizedSession(service_account.Credentials.from_service_account_info(info, scopes=SCOPES))


def gsc_query(s, start, end, dimensions, limit=25):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{quote(SITE, safe='')}/searchAnalytics/query"
    body = {"startDate": start.isoformat(), "endDate": end.isoformat(), "dimensions": dimensions, "rowLimit": limit}
    r = s.post(url, json=body)
    r.raise_for_status()
    return r.json().get("rows", [])


def gsc_totals(s, start, end):
    rows = gsc_query(s, start, end, [], 1)
    return rows[0] if rows else {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0}


def gsc_inspect(s, url):
    r = s.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
               json={"inspectionUrl": url, "siteUrl": SITE, "languageCode": "pt-BR"})
    if r.status_code != 200:
        return {"verdict": f"erro {r.status_code}"}
    res = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
    return {"verdict": res.get("verdict", ""), "coverage": res.get("coverageState", ""), "lastCrawl": res.get("lastCrawlTime", "")[:10]}


def ga4_report(s, start, end, dimensions, metrics, limit=15, event_filter=None):
    body = {"dateRanges": [{"startDate": start.isoformat(), "endDate": end.isoformat()}],
            "dimensions": [{"name": d} for d in dimensions], "metrics": [{"name": m} for m in metrics], "limit": limit}
    if event_filter:
        body["dimensionFilter"] = {"filter": {"fieldName": "eventName", "inListFilter": {"values": event_filter}}}
    r = s.post(f"https://analyticsdata.googleapis.com/v1beta/properties/{GA4_PROPERTY}:runReport", json=body)
    if r.status_code != 200:
        raise PermissionError(r.json().get("error", {}).get("message", r.text)[:200])
    out = []
    for row in r.json().get("rows", []):
        out.append([v["value"] for v in row.get("dimensionValues", [])] + [v["value"] for v in row.get("metricValues", [])])
    return out


def fmt_pct(x):
    return f"{x * 100:.1f}%"


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(lines) if rows else "_sem dados no período_"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dias", type=int, default=28)
    parser.add_argument("--salvar", action="store_true")
    args = parser.parse_args()

    s = session()
    end = dt.date.today() - dt.timedelta(days=2)  # Search Console tem atraso de cerca de 2 dias
    start = end - dt.timedelta(days=args.dias - 1)
    prev_end = start - dt.timedelta(days=1)
    prev_start = prev_end - dt.timedelta(days=args.dias - 1)
    out = [f"# Relatório do Google — ritosistemas.com", "",
           f"Período: {start.isoformat()} a {end.isoformat()} ({args.dias} dias), comparado com {prev_start.isoformat()} a {prev_end.isoformat()}.", ""]

    # Search Console
    cur, prev = gsc_totals(s, start, end), gsc_totals(s, prev_start, prev_end)
    out += ["## Busca no Google (Search Console)", "",
            table(["Métrica", "Período", "Anterior"], [
                ["Cliques", int(cur["clicks"]), int(prev["clicks"])],
                ["Impressões", int(cur["impressions"]), int(prev["impressions"])],
                ["CTR", fmt_pct(cur["ctr"]), fmt_pct(prev["ctr"])],
                ["Posição média", f"{cur['position']:.1f}", f"{prev['position']:.1f}"]]), ""]
    queries = gsc_query(s, start, end, ["query"], 50)
    out += ["### Termos de busca", "", table(["Termo", "Cliques", "Impressões", "CTR", "Posição"],
            [[r["keys"][0], int(r["clicks"]), int(r["impressions"]), fmt_pct(r["ctr"]), f"{r['position']:.1f}"] for r in queries[:20]]), ""]
    chances = [r for r in queries if r["impressions"] >= 20 and r["ctr"] < 0.02]
    out += ["### Oportunidades (muitas impressões, poucos cliques)", "", table(["Termo", "Impressões", "CTR", "Posição"],
            [[r["keys"][0], int(r["impressions"]), fmt_pct(r["ctr"]), f"{r['position']:.1f}"] for r in chances[:10]]), ""]
    pages = gsc_query(s, start, end, ["page"], 25)
    out += ["### Páginas", "", table(["Página", "Cliques", "Impressões", "Posição"],
            [[r["keys"][0].replace("https://ritosistemas.com", "") or "/", int(r["clicks"]), int(r["impressions"]), f"{r['position']:.1f}"] for r in pages]), ""]
    devices = gsc_query(s, start, end, ["device"], 5)
    out += ["### Dispositivos", "", table(["Dispositivo", "Cliques", "Impressões"], [[r["keys"][0], int(r["clicks"]), int(r["impressions"])] for r in devices]), ""]

    # Indexação das páginas do sitemap
    sitemap_urls = ["https://ritosistemas.com/"] + [f"https://ritosistemas.com/pages/{p}.html" for p in
                    ["ofertas", "solucoes", "como-funciona", "para-quem", "sobre", "contato", "case-relatorio-de-vendas", "privacidade"]]
    out += ["### Indexação", "", table(["Página", "Situação", "Cobertura", "Último rastreio"],
            [[u.replace("https://ritosistemas.com", "") or "/", *gsc_inspect(s, u).values()] for u in sitemap_urls]), ""]

    # GA4
    out += ["## Visitas no site (GA4)", ""]
    try:
        totals = ga4_report(s, start, end, [], ["activeUsers", "sessions", "screenPageViews"], 1)
        t = totals[0] if totals else ["0", "0", "0"]
        out += [table(["Usuários", "Sessões", "Visualizações"], [t]), ""]
        out += ["### Origem do tráfego", "", table(["Origem / meio", "Sessões"], ga4_report(s, start, end, ["sessionSourceMedium"], ["sessions"], 10)), ""]
        out += ["### Páginas mais vistas", "", table(["Página", "Visualizações"], ga4_report(s, start, end, ["pagePath"], ["screenPageViews"], 10)), ""]
        out += ["### Ações de contato", "", table(["Evento", "Quantidade"], ga4_report(s, start, end, ["eventName"], ["eventCount"], 10, LEAD_EVENTS)), ""]
    except PermissionError as exc:
        out += [f"_GA4 sem acesso: {exc}. Adicionar `rito-relatorios@rito-relatorios.iam.gserviceaccount.com` como Leitor na propriedade {GA4_PROPERTY}._", ""]

    report = "\n".join(out)
    print(report)
    if args.salvar:
        dest = ROOT / "ops" / "ai-os" / "growth" / "relatorios" / f"{dt.date.today().isoformat()}-google.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(report + "\n", encoding="utf-8")
        print(f"\nSalvo em {dest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
