---
id: "20261012-reversao-dos-efeitos-parciais-da-importacao-claramax"
project: "RITO"
type: "operation"
status: "completed"
title: "Revertidos os efeitos parciais da tentativa de importacao CLARAMAX de 10/10"
summary: "A pedido do usuario, revertidos apenas os efeitos de cadastro/classificacao das duas tentativas falhas de temp154742738.xlsx em 10/10/2026: 4 clientes novos sem movimentos removidos, 6 vinculos novos removidos e 2 vinculos anteriores reabertos. Teste com rollback passou antes da execucao atomica; verificacao posterior confirmou por contagem e fingerprint que os 11823 movimentos e as 32 importacoes permaneceram identicos, assim como os 2 clientes antigos. Cache Cloudflare invalidado. Backup completo privado e recibo salvos no clone local, fora do Git. Nenhum parser foi alterado, nenhum novo arquivo importado e nenhum deploy executado."
why: "A confirmacao grava cadastros/classificacao em uma RPC anterior a confirm_import; erro de duplicidade na segunda etapa deixou efeitos da primeira. O usuario autorizou especificamente a reversao."
source: "codex; Supabase Management API; verificacao antes/depois"
created_at: "2026-10-12T00:00:00-03:00"
updated_at: "2026-10-12T00:00:00-03:00"
tags: ["relatorio-vendas", "claramax", "importacao", "reversao", "atomicidade"]
related_ids: ["20261009-relatorio-vendas-estado-revisado-e-pendencias"]
---

## Evidencia e escopo

As duas tentativas de 10/10 as 17:07 (America/Sao_Paulo) falharam por chave
duplicada. Nao criaram imports nem movimentos; por isso nao aparecem no
historico de uploads concluidos. Ficaram 4 clientes sem movimentos e 6
vinculos novos; nos 2 clientes antigos o vendedor permaneceu o mesmo.
Reversao executada em um unico bloco transacional com guardas contra mudancas
posteriores e contra alteracao de vendas/imports. Os 2 clientes antigos
permaneceram intactos; seus vinculos de agosto foram reabertos. Total final:
1616 clientes, 11823 movimentos e 32 imports.

Backup privado (nao versionar ou enviar sem autorizacao):
`/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web/data/rollback/2026-10-12-import-failure/`.
Contem `snapshot.json`, `rollback.sql` e `receipt.json`. Snapshot preserva os
registros completos anteriores a reversao. `data/` e ignorado no Git.

## Problemas ainda abertos — nao corrigidos nesta operacao

- Movimento de origem 10310 vinculado ao cadastro 10309 na importacao anterior
  de 09/10; dedup reconstrui a chave pelo cadastro vinculado e nao reconhece
  a chave original persistida, causando colisao no banco. Precisa de decisao
  sobre o cliente correto e ajuste da deteccao, nao exclusao de todo o lote.
- Novo arquivo tem blocos 0067 (614 linhas, 39028.92) e 0099 (94 linhas,
  4791.66). Parser atual le 708 movimentos, soma 43820.58, sem perda de datas;
  nao preserva bloco e ignora abatimentos finais de 1.5%, cuja regra precisa
  ser confirmada. Nao atribuir esses blocos a vendedores por suposicao.
- Tornar cadastro/classificacao e confirmacao uma transacao unica. Revisar
  historico de tentativas, refresh apos sucesso e opcao de reverter imports.
- Nao reenviar o arquivo antes de tratar a colisao: a falha pode repetir
  efeitos parciais. Preservar a importacao anterior de 614 movimentos.
