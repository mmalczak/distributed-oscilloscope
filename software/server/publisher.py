import zmq
import pickle

import logging
logger = logging.getLogger(__name__)


class Publisher():
    def __init__(self, ip, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
        addr = str(ip) + ':' + str(port)
        self.socket.connect("tcp://" + addr)

    def send_message(self, data):
        msg = pickle.dumps(data)
        self.socket.send(msg)
