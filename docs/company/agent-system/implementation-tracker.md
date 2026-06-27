# Tracker de Implementação

## Como usar

Este tracker existe para manter rastreabilidade e retomada segura.

- `nao iniciado`: ainda não começou
- `em andamento`: material em elaboração
- `concluido`: pacote entregue e integrado
- `bloqueado`: depende de algo externo ou de decisão

## Estado atual

- Data de referência: `2026-04-20`
- Implantação aprovada: `sim`
- Escopo ativo: `fase 1 e fase 2`
- Frente crítica adicional: `hardening de marketing, growth e tráfego`

## Pacotes de trabalho

### 1. Governança central

- Status: `concluido`
- Entregáveis:
  - `agent-directory.md`
  - `operating-model.md`
  - `workflow-map.md`
  - `approval-matrix.md`
  - `memory-protocol.md`
  - `handoff-rules.md`
  - `implementation-plan.md`
  - `implementation-tracker.md`
- Ponto de retomada se falhar: revisar primeiro `agent-directory.md` e depois `operating-model.md`

### 2. Fase 1

- Status: `concluido`
- Entregáveis esperados:
  - prompts de Orquestrador, Atendimento, Comercial, Conteúdo, Growth e Revisor
  - playbooks da fase 1
- Dependências: governança central concluída
- Ponto de retomada se falhar: verificar `prompts/` e `playbooks/phase-1/`

### 3. Fase 2

- Status: `concluido`
- Entregáveis esperados:
  - prompts de Branding, Site/UX, Operações e Pricing
  - playbooks da fase 2
- Dependências: governança central concluída
- Ponto de retomada se falhar: verificar `prompts/` e `playbooks/phase-2/`

### 4. Estrutura operacional

- Status: `concluido`
- Entregáveis esperados:
  - expansão de `operations/ai-os`
  - templates por pasta operacional
- Dependências: modelo operacional definido
- Ponto de retomada se falhar: verificar `operations/ai-os/README.md`

### 5. Consolidação final

- Status: `concluido`
- Entregáveis esperados:
  - revisão crítica do conjunto
  - atualização dos READMEs
  - registro final na memória persistente
- Dependências: pacotes 2, 3 e 4 concluídos
- Ponto de retomada se falhar: conferir checklist final desta página

### 6. Hardening de marketing, growth e tráfego

- Status: `em andamento`
- Entregáveis esperados:
  - `marketing-agent-engineering-research.md`
  - `marketing-agent-hardening-plan.md`
  - revisão dos prompts e playbooks de marketing
  - definição de um workflow operacional com DoD e gate de publicação
  - plano de uso de Canva, memória e evals
  - asset limpo da marca para hero visual
  - templates-base de Instagram
  - checklist visual rígido integrado aos agentes
- Dependências: pacotes 1, 2 e 3 concluídos
- Ponto de retomada se falhar:
  - ler primeiro `marketing-agent-engineering-research.md`
  - depois `marketing-agent-hardening-plan.md`
  - então revisar `docs/company/reviews/instagram-launch-flow-audit-and-dod.md`
  - então revisar `docs/company/presence/canva-brand-setup.md`
  - e `docs/company/agent-system/review-checklists/instagram-visual-qa.md`

#### Estado detalhado da frente de hardening em `2026-04-20`

- `concluido`: monograma limpo exportado para `logos/rito_monogram_r_clean.svg` e `logos/rito_monogram_r_clean_2048.png`
- `concluido`: assets da marca enviados para a biblioteca do Canva
- `concluido`: templates locais de Instagram gerados em `deliverables/social-assets/templates/`
- `concluido`: templates de Instagram enviados também como assets na biblioteca do Canva
- `concluido`: checklist visual rígido criado em `review-checklists/instagram-visual-qa.md`
- `em andamento`: prompts e playbooks atualizados para usar o checklist como gate operacional
- `parcial`: conector do Canva voltou a responder após falha de transporte `missing-content-type; body:`
- `parcial`: leitura de brand kits funciona, mas o resultado atual é `0` brand kits configurados
- `bloqueado`: `image-to-design` sujeito ao limite mensal de AI do plano Canva
- `bloqueado`: `import-design-from-url` ainda rejeitando PNG flat com `invalid_file`
- `pendente`: refazer e aprovar os 3 posts finais em cima dos templates novos e do asset limpo

## Checklist de consolidação final

- prompts revisados
- playbooks revisados
- templates operacionais criados
- READMEs atualizados
- memória do projeto atualizada
- riscos residuais anotados
- frente de hardening de marketing registrada
