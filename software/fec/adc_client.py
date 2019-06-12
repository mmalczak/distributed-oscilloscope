import sys
sys.path.append('../general')
import numpy as np
import xmlrpc.client
import zeroconf
import os
import argparse
import threading
from ADC import *
from server_expose import *
from commands import *
def main():



    parser = argparse.ArgumentParser()
    parser.add_argument('--port', nargs=1,
                        help='port used on the current machine',
                        type=int, default=[8000])
    parser.add_argument('--pci_addr', nargs=1,
                        help='pci address of the desired board',
                        type=int, default=[0x01])
    parser.add_argument('--ip_server', nargs=1,
                        help='IP address of the server')

    args = parser.parse_args()
    port = int(args.port[0])
    pci_addr = int(args.pci_addr[0])

    number_of_channels = 4  # TODO
    addr = os.popen("ifconfig| grep inet").read().split()[1]
    ADC_idx = addr + '_' +  str(port)
    ADC_name = 'ADC' + '_' + ADC_idx + '._tcp.local.'

    server_proxy = Proxy()
    pci_addr = pci_addr
    trtl = 'trtl-000' + str(pci_addr)
    adc = ADC_100m14b4cha_extended_API_WRTD(pci_addr, trtl,
                                            server_proxy, ADC_name)
    conf = adc.get_current_conf()
    serv_expose = ServerExpose(addr, port, server_proxy, adc)

    zeroconf_service = None
    zeroconf_info = None
    if(args.ip_server is None):
        zeroconf_info = zeroconf.ServiceInfo("_http._tcp.local.",
                            ADC_name, zeroconf.socket.inet_aton(addr),
                            8000, properties={'addr': addr,
                            'port': str(port), 'conf': conf})
        zeroconf_service = zeroconf.Zeroconf()
        zeroconf_service.register_service(zeroconf_info)
        """TODO check if it is working, if it will not block until the
        registration is finished(during registration the server will
        try to set it's own addres in the ADC"""
    else:
        serv_expose.set_server_address(args.ip_server[0])
        xmlrpc.client.ServerProxy("http://" + args.ip_server[0] + ":7999/").\
                                  add_service(ADC_name, addr, port, conf)

    try:
        print("Application starting")
        serv_expose.run()
    finally:
        if(zeroconf_service is not None):
            zeroconf_service.unregister_service(zeroconf_info)
        else:
            proxy = get_proxy(server_proxy.proxy_addr)
            proxy.remove_service(ADC_name)
        os._exit(1)

if __name__ == '__main__':
    main()
