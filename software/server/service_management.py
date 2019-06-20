from zeroconf import ServiceBrowser, Zeroconf
import threading
import os
import socket


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
            conf = None
            if b'conf' in info.properties:
                conf = info.properties[b'conf']
            try:
                addr = socket.inet_ntoa(info.address)
                port = str(int(info.properties[b'port']))
                osc.register_ADC(name, conf['board_conf']['n_chan'], str(addr), port)
                if not server_addr_known:
                    server_addr = os.popen("ifconfig| grep inet").read().split()[1]
                    ADC = self.osc.get_ADC(unique_ADC_name)
                    zmq_rpc = ADC.zmq_rpc
                    zmq_rpc.send_RPC('set_server_address', server_addr)
                    """This part is not tested"""
            except Exception as e:
                pass
