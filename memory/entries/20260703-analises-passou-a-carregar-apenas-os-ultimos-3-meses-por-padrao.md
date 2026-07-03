---
id: "20260703-analises-passou-a-carregar-apenas-os-ultimos-3-meses-por-padrao"
project: "RITO"
type: "decision"
status: "active"
title: "Analises do Relatorio de Vendas web passou a carregar apenas os ultimos 3 meses por padrao apos um Error 1102 do Cloudflare"
summary: "/analises buscava e agregava em JS a tabela sales_transactions inteira em toda requisicao, sem levar o filtro de data em conta na query. Com o crescimento da base durante os testes do dia (6.393 -> 7.910 transacoes), isso disparou um Error 1102 (Worker exceeded resource limits) uma vez, sem perda de dados. Corrigido: periodo padrao agora e os ultimos 3 meses (busca ampliada o suficiente para cobrir o periodo anterior usado na comparacao do dashboard), ~40% menos linhas buscadas no caso padrao. O usuario pode escolher um periodo maior nos filtros da tela quando precisar."
why: "O usuario reportou o erro, navegando entre paginas e clicando por ultimo em Analises. Investigado com wrangler tail (nada capturado ao vivo, o erro nao se repetiu) e checagem de dados (nenhuma escrita parcial no horario do erro). Causa raiz identificada por leitura de codigo: getDatabaseAnalyticsSource() nao aplicava filtro de data na query ao Supabase, so filtrava depois em JS."
source: "claude-code-session"
created_at: "2026-07-03T22:32:07-03:00"
updated_at: "2026-07-03T22:32:07-03:00"
tags: ["relatorio-vendas","performance","cloudflare-workers","analises","supabase"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/src/app/(app)/analises/page.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/lib/database-data.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/legacy-data.ts","S:/RITO/Projetos/relatorio-vendas-web/docs/current-state.md"]
related_ids: ["20260703-fluxo-de-confirmacao-e-gravacao-da-importacao-web-foi-implementado-e-publicado", "20260702-plano-de-performance-do-relatorio-de-vendas-web-foi-concluido-com-um-item-adiado"]
issue: ""
pr: ""
commit: "7fe17ec,c7b8527"
---

## Mudanca

`getDatabaseAnalyticsSource()` (`src/lib/database-data.ts`) passou a aceitar um `range?: { startDate, endDate }` opcional, aplicado como `.gte()/.lte()` na query paginada de `sales_transactions`. `src/app/(app)/analises/page.tsx` agora calcula um periodo padrao de 3 meses quando o usuario nao informa filtro (`params.inicio`/`params.fim` ausentes), amplia a janela de busca para cobrir tambem o periodo anterior (mesma logica de `daysBetween`/`addDays` que o calculo de comparacao ja usava, agora exportadas de `legacy-data.ts`) e so entao chama `getDatabaseAnalyticsSource` com esse range.

`catalog.minDate`/`maxDate` (usado por `/importar` para o intervalo padrao do gerador de Excel e nao deve encolher com o novo filtro) passou a vir de duas queries indexadas baratas (`order + limit(1)`, ascendente e descendente) em vez de ser derivado do array de linhas buscadas — assim continua refletindo o historico completo mesmo quando a busca principal esta com escopo reduzido.

## Risco residual, nao mitigado

`/importar` (`src/app/(app)/importar/page.tsx`) ainda chama `getDatabaseAnalyticsSource()` sem range, buscando a tabela inteira — mesmo padrao que causou o erro em Analises. Nao foi alterado nesta rodada (fora do pedido do usuario). Registrado como pendencia 7 em `docs/current-state.md`.

## Verificacao

`npx tsc --noEmit` e `npm run build` limpos. Reducao de volume medida contra dados reais de producao: janela padrao (~6 meses, cobrindo periodo atual + anterior) trouxe 4.686 de 7.910 transacoes totais (-40.8%). Nenhuma escrita parcial encontrada no horario do erro original (2026-07-03 22:52:38 UTC) ao consultar `clients`, `client_vendor_assignments` e `imports` na janela de tempo correspondente — o erro nao deixou nada inconsistente no banco.
