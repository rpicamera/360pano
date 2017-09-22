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
    size=input('size=')
    imgFile = 'img/test.jpg'

    if _debug>=1:
        print('Front file is: ', imgFile)

    img = cv2.imread(imgFile,cv2.IMREAD_COLOR)

    while(left>0):
        left = input('left=')
        top = input('top=')
        cv2.circle(img, (int(0.5*size),int(0.5*size)), int(0.5*size), (0,0,255), 5)
        cv2.imshow('image',img)
        cv2.waitKey(2)



if __name__ == "__main__":
   main()

