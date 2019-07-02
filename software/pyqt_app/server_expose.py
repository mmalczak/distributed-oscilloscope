from PyQt5 import QtCore
from PyQt5 import QtGui
import zmq
import sys
sys.path.append('../')
from general.ipaddr import get_ip
from general.tcp_server import TCPServer


class ServerExposeZMQ(QtCore.QObject):

    signal = QtCore.pyqtSignal(['QByteArray'])

    def __init__(self, GUI, port_GUI):
        super().__init__()
        self.GUI = GUI
        self.port_GUI = port_GUI
        self.signal.connect(self.GUI.socket_communication)

    def monitorSlot(self):
        context = zmq.Context()
        ip = get_ip()

        poller = zmq.Poller()

        tcp_server = TCPServer(ip, self.port_GUI, poller)
        poller.register(tcp_server.socket)

        while True:
            socks = dict(poller.poll())

            if tcp_server.socket.fileno() in socks:
                tcp_server.register_connection()
            for sock, event in socks.items():
                if sock in tcp_server.fd_conn:
                    message = tcp_server.receive_packet(sock)
                    if message:
                        self.signal.emit(message)


class ThreadServerExposeZMQ(QtGui.QWidget):

    def __init__(self, GUI, port_GUI):
        super().__init__()
        self.server_share = ServerExposeZMQ(GUI, port_GUI)
        self.thread = QtCore.QThread(self)
        self.server_share.moveToThread(self.thread)
        self.thread.started.connect(self.server_share.monitorSlot)
        self.thread.start()
