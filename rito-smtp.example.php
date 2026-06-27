<?php

// Local: copie para `rito-smtp.php` na raiz do projeto.
// Hostinger: crie `rito-smtp.php` um nivel acima de `public_html`,
// para que o arquivo fique fora da pasta publica e fora do Git deploy.
//
// Este exemplo e para caixa comum da Hostinger. Para campanha/prospeccao,
// use `rito-smtp.brevo.example.php` e uma chave SMTP da Brevo.

return [
    'host' => 'smtp.hostinger.com',
    'port' => 465,
    'encryption' => 'ssl',
    'username' => 'contato@seudominio.com',
    'password' => 'SUA_SENHA_AQUI',
    'from_email' => 'contato@seudominio.com',
    'from_name' => 'RITO Sistemas',
    'to_email' => 'contato@seudominio.com',
];
