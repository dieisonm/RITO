# Server Ops

Esta pasta documenta como operar a RITO em um computador dedicado, ligado 24/7, para rotinas locais de WhatsApp, prospecção, monitoramento e apoio aos agentes.

## Documentos

- `desktop-server-replication-runbook.md`: passo a passo completo para replicar este ambiente em outro computador.
- `server-pc-bootstrap-checklist.md`: checklist curto de instalação, validação e primeiro dia de operação.
- `server-codex-handoff-prompt.md`: prompt inicial para colar no Codex do computador servidor.

## Princípio

O computador servidor pode executar rotinas locais, mas a fonte de verdade precisa continuar versionada e rastreável. Para isso:

- código, documentos e artefatos operacionais ficam no repositório GitHub da RITO;
- arquivos grandes ficam no Google Drive `RITO_Files` e são rastreados por `assets/drive/asset-manifest.json`;
- memórias duráveis ficam em documentos do projeto e em `memory/entries/`;
- dados sensíveis e sessões locais nunca entram no Git;
- OneDrive via navegador é apoio de bootstrap e contingência, não mecanismo principal de sincronização 24/7.
