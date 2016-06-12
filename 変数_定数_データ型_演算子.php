<?php

// 変数_定数_データ型_演算子

// $からはじまる
// 英数字_が使える
// $のあとは数字はだめ
// 大文字小文字は区別される

$message = "Hello";
$x = 5;
$y = 1.22;
$flag = true;
$n = null;

var_dump($x);
var_dump($y);
var_dump($flag);
var_dump($n);
var_dump($message);

define("ADMIN_EMAIL", "a@aaa");
var_dump(ADMIN_EMAIL);

// 使える演算子
// 　　+ - * / %
// 　　単項演算子

$x++;
echo $x;

--$x;
echo $x;

$x += 1;
echo $x;

?>
