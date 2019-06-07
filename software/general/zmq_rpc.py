import zmq
import pickle

import logging
logger = logging.getLogger(__name__)

class ZMQ_RPC():
    def __init__(self, ip, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
#        self.socket.setsockopt(zmq.IDENTITY, b'GUI')
        self.socket.setsockopt(zmq.RCVTIMEO, 3000)
#        self.socket.connect("tcp://localhost:8003")
        addr = str(ip) + ':' + str(port)
        self.socket.connect("tcp://" + addr)

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
        if message == b'Error':
            logger.error(function_name + ' not available in the server')
        else:
            ret = pickle.loads(message)
            logger.info(function_name + ' success')
            return ret
