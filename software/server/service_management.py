from zeroconf import ServiceBrowser, Zeroconf
import threading
import os
import socket
import logging
logger = logging.getLogger(__name__)


class ThreadZeroConf(threading.Thread):

    def __init__(self, osc):
        threading.Thread.__init__(self)
        self.osc = osc

    def run(self):
        zeroconf = Zeroconf()
        listener = ZeroconfListener(self.osc)
        browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)


class ZeroconfListener:

    def __init__(self, osc):
        self.osc = osc

    def remove_service(self, zeroconf, type, name):
        if name.startswith("ADC"):
            self.osc.unregister_ADC(name)

    def add_service(self, zeroconf, type, name):
        if name.startswith("ADC"):
            info = zeroconf.get_service_info(type, name)
            n_chan = int(info.properties[b'n_chan'])
            addr = socket.inet_ntoa(info.address)
            port = int(info.properties[b'port'])
            self.osc.register_ADC(name, n_chan, str(addr), port)
            server_addr = os.popen("ifconfig| grep inet").read().split()[1]
            ADC = self.osc.get_ADC(name)
            ADC.zmq_rpc.set_server_address(server_addr)
