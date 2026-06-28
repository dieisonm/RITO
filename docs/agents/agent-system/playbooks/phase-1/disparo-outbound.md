# Playbook de Disparo / Outbound

## Objetivo

Executar contato outbound com segurança operacional, validando o canal na hora do envio e registrando tudo na mesma base.

## Resultado esperado

Ao final de cada lote, a RITO deve ter:

- leads com canal final validado
- envios registrados com status e tentativa
- fallback aplicado quando o canal sugerido falhar
- histórico pronto para atendimento ou comercial

## Etapas

### 1. Receber o lote aprovado

- ler somente registros aprovados
- confirmar template e CTA aprovados
- bloquear itens com `do_not_contact` ou `opt_out_received`

### 2. Validar o canal sugerido

- se for `email`, conferir se existe endereço público real
- se for `whatsapp-manual` ou `whatsapp`, consultar o transporte
- se for formulário, validar rota e campos mínimos
- se o canal sugerido falhar, tentar o `fallback_contact_channel`

### 3. Resolver o WhatsApp corretamente

- nunca assumir `55numero@c.us` como destino final
- consultar o transporte para obter o `chatId` real
- salvar `resolved_chat_id`
- salvar `number_exists`
- se não houver resolução confiável:
  - marcar `dispatch_ready = false`
  - preencher `dispatch_error`
  - cair para fallback

### 4. Decidir o canal final

- preencher `dispatch_channel_final`
- preencher `dispatch_readiness_reason`
- marcar `dispatch_ready = true` somente quando o canal estiver tecnicamente utilizável

### 5. Enviar com cadência

- executar com throttling
- registrar tentativa
- guardar identificador da mensagem quando existir
- marcar:
  - `dispatch_status = sent`
  - ou `failed`
  - ou `fallback`

### 6. Registrar telemetria

- horário do envio
- tentativa
- erro técnico
- status do transporte
- observação de entrega quando disponível

### 7. Encaminhar respostas

- resposta nova no WhatsApp entra em `ops/ai-os/whatsapp/inbox/pending/pending-replies.jsonl`
- atendimento assume a conversa
- comercial entra quando houver interesse claro

### 8. Fechar aprendizado do lote

Ao final de cada rodada, consolidar:

- taxa de bounce por e-mail
- WhatsApps entregues em dispositivo
- leituras
- autorespostas
- respostas humanas
- respostas qualificadas
- leads que exigem fallback

Se o lote tiver entrega técnica, mas baixa resposta humana, registrar isso como aprendizado de canal e abrir handoff para `Growth / Aquisição` com recomendação de aquecimento por SEO, Google Ads, Meta Ads ou conteúdo antes de escalar novos disparos frios.

## Critérios de bloqueio

- número de WhatsApp sem resolução técnica
- e-mail ausente quando o canal final for e-mail
- lead com `do_not_contact`
- mensagem não aprovada
- ausência de fallback em caso de falha previsível

## Regra de ownership

- prospecção prepara o dado
- revisão aprova a abordagem
- disparo valida transporte e envia
- atendimento responde

## Saída mínima por lead

- `dispatch_channel_final`
- `resolved_chat_id`
- `number_exists`
- `dispatch_ready`
- `dispatch_status`
- `dispatch_attempts`
- `dispatch_last_attempt_at`
- `dispatch_error`
