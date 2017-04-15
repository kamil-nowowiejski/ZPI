import BaseHTTPServer
import socket


class HTTPServer:

    def __init__(self):
        pass

    def run(self):
        ip = socket.gethostbyname(socket.gethostname())
        address = (ip, 8080)
        server = BaseHTTPServer.HTTPServer(address, Handler)
        server.serve_forever()


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        '''do something with data - go forward, turn or something'''
        self.send_response(200)
        self.send_header('content-type', 'text/plain')
        self.end_headers()

