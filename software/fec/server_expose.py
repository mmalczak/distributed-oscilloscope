import threading
from xmlrpc.server import SimpleXMLRPCServer
import sys
import selectors

from ADC import *


thismodule = sys.modules[__name__]

class ServerExpose(threading.Thread):
    adc = None
    def __init__(self, addr, port, server_proxy, adc):
        threading.Thread.__init__(self)
        self.addr = addr
        self.port = port
        self.server_proxy = server_proxy
        self.adc = adc
    def set_server_address(self, addr):
        self.server_proxy.proxy_addr = "http://" + addr + ":7999/"

    def set_channel_range(self, channel_range, channel_idx):
        self.adc.configure_parameter(set_channel_range, [channel_idx, channel_range])

 
    def set_adc_parameter(self, function_name, value, idx=-1):
        if(idx == -1):
            self.adc.configure_parameter(getattr(thismodule, function_name), [value]) 
        else:
            self.adc.configure_parameter(getattr(thismodule, function_name), [idx, value]) 


    def run(self):
        self.server = SimpleXMLRPCServer((self.addr, self.port), allow_none=True)
        self.server.register_function(self.set_adc_parameter, "set_adc_parameter")
        self.server.register_function(self.set_server_address, "set_server_address")
        self.server.register_function(self.set_channel_range, "set_channel_range")
        self.server.register_function(self.adc.get_current_conf, "get_current_conf")
        self.server.register_function(self.adc.configure_acquisition_retrieve_and_send_data, "configure_acquisition_async")
        self.server.register_function(self.adc.set_WRTD_master, "set_WRTD_master")
        self.server.register_function(self.adc.stop_acquisition, "stop_acquisition")

        #self.server.serve_forever()
        _ServerSelector = selectors.PollSelector
        try:
            with _ServerSelector() as selector:
                self.adc.selector = selector
                selector.register(self.server, selectors.EVENT_READ)
               # self.adc_selector = selector.register(self.adc, selectors.EVENT_READ)
                while True: 
                    ready = selector.select(0.5)
                    # bpo-35017: shutdown() called during select(), exit immediately.
                    if ready:
                        if ready[0][0] == self.adc.adc_selector:
                            print("Dupa")
                            selector.unregister(self.adc)
                            self.adc.adc_selector = None
                            timestamp_and_data = self.adc.retrieve_ADC_timestamp_and_data(self.adc.channels)
                            proxy = get_proxy(self.server_proxy.proxy_addr)
                            proxy.update_data(timestamp_and_data, self.adc.unique_ADC_name) 
                        else:
                            self.server._handle_request_noblock()

                    self.server.service_actions()
        finally:
            pass
