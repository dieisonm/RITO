# Plano de Campanha: Projeto Piloto RITO

Data: `2026-05-10`

## Status

- conta Meta em revisao/desbloqueio
- nao acessar Instagram automaticamente
- criativos feed 4:5 prontos
- landing publicada em `https://ritosistemas.com/pages/projeto-piloto.html`
- UTMs preparadas
- Pixel/Dataset pendente

## Objetivo do primeiro teste

Validar se uma oferta pequena e concreta gera leads melhores do que outbound frio.

Oferta:

```text
Projeto Piloto RITO: soluções pequenas sob medida para pequenos negócios.
```

## Estrutura Recomendada

Campanha:

```text
RITO | Projeto Piloto MEI | Maio 2026
```

Objetivo recomendado:

```text
Tráfego
```

Motivo:

```text
Usar Tráfego até o Meta Pixel/Dataset estar criado, instalado e testado. Depois migrar para Leads ou Conversões quando houver evento confiável de envio de formulário.
```

Conjunto de anúncios:

```text
NH e região | Pequenos negócios | Feed 4x5
```

Localização inicial:

```text
Novo Hamburgo + raio regional próximo
```

Publico inicial:

```text
Pessoas adultas com interesse em empreendedorismo, MEI, pequenos negócios, loja virtual, gestão financeira, vendas online e negócios locais.
```

Orçamento inicial:

```text
R$ 20 a R$ 30 por dia por 5 a 7 dias.
```

Regra:

```text
Nao ficar mexendo diariamente. A campanha precisa de pelo menos 48h para leitura inicial.
```

## Anuncios

1. `RITO_PP_MEI_Feed_00_Principal_Cases`
2. `RITO_PP_MEI_Feed_01_Controles_Simples`
3. `RITO_PP_MEI_Feed_02_Rotina_Solucao`

Detalhes de copy e links:

`ops/ai-os/growth/meta-projeto-piloto/ad-copies.md`

Links com UTM:

`ops/ai-os/growth/meta-projeto-piloto/utm-links.csv`

## Medicao Sem Pixel

Enquanto o Pixel nao estiver instalado, medir pelo backend da landing:

- `utm_source`
- `utm_medium`
- `utm_campaign`
- `utm_content`
- leads no formulario
- cliques WhatsApp quando capturados pelo frontend

## Medicao Com Pixel

Quando a conta Meta estiver liberada:

1. Criar ou localizar o Dataset/Pixel.
2. Enviar o Pixel ID para instalar no site.
3. Testar eventos no Events Manager.
4. Medir pelo menos:
   - `PageView`
   - `ViewContent`
   - `Lead`
   - `Contact`
5. So depois considerar campanha com objetivo `Leads`.

## Criterios de Leitura

Primeiras 48h:

- verificar se os anuncios estao sendo aprovados e entregues
- nao otimizar ainda

Dia 3 a 5:

- pausar criativo com CTR muito baixo
- manter criativo com maior taxa de clique qualificado
- revisar se leads chegaram com problema claro

Dia 7:

- calcular custo por lead
- decidir se aumenta verba, troca promessa ou troca publico

## Riscos

- A conta Meta esta sensivel por bloqueio recente, entao evitar qualquer automacao.
- Nao usar scraping de Instagram.
- Nao conectar ferramentas de terceiros desnecessarias.
- Nao impulsionar post diretamente se o objetivo for medir aprendizado.

## Proximas Pecas

Gerar as mesmas 3 linhas criativas em formato Stories/Reels:

```text
1080x1920, vertical 9:16
```

