---
id: "20261012-classificacao-em-massa-corrigida-no-codigo-sem-deploy"
project: "RITO"
type: "operation"
status: "completed"
title: "Correcao implementada: classificacao em massa preserva filiais e API valida identidade; deploy pendente"
summary: "A pedido do usuario, corrigidas as duas acoes em massa da importacao: sameImportClient impede agrupar codigos/IDs diferentes por nome e cada linha constroi sua propria resolucao, sem copiar clientId/newClient de outra filial. API valida todas as resolucoes antes de qualquer RPC de negocio, incluindo modos futuro/retroativo, rejeitando cliente de outra empresa/filial ou novo codigo diferente da origem. Regressao com UI e rota reais em memoria passou, assim como tsc e build; lint sem erros (14 avisos preexistentes em pdf-polyfills). Codigo/docs compartilhados pelo Git. Sem deploy, migration ou correcao de dados nesta etapa; RPC unica, historico e reparo legado continuam pendentes."
why: "Usuario pediu corrigir o erro grave de salvar classificacao/cadastro de uma filial em outra, apos confirmar a regra de codigos distintos mesmo com nome igual."
source: "codex; implementacao e testes locais sem escrita no Supabase"
created_at: "2026-10-12T00:00:00-03:00"
updated_at: "2026-10-12T00:00:00-03:00"
tags: ["relatorio-vendas", "importacao", "filiais", "correcao", "regressao", "deploy-pendente"]
commit: "32c2b28"
related_ids: ["20261012-plano-de-importacao-atomica-filiais-e-historico-de-tentativas", "20261012-reversao-dos-efeitos-parciais-da-importacao-claramax"]
---

Arquivos do app: `src/lib/import-client-identity.ts`,
`src/components/import-preview.tsx`, `src/app/api/importar/confirmar/route.ts`.
Teste: `npm run test:import-identity` (script versionado em scripts/).

Regressao cobre nomes iguais/codigos distintos; IDs distintos; zeros a esquerda
com guarda de IDs; fallback de nome apenas sem codigo; nao copiar cadastro nas
duas acoes em massa; recusas da rota sem RPCs de negocio para classificacao
cruzada, outra empresa e criacao com identidade errada, incluindo futuro e
retroativo; confirmacao legitima ainda funciona com I/O simulado.

Nao considerar a producao corrigida antes do deploy. Esta entrega nao resolve
a falta de transacao unica, a dedup por chave original nem o vinculo legado
10310/10309. Nao reenviar o arquivo problematico ate tratar essas pendencias.
Plano atualizado em `docs/import-integrity-plan.md` e `docs/current-state.md`.
