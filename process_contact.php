<?php
// Sécurité stricte
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: SAMEORIGIN');
ini_set('display_errors', 0);
error_reporting(E_ALL);

// Configuration
define('RATE_LIMIT', 5); // 5 tentatives
define('RATE_LIMIT_WINDOW', 3600); // par heure
define('MAX_EMAIL_LENGTH', 254);
define('MAX_NAME_LENGTH', 100);
define('MAX_MESSAGE_LENGTH', 5000);
define('ALLOWED_MIME_TYPES', ['text/plain', 'application/json']);

// Session de sécurité
session_start();
session_regenerate_id(true);

function sanitizeInput($input, $maxLength) {
    $input = trim($input);
    $input = stripslashes($input);
    $input = substr($input, 0, $maxLength);
    return htmlspecialchars($input, ENT_QUOTES, 'UTF-8');
}

function validateEmail($email) {
    $email = filter_var($email, FILTER_SANITIZE_EMAIL);
    if (filter_var($email, FILTER_VALIDATE_EMAIL) && strlen($email) <= MAX_EMAIL_LENGTH) {
        return $email;
    }
    return false;
}

function checkRateLimit($ip) {
    $filename = sys_get_temp_dir() . '/rate_limit_' . md5($ip);
    if (file_exists($filename)) {
        $data = json_decode(file_get_contents($filename), true);
        if (time() - $data['first_attempt'] < RATE_LIMIT_WINDOW) {
            if ($data['count'] >= RATE_LIMIT) {
                return false;
            }
            $data['count']++;
        } else {
            $data = ['count' => 1, 'first_attempt' => time()];
        }
    } else {
        $data = ['count' => 1, 'first_attempt' => time()];
    }
    file_put_contents($filename, json_encode($data));
    return true;
}

function generateResponse($success, $message) {
    return json_encode([
        'success' => $success,
        'message' => $message
    ]);
}

// Vérifier la méthode
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit(generateResponse(false, 'Méthode non autorisée'));
}

// Accept form-data or JSON
$contentType = $_SERVER['CONTENT_TYPE'] ?? '';
if (strpos($contentType, 'application/json') !== false) {
    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);
    $_POST = is_array($data) ? $data : $_POST;
}

// Rate limiting
$clientIp = $_SERVER['REMOTE_ADDR'];
if (!checkRateLimit($clientIp)) {
    http_response_code(429);
    exit(generateResponse(false, 'Trop de tentatives. Réessayez plus tard.'));
}

// Récupérer et valider les données (simplifié: message only)
$message = sanitizeInput($_POST['message'] ?? '', MAX_MESSAGE_LENGTH);

// Validation
$errors = [];

if (empty($message) || strlen($message) < 10) {
    $errors[] = 'Le message est requis (min 10 caractères)';
}

if (!empty($errors)) {
    http_response_code(400);
    exit(generateResponse(false, implode(' | ', $errors)));
}

// Configuration email
$to = 'aarenovation37@gmail.com';
// Subject and headers (no client email provided)
$subject = 'Nouvelle demande de contact';

// Headers email sécurisés
$headers = "MIME-Version: 1.0\r\n";
$headers .= "Content-type: text/plain; charset=UTF-8\r\n";
$headers .= "From: noreply@aarenovation.fr\r\n";
$headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";

// Body du message
$body = "Nouvelle demande de contact\n";
$body .= "========================\n\n";
$body .= "Date: " . date('d/m/Y à H:i:s') . "\n";
$body .= "IP: " . $clientIp . "\n\n";
$body .= "Message:\n";
$body .= str_repeat("-", 40) . "\n";
$body .= $message . "\n";
$body .= str_repeat("-", 40) . "\n";

// Sending strategy: try mail() by default. If SMTP is configured (PHPMailer), prefer SMTP.
$mailSent = false;
// If PHPMailer is available and SMTP env vars are set, user can enable SMTP by installing PHPMailer via Composer.
if (class_exists('PHPMailer\PHPMailer\PHPMailer')) {
    try {
        $mail = new PHPMailer\PHPMailer\PHPMailer(true);
        // SMTP configuration would go here (examples in README)
        // $mail->isSMTP(); $mail->Host = SMTP_HOST; ...
        $mail->setFrom('noreply@aarenovation.fr', 'AAR');
        $mail->addAddress($to);
        $mail->addReplyTo($email);
        $mail->Subject = $subject;
        $mail->Body = $body;
        $mail->send();
        $mailSent = true;
    } catch (Exception $e) {
        $mailSent = false;
    }
} else {
    // fallback to PHP mail()
    $mailSent = mail($to, $subject, $body, $headers);
}

// Envoyer l'email
if ($mailSent) {
    http_response_code(200);
    exit(generateResponse(true, 'Merci! Votre message a été envoyé avec succès.'));
} else {
    http_response_code(500);
    exit(generateResponse(false, 'Erreur lors de l\'envoi. Veuillez réessayer.'));
}
?>
