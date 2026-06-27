# Setup de Marca no Canva

## Objetivo

Registrar o estado atual dos assets da RITO dentro do Canva e o que foi possível configurar via plugin conectado.

## Estado atual

### Assets enviados com sucesso para a biblioteca do Canva

- Monograma limpo da marca
  - nome no Canva: `RITO Monograma Limpo 2048`
  - asset id: `MAHHZDqmJ4M`
- Wordmark da marca
  - nome no Canva: `RITO Wordmark`
  - asset id: `MAHHZLb-WtM`
- Template institucional de Instagram
  - nome no Canva: `RITO Instagram Template Institucional PNG`
  - asset id: `MAHHZ0nhDtE`
- Template dor e resultado de Instagram
  - nome no Canva: `RITO Instagram Template Dor Resultado PNG`
  - asset id: `MAHHZ4w8SM0`

### Brand kits disponíveis

- `list-brand-kits` voltou a responder em `2026-04-20`
- resultado atual: `0` brand kits configurados

## Paleta oficial da RITO

- `#173847` brand principal
- `#0d2430` brand forte
- `#315161` brand médio
- `#f4f0e9` fundo quente
- `#fbf7f1` off-white
- `#152733` texto principal
- `#b89163` acento

## Tipografia de referência

- títulos: `Sora`
- texto corrido: `Manrope`
- labels e detalhes técnicos: `IBM Plex Mono`

## Templates locais preparados para Canva

Os arquivos abaixo foram gerados e publicados para uso como base visual:

- [instagram-template-institucional.png](../../../deliverables/social-assets/templates/instagram-template-institucional.png)
- [instagram-template-dor-resultado.png](../../../deliverables/social-assets/templates/instagram-template-dor-resultado.png)

## Assets locais oficiais para uso institucional no Canva

Para posts, capas, apresentações e peças institucionais que usem a família atual da marca, os assets preferenciais locais agora são:

- [rito-monograma-petroleo-4x.png](../../../logos/site-and-institutional-high-res/rito-monograma-petroleo-4x.png)
- [rito-monograma-branco-4x.png](../../../logos/site-and-institutional-high-res/rito-monograma-branco-4x.png)
- [rito-wordmark-petroleo-4x.png](../../../logos/site-and-institutional-high-res/rito-wordmark-petroleo-4x.png)
- [rito-wordmark-branco-4x.png](../../../logos/site-and-institutional-high-res/rito-wordmark-branco-4x.png)

## Limitação atual do plugin

No momento, o conector disponível do Canva:

- permite listar brand kits
- permite gerar designs
- permite criar designs a partir de candidatos
- permite editar designs existentes
- permite subir alguns assets por URL

Mas, neste ambiente, ele **não expôs criação de brand kit** e as chamadas de:

- `import-design-from-url`
- `image-to-design`

falharam com erro de transporte `missing-content-type; body:` ao tentar importar os templates PNG por URL pública.

Em `2026-04-20`, a tentativa de leitura de:

- `list-brand-kits`
- `get-assets`

primeiro retornou o mesmo erro de transporte `missing-content-type; body:`, mas depois o conector voltou a responder normalmente.

Isso indica que o problema não era apenas permissão. Havia também uma instabilidade temporária do `codex_apps` / conector Canva no desktop.

### Estado confirmado em `2026-04-20` após recuperação parcial

- `list-brand-kits`: funcionando
- `get-assets`: funcionando
- `upload-asset-from-url`: funcionando
- `image-to-design`: respondeu, mas a rota de AI ficou limitada pelo plano da Canva
- `import-design-from-url`: ainda falhou para PNG flat com `invalid_file`

### Limite de plano identificado

Ao tentar converter template em design editável com `image-to-design`, a Canva retornou a mensagem:

`You've hit your Canva plan's monthly AI limit. To keep creating with ChatGPT, you may need to upgrade. For options, check your plan settings in Canva.`

## Consequência prática

Hoje foi possível criar o equivalente operacional mínimo de marca no Canva por meio de:

- assets oficiais na biblioteca
- templates locais publicados e prontos para reaproveitamento
- templates também enviados como assets para uso manual em novos designs

Mas a criação do **Brand Kit nativo do Canva** continua dependente de:

1. o conector passar a expor essa função, ou
2. configuração manual dentro do Canva com os mesmos assets e paleta.

## Próximo uso recomendado

- usar os assets `MAHHZDqmJ4M` e `MAHHZLb-WtM` em novas gerações no Canva
- usar também os templates `MAHHZ0nhDtE` e `MAHHZ4w8SM0` como base manual de composição
- evitar gerar peças sem os assets reais da marca
- tratar `image-to-design` como rota opcional, porque hoje ela está sujeita ao limite mensal de AI do plano Canva
- usar os templates locais como referência visual até o fluxo de importação do Canva estabilizar

## Regra de proteção da marca

- não usar o monograma derivado `rito_monogram_r_clean.*` como substituto automático do logo oficial em peças institucionais
- qualquer simplificação, reconstrução ou vetorização do `R` exige aprovação humana explícita antes de virar asset protagonista
- para posts do Instagram, o uso preferencial é:
  1. assets oficiais originais da marca, com preferência para `logos/site-and-institutional-high-res/` quando a peça usar a família atual institucional
  2. composição manual em artboard nativo
  3. revisão visual antes de qualquer commit no Canva
