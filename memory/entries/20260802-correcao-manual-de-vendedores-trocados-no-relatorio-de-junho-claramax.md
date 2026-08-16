---
id: "20260802-correcao-manual-de-vendedores-trocados-no-relatorio-de-junho-claramax"
project: "RITO"
type: "operation"
status: "active"
title: "Correcao manual: vendedores ANDRE/OBERDAN trocados no relatorio de comissao de junho/2026 (4 clientes CLARAMAX)"
summary: "O relatorio de comissao de JUNHO/2026 da CLARAMAX tinha ANDRE e OBERDAN trocados para 4 clientes: codigos 6561 (CLA DISTRIBUIDORA), 9073 (TANIA MARIA DOS SANTOS) e 7712 (TOMAFEL) apareciam com ANDRE mas deveriam ser OBERDAN; 7317 (MUNDO DA LIMPEZA) aparecia com OBERDAN mas deveria ser ANDRE. Em todos, julho e o current_vendor_id ja estavam corretos — so o mes de junho estava trocado. Corrigidas 24 transacoes de junho (sales_transactions.vendor_id) via SQL direto na Management API do Supabase, com o estado anterior salvo para reversao. O relatorio le sales_transactions.vendor_id (congelado na importacao) e NAO usa cache (no-store), entao a correcao aparece imediatamente ao regerar."
why: "Cliente do usuario pediu para corrigir vendedores no relatorio mais recente e nao havia opcao na tela (a edicao inline ainda nao foi construida — ver plano). Feito como correcao pontual para desbloquear. Escolhido escopo cirurgico (so as linhas de junho) porque julho e os vendedores-padrao dos clientes ja estavam certos; o objetivo era apenas o relatorio de junho."
source: "claude-code-session"
created_at: "2026-08-02T00:00:00-03:00"
updated_at: "2026-08-02T00:00:00-03:00"
tags: ["relatorio-vendas","comissao","correcao-manual","dados","vendedor","claramax"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/src/lib/commission-report.ts","S:/RITO/Projetos/relatorio-vendas-web/src/app/api/relatorios/comissao/route.ts"]
related_ids: ["20260802-relatorio-vendas-tres-correcoes-criticas-de-importacao-e-comissao","20260802-plano-de-edicao-de-vendedor-no-relatorio-de-comissao-e-workbook-de-setup"]
issue: ""
pr: ""
commit: ""
---

## O que foi feito

Update direto em `sales_transactions.vendor_id` restrito a `effective_date` entre 2026-06-01 e 2026-06-30 para os 4 clientes:

- 6561 CLA DISTRIBUIDORA -> OBERDAN (8 linhas, R$1.110,09)
- 9073 TANIA MARIA DOS SANTOS -> OBERDAN (8 linhas, R$334,68)
- 7712 TOMAFEL -> OBERDAN (3 linhas, R$89,04)
- 7317 MUNDO DA LIMPEZA -> ANDRE (5 linhas, R$310,51)

Total: 24 linhas. Estado anterior (em junho os tres primeiros estavam em ANDRE e o 7317 em OBERDAN) foi capturado antes do update para permitir reversao exata.

## Como o relatorio atribui vendedor (importante para o futuro)

O relatorio de comissao (`getCommissionReportData` em `commission-report.ts`) credita cada linha pelo `sales_transactions.vendor_id` CONGELADO no momento da importacao — nao pelo vendedor atual do cliente. Consequencias:

- Mudar o vendedor do cliente na tela /clientes so afeta importacoes FUTURAS; nao corrige um relatorio ja gerado.
- Linhas com vendedor nulo sao DESCARTADAS do relatorio (comissao invisivel).
- A rota manda `Cache-Control: no-store` e `getCommissionReportData` nao tem cache -> qualquer correcao aparece na hora ao regerar.

## Ponto em aberto (nao explicado)

Existem transacoes CLARAMAX com `effective_date` em junho E julho/2026, mas NENHUMA importacao CLARAMAX de junho/julho aparece na tabela `imports` (a ultima foi a de maio, `temp145753043.xlsx`). Vale rastrear como esses dados entraram, ja que junho entrou justamente com os vendedores trocados.
