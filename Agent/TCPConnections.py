import socket
from threading import Thread
from time import sleep

import main_loop
from resources import res


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


class TCPAgent(TCPServer):

    def __init__(self):
        super(TCPAgent, self).__init__(('', 0))
        self.name = 'Agent'

    def run(self):
        self.receive_socket.bind(self.address)
        self.receive_socket.settimeout(2)
        self.receive_socket.listen(1)
        self.address = (res('tcp_server\\ip'), self.receive_socket.getsockname()[1])
        self.send_socket.connect((res('tcp_server\\ip'), res('tcp_server\\server_port')))
        self._send('REGISTER|%s:%d|Andrzej' % (self.address[0], self.address[1]))
        timeouts = 0
        print 'agent started'
        while not self._stop:
            try:
                connection, client_address = self.receive_socket.accept()
            except socket.timeout:
                sleep(2)
                timeouts += 1
                if timeouts == 10:
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
                        if message.split('|')[0] == 'REGISTER':
                            send_address = (message.split('|')[1].split(':')[0], int(message.split('|')[1].split(':')[1]))
                            self.send_socket.close()
                            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            self.send_socket.connect(send_address)
                            print 'agent connected'
                        elif message == 'SHUTDOWN':
                            main_loop.Main.stop[0] = True
        print 'agent stopped'
        self.send_socket.close()
        self.receive_socket.close()


'''
def remotely_process_image(image):
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (res('tcp_server\\ip'), res('tcp_server\\server_port'))
    send_socket.connect(server_address)

    f = StringIO()
    np.savez_compressed(f, frame=image)
    f.seek(0)
    out = f.read()
    _send_message(send_socket, out)
    send_socket.close()

    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_address = (res('agent_info\\ip'), res('tcp_server\\client_port'))
    receive_socket.bind(my_address)
    receive_socket.listen(1)
    connection, _ = receive_socket.accept()
    msg = _receive_response(connection)
    receive_socket.close()

    return msg


class TCPServer:

    def __init__(self):
        pass

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_address = (res('tcp_server\\ip'), res('tcp_server\\server_port'))
        sock.bind(my_address)
        sock.listen(1)
        print 'server started'
        while True:
            connection, client_address = sock.accept()
            chunks = _receive_response(connection)
            connection.close()

            print 'received image'
            image = np.load(StringIO(chunks))['frame']
            ''''''here we do stuff with image''''''
            message = 'ala ma kota'
            time.sleep(3)

            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (client_address[0], res('tcp_server\\client_port'))
            send_socket.connect(server_address)
            send_socket.sendall(message)
            send_socket.close()
'''
