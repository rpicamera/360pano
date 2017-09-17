<?php

  header("Content-Type: image/jpeg");
   if (isset($_GET["pDelay"]))
   {
      $preview_delay = $_GET["pDelay"];
   } else {
      $preview_delay = 10000;
   }
   usleep($preview_delay);
   file_put_contents('/var/www/picam/slave/s_cam.jpg',file_get_contents('http://raspberrypi.local/picam/cam.jpg'));
   readfile("/var/www/picam/slave/s_cam.jpg");
?>

