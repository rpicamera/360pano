# Build the mapx and mapy for pano converting. 
# input parameter: sz_src: square source image size
#                  sz_out: ouput image height
#                  fov:    filed of view
#                  qvert:  Camera facing, Vertical or Horizontal
# output: mapx, mapy
# by testing, loading mapx and mapy is 3 times faster than live build

import sys, getopt
import numpy as np
import time
from pathlib import Path

_debug=2

conf={
    'src':2190,
    'out':1024,
    'fov':200,
    'vnh':1,
    'del':30,
    'mlf':155,
    'slf':250,
    'amt':100,
    'ast':105,
    'msz':2190,
    'ssz':2190
}

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
        print('Vertical')
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
        print('Horizontal')
        Phi       = np.pi*(np.arange(float(sz_out))/float(sz_out-1))
        Theta     = np.pi*(np.arange(float(2*sz_out))/float(sz_out-1)-1)
        R         = sz_src*Phi/vfov

        map_x     = (np.dot(R[:].reshape(sz_out,1),np.cos(Theta).reshape(1,2*sz_out))).astype('float32')+0.5*sz_src
        map_y     = (np.dot(R[:].reshape(sz_out,1),np.sin(Theta).reshape(1,2*sz_out))).astype('float32')+0.5*sz_src

    return map_x, map_y

def main():
    conf_file = Path('config.txt')
    in_sz_src=0
    in_sz_out=0
    in_fov = 0
    in_qvert=0
    in_delta=0
    if conf_file.is_file():
        f = open('config.txt','r')
        for line in f:
            if line[0:2]=='src':
                conf['src']=int(line[line.index('=')+1:])
            if line[0:2]=='out':
                conf['out']=int(line[line.index('=')+1:])
            if line[0:2]=='fov':
                conf['fov']=int(line[line.index('=')+1:])
            if line[0:2]=='v/h':
                vnh=line[line.index('=')+1:]
                conf['vnh']=int(vnh=='v')
            if line[0:2]=='del':
                conf['del']=int(line[line.index('=')+1:])
        f.close()
    else:
        conf['src']   = int(input('Source image size:'))
        conf['out']   = int(input('Output image size:'))
        conf['fov']   = int(input('Fov:'))
        in_qvert      = input('Position(v/h):')
        conf['vnh']   = int(in_qvert=='v')
        conf['del']   = int(input('Boundary smooth delta:'))

    sz_src= conf['src']
    sz_out= conf['out'] 
    fov   = float(conf['fov'])
    delta = conf['del']
    qvert = conf['vnh']==1

    # build map
    mapstart  = int(round(time.time() * 1000))
    mapx,mapy = buildMap(sz_src,sz_out,fov,qvert)
    mapstop   = int(round(time.time() * 1000))

    if _debug>=1:
        print("Build map cost %d msec" % (mapstop-mapstart))

    np.save('mapx',mapx)
    np.save('mapy',mapy)

    if _debug >= 1:
        print('Map saved as mapx, mapy')

    vfilter = np.ones((1,2*sz_out,1),np.float32)
    for i in range(int(0.5*sz_out-delta),int(0.5*sz_out+delta)):
        vfilter[0,i,0] = 0.5*np.cos(float(i-(0.5*sz_out+delta))/float(delta)*np.pi/2.0)+0.5
    for i in range(int(1.5*sz_out-delta),int(1.5*sz_out+delta)):
        vfilter[0,i,0] = 0.5*np.cos(float(i-(1.5*sz_out-delta))/float(delta)*np.pi/2.0)+0.5

    np.save('vfilter',vfilter)

    if _debug >= 1:
        print('Boundary filer saved as vfilter')


if __name__ == "__main__":
   main()



