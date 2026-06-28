---
id: "20260412-publicacao-para-hostinger-foi-enviada-para-a-branch-de-deplo"
project: "RITO"
type: "rationale"
status: "in_progress"
title: "Publicação para Hostinger foi enviada para a branch de deploy, mas o site público ainda serve versão antiga"
summary: "A versão nova do site foi publicada com sucesso na branch `hostinger` em 12 de abril de 2026, mas ao verificar `https://ritosistemas.com` o conteúdo público ainda refletia a versão antiga, indicando que o auto deploy da Hostinger não executou ou ainda não propagou."
why: "Registrar que o repositório já entregou o artefato correto e que o próximo gargalo está no mecanismo de implantação da Hostinger, não no build local."
source: "codex"
created_at: "2026-04-12T22:50:28.610Z"
updated_at: "2026-04-12T22:50:28.610Z"
tags: ["deployment","hostinger","site","branch-hostinger","release"]
files: ["scripts/publish_hostinger_branch.sh","scripts/package_hostinger.sh","release/ritosistemas-hostinger.zip","dist/index.html","dist/pages/contato.html"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

Foi validado que `dist/` contém os arquivos novos, incluindo o número `(51) 99659-9049`, os SVGs em `site/assets/icons/` e o `contact.php` sem erros de sintaxe. Em seguida, `scripts/publish_hostinger_branch.sh` fez push forçado com sucesso para `origin/hostinger` (commit remoto `49f2236`). O conteúdo da branch remota confirma as mudanças. Como fallback, também foi gerado `release/ritosistemas-hostinger.zip`. Apesar disso, a verificação pública mostrou que `https://ritosistemas.com/pages/contato.html` ainda serve a versão antiga com `placeholder aguardando definicao`, sugerindo que o deploy automático da Hostinger não foi disparado, falhou ou ainda não concluiu. Também foi observado que `ritosistemas.com.br` não resolve DNS neste momento.
