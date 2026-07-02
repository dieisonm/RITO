---
id: "20260702-fluxo-canonico-de-codigo-arquivos-e-deploy-do-relatorio-de-vendas"
project: "RITO"
type: "decision"
status: "active"
title: "Fluxo canonico de codigo, arquivos e deploy do Relatorio de Vendas foi definido"
summary: "O codigo web, a memoria, os assets-fonte, as copias de runtime e a publicacao Cloudflare agora possuem caminhos canonicos no S e um runbook versionado. Deploy so pode sair de working tree limpa, validada e enviada ao GitHub."
why: "Deploys anteriores publicaram alteracoes locais nao commitadas e a migracao C para S deixou memoria e branding divergentes. O processo precisava impedir novas perdas e publicacoes acidentais."
source: "codex-session"
created_at: "2026-07-02T21:27:31.549Z"
updated_at: "2026-07-02T21:27:31.549Z"
tags: ["relatorio-vendas","deployment","cloudflare-workers","github","supabase","canonical-paths","operations"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/docs/deployment-runbook.md","S:/RITO/Projetos/relatorio-vendas-web/docs/current-state.md","S:/RITO/Projetos/relatorio-vendas-web/README.md","S:/RITO/Automations/RITO/memory/README.md"]
related_ids: ["20260702-relatorio-de-vendas-web-esta-em-producao-com-cloudflare-e-supabase","20260702-assinatura-horizontal-areia-foi-restaurada-como-logo-do-relatorio-de-vendas"]
issue: ""
pr: ""
commit: ""
---

## Details

Codigo: `S:/RITO/Projetos/relatorio-vendas-web`, GitHub privado
`dieisonm/relatorio-vendas-web`, branch `master`. Memoria: exclusivamente
`S:/RITO/Automations/RITO/memory`. Producao: Worker Cloudflare `rito` em
`https://rito.relatorio-vendas.workers.dev`. Banco e autenticacao: Supabase
`xnjblqigsvnyuyfklcud`.

Assets de marca devem ser salvos primeiro na biblioteca canonica da RITO em
`S:/RITO/Automations/RITO/assets/brand/`. Se o navegador precisar servir o
arquivo, uma copia deve entrar em `public/` no repositorio web. O logo aprovado
e `rito-assinatura-horizontal-areia.svg`, presente nos dois locais.

Relatorios manuais ficam em `imports/`, base legada em `data/` e segredos em
`.env.local`; todos sao locais e ignorados pelo Git. Dados reais de producao
ficam no Supabase. Nenhuma credencial deve entrar em codigo, memoria ou GitHub.

Antes do deploy: atualizar `master`, exigir working tree limpa, executar
`npm ci`, `npm run lint`, `npx tsc --noEmit` e `npm run build`, depois carregar
`CLOUDFLARE_API_TOKEN` a partir do gerenciador de senhas e executar
`npm run deploy:cloudflare`. O Wrangler publica todo o conteudo do working tree,
nao apenas o ultimo commit; por isso alteracoes devem ser revisadas, commitadas
e enviadas antes da publicacao.

O login local e producao usam o mesmo Supabase Auth. A senha do banco Supabase
nao serve como senha do aplicativo. Em 02/07/2026, o usuario confirmou que as
mesmas credenciais Auth funcionam localmente e em producao.
