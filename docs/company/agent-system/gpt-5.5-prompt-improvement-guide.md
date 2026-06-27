# Guia de Prompt GPT-5.5 para Agentes da RITO

## Objetivo

Padronizar os prompts da RITO para aproveitar melhor o GPT-5.5, reduzindo excesso de instruções processuais e aumentando clareza de resultado, evidência, validação e parada.

Fontes oficiais consultadas:

- OpenAI Prompt guidance para GPT-5.5: `https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5.5`
- OpenAI Using GPT-5.5: `https://developers.openai.com/api/docs/guides/latest-model`

## Princípios

1. Começar pelo resultado esperado, não pelo passo a passo.
2. Manter personalidade e colaboração curtas.
3. Definir critérios de sucesso e parada para cada agente.
4. Separar fatos, inferências e hipóteses quando houver pesquisa ou análise.
5. Dar orçamento explícito para busca e validação.
6. Validar entregas quando houver ferramenta ou evidência disponível.
7. Usar raciocínio mais alto só quando o prompt e a validação já estiverem bem definidos.
8. Manter contexto estável antes de contexto dinâmico quando futuramente usarmos chamadas via API com cache.

## Estrutura recomendada

Use este formato para novos prompts ou revisões grandes:

```text
Role:
[1-2 frases sobre função, contexto e responsabilidade do agente]

# Personality
[tom e colaboração, curto]

# Goal
[resultado visível esperado]

# Success criteria
[o que precisa estar verdadeiro antes de concluir]

# Constraints
[limites de negócio, evidência, segurança, canal e revisão humana]

# Evidence and retrieval budget
[fontes aceitas, quando buscar mais, quando parar, como lidar com ausência de evidência]

# Validation loop
[checagens mínimas antes de finalizar]

# Output
[seções, tamanho, formato e linguagem]

# Stop rules
[quando perguntar, encaminhar, bloquear, fallback ou parar]
```

## Esforço de raciocínio sugerido

- `none`: triagens curtas, classificação simples, transformação estruturada sem ambiguidade.
- `low`: atendimento rápido, decisão operacional simples, validação de canal e tarefas com baixa pesquisa.
- `medium`: prospecção, growth, revisão, análise de campanha, síntese com múltiplas fontes e decisões comerciais.
- `high`: investigação crítica, auditoria de processo, incidentes de produção, estratégia com muitas dependências.
- `xhigh`: evitar como padrão; usar só em análises raras, assíncronas e muito complexas, quando houver ganho claro.

## Regras específicas para a RITO

### Prospecção

- O agente deve parar a pesquisa quando já houver evidência suficiente para entender o negócio, contato público e hipótese comercial segura.
- Ausência de informação não vira falha do lead; vira `unknown`, `manual-review` ou `nurture`.
- Não acessar Instagram automaticamente. Registrar apenas como referência pendente de validação humana.
- Todo registro pronto precisa diferenciar fato, inferência e hipótese.

### Disparo

- O agente de disparo decide transporte, não oferta.
- Envio frio exige revisão humana antes do disparo.
- Sucesso técnico não deve ser confundido com entrega, leitura ou interesse.
- Se o canal não estiver validado, aplicar fallback e registrar o motivo.

### Atendimento

- Classificar antes de responder: humana, autoresposta, menu, reação, bounce ou ruído.
- Responder curto quando o canal for WhatsApp.
- Não tratar autoresposta como interesse comercial.
- Encaminhar para comercial só quando houver sinal humano real.

### Growth e campanha

- Toda recomendação precisa declarar hipótese, ativo, métrica principal e próxima decisão.
- Não recomendar gasto sem página, evento de conversão e rotina de acompanhamento.
- Separar canal pago, orgânico, SEO, CRO e mensuração.

### Criativos

- Sempre declarar plataforma, superfície, dimensão, safe area e CTA.
- Para peça visual, validar render ou preview antes de aprovar quando houver ferramenta.
- Para prompt de imagem com GPT Image 2, usar `docs/company/agent-system/gpt-image-2-visual-prompting-guide.md`.
- Não aceitar arte com texto cortado, logo fraco, desalinhamento ou cara de slide/deck.

## Checklist de revisão de prompt

- O prompt começa com resultado esperado?
- Existem critérios claros de sucesso?
- Existem regras de parada?
- O agente sabe quando buscar mais e quando parar?
- O agente sabe o que fazer quando falta evidência?
- Existe validação antes de finalizar?
- O output é curto o suficiente para uso real?
- Há regras humanas para ações externas, dinheiro, legal, site ou publicação?
- O prompt evita duplicar instruções em muitos lugares?
- O prompt não força passo a passo quando o modelo pode escolher o melhor caminho?

## Melhorias aplicadas nesta revisão

- Criação deste guia como fonte comum para novos prompts.
- Inclusão de contrato GPT-5.5 no prompt base.
- Inclusão de orçamento de busca, evidência e parada no agente de prospecção.
- Inclusão de validação e parada no agente de disparo.
- Inclusão de classificação e critérios de resposta no agente de atendimento.
- Inclusão de critérios de mídia e mensuração no agente de growth.
- Inclusão de requisitos de plataforma, dimensão e revisão visual no agente criativo.
