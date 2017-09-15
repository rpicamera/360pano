import io
import cv2
import time
import threading
import numpy as np
import urllib,StringIO

from PIL            import Image
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer   import ThreadingMixIn

_debug=1
ip="192.168.1.7"

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while(True):
                try:
                    imgMstRGB = cv2.imread('/dev/shm/mjpeg/cam.jpg')
                    imgMstRGB = cv2.resize(imgMstRGB,(171,128))
                    imgMstRGB = imgMstRGB[mtop:width,mleft:(mleft+width)]
                    imgMstRGB = cv2.remap(imgMstRGB,xmap,ymap,cv2.INTER_LINEAR)

                    resp = urllib.urlopen("http://raspberrypi.local/picam/cam.jpg")
                    image = np.asarray(bytearray(resp.read()), dtype="uint8")
                    imgSlvRGB = cv2.imdecode(image, cv2.IMREAD_COLOR)
                    imgSlvRGB = cv2.resize(imgSlvRGB,(171,128))
                    imgSlvRGB = imgSlvRGB[mtop:width,mleft:(mleft+width)]
                    imgSlvRGB = cv2.remap(imgSlvRGB,xmap,ymap,cv2.INTER_LINEAR)
                    
                    imgRGB = imgSlvRGB[73:146,0:width]+imgMstRGB[73:219,0:width]
                    imgRGB = imgRGB[0:219,0:width]+imgSlvRGB[73:146,0:width]

                    jpg = Image.fromarray(imgRGB)
                    tmpFile = StringIO.StringIO()
                    jpg.save(tmpFile,'JPEG')

                    self.wfile.write("--jpgboundary")
                    self.send_header('Content-type','image/jpeg')
                    self.send_header('Content-length',str(tmpFile.len))
                    self.end_headers()
                    jpg.save(self.wfile,'JPEG')

                except KeyboardInterrupt:
                    break
            return
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://'+ip+':8080/cam.mjpg"/>')
            self.wfile.write('</body></html>')
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Handle requests in a separate thread. """

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

def main():
    global xmap,ymap
    global width
    global mleft
    global mtop

    mleft = 15
    mtop = 0
    width= 146

    fov=float(220)
    xmap,ymap = buildMap(width,width,fov,True)

    try:
        server = ThreadedHTTPServer((ip, 8080), CamHandler)
        print "server started"
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main()
