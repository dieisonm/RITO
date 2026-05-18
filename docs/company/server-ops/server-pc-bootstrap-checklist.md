# Checklist de Bootstrap do PC Servidor

Use este checklist junto com `desktop-server-replication-runbook.md`.

## Antes de começar neste computador

- Confirmar que o repositório atual foi revisado, commitado e enviado para o GitHub.
- Confirmar qual branch o PC servidor deve usar.
- Separar credenciais em canal seguro, sem colocar senhas no Git.
- Confirmar que `memory/project-memory/entries/` existe no clone.
- Confirmar que `assets/drive/asset-manifest.json` existe no clone.
- Usar Google Drive `RITO_Files` para arquivos grandes.
- Confirmar que nenhuma automação de Instagram será usada.

## Instalar no PC servidor

- Codex.
- Git.
- GitHub CLI (`gh`).
- Python 3.12 ou superior.
- PHP CLI.
- Node.js LTS.
- Docker Desktop ou Docker + Docker Compose.
- Navegador Chrome ou Chromium.
- Plugins úteis do Codex: GitHub, Browser, Google Drive, Canva opcional, Documents/Spreadsheets/Presentations se forem necessários.

## Clonar e validar

```bash
git clone https://github.com/dieisonm/RITO.git
cd RITO
git status --short
```

Se a operação ainda depender de arquivos não commitados deste Mac, primeiro corrigir isso no GitHub. Se forem arquivos grandes, subir para o Google Drive e registrar em `assets/drive/asset-manifest.json`.

## Preparar WAHA

```bash
cp operations/ai-os/whatsapp/waha/.env.example operations/ai-os/whatsapp/waha/.env
```

Editar `.env` localmente:

- trocar `WAHA_API_KEY`;
- trocar senhas do dashboard e Swagger;
- trocar `RITO_WAHA_WEBHOOK_SECRET`;
- trocar `RITO_WAHA_WEBHOOK_TOKEN`;
- ajustar `WAHA_IMAGE` conforme arquitetura.

Recomendação de imagem:

- Apple Silicon: `devlikeapro/waha:arm`
- Windows/Linux Intel ou AMD: validar uma tag x86 do WAHA antes de subir, normalmente `devlikeapro/waha:latest`

## Subir WhatsApp

```bash
bash scripts/waha_local.sh up -d
python3 scripts/whatsapp_waha_outbound.py session-start
python3 scripts/whatsapp_waha_outbound.py session-status
python3 scripts/configure_waha_webhook.py
curl -s http://127.0.0.1:8787/health
```

Depois abrir `http://127.0.0.1:3000/`, escanear o QR Code com o WhatsApp Business da RITO e testar envio apenas para número próprio aprovado.

## Validar memória

Memória versionada:

```bash
find memory/project-memory/entries -type f | wc -l
```

MCP opcional:

```bash
cd /caminho/para/Automations
./project-memory-mcp/scripts/install-codex-mcp.sh
```

## Validar assets do Drive

```bash
python3 -B scripts/drive_assets.py check
```

Pasta raiz:

```text
https://drive.google.com/drive/folders/1PrfwG1Sjawv4pF6ObxRAwKjpgX8iD00o
```

## Primeiro teste operacional

- Rodar build do site localmente.
- Verificar status WAHA.
- Enviar mensagem de teste para número pessoal aprovado.
- Confirmar que webhook gravou a conversa localmente.
- Criar um commit pequeno de documentação ou log operacional.
- Fazer `git push`.
- No Mac principal, fazer `git pull` e confirmar que a alteração chegou.

## Travas obrigatórias

- Não automatizar Instagram.
- Não disparar campanha paga.
- Não enviar lote frio sem aprovação humana explícita.
- Não commitar `.env`, sessão WAHA, logs brutos de inbox, credenciais SMTP/IMAP, credenciais de hospedagem ou documentos `.local.md`.
- Não commitar arquivos pesados de `deliverables/`; registrar no Drive e no manifesto.
- Não deixar dois computadores editando o mesmo arquivo operacional ao mesmo tempo.
