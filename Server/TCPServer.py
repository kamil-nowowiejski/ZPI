import socket
import numpy as np
from threading import Thread
from time import sleep
from resources import res
from cStringIO import StringIO
import Tkinter as tk
import cv2
from PIL import Image, ImageTk
import errno
from object import Shape
import enums


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


class TCPServerManager(TCPServer):

    def __init__(self, context):
        super(TCPServerManager, self).__init__((res('tcp_server\\ip'), res('tcp_server\\server_port')))
        self.agents = []
        self.name = 'Manager'
        self.context = context

    def stop(self):
        for agent in self.agents:
            agent.stop()
        sleep(2)
        super(TCPServerManager, self).stop()

    def run(self):
        self.receive_socket.bind(self.address)
        self.receive_socket.settimeout(0.5)
        self.receive_socket.listen(1)
        print 'manager server started on: %s' % self.address[1]
        while not self._stop:
            try:
                connection, client_address = self.receive_socket.accept()
            except socket.timeout:
                sleep(1)
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
                            agent = TCPServerAgent(self.context,
                                                   (message.split('|')[1].split(':')[0],
                                                    int(message.split('|')[1].split(':')[1])),
                                                   message.split('|')[2])
                            self.agents.append(agent)
                            agent.start()
                connection.close()
        self.send_socket.close()
        self.receive_socket.close()
        print 'manager server stopped'


class TCPServerAgent(TCPServer):

    def __init__(self, context, send_address, name):
        super(TCPServerAgent, self).__init__(('', 0))
        self.send_address = send_address
        self.name = 'Agent Server'
        self.agent_name = name
        self.context = context
        self.context.agents_list.insert(tk.END, self.agent_name)
        self.autonomous = True
        self.feed = False

    def run(self):
        self.receive_socket.bind(self.address)
        self.send_socket.connect(self.send_address)
        self.address = (res('tcp_server\\ip'), self.receive_socket.getsockname()[1])
        self._send('REGISTER|%s:%s' % (self.address[0], self.address[1]))
        self.receive_socket.settimeout(0.5)
        self.receive_socket.listen(1)
        print 'agent server started'
        while not self._stop:
            try:
                connection, client_address = self.receive_socket.accept()
            except socket.timeout:
                sleep(1)
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
                        self.process_request(message)
        self.send_socket.close()
        self.receive_socket.close()
        print 'agent server stopped'

    def process_request(self, message):
        if message == 'LOGIC_ON':
            self.autonomous = True
            self.context.update_info()
        elif message == 'LOGIC_OFF':
            self.autonomous = False
            self.context.update_info()
        elif message == 'FEED_ON':
            self.feed = True
            self.context.update_info()
        elif message == 'FEED_OFF':
            self.feed = False
            self.context.update_info()
        elif self.feed and message.split('|')[0] == 'FEED':
            image = np.load(StringIO(message[5:]))['frame']
            b, g, r = cv2.split(image)
            image = cv2.merge((r, g, b))
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image=image)
            self.context.video_feed.create_image(480, 320, image=image)
            self.context.video_feed.frame = image
        elif message.split('|')[0] == 'DETECT':
            message = message.split('|')
            objects = []
            offset = 2
            for i in range(int(message[1])):
                type = int(message[offset])
                height = int(message[offset + 1])
                width = int(message[offset + 2])
                color = int(message[offset + 3])
                symbol_count = int(message[offset + 4])
                offset += 5
                symbols = []
                for j in range(symbol_count):
                    s_type = int(message[offset])
                    s_height = int(message[offset + 1])
                    s_width = int(message[offset + 2])
                    s_color = int(message[offset + 3])
                    offset += 4
                    symbols.append(Shape(enums.Shape(s_type), enums.Size(s_height),
                                         enums.Size(s_width), enums.Color(s_color)))
                objects.append(Shape(enums.Shape(type), enums.Size(height),
                                     enums.Size(width), enums.Color(color), symbols))
            self.context.show_detected(objects)
        elif message.split('|')[0] == 'PROCESS':
            pass

    def shutdown(self):
        self._send('SHUTDOWN')
        for i in range(self.context.agents_list.size()):
            if self.context.agents_list.get(i) == self.agent_name:
                self.context.agents_list.delete(i)
                break
        self.stop()

    def switch_logic(self):
        if self.autonomous:
            self._send('LOGIC_OFF')
        else:
            self._send('LOGIC_ON')

    def switch_feed(self):
        if self.feed:
            self._send('FEED_OFF')
        else:
            self._send('FEED_ON')

    def detect(self):
        self._send('DETECT')

    def __str__(self):
        return self.agent_name
