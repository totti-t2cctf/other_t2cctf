<?php

if($_SERVER['REQUIEST_METHOD'] == 'POST' &&
	isset($_POST['user']) &&
	isset($_POST['message'])){

	$message = $_POST['message'];
	$user = $_POST['user'];

	if($message !== ''){
		$user = ($user === '') ? "名無しさん" : $user;
	}

}

$records = //配列;

?>

<!DOCTYPE html>
<html lang="ja">
<head>
	<meta charset="utf-8">
	<title>掲示板</title>
</head>
<body>
	<h1>簡易掲示板</h1>
	<form action="" method="post">
		user: <input type="text" name="user">
		message: <input type="text" name="message">
		<input type="submit" value="投稿">
	</form>
	<h2>投稿一覧 (<?php echo count($records); ?>)</h2>
	<ul>
		<?php if (count($records)) : ?>
			<?php foreach ($records as $record) : ?>
			<?php list($message, $user, $postedAt) = explode("@", $record);
				<li><?php echo $message ?> <?php echo $user ?> - <?php echo $postdAt ?></li>
			<?php endforeach; ?>
		<?php else : ?>
			<li>まだ投稿はありません。</li>
		<?php endif; ?>
	</ul>

</body>
</html>
