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
  <img src="https://github.com/rpicamera/360pano/blob/master/img/resizecrpped.png" width="350"/>
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

MJPEG server

### 3.1: simple html server to prove that it works

mjpeg.py shows the basic python http mjpeg server, modified from https://gist.github.com/n3wtron/4624820 
My version uses the picamera to capture the image. 

360mjpeg.py added the pano converting to the simple http mjpeg server.

These two methods have large time lag because of IO I believe.

### 3.2: Django mjpeg server, implement some functionalities, such as take picture, download picture, preview


