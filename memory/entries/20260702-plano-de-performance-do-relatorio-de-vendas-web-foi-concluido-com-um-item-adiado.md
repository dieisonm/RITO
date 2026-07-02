---
id: "20260702-plano-de-performance-do-relatorio-de-vendas-web-foi-concluido-com-um-item-adiado"
project: "RITO"
type: "decision"
status: "active"
title: "Plano de performance do Relatorio de Vendas web foi concluido, com a camada de cache adiada de proposito"
summary: "Alem dos 3 quick wins ja registrados, a paginacao sequencial de sales_transactions e clients foi trocada por busca em paralelo (parity 100% validada contra dados reais) e as dependencias nao usadas pg/unpdf foram removidas. Tudo foi implantado em producao e validado. A reescrita para agregacao SQL completa e a camada de cache entre requisicoes foram avaliadas e conscientemente adiadas: exigiriam reimplementar logica de negocio complexa (comparacao de periodo anterior, clientes novos/recorrentes/inativos, alertas) e uma camada de invalidacao de cache corretas demais para justificar risco autonomo numa ferramenta financeira sem testes automatizados."
why: "Conclui a execucao do plano aprovado em 20260702-auditoria-de-performance-do-relatorio-de-vendas-web-identifi e 20260702-quick-wins-de-performance-do-relatorio-de-vendas-web-foram-implantados. O usuario autorizou execucao autonoma completa comecando pelos quick wins; este registro documenta onde a autonomia foi conscientemente limitada e por que."
source: "claude-code-session"
created_at: "2026-07-02T00:00:00-03:00"
updated_at: "2026-07-02T00:00:00-03:00"
tags: ["relatorio-vendas","performance","cloudflare-workers","supabase","pagination","cache","sql-aggregation"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/src/lib/pagination.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/legacy-data.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/database-data.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/commission-report.ts","S:/RITO/Projetos/relatorio-vendas-web/src/app/api/clientes/route.ts","S:/RITO/Projetos/relatorio-vendas-web/package.json"]
related_ids: ["20260702-auditoria-de-performance-do-relatorio-de-vendas-web-identifi", "20260702-quick-wins-de-performance-do-relatorio-de-vendas-web-foram-implantados", "20260702-relatorio-de-vendas-web-esta-em-producao-com-cloudflare-e-supabase"]
issue: ""
pr: ""
commit: ""
---

## O que foi feito nesta etapa

Criado `src/lib/pagination.ts` com `fetchAllPages()`: busca a primeira pagina com `count: "exact"`, calcula quantas paginas faltam e busca todas em paralelo com `Promise.all` em vez de um loop sequencial `while`/`for`. Aplicado nos 4 pontos que paginavam tabelas inteiras: `legacy-data.ts` (`getLegacyDashboard`, usado por `/`, `/clientes`, `/vendedores`, `/importar`), `database-data.ts` (`getDatabaseAnalyticsSource`, usado por `/analises`), `src/app/api/clientes/route.ts` (`fetchClients`) e `commission-report.ts` (`getCommissionReportData`, gerador de XLSX).

**Validacao de correcao**: script standalone comparou os resultados da busca paralela contra a busca sequencial antiga direto no Supabase remoto de producao — `clients: 1522 = 1522` e `sales_transactions: 6393 = 6393`, com os mesmos IDs em ambos os conjuntos. Sem perda ou duplicacao de linhas. Tempo de busca da tabela de transacoes caiu de ~3.36s para ~1.79s mesmo a partir de uma maquina fora da regiao do Supabase; o ganho tende a ser proporcionalmente maior a partir do Worker (que agora roda colocado com o Supabase gracas ao Smart Placement).

**Housekeeping**: removidas as dependencias `pg` e `unpdf` de `package.json` (confirmado sem nenhum import em `src/` ou `scripts/`); `npm install` removeu 15 pacotes transitivos.

Todos os itens foram implantados em `https://rito.relatorio-vendas.workers.dev` com `npx tsc --noEmit` e `npm run build` limpos antes de cada deploy, seguidos de smoke test em producao (`/login` 200, `/`, `/clientes`, `/analises` com `307` para usuario nao autenticado).

## O que foi avaliado e adiado de proposito

1. **Agregacao SQL completa** (item originalmente listado no plano): ao ler `legacy-data.ts` e `commission-report.ts` por inteiro, a "agregacao em JS" nao e um simples `SUM`/`GROUP BY` — inclui comparacao com periodo anterior dinamico, calculo de clientes novos/recorrentes/inativos por diferenca de conjuntos, participacao percentual, "clientes com mais de um documento" e geracao de alertas por limiar. Reescrever isso como views/RPC do Postgres é viavel, mas é um projeto proprio, arriscado de fazer sem suite de testes numa ferramenta que already alimenta pagamento de comissao. Recomendacao: tratar como proxima fase, com paridade validada por comparacao de resultados (como foi feito aqui para a paginacao) antes de substituir a logica em JS.
2. **Camada de cache entre requisicoes**: o adaptador OpenNext no Cloudflare Worker (`open-next.config.ts`) esta com configuracao padrao, sem KV vinculado — ou seja, `unstable_cache`/revalidate do Next nao persistem entre invocacoes do Worker hoje. Adicionar isso exigiria criar um KV namespace, vincular no `wrangler.jsonc`, e o mais importante: implementar invalidacao correta em toda mutacao (`api/clientes`, `api/vendedores`, `api/empresas`), porque esta e uma ferramenta admin com escrita frequente — cache desatualizado mostrando dados antigos apos uma edicao seria um bug pior que a lentidao atual. Adiado ate o usuario decidir o nivel de staleness aceitavel.

## Proximos passos sugeridos (nao executados)

1. Login real e navegacao autenticada ainda precisam de confirmacao manual do usuario — nao ha credenciais de teste disponiveis para o agente validar o caminho autenticado ponta a ponta.
2. Se a lentidao persistir apos estas mudancas, o proximo suspeito e a agregacao SQL (item 1 acima), nao infraestrutura adicional.
3. KV cache so deve entrar depois que o fluxo de confirmacao/gravacao de importacao (ainda pendente, ver `docs/current-state.md`) estiver pronto, para desenhar a invalidacao junto com o novo fluxo de escrita.
