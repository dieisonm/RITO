# Google Drive Asset Store

Esta pasta guarda a ponte entre o GitHub da RITO e os arquivos grandes salvos no Google Drive.

## Decisão

- GitHub é a fonte de verdade para código, documentação, prompts, scripts, templates, memória e manifestos.
- Google Drive é a fonte de verdade para arquivos pesados: imagens geradas, vídeos, PDFs, exports de campanha e imagens-fonte.
- OneDrive via navegador fica apenas como contingência manual, não como mecanismo operacional do servidor.

## Pasta raiz no Google Drive

```text
Nome: RITO_Files
ID: 1PrfwG1Sjawv4pF6ObxRAwKjpgX8iD00o
URL: https://drive.google.com/drive/folders/1PrfwG1Sjawv4pF6ObxRAwKjpgX8iD00o
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
- `file_id` e URL do Google Drive quando o upload estiver concluído.

## Fluxo de trabalho

1. Gerar ou receber o asset localmente.
2. Rodar o scanner:

```bash
python3 scripts/drive_assets.py scan --write-manifest --write-queue
```

3. Fazer upload dos arquivos pendentes:

```bash
python3 scripts/drive_assets.py upload
```

4. Se algum upload for feito manualmente, registrar o arquivo enviado:

```bash
python3 scripts/drive_assets.py register \
  --path assets/deliverables/social-assets/exemplo.png \
  --drive-id GOOGLE_DRIVE_FILE_ID \
  --drive-url https://drive.google.com/file/d/GOOGLE_DRIVE_FILE_ID/view
```

5. Commitar o manifesto atualizado.

## Upload automatizado

O upload automatizado usa `rclone`.

Remote configurado neste Mac:

```text
rito-drive:
```

Destino:

```text
Google Drive / RITO_Files
```

Comandos úteis:

```bash
python3 scripts/drive_assets.py upload --dry-run
python3 scripts/drive_assets.py upload
rclone size rito-drive:
```

## Observação sobre o conector do Google Drive

O conector disponível no Codex consegue validar a pasta, listar arquivos e trabalhar com Docs/Sheets/Slides. Nesta sessão, ele não expôs upload binário genérico de PNG/JPG/PDF. Por isso, o upload binário foi resolvido com `rclone`.

Alternativas se `rclone` não estiver configurado em outro computador:

- Google Drive no navegador;
- Google Drive Desktop;
- futura ferramenta de upload binário quando disponível no Codex.

Depois do upload, o manifesto continua sendo atualizado no Git para manter Mac e servidor sincronizados.

## O que deve sair do Git

- imagens pesadas em `assets/deliverables/`
- binários comerciais como `docx`, `xlsx`, `pptx` e `pdf` em `assets/deliverables/business-kit/`
- PNGs institucionais de alta resolução em `assets/brand/logos/site-and-institutional-high-res/`

No Git devem ficar apenas:

- o manifesto `assets/drive/asset-manifest.json`
- os READMEs e estruturas de pasta
- assets leves realmente necessários para runtime do site em `site/`
