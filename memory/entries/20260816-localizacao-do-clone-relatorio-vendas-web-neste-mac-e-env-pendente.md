---
id: "20260816-localizacao-do-clone-relatorio-vendas-web-neste-mac-e-env-pendente"
project: "RITO"
type: "operation"
status: "active"
title: "Clone local do relatorio-vendas-web neste Mac foi validado; .env.local ainda precisa ser restaurado"
summary: "Neste Mac, o repo do app relatorio-vendas-web esta clonado em /Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web, remoto https://github.com/dieisonm/relatorio-vendas-web.git, branch master, alinhado ao origin/master no commit b38bb02. A pasta esta dentro do repo RITO apenas como workspace local e foi adicionada ao .gitignore do repo RITO para evitar commit acidental do app inteiro. O .env.local ainda NAO foi restaurado neste Mac: buscas locais nao encontraram o env do relatorio e o Google Drive conectado ao Codex nao mostrou RITO/secrets/relatorio-vendas-web/.env.local. Quando o Drive correto estiver acessivel, copiar o backup para /Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web/.env.local sem commitar."
why: "O usuario quer continuar o app neste PC e pediu para verificar a clonagem, achar o env e deixar memoria do local. A clonagem esta correta, mas o env depende do backup privado registrado em outra memoria; o conector atual do Drive nao conseguiu acessar esse arquivo."
source: "codex"
created_at: "2026-08-16T16:44:47Z"
updated_at: "2026-08-16T16:44:47Z"
tags: ["relatorio-vendas","local-setup","env","mac","google-drive","gitignore","onboarding"]
files: ["/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web", "/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web/.env.local", "/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/.gitignore"]
related_ids: ["20260816-backup-do-env-local-do-relatorio-vendas-web-no-google-drive-rito-excecao", "20260802-plano-de-edicao-de-vendedor-no-relatorio-de-comissao-e-workbook-de-setup"]
issue: ""
pr: ""
commit: ""
---

## Estado neste Mac

- Repo RITO: `/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO`.
- Clone do app: `/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web`.
- Remoto do app: `https://github.com/dieisonm/relatorio-vendas-web.git`.
- Branch do app: `master`.
- Commit validado do app: `b38bb02`.
- `node_modules`: ausente.
- `.env.local`: ausente neste Mac no momento desta verificacao.

## Env

O backup duravel do `.env.local` foi registrado em
`20260816-backup-do-env-local-do-relatorio-vendas-web-no-google-drive-rito-excecao`
como `H:/Meu Drive/RITO/secrets/relatorio-vendas-web/.env.local` no Windows.
No Mac, nao ha Google Drive montado localmente em `/Users/I858224/Library/CloudStorage`;
apenas OneDrive aparece. O conector Google Drive do Codex encontrou duas pastas
`RITO`, mas nenhuma `secrets` nem `.env.local`.

Quando o Drive correto estiver conectado/acessivel, restaurar o arquivo para:

`/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations/RITO/Projetos/relatorio-vendas-web/.env.local`

Nunca commitar `.env.local` nem colar valores em chat/documentacao.

## Git do repo RITO

`Projetos/` foi adicionado ao `.gitignore` do repo RITO para evitar que o clone
do app entre por acidente em commits de memoria/documentacao. Commits de memoria
devem continuar cirurgicos (`git add memory/entries/<arquivo>.md` e, quando
necessario, `.gitignore`), nunca `git add -A`.
