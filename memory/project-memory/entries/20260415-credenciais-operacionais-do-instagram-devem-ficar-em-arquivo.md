---
id: "20260415-credenciais-operacionais-do-instagram-devem-ficar-em-arquivo"
project: "RITO"
type: "decision"
status: "active"
title: "Credenciais operacionais do Instagram devem ficar em arquivo local ignorado pelo Git"
summary: "As credenciais do Instagram da RITO passaram a ser guardadas em um arquivo local privado dentro de `operations/instagram`, com documentação de uso no README da frente e sem replicar senha em arquivos versionados ou na memória persistente."
why: "Isso permite manter o acesso operacional registrado no projeto sem expor credenciais reais no repositório, nos documentos públicos ou na memória persistente."
source: "codex"
created_at: "2026-04-15T22:16:23.013Z"
updated_at: "2026-04-15T22:16:23.013Z"
tags: ["security","instagram","credentials","operations"]
files: [".gitignore","operations/instagram/README.md"]
related_ids: []
issue: ""
pr: ""
commit: ""
---

## Details

Foi adotado o padrão `operations/instagram/instagram-access.local.md` como arquivo local privado para consulta operacional. O caminho foi adicionado ao `.gitignore`, e o `operations/instagram/README.md` passou a orientar que credenciais reais devem permanecer apenas nesse arquivo local e não devem ser repetidas em outros documentos, playbooks ou memória.
