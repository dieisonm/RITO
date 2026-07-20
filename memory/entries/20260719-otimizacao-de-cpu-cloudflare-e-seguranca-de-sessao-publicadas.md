---
id: "20260719-otimizacao-de-cpu-cloudflare-e-seguranca-de-sessao-publicadas"
project: "RITO"
type: "decision"
status: "active"
title: "Otimizacao de CPU (agregacao SQL + cache KV) e seguranca de sessao do Relatorio de Vendas foram publicadas"
summary: "O app estava batendo no limite de CPU por request do Cloudflare Workers free (Error 1102) porque /, /clientes, /vendedores e /importar buscavam a tabela sales_transactions inteira e agregavam em JS a cada navegacao. Corrigido movendo a agregacao para RPCs Postgres (paridade validada contra o JS antigo), removendo o fetch total do /importar, limitando o Excel a 12 meses, e adicionando um cache KV entre requisicoes com invalidacao por chave de versao global. Tambem foi adicionada seguranca de sessao: logout por 20 min de inatividade e cookies de sessao (derrubados ao fechar o navegador). Tudo validado localmente pelo usuario e publicado em producao (Worker version 59851c56)."
why: "O usuario reportou que o app free estava travando por limite de recursos apesar de otimizacoes anteriores documentadas. Pediu revisao profunda delegando trabalho barato (leitura de docs/codigo) a modelos baratos (haiku/sonnet) e o trabalho pesado/arriscado (agregacao SQL, cache, sessao) ao opus, com um plano bem documentado e resumivel. Tambem pediu logout por inatividade e ao fechar o navegador como medida de seguranca (sessao persistia em computador de terceiros)."
source: "claude-code-session"
created_at: "2026-07-19T00:00:00-03:00"
updated_at: "2026-07-19T00:00:00-03:00"
tags: ["relatorio-vendas","performance","cloudflare-workers","supabase","sql-aggregation","kv-cache","seguranca","sessao","producao"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/supabase/migrations/20260706000001_analytics_rpc.sql","S:/RITO/Projetos/relatorio-vendas-web/src/lib/analytics.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/cache.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/database-data.ts","S:/RITO/Projetos/relatorio-vendas-web/src/app/(app)/importar/page.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/components/session-timeout.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/lib/supabase/session-cookies.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/supabase/client.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/supabase/server.ts","S:/RITO/Projetos/relatorio-vendas-web/wrangler.jsonc","S:/RITO/Projetos/relatorio-vendas-web/docs/current-state.md"]
related_ids: ["20260703-analises-passou-a-carregar-apenas-os-ultimos-3-meses-por-padrao","20260702-plano-de-performance-do-relatorio-de-vendas-web-foi-concluido-com-um-item-adiado","20260705-ui-overhaul-e-provisionamento-de-acesso-de-vendedores-foram-publicados"]
issue: ""
pr: ""
commit: "cddb6b8,9e4afd7,fde919f,cb17113,a55b520,837e239,c4d23f9"
---

## Causa raiz e correcao de CPU

`getLegacyDashboard()` buscava cinco tabelas inteiras (incluindo toda a `sales_transactions`, sem recorte de data) e fazia varios passes O(N) e O(vendedores*N) em JS, e era chamada por `/`, `/clientes`, `/vendedores` e `/importar` — custo pago a CADA navegacao (o `cache()` do React so deduplica dentro de um request). `/importar` era o pior: buscava o historico inteiro duas vezes.

Correcao, em fases (plano resumivel em `~/.claude/plans/i-want-you-to-atomic-thunder.md`):
- **1A**: `/importar` passou a usar selects pequenos + `getTransactionDateBounds()` (min/max indexado). Excel do gerador de comissao limitado a 12 meses.
- **1B (nucleo)**: migracao `20260706000001_analytics_rpc.sql` cria a view `dashboard_entries` (deduplicacao global igual ao `entryKey` do JS) + funcoes `dashboard_summary`/`monthly_totals`/`vendor_metrics`/`top_clients`/`client_metrics`. `src/lib/analytics.ts` embrulha as RPCs. Um harness de paridade (helpers do JS copiados verbatim vs saida das RPCs, contra o banco de producao) confirmou numeros identicos. `client_metrics` junta por `client_id` de proposito, entao TODOS os clientes (nao so CLARAMAX, que era um filtro legado) mostram metricas reais. `getLegacyDashboard` aposentado.
- **1C**: cache KV (`src/lib/cache.ts`, binding `rito_cache`) entre requisicoes, com uma chave `dataVersion` global incrementada por toda rota de mutacao (+ TTL 300s). Degrada com seguranca: `getCloudflareContext()` sincrono lanca em `next dev` (sem binding) — capturado e cai para calculo direto, entao dev sempre fresco e so o Worker publicado cacheia.

## Seguranca de sessao

- Logout automatico apos 20 min de inatividade (`src/components/session-timeout.tsx`, montado no AppShell; re-checa em visibilitychange/focus para cobrir sleep/wake).
- Cookies de sessao (derrubados ao fechar o navegador): `@supabase/ssr` v0.12 fixa maxAge (~400 dias) e ignora `cookieOptions` (verificado no node_modules), entao `src/lib/supabase/session-cookies.ts` remove maxAge/expires nos adaptadores `setAll` do cliente server E browser — PRESERVANDO na delecao para o signOut continuar limpando os cookies. Um bug de acesso a `document` no adaptador do browser (SSR) foi pego e corrigido no teste local.

## Como foi conduzido (delegacao de modelos, a pedido do usuario)

Leitura de documentacao propria e de docs externas + inspecao de pacotes instalados (@supabase/ssr, @opennextjs/cloudflare) delegada a agentes **haiku**; mapeamento de codigo/rotas a um agente **sonnet**; a sintese, a autoria de SQL, o harness de paridade, o cache e a logica de sessao feitos em **opus**. Cada fase foi commitada + enviada ao GitHub como ponto de restauracao, com o plano atualizado a cada passo para ser resumivel se a sessao/tokens acabassem.

## Verificacao

Paridade das RPCs == JS antigo confirmada contra producao (harness em scratchpad, mantido fora do repo). `npx tsc --noEmit`, `npm run build`, `npm run lint` limpos a cada fase. Usuario validou localmente (dashboard/clientes/vendedores/importar + login/logout + fechar-e-reabrir navegador) e aprovou. Deploy pelo runbook: `git status` limpo, `npm ci`/lint/tsc/build, `npm run deploy:cloudflare` (Worker version `59851c56`, binding `rito_cache` confirmado), smoke test `/login` 200 e `/` -> 307. Migracao aplicada ao Supabase de producao via Management API (dev usa o mesmo banco de producao).
