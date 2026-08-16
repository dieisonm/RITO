---
id: "20260816-env-local-do-relatorio-vendas-web-restaurado-neste-mac"
project: "RITO"
type: "operation"
status: "active"
title: ".env.local do relatorio-vendas-web foi restaurado neste Mac a partir do Google Drive"
summary: "O backup do .env.local do relatorio-vendas-web apareceu no Google Drive em RITO/secrets/relatorio-vendas-web/.env.local e foi baixado para o clone local deste Mac em /Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web/.env.local. O arquivo tem 726 bytes, permissao 600, hash SHA-256 bbe90f67923ceff0cbb0b52f323decb29d3f5960329e5b500a7848768772fc4a, e contem as variaveis esperadas sem ser versionado no Git."
why: "O usuario adicionou a pasta ausente no Drive e pediu para verificar novamente, restaurar o env localmente e atualizar a memoria. Esta entrada substitui o estado anterior de env pendente neste Mac."
source: "codex"
created_at: "2026-08-16T16:53:23Z"
updated_at: "2026-08-16T16:53:23Z"
tags: ["relatorio-vendas","env","secrets","google-drive","mac","local-setup","sync"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web/.env.local"]
related_ids: ["20260816-localizacao-do-clone-relatorio-vendas-web-neste-mac-e-env-pendente", "20260816-backup-do-env-local-do-relatorio-vendas-web-no-google-drive-rito-excecao"]
issue: ""
pr: ""
commit: ""
---

## Verificacao

- Drive: encontrado arquivo `.env.local` dentro da pasta `RITO/secrets/relatorio-vendas-web`.
- Local: restaurado em `/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web/.env.local`.
- Permissao local: `600`.
- Tamanho: `726` bytes.
- SHA-256: `bbe90f67923ceff0cbb0b52f323decb29d3f5960329e5b500a7848768772fc4a`.
- Variaveis presentes: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ACCESS_TOKEN`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`.
- Git do app mostra `.env.local` como ignorado (`!! .env.local`), portanto nao entra em commit.

Nunca colar valores do env em memoria, chat, docs ou Git.
