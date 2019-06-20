import sys
from oscilloscope import Oscilloscope
from zeroconf_listener import ThreadZeroConf
from expose import Expose
import logging.config
from logging_conf import DEFAULT_CONFIG


def main():
    logging.config.dictConfig(DEFAULT_CONFIG)

    osc = Oscilloscope()
    thread_zero_conf = ThreadZeroConf()
    thread_zero_conf.start()
    expose = Expose(osc)


if __name__ == '__main__':
    main()
