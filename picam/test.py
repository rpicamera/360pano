import sys, getopt
import cv2
import numpy as np
import requests,time
from   urllib  import urlopen
from   pathlib import Path
import re

def main():

    # get image from master and slave pi
    requests.get("http://127.0.0.1/picam/cmd_pipe.php?cmd=im")

    time.sleep(1)

    paternsize = 1000

    master_media_dir = 'http://127.0.0.1/picam/media/'

    urlpath = urlopen(master_media_dir)
    patern = re.compile('([^\"\']*\.jpg)');
    string = urlpath.read().decode('utf-8')
    filelist = patern.findall(string[len(string)-paternsize:])
    filename = filelist[len(filelist)-4]
    rsp = urlopen(master_media_dir+filename)
    master_image = np.array(bytearray(rsp.read()), dtype=np.uint8)

    master_img = cv2.imdecode(master_image, -1)

    cv2.imwrite("img/newpano.png",master_img)

if __name__ == "__main__":
   main()
