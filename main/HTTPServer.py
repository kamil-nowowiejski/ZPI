import BaseHTTPServer
import socket
import main_loop
from resources import res
from threading import Thread


class HTTPServer(BaseHTTPServer.HTTPServer):

    def __init__(self):
        self.address = (socket.gethostbyname(socket.gethostname()), res('http_server\\port'))
        print self.address
        BaseHTTPServer.HTTPServer.__init__(self, self.address, Handler)

    def close(self):
        self.shutdown()
        self.socket.close()

    def start(self):
        Thread(target=self.serve_forever).start()


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        '''do something with data - go forward, turn or something'''
        if data == '{command: exit}':
            main_loop.Main.stop[0] = True
        self.send_response(200)
        self.send_header('content-type', 'text/plain')
        self.end_headers()
