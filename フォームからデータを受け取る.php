<?php

// �t�H�[������̃f�[�^���󂯎��

$birthday = $_POST['birthday'];

?>

<!DOCTYPE html>
<html lang="ja">
<head>
	<meta charset="utf-8">
	<title>PHP��HTML</title>
</head>
<body>
	<h1>PHP�̗��K</h1>
	<p><?php echo htmlspecialchars($birthday); ?></p>
</body>
</html>
