<?php

// Local: copie para `rito-smtp.php` na raiz do projeto.
// Hostinger: crie `rito-smtp.php` um nivel acima de `public_html`,
// para que o arquivo fique fora da pasta publica e fora do Git deploy.

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
