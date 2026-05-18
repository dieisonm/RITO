---
id: "20260518-rito-passa-a-usar-github-first-com-google-drive-para-assets-"
project: "RITO"
type: "decision"
status: "active"
title: "RITO passa a usar GitHub-first com Google Drive para assets pesados"
summary: "A arquitetura operacional foi ajustada para GitHub como fonte de verdade de código, docs, scripts, prompts, memória e manifestos, com Google Drive RITO_Files como armazenamento de imagens, vídeos, PDFs e exports pesados."
why: "Isso evita depender do OneDrive corporativo via browser e reduz risco de estouro/crescimento do repositório Git com binários gerados, mantendo Mac e servidor sincronizados por Git e manifestos versionados."
source: "codex-session"
created_at: "2026-05-18T15:29:07.187Z"
updated_at: "2026-05-18T15:29:07.187Z"
tags: ["github-first","google-drive","assets","server-ops","memory","sync"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/assets/drive/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/assets/drive/asset-manifest.json","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/drive_assets.py","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/memory/project-memory/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/memory/project-memory/entries","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/.gitignore","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/company/server-ops/desktop-server-replication-runbook.md"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

Foi criada a pasta assets/drive com README e asset-manifest.json apontando para a pasta RITO_Files no Google Drive. O script scripts/drive_assets.py escaneia mídia local, calcula hash/tamanho/dimensões, atualiza manifesto, gera fila de upload e permite registrar file_id/URL após upload. A primeira varredura encontrou 37 assets locais marcados como local_pending_upload. A memória do projeto foi espelhada em memory/project-memory/entries para ser versionada no Git. .gitignore passou a ignorar .colima, filas temporárias de upload e binários pesados de deliverables. O conector atual do Google Drive valida/lista a pasta, mas não expõe upload binário genérico; por isso, uploads de PNG/JPG/PDF ainda precisam ser feitos por Drive web/Desktop/rclone ou ferramenta futura, com registro posterior no manifesto.
