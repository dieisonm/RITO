# RITO

Base principal da RITO Sistemas para site, documentação, operação e memória versionada.

## Estrutura

- `site/`: site institucional e arquivos publicos de runtime.
- `docs/`: documentação estável de marca, vendas, site, operações e agentes.
- `ops/`: operação viva, campanhas, WhatsApp, playbooks e rotinas locais.
- `assets/brand/`: base de marca e logos fonte.
- `assets/business-kit/`: editáveis e PDFs comerciais pesados.
- `assets/social/`: peças e fontes pesadas de social media.
- `assets/deliverables/`: estrutura leve, READMEs e trilha dos entregáveis.
- `assets/drive/`: manifesto oficial dos arquivos pesados guardados no Google Drive.
- `memory/`: memória durável versionada do projeto.
- `scripts/`: automações, geração de assets, validações e publicação.

## Como abrir o site

Abra `site/index.html` no navegador.

## Como gerar a versao de deploy

Execute:

```bash
./scripts/build_dist.sh
```

O deploy operacional do site e feito somente por Git: o GitHub Actions publica a branch `hostinger`, e a Hostinger faz o deploy dessa branch.

Para gerar um `.zip` pronto para upload:

```bash
./scripts/package_hostinger.sh
```

Para publicar a branch pronta para Git Deployment na Hostinger:

```bash
./scripts/publish_hostinger_branch.sh
```

Nao usar upload direto para publicar o site. Qualquer arquivo ou script que proponha publicacao direta na hospedagem deve ser tratado como legado invalido.

## Fluxo recomendado de publicacao

### Repositorio principal

- Branch principal de desenvolvimento: `main`
- Repositorio GitHub: `https://github.com/dieisonm/RITO`

### Branch de deploy da Hostinger

- Branch de deploy estatico: `hostinger`
- Essa branch contem apenas os arquivos publicos do site
- Objetivo: permitir deploy direto na Hostinger sem expor `docs/`, `scripts/` e outros arquivos internos

### Configuracao na Hostinger

Se estiver usando `Git Deployment` na hospedagem comum, usar:

- Repositorio: `https://github.com/dieisonm/RITO.git`
- Ramo: `hostinger`
- Install Path: vazio, para publicar diretamente em `/public_html`
- Implantacao automatica: webhook do GitHub ativo para `push` na branch `hostinger`

Importante:

- para trabalho humano, usar apenas `main`
- `hostinger` existe apenas como branch tecnica publicada pelo workflow
- a branch `hostinger` precisa manter historico linear
- deploy so deve ser considerado concluido quando `https://ritosistemas.com/deploy-info.json` abrir e mostrar a mesma `asset_version` do `dist/deploy-info.json`
- mudancas em `docs/`, `ops/`, `memory/`, `assets/drive/`, `assets/business-kit/`, `assets/social/` e arquivos administrativos nao devem disparar deploy do site

## Documentos principais

- `docs/brand/foundation.md`: posicionamento, tom, identidade, dominios e contatos.
- `docs/site/site-content.md`: estrutura editorial e textos-base do site.
- `docs/ops/hostinger-deploy.md`: passo a passo para publicacao na Hostinger.
- `docs/ops/server/desktop-server-replication-runbook.md`: rotina do PC servidor 24/7.
- `docs/ops/server/other-computer-onboarding.md`: retomada rapida do projeto em outro computador.

## Arquivos grandes

Arquivos criativos pesados, como PNG, JPG, PDF, DOCX, XLSX, PPTX, exports de campanha e fontes de criação, devem ficar no Google Drive:

```text
RITO (raiz): https://drive.google.com/drive/folders/1FkgsOUtxmFdLIGwRBSmpqrFQ7EpClzxi
RITO/assets: https://drive.google.com/drive/folders/1t_ZfqPZl_-hhlzgPF3Lbnf3nOYPdZz3L
```

O Git guarda apenas a estrutura, SVGs fonte, READMEs, scripts, memória e o manifesto. Os binários pesados devem ser enviados ao Drive:

```bash
python3 scripts/drive_assets.py scan --write-manifest --write-queue
python3 scripts/drive_assets.py upload
python3 scripts/drive_assets.py check
```

Regra prática:

- vai para Git: `site/`, `docs/`, `ops/`, `memory/`, `scripts/`, SVGs de marca, READMEs e `assets/drive/asset-manifest.json`
- vai para Drive: PNG/JPG/PDF/DOCX/XLSX/PPTX pesados em `assets/brand/logos/`, `assets/business-kit/` e `assets/social/`
- fica só local: segredos, sessões, caches, inbox bruto, `.env` e arquivos temporários

## Atualização segura do Git sem disparar deploy do site

Para mudanças só de documentação, memória, operação ou política de assets:

```bash
git checkout main
git pull --ff-only origin main
git status --short
git add README.md docs/ memory/ assets/drive/ .gitignore scripts/drive_assets.py
git diff --cached --name-only
git push origin main
```

Antes do push, confirme que o diff staged não inclui:

- `site/**`
- `logos/**`
- `scripts/build_dist.sh`
- `.github/workflows/deploy-hostinger.yml`

Se esses caminhos não estiverem staged, o workflow de deploy do site não deve rodar.

## Informacoes iniciais cadastradas

- Nome comercial: RITO Sistemas
- CNPJ: `66.723.374/0001-43`
- Assinatura institucional: Rotinas Inteligentes de Tecnologia e Operacao
- Dominio principal: `ritosistemas.com`
- Dominio secundario: `ritosistemas.com.br`
- Hospedagem: Hostinger
- Localizacao: Novo Hamburgo - Rio Grande do Sul
- E-mail: `contato@ritosistemas.com`
- Telefone: placeholder aguardando definicao
