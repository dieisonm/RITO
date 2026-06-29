# Asset Sync

Esta área organiza a rotina de sincronização de arquivos grandes entre o projeto local, GitHub e Google Drive.

## Princípio

- O Git guarda o manifesto e as decisões.
- O Google Drive guarda os arquivos grandes.
- O servidor e o Mac principal leem o mesmo manifesto.
- Uploads pendentes são tratados como fila operacional, não como fonte de verdade.

## Pasta raiz no Drive

```text
RITO_Files
https://drive.google.com/drive/folders/1PrfwG1Sjawv4pF6ObxRAwKjpgX8iD00o
```

## Scanner

Gerar ou atualizar manifesto local:

```bash
python3 scripts/drive_assets.py scan --write-manifest --write-queue
```

Validar manifesto:

```bash
python3 scripts/drive_assets.py check
```

Subir assets pendentes para o Google Drive e atualizar manifesto:

```bash
python3 scripts/drive_assets.py upload --dry-run
python3 scripts/drive_assets.py upload
```

Registrar arquivo já enviado ao Drive:

```bash
python3 scripts/drive_assets.py register \
  --path assets/social/campanha/arte.png \
  --drive-id GOOGLE_DRIVE_FILE_ID \
  --drive-url https://drive.google.com/file/d/GOOGLE_DRIVE_FILE_ID/view
```

## Upload queue

A pasta `upload-queue/` recebe filas geradas localmente. Esses JSONs são temporários e ficam ignorados pelo Git para não transformar cada varredura em ruído de versionamento.

## Validação remota

```bash
rclone size rito-drive:
```
