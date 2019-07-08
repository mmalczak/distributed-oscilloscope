import zmq
import socket
from general import serialization
import logging
logger = logging.getLogger(__name__)


class Publisher:
    
    message_length_size = 10
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("socket created")
        self.socket.connect((self.ip, self.port))
        print("socket connected")

    def send_message(self, data):
        msg = serialization.serialize(data)
        length = str(len(msg)).encode('utf-8')
        length = length.rjust(self.message_length_size, b'0')
        self.socket.send(length)
        self.socket.send(msg)

    def __del__(self):
        self.socket.close()


class PublisherIPC():

    def __init__(self, ipc_name):
        """TODO should I add some logging here or some error handling?"""
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
        self.socket.connect("ipc:///tmp/" + ipc_name)

    def send_message(self, data):
        msg = pickle.dumps(data)
        self.socket.send(msg)


