import sys
import os
import zmq
from zmq.utils.monitor import recv_monitor_message
from zmq.utils.monitor import parse_monitor_message
import pickle
import time
sys.path.append('../')
from general.publisher import Publisher
from general.addresses import server_expose_to_device_port
from general.ipaddr import get_ip

thismodule = sys.modules[__name__]


class ServerExpose():
    devices_access = None

    def __init__(self, port, devices_access):
        self.port = port
        self.server_publisher = None
        self.devices_access = devices_access
        self.server = None

    def __getattr__(self, function_name):
        """ If he requered function is not defined here, look for it in the
        devices_access object"""
        return getattr(self.devices_access, function_name)

    def set_server_address(self, addr):
        self.server_publisher = Publisher(addr, server_expose_to_device_port)

    def set_adc_parameter(self, function_name, *args):
        self.devices_access.configure_adc_parameter(function_name, [*args])

    def exit(self):
        """This fucntion is just for testing and will be removed after
        addding ZeroMQ"""
        """doesn'r work with zeroconf"""
        data = {'function_name': 'unregister_ADC',
                                 'args': [self.devices_access.unique_ADC_name]}
        self.server_publisher.send_message(data)
        time.sleep(0.1)  # otherwise the message is lost
        os._exit(1)

    def run(self):

        context = zmq.Context()
        socket = context.socket(zmq.ROUTER)
        monitor = socket.get_monitor_socket()
        ip = get_ip()
        port_zmq = str(self.port)
        socket.bind("tcp://" + ip + ":" + port_zmq)

        poller = zmq.Poller()
        poller.register(monitor, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket, zmq.POLLIN | zmq.POLLERR)

        EVENT_MAP = {}
        for name in dir(zmq):
            if name.startswith('EVENT_'):
                value = getattr(zmq, name)
                EVENT_MAP[value] = name

        self.devices_access.selector = poller
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

            if self.devices_access.fileno() in socks:
                dev_ac = self.devices_access
                poller.unregister(dev_ac)
                [timestamp, pre_post, data] = dev_ac.retrieve_ADC_data(
                                                            dev_ac.channels)
                data = {'function_name': 'update_data',
                        'args': [timestamp, pre_post, data,
                                 dev_ac.unique_ADC_name]}
                self.server_publisher.send_message(data)
