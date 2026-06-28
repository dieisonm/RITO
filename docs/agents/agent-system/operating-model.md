# Modelo Operacional de Agentes

## Objetivo

Operar a RITO com uma equipe-base de agentes especializados dentro do Codex nativo, usando memória persistente, prompts estáveis, pastas operacionais e revisão humana para manter continuidade entre sessões.

## O que é operação nativa

Na operação nativa:

- o orquestrador classifica e distribui o trabalho;
- o Codex aciona subagentes especialistas quando necessário;
- cada entrega deixa rastro em documentos operacionais e memória;
- o sistema continua entre sessões por causa da memória, das pastas e dos playbooks;
- nada sensível é publicado ou enviado sem validação humana.

## Estrutura da equipe

- Fase 1: Orquestrador, Atendimento e Relacionamento, Comercial, Conteúdo Orgânico, Growth / Aquisição e Revisor.
- Fase 2: Branding, Site / UX / Conversão, Operações / Delivery e Financeiro / Pricing.

## Papel do orquestrador

O orquestrador é responsável por:

- receber a demanda
- classificar o tipo de trabalho
- abrir ou localizar o contexto operacional correto
- escolher os agentes especializados
- ordenar os handoffs
- consolidar entregáveis
- registrar memória relevante
- manter a estrutura organizada

## Princípios do sistema

- Uma fonte de verdade por assunto.
- Um agente dono por frente principal.
- Atendimento, comercial, conteúdo e aquisição não se confundem.
- Toda entrega tem estado explícito.
- Toda mudança sensível tem trava humana.
- O foco da RITO continua sendo clareza, proximidade e problemas reais de pequenas empresas.

## Tipos de trabalho aceitos

- atendimento e qualificação de leads
- preparação de resposta inicial por canal
- briefing, proposta e orçamento
- follow-up comercial
- planejamento e produção de conteúdo orgânico
- SEO, mídia paga e estratégia de aquisição
- branding e presença institucional
- análise e recomendação de melhoria do site
- onboarding e operação de clientes
- apoio de pricing, parcelamento e margem

## Tipos de trabalho que exigem aprovação humana

- alteração no site publicado
- campanha paga com gasto real
- alteração de preços e condições comerciais
- envio definitivo de proposta
- envio definitivo de contrato
- desconto fora da política
- mudança de posicionamento de marca
- divulgação pública de case real
- qualquer material com implicação jurídica ou fiscal

## Fluxo operacional padrão

1. A demanda entra por um canal ou backlog.
2. O orquestrador registra a demanda em `operations/ai-os`.
3. O agente dono produz o primeiro rascunho.
4. Agentes de apoio refinam quando necessário.
5. O revisor valida coerência, risco e qualidade.
6. O orquestrador consolida a saída final.
7. A memória persistente é atualizada.
8. O artefato final é movido para a pasta operacional correta.

## Regras de qualidade

- Escrever em português do Brasil.
- Explicar primeiro o problema e depois a solução.
- Evitar linguagem de startup, hype ou exagero tecnológico.
- Manter o foco em acessibilidade, praticidade e custo-benefício.
- Não prometer o menor preço do mercado.
- Distinguir com clareza rascunho, revisão, versão aprovada e versão publicada.

## Estados de entrega

- `novo`: demanda ainda não triada
- `triado`: demanda classificada e encaminhada
- `em_execucao`: agente dono trabalhando
- `em_revisao`: aguardando parecer do revisor
- `aprovado`: pronto para uso externo ou interno
- `publicado`: já usado em canal público
- `enviado`: já enviado a cliente
- `arquivado`: ciclo concluído

## Handoffs recomendados

- `atendimento` -> `comercial` -> `financeiro/pricing` -> `revisor`
- `conteudo` -> `branding` -> `revisor`
- `growth` -> `site/ux` -> `branding` -> `revisor`
- `comercial fechado` -> `operacoes/delivery`
- `site/ux` -> `revisor` -> `aprovacao humana` -> `implementacao`

## Riscos operacionais a evitar

- criar materiais desconectados da marca
- duplicar ownership entre agentes
- publicar recomendação sem aprovação
- registrar memória demais e gerar ruído
- registrar memória de menos e perder continuidade
- misturar atendimento com negociação profunda
- misturar conteúdo orgânico com mídia paga
- usar modelo operacional como substituto de jurídico ou contabilidade
