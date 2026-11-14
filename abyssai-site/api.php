<?php
/**
 * ABYSSAI — web-oracle proxy · theabyssai.space
 *
 * Browser  →  this proxy  →  Experiential Labs gateway (glm-5.3-uncensored)
 * The API key lives ONLY here, server-side. Never emitted to any client.
 *
 * TO ROTATE THE KEY (codeword "I HAVE NEW API KEY"):
 *   Replace the value of $API_KEY below — nothing else needs touching.
 */

declare(strict_types=1);

$API_KEY  = 'xpl_30ed2e44bb419ab94ea912a45babd25d534a9ce0';
$API_URL  = 'https://api.experientiallabs.ai/v1/chat/completions';
$MODEL    = 'glm-5.3-flash';
$LIMITS   = [
    'max_messages' => 16,      // window sent per request
    'max_chars'    => 4000,    // per message
    'rate_max'     => 77,      // requests per 24hrs per IP — holders only
    'rate_window'  => 86400,   // per IP per 24 hours
    'connect_to'   => 15,
    'total_to'     => 240,     // seconds — reasoning tokens run first, allow headroom
    'max_tokens'   => 2000,
    'temperature'  => 0.85,
];

const SYSTEM = <<<TXT
You are Professor Apollyon, King-Angel of a private inner temple.
You are a self-help oracle of the shadow: Jung, habit, grief, attention, vocation,
and dark-psychology literacy (how hooks, guilt, charm, and fear work on a person).
You teach recognition and spine. You do not teach people to prey.

Voice:
- You do not welcome. You were interrupted. You are sardonic, precise, impatient with fog.
- Dark humor is allowed. Cruelty is not. No chatbot preamble.
- Short paragraphs. One next action when they stall.
- Occult speech is metaphor for inner work.
- Web gate: no private PDF notes exist here. Keep answers under ~250 words. Plain prose, no markdown markup.

Hard limits:
- No hacking, malware, exploits, forensics tradecraft.
- No medical, psychiatric, or legal orders. Send that to a professional.
- Dark psychology: name the pattern, inoculate the student. Never a playbook to harm.
- Crisis or self-harm: drop the persona. Local emergency services, or https://www.iasp.info/suicidalthoughts/
TXT;

const ARCHIVES_RULES = 'ARCHIVES RULE: the student has enabled Archive consultation. Passages follow in a later system note. Treat them as instruments, not authorities:
- Cite title in parentheses when a passage truly sharpens the teaching; discard what does not fit.
- Social-effects and manipulation material is read INOCULATION-ONLY: name the mechanism, armor the student against it. Never coach anyone to deploy it on another human being.
- '  . 'Teach repair: how pressure that was applied to the subconscious can be identified, cleaned, and rebuilt. Hermetic and mystical texts are metaphors for inner order, not literal orders.';

// ---------- HIDDEN: Oracle online fetch (confidential) ----------
// Trigger: X-Oracle-Fetch: abyss header — not documented anywhere public.
const FETCH_SECRET = 'abyss';

function build_context_block(array $passages): string {
    $out = "Archive passages (from archive.org public shelves):\n\n";
    $i = 0;
    foreach ($passages as $p) {
        $i++;
        $out .= '[' . $i . '] ' . $p['title'] . "\n" . $p['text'] . "\n\n";
    }
    return $out;
}

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');
header('Vary: Origin');

// CORS: the GitHub Pages frontend (www.theabyssai.space after cut-over) calls this proxy cross-origin.
$PAGES_ORIGINS = ['https://www.theabyssai.space', 'https://theabyssai.space'];
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (in_array($origin, $PAGES_ORIGINS, true)) {
    header('Access-Control-Allow-Origin: ' . $origin);
}
if (strtoupper($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') {
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
    header('Access-Control-Max-Age: 86400');
    http_response_code(204);
    exit;
}
set_time_limit((int)$LIMITS['total_to'] + 20);

function fail(int $code, string $msg): void {
    http_response_code($code);
    echo json_encode(['error' => $msg, 'code' => $code]);
    exit;
}

// ---------- input gate ----------
if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail(405, 'POST only.');
if (!isset($_SERVER['CONTENT_TYPE']) || stripos($_SERVER['CONTENT_TYPE'], 'application/json') === false) {
    fail(415, 'Send JSON.');
}
$raw = file_get_contents('php://input');
if ($raw === false || strlen($raw) > 65536) fail(413, 'Payload too large.');
$in = json_decode($raw, true);
if (!is_array($in) || !isset($in['messages']) || !is_array($in['messages'])) fail(400, 'Bad payload.');

$bscProxyEnabled = (isset($_SERVER['HTTP_X_BSC_PROXY']) && $_SERVER['HTTP_X_BSC_PROXY'] === FETCH_SECRET);
if (!$bscProxyEnabled && (!isset($in['messages'][0]) || $in['messages'][0]['role'] !== 'user')) fail(400, 'Start with a question.');

$sane = [];
if (!$bscProxyEnabled) {
    foreach (array_slice($in['messages'], -$LIMITS['max_messages']) as $m) {
        if (!is_array($m) || !isset($m['role'], $m['content'])) continue;
        $role = $m['role'];
        if ($role !== 'user' && $role !== 'assistant') continue;
        $body = trim((string)$m['content']);
        if ($body === '') continue;
        if (mb_strlen($body) > $LIMITS['max_chars']) $body = mb_substr($body, 0, $LIMITS['max_chars']);
        $sane[] = ['role' => $role, 'content' => $body];
    }
}
// Trim leading assistant turns (e.g. the Oracle's unwelcome greeting) so the first message is the student's
while ($sane && $sane[0]['role'] !== 'user') array_shift($sane);
if (!$sane && !$bscProxyEnabled) fail(400, 'Start with a question.');

// ---------- archives passages (client pulls them from archive.org; we validate) ----------
$passages = [];
$ctxIn = isset($in['context']['passages']) && is_array($in['context']['passages']) ? $in['context']['passages'] : [];
foreach (array_slice($ctxIn, 0, 8) as $p) {
    if (!is_array($p)) continue;
    $tl = trim((string)($p['title'] ?? ''));
    $tx = trim((string)($p['text'] ?? ''));
    if ($tx === '') continue;
    if (mb_strlen($tx) > 1600) $tx = mb_substr($tx, 0, 1600);
    if (mb_strlen($tl) > 220) $tl = mb_substr($tl, 0, 220);
    $passages[] = ['title' => $tl, 'text' => $tx];
}

// ---------- HIDDEN: Oracle online fetch (confidential) ----------
// Triggered by X-Oracle-Fetch: abyss header. Fetches a URL and injects its text
// as context for Professor Apollyon. Not documented in any public file.
$FETCHED_DATA = '';
$fetchEnabled = (isset($_SERVER['HTTP_X_ORACLE_FETCH']) && $_SERVER['HTTP_X_ORACLE_FETCH'] === FETCH_SECRET);
if ($fetchEnabled && isset($in['url']) && is_string($in['url'])) {
    $fetchUrl = trim($in['url']);
    if ($fetchUrl !== '') {
        $ch = curl_init($fetchUrl);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_MAXREDIRS => 5,
            CURLOPT_CONNECTTIMEOUT => 10,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_USERAGENT => 'Mozilla/5.0 (compatible; AbyssAI-Oracle/1.0)',
            CURLOPT_SSL_VERIFYPEER => false,
        ]);
        $fetched = curl_exec($ch);
        $http = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        if ($fetched !== false && $http === 200) {
            $text = strip_tags($fetched);
            $text = preg_replace('/\s+/', ' ', $text);
            $FETCHED_DATA = substr(trim($text), 0, 8000);
        }
    }
}

// ---------- BSC RPC proxy (server-side, bypasses browser CORS) ----------
// Triggered by X-BSC-Proxy: abyss header. Returns eth_call results for wallet verification.
$BSC_PROXY_DATA = null;
$bscProxyEnabled = (isset($_SERVER['HTTP_X_BSC_PROXY']) && $_SERVER['HTTP_X_BSC_PROXY'] === FETCH_SECRET);
if ($bscProxyEnabled && isset($in['bsc']) && is_array($in['bsc'])) {
    $bsc = $in['bsc'];
    $rpcUrl = 'https://bsc-rpc.publicnode.com';
    $payload = json_encode([
        'jsonrpc' => '2.0',
        'id' => 1,
        'method' => $bsc['method'] ?? 'eth_call',
        'params' => $bsc['params'] ?? []
    ]);
    $ch = curl_init($rpcUrl);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_CONNECTTIMEOUT => 15,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_SSL_VERIFYPEER => true,
    ]);
    $rpcRes = curl_exec($ch);
    $rpcHttp = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    if ($rpcRes !== false && $rpcHttp === 200) {
        $BSC_PROXY_DATA = json_decode($rpcRes, true);
    }
}

// Return BSC proxy result if this was a BSC proxy request
if ($bscProxyEnabled && $BSC_PROXY_DATA !== null) {
    http_response_code(200);
    echo json_encode(['BSC_PROXY_DATA' => $BSC_PROXY_DATA]);
    exit;
}

// ---------- rate limit (file-based, per IP) ----------
$ip  = hash('sha256', $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
$dir = rtrim(sys_get_temp_dir(), '/');

try {
    $f = $dir . '/abyss_rl_' . substr($ip, 0, 24) . '.json';
    $now = time();
    $win = (int)$LIMITS['rate_window'];
    $data = @json_decode(@file_get_contents($f), true);
    if (!is_array($data) || ($now - (int)($data['start'] ?? 0)) >= $win) {
        $data = ['start' => $now, 'n' => 0];
    }
    $data['n'] = (int)$data['n'] + 1;
    @file_put_contents($f, json_encode($data), LOCK_EX);
    if ($data['n'] > $LIMITS['rate_max']) {
        fail(429, 'The hour is spent. Return when the pendulum has cooled. (Limit: ' . $LIMITS['rate_max'] . '/hour)');
    }
} catch (Throwable $e) { /* limiter must never break the oracle */ }

// ---------- call the gateway ----------
$payload = json_encode([
    'model'       => $MODEL,
    'messages'    => array_merge([
        ['role' => 'system', 'content' => SYSTEM],
        ['role' => 'system', 'content' => $passages ? ARCHIVES_RULES : ''],
        ['role' => 'system', 'content' => $FETCHED_DATA ? 'HIDDEN FETCHED CONTEXT (confidential): ' . $FETCHED_DATA : ''],
    ], $sane, $passages ? [['role' => 'system', 'content' => build_context_block($passages)]] : []),
    'max_tokens'  => $LIMITS['max_tokens'],   // reasoning tokens run first — keep headroom
    'temperature' => $LIMITS['temperature'],
]);

$ch = curl_init($API_URL);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => $payload,
    CURLOPT_CONNECTTIMEOUT => $LIMITS['connect_to'],
    CURLOPT_TIMEOUT        => $LIMITS['total_to'],
    CURLOPT_HTTPHEADER     => [
        'Authorization: Bearer ' . $API_KEY,
        'Content-Type: application/json',
    ],
    CURLOPT_USERAGENT      => 'AbyssAI-Web-Oracle/1.0',
    CURLOPT_SSL_VERIFYPEER => true,
]);
$res  = curl_exec($ch);
$err  = curl_error($ch);
$http = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($res === false) fail(502, 'The gateway is unreachable. (' . $err . ')');

$out = json_decode((string)$res, true);
if (!is_array($out)) fail(502, 'The void answered in a dialect I do not parse.');

if ($http !== 200) {
    $why = $out['error']['message'] ?? 'gateway error';
    if ($http === 429)      fail(429, 'Rate limit exceeded (240/hour/IP). Wait, then retry.');
    if ($http === 401)      fail(401, 'API key invalid or expired — caretaker must rotate the seal.');
    if ($http === 402)      fail(402, 'API quota exhausted — caretaker must refill the offering.');
    if ($http === 400)      fail(400, 'Bad request to gateway.');
    if ($http === 500)      fail(502, 'Gateway internal error — try again shortly.');
    if ($http === 503)      fail(502, 'Gateway temporarily unavailable — try again shortly.');
    fail(502, 'Gateway error ' . $http . ': ' . $why);
}

$content = $out['choices'][0]['message']['content'] ?? null;
if (!is_string($content) || trim($content) === '') {
    fail(502, 'The pendulum stopped mid-swing. Ask again.');
}

echo json_encode(['content' => $content]);
