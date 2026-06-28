# Prospecção Territorial

Esta área organiza a prospecção ativa da RITO por território, cidade e batches sucessivos.

## Objetivo

Permitir que a descoberta de empresas aconteça em várias interações sem perder:

- cobertura do território
- histórico do que já foi analisado
- status de revisão e contato
- hipóteses de oferta por empresa
- sinais novos encontrados em rodadas futuras

## Estrutura

- `territories/`: uma pasta por cidade ou região
- `batches/`: lotes fechados de descoberta e análise
- `queries/`: bancos de busca e ondas de descoberta

## Regra operacional

- trabalhar por lotes pequenos e cumulativos
- deduplicar por nome, domínio, telefone e WhatsApp
- registrar a origem pública de cada dado importante
- separar descoberta de envio
- revisar antes de qualquer contato externo
- quando houver referência a Instagram, escalar para verificação manual do usuário

## Cadência recomendada

- rodadas de descoberta: batches de `25` a `40` empresas por interação
- revisão e contato: batches menores, de maior qualidade
- refresh territorial: semanal ou quinzenal

## Estado mínimo por empresa

- `descoberta`
- `analisada`
- `revisando`
- `pronta-para-contato`
- `contatada`
- `respondeu`
- `sem-resposta`
- `nao-contatar`
- `stale`
