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


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while(True):
                try:
                    file = cStringIO.StringIO(urllib.urlopen("http://raspberrypi.local/picam/cam.jpg").read())
                    jpg = Image.open(file,'r')
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
            self.wfile.write('<img src="http://192.168.1.6:8080/cam.mjpg"/>')
            self.wfile.write('</body></html>')
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Handle requests in a separate thread. """

def main():
    stream = io.BytesIO()

    try:
        server = ThreadedHTTPServer(('192.168.1.6', 8080), CamHandler)
        print "server started"
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main()
