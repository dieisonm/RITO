# Project Memory Versionada

> Fonte canonica no Windows: `S:/RITO/Automations/RITO/memory`.
> A copia antiga em `C:/Users/Dieison/OneDrive/Documentos/Google Drive/Projetos/RITO/memory`
> e somente legado e nao deve receber novas entradas.

Esta pasta é o espelho versionado das memórias duráveis do projeto RITO.

## Objetivo

Garantir que o Mac principal e o PC servidor tenham a mesma base de decisões, bugs, correções e racional do projeto sem depender de uma cópia manual do `project-memory` fora do repositório.

## Fonte

As entradas duraveis ficam em:

```text
S:/RITO/Automations/RITO/memory/entries/
```

## Regra

- `entries/*.md` é versionado no Git.
- `index.sqlite` não é versionado aqui.
- dados sensíveis, conversas brutas, credenciais e números pessoais não devem virar memória.
- quando o MCP `project-memory` estiver disponível, ele pode continuar sendo usado como interface de busca/escrita.
- quando o MCP não estiver disponível, estes arquivos Markdown continuam sendo a fonte durável.

## Sincronização

Para restaurar em outro computador, basta manter esta pasta no clone do repositório e apontar o Codex para `memory/entries/`.

## Relatorio de vendas web

Estado revisado em 09/10/2026:
[`entries/20261009-relatorio-vendas-estado-revisado-e-pendencias.md`](entries/20261009-relatorio-vendas-estado-revisado-e-pendencias.md).
O detalhe canonico vive em `docs/current-state.md` no repo separado
`dieisonm/relatorio-vendas-web` (`master`); esta memoria viaja no repo RITO
(`main`). Atualizar ambos ao concluir mudancas relevantes. Memoria local de
MCP/Claude sem commit nao e sincronizacao entre computadores.

Nesta maquina o app fica em
`/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web`.
O clone e ignorado pelo Git RITO; seus docs precisam ser commitados no Git do
app. No RITO, fazer stage explicito de `memory/**`; esse escopo nao aciona
o workflow Hostinger. O app tem publicacao manual via OpenNext/Cloudflare;
atualizar memoria/documentacao nao exige executar deploy.
