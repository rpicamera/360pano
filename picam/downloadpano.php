<?php
  define('MEDIA_DIR','192.168.1.10/picam/img/');
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
            <button class='btn btn-primary' type='submit' name='previewpano' value='newpano.png'>newpano</button>
         </form>
      </div>
   </body>
</html>
