---
id: "20260702-logo-azul-foi-publicado-por-engano-e-corrigido-para-wordmark-areia"
project: "RITO"
type: "decision"
status: "superseded"
title: "Logo azul foi publicado por engano no Relatorio de Vendas web e corrigido para o wordmark areia"
summary: "Ao publicar as correcoes de performance, o deploy embarcou o estado inteiro da working tree local (nao so o diff do agente), incluindo uma troca de logo (assinatura azul no lugar do wordmark dourado/areia) que ja estava no disco antes da sessao comecar, nunca publicada. O usuario identificou o arquivo correto e o logo foi revertido para `rito-wordmark-areia.svg` na sidebar (`app-shell.tsx`) e no skeleton de loading (`route-skeleton.tsx`)."
why: "O usuario relatou que o logo ficou azul e menor apos o deploy de performance, quando antes era dourado e do tamanho certo. Investigacao confirmou que o agente nao editou o logo, mas o deploy publicou uma mudanca de marca (28/06) que estava pendurada, sem commit, no disco local havia dias."
source: "claude-code-session"
created_at: "2026-07-02T00:00:00-03:00"
updated_at: "2026-07-02T20:00:00.000Z"
tags: ["relatorio-vendas","logo","brand","deploy-hygiene","cloudflare-workers"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/src/components/app-shell.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/components/route-skeleton.tsx","S:/RITO/Automations/RITO/assets/brand/logos/systems-and-apps/rito-wordmark-areia.svg","S:/RITO/Projetos/relatorio-vendas-web/public/logos/rito-wordmark-areia.svg"]
related_ids: ["20260702-plano-de-performance-do-relatorio-de-vendas-web-foi-concluido-com-um-item-adiado", "20260412-brand-sources-and-visual-system-are-canonical", "20260702-assinatura-horizontal-areia-foi-restaurada-como-logo-do-relatorio-de-vendas"]
issue: ""
pr: ""
commit: ""
---

## Diagnostico

> Superado em 02/07/2026: `rito-wordmark-areia.svg` nao era o logo completo
> usado no produto. A variante correta e a assinatura horizontal dourada com
> monograma, registrada na entrada relacionada.

O repositorio `relatorio-vendas-web` nao tem historico de commits reais (so existe "Initial commit from Create Next App"); nenhum arquivo de UI, logo ou branding jamais foi versionado ali. Deploys sao manuais via `npm run deploy:cloudflare`, que empacota tudo o que estiver no disco local naquele momento — nao apenas o diff da sessao. Quando a sessao de performance comecou, `git status` ja mostrava dezenas de arquivos "modificados"/"nao rastreados" preexistentes (`globals.css`, `layout.tsx`, `next.config.ts`, `public/logos/`, etc.), sinal de que havia trabalho de rebranding em andamento, nunca publicado.

O componente `app-shell.tsx` ja referenciava `/logos/rito-assinatura-horizontal-branco.svg` (gradiente azul petroleo, `#2a5570`/`#173847`) antes do agente tocar em qualquer coisa. Esse arquivo bate byte a byte com a versao canonica em `S:/RITO/Automations/RITO/assets/brand/logos/systems-and-apps/rito-assinatura-horizontal-branco.svg`, ou seja, nao e um arquivo corrompido — e a "assinatura horizontal" oficial para fundos escuros segundo o README daquela pasta. O problema nao foi o conteudo do arquivo, foi que essa troca de familia de logo (da versao anterior, dourada, para essa nova familia "systems-and-apps") nunca tinha chegado a producao ate o deploy de hoje.

O usuario identificou o arquivo correto: `rito-wordmark-areia.svg` (texto "RITO SISTEMAS" em tom dourado/areia `#b89163`, sem o icone), presente tanto na pasta canonica quanto ja copiado em `public/logos/` do proprio projeto.

## Correcao aplicada

Trocado `src="/logos/rito-assinatura-horizontal-branco.svg"` por `src="/logos/rito-wordmark-areia.svg"` em `app-shell.tsx` (sidebar real) e `route-skeleton.tsx` (skeleton de loading, para manter consistencia visual durante o carregamento). Ajustado `width`/`height` de `420x120` para `640x200` para casar com o viewBox real do wordmark (proporcao 3.2:1, diferente da assinatura anterior 4.44:1) e evitar distorcao — o container (`w-44`, `h-auto w-full`) nao foi alterado. Validado com `tsc --noEmit`, `next build` e publicado; `GET /logos/rito-wordmark-areia.svg` responde 200 em producao.

## Achado pendente, nao corrigido

`src/components/login-form.tsx` referencia `/logos/rito-assinatura-horizontal-areia.svg`, arquivo que **nao existe** em `public/logos/` (so existe `rito-wordmark-areia.svg`). A tela de login provavelmente exibe uma imagem quebrada. Usuario pediu para nao mexer em mais nada por enquanto; correcao fica pendente de decisao.

## Licao para deploys futuros neste projeto

Antes de qualquer `npm run deploy:cloudflare`, checar `git status`/diff completo do working tree, nao so o que a sessao atual mudou — o deploy publica tudo. Se houver mudancas de UI/branding preexistentes e nao relacionadas ao que esta sendo trabalhado, confirmar com o usuario antes de publicar, para nao embarcar trabalho em andamento por engano.
