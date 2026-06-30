---
id: "20260630-drive-root-e-politica-de-sync-da-rito-foram-corrigidos"
project: "RITO"
type: "decision"
status: "active"
title: "Drive root e política de sync da RITO foram corrigidos"
summary: "A réplica oficial dos assets pesados passou a apontar para `RITO/assets` na conta `dieison.medinger@gmail.com`, com documentação e regras operacionais atualizadas para separar claramente o que vai para Drive, Git e local-only."
why: "O outro computador ficou sem contexto porque os links e instruções ainda apontavam para estruturas antigas, o que aumentava o risco de arquivos importantes ficarem apenas locais ou de commits administrativos acionarem deploy do site por engano."
source: "codex-session"
created_at: "2026-06-30T13:30:00.000Z"
updated_at: "2026-06-30T13:30:00.000Z"
tags: ["google-drive","sync","git-policy","deploy-safety","documentation","assets"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/assets/drive/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/ops/hostinger-deploy.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/ops/server/other-computer-onboarding.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/ops/server/desktop-server-replication-runbook.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/drive_assets.py","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/.gitignore"]
related_ids: ["20260628-repositorio-foi-enxugado-e-outros-pcs-devem-usar-main-drive-e-caminhos-canonicos","20260518-deploy-do-site-e-git-only-pela-branch-hostinger","20260518-rito-passa-a-usar-github-first-com-google-drive-para-assets-"]
issue: ""
pr: ""
commit: ""
---

## Details

O link canônico dos assets pesados foi corrigido para a pasta `RITO/assets` no Google Drive da conta `dieison.medinger@gmail.com`. A documentação passou a distinguir quatro classes de armazenamento: Git para código/docs/memória/SVGs fonte e manifestos; Drive para PNG/JPG/PDF/DOCX/XLSX/PPTX e outros binários pesados em `assets/brand/logos/`, `assets/business-kit/` e `assets/social/`; local-only para segredos, sessões e caches; e `site/` para os assets de runtime que realmente precisam participar do deploy. Também ficou explícito que `main` é a única branch de trabalho humano e que commits administrativos só são seguros quando não incluem `site/**`, `logos/**`, `scripts/build_dist.sh` ou `.github/workflows/deploy-hostinger.yml`.
