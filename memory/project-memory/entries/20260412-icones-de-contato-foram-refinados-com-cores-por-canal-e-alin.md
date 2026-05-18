---
id: "20260412-icones-de-contato-foram-refinados-com-cores-por-canal-e-alin"
project: "RITO"
type: "fix"
status: "completed"
title: "Ícones de contato foram refinados com cores por canal e alinhamento corrigido"
summary: "A linha de ícones do rodapé e do card de contato foi refinada com novo glyph do WhatsApp, alinhamento consistente e cores reconhecíveis por serviço: verde para WhatsApp, magenta/gradiente para Instagram e azul para LinkedIn."
why: "Isso melhora a leitura visual, aproxima o site de padrões institucionais mais comuns e resolve o principal ponto de acabamento percebido no rodapé."
source: "codex"
created_at: "2026-04-12T21:42:43.508Z"
updated_at: "2026-04-12T21:42:43.508Z"
tags: ["site","icons","footer","ui","branding","ux"]
files: ["site/index.html","site/pages/contato.html","site/pages/para-quem.html","site/pages/sobre.html","site/pages/solucoes.html","site/pages/como-funciona.html","site/assets/css/styles.css"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

O problema reportado era visual: o ícone do WhatsApp estava feio e a linha de ícones parecia desalinhada no rodapé. A correção incluiu um novo SVG para WhatsApp, ajustes de flex e line-height no container e nos botões, redução do ruído visual e adoção de tratamento cromático por serviço sem mudar a estrutura do layout. Instagram e LinkedIn continuam sem links reais porque o repositório ainda não traz as URLs oficiais, mas agora aparecem com presença visual mais profissional.
