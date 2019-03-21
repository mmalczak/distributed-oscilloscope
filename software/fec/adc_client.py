import numpy as np
import xmlrpc.client
import zeroconf
import os
import random 
import argparse
import threading
from ADC import *
#from map_timer_trig import *
from server_expose import *
from commands import *



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', nargs =1, help='port used on the current machine')
    parser.add_argument('--ip_server', nargs =1, help='IP address of the server')
    args = parser.parse_args()
    if(args.port == None):
        port = 8000
        pci_addr = 0x01
    else:
        port = int(args.port[0])
        pci_addr = 0x02


    number_of_channels = 4 #TODO
    addr = os.popen("ifconfig| grep inet").read().split()[1]
    ADC_idx = str(random.random())
    ADC_name = "ADC" + ADC_idx + "._http._tcp.local."



    server_proxy = Proxy()
    pci_addr = pci_addr
    trtl = 'trtl-000' + str(pci_addr)
    adc = ADC(pci_addr, trtl, server_proxy, ADC_name)
 
    serv_expose = ServerExpose(addr, port, server_proxy, adc)
    serv_expose.start()


    zeroconf_service = None
    zeroconf_info = None
    if(args.ip_server == None):
        zeroconf_info = zeroconf.ServiceInfo("_http._tcp.local.", ADC_name, zeroconf.socket.inet_aton(addr), 8000, properties={'addr': addr, 'port':str(port)})
        zeroconf_service = zeroconf.Zeroconf()
        zeroconf_service.register_service(zeroconf_info)
    else: 
        xmlrpc.client.ServerProxy("http://" + args.ip_server[0] + ":7999/").add_service(ADC_name, addr, port)
    
    cmd = Commands(zeroconf_service, zeroconf_info, ADC_name, server_proxy)
    cmd_thread = CommandsThread(cmd)
    cmd_thread.start()
    while(True):
        pass

if __name__ == '__main__':
     main()


