---
id: "20260703-fluxo-de-confirmacao-e-gravacao-da-importacao-web-foi-implementado-e-publicado"
project: "RITO"
type: "decision"
status: "active"
title: "Fluxo de pre-visualizacao editavel + confirmacao/gravacao da importacao web foi implementado e publicado em producao"
summary: "A maior lacuna do app web em relacao ao app Windows (pendencias 1-3 de docs/current-state.md) foi fechada: a tela de importacao agora deixa o usuario resolver cliente/vendedor por linha (match, criacao de cliente, atribuicao futura ou retroativa com confirmacao em duas etapas), tudo em estado local no navegador, e so grava no banco (imports + sales_transactions, atomico via funcao Postgres confirm_import) quando o usuario clica em 'Salvar na base'. Nenhuma linha e omitida da tela independente da quantidade (limite de 300 linhas removido por exigencia explicita do usuario). Quatro bugs reais foram encontrados e corrigidos testando em producao (ver detalhe abaixo) e uma inconsistencia de cadastro de clientes CAMNPAL foi descoberta e parcialmente corrigida."
why: "O app Windows permitia resolver cliente/vendedor e confirmar a gravacao; o app web so tinha preview somente-leitura. O usuario testou em producao (banco real, ja que o dev local usa o mesmo Supabase de producao) e reportou cada bug conforme aparecia; todos foram corrigidos e reimplantados no mesmo dia."
source: "claude-code-session"
created_at: "2026-07-03T22:32:07-03:00"
updated_at: "2026-07-03T22:32:07-03:00"
tags: ["relatorio-vendas","importacao","supabase","cloudflare-workers","dedup","producao","data-quality"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/src/components/import-preview.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/app/api/importar/preview/route.ts","S:/RITO/Projetos/relatorio-vendas-web/src/app/api/importar/confirmar/route.ts","S:/RITO/Projetos/relatorio-vendas-web/src/app/api/clientes/atribuir-vendedor/route.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/vendor-assignment.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/import-dedup.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/pagination.ts","S:/RITO/Projetos/relatorio-vendas-web/src/lib/error-message.ts","S:/RITO/Projetos/relatorio-vendas-web/supabase/migrations/202607030001_import_confirm_workflow.sql","S:/RITO/Projetos/relatorio-vendas-web/docs/current-state.md"]
related_ids: ["20260702-relatorio-de-vendas-web-esta-em-producao-com-cloudflare-e-supabase", "20260702-fluxo-canonico-de-codigo-arquivos-e-deploy-do-relatorio-de-vendas"]
issue: ""
pr: ""
commit: "95b35ab,c3a541c,cd2ebab,35c6d86"
---

## O que foi construido

- Tabela `vendor_aliases` (por empresa, rotulo do relatorio -> vendedor) para sugerir vendedor a partir do texto do relatorio, sempre exigindo confirmacao explicita do usuario (nunca aplicada sozinha). Seed inicial: BISCOBOM "ADAO" -> "PANTHER".
- Funcao Postgres `confirm_import(...)` (security definer) que insere `imports` + todas as `sales_transactions` do lote numa unica transacao — atomicidade real, sem necessidade de transacao client-side no supabase-js.
- `src/lib/import-dedup.ts`: logica de match de cliente e calculo de chave de dedup extraida para um modulo unico, compartilhado entre a rota de preview (somente leitura) e a rota de confirmacao — evita que as duas divirjam silenciosamente.
- `src/lib/vendor-assignment.ts`: unico lugar que efetivamente cria cliente (com codigo auto-gerado `AUTO-{prefixo}-####` quando o relatorio nao traz codigo) e grava atribuicao de vendedor (com historico em `client_vendor_assignments`, incluindo reescrita retroativa opcional de `sales_transactions.vendor_id`).
- Abas "Sem vendedor" / "Com vendedor" na tela (troca por pedido do usuario, que nao gostou do filtro "somente pendentes" da primeira versao), selecao em massa com "aplicar vendedor" e "aceitar sugestao de vendedor".

## Bug critico: escrita imediata durante a preview

Descoberta do usuario: interagir com a preview (ex.: "aceitar sugestao de vendedor" em massa) estava gravando cliente/vendedor no banco **antes** do clique em "Salvar na base". Corrigido restruturando para que toda resolucao fique em estado React local (`resolutions`) e só as rotas `/api/importar/confirmar` (grava tudo) e o dry-run de `/api/clientes/atribuir-vendedor` (somente leitura, usado so para mostrar o impacto de uma reatribuicao retroativa antes do usuario decidir) toquem o banco.

## Bugs encontrados testando em producao (todos corrigidos e implantados)

1. **Hash do arquivo colidindo entre uploads diferentes**: `source_hash` era calculado depois do parser de PDF (pdfjs-dist) rodar — o parser destaca/consome o `ArrayBuffer` como efeito colateral, entao o hash acabava sendo o de um buffer vazio, identico para qualquer PDF da mesma empresa apos o primeiro salvamento. Corrigido calculando o hash antes do parse.
2. **Verificacao de "ja importado" sem paginacao**: a query de `sales_transactions` usava `.select()` simples do Supabase, que corta em ~1000 linhas por padrao. CAMNPAL passou de 1342 transacoes durante os testes e comecou a perder linhas dessa verificacao, fazendo dados ja salvos reaparecerem como "novos". Corrigido com o helper `fetchAllPages` (ja usado em outras partes do app).
3. **Chave de dedup priorizando o codigo cru do relatorio**: quando um cliente so casava por nome (codigo do relatorio diferente do codigo cadastrado), a chave de dedup ainda usava o codigo cru em vez do codigo real do cliente casado — a mesma linha ja salva reaparecia como "nova" para sempre. Corrigido priorizando o codigo do cliente casado.
4. **Check constraint de `client_vendor_assignments`**: reatribuir vendedor no mesmo dia (ou retroativo para uma data posterior ao inicio da atribuicao aberta atual) tentava fechar a linha aberta com uma data anterior ao proprio inicio dela, violando `valid_until >= valid_from`. Corrigido para so fechar linhas genuinamente anteriores e remover (em vez de fechar) linhas superadas pela nova data.

## Achado de qualidade de dados (nao e bug de codigo)

Investigando o bug 3 acima, foi descoberto que o cadastro legado da CAMNPAL tem **nomes de cliente duplicados sob codigos diferentes**: "REDE WT LTDA" (2 codigos), "MG FINK LTDA" (2 codigos), "MARISUL COMERCIO DE ALIMENTOS LTD" (4 codigos, aparentemente uma mesma transacao fragmentada no import legado) e "RIBACHEK DISTRIBUIDORA DE ALIMENT" (3 codigos, ainda recebendo transacoes novas em datas diferentes ate maio/2026). Consolidados por pedido do usuario usando o codigo com a transacao mais recente por nome (empate no caso MARISUL, resolvido de forma arbitraria e documentada). Total: 7 registros de cliente duplicados removidos, transacoes redirecionadas para o sobrevivente, nenhuma transacao perdida (1342 antes e depois da consolidacao).

**Decisao pendente do usuario/cliente RITO**: cogitar remover codigo como identificador de cliente e usar somente nome, dado o historico de inconsistencia de codigos no cadastro legado da CAMNPAL. Ainda nao implementado — aguardando revisao do cliente final.

## Verificacao

Cada rodada de correcao seguiu o runbook padrao: `npx tsc --noEmit`, `npm run build`, `npm run lint`, deploy via `npm run deploy:cloudflare`, smoke test (`/login` 200, `/` -> 307). Bugs de producao foram diagnosticados ao vivo com `wrangler tail` (nenhum reproduzia localmente da mesma forma, ja que dependiam de volume real de dados ou de peculiaridades do runtime Cloudflare Workers). Dados de teste incorretamente gravados pelo bug de escrita imediata (13 clientes sinteticos, mudanca de vendedor em 8 clientes reais preexistentes e em 1 cliente sem historico) foram identificados e revertidos antes do deploy final, comparando contra `sales_transactions` (nunca tocadas pelo bug, ja que so client/vendor assignment era escrito cedo demais) para reconstruir o estado correto anterior.

## Correcao (03/07/2026, mais tarde no mesmo dia)

A consolidacao de clientes CAMNPAL com nome duplicado descrita acima **estava errada** e foi revertida. Ver `20260703-clientes-com-mesmo-nome-e-codigos-diferentes-sao-filiais-distintas-nunca-fundir` para a regra de negocio correta e como a reversao foi feita.
