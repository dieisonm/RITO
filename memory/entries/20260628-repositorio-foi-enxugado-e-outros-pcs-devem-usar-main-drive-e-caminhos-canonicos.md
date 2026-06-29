---
id: "20260628-repositorio-foi-enxugado-e-outros-pcs-devem-usar-main-drive-e-caminhos-canonicos"
project: "RITO"
type: "decision"
status: "active"
title: "Repositório foi enxugado e outros PCs devem usar main, Drive e caminhos canônicos"
summary: "A estrutura do repositório foi simplificada para poucas pastas estáveis, com `main` como única branch de trabalho, `hostinger` apenas para deploy e Google Drive como destino dos assets pesados."
why: "Isso reduz perda de contexto entre computadores, evita caminhos antigos conflitarem com a operação atual e elimina o risco de arquivos importantes existirem só localmente ou inflarem o Git sem necessidade."
source: "codex-session"
created_at: "2026-06-28T12:00:00.000Z"
updated_at: "2026-06-28T12:00:00.000Z"
tags: ["repo-structure","sync","github-first","google-drive","onboarding","canonical-paths"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/ops/server/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/ops/server/other-computer-onboarding.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/assets/drive/asset-manifest.json"]
related_ids: ["20260517-pc-servidor-rito-deve-sincronizar-por-github-e-usar-onedrive.md","20260518-rito-passa-a-usar-github-first-com-google-drive-para-assets-"]
issue: ""
pr: ""
commit: ""
---

## Details

A estrutura operacional passou a girar em torno de poucos diretórios canônicos: `site/`, `docs/`, `ops/`, `memory/`, `assets/` e `scripts/`. Os caminhos antigos como `operations/`, `docs/company/` e `memory/project-memory/` deixaram de ser base válida de trabalho. Os logos usados no site ficam em `site/logos/`, enquanto a base de marca e os logos para uso interno ficam em `assets/brand/logos/`. Assets pesados e editáveis grandes devem ser enviados ao Google Drive e registrados em `assets/drive/asset-manifest.json`, não mantidos como fonte principal no Git. Para retomada em outro computador, o fluxo padrão é abrir `main`, puxar o estado mais recente e usar o guia `docs/ops/server/other-computer-onboarding.md`.
