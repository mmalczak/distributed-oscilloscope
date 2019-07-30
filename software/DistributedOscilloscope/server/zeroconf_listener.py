from zeroconf import ServiceBrowser, Zeroconf
import threading
import os
import socket
import logging
from DistributedOscilloscope.utilities.ipaddr import get_ip
from DistributedOscilloscope.utilities.publisher import PublisherIPC
logger = logging.getLogger(__name__)


class ThreadZeroConf(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        zeroconf = Zeroconf()
        listener = ZeroconfListener()
        browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)


class ZeroconfListener:

    def __init__(self):
        self.publisher = PublisherIPC('zeroconf')

    def remove_service(self, zeroconf, type, name):
        if name.startswith("ADC"):
            data = {'function_name': 'unregister_ADC',
                    'args': [name]}
            self.publisher.send_message(data)

    def add_service(self, zeroconf, type, name):
        if name.startswith("ADC"):
            info = zeroconf.get_service_info(type, name)
            addr = str(socket.inet_ntoa(info.address))
            port = int(info.properties[b'port'])
            data = {'function_name': 'register_ADC',
                    'args': [name, addr, port]}
            self.publisher.send_message(data)
            server_addr = get_ip()
            data = {'function_name': 'set_server_address',
                    'args': [name, server_addr]}
            self.publisher.send_message(data)
