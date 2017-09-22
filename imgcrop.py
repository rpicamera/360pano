# crop helper
# crop the original image to square size. 
# the circular image should locate in the middle

import sys, getopt
import numpy as np
import cv2

_debug=2

def main():
    left=0
    top=0
    size=0
    imgFile = 'img/test.jpg'

    if _debug>=1:
        print('Front file is: ', imgFile)

    img = cv2.imread(imgFile,cv2.IMREAD_COLOR)

    while(left>=0):
        left = int(input('left='))
        top  = int(input('top='))
        size = int(input('size='))
        tmpimg = img
        cv2.circle(tmpimg, (int(0.5*size)+left,int(0.5*size)+top), int(0.5*size), (0,0,255), 5)
        cv2.imwrite("img/helpcroped.png",tmpimg)



if __name__ == "__main__":
   main()
