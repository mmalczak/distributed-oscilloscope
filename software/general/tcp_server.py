import socket
import zmq

class TCPServer:
   
    mess_length_size = 10
    READ_ONLY = zmq.POLLIN | zmq.POLLERR 
    
    def __init__(self, ip, port, poller):
        self.ip = ip
        self.port = port
        self.poller = poller
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        self.fd_conn = {}

    def receive_packet(self, fd):
        conn = self.fd_conn[fd]

        mess_size = self.receive_message(conn, fd, self.mess_length_size)
        mess_size = int(mess_size)

        data = self.receive_message(conn, fd, mess_size)
        return data

    def receive_message(self, conn, fd, size):
        buff = b''
        total_bytes = 0

        while(total_bytes < size):
            data = self.receive_trunc(conn, fd, size - total_bytes)
            total_bytes += len(data)
            buff += data
        return buff

    def receive_trunc(self, conn, fd, size):
        trunc = conn.recv(size)
        if not trunc:
            self.unregister_connection(fd)
            return None
        else:
            return trunc

    def register_connection(self):
        conn, addr = self.socket.accept()
        self.fd_conn[conn.fileno()] =  conn
        self.poller.register(conn, self.READ_ONLY)
        print('Connection address: ' + str(addr))

    def unregister_connection(self, fd):
        conn = self.fd_conn[fd] 
        self.poller.unregister(conn)
        conn.close()
        del self.fd_conn[fd]
        print("No data, finish")
