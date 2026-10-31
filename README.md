# RITO

Base principal da RITO Sistemas para site, documentação, operação e memória versionada.

## Estrutura

- `docs/`: documentação estável de marca, vendas, site, operações e agentes.
- `ops/`: operação viva, campanhas, WhatsApp, playbooks e rotinas locais.
- `ops/ai-os/growth/prospecting/base-prospeccao-rito.xlsx`: **base única de prospecção** (empresas, contatos e resultados), gerada por `scripts/build_prospect_base.py`. Fica fora do Git.
- `assets/brand/`: base de marca e logos fonte.
- `assets/business-kit/`: editáveis e PDFs comerciais pesados.
- `assets/social/`: peças e fontes pesadas de social media.
- `assets/deliverables/`: estrutura leve, READMEs e trilha dos entregáveis.
- `assets/drive/`: manifesto oficial dos arquivos pesados guardados no Google Drive.
- `memory/`: memória durável antiga do projeto (a memória atual fica no vault Obsidian).
- `scripts/`: automações de e-mail, caixa de entrada, base de prospecção, assets e precificação.
- `_arquivo/`: histórico fora da operação ativa (ver `_arquivo/README.md`).

## Site

O site institucional saiu deste repositório em 2026-10-26. Código, build e deploy ficam em `dieisonm/rito-site` (local: `~/Documents/Projects/Rito/dev/rito-site`); a Hostinger faz o Git Deployment da branch `hostinger` desse repositório. Não há mais build nem deploy a partir daqui.

## Caixas de e-mail

- Ler: `python3 -I scripts/read_hostinger_inbox.py --account contato|comercial --limit 20` (somente leitura).
- Mover para a lixeira: `python3 -I scripts/trash_hostinger_messages.py --account contato --from remetente@exemplo.com` (simulação) e `--apply` para mover.
- Credenciais em `rito-secrets.local.php` (`hostinger_mailbox` e `hostinger_mailbox_comercial`), fora do Git.

## Documentos principais

- `docs/brand/foundation.md`: posicionamento, tom, identidade, dominios e contatos.
- `docs/site/site-content.md`: estrutura editorial e textos-base do site.
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

- vai para Git: `docs/`, `ops/`, `memory/`, `scripts/`, SVGs de marca, READMEs e `assets/drive/asset-manifest.json`
- vai para Drive: PNG/JPG/PDF/DOCX/XLSX/PPTX pesados em `assets/brand/logos/`, `assets/business-kit/` e `assets/social/`
- fica só local: segredos, sessões, caches, inbox bruto, `.env` e arquivos temporários

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
