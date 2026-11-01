# Pesquisa: Engenharia de Agentes para Marketing, Growth e Tráfego

Data de referência: `2026-04-19`

## Objetivo

Consolidar o que a RITO aprendeu com os erros recentes de Instagram, comparar o sistema atual com boas práticas atuais de engenharia de agentes e indicar quais ferramentas, skills, plugins e MCPs devem sustentar a operação de marketing daqui para frente.

## Contexto da RITO

O problema atual não é apenas de direção de arte. Os erros repetidos no Instagram mostraram que os agentes de marketing ainda estão bons demais para `documentar intenção` e fracos demais para `entregar peça pronta`.

Os sintomas mais claros no projeto hoje são:

- prompts amplos demais e com sobreposição de responsabilidade;
- revisão subjetiva, sem gate intermediário;
- ausência de uma etapa de produção visual apoiada por ferramenta;
- falta de critérios objetivos para dizer que uma peça está pronta;
- agent de growth genérico demais para SEO, Meta Ads, Google Ads e CRO.

## Base local auditada

- `docs/agents/agent-system/prompts/content-agent.md`
- `docs/agents/agent-system/prompts/growth-aquisicao-agent.md`
- `docs/agents/agent-system/prompts/branding-agent.md`
- `docs/agents/agent-system/prompts/revisor-agent.md`
- `docs/agents/agent-system/playbooks/phase-1/conteudo-organico.md`
- `docs/agents/agent-system/playbooks/phase-1/growth-aquisicao.md`
- `docs/agents/agent-system/playbooks/phase-1/revisor.md`
- `docs/agents/agent-system/operating-model.md`
- `docs/brand/presence/instagram-launch-strategy.md`
- `ops/instagram/README.md`
- `ops/instagram/posts/README.md`
- `docs/reviews/instagram-launch-flow-audit-and-dod.md`

## Achados principais na RITO

### 1. O sistema atual mistura estratégia, criação e revisão

Hoje `Conteúdo`, `Branding` e `Revisor` encostam no mesmo problema visual, mas nenhum é o dono final do critério de aceite da peça. Isso cria revisão em série, subjetiva e conflitante.

### 2. O sistema aceita “direção visual” como se fosse “post pronto”

Os documentos já apontam boas intenções, como `image-first`, pouco texto e rejeição a peças com cara de slide. O problema é que ainda faltam critérios operacionais duros, como:

- formato obrigatório;
- teste de grid;
- regra de unicidade visual entre os 3 posts;
- regra de export;
- prova de validação no app;
- pacote final pronto para publicação.

### 3. O agente de growth está amplo demais

Hoje o agente de growth reúne:

- SEO;
- tráfego pago;
- canais;
- landing pages;
- CRO;
- priorização;
- hipóteses.

Isso é amplo demais para um único modo operacional. O resultado tende a ser plano genérico em vez de briefing executável por canal.

### 4. A revisão está entrando tarde

O fluxo atual tende a revisar só depois da peça praticamente pronta. Na prática, isso significa descobrir erro caro no fim do processo.

## O que as fontes primárias dizem

### Anthropic: começar simples e compor padrões

No artigo oficial [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), a Anthropic defende começar com padrões simples e composáveis, não com arquitetura excessivamente complexa. A implicação para a RITO é direta: antes de criar mais “agentes criativos”, precisamos de um workflow enxuto, com passos claros e separação de responsabilidade.

### OpenAI: desenvolvimento guiado por avaliação

Na documentação oficial [Agent evals](https://platform.openai.com/docs/guides/agent-evals), a OpenAI recomenda desenvolvimento guiado por avaliação e uma suíte de tarefas representativas. Para a RITO, isso significa parar de julgar agentes de marketing só por sensação e passar a medir:

- se o entregável sai no formato certo;
- se a peça respeita o canal;
- se a copy cabe na arte;
- se o grid inicial não repete cena;
- se o pacote final realmente está pronto para publicação.

### Model Context Protocol: interfaces mais limpas entre agentes e ferramentas

A introdução oficial do [Model Context Protocol](https://modelcontextprotocol.io/introduction) reforça a separação entre `tools`, `resources` e `prompts`. Para a RITO, a leitura prática é esta:

- prompts dos agentes devem definir responsabilidade;
- ferramentas devem executar produção e edição;
- memória e ativos devem ser tratados como recursos claros;
- o agente não deve “simular” uma ferramenta quando existe um MCP melhor para aquilo.

### Meta / Instagram: operar por superfície real, não por canal genérico

As superfícies oficiais do ecossistema Meta usadas hoje pela RITO são [Instagram for Business](https://business.instagram.com/?locale=pt_BR) e as superfícies de impulsionamento e conta comercial já documentadas em `docs/brand/presence/instagram-launch-strategy.md`. A implicação prática é que “Instagram” não é um único formato. O agente precisa pensar por superfície:

- feed;
- stories;
- reels;
- direct;
- impulsionamento posterior.

### Google Ads: boas práticas são específicas por formato e objetivo

As páginas oficiais de ajuda do Google Ads para boas práticas de criativo e formatos reforçam a mesma lógica: a operação precisa ser específica por formato, objetivo e ativo. Para a RITO, isso enfraquece ainda mais a ideia de um único agente genérico de “growth” sem modos bem definidos.

## Conclusão da pesquisa externa

O padrão que aparece nas fontes é consistente:

- agentes bons não são “mais criativos por padrão”;
- agentes bons operam com escopo claro;
- workflow simples vence arquitetura confusa;
- ferramenta certa reduz improviso;
- avaliação objetiva reduz retrabalho.

## Ferramentas e capacidades já disponíveis neste ambiente

### 1. Canva plugin

O plugin Canva já expõe ferramentas úteis para a operação de marketing:

- gerar design (`generate-design`);
- criar post de Instagram;
- editar design existente;
- transformar imagem em design editável;
- usar brand kits quando existirem.

Diagnóstico atual: o conector está acessível, mas a listagem de brand kits retornou vazia. Ou seja, a RITO ainda não tem um `brand kit` configurado no Canva para produção on-brand consistente.

### 2. Skill `canva-resize-for-all-social-media`

Essa skill é útil para adaptar uma peça para múltiplos formatos depois da aprovação da arte-mãe. Para a RITO, isso é especialmente útil quando a base do post já estiver aprovada e quisermos derivar versões para stories, Facebook e LinkedIn.

### 3. `project-memory`

A memória persistente já está disponível e deve virar parte obrigatória do marketing para guardar:

- direções aprovadas;
- direções rejeitadas;
- formatos que performam melhor;
- dores recorrentes do público;
- objeções comerciais;
- aprendizados por canal.

### 4. Skills `aeval-set-up` e `aeval-run-eval`

Essas skills são a melhor oportunidade local para profissionalizar a engenharia dos agentes. Elas permitem criar uma suíte de avaliação para:

- briefs de conteúdo;
- saídas de growth;
- revisão visual;
- checklists de peça pronta.

### 5. `tool_search`

Já existe capacidade para descobrir MCPs e ferramentas adicionais disponíveis na sessão. Isso ajuda a expandir a stack sem improvisar.

### 6. Google Drive plugin

É útil para:

- aprovações em docs;
- planilhas de pauta e mídia;
- roteiros;
- decks e materiais comerciais.

Não resolve produção visual sozinho, mas organiza bem a operação ao redor dela.

## O que falta hoje

### Faltas internas

- um agente ou modo específico de `creative production`;
- critérios objetivos de aceite por superfície;
- avaliação automática dos agentes de marketing;
- brand kit operacional em ferramenta de design;
- modos separados dentro de growth;
- gate intermediário antes da peça final.

### Faltas de tooling

- conector de analytics e mídia para Meta Ads;
- conector de Google Ads;
- conector de GA4 e Search Console;
- eventualmente um fluxo mais rico de asset management.

Essas ausências não impedem o trabalho de hoje, mas limitam a maturidade da operação de growth.

## Decisão recomendada para a RITO

### 1. Não deixar mais o marketing operar só “no prompt”

O stack deve ser:

- `prompt` para responsabilidade e decisão;
- `tool` para produção;
- `memory` para aprendizado;
- `eval` para qualidade.

### 2. Criar um pipeline específico para Instagram

Fluxo recomendado:

1. objetivo e papel do post;
2. brief criativo curto;
3. produção visual em ferramenta;
4. revisão objetiva;
5. pacote pronto para publicação.

### 3. Reestruturar o bloco de growth por modo operacional

Mesmo que continue sendo um agente só no diretório, ele deve operar com modos obrigatórios:

- `SEO e descoberta`;
- `Meta Ads`;
- `Google Ads`;
- `CRO e landing pages`;
- `mensuração e priorização`.

### 4. Adicionar um agente ou modo explícito de produção visual

Sem isso, o conteúdo continua tentando cobrir:

- estratégia;
- copy;
- visual;
- adequação de canal.

Esse acúmulo está no centro do retrabalho.

## O que isso significa para os 3 posts de hoje

Para hoje, a recomendação não é criar mais variações cegas. É endurecer o workflow:

1. congelar o papel de cada post;
2. gerar ou editar peça em ferramenta visual adequada;
3. validar em `4:5` e no grid quadrado;
4. revisar o trio como conjunto;
5. publicar só quando o pacote estiver fechado.

## Resumo executivo

Se quisermos reduzir retrabalho rápido, a prioridade não é “mais agentes”. A prioridade é:

1. separar `strategy`, `creative production` e `review`;
2. usar ferramenta visual de verdade para produção;
3. criar um DoD objetivo por canal;
4. transformar os agentes de marketing em um sistema avaliado, não apenas opinativo.

## Próximo documento

Este diagnóstico é complementado por:

- `marketing-agent-hardening-plan.md`

Esse segundo documento traduz a pesquisa em mudanças concretas para os agentes da RITO.
