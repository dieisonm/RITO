# Email Operacional e Campanhas

## Regra atual

- `contato@ritosistemas.com` e `comercial@ritosistemas.com` ficam como caixas de entrada/resposta na Hostinger.
- Disparos de campanha/prospeccao devem usar Brevo, nao SMTP da Hostinger.
- A senha da caixa Hostinger nao deve ser usada para campanha. A Brevo usa chave SMTP propria.
- `rito-smtp.php` e local, esta no `.gitignore` e nao deve ser versionado.

## Configuracao Brevo para disparo

1. Criar/verificar o remetente `comercial@ritosistemas.com` na Brevo.
2. Autenticar o dominio `ritosistemas.com` na Brevo.
3. Copiar os registros DNS indicados pela Brevo para o DNS da Hostinger:
   - codigo Brevo de verificacao;
   - DKIM;
   - DMARC;
   - SPF apenas se a Brevo solicitar e sempre mantendo um unico registro SPF no dominio.
4. Criar uma chave SMTP na Brevo.
5. Copiar `rito-smtp.brevo.example.php` para `rito-smtp.php`.
6. Preencher `username` com o login SMTP da Brevo e `password` com a chave SMTP da Brevo.
7. Fazer primeiro um envio de teste para `comercial@ritosistemas.com`.

Configuracao esperada no arquivo local:

```php
return [
    'host' => 'smtp-relay.brevo.com',
    'port' => 587,
    'encryption' => 'tls',
    'username' => 'SEU_LOGIN_SMTP_DA_BREVO',
    'password' => 'SUA_CHAVE_SMTP_DA_BREVO',
    'from_email' => 'comercial@ritosistemas.com',
    'from_name' => 'RITO Sistemas',
    'to_email' => 'comercial@ritosistemas.com',
];
```

## Envio de campanha

Arquivo:

- `scripts/send_outbound_emails.php`

O script envia `multipart/alternative`, com texto e HTML, usando:

- `operations/ai-os/email/templates/prospecting-outbound-email-template-v2.html`
- anexos inline da marca quando disponiveis

Antes de qualquer envio externo:

1. revisar lista de destinatarios;
2. revisar assunto e corpo final;
3. enviar teste interno;
4. confirmar que Brevo esta autenticado;
5. pedir aprovacao explicita para aplicar.

Exemplo de teste interno:

```bash
php scripts/send_outbound_emails.php \
  --batch-csv=2026-05-18-batch-006-pilot.csv \
  --batch-json=2026-05-18-batch-006-outreach-data.json \
  --company-ids=nh-006-001 \
  --test-to=comercial@ritosistemas.com
```

Exemplo de envio real, apenas depois de aprovacao:

```bash
php scripts/send_outbound_emails.php \
  --batch-csv=2026-05-18-batch-006-pilot.csv \
  --batch-json=2026-05-18-batch-006-outreach-data.json \
  --throttle-seconds=90 \
  --apply
```

## Leitura Hostinger

## Script

Arquivo:

- `scripts/read_hostinger_inbox.py`

Como funciona:

- leitura por `IMAP SSL`;
- servidor padrao da Hostinger: `imap.hostinger.com:993`;
- usado para acompanhar respostas, nao para disparar campanha.

Exemplos:

```bash
python3 scripts/read_hostinger_inbox.py --pretty
python3 scripts/read_hostinger_inbox.py --unseen --limit 20 --pretty
python3 scripts/read_hostinger_inbox.py --mailbox INBOX --limit 5 --pretty
```

## Template HTML

Arquivos:

- `operations/ai-os/email/templates/prospecting-outbound-email-template.html`
- `operations/ai-os/email/previews/prospecting-outbound-email-preview-dalis.html`
- `operations/ai-os/email/templates/prospecting-outbound-email-template-v2.html`
- `operations/ai-os/email/previews/prospecting-outbound-email-preview-v2-dalis.html`

Uso sugerido:

- aprovar a direção visual primeiro pela prévia local
- depois adaptar o sender para enviar `multipart/alternative` com versão texto e HTML

## Referência operacional

Segundo as documentacoes oficiais:

- Brevo SMTP relay: `smtp-relay.brevo.com`, porta `587`, `465` ou `2525`; para SMTP usar chave SMTP, nao API key.
- Autenticacao Brevo: validar dominio/remetente com registros DNS de verificacao, DKIM e DMARC.
- Hostinger IMAP: `imap.hostinger.com`, porta `993`, criptografia `SSL`.

O webmail direto fica em:

- `https://mail.hostinger.com`
