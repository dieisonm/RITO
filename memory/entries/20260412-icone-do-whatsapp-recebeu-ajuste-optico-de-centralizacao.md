---
id: "20260412-icone-do-whatsapp-recebeu-ajuste-optico-de-centralizacao"
project: "RITO"
type: "fix"
status: "completed"
title: "Ícone do WhatsApp recebeu ajuste óptico de centralização"
summary: "A raiz do bug era um override de `.footer a` sobre o componente de ícone; a correção separou o comportamento do rodapé sem quebrar o card."
why: "O ajuste corrige um detalhe visual que passava sensação de falta de acabamento, especialmente no rodapé, sem introduzir mudanças estruturais desnecessárias."
source: "codex"
created_at: "2026-04-12T21:44:53.400Z"
updated_at: "2026-04-12T22:36:05.515Z"
tags: ["site","icons","whatsapp","alignment","ux"]
files: ["site/index.html","site/pages/contato.html","site/pages/para-quem.html","site/pages/sobre.html","site/pages/solucoes.html","site/pages/como-funciona.html","site/assets/css/styles.css"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

A causa raiz final foi confirmada no CSS: o mesmo componente de canal estava sendo reutilizado corretamente no card e no rodapé, mas o rodapé tinha uma regra genérica `.footer a` com `display: block` e `margin-bottom` que sobrescrevia o botão `.channel-icon` apenas nesse contexto. Isso quebrava a centralização do ícone no footer, enquanto o card permanecia correto. A correção estrutural foi: 1. restringir a regra genérica para `.footer a:not(.channel-icon), .footer p`; 2. forçar `.footer .channel-icon` a manter `display: inline-flex` e `margin: 0`; 3. manter os ícones como arquivos SVG reais de marca em `site/assets/icons/`. A validação final por screenshots renderizadas confirmou alinhamento consistente tanto no rodapé quanto no card da página de contato.
