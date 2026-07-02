---
id: "20260702-assinatura-horizontal-areia-foi-restaurada-como-logo-do-relatorio-de-vendas"
project: "RITO"
type: "fix"
status: "active"
title: "Assinatura horizontal areia foi restaurada como logo do Relatorio de Vendas"
summary: "O logo correto do produto e a assinatura horizontal completa, com monograma R, RITO e SISTEMAS em dourado/areia. A variante foi recriada a partir de rito-assinatura-horizontal-claro.svg e aplicada na sidebar, no loading e no login."
why: "A variante dourada havia desaparecido durante a migracao de pastas. O wordmark areia sem monograma foi registrado e publicado por engano como se fosse o logo correto."
source: "codex-session"
created_at: "2026-07-02T20:00:00.000Z"
updated_at: "2026-07-02T21:27:31.549Z"
tags: ["relatorio-vendas","logo","brand","assinatura-horizontal","areia","migration-fix"]
files: ["S:/RITO/Automations/RITO/assets/brand/logos/systems-and-apps/rito-assinatura-horizontal-areia.svg","S:/RITO/Projetos/relatorio-vendas-web/public/logos/rito-assinatura-horizontal-areia.svg","S:/RITO/Projetos/relatorio-vendas-web/src/components/app-shell.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/components/route-skeleton.tsx","S:/RITO/Projetos/relatorio-vendas-web/src/components/login-form.tsx"]
related_ids: ["20260702-logo-azul-foi-publicado-por-engano-e-corrigido-para-wordmark-areia","20260412-brand-sources-and-visual-system-are-canonical"]
issue: ""
pr: ""
commit: ""
---

## Details

A geometria veio do arquivo confirmado pelo usuario,
`C:/Users/Dieison/Downloads/rito-assinatura-horizontal-claro.svg`. A nova
variante usa o gradiente oficial `#d4b08a` para `#b89163`, recorte petroleo
`#0d2430` e viewBox ajustado para `520x150`, removendo o espaco vazio que fazia
o logo parecer pequeno.

O arquivo canonico de marca fica em
`S:/RITO/Automations/RITO/assets/brand/logos/systems-and-apps/rito-assinatura-horizontal-areia.svg`.
A copia de runtime fica em
`S:/RITO/Projetos/relatorio-vendas-web/public/logos/rito-assinatura-horizontal-areia.svg`.
Nao substituir pela versao `rito-wordmark-areia.svg`, pois ela nao possui o
monograma e nao e a assinatura completa aprovada para este produto.

Depois da validacao humana, o logo foi ampliado discretamente: `w-48` na
sidebar e no skeleton, e `w-72` no login. Essas dimensoes mantem a assinatura
legivel sem disputar atencao com o titulo do produto.
