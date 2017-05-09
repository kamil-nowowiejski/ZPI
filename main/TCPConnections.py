import socket
import numpy as np
import threading
import time
from resources import res
from cStringIO import StringIO


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


def _send_message(connection, message):
    connection.sendall(message)


def _receive_response(connection):
    chunks = ''
    buffer_size = res('tcp_server\\buffer_size')
    while True:
        chunk = connection.recv(buffer_size)
        if not chunk:
            break
        chunks += chunk
    return chunks


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
            '''here we do stuff with image'''
            message = 'ala ma kota'
            time.sleep(3)

            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (client_address[0], res('tcp_server\\client_port'))
            send_socket.connect(server_address)
            send_socket.sendall(message)
            send_socket.close()


