# Guia de Prompt Visual GPT Image 2 para Marketing da RITO

## Objetivo

Padronizar como os agentes da RITO criam prompts para imagens de campanha, posts, stories, criativos de anúncio, mockups e peças visuais geradas com GPT Image 2.

Fontes oficiais consultadas:

- OpenAI Cookbook, GPT Image Generation Models Prompting Guide: `https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide`
- OpenAI API Docs, Image generation: `https://developers.openai.com/api/docs/guides/image-generation`
- OpenAI API Docs, GPT Image 2 model: `https://developers.openai.com/api/docs/models/gpt-image-2`

## Regra central

Prompt visual da RITO deve ser escrito como especificação de produção, não como frase inspiracional.

Um bom prompt precisa dizer:

- para qual plataforma e superfície a imagem será usada;
- qual tamanho/proporção final precisa funcionar;
- qual cena principal deve aparecer;
- qual texto exato deve estar na arte, quando houver;
- onde ficam logo, CTA, headline e elementos principais;
- quais elementos devem ser preservados ou proibidos;
- quantas variações devem ser geradas;
- quais critérios bloqueiam a peça.

## Decisão operacional atual

A partir de `2026-05-17`, a RITO pode gerar imagens de campanhas, stories, posts, mockups e variações diretamente no Codex usando a ferramenta `ImageGen`.

Fluxo padrão:

1. Criar o prompt visual seguindo este guia.
2. Enviar o prompt para `ImageGen` quando a solicitação for produção de imagem.
3. Preservar o arquivo original gerado na pasta interna do Codex.
4. Copiar a imagem aprovada ou candidata para o diretório correto em `deliverables/social-assets/`.
5. Validar proporção e dimensão; se necessário, exportar uma versão final no tamanho correto.
6. Criar ou atualizar o `README.md` do lote com prompt, objetivo, data e observações.
7. Encaminhar para revisão visual antes de publicar.

Exceção:

- Se o usuário pedir explicitamente apenas o prompt, não gerar imagem.
- Se a imagem exigir asset externo que não está disponível, registrar o bloqueio antes de gerar.
- Se a fidelidade do logo for crítica, gerar a imagem com espaço reservado e aplicar o logo oficial depois em ferramenta de design.

## Diretórios de saída

- Stories orgânicos: `deliverables/social-assets/instagram-stories/YYYY-MM-DD-nome-do-lote/`
- Feed de campanha Meta: `deliverables/social-assets/meta-projeto-piloto/feed-4x5/`
- Fontes/originais de campanha: `deliverables/social-assets/meta-projeto-piloto/source/`
- Avatares e perfis: `deliverables/social-assets/profile-images/`
- Templates e experimentos reutilizáveis: `deliverables/social-assets/templates/`

Nomear arquivos com prefixo numérico e descrição curta:

```text
01-projeto-piloto-story-codex-imagegen.png
02-rotina-cliente-dashboard-story.png
03-site-simples-feed-4x5.png
```

## Modelo padrão de prompt

Use este formato sempre que o agente for gerar prompt para GPT Image 2:

```text
Criar [N] imagens finais para [plataforma/superfície].

Uso:
- Campanha/objetivo:
- Público:
- Peça:
- Formato final:
- Proporção:
- Dimensão final desejada:

Cena principal:
- Ambiente:
- Pessoa/objeto principal:
- Ação ou situação:
- Emoção:
- Estilo visual:

Composição:
- Hierarquia:
- Posição do assunto:
- Espaço livre para texto:
- Safe area:
- Logo:
- CTA:

Texto na imagem, EXATO, sem alterar:
"..."

Identidade RITO:
- Paleta:
- Sensação:
- Tipografia desejada:
- Usar logo oficial fornecido como referência, sem redesenhar.

Restrições:
- Não adicionar textos além dos especificados.
- Não alterar nem inventar logo.
- Não usar marca d'água.
- Não usar aparência de slide, flyer ou apresentação.
- Não cortar palavras.
- Não encostar texto nas bordas.
- Não usar elementos que pareçam genéricos de banco de imagem.

Entrega:
- Gerar exatamente [N] imagens.
- Cada imagem deve ter variação real de cena, pessoa/objeto ou composição.
- Manter a mesma identidade visual entre as variações.
```

## Tamanhos e proporções

### Quando a imagem for gerada no ChatGPT ou ferramenta visual

Pedir diretamente a dimensão final de uso:

- Instagram Feed retrato: `1080x1350`, proporção `4:5`.
- Instagram Stories/Reels: `1080x1920`, proporção `9:16`.
- Quadrado/feed grid: `1080x1080`, proporção `1:1`.
- Facebook/LinkedIn feed retrato: preferir `1080x1350`, se o canal aceitar.

Observação operacional:

- a ferramenta pode devolver uma imagem na proporção correta, mas em resolução diferente;
- nesse caso, preservar o arquivo original e criar uma versão final exportada no tamanho correto;
- nomear a versão final com dimensão explícita, por exemplo `01-story-1080x1920.png`;
- a versão final, não apenas o original bruto, deve ser usada para publicação.

### Quando a imagem for gerada via API com `gpt-image-2`

O `gpt-image-2` aceita tamanhos flexíveis, mas as bordas precisam respeitar as restrições do modelo, incluindo múltiplos de 16. Por isso:

- para uma peça final `1080x1350`, gerar em `1088x1360` e depois exportar/cortar para `1080x1350`;
- para uma peça final `1080x1920`, gerar em `1088x1920` e depois exportar/cortar para `1080x1920`;
- para `1080x1080`, gerar em `1088x1088` e depois exportar/cortar para `1080x1080`;
- evitar pedir acima de `2560x1440` sem motivo, porque saídas maiores tendem a variar mais.

## Qualidade

- `low`: exploração rápida, variações iniciais, ideias com pouco texto e baixo risco.
- `medium`: padrão recomendado para posts e criativos simples.
- `high`: peças com texto pequeno, anúncios com copy dentro da imagem, mockups, close-ups, identidade visual sensível ou arte final para campanha.

Para os criativos principais da RITO, usar `medium` ou `high`. Usar `low` apenas para rascunhos.

## Texto dentro da imagem

Quando houver texto na arte:

- escrever o texto exato entre aspas;
- pedir para aparecer uma única vez;
- limitar a quantidade de texto;
- indicar posição, tamanho relativo, contraste e estilo tipográfico;
- não pedir parágrafos longos dentro da imagem;
- para palavras importantes como `RITO`, soletrar se houver risco de erro: `R-I-T-O`;
- se o texto vier errado, pedir uma nova versão alterando apenas a tipografia ou o bloco de texto.

## Logos e identidade visual

Para peças da RITO:

- preferir inserir o logo oficial depois, em ferramenta de design, quando fidelidade for crítica;
- se o logo for gerado dentro da imagem, fornecer o asset oficial como referência e exigir que ele não seja redesenhado;
- nunca aceitar logo inventado, distorcido, serrilhado ou com letras erradas;
- quando houver dúvida entre estética da imagem e fidelidade do logo, priorizar fidelidade e escalar para revisão humana.

## Fotorealismo

Para imagens de campanha com pessoas ou pequenos negócios:

- descrever a cena como uma foto real acontecendo naquele momento;
- usar textura real: papel, madeira, tecido, tela, reflexo, sombra, objetos do cotidiano;
- evitar excesso de perfeição, pose publicitária ou brilho artificial;
- pedir luz natural, enquadramento plausível e ambiente coerente com MEI/microempresa;
- evitar pessoa com aparência genérica demais de banco de imagem.

## Variações

Quando pedir variações:

- indicar explicitamente o número de imagens;
- manter o mesmo objetivo, texto, CTA e identidade;
- variar uma dimensão por vez:
  - cenário;
  - arquétipo de negócio;
  - composição;
  - pessoa/objeto principal;
  - proximidade do enquadramento.

Exemplo:

```text
Gerar exatamente 3 imagens:
1. pequeno varejo/oficina com controles de pedidos;
2. loja/ateliê com rotina de clientes e entregas;
3. prestador de serviço com dashboard simples no tablet.
```

## Iteração

Não corrigir tudo ao mesmo tempo. Quando uma imagem vier quase boa:

- preservar cena, composição, logo, paleta e texto que funcionaram;
- mudar apenas um problema por vez;
- repetir o que deve permanecer igual;
- não pedir nova direção criativa se o problema for só corte, texto ou contraste.

## Prompt negativo padrão da RITO

Use quando fizer sentido:

```text
Evitar: aparência de slide, flyer corporativo genérico, banco de imagem frio, texto excessivo, botão falso, marca d'água, logo inventado, letras erradas, palavras cortadas, elementos encostando nas bordas, estética futurista, neon, excesso de brilho, pessoas posando de forma artificial, interface impossível ou dashboard ilegível.
```

## Checklist antes de entregar prompt ao usuário

- A plataforma está explícita?
- A dimensão/proporção está explícita?
- O número de imagens está explícito?
- O texto da arte está exato e curto?
- A posição do texto e do logo foi indicada?
- Há safe area?
- A cena descreve um negócio pequeno real, não um cenário genérico?
- Há restrições contra logo errado, texto extra e marca d'água?
- O prompt pede variações reais, não clones?
- Está claro o que preservar em uma iteração?
- Se a tarefa era produção, a imagem foi gerada via ImageGen?
- A imagem gerada foi copiada para o diretório correto do projeto?
- Existe versão final na dimensão correta para a plataforma?
- O README do lote registra prompt, objetivo e arquivo final?

## Exemplo para campanha Projeto Piloto

```text
Criar exatamente 3 imagens finais para campanha da RITO Sistemas no Instagram Feed.

Uso:
- Campanha: Projeto Piloto RITO para MEIs e pequenos negócios.
- Objetivo: atrair pessoas que têm uma rotina pequena para organizar com software, planilha inteligente, automação, dashboard ou site simples.
- Formato final: Instagram Feed retrato.
- Proporção: 4:5.
- Dimensão final desejada: 1080x1350.

Cena principal:
- Ambiente realista de pequeno negócio brasileiro, com mesa de trabalho, pedidos, anotações, notebook ou tablet com painel simples.
- A cena deve parecer cotidiana, organizada e humana, não corporativa demais.
- Estilo fotorealista premium, luz natural quente, textura real de papel, madeira, tela e objetos de rotina.

Composição:
- Deixar área livre à esquerda ou no topo para headline.
- Assunto principal visível à direita ou no centro inferior.
- Manter safe area nas bordas.
- Inserir logo RITO Sistemas no topo com boa legibilidade, usando o asset oficial como referência, sem redesenhar.

Texto na imagem, EXATO, sem alterar:
"Tem uma rotina que você queria organizar?"
"Condição especial para primeiros cases"
"Controle • Automação • Planilha inteligente • Dashboard • Site simples"
"Enviar minha ideia"

Identidade RITO:
- Azul petróleo profundo, off-white quente e dourado discreto.
- Visual sóbrio, moderno, confiável e próximo.
- Tipografia elegante, clara, com boa leitura em tela pequena.

Restrições:
- Não adicionar textos além dos especificados.
- Não cortar nenhuma palavra.
- Não criar logo alternativo.
- Não usar marca d'água.
- Não parecer slide, flyer ou apresentação.
- Não usar aparência futurista ou startup genérica.

Entrega:
- Gerar exatamente 3 imagens.
- Cada imagem deve variar o tipo de pequeno negócio e a composição, mantendo a mesma identidade visual.
```
