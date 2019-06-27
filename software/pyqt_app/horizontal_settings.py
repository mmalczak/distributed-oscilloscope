from parent_classes import *
import sys
sys.path.append('../')
from general.zmq_rpc import *
from PyQt5.QtWidgets import QHBoxLayout


class Presamples(Box):
    def __init__(self, zmq_rpc, GUI_name, GUI, acq_set):
        super().__init__(0, "No_ADC", "Presamples")
        self.box.setMinimum(0)
        self.box.setMaximum(1000000)
        """TODO check how many pre and postsamples maximum"""
        self.zmq_rpc = zmq_rpc
        self.GUI_name = GUI_name
        self.GUI = GUI
        self.acq_set = acq_set

    def value_change(self):
        presamples = self.box.value()
        self.acq_set.set_pre_post_samples(presamples=presamples)

class Postsamples(Box):
    def __init__(self, zmq_rpc, GUI_name, GUI, acq_set):
        super().__init__(0, "No_ADC", "Postsamples")
        self.box.setMinimum(0)
        self.box.setMaximum(1000000)
        """TODO check how many pre and postsamples maximum"""
        self.zmq_rpc = zmq_rpc
        self.GUI_name = GUI_name
        self.GUI = GUI
        self.acq_set = acq_set

    def value_change(self):
        postsamples = self.box.value()
        self.acq_set.set_pre_post_samples(postsamples=postsamples)

class AcquisitionSettings(QHBoxLayout):
    def __init__(self, zmq_rpc, GUI_name, GUI):
        super().__init__()
        self.zmq_rpc = zmq_rpc
        self.GUI = GUI
        self.GUI_name = GUI_name
        self.presamples = Presamples(zmq_rpc, GUI_name, GUI, self)
        self.postsamples = Postsamples(zmq_rpc, GUI_name, GUI, self)
        self.addWidget(self.presamples)
        self.addWidget(self.postsamples)

    def set_params(self, presamples, postsamples):
        self.presamples.set_value(presamples)
        self.postsamples.set_value(postsamples)

    def set_pre_post_samples(self, presamples=None, postsamples=None):
        if not presamples:
            presamples = self.presamples.get_value()
        if not postsamples:
            postsamples = self.postsamples.get_value()

        self.zmq_rpc.send_RPC('set_pre_post_samples', presamples, postsamples,
                              self.GUI_name)
        self.GUI.update_GUI_params()
