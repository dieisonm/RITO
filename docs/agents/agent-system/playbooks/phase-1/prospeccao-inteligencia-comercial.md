# Playbook de Prospecção e Inteligência Comercial

## Objetivo

Operar prospecção ativa com foco em precisão, relevância comercial e baixo risco de abordagem errada.

## Resultado esperado

Ao final de cada lote, a RITO deve ter:

- uma base organizada de empresas-alvo
- hipóteses de oferta com evidência
- rascunhos de contato mais personalizados
- uma fila priorizada para revisão e envio humano

## Etapas

### 1. Definir o recorte

- cidade, bairro, região ou raio
- segmentos abertos ou nicho específico
- volume do lote
- objetivo do ciclo:
  - gerar primeiras reuniões
  - validar oferta
  - abrir mercado em uma região
- hipótese do lote:
  - segmento ou arquétipo operacional testado
  - oferta principal testada
  - canal principal testado
  - variação de mensagem usada

Quando os últimos lotes tiverem gerado muita entrega e pouca resposta humana, o próximo lote não deve ser apenas "mais volume". Ele deve testar uma mudança clara: outro segmento, outra oferta, outro CTA, outro canal ou outro ativo de destino.

### 2. Descobrir empresas

Fontes preferenciais:

- busca web por cidade + segmento
- sites oficiais das empresas
- páginas de contato
- diretórios públicos que permitam uso compatível
- presença social apenas como referência indireta encontrada em site, diretório ou busca

Fontes com atenção operacional:

- Instagram não deve ser acessado pelo agente de prospecção
- se um Instagram aparecer citado em site, diretório ou busca, registrar apenas como `referência pendente de verificação manual`
- quando essa verificação for necessária para entender melhor o negócio ou confirmar contato, escalar para o usuário fazer a checagem manual
- quando a fonte tiver maior risco de plataforma ou sensibilidade operacional, isso deve ser registrado no dossiê

### 3. Consolidar o registro

Para cada empresa, registrar no mínimo:

- nome
- cidade
- segmento
- website, se houver
- referência a Instagram, se houver, marcada como manual
- e-mail comercial público, se houver
- telefone ou WhatsApp público empresarial, se houver
- e-mail ou número pessoal quando o próprio negócio o expuser como canal de atendimento
- links de origem
- status de prontidão do WhatsApp
- canal de fallback se o canal principal não estiver realmente pronto
- canal sugerido para contato, deixando claro que a validação técnica final acontece no disparo

### 4. Entender o negócio

Responder com base em evidência:

- o que a empresa vende ou faz
- como ela se apresenta
- quais canais usa
- qual o nível aparente de maturidade digital
- quais sinais apontam para oportunidade real

Nunca transformar hipótese em fato.

### 5. Classificar a oportunidade

Usar uma leitura simples:

- `Presença básica`: negócio sem site próprio, com comunicação simples e poucos pontos de conversão
- `Presença funcional`: site e outros canais públicos existem, mas a jornada é fraca ou pouco organizada
- `Operação manual visível`: indícios de orçamento manual, contato disperso, processos descentralizados
- `Maturidade maior`: pode fazer mais sentido ofertar automação, painel, controle interno ou melhoria operacional

### 6. Sugerir a oferta

Exemplos de mapeamento:

- negócio sem site próprio e com referência social pública: site institucional, landing page, página de contato e estrutura básica de presença
- site simples e contato fraco: melhoria de conversão, captação de leads, formulários, CTA e jornada
- negócio com forte operação manual visível: sistema interno, painel, controle, automação e relatórios
- serviços com orçamento recorrente: calculadora, proposta, CRM leve, fluxo comercial
- clínica, consultório ou agenda: organização operacional, lembretes, controles internos, sem presumir tratamento de dados sensíveis

Regra de formulação:

- a hipótese deve sair em linguagem de `possibilidades alinhadas ao tipo de negócio`
- não sair em linguagem de `falta identificada` sem evidência forte
- registrar sempre `4` frentes plausíveis de solução
- o foco deve ser:
  - rotina
  - operação
  - controles
  - automação
  - sistemas
  - dashboards
  - site, quando fizer sentido
- evitar reduzir tudo a marketing digital ou presença digital

### 7. Preparar abordagem

Canal padrão recomendado:

1. formulário do site
2. e-mail corporativo público
3. e-mail ou número pessoal quando o negócio usar isso comercialmente
4. mensagem manual em canal claramente aberto para contato comercial

WhatsApp:

- não usar como canal frio automatizado padrão
- preparar rascunho quando houver canal público útil
- envio sempre humano e caso a caso
- só marcar `whatsapp-manual` quando houver número confirmado e normalizado
- a prospecção não resolve `chatId` técnico nem garante entrega; isso é responsabilidade do agente de `Disparo / Outbound`
- a mensagem não deve começar apontando falha
- a mensagem deve começar mostrando entendimento do tipo de negócio
- esse entendimento deve soar executivo e impessoal, evitando a moldura `vi que vocês atuam com`
- em seguida, deve citar possibilidades concretas do que a RITO pode construir para operações desse tipo
- considerar número confirmado apenas quando houver:
  - número visível
  - `wa.me/<numero>`
  - `api.whatsapp.com/send?phone=<numero>`
  - configuração pública do site com telefone inequívoco
- se existir apenas CTA genérico, grupo, link curto ou descrição vaga, não tratar isso como contato pronto
- nesse caso, cair para:
  - `email`
  - `formulario`
  - `telefone-manual`
  - `manual-review`

### 8. Revisar antes de enviar

Nenhum contato sai sem checar:

- fonte de cada fato
- qualidade do canal
- tom da mensagem
- adequação da oferta
- risco de parecer spam ou abordagem genérica
- se o canal sugerido realmente está pronto para uso
- se o agente de `Disparo / Outbound` confirmou o canal final, o `resolved_chat_id` no caso de WhatsApp e o fallback correto quando necessário
- se a mensagem fala de possibilidades úteis, e não de deficiência presumida

### 9. Registrar resposta e aprender

Após qualquer resposta:

- atualizar status
- registrar objeções
- registrar sinais que melhoram a próxima prospecção
- alimentar a base com `não contatar`, `sem resposta`, `interessado`, `responder depois`, `rejeitado`

Após silêncio relevante:

- registrar `sem-resposta` por canal e por batch
- comparar segmento, origem do lead, tipo de oferta e canal usado
- reduzir prioridade de segmentos que só geram autoresposta, bounce ou leitura sem conversa
- enviar aprendizado para `Growth / Aquisição` quando o outbound indicar que o público precisa conhecer a RITO antes do contato direto

## Notas de compliance

- Dados de pessoas jurídicas não são, por si só, dados pessoais para fins da LGPD, mas e-mails e telefones podem identificar pessoas naturais em muitos casos.
- Se houver dado pessoal, tratar com minimização, finalidade clara, necessidade e salvaguardas.
- A abordagem deve respeitar a legítima expectativa do titular quando houver dado pessoal envolvido.
- WhatsApp Business exige opt-in para contato subsequente e tem forte política contra mensagens não solicitadas em escala.
- A orientação jurídica da RITO pode permitir coleta ampla de dados públicos de negócio; o agente deve executar essa coleta e registrar origem, tipo de contato e contexto comercial.

## Escalada obrigatória

Escalar para humano quando:

- a origem do contato for duvidosa
- o negócio for regulado ou sensível
- a hipótese de oferta tiver baixa confiança
- houver risco de interpretação errada do negócio
- o WhatsApp público não puder ser reduzido a número confirmável
- houver necessidade de abrir ou validar Instagram

## Limite explícito da prospecção

- o agente de prospecção prepara o contato
- o agente de prospecção não valida transporte
- a decisão final entre `whatsapp`, `email`, `formulario` ou `telefone-manual` no momento do envio pertence ao agente de `Disparo / Outbound`
