# Meta Ads Launch Playbook

Atualizado em `2026-06-17`.

## Base oficial validada

- O Meta Ads Manager hoje trabalha com `6` objetivos consolidados: `Awareness`, `Traffic`, `Engagement`, `Leads`, `App promotion` e `Sales`.
- O Meta também permite campanhas que levam a conversa para o WhatsApp.
- Para campanhas com site, a base mínima recomendável é ter o `Meta Pixel` instalado e validar pelo menos o evento `PageView` antes de depender de otimização por conversão.
- O `Lead` é um dos eventos padrão do Pixel e é o melhor ponto de partida para a RITO neste momento.

Referências oficiais:

- https://www.facebook.com/business/help
- https://developers.facebook.com/docs/meta-pixel/
- https://developers.facebook.com/docs/meta-pixel/get-started/
- https://developers.facebook.com/docs/meta-pixel/reference/

## O que já ficou preparado no site

Foi deixada uma base única de configuração em `site/assets/js/measurement-config.js`.

Com isso, o site agora está pronto para:

- ligar o `Meta Pixel` em um único arquivo, sem espalhar ID em várias páginas;
- manter `GA4` e `Meta` no mesmo fluxo de mensuração;
- registrar `PageView` e `Lead`;
- registrar cliques importantes como eventos customizados:
  - `RitoClickWhatsApp`
  - `RitoClickEmail`
  - `RitoClickInstagram`
  - `RitoClickPilotLanding`
- enviar para os formulários os dados de origem já capturados:
  - UTM
  - `fbclid`
  - `meta_fbp`
  - `meta_fbc`

Isso deixa a RITO em uma posição melhor para:

- medir tráfego pago com menos achismo;
- verificar quais anúncios geram visita e lead;
- preparar uma futura camada de `Conversions API`, se isso passar a valer a pena.

## Passos antes de subir a primeira campanha

1. Criar o Pixel da RITO no Events Manager do Meta.
2. Copiar o ID do Pixel.
3. Preencher `metaPixelId` em `site/assets/js/measurement-config.js`.
4. Publicar a nova versão do site.
5. Abrir o site com a URL normal e depois com UTMs de teste.
6. Confirmar no Meta se `PageView` aparece.
7. Enviar um formulário de teste em:
   - `site/pages/contato.html`
   - `site/pages/projeto-piloto.html`
8. Confirmar se o evento `Lead` aparece.

## Recomendação de campanha inicial

### Fase 1

Rodar `1` campanha principal, não várias ao mesmo tempo.

Motivo:

- a conta acabou de ser desbloqueada;
- a RITO ainda está construindo histórico;
- dividir pouco orçamento em muitas campanhas tende a diluir aprendizado.

### Campanha sugerida

- Objetivo: `Leads`
- Local de conversão: `Website`
- Evento principal: `Lead`
- Página principal: `https://ritosistemas.com/pages/projeto-piloto.html`
- Página secundária de apoio: `https://ritosistemas.com/pages/contato.html`

### Público inicial sugerido

Inferência operacional da RITO, não regra do Meta:

- começar localmente em `Novo Hamburgo` e `Vale dos Sinos`;
- manter foco em MEI, microempresa e pequena empresa;
- evitar abrir Brasil inteiro na primeira rodada.

### Criativos iniciais

Rodar poucos criativos, com proposta diferente entre si:

- linha `rotina e clareza operacional`
- linha `site e presença digital`
- linha `projeto piloto / solução simples sob medida`

O ideal é usar peças que já existem no banco de stories e transformar só o necessário em formato de anúncio.

## Segunda frente, só depois da primeira leitura

Depois que a campanha de website tiver algum volume mínimo, abrir uma frente de `Click to WhatsApp`.

Uso recomendado:

- quando o lead tende a converter melhor em conversa rápida;
- quando a pessoa ainda não quer preencher formulário;
- quando vocês quiserem testar uma abordagem mais direta e menos formal.

Mas a ordem sugerida é:

1. primeiro medir `Lead` no site;
2. depois abrir `WhatsApp` como segunda rota de captura.

## O que observar nos primeiros dias

- se o Pixel dispara `PageView` em todas as páginas principais;
- se o formulário dispara `Lead`;
- se o tráfego pago está chegando com `utm_source`, `utm_medium`, `utm_campaign` e `fbclid`;
- se os leads do piloto têm qualidade melhor do que os leads da página geral;
- se o volume de clique em WhatsApp começa a competir com o formulário.

## Próximo passo mais lógico

Depois que o Pixel ID existir, fazer:

1. preencher `metaPixelId`;
2. publicar o site;
3. validar evento no Meta;
4. criar a campanha `Leads | Website | Projeto Piloto`.
