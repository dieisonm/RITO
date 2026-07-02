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
