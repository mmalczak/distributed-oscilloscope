import zmq
import pickle

import logging
import logging.config
from logging_conf import DEFAULT_CONFIG

logging.config.dictConfig(DEFAULT_CONFIG)
logger = logging.getLogger(__name__)

class ZMQ_RPC():
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
#        self.socket.setsockopt(zmq.IDENTITY, b'GUI')
        self.socket.setsockopt(zmq.RCVTIMEO, 3000)
#        self.socket.connect("tcp://localhost:8003")
        self.socket.connect("tcp://128.141.79.50:8003")

    #def set_GUI_parameter(self, name, value, GUI_name):
    def send_RPC(self, function_name, *args):
        msg = [function_name, *args]
        msg = pickle.dumps(msg)
        self.socket.send(msg)
        try:
            message = self.socket.recv()
        except Exception as e:
            logger.error("Server not replying")
            """TODO decide what to do: close application, save conf,
            or sth. else"""
            return None
        if message == b'Success':
            logger.info(function_name + ' success')
        if message == b'Error':
            logger.error(function_name + ' not available in the server')
