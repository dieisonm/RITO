# WhatsApp Outbound Local

## Objetivo

Operar disparo local de WhatsApp pela RITO sem depender da API oficial da Meta nesta fase inicial.

## Stack atual

- `WAHA Core` local via Docker para transporte principal
- `WEBJS` como engine do WAHA
- fila de envio baseada em CSV
- receiver de webhook em Python puro rodando como sidecar do `docker-compose`

## Motivação da escolha

No ambiente atual do projeto:

- `WAHA` é a base mais sólida para evoluir de simples disparo para webhook e atendimento assistido
- o runtime local usa `Colima + Docker` para manter custo zero nesta fase

## WAHA local

Arquivos da instalação:

- `ops/ai-os/whatsapp/waha/docker-compose.yml`
- `ops/ai-os/whatsapp/waha/.env`
- `ops/ai-os/whatsapp/waha/.env.example`
- `scripts/waha_local.sh`

Comandos principais:

- puxar e subir:
  - `bash scripts/waha_local.sh up -d`
- ver logs:
  - `bash scripts/waha_local.sh logs -f`
- parar:
  - `bash scripts/waha_local.sh down`

Painel e Swagger local:

- `http://127.0.0.1:3000/`
- receiver local do webhook:
  - `http://127.0.0.1:8787/health`

Scripts principais do WAHA:

- status da sessão:
  - `python3 scripts/whatsapp_waha_outbound.py session-status`
- testar envio:
  - `python3 scripts/whatsapp_waha_outbound.py send-test --to 5551999999999 --message "Mensagem de teste" --apply`
- simular lote:
  - `python3 scripts/whatsapp_waha_outbound.py send-batch --dry-run`
- enviar lote real:
  - `python3 scripts/whatsapp_waha_outbound.py send-batch --apply --throttle-seconds 45`
- responder conversa:
  - `python3 scripts/whatsapp_waha_outbound.py send-reply --chat-id 5551999999999@c.us --message "Texto da resposta"`
- marcar como lido:
  - `python3 scripts/whatsapp_waha_outbound.py send-seen --chat-id 5551999999999@c.us`
- configurar webhook da sessão:
  - `python3 scripts/configure_waha_webhook.py`

Persistência:

- sessões do WAHA ficam em `ops/ai-os/whatsapp/waha/.sessions/`
- credenciais locais do WAHA ficam em `ops/ai-os/whatsapp/waha/.env`
- eventos recebidos ficam em `ops/ai-os/whatsapp/inbox/`

Engine escolhida para a operação:

- `WEBJS`
- motivo: no ambiente real da RITO, o `NOWEB` aceitou envios mas deixou mensagens presas em `PENDING`; `WEBJS` é mais pesado, porém mais alinhado com o caminho que já se mostrou confiável para envio

Limitação importante da versão atual:

- `WAHA Core` suporta apenas a sessão `default`
- se no futuro precisarmos de múltiplas contas WhatsApp em paralelo, isso exige `WAHA Plus`

## Scripts legados

- autenticar sessão:
  - `python3 scripts/whatsapp_web_outbound.py auth`
- testar envio unitário:
  - `python3 scripts/whatsapp_web_outbound.py send-test --to 5551999999999 --message "Mensagem de teste"`
- testar envio unitário sem abrir a janela:
  - `python3 scripts/whatsapp_web_outbound.py send-test --to 5551999999999 --message "Mensagem de teste" --headless`
- simular lote:
  - `python3 scripts/whatsapp_web_outbound.py send-batch --dry-run`
- enviar lote real:
  - `python3 scripts/whatsapp_web_outbound.py send-batch --apply --throttle-seconds 45`
- enviar lote real sem abrir a janela:
  - `python3 scripts/whatsapp_web_outbound.py send-batch --apply --throttle-seconds 45 --headless`

Observação:

- os scripts `whatsapp_web_outbound.py` e `waha_webhook_local.sh` ficam mantidos apenas para diagnóstico e laboratório
- o fluxo operacional da RITO deve usar `WAHA + webhook sidecar`, sem depender de fallback por browser

## Fila atual

Arquivo padrão:

- `ops/ai-os/growth/prospecting/territories/novo-hamburgo-rs/batches/2026-04-21-batch-001-whatsapp-manual-queue.csv`

## Regras operacionais

- só entram na fila contatos com `whatsapp_readiness = confirmed`
- a sessão autenticada não deve ser versionada
- o primeiro teste deve ser sempre no número pessoal do operador
- no começo, usar lotes pequenos
- a autenticação inicial por QR code continua visual
- depois da sessão persistida, os envios devem sair pelo WAHA

## Logs

As execuções ficam em:

- `ops/ai-os/whatsapp/runs/`

## Webhook e atendimento

Receiver local:

- endpoint de webhook: `POST /webhook/waha`
- health check: `GET /health`
- porta padrão local: `8787`
- serviço do compose: `webhook`

Persistência do receiver:

- bruto: `ops/ai-os/whatsapp/inbox/raw/`
- conversas: `ops/ai-os/whatsapp/inbox/conversations/`
- pendências novas: `ops/ai-os/whatsapp/inbox/pending/pending-replies.jsonl`

Configuração padrão do WAHA:

- URL interna entre containers:
  - `http://webhook:8787/webhook/waha`
- eventos padrão:
  - `session.status`
  - `message`
  - `message.any`
  - `message.ack`

O receiver já valida:

- `X-Rito-Webhook-Token`
- HMAC `sha512` do WAHA, quando presente

## Próxima evolução sugerida

Quando a operação validar:

- manter o WAHA como transporte principal
- conectar com `n8n` ou com um worker Python para classificação e resposta assistida
