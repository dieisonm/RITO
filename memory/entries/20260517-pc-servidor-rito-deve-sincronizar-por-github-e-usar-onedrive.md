---
id: "20260517-pc-servidor-rito-deve-sincronizar-por-github-e-usar-onedrive"
project: "RITO"
type: "decision"
status: "active"
title: "PC servidor RITO deve sincronizar por GitHub e usar OneDrive navegador só como bootstrap"
summary: "A replicação do ambiente para um computador 24/7 foi documentada com GitHub como fonte principal de código/docs e OneDrive corporativo via navegador apenas como apoio manual de bootstrap ou contingência."
why: "O servidor precisa ser previsível para WAHA, WhatsApp, prospecção e atendimento; automação de OneDrive via browser é frágil por sessão, MFA e políticas corporativas, enquanto GitHub oferece histórico, revisão e sincronização confiável."
source: "codex-session"
created_at: "2026-05-17T19:23:43.277Z"
updated_at: "2026-05-17T19:23:43.277Z"
tags: ["server-ops","waha","sync","github","onedrive","project-memory"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/ops/server/desktop-server-replication-runbook.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/ops/server/server-pc-bootstrap-checklist.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/ops/server/server-codex-handoff-prompt.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/ops/server/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/waha_local.sh","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/ops/ai-os/whatsapp/waha/docker-compose.yml","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/ops/ai-os/whatsapp/waha/.env.example"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

Foram criados documentos em `docs/ops/server/` com runbook completo, checklist de bootstrap e prompt de handoff para o Codex do servidor. O runbook orienta instalação de Codex, GitHub CLI, Docker, Python, PHP, Node, skills customizadas e project-memory, além de travas para não automatizar Instagram, não enviar lotes frios sem aprovação e não commitar segredos ou inbox bruto. Também foi ajustado o WAHA para ser mais portátil: docker-compose agora aceita WAHA_IMAGE via `.env` e `scripts/waha_local.sh` não força `DOCKER_HOST` de Colima quando o ambiente usa Docker Desktop ou Docker Compose nativo.
