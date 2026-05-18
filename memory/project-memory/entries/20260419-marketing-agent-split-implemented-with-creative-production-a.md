---
id: "20260419-marketing-agent-split-implemented-with-creative-production-a"
project: "RITO"
type: "fix"
status: "active"
title: "Marketing agent split implemented with Creative Production and Instagram launch board"
summary: "RITO implemented the first hardening pass on marketing agents: content, growth, branding and revisor were rewritten, a new Creative Production / Social Design Ops role was added, and the Instagram launch trio is now tracked as a production package."
why: "This captures the first implemented correction to stop the marketing workflow from treating exploratory creative direction as final publishable output."
source: "codex"
created_at: "2026-04-19T23:13:24.289Z"
updated_at: "2026-04-19T23:13:24.289Z"
tags: ["marketing","agents","instagram","creative-production","workflow","fix"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/company/agent-system/prompts/content-agent.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/company/agent-system/prompts/growth-aquisicao-agent.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/company/agent-system/prompts/branding-agent.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/company/agent-system/prompts/revisor-agent.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/company/agent-system/prompts/creative-production-social-design-ops-agent.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/docs/company/agent-system/playbooks/phase-1/creative-production-social-design-ops.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/operations/instagram/launch-production-board.md","/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/scripts/generate_instagram_launch_assets.py"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

The agent system now separates strategy/copy from visual production. Updated files include content-agent.md, growth-aquisicao-agent.md, branding-agent.md, revisor-agent.md, corresponding playbooks, agent-directory.md, workflow-map.md, prompts/README.md and phase-1/README.md. A new prompt and playbook were added for Creative Production / Social Design Ops. For the Instagram launch, operations/instagram/launch-production-board.md now tracks the 3-post package, and generate_instagram_launch_assets.py was adjusted so the carousel relies less on human-centered stock imagery: slide 2 now uses an object-based calculator/document scene and slide 3 closes with a brand-led panel. Current assets remain 1080x1350 PNGs and are ready for human review before publication.
