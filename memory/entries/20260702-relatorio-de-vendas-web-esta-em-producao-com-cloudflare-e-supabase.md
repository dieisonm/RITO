---
id: "20260702-relatorio-de-vendas-web-esta-em-producao-com-cloudflare-e-supabase"
project: "RITO"
type: "decision"
status: "active"
title: "Relatorio de Vendas web esta em producao com Cloudflare e Supabase"
summary: "O app de comissoes da RITO esta ativo em Cloudflare Workers, usa Supabase remoto para autenticacao e dados, suporta CLARAMAX, CAMNPAL e BISCOBOM e tem seu estado operacional consolidado em docs/current-state.md."
why: "O projeto evoluiu rapidamente em outra conversa e a memoria anterior ainda descrevia Vercel, JSON local e Supabase pendente. Este registro evita retomadas com arquitetura, dados ou pendencias incorretas."
source: "codex-session"
created_at: "2026-07-02T11:18:11.4308472-03:00"
updated_at: "2026-07-02T11:18:11.4308472-03:00"
tags: ["relatorio-vendas","cloudflare-workers","supabase","nextjs","comissoes","importacao","producao"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/docs/current-state.md","S:/RITO/Projetos/relatorio-vendas-web/supabase/migrations/202606280001_initial_schema.sql","S:/RITO/Projetos/relatorio-vendas-web/src/lib/sales-parser.ts","S:/RITO/Projetos/relatorio-vendas-web/wrangler.jsonc"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

O app Windows permanece intacto. A versao web vive em `S:/RITO/Projetos/relatorio-vendas-web`, deve receber dependencias e builds somente no disco S, e esta publicada em `https://rito.relatorio-vendas.workers.dev`. A Vercel permanece apenas como copia de contingencia; Cloudflare Workers via OpenNext e o destino canonico de producao. O banco e a autenticacao ficam no projeto Supabase `xnjblqigsvnyuyfklcud`; credenciais nunca devem ser registradas na memoria.

Em 02/07/2026, o banco remoto tinha 3 empresas, 4 vendedores, 1.522 clientes, 1.340 periodos de atribuicao, 12 importacoes, 6.393 transacoes e 1 perfil administrativo. As empresas ativas eram BISCOBOM (`001`), CAMNPAL (`003`) e CLARAMAX (`600`). Vendas preservam empresa, cliente e vendedor historico, e as restricoes `unique (company_id, source_hash)` e `unique (company_id, source_key)` protegem contra arquivos e movimentos duplicados.

CLARAMAX usa Excel; CAMNPAL e BISCOBOM usam PDF. CAMNPAL interpreta os sinais `(+)` e `(-)`. BISCOBOM interpreta as secoes Credito e Debito; debitos viram devolucao negativa. Promotores e IRRF do relatorio BISCOBOM continuam fora do calculo ate decisao do cliente. O usuario seleciona a empresa antes do arquivo e confirma a escolha. Arquivos sao lidos em memoria e nao sao armazenados.

A rota web atual de importacao faz pre-visualizacao, identifica clientes ausentes, duplicatas no arquivo e movimentos ja existentes, mas ainda nao grava o lote confirmado no banco. As cargas ja existentes foram feitas por migracao e scripts administrativos. A proxima etapa funcional e criar a confirmacao/gravyacao transacional da importacao, com resolucao de clientes e vendedores, auditoria e resposta idempotente.

O acesso atual e somente de administrador via Supabase Auth e perfil `admin`. Contas de vendedores e telas restritas por carteira sao fase futura, embora o schema e as politicas RLS ja tenham estrutura inicial para `seller`. O relatorio consolidado XLSX permite periodo, empresa e vendedor, com resumo por vendedor, por empresa e detalhamento por cliente.

Decisoes tecnicas importantes: builds de producao usam `next build --webpack`; Turbopack causou erro de chunks no runtime OpenNext. PDFs sao lidos diretamente com `pdfjs-dist/legacy`. O deploy OpenNext no Windows pode depender de fallback local para falha de symlink em `@opennextjs/aws`; isso nao esta garantido apos reinstalar `node_modules`, portanto deve ser revalidado antes de futuros deploys. O ESLint local tambem apresentou dependencia incompleta em `eslint-plugin-import`, mas TypeScript e build de producao passam.

Codigos de cliente sao texto. Clientes BISCOBOM criados a partir de relatorio sem codigo usam `AUTO-BISCO-####`. A interface antes convertia esses valores para numero e exibia `NaN`; a correcao para preservar texto foi publicada em 02/07/2026 sem alterar os registros do banco.

O documento operacional canonico e `docs/current-state.md`. O schema executavel canonico e `supabase/migrations/202606280001_initial_schema.sql`. Nao usar os antigos planos de Vercel ou schemas em portugues como retrato da producao.
