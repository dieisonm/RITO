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
$solutionType = cleanLine((string) ($_POST['solution_type'] ?? ''));
$leadSource = cleanLine((string) ($_POST['lead_source'] ?? 'site_form'));
$campaign = cleanLine((string) ($_POST['campaign'] ?? ''));
$sourcePage = cleanLine((string) ($_POST['source_page'] ?? ''));
$utmId = cleanLine((string) ($_POST['utm_id'] ?? ''));
$utmSource = cleanLine((string) ($_POST['utm_source'] ?? ''));
$utmMedium = cleanLine((string) ($_POST['utm_medium'] ?? ''));
$utmCampaign = cleanLine((string) ($_POST['utm_campaign'] ?? ''));
$utmSourcePlatform = cleanLine((string) ($_POST['utm_source_platform'] ?? ''));
$utmContent = cleanLine((string) ($_POST['utm_content'] ?? ''));
$utmTerm = cleanLine((string) ($_POST['utm_term'] ?? ''));
$utmCreativeFormat = cleanLine((string) ($_POST['utm_creative_format'] ?? ''));
$utmMarketingTactic = cleanLine((string) ($_POST['utm_marketing_tactic'] ?? ''));
$gclid = cleanLine((string) ($_POST['gclid'] ?? ''));
$gbraid = cleanLine((string) ($_POST['gbraid'] ?? ''));
$wbraid = cleanLine((string) ($_POST['wbraid'] ?? ''));
$fbclid = cleanLine((string) ($_POST['fbclid'] ?? ''));
$msclkid = cleanLine((string) ($_POST['msclkid'] ?? ''));
$liFatId = cleanLine((string) ($_POST['li_fat_id'] ?? ''));
$ttclid = cleanLine((string) ($_POST['ttclid'] ?? ''));
$metaFbp = cleanLine((string) ($_POST['meta_fbp'] ?? ''));
$metaFbc = cleanLine((string) ($_POST['meta_fbc'] ?? ''));
$landingPage = cleanLine((string) ($_POST['landing_page'] ?? ''));
$referrer = cleanLine((string) ($_POST['referrer'] ?? ''));
$firstLandingPage = cleanLine((string) ($_POST['first_landing_page'] ?? ''));
$firstReferrer = cleanLine((string) ($_POST['first_referrer'] ?? ''));
$firstUtmId = cleanLine((string) ($_POST['first_utm_id'] ?? ''));
$firstUtmSource = cleanLine((string) ($_POST['first_utm_source'] ?? ''));
$firstUtmMedium = cleanLine((string) ($_POST['first_utm_medium'] ?? ''));
$firstUtmCampaign = cleanLine((string) ($_POST['first_utm_campaign'] ?? ''));
$firstUtmSourcePlatform = cleanLine((string) ($_POST['first_utm_source_platform'] ?? ''));
$firstUtmContent = cleanLine((string) ($_POST['first_utm_content'] ?? ''));
$firstUtmTerm = cleanLine((string) ($_POST['first_utm_term'] ?? ''));
$casePermission = cleanLine((string) ($_POST['case_permission'] ?? ''));
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

if ($campaign === 'projeto_piloto_mei' && $casePermission !== 'accepted') {
    respond(false, 'Para participar do projeto piloto, confirme a condição de documentação do caso com aprovação prévia.');
}

$name = shorten($name, 120);
$business = shorten($business, 160);
$email = shorten($email, 160);
$whatsapp = shorten(formatPhone($whatsappDigits), 60);
$businessProfile = shorten($businessProfile, 80);
$preferredContact = shorten($preferredContact, 40);
$solutionType = shorten($solutionType, 120);
$leadSource = shorten($leadSource !== '' ? $leadSource : 'site_form', 120);
$campaign = shorten($campaign, 120);
$sourcePage = shorten($sourcePage, 240);
$utmId = shorten($utmId, 160);
$utmSource = shorten($utmSource, 120);
$utmMedium = shorten($utmMedium, 120);
$utmCampaign = shorten($utmCampaign, 160);
$utmSourcePlatform = shorten($utmSourcePlatform, 120);
$utmContent = shorten($utmContent, 160);
$utmTerm = shorten($utmTerm, 160);
$utmCreativeFormat = shorten($utmCreativeFormat, 160);
$utmMarketingTactic = shorten($utmMarketingTactic, 160);
$gclid = shorten($gclid, 220);
$gbraid = shorten($gbraid, 220);
$wbraid = shorten($wbraid, 220);
$fbclid = shorten($fbclid, 400);
$msclkid = shorten($msclkid, 220);
$liFatId = shorten($liFatId, 220);
$ttclid = shorten($ttclid, 220);
$metaFbp = shorten($metaFbp, 240);
$metaFbc = shorten($metaFbc, 240);
$landingPage = shorten($landingPage, 400);
$referrer = shorten($referrer, 400);
$firstLandingPage = shorten($firstLandingPage, 400);
$firstReferrer = shorten($firstReferrer, 400);
$firstUtmId = shorten($firstUtmId, 160);
$firstUtmSource = shorten($firstUtmSource, 120);
$firstUtmMedium = shorten($firstUtmMedium, 120);
$firstUtmCampaign = shorten($firstUtmCampaign, 160);
$firstUtmSourcePlatform = shorten($firstUtmSourcePlatform, 120);
$firstUtmContent = shorten($firstUtmContent, 160);
$firstUtmTerm = shorten($firstUtmTerm, 160);
$casePermission = shorten($casePermission, 40);
$message = shorten($message, 5000);

$subjectName = $business !== '' ? $business : $name;
$subjectPrefix = $campaign === 'projeto_piloto_mei' ? 'Novo candidato ao Projeto Piloto' : 'Novo pedido de orçamento';
$subjectText = "{$subjectPrefix} - {$subjectName}";
$subject = mimeHeader($subjectText);

$bodyLines = [
    'Novo pedido de orçamento recebido pelo site da RITO.',
    '',
    'Nome: ' . $name,
    'Empresa ou negócio: ' . $business,
    'E-mail: ' . ($email !== '' ? $email : 'Não informado'),
    'WhatsApp: ' . $whatsapp,
    'Perfil do negócio: ' . ($businessProfile !== '' ? $businessProfile : 'Não informado'),
    'Tipo de solução desejada: ' . ($solutionType !== '' ? $solutionType : 'Não informado'),
    'Canal preferido para retorno: ' . ($preferredContact !== '' ? $preferredContact : 'email'),
    'Origem: ' . $leadSource,
    'Campanha: ' . ($campaign !== '' ? $campaign : 'Não informada'),
    'Página de origem: ' . ($sourcePage !== '' ? $sourcePage : 'Não informada'),
    'UTM ID: ' . ($utmId !== '' ? $utmId : 'Não informado'),
    'UTM source: ' . ($utmSource !== '' ? $utmSource : 'Não informado'),
    'UTM medium: ' . ($utmMedium !== '' ? $utmMedium : 'Não informado'),
    'UTM campaign: ' . ($utmCampaign !== '' ? $utmCampaign : 'Não informado'),
    'UTM source platform: ' . ($utmSourcePlatform !== '' ? $utmSourcePlatform : 'Não informado'),
    'UTM content: ' . ($utmContent !== '' ? $utmContent : 'Não informado'),
    'UTM term: ' . ($utmTerm !== '' ? $utmTerm : 'Não informado'),
    'UTM creative format: ' . ($utmCreativeFormat !== '' ? $utmCreativeFormat : 'Não informado'),
    'UTM marketing tactic: ' . ($utmMarketingTactic !== '' ? $utmMarketingTactic : 'Não informado'),
    'GCLID: ' . ($gclid !== '' ? $gclid : 'Não informado'),
    'GBRAID: ' . ($gbraid !== '' ? $gbraid : 'Não informado'),
    'WBRAID: ' . ($wbraid !== '' ? $wbraid : 'Não informado'),
    'FBCLID: ' . ($fbclid !== '' ? $fbclid : 'Não informado'),
    'MSCLKID: ' . ($msclkid !== '' ? $msclkid : 'Não informado'),
    'LI FAT ID: ' . ($liFatId !== '' ? $liFatId : 'Não informado'),
    'TTCLID: ' . ($ttclid !== '' ? $ttclid : 'Não informado'),
    'Meta FBP: ' . ($metaFbp !== '' ? $metaFbp : 'Não informado'),
    'Meta FBC: ' . ($metaFbc !== '' ? $metaFbc : 'Não informado'),
    'Landing page: ' . ($landingPage !== '' ? $landingPage : 'Não informada'),
    'Referrer: ' . ($referrer !== '' ? $referrer : 'Não informado'),
    'Primeira landing page: ' . ($firstLandingPage !== '' ? $firstLandingPage : 'Não informada'),
    'Primeiro referrer: ' . ($firstReferrer !== '' ? $firstReferrer : 'Não informado'),
    'Primeira UTM ID: ' . ($firstUtmId !== '' ? $firstUtmId : 'Não informada'),
    'Primeira UTM source: ' . ($firstUtmSource !== '' ? $firstUtmSource : 'Não informada'),
    'Primeira UTM medium: ' . ($firstUtmMedium !== '' ? $firstUtmMedium : 'Não informada'),
    'Primeira UTM campaign: ' . ($firstUtmCampaign !== '' ? $firstUtmCampaign : 'Não informada'),
    'Primeira UTM source platform: ' . ($firstUtmSourcePlatform !== '' ? $firstUtmSourcePlatform : 'Não informada'),
    'Primeira UTM content: ' . ($firstUtmContent !== '' ? $firstUtmContent : 'Não informada'),
    'Primeira UTM term: ' . ($firstUtmTerm !== '' ? $firstUtmTerm : 'Não informada'),
    'Autorização para case com aprovação prévia: ' . ($casePermission === 'accepted' ? 'Sim' : 'Não informada'),
    '',
    'Necessidade informada:',
    $message,
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
    'solution_type' => $solutionType !== '' ? $solutionType : null,
    'preferred_contact' => $preferredContact !== '' ? $preferredContact : 'email',
    'lead_source' => $leadSource,
    'campaign' => $campaign !== '' ? $campaign : null,
    'source_page' => $sourcePage !== '' ? $sourcePage : null,
    'utm_id' => $utmId !== '' ? $utmId : null,
    'utm_source' => $utmSource !== '' ? $utmSource : null,
    'utm_medium' => $utmMedium !== '' ? $utmMedium : null,
    'utm_campaign' => $utmCampaign !== '' ? $utmCampaign : null,
    'utm_source_platform' => $utmSourcePlatform !== '' ? $utmSourcePlatform : null,
    'utm_content' => $utmContent !== '' ? $utmContent : null,
    'utm_term' => $utmTerm !== '' ? $utmTerm : null,
    'utm_creative_format' => $utmCreativeFormat !== '' ? $utmCreativeFormat : null,
    'utm_marketing_tactic' => $utmMarketingTactic !== '' ? $utmMarketingTactic : null,
    'gclid' => $gclid !== '' ? $gclid : null,
    'gbraid' => $gbraid !== '' ? $gbraid : null,
    'wbraid' => $wbraid !== '' ? $wbraid : null,
    'fbclid' => $fbclid !== '' ? $fbclid : null,
    'msclkid' => $msclkid !== '' ? $msclkid : null,
    'li_fat_id' => $liFatId !== '' ? $liFatId : null,
    'ttclid' => $ttclid !== '' ? $ttclid : null,
    'meta_fbp' => $metaFbp !== '' ? $metaFbp : null,
    'meta_fbc' => $metaFbc !== '' ? $metaFbc : null,
    'landing_page' => $landingPage !== '' ? $landingPage : null,
    'referrer' => $referrer !== '' ? $referrer : null,
    'first_landing_page' => $firstLandingPage !== '' ? $firstLandingPage : null,
    'first_referrer' => $firstReferrer !== '' ? $firstReferrer : null,
    'first_utm_id' => $firstUtmId !== '' ? $firstUtmId : null,
    'first_utm_source' => $firstUtmSource !== '' ? $firstUtmSource : null,
    'first_utm_medium' => $firstUtmMedium !== '' ? $firstUtmMedium : null,
    'first_utm_campaign' => $firstUtmCampaign !== '' ? $firstUtmCampaign : null,
    'first_utm_source_platform' => $firstUtmSourcePlatform !== '' ? $firstUtmSourcePlatform : null,
    'first_utm_content' => $firstUtmContent !== '' ? $firstUtmContent : null,
    'first_utm_term' => $firstUtmTerm !== '' ? $firstUtmTerm : null,
    'case_permission' => $casePermission === 'accepted',
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
