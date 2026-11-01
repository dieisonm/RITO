# Agentes da RITO

Arquitetura enxuta aprovada em 2026-11-01: **5 agentes**, um por passo do funil de venda e entrega. Detalhes e motivo no vault: `60 Projetos/Projetos de código/RITO/Documentos/2026-11-01 Inventário e arquitetura dos agentes.md`. A equipe antiga (16 agentes, abril e maio de 2026) está em `_arquivo/2026-11-agentes/`.

| # | Agente | Faz | Base atual (até virar skill) |
| --- | --- | --- | --- |
| 1 | **Prospecção** | encontra empresas em fontes públicas, sem Instagram, e grava na base única | `prompts/prospeccao-inteligencia-comercial-agent.md` |
| 2 | **Contato** | escreve, revisa e envia mensagens em lotes pequenos, depois da aprovação | `prompts/disparo-outbound-agent.md` + `prompts/revisor-agent.md` + `review-checklists/prospecting-outbound-qa.md` |
| 3 | **Triagem diária** | lê e-mails, formulário e WhatsApp, separa humano de automático, sugere respostas | `prompts/atendimento-relacionamento-agent.md` |
| 4 | **Comercial** | transforma conversa em oferta: ficha, briefing, valor final, contrato | `prompts/commercial-agent.md` + `docs/sales/ofertas/` |
| 5 | **Entrega** | acompanha a execução de cada oferta até a entrega e oferece manutenção | `prompts/operacoes-delivery-agent.md` |

## Regras que valem para todos

1. **Nada sai sem aprovação.** Mensagem, proposta ou publicação só é enviada depois que o Dieison aprova o texto final exato, mostrado como será enviado. Vale também quando a rotina for automática.
2. **Português revisado.** Todo texto externo tem acentos e revisão de português antes da amostra de aprovação (lição do incidente de 2026-05-19).
3. **Uma fonte de dados.** Empresas, contatos e resultados ficam em `ops/ai-os/growth/prospecting/base-prospeccao-rito.xlsx` (fora do Git).
4. **Só canais oficiais.** Nenhuma automação na interface do Instagram ou do Facebook; WhatsApp conforme o redesenho da infraestrutura (app WhatsApp Business ou API oficial).
5. **Não contatar** quem pediu para sair ou está marcado em `do_not_contact` / `opt_out_received`.

## Próximo passo

Cada agente vira uma skill do Claude Code em `RITO/.claude/skills/<agente>/SKILL.md`, reaproveitando os critérios dos prompts acima. Métricas e Conteúdo entram na fase 9.
