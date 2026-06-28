---
id: "20260520-tracking-da-rito-ampliado-para-utm-avancado-e-atribuicao-90-"
project: "RITO"
type: "decision"
status: "active"
title: "Tracking da RITO ampliado para UTM avancado e atribuicao 90 dias"
summary: "O tracking do site passou a capturar UTMs avancadas, IDs de clique de midia paga e first-touch/last-touch com persistencia de 90 dias."
why: "Melhorar atribuicao de origem para campanhas de Instagram, Brevo, Meta Ads, Google Ads e canais futuros, evitando perder a origem quando o visitante volta dias depois para converter."
source: "Codex session 2026-05-19"
created_at: "2026-05-20T00:19:13.913Z"
updated_at: "2026-05-20T00:19:13.913Z"
tags: ["analytics","utm","ga4","attribution","growth"]
files: ["site/assets/js/measurement.js","site/contact.php"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

Em 2026-05-19, measurement.js foi ampliado para capturar utm_id, utm_source_platform, utm_creative_format, utm_marketing_tactic, li_fat_id e ttclid, alem dos UTMs e click IDs ja existentes. A atribuicao passou de sessionStorage para localStorage com TTL de 90 dias e fallback para sessionStorage. O formulario passa a receber landing/referrer atuais e tambem first_landing_page, first_referrer e primeiras UTMs principais. contact.php salva e envia esses dados no lead.
