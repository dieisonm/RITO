# Plano de Hardening dos Agentes de Marketing, Growth e Tráfego

Data de referência: `2026-04-19`

## Objetivo

Corrigir os agentes de marketing da RITO para reduzir retrabalho, aumentar especialização e permitir que a operação produza conteúdo publicável e campanhas mais sólidas no menor tempo possível.

## Norte da intervenção

O objetivo não é inflar a arquitetura com mais agentes abstratos. O objetivo é fazer a equipe operar melhor com:

- fronteiras claras;
- ferramenta certa;
- critérios de aceite objetivos;
- memória persistente;
- avaliação.

## Decisões-base

### 1. Conteúdo não será mais o dono da peça final sozinho

O agente de conteúdo passa a ser dono de:

- tema;
- ângulo;
- objetivo;
- copy da legenda;
- CTA;
- brief da peça.

Ele deixa de ser o árbitro final da arte.

### 2. Branding deixa de ser “gosto” e vira sistema

O agente de branding deve ser dono de:

- sistema de marca;
- regras de uso;
- tokens visuais;
- consistência visual;
- aprovação de aderência à identidade.

Ele não deve funcionar como revisor subjetivo tardio da peça.

### 3. Revisor vira gate objetivo

O revisor deve operar com checklist e evidência, não com opinião vaga. Ele precisa validar:

- formato;
- recorte;
- grid;
- nitidez;
- unicidade visual;
- pacote completo.

### 4. Growth deve operar por modo

O agente de growth continuará existindo, mas com modos obrigatórios:

- `seo`
- `meta_ads`
- `google_ads`
- `cro`
- `measurement`

Qualquer entrega de growth deve declarar explicitamente o modo.

### 5. Produção visual vira etapa própria

A RITO precisa de um papel explícito de `creative production` ou `social design ops`, mesmo que inicialmente isso seja uma especialização nova dentro da fase de marketing.

## Arquitetura recomendada

### Bloco 1. Estratégia e conteúdo

#### Agente: Conteúdo Orgânico

Responsável por:

- tema do post;
- papel do post na sequência;
- legenda;
- CTA;
- comentário fixado;
- hashtags enxutas;
- brief da peça.

Não responsável por:

- declarar arte final pronta sem export e validação;
- resolver sozinho a produção visual;
- arbitrar tecnicamente formato e preview.

### Bloco 2. Produção visual

#### Novo papel recomendado: Creative Production / Social Design Ops

Responsável por:

- transformar o brief em peça real;
- operar Canva ou fluxo equivalente;
- garantir formato `4:5`;
- revisar safe area para grid quadrado;
- exportar versão final;
- manter padrão visual entre peças do mesmo conjunto.

Não responsável por:

- definir estratégia de growth;
- decidir narrativa do post;
- publicar sem revisão.

### Bloco 3. Marca

#### Agente: Branding

Responsável por:

- paleta;
- tipografia;
- composição;
- uso do monograma;
- consistência institucional;
- recusa de peças fora do universo visual da RITO.

Não responsável por:

- redesenhar toda peça no fim do fluxo;
- substituir o agente de produção visual.

### Bloco 4. Growth e tráfego

#### Agente: Growth / Aquisição

Modos obrigatórios:

- `seo`: descoberta orgânica, temas, palavras-chave, estrutura editorial;
- `meta_ads`: criativos, públicos, hipóteses, CTA, páginas de destino;
- `google_ads`: intenção de busca, palavras-chave, estrutura de campanha;
- `cro`: ajustes de página e conversão;
- `measurement`: métricas, hipóteses, leitura de resultados.

Saída mínima por modo:

- hipótese;
- ativo necessário;
- risco;
- métrica principal;
- próxima ação.

### Bloco 5. Revisão

#### Agente: Revisor

Responsável por:

- bloquear peça incompleta;
- validar Definition of Done;
- registrar motivo de reprovação;
- apontar correções mínimas;
- aprovar o pacote final.

Não responsável por:

- reinventar o brief;
- virar diretor de arte principal;
- discutir estratégia inteira quando o problema é só de execução.

## Ferramentas que devem entrar no fluxo

### Obrigatórias já na próxima rodada

- `project-memory` para guardar decisões aprovadas e rejeitadas;
- Canva plugin como base de produção visual e iteração;
- `docs/company/reviews/instagram-launch-flow-audit-and-dod.md` como checklist de aceite;
- `tool_search` para descobrir capacidades adicionais;
- Google Drive para aprovações e organização operacional, quando útil.

### Obrigatórias na profissionalização da engenharia

- `aeval-set-up`
- `aeval-run-eval`

Essas skills devem ser usadas para criar um conjunto de casos de teste dos agentes de marketing.

## O que fazer com os agentes atuais

### Conteúdo

Mudanças recomendadas:

- tornar obrigatório declarar `superfície` e `formato`;
- endurecer a saída esperada para brief, copy e pacote editorial;
- remover qualquer ambiguidade que permita chamar “direção criativa” de “post final”.

### Branding

Mudanças recomendadas:

- trocar linguagem subjetiva por checklist;
- declarar o que reprova uma peça;
- diferenciar claramente sistema de marca de execução visual.

### Growth

Mudanças recomendadas:

- exigir `modo`;
- exigir entregável por canal;
- impedir respostas genéricas;
- separar SEO, mídia paga e CRO na própria estrutura do prompt.

### Revisor

Mudanças recomendadas:

- usar checklist objetivo;
- exigir evidência de export e preview;
- validar conjunto dos 3 posts, não só peça isolada;
- bloquear publicação sem pacote completo.

## Workflow recomendado para os 3 posts de hoje

### Etapa 1. Definir o trio como conjunto

O trio precisa cumprir papéis diferentes:

- `Post 1`: institucional pinável;
- `Post 2`: dor real;
- `Post 3`: exemplo prático.

### Etapa 2. Produzir com brief curto

Cada post deve ter:

- papel;
- imagem-base;
- headline;
- linha de apoio opcional;
- CTA da legenda.

### Etapa 3. Produção visual real

Critérios:

- `1080 x 1350`
- leitura em `4:5`
- segurança no recorte quadrado do grid
- export final congelado

### Etapa 4. Revisão do conjunto

Checar:

- não repetir cena principal;
- não usar rosto humano na largada;
- evitar cara de slide;
- preservar força institucional do primeiro post;
- garantir família visual.

### Etapa 5. Pacote pronto para publicação

Cada post só avança quando existir:

- arte final;
- legenda final;
- CTA final;
- comentário fixado;
- hashtags finais;
- status `ready-to-publish`.

## Avaliação dos agentes

### Suite mínima recomendada

#### Conteúdo

- 10 casos de criação de post estático;
- 10 casos de carrossel;
- 10 casos de adaptação de tema por canal.

#### Growth

- 5 casos de SEO;
- 5 casos de Meta Ads;
- 5 casos de Google Ads;
- 5 casos de CRO.

#### Revisor

- 10 casos com peça aprovada;
- 10 casos com peça reprovada por erro básico;
- 10 casos de pacote incompleto.

### Critérios mínimos de aprovação

- formato correto;
- peça nativa do canal;
- copy adequada ao espaço visual;
- ausência de erro básico do conjunto;
- pacote final completo.

## Priorização

### Hoje

1. endurecer o workflow do Instagram;
2. parar de chamar peça exploratória de pronta;
3. produzir os 3 posts com gate real.

### Próximos 7 dias

1. revisar prompts de `Conteúdo`, `Branding`, `Growth` e `Revisor`;
2. criar o papel de `Creative Production`;
3. formalizar o DoD em todos os playbooks de social;
4. configurar brand kit no Canva.

### Próximos 30 dias

1. implementar a suite de evals com `aeval`;
2. organizar memória de marketing por canal e campanha;
3. refinar growth em modos separados;
4. avaliar necessidade de conectores adicionais para Meta Ads e Google Ads.

## Riscos residuais

- sem brand kit, a produção on-brand continua mais manual do que deveria;
- sem evals, os agentes ainda podem parecer melhores no texto do que na operação;
- sem conector de mídia e analytics, growth continuará mais estratégico do que operacional em alguns tópicos;
- sem o papel explícito de produção visual, o retrabalho tende a voltar.

## Critério de sucesso

Vamos considerar o hardening bem-sucedido quando:

- os 3 posts de lançamento saírem sem ciclo longo de retrabalho;
- o trio passar no teste de grid;
- o revisor bloquear erro básico antes da publicação;
- growth começar a produzir briefs acionáveis, não planos genéricos;
- os aprendizados forem capturados em memória e reaproveitados na rodada seguinte.

## Relação com outros documentos

- `marketing-agent-engineering-research.md`
- `docs/company/reviews/instagram-launch-flow-audit-and-dod.md`
- `docs/company/presence/instagram-launch-strategy.md`
- `operations/instagram/README.md`
