---
id: "20260816-backup-do-env-local-do-relatorio-vendas-web-no-google-drive-rito-excecao"
project: "RITO"
type: "decision"
status: "active"
title: "Backup do .env.local do relatorio-vendas-web no Google Drive RITO (excecao a regra de segredos local-only) + regra de sync entre PCs"
summary: "O arquivo de segredos do relatorio-vendas-web foi copiado para o Google Drive RITO como backup sincronizavel entre computadores. LOCAL: S:/RITO/Projetos/relatorio-vendas-web/.env.local. DRIVE: H:/Meu Drive/RITO/secrets/relatorio-vendas-web/.env.local (conta dieison.medinger@gmail.com = drive H:, a mesma conta do RITO Drive). Isso e uma EXCECAO consciente a politica RITO de que segredos ficam local-only (fora de Git e Drive) — feita porque alguns tokens dependem de acesso do cliente e nao dao para regenerar a vontade. Continua fora do Git (.env.local ja e ignorado) e nunca deve ser compartilhado nem tornado publico; manter a pasta secrets privada."
why: "O usuario pediu um backup do .env.local que sincronize entre computadores, porque perder alguns tokens (que exigem acesso do cliente) e caro. Registrado para nao esquecer onde esta e para manter local e Drive iguais."
source: "codex"
created_at: "2026-08-16T16:36:26.550Z"
updated_at: "2026-08-16T16:36:26.550Z"
tags: ["relatorio-vendas","env","secrets","google-drive","sync","backup","onboarding","deploy-safety"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/.env.local","H:/Meu Drive/RITO/secrets/relatorio-vendas-web/.env.local"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

## Onde esta

- LOCAL (fonte de trabalho): `S:/RITO/Projetos/relatorio-vendas-web/.env.local`
- DRIVE (backup): `H:/Meu Drive/RITO/secrets/relatorio-vendas-web/.env.local` — conta `dieison.medinger@gmail.com` (drive `H:`), mesma conta do RITO Drive (`H:/Meu Drive/RITO`).

## Regra de sync (a mais recente vence)

SEMPRE, antes de trabalhar no relatorio-vendas-web, comparar a versao LOCAL (S) com a do DRIVE (H) — por data de modificacao e/ou hash. Se forem diferentes, atualizar a MAIS ANTIGA a partir da MAIS NOVA:

- Mudou o `.env.local` LOCAL aqui (novo token, nova chave) -> copiar S -> H (atualiza o Drive).
- O `.env.local` do DRIVE esta mais novo (foi alterado em outro computador) -> copiar H -> S (pega a versao do Drive como a mais recente).
- Se forem iguais (hash igual), nada a fazer.

Comando de verificacao rapida (PowerShell): comparar `(Get-Item ...).LastWriteTime` e `(Get-FileHash ...).Hash` dos dois caminhos.

## Politica e seguranca

- Isto contraria a regra padrao RITO (ver `20260630-drive-root-e-politica-de-sync-da-rito-foram-corrigidos`): segredos sao local-only. E uma excecao deliberada SO para este `.env.local`, como backup pessoal no Drive privado do usuario.
- NUNCA commitar no Git, NUNCA compartilhar a pasta `secrets`, NUNCA colar os valores em chat/doc versionado.
- Em outro computador: puxar do Drive para recriar o `.env.local` (o repo nao traz o arquivo; `.env.local` e ignorado no Git).
