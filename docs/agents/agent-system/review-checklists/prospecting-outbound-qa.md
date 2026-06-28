# Checklist de QA para Prospecção e Outbound

## Regra principal

Nenhum lead outbound pode seguir para contato se qualquer item crítico abaixo estiver sem resposta.

## Fonte e rastreabilidade

- Cada fato comercial importante tem URL de origem.
- O site oficial foi diferenciado de perfis de terceiros.
- O Instagram, quando citado, veio apenas como referência indireta e foi marcado para verificação manual do usuário.
- A origem da informação foi classificada com clareza: site, diretório, busca, outro, referência manual.
- Se a fonte tiver risco de plataforma ou sensibilidade operacional, isso está anotado.

## Contato

- O e-mail é claramente comercial ou corporativo, quando possível.
- O telefone, WhatsApp ou e-mail encontrado foi classificado como `corporativo`, `pessoal-em-uso-comercial` ou `indefinido`.
- Existe justificativa para o canal sugerido.
- Se o canal sugerido for WhatsApp, existe `normalized_whatsapp` confirmado.
- `public_whatsapp` contém número ou link direto, nunca descrição vaga.
- Se o WhatsApp não está confirmado, existe `fallback_contact_channel` coerente.
- `contact_readiness` está coerente com as evidências.
- O lead não está marcado como `não contatar` ou `opt-out`.
- O checklist separa claramente sugestão de canal e validação técnica de envio.

## Disparo técnico

- Se o envio for por WhatsApp, existe `resolved_chat_id` obtido pelo transporte no momento do disparo.
- Se o transporte não confirmou o chat de WhatsApp, existe fallback coerente para `email`, `formulario`, `telefone-manual` ou `manual-review`.
- `dispatch_channel_final` está preenchido quando o lead entrou em fila de envio.
- `dispatch_ready` reflete a checagem técnica do agente de disparo, não só a hipótese da prospecção.
- `dispatch_error` ou `dispatch_readiness_reason` existe quando o canal final não pôde ser usado.

## Análise

- O resumo do negócio está coerente com a evidência.
- A oferta sugerida faz sentido para o estágio observado.
- A mensagem não presume dor específica sem evidência.
- A mensagem parte do tipo de negócio e de possibilidades plausíveis, não de uma deficiência afirmada sem prova.
- As hipóteses foram escritas como hipótese, não como certeza.
- A nota de confiança foi preenchida.

## Mensagem

- O texto não parece spam em massa.
- O texto cita observação real do negócio ou do canal.
- O texto cita possibilidades de solução coerentes com o tipo de negócio.
- O CTA é simples e respeitoso.
- Existe saída clara ou não insistência implícita.
- O texto evita promessas exageradas e buzzwords.

## Compliance

- Houve minimização de dados.
- Se houver dado pessoal, há base legal plausível e salvaguardas.
- A abordagem por WhatsApp não está configurada para automação fria.
- O lote respeita volume prudente e revisão humana.

## Critério de bloqueio

Bloquear se aparecer qualquer um dos itens abaixo:

- fonte duvidosa
- contato pessoal sem contexto comercial minimamente justificável
- WhatsApp sugerido sem número confirmado
- WhatsApp em fila de envio sem `resolved_chat_id`
- canal principal marcado como `email` sem e-mail público real
- canal principal marcado como pronto sem `contact_readiness = ready`
- canal final de disparo sem `dispatch_ready = true`
- oferta desconectada do negócio
- mensagem genérica demais
- hipótese vendida como fato
- automação fria por WhatsApp
- uso de Instagram como fonte ativa sem verificação manual do usuário
