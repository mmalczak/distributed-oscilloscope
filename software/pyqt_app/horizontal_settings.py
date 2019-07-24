from parent_classes import Slider_Box
from parent_classes import Box
import sys
sys.path.append('../')
from PyQt5.QtWidgets import QVBoxLayout


class Percentage(Slider_Box):
    def __init__(self, zmq_rpc, GUI_name, GUI, acq_set):
        super().__init__(0, "No_ADC", "Trigger Position[%]")
        self.slider.setMinimum(0)
        self.box.setMinimum(0)
        self.slider.setMaximum(99)
        self.box.setMaximum(99)
        """TODO check how many pre and postsamples maximum"""
        self.zmq_rpc = zmq_rpc
        self.GUI_name = GUI_name
        self.GUI = GUI
        self.acq_set = acq_set

    def value_change_slider(self):
        percentage = self.slider.value()
        self.acq_set.set_acq_set(percentage=percentage)

    def value_change_box(self):
        percentage = self.box.value()
        self.acq_set.set_acq_set(percentage=percentage)



class Time(Box):
    def __init__(self, zmq_rpc, GUI_name, GUI, acq_set):
        super().__init__(0, "No_ADC", "Acquisition Time[us]")
        self.box.setMinimum(1)
        self.box.setMaximum(1000)
        """TODO check how many pre and postsamples maximum"""
        self.zmq_rpc = zmq_rpc
        self.GUI_name = GUI_name
        self.GUI = GUI
        self.acq_set = acq_set

    def value_change(self):
        time = self.box.value()
        self.acq_set.set_acq_set(time=time)


class AcquisitionSettings(QVBoxLayout):
    def __init__(self, zmq_rpc, GUI_name, GUI):
        super().__init__()
        self.zmq_rpc = zmq_rpc
        self.GUI = GUI
        self.GUI_name = GUI_name
        self.time= Time(zmq_rpc, GUI_name, GUI, self)
        self.percentage= Percentage(zmq_rpc, GUI_name, GUI, self)
        self.addWidget(self.time)
        self.addWidget(self.percentage)

    def set_params(self, presamples, postsamples):
        time = (presamples + postsamples)/100
        percentage = presamples / (presamples + postsamples) * 100
        self.time.set_value(time)
        self.percentage.set_value(percentage)

    def set_acq_set(self, time=None, percentage=None):
        if not time:
            time = self.time.get_value()
        if not percentage:
            percentage= self.percentage.get_value()
        samples = time * 100
        presamples = int(samples * percentage / 100)
        postsamples = int(samples * (100 - percentage) / 100)

        self.zmq_rpc.send_RPC('set_pre_post_samples', presamples, postsamples,
                              self.GUI_name)
        self.GUI.update_GUI_params()
