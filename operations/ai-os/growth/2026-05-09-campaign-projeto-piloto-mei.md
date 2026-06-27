# Campaign Brief: Projeto Piloto RITO para MEIs

## Status

- estado: criativos feed aprovados / aguardando liberacao da conta Meta
- dono: growth

## Contexto

- data: `2026-05-09`
- canal: landing page + campanha pequena de teste
- modo: meta_ads / google_ads / cro / measurement
- objetivo: gerar primeiros projetos pequenos para validar entrega, criar portfólio e obter cases reais
- publico: MEIs, autônomos, microempresas e pequenos negócios com rotina manual
- oferta: condição especial para soluções pequenas sob medida
- pagina de destino: `https://ritosistemas.com/pages/projeto-piloto.html`
- origem do aprendizado: baixa resposta humana nos primeiros lotes outbound

## Hipotese

- problema a resolver: pequenos negócios têm rotinas manuais incômodas, mas não se reconhecem na compra de "software sob medida"
- promessa principal: uma solução pequena, útil e viável para organizar uma rotina real
- acao desejada: enviar a rotina pelo formulário ou chamar no WhatsApp
- metricas de sucesso:
  - leads recebidos pelo formulário
  - cliques no WhatsApp da landing
  - leads com problema claro e projeto pequeno viável
  - cases autorizados
- criterio para pausar ou iterar:
  - muitos leads sem rotina concreta
  - curiosidade sem disposição para pagar
  - pedidos grandes demais para piloto
  - baixo clique em CTA após tráfego pago

## Estrutura da Campanha

- formato: landing page específica + criativos curtos
- mensagem principal: `Uma solução pequena para tirar uma rotina do improviso`
- criativo ou copia base:
  - `Sua rotina ainda depende de planilha, caderno ou mensagens perdidas no WhatsApp?`
  - `A RITO está selecionando pequenos negócios para criar soluções simples sob medida.`
  - `Pode ser uma planilha inteligente, controle, automação, painel ou ferramenta interna.`
- pagina de destino: `/pages/projeto-piloto.html`
- verba prevista: pequena, a definir após medição
- UTM ou identificacao de origem:
  - `utm_source=meta`
  - `utm_medium=paid_social`
  - `utm_campaign=projeto_piloto_mei`
  - `utm_content=<criativo>`
- evento de conversao principal: envio do formulário da landing
- evento de apoio: clique no WhatsApp

## Medicao

- base implementada no site: `window.dataLayer` + `window.ritoTrack`
- eventos:
  - `rito_page_view`
  - `click_pilot_landing`
  - `click_whatsapp`
  - `click_email`
  - `click_instagram`
  - `generate_lead_form`
- campos salvos no lead:
  - `utm_source`
  - `utm_medium`
  - `utm_campaign`
  - `utm_content`
  - `utm_term`
  - `landing_page`
  - `referrer`
- proximo encaixe: adicionar GA4, GTM ou Pixel quando os IDs forem definidos

## Criativos Selecionados

- pacote: `deliverables/social-assets/meta-projeto-piloto/`
- formato: `1080x1350`
- principal:
  - `feed-4x5/00-principal-cases-1080x1350.png`
- variacoes:
  - `feed-4x5/01-controles-simples-1080x1350.png`
  - `feed-4x5/02-rotina-solucao-1080x1350.png`
- plano da campanha:
  - `operations/ai-os/growth/meta-projeto-piloto/campaign-launch-plan.md`
- copies:
  - `operations/ai-os/growth/meta-projeto-piloto/ad-copies.md`
- UTMs:
  - `operations/ai-os/growth/meta-projeto-piloto/utm-links.csv`

## Prompts de Criativos

### Criativo 1: Rotina no improviso

Prompt:

```text
Crie uma imagem publicitaria vertical 4:5 para uma pequena empresa de software chamada RITO Sistemas. Estilo fotografia editorial realista, brasileira, acolhedora e premium, sem parecer banco de imagens corporativo. Cena: uma mesa de pequeno negocio local com caderno de pedidos, post-its, celular com conversas de WhatsApp borradas, planilha aberta no notebook e uma xicara de cafe; a composicao deve sugerir rotina manual, mas com uma area limpa para texto no lado esquerdo. Paleta: azul petroleo profundo, areia clara, dourado discreto e branco. Iluminacao natural de manha, detalhes organizados, sensacao de "da para simplificar". Nao inserir textos, nao inventar logotipo, nao mostrar marcas de aplicativos claramente.
```

### Criativo 2: Solucao pequena, resultado visivel

Prompt:

```text
Crie uma imagem publicitaria vertical 4:5 para campanha de uma empresa brasileira de software sob medida para MEIs e pequenos negocios. Estilo 3D editorial sofisticado misturado com fotografia de produto, visual moderno e humano. Cena: um notebook e um celular exibindo interfaces genericas de controle simples, dashboard limpo, lista de pedidos e grafico pequeno; ao redor, objetos de pequenos negocios como etiquetas, embalagem, agenda e maquina de cartao sem marca. A imagem deve transmitir "uma ferramenta simples feita para a rotina real". Paleta azul petroleo, areia, branco quente e acento dourado. Deixar espaco vazio elegante para titulo. Sem texto renderizado, sem logos falsos, sem icones de redes sociais reconheciveis.
```

### Criativo 3: Do pedido ao controle

Prompt:

```text
Crie uma imagem publicitaria vertical 4:5, cinematic clean, para uma campanha de tecnologia para pequenos negocios. Cena: uma pessoa dona de microempresa em um ambiente realista e bonito, olhando para um tablet ou notebook com um painel simples de controle; ao fundo, elementos sutis de loja, consultorio ou atelie, sem especificar segmento. A expressao deve ser tranquila, como se a rotina estivesse mais clara. Estetica premium, luz natural, profundidade de campo, tons azul petroleo, areia clara, branco e dourado suave. Composicao com area livre na parte superior para copy. Nao colocar texto, nao criar logotipo, nao mostrar marcas reais.
```

## Proximo Passo

- responsavel: Growth / Site / UX
- prazo: imediato
- dependencia:
  - landing page publicada no branch `hostinger`
  - formulário validado localmente com campos de campanha e rastreamento
  - validar URL pública fora do bloqueio corporativo de domínio recém-registrado
  - conectar GA4, GTM ou Pixel quando os IDs forem definidos
- criterio de aprovacao:
  - página publicada
  - formulário recebendo origem `projeto_piloto_mei`
  - copy aprovada
  - condição de case clara
- decisao esperada ao final do teste:
  - manter oferta
  - ajustar público
  - trocar promessa
  - pausar se os leads vierem sem aderência

## Memoria

- aprendizado esperado: se uma oferta pequena e concreta gera mais conversa do que outbound frio
- risco de campanha: atrair pedidos grandes, genéricos ou sem disposição de investimento
- teste a repetir ou evitar:
  - repetir se vierem rotinas pequenas com clareza
  - evitar promessa de gratuidade ou "fazemos qualquer coisa"
