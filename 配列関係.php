<?php

// �z��

$youbi = array("Sun", "Mon", "Tue");
echo $youbi[1];

echo "<br><br>";

// ------------------------------------------------------------
// �v�f�̒ǉ�

$youbi[] = "Wed";
var_dump($youbi);

echo "<br><br>";

// ------------------------------------------------------------
// �v�f�̏�������

$youbi[0] = "Sunday";
var_dump($youbi);

echo "<br><br>";

// ------------------------------------------------------------
// �v�f�̍폜(�������񐄏�)

unset($youbi[1]);
var_dump($youbi);

echo "<br><br>";

$youbi[1] = "AAAA";
var_dump($youbi);

echo "<br><br>";
echo $youbi[1];

// ------------------------------------------------------------
// �A�z�z��

$sales = array("aaa"=>150, "bbb"=>200);

echo $sales["aaa"];
echo "<br><br>";

// ------------------------------------------------------------
// �z��̃��[�v(���[�v����鏇�Ԃɒ���)

foreach($youbi as $y){
	echo $y;
}

echo "<br><br>";

// ------------------------------------------------------------
// �A�z�z��̃��[�v(���[�v����鏇�Ԃɒ���)

foreach($sales as $k => $v){
	echo "key:" . $k . ", " . "value:" . $v . "<br>";
}

echo "<br><br>";

// ------------------------------------------------------------
// �v�f�̌�

$members = array("tanaka", "yoshida", "kimura", "sasaki", "uchida");
echo count($members);
echo "<br><br>";

// ------------------------------------------------------------
// �v�f�̃\�[�g

sort($members);
var_dump($members);
echo "<br><br>";

// �t�]
$mem_rev = array_reverse($members);
var_dump($members);
var_dump($mem_rev);
echo "<br><br>";

// ------------------------------------------------------------
// �z����̑���

if(in_array("tanaka", $members)){
	echo "In";
}
echo "<br><br>";

// ------------------------------------------------------------
// �z��ɑ΂��z����̒��g����؂蕶����ɂ����ď���

$joinstr = implode("@", $members);
echo $joinstr;
echo "<br><br>";

$splitstr = explode("@", $joinstr);
var_dump($splitstr);
echo "<br><br>";




?>
