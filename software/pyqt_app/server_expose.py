from PyQt5 import QtCore
from PyQt5 import QtGui
import zmq
import sys
sys.path.append('../')
from general.ipaddr import get_ip

class ServerExposeZMQ(QtCore.QObject):

    signal = QtCore.pyqtSignal(['QByteArray'])

    def __init__(self, GUI, port_GUI):
        super().__init__()
        self.GUI = GUI
        self.port_GUI = port_GUI
        self.signal.connect(self.GUI.socket_communication)

    def monitorSlot(self):
        context = zmq.Context()
        socket = context.socket(zmq.ROUTER)
        ip = get_ip()
        socket.bind("tcp://" + ip  + ":" + str(self.port_GUI))

        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN | zmq.POLLERR)

        while True:
            socks = dict(poller.poll())
            if socket in socks:
                [identity, message] = socket.recv_multipart()
                self.signal.emit(message)


class ThreadServerExposeZMQ(QtGui.QWidget):

    def __init__(self, GUI, port_GUI):
        super().__init__()
        self.server_share = ServerExposeZMQ(GUI, port_GUI)
        self.thread = QtCore.QThread(self)
        self.server_share.moveToThread(self.thread)
        self.thread.started.connect(self.server_share.monitorSlot)
        self.thread.start()
