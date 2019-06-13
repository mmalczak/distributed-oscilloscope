from PyQt5 import QtGui


class SingleAcquisitionButton(QtGui.QPushButton):

    def __init__(self, zmq_rpc, GUI_name):
        super().__init__('Single')
        self.zmq_rpc = zmq_rpc
        self.GUI_name = GUI_name
        self.setCheckable(False)
        self.clicked.connect(self.action)

    def action(self):
        rpc = self.zmq_rpc
        rpc.send_RPC('single_acquisition', self.GUI_name)


class RunStopButton(QtGui.QPushButton):

    def __init__(self, zmq_rpc, GUI_name):
        super().__init__('Run/Stop')
        self.zmq_rpc = zmq_rpc
        self.GUI_name = GUI_name
        self.setCheckable(True)
        self.toggle()
        self.clicked.connect(self.action)

    def is_active(self):
        return (not self.isChecked())

    def action(self):
        rpc = self.zmq_rpc
        rpc.send_RPC('run_acquisition', self.is_active(), self.GUI_name)
