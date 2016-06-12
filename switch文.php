<?php

// switch•¶

$signal = "red";

switch($signal){
	case "red":
		echo "stop";
		break;

	case "green":
	case "blue";
		echo "start";
		break;

	case "yellow":
		echo "attention";
		break;

	default:
		echo "exception";
		break;

}


?>
