# Google Drive Asset Store

Esta pasta documenta a réplica oficial dos assets pesados da RITO no Google Drive.

## Fonte de verdade

- Git guarda código, documentação, memória, scripts, READMEs, SVGs fonte e manifestos.
- Google Drive guarda binários pesados e editáveis de trabalho.
- arquivos nunca devem existir só localmente se ainda forem reutilizados pelo projeto.

## Pastas canônicas no Google Drive

```text
RITO (raiz)
ID: 1FkgsOUtxmFdLIGwRBSmpqrFQ7EpClzxi
URL: https://drive.google.com/drive/folders/1FkgsOUtxmFdLIGwRBSmpqrFQ7EpClzxi

RITO/assets
ID: 1t_ZfqPZl_-hhlzgPF3Lbnf3nOYPdZz3L
URL: https://drive.google.com/drive/folders/1t_ZfqPZl_-hhlzgPF3Lbnf3nOYPdZz3L
```

## Manifesto

O arquivo versionado oficial é:

```text
assets/drive/asset-manifest.json
```

Ele registra:

- caminho local original;
- hash;
- tamanho;
- tipo de arquivo;
- dimensões quando possível;
- campanha ou contexto;
- status no Drive;
- `file_id` e URL do Google Drive quando o vínculo já tiver sido conferido.

## O que vai para Drive

- PNG/JPG de `assets/brand/logos/` que não são runtime do site
- tudo que for pesado em `assets/business-kit/`
- tudo que for pesado em `assets/social/`
- exports finais, fontes de campanha e editáveis comerciais

## O que fica no Git

- `site/`
- `docs/`
- `ops/`
- `memory/`
- `scripts/`
- SVGs fonte em `assets/brand/logos/systems-and-apps/`
- READMEs
- `assets/drive/asset-manifest.json`

## Fluxo padrão quando um novo arquivo é criado

1. Gerar ou receber o asset localmente.
2. Salvar no caminho canônico:

- logo/brand pesado: `assets/brand/logos/...`
- material comercial pesado: `assets/business-kit/...`
- peça social ou imagem-fonte: `assets/social/...`

3. Rodar o scanner:

```bash
python3 scripts/drive_assets.py scan --write-manifest --write-queue
```

4. Fazer upload dos arquivos pendentes:

```bash
python3 scripts/drive_assets.py upload
```

5. Se algum upload for feito manualmente, registrar ou revisar o manifesto.

6. Commitar apenas manifesto e documentação, nunca os binários pesados.

## Registro manual no manifesto

Se algum upload for feito fora do script, registrar o arquivo enviado:

```bash
python3 scripts/drive_assets.py register \
  --path assets/social/campanha/exemplo.png \
  --drive-id GOOGLE_DRIVE_FILE_ID \
  --drive-url https://drive.google.com/file/d/GOOGLE_DRIVE_FILE_ID/view
```

## Upload automatizado com script

O upload automatizado usa `rclone`.

O script considera como raízes padrão:

```text
assets/brand/logos
assets/business-kit
assets/social
```

Se `rclone` estiver configurado, o remote deve apontar para a conta nova e para a pasta `RITO` ou `RITO/assets`, conforme o setup local.

Comandos úteis:

```text
python3 scripts/drive_assets.py upload --dry-run
python3 scripts/drive_assets.py upload
python3 scripts/drive_assets.py check
```

## Regra operacional

Se um arquivo novo for importante para continuidade do projeto:

- ele não pode ficar só local
- ele deve ir para o caminho canônico local
- ele deve ser replicado para `RITO/assets`
- e a documentação/memória deve ser atualizada se isso mudar a operação
