from parent_classes import *
import sys
sys.path.append('../')
from general.zmq_rpc import *
from PyQt5.QtWidgets import QHBoxLayout


class Presamples(Box):
    def __init__(self, zmq_rpc, GUI_name, GUI):
        super().__init__(0, "No_ADC", "Presamples")
        self.box.setMinimum(0)
        self.box.setMaximum(1000000)
        """TODO check how many pre and postsamples maximum"""
        self.zmq_rpc = zmq_rpc
        self.GUI_name = GUI_name
        self.GUI = GUI

    def value_change(self):
        presamples = self.box.value()
        self.zmq_rpc.send_RPC('set_presamples', presamples, self.GUI_name)
        self.GUI.update_GUI_params()

class Postsamples(Box):
    def __init__(self, zmq_rpc, GUI_name, GUI):
        super().__init__(0, "No_ADC", "Postsamples")
        self.box.setMinimum(0)
        self.box.setMaximum(1000000)
        """TODO check how many pre and postsamples maximum"""
        self.zmq_rpc = zmq_rpc
        self.GUI_name = GUI_name
        self.GUI = GUI

    def value_change(self):
        postsamples = self.box.value()
        self.zmq_rpc.send_RPC('set_postsamples', postsamples, self.GUI_name)
        self.GUI.update_GUI_params()

class AcquisitionSettings(QHBoxLayout):
    def __init__(self, zmq_rpc, GUI_name, GUI):
        super().__init__()
        self.zmq_rpc = zmq_rpc
        self.GUI_name = GUI_name
        self.presamples = Presamples(zmq_rpc, GUI_name, GUI)
        self.postsamples = Postsamples(zmq_rpc, GUI_name, GUI)
        self.addWidget(self.presamples)
        self.addWidget(self.postsamples)

    def set_params(self, presamples, postsamples):
        self.presamples.set_value(presamples)
        self.postsamples.set_value(postsamples)
