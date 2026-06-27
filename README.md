# RITO

Base inicial da empresa RITO Sistemas, pensada para organizar marca, site institucional e evolucao operacional desde o inicio.

## Estrutura

- `site/`: site institucional estatico com home e paginas principais.
- `docs/`: base da marca, conteudo do site e direcionamento institucional.
- `operations/`: espaco reservado para a evolucao futura das frentes operacionais.
- `assets/drive/`: manifesto dos arquivos grandes guardados no Google Drive.
- `memory/project-memory/`: memoria duravel versionada do projeto.

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

- a branch `hostinger` precisa manter historico linear
- nao usar `push -f` recorrente nessa branch, porque a Hostinger tende a fazer `pull/merge` no deploy automatico
- deploy so deve ser considerado concluido quando `https://ritosistemas.com/deploy-info.json` abrir e mostrar a mesma `asset_version` do `dist/deploy-info.json`
- mudancas em `docs/`, `operations/`, `memory/`, `assets/drive/` e arquivos administrativos nao disparam deploy do site

## Documentos principais

- `docs/brand-foundation.md`: posicionamento, tom, identidade, dominios e contatos.
- `docs/site-content.md`: estrutura editorial e textos-base do site.
- `docs/hostinger-deploy.md`: passo a passo para publicacao na Hostinger.
- `docs/company/server-ops/desktop-server-replication-runbook.md`: rotina do PC servidor 24/7.

## Arquivos grandes

Arquivos criativos pesados, como imagens geradas, vídeos, PDFs e exports de campanha, devem ficar no Google Drive:

```text
https://drive.google.com/drive/folders/1PrfwG1Sjawv4pF6ObxRAwKjpgX8iD00o
```

O Git guarda apenas o manifesto:

```bash
python3 scripts/drive_assets.py scan --write-manifest --write-queue
python3 scripts/drive_assets.py check
```

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
