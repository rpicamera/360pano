for php_f in *.php
do 
   cp -v "$php_f" /var/www/picam/"$php_f"
done

for py_f in *.py
do 
   cp -v "$py_f" /var/www/picam/"$py_f"
done

cp -v aframe.min.js /var/www/picam/js/aframe.min.js