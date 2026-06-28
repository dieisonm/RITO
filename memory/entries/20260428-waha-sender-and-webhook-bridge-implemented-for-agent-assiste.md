---
id: "20260428-waha-sender-and-webhook-bridge-implemented-for-agent-assiste"
project: "RITO"
type: "fix"
status: "resolved"
title: "WAHA sender and webhook bridge implemented for agent-assisted WhatsApp"
summary: "RITO has a WAHA-based outbound sender and validated webhook bridge, but every real WhatsApp batch requires human approval of final copy, recipients and an exact rendered sample before apply."
why: "This establishes the actual operational bridge between inbound WhatsApp traffic and the Atendimento agent, and captures the non-obvious runtime behavior difference between a persistent foreground process and detached background execution in Codex."
source: "codex-session"
created_at: "2026-04-28T23:13:18.611Z"
updated_at: "2026-06-27T12:00:00-03:00"
tags: ["whatsapp","waha","agent","webhook","atendimento","inbound","outbound"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/whatsapp_waha_common.py","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/whatsapp_waha_outbound.py","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/whatsapp_waha_webhook.py","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/configure_waha_webhook.py","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/waha_webhook_local.sh","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/ops/ai-os/whatsapp/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/ops/ai-os/whatsapp/inbox/README.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/agents/agent-system/prompts/atendimento-relacionamento-agent.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/agents/agent-system/playbooks/phase-1/atendimento-relacionamento.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/agents/agent-system/workflow-map.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/.gitignore"]
related_ids: ["20260428-waha-local-installed-and-authenticated-for-rito-outbound-wha"]
issue: ""
pr: ""
commit: ""
---

## Details

Implemented Python-only WAHA integration without extra framework dependencies. Added scripts/whatsapp_waha_common.py for local env/API helpers, scripts/whatsapp_waha_outbound.py for session status, send-test, send-batch, send-reply and send-seen, scripts/whatsapp_waha_webhook.py as a local HTTP webhook receiver, and scripts/configure_waha_webhook.py to register WAHA session webhooks with HMAC and custom header token. Added inbox persistence under ops/ai-os/whatsapp/inbox/ with raw events, conversation logs per chat_id and pending-replies queue. Validated with real WAHA session.status events after reconfiguring the authenticated default session. Updated atendimento-relacionamento prompt/playbook and workflow-map so the Atendimento agent knows to read pending-replies.jsonl and answer via send-reply. In this Codex environment, the webhook receiver is most reliable as a long-lived foreground session; a local background helper script was added but detached background execution can be unstable under the tool runtime.

After a 2026-05-19 copy-quality incident, technical validation alone is no longer sufficient for outbound WhatsApp. Before any real `--apply`, the operator must approve the final accented Portuguese copy, an exact rendered sample, the reviewed recipient queue and the dry-run result. Raw queues, contact datasets, inbox events, sessions and run logs are operational private data and must not be committed to the public repository.
