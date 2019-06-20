import sys
sys.path.append('../general')
import zeroconf
import os
import argparse
from devices_access import DevicesAccess
from server_expose import ServerExpose
from publisher import Publisher
import time


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
    ADC_idx = addr + '_' + str(port)
    unique_ADC_name = 'ADC' + '_' + ADC_idx + '._http._tcp.local.'

    pci_addr = pci_addr
    trtl = 'trtl-000' + str(pci_addr)
    devices_access = DevicesAccess(pci_addr, trtl, unique_ADC_name)
    conf = devices_access.get_current_adc_conf()
    if args.ip_server:
        ip_server = {'addr': args.ip_server[0]}
    else:
        ip_server = {'addr': None}

    serv_expose = ServerExpose(addr, port, devices_access, ip_server)

    zeroconf_service = None
    zeroconf_info = None
    server_publisher = None
    if(args.ip_server is None):
        zeroconf_info = zeroconf.ServiceInfo("_http._tcp.local.",
                            unique_ADC_name, zeroconf.socket.inet_aton(addr),
                            8000, properties={'addr': addr,
                            'port': str(port), 'conf': conf})
        zeroconf_service = zeroconf.Zeroconf()
        zeroconf_service.register_service(zeroconf_info)
        while ip_server['addr'] is None:
            pass
        """TODO check if it is working, if it will not block until the
        registration is finished(during registration the server will
        try to set it's own addres in the ADC"""
        server_publisher = Publisher(ip_server['addr'], 8023)
    else:
        serv_expose.set_server_address(ip_server['addr'])
        server_publisher = Publisher(ip_server['addr'], 8023)
        data = {'function_name': 'register_ADC',
                                 'args': [unique_ADC_name, addr, port, conf]}
        server_publisher.send_message(data)

    serv_expose.server_publisher = server_publisher

    try:
        print("Application starting")
        serv_expose.run()
    except KeyboardInterrupt:
        if(zeroconf_service is not None):
            zeroconf_service.unregister_service(zeroconf_info)
        else:
            data = {'function_name': 'unregister_ADC',
                    'args': [unique_ADC_name]}
            server_publisher.send_message(data)
            time.sleep(0.1)  # otherwise the message is lost

        os._exit(1)


if __name__ == '__main__':
    main()
