<?php

declare(strict_types=1);

function cleanLine(string $value): string
{
    $normalized = preg_replace('/[\r\n]+/', ' ', $value);
    return trim((string) $normalized);
}

function mimeHeader(string $value): string
{
    return '=?UTF-8?B?' . base64_encode($value) . '?=';
}

function mailboxHeader(string $name, string $email): string
{
    return mimeHeader($name) . ' <' . $email . '>';
}

function smtpConfigFilePath(): string
{
    return dirname(__DIR__) . '/rito-smtp.php';
}

function brevoConfigFilePath(): string
{
    return dirname(__DIR__) . '/rito-brevo.php';
}

function secretsConfigFilePath(): string
{
    return dirname(__DIR__) . '/rito-secrets.local.php';
}

function repoRootPath(): string
{
    return dirname(__DIR__);
}

function loadLocalSecrets(): array
{
    $configFile = secretsConfigFilePath();
    if (!is_file($configFile)) {
        return [];
    }

    $rawConfig = require $configFile;
    return is_array($rawConfig) ? $rawConfig : [];
}

function loadBrevoApiConfig(): ?array
{
    $apiKey = cleanLine((string) getenv('BREVO_API_KEY'));
    $secrets = loadLocalSecrets();
    $brevoApi = is_array($secrets['brevo_api'] ?? null) ? $secrets['brevo_api'] : [];

    if ($apiKey === '') {
        $apiKey = cleanLine((string) ($brevoApi['api_key'] ?? ''));
    }

    $configFile = brevoConfigFilePath();
    if ($apiKey === '' && is_file($configFile)) {
        $rawConfig = require $configFile;
        if (is_array($rawConfig)) {
            $apiKey = cleanLine((string) ($rawConfig['api_key'] ?? ''));
        }
    }

    if ($apiKey === '') {
        return null;
    }

    return [
        'api_key' => $apiKey,
    ];
}

function loadOutboundSmtpConfig(): ?array
{
    $secrets = loadLocalSecrets();
    $brevoSmtp = is_array($secrets['brevo_smtp'] ?? null) ? $secrets['brevo_smtp'] : [];

    if ($brevoSmtp !== []) {
        $rawConfig = [
            'host' => $brevoSmtp['host'] ?? '',
            'port' => $brevoSmtp['port'] ?? 0,
            'encryption' => $brevoSmtp['encryption'] ?? 'tls',
            'username' => $brevoSmtp['login'] ?? '',
            'password' => $brevoSmtp['smtp_key'] ?? '',
            'from_email' => $brevoSmtp['from_email'] ?? 'comercial@ritosistemas.com',
            'from_name' => $brevoSmtp['from_name'] ?? 'RITO Sistemas',
        ];
    } else {
        $configFile = smtpConfigFilePath();
        if (!is_file($configFile)) {
            return null;
        }

        $rawConfig = require $configFile;
        if (!is_array($rawConfig)) {
            return null;
        }
    }

    $host = cleanLine((string) ($rawConfig['host'] ?? ''));
    $encryption = strtolower(cleanLine((string) ($rawConfig['encryption'] ?? 'ssl')));
    $username = cleanLine((string) ($rawConfig['username'] ?? ''));
    $password = (string) ($rawConfig['password'] ?? '');
    $fromEmail = cleanLine((string) ($rawConfig['from_email'] ?? $username));
    $fromName = cleanLine((string) ($rawConfig['from_name'] ?? 'RITO Sistemas'));
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
        filter_var($fromEmail, FILTER_VALIDATE_EMAIL) === false
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
    ];
}

function isHostingerSmtp(array $config): bool
{
    $host = strtolower((string) ($config['host'] ?? ''));
    return str_contains($host, 'hostinger');
}

function assertCampaignTransportAllowed(array $config): void
{
    if (!isHostingerSmtp($config)) {
        return;
    }

    throw new RuntimeException(
        'Disparo bloqueado: o SMTP configurado ainda e da Hostinger. ' .
        'Campanhas devem usar Brevo em rito-smtp.php.'
    );
}

function assertSmtpTransportComplete(array $config): void
{
    if ((string) ($config['password'] ?? '') !== '') {
        return;
    }

    throw new RuntimeException('Disparo SMTP bloqueado: senha/chave SMTP ausente em rito-smtp.php.');
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

function buildMimeMessage(string $textBody, ?string $htmlBody = null, array $inlineAttachments = []): array
{
    if ($htmlBody === null) {
        return [
            'headers' => [
                'MIME-Version: 1.0',
                'Content-Type: text/plain; charset=UTF-8',
                'Content-Transfer-Encoding: 8bit',
            ],
            'body' => $textBody,
        ];
    }

    $alternativeBoundary = '=_rito_alt_' . bin2hex(random_bytes(8));
    $relatedBoundary = '=_rito_related_' . bin2hex(random_bytes(8));

    $parts = [];
    $parts[] = '--' . $relatedBoundary;
    $parts[] = 'Content-Type: multipart/alternative; boundary="' . $alternativeBoundary . '"';
    $parts[] = '';

    $parts[] = '--' . $alternativeBoundary;
    $parts[] = 'Content-Type: text/plain; charset=UTF-8';
    $parts[] = 'Content-Transfer-Encoding: 8bit';
    $parts[] = '';
    $parts[] = $textBody;
    $parts[] = '';

    $parts[] = '--' . $alternativeBoundary;
    $parts[] = 'Content-Type: text/html; charset=UTF-8';
    $parts[] = 'Content-Transfer-Encoding: 8bit';
    $parts[] = '';
    $parts[] = $htmlBody;
    $parts[] = '';
    $parts[] = '--' . $alternativeBoundary . '--';
    $parts[] = '';

    foreach ($inlineAttachments as $attachment) {
        $contentType = cleanLine((string) ($attachment['content_type'] ?? 'application/octet-stream'));
        $filename = cleanLine((string) ($attachment['filename'] ?? 'attachment.bin'));
        $contentId = cleanLine((string) ($attachment['content_id'] ?? 'attachment'));
        $content = (string) ($attachment['content'] ?? '');

        $parts[] = '--' . $relatedBoundary;
        $parts[] = 'Content-Type: ' . $contentType . '; name="' . $filename . '"';
        $parts[] = 'Content-Transfer-Encoding: base64';
        $parts[] = 'Content-ID: <' . $contentId . '>';
        $parts[] = 'Content-Disposition: inline; filename="' . $filename . '"';
        $parts[] = '';
        $parts[] = rtrim(chunk_split(base64_encode($content), 76, "\r\n"));
        $parts[] = '';
    }

    $parts[] = '--' . $relatedBoundary . '--';

    return [
        'headers' => [
            'MIME-Version: 1.0',
            'Content-Type: multipart/related; boundary="' . $relatedBoundary . '"',
        ],
        'body' => implode("\r\n", $parts),
    ];
}

function sendEmailViaSmtp(
    array $config,
    string $toEmail,
    string $subjectText,
    string $textBody,
    ?string $htmlBody = null,
    array $inlineAttachments = []
): bool
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
        smtpCommand($socket, 'RCPT TO:<' . $toEmail . '>', [250, 251]);
        smtpCommand($socket, 'DATA', [354]);

        $mimeMessage = buildMimeMessage($textBody, $htmlBody, $inlineAttachments);

        $headers = [
            'Date: ' . date(DATE_RFC2822),
            'Subject: ' . mimeHeader($subjectText),
            'From: ' . mailboxHeader($config['from_name'], $config['from_email']),
            'To: <' . $toEmail . '>',
            'Reply-To: ' . mailboxHeader($config['from_name'], $config['from_email']),
            'X-Mailer: RITO Outbound SMTP',
        ];
        $headers = array_merge($headers, $mimeMessage['headers']);

        $payload = implode("\r\n", $headers) . "\r\n\r\n" . dotStuff($mimeMessage['body']) . "\r\n.";
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

function sendEmailViaBrevoApi(
    array $smtpConfig,
    array $brevoConfig,
    string $toEmail,
    string $subjectText,
    string $textBody,
    ?string $htmlBody = null
): bool
{
    $payload = [
        'sender' => [
            'name' => $smtpConfig['from_name'],
            'email' => $smtpConfig['from_email'],
        ],
        'to' => [
            [
                'email' => $toEmail,
            ],
        ],
        'replyTo' => [
            'name' => $smtpConfig['from_name'],
            'email' => $smtpConfig['from_email'],
        ],
        'subject' => $subjectText,
        'textContent' => $textBody,
    ];

    if ($htmlBody !== null) {
        $payload['htmlContent'] = $htmlBody;
    }

    $encodedPayload = json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    if ($encodedPayload === false) {
        fwrite(STDERR, "Nao foi possivel montar o payload Brevo.\n");
        return false;
    }

    $curl = curl_init('https://api.brevo.com/v3/smtp/email');
    if ($curl === false) {
        fwrite(STDERR, "Nao foi possivel iniciar cURL.\n");
        return false;
    }

    curl_setopt_array($curl, [
        CURLOPT_POST => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            'accept: application/json',
            'api-key: ' . $brevoConfig['api_key'],
            'content-type: application/json',
        ],
        CURLOPT_POSTFIELDS => $encodedPayload,
        CURLOPT_TIMEOUT => 30,
    ]);

    $responseBody = curl_exec($curl);
    $httpStatus = (int) curl_getinfo($curl, CURLINFO_HTTP_CODE);
    $curlError = curl_error($curl);

    if ($responseBody === false || $httpStatus < 200 || $httpStatus >= 300) {
        $safeBody = is_string($responseBody) ? trim($responseBody) : '';
        fwrite(
            STDERR,
            'Falha Brevo API'
            . ($httpStatus > 0 ? ' HTTP ' . $httpStatus : '')
            . ($curlError !== '' ? ': ' . $curlError : '')
            . ($safeBody !== '' ? "\nResposta: " . $safeBody : '')
            . "\n"
        );
        return false;
    }

    $responseData = json_decode((string) $responseBody, true);
    if (is_array($responseData) && isset($responseData['messageId'])) {
        fwrite(STDOUT, 'Brevo messageId: ' . cleanLine((string) $responseData['messageId']) . "\n");
    }

    return true;
}

function parseArgs(array $argv): array
{
    $args = [
        'apply' => false,
        'batch_dir' => dirname(__DIR__) . '/ops/ai-os/growth/prospecting/territories/novo-hamburgo-rs/batches',
        'batch_csv' => '2026-04-21-batch-001-pilot.csv',
        'batch_json' => '2026-04-21-batch-001-outreach-data.json',
        'company_ids' => [],
        'throttle_seconds' => 60,
        'test_to' => '',
        'test_subject' => 'Teste do novo template comercial da RITO',
        'transport' => 'smtp',
    ];

    foreach ($argv as $arg) {
        if ($arg === '--apply') {
            $args['apply'] = true;
            continue;
        }
        if (strpos($arg, '--batch-csv=') === 0) {
            $args['batch_csv'] = trim((string) substr($arg, strlen('--batch-csv=')));
            continue;
        }
        if (strpos($arg, '--batch-json=') === 0) {
            $args['batch_json'] = trim((string) substr($arg, strlen('--batch-json=')));
            continue;
        }
        if (strpos($arg, '--company-ids=') === 0) {
            $ids = substr($arg, strlen('--company-ids='));
            $args['company_ids'] = array_values(array_filter(array_map('trim', explode(',', $ids))));
            continue;
        }
        if (strpos($arg, '--throttle-seconds=') === 0) {
            $args['throttle_seconds'] = max(0, (int) substr($arg, strlen('--throttle-seconds=')));
            continue;
        }
        if (strpos($arg, '--test-to=') === 0) {
            $args['test_to'] = trim((string) substr($arg, strlen('--test-to=')));
            continue;
        }
        if (strpos($arg, '--test-subject=') === 0) {
            $args['test_subject'] = trim((string) substr($arg, strlen('--test-subject=')));
            continue;
        }
        if (strpos($arg, '--transport=') === 0) {
            $args['transport'] = trim((string) substr($arg, strlen('--transport=')));
        }
    }

    if (!in_array($args['transport'], ['smtp', 'brevo-api'], true)) {
        $args['transport'] = 'smtp';
    }

    return $args;
}

function loadCsvRows(string $filePath): array
{
    $handle = fopen($filePath, 'r');
    if ($handle === false) {
        throw new RuntimeException('Nao foi possivel abrir o CSV do batch.');
    }

    $header = fgetcsv($handle, 0, ',', '"', '\\');
    if ($header === false) {
        fclose($handle);
        throw new RuntimeException('CSV vazio ou invalido.');
    }

    $rows = [];
    while (($line = fgetcsv($handle, 0, ',', '"', '\\')) !== false) {
        $row = [];
        foreach ($header as $index => $column) {
            $row[$column] = $line[$index] ?? '';
        }
        $rows[$row['company_id']] = $row;
    }
    fclose($handle);
    return $rows;
}

function loadJsonRows(string $filePath): array
{
    $raw = file_get_contents($filePath);
    if ($raw === false) {
        throw new RuntimeException('Nao foi possivel abrir o JSON de outreach.');
    }
    $items = json_decode($raw, true);
    if (!is_array($items)) {
        throw new RuntimeException('JSON de outreach invalido.');
    }
    $rows = [];
    foreach ($items as $item) {
        if (!is_array($item) || !isset($item['company_id'])) {
            continue;
        }
        $rows[$item['company_id']] = $item;
    }
    return $rows;
}

function normalizeBody(string $body): string
{
    return str_replace("\n", "\r\n", trim($body));
}

function polishPortugueseCopy(string $value): string
{
    return strtr($value, [
        'Possiveis' => 'Possíveis',
        'possiveis' => 'possíveis',
        'Ola' => 'Olá',
        'automacao' => 'automação',
        'Automacao' => 'Automação',
        'operacao' => 'operação',
        'operacoes' => 'operações',
        'Operacoes' => 'Operações',
        'organizacao' => 'organização',
        'Organizacao' => 'Organização',
        'historico' => 'histórico',
        'Historico' => 'Histórico',
        'pendencias' => 'pendências',
        'Pendencias' => 'Pendências',
        'solucoes' => 'soluções',
        'Solucoes' => 'Soluções',
        'voces' => 'vocês',
        'Voces' => 'Vocês',
        'disposicao' => 'disposição',
        'Disposicao' => 'Disposição',
        'sugestao' => 'sugestão',
        'Sugestao' => 'Sugestão',
        'orcamento' => 'orçamento',
        'orcamentos' => 'orçamentos',
        'Orcamentos' => 'Orçamentos',
        'distribuicao' => 'distribuição',
        'Distribuicao' => 'Distribuição',
        'moveis' => 'móveis',
        'Moveis' => 'Móveis',
        'mudancas' => 'mudanças',
        'Mudancas' => 'Mudanças',
        'Quimica' => 'Química',
        'quimica' => 'química',
        'Industria' => 'Indústria',
        'industria' => 'indústria',
        'Grafica' => 'Gráfica',
        'grafica' => 'gráfica',
    ]);
}

function renderHtmlTemplate(string $templatePath, array $context): string
{
    $template = file_get_contents($templatePath);
    if ($template === false) {
        throw new RuntimeException('Nao foi possivel carregar o template HTML.');
    }

    $replacements = [];
    foreach ($context as $key => $value) {
        $replacements['{{' . $key . '}}'] = (string) $value;
    }

    return strtr($template, $replacements);
}

function buildInlineBrandAttachments(): array
{
    $attachments = [];
    $logoPath = repoRootPath() . '/site/logos/rito_sistemas_wordmark_01.png';
    $monogramPath = repoRootPath() . '/site/logos/rito_monogram_r_01.png';

    $logoContent = file_get_contents($logoPath);
    if ($logoContent !== false) {
        $attachments[] = [
            'content_type' => 'image/png',
            'filename' => 'rito-wordmark.png',
            'content_id' => 'rito-wordmark',
            'content' => $logoContent,
        ];
    }

    $monogramContent = file_get_contents($monogramPath);
    if ($monogramContent !== false) {
        $attachments[] = [
            'content_type' => 'image/png',
            'filename' => 'rito-monogram.png',
            'content_id' => 'rito-monogram',
            'content' => $monogramContent,
        ];
    }

    return $attachments;
}

function brandImageUrls(string $transport): array
{
    if ($transport === 'brevo-api') {
        return [
            'wordmark' => 'https://ritosistemas.com/logos/rito_sistemas_wordmark_01.png',
            'monogram' => 'https://ritosistemas.com/logos/rito_monogram_r_01.png',
        ];
    }

    return [
        'wordmark' => 'cid:rito-wordmark',
        'monogram' => 'cid:rito-monogram',
    ];
}

function appendQueryParams(string $url, array $params): string
{
    $filtered = [];
    foreach ($params as $key => $value) {
        $value = cleanLine((string) $value);
        if ($value !== '') {
            $filtered[$key] = $value;
        }
    }

    if ($filtered === []) {
        return $url;
    }

    $separator = str_contains($url, '?') ? '&' : '?';
    return $url . $separator . http_build_query($filtered, '', '&', PHP_QUERY_RFC3986);
}

function campaignSlugFromBatch(string $batchCsv): string
{
    $name = preg_replace('/\.csv$/', '', basename($batchCsv)) ?: 'outbound-email';
    $name = strtolower((string) preg_replace('/[^a-zA-Z0-9]+/', '_', $name));
    return trim($name, '_') ?: 'outbound_email';
}

function trackedUrl(string $url, string $campaign, string $content): string
{
    return appendQueryParams($url, [
        'utm_id' => $campaign,
        'utm_source' => 'brevo',
        'utm_medium' => 'email',
        'utm_campaign' => $campaign,
        'utm_source_platform' => 'brevo',
        'utm_content' => $content,
    ]);
}

function trackedTextBody(string $body, array $csv, string $campaign): string
{
    $companyId = cleanLine((string) ($csv['company_id'] ?? 'unknown'));
    return strtr($body, [
        'https://ritosistemas.com/pages/projeto-piloto.html' => trackedUrl(
            'https://ritosistemas.com/pages/projeto-piloto.html',
            $campaign,
            $companyId . '_pilot_text'
        ),
        'https://ritosistemas.com' => trackedUrl(
            'https://ritosistemas.com',
            $campaign,
            $companyId . '_site_text'
        ),
    ]);
}

function titleCaseFront(string $value): string
{
    $value = trim(polishPortugueseCopy($value));
    if ($value === '') {
        return 'Solução sob medida';
    }

    $value = mb_convert_case($value, MB_CASE_TITLE, 'UTF-8');
    $replacements = [
        'Crm' => 'CRM',
        'B2B' => 'B2B',
        'Os' => 'OS',
    ];

    return strtr($value, $replacements);
}

function frontDescription(string $front): string
{
    $normalized = mb_strtolower(trim(polishPortugueseCopy($front)), 'UTF-8');

    $map = [
        'entrada e triagem de demandas' => 'Organizar melhor o primeiro contato, a leitura da demanda e o encaminhamento interno.',
        'triagem de demandas' => 'Dar mais clareza ao primeiro contato, à classificação da demanda e ao próximo passo do atendimento.',
        'organização de contatos e histórico' => 'Concentrar informações, interações e contexto para não depender de memória ou troca dispersa.',
        'acompanhamento comercial' => 'Acompanhar oportunidades, retornos e próximos passos com mais previsibilidade.',
        'crm consultivo' => 'Estruturar o relacionamento com clientes e oportunidades em uma base simples e útil para o dia a dia.',
        'painéis internos' => 'Reunir informações operacionais em uma visão mais clara para acompanhamento e tomada de decisão.',
        'painel interno de leads' => 'Dar visibilidade ao funil de contatos, retornos e prioridades da equipe.',
        'organização documental' => 'Reduzir dispersão de arquivos e facilitar acesso ao que importa em cada atendimento.',
        'dashboard gerencial' => 'Trazer indicadores e status da operação para uma leitura mais rápida no dia a dia.',
        'dashboards gerenciais' => 'Trazer indicadores e status da operação para uma leitura mais rápida no dia a dia.',
        'dashboards operacionais' => 'Dar visibilidade ao que está acontecendo na operação sem depender de planilhas soltas.',
        'onboarding de clientes' => 'Organizar melhor a entrada de novos clientes, documentos e etapas recorrentes.',
        'briefing e entrada de demandas' => 'Registrar necessidades com mais consistência desde o início do relacionamento.',
        'briefing de demandas' => 'Transformar a entrada de demandas em algo mais claro, rastreável e fácil de acompanhar.',
        'site institucional ou renovação do site atual' => 'Fortalecer a apresentação da empresa com uma base digital própria mais alinhada ao negócio.',
        'crm leve' => 'Acompanhar contatos e retornos com uma estrutura simples, sem peso de ferramenta corporativa.',
        'funil de agendamento odontológico' => 'Organizar melhor avaliação, agenda e retorno para não perder oportunidades no caminho.',
        'crm leve e follow-up' => 'Manter o histórico e o retorno ao paciente de forma mais consistente.',
        'painel de atendimento' => 'Dar visão rápida sobre agenda, contatos e andamento dos atendimentos.',
        'triagem inicial e agendamento' => 'Deixar a entrada do paciente mais organizada entre interesse, agenda e confirmação.',
        'crm de relacionamento' => 'Manter histórico de clientes, preferências e retornos em uma base simples e acionável.',
        'controles operacionais' => 'Acompanhar melhor rotinas internas, execução e pontos que hoje ficam dispersos.',
        'captação e relacionamento' => 'Organizar melhor a entrada de interessados e o retorno comercial no tempo certo.',
        'painel de alunos' => 'Dar visibilidade a captação, recorrência e acompanhamento da base ativa.',
        'agenda de avaliações' => 'Estruturar melhor avaliação inicial, retorno e próximos passos.',
        'catálogo e pedidos' => 'Centralizar melhor produtos, pedidos e contatos para reduzir atrito no atendimento.',
        'crm simples' => 'Acompanhar contatos e pedidos com uma estrutura leve e mais organizada.',
        'atendimento e orçamentos' => 'Dar mais clareza à entrada de pedidos, orçamentos e retornos comerciais.',
        'painel operacional' => 'Reunir status, fluxo e acompanhamento da operação em uma visão mais objetiva.',
        'agendamento e relacionamento' => 'Organizar agenda, confirmações e relacionamento recorrente com mais consistência.',
        'crm b2b e orçamentos' => 'Estruturar melhor proposta, relacionamento e acompanhamento de contas B2B.',
        'pipeline de propostas' => 'Dar mais visibilidade ao andamento de propostas, retornos e prioridades comerciais.',
        'atendimento e ordens de serviço' => 'Organizar chamados, execução e histórico técnico sem depender de processos soltos.',
        'pós-venda e relacionamento' => 'Manter o cliente por perto com histórico, retorno e continuidade mais bem organizados.',
        'follow-up de contatos' => 'Garantir que contatos recebam continuidade e não se percam entre canais.',
        'controles administrativos' => 'Trazer mais previsibilidade para rotinas internas e acompanhamento operacional.',
    ];

    return $map[$normalized] ?? 'Transformar essa frente em uma rotina mais clara, previsível e adaptada ao negócio.';
}

function buildHtmlContextPhrase(array $fronts): string
{
    $normalized = array_map(
        static fn(string $value): string => mb_strtolower(trim($value), 'UTF-8'),
        array_values(array_filter($fronts, static fn($value): bool => trim((string) $value) !== ''))
    );

    $needles = implode(' | ', $normalized);

    if (str_contains($needles, 'agendamento') || str_contains($needles, 'paciente')) {
        return 'agilidade no atendimento, organização da agenda e retorno ao cliente';
    }
    if (str_contains($needles, 'orçamento') || str_contains($needles, 'proposta') || str_contains($needles, 'b2b')) {
        return 'clareza comercial, acompanhamento de propostas e previsibilidade no retorno';
    }
    if (str_contains($needles, 'ordens de serviço') || str_contains($needles, 'os') || str_contains($needles, 'técnic')) {
        return 'controle de atendimento, histórico técnico e visibilidade operacional';
    }
    if (str_contains($needles, 'alunos') || str_contains($needles, 'captação') || str_contains($needles, 'avalia')) {
        return 'captação organizada, acompanhamento recorrente e visibilidade da base ativa';
    }
    if (str_contains($needles, 'pedido') || str_contains($needles, 'catálogo') || str_contains($needles, 'atendimento')) {
        return 'atendimento mais claro, acompanhamento de pedidos e relacionamento contínuo';
    }

    return 'organização de demanda, acompanhamento recorrente e visibilidade da operação';
}

function buildHtmlHeadline(array $csv): string
{
    $segment = trim((string) ($csv['segment'] ?? ''));
    $segment = str_replace('-', ' ', $segment);

    if ($segment !== '') {
        $segment = mb_strtolower($segment, 'UTF-8');
        return 'Possibilidades de software que podem fortalecer a rotina da ' . $segment . '.';
    }

    return 'Possibilidades de software que podem fortalecer a rotina de vocês.';
}

function buildRealHtmlEmail(
    array $csv,
    array $json,
    string $subjectText,
    string $transport = 'smtp',
    string $campaign = 'outbound_email'
): array
{
    $templatePath = repoRootPath() . '/ops/ai-os/email/templates/prospecting-outbound-email-template-v2.html';
    $fronts = array_values(array_filter(
        array_map(
            static fn($value): string => trim((string) $value),
            (array) ($json['suggested_solution_fronts'] ?? [])
        ),
        static fn(string $value): bool => $value !== ''
    ));

    while (count($fronts) < 4) {
        $fronts[] = 'solução sob medida';
    }
    $fronts = array_slice($fronts, 0, 4);

    $replySubject = 'Resposta · ' . $subjectText;
    $clientContext = buildHtmlContextPhrase($fronts);
    $clientSegment = 'operação como a da ' . trim((string) ($csv['company_name'] ?? 'sua empresa'));
    $brandImages = brandImageUrls($transport);
    $companyId = cleanLine((string) ($csv['company_id'] ?? 'unknown'));
    $siteUrl = trackedUrl('https://ritosistemas.com', $campaign, $companyId . '_site_html');
    $instagramUrl = trackedUrl('https://www.instagram.com/ritosistemas/', $campaign, $companyId . '_instagram_html');

    $htmlBody = renderHtmlTemplate($templatePath, [
        'CLIENTE_NOME' => trim((string) ($csv['company_name'] ?? 'Cliente')),
        'CLIENTE_SEGMENTO' => $clientSegment,
        'CLIENTE_CONTEXTO' => $clientContext,
        'ASSUNTO_RESPOSTA' => rawurlencode($replySubject),
        'EMAIL_HEADLINE' => polishPortugueseCopy(buildHtmlHeadline($csv)),
        'FRENTE_01_TITULO' => titleCaseFront($fronts[0]),
        'FRENTE_01_DESCRICAO' => frontDescription($fronts[0]),
        'FRENTE_02_TITULO' => titleCaseFront($fronts[1]),
        'FRENTE_02_DESCRICAO' => frontDescription($fronts[1]),
        'FRENTE_03_TITULO' => titleCaseFront($fronts[2]),
        'FRENTE_03_DESCRICAO' => frontDescription($fronts[2]),
        'FRENTE_04_TITULO' => titleCaseFront($fronts[3]),
        'FRENTE_04_DESCRICAO' => frontDescription($fronts[3]),
        'SITE_URL' => $siteUrl,
        'INSTAGRAM_URL' => $instagramUrl,
        'REPLY_EMAIL' => 'comercial@ritosistemas.com',
        'WORDMARK_URL' => $brandImages['wordmark'],
        'MONOGRAM_URL' => $brandImages['monogram'],
    ]);

    return [
        'html_body' => normalizeBody($htmlBody),
        'inline_attachments' => buildInlineBrandAttachments(),
    ];
}

function buildTestHtmlEmailPreview(string $subjectText, string $transport = 'smtp'): array
{
    $templatePath = repoRootPath() . '/ops/ai-os/email/templates/prospecting-outbound-email-template-v2.html';
    $brandImages = brandImageUrls($transport);
    $siteUrl = trackedUrl('https://ritosistemas.com', 'email_test', 'test_site_html');
    $instagramUrl = trackedUrl('https://www.instagram.com/ritosistemas/', 'email_test', 'test_instagram_html');

    $textBody = normalizeBody(implode("\n\n", [
        'Olá, tudo bem?',
        'Sou da RITO Sistemas.',
        'Este é um teste visual do novo formato de e-mail comercial da RITO. A proposta é manter o e-mail leve, institucional e mais profissional no recebimento.',
        "Frentes exibidas neste modelo:\n- software sob medida para rotinas específicas\n- automações e integrações\n- dashboards e controles internos\n- renovação de site quando fizer sentido",
        'Se essa linha visual fizer sentido para vocês, o próximo passo é adaptar os envios reais da prospecção para usar este formato em HTML junto com a versão texto.',
        'Site: https://ritosistemas.com',
        'Instagram: https://www.instagram.com/ritosistemas/',
        "Atenciosamente,\nRITO Sistemas\ncomercial@ritosistemas.com",
    ]));

    $replySubject = 'Resposta · Teste do template comercial da RITO';
    $htmlBody = renderHtmlTemplate($templatePath, [
        'CLIENTE_NOME' => 'Dieison',
        'CLIENTE_SEGMENTO' => 'operação comercial em avaliação',
        'CLIENTE_CONTEXTO' => 'clareza de proposta, leitura rápida e confiança visual',
        'ASSUNTO_RESPOSTA' => rawurlencode($replySubject),
        'EMAIL_HEADLINE' => 'Possibilidades de software que podem fortalecer a rotina de vocês.',
        'FRENTE_01_TITULO' => 'Software sob medida',
        'FRENTE_01_DESCRICAO' => 'Ferramentas desenhadas para a rotina real da empresa, sem pacote genérico pesado.',
        'FRENTE_02_TITULO' => 'Automações e integrações',
        'FRENTE_02_DESCRICAO' => 'Reduzir trabalho manual entre atendimento, operação e acompanhamento comercial.',
        'FRENTE_03_TITULO' => 'Dashboards e controles internos',
        'FRENTE_03_DESCRICAO' => 'Organizar melhor informações, indicadores e visibilidade do que acontece no dia a dia.',
        'FRENTE_04_TITULO' => 'Base digital mais forte',
        'FRENTE_04_DESCRICAO' => 'Quando fizer sentido, renovar site, organizar canais e melhorar a apresentação institucional.',
        'SITE_URL' => $siteUrl,
        'INSTAGRAM_URL' => $instagramUrl,
        'REPLY_EMAIL' => 'comercial@ritosistemas.com',
        'WORDMARK_URL' => $brandImages['wordmark'],
        'MONOGRAM_URL' => $brandImages['monogram'],
    ]);

    return [
        'text_body' => $textBody,
        'html_body' => normalizeBody($htmlBody),
        'inline_attachments' => buildInlineBrandAttachments(),
    ];
}

$args = parseArgs(array_slice($argv, 1));
$batchDir = rtrim($args['batch_dir'], '/');
$csvPath = $batchDir . '/' . $args['batch_csv'];
$jsonPath = $batchDir . '/' . $args['batch_json'];
$campaignSlug = campaignSlugFromBatch($args['batch_csv']);

$csvRows = loadCsvRows($csvPath);
$jsonRows = loadJsonRows($jsonPath);
$smtpConfig = loadOutboundSmtpConfig();
$brevoConfig = $args['transport'] === 'brevo-api' ? loadBrevoApiConfig() : null;

if ($smtpConfig === null) {
    fwrite(STDERR, "Configuracao SMTP invalida ou ausente.\n");
    exit(1);
}

if ($args['transport'] === 'brevo-api' && $brevoConfig === null) {
    fwrite(STDERR, "Configuracao Brevo API invalida ou ausente.\n");
    exit(1);
}

if ($args['apply'] === true && $args['transport'] === 'smtp') {
    try {
        assertSmtpTransportComplete($smtpConfig);
        assertCampaignTransportAllowed($smtpConfig);
    } catch (Throwable $exception) {
        fwrite(STDERR, $exception->getMessage() . "\n");
        exit(1);
    }
}

if ($args['test_to'] !== '') {
    $testTo = cleanLine($args['test_to']);
    if (filter_var($testTo, FILTER_VALIDATE_EMAIL) === false) {
        fwrite(STDERR, "Endereco de teste invalido.\n");
        exit(1);
    }

    $preview = buildTestHtmlEmailPreview($args['test_subject'], $args['transport']);
    fwrite(STDOUT, '[TEST] ' . $testTo . "\n");
    fwrite(STDOUT, 'Assunto: ' . $args['test_subject'] . "\n");

    if ($args['apply'] !== true) {
        fwrite(STDOUT, "Modo dry-run. Nenhum e-mail foi enviado.\n");
        exit(0);
    }

    if ($args['transport'] === 'brevo-api') {
        $sent = sendEmailViaBrevoApi(
            $smtpConfig,
            $brevoConfig,
            $testTo,
            $args['test_subject'],
            $preview['text_body'],
            $preview['html_body']
        );
    } else {
        $sent = sendEmailViaSmtp(
            $smtpConfig,
            $testTo,
            $args['test_subject'],
            $preview['text_body'],
            $preview['html_body'],
            $preview['inline_attachments']
        );
    }

    fwrite(STDOUT, $sent ? "Enviado com sucesso.\n" : "Falha no envio.\n");
    exit($sent ? 0 : 1);
}

$selectedIds = $args['company_ids'];
if ($selectedIds === []) {
    $selectedIds = array_keys($jsonRows);
}

$queue = [];
foreach ($selectedIds as $companyId) {
    $csv = $csvRows[$companyId] ?? null;
    $json = $jsonRows[$companyId] ?? null;
    if ($csv === null || $json === null) {
        continue;
    }
    if (($json['recommended_channel'] ?? '') !== 'email') {
        continue;
    }
    $email = trim((string) ($csv['public_email'] ?? ''));
    $subject = polishPortugueseCopy(trim((string) ($json['email_subject'] ?? '')));
    $body = polishPortugueseCopy(trim((string) ($json['email_body'] ?? '')));
    if ($email === '' || $subject === '' || $body === '') {
        continue;
    }
    $queue[] = [
        'company_id' => $companyId,
        'company_name' => $csv['company_name'] ?? $companyId,
        'to' => $email,
        'subject' => $subject,
        'body' => normalizeBody(trackedTextBody($body, $csv, $campaignSlug)),
        'csv' => $csv,
        'json' => $json,
    ];
}

if ($queue === []) {
    fwrite(STDOUT, "Nenhum e-mail elegivel encontrado para envio.\n");
    exit(0);
}

foreach ($queue as $index => $item) {
    fwrite(STDOUT, '[' . ($index + 1) . '/' . count($queue) . '] ' . $item['company_name'] . ' <' . $item['to'] . ">\n");
    fwrite(STDOUT, 'Assunto: ' . $item['subject'] . "\n");
    if ($args['apply'] !== true) {
        fwrite(STDOUT, "Modo dry-run. Nenhum e-mail foi enviado.\n\n");
        continue;
    }

    $htmlPayload = null;
    $inlineAttachments = [];
    try {
        $preview = buildRealHtmlEmail(
            $item['csv'],
            $item['json'],
            $item['subject'],
            $args['transport'],
            $campaignSlug
        );
        $htmlPayload = $preview['html_body'] ?? null;
        $inlineAttachments = $preview['inline_attachments'] ?? [];
    } catch (Throwable $exception) {
        $htmlPayload = null;
        $inlineAttachments = [];
    }

    if ($args['transport'] === 'brevo-api') {
        $sent = sendEmailViaBrevoApi(
            $smtpConfig,
            $brevoConfig,
            $item['to'],
            $item['subject'],
            $item['body'],
            $htmlPayload
        );
    } else {
        $sent = sendEmailViaSmtp(
            $smtpConfig,
            $item['to'],
            $item['subject'],
            $item['body'],
            $htmlPayload,
            $inlineAttachments
        );
    }
    fwrite(STDOUT, $sent ? "Enviado com sucesso.\n\n" : "Falha no envio.\n\n");

    if ($args['throttle_seconds'] > 0 && $index < count($queue) - 1) {
        sleep((int) $args['throttle_seconds']);
    }
}
