---
id: "20260802-plano-de-edicao-de-vendedor-no-relatorio-de-comissao-e-workbook-de-setup"
project: "RITO"
type: "plan"
status: "active"
title: "Plano: edicao de vendedor direto no relatorio de comissao + workbook de setup local; estado detalhado migrado para docs/ do repo"
summary: "Especificada (nao construida) a feature de editar vendedor direto na pre-visualizacao do relatorio de comissao (/comissoes): coluna de checkbox como na tela de importacao, filtro por nome de cliente, paginacao no cliente para mostrar TODAS as linhas (hoje mostra so 40), acao em massa de vendedor, Salvar via NOVO endpoint set-based POST /reatribuir que atualiza sales_transactions.vendor_id em UMA query + opcional apply_vendor_resolutions para valer daqui pra frente + tabela de auditoria commission_vendor_edits + invalidateCache, depois refazer o fetch do preview. Escopo padrao = cirurgico (so as linhas selecionadas), com toggle opcional 'tambem definir como vendedor padrao do cliente'. Tambem escritos docs de onboarding para continuar o projeto em outro computador."
why: "O usuario quer poder corrigir vendedores errados sem re-importar (a correcao de junho/2026 teve que ser feita na mao no banco). E vai continuar o projeto em outra maquina, entao pediu que tudo importante ficasse documentado em git (que ele carrega antes de trabalhar). Detalhe critico descoberto: a memoria RITO versionada estava parada em 2026-07-02 — todo o arco do relatorio-vendas depois disso (fluxo de importacao, overhaul de UI, fix de CPU, revamp de analytics, e os fixes de hoje) so estava na auto-memoria local do Claude Code, nao neste git. Por isso o estado detalhado agora vive em docs/ do repo relatorio-vendas-web (que viaja no clone) e estas entradas registram o essencial na memoria RITO."
source: "claude-code-session"
created_at: "2026-08-02T00:00:00-03:00"
updated_at: "2026-08-02T00:00:00-03:00"
tags: ["relatorio-vendas","comissao","plano","documentacao","setup","onboarding"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/docs/comissao-edit-vendor-plan.md","S:/RITO/Projetos/relatorio-vendas-web/docs/local-setup.md","S:/RITO/Projetos/relatorio-vendas-web/docs/current-state.md"]
related_ids: ["20260802-relatorio-vendas-tres-correcoes-criticas-de-importacao-e-comissao","20260802-correcao-manual-de-vendedores-trocados-no-relatorio-de-junho-claramax"]
issue: ""
pr: ""
commit: "b38bb02"
---

## Feature planejada (spec completa no repo)

`docs/comissao-edit-vendor-plan.md` (no repo relatorio-vendas-web, commit b38bb02) tem a spec resumivel e retomavel. Resumo:

- Pre-visualizacao do relatorio vira tabela editavel: coluna 1 = checkbox (como na tela de importacao), filtro instantaneo por nome/codigo de cliente, **paginacao no cliente para mostrar TODAS as linhas** (hoje a API devolve so `sample = entries.slice(0,40)`), barra de acao em massa (escolher vendedor -> Aplicar).
- Salvar -> **novo endpoint set-based `POST /api/relatorios/comissao/reatribuir`**: `update sales_transactions set vendor_id = X where id in (...)` em UMA query (nunca laco por linha — licao do fix de subrequests); opcional `alsoSetClientDefault` chama `apply_vendor_resolutions`; grava auditoria; `invalidateCache()`; retorna N.
- Nova migration: tabela de auditoria `commission_vendor_edits` (quem mudou, de/para vendedor por transacao, para reversibilidade).
- Depois de salvar: **refazer o fetch do preview com os mesmos filtros** (relatorio e no-store -> mostra os totais corrigidos).
- Precisa adicionar `id` (sales_transactions.id) a cada entry do relatorio (hoje nao e selecionado).
- Ordem de build e perguntas em aberto (escopo padrao; incluir linhas sem vendedor?) estao na spec.

## Onboarding em outro computador

`docs/local-setup.md` (repo): clonar em disco LOCAL (nunca dentro de OneDrive/Google Drive — ja corrompeu git/node_modules aqui), `npm ci`, recriar `.env.local` (nomes das variaveis documentados; valores vem do password manager / copia segura, nunca commitados), `npm run dev`, gates de qualidade, aplicar migrations pela Management API, deploy. Regra de ouro: **dev local fala com o Supabase de PRODUCAO — nao ha banco local; escrita local e escrita em producao.** Scripts `tsx` que usam o alias `@/` precisam ficar na raiz do projeto.

## Estado canonico

`docs/current-state.md` (repo relatorio-vendas-web) foi atualizado para 02/08/2026 com os fixes de hoje e a correcao manual de junho. Esse arquivo + as entradas irma desta data sao a fonte para retomar o trabalho.
