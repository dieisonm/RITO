<?php

// Local: copie este arquivo para `rito-smtp.php` na raiz do projeto.
// Nao versione `rito-smtp.php`; ele fica no .gitignore.
//
// Brevo:
// - host: smtp-relay.brevo.com
// - porta recomendada: 587 com STARTTLS
// - username: login SMTP exibido pela Brevo
// - password: chave SMTP da Brevo, nao a senha da caixa Hostinger
//
// Use `comercial@ritosistemas.com` como remetente depois de validar o
// dominio/remetente na Brevo e autenticar os registros DNS.

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
