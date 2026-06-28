# WhatsApp Inbox Local

## Objetivo

Persistir eventos recebidos do WAHA para que o agente de atendimento consiga:

- ler mensagens novas
- consultar histórico por conversa
- sugerir resposta com contexto
- registrar fila de pendências

## Estrutura

- `raw/`
  - eventos brutos recebidos do WAHA em JSONL
- `conversations/`
  - histórico por `chat_id`, também em JSONL
- `pending/`
  - fila de mensagens novas aguardando análise ou resposta

## Observação

Os dados operacionais dessa pasta são locais e não devem ser versionados.
