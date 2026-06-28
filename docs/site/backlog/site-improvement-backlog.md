# Site Improvement Backlog

## Resumo executivo

O site da RITO Sistemas ja comunica a proposta, mas ainda precisa de uma camada mais forte de conversao, prova e hierarquia editorial.

Este backlog transforma as auditorias em tarefas praticas, priorizadas e com criterio de pronto. A ordem abaixo privilegia os pontos que mais afetam entendimento, confianca e geracao de contato.

## Legenda

- `P1`: impacto alto, deve vir primeiro
- `P2`: importante, entra logo depois dos itens criticos
- `P3`: desejavel, mas pode esperar a base estar consistente

## Backlog priorizado

| ID | Tarefa | Tipo | Prioridade | Dependencia | Dono sugerido | Criterio de pronto | Risco se nao fizer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SB-01 | Definir funcao unica de cada pagina e a hierarquia editorial do site | Arquitetura / IA | P1 | Auditorias de IA e site plans | `ux/conversao` | Cada pagina tem uma funcao primaria clara e nao repete o papel das demais | O site continua explicativo, mas sem jornada nitida de decisao |
| SB-02 | Reescrever a homepage com foco em resultado, problema e CTA principal | Copy / Conversao | P1 | SB-01 e `homepage-copy-recommendations.md` | `copy/site` | Hero, subtitulo, CTA e secoes principais deixam claro o que a RITO faz, para quem faz e por que agir agora | A home segue correta, mas pouco persuasiva |
| SB-03 | Criar a faixa de confianca da homepage e padronizar mensagens de orcamento gratis | UX / Copy | P1 | SB-02 | `ux/conversao` | A homepage reforca analise inicial gratuita, atendimento direto e escopo sob medida sem exagero visual | O visitante entende a oferta, mas ainda hesita em seguir para contato |
| SB-04 | Tornar a pagina de Solucoes mais concreta, com exemplos de uso e resultado pratico | Copy / Conteudo | P1 | SB-01 e `internal-pages-copy-recommendations.md` | `copy/site` | A pagina mostra problemas resolvidos, exemplos reais e ganho operacional claro | A proposta continua ampla demais e pouco visual |
| SB-05 | Reescrever a pagina Como Funciona para explicar o processo e o que acontece depois do contato | Copy / Comercial | P1 | SB-01, `contact-flow-audit.md` e `internal-pages-copy-recommendations.md` | `comercial` | O visitante entende o fluxo de atendimento, as etapas e o que a RITO espera receber | O lead nao sabe o que enviar nem o que acontece depois |
| SB-06 | Reescrever a pagina Para Quem E para qualificar melhor o publico | Copy / Conversao | P2 | SB-01 e `internal-pages-copy-recommendations.md` | `copy/site` | Fica claro para quem a RITO faz sentido, quem nao e o foco e em que contexto a oferta funciona melhor | A pagina atrai publico demais e reduz qualificacao |
| SB-07 | Reescrever a pagina Sobre para consolidar posicionamento e criterio de trabalho | Copy / Institucional | P2 | SB-01 e `internal-pages-copy-recommendations.md` | `copy/site` | A pagina explica a marca, o criterio de trabalho e o compromisso com praticidade | A marca fica conhecida, mas ainda pouco diferenciada |
| SB-08 | Fortalecer a pagina de Contato com promessa de retorno, texto de apoio e expectativa clara | Copy / Conversao | P1 | SB-05 e `contact-page-copy-strengthening.md` | `copy/site` | O contato mostra prazo ou expectativa de retorno, reduz friccao e deixa claro o proximo passo | O formulario recebe visitas, mas perde conversao por inseguranca |
| SB-09 | Criar o pacote de prova com exemplos de solucao, casos ficticios e antes/depois | Conteudo / Prova | P1 | SB-04 e `site-ux-conversion-audit.md` | `conteudo` | Existem materiais reutilizaveis que mostram resultado pratico sem prometer caso real nao validado | Falta evidencia concreta e o site continua institucional demais |
| SB-10 | Consolidar FAQ comercial e microcopy padrao para site, contato e follow-up | Comercial / Copy | P2 | SB-05 e SB-08 | `comercial` | Existe uma biblioteca curta de respostas e frases padrao coerentes com a marca | A equipe reescreve as mesmas respostas varias vezes e perde consistencia |
| SB-11 | Criar um pacote de CTA e mensagens de confianca reutilizaveis | Copy / Conversao | P2 | SB-02, SB-03 e SB-08 | `copy/site` | Headlines, CTAs e frases de apoio seguem um mesmo padrao em todo o site | O site fica com mensagens dispersas e repetitivas |
| SB-12 | Preparar checklist final de revisao editorial antes de qualquer publicacao futura | QA / Governanca | P3 | Todos os itens anteriores | `orquestrador` | Existe um checklist unico para revisar coerencia, risco e consistencia antes de publicar | Mudancas podem sair desalinhadas entre paginas |

## Top 5 tarefas por impacto

1. SB-01 Definir funcao unica de cada pagina e a hierarquia editorial do site.
2. SB-02 Reescrever a homepage com foco em resultado, problema e CTA principal.
3. SB-08 Fortalecer a pagina de Contato com promessa de retorno, texto de apoio e expectativa clara.
4. SB-09 Criar o pacote de prova com exemplos de solucao, casos ficticios e antes/depois.
5. SB-04 Tornar a pagina de Solucoes mais concreta, com exemplos de uso e resultado pratico.

## Observacao de uso

Se houver conflito entre tarefas, a regra e sempre fazer primeiro o que reduz mais incerteza para o visitante:

1. arquitetura da jornada
2. mensagem principal
3. prova
4. contato
5. refinamento das paginas internas
