import sys
sys.path.append('../general')
from oscilloscope import *
from service_management import *
from expose import *

def main():
    import logging.config
    from logging_conf import DEFAULT_CONFIG
    logging.config.dictConfig(DEFAULT_CONFIG)

    osc = Oscilloscope()
    thread_GUI_zmq_expose = ThreadGUI_zmq_Expose(osc)
    thread_GUI_zmq_expose.start()
    thread_zero_conf = ThreadZeroConf(osc)
    thread_zero_conf.start()


if __name__ == '__main__':
    main()
