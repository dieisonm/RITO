# Pesquisa: automacao Instagram e Meta Ads

Data: `2026-05-12`

## Resumo executivo

A novidade da Meta e util para a RITO, mas ela cobre principalmente **Meta Ads**, nao a operacao organica completa do Instagram.

O melhor caminho e separar a operacao em tres camadas:

1. **Ads via Meta Ads AI Connectors**
   - usar o MCP/CLI oficial da Meta para relatorios, criacao assistida de campanhas, ajustes controlados, diagnostico de Pixel/Dataset e leitura de performance;
   - comecar em modo leitura por causa do historico recente de conta em revisao/desbloqueio.

2. **Instagram organico via Instagram Platform / Graph API**
   - usar API propria para publicar posts, carrosseis, Reels e Stories quando a conta estiver corretamente conectada e autorizada;
   - manter aprovacao humana antes de publicar, especialmente na fase inicial da marca.

3. **Pipeline interno RITO**
   - transformar os ativos ja existentes em uma esteira versionada: pauta, criativo, legenda, UTM, revisao, publicacao, metricas e aprendizado;
   - usar os documentos atuais de `ops/instagram/` e `ops/ai-os/growth/meta-projeto-piloto/` como base.

## O que a Meta lancou

Em 29 de abril de 2026, a Meta anunciou os **Meta Ads AI Connectors** em open beta. O pacote tem duas superficies:

- **Ads MCP Server**: endpoint remoto `https://mcp.facebook.com/ads`, para clientes compativeis com MCP como ChatGPT, Claude e outros.
- **Ads CLI**: ferramenta de linha de comando para agentes locais, scripts e fluxos repetiveis.

As capacidades divulgadas se agrupam em:

- relatorios e insights de performance;
- criacao e edicao de campanhas, conjuntos e anuncios;
- catalogo de produtos;
- diagnostico de sinais, Pixel/Dataset e qualidade de eventos.

Importante: isso e **Meta Ads**, nao um substituto direto para a API organica do Instagram.

## O que podemos automatizar para a RITO

### Meta Ads

Podemos usar para:

- listar contas de anuncio e ativos disponiveis;
- puxar relatorios por campanha, conjunto, anuncio e periodo;
- comparar criativos do Projeto Piloto MEI;
- criar campanhas, conjuntos e anuncios em pausa;
- revisar estrutura, orcamento, publico, UTM e consistencia das copies;
- monitorar anomalias de performance;
- diagnosticar Pixel/Dataset e qualidade de eventos;
- gerar resumo diario/semanal de investimento, CTR, CPC, leads e custo por lead.

Uso recomendado:

- **MCP** para perguntas, auditoria e exploracao.
- **CLI** para rotinas repetiveis e execucao versionada.

Para a campanha atual `Projeto Piloto RITO`, o primeiro fluxo seguro seria:

1. conectar em modo leitura;
2. validar se a conta, pagina e Instagram aparecem corretamente;
3. localizar ou criar o Dataset/Pixel pelo fluxo oficial da Meta;
4. conferir se eventos `PageView`, `ViewContent`, `Lead` e `Contact` estao chegando;
5. so depois montar campanha em pausa usando os ativos existentes em `assets/social/meta-projeto-piloto/`.

### Instagram organico

O MCP de Ads nao e o caminho principal para publicar no feed organico. Para isso, o caminho e Instagram Platform / Graph API.

Podemos automatizar:

- publicacao de imagem unica;
- publicacao de video/Reels;
- carrosseis;
- Stories;
- legenda com hashtags e mencoes;
- alt text em imagens;
- leitura de posts publicados;
- metricas/insights de midia e conta;
- moderacao e resposta de comentarios, dependendo das permissoes;
- webhooks para comentarios, mensagens e eventos suportados.

Limites e cuidados:

- requer conta Instagram profissional e permissoes adequadas;
- os arquivos precisam estar em URL publica ou passar pelo fluxo de upload suportado;
- containers de midia expiram em 24h;
- a conta pode criar ate 400 containers em janela movel de 24h;
- publicar stickers interativos de Story, como enquete ou link sticker, nao e suportado pela API documentada;
- Reels nao entram em carrossel;
- legenda tem limite de 2200 caracteres, 30 hashtags e 20 mencoes.

### Leads e atendimento

O conector oficial de Ads nao resolve sozinho a captura e atendimento do lead depois do clique.

Para a RITO, a cadeia completa deve ser:

- Meta Ads leva trafego para `https://ritosistemas.com/pages/projeto-piloto.html`;
- formulario grava UTM e envia contato;
- WhatsApp/manual ou WAHA cuida do retorno;
- planilha/base interna acompanha status;
- relatorio compara criativo -> lead -> conversa -> proposta.

## Recomendacao de implantacao

### Fase 1: leitura e seguranca

- Nao dar permissao financeira no primeiro momento.
- Usar somente leitura enquanto a conta Meta estiver sensivel.
- Validar se a conta de anuncio, pagina e Instagram estao no Business Manager correto.
- Gerar primeiro relatorio real da campanha, mesmo que manual ou com dados pequenos.

### Fase 2: medicao

- Instalar/configurar Pixel ou Dataset.
- Testar eventos no Events Manager.
- Conferir se o backend da landing preserva `utm_source`, `utm_medium`, `utm_campaign` e `utm_content`.
- Criar um relatorio semanal de campanha com gasto, cliques, CTR, CPC, leads e custo por lead.

### Fase 3: execucao assistida

- Criar campanhas sempre em `PAUSED`.
- Exigir revisao humana antes de ativar qualquer campanha, conjunto ou anuncio.
- Nao alterar orcamento, publico ou criativo mais de uma vez por dia para evitar reset desnecessario da fase de aprendizado.
- Versionar especificacoes de campanha em markdown ou CSV antes da criacao.

### Fase 4: Instagram organico

- Criar uma pequena ferramenta propria para publicar os assets ja aprovados.
- Usar fila local com status: `rascunho`, `aprovado`, `agendado`, `publicado`, `erro`.
- Validar imagem/video antes de chamar a API.
- Salvar ID do post publicado, legenda final, UTM e metricas iniciais.

## O que nao recomendo agora

- Usar conectores comunitarios ou scraping para Instagram/Ads enquanto a conta estiver sensivel.
- Deixar agente com permissao de ativar campanha ou mexer em billing sem aprovacao humana.
- Pedir para a IA "otimizar a campanha" de forma aberta; melhor pedir diagnosticos e propostas de alteracao.
- Fazer edicoes frequentes de budget/audiencia durante as primeiras 48h de campanha.
- Tentar automatizar DMs em massa; risco operacional e de politica e alto.

## Proximo passo pratico

Criar um pequeno pacote de operacao:

- `campaign-spec.yml` para a campanha Projeto Piloto MEI;
- `weekly-report.md` gerado a partir do Ads MCP/CLI;
- `instagram-publishing-queue.csv` para posts organicos;
- checklist de permissao para Business Manager, Instagram profissional, Pixel/Dataset e Page tasks.

## Fontes

- Meta for Business: `https://www.facebook.com/business/news/meta-ads-ai-connectors`
- Meta Business Help Center: `https://www.facebook.com/business/help/1456422242197840`
- Meta Ads MCP/CLI analysis with official source links: `https://mcp.directory/blog/meta-ads-cli-mcp`
- PPC Land coverage: `https://ppc.land/meta-opens-its-ad-system-to-claude-and-chatgpt-with-new-ai-connectors/`
- Meta announcement mirror: `https://www.mediainfoline.com/techno/meta-introduces-meta-ads-ai-connectors-to-help-businesses-manage-ads-from-the-ai-tools-they-already-use`
- Instagram Platform media reference archive: `https://archive.ph/20251231074512/https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media`
