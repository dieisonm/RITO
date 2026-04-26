<?php

declare(strict_types=1);

function contactPageUrl(): string
{
    $scriptName = (string) ($_SERVER['SCRIPT_NAME'] ?? '/contact.php');
    $basePath = str_replace('\\', '/', dirname($scriptName));

    if ($basePath === '/' || $basePath === '.') {
        return '/pages/contato.html';
    }

    return rtrim($basePath, '/') . '/pages/contato.html';
}

function wantsJsonResponse(): bool
{
    $requestedWith = strtolower((string) ($_SERVER['HTTP_X_REQUESTED_WITH'] ?? ''));
    $accept = strtolower((string) ($_SERVER['HTTP_ACCEPT'] ?? ''));

    return $requestedWith === 'xmlhttprequest' || strpos($accept, 'application/json') !== false;
}

function mimeHeader(string $value): string
{
    return '=?UTF-8?B?' . base64_encode($value) . '?=';
}

function cleanLine(string $value): string
{
    $normalized = preg_replace('/[\r\n]+/', ' ', $value);

    return trim((string) $normalized);
}

function shorten(string $value, int $limit): string
{
    if (function_exists('mb_substr')) {
        return mb_substr($value, 0, $limit);
    }

    return substr($value, 0, $limit);
}

function digitsOnly(string $value): string
{
    return preg_replace('/\D+/', '', $value) ?? '';
}

function formatPhone(string $value): string
{
    $digits = digitsOnly($value);

    if (strlen($digits) <= 2) {
        return $digits;
    }

    if (strlen($digits) <= 6) {
        return substr($digits, 0, 2) . ' ' . substr($digits, 2);
    }

    if (strlen($digits) <= 10) {
        return substr($digits, 0, 2) . ' ' . substr($digits, 2, 4) . ' ' . substr($digits, 6);
    }

    return substr($digits, 0, 2) . ' ' . substr($digits, 2, 5) . ' ' . substr($digits, 7, 4);
}

function smtpConfigFilePath(): string
{
    return dirname(__DIR__) . '/rito-smtp.php';
}

function envString(string $name): string
{
    $value = getenv($name);

    if ($value === false) {
        return '';
    }

    return trim((string) $value);
}

function mailboxHeader(string $name, string $email): string
{
    return mimeHeader($name) . ' <' . $email . '>';
}

function loadSmtpConfig(): ?array
{
    $rawConfig = [];
    $configFile = smtpConfigFilePath();

    if (is_file($configFile)) {
        $loadedConfig = require $configFile;

        if (is_array($loadedConfig)) {
            $rawConfig = $loadedConfig;
        }
    }

    if ($rawConfig === []) {
        $rawConfig = [
            'host' => envString('RITO_SMTP_HOST'),
            'port' => envString('RITO_SMTP_PORT'),
            'encryption' => envString('RITO_SMTP_ENCRYPTION'),
            'username' => envString('RITO_SMTP_USERNAME'),
            'password' => envString('RITO_SMTP_PASSWORD'),
            'from_email' => envString('RITO_SMTP_FROM_EMAIL'),
            'from_name' => envString('RITO_SMTP_FROM_NAME'),
            'to_email' => envString('RITO_SMTP_TO_EMAIL'),
        ];
    }

    $host = cleanLine((string) ($rawConfig['host'] ?? ''));
    $encryption = strtolower(cleanLine((string) ($rawConfig['encryption'] ?? 'ssl')));
    $username = cleanLine((string) ($rawConfig['username'] ?? ''));
    $password = (string) ($rawConfig['password'] ?? '');
    $fromEmail = cleanLine((string) ($rawConfig['from_email'] ?? $username));
    $fromName = cleanLine((string) ($rawConfig['from_name'] ?? 'RITO Sistemas'));
    $toEmail = cleanLine((string) ($rawConfig['to_email'] ?? $username));
    $port = (int) ($rawConfig['port'] ?? 0);

    if (!in_array($encryption, ['ssl', 'tls'], true)) {
        $encryption = 'ssl';
    }

    if ($port <= 0) {
        $port = $encryption === 'tls' ? 587 : 465;
    }

    if (
        $host === '' ||
        $username === '' ||
        $password === '' ||
        filter_var($fromEmail, FILTER_VALIDATE_EMAIL) === false ||
        filter_var($toEmail, FILTER_VALIDATE_EMAIL) === false
    ) {
        return null;
    }

    return [
        'host' => $host,
        'port' => $port,
        'encryption' => $encryption,
        'username' => $username,
        'password' => $password,
        'from_email' => $fromEmail,
        'from_name' => $fromName !== '' ? $fromName : 'RITO Sistemas',
        'to_email' => $toEmail,
    ];
}

function smtpReadResponse($socket, array $expectedCodes): void
{
    $response = '';

    while (($line = fgets($socket, 515)) !== false) {
        $response .= $line;

        if (preg_match('/^\d{3} /', $line) === 1) {
            break;
        }
    }

    if ($response === '') {
        throw new RuntimeException('SMTP sem resposta do servidor.');
    }

    $code = (int) substr($response, 0, 3);

    if (!in_array($code, $expectedCodes, true)) {
        throw new RuntimeException('Resposta SMTP inesperada: ' . trim($response));
    }
}

function smtpWriteLine($socket, string $line): void
{
    $bytesWritten = fwrite($socket, $line . "\r\n");

    if ($bytesWritten === false) {
        throw new RuntimeException('Nao foi possivel escrever no servidor SMTP.');
    }
}

function smtpCommand($socket, string $command, array $expectedCodes): void
{
    smtpWriteLine($socket, $command);
    smtpReadResponse($socket, $expectedCodes);
}

function smtpCryptoMethod(): int
{
    if (defined('STREAM_CRYPTO_METHOD_TLS_CLIENT')) {
        return STREAM_CRYPTO_METHOD_TLS_CLIENT;
    }

    if (defined('STREAM_CRYPTO_METHOD_SSLv23_CLIENT')) {
        return STREAM_CRYPTO_METHOD_SSLv23_CLIENT;
    }

    return 0;
}

function dotStuff(string $message): string
{
    $lines = preg_split("/\r\n|\n|\r/", $message) ?: [];

    foreach ($lines as &$line) {
        if (strpos($line, '.') === 0) {
            $line = '.' . $line;
        }
    }

    unset($line);

    return implode("\r\n", $lines);
}

function sendEmailViaSmtp(array $config, string $subjectText, string $body, ?string $replyToEmail, ?string $replyToName): bool
{
    $protocol = $config['encryption'] === 'ssl' ? 'ssl://' : 'tcp://';
    $socketTarget = $protocol . $config['host'] . ':' . $config['port'];
    $context = stream_context_create([
        'ssl' => [
            'verify_peer' => true,
            'verify_peer_name' => true,
            'allow_self_signed' => false,
        ],
    ]);

    $socket = @stream_socket_client(
        $socketTarget,
        $errorNumber,
        $errorMessage,
        20,
        STREAM_CLIENT_CONNECT,
        $context
    );

    if (!is_resource($socket)) {
        return false;
    }

    stream_set_timeout($socket, 20);

    try {
        smtpReadResponse($socket, [220]);
        smtpCommand($socket, 'EHLO ritosistemas.com', [250]);

        if ($config['encryption'] === 'tls') {
            smtpCommand($socket, 'STARTTLS', [220]);

            $cryptoMethod = smtpCryptoMethod();
            $cryptoEnabled = $cryptoMethod > 0
                ? stream_socket_enable_crypto($socket, true, $cryptoMethod)
                : stream_socket_enable_crypto($socket, true);

            if ($cryptoEnabled !== true) {
                throw new RuntimeException('Nao foi possivel iniciar TLS com o servidor SMTP.');
            }

            smtpCommand($socket, 'EHLO ritosistemas.com', [250]);
        }

        smtpCommand($socket, 'AUTH LOGIN', [334]);
        smtpCommand($socket, base64_encode($config['username']), [334]);
        smtpCommand($socket, base64_encode($config['password']), [235]);
        smtpCommand($socket, 'MAIL FROM:<' . $config['from_email'] . '>', [250]);
        smtpCommand($socket, 'RCPT TO:<' . $config['to_email'] . '>', [250, 251]);
        smtpCommand($socket, 'DATA', [354]);

        $headers = [
            'Date: ' . date(DATE_RFC2822),
            'Subject: ' . mimeHeader($subjectText),
            'From: ' . mailboxHeader($config['from_name'], $config['from_email']),
            'To: ' . mailboxHeader($config['from_name'], $config['to_email']),
            'MIME-Version: 1.0',
            'Content-Type: text/plain; charset=UTF-8',
            'Content-Transfer-Encoding: 8bit',
            'X-Mailer: RITO SMTP',
        ];

        if ($replyToEmail !== null && filter_var($replyToEmail, FILTER_VALIDATE_EMAIL) !== false) {
            $replyToLabel = $replyToName !== null && $replyToName !== '' ? $replyToName : $replyToEmail;
            $headers[] = 'Reply-To: ' . mailboxHeader($replyToLabel, $replyToEmail);
        }

        $payload = implode("\r\n", $headers) . "\r\n\r\n" . dotStuff($body) . "\r\n.";
        smtpWriteLine($socket, $payload);
        smtpReadResponse($socket, [250]);
        smtpCommand($socket, 'QUIT', [221]);
        fclose($socket);

        return true;
    } catch (Throwable $exception) {
        if (is_resource($socket)) {
            @fclose($socket);
        }

        return false;
    }
}

function respond(bool $success, string $message)
{
    if (wantsJsonResponse()) {
        header('Content-Type: application/json; charset=UTF-8');
        http_response_code($success ? 200 : 400);
        echo json_encode(
            ['ok' => $success, 'message' => $message],
            JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES
        );
        exit;
    }

    $status = $success ? 'success' : 'error';
    header('Location: ' . contactPageUrl() . '?status=' . $status);
    exit;
}

function storageDirectory(): string
{
    return __DIR__ . '/storage';
}

function storageFilePath(): string
{
    return storageDirectory() . '/contact_requests.jsonl';
}

function ensureStorageReady(): bool
{
    $directory = storageDirectory();

    if (is_dir($directory)) {
        return is_writable($directory);
    }

    return mkdir($directory, 0755, true);
}

function saveLead(array $payload): bool
{
    if (!ensureStorageReady()) {
        return false;
    }

    $record = json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

    if ($record === false) {
        return false;
    }

    return file_put_contents(storageFilePath(), $record . PHP_EOL, FILE_APPEND | LOCK_EX) !== false;
}

if (strtoupper((string) ($_SERVER['REQUEST_METHOD'] ?? 'GET')) !== 'POST') {
    header('Location: ' . contactPageUrl());
    exit;
}

$name = cleanLine((string) ($_POST['name'] ?? ''));
$business = cleanLine((string) ($_POST['business'] ?? ''));
$email = cleanLine((string) ($_POST['email'] ?? ''));
$whatsapp = cleanLine((string) ($_POST['whatsapp'] ?? ''));
$businessProfile = cleanLine((string) ($_POST['business_profile'] ?? ''));
$preferredContact = cleanLine((string) ($_POST['preferred_contact'] ?? 'email'));
$message = trim((string) ($_POST['message'] ?? ''));
$honeypot = trim((string) ($_POST['website'] ?? ''));

if ($honeypot !== '') {
    respond(true, 'Recebemos a sua mensagem e entraremos em contato em breve.');
}

if ($name === '' || $business === '' || $whatsapp === '' || $message === '') {
    respond(false, 'Preencha nome, empresa ou negócio, telefone e a descrição da sua necessidade.');
}

$whatsappDigits = digitsOnly($whatsapp);

if (strlen($whatsappDigits) < 10 || strlen($whatsappDigits) > 11) {
    respond(false, 'Informe um telefone ou WhatsApp válido com DDD.');
}

if ($email !== '' && filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
    respond(false, 'Informe um e-mail válido ou deixe esse campo em branco.');
}

if ($preferredContact === 'email' && $email === '') {
    respond(false, 'Se preferir retorno por e-mail, informe um e-mail válido.');
}

$name = shorten($name, 120);
$business = shorten($business, 160);
$email = shorten($email, 160);
$whatsapp = shorten(formatPhone($whatsappDigits), 60);
$businessProfile = shorten($businessProfile, 80);
$preferredContact = shorten($preferredContact, 40);
$message = shorten($message, 5000);

$subjectName = $business !== '' ? $business : $name;
$subjectText = "Novo pedido de orçamento - {$subjectName}";
$subject = mimeHeader($subjectText);

$bodyLines = [
    'Novo pedido de orçamento recebido pelo site da RITO.',
    '',
    'Nome: ' . $name,
    'Empresa ou negócio: ' . $business,
    'E-mail: ' . ($email !== '' ? $email : 'Não informado'),
    'WhatsApp: ' . $whatsapp,
    'Perfil do negócio: ' . ($businessProfile !== '' ? $businessProfile : 'Não informado'),
    'Canal preferido para retorno: ' . ($preferredContact !== '' ? $preferredContact : 'email'),
    '',
    'Necessidade informada:',
    $message,
    '',
    'Origem: formulário do site RITO',
];

$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'From: RITO Sistemas <contato@ritosistemas.com>',
];

if ($email !== '') {
    $headers[] = 'Reply-To: ' . $email;
}

$body = implode("\r\n", $bodyLines);
$leadPayload = [
    'submitted_at' => gmdate('c'),
    'name' => $name,
    'business' => $business,
    'email' => $email !== '' ? $email : null,
    'whatsapp' => $whatsapp,
    'business_profile' => $businessProfile !== '' ? $businessProfile : null,
    'preferred_contact' => $preferredContact !== '' ? $preferredContact : 'email',
    'message' => $message,
    'ip' => cleanLine((string) ($_SERVER['REMOTE_ADDR'] ?? '')),
    'user_agent' => cleanLine((string) ($_SERVER['HTTP_USER_AGENT'] ?? '')),
];

if (!saveLead($leadPayload)) {
    respond(
        false,
        'Não conseguimos registrar sua solicitação agora. Tente novamente em instantes ou use o envio por e-mail.'
    );
}

$smtpConfig = loadSmtpConfig();

if ($smtpConfig !== null) {
    $sent = sendEmailViaSmtp(
        $smtpConfig,
        $subjectText,
        $body,
        $email !== '' ? $email : null,
        $name !== '' ? $name : null
    );
} else {
    $sent = @mail('contato@ritosistemas.com', $subject, $body, implode("\r\n", $headers));
}

if (!$sent) {
    respond(true, 'Recebemos a sua solicitação e ela foi registrada. Se necessário, entraremos em contato mesmo que o envio de e-mail interno tenha falhado.');
}

respond(true, 'Recebemos a sua solicitação. A RITO entrará em contato em breve.');
