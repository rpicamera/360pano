# covert circular image to rectangle
# image info: 2200*220 center need to be set manuely
# since settled, everything will be fixed for the next time
# after initial, the config file will be generated, in formation of 
# crop location
# matrix size
# pairs of x and y 

import sys, getopt
import cv2
import numpy as np

_debug=2

"""
input:
1: source image size: it is from source image, which was hard code as 2200 pixels
2: output image size
3: field of view, unit in degree 
4: camera facing vertically or horizontally.
"""
def buildMap(sz_src,sz_out,fov,qvert):
    if _debug>=1:
        print("Building map...")

    vfov=fov/180*np.pi
    
    """ serial version, for better understanding

    ********************* vertical position ************************
    for y in range(0,int(sz_out)):
        phi    = np.pi*(float(y)/float(sz_out-1)-0.5)
        cosPhi = np.cos(phi)
        spz    = np.sin(phi)

        for x in range(0,int(sz_out*2)):

            theta = np.pi*(float(x)/float(sz_out-1)-1)
            spx   =cosPhi*np.sin(theta);
            spy   =cosPhi*np.cos(theta);

            a_theta = np.arctan(spz/(spx+1e-20))
            a_phi   = np.arctan(np.sqrt(spx*spx+spz*spz)/(spy+1e-20))
            r=sz_src*a_phi/vfov

            if spy<0:
                r=sz_src*180/fov-abs(r)

            if spx<0:
                r=-r

            xS = int(0.5*sz_src+r*np.cos(a_theta))
            yS = int(0.5*sz_src+r*np.sin(a_theta))

            map_x.itemset((y,x),xS)
            map_y.itemset((y,x),yS)

    ********************* horizontal posiation *********************

    for y in range(0,int(sz_out)):
        phi    = np.pi*(float(y)/float(sz_out-1))
        sinPhi = np.sin(phi)

        for x in range(0,int(sz_out*2)):

            theta = np.pi*(float(x)/float(sz_out)-1)
            r=sz_src*phi/vfov

            xS = int(0.5*sz_src+r*np.cos(theta))
            yS = int(0.5*sz_src+r*np.sin(theta))

            map_x.itemset((y,x),xS)
            map_y.itemset((y,x),yS)

    """

    map_x = np.zeros((sz_out,sz_out*2),np.float32)
    map_y = np.zeros((sz_out,sz_out*2),np.float32)
    # vectorizion version
    if qvert:
        Phi       = np.pi*(np.arange(float(  sz_out))/float(sz_out-1)-0.5)
        Theta     = np.pi*(np.arange(float(2*sz_out))/float(sz_out-1)-1)
        CosPhi    = np.cos(Phi)

        Spx       = np.dot(CosPhi[:].reshape(sz_out,1),np.sin(Theta).reshape(1,2*sz_out))
        Spy       = np.dot(CosPhi[:].reshape(sz_out,1),np.cos(Theta).reshape(1,2*sz_out))
        Spz       = np.sin(Phi)

        R         = sz_src * np.arctan(np.sqrt(Spx*Spx+(Spz*Spz)[:].reshape(sz_out,1))/(Spy+1e-20))/vfov
        # Fixing arctan range 
        halfOutSz = int(sz_out/2)
        aPhiMod   = np.append(np.append(np.ones(halfOutSz),np.zeros(sz_out-1)),np.ones(halfOutSz+1))*sz_src*180/fov
        R         = (R + aPhiMod) * np.append(np.ones(sz_out-1)*-1,np.ones(sz_out+1))   # fixed atan problem

        aTheta    = np.arctan(Spz[:].reshape(sz_out,1)/(Spx+1e-20))
        map_x     = 0.5*sz_src+(R*np.cos(aTheta)).astype('float32')
        map_y     = 0.5*sz_src+(R*np.sin(aTheta)).astype('float32')

    else:
        Phi       = np.pi*(np.arange(float(sz_out))/float(sz_out-1))
        Theta     = np.pi*(np.arange(float(2*sz_out))/float(sz_out-1)-1)
        R         = sz_src*Phi/vfov

        map_x     = 0.5*sz_src+(np.dot(R[:].reshape(sz_out,1),np.cos(Theta).reshape(1,2*sz_out))).astype('float32')
        map_y     = 0.5*sz_src+(np.dot(R[:].reshape(sz_out,1),np.sin(Theta).reshape(1,2*sz_out))).astype('float32')

    return map_x, map_y

    


def unwarp(img,xmap,ymap):
    rst=cv2.remap(img,xmap,ymap,cv2.INTER_LINEAR)
    return rst


def crop(img,left,top,sz):
    crop_img = img[top:top+sz, left:left+sz] 
    return crop_img


def main():
    imgFile = 'img/test.jpg'

    if _debug>=1:
        print('Front file is: ', imgFile)

    img = cv2.imread(imgFile,cv2.IMREAD_COLOR)

    sz_src   = 2200   # source image size in pixel after squaring
    sz_out   = 2200   # output pano image hight in pixel
    ml       = 220    # modified pixels from left
    mt       = 0      # modified pixels from top
    fov      = float(220)
    
    # square the image, better to get full circular image
    rows= img.shape
    atop = 170        # modified pixels from top
    abottom = sz_src-atop-rows[0]
    if _debug>=1:
        print("rows:%d" % (rows[0]))

    img = crop(img,ml,mt,sz_src)
    M = np.float32([[1,0,0],[0,1,atop]])
    img = cv2.warpAffine(img,M,(2200,2200))
    # rotated the image. 
    img=np.rot90(img)
    img=np.rot90(img)
    img=np.rot90(img)
    
    if _debug>=2:
        cv2.imwrite("img/resizecroped.png",img)

    if _debug>=1:
        print("cropped image size: %d*%d pixels " % (sz_src,sz_src))

    # build map
    mapx,mapy = buildMap(sz_src,sz_out,fov,True)

    # apply map and output image
    img = unwarp(img,mapx,mapy)
    cv2.imwrite("img/convertpanotest.png",img)


if __name__ == "__main__":
   main()

