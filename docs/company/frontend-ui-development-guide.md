# Guia de Desenvolvimento UI e Front-end da RITO

## Objetivo

Definir boas práticas para manter o site da RITO e construir interfaces futuras para clientes com qualidade visual, consistência, responsividade e validação real no navegador.

Fontes oficiais consultadas:

- OpenAI Codex Use Case, Make granular UI changes: `https://developers.openai.com/codex/use-cases/make-granular-ui-changes`
- OpenAI Codex Use Case, Build responsive front-end designs: `https://developers.openai.com/codex/use-cases/frontend-designs`

## Dois modos de trabalho

### 1. Ajuste granular de UI

Usar quando a estrutura já existe e queremos polir algo específico.

Exemplos:

- espaçamento
- alinhamento
- cor
- responsividade pontual
- estado de botão, card, formulário ou menu
- copy curta em um componente já existente

Regra:

- uma nota visual por vez;
- menor patch defensável;
- preservar comportamento, dados, rota e estrutura;
- reutilizar componentes, tokens, ícones e padrões existentes;
- verificar a rota no navegador real antes de concluir.

### 2. Construção de UI responsiva

Usar quando vamos criar tela, fluxo, landing, dashboard ou sistema de cliente.

Exemplos:

- nova landing page
- tela de login
- dashboard
- lista de pedidos
- formulário operacional
- painel interno
- app simples para cliente

Regra:

- começar por screenshot, referência visual, wireframe ou brief claro;
- declarar desktop, mobile e estados importantes;
- traduzir referência para o design system real do projeto;
- não inventar um sistema paralelo;
- validar visual e comportamento em navegador, desktop e mobile.

## Checklist antes de implementar

- A rota ou tela alvo está definida?
- O objetivo de negócio da tela está claro?
- Existe referência visual, screenshot, wireframe ou descrição suficiente?
- A superfície está clara: site institucional, landing, sistema interno, app ou dashboard?
- O viewport principal está definido: desktop, mobile ou ambos?
- Os estados estão definidos: vazio, carregando, erro, sucesso, hover, ativo ou selecionado?
- O design system do projeto foi identificado?
- Componentes, tokens, ícones, fontes e padrões existentes foram localizados?
- Existe critério de pronto visual?
- Existe forma de validar em navegador real?

## Prompt padrão para ajuste granular

```text
Faça este ajuste granular de UI na aplicação existente:
[descrever exatamente espaçamento, alinhamento, cor, copy, responsividade ou estado do componente]

Contexto:
- rota:
- viewport:
- componente/bloco:
- comportamento que deve permanecer igual:

Restrições:
- alterar apenas os arquivos necessários para este ajuste;
- reutilizar componentes, tokens, ícones e padrões existentes;
- manter comportamento, dados, rotas e fluxo inalterados;
- fazer o menor patch defensável;
- verificar visualmente no navegador antes de concluir.

Ao finalizar:
- listar arquivos alterados;
- descrever a verificação visual feita;
- parar após este ajuste.
```

## Prompt padrão para nova UI responsiva

```text
Implemente esta UI no projeto atual usando as referências abaixo como fonte de verdade:
[screenshots, wireframe, imagem, nota ou brief]

Requisitos:
- reutilizar o design system, componentes, tokens e padrões existentes;
- traduzir a referência para as utilities e componentes reais do repo;
- corresponder de perto a espaçamento, layout, hierarquia, contraste e comportamento responsivo;
- respeitar rotas, estado, dados e padrões de fetch do projeto;
- funcionar em desktop e mobile;
- se algo estiver ambíguo, escolher a solução mais simples que preserve a direção visual e registrar a premissa.

Validação:
- abrir a tela no navegador;
- verificar desktop e mobile;
- comparar com as referências visuais;
- iterar até ficar visualmente coerente;
- registrar arquivos alterados e checks executados.
```

## Design system e tokens

Antes de criar UI, identificar:

- cores oficiais;
- escala tipográfica;
- espaçamento;
- botões;
- inputs;
- cards;
- ícones;
- grid/layout;
- breakpoints;
- padrões de navegação;
- componentes canônicos.

Se o projeto ainda não tiver design system, criar um mínimo:

- tokens de cor;
- escala de fonte;
- escala de espaçamento;
- componentes base para botão, input, card e alerta;
- regras de responsividade.

## Critérios visuais da RITO

Para o site da RITO:

- manter a linguagem boutique/premium já estabelecida;
- evitar mudanças grandes disfarçadas de ajuste pequeno;
- preservar paleta, tipografia e hierarquia visual;
- testar sempre home, landing e contato quando mexer em estilos globais;
- publicar apenas via Git/Hostinger depois de validação local.

Para sistemas de clientes:

- começar simples, claro e responsivo;
- priorizar operação real do usuário, não estética isolada;
- usar UI limpa, com hierarquia forte e baixa fricção;
- documentar estados vazios, erros e sucesso;
- validar fluxo completo, não só tela bonita.

## Validação obrigatória

### Para site estático da RITO

- rodar build/validação quando houver mudança de site;
- abrir a rota afetada em navegador;
- testar mobile e desktop;
- verificar CTA, menu, formulário e WhatsApp quando impactados;
- validar `deploy-info` depois da publicação.

### Para sistemas e apps

- rodar testes disponíveis;
- abrir a aplicação no navegador;
- testar desktop e mobile;
- testar estados principais;
- conferir acessibilidade básica: foco, contraste, labels e navegação por teclado quando aplicável;
- registrar evidência de validação.

## Regras de parada

Parar e pedir alinhamento quando:

- a alteração granular começar a virar redesign;
- a referência visual conflitar com o design system;
- faltar rota, viewport ou objetivo;
- houver risco de quebrar fluxo, dados ou navegação;
- o visual ficar bom, mas o comportamento quebrar;
- a implementação exigir decisão de produto, preço, legal ou marca.

## Definition of Done

Uma entrega UI/front-end só está pronta quando:

- escopo foi mantido;
- arquivos alterados são os mínimos necessários;
- componentes e tokens existentes foram reutilizados;
- desktop e mobile foram verificados;
- comportamento principal continua funcionando;
- divergências ou premissas foram registradas;
- screenshots/referências foram consideradas;
- revisão humana foi indicada quando houver publicação externa ou entrega para cliente.
