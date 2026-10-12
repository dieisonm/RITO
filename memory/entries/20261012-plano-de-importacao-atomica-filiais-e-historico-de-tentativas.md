---
id: "20261012-plano-de-importacao-atomica-filiais-e-historico-de-tentativas"
project: "RITO"
type: "plan"
status: "active"
title: "Importacao: preservar filiais por codigo, rollback completo e historico de tentativas; ignorar blocos e 1,5%"
summary: "Usuario reafirmou 10309/10310 como filiais distintas mesmo com nome igual, regra ja registrada em julho. Investigacao confirmou OR por nome nas acoes em massa da preview que copia resolucao/clientId entre codigos, reproduzido com codigo real em memoria. Confirmacao usa duas RPCs separadas; propor orquestradora unica para cadastro, carteira, aliases, retroatividade e movimentos, com rollback integral. Planejar tentativas consultaveis, log fora da transacao de negocio, idempotencia/status para timeouts e mensagens claras. Headers de blocos CLARAMAX e abatimento de 1,5% devem continuar ignorados: vendedor escolhido pelo usuario e calculo do abatimento manual. Apenas plano/docs nesta etapa, sem alteracao funcional ou de dados."
why: "Usuario pediu investigar atomicidade e historico, esclareceu que filiais nao devem ser fundidas e rejeitou implementar tratamento de blocos/abatimento."
source: "codex; instrucao direta do usuario; leitura do codigo e reproducao em memoria"
created_at: "2026-10-12T00:00:00-03:00"
updated_at: "2026-10-12T00:00:00-03:00"
tags: ["relatorio-vendas", "importacao", "filiais", "atomicidade", "logs", "plano"]
related_ids: ["20260703-clientes-com-mesmo-nome-e-codigos-diferentes-sao-filiais-distintas-nunca-fundir", "20261012-reversao-dos-efeitos-parciais-da-importacao-claramax"]
---

Plano tecnico canonico no repo do app:
`docs/import-integrity-plan.md`. Estado resumido: `docs/current-state.md`.

## Decisoes que prevalecem

- Identidade de cliente por empresa/codigo; codigos diferentes com nome igual
  sao clientes diferentes. Nunca consolidar 10309 e 10310. Nome so quando
  arquivo nao tem codigo, com tolerancia existente a zeros/guarda de colisao.
- Headers/separadores de blocos nao determinam vendedor. Usuario classifica.
- Ignorar abatimento 1,5%; nao inferir imposto. Essa decisao encerra a duvida
  registrada na investigacao/reversao anterior; nao e feature pendente.
- Falha deve reverter todas as escritas de negocio, incluindo retroatividade.
  Log de tentativa pode persistir fora desse rollback para explicar a falha.

## Achados novos

`runMassAssign` e `applyMassNoVendor` em `import-preview.tsx` fazem OR por
nome, propagando `clientId`/`newClient` entre filiais. Reproducao com funcoes
reais em memoria: selecionar 10309 copia seu ID para a linha 10310. Explica
um mecanismo para a divergencia legado, mas nao prova o clique historico.
API/RPC precisam revalidar codigo e empresa, inclusive em ramos com mode.

`apply_vendor_resolutions` pode gravar clientes, fechar/deletar vinculos,
mudar carteira, reatribuir movimentos antigos e aliases. `confirm_import`
separada nao reverte esses efeitos. Nova RPC pode envolver ambas na mesma
transacao PostgreSQL sem consultas HTTP por linha. Cache so apos commit.

Historico atual so lista imports concluidos; log tecnico so captura catch,
nao retornos antecipados, e helper nao confere error do insert Supabase.
Proposta: tentativas com IDs, etapas, estados, import_id, motivo legivel,
detalhe admin-only e refresh. Sucesso registrado na transacao da RPC; erro
confirmado registrado apos rollback. Timeout requer consultar status:
nao afirmar "nada salvo" sem saber se a transacao concluiu.

Nao foram alterados parser, rotas, UI, RPCs, banco ou deploy nesta investigacao.
Reparo de vinculo legado e implementacao devem ser tratados como proximos
passos; a reversao operacional de 12/10 ja foi concluida separadamente.
