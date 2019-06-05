import sys
sys.path.append('../general')
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from mainwindow import Ui_MainWindow
import os
import argparse
from PyQt5 import QtGui
from server_expose import *
from GUI import *
from zmq_rpc import ZMQ_RPC
from addresses import server_zmq_expose_port

"""TODO number of ADCs different from data dimension occuring when I
switch off ADC"""


class MainWindow(QMainWindow):
    def __init__(self, zmq_rpc):
        super(MainWindow, self).__init__()
        self.threading_widget = None
        self.zmq_rpc = zmq_rpc
        self.ui = Ui_MainWindow()
        self.GUI_name = None
        self.ui.setupUi(self)
        self.show()

    def closeEvent(self, *args, **kwargs):
        super(QtGui.QMainWindow, self).closeEvent(*args, **kwargs)
        self.zmq_rpc.send_RPC("remove_service", self.GUI_name)
        self.threading_widget.thread.exit()  # TODO not really working


def main():
    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'w')

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', nargs=1,
                        help='port used on the current machine')
    parser.add_argument('--ip_server', nargs=1,
                        help='IP address of the server')
    args = parser.parse_args()

    if(args.port is None):
        port = 8001
    else:
        port = int(args.port[0])

    ip_server = args.ip_server[0]

    addr = os.popen("ifconfig| grep inet").read().split()[1]
    GUI_idx = addr + "_" + str(port)
    GUI_name = "GUI" + "_" + GUI_idx + "._http._tcp.local."
    zmq_rpc = ZMQ_RPC(ip_server, server_zmq_expose_port)
    app = QApplication([])
    win = MainWindow(zmq_rpc)
    GUI = GUI_Class(win.ui, zmq_rpc, GUI_name)
    threading_widget = ThreadServerExpose(GUI, port)
    threading_widget.server_share.app = app
    """So that I can list all widgets"""
    win.threading_widget = threading_widget
    """I want the thread to be destroyed when I close the window"""
    threading_widget.setParent(win)
    """remove widgets after close"""


    zmq_rpc.send_RPC('add_service', GUI_name, addr, port)

    win.GUI_name = GUI_name
    app.exec()


if __name__ == '__main__':
    main()
