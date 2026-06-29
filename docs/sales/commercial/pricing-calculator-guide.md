# Guia da Calculadora de Precificação

## Objetivo

Padronizar o uso da planilha oficial de precificação da RITO Sistemas para transformar horas estimadas em proposta de valor com lógica comercial consistente.

## Arquivo oficial

- Planilha final: `assets/business-kit/editable-xlsx/rito-pricing-calculator.xlsx`
- Gerador: `scripts/generate_pricing_calculator_xlsx.py`

## Estrutura da planilha

### 1. Aba `Calculadora`

É a aba principal.

Nela, a equipe deve:

- informar cliente e projeto;
- escolher tipo de serviço;
- escolher pacote comercial;
- definir complexidade, urgência, integrações e documentação extra;
- preencher as horas por etapa;
- revisar o preço mínimo, ideal e premium calculados automaticamente.

### 2. Aba `Cenarios`

Compara três leituras de preço para o mesmo projeto:

- `Mínimo defensável`
- `Ideal comercial`
- `Premium estratégico`

Também mostra a diferença entre os pacotes:

- `Essencial`
- `Operacional`
- `Sob Medida`

### 3. Aba `Parcelamento`

Simula a proposta parcelada por marcos com base no cenário escolhido.

Traz três modelos padrão:

- `2 marcos`
- `3 marcos`
- `4 marcos`

### 4. Aba `Resumo-Proposta`

É a aba preparada para consolidar a estimativa em um orçamento-resumo exportável.

Ela:

- reflete automaticamente cliente, projeto, pacote, cenário e investimento;
- traz campos rápidos para prazo, validade, resumo da demanda e solução sugerida;
- organiza a composição do investimento em um formato limpo;
- pode ser exportada em PDF diretamente pelo Excel.

### 5. Aba `Historico`

É a aba de acompanhamento depois do fechamento.

Ela compara:

- horas estimadas;
- horas vendidas;
- horas reais;
- valor vendido por etapa;
- custo real por etapa;
- saldo operacional por etapa.

### 6. Aba `Parametros`

Guarda as regras internas da calculadora:

- valores/hora por etapa;
- multiplicadores;
- faixas de serviço;
- pacotes;
- cenários;
- modelos de parcelamento.

## Regra de uso

- No uso diário, editar principalmente as células amarelas.
- A aba `Parametros` só deve ser alterada quando a regra comercial da RITO mudar de forma deliberada.
- O preço `Ideal comercial` deve ser a referência principal da proposta, salvo decisão consciente.
- O preço `Mínimo defensável` não deve virar padrão de venda.
- O cenário `Premium estratégico` faz sentido quando há alto valor percebido, risco, urgência ou personalização relevante.
- A aba `Resumo-Proposta` deve ser usada como base para exportação de um orçamento-resumo em PDF.
- A aba `Historico` deve ser preenchida após o fechamento e durante a execução.

## Lógica comercial adotada

### Horas por etapa

A planilha calcula a base a partir das etapas previstas no guia comercial:

1. análise e descoberta;
2. planejamento da solução;
3. desenvolvimento;
4. testes e ajustes;
5. entrega e orientação;
6. suporte inicial;
7. treinamento adicional.

### Pacotes

Os pacotes funcionam como leitura comercial da proposta:

- `Essencial`: proposta mais enxuta, com menor gordura comercial;
- `Operacional`: leitura padrão da RITO;
- `Sob Medida`: protege melhor projetos mais críticos, personalizados ou complexos.

### Cenários

Os cenários ajudam a evitar improviso:

- `Mínimo defensável`: limite abaixo do qual a proposta começa a enfraquecer;
- `Ideal comercial`: preço-base recomendado;
- `Premium estratégico`: leitura superior quando o contexto justifica.

## Fluxo recomendado

1. Fazer briefing e entendimento da necessidade.
2. Estimar horas por etapa na aba `Calculadora`.
3. Escolher o pacote comercial coerente com a proposta.
4. Revisar os três cenários.
5. Checar a aba `Parcelamento`.
6. Consolidar o envio na aba `Resumo-Proposta`.
7. Exportar o resumo, quando necessário.
8. Depois do fechamento, acompanhar o projeto na aba `Historico`.

## Quando revisar o preço

Reavaliar antes de enviar a proposta quando:

- o preço ideal ficar muito fora da faixa de referência do tipo de serviço;
- o escopo estiver vago;
- houver integração ou risco mal mapeado;
- o cliente pedir desconto antes de entender o valor da solução;
- a equipe perceber que o pacote comercial não corresponde ao nível de personalização da demanda.

## Boas práticas

- Preferir ajustar escopo antes de conceder desconto.
- Não usar a planilha como substituto do julgamento comercial.
- Sempre validar se o total faz sentido para o porte da entrega e para o risco assumido.
- Registrar no orçamento qual cenário foi adotado.
- Atualizar as `Horas vendidas` e `Horas reais` no histórico para gerar aprendizado comercial.
- Revisar projetos com saldo negativo por etapa para recalibrar futuras propostas.

## Observação final

A calculadora existe para reduzir improviso e aumentar consistência. Ela não substitui validação humana, mas cria uma base sólida para a RITO precificar com mais segurança.
