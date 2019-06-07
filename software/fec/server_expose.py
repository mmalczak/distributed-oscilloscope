import threading
from xmlrpc.server import SimpleXMLRPCServer
import sys
import selectors
import os
from ADC import *
import selectors
import zmq
from zmq.utils.monitor import recv_monitor_message
from zmq.utils.monitor import parse_monitor_message
import pickle


thismodule = sys.modules[__name__]


class ServerExpose():
    adc = None

    def __init__(self, addr, port, server_proxy, adc):
        self.addr = addr
        self.port = port
        self.server_proxy = server_proxy
        self.adc = adc
        self.server = None

    def __getattr__(self, function_name):
        """ If he requered function is not defined here, look for it in the
        adc object"""
        return getattr(self.adc, function_name)

    def set_server_address(self, addr):
        self.server_proxy.proxy_addr = "http://" + addr + ":7999/"

    def set_adc_parameter(self, function_name, value, idx=-1):
        if(idx == -1):
            self.adc.configure_parameter(function_name, [value])
        else:
            self.adc.configure_parameter(function_name, [idx, value])

    def exit(self):
        """This fucntion is just for testing and will be removed after 
        addding ZeroMQ"""
        """doesn'r work with zeroconf"""
        proxy = get_proxy(self.server_proxy.proxy_addr)
        proxy.remove_service(self.adc.unique_ADC_name)
        os._exit(1)

    def run(self):
        self.server = SimpleXMLRPCServer((self.addr, self.port),
                                         allow_none=True)
        self.server.register_function(self.set_adc_parameter,
                                      "set_adc_parameter")
        self.server.register_function(self.set_server_address,
                                      "set_server_address")
        self.server.register_function(self.adc.get_current_conf,
                                      "get_current_conf")
        self.server.register_function(self.adc.
                configure_acquisition_retrieve_and_send_data,
                "configure_acquisition_async")
        self.server.register_function(self.adc.set_WRTD_master,
                                      "set_WRTD_master")
        self.server.register_function(self.adc.stop_acquisition,
                                      "stop_acquisition")
        self.server.register_function(self.exit, "exit")


        """self.server.serve_forever()"""

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



        _ServerSelector = selectors.PollSelector
        try:
            with _ServerSelector() as selector:
                self.adc.selector = poller
                selector.register(self.server, selectors.EVENT_READ)

                while True:
                    ready = selector.select(0.01)
                    if ready:
                        self.server._handle_request_noblock()

                    socks = dict(poller.poll(10))
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
                        proxy = get_proxy(self.server_proxy.proxy_addr)
                        proxy.update_data(timestamp_and_data, self.adc.unique_ADC_name)

                    self.server.service_actions()
        finally:
            pass

        while(True):
            pass



