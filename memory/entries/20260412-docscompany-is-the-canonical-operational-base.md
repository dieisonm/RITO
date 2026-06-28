---
id: "20260412-docscompany-is-the-canonical-operational-base"
project: "RITO"
type: "decision"
status: "active"
title: "docs/company is the canonical operational base"
summary: "The operational source of truth for the company lives under docs/company, while final customer-facing artifacts are generated into assets/deliverables/business-kit from those sources."
why: "This keeps one editable knowledge base for brand, commercial, legal and sales materials, while preserving repeatable generation of final assets."
source: "codex"
created_at: "2026-04-12T19:24:05.366Z"
updated_at: "2026-04-12T19:24:05.366Z"
tags: ["operations","documentation","deliverables"]
files: ["docs/README.md","assets/deliverables/business-kit/README.md","scripts/generate_final_business_assets.py","scripts/generate_pricing_calculator_xlsx.py"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

Institutional, commercial, client-ready, legal-operational, portfolio, presence, reviews and site-planning materials should be maintained in docs/company. Final DOCX, PDF, PPTX and XLSX assets are derivative outputs and should be regenerated from the source documents and scripts when the content changes.
