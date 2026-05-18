---
id: "20260428-waha-local-installed-and-authenticated-for-rito-outbound-wha"
project: "RITO"
type: "fix"
status: "resolved"
title: "WAHA local installed and authenticated for RITO outbound WhatsApp"
summary: "Installed free local WAHA Core with Colima+Docker, configured NOWEB engine, persisted local credentials, and authenticated the default WhatsApp session for the RITO company number."
why: "This is a major operational milestone for prospecting and future agent-assisted customer conversations, and it includes a non-obvious Core limitation that should persist across sessions."
source: "codex-session"
created_at: "2026-04-28T22:50:37.941Z"
updated_at: "2026-04-28T22:50:37.941Z"
tags: ["whatsapp","waha","docker","colima","outbound","inbound"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/operations/ai-os/whatsapp/waha/docker-compose.yml","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/operations/ai-os/whatsapp/waha/.env.example","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/operations/ai-os/whatsapp/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/waha_local.sh","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/.gitignore"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

WAHA Core was installed locally using Colima and Docker with helper script scripts/waha_local.sh. The container is exposed on localhost:3000, uses engine NOWEB, and stores credentials in operations/ai-os/whatsapp/waha/.env plus sessions in operations/ai-os/whatsapp/waha/.sessions. Core limitation discovered and documented: only session name 'default' is supported. Authentication completed successfully; /api/sessions/default status reached WORKING and /api/sessions/default/me returned id 555196599049@c.us with pushName 'RITO Rotinas Inteligentes de Tecnologia e Operação'. This replaces browser-only transport as the preferred path for future outbound and inbound WhatsApp automation.
