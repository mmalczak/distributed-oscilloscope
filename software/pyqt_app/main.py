import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from mainwindow import Ui_MainWindow
import os
import argparse
from PyQt5 import QtGui
from server_expose import *
from GUI import *
sys.path.append('../')
from general.zmq_rpc import ZMQ_RPC
from general.addresses import server_expose_to_user_port
from general.ipaddr import get_ip

"""TODO number of ADCs different from data dimension occuring when I
switch off ADC"""


class MainWindow(QMainWindow):
    def __init__(self, zmq_rpc):
        super(MainWindow, self).__init__()
        self.zmq_rpc = zmq_rpc
        self.ui = Ui_MainWindow()
        self.GUI_name = None
        self.ui.setupUi(self)
        self.show()

    def closeEvent(self, *args, **kwargs):
        super(QtGui.QMainWindow, self).closeEvent(*args, **kwargs)
        self.zmq_rpc.send_RPC("unregister_GUI", self.GUI_name)


def main():
    import logging.config
    from logging_conf import DEFAULT_CONFIG
    logging.config.dictConfig(DEFAULT_CONFIG)

    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'w')

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', nargs=1,
                        help='port used on the current machine')
    parser.add_argument('--port_server', nargs=1,
                        help='port used on the server')
    parser.add_argument('--ip_server', nargs=1,
                        help='IP address of the server')
    args = parser.parse_args()

    if(args.port is None):
        port = 8001
    else:
        port = int(args.port[0])

    server_port = None
    if args.port_server:
        server_port = args.port_server[0]
    else:
        server_port = server_expose_to_user_port

    ip_server = args.ip_server[0]

    addr = get_ip()
    GUI_idx = addr + "_" + str(port)
    GUI_name = "GUI" + "_" + GUI_idx + "._http._tcp.local."
    print(server_port)
    zmq_rpc = ZMQ_RPC(ip_server, server_port)
    app = QApplication([])
    win = MainWindow(zmq_rpc)
    GUI = GUI_Class(win.ui, zmq_rpc, GUI_name)
    threading_widget_zmq = ThreadServerExposeZMQ(GUI, port)


    zmq_rpc.send_RPC('register_GUI', GUI_name, addr, port)

    win.GUI_name = GUI_name
    app.exec()


if __name__ == '__main__':
    main()
