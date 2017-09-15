'''
    Author: Craig Li - rpi.camera.studio@gmail.com
    A 360 pano mjpg stream http server
'''
import io
import time
import threading
import urllib,cStringIO,StringIO

from PIL            import Image
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer   import ThreadingMixIn

ip="192.168.1.7"

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while(True):
                try:
                    file = cStringIO.StringIO(urllib.urlopen("http://raspberrypi.local/picam/cam.jpg").read())
                    jpgslv = Image.open(file,'r')
                    jpgmst = Image.open('/dev/shm/mjpeg/cam.jpg','r')
                    width,height = jpgmst.size
                    jpg = Image.new("RGB",(2*width,height))
                    jpg.paste(jpgmst,(0,0))
                    jpg.paste(jpgslv,(width,0))
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

def main():
    stream = io.BytesIO()

    try:
        server = ThreadedHTTPServer((ip, 8080), CamHandler)
        print "server started"
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main()
