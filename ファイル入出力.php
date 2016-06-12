<?php

// �t�@�C�����o��

// ----------------------------------------------------
// �t�@�C����������
$testFile = "test.txt";
$contents = "hello";

if(is_writable($testFile)){

	if(!$fp = fopen($testFile, "a")){
		echo "could not open!";
		exit;
	}

	if(fwrite($fp, $contents) === false){
		echo "could not write!!";
		exit;
	}

	echo "success";

	fclose($fp);

} else{
	echo "not writable!";
	exit;
}

echo "<br><br>";

// ----------------------------------------------------
// �t�@�C���ǂݍ���1

if(!$fp = fopen($testFile, "r")){
	echo "could not open";
	exit;
}

$contents = fread($fp, filesize($testFile));
var_dump($contents);
fclose($fp);

echo "11111111111111";
echo "<br><br>";

// ----------------------------------------------------
// �t�@�C���ǂݍ���2

$contents = file_get_contents($testFile);
var_dump($contents);

echo "2<br><br>";

// ----------------------------------------------------
// �t�@�C���ǂݍ���3(���s��z��Ƃ���)

$contentslist = file($testFile);
var_dump($contentslist);
echo $contentslist[0];
echo $contentslist[1];

echo "3<br><br>";

// ----------------------------------------------------
// �t�@�C���ǂݍ���3(���s�Ŕz�񊎂��s����菜��)

$contentslist2 = file($testFile, FILE_IGNORE_NEW_LINES);
echo $contentslist2[0];
echo $contentslist2[1];

?>
