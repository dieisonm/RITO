---
id: "20260518-deploy-do-site-e-git-only-pela-branch-hostinger"
project: "RITO"
type: "decision"
status: "active"
title: "Deploy do site e Git-only pela branch hostinger"
summary: "O fluxo canonico de deploy do site da RITO e Git-only: GitHub Actions publica a branch hostinger e a Hostinger faz o deploy dessa branch. Publicacao direta na hospedagem nao deve ser usada nem documentada como rotina."
why: "Evitar que documentacao, memoria, operacao, agentes ou scripts internos disparem deploy do site e impedir que um fallback operacional vire fluxo paralelo fragil."
source: "Codex session 2026-05-18"
created_at: "2026-05-18T19:51:55.699Z"
updated_at: "2026-05-18T21:54:02.932Z"
tags: ["deploy","hostinger","github-actions","git-only"]
files: [".github/workflows/deploy-hostinger.yml","docs/ops/hostinger-deploy.md","README.md","docs/ops/server/desktop-server-replication-runbook.md"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

Em 2026-05-18 foi removido o commit invalido de bootstrap do servidor que entrou em origin/main e falhou no deploy. Tambem foram limpos residuos locais que reintroduziam publicacao direta e gatilho amplo para a pasta de scripts no workflow. O workflow deve disparar apenas para site/**, assets/brand/**, scripts/build_dist.sh e .github/workflows/deploy-hostinger.yml.
