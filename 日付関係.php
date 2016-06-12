<?php

// “ú•tŠÖŒW

// ----------------------------------
// unixƒ^ƒCƒ€

var_dump(time());
echo "<br><br>";

var_dump(mktime(1, 10, 11, 1, 2, 2000)); // 2000/1/2 1:10:11
echo "<br><br>";

var_dump(strtotime("2000/1/2 1:10:11"));
echo "<br><br>";

var_dump(strtotime("last Sunday"));
echo "<br><br>";

var_dump(strtotime("+2 day"));
echo "<br><br>";

// ----------------------------------
echo date("Y-m-d H:i:s");
echo "<br><br>";

echo date("Y-m-d H:i:s", strtotime("last Sunday"));
echo "<br><br>";




?>
