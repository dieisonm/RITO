# Runbook de Replicação do PC Servidor RITO

Data de criação: 2026-05-17

## Objetivo

Replicar a operação da RITO em um computador de mesa ligado 24/7, funcionando como servidor local para:

- manter o WhatsApp Business da RITO conectado via WAHA;
- escutar mensagens recebidas e salvar eventos para atendimento;
- preparar respostas básicas com agente, inicialmente com aprovação humana;
- rodar rotinas de prospecção e organização de contatos;
- manter arquivos, decisões e memória sincronizados com o ambiente principal.

Este runbook foi escrito para o Codex daquele computador seguir sem depender de contexto da conversa original.

## Decisão de arquitetura

A sincronização principal deve ser GitHub, não OneDrive via navegador. Arquivos grandes devem ficar no Google Drive e ser referenciados por manifesto versionado no Git.

Motivo:

- GitHub permite histórico, branch, revisão, rollback e comparação de mudanças;
- Google Drive é melhor para mídia pesada, como imagens geradas, vídeos, PDFs, exports e fontes criativas;
- OneDrive corporativo via browser é útil para baixar arquivos, mas é frágil como mecanismo automático 24/7;
- automações de browser em OneDrive podem quebrar por MFA, sessão expirada, políticas corporativas ou layout da página;
- o servidor precisa ser previsível, especialmente para WhatsApp, atendimento e prospecção.

Uso recomendado:

- GitHub: fonte de verdade para código, docs, prompts, templates, site, scripts, memória versionada, manifestos e artefatos operacionais não sensíveis.
- Google Drive: fonte de verdade para mídia pesada em `RITO/assets`.
- OneDrive navegador: bootstrap manual, baixar pastas auxiliares e contingência quando algo ainda não estiver versionado.
- `memory/project-memory`: espelho versionável das memórias duráveis do projeto.
- `project-memory` MCP: interface opcional para busca/escrita local, reconstruível a partir dos Markdown versionados.

## Estado importante do ambiente atual

No momento em que este documento foi criado, o projeto local tinha muitos arquivos modificados e não versionados. Isso significa que um clone puro do GitHub pode não reproduzir exatamente a máquina atual até que esses arquivos sejam commitados/pushados ou transferidos manualmente.

Antes de configurar o PC servidor, o operador principal deve decidir:

- quais arquivos locais entram no Git;
- quais arquivos pesados entram no Google Drive e ficam só no manifesto;
- quais arquivos ficam privados;
- qual branch será a base operacional do servidor;
- se há alguma contingência manual via OneDrive ou se o clone Git já é suficiente.

Regra prática:

- se um arquivo é necessário para o servidor operar e não contém segredo, ele deve ir para o Git;
- se é mídia pesada, deve ir para o Google Drive e ser registrado no manifesto;
- se contém segredo, sessão, token, senha, credencial, inbox bruto ou dados sensíveis, ele deve ficar local e ser copiado/configurado manualmente.

## Fontes de verdade

### Repositório da RITO

```text
https://github.com/dieisonm/RITO.git
```

Contém:

- site;
- docs da empresa;
- prompts e playbooks dos agentes;
- scripts de deploy, WhatsApp, e-mail e prospecção;
- templates;
- assets públicos leves necessários para site;
- manifestos dos assets pesados;
- memórias do projeto em Markdown;
- base operacional sem dados sensíveis.

### Google Drive de assets

Pasta raiz operacional:

```text
Nome: RITO/assets
ID: 1t_ZfqPZl_-hhlzgPF3Lbnf3nOYPdZz3L
URL: https://drive.google.com/drive/folders/1t_ZfqPZl_-hhlzgPF3Lbnf3nOYPdZz3L
```

Manifesto versionado:

```text
assets/drive/asset-manifest.json
```

Rotina:

```bash
python3 scripts/drive_assets.py scan --write-manifest --write-queue
python3 scripts/drive_assets.py check
python3 scripts/drive_assets.py upload
```

Depois de subir manualmente um arquivo grande ao Drive, registrar:

```bash
python3 scripts/drive_assets.py register \
  --path assets/social/campanha/arte.png \
  --drive-id GOOGLE_DRIVE_FILE_ID \
  --drive-url https://drive.google.com/file/d/GOOGLE_DRIVE_FILE_ID/view
```

### Pasta Automations

No Mac principal, a raiz atual é:

```text
/Users/I858224/Library/CloudStorage/OneDrive-SAPSE/Procurement/Automations
```

Pastas auxiliares relevantes:

```text
Automations/RITO
Automations/skills
Automations/AGENTS.md
```

No PC servidor, não é obrigatório usar o mesmo caminho. O importante é manter uma estrutura equivalente:

```text
Automations/
├── RITO/
├── skills/
└── AGENTS.md
```

O MCP `project-memory` pode ser instalado depois se necessário, mas o espelho versionado em `RITO/memory/entries/` deve ser suficiente para manter Mac e servidor alinhados.

## Mapa do projeto RITO

### `site/`

Fonte do site institucional publicado.

Uso:

- alterações de conteúdo e UI do site;
- páginas como home e projeto piloto;
- assets públicos servidos no domínio.

Trava:

- não publicar alteração sem validação humana.

### `scripts/`

Scripts operacionais.

Principais:

- `build_dist.sh`: gera `dist/`;
- `publish_hostinger_branch.sh`: publica branch `hostinger`;
- `verify_live_site.py`: verifica site no ar;
- `send_outbound_emails.php`: envia e-mails outbound;
- `read_hostinger_inbox.py`: lê inbox do e-mail Hostinger;
- `waha_local.sh`: sobe/para WAHA via Docker Compose;
- `waha_webhook_local.sh`: controla webhook local fora do Compose;
- `configure_waha_webhook.py`: configura webhook no WAHA;
- `whatsapp_waha_outbound.py`: sessão, teste, envio, resposta e visto via WAHA;
- `whatsapp_waha_webhook.py`: receiver local de eventos WAHA;
- `whatsapp_waha_common.py`: funções comuns de WAHA.

### `ops/ai-os/`

Sistema operacional interno dos agentes.

Uso:

- inbox de demandas;
- leads;
- propostas;
- clientes;
- conteúdo;
- growth;
- suporte;
- reviews;
- templates;
- conhecimento aprovado.

### `ops/ai-os/whatsapp/`

Operação local de WhatsApp.

Uso:

- documentação WAHA;
- configuração Docker;
- webhook;
- filas;
- logs locais.

Dados versionáveis:

- `README.md`;
- `waha/docker-compose.yml`;
- `waha/.env.example`;
- scripts.

Dados não versionáveis:

- `waha/.env`;
- `waha/.sessions/`;
- `inbox/raw/*.jsonl`;
- `inbox/conversations/*.jsonl`;
- `inbox/pending/*.jsonl`;
- `runs/*.jsonl`;
- `runtime/`.

### `ops/ai-os/growth/prospecting/`

Base de prospecção territorial.

Uso:

- estratégia por território;
- batches;
- bases de busca;
- registros de empresas;
- hipóteses de oferta;
- status de contato.

Regra crítica:

- o agente não deve acessar Instagram;
- se encontrar referência a Instagram, deve registrar como pendente de verificação manual.

### `docs/agents/agent-system/`

Arquitetura de agentes.

Leitura obrigatória no servidor:

- `operating-model.md`;
- `agent-directory.md`;
- `memory-protocol.md`;
- `handoff-rules.md`;
- `prompts/`;
- `playbooks/phase-1/atendimento-relacionamento.md`;
- `playbooks/phase-1/prospeccao-inteligencia-comercial.md`;
- `playbooks/phase-1/disparo-outbound.md`;
- `playbooks/phase-1/growth-aquisicao.md`;
- `playbooks/phase-1/revisor.md`.

### `docs/ops/server/`

Documentação específica do PC servidor.

Uso:

- bootstrap;
- rotinas 24/7;
- handoff para Codex;
- operação e sincronização.

### `assets/deliverables/social-assets/`

Peças e imagens geradas para campanhas e redes sociais.

Regra:

- imagens, vídeos, PDFs e exports grandes devem ficar no Google Drive;
- o Git deve guardar `README.md`, prompts, manifestos e metadados;
- assets leves usados diretamente pelo site ficam em `site/`.

### `assets/drive/`

Ponte entre GitHub e Google Drive.

Uso:

- `asset-manifest.json`: lista oficial de arquivos grandes;
- `README.md`: política e fluxo;
- `scripts/drive_assets.py`: scanner, validação e registro.

### `memory/`

Memória versionada do projeto RITO.

Uso:

- `entries/*.md`: decisões, bugs, correções e racional durável;
- deve ser lida pelo Mac principal e pelo PC servidor;
- não guardar segredos, dados pessoais sensíveis ou conversas brutas.

### `dist/` e `release/`

Artefatos gerados.

Regra:

- não são fonte de verdade;
- recriar com scripts;
- não usar como base para edição.

## Instalações necessárias no PC servidor

### Obrigatórias

- Codex.
- Git.
- GitHub CLI (`gh`).
- Python 3.12 ou superior.
- PHP CLI.
- Node.js LTS.
- Docker Desktop ou Docker Engine.
- Docker Compose.
- `curl`.
- Chrome ou Chromium.

### Plugins e capacidades do Codex

Essenciais:

- GitHub: trabalhar com repositório, branches, PRs e histórico.
- Browser: validar páginas locais, dashboards e localhost.

Recomendados:

- Canva: se o servidor também apoiar produção de social/design.
- Google Drive: recomendado para consultar metadados e assets pesados. O conector atual valida/lista arquivos, mas upload binário de PNG/JPG/PDF pode exigir navegador, Drive Desktop ou `rclone`.
- Documents, Spreadsheets e Presentations: se forem usados documentos, planilhas ou apresentações locais.

Sistema de skills:

- skills nativas do Codex, como `imagegen` e `openai-docs`, vêm pelo ambiente do Codex;
- skills customizadas da RITO ficam em `Automations/skills`;
- não copiar manualmente cache interno de plugins de `~/.codex/plugins/cache`; instalar plugins pelo próprio Codex quando necessário.

Skills customizadas relevantes:

```text
Automations/skills/frontend-design/SKILL.md
Automations/skills/creating-ise-modules/SKILL.md
Automations/skills/aeval-run-eval/SKILL.md
Automations/skills/aeval-set-up/SKILL.md
Automations/skills/sap-*/SKILL.md
```

Para RITO, a skill mais importante no dia a dia tende a ser:

```text
Automations/skills/frontend-design/SKILL.md
```

## Instalação por sistema operacional

### Windows recomendado

Usar Windows com WSL2 e Docker Desktop.

Instalar:

```powershell
winget install Git.Git
winget install GitHub.cli
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
winget install Docker.DockerDesktop
wsl --install -d Ubuntu
```

Depois reiniciar, abrir Docker Desktop e habilitar integração com WSL.

Clonar o repositório dentro do filesystem do WSL, não dentro de uma pasta Windows montada, para evitar lentidão e problemas de permissão.

Exemplo:

```bash
mkdir -p ~/Automations
cd ~/Automations
git clone https://github.com/dieisonm/RITO.git
```

### macOS recomendado

Instalar Homebrew, depois:

```bash
brew install git gh python php node docker-compose colima
```

Se usar Colima:

```bash
colima start
```

Também pode usar Docker Desktop.

### Linux recomendado

Instalar pelo gerenciador da distro:

```bash
sudo apt update
sudo apt install -y git gh python3 php-cli nodejs npm curl docker.io docker-compose-plugin
sudo usermod -aG docker "$USER"
```

Depois sair e entrar novamente na sessão.

## Bootstrap do projeto

### Caminho preferencial: GitHub

```bash
mkdir -p ~/Automations
cd ~/Automations
git clone https://github.com/dieisonm/RITO.git
cd RITO
git status --short
```

Escolher branch operacional:

```bash
git branch --show-current
git fetch origin
```

Se o servidor for operar direto na branch principal, usar a branch definida pelo operador. Se ele for executar mudanças próprias, criar branch de trabalho:

```bash
git switch -c server/YYYY-MM-DD-operacao
```

### Caminho de contingência: OneDrive navegador

Usar apenas quando o GitHub ainda não tiver todos os arquivos necessários e quando o Google Drive não for o local correto para mídia pesada.

Passos:

1. Abrir OneDrive pelo navegador.
2. Entrar na raiz `Automations`.
3. Baixar como ZIP as pastas necessárias.
4. Descompactar localmente.
5. Comparar com o clone Git.
6. Trazer para o Git apenas arquivos não sensíveis.

Não tentar manter uma automação de leitura/escrita no OneDrive pelo navegador como mecanismo 24/7. Isso deve ser tratado como contingência manual.

## Sincronização de assets grandes

Arquivos pesados não devem entrar no Git.

Fluxo padrão:

1. O asset nasce localmente em `assets/brand/logos/`, `assets/business-kit/` ou `assets/social/`, ou chega por download e é movido para um desses caminhos canônicos.
2. O scanner atualiza o manifesto e gera fila:

```bash
python3 scripts/drive_assets.py scan --write-manifest --write-queue
```

3. O operador sobe os arquivos pendentes para `RITO/assets` no Google Drive.
4. Se o upload foi feito via `scripts/drive_assets.py upload`, o manifesto é atualizado automaticamente.
5. Se o upload foi manual, o Codex registra `drive_id` e URL no manifesto:

```bash
python3 scripts/drive_assets.py register \
  --path CAMINHO_RELATIVO \
  --drive-id GOOGLE_DRIVE_FILE_ID \
  --drive-url GOOGLE_DRIVE_URL
```

6. O manifesto é commitado e enviado ao GitHub.

Regra:

- se o servidor precisa usar um asset, ele lê o manifesto e baixa/abre pelo Drive;
- se o asset precisa ir para o site, criar uma versão otimizada e leve em `site/`;
- PNG/JPG/PDF/DOCX/XLSX/PPTX pesados em `assets/brand/logos/`, `assets/business-kit/` e `assets/social/` ficam fora do Git e devem ser replicados no Drive.

## Sincronização de arquivos

### Regra principal

Tudo que o servidor produzir e for útil para a operação deve voltar pelo Git.

Fluxo no início de cada sessão:

```bash
git status --short
git pull --rebase
```

Fluxo no fim de cada entrega:

```bash
git status --short
git add <arquivos>
git commit -m "docs: registrar operação do servidor"
git push
```

Se o servidor estiver em branch própria:

```bash
git push -u origin server/YYYY-MM-DD-operacao
```

### Regra contra conflito

Não editar o mesmo arquivo em dois computadores ao mesmo tempo.

Para rotinas 24/7:

- servidor escreve logs e resumos em arquivos próprios;
- Mac principal edita site, estratégia e documentação mais sensível;
- quando o servidor precisar mudar arquivo importante, criar branch e avisar.

### Onde registrar logs duráveis

Criar, quando necessário:

```text
ops/ai-os/reviews/YYYY-MM-DD-server-review.md
ops/ai-os/support/YYYY-MM-DD-whatsapp-summary.md
ops/ai-os/growth/YYYY-MM-DD-prospecting-summary.md
docs/ops/server/YYYY-MM-DD-server-ops-log.md
```

Evitar commitar logs brutos com dados pessoais. Preferir resumos operacionais.

## Sincronização de memória

Existem três camadas.

### Camada 1: memória em arquivos do projeto

É a camada mais simples e confiável.

Registrar decisões duráveis em:

```text
docs/
ops/ai-os/
```

Exemplos:

- decisão de canal;
- aprendizado de campanha;
- ajuste de playbook;
- mudança de regra operacional;
- bug e correção de deploy;
- aprendizado de WhatsApp.

### Camada 2: memória versionada em `memory/entries`

Esta é a fonte de verdade recomendada para Mac e servidor.

```text
memory/entries/*.md
```

Regra:

- commit/push após novas memórias duráveis;
- pull antes de trabalhar;
- não registrar dados sensíveis.

### Camada 3: `project-memory` MCP

O MCP de memória pode existir fora do repositório RITO como interface local:

```text
Automations/project-memory
Automations/project-memory-mcp
```

Instalação:

```bash
cd ~/Automations
./project-memory-mcp/scripts/install-codex-mcp.sh
./project-memory-mcp/scripts/project-memory-global.sh recent --project RITO
```

Se copiar a memória por pacote:

```bash
./project-memory-mcp/scripts/unpack-project-memory.sh RITO-project-memory-YYYYMMDD-HHMMSS.tar.gz
./project-memory-mcp/scripts/project-memory-global.sh rebuild --project RITO
```

Empacotar no Mac principal:

```bash
cd ~/Automations
./project-memory-mcp/scripts/pack-project-memory.sh RITO
```

Fonte original do MCP:

```text
project-memory/data/projects/RITO/entries/*.md
```

Regra:

- se o MCP não estiver disponível, não parar a operação;
- registrar a decisão em docs ou em `memory/entries/`;
- sincronizar ou reconstruir o MCP depois.

## Configuração de segredos

Nunca commitar:

```text
rito-smtp.php
ops/ai-os/whatsapp/waha/.env
ops/ai-os/whatsapp/waha/.sessions/
ops/ai-os/whatsapp/.session/
ops/instagram/instagram-access.local.md
ops/web/registrobr-access.local.md
ops/ai-os/whatsapp/inbox/raw/*.jsonl
ops/ai-os/whatsapp/inbox/conversations/*.jsonl
ops/ai-os/whatsapp/inbox/pending/*.jsonl
ops/ai-os/whatsapp/runs/*.jsonl
ops/ai-os/whatsapp/runtime/
.colima/
```

Credenciais necessárias no servidor:

- GitHub;
- Codex/OpenAI;
- WAHA API key local;
- WAHA dashboard user/pass;
- WhatsApp Business da RITO via QR Code;
- SMTP/IMAP da Hostinger se o servidor for ler/enviar e-mail;
- acesso GitHub autorizado para sincronizar operacao e codigo.

Guardar em:

- gerenciador de senhas;
- arquivo `.env` local ignorado pelo Git;
- variáveis de ambiente locais.

## WAHA e WhatsApp 24/7

### Arquivos relevantes

```text
ops/ai-os/whatsapp/README.md
ops/ai-os/whatsapp/waha/docker-compose.yml
ops/ai-os/whatsapp/waha/.env.example
scripts/waha_local.sh
scripts/configure_waha_webhook.py
scripts/whatsapp_waha_outbound.py
scripts/whatsapp_waha_webhook.py
scripts/whatsapp_waha_common.py
```

### Criar `.env`

```bash
cp ops/ai-os/whatsapp/waha/.env.example ops/ai-os/whatsapp/waha/.env
```

Editar:

```text
WAHA_IMAGE=
WAHA_API_KEY=
WAHA_DASHBOARD_USERNAME=
WAHA_DASHBOARD_PASSWORD=
WHATSAPP_SWAGGER_USERNAME=
WHATSAPP_SWAGGER_PASSWORD=
RITO_WAHA_WEBHOOK_SECRET=
RITO_WAHA_WEBHOOK_TOKEN=
```

Imagem WAHA:

- Apple Silicon: `devlikeapro/waha:arm`
- Windows/Linux Intel ou AMD: usar imagem compatível com x86, normalmente `devlikeapro/waha:latest`

Engine:

```text
WHATSAPP_DEFAULT_ENGINE=WEBJS
```

Motivo:

- na operação real da RITO, `NOWEB` enviou mensagens mas deixou itens em `PENDING`;
- `WEBJS` é mais pesado, mas foi o caminho confiável para envio.

### Subir stack

```bash
bash scripts/waha_local.sh up -d
```

Ver logs:

```bash
bash scripts/waha_local.sh logs -f
```

Parar:

```bash
bash scripts/waha_local.sh down
```

Painel:

```text
http://127.0.0.1:3000/
```

Webhook health:

```text
http://127.0.0.1:8787/health
```

### Iniciar sessão

```bash
python3 scripts/whatsapp_waha_outbound.py session-start
python3 scripts/whatsapp_waha_outbound.py session-status
```

Escanear QR Code pelo WhatsApp Business da RITO.

Depois configurar webhook:

```bash
python3 scripts/configure_waha_webhook.py
```

### Teste seguro

Somente com aprovação humana, enviar para número próprio:

```bash
python3 scripts/whatsapp_waha_outbound.py send-test \
  --to 5551998111678 \
  --message "Teste técnico RITO via WAHA no PC servidor." \
  --apply
```

Confirmar:

- mensagem recebida no número correto;
- status da sessão continua `WORKING`;
- webhook gravou evento local;
- não houve fallback por browser.

### Onde as respostas entram

```text
ops/ai-os/whatsapp/inbox/raw/
ops/ai-os/whatsapp/inbox/conversations/
ops/ai-os/whatsapp/inbox/pending/pending-replies.jsonl
```

Esses dados são locais e ignorados pelo Git. Para sincronizar aprendizado, criar resumo sem dados sensíveis em `ops/ai-os/support/` ou `ops/ai-os/reviews/`.

## Atendimento por agente

Fase atual recomendada:

- webhook recebe mensagens;
- agente lê pendências;
- agente sugere resposta;
- humano aprova envio;
- envio é feito via WAHA;
- resumo é registrado.

Não ativar resposta automática completa ainda.

Motivo:

- a RITO ainda está validando tom e oferta;
- uma resposta errada pode gerar percepção ruim;
- WhatsApp é canal sensível;
- o sistema ainda precisa de regras de segurança e fallback.

Fluxo futuro:

1. Classificar mensagem recebida.
2. Identificar se é autoresposta, lead humano, opt-out, dúvida ou suporte.
3. Gerar resposta curta.
4. Validar se a resposta pode ser automática.
5. Enviar automaticamente apenas casos de baixo risco.
6. Escalar para humano em preço, proposta, contrato, escopo, reclamação ou dúvida ambígua.

## Prospecção no PC servidor

O servidor pode rodar descoberta e organização de empresas, mas precisa respeitar os playbooks.

Leitura obrigatória:

```text
docs/agents/agent-system/playbooks/phase-1/prospeccao-inteligencia-comercial.md
docs/agents/agent-system/playbooks/phase-1/disparo-outbound.md
ops/ai-os/growth/prospecting/README.md
ops/ai-os/growth/prospecting/outbound-automation-architecture.md
```

Regras:

- não acessar Instagram;
- usar fontes web públicas, sites oficiais, diretórios públicos e páginas de contato;
- registrar fonte de cada dado;
- marcar Instagram apenas como referência pendente de verificação manual;
- separar descoberta de disparo;
- não transformar hipótese em fato;
- salvar 4 frentes plausíveis de oferta;
- enviar apenas após revisão/aprovação humana.

Pasta territorial atual:

```text
ops/ai-os/growth/prospecting/territories/novo-hamburgo-rs/
```

Cadência recomendada:

- descoberta: 25 a 40 empresas por lote;
- envio: lotes menores;
- refresh: semanal ou quinzenal.

## Disparo outbound

O servidor pode preparar e executar disparos aprovados, mas não decidir sozinho uma campanha.

Travas:

- lote precisa estar aprovado;
- template precisa estar aprovado;
- canal precisa ser validado no momento do envio;
- WhatsApp precisa resolver `chatId` real pelo WAHA;
- se o canal falhar, aplicar fallback;
- registrar telemetria.

WhatsApp:

```bash
python3 scripts/whatsapp_waha_outbound.py send-batch --dry-run
python3 scripts/whatsapp_waha_outbound.py send-batch --apply --throttle-seconds 45
```

E-mail:

```bash
php scripts/send_outbound_emails.php
```

Inbox Hostinger:

```bash
python3 scripts/read_hostinger_inbox.py
```

Observação:

- scripts de e-mail dependem de configuração local de SMTP/IMAP;
- não commitar credenciais;
- monitorar bounces e respostas depois do envio.

## Deploy do site

O PC servidor pode validar, mas não deve publicar sem aprovação.

Comandos úteis:

```bash
bash scripts/build_dist.sh
python3 scripts/validate_dist.py
bash scripts/publish_hostinger_branch.sh
```

Fluxo completo:

```bash
bash scripts/publish_hostinger_branch.sh
```

Regra:

- preferir Git Deployment da Hostinger pela branch `hostinger`;
- nao usar publicacao direta na hospedagem como rotina;
- confirmar `https://ritosistemas.com/deploy-info.json` após deploy.

## Serviços 24/7

### Processos mínimos

- Docker/WAHA;
- webhook WAHA;
- job de monitoramento de inbox;
- job de prospecção, quando aprovado;
- job de leitura de e-mail, quando configurado.

### Windows

Usar Agendador de Tarefas para iniciar:

- Docker Desktop no login;
- stack WAHA;
- script de monitoramento, se existir.

Recomendação:

- começar com acionamento manual supervisionado;
- só depois transformar em tarefa agendada.

### macOS

Usar `launchd` ou iniciar manualmente com sessão persistente.

### Linux

Usar `systemd` para Docker Compose e workers.

## Rotina diária do PC servidor

Ao iniciar:

```bash
git status --short
git pull --rebase
bash scripts/waha_local.sh up -d
python3 scripts/whatsapp_waha_outbound.py session-status
curl -s http://127.0.0.1:8787/health
```

Durante o dia:

- monitorar pendências do WhatsApp;
- verificar bounces de e-mail;
- preparar lotes, se aprovado;
- registrar resumos;
- não enviar sem aprovação.

Ao finalizar entrega:

```bash
git status --short
git add <arquivos-aprovados>
git commit -m "ops: registrar atualização do servidor"
git push
```

## Travas de segurança

Proibido:

- acessar ou automatizar Instagram;
- fazer scraping de Meta/Instagram;
- disparar lote frio sem aprovação humana;
- responder automaticamente conversas reais sem regra aprovada;
- commitar credenciais;
- commitar sessão WAHA;
- commitar inbox bruto do WhatsApp;
- alterar preço, proposta, contrato ou promessa comercial sem validação;
- publicar site sem validação;
- rodar campanha paga sem validação.

Escalar para humano:

- lead interessado;
- pedido de preço;
- dúvida sobre escopo;
- reclamação;
- opt-out;
- conversa ambígua;
- negócio regulado ou sensível;
- contato com dado pessoal exposto;
- qualquer risco reputacional.

## Validação final da instalação

O setup só está pronto quando todos os itens abaixo estiverem verdadeiros:

- `git pull` e `git push` funcionam;
- Codex abre o projeto e lê os docs;
- skills customizadas estão acessíveis ou documentadas;
- project-memory funciona ou existe fallback em docs;
- Docker sobe;
- WAHA abre em `http://127.0.0.1:3000/`;
- sessão WhatsApp está conectada;
- webhook responde em `http://127.0.0.1:8787/health`;
- mensagem de teste para número próprio chega corretamente;
- evento de resposta aparece no inbox local;
- nenhum segredo aparece em `git status`;
- o Mac principal consegue receber uma alteração feita pelo servidor via Git.

## Procedimento de emergência

Se algo estranho acontecer:

1. parar envios;
2. parar workers agendados;
3. manter WAHA ligado apenas se precisar preservar sessão;
4. salvar logs locais;
5. registrar resumo do incidente;
6. avisar operador humano;
7. só retomar depois de entender causa.

Comandos:

```bash
bash scripts/waha_local.sh down
bash scripts/waha_webhook_local.sh stop
git status --short
```

Se houver risco de mensagem errada:

- não apagar logs;
- não tentar corrigir enviando outra mensagem sem revisão;
- preparar resumo para atendimento humano.

## Primeiro dia recomendado

1. Instalar dependências.
2. Clonar RITO.
3. Validar `memory/entries/`.
4. Instalar MCP de memória apenas se necessário.
5. Configurar `.env` do WAHA.
6. Subir WAHA.
7. Escanear QR.
8. Testar envio próprio.
9. Testar recebimento próprio.
10. Validar `assets/drive/asset-manifest.json`.
11. Criar um pequeno log operacional versionável.
12. Fazer commit e push.
13. Validar no Mac principal com `git pull`.

Se esse ciclo funcionar, o servidor está pronto para receber rotinas maiores.
