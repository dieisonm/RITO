---
id: "20260702-quick-wins-de-performance-do-relatorio-de-vendas-web-foram-implantados"
project: "RITO"
type: "decision"
status: "active"
title: "Quick wins de performance do Relatorio de Vendas web foram implantados em producao"
summary: "As 3 correcoes rapidas do plano de performance (Smart Placement, loading.tsx/Suspense por rota e colapso do round trip duplo de auth) foram implementadas, validadas (typecheck, build, smoke test local e em producao) e implantadas em https://rito.relatorio-vendas.workers.dev. As duas frentes estruturais (agregacao SQL e cache) continuam pendentes."
why: "Continuar a auditoria registrada em 20260702-auditoria-de-performance-do-relatorio-de-vendas-web-identifi: o usuario aprovou o plano e autorizou execucao autonoma comecando pelos quick wins, com checagem de regressao apos cada mudanca."
source: "claude-code-session"
created_at: "2026-07-02T00:00:00-03:00"
updated_at: "2026-07-02T00:00:00-03:00"
tags: ["relatorio-vendas","performance","cloudflare-workers","supabase","auth","smart-placement","loading-states"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/wrangler.jsonc","S:/RITO/Projetos/relatorio-vendas-web/src/lib/auth.ts","S:/RITO/Projetos/relatorio-vendas-web/src/app/(app)/layout.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/app/(app)/loading.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/components/route-skeleton.tsx"]
related_ids: ["20260702-auditoria-de-performance-do-relatorio-de-vendas-web-identifi", "20260702-relatorio-de-vendas-web-esta-em-producao-com-cloudflare-e-supabase"]
issue: ""
pr: ""
commit: ""
---

## O que foi feito

1. **Smart Placement**: `wrangler.jsonc` ganhou `"placement": {"mode": "smart"}`. Confirmado em producao pelo header `Cf-Placement: local-GRU` (o Worker agora roda perto da regiao do Supabase, nao so perto do navegador do usuario).
2. **Loading states**: as 6 rotas protegidas (`/`, `/clientes`, `/vendedores`, `/empresas`, `/importar`, `/analises`) foram movidas para um route group `src/app/(app)/` com um unico `loading.tsx` compartilhado (`src/components/route-skeleton.tsx`), eliminando a sensacao de aba congelada durante o fetch.
3. **Auth colapsada**: `src/lib/auth.ts` trocou `supabase.auth.getUser()` (round trip de rede) por `supabase.auth.getSession()` (leitura local de cookie) e mantem apenas a query de `profiles` como round trip real; essa query ja autentica o JWT via PostgREST/RLS como efeito colateral, entao a seguranca nao mudou. A funcao foi envolvida em `React.cache()` para que o layout (que faz o gate antes do Suspense) e a pagina (que le a sessao para exibir nome/email) nao dupliquem a chamada dentro da mesma requisicao.

## Armadilha encontrada e corrigida

Adicionar `loading.tsx` diretamente nas paginas que chamam `redirect()` (via `requireAdminPage`) quebrou o redirecionamento HTTP limpo: como a pagina passa a ficar dentro de um Suspense boundary, o Next nao consegue mais responder com um 307 direto e cai para um redirecionamento via meta-refresh/JS no lado cliente. A correcao foi mover o `requireAdminPage()` para um `layout.tsx` do route group `(app)`, que roda fora do Suspense do `loading.tsx` filho. Validado em producao: `/`, `/clientes` e `/analises` sem sessao voltam a responder `307` com `Location: /login` corretamente.

`lucide-react` tambem quebrou o build (`d.createContext is not a function`) quando usado dentro de um componente Server-only renderizado por um `loading.tsx` (prerender estatico). A correcao foi marcar `route-skeleton.tsx` como `"use client"`, igual ao padrao ja usado em `app-shell.tsx`.

## Validacao

`npx tsc --noEmit` limpo, `npm run build` limpo, smoke test local (`next start` em porta alternativa) e smoke test em producao confirmando `/login` 200 e `/`, `/clientes`, `/analises` com `307` para usuario nao autenticado. O fluxo autenticado (login real) ainda precisa de confirmacao manual do usuario, pois nao ha credenciais de teste disponiveis para o agente.

## Pendente

Itens estruturais do plano original (agregacao SQL no lugar de fetch de tabela inteira + soma em JS, e camada de cache) continuam em andamento — ver `20260702-auditoria-de-performance-do-relatorio-de-vendas-web-identifi` para o plano completo.
