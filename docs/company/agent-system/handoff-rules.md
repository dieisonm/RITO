# Regras de Handoff

## Objetivo

Garantir passagem clara de contexto entre agentes sem duplicidade de trabalho nem perda de informação.

## Regras gerais

- Todo handoff deve nomear o agente dono seguinte.
- Todo handoff deve indicar estado atual.
- Todo handoff deve explicitar pendências e risco.
- Um agente não deve continuar executando tema cujo ownership já mudou.
- Quando houver material externo ou sensível, o revisor entra antes da saída final.

## Formato mínimo

```text
Tipo de demanda:
Agente atual:
Agente de destino:
Objetivo:
Estado:
Contexto essencial:
Artefatos associados:
Pendencias:
Riscos:
Proxima acao esperada:
```

## Handoffs principais

### Atendimento -> Comercial

Usar quando:

- o lead já tem contexto mínimo
- existe oportunidade comercial real

### Comercial -> Financeiro / Pricing

Usar quando:

- houver necessidade de preço, cenário, parcelamento ou validação de margem

### Comercial -> Revisor

Usar quando:

- a proposta ou orçamento estiver pronta para checagem final

### Conteúdo -> Branding

Usar quando:

- a peça tiver impacto institucional ou precisar de reforço de identidade

### Growth -> Site / UX / Conversão

Usar quando:

- a hipótese de aquisição depender de página, CTA, formulário ou fluxo do site

### Comercial fechado -> Operações / Delivery

Usar quando:

- a proposta foi aprovada e o cliente precisa ser onboardado

## Escalada

Escalar para humano quando:

- houver conflito entre agentes
- o handoff chegar sem contexto suficiente
- a decisão envolver preço, jurídico, publicação ou reputação
