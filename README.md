# 2PiView

Panomanric photo camera kit. It uses simplest panomanric camera frame, which including 2 fisheye camera modules (fov > 180), and computing unite to generate panomanric image from two circular images from fisheye cameras. It uses one Raspberry Pi W (RPi0W) and one Raspberry Pi Zero (w) (RPi0). The RPi0 acts as USB gadget slave, ready to recieve the commands from RPi0W. The RPi0W is used as the master pi, which do the UI on WiFi, get image from slave Pi and generate panoramic image from two circular images. The kit offered the USB and power connection between two Pis, so no other usb cables needed.

## Step 0 - Prepare the Raspberry Pi Zero 

In this section, the dual RPis camera system will be set up. Dual RPis system communicate via USB Ethernet. 

For both RPi, flash latest Raspbian lite (desktop could be fine, but it is not necessary.). Once Raspbian if flashed, open up the boot partition and add new file ssh to enable the ssh on boot. The different setting between master and slave RPi is as follows.

### Slave Pi, Pi zero 
  
1. Follow the instructions to set up the USBGadget. The full instruction can be found in [here](http://blog.gbaman.info/?p=791).  In short, here is the steps copied from that instruction. 

  _For this method, alongside your Pi Zero, MicroUSB cable and MicroSD card, only an additional computer is required, which can be running Windows (with Bonjour, iTunes or Quicktime installed), Mac OS or Linux (with Avahi Daemon installed, for example Ubuntu has it built in)._

  * _Flash Raspbian Jessie full or Raspbian Jessie Lite onto the SD card_

  * _Once Raspbian is flashed, open up the boot partition (in Windows Explorer, Finder etc) and add to the bottom of the config.txt file dtoverlay=dwc2 on a new line, then save the file._

  * _If using a recent release of Jessie (Dec 2016 onwards), then create a new file simply called ssh in the SD card as well. By default SSH is now disabled so this is required to enable it. Remember - Make sure your file doesn't have an extension (like .txt etc)!_

  * _Finally, open up the cmdline.txt. Be careful with this file, it is very picky with its formatting! Each parameter is seperated by a single space (it does not use newlines). Insert modules-load=dwc2,g_ether after rootwait. To compare, an edited version of the cmdline.txt file at the time of writing, can be found here._

  * _That's it, eject the SD card from your computer, put it in your Raspberry Pi Zero and connect it via USB to your computer. It will take up to 90s to boot up (shorter on subsequent boots). It should then appear as a USB Ethernet device. You can SSH into it using raspberrypi.local as the address._
  
2. Install the rpi cam web interface, better to follow the instructions [here](https://elinux.org/RPi-Cam-Web-Interface).
  
  * _**TP**: connect the slave pi to the PC, open a browser, input raspberrypi.local/picam  if shown the live stream, it means it works._

### Master Pi, Pi Zero W

1. Set up the wireless. 

  Still in the boot partition, add the file **wpa_supplicant.conf** and add the following lines and replace SSID and PASSWORD with the ones for your network:

        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        network={
            ssid="SSID"
            psk="PASSWORD"
        }

2. Setup USBNet

  Boot the master RPi and add the following line at the end of the file /etc/network/interfaces

        auto lo
        iface lo inet loopback

        iface eth0 inet manual

        allow-hotplug wlan0
        iface wlan0 inet manual
            wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
       
  Reboot the mater pi.

2. Install the rpi web cam interface
  
  * _**TP**: connect RPi0W to your WiFi, open a browser, check the IP and input the http://rpi-ip/picam. If shown the live stream, it worded._

## Step 1 - Software Setup

1. Follow the order of install.list to install the needed packages in RPi0W. In short
  * sudo apt-get install python-opencv
  * sudo apt-get install libopencv-dev
  * sudo apt-get install python-pip
  * sudo apt-get install python-numpy
  * sudo apt-get install libjpeg8-dev
  * sudo pip install pillow

2. Clone this git and test
  * git clone https://github.com/rpicamera/360pano.git

  * _**TP**: Test the regression code. Run the following line. If no error message and it generate the sample pano image named **regression.png** as follows, it worked._

  ```python
  python regression.py
  ```

  <p align="center">
    <img src="https://github.com/rpicamera/360pano/blob/master/img/regression.png" width="350"/>
  </p>
  
## Step 2 - Setup the kit

1. Introduction of 2PiView kit
2. Setup steps
3. Test the connection

## Step 3 - Setup HTML interface

1. copy files

  * copy all files in _/picam_ except for _aframe.min.js_ into the rpi-web-cam-interface directory.

  * copy _aframe.min.js_ to _rpi-web-cam-interface/js/aframe.min.js_

  * create the directory named _img_

  * copy _../img/panowd.jpg_ into _rpi-web-cam-interface/img_

  * return to _/var/www_ and run the command:

    ```
        sudo chown -R www-data:www-data <rpi-web-cam-interface>
    ```
  * go to directory and test the python setting by
 
    ```
        sudo python genpano.py
    ```
    
  wait for it finished, go to _img_ and check is there a new file. If passed the test, it means it worked. 

2. test the whole thing

the address for taking photos is : _ip/rpi-web-cam-interface/panoindex.php_

the address for download photos is: _ip/rpi-web-cam-interface/downloadpano.php_

the address for preview photos is: _ip/rpi-web-cam-interface>/previewpano.php_


## Example images

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


