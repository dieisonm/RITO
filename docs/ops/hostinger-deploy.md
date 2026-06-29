# Hostinger Deploy

## Regra principal

O deploy do site da RITO deve ser feito somente por Git.

Fluxo canonico:

1. `main` guarda o projeto completo.
2. GitHub Actions roda apenas quando arquivos do site mudam.
3. O workflow gera a pasta `dist/`.
4. O workflow publica os arquivos estaticos na branch `hostinger`.
5. A Hostinger recebe o webhook de `push` na branch `hostinger`.
6. A Hostinger faz o checkout da branch em `public_html`.

Nao usar publicacao direta na hospedagem como rotina. Se algum arquivo local sugerir upload direto para publicar o site, tratar como legado invalido e remover antes de commitar.

## Configuracao da Hostinger

No Git Deployment da Hostinger:

- Repositorio: `https://github.com/dieisonm/RITO.git`
- Ramo: `hostinger`
- Install Path: vazio, para publicar diretamente em `/public_html`
- Auto Deployment: ativo

O site da RITO e estatico em HTML/CSS/JS. Nao usar fluxo de `Node.js`, `Frameworks`, React, Vite, Next.js ou similar.

## Workflow do GitHub

Arquivo:

```text
.github/workflows/deploy-hostinger.yml
```

Gatilho:

- `push` na branch `main`
- apenas quando houver mudancas em:
  - `site/**`
  - `logos/**`
  - `scripts/build_dist.sh`
  - `.github/workflows/deploy-hostinger.yml`

Isso evita que alteracoes em documentacao, memoria, operacao, agentes ou assets externos disparem deploy do site.

## Branches

- `main`: projeto completo, incluindo docs, scripts, memoria e operacao.
- `hostinger`: artefato estatico publicado, contendo apenas arquivos publicos do site.

A branch `hostinger` deve manter historico linear para a Hostinger conseguir atualizar o checkout sem conflitos.

## Publicacao automatica

Em publicacoes normais:

```bash
git add .
git commit -m "Mensagem"
git push origin main
```

Se a mudanca tocar arquivos do site, o GitHub Actions publica a branch `hostinger` automaticamente.

Se a mudanca tocar apenas `docs/`, `operations/`, `memory/`, `assets/drive/` ou outros arquivos administrativos, o deploy do site nao deve rodar.

## Publicacao manual da branch hostinger

Use apenas quando precisar regerar a branch de deploy localmente:

```bash
bash scripts/publish_hostinger_branch.sh
```

Esse comando:

- gera `dist/`
- cria uma publicacao limpa
- envia somente arquivos publicos para a branch `hostinger`

Depois, confirmar no GitHub e na Hostinger que o webhook foi recebido.

## Verificacao

O deploy so esta concluido quando:

```text
https://ritosistemas.com/deploy-info.json
```

mostrar a mesma `asset_version` gerada no build.

Tambem conferir:

- `https://ritosistemas.com/`
- `https://ritosistemas.com/pages/projeto-piloto.html`, quando a landing estiver em uso

## Diagnostico quando o site nao atualizar

Se a branch `hostinger` foi atualizada, mas o dominio nao mudou, investigar no painel da Hostinger:

- repositorio correto;
- branch `hostinger`;
- install path vazio;
- Auto Deployment ativo;
- ultimo log de deploy sem erro.

Se o problema persistir, corrigir a configuracao do Git Deployment na Hostinger. Nao criar fluxo paralelo de publicacao direta como solucao permanente.

## Dominio

- Dominio principal: `ritosistemas.com`
- Dominio secundario: `ritosistemas.com.br`

Na Hostinger, manter redirecionamento 301 de `ritosistemas.com.br` para `ritosistemas.com`.
