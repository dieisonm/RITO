# Project Memory Versionada

Esta pasta é o espelho versionável das memórias duráveis do projeto RITO.

## Objetivo

Garantir que o Mac principal e o PC servidor tenham a mesma base de decisões, bugs, correções e racional do projeto sem depender de uma cópia manual do `project-memory` fora do repositório.

## Fonte

As entradas foram espelhadas de:

```text
Automations/project-memory/data/projects/RITO/entries/
```

## Regra

- `entries/*.md` é versionado no Git.
- `index.sqlite` não é versionado aqui.
- dados sensíveis, conversas brutas, credenciais e números pessoais não devem virar memória.
- quando o MCP `project-memory` estiver disponível, ele pode continuar sendo usado como interface de busca/escrita.
- quando o MCP não estiver disponível, estes arquivos Markdown continuam sendo a fonte durável.

## Sincronização

Para atualizar o espelho manualmente a partir da memória local:

```bash
cp ../project-memory/data/projects/RITO/entries/*.md memory/project-memory/entries/
```

Para restaurar em outro computador, copiar estes arquivos para o MCP local ou simplesmente manter o Codex lendo esta pasta como memória versionada.
