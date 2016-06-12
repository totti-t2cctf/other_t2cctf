<?php

// 配列

$youbi = array("Sun", "Mon", "Tue");
echo $youbi[1];

echo "<br><br>";

// ------------------------------------------------------------
// 要素の追加

$youbi[] = "Wed";
var_dump($youbi);

echo "<br><br>";

// ------------------------------------------------------------
// 要素の書き換え

$youbi[0] = "Sunday";
var_dump($youbi);

echo "<br><br>";

// ------------------------------------------------------------
// 要素の削除(※やり方非推奨)

unset($youbi[1]);
var_dump($youbi);

echo "<br><br>";

$youbi[1] = "AAAA";
var_dump($youbi);

echo "<br><br>";
echo $youbi[1];

// ------------------------------------------------------------
// 連想配列

$sales = array("aaa"=>150, "bbb"=>200);

echo $sales["aaa"];
echo "<br><br>";

// ------------------------------------------------------------
// 配列のループ(ループされる順番に注意)

foreach($youbi as $y){
	echo $y;
}

echo "<br><br>";

// ------------------------------------------------------------
// 連想配列のループ(ループされる順番に注意)

foreach($sales as $k => $v){
	echo "key:" . $k . ", " . "value:" . $v . "<br>";
}

echo "<br><br>";

// ------------------------------------------------------------
// 要素の個数

$members = array("tanaka", "yoshida", "kimura", "sasaki", "uchida");
echo count($members);
echo "<br><br>";

// ------------------------------------------------------------
// 要素のソート

sort($members);
var_dump($members);
echo "<br><br>";

// 逆転
$mem_rev = array_reverse($members);
var_dump($members);
var_dump($mem_rev);
echo "<br><br>";

// ------------------------------------------------------------
// 配列内の存在

if(in_array("tanaka", $members)){
	echo "In";
}
echo "<br><br>";

// ------------------------------------------------------------
// 配列に対し配列内の中身を区切り文字列にそって処理

$joinstr = implode("@", $members);
echo $joinstr;
echo "<br><br>";

$splitstr = explode("@", $joinstr);
var_dump($splitstr);
echo "<br><br>";




?>
