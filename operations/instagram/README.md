# Instagram AI

Espaço para organizar a operação de Instagram da RITO.

## Objetivos iniciais

- Criar presença com cara de empresa
- Testar formatos curtos e diretos
- Aumentar reconhecimento de marca entre micro e pequenas empresas
- Preparar a conta para impulsionamento futuro sem depender de volume artificial

## Materiais oficiais

- [Instagram Company Bio](../../docs/company/presence/instagram-company-bio.md)
- [Social Profile Setup Checklist](../../docs/company/presence/social-profile-setup-checklist.md)
- [Instagram Launch Strategy](../../docs/company/presence/instagram-launch-strategy.md)
- [Instagram Official Post Direction](../../docs/company/presence/instagram-official-post-direction.md)
- [Instagram Launch Audit and DoD](../../docs/company/reviews/instagram-launch-flow-audit-and-dod.md)
- [Launch Production Board](../../operations/instagram/launch-production-board.md)
- [Organic Growth Starter](../../operations/instagram/organic-growth-starter.md)
- [Hashtag Bank](../../operations/instagram/hashtag-bank.md)
- [Posts Iniciais](../../operations/instagram/posts/README.md)

## Diretriz da fase inicial

- Priorizar 2 posts estáticos e 1 carrossel curto
- Usar peças `photo-led`, não layouts com cara de apresentação
- Manter CTA único para WhatsApp
- Usar hashtags como apoio, não como estratégia principal
- Repetir os temas que falam de rotina, planilha, retrabalho e controle
- Deixar a conta pronta para tráfego pago com contexto visual e mensagem clara

## Entregas atuais

- artes finais em `deliverables/social-assets/instagram-launch/`
- textos de publicação em `operations/instagram/posts/`
- estratégia de largada em `docs/company/presence/instagram-launch-strategy.md`
- direção oficial extraída das peças aprovadas em `docs/company/presence/instagram-official-post-direction.md`

## Ativos futuros

- Linha editorial
- Modelos de reels, stories e posts
- Banco de prompts visuais
- Painel de métricas

## Agendamento automatizado

- Automação local em Playwright para stories: [scripts/meta-story-scheduler/README.md](../../scripts/meta-story-scheduler/README.md)
- Template de plano para o Meta Planner: [story-schedule.plan.template.json](../../operations/instagram/story-schedule.plan.template.json)
- O fluxo recomendado é autenticar uma vez no perfil persistente e depois agendar por arquivo JSON.
- A lógica editorial fica no plano, e o trabalho repetitivo fica no script.

## Prompt visual

- Guia oficial interno para GPT Image 2: [GPT Image 2 Visual Prompting Guide](../../docs/company/agent-system/gpt-image-2-visual-prompting-guide.md)
- A geração de imagens pode ser feita diretamente no Codex via ImageGen quando a demanda for produção visual.
- Depois de gerar, copiar o arquivo para `deliverables/social-assets/`, validar dimensão final e registrar o lote.

## Acesso local

- Credenciais locais devem ficar em `operations/instagram/instagram-access.local.md`.
- Esse arquivo é privado e não deve ser versionado no Git.
- Evite repetir senha em documentação pública, memória persistente ou materiais de operação.
- Use apenas o arquivo local privado para credenciais e não replique dados sensiveis em outros documentos.

## Observação de segurança

Se a senha mudar, atualize apenas o arquivo local privado e não replique a credencial em outros documentos.
