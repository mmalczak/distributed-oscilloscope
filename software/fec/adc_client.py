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
import selectors
import zmq
from zmq.utils.monitor import recv_monitor_message
from zmq.utils.monitor import parse_monitor_message
import pickle


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
    serv_expose.run()

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
        xmlrpc.client.ServerProxy("http://" + args.ip_server[0] +
                                  ":7999/").add_service(ADC_name, addr,
                                                        port, conf)

    cmd = Commands(zeroconf_service, zeroconf_info, ADC_name,
                   server_proxy)
    cmd_thread = CommandsThread(cmd)
    cmd_thread.start()

    EVENT_MAP = {}
    for name in dir(zmq):
        if name.startswith('EVENT_'):
            value = getattr(zmq, name)
            EVENT_MAP[value] = name

    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    monitor = socket.get_monitor_socket()
    #socket.bind("tcp://*:8003")
    ip = '128.141.162.185'
    port_zmq = str(port + 8)
    socket.bind("tcp://" + ip  + ":" + port_zmq)

    poller = zmq.Poller()
    poller.register(monitor, zmq.POLLIN | zmq.POLLERR)
    poller.register(socket, zmq.POLLIN | zmq.POLLERR)


    _ServerSelector = selectors.PollSelector
    try:
        with _ServerSelector() as selector:
            adc.selector = selector
            selector.register(serv_expose.server, selectors.EVENT_READ)

            while True:
                ready = selector.select(0.01)
                if ready:
                    if ready[0][0] == adc.adc_selector:
                        selector.unregister(adc)
                        adc.adc_selector = None
                        timestamp_and_data =\
                            adc.retrieve_ADC_timestamp_and_data(
                                adc.channels)
                        proxy = get_proxy(
                                    serv_expose.server_proxy.proxy_addr)
                        proxy.update_data(timestamp_and_data,
                                          adc.unique_ADC_name)
                    else:
                        serv_expose.server._handle_request_noblock()

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




                serv_expose.server.service_actions()
    finally:
        pass

    while(True):
        pass


if __name__ == '__main__':
    main()
