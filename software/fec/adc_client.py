import sys
sys.path.append('../')
import zeroconf
import os
import argparse
from server_expose import ServerExpose
import time
from general.ipaddr import get_ip

from general import rpc_pb2
from general import rpc_pb2_grpc

import grpc


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

    addr = get_ip()
    ADC_idx = addr + '_' + str(port)
    unique_ADC_name = 'ADC' + '_' + ADC_idx + '._http._tcp.local.'

    pci_addr = pci_addr
    trtl = 'trtl-000' + str(pci_addr)
    if args.ip_server:
        ip_server = {'addr': args.ip_server[0]}
    else:
        ip_server = {'addr': None}

    serv_expose = ServerExpose(port, pci_addr, trtl, unique_ADC_name)



    zeroconf_service = None
    zeroconf_info = None
    if(args.ip_server is None):
        zeroconf_info = zeroconf.ServiceInfo("_http._tcp.local.",
                            unique_ADC_name, zeroconf.socket.inet_aton(addr),
                            8000, properties={'addr': addr, 'port': str(port)})
        zeroconf_service = zeroconf.Zeroconf()
        zeroconf_service.register_service(zeroconf_info)
    else:
        with grpc.insecure_channel('128.141.79.50:50051') as channel:
            stub = rpc_pb2_grpc.RPC_reqStub(channel)
            response = stub.register_ADC(rpc_pb2.Args(
                                            unique_ADC_name=unique_ADC_name))
        print("Greeter client received: " + response.value)

        serv_expose.set_server_address(ip_server['addr'])
        data = {'function_name': 'register_ADC',
                                 'args': [unique_ADC_name, addr, port]}
        serv_expose.server_publisher.send_message(data)
        



    try:
        print("Application starting")
        serv_expose.run()
    except KeyboardInterrupt:
        if(zeroconf_service is not None):
            zeroconf_service.unregister_service(zeroconf_info)
        else:
            data = {'function_name': 'unregister_ADC',
                    'args': [unique_ADC_name]}
            serv_expose.server_publisher.send_message(data)
            time.sleep(0.1)  # otherwise the message is lost

        os._exit(1)


if __name__ == '__main__':
    main()
