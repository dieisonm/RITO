# Checklist de QA Visual para Instagram

## Regra principal

Nenhuma peça de Instagram da RITO pode ser considerada pronta se qualquer item abaixo falhar.

## Asset e marca

- O logo principal ou monograma usado como protagonista é o asset oficial aprovado da marca.
- Para a família atual institucional da RITO, preferir os arquivos em `assets/brand/logos/site/` quando a peça exigir logo grande ou export de alta nitidez.
- Não substituir o logo oficial por releitura, simplificação, vetorização derivada ou variação reconstruída sem aprovação humana explícita.
- Se houver dúvida entre fidelidade ao logo e nitidez, priorizar fidelidade e escalar em vez de “corrigir” a marca por conta própria.
- Não usar logo raster pequeno ampliado como hero.
- O monograma não pode apresentar serrilhado visível em zoom.
- O wordmark precisa ter contraste suficiente com o fundo.
- Não usar marca d'água gigante por padrão.
- O logo só aparece grande quando ele realmente sustenta a composição.

## Composição

- A peça não pode parecer slide de apresentação.
- A peça não pode parecer flyer genérico.
- A peça não pode parecer capa de documento ou página com foto em cima e “texto corrido embaixo” quando o objetivo for post nativo de Instagram.
- A hierarquia visual precisa ser clara em miniatura.
- O fundo precisa contribuir para a peça, não servir apenas como preenchimento morto.
- O espaço negativo deve ser intencional, não vazio sem função.
- Os elementos precisam estar alinhados com consistência óptica, não só matemática.

## Texto

- Nenhuma palavra pode ficar cortada.
- Nenhuma linha pode encostar na borda inferior ou lateral.
- O texto precisa respeitar safe area de feed e grid.
- O bloco de texto não pode ficar perdido sobre área de baixa legibilidade.
- Não usar texto demais na arte.
- O CTA na arte deve parecer editorial e real, não botão falso.

## Formato de Instagram

- Exportação em `1080 x 1350` para feed retrato.
- Conferir a leitura também no recorte do grid.
- Não usar elementos tipo `1/3`, `2/3`, `3/3` se isso não fizer sentido na publicação final.
- O conjunto dos 3 primeiros posts não pode repetir hero visual de forma óbvia.

## Foto e imagem

- Foto não pode ter cara óbvia de banco de imagem genérico.
- Se a regra do projeto pedir, não usar rosto humano.
- Não repetir a mesma foto em peças diferentes do mesmo grid inicial.
- A foto precisa reforçar o tema, não competir com o texto.
- O crop deve ser pensado para a mensagem da peça.

## Imagens geradas por IA

- O prompt usado precisa declarar plataforma, superfície, formato, proporção, dimensão, texto exato e número de variações.
- Quando houver texto na imagem, a revisão deve conferir palavra por palavra.
- Se o logo da RITO foi gerado dentro da imagem, revisar com rigor extra; qualquer distorção bloqueia a peça.
- Se a IA gerou layout quase bom, mas com erro pequeno, pedir iteração cirúrgica em vez de nova direção criativa completa.
- Se o objetivo for anúncio, a peça precisa parecer criativo nativo do canal, não mockup bonito sem CTA claro.

## Revisão final obrigatória

- Ver em tamanho normal.
- Ver com zoom para detectar serrilhado, corte e microerros.
- Ver em conjunto com os outros posts do grid.
- Ver se a peça continua boa sem depender de explicação.

## Critério de bloqueio

Se qualquer um destes problemas aparecer, a peça deve ser bloqueada:

- serrilhado no logo
- texto cortado
- alinhamento amador
- cara de slide
- repetição de foto no grid
- CTA falso
- marca usada em lugar errado
- composição confusa

## Aplicação nos agentes

Este checklist deve ser tratado como gate para:

- `Conteúdo Orgânico`
- `Creative Production / Social Design Ops`
- `Branding`
- `Revisor`

Quando a peça vier de GPT Image 2 ou outra IA de imagem, aplicar também `docs/agents/agent-system/gpt-image-2-visual-prompting-guide.md`.

## Regra operacional adicional para Canva

- Não usar `image-to-design` como fluxo padrão para posts institucionais ou peças centrais de marca da RITO.
- Para posts da RITO no Canva, preferir artboard nativo e composição manual com assets oficiais da marca.
