<?php
   define('BASE_DIR', dirname(__FILE__));
   require_once(BASE_DIR.'/config.php');

   if (isset($_POST['save'])) 
   {
      $mleft=$_POST['mleft'];
      $sleft=$_POST['sleft'];
      $mtop=$_POST['mtop'];
      $stop=$_POST['stop'];
      $msize=$_POST['msize'];
      $ssize=$_POST['ssize'];
      saveconfig($mleft,$sleft,$mtop,$stop,$msize,$ssize);
   } 

   if (isset($_POST['crop'])) 
   {
      $mleft=$_POST['mleft'];
      $sleft=$_POST['sleft'];
      $mtop=$_POST['mtop'];
      $stop=$_POST['stop'];
      $msize=$_POST['msize'];
      $ssize=$_POST['ssize'];
      cropimage($mleft,$sleft,$mtop,$stop,$msize,$ssize);
   } 

   function saveconfig($mleft,$sleft,$mtop,$stop,$msize,$ssize) 
   {
      writeLog("saving to config file");
      exec("python saveconf.py $mleft $sleft $mtop $stop $msize $ssize");
   }

   function cropimage($mleft,$sleft,$mtop,$stop,$msize,$ssize)
   {
      writeLog("crop the image");
      exec("python crophelper.py $mleft $sleft $mtop $stop $msize $ssize");
   }
?>

<!doctype html>
<html>
  <head>
    <title>Dual Camera</title>
    <link rel="stylesheet" href="css/style_minified.css" />
    <script src="js/style_minified.js"></script>
  </head>
  <body>
    <div class="container-fluid">
      <img style="width:320px" id="mjpeg_left" src="imghelp/helpcroppedmaster.png">
      <img style="width:320px" id="mjpeg_right" src="imghelp/helpcroppedslave.png">
      <hr>
        <table style='margin-left: 80px;' >
          <form action="crophelper.php" method="POST">
            <tr>
              <td> 
                master left: <input type="text" name="mleft" value="150"><br>
              </td>
              <td>
                slave left: <input type="text" name="sleft" value="150"><br>
              </td>
            </tr>
            <tr>
              <td> 
                master top: <input type="text" name="mleft" value="100"><br>
              </td>
              <td>
                slave top: <input type="text" name="sleft" value="100"><br>
              </td>
            </tr>
            <tr>
              <td> 
                master size: <input type="text" name="mleft" value="2190"><br>
              </td>
              <td>
                slave size: <input type="text" name="sleft" value="2190"><br>
              </td>
            </tr>
            <tr>
              <td><button style='margin-left:10px;' class='btn btn-primary' type='submit' name='crop'>crop</button></td>
              <br>
              <td><button style='margin-left:10px;' class='btn btn-primary' type='submit' name='save'>save</button></td>
              <br>
            </tr>
          </form> 
        </table>
      <hr>
    </div>
  </body>
</html>
