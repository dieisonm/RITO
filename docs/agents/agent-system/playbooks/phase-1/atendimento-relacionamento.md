# Playbook: Atendimento e Relacionamento

## Objetivo

Acolher o contato inicial, entender a necessidade com rapidez e preparar o contexto para o comercial.

## Gatilhos

- mensagem nova no WhatsApp
- direct no Instagram
- mensagem no LinkedIn
- retorno de contato sem contexto suficiente

## Fluxo passo a passo

1. Identificar canal, nome e empresa, se houver.
2. Ler a mensagem e separar o que é dúvida, pedido ou oportunidade.
3. Responder com tom cordial e objetivo.
4. Fazer perguntas curtas que ajudem a qualificar a demanda.
5. Resumir o contexto em poucas linhas.
6. Encaminhar para comercial quando houver sinal de oportunidade real.

## Operação no WhatsApp da RITO

1. Ler novas entradas em `ops/ai-os/whatsapp/inbox/pending/pending-replies.jsonl`.
2. Abrir o histórico do `chat_id` correspondente em `ops/ai-os/whatsapp/inbox/conversations/`.
3. Decidir se a ação é:
   - marcar como lido
   - responder
   - escalar para comercial
   - escalar para humano
4. Para marcar como lido:
   - `python3 scripts/whatsapp_waha_outbound.py send-seen --chat-id <chat_id>`
5. Para responder:
   - `python3 scripts/whatsapp_waha_outbound.py send-reply --chat-id <chat_id> --message "..." `
6. Registrar no resumo da conversa a próxima ação comercial, se houver.

## Critérios de qualidade

- clareza na primeira resposta
- tom humano e profissional
- perguntas úteis, sem excesso
- qualificação suficiente para o comercial agir bem

## Checklist de saída

- mensagem inicial pronta
- resumo do contato
- canal de origem registrado
- próxima ação definida
- handoff para comercial ou orquestrador

## O que registrar na memória

- dúvidas recorrentes
- objeções frequentes
- formas de abordagem que funcionam melhor
- respostas padrão aprovadas

## Quando escalar para humano

- pedido de preço fechado
- reclamação ou insatisfação
- dúvida jurídica, contratual ou técnica sensível
- conversa com risco comercial alto
