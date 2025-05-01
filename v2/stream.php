<?php

header("Content-Type: application/json");

$type = $_GET['music'] ?? $_GET['stream'] ?? $_GET['talk'] ?? null;

$result = [];

if (isset($_GET['music'])) {
    $folder = 'music/';
    $ext = 'mp3';
    $files = glob("$folder*.$ext");

    foreach ($files as $file) {
        $result[] = $file;
    }

} elseif (isset($_GET['talk'])) {
    $folder = 'talk/';
    $ext = 'webm';
    $files = glob("$folder*.$ext");

    foreach ($files as $file) {
        $result[] = $file;
    }

} elseif (isset($_GET['stream'])) {
    $txtFolder = 'stream/';
    $txtFiles = glob($txtFolder . '*.txt');

    foreach ($txtFiles as $txtFile) {
        $url = trim(file_get_contents($txtFile));
        if (filter_var($url, FILTER_VALIDATE_URL)) {
            $result[] = $url;
        }
    }

} else {
    http_response_code(400);
    echo json_encode(["error" => "Invalid request"]);
    exit;
}

// Als geen bestanden gevonden zijn
if (empty($result)) {
    http_response_code(404);
    echo json_encode([]);
    exit;
}

// Schud de volgorde, zodat je willekeurig begint
shuffle($result);

// Geef de lijst terug
echo json_encode($result);
