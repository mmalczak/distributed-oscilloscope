from parent_classes import *
from proxy import *


class SingleAcquisitionButton(QtGui.QPushButton):

    def __init__(self, server_proxy, GUI_name):
        super().__init__('Single')
        self.server_proxy = server_proxy
        self.GUI_name = GUI_name
        self.setCheckable(False)
        self.clicked.connect(self.action)

    def action(self):
        proxy = get_proxy(self.server_proxy.proxy_addr)
        proxy.single_acquisition(self.GUI_name)

class RunStopButton(QtGui.QPushButton):

    def __init__(self, server_proxy, GUI_name):
        super().__init__('Run/Stop')
        self.server_proxy = server_proxy
        self.GUI_name = GUI_name
        self.setCheckable(True)
        self.toggle()
        self.clicked.connect(self.action)

    def is_active(self):
        return (not self.isChecked())

    def action(self):
        proxy = get_proxy(self.server_proxy.proxy_addr)
        proxy.run_acquisition(self.is_active(), self.GUI_name)


        




