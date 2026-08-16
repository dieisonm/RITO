---
id: "20260721-analises-revamp-panorama-e-clientes-com-rpcs-sql-e-recharts"
project: "RITO"
type: "decision"
status: "active"
title: "/analises: revamp de analytics (abas Panorama + Clientes) com RPCs SQL e Recharts; ultima agregacao em JS aposentada"
summary: "A tela /analises rasa (4 KPIs) virou um workspace de analytics apoiado em RPCs de Postgres, e com isso a ULTIMA agregacao em JS foi aposentada (analyzeLegacyData + getLegacyDashboard + getDatabaseAnalyticsSource deletados — nenhuma pagina puxa mais a tabela sales_transactions inteira). Migrations novas: 20260720000001_analytics_revamp.sql (RPCs read-only: analytics_period, company_vendor_matrix, dimension_monthly, top_clients_period, client_changes, dormant_clients, vendor_scorecards, receipt_timing), 20260721000001_receipt_timing_by_company.sql (v2 por empresa) e 20260724000001_client_recency.sql. Camada de dados getAnalytics em src/lib/analytics.ts (cacheada em KV, chaveada por filtros). Graficos com Recharts 3.10 (client-side, code-split -> zero impacto na CPU do Worker) e paleta categorica validada para daltonismo em chart-theme.ts (a paleta da marca REPROVOU no teste CVD). Depois de um primeiro build de 5 abas que o usuario achou fragmentado, consolidou em UMA aba densa Panorama; depois a aba Clientes (toggle Presente/Historico, recencia 60/90 dias). Panorama foi publicado primeiro (Worker 164a8aeb, 21/07); a aba Clientes foi ligada e publicada no lote de 02/08 (Worker 5cc2f97e)."
why: "Fecha o trabalho de CPU/Cloudflare (a /analises era a unica pagina ainda agregando em JS sobre um fetch da tabela inteira). E documenta duas decisoes de produto/dados que mudam como ler a tela: (1) a janela padrao ancora no ULTIMO mes com dados (max(effective_date)), nao em hoje, porque os dados vem de relatorios importados e ficam atras do calendario (aparecia mes vazio quando ancorava em hoje); (2) semantica de recebimento."
source: "claude-code-session"
created_at: "2026-07-21T00:00:00-03:00"
updated_at: "2026-08-02T00:00:00-03:00"
tags: ["relatorio-vendas","analises","analytics","supabase","rpc","recharts","cloudflare-workers","kv-cache","dataviz","cvd"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/supabase/migrations/20260720000001_analytics_revamp.sql","S:/RITO/Projetos/relatorio-vendas-web/supabase/migrations/20260721000001_receipt_timing_by_company.sql","S:/RITO/Projetos/relatorio-vendas-web/supabase/migrations/20260724000001_client_recency.sql","S:/RITO/Projetos/relatorio-vendas-web/src/lib/analytics.ts","S:/RITO/Projetos/relatorio-vendas-web/src/components/analytics/analytics-workspace.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/components/analytics/panorama-tab.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/components/analytics/clients-tab.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/components/analytics/chart-theme.ts","S:/RITO/Projetos/relatorio-vendas-web/src/app/(app)/analises/page.tsx"]
related_ids: ["20260719-otimizacao-de-cpu-cloudflare-e-seguranca-de-sessao-publicadas","20260802-relatorio-vendas-tres-correcoes-criticas-de-importacao-e-comissao"]
issue: ""
pr: ""
commit: "ee38b1a, 89ba40a, 1ac517b, d1afb50, 8b822fc, 794be9c, e7bbfd3, ff1ceb0"
---

## O que foi feito

- **Agregacao 100% em SQL**: 8 RPCs read-only sobre a view `dashboard_entries`/`sales_transactions`, com harness de paridade validando `analytics_period` contra o antigo JS em producao. Retirados `analyzeLegacyData`, `getLegacyDashboard` e `getDatabaseAnalyticsSource` — nenhuma pagina puxa mais a tabela inteira (fecha a serie de fixes de Error 1102/CPU).
- **Aba Panorama** (densa): KPIs + coortes, tendencia de comissao com toggle Total/empresa/vendedor, matriz empresa x vendedor legivel (texto claro em celulas escuras) com hover de movimentos/clientes, card de concentracao, comparativo de vendedores e card de recebimento.
- **Aba Clientes** (Presente/Historico): escada de recencia (Ativo <=60d / Esfriando 61-90d / Inativo >90d / Nunca comprou), "regulares esfriando", reativacao e novos; Historico reusa client_changes/top_clients_period/cohorts. Usa a RPC `client_recency` ancorada em `max(effective_date)`.
- **Graficos**: Recharts 3.10 client-side, code-split para /analises (nao roda no Worker -> nao conta na CPU). Paleta categorica validada para CVD em `chart-theme.ts` — a paleta da marca reprovou e foi trocada por uma segura.

## Decisoes que mudam a leitura da tela

1. **A janela padrao e os presets ancoram no ultimo mes COM DADOS** (`max(effective_date)`, primeiro dia do mes, 3 meses), NAO em hoje — os dados de relatorio ficam atras do calendario. Manter isso ao mexer na logica de datas.
2. **Semantica de recebimento (verificada em prod)**: `issue_date`=emissao e `receipt_date`=recebimento sao datas reais por documento; `effective_date` = `receipt_date` em toda linha (a tela agrupa por data de recebimento). Lag emissao->recebimento real ~30d (CLARAMAX ~31d, CAMNPAL ~27d). O relatorio da BISCOBOM carrega UMA data so, entao o parser forca emissao=recebimento (artefato de 0 dias) — `receipt_timing` v2 exclui empresas de fonte de data unica da media/mediana principal.

## Estado

Panorama publicado em 21/07 (Worker `164a8aeb`); aba Clientes ligada e publicada no lote de 02/08 (Worker `5cc2f97e`). Detalhe completo e pendencias em `docs/current-state.md` do repo relatorio-vendas-web. O plano faseado/resumivel viveu em `~/.claude/plans/i-want-you-to-atomic-thunder.md`.
