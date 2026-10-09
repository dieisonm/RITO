---
id: "20261009-relatorio-vendas-estado-revisado-e-pendencias"
project: "RITO"
type: "operation"
status: "active"
title: "Relatorio de vendas: documentacao reconciliada com edicao de vendedor, repasses, Clientes e banco reativado"
summary: "Revisao de 09/10/2026 confirmou master/origin/master em 5e48271. Edicao de vendedor (17d30be), taxas com vigencia e snapshots de repasse (a105c6d), Clientes Presente/Historico e RLS de error_logs ja existem. Supabase xnjblqigsvnyuyfklcud foi restaurado de INACTIVE para ACTIVE_HEALTHY; Auth e leitura REST retornaram 200. Banco possui 32 importacoes, 11823 movimentos, 1616 clientes, 6 vigencias, 5 repasses e 1 auditoria. Docs antigos corrigidos; pendencias reais incluem homologacao financeira, reatribuicao atomica, aviso de exclusoes por taxas ausentes, acesso seller e menu mobile. Nao houve teste autenticado de ponta a ponta nem deploy nesta revisao."
why: "O usuario pediu revisar o app e atualizar documentacao/memoria antes de discutir proximos passos; os docs ainda tratavam features implementadas como pendentes e a memoria entre computadores estava incompleta."
source: "codex; codigo Git; APIs Supabase/Cloudflare somente leitura na auditoria"
created_at: "2026-10-09T00:00:00-03:00"
updated_at: "2026-10-09T00:00:00-03:00"
tags: ["relatorio-vendas", "comissao", "repasse", "analytics", "supabase", "documentacao", "retomada"]
files: ["Projetos/relatorio-vendas-web/docs/current-state.md", "Projetos/relatorio-vendas-web/docs/comissao-edit-vendor-plan.md", "Projetos/relatorio-vendas-web/docs/local-setup.md", "Projetos/relatorio-vendas-web/docs/deployment-runbook.md"]
related_ids: ["20260802-plano-de-edicao-de-vendedor-no-relatorio-de-comissao-e-workbook-de-setup", "20260721-analises-revamp-panorama-e-clientes-com-rpcs-sql-e-recharts", "20260816-env-local-do-relatorio-vendas-web-restaurado-neste-mac", "20260816-backup-do-env-local-do-relatorio-vendas-web-no-google-drive-rito-excecao"]
issue: ""
pr: ""
commit: "5e48271"
---

## Fonte para retomar

- App: `dieisonm/relatorio-vendas-web`, `master`, codigo-base revisado `5e48271`.
- Memoria compartilhada: `dieisonm/RITO`, `main`, `memory/entries/*.md`.
- Ambos alinhados aos remotos apos fetch nesta revisao. `docs/current-state.md`
  do app e o retrato canonico; propostas e auditorias antigas sao historicas.
- Documentacao reconciliada no app em `514a70f` (somente README/docs),
  compartilhada na `master`; codigo funcional revisado continua `5e48271`.
- Mac: `/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web`.
  `.env.local` fica na raiz, ignorado no Git. Backup privado aprovado no Drive
  `RITO/secrets/relatorio-vendas-web/.env.local`, conta
  `dieison.medinger@gmail.com`; pasta:
  https://drive.google.com/drive/folders/1lg992LnNDrB4tm0h-hA5D26GZAX0_d9v.
  A pasta Drive nao foi reinspecionada nesta auditoria; o local foi confirmado
  na restauracao de agosto. Nao registrar valores de segredos.
- Windows: app `S:/RITO/Projetos/relatorio-vendas-web`; memoria
  `S:/RITO/Automations/RITO/memory`. Novos clones: disco local sem sync;
  clone atual do Mac continua dentro do OneDrive.

## Ja implementado

- Importacao com preview somente leitura, confirmacao, deduplicacao, cliente/
  vendedor e gravacao transacional. Correcoes de paginacao, zeros a esquerda
  e RPC em lote evitam perder clientes ou estourar subrequests.
- `/comissoes`: selecao e reatribuicao sem reimportar, auditoria e refresh.
  O padrao tambem atualiza o vendedor do cliente para futuras importacoes;
  "so para esse relatorio" opta por alterar apenas os movimentos selecionados.
  API aceita 2000 IDs por chamada; UI divide selecoes maiores.
- Taxas em `vendor_commission_rates`, com vigencias por vendedor e mudancas
  retroativas. `amount` e comissao da representacao, nao venda. Repasse deriva
  a venda pela taxa da representacao e aplica a taxa do vendedor na data de
  cada movimento; movimento proprio da representacao tem repasse zero.
- `/repasse-vendedores`: periodo ate 366 dias, snapshot salvo por vendedor/
  empresa, reabertura dos ultimos 50. Mudar taxas ou movimentos nao altera
  os valores de um snapshot ja salvo.
- `/analises`: Panorama e Clientes conectadas; Clientes separa Presente
  (recencia desde o ultimo dado, 60/90 dias por padrao) e Historico (periodo).
  RPCs SQL + cache KV, graficos no browser e sessao com timeout local.
- Provisionamento Auth de vendedores ja existe; perfil seller inicia inativo.
  A protecao do app ainda exige admin: ativar seller nao cria a tela restrita.
- RLS em `error_logs` foi confirmado no banco, assim como nas demais 10
  tabelas selecionadas na auditoria.

## Producao observada em 09/10/2026

- Supabase `xnjblqigsvnyuyfklcud`: restaurado a pedido do usuario de INACTIVE
  para ACTIVE_HEALTHY nesta sessao. Auth/REST: 200; Cloudflare `/login`: 200;
  API protegida sem sessao: 401 esperado. Plano gratuito pode pausar por baixa
  atividade ao longo de 7 dias; politica:
  https://supabase.com/docs/guides/platform/free-project-pausing.
- Worker `rito`, https://rito.relatorio-vendas.workers.dev:
  ultimo deploy informado pela API `4f61f709-b8e8-47de-b2d2-c2749ee25894`,
  `2026-08-18T00:26:30.223831Z`. Metadata nao prova equivalencia integral do
  bundle remoto com o HEAD; nao foi feito novo deploy nesta revisao.
- Banco, leitura somente: 3 empresas, 4 vendedores, 1616 clientes,
  32 importacoes, 11823 movimentos (01/09/2025 a 30/09/2026), 6 vigencias,
  5 snapshots de repasse e 1 auditoria de reatribuicao. Tabelas novas e RPCs
  de recencia, taxas, repasse e atribuicao existem.
- Nao foram feitos login de usuario, salvamento de relatorio ou teste de
  valores financeiros na interface. Dados existentes nao provam homologacao.

## Pendencias para discutir (nao executar automaticamente)

1. Homologar comissoes, reatribuicao, vigencias e repasses contra mes conhecido.
2. Reatribuicao hoje e multietapas: movimentos, carteira por empresa, auditoria
   e cache nao compartilham uma transacao. Discutir atomicidade.
3. Sem taxa vigente, comissoes mostra repasse vazio; RPC de repasse exclui as
   linhas e emite NOTICE no banco, sem aviso de exclusao visivel na UI.
   Movimentos sem vendedor sao omitidos do gerador de comissoes. Discutir
   cobertura e transparencia antes de confiar no total como completo.
4. Experiencia seller restrita por carteira; menu mobile abaixo de 1280px;
   revalidacao de acessibilidade. Clientes ja existe, precisa de validacao
   de UX/regra, nao de construir a aba do zero.
5. Preservar a regra CAMNPAL: codigos diferentes com mesmo nome sao filiais
   distintas; nao consolidar sem decisao expressa do cliente.
6. Disponibilidade/backups Supabase e eventual problema de symlinks Windows.

## Como compartilhar sem deploy

Docs e codigo vao no Git do app; memoria no Git RITO. Stage explicito dos
caminhos documentais; nao usar add -A. Push de memory/** nao dispara o
workflow Hostinger, que filtra site/**, logos/**, scripts/build_dist.sh e o
proprio workflow. O repo do app nao tem workflow GitHub versionado nesta
revisao; deploy canonico e manual (`npm run deploy:cloudflare`). Atualizar
memoria/docs nao requer deploy. Nunca comitar env, dados pessoais ou imports.
