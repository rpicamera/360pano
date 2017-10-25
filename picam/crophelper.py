# crop helper
# crop the original image to square size. 
# the circular image should locate in the middle
# read the image from the master and slave pis
# save the images to the local img/helpmaster.jpg & img/helpslave.jpg
# save the cropped image to the local img/helpcroppedmaster.jpg & img/helpcroppedslave.jpg
# show the cropped image on html

import sys
import numpy as np
import cv2
import requests,time
from   urllib  import urlopen
from   pathlib import Path
import re

def main():
    [tmp,mleft,sleft,mtop,stop,msize,ssize] = sys.argv    
    print(tmp)
    mleft=int(mleft)
    sleft=int(sleft)
    mtop =int(mtop)
    stop =int(stop)
    msize=int(msize)
    ssize=int(ssize)

    imgmasterori='imghelp/helpmaster.jpg'
    imgslaveori='imghelp/helpslave.jpg'

    masterori_file = Path(imgmasterori)
    slaveori_file  = Path(imgslaveori)
    
    if not masterori_file.is_file() or not slaveori_file.is_file():
        # get image from master and slave pi and save them to local
        requests.get("http://127.0.0.1/picam/cmd_pipe.php?cmd=im");
        requests.get("http://raspberrypi.local/picam/cmd_pipe.php?cmd=im");

        time.sleep(1)

        paternsize = 1000

        slave_media_dir  = 'http://raspberrypi.local/picam/media/'
        master_media_dir = 'http://127.0.0.1/picam/media/'
        urlpath = urlopen(slave_media_dir)
        string = urlpath.read().decode('utf-8')
        patern = re.compile('([^\"\']*\.jpg)');
        filelist = patern.findall(string[len(string)-paternsize:])
        filename = filelist[len(filelist)-4]
        output = open(imgslaveori,"wb")
        rsc = urlopen(slave_media_dir+filename)
        output.write(rsc.read())
        output.close()

        urlpath = urlopen(master_media_dir)
        string = urlpath.read().decode('utf-8')
        filelist = patern.findall(string[len(string)-paternsize:])
        filename = filelist[len(filelist)-4]
        output = open(imgmasterori,"wb")
        rsc = urlopen(master_media_dir+filename)
        output.write(rsc.read())
        output.close()


    imgmaster = cv2.imread(imgmasterori,cv2.IMREAD_COLOR)
    imgslave  = cv2.imread(imgslaveori ,cv2.IMREAD_COLOR)
    tmpimg = imgmaster
    cv2.circle(tmpimg, (int(0.5*msize)+mleft,int(0.5*msize)-mtop), int(0.5*msize), (0,0,255), 5)
    cv2.imwrite("imghelp/helpcroppedmaster.png",tmpimg)
    tmpimg = imgslave
    cv2.circle(tmpimg, (int(0.5*ssize)+sleft,int(0.5*ssize)-stop), int(0.5*ssize), (0,0,255), 5)
    cv2.imwrite("imghelp/helpcroppedslave.png",tmpimg)
    print('finished the crop!')

if __name__ == "__main__":
   main()
