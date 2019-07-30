import sys
from connection_manager import ConnectionManager
from zeroconf_listener import ThreadZeroConf
from expose import Expose
import argparse
from DistScopeUtilities.addresses import server_expose_to_user_port
from DistScopeUtilities.addresses import server_expose_to_device_port
import logging.config
from logging_conf import DEFAULT_CONFIG


def main():
    logging.config.dictConfig(DEFAULT_CONFIG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--port_user', nargs=1,
                        help='port of the server exposed to the user')
    parser.add_argument('--port_device', nargs=1,
                        help='port of the server exposed to the device')

    args = parser.parse_args()

    port_user = None
    if args.port_user:
        port_user = args.port_user[0]
    else:
       port_user = server_expose_to_user_port

    port_device = None
    if args.port_device:
        port_device = args.port_device[0]
    else:
        port_device = server_expose_to_device_port

    connection_manager = ConnectionManager()
    thread_zero_conf = ThreadZeroConf()
    thread_zero_conf.start()
    expose = Expose(connection_manager, port_user, port_device)


if __name__ == '__main__':
    main()
