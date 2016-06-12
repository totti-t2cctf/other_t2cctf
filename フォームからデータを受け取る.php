<?php

// フォームからのデータを受け取る

$birthday = $_POST['birthday'];

?>

<!DOCTYPE html>
<html lang="ja">
<head>
	<meta charset="utf-8">
	<title>PHPのHTML</title>
</head>
<body>
	<h1>PHPの練習</h1>
	<p><?php echo htmlspecialchars($birthday); ?></p>
</body>
</html>
