<?php
   define('BASE_DIR', dirname(__FILE__));
   require_once(BASE_DIR.'/config.php');

   $mleft=150;
   $sleft=150;
   $mtop=100;
   $stop=100;
   $msize=2190;
   $ssize=2190;

   $handle = fopen("config.txt", "r");
   if ($handle) {
      while (($line = fgets($handle)) !== false) {
          if(substr($line, 0,3)=="mlf")
          {
              $mleft=substr($line, 4);
          }
          else if(substr($line, 0,3)=="slf")
          {
              $sleft=substr($line, 4);
          }
          else if(substr($line, 0,3)=="amt")
          {
              $mtop=substr($line, 4);
          }
          else if(substr($line, 0,3)=="ast")
          {
              $stop=substr($line, 4);
          }
          else if(substr($line, 0,3)=="msz")
          {
              $msize=substr($line, 4);
          }
          else if(substr($line, 0,3)=="ssz")
          {
              $ssize=substr($line, 4);
          }
      }

      fclose($handle);
   }
   // read the settings from tmp file

   if (isset($_POST['save'])) 
   {
      $mleft=$_POST['mleft'];
      $sleft=$_POST['sleft'];
      $mtop=$_POST['mtop'];
      $stop=$_POST['stop'];
      $msize=$_POST['msize'];
      $ssize=$_POST['ssize'];
      saveconfig($mleft,$sleft,$mtop,$stop,$msize,$ssize);
      $dbg = "cde";
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
      $dbg="edf";
   } 

   function saveconfig($mleft,$sleft,$mtop,$stop,$msize,$ssize) 
   {
      $output="";
      $ret_code="";
      writeLog("saving to config file");
      exec("python saveconf.py $mleft $sleft $mtop $stop $msize $ssize",$output, $ret_code);
   }

   function cropimage($mleft,$sleft,$mtop,$stop,$msize,$ssize)
   {
      writeLog("crop the image");
      $output="";
      $ret_code="";
      exec("python crophelper.py $mleft $sleft $mtop $stop $msize $ssize", $output, $ret_code);
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
      <p>left image: master    --|--    right image: slave</p>
      <img style="width:320px" id="mjpeg_left" src="imghelp/helpcroppedmaster.png">
      <img style="width:320px" id="mjpeg_right" src="imghelp/helpcroppedslave.png">
      <hr>
        <table style='margin-left: 80px;' >
          <form action="crophelper.php" method="POST">
            <tr>
              <td> 
                master left: <input type="text" name="mleft" value="<?php echo $mleft; ?>"><br>
              </td>
              <td>
                slave left: <input type="text" name="sleft" value="<?php echo $sleft; ?>"><br>
              </td>
            </tr>
            <tr>
              <td> 
                master top: <input type="text" name="mtop" value="<?php echo $mtop; ?>"><br>
              </td>
              <td>
                slave top: <input type="text" name="stop" value="<?php echo $stop; ?>"><br>
              </td>
            </tr>
            <tr>
              <td> 
                master size: <input type="text" name="msize" value="<?php echo $msize; ?>"><br>
              </td>
              <td>
                slave size: <input type="text" name="ssize" value="<?php echo $ssize; ?>"><br>
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
<p><?php echo $dbg ?></p>
      <hr>
    </div>
  </body>
</html>
