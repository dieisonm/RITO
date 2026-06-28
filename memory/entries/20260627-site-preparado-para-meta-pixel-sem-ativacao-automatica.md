---
id: "20260627-site-preparado-para-meta-pixel-sem-ativacao-automatica"
project: "RITO"
type: "decision"
status: "active"
title: "Site preparado para Meta Pixel sem ativacao automatica"
summary: "A mensuracao do site ganhou suporte centralizado a Meta Pixel, eventos PageView/Lead, eventos customizados e captura de fbp/fbc, mas o Pixel permanece desligado ate existir um ID criado e validado no Events Manager."
why: "Permitir uma futura campanha de Leads com atribuicao consistente sem publicar um identificador inexistente, disparar eventos duplicados ou considerar o tracking pronto antes da validacao real."
source: "workspace review 2026-06-27; implementation prepared 2026-06-17"
created_at: "2026-06-27T12:00:00-03:00"
updated_at: "2026-06-27T12:00:00-03:00"
tags: ["meta-ads", "meta-pixel", "analytics", "tracking", "lead", "attribution"]
files: ["site/assets/js/measurement-config.js", "site/assets/js/measurement.js", "site/assets/js/app.js", "site/contact.php", "ops/meta-ads/launch-playbook.md"]
related_ids: ["20260519-ga4-instalado-no-site-da-rito", "20260520-tracking-da-rito-ampliado-para-utm-avancado-e-atribuicao-90-"]
issue: ""
pr: ""
commit: ""
---

## Decisao operacional

- `site/assets/js/measurement-config.js` e a fonte unica dos IDs de mensuracao no frontend.
- O GA4 continua ativo pelo ID atual.
- `metaPixelId` deve permanecer vazio enquanto o Pixel da RITO nao for criado no Meta Events Manager.
- Depois de preencher o ID, publicar e validar `PageView` e `Lead` no Events Manager antes de iniciar campanha otimizada por conversao.
- Cliques em WhatsApp, e-mail, Instagram e projeto piloto sao enviados ao Meta como eventos customizados quando o Pixel estiver ativo.
- Formularios carregam `meta_fbp` e `meta_fbc` junto da atribuicao UTM/click IDs; uma futura Conversions API deve reutilizar o mesmo `event_id` para deduplicacao.

## Proxima acao que exige estado externo

Criar o Pixel, preencher seu ID, publicar o site e executar testes reais. Ate isso acontecer, a implementacao esta pronta no codigo, mas o tracking da Meta nao deve ser descrito como ativo.
