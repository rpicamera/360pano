<?php
  define('MEDIA_DIR','192.168.1.10/picam/img/');

  //$files = scandir('192.168.1.10/picam/img');
  //usort($files, function($a, $b) {
  //  return filemtime($a) < filemtime($b);
  //});

  //function drawFile($file)
  //{
  //  if(strlen($file)-strpos($file,".png")== 4)
  //  {
  //    echo "<tr><button class='btn btn-primary' type='submit' name='previewpano' value='$file'>$file</button></tr>";
  //  }
  //}
?>

<!DOCTYPE html>
<html>
   <head>
      <meta name="viewport" content="width=550, initial-scale=1">
      <title> Download </title>
      <link rel="stylesheet" href="css/style_minified.css" />
      <script src="js/style_minified.js"></script>
   </head>
   <body>
      <div class="container-fluid">
         <form action="previewpano.php" method="POST">
            <?php
                $files = scandir('/var/www/picam/img');
                if(count($files) == 0) echo "<p>No videos/images saved</p>";
                else 
                {
                   foreach($files as $file) 
                   {
                      if($file!="." && $file!="..")
                      {
                         echo "<tr><button class='btn btn-primary' type='submit' name='previewpano' value='$file'>$file</button></tr>";
                      }
                   }
                }
            ?>
         </form>
      </div>
   </body>
</html>
