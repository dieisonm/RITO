---
id: "20260519-ga4-instalado-no-site-da-rito"
project: "RITO"
type: "decision"
status: "active"
title: "GA4 instalado no site da RITO"
summary: "O site da RITO usa a propriedade GA4 com Measurement ID G-ZTLGY2QWVR para medir page views, cliques e envio de formulario."
why: "Dar visibilidade real a visitas, campanhas e conversoes do Projeto Piloto e preparar a base para Google Ads, Meta Ads, Search Console e analise por canal."
source: "Codex session 2026-05-19"
created_at: "2026-05-19T23:45:29.517Z"
updated_at: "2026-05-19T23:45:29.517Z"
tags: ["ga4","analytics","utm","tracking","site"]
files: ["site/assets/js/measurement.js","site/contact.php"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

Em 2026-05-19 o measurement.js passou a carregar gtag.js, configurar GA4 com send_page_view false e enviar eventos: page_view, click_whatsapp, click_email, click_instagram, click_pilot_landing e generate_lead_form. A captura de origem tambem foi ampliada de UTM para click IDs: gclid, gbraid, wbraid, fbclid e msclkid. O contact.php passa a salvar e enviar esses IDs nos leads quando presentes.
