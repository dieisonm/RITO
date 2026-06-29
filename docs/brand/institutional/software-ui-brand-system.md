# Sistema Visual para Software e UI

## Objetivo

Definir como a identidade da RITO Sistemas deve se comportar dentro de produtos digitais, painéis, formulários, relatórios e sistemas internos.

Este documento traduz a marca do site para interfaces de software sem perder sobriedade, clareza e consistência.

## Base de referência

- Paleta real do site em `site/assets/css/styles.css`
- Tipografia real do site em `site/index.html`
- Lógica visual editorial e limpa já usada na home
- Família atual do site em `logos/`
- Família oficial para software e aplicativos em `assets/brand/logos/systems-and-apps/`

## Regra de logo para produto

- Para software, dashboards, aplicativos e interfaces internas, usar como padrão os SVGs de `assets/brand/logos/systems-and-apps/`.
- O site continua com a família atual de `logos/` até decisão explícita de migração.
- Em produto, preferir assets vetoriais antes de PNG.
- Para fundos claros, usar as variantes `escuro` ou `claro` conforme contraste.
- Para fundos escuros, usar as variantes `claro` ou `branco`.
- Reservar a variante `areia` para acento premium, telas de destaque ou aplicações especiais.

## Mapa rápido de uso de logo

| Contexto | Arquivo recomendado |
| --- | --- |
| App icon, avatar de produto e navegação compacta | `assets/brand/logos/systems-and-apps/rito-monograma-r-escuro.svg` |
| App icon em fundo escuro | `assets/brand/logos/systems-and-apps/rito-monograma-r-claro.svg` |
| Login, splash, onboarding e header principal | `assets/brand/logos/systems-and-apps/rito-assinatura-horizontal-claro.svg` ou `assets/brand/logos/systems-and-apps/rito-assinatura-horizontal-branco.svg` |
| Rodapé de produto e tela "sobre" | `assets/brand/logos/systems-and-apps/rito-wordmark-claro.svg` ou `assets/brand/logos/systems-and-apps/rito-wordmark-branco.svg` |
| Destaques especiais | `assets/brand/logos/systems-and-apps/rito-monograma-r-areia.svg` ou `assets/brand/logos/systems-and-apps/rito-wordmark-areia.svg` |

## Princípios de interface

- Clareza acima de enfeite
- Estrutura editorial, com boa hierarquia
- Poucos efeitos, mais legibilidade
- Bordas suaves e sombras discretas
- Alto respiro entre blocos
- Linguagem visual profissional, sem aparência de template genérico

## Tokens de cor

### Cores de base

| Token | Valor | Uso |
| --- | --- | --- |
| `bg` | `#f4f0e9` | Fundo global, áreas amplas e contexto calmo |
| `surface` | `rgba(255, 251, 245, 0.88)` | Cartões e painéis leves |
| `surface-strong` | `#fffdf9` | Superfícies principais, cards, modais e caixas de leitura |
| `surface-soft` | `#f6f0e7` | Áreas de apoio, faixas e divisões sutis |

### Cores de texto e marca

| Token | Valor | Uso |
| --- | --- | --- |
| `ink` | `#152733` | Texto principal, labels e leitura longa |
| `ink-soft` | `#5d6b72` | Texto secundário, metadados e ajuda |
| `brand` | `#173847` | CTA primário, cabeçalhos, barras e destaque institucional |
| `brand-strong` | `#0d2430` | CTA principal, hero, fundo escuro e ênfase forte |
| `brand-mid` | `#315161` | Estados de apoio, subtítulos e blocos informativos |
| `brand-soft` | `#5F8192` | Destaques discretos e suporte visual |
| `accent` | `#b89163` | Chamadas pontuais, marcas de ênfase e detalhes premium |
| `accent-soft` | `rgba(184, 145, 99, 0.18)` | Fundo de badges e áreas de destaque leve |

### Cores estruturais

| Token | Valor | Uso |
| --- | --- | --- |
| `line` | `rgba(21, 39, 51, 0.08)` | Bordas leves e separadores |
| `line-strong` | `rgba(21, 39, 51, 0.15)` | Bordas de cards, inputs e containers |
| `shadow` | `0 32px 90px rgba(13, 36, 48, 0.05)` | Sombras amplas e suaves, nunca dramáticas |

## Contraste e legibilidade

- `brand` sobre `bg`: contraste alto, adequado para títulos e botões.
- `brand-strong` sobre `surface-strong`: contraste excelente para chamadas principais.
- `ink` sobre `bg` e `surface-strong`: contraste muito alto para leitura longa.
- `ink-soft` sobre `bg`: adequado para texto secundário e metadados.
- `accent` não deve ser usado como cor principal de texto em corpo pequeno, porque o contraste é baixo para leitura contínua.

## Tipografia

### Sistema oficial

- Títulos: `Sora`
- Texto e interface: `Manrope`
- Dados auxiliares, códigos curtos e labels estruturais: `IBM Plex Mono`

### Escala recomendada

| Uso | Fonte | Tamanho sugerido | Peso |
| --- | --- | --- | --- |
| Hero / capa | Sora | 40 a 56 px | 700 a 800 |
| Título de seção | Sora | 28 a 36 px | 700 |
| Título de card | Sora | 18 a 24 px | 600 a 700 |
| Corpo principal | Manrope | 15 a 18 px | 400 a 500 |
| Texto auxiliar | Manrope | 13 a 14 px | 400 a 500 |
| Eyebrow / label | IBM Plex Mono | 11 a 12 px | 400 a 500 |

### Regras tipográficas

- Use títulos curtos e com ritmo visual forte.
- Evite blocos longos em caixa alta.
- Mantenha contraste claro entre título, subtítulo e corpo.
- Não misture fontes fora do sistema oficial sem justificativa.

## Espaçamento e forma

- Prefira cartões com raio médio e borda sutil.
- Mantenha margens generosas entre blocos.
- Não use sombras duras ou profundidade exagerada.
- Dê prioridade a grades simples, com 2 ou 3 colunas no máximo em telas de conteúdo.

## Componentes recomendados

### Botão primário

- Fundo: `brand-strong`
- Texto: branco
- Raio: alto, em cápsula ou arredondado
- Uso: ação principal, envio, orçamento, contato

### Botão secundário

- Fundo: transparente ou `surface-strong`
- Borda: `line-strong`
- Texto: `ink`
- Uso: ação complementar, navegação secundária

### Card padrão

- Fundo: `surface-strong`
- Borda: `line`
- Sombra: muito leve
- Título em `Sora`
- Corpo em `Manrope`

### Badge ou chip

- Fundo: `accent-soft` ou `surface-soft`
- Texto: `ink`
- Uso: status, categoria, destaque curto

### Formulários

- Fundo branco quente ou `surface-strong`
- Borda sutil, visível em foco
- Labels em `ink-soft` ou `ink`
- Ajuda textual curta e objetiva

## Aplicação em software

### Painéis

- Usar fundo claro com blocos bem separados.
- Mostrar números com boa margem e pouco ruído visual.
- Priorizar leitura rápida e hierarquia de informação.

### Sistemas internos

- Evitar densidade excessiva em tabelas e listas.
- Usar linhas leves e alternância discreta de fundo.
- Destacar ações críticas com `brand-strong`, não com cores chamativas.

### Relatórios e telas de conferência

- Cabeçalho editorial com logo e título da seção.
- Blocos de resumo com bordas suaves.
- Destaques pontuais em `accent`, nunca como cor dominante.

## Regras de uso de cor em produto

- Não usar roxo, neon ou gradientes agressivos.
- Não transformar o sistema em uma aparência de startup especulativa.
- Não usar `accent` para sinalizar erro ou alerta principal.
- Não depender de cor para transmitir informação sem texto de apoio.

## Hierarquia visual mínima

1. Contexto da tela
2. Título da tarefa ou página
3. Subtítulo ou explicação curta
4. Ação principal
5. Conteúdo de apoio

## Direção para futuras interfaces

Se um software da RITO precisar de uma identidade própria, ele deve herdar:

- a mesma base cromática do site
- a mesma lógica tipográfica
- o mesmo comportamento de cartões e bordas
- o mesmo tom sóbrio e prático
- a família de logos de `assets/brand/logos/systems-and-apps/` como base visual primária de produto

## Resumo operacional

Esta marca funciona melhor quando parece:

- clara, não fria
- elegante, não luxuosa demais
- técnica, mas acessível
- organizada, mas não rígida
