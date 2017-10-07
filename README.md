# 360 Pano
2piview project. Embedded two 220 degree fisheye camera module and produce a 360 pano image. 

## Step 1:
Covert circular image into pano image. And use github page to show the 360 pano image for testing. 

This is the originial image, the left most circular to the left boundary is about 220 pixels.

<p align="center">
  <img src="https://github.com/rpicamera/360pano/blob/master/img/test.jpg" width="350"/>
</p>

Here is the image after crop and rotation
<p align="center">
  <img src="https://github.com/rpicamera/360pano/blob/master/img/resizecroped.png" width="350"/>
</p>

And here is the pano image after remapping the above squared circular image
<p align="center">
  <img src="https://github.com/rpicamera/360pano/blob/master/img/convertpanotest.png" width="350"/>
</p>

## Step 2:

Create the pano from the my 2PiView kit using Python code, detail in genpano.py. And here is the example

<p align="center">
  <img src="https://github.com/rpicamera/360pano/blob/master/img/pano.png" width="350"/>
</p>

This is the view from the phone. 

<p align="center">
  <img src="https://github.com/rpicamera/360pano/blob/master/img/VRExample.png" width="350"/>
</p>

Here is my 2PiView kit:

<p align="center">
  <img src="https://github.com/rpicamera/360pano/blob/master/img/2PiViewKit.jpg" width="350"/>
</p>

## Step 3:

Pano server

### 3.1 copy files

copy all files in _/picam_ except for _aframe.min.js_ into the rpi-web-cam-interface directory.

copy _aframe.min.js_ to _rpi-web-cam-interface/js/aframe.min.js_

create the directory named _img_

copy _../img/panowd.jpg_ into _rpi-web-cam-interface/img_

return to _/var/www_ and run the command:

    sudo chown -R www-data:www-data <rpi-web-cam-interface>

go to directory and test the python setting by

    sudo python genpano.py
    
wait for it finished, go to _img_ and check is there a new file. If passed the test, it means it worked. 

### 3.2 test the whole thing

the address for taking photos is : _ip/rpi-web-cam-interface/panoindex.php_

the address for download photos is: _ip/rpi-web-cam-interface/downloadpano.php_

the address for preview photos is: _ip/rpi-web-cam-interface>/previewpano.php_


