# Case: Relatório de Vendas e Comissões

> Case real, uso autorizado pelo cliente em 2026-10-31. O cliente aparece de forma anônima ("escritório de representação comercial") até confirmar se o nome pode ser citado.

## Resumo

Um escritório de representação comercial controlava vendas, comissões e repasses a vendedores com um aplicativo Windows e relatórios mensais em planilha e PDF enviados pelas empresas que representa. A RITO criou uma **aplicação web** que importa esses relatórios, calcula as comissões e mostra os números em painéis, acessível de qualquer lugar e com área própria para os vendedores. Em produção desde julho de 2026.

## O problema

- Cada empresa representada envia o relatório de vendas em um formato diferente (Excel ou PDF).
- Comissão da representação e repasse a cada vendedor eram calculados manualmente, com percentuais que mudam ao longo do tempo.
- Clientes com o mesmo nome e códigos diferentes (filiais) se misturavam nos controles.
- Os números ficavam presos a um computador com o aplicativo Windows; vendedores não tinham acesso às próprias comissões.

## A solução

- **Importação de relatórios** em Excel e PDF por empresa representada, com pré-visualização antes de gravar, confirmação em uma única transação (tudo ou nada) e histórico de cada tentativa.
- **Cadastro inteligente** de clientes e filiais pelo código do relatório, sem fundir filiais de mesmo nome, e atribuição de vendedor por cliente com período de vigência.
- **Comissões e repasses** calculados pela data de cada venda, com percentuais versionados, reatribuição de vendedor em lote com auditoria e relatórios de repasse salvos.
- **Painéis de análise**: indicadores com comparação ao período anterior, evolução mensal da comissão por empresa e vendedor, matriz empresa x vendedor e uma visão de clientes ativos, esfriando, inativos e que nunca compraram.
- **Relatório consolidado em Excel** por período, com resumo por vendedor e por empresa.
- **Área do vendedor** com login próprio para consultar comissões e clientes.
- Tecnologia: Next.js, Supabase e Cloudflare Workers.

## O resultado

- Os relatórios das representadas entram no sistema em poucos passos, com conferência antes de gravar.
- Comissões e repasses saem calculados por regra, com histórico de quem mudou o quê.
- A base em julho de 2026 já tinha cerca de 7.900 vendas registradas e segue crescendo a cada importação mensal.
- O aplicativo Windows original continua intacto como contingência.

## Como usar este case

- Prova para a oferta **Painel de Controle** e para projetos sob medida de gestão.
- Site: página de case com o resumo, 3 itens da solução e uma imagem da tela de análises com dados fictícios ou borrados.
- Não divulgar nomes de clientes finais, vendedores, empresas representadas nem valores.
