# Arquitetura de Automacao de Outbound

## Objetivo

Desenhar como a RITO pode evoluir da prospeccao assistida para disparos semiautomaticos e automaticos com rastreabilidade, controle de fila e historico por empresa.

## Premissa

A prospeccao da RITO tem duas partes diferentes:

1. descoberta e analise das empresas
2. disparo e acompanhamento dos contatos

Essas duas partes nao devem ficar acopladas. O agente de prospeccao descobre, analisa e prepara o contato. O modulo de outbound decide se envia, quando envia, por qual canal e como registra a resposta.

## Estado atual que podemos aproveitar

- a base de prospeccao ja nasce estruturada por territorio e batch
- o projeto ja possui infraestrutura SMTP em `site/contact.php` e `rito-smtp.php`
- a fila atual pode ser operada a partir de planilha + arquivos do batch

## Arquitetura recomendada

### Camada 1. Descoberta

Responsavel:

- `Prospecção e Inteligência Comercial`

Saida:

- empresa analisada
- contato publico
- canal sugerido
- hipotese de oferta
- rascunho de e-mail ou WhatsApp

Limite:

- nao resolve `chatId`
- nao valida entrega
- nao decide o canal tecnico final no momento do disparo

### Camada 2. Revisao

Responsavel:

- `Revisor`
- `Comercial`, quando o lote estiver proximo do envio

Saida:

- `pronta-para-contato`
- `bloqueada`
- `nao-contatar`

### Camada 3. Fila de envio

Responsavel:

- `Disparo / Outbound`

Entradas:

- registros aprovados
- canal escolhido
- horario permitido
- cadencia
- transporte disponivel: SMTP, WAHA, formulario ou fluxo manual

Saidas:

- `enviado`
- `falhou`
- `aguardando-resposta`
- `fallback`
- `resolved_chat_id`
- `dispatch_channel_final`

Regras:

- validar o canal no momento do envio
- resolver `chatId` tecnico em tempo real quando o canal for WhatsApp
- usar exatamente o `chatId` retornado pelo transporte
- se a resolucao tecnica falhar, cair para o canal de fallback
- registrar `dispatch_ready`, `dispatch_error` e tentativas

### Camada 4. Resposta e follow-up

Responsavel:

- `Atendimento e Relacionamento`
- `Comercial`

Saidas:

- resposta registrada
- follow-up agendado
- lead promovido para proposta

## Modelo recomendado por canal

### E-mail

#### Fase 1. Semiautomatico

- gerar o e-mail a partir da fila aprovada
- enviar um por um com revisao humana
- registrar data, assunto, resposta e proximo passo

#### Fase 2. Automatico com aprovacao em lote

- aprovar de `10` a `20` e-mails por vez
- o sistema envia com throttling
- registrar entrega, bounce e resposta

#### Infraestrutura recomendada

Curto prazo:

- usar o SMTP ja existente da RITO, reaproveitando a estrutura de `rito-smtp.php`

Medio prazo:

- migrar o envio outbound para um remetente dedicado, como `contato@` ou `comercial@`
- separar e-mail de formulario do site de e-mail de prospeccao
- configurar SPF, DKIM e DMARC para melhorar entregabilidade

#### Regras operacionais

- no comeco, limitar o volume diario
- sugerido:
  - semana 1: `10` por dia util
  - semana 2: `15` por dia util
  - semana 3 em diante: `20` a `30` por dia util, conforme resposta e reputacao
- espacamento entre disparos:
  - `60` a `180` segundos
- nao disparar lotes grandes sem aquecimento

### WhatsApp

#### Fase 1. Manual assistido

- o sistema gera o texto
- o sistema so inclui na fila casos com `whatsapp_readiness = confirmed`
- o agente de disparo ainda precisa resolver `chatId` antes do envio
- o operador abre link pre-preenchido
- envio humano, um a um
- ideal para lotes pequenos e canais publicos do negocio

#### Fase 2. Semiautomatico local

- o sistema monta a fila
- o operador valida e aciona disparo por lotes pequenos
- o envio roda por infraestrutura local, sem Meta API
- ainda com forte revisao humana

#### Opcao gratuita recomendada agora

Para a RITO, a melhor opcao gratuita e local para disparo inicial e:

- `WAHA Core` self-hosted

Motivos:

- roda localmente ou em Docker
- expos API HTTP simples para envio
- permite evoluir depois para webhook e recebimento
- conversa bem com Python e com n8n
- evita automacao de navegador montada do zero

Opcoes que nao sao a melhor base principal:

- `PyWhatKit`: simples demais e dependente de abrir o WhatsApp Web de forma frágil
- `Playwright` ou `Selenium` puro: servem para laboratorio, mas criam manutencao demais
- `OpenWA`: alternativa interessante, mas hoje a recomendacao principal continua `WAHA Core` pela simplicidade do caminho atual da RITO

#### Caminho recomendado para a RITO

1. corrigir e endurecer a fila de prospeccao
2. operar a fila manual assistida
3. subir `WAHA Core` localmente so para disparo
4. deixar respostas manuais neste primeiro momento
5. se a operacao provar valor, ligar webhook e depois plugar `n8n` ou Python para classificar conversas

#### Regra critica para numeros novos

- numeros desconhecidos nao devem ser enviados assumindo `@c.us`
- o agente de disparo deve consultar o transporte para obter o `chatId` real
- em numeros do Brasil, o transporte pode devolver `@c.us` ou `@lid`
- o envio deve usar exatamente esse `chatId`

## Sequencia ideal de implantacao

### Etapa 1. Operar com a planilha

- aprovar lote
- registrar canal
- enviar manualmente
- capturar resposta

### Etapa 2. Criar fila automatizada de e-mail

- ler registros `pronta-para-contato`
- enviar por SMTP com throttling
- atualizar status automatico

### Etapa 3. Integrar respostas

- e-mail reply -> registro no lead
- formulario -> registrar no mesmo dossie
- WhatsApp -> mover para atendimento/comercial

### Etapa 4. Integrar recebimento e automacao de resposta

- webhook de mensagem
- status de entrega
- historico por lead
- agente de atendimento com aprovacao humana no começo

## Estrutura tecnica minima

### Banco ou fonte de verdade

Pode comecar com:

- planilha operacional
- CSV do batch
- JSON de outreach

Depois evoluir para:

- SQLite ou Postgres

### Campos extras para fila

- `approved_for_send`
- `send_channel`
- `dispatch_channel_final`
- `resolved_chat_id`
- `number_exists`
- `dispatch_ready`
- `dispatch_readiness_reason`
- `send_status`
- `send_attempts`
- `last_sent_at`
- `reply_status`
- `next_follow_up_at`
- `owner_human`

### Workers sugeridos

- `outbound_email_worker`
- `outbound_queue_builder`
- `reply_sync_worker`
- `whatsapp_followup_worker`

## Recomendacao pratica para a RITO agora

1. automatizar e-mail antes de escalar WhatsApp
2. manter WhatsApp inicial com fila forte e numero confirmado
3. usar `WAHA Core` como proxima camada local de envio quando quisermos sair do clique manual
4. registrar tudo na mesma base
5. escalar volume so depois de validar resposta e qualidade da mensagem

## Decisao recomendada

Para o lote de Novo Hamburgo:

- comecar com e-mail automatico apenas para os casos com e-mail corporativo claro
- manter WhatsApp manual assistido para os demais
- usar a planilha operacional como fila unica

## Implementacao local atual

Enquanto `Docker` nao estiver disponivel no ambiente, o MVP operacional do projeto fica assim:

- `Playwright + Chromium persistente`
- `WhatsApp Web`
- fila CSV
- logs locais por execucao

Arquivos do MVP:

- `scripts/whatsapp_web_outbound.py`
- `ops/ai-os/whatsapp/README.md`

Posicionamento:

- isso resolve autenticacao por QR e disparo local
- isso nao substitui a futura opcao com `WAHA Core`
- quando o transporte mais robusto entrar, a fila atual continua servindo
