<?php
   define('BASE_DIR', dirname(__FILE__));
   require_once(BASE_DIR.'/config.php');

   if (isset($_POST['shoot'])) 
   {
      $tFile = $_POST['shoot'];
      startShooting();
      $tFile = "";
   } 

   function startShooting() {
      writeLog("start take pano pictures");
      exec("python test.py");
      writeLog("Photo taking finished");
   }
?>
