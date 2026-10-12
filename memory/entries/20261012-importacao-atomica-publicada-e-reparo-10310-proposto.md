---
id: "20261012-importacao-atomica-publicada-e-reparo-10310-proposto"
project: "RITO"
type: "operation"
status: "completed"
title: "Rollback automatico da importacao publicado; reparo da filial 10310 apenas proposto"
summary: "Implementada confirm_import_atomic, envolvendo cadastro, vinculos, carteira, aliases, retroatividade, imports e movimentos em uma transacao. Teste SQL com falha forcada no insert confirmou rollback integral por fingerprints; fixtures e primeira execucao da migration foram revertidas no teste. Depois migration aplicada e Worker be42c1e0-62a2-45c6-bb33-ccac49fd15fa publicado, incluindo fix da classificacao em massa. Rota mostra motivo e rollback confirmado; conexao perdida nao afirma que nada foi salvo. Reparo de dados 10309/10310 NAO executado: 10309 tem dois movimentos, um pertence a origem 10310; destino 10310 precisa ser criado, mantendo filiais distintas e transferindo so client_id do movimento errado."
why: "Usuario pediu implementar rollback automatico e listar os dados a alterar para o reparo das filiais, sem autorizar esse reparo ainda."
source: "codex; testes locais e SQL revertido; Supabase e deploy Cloudflare"
created_at: "2026-10-12T00:00:00-03:00"
updated_at: "2026-10-12T00:00:00-03:00"
commit: "5e723a1"
tags: ["relatorio-vendas", "importacao", "rollback", "atomicidade", "cloudflare", "filiais"]
related_ids: ["20261012-plano-de-importacao-atomica-filiais-e-historico-de-tentativas", "20261012-classificacao-em-massa-corrigida-no-codigo-sem-deploy", "20261012-reversao-dos-efeitos-parciais-da-importacao-claramax"]
---

## Implementado e publicado

Migration `20261012000001_atomic_import.sql`; nova RPC service_role-only,
serializacao por empresa, validacao de cadastro/empresa/codigo/vendedor no
banco. Rota HTTP faz uma unica RPC de negocio, invalidando cache apos commit.
Log fora da transacao registra fase/rollback e confere falha do insert.
Mensagens de duplicidade, classificacao, data invalida, FK e timeout SQL
explicam rollback. Perda de resposta HTTP informa resultado desconhecido e
orienta conferir historico; nao promete rollback de transacao ja commitada.

Testes: `npm run test:import-identity`, tipos/build e lint sem erros (14 avisos
preexistentes em pdf-polyfills). Teste de integracao em
`scripts/test-atomic-import.sql`, com migration prepended e excecao final:
clientes novos, vinculos removidos/fechados, carteira, transacoes retroativas
e aliases sao todos restaurados em falha forcada; sucesso e privilegios
tambem testados. Nenhuma fixture permaneceu no banco. Migration posteriormente
aplicada de forma persistente e reconhecida pela API REST.

Publicado no Worker `rito`, versao `be42c1e0-62a2-45c6-bb33-ccac49fd15fa`,
https://rito.relatorio-vendas.workers.dev. Esta entrega inclui a correcao
de filiais `32c2b28` que anteriormente aguardava deploy. Sem importacao real
de teste ou reparo de movimentos reais nesta etapa.

## Reparo proposto, nao executado

Na CLARAMAX, cadastro 10309 tem 2 movimentos; origem de um deles indica 10310.
10310 nao existe apos a reversao dos efeitos da tentativa de 10/10. Proposta:
criar cadastro/vinculo da filial 10310 e mover apenas o client_id desse
movimento, preservando documento, valor, datas, vendedor, import_id e chave
original. Manter 10309 e seu movimento legitimo, sem fusao/renumeracao.
Detalhes foram consultados para apresentar ao usuario; executar somente
apos autorizacao para esse reparo especifico e com backup/auditoria.

Backlog ainda aberto: historico consultavel de tentativas, dedup considerando
a chave original e reparo legado. Ignorar headers dos blocos e abatimento
1,5% continua sendo a regra aprovada.
