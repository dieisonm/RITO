---
id: "20260414-arquitetura-inicial-de-agentes-da-rito-deve-separar-conteudo"
project: "RITO"
type: "decision"
status: "active"
title: "Arquitetura inicial de agentes da RITO deve separar conteúdo, aquisição e atendimento"
summary: "O planejamento da operação por agentes da RITO deve usar uma equipe-base com papéis separados para conteúdo orgânico, aquisição paga/SEO e atendimento, além de comercial, branding, site/UX, operações, pricing e revisão."
why: "Essas frentes exigem ritmos, métricas e competências diferentes; juntar tudo em poucos agentes deixaria a execução genérica e reduziria qualidade operacional."
source: "codex"
created_at: "2026-04-14T12:31:04.858Z"
updated_at: "2026-04-14T12:31:04.858Z"
tags: ["agents","operations","planning","content","growth","support"]
files: ["docs/agents/agent-system/agent-directory.md","docs/agents/agent-system/operating-model.md","ops/ai-os/README.md"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

A recomendação é começar com um agente de conteúdo orgânico dono de LinkedIn, Instagram e Facebook, mas sem misturar isso com tráfego pago ou inbox. Tráfego, SEO, Google Ads, Meta Ads, landing pages e métricas de aquisição devem ficar sob um agente próprio de Growth/Aquisição. Atendimento em WhatsApp, Instagram e LinkedIn também deve ser um agente próprio, separado do comercial, para preservar velocidade, consistência e triagem correta. A arquitetura inicial recomendada fica: Orquestrador, Atendimento e Relacionamento, Comercial, Conteúdo Orgânico, Growth/Aquisição, Branding, Site/UX/Conversão, Operações/Delivery, Financeiro/Pricing e Revisor. Canais sociais podem ser detalhados depois em subplaybooks por canal, sem necessidade de um agente isolado para cada rede na fase 1.
