from zeroconf import ServiceBrowser, Zeroconf
import threading
from proxy import *
import os
import socket


class ThreadZeroConf(threading.Thread):

    def __init__(self, osc):
        threading.Thread.__init__(self)
        self.osc = osc

    def run(self):
        zeroconf = Zeroconf()
        listener = ZeroconfListener(self.osc)
        browser = ServiceBrowser(zeroconf, "_http._tcp.local.",
                                 listener)


class ZeroconfListener:

    def __init__(self, osc):
        self.osc = osc

    def remove_service(self, zeroconf, type, name):
        remove_service(name, self.osc)

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        conf = None
        if b'conf' in info.properties:
            conf = info.properties[b'conf']
        try:
            add_service(name, socket.inet_ntoa(info.address),
                        str(int(info.properties[b'port'])), self.osc,
                        conf)
        except Exception as e:
            pass


def remove_service(name, osc):
    """adding and removing service could be done either by zeroconf,
    or directly by the client using RPC call"""

    if name.startswith("GUI"):
        print("Service %s removed" % (name,))
        osc.unregister_GUI(name)

    if name.startswith("ADC"):
        print("Service %s removed" % (name,))
        osc.remove_available_ADC(name)


def add_service(name, addr, port, osc, conf=None,
                server_addr_known=False):

    if name.startswith("ADC"):
        ADC_proxy_addr = "http://" + str(addr) + ":" + str(port) + "/"
        """name provided by zeroconf ihas to be unique and is not user
        friendly, thats why user selected name is passed in properties"""
        osc.add_available_ADC(name, conf['board_conf']['n_chan'],
                              ADC_proxy_addr, conf)
        """server_address should be set at the end, (ADC checks if
        server_address was set and assumes that if it was set, server
        is properly configured)"""
        if not server_addr_known:
            server_addr =\
                 os.popen("ifconfig| grep inet").read().split()[1]
            get_proxy(ADC_proxy_addr).set_server_address(server_addr)
        print("Service %s added" % (name))

    if name.startswith("GUI"):
        GUI_proxy_addr = "http://" + str(addr) + ":" + str(port) + "/"
        server_addr = os.popen("ifconfig| grep inet").read().split()[1]
        get_proxy(GUI_proxy_addr).set_server_address(server_addr)
        osc.register_GUI(name, GUI_proxy_addr)
        print("Service %s added" % (name))
