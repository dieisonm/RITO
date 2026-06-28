# Sistema de Agentes

Esta pasta define como a RITO opera com agentes no Codex nativo.

## O que existe aqui

- `agent-directory.md`: quem são os agentes e onde cada um atua.
- `operating-model.md`: princípios da operação e regras do sistema.
- `workflow-map.md`: fluxos principais da empresa com handoffs.
- `implementation-plan.md`: plano mestre de implantação.
- `implementation-tracker.md`: estado atual, checkpoints e ponto de retomada.
- `marketing-agent-engineering-research.md`: diagnóstico e pesquisa sobre hardening dos agentes de marketing.
- `marketing-agent-hardening-plan.md`: plano de correção para marketing, growth e tráfego.
- `gpt-5.5-prompt-improvement-guide.md`: padrão de prompts para GPT-5.5, com critérios de sucesso, busca, validação e parada.
- `gpt-image-2-visual-prompting-guide.md`: padrão de prompts visuais para campanhas, posts, stories e criativos gerados com GPT Image 2.
- `../frontend-ui-development-guide.md`: boas práticas para ajuste granular de UI, construção responsiva e validação visual.
- `review-checklists/instagram-visual-qa.md`: gate visual obrigatório para posts e criativos de Instagram.
- `approval-matrix.md`: o que exige validação humana.
- `memory-protocol.md`: quando ler, buscar, criar e atualizar memória.
- `handoff-rules.md`: regras de passagem entre agentes.
- `base-prompt.md`: prompt-base compartilhado.
- `prompts/`: prompts específicos por agente.
- `playbooks/`: guias operacionais por fase.
- `templates/`: moldes para briefing, handoff e captura de memória.

## Ordem recomendada de leitura

1. `implementation-plan.md`
2. `agent-directory.md`
3. `operating-model.md`
4. `marketing-agent-engineering-research.md`
5. `marketing-agent-hardening-plan.md`
6. `gpt-5.5-prompt-improvement-guide.md`
7. `gpt-image-2-visual-prompting-guide.md`
8. `../frontend-ui-development-guide.md`
9. `review-checklists/instagram-visual-qa.md`
10. `approval-matrix.md`
11. `memory-protocol.md`
12. `handoff-rules.md`
13. `prompts/` e `playbooks/`

## Como usar no dia a dia

1. O orquestrador lê a demanda.
2. Consulta a memória e localiza o contexto operacional.
3. Aciona o menor conjunto de agentes necessário.
4. Usa os playbooks e templates para padronizar saída.
5. Passa pelo revisor quando o material for externo ou sensível.
6. Atualiza memória e pasta operacional ao final.
