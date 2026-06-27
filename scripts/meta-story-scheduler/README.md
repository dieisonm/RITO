# Meta Story Scheduler

Automacao local em Playwright para agendar stories no Meta Business Suite sem depender do addon do Codex.

## O que faz

- usa um perfil proprio do navegador para manter a sessao do Meta
- agenda stories a partir de um arquivo JSON com datas, horarios e caminhos de imagem
- valida arquivos antes de abrir o navegador
- permite autenticar uma vez e depois rodar o agendamento em lote

## Setup

```bash
cd ../../scripts/meta-story-scheduler
npm install
```

## Fluxo recomendado

1. Copie o template em `operations/instagram/story-schedule.plan.template.json` para um plano real.
2. Rode a autenticacao inicial:

```bash
node schedule_instagram_stories.mjs auth --config ../../operations/instagram/story-schedule.plan.template.json
```

3. Faça login no Meta Business Suite na janela aberta e pressione `Enter` no terminal.
4. Ajuste o arquivo JSON com os stories reais.
5. Rode o agendamento:

```bash
node schedule_instagram_stories.mjs schedule --config ../../operations/instagram/story-schedule.plan.template.json
```

## Comandos

### Validar o plano

```bash
node schedule_instagram_stories.mjs validate --config ../../operations/instagram/story-schedule.plan.template.json
```

### Agendar apenas os primeiros N stories

```bash
node schedule_instagram_stories.mjs schedule --config ../../operations/instagram/story-schedule.plan.template.json --limit 5
```

### Continuar mesmo se um story falhar

```bash
node schedule_instagram_stories.mjs schedule --config ../../operations/instagram/story-schedule.plan.template.json --continue-on-error
```

### Rodar em dry-run

```bash
node schedule_instagram_stories.mjs schedule --config ../../operations/instagram/story-schedule.plan.template.json --dry-run
```

## Observacoes

- o script usa `channel: chrome`, entao espera Google Chrome instalado na maquina
- o perfil persistente fica fora do Git em `scripts/meta-story-scheduler/.auth/`
- se a sessao do Meta expirar, rode `auth` de novo
- o script foi pensado para stories com uma imagem por publicacao
- o pacing fica no JSON em `pacing`, entao voce pode desacelerar ou acelerar sem editar o codigo

## Pacing

Campos do bloco `pacing`:

- `afterComposerLoadMs`: pausa depois de abrir o composer
- `afterMediaClearMs`: pausa depois de remover uma imagem antiga do composer
- `afterMediaUploadMs`: pausa depois do upload da imagem
- `afterScheduleToggleMs`: pausa depois de ativar o agendamento
- `afterDateSetMs`: pausa depois de preencher a data
- `afterTimeSetMs`: pausa depois de ajustar o horario
- `beforeScheduleClickMs`: pausa final antes de clicar em `Schedule`
- `afterScheduleSuccessMs`: pausa depois da confirmacao de sucesso
- `betweenStoriesMs`: pausa entre um story e o proximo
- `stepPauseMs`: micro pausa entre pressionamentos em controles de hora
