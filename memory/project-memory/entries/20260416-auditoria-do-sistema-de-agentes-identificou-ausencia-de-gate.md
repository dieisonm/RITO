---
id: "20260416-auditoria-do-sistema-de-agentes-identificou-ausencia-de-gate"
project: "RITO"
type: "decision"
status: "active"
title: "Auditoria do sistema de agentes identificou ausência de gate visual por canal para Instagram"
summary: "A análise dos prompts e playbooks de conteúdo, branding e revisão mostrou que a esteira da RITO valida tom, clareza e coerência de marca, mas não exige adequação visual nativa ao canal. Isso permitiu que peças com aparência de slide passassem pela revisão."
why: "Sem critérios obrigatórios de formato, densidade de texto, image-first composition e bloqueio explícito para layouts com cara de apresentação, os agentes entregam materiais corretos no texto, porém inadequados para Instagram."
source: "codex"
created_at: "2026-04-16T00:00:31.408Z"
updated_at: "2026-04-16T00:00:31.408Z"
tags: ["agents","instagram","content","branding","review","quality-gate"]
files: ["docs/company/agent-system/prompts/content-agent.md","docs/company/agent-system/prompts/branding-agent.md","docs/company/agent-system/prompts/revisor-agent.md","docs/company/agent-system/playbooks/phase-1/conteudo-organico.md","docs/company/agent-system/playbooks/phase-1/revisor.md","docs/company/agent-system/playbooks/phase-2/branding.md"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

Foram auditados `docs/company/agent-system/prompts/content-agent.md`, `branding-agent.md`, `revisor-agent.md`, `playbooks/phase-1/conteudo-organico.md`, `playbooks/phase-1/revisor.md` e `playbooks/phase-2/branding.md`. O diagnóstico central foi: o agente de conteúdo não é obrigado a entregar arte final ou direção visual nativa do canal; branding privilegia consistência geral, mas não veta estética de slide; revisão não possui perguntas de bloqueio sobre adequação ao Instagram. A correção recomendada é introduzir critérios mandatórios de canal, especialmente para estáticos e carrosséis: composição image-first, teto de texto na arte, teste de legibilidade em thumbnail, distinção clara entre static/carousel/reel e bloqueio explícito de layouts que pareçam deck, PDF, one-pager ou post corporativo de baixa aderência ao feed.
