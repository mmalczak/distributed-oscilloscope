import zmq
from DistScopeUtilities import serialization
import logging
logger = logging.getLogger(__name__)


class Publisher():

    def __init__(self, ip, port):
        """TODO should I add some logging here or some error handling?"""
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
        addr = str(ip) + ':' + str(port)
        self.socket.connect("tcp://" + addr)

    def send_message(self, data):
        msg = serialization.serialize(data)
        self.socket.send(msg)


class PublisherIPC():

    def __init__(self, ipc_name):
        """TODO should I add some logging here or some error handling?"""
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
        self.socket.connect("ipc:///tmp/" + ipc_name)

    def send_message(self, data):
        msg = pickle.dumps(data)
        self.socket.send(msg)
