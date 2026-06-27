# Revisão de Eficiência dos Agentes

Data: `2026-05-08`

## Contexto

A RITO já executou vários lotes outbound em Novo Hamburgo com e-mail, WhatsApp e fallback operacional. A entrega técnica melhorou bastante, especialmente depois da adoção do template HTML v2 e do WAHA como transporte principal de WhatsApp, mas a resposta humana segue muito baixa.

Leitura principal: o problema deixou de ser apenas execução. A operação agora precisa tratar outbound como aprendizado de mercado e abrir uma frente de aquisição que gere confiança antes do contato direto.

## Achados

### 1. Prospecção estava boa em volume, mas pouco orientada a aprendizado

O agente já coleta empresas, canais e hipóteses de oferta com boa estrutura. O ajuste necessário era impedir que silêncio virasse apenas mais volume.

Mudança aplicada:

- cada novo lote deve declarar hipótese de teste
- batches sem resposta devem gerar aprendizado por segmento, canal, oferta e CTA
- o agente deve classificar `probabilidade_de_dor_visivel` e `momento_de_compra_provavel`

### 2. Disparo precisava fechar o ciclo de performance

O agente de disparo já validava canal, chatId, WAHA e fallback. Faltava transformar telemetria em decisão comercial.

Mudança aplicada:

- consolidar enviados, entregues, lidos, bounces, autorespostas, respostas humanas e conversas qualificadas
- enviar aprendizado para `Growth / Aquisição` quando houver entrega técnica sem resposta humana
- registrar follow-up curto em autorespostas abertas como ação operacional, não como resposta humana

### 3. Atendimento precisava distinguir ruído de interesse

Autorespostas, menus automáticos e reações estavam entrando muito perto do mesmo fluxo de conversa. Isso poderia inflar percepção de resposta ou gerar réplica inadequada.

Mudança aplicada:

- classificar entrada como humana, autoresposta, menu, reação ou ruído técnico
- não tratar autoresposta como interesse comercial
- usar resposta curta aprovada apenas quando a autoresposta abrir espaço com algo como `como podemos ajudar?`

### 4. Growth estava correto, mas ainda genérico para o momento atual

O agente de Growth já tinha modos para SEO, Meta Ads, Google Ads, CRO e mensuração. O ajuste foi transformar baixa resposta outbound em gatilho explícito para aquisição, não em plano abstrato.

Mudança aplicada:

- adicionar `local_presence`
- exigir evento de conversão antes de mídia paga
- separar Google Ads de intenção ativa e Meta/Instagram Ads de reconhecimento/aquecimento
- bloquear qualquer dependência de acesso automatizado a Instagram

## Direção recomendada

1. Parar de escalar outbound frio como canal principal por alguns dias.
2. Criar medição mínima do site antes de investir em ads.
3. Fortalecer páginas de destino por oferta:
   - software sob medida para pequenas empresas
   - automação de atendimento e rotina
   - dashboards e controles internos
   - site institucional para negócios locais
4. Rodar Google Ads pequeno para intenção ativa.
5. Rodar Meta/Instagram Ads com criativos educativos, sem scraping ou visita automatizada a perfis.
6. Usar outbound como complemento: contato com empresas que já viram anúncio, clicaram, responderam formulário ou pertencem a segmentos que performaram.

## Fontes oficiais usadas como referência

- Google Search Central, SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google Search Console, Getting Started: https://support.google.com/webmasters/answer/10267942
- Google Analytics, key events: https://support.google.com/analytics/answer/12844695
- Google Ads, Search campaigns: https://support.google.com/google-ads/answer/9510373
- Google Business Profile, getting started: https://support.google.com/business/answer/6337431
- Meta for Business, Instagram ads: https://www.facebook.com/business/ads/instagram-ad
- Meta for Business, Advantage+ placements: https://www.facebook.com/business/ads/meta-advantage-plus/placements

