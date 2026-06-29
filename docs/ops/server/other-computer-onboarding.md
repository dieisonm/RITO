# Onboarding rápido em outro computador

Este guia existe para retomar o projeto sem depender de arquivos locais soltos.

## Fonte de verdade

- `main` é a única branch de trabalho.
- `hostinger` continua existindo só como branch técnica de deploy do site.
- Git guarda código, documentação, memória, prompts, scripts e manifestos.
- Google Drive guarda imagens pesadas, exports e editáveis grandes.
- Arquivos sensíveis, sessões locais e caches nunca devem entrar no Git.

## Pastas canônicas

- `site/`: site institucional.
- `docs/`: documentação estável.
- `ops/`: operação viva.
- `memory/`: memória durável do projeto.
- `assets/brand/`: fontes de marca e logos para uso interno.
- `assets/`: estrutura dos entregáveis.
- `assets/drive/asset-manifest.json`: registro oficial dos assets pesados.

## Onde procurar cada coisa

- decisão de marca e logo: `docs/brand/` e `assets/brand/logos/`
- logos usados pelo site: `assets/brand/logos/site/`
- logos para sistemas, dashboards, apps e interfaces criadas pela RITO: `assets/brand/logos/product/`
- conteúdo e estrutura do site: `docs/website/`
- operação comercial, outbound, WhatsApp e campanhas: `ops/`
- decisões já tomadas: `memory/entries/`

## Regra rápida de escolha de logo

- Se a entrega for site institucional, página pública, material comercial, Canva, proposta, PDF ou rede social, usar a família de `assets/brand/logos/site/`.
- Se a entrega for sistema, dashboard, app, portal, login, onboarding, header de produto, avatar de software ou interface interna, usar a família de `assets/brand/logos/product/`.
- Em sistemas criados por nós, a regra padrão é usar `assets/brand/logos/product/` e preferir SVG antes de PNG.
- Não puxar logo diretamente de memória, de screenshots antigas ou do HTML do site. Sempre partir da pasta canônica em `assets/brand/logos/`.

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
- se um asset pesado for criado, subir para o Drive e registrar no manifesto
- se uma decisão mudar a operação, registrar em `memory/entries/`

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
