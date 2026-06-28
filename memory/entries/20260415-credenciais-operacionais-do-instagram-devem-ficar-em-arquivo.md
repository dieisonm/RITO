---
id: "20260415-credenciais-operacionais-do-instagram-devem-ficar-em-arquivo"
project: "RITO"
type: "decision"
status: "active"
title: "Credenciais operacionais do Instagram devem ficar em arquivo local ignorado pelo Git"
summary: "As credenciais do Instagram da RITO devem ser guardadas em um arquivo local privado dentro de `ops/instagram`, com documentação de uso no README da frente e sem replicar senha em arquivos versionados ou na memória persistente."
why: "Isso permite manter o acesso operacional registrado no projeto sem expor credenciais reais no repositório, nos documentos públicos ou na memória persistente."
source: "codex"
created_at: "2026-04-15T22:16:23.013Z"
updated_at: "2026-06-28T12:20:00.000Z"
tags: ["security","instagram","credentials","operations"]
files: [".gitignore","ops/instagram/README.md"]
related_ids: ["20260628-repositorio-foi-enxugado-e-outros-pcs-devem-usar-main-drive-e-caminhos-canonicos"]
issue: ""
pr: ""
commit: ""
---

## Details

Foi adotado o padrão `ops/instagram/instagram-access.local.md` como arquivo local privado para consulta operacional. O caminho foi adicionado ao `.gitignore`, e o `ops/instagram/README.md` passou a orientar que credenciais reais devem permanecer apenas nesse arquivo local e não devem ser repetidas em outros documentos, playbooks ou memória.
