#!/usr/bin/env python3
"""
Registra um contato (recebido ou enviado) no log da base de prospecção e regenera a planilha.

O log ops/ai-os/growth/prospecting/contatos-registrados.jsonl (fora do Git) é lido por
scripts/build_prospect_base.py, então o registro sobrevive a cada nova geração da planilha.

Uso:
  python3 scripts/registrar_contato.py --empresa "Nome ou ID" --canal e-mail --resultado "resposta humana" \
      --observacao "pediu orçamento do Site Express" [--data 2026-11-02] [--nao-contatar]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "ops" / "ai-os" / "growth" / "prospecting" / "contatos-registrados.jsonl"
RESULTS = ["enviado", "erro no envio", "bounce", "autoresposta", "resposta humana", "mensagem recebida", "cliente", "sem interesse"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--empresa", required=True, help="company_id (ex.: nh-0622) ou nome da empresa")
    parser.add_argument("--canal", required=True, choices=["e-mail", "WhatsApp", "formulário", "telefone", "presencial", "outro"])
    parser.add_argument("--resultado", required=True, choices=RESULTS)
    parser.add_argument("--observacao", default="")
    parser.add_argument("--data", default=dt.date.today().isoformat())
    parser.add_argument("--nao-contatar", action="store_true", help="marca a empresa como não contatar")
    parser.add_argument("--sem-regenerar", action="store_true")
    args = parser.parse_args()

    LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {"data": args.data, "empresa": args.empresa, "canal": args.canal, "resultado": args.resultado,
             "observacao": args.observacao, "nao_contatar": args.nao_contatar,
             "registrado_em": dt.datetime.now().isoformat(timespec="seconds")}
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("Registrado:", entry)
    if not args.sem_regenerar:
        return subprocess.call([sys.executable, str(ROOT / "scripts" / "build_prospect_base.py")])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
