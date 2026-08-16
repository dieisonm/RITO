---
id: "20260802-memory-mcp-instalado-e-regra-de-push-seguro-no-repo-rito"
project: "RITO"
type: "decision"
status: "active"
title: "MCP de memoria instalado neste PC + regra de push seguro no repo RITO (memory/** nao dispara deploy do site)"
summary: "O servidor MCP de memoria fica em S:/RITO/ProjectMemory/project-memory-mcp.js e foi registrado em C:/Users/Dieison/.claude.json (escopo de usuario, carrega ao reiniciar o Claude Code; backup em .claude.json.bak-premcp). O store do MCP e PROJECT_MEMORY_ROOT/projects/RITO/entries (default S:/RITO/ProjectMemory/data) — LOCAL por PC — e e separado do store versionado em git S:/RITO/Automations/RITO/memory/entries (repo dieisonm/RITO). Escrever memoria (memory_remember) grava so no store local; NAO altera o git automaticamente. Regra de ouro de seguranca: o site Hostinger faz deploy via .github/workflows/deploy-hostinger.yml em push na branch main SOMENTE quando o commit toca site/**, logos/**, scripts/build_dist.sh ou o proprio workflow. Um commit de memoria que toca apenas memory/** NAO dispara deploy. NUNCA usar git add -A num commit de memoria (varreria mudancas de site/logos e publicaria o site sem querer)."
why: "O usuario avisou que fazer o git errado ja disparou mudancas no site antes, e pediu para instalar o MCP e usar como memoria principal, mantendo este PC e o remoto iguais. Este registro fixa como o sistema de memoria esta montado e o procedimento seguro de publicacao para evitar deploy acidental do site."
source: "claude-code-session"
created_at: "2026-08-02T00:00:00-03:00"
updated_at: "2026-08-02T00:00:00-03:00"
tags: ["memory","mcp","git","deploy","hostinger","seguranca","rito","onboarding"]
files: ["S:/RITO/ProjectMemory/project-memory-mcp.js","S:/RITO/ProjectMemory/README.md","C:/Users/Dieison/.claude.json","S:/RITO/Automations/RITO/memory/entries","S:/RITO/Automations/RITO/.github/workflows/deploy-hostinger.yml"]
related_ids: ["20260802-relatorio-vendas-tres-correcoes-criticas-de-importacao-e-comissao","20260518-deploy-do-site-e-git-only-pela-branch-hostinger"]
issue: ""
pr: ""
commit: ""
---

## Como o sistema de memoria esta montado (neste PC)

- **Servidor MCP**: `S:/RITO/ProjectMemory/project-memory-mcp.js` (stdio, Node 24 ok — usa `node:sqlite`). Ferramentas: `memory_search`, `memory_recent`, `memory_get`, `memory_remember`, `memory_projects`, `memory_rebuild`.
- **Registrado** em `C:/Users/Dieison/.claude.json` sob `mcpServers.project-memory` (command `node`, args = caminho do servidor, env `PROJECT_MEMORY_ROOT=S:/RITO/ProjectMemory/data`). Carrega no PROXIMO start do Claude Code (nao no meio da sessao). Backup: `.claude.json.bak-premcp`.
- **Store local do MCP**: `S:/RITO/ProjectMemory/data/projects/RITO/entries/*.md` (+ `index.sqlite` reconstruivel). Fonte durável = os `.md`; o SQLite se refaz sozinho no start ou via `memory_rebuild`.
- **Store versionado em git**: `S:/RITO/Automations/RITO/memory/entries/*.md`, no repo `dieisonm/RITO` (branch `main`). E o que viaja para o outro computador.
- Os dois stores sao **diretorios diferentes** e nao sincronizam sozinhos.

## Regras de conteudo (do proprio servidor)

Gravar apenas memoria durável e reutilizavel: `decision`, `bug`, `fix`, `rationale`. Buscar a memoria antes de trabalho relevante. Nao gravar conversa crua, credenciais ou dados pessoais.

## Procedimento seguro para publicar memoria no git (outro PC)

1. Escrever a entrada (via `memory_remember` -> vai para o store local, ou como `.md` no formato de frontmatter).
2. Copiar o(s) `.md` novo(s) para `S:/RITO/Automations/RITO/memory/entries/`.
3. `git add memory/entries/<arquivo>.md` — **SOMENTE `memory/**`**. Nunca `git add -A`.
4. `git commit` e `git push origin main`.
5. **Seguranca de deploy**: publicar so `memory/**` na `main` NAO dispara o deploy Hostinger (que so roda para `site/**`, `logos/**`, `scripts/build_dist.sh`, `.github/workflows/deploy-hostinger.yml`). Se o worktree tiver mudancas de site/logos pendentes, fazer o commit de memoria de forma cirurgica (staged so os arquivos de memoria) para nao arrastar o site junto.

## Reconciliacao feita em 02/08/2026

O store local do MCP estava com 46 entradas (latest 2026-07-02); o `origin/main` tinha 57. Sincronizado copiando as 57 do `origin/main` para o store local e refeito o indice (`memory_rebuild`) -> 57 = 57. O working tree local de `S:/RITO/Automations/RITO` continua atrasado/sujo (migracao em andamento do usuario, com arquivos untracked que colidem com o remoto e delecoes nao commitadas) — reconciliar com um clone limpo ou resolver as colisoes antes de dar `git pull`.
