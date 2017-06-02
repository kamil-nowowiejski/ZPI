import socket
from threading import Thread
from time import sleep
import main_loop
from resources import res, ares
import numpy as np
from cStringIO import StringIO

import random as r


class TCPServer(Thread):

    def __init__(self, address):
        super(TCPServer, self).__init__()
        self._stop = False
        self.address = address
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def stop(self):
        self._stop = True

    def run(self):
        while not self._stop:
            sleep(1)
        self.send_socket.close()
        self.receive_socket.close()

    def _send(self, message):
        self.send_socket.sendall(message)
        print '%s:%d -> %s' % (self.send_socket.getsockname()[0], self.send_socket.getsockname()[1], message)

    def _receive(self, connection):
        chunks = ''
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
            print '%s:%d <- %s' % (self.receive_socket.getsockname()[0], self.receive_socket.getsockname()[1], chunks)
        return chunks


class TCPAgent(TCPServer):

    def __init__(self, context):
        super(TCPAgent, self).__init__(('', 0))
        self.name = 'Agent'
        self.context = context
        self.connected = False
        self.feed = False
        self.autonomous = True

    def run(self):
        self.receive_socket.bind(self.address)
        self.receive_socket.settimeout(2)
        self.receive_socket.listen(1)
        self.address = (ares('agent_info\\ip'), self.receive_socket.getsockname()[1])
        self.send_socket.connect((res('tcp_server\\ip'), res('tcp_server\\server_port')))
        # temporary workaround
        # r.seed(None)
        # self._send('REGISTER|%s:%d|%d' % (self.address[0], self.address[1], r.randint(1000, 9999)))
        self._send('REGISTER|%s:%d|%s' % (self.address[0], self.address[1], ares('agent_info\\name')))
        timeouts = 0
        print 'agent started'
        while not self._stop:
            try:
                connection, client_address = self.receive_socket.accept()
            except socket.timeout:
                sleep(0.5)
                timeouts += 1
                if timeouts == 5:
                    self.stop()
            except socket.error:
                print 'agent error'
                self.stop()
            else:
                while not self._stop:
                    try:
                        message = self._receive(connection)
                    except socket.timeout:
                        print 'agent timeout'
                    except socket.error:
                        print 'agent error'
                        self.stop()
                    else:
                        self.process_request(message)
        print 'agent stopped'
        self.send_socket.close()
        self.receive_socket.close()

    def process_request(self, message):
        if message.split('|')[0] == 'REGISTER':
            send_address = (message.split('|')[1].split(':')[0], int(message.split('|')[1].split(':')[1]))
            self.send_socket.close()
            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.send_socket.connect(send_address)
            print 'agent connected'
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
        elif message == 'DETECT':
            _, image = self.context.camera_manager.read()
            objects = self.context.detector.detect_objects(image)
            for obj in objects:
                self.context.db.insert(obj)
            self.send_detection(objects)
        elif message.split('|')[0] == 'PROCESS':
            pass

    def send_feed(self, image):
        sio = StringIO()
        np.savez_compressed(sio, frame=image)
        sio.seek(0)
        data = sio.read()
        self._send('FEED|%s' % data)

    def send_detection(self, objects):
        message = 'DETECT|%d' % len(objects)
        for obj in objects:
            message += '|%d|%d|%d|%d|%d' % (obj.type.value, obj.height.value, obj.width.value,
                                            obj.color.value, len(obj.symbols))
            for sym in obj.symbols:
                message += '|%d|%d|%d|%d' % (sym.type.value, sym.height.value, sym.width.value, sym.color.value)
        self._send(message)

    def process_image(self, image):
        sio = StringIO()
        np.savez_compressed(sio, frame=image)
        sio.seek(0)
        data = sio.read()
        self._send('PROCESS|%s' % data)
