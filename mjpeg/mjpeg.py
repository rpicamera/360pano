'''
    Author: Craig Li - rpi.camera.studio@gmail.com
    A Simple mjpg stream http server modified from Igor Maculan
'''
import io
import cv2
import time
import picamera
import threading
import numpy as np

from PIL            import Image
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer   import ThreadingMixIn


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            for foo in camera.capture_continuous(stream, 'jpeg'):
                try:
                    stream.seek(0)
                    jpg = Image.open(stream)
                    self.wfile.write("--jpgboundary")
                    self.send_header('Content-type','image/jpeg')
                    self.send_header('Content-length',str(len(stream.read())))
                    self.end_headers()
                    jpg.save(self.wfile,'JPEG')

                    stream.seek(0)
                    stream.truncate()
                except KeyboardInterrupt:
                    break
            return
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://127.0.0.1:8080/cam.mjpg"/>')
            self.wfile.write('</body></html>')
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main():
    global camera
    global stream
    camera = picamera.PiCamera()
    camera.resolution = (341, 256)
    camera.start_preview()
    time.sleep(2)

    stream = io.BytesIO()
    
    try:
        server = ThreadedHTTPServer(('localhost', 8080), CamHandler)
        print "server started"
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main()
