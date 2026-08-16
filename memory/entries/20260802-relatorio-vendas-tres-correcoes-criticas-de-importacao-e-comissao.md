---
id: "20260802-relatorio-vendas-tres-correcoes-criticas-de-importacao-e-comissao"
project: "RITO"
type: "fix"
status: "active"
title: "Relatorio de Vendas web: 3 correcoes criticas de importacao/comissao publicadas (subrequests, zeros a esquerda, paginacao de clientes)"
summary: "Publicado o Worker 5cc2f97e com tres correcoes independentes. (1) 'Too many subrequests by single Worker invocation' ao salvar importacao e no ajuste em massa de vendedor: a gravacao de cliente/vendedor era um laco por cliente (4-9 consultas Supabase cada) e um arquivo CLARAMAX grande (centenas de clientes) estourava o limite de subrequests por invocacao do Cloudflare Worker; trocado por uma unica RPC set-based apply_vendor_resolutions (migration 20260802000002), atomica e em uma so subrequest. (2) Correspondencia de codigo de cliente tolerante a zeros a esquerda: o relatorio CLARAMAX escreve codigos com zero a esquerda (01649) e a base guarda sem zero (1649), entao a correspondencia exata falhava em quase todas as linhas de uma importacao real; normalizeCode em import-dedup.ts agora casa os dois (match exato primeiro, depois normalizado), com guarda de colisao. (3) Consulta de clientes paginada nas rotas de importacao: o fetch de clientes era um .select() sem paginacao, limitado a 1000 pelo PostgREST, e CLARAMAX ja tem 1132 clientes -> os ~132 excedentes sumiam do matcher e as linhas apareciam como 'sem vendedor'."
why: "Bugs reais reportados pelo usuario a partir de um arquivo CLARAMAX de producao. Os tres se manifestavam no mesmo fluxo (importar/gerar comissao) e, se nao corrigidos, o salvamento falhava por completo (1) ou criava clientes duplicados e duplicava transacoes (2 e 3). Sao a base de comissao paga, entao a correcao foi validada contra dados reais antes de publicar."
source: "claude-code-session"
created_at: "2026-08-02T00:00:00-03:00"
updated_at: "2026-08-02T00:00:00-03:00"
tags: ["relatorio-vendas","cloudflare-workers","supabase","importacao","matching","subrequests","pagination","comissao","postgrest"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/supabase/migrations/20260802000002_bulk_apply_vendor_resolutions.sql","S:/RITO/Projetos/relatorio-vendas-web/src/lib/import-dedup.ts","S:/RITO/Projetos/relatorio-vendas-web/src/app/api/importar/confirmar/route.ts","S:/RITO/Projetos/relatorio-vendas-web/src/app/api/importar/preview/route.ts","S:/RITO/Projetos/relatorio-vendas-web/src/app/api/clientes/mass-vendor/route.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/vendor-assignment.ts"]
related_ids: ["20260702-relatorio-de-vendas-web-esta-em-producao-com-cloudflare-e-supabase","20260802-correcao-manual-de-vendedores-trocados-no-relatorio-de-junho-claramax","20260802-plano-de-edicao-de-vendedor-no-relatorio-de-comissao-e-workbook-de-setup"]
issue: ""
pr: ""
commit: "189c142, 1fdb250, 85965c5"
---

## 1. "Too many subrequests" na gravacao (commit 189c142)

`confirmar/route.ts` e `clientes/mass-vendor/route.ts` resolviam cliente + atribuicao de vendedor em um laco por cliente, cada iteracao disparando 4-9 consultas Supabase (cada consulta = 1 subrequest do Worker). Uma importacao CLARAMAX grande, ou um ajuste em massa com muitos clientes, multiplicava para 1000+ subrequests numa unica invocacao e batia no teto do Cloudflare -> o salvamento falhava e nada era gravado.

Correcao: nova RPC set-based `apply_vendor_resolutions(company, resolutions jsonb)` (migration `20260802000002`) faz todo o lote dentro do Postgres, atomico e em UMA subrequest, espelhando fielmente `applyClientAndVendorAssignment` (auto-codigo, valid_from future/retroactive, fechar/superar atribuicoes abertas, current_vendor_id, reescrita retroativa, alias). As duas rotas passam a chamar a RPC uma vez; a rota single-client `atribuir-vendedor` mantem o helper JS (sempre <=1 cliente, seguro). Validado 11/11 contra dados reais em transacoes revertidas (BEGIN ... raise exception 'VRESULT:%' ... rollback) antes de publicar.

**Licao durável: nunca fazer laco por entidade com varias consultas cada dentro de uma rota do Worker — batch em uma RPC set-based do Postgres.**

## 2. Codigo tolerante a zeros a esquerda (commit 1fdb250)

O relatorio CLARAMAX escreve o codigo do cliente com zero a esquerda em 5 digitos (`01649 - FORTPEL...`); a base foi semeada com o mesmo codigo sem zero (`1649`). A correspondencia exata falhava em ~todas as linhas de uma importacao real: preview mostrava tudo como novo/sem vendedor, e um salvamento criaria clientes duplicados com codigo com zero + duplicaria todas as transacoes.

Correcao em `import-dedup.ts`: `matchClient` tenta match EXATO por codigo primeiro (mantem a regra de filiais estrita) e so entao cai no match por `normalizeCode` (tira zeros a esquerda de codigos puramente numericos; codigos alfanumericos como AUTO-BISCO-0001 ficam intactos). `buildClientMatchers` indexa por codigo normalizado com **guarda de colisao**: se dois clientes distintos normalizam para o mesmo codigo, aquela chave e removida do indice normalizado (nunca funde filiais reais). Validado: 0 colisoes em todas as empresas; o arquivo problematico foi de ~0 para 259/259 clientes casados.

## 3. Paginacao da consulta de clientes (commit 85965c5)

Depois do item 2, ainda sobravam ~113 linhas "sem vendedor". Causa: o fetch de clientes nas rotas `importar/preview` e `importar/confirmar` era um `.select().eq()` sem paginacao -> PostgREST limita silenciosamente a 1000 linhas, e CLARAMAX ja tem 1132 clientes, entao ~132 sumiam do matcher. Reproduzido fielmente pelo endpoint REST (que aplica o teto de 1000 como o supabase-js): com teto -> 114 linhas sem vendedor; paginado -> 0. Correcao: ambas as rotas passam a usar `fetchAllPages<DedupClient>` (mesmo helper que a dedup de transacoes ja usava).

**Licao durável: qualquer `.select()` por empresa que possa passar de 1000 linhas TEM que usar `fetchAllPages`.**

## Estado

Worker de producao: `5cc2f97e` (`https://rito.relatorio-vendas.workers.dev`). `tsc`/`lint`/`build` limpos e smoke test pos-deploy (`/login` 200, `/` 307) em cada publicacao. Estado detalhado versionado em `docs/current-state.md` do repo relatorio-vendas-web.
