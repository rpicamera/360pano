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
import requests,time
from   urllib  import urlopen
from   pathlib import Path
import re

_debug=1

def getmap(sz_src,sz_out,fov,qvert,qbmap):
    map_file = Path('mapx.npy')

    if not map_file.is_file() or qbmap:
        map_x,map_y = buildMap(sz_src,sz_out,fov,qvert)
        return map_x,map_y
    
    print('Load map...')
    map_x = np.load('mapx.npy')
    map_y = np.load('mapy.npy')
    return map_x,map_y

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
        Phi=0
        Theta=0
        CosPhi=0

        R         = sz_src * np.arctan(np.sqrt(Spx*Spx+(Spz*Spz)[:].reshape(sz_out,1))/(Spy+1e-20))/vfov
        Spy=0
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

def smoothBound(img1, img2, w, h, delta):
    filer_file = Path('vfilter.npy')
    vfilter=0
    if filer_file.is_file():
        vfilter = np.load('vfilter.npy')
    else:
        sz_out = w
        vfilter = np.ones((1,2*sz_out,1),np.float32)
        for i in range(int(0.5*sz_out-delta),int(0.5*sz_out+delta)):
            vfilter[0,i,0] = 0.5*np.cos(float(i-(0.5*sz_out+delta))/float(delta)*np.pi/2.0)+0.5
        for i in range(int(1.5*sz_out-delta),int(1.5*sz_out+delta)):
            vfilter[0,i,0] = 0.5*np.cos(float(i-(1.5*sz_out-delta))/float(delta)*np.pi/2.0)+0.5

    img1 = np.multiply(img1,vfilter)
    img2 = np.multiply(img2,vfilter)
    leftsmooth = img1[0:h,int(1.5*w-delta):int(1.5*w+delta)] + img2[0:h,int(0.5*w-delta):int(0.5*w+delta)]
    rightsmooth = img1[0:h,int(0.5*w-delta):int(0.5*w+delta)] + img2[0:h,int(1.5*w-delta):int(1.5*w+delta)]
    rst = np.concatenate((img1[0:h,w:int(1.5*w-delta)], leftsmooth,img2[0:h,int(0.5*w+delta):int(1.5*w-delta)],rightsmooth,img1[0:h,int(0.5*w+delta):w]), axis=1)
    return rst

def main():

    # get image from master and slave pi
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
    rsp = urlopen(slave_media_dir+filename)
    slave_image = np.array(bytearray(rsp.read()), dtype=np.uint8)

    if _debug>=2:
        print(slave_media_dir + filename)
        output = open("img/slave.jpg","wb")
        rsc = urlopen(slave_media_dir+filename)
        output.write(rsc.read())
        output.close()

    urlpath = urlopen(master_media_dir)
    string = urlpath.read().decode('utf-8')
    filelist = patern.findall(string[len(string)-paternsize:])
    filename = filelist[len(filelist)-4]
    rsp = urlopen(master_media_dir+filename)
    master_image = np.array(bytearray(rsp.read()), dtype=np.uint8)

    if _debug>=2:
        print(master_media_dir+filename+'|')
        output = open("img/master.jpg","wb")
        rsc = urlopen(master_media_dir+filename)
        output.write(rsc.read())
        output.close()

    slave_img  = cv2.imdecode(slave_image, -1)
    master_img = cv2.imdecode(master_image, -1)
    print(slave_img.shape)
    print(master_img.shape)
 
    sz_src   = 2190   # source image size in pixel after squaring
    sz_out   = 1024   # output pano image hight in pixel
    ml       = 155    # modified pixels from left
    mt       = 0      # modified pixels from top
    sl       = 250
    fov      = float(200)

    # square the image, better to get full circular image
    rows= slave_img.shape
    amtop = 100        # modified pixels from top
    astop = 105
    ambottom = sz_src-amtop-rows[0]
    asbottom = sz_src-astop-rows[0]
    if _debug>=1:
        print("rows:%d" % (rows[0]))

    slave_img  = crop(slave_img,sl,mt,sz_src)
    master_img = crop(master_img,ml,mt,sz_src)
    MM         = np.float32([[1,0,0],[0,1,amtop]])
    MS         = np.float32([[1,0,0],[0,1,astop]])
    slave_img  = cv2.warpAffine(slave_img,MS,(sz_src,sz_src))
    master_img = cv2.warpAffine(master_img,MM,(sz_src,sz_src))

    if _debug>=2:
        cv2.imwrite("img/resizecrpped_slave.png",slave_img)
        cv2.imwrite("img/resizecrpped_master.png",master_img)

    if _debug>=1:
        print("cropped image size: %d*%d pixels " % (sz_src,sz_src))

    # build map
    mapx,mapy = getmap(sz_src,sz_out,fov,True,True)

    # apply map and output image
    slave_img  = unwarp(slave_img,mapx,mapy)
    master_img = unwarp(master_img,mapx,mapy)
    
    if _debug>=2:
        cv2.imwrite("img/convertpanoslave.png",slave_img)
        cv2.imwrite("img/convertpanomaster.png",master_img)

    pano_img = smoothBound(master_img,slave_img,sz_out,sz_out,30)
    time_name = time.strftime(%Y%m%d_%H%M%S,time.gmtime())
    img_name = "img/pano_"+ time_name +".png"
    thumb_name = "img/thumb_pano_"+time_name+".png"
    cv2.imwrite(img_name,pano_img)
    thumb_img = cv2.resize(pano_img,(100, 50)) 
    cv2.imwrite(thumb_name,thumb_img)

if __name__ == "__main__":
   main()



