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
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:8003")

    #def set_GUI_parameter(self, name, value, GUI_name):
    def send_RPC(self, function_name, *args):
        msg = [function_name, *args]
        msg = pickle.dumps(msg)
        self.socket.send(msg)
        message = self.socket.recv()
        if message == b'Success':
            logger.info(function_name + ' success')
        if message == b'Error':
            logger.error(function_name + ' not available in the server')
