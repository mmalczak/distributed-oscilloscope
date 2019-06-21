import sys
from connection_manager import ConnectionManager
from zeroconf_listener import ThreadZeroConf
from expose import Expose
import logging.config
from logging_conf import DEFAULT_CONFIG


def main():
    logging.config.dictConfig(DEFAULT_CONFIG)

    connection_manager = ConnectionManager()
    thread_zero_conf = ThreadZeroConf()
    thread_zero_conf.start()
    expose = Expose(connection_manager)


if __name__ == '__main__':
    main()
