from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from mainwindow import Ui_MainWindow
import os
import zeroconf
import argparse
import random
from PyQt5 import QtGui
from server_expose import *
from proxy import *
from GUI import *

#TODO number of ADCs different from data dimension occuring when I switch off ADC
# fixme put empty lines to divide methods

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.threading_widget = None
        self.ui = Ui_MainWindow()
        self.zeroconf_service = None
        self.zeroconf_info = None
        self.GUI_name = None
        self.ui.setupUi(self)
        self.show()
#        self.ui.graphicsView.addItem(pg.PlotItem())
        self.server_proxy = None

    def closeEvent(self, *args, **kwargs):
        super(QtGui.QMainWindow, self).closeEvent(*args, **kwargs)
        if(self.zeroconf_service != None):
            self.zeroconf_service.unregister_service(self.zeroconf_info)
        else:
            proxy = get_proxy(self.server_proxy.proxy_addr)
            proxy.remove_service(self.GUI_name)
        self.threading_widget.thread.exit() # TODO not really working


def main():
    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'w')

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', nargs =1, help='port used on the current machine')
    parser.add_argument('--ip_server', nargs =1, help='IP address of the server')
    args = parser.parse_args()

    if(args.port == None):
        port = 8001
    else:
        port = int(args.port[0])

    addr = os.popen("ifconfig| grep inet").read().split()[1]
    GUI_idx = str(random.random())
    GUI_name = "GUI" + GUI_idx + "._http._tcp.local."
    app = QApplication([])
    win = MainWindow()
    GUI = GUI_Class(win.ui, GUI_name)
    win.server_proxy = GUI.server_proxy
    threading_widget = ThreadServerExpose(GUI, port)
    threading_widget.server_share.app = app  # So that I can list all widgets
    win.threading_widget = threading_widget # I want the thread to be destroyed when I close the window
    threading_widget.setParent(win) # remove widgets after close

    zeroconf_service = None
    zeroconf_info = None

    if(args.ip_server == None):
        zeroconf_info = zeroconf.ServiceInfo("_http._tcp.local.", GUI_name, zeroconf.socket.inet_aton(addr), 8000, properties={'addr': addr, 'port':str(port)})
        zeroconf_service = zeroconf.Zeroconf()
        zeroconf_service.register_service(zeroconf_info)

    else:
        xmlrpc.client.ServerProxy("http://" + args.ip_server[0] + ":8000/").add_service(GUI_name, addr, port)

    win.zeroconf_info = zeroconf_info
    win.zeroconf_service = zeroconf_service
    win.GUI_name = GUI_name
    app.exec()

if __name__ == '__main__':
     main()

