<?php
header('Content-Type: application/json');

$passphrase = $_REQUEST['passphrase'] ?? '';
$message = $_REQUEST['message'] ?? '';

if ($passphrase !== 'kR9x$mTv!pL3nQ7w') {
    http_response_code(403);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

if (empty($message)) {
    http_response_code(400);
    echo json_encode(['error' => 'Message required']);
    exit;
}

$to = 'andrewmcromar@gmail.com';
$subject = 'Portfolio Deploy Monitor';
$headers = 'From: noreply@andrewcromar.org';

$sent = mail($to, $subject, $message, $headers);

echo json_encode(['success' => $sent]);
