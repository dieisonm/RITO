# Onboarding rápido em outro computador

Este guia existe para retomar o projeto sem depender de arquivos locais soltos.

## Fonte de verdade

- `main` é a única branch de trabalho humano.
- `hostinger` existe só como branch técnica de deploy do site.
- Git guarda código, documentação, memória, prompts, scripts e manifestos.
- Google Drive guarda imagens pesadas, exports e editáveis grandes.
- Arquivos sensíveis, sessões locais e caches nunca devem entrar no Git.

## Pastas canônicas

- `site/`: site institucional.
- `docs/`: documentação estável.
- `ops/`: operação viva.
- `memory/`: memória durável do projeto.
- `assets/brand/`: base de marca e logos.
- `assets/business-kit/`: editáveis e PDFs comerciais.
- `assets/social/`: assets sociais e imagens-fonte.
- `assets/deliverables/`: trilha leve dos entregáveis.
- `assets/drive/asset-manifest.json`: registro oficial dos assets pesados.

## Onde procurar cada coisa

- decisão de marca e logo: `docs/brand/` e `assets/brand/logos/`
- logos usados pelo site: `site/logos/`
- logos pesados para uso institucional e social: `assets/brand/logos/site/`
- logos fonte para sistemas e apps: `assets/brand/logos/systems-and-apps/`
- conteúdo e estrutura do site: `docs/site/`
- operação comercial, outbound, WhatsApp e campanhas: `ops/`
- decisões já tomadas: `memory/entries/`

## Primeiros passos no outro PC

```bash
git checkout main
git pull --ff-only origin main
python3 scripts/drive_assets.py check
./scripts/build_dist.sh
```

Se precisar validar o site empacotado:

```bash
python3 scripts/validate_dist.py --dist dist
```

## Regras simples para não quebrar a sincronização

- não trabalhar em caminhos antigos como `operations/`, `docs/company/` ou `memory/project-memory/`
- não versionar `.png`, `.jpg`, `.pdf`, `.docx`, `.xlsx`, `.pptx` pesados quando forem assets de trabalho
- não deixar arquivo importante apenas local
- se um asset pesado for criado, salvar em `assets/brand/logos/`, `assets/business-kit/` ou `assets/social/`, subir para o Drive e registrar no manifesto
- se uma decisão mudar a operação, registrar em `memory/entries/`

## Push seguro sem disparar deploy do site

Quando a mudança for só de documentação, memória, operação interna ou política de assets:

```bash
git checkout main
git pull --ff-only origin main
git add README.md docs/ memory/ assets/drive/ .gitignore scripts/drive_assets.py
git diff --cached --name-only
git push origin main
```

Antes do push, confirme que não há nada staged em:

- `site/**`
- `logos/**`
- `scripts/build_dist.sh`
- `.github/workflows/deploy-hostinger.yml`

Se esses caminhos não entrarem no commit, o deploy do site não deve rodar.

## O que nunca deve ficar só local

- logos oficiais e fontes de marca que ainda serão reutilizados
- apresentações, propostas, planilhas e templates finais
- documentação operacional
- decisões sobre estrutura, marca, deploy e sincronização

## Referências principais

- `README.md`
- `docs/README.md`
- `docs/ops/server/desktop-server-replication-runbook.md`
- `docs/brand/institutional/mini-brand-guide.md`
- `assets/drive/README.md`
