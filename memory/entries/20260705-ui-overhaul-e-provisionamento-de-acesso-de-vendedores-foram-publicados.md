---
id: "20260705-ui-overhaul-e-provisionamento-de-acesso-de-vendedores-foram-publicados"
project: "RITO"
type: "decision"
status: "active"
title: "Reforma de UI do Relatorio de Vendas web e provisionamento de acesso de vendedores foram implementados e publicados"
summary: "Sidebar e header do app agora ficam fixos, so o conteudo central rola. Cabecalho trocou 'Console Administrativo' + icone sem sentido por nome/icone da pagina atual; sino leva a clientes sem vendedor; engrenagem abre menu real (alterar senha via modal, sair). Item de navegacao 'Importar' virou 'Comissões'. Corrigida mensagem falsa de 'ultima atualizacao' no dashboard inicial (hora fixa hardcoded). Cadastro de vendedor agora cria login real via Supabase Auth (email + senha), mas o profile e criado com active=false ate a tela de vendedor existir; vendedores antigos podem ser editados para receber acesso retroativamente. Pagina de clientes ganhou update em massa de vendedor e teve dois bugs de UI corrigidos no modal de edicao (campo de empresa vazando do popup, campo de vendedor que parecia dropdown mas aceitava texto livre)."
why: "Usuario pediu uma rodada de pequenas correcoes de UI/UX usando a skill ui-ux-pro-max (instalada mas nao registrada nesta sessao do Claude Code — mesma limitacao de contexto de sessao ja registrada em outras memorias). Ao construir o provisionamento de conta de vendedor, descobriu-se que o vendedor 'OBERDAN' e a mesma pessoa que o unico usuario administrador do sistema — o usuario pediu explicitamente para tratar como a mesma entidade em vez de contas separadas."
source: "claude-code-session"
created_at: "2026-07-06T00:21:20-03:00"
updated_at: "2026-07-06T00:21:20-03:00"
tags: ["relatorio-vendas","ui-ux","supabase-auth","vendedores","clientes","producao"]
files: ["S:/RITO/Projetos/relatorio-vendas-web/src/components/app-shell.tsx", "S:/RITO/Projetos/relatorio-vendas-web/src/components/vendor-management.tsx", "S:/RITO/Projetos/relatorio-vendas-web/src/components/client-management.tsx", "S:/RITO/Projetos/relatorio-vendas-web/src/app/api/vendedores/route.ts", "S:/RITO/Projetos/relatorio-vendas-web/src/app/api/clientes/mass-vendor/route.ts", "S:/RITO/Projetos/relatorio-vendas-web/docs/ui-ux-audit-2026-07-03.md", "S:/RITO/Projetos/relatorio-vendas-web/docs/current-state.md"]
related_ids: ["20260703-fluxo-de-confirmacao-e-gravacao-da-importacao-web-foi-implementado-e-publicado", "20260703-clientes-com-mesmo-nome-e-codigos-diferentes-sao-filiais-distintas-nunca-fundir"]
issue: ""
pr: ""
commit: "681632c,f9bd43b"
---

## Identidade Oberdan = administrador

Verificado por consulta direta ao banco antes de qualquer alteracao: existia
apenas 1 profile no sistema todo (`role='admin', vendor_id=null`, o login
usado durante toda a sessao) e o vendedor "OBERDAN" nao tinha profile
vinculado. Confirmado por `auth.admin.getUserById` que o e-mail real do admin
e' `oberdanvsilva@gmail.com` — mesma pessoa. Vinculado `profiles.vendor_id` do
admin ao id do vendedor OBERDAN e sincronizado `vendors.email`. O campo
`Acesso` (API `/api/vendedores`, tipo `VendorRegistryRow`) agora e
`"nenhum" | "seller" | "admin"` em vez de um booleano — a UI de edicao de
vendedor esconde os campos de senha e mostra "mesma conta do administrador"
quando `Acesso === "admin"`, e o endpoint de provisionamento recusa
explicitamente criar uma segunda conta nesse caso.

## Politica de acesso de vendedor

Toda conta de vendedor criada por `/api/vendedores` (POST ou PUT com senha)
fica com `profiles.active = false` por padrao, independente do campo "Ativo"
do proprio vendedor (que e um conceito de negocio distinto — se ele esta
recebendo atribuicoes, nao se pode logar). So deve virar `true` quando a
tela de vendedor (visao restrita por carteira, pendencia 2 em
`docs/current-state.md`) estiver pronta e um admin decidir ativar.

## Verificacao

Cada peca seguiu o runbook padrao: `npx tsc --noEmit`, `npm run build`,
`npm run lint` limpos a cada rodada, tudo mantido local ate o usuario validar
visualmente, so entao commit + push + `npm ci` + build limpo + deploy +
smoke test (`/login` 200, `/` → 307). Link admin/vendedor verificado por
consulta direta antes e depois da alteracao, nao assumido.
