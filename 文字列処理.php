<?php

// �����񏈗�

$s = "abcdefg";

echo strlen($s);
echo "<br><br>";

echo strpos($s, "c");
echo "<br><br>";

echo substr($s, 2);
echo "<br><br>";

echo substr($s, 2, 3);
echo "<br><br>";

echo substr($s, -4, 2);
echo "<br><br>";

echo str_replace("abc", "ABC", $s);
echo "<br><br>";

echo $s;

// -------------------------------------------------
// ���{��Ή�

$s = "��������������������";

echo $s;

echo mb_strlen($s);
echo "<br><br>";


echo mb_strpos($s, "��");
echo "<br><br>";

echo mb_substr($s, 2);
echo "<br><br>";

echo mb_substr($s, 2, 3);
echo "<br><br>";

echo mb_substr($s, -4, 2);
echo "<br><br>";

echo mb_str_replace("������", "����", $s);
echo "<br><br>";

echo $s;

?>
