<?php
   define('BASE_DIR', dirname(__FILE__));
   require_once(BASE_DIR.'/config.php');

   if (isset($_POST['shoot'])) 
   {
      startShooting();
   } 

   function startShooting() {
      writeLog("start take pano pictures");
      exec("python test.py");
      writeLog("Photo taking finished");
   }
?>

<!doctype html>
<html>
  <head>
    <title>Dual Camera</title>
  </head>
  <body style='background-color:black'>
    <div id="background" onclick="toggle_fullscreen(this);">
      <img style="width:320" id="mjpeg_left">
    </div>

    <form action="testindex.php" method="POST">
      <h1>
        <button class='btn btn-primary' type='submit' name='shoot'>shoot</button>
        <br>
      </h1>
    </form> 

    <script src="http://code.jquery.com/jquery-1.11.1.js"></script>
    <script type="text/javascript">
      //
      // MJPEG
      //
      var $mjpeg_left_img =$("#mjpeg_left");
      
      var localhost=location.host;
      var ip = '192.168.1.10'//localhost.substring(0,localhost.indexOf(':'));
      var ip_left ="http://"+ip+":80/picam";
      $mjpeg_left_img[0].src =ip_left +"/loading.jpg"
      
      var halted = 0;
      var previous_halted = 99;
      var mjpeg_mode = 0;
      var preview_delay = 50000;

      $(function() {
          
          reload_img();
          updatePreview(true);
      });

      function toggle_fullscreen(e) {

          var background = document.getElementById("background");

          if(!background) {
              background = document.createElement("div");
              background.id = "background";
              document.body.appendChild(background);
          }
        
          if(e.className == "fullscreen") {
              e.className = "";
              background.style.marginTop = 0 + 'px';
          }
          else {
              e.className = "fullscreen";
              background.style.marginTop = 50 + 'px';
          }
      }

      function reload_img () {
          if(!halted) 
          {
              $mjpeg_left_img[0].src = ip_left+"/cam_pic.php?time=" + new Date().getTime() + "&pDelay=" + preview_delay;
          }
          else 
          {
              setTimeout("reload_img()", 500);
          }
      }

      function error_img () {
          setTimeout("mjpeg_left_img.src  = "+ip_left +"'/cam_pic.php?time='       + new Date().getTime();", 100);
      }

      function updatePreview(cycle)
      {
          if (cycle !== undefined && cycle == true)
          {
              $mjpeg_left_img[0].src = ip_left +"/updating.jpg";
              setTimeout("$mjpeg_left_img[0].src = \" " + ip_left + "/cam_pic_new.php?time=\"       + new Date().getTime()  + \"&pDelay=\" + preview_delay;", 1000);
              return;
          }
        
          if (previous_halted != halted)
          {
              if(!halted)
              {
                  $mjpeg_left_img[0].src  = ip_left  +"/cam_pic.php?time="       + new Date().getTime() + "&pDelay=" + preview_delay;
              }
              else
              {
                  $mjpeg_left_img[0].src  = ip_left +"/updating.jpg";
              }
          }
          previous_halted = halted;

      }
    </script>
  </body>
</html>


