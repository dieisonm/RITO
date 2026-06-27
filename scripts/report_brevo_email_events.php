<?php

declare(strict_types=1);

function repoRootPath(): string
{
    return dirname(__DIR__);
}

function loadBrevoApiKey(): string
{
    $secretsFile = repoRootPath() . '/rito-secrets.local.php';
    if (!is_file($secretsFile)) {
        return '';
    }

    $secrets = require $secretsFile;
    if (!is_array($secrets)) {
        return '';
    }

    return trim((string) ($secrets['brevo_api']['api_key'] ?? ''));
}

function parseArgs(array $argv): array
{
    $args = [
        'days' => 7,
        'limit' => 500,
    ];

    foreach ($argv as $arg) {
        if (strpos($arg, '--days=') === 0) {
            $args['days'] = max(1, (int) substr($arg, strlen('--days=')));
        }
        if (strpos($arg, '--limit=') === 0) {
            $args['limit'] = max(1, min(500, (int) substr($arg, strlen('--limit='))));
        }
    }

    return $args;
}

function fetchBrevoEvents(string $apiKey, int $days, int $limit): array
{
    $url = 'https://api.brevo.com/v3/smtp/statistics/events?'
        . http_build_query([
            'limit' => $limit,
            'offset' => 0,
            'days' => $days,
        ]);

    $curl = curl_init($url);
    if ($curl === false) {
        throw new RuntimeException('Nao foi possivel iniciar cURL.');
    }

    curl_setopt_array($curl, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            'accept: application/json',
            'api-key: ' . $apiKey,
        ],
        CURLOPT_TIMEOUT => 30,
    ]);

    $body = curl_exec($curl);
    $status = (int) curl_getinfo($curl, CURLINFO_HTTP_CODE);
    if (!is_string($body) || $status < 200 || $status >= 300) {
        throw new RuntimeException('Falha ao consultar Brevo. HTTP ' . $status);
    }

    $data = json_decode($body, true);
    if (!is_array($data)) {
        throw new RuntimeException('Resposta invalida da Brevo.');
    }

    $events = $data['events'] ?? $data;
    return is_array($events) ? $events : [];
}

$args = parseArgs(array_slice($argv, 1));
$apiKey = loadBrevoApiKey();
if ($apiKey === '') {
    fwrite(STDERR, "Brevo API key ausente em rito-secrets.local.php.\n");
    exit(1);
}

try {
    $events = fetchBrevoEvents($apiKey, $args['days'], $args['limit']);
} catch (Throwable $exception) {
    fwrite(STDERR, $exception->getMessage() . "\n");
    exit(1);
}

$counts = [];
$clicks = [];
$notable = [];

foreach ($events as $event) {
    if (!is_array($event)) {
        continue;
    }

    $eventName = (string) ($event['event'] ?? 'unknown');
    $counts[$eventName] = ($counts[$eventName] ?? 0) + 1;

    if (in_array($eventName, ['clicks', 'uniqueClicks'], true)) {
        $clicks[] = $event;
    }

    if (in_array($eventName, ['error', 'softBounces', 'hardBounces', 'blocked', 'deferred'], true)) {
        $notable[] = $event;
    }
}

ksort($counts);

echo '# Brevo transactional events - last ' . $args['days'] . " day(s)\n\n";
foreach ($counts as $eventName => $count) {
    echo '- ' . $eventName . ': ' . $count . "\n";
}

echo "\n## Clicks\n\n";
if ($clicks === []) {
    echo "Nenhum clique registrado no periodo.\n";
} else {
    foreach ($clicks as $event) {
        echo '- '
            . ($event['date'] ?? '')
            . ' | ' . ($event['email'] ?? '')
            . ' | ' . ($event['link'] ?? $event['url'] ?? '')
            . ' | ' . ($event['subject'] ?? '')
            . "\n";
    }
}

echo "\n## Atencao\n\n";
if ($notable === []) {
    echo "Nenhum erro/bounce/deferred registrado no periodo.\n";
} else {
    foreach ($notable as $event) {
        echo '- '
            . ($event['date'] ?? '')
            . ' | ' . ($event['event'] ?? '')
            . ' | ' . ($event['email'] ?? '')
            . ' | ' . ($event['reason'] ?? '')
            . "\n";
    }
}
