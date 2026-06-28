---
id: "20260412-docscompany-is-the-canonical-operational-base"
project: "RITO"
type: "decision"
status: "resolved"
title: "docs/company foi a base operacional canônica inicial, mas foi superado pela estrutura enxuta atual"
summary: "Esta decisão refletia a estrutura inicial em `docs/company`, mas foi substituída pela organização atual com `docs/`, `ops/`, `memory/` e `assets/` como caminhos canônicos."
why: "A entrada foi mantida como histórico, mas precisa deixar claro que não representa mais a estrutura válida do repositório."
source: "codex"
created_at: "2026-04-12T19:24:05.366Z"
updated_at: "2026-06-28T12:20:00.000Z"
tags: ["operations","documentation","deliverables"]
files: ["docs/README.md","assets/deliverables/business-kit/README.md","scripts/generate_final_business_assets.py","scripts/generate_pricing_calculator_xlsx.py"]
related_ids: ["20260518-rito-passa-a-usar-github-first-com-google-drive-para-assets-","20260628-repositorio-foi-enxugado-e-outros-pcs-devem-usar-main-drive-e-caminhos-canonicos"]
issue: ""
pr: ""
commit: ""
---

## Details

Historicamente, esta entrada registrou a primeira tentativa de consolidar a base operacional em `docs/company`. Ela nao deve mais ser usada como instrução vigente. A estrutura canônica atual está distribuída entre `docs/`, `ops/`, `memory/` e `assets/`, conforme a reorganização registrada em `20260628-repositorio-foi-enxugado-e-outros-pcs-devem-usar-main-drive-e-caminhos-canonicos`. O princípio que continua válido é apenas este: arquivos finais grandes continuam sendo derivados e não devem ser tratados como fonte principal no Git.
