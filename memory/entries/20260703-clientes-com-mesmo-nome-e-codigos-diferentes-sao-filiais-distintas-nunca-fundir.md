---
id: "20260703-clientes-com-mesmo-nome-e-codigos-diferentes-sao-filiais-distintas-nunca-fundir"
project: "RITO"
type: "decision"
status: "active"
title: "Clientes com mesmo nome e codigos diferentes sao filiais distintas — nunca fundir; match de cliente exige codigo exato quando o relatorio traz um"
summary: "O cliente RITO esclareceu: uma mesma empresa pode ter varias filiais cadastradas sob o nome identico, cada uma um cliente distinto pelo codigo. A consolidacao de clientes CAMNPAL feita mais cedo no mesmo dia (ver 20260703-fluxo-de-confirmacao-e-gravacao-da-importacao-web-foi-implementado-e-publicado) estava errada e foi revertida com precisao usando sales_transactions.source_key, que preserva o codigo original de cada linha mesmo apos uma fusao. matchClient (src/lib/import-dedup.ts) foi corrigido: quando o relatorio traz um codigo, o match exige esse codigo exato — nunca cai para nome. Nome sozinho so e usado quando o relatorio nao traz codigo nenhum."
why: "O usuario reportou explicitamente a regra de negocio depois de ver o resultado da consolidacao anterior: 'um cliente tem varias filiais com mesmo nome mas cada um precisa ser tratado como um cliente especifico, por isso o match precisa sempre ser cliente nome e codigo. Se o relatorio nao vier com codigo ai pegamos o nome.' Isso inverte a decisao registrada horas antes na mesma sessao."
source: "claude-code-session"
created_at: "2026-07-03T23:23:02-03:00"
updated_at: "2026-07-03T23:23:02-03:00"
tags: ["relatorio-vendas","importacao","dedup","data-quality","camnpal","supabase"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/src/lib/import-dedup.ts", "S:/RITO/Projetos/relatorio-vendas-web/docs/current-state.md"]
related_ids: ["20260703-fluxo-de-confirmacao-e-gravacao-da-importacao-web-foi-implementado-e-publicado"]
issue: ""
pr: ""
commit: "c796b64,108399a"
---

## Regra de negocio (definitiva)

Match de cliente em `matchClient` (`src/lib/import-dedup.ts`):
- Relatorio traz codigo -> so casa por esse codigo exato. Codigo que nao bate com nenhum cadastrado NUNCA cai para nome (o nome pode ser de uma filial diferente).
- Relatorio nao traz codigo nenhum -> so entao casa por nome.

## O que estava errado e como foi corrigido

Investigando por que a mesma linha reaparecia como "nova" a cada preview (bug de outra entrada), foi descoberto que a CAMNPAL tem varios nomes de cliente registrados sob multiplos codigos: "REDE WT LTDA", "MG FINK LTDA", "MARISUL COMERCIO DE ALIMENTOS LTD", "RIBACHEK DISTRIBUIDORA DE ALIMENT". A primeira hipotese (registrada em `20260703-fluxo-de-confirmacao-e-gravacao-da-importacao-web-foi-implementado-e-publicado`) foi tratar isso como erro de cadastro legado e consolidar cada nome num codigo so, usando o codigo com a transacao mais recente. **Essa hipotese estava errada** — sao filiais legitimamente distintas.

O `matchClient` antigo (`byCode.get(codigo) ?? byName.get(nome)`) tambem continuou causando o mesmo problema em importacoes feitas *depois* da fusao errada: qualquer linha cujo codigo do relatorio nao batesse com nenhum cadastrado caia para o nome e era silenciosamente atribuida ao cliente "vencedor" da fusao, mesmo sendo de uma filial diferente (inclusive um codigo, "110730", que nunca tinha aparecido antes da fusao).

Reversao: como `sales_transactions.source_key` guarda o `movementKey` calculado no momento da importacao original — que inclui o codigo do relatorio — cada transacao "fundida" ainda carregava seu codigo real, nunca reescrito pela fusao. Agrupando as transacoes de cada cliente "vencedor" pelo codigo embutido no `source_key`, foi possivel recriar exatamente os 8 clientes que tinham sido apagados (mais 1 novo, "110730", que so existia por causa do bug continuando a rodar) e mover cada transacao de volta ao codigo certo — 25 transacoes reatribuidas, nenhuma perdida. Cada cliente recriado ganhou um registro em `client_vendor_assignments` (vendedor OBERDAN, `valid_from = 1900-01-01`, igual ao padrao original).

## Verificacao

Contagem total de `sales_transactions` da CAMNPAL antes/depois da reversao bateu exatamente com o esperado (a diferenca observada, 1342 -> 1817, foi explicada por uma importacao legitima do usuario feita em paralelo, "29775-4.pdf", 475 linhas — confirmado via a tabela `imports`, nao um efeito da correcao). Nova varredura por nomes duplicados na CAMNPAL depois da correcao encontrou apenas os mesmos 4 nomes, agora corretamente divididos por codigo — nenhum nome novo afetado pelo bug historico. `npx tsc --noEmit`, `npm run build`, `npm run lint` limpos; deploy e smoke test (`/login` 200, `/` -> 307) ok.
