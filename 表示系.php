<?php

echo "Hello, World!";

$message = "hi";
var_dump($message);

echo "<br>";
echo "Hello, $message _\nAAAA"; // \nÇÕÉ\Å[ÉXÇ≈âeãø
echo "<br>";
echo 'Hello, $message _\nAAAA';

echo "<br><br>";
// --------------------------------------------------------
// printf

$s = "banana";
$n = 40;
$p = 5.23;

printf("we have %05d %ss for $%.2f", $n, $s, $p);

echo "<br><br>";
$result = sprintf("we have %05d %ss for $%.2f", $n, $s, $p);
echo $result;

echo "<br><br>";

printf("%x"); // ìÆÇ©Ç»Ç¢

?>
