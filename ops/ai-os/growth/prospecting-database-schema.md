# Esquema da Base de Prospecção

## Objetivo

Padronizar a base de empresas prospectadas para que descoberta, análise, revisão e contato usem a mesma estrutura.

## Registro mínimo por empresa

| Campo | Tipo | Obrigatório | Uso |
| --- | --- | --- | --- |
| `company_id` | texto | sim | identificador único |
| `company_name` | texto | sim | nome visível do negócio |
| `city` | texto | sim | cidade principal |
| `state` | texto | sim | UF |
| `territory_batch` | texto | sim | lote ou campanha territorial |
| `segment` | texto | sim | nicho presumido |
| `website_url` | url | não | site oficial |
| `instagram_url` | url | não | referência a Instagram obtida sem acesso direto; depende de verificação manual do usuário |
| `other_channels` | texto | não | Facebook, LinkedIn, catálogo, marketplace |
| `public_email` | texto | não | contato corporativo público |
| `public_phone` | texto | não | telefone comercial público |
| `public_whatsapp` | texto | não | WhatsApp comercial público |
| `normalized_whatsapp` | texto | não | WhatsApp em formato normalizado, somente se confirmado |
| `whatsapp_readiness` | texto | sim | confirmed, unconfirmed, not-found |
| `contact_type` | texto | sim | corporativo, pessoal-em-uso-comercial, indefinido |
| `primary_contact_channel` | texto | sim | canal sugerido pela prospecção: e-mail, formulário, telefone manual, WhatsApp manual, manual-review, outro |
| `fallback_contact_channel` | texto | não | próximo canal sugerido se o principal não estiver pronto |
| `contact_readiness` | texto | sim | prontidão do registro para revisão comercial: ready, fallback-needed, manual-review, blocked |
| `source_risk_note` | texto | não | observação de sensibilidade da fonte ou da plataforma |
| `source_primary_url` | url | sim | principal fonte usada |
| `source_secondary_urls` | texto | não | outras fontes |
| `business_summary` | texto | sim | o que o negócio faz |
| `digital_presence_stage` | texto | sim | básica, funcional, manual visível, madura |
| `observed_signals` | texto | sim | fatos observados |
| `suggested_offer_primary` | texto | sim | principal serviço sugerido |
| `suggested_offer_secondary` | texto | não | segunda hipótese |
| `suggested_solution_fronts` | texto | não | lista curta com exatamente `4` frentes plausíveis para oferecer |
| `offer_rationale` | texto | sim | justificativa com evidência |
| `outreach_angle` | texto | sim | enquadramento comercial da abordagem, sem presumir falta ou falha |
| `confidence_business` | número 1-5 | sim | confiança no entendimento do negócio |
| `confidence_contact` | número 1-5 | sim | confiança no contato |
| `confidence_offer_fit` | número 1-5 | sim | confiança na aderência da oferta |
| `review_status` | texto | sim | novo, revisando, aprovado, bloqueado, contatado |
| `do_not_contact` | booleano | sim | trava operacional |
| `opt_out_received` | booleano | sim | controle de saída |
| `last_verified_at` | data | sim | última checagem |
| `owner` | texto | sim | agente ou responsável humano |
| `resolved_chat_id` | texto | não | chat ID resolvido pelo transporte no momento do disparo |
| `number_exists` | booleano | não | resultado da checagem técnica do número no WhatsApp |
| `dispatch_channel_final` | texto | não | canal final escolhido pelo agente de disparo |
| `dispatch_ready` | booleano | não | se o lead está tecnicamente pronto para envio no canal final |
| `dispatch_readiness_reason` | texto | não | explicação curta da decisão de disparo |
| `dispatch_status` | texto | não | pending, sent, failed, fallback, replied, skipped |
| `dispatch_last_attempt_at` | data/hora | não | última tentativa de envio |
| `dispatch_attempts` | número | não | quantidade de tentativas |
| `dispatch_error` | texto | não | erro técnico ou motivo do fallback |

## Regras de preenchimento

- Sempre registrar pelo menos uma URL de origem.
- Se o contato parecer pessoal, mas estiver exposto pelo próprio negócio para atendimento, registrar isso em `contact_type`.
- Se o contato for formulário do site, registrar isso em `primary_contact_channel`.
- `public_whatsapp` não deve receber texto descritivo.
- `normalized_whatsapp` só pode ser preenchido quando o número estiver claramente confirmável.
- Se não houver WhatsApp confirmável, marcar `whatsapp_readiness = unconfirmed` ou `not-found`.
- Se o canal principal não estiver pronto, preencher `fallback_contact_channel` e ajustar `contact_readiness`.
- `primary_contact_channel` é uma sugestão da prospecção; o canal final de envio nasce em `dispatch_channel_final`.
- `contact_readiness` não substitui `dispatch_ready`.
- `resolved_chat_id` só deve ser preenchido pelo agente de disparo após checagem técnica do transporte.
- quando `primary_contact_channel = whatsapp-manual`, o agente de disparo deve consultar o transporte para resolver `chatId` e pode cair para outro canal se necessário.
- `instagram_url` não deve vir de navegação ativa no Instagram; quando existir, tratar como referência indireta e manual.
- `observed_signals` deve conter fatos, não opinião vaga.
- `suggested_solution_fronts` deve refletir exatamente `4` possibilidades plausíveis para o tipo de operação, não um diagnóstico fechado.
- `offer_rationale` deve amarrar oferta à evidência.

## Canais recomendados

Ordem padrão:

1. formulário do site
2. e-mail corporativo
3. contato pessoal em uso comercial, quando o próprio negócio o expuser
4. telefone comercial para contato humano
5. WhatsApp manual e altamente seletivo

## Regra específica para WhatsApp

Usar `whatsapp-manual` somente quando houver pelo menos uma destas evidências:

- número visível no site
- link `wa.me/<numero>`
- link `api.whatsapp.com/send?phone=<numero>`
- configuração pública do site que exponha o telefone sem ambiguidade

Se isso não existir:

- não marcar WhatsApp como canal principal
- escolher `email`, `formulario`, `telefone-manual` ou `manual-review`

## Saídas derivadas

Da base de prospecção podem nascer:

- fila de revisão
- fila de contato
- fila de disparo técnico
- campanhas por território
- lista de rejeições e opt-out
- base de aprendizados por segmento
