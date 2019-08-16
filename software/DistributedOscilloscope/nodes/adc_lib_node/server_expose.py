import sys
import os
import zmq
from zmq.utils.monitor import recv_monitor_message
from zmq.utils.monitor import parse_monitor_message
import pickle
import time
from DistributedOscilloscope.utilities.publisher import Publisher
from DistributedOscilloscope.utilities.ipaddr import get_ip
from .devices_access import DevicesAccess
import logging
logger = logging.getLogger(__name__)

thismodule = sys.modules[__name__]


class ServerExpose():

    def __init__(self, port, port_server, pci_addr, trtl, unique_ADC_name):
        self.__port = port
        self.__port_server = port_server
        self.server_publisher = None
        self.__devices_access = DevicesAccess(pci_addr, trtl, unique_ADC_name)

    def __getattr__(self, function_name):
        """ If he requered function is not defined here, look for it in the
        devices_access object"""
        return getattr(self.__devices_access, function_name)

    def set_server_address(self, addr):
        self.server_publisher = Publisher(addr, self.__port_server)

    def set_user_app_name(self, user_app_name):
        self.__devices_access.set_user_app_name(user_app_name)

    def exit(self):
        """This fucntion is just for testing and will be removed after
        addding ZeroMQ"""
        """doesn'r work with zeroconf"""
        data = {'function_name': 'unregister_ADC',
                                 'args': [self.__devices_access.unique_ADC_name]}
        self.server_publisher.send_message(data)
        time.sleep(0.1)  # otherwise the message is lost
        os._exit(1)

    def run(self):

        context = zmq.Context()
        socket = context.socket(zmq.ROUTER)
        monitor = socket.get_monitor_socket()
        ip = get_ip()
        port_zmq = str(self.__port)
        socket.bind("tcp://" + ip + ":" + port_zmq)

        poller = zmq.Poller()
        poller.register(monitor, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket, zmq.POLLIN | zmq.POLLERR)

        EVENT_MAP = {}
        for name in dir(zmq):
            if name.startswith('EVENT_'):
                value = getattr(zmq, name)
                EVENT_MAP[value] = name

        self.__devices_access.selector = poller
        while True:
            socks = dict(poller.poll())
            if socket in socks:
                [identity, message] = socket.recv_multipart()
                message = pickle.loads(message)
                try:
                    func = getattr(self, message[0])
                    ret = func(*message[1:])
                    ret = pickle.dumps(ret)
                    socket.send_multipart([identity, ret])
                except AttributeError:
                    socket.send_multipart([identity, b"Error"])
            if monitor in socks:
                evt = recv_monitor_message(monitor)
                evt.update({'description': EVENT_MAP[evt['event']]})
                # logger.info("Event: {}".format(evt))

            if self.__devices_access.fileno() in socks:
                dev_ac = self.__devices_access
                try:
                    poller.unregister(dev_ac)
                    logger.debug("The ADC device unregistered from the poller "
                                "selector")
                except KeyError:
                    logger.warning("The ADC device not available to unregister"
                                   " from the poller selector, expose")

                [timestamp, pre_post, data] = dev_ac.retrieve_ADC_data()
                data = {'function_name': 'update_data',
                        'args': [timestamp, pre_post, data,
                                 dev_ac.unique_ADC_name]}
                self.server_publisher.send_message(data)
