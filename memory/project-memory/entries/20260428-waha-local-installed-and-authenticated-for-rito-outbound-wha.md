---
id: "20260428-waha-local-installed-and-authenticated-for-rito-outbound-wha"
project: "RITO"
type: "fix"
status: "resolved"
title: "WAHA local installed and authenticated for RITO outbound WhatsApp"
summary: "Installed free local WAHA Core with Colima+Docker, persisted local credentials, authenticated the default WhatsApp session and standardized WEBJS as the reliable engine for the RITO operation."
why: "This is a major operational milestone for prospecting and future agent-assisted customer conversations, and it includes a non-obvious Core limitation that should persist across sessions."
source: "codex-session"
created_at: "2026-04-28T22:50:37.941Z"
updated_at: "2026-06-27T12:00:00-03:00"
tags: ["whatsapp","waha","docker","colima","outbound","inbound"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/operations/ai-os/whatsapp/waha/docker-compose.yml","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/operations/ai-os/whatsapp/waha/.env.example","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/operations/ai-os/whatsapp/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/waha_local.sh","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/.gitignore"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

WAHA Core was installed locally using Colima and Docker with helper script scripts/waha_local.sh. The container is exposed on localhost:3000 and stores credentials in operations/ai-os/whatsapp/waha/.env plus sessions in operations/ai-os/whatsapp/waha/.sessions. Core limitation discovered and documented: only session name 'default' is supported. The initial NOWEB setup could accept sends while leaving messages in PENDING, so the operational engine was changed to WEBJS, which proved more reliable for delivery. Authentication completed successfully for the RITO company account. WAHA remains the preferred transport for outbound and inbound WhatsApp automation, while credentials, sessions, inbox events and run logs stay local and outside Git.
