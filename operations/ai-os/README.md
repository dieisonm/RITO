# AI OS

Esta area organiza a operacao da RITO com apoio dos agentes nativos do Codex.

## Objetivo

Centralizar entrada, triagem, producao, revisao e historico operacional para que a equipe de agentes trabalhe com continuidade, memoria e rastreabilidade.

## Fluxo Operacional

1. Tudo entra por `inbox/` como demanda bruta.
2. O orquestrador classifica e encaminha para `leads/`, `content/`, `growth/`, `support/` ou `proposals/`.
3. O agente dono da frente preenche o template correspondente.
4. O revisor registra observacoes em `reviews/`.
5. Materiais prontos seguem para `clients/`, `knowledge-base/` ou retorno ao fluxo comercial.

## Estrutura

- `inbox/`: capturas iniciais e entradas sem triagem
- `leads/`: dossies comerciais em qualificar ou negociar
- `proposals/`: propostas, orcamentos, follow-ups e versoes
- `clients/`: dossies de clientes ativos ou aprovados
- `content/`: briefings, pautas e pecas de conteudo
- `support/`: atendimento, respostas e logs de interacao
- `growth/`: campanhas, SEO, trafego pago, testes e prospecção ativa
- `reviews/`: revisoes criticas, riscos e pendencias
- `playbooks/`: rotinas e procedimentos dos agentes
- `templates/`: modelos oficiais para copiar e preencher
- `knowledge-base/`: ativos aprovados e fontes de verdade

## Quem Atua Onde

- `Orquestrador`: decide o destino da demanda e controla estado
- `Atendimento`: alimenta `support/` e organiza respostas
- `Comercial`: trabalha `leads/` e `proposals/`
- `Conteudo`: preenche `content/`
- `Growth`: preenche `growth/`
- `Prospecção e Inteligência Comercial`: alimenta a base outbound em `growth/` e encaminha dossiês aprovados para `leads/`
- `Revisor`: escreve em `reviews/`
- `Operacoes`: consolida em `clients/`

## Convencao de Nomes

Use nomes em minusculo, com data, canal ou cliente quando fizer sentido.

Exemplos:

- `2026-04-14-lead-metalurgica-rio.md`
- `2026-04-14-proposta-ponto-de-venda-v2.md`
- `2026-04-14-support-whatsapp-entrada.md`
- `2026-04-14-campaign-meta-abertura.md`
- `2026-04-14-review-homepage-v1.md`

## Regra de Memoria

Ao concluir uma entrega relevante, registrar:

- decisao tomada
- motivo
- estado final
- riscos remanescentes
- proximo passo

## Uso Recomendado

1. Criar ou localizar o item na pasta correta.
2. Preencher o template correspondente.
3. Consultar os playbooks canonicos em `docs/company/agent-system/playbooks/` quando houver duvida de fluxo.
4. Registrar a entrega em `reviews/` se houver revisao.
5. Atualizar `knowledge-base/` quando surgir algo reutilizavel.
