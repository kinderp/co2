from co2.ipc import Server

server = Server('/tmp/uds_socket')
server.start()
