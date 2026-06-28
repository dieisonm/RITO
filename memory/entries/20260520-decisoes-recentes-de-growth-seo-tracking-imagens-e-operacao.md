---
id: "20260520-decisoes-recentes-de-growth-seo-tracking-imagens-e-operacao"
project: "RITO"
type: "decision"
status: "active"
title: "Decisoes recentes de growth, SEO, tracking, imagens e operacao"
summary: "Foram consolidadas as decisoes de ontem e hoje sobre GA4, Search Console, SEO organico, UTMs, uso do Codex para imagens, deploy Git-only, prospeccao sem Instagram automatizado e proximas paginas SEO da RITO."
why: "Garantir continuidade entre chats, Mac principal e PC servidor, evitando perda de contexto operacional em decisoes criticas de aquisicao, tracking, site e automacao."
source: "Codex sessions 2026-05-19 e 2026-05-20"
created_at: "2026-05-20T13:30:00-03:00"
updated_at: "2026-05-20T13:30:00-03:00"
tags: ["growth","seo","ga4","search-console","tracking","image-generation","deploy","server-ops","prospecting"]
files: ["site/index.html","site/assets/js/measurement.js","site/contact.php","site/sitemap.xml","site/robots.txt","docs/brand/presence/seo-organic-google-baseline.md","docs/brand/presence/seo-topic-pages-concept.md"]
related_ids: ["20260518-deploy-do-site-e-git-only-pela-branch-hostinger","20260519-ga4-instalado-no-site-da-rito","20260520-tracking-da-rito-ampliado-para-utm-avancado-e-atribuicao-90-","20260520-seo-organico-da-rito-foi-reforcado-com-schema-e-conteudo-local","20260518-rito-passa-a-usar-github-first-com-google-drive-para-assets-"]
issue: ""
pr: ""
commit: ""
---

## Decisoes consolidadas

- O deploy do site da RITO deve continuar Git-only: push em `main` publica o site por GitHub Actions para a branch `hostinger`, e a Hostinger consome essa branch. FTP direto nao deve ser usado como fluxo normal.
- O site esta com GA4 instalado usando Measurement ID `G-ZTLGY2QWVR`. Eventos importantes: page view, cliques em WhatsApp/e-mail/Instagram e envio de formulario como `generate_lead`.
- O GA4 deve ter `generate_lead` e `click_whatsapp` marcados como eventos principais.
- A captura de origem deve manter UTMs, click IDs e primeira atribuicao por 90 dias para melhorar leitura de campanhas futuras.
- O Google Search Console foi verificado por DNS TXT. O registro usado foi `google-site-verification=fm9CJ0Nc8tw0mDycVs_hmh7mA1qNtJYWglfEtpqlgyk`.
- O sitemap oficial e `https://ritosistemas.com/sitemap.xml`. Ele foi processado com sucesso pelo Search Console e encontrou 7 paginas.
- O SEO organico foi reforcado com titulos, descriptions, canonicals, hreflang, Open Graph, Twitter tags, JSON-LD, sitemap com lastmod e robots.txt.
- O site deve crescer organicamente com paginas especificas, mas sem virar um bloco cansativo de texto. As novas paginas SEO precisam ser mais visuais, interativas e orientadas a exemplos.
- As quatro primeiras paginas SEO planejadas sao: software sob medida para pequenas empresas; automacao para MEI e pequenos negocios; planilhas inteligentes e dashboards sob medida; criacao de site simples para MEI.
- As paginas devem usar componentes visuais como carrossel de mockups, exemplos de antes/depois, mini dashboards, cards de problemas reais e CTAs claros.
- A RITO pode gerar imagens de campanha, stories, posts e conceitos diretamente pelo Codex usando a ferramenta de imagem atual, seguindo os guias de prompt ja documentados. O agente de imagens deve gerar prompt, chamar o gerador e salvar o resultado no local correto quando for ativo de projeto.
- O Instagram nao deve ser acessado automaticamente por agentes. Qualquer verificacao de Instagram deve ser manual pelo usuario para evitar novos bloqueios da Meta.
- O PC servidor deve sincronizar pelo GitHub e usar Google Drive para assets grandes; decisoes duraveis devem ser registradas em `memory/entries/`.

## Implicacoes para o proximo trabalho

Antes de implementar novas paginas, desenhar o conceito e aprovar a experiencia: menos texto corrido, mais demonstracao visual do que a RITO pode entregar. Cada pagina deve ranquear por uma intencao de busca especifica e, ao mesmo tempo, servir como pagina comercial com conversao para WhatsApp/formulario.
