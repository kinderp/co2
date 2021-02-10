import socket
import sys
import json

class Client:
    def __init__(self):
        self.server_address = '/tmp/uds_socket'
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        print('connecting to {}'.format(self.server_address))
        try:
            self.sock.connect(self.server_address)
        except socket.error as msg:
            print(msg)
            sys.exit(1)

    def execute(self, command):
        try:
            # Send data.
            message = json.dumps(command.to_dict())
            print('sending {}'.format(message))
            self.sock.sendall(message.encode('utf-8'))
            response = self.sock.recv(1024)
            print('Received response: {}'.format(response.decode('utf-8',
                                                               errors='replace')))
            return response
        finally:
            print('closing socket')
            self.sock.close()

