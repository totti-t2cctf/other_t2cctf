<?php

// ŠÖ”

$myname = "python";
function sayHi($name = "taguchi"){
	$myname = "ruby";
	echo $myname;
	return "hi! $name";
}

echo sayHi();

echo "<br><br>";

echo sayHi("tanaka");
echo $myname;

?>
