import threading
from xmlrpc.server import SimpleXMLRPCServer
import sys
import os
from ADC import *
import zmq
from zmq.utils.monitor import recv_monitor_message
from zmq.utils.monitor import parse_monitor_message
import pickle
import time

thismodule = sys.modules[__name__]


class ServerExpose():
    adc = None

    def __init__(self, addr, port, adc, ip_server):
        self.addr = addr
        self.port = port
        self.server_publisher = None
        self.adc = adc
        self.server = None
        self.ip_server = ip_server

    def __getattr__(self, function_name):
        """ If he requered function is not defined here, look for it in the
        adc object"""
        return getattr(self.adc, function_name)

    def set_server_address(self, addr):
        self.ip_server['addr'] = addr

    def set_adc_parameter(self, function_name, value, idx=-1):
        if(idx == -1):
            self.adc.configure_parameter(function_name, [value])
        else:
            self.adc.configure_parameter(function_name, [idx, value])

    def exit(self):
        """This fucntion is just for testing and will be removed after 
        addding ZeroMQ"""
        """doesn'r work with zeroconf"""
        data = {'function_name': 'remove_service',
                                 'args': [self.adc.unique_ADC_name]}
        self.server_publisher.send_message(data)
        time.sleep(0.1)  # otherwise the message is lost
        os._exit(1)

    def run(self):

        context = zmq.Context()
        socket = context.socket(zmq.ROUTER)
        monitor = socket.get_monitor_socket()
        #socket.bind("tcp://*:8003")
        ip = '128.141.162.185'
        port_zmq = str(self.port + 8)
        socket.bind("tcp://" + ip  + ":" + port_zmq)

        poller = zmq.Poller()
        poller.register(monitor, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket, zmq.POLLIN | zmq.POLLERR)
        
        EVENT_MAP = {}
        for name in dir(zmq):
            if name.startswith('EVENT_'):
                value = getattr(zmq, name)
                EVENT_MAP[value] = name

        self.adc.selector = poller
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
                #logger.info("Event: {}".format(evt))

            if self.adc.fileno() in socks:
                poller.unregister(self.adc)
                timestamp_and_data = self.adc.retrieve_ADC_timestamp_and_data(
                                                            self.adc.channels)
                data = {'function_name': 'update_data',
                        'args': [timestamp_and_data, self.adc.unique_ADC_name]}
                self.server_publisher.send_message(data)
