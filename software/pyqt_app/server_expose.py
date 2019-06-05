from PyQt5 import QtCore
from PyQt5 import QtGui
from proxy import *


class ServerExpose(QtCore.QObject):

    rem_av_ADC_signal = QtCore.pyqtSignal(['QString'])
    add_av_ADC_signal = QtCore.pyqtSignal(['QString', int])

    def __init__(self, GUI, port_GUI):
        super().__init__()
        self.port_GUI = port_GUI
        self.GUI = GUI
        self.app = None
        self.rem_av_ADC_signal.connect(self.GUI.remove_available_ADC)
        self.add_av_ADC_signal.connect(self.GUI.add_available_ADC)

    def show_widgets(self):
        for w in self.app.allWidgets():
            print(w)
        return True

    def remove_available_ADC(self, *args, **kwargs):
        self.rem_av_ADC_signal.emit(*args, **kwargs)

    def add_available_ADC(self, *args, **kwargs):
        self.add_av_ADC_signal.emit(*args, **kwargs)

    def monitorSlot(self):
        server = SimpleXMLRPCServer(("", self.port_GUI),
                                    allow_none=True)
        print("Listening on port " + str(self.port_GUI) + "...")
        server.register_function(self.add_available_ADC, "add_available_ADC")
        server.register_function(self.remove_available_ADC,
                                 "remove_available_ADC")
        server.register_function(self.show_widgets, "show_widgets")
        server.register_function(self.GUI.update_data, "update_data")
        server.register_function(self.GUI.set_horizontal_params,
                                 "set_horizontal_params")
        server.register_function(self.GUI.set_channel_params,
                                 "set_channel_params")
        server.register_function(self.GUI.set_trigger_params,
                                 "set_trigger_params")
        """server.register_function(self.set_acq_params, "set_acq_params")"""
        server.register_function(print, "print")

        server.serve_forever()


class ThreadServerExpose(QtGui.QWidget):

    def __init__(self, GUI, port_GUI):
        super().__init__()
        self.server_share = ServerExpose(GUI, port_GUI)
        self.thread = QtCore.QThread(self)
        self.server_share.moveToThread(self.thread)
        self.thread.started.connect(self.server_share.monitorSlot)
        self.thread.start()
