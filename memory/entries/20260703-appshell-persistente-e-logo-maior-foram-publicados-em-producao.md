---
id: "20260703-appshell-persistente-e-logo-maior-foram-publicados-em-producao"
project: "RITO"
type: "decision"
status: "active"
title: "AppShell persistente entre navegacoes e logo maior foram publicados em producao"
summary: "AppShell (sidebar + header) saiu de dentro de cada page.tsx e passou a viver em src/app/(app)/layout.tsx, ficando montado uma unica vez entre navegacoes: o destaque da aba ativa agora atualiza instantaneamente ao clicar, e o header/busca pararam de recarregar a cada troca de aba. O skeleton de loading foi corrigido para nao renderizar mais sua propria sidebar/header falsa (o que causava uma sidebar duplicada dentro da real durante o carregamento). O logo da sidebar foi ampliado. Tudo validado local (127.0.0.1:3001) antes de publicar."
why: "Usuario reportou que o destaque da aba so mudava depois da pagina carregar, que o header/busca recarregavam a cada troca de aba, e que o logo estava pequeno. Ao corrigir isso hoisting o AppShell para o layout, surgiu uma regressao (skeleton duplicando a sidebar dentro do conteudo) que tambem foi corrigida antes da publicacao."
source: "claude-code-session"
created_at: "2026-07-03T00:00:00-03:00"
updated_at: "2026-07-03T00:00:00-03:00"
tags: ["relatorio-vendas","ui","ux","app-router","layout","cloudflare-workers","deploy"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/src/app/(app)/layout.tsx", "S:/RITO/Projetos/relatorio-vendas-web/src/components/app-shell.tsx", "S:/RITO/Projetos/relatorio-vendas-web/src/components/route-skeleton.tsx", "S:/RITO/Projetos/relatorio-vendas-web/src/lib/database-data.ts"]
related_ids: ["20260702-fluxo-canonico-de-codigo-arquivos-e-deploy-do-relatorio-de-vendas", "20260702-assinatura-horizontal-areia-foi-restaurada-como-logo-do-relatorio-de-vendas", "20260702-plano-de-performance-do-relatorio-de-vendas-web-foi-concluido-com-um-item-adiado"]
issue: ""
pr: ""
commit: "d39e0fd"
---

## Diagnostico

`AppShell` era renderizado de dentro de cada `page.tsx` (ou dentro de `home-dashboard.tsx`/`analytics-dashboard.tsx`). Como cada navegacao troca o Server Component da pagina, o React desmontava e remontava a sidebar/header inteiros a cada clique, e o `usePathname()` (que decide o item ativo) so atualizava quando os novos dados chegavam — daí o atraso no destaque e o header "recarregando".

## Correcao

`AppShell` passou a ser renderizado uma unica vez em `src/app/(app)/layout.tsx` (que ja fazia o gate de auth fora do Suspense do `loading.tsx`, ver `20260702-plano-de-performance...`), recebendo sessao e um contador de notificacao vindo de uma query `COUNT` leve (`getUnassignedClientsCount` em `database-data.ts`) em vez do fetch completo de clientes. Todas as 6 paginas protegidas e os dois componentes que auto-envolviam `AppShell` foram ajustados para nao renderizar mais o shell, apenas o conteudo.

Essa mudanca expos uma regressao: como `loading.tsx` renderiza dentro do `{children}` do `AppShell` persistente, o `route-skeleton.tsx` antigo (que desenhava sua propria sidebar/header falsa) passou a aparecer *dentro* do conteudo da sidebar real durante o carregamento — uma sidebar dentro da outra. Corrigido reescrevendo `route-skeleton.tsx` para conter apenas os placeholders de conteudo (cards e tabela), sem replicar sidebar/header/logo.

Logo da sidebar ampliado: container passou de `w-48` para `w-full` com padding lateral reduzido (`px-6` para `px-5`).

## Publicacao

Validado local em `http://127.0.0.1:3001` pelo usuario antes de subir. Fluxo seguido conforme `docs/deployment-runbook.md`: `git pull --ff-only`, commit `d39e0fd` ("Make sidebar persistent across navigation and fix loading skeleton"), push, `npm ci && npm run lint && npx tsc --noEmit && npm run build`, deploy via `npm run deploy:cloudflare`. Validacao pos-deploy: `/login` 200, `/`/`/clientes`/`/analises` sem sessao com `307`, asset do logo acessivel (200) em producao.
