import socket
import sys
import os
import struct
import json

from co2.core.interfaces.kernel import _SYSCALL

class SERVER:
    def __init__(self, socket_address: str = '/tmp/uds_socket'):
        self.server_address = socket_address
        # Make sure the socket does not already exist. try:
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                raise

        # Create a UDS socket.
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        # Bind the socket to the address.
        print('starting up on {}'.format(self.server_address))
        self.sock.bind(self.server_address)


    def start(self):
        # Listen for incoming connections.
        self.sock.listen(1)
        while True:
            # Wait for a connection.
            print('waiting for a connection')
            connection, client_address = self.sock.accept()
            try:
                print('connection from', client_address)
                # Receive the data in small chunks and retransmit it.
                while True:
                    received = connection.recv(1024)
                    if not received: break
                    message = received.decode('utf-8', errors='replace')
                    print("Received command:\n")
                    print(message)
                    # return a response
                    command = json.loads(message)
                    exit = _SYSCALL(
                        num=command['code'], args=command['data']
                    )
                    response = {"code": 0, "description": exit}
                    print("Sent response:\n")
                    print(response)
                    connection.sendall(json.dumps(response).encode('utf-8'))
                connection.close()
                print("Disconnected from: {}".format(client_address))
            finally:
                    # Clean up the connection.
                    connection.close()

class IO(SERVER):
    def __init__(self, socket_address : str):
       super().__init__(socket_address)


class PS(SERVER):
    def __init__(self, socket_address : str):
       super().__init__(socket_address)
