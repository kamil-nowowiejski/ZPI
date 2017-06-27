import socket
from threading import Thread
from time import sleep
import main_loop
from resources import res, ares
import numpy as np
from cStringIO import StringIO
from object import Shape, CombinedObject
import errno
import database as db


class TCPServer(Thread):

    def __init__(self, address):
        super(TCPServer, self).__init__()
        self._stop = False
        self.address = address
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._overflow = None

    def stop(self):
        self._stop = True

    def run(self):
        while not self._stop:
            sleep(1)
        self.send_socket.close()
        self.receive_socket.close()

    def _send(self, message):
        message = '%d|%s' % (len(message), message)
        self.send_socket.sendall(message)
        if len(message) > 60:
            message = message[:20] + '...' + message[-20:]
        if main_loop.Main.debug_tcp:
            print '[TCP] %s:%d -> %s' % (self.send_socket.getsockname()[0], self.send_socket.getsockname()[1], message)

    def _receive(self, connection):
        chunks = ''
        command = ''
        if self._overflow is not None:
            chunks = self._overflow
            self._overflow = None
        buffer_size = res('tcp_server\\buffer_size')
        timeouts = 0
        connection.settimeout(0.1)
        while True:
            try:
                chunk = connection.recv(buffer_size)
            except socket.timeout:
                timeouts += 1
                if timeouts == 5:
                    break
            except socket.error, e:
                if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                    break
                else:
                    break
            else:
                if not chunk:
                    break
                chunks += chunk
                timeouts = 0
        if chunks:
            length = int(chunks.split('|')[0])
            command = chunks[len(str(length)) + 1:len(str(length)) + 1 + length]
            if len(chunks) > len(str(length)) + 1+ length:
                self._overflow = chunks[len(str(length)) + 1 + length:]
            if len(chunks) > 60:
                message = chunks[:20] + '...' + chunks[-20:]
            else:
                message = chunks
            if main_loop.Main.debug_tcp:
                print '[TCP] %s:%d <- %s' % (self.receive_socket.getsockname()[0], self.receive_socket.getsockname()[1], message)
        return command


class TCPAgent(TCPServer):

    def __init__(self, context):
        super(TCPAgent, self).__init__(('', 0))
        self.name = 'Agent'
        self.context = context
        self.connected = False
        self.feed = False
        self.autonomous = True
        self.aruco = None
        self.has_aruco = False
        self.received_aruco_answer = False

    def run(self):
        self.receive_socket.bind(self.address)
        self.receive_socket.settimeout(2)
        self.receive_socket.listen(1)
        self.address = (ares('agent_info\\ip'), self.receive_socket.getsockname()[1])
        self.send_socket.connect((res('tcp_server\\ip'), res('tcp_server\\server_port')))
        self._send('REGISTER|%s:%d|%s' % (self.address[0], self.address[1], ares('agent_info\\name')))
        timeouts = 0
        if main_loop.Main.debug_tcp:
            print '[TCP] Server started'
        while not self._stop:
            try:
                connection, client_address = self.receive_socket.accept()
            except socket.timeout:
                sleep(0.5)
                timeouts += 1
                if timeouts == 5:
                    self.stop()
            except socket.error:
                if main_loop.Main.debug_tcp:
                    print '[TCP] Socket error'
                self.stop()
            else:
                while not self._stop:
                    try:
                        message = self._receive(connection)
                    except socket.timeout:
                        if main_loop.Main.debug_tcp:
                            print '[TCP] Socket timeout'
                    except socket.error:
                        if main_loop.Main.debug_tcp:
                            print '[TCP] Socket error'
                        self.stop()
                    else:
                        self.process_request(message)
        if main_loop.Main.debug_tcp:
            print '[TCP] Server stopped'
        self.send_socket.close()
        self.receive_socket.close()

    def process_request(self, message):
        if message.split('|')[0] == 'REGISTER':
            send_address = (message.split('|')[1].split(':')[0], int(message.split('|')[1].split(':')[1]))
            self.send_socket.close()
            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.send_socket.connect(send_address)
            self.connected = True
            if main_loop.Main.debug_tcp:
                print '[TCP] Server connected'
        elif message == 'SHUTDOWN':
            main_loop.Main.stop[0] = True
        elif message == 'LOGIC_ON':
            self.autonomous = True
            self._send('LOGIC_ON')
        elif message == 'LOGIC_OFF':
            self.autonomous = False
            self._send('LOGIC_OFF')
        elif message == 'FEED_ON':
            self.feed = True
            self._send('FEED_ON')
        elif message == 'FEED_OFF':
            self.feed = False
            self._send('FEED_OFF')
        elif message.split('|')[0] == 'ARUCO':
            parts = message.split('|')
            if parts[1] == 'None':
                self.aruco = None
            else:
                self.aruco = ([float(parts[1]), float(parts[2]), float(parts[3])],
                              [float(parts[4]), float(parts[5]), float(parts[6])])
            self.has_aruco = True
            self.received_aruco_answer = True
        elif message.split('|')[0] == 'PROCESS':
            parts = message.split('|')
            objects = []
            offset = 3
            for i in range(int(parts[1])):
                if parts[offset - 1] == '0':
                    obj, offset = Shape.from_repr(message, offset)
                else:
                    obj, offset = CombinedObject.from_repr(message, offset)
                objects.append(obj)
                offset += 1
            for obj in objects:
                db.insert(obj)
                if main_loop.Main.debug_db:
                    print '[SQL] %s' % str(obj)

    def send_feed(self, image):
        sio = StringIO()
        np.savez_compressed(sio, frame=image)
        sio.seek(0)
        data = sio.read()
        self._send('FEED|%s' % data)

    def find_aruco(self, image):
        sio = StringIO()
        np.savez_compressed(sio, frame=image)
        sio.seek(0)
        data = sio.read()
        self._send('ARUCO|%s' % data)

    def process_image(self, image):
        sio = StringIO()
        np.savez_compressed(sio, frame=image)
        sio.seek(0)
        data = sio.read()
        self._send('PROCESS|%s' % data)
