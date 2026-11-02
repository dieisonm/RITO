# Agentes da RITO

Arquitetura enxuta aprovada em 2026-11-01: **5 agentes**, um por passo do funil de venda e entrega. Detalhes e motivo no vault: `60 Projetos/Projetos de código/RITO/Documentos/2026-11-01 Inventário e arquitetura dos agentes.md`. A equipe antiga (16 agentes, abril e maio de 2026) está em `_arquivo/2026-11-agentes/`.

| # | Agente | Faz | Skill do Claude Code |
| --- | --- | --- | --- |
| 1 | **Prospecção** | encontra empresas em fontes públicas, sem Instagram, e grava na base única (`empresas-novas.csv`) | `rito-prospeccao` |
| 2 | **Contato** | escreve, revisa e envia mensagens em lotes pequenos, depois da aprovação; e-mail por `scripts/enviar_email.py`, WhatsApp manual por link `wa.me` | `rito-contato` |
| 3 | **Contatos do dia** | lê as caixas de e-mail, separa humano de automático, sugere respostas e registra na base | `rito-contatos-do-dia` |
| 4 | **Comercial** | transforma conversa em oferta: ficha, briefing, valor final, proposta, contrato, follow-up | `rito-comercial` |
| 5 | **Entrega** | acompanha a execução de cada oferta até a entrega, cobrança do saldo e manutenção | `rito-entrega` |

As skills ficam em `Automations/.claude/skills/` (onde as sessões rodam) e rodam só quando o Dieison pedir. Os prompts em `prompts/` ficam como referência dos critérios originais. Relatório do site: skill `rito-relatorio-google`.

## Regras que valem para todos

1. **Nada sai sem aprovação.** Mensagem, proposta ou publicação só é enviada depois que o Dieison aprova o texto final exato, mostrado como será enviado. Vale também quando a rotina for automática.
2. **Português revisado.** Todo texto externo tem acentos e revisão de português antes da amostra de aprovação (lição do incidente de 2026-05-19).
3. **Uma fonte de dados.** Empresas, contatos e resultados ficam em `ops/ai-os/growth/prospecting/base-prospeccao-rito.xlsx` (fora do Git).
4. **Só canais oficiais.** Nenhuma automação na interface do Instagram ou do Facebook; WhatsApp conforme o redesenho da infraestrutura (app WhatsApp Business ou API oficial).
5. **Não contatar** quem pediu para sair ou está marcado em `do_not_contact` / `opt_out_received`.

## Próximo passo

Pendente: redesenho da infraestrutura de WhatsApp (app WhatsApp Business ou API oficial). Métricas e Conteúdo entram na fase 9.
