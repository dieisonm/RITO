---
id: "20260702-auditoria-de-performance-do-relatorio-de-vendas-web-identifi"
project: "RITO"
type: "decision"
status: "active"
title: "Auditoria de performance do Relatorio de Vendas web identificou causa raiz da lentidao entre abas e iniciou plano de correcao"
summary: "Investigacao (3 agentes Explore em paralelo) confirmou que trocar de aba na app de comissoes leva alguns segundos por causa de dupla verificacao sequencial de auth a cada navegacao, fetch de tabelas inteiras com agregacao em JS em vez de SQL, ausencia total de cache e falta de loading states. Plano de correcao em 5 frentes foi aprovado e a implementacao esta em andamento, comecando pelos quick wins."
why: "O usuario reportou lentidao perceptivel (poucos segundos) ao trocar de aba na app em producao (https://rito.relatorio-vendas.workers.dev) e pediu analise de gargalos, plano de melhoria e estimativa de ganho. Apos aprovacao, pediu execucao autonoma comecando pelos quick wins, com checagem de regressao apos cada mudanca antes de avancar para o proximo topico."
source: "claude-code-session"
created_at: "2026-07-02T00:00:00-03:00"
updated_at: "2026-07-02T00:00:00-03:00"
tags: ["relatorio-vendas","performance","cloudflare-workers","supabase","auth","caching","sql-aggregation","smart-placement"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/src/lib/auth.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/database-data.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/legacy-data.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/commission-report.ts","S:/RITO/Projetos/relatorio-vendas-web/src/app/api/clientes/route.ts","S:/RITO/Projetos/relatorio-vendas-web/wrangler.jsonc"]
related_ids: ["20260702-relatorio-de-vendas-web-esta-em-producao-com-cloudflare-e-supabase"]
issue: ""
pr: ""
commit: ""
---

## Diagnostico

Toda navegacao entre abas (Dashboard, Clientes, Vendedores, Empresas, Importar, Analises) dispara um novo render de Server Component sem nenhum cache entre requisicoes. A causa raiz tem quatro componentes que se somam:

1. `requireAdminPage`/`requireAdminApi` em `src/lib/auth.ts` chamam `supabase.auth.getUser()` (round trip real ao servidor de Auth da Supabase, nao decodificacao local de JWT) seguido de uma segunda query sequencial na tabela `profiles`. Isso roda em toda pagina e toda API, sem cache entre requests, e sem layout compartilhado que hospede essa checagem uma unica vez.
2. `getDatabaseAnalyticsSource` (`src/lib/database-data.ts`), `getLegacyDashboard` (`src/lib/legacy-data.ts`), `getCommissionReportData` (`src/lib/commission-report.ts`) e `fetchClients` (`src/app/api/clientes/route.ts`) paginam a tabela inteira (`sales_transactions` com ~6.393 linhas, `clients` com ~1.522 linhas) em blocos de 1000 com joins relacionais, e agregam/somam no JavaScript em vez de usar `SUM`/`GROUP BY` no Postgres. `/analises` e o pior caso: ate 7 paginas sequenciais so para os totais.
3. Nao existe nenhuma camada de cache (`revalidate`, `unstable_cache`, KV, cache HTTP) nem `loading.tsx`/Suspense em nenhuma rota, entao a UI fica completamente congelada durante toda a cadeia auth -> fetch -> agregacao -> render, e tudo e refeito do zero mesmo ao voltar para uma aba ja visitada.
4. O Worker Cloudflare (`wrangler.jsonc`) nao usa Smart Placement, entao roda proximo do navegador do usuario em vez de proximo da regiao fixa do Supabase, multiplicando a latencia de cada round trip acima.

Bundle client-side, fontes e dependencias pesadas (`exceljs`, `pdfjs-dist`) foram auditados e estao corretos (server-only, sem vazamento para o client). Nao e um problema de bundle size.

## Plano de correcao (ordem de execucao)

1. Habilitar Smart Placement em `wrangler.jsonc` (config trivial).
2. Adicionar `loading.tsx`/Suspense por rota para eliminar a sensacao de tela congelada.
3. Colapsar a dupla verificacao de auth por navegacao (evitar round trip duplicado por request).
4. Substituir fetch de tabela inteira + agregacao em JS por agregacao SQL (views/RPC) no dashboard, analises e relatorio de comissao.
5. Adicionar camada de cache para dados agregados, invalidada em eventos de importacao.
6. Limpeza: remover dependencias nao usadas (`pg`, `unpdf`).

Estimativa combinada (1+2+3+4+5): reduzir a troca de aba de ~2-4s para ~200-500ms em cache miss e <100ms em cache hit (reducao de 80-95%).

## Execucao

Trabalho autorizado para rodar de forma autonoma: implementar, validar (typecheck/build/checagem funcional) e avancar item a item sem pedir confirmacao a cada mudanca, comecando pelos quick wins (1-3) antes dos itens estruturais (4-5). Atualizar este registro (ou criar entrada de acompanhamento) conforme cada frente for concluida.
