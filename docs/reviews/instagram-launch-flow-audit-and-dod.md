# Auditoria do Fluxo de Instagram e Definition of Done

Data: 19/04/2026

## Escopo auditado

- `ops/instagram/README.md`
- `docs/brand/presence/instagram-launch-strategy.md`
- `ops/instagram/posts/README.md`
- `ops/instagram/posts/2026-04-launch-post-01-apresentacao.md`
- `ops/instagram/posts/2026-04-launch-post-02-dor-planilhas-e-retrabalho.md`
- `ops/instagram/posts/2026-04-launch-post-03-exemplo-controle-e-rotina.md`

## Diagnóstico resumido

O fluxo atual acerta bem a intenção editorial da largada do Instagram, mas ainda trata "direção criativa" como se fosse "post pronto para publicação". Isso abriu espaço para retrabalho em quatro pontos recorrentes:

1. a ideia estava aprovada, mas a arte final não estava realmente pronta;
2. a revisão estava subjetiva e sem checklist objetivo;
3. não havia pacote de publicação fechado por post;
4. a equipe não tinha uma Definition of Done operacional para bloquear peça incompleta.

## Por que o processo gerou retrabalho

### 1. Existe estratégia, mas não existe um workflow de produção fechado

O fluxo define bem o que publicar e em qual ordem, mas não define os entregáveis mínimos por etapa.

Exemplos:

- `ops/instagram/README.md` diz quais materiais existem e qual é a diretriz geral, mas não descreve um pipeline de `brief -> criação -> revisão -> exportação -> validação no app -> publicação`.
- `docs/brand/presence/instagram-launch-strategy.md` orienta formato, frequência, CTA e tom, mas não define quem aprova o quê, nem qual evidência precisa existir para a peça ser considerada pronta.

Resultado: a equipe aprovou peças ainda em estado de exploração visual.

### 2. As regras visuais são corretas, mas ainda genéricas demais para impedir erro básico

Os documentos já dizem para evitar slide, deck e excesso de texto, o que é bom.

Mas faltam regras concretas como:

- formato final obrigatório por post;
- área segura para grid quadrado;
- limite visual de texto por arte;
- regra de unicidade de imagem no conjunto de 3 posts;
- proibição de rostos em banco de imagem para a largada;
- validação de thumbnail antes de aprovar.

Resultado: a peça podia "respeitar a estratégia" no papel e ainda assim falhar no feed real.

### 3. Os briefs dos posts ainda aprovam conceito, não publicação

Os três briefs têm objetivo, ideia visual, legenda e CTA. Isso é um bom começo.

Mas eles ainda não exigem, por exemplo:

- mock de grid com os três posts lado a lado;
- conferência da arte em `4:5` e no corte quadrado;
- checklist visual aprovado;
- arquivo final exportado e validado;
- teste no app do Instagram antes de declarar pronto.

Resultado: houve vários ciclos de "arruma a arte", "agora ficou bom", "no app não encaixou", "a imagem repetiu", "parece slide".

### 4. Não existe um gate explícito de "pacote pronto para publicação"

Hoje o fluxo separa estratégia, posts e artes, mas não existe um estado formal de aprovação final.

O post só deveria avançar para publicação quando existir um pacote fechado contendo:

- arte final;
- legenda final;
- CTA final;
- comentário fixado;
- hashtags finais;
- formato validado;
- thumbnail validada;
- observações de publicação;
- status `ready-to-publish`.

Resultado: materiais "quase prontos" foram tratados como entrega final.

## Critérios de aceite que faltam

### Critérios gerais

- O post precisa existir como peça final, não como direção criativa.
- O formato precisa estar validado para Instagram feed em `4:5`.
- A composição precisa sobreviver ao recorte quadrado do grid do perfil.
- O visual precisa parecer nativo de Instagram, não slide, flyer ou deck.
- O texto na arte precisa ser mínimo e legível em thumbnail.
- O CTA da arte, legenda e comentário fixado precisa estar coerente.
- A peça precisa ser aprovada junto com os outros dois posts, não isoladamente.
- O conjunto dos 3 posts precisa funcionar como vitrine inicial do perfil.

### Critérios visuais ausentes

- Sem repetição de foto ou cena principal entre os 3 posts.
- Sem rostos de banco de imagem na largada.
- Sem cabeçalho fixo, cápsula decorativa desnecessária ou etiqueta que pareça template.
- Sem elementos visuais duplicando demais o mesmo símbolo da marca na mesma peça.
- Logo e monograma com nitidez suficiente, sem serrilhado visível.
- Hierarquia clara: imagem primeiro, marca depois, texto por último.
- Leitura boa tanto no post aberto quanto no grid do perfil.

### Critérios de produção ausentes

- Export final em formato único aprovado.
- Nome de arquivo definitivo.
- Versão congelada para publicação.
- Aprovação registrada do revisor.
- Teste real no app antes de publicar.

## Definition of Done para os 3 posts de lançamento de hoje

Um post só está `Done` quando cumprir todos os itens abaixo.

### 1. Escopo e objetivo

- O papel do post está claro dentro da sequência:
  - `Post 1`: institucional pinável;
  - `Post 2`: dor real;
  - `Post 3`: exemplo prático.
- O post reforça a proposta da RITO para micro e pequenas empresas.

### 2. Formato e exportação

- O arquivo final está em `1080 x 1350`.
- O layout foi pensado para `4:5`.
- O centro visual funciona também no recorte quadrado do grid.
- A peça foi validada em preview real antes da publicação.

### 3. Qualidade visual

- A peça não parece slide, flyer corporativo ou deck.
- O texto da arte é curto e legível.
- A cena principal é forte o suficiente para parar o scroll.
- Não há repetição de foto principal entre os 3 posts.
- Não há rosto humano na base visual da largada.
- O uso da marca está limpo, sem excesso de logos ou monogramas.
- Não há cápsulas, tarjas ou fundos de etiqueta desnecessários.
- Os elementos estão alinhados, centralizados quando necessário e com respiro adequado.

### 4. Qualidade da marca

- As cores pertencem claramente ao universo da RITO.
- O monograma e o nome da marca estão nítidos.
- Não há pixelização perceptível nos elementos da identidade.
- A peça parece de empresa séria e atual, não de material improvisado.

### 5. Coerência do conjunto

- Os 3 posts funcionam juntos quando vistos no grid.
- O `Post 1` é o mais forte institucionalmente para ficar fixado.
- O `Post 2` gera identificação com dor real.
- O `Post 3` mostra transformação de forma simples.
- O trio não parece repetitivo nem genérico.

### 6. Pacote de publicação

- A legenda final está aprovada.
- O CTA final está alinhado com WhatsApp.
- O comentário fixado está pronto.
- As hashtags finais foram reduzidas ao essencial e revisadas.
- A ordem de publicação está definida.

### 7. Gate final

- O criador marca o post como `pronto`.
- O revisor valida a peça com checklist.
- O post passa no teste "eu publicaria isso hoje sem pedir mais ajustes?".
- Se qualquer resposta for `não`, o post volta para produção e não é chamado de pronto.

## Definition of Done específica por post

### Post 1 - Institucional pinável

- peça de marca forte o suficiente para ser o primeiro post fixado;
- composição central clara;
- um único gesto principal de marca;
- nome da empresa e assinatura bem posicionados;
- fundo e composição com presença visual, não tela branca ou layout morto;
- leitura forte no grid e no post aberto.

### Post 2 - Dor real

- imagem ou cena diferente das do carrossel;
- dor identificável em menos de 2 segundos;
- headline curta e humana;
- sem cara de banco de imagem genérico com rosto;
- foco em objeto, rotina, papel, tela, mesa, processo ou sinal visual de retrabalho.

### Post 3 - Carrossel curto

- cada slide comunica uma única ideia;
- slide 1 mostra problema;
- slide 2 mostra organização ou clareza;
- slide 3 fecha com marca e CTA;
- os três slides parecem parte da mesma família visual;
- rótulos como `Antes` e `Depois` entram integrados na composição, nunca como adereço solto.

## Recomendação operacional imediata

Para hoje, o melhor fluxo é:

1. aprovar primeiro o grid dos 3 posts juntos;
2. congelar direção visual antes de refinar detalhes;
3. validar cada peça em `4:5` e no recorte quadrado;
4. só depois fechar legenda, CTA e comentário fixado;
5. publicar apenas quando o trio inteiro passar na Definition of Done acima.

## Mudança de regra sugerida para os agentes

Nenhum agente pode chamar uma peça de "pronta" se não existir:

- arte final exportada;
- revisão de formato;
- revisão de grid;
- revisão de unicidade visual do conjunto;
- pacote de publicação completo.
