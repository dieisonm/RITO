# Plano de Implementação do Sistema de Agentes

## Objetivo

Implantar a operação nativa de agentes da RITO no Codex com governança clara, memória persistente, estrutura operacional e playbooks suficientes para executar a fase 1 e a fase 2 sem depender de improviso.

## Escopo aprovado

### Fase 1

- Orquestrador
- Atendimento e Relacionamento
- Comercial
- Conteúdo Orgânico
- Growth / Aquisição
- Revisor

### Fase 2

- Branding
- Site / UX / Conversão
- Operações / Delivery
- Financeiro / Pricing

## O que esta implementação inclui

- arquitetura oficial de agentes
- governança central do sistema
- protocolo de memória
- regras de handoff
- matriz de aprovação humana
- prompts por agente
- playbooks por agente
- templates mínimos de operação
- estrutura operacional em `operations/ai-os`
- tracker para retomada em caso de falha

## O que não entra nesta etapa

- integrações externas com WhatsApp, Instagram, LinkedIn ou CRM
- automações recorrentes ativadas
- runtime externo com CrewAI, LiteLLM, LangGraph ou similares
- publicação automática sem checkpoints humanos

## Estratégia de implantação

### Frente 1. Governança central

Entregáveis:

- diretório oficial de agentes
- modelo operacional revisado
- mapa de fluxos revisado
- matriz de aprovação
- protocolo de memória
- regras de handoff
- tracker de implantação

### Frente 2. Fase 1

Entregáveis:

- prompts
- playbooks
- templates operacionais ligados à entrada, venda, conteúdo, growth e revisão

### Frente 3. Fase 2

Entregáveis:

- prompts
- playbooks
- integração com operações, pricing, site e branding

### Frente 4. Operação

Entregáveis:

- expansão de `operations/ai-os`
- convenções de nome
- templates prontos para copiar e preencher

## Dependências

- marca e posicionamento já consolidados em `docs/brand/foundation.md`
- pricing oficial já documentado em `docs/sales/commercial/`
- memória persistente operacional para o projeto `RITO`

## Critérios de aceite

- cada agente tem dono, limites, entradas, saídas e handoffs claros
- fase 1 e fase 2 estão documentadas com playbooks próprios
- existe um plano claro de retomada se a implantação parar no meio
- a estrutura operacional aponta onde cada material deve nascer e terminar
- o sistema respeita as travas humanas em site, preço, jurídico e publicação

## Estratégia de retomada se algo falhar

Se a implantação parar ou ficar incompleta:

1. abrir `implementation-tracker.md`
2. localizar o último pacote marcado como concluído
3. verificar os arquivos associados ao pacote
4. retomar pelo primeiro pacote com status `pendente` ou `em andamento`
5. registrar memória se a interrupção gerar decisão ou ajuste estrutural

## Próxima evolução após aprovação da implantação

- ativar automações recorrentes do Codex
- medir cadência real de uso por agente
- decidir se algum agente da fase 1 deve ser desdobrado
- incorporar o agente crítico adicional que o usuário mencionou
