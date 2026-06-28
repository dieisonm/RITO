---
id: "20260419-marketing-agent-hardening-must-be-tool-backed-and-evaluation"
project: "RITO"
type: "decision"
status: "active"
title: "Marketing agent hardening must be tool-backed and evaluation-driven"
summary: "RITO documented a hardening plan for marketing/growth agents after repeated Instagram rework. The system should stop treating direction as final output and separate strategy, creative production, branding and review with objective Definition of Done."
why: "Repeated Instagram failures showed that the existing marketing agent architecture was too document-centric and subjective. This decision creates a concrete correction path before further content production."
source: "codex"
created_at: "2026-04-19T21:57:25.688Z"
updated_at: "2026-04-19T21:57:25.688Z"
tags: ["marketing","agents","growth","instagram","hardening","evaluation","canva"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/agents/agent-system/marketing-agent-engineering-research.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/agents/agent-system/marketing-agent-hardening-plan.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/reviews/instagram-launch-flow-audit-and-dod.md"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

Research and local audit concluded that the main issue is not lack of agents but lack of clear ownership, tool-backed production and objective gates. New reference docs were created: marketing-agent-engineering-research.md and marketing-agent-hardening-plan.md. The recommended direction is: content owns angle/caption/CTA/brief; creative production owns final social asset generation and export; branding owns system-level identity rules; revisor owns objective gate; growth must operate by explicit modes (seo, meta_ads, google_ads, cro, measurement). Canva should be the primary production tool, but the Canva connector currently has no brand kit configured for RITO, so on-brand automation is limited until a brand kit is set up. Aeval should be adopted to create representative eval suites for content, growth and review outputs. For Instagram, the minimum publication workflow is brief -> production in tool -> format/grid validation -> package ready-to-publish.
