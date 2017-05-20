import socket
import numpy as np
from threading import Thread
from time import sleep
from resources import res
from cStringIO import StringIO


class TCPServer(Thread):

    def __init__(self, address):
        super(TCPServer, self).__init__()
        self._stop = False
        self.address = address
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def stop(self):
        sleep(5)
        self._stop = True

    def run(self):
        while not self._stop:
            sleep(1)
        self.send_socket.close()
        self.receive_socket.close()

    def _send(self, message):
        self.send_socket.sendall(message)
        print '%d -> %s' % (self.address[1], message)

    def _receive(self, connection):
        chunks = ''
        buffer_size = res('tcp_server\\buffer_size')
        errors = 0
        timeouts = 0
        while True:
            try:
                chunk = connection.recv(buffer_size)
            except socket.timeout:
                sleep(1)
                timeouts += 1
                if timeouts == 10:
                    raise socket.timeout
            except socket.error:
                errors += 1
                if errors == 5:
                    break
            else:
                if not chunk:
                    break
                chunks += chunk
                errors = 0
        if chunks:
            print '%d <- %s' % (self.address[1], chunks)
        return chunks


class TCPServerManager(TCPServer):

    def __init__(self):
        super(TCPServerManager, self).__init__((res('tcp_server\\ip'), res('tcp_server\\server_port')))
        self.agents = []
        self.name = 'Manager'

    def stop(self):
        for agent in self.agents:
            agent.stop()
        super(TCPServerManager, self).stop()

    def run(self):
        self.receive_socket.bind(self.address)
        self.receive_socket.settimeout(2)
        self.receive_socket.listen(1)
        print 'manager server started'
        while not self._stop:
            try:
                connection, client_address = self.receive_socket.accept()
            except socket.timeout:
                sleep(2)
            except socket.error:
                print 'manager server error'
                self.stop()
            else:
                try:
                    message = self._receive(connection)
                except socket.timeout:
                    pass
                except socket.error:
                    pass
                else:
                    if message:
                        if message.split('|')[0] == 'REGISTER':
                            agent = TCPServerAgent((message.split('|')[1].split(':')[0],
                                                    int(message.split('|')[1].split(':')[1])),
                                                   message.split('|')[2])
                            self.agents.append(agent)
                            agent.start()
                connection.close()
        self.send_socket.close()
        self.receive_socket.close()
        print 'manager server stopped'


class TCPServerAgent(TCPServer):

    def __init__(self, send_address, name):
        super(TCPServerAgent, self).__init__(('', 0))
        self.send_address = send_address
        self.name = 'Agent Server'

    def run(self):
        self.receive_socket.bind(self.address)
        self.send_socket.connect(self.send_address)
        self.address = (res('tcp_server\\ip'), self.receive_socket.getsockname()[1])
        self._send('REGISTER|%s:%s' % (self.address[0], self.address[1]))
        self.receive_socket.settimeout(2)
        self.receive_socket.listen(1)
        print 'agent server started'
        while not self._stop:
            try:
                connection, client_address = self.receive_socket.accept()
            except socket.timeout:
                sleep(2)
            except socket.error:
                print 'agent server error'
                self.stop()
            else:
                while not self._stop:
                    try:
                        message = self._receive(connection)
                    except socket.timeout:
                        print 'agent server timeout'
                    except socket.error:
                        print 'agent server error'
                        self.stop()
                    else:
                        sleep(2)
        self.send_socket.close()
        self.receive_socket.close()
        print 'agent server stopped'

    def shutdown(self):
        self._send('SHUTDOWN')
        self.stop()
