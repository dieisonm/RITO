---
id: "20260629-folder-structure-was-simplified-around-website-brand-and-assets"
project: "RITO"
type: "decision"
status: "active"
title: "Estrutura de pastas foi simplificada em torno de website, brand e assets"
summary: "A árvore de pastas foi enxugada para reduzir duplicação de `site`, `logos` e `deliverables`, com nomes mais curtos e caminhos canônicos para website, marca e assets sociais/comerciais."
why: "Isso reduz ambiguidade entre arquivos do site público, fontes internas de marca e outputs pesados, facilitando navegação local, retomada em outro computador e futura replicação para Google Drive."
source: "codex-session"
created_at: "2026-06-29T00:00:00.000Z"
updated_at: "2026-06-29T00:00:00.000Z"
tags: ["repo-structure","canonical-paths","website","brand","assets","cleanup"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/assets/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/assets/brand/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/assets/drive/asset-manifest.json","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/ops/server/other-computer-onboarding.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/build_dist.sh"]
related_ids: ["20260628-repositorio-foi-enxugado-e-outros-pcs-devem-usar-main-drive-e-caminhos-canonicos"]
issue: ""
pr: ""
commit: ""
---

## Details

Os caminhos canônicos agora são:

- `docs/website/` para documentação do site
- `ops/web/` para acessos e operação web local
- `assets/brand/logos/site/` para a família de logos usada no site e em materiais institucionais
- `assets/brand/logos/product/` para a família de logos de software/produto
- `assets/business-kit/` para kit comercial final
- `assets/social/` para peças sociais, templates, batches e imagens de apoio

Os caminhos antigos `docs/site/`, `ops/website/`, `site/logos/`, `site/assets/brand/`, `assets/deliverables/business-kit/`, `assets/deliverables/social-assets/`, `assets/brand/logos/site-and-institutional-high-res/` e `assets/brand/logos/systems-and-apps/` deixaram de ser os caminhos de trabalho.
