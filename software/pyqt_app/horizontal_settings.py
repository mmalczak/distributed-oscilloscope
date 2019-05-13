from parent_classes import *
from proxy import *
from PyQt5.QtWidgets import QVBoxLayout


class Presamples(Box):
    def __init__(self, server_proxy, GUI_name):
        super().__init__(0, "No_ADC", "Presamples")
        self.box.setMinimum(0)
        self.box.setMaximum(1000000)
        """TODO check how many pre and postsamples maximum"""
        self.server_proxy = server_proxy
        self.GUI_name = GUI_name

    def value_change(self):
        presamples = self.box.value()
        proxy = get_proxy(self.server_proxy.proxy_addr)
        proxy.set_presamples(presamples, self.GUI_name)


class Postsamples(Box):
    def __init__(self, server_proxy, GUI_name):
        super().__init__(0, "No_ADC", "Postsamples")
        self.box.setMinimum(0)
        self.box.setMaximum(1000000)
        """TODO check how many pre and postsamples maximum"""
        self.server_proxy = server_proxy
        self.GUI_name = GUI_name

    def value_change(self):
        postsamples = self.box.value()
        proxy = get_proxy(self.server_proxy.proxy_addr)
        proxy.set_postsamples(postsamples, self.GUI_name)

class AcquisitionSettings(QVBoxLayout):
    def __init__(self, server_proxy, GUI_name):
        super().__init__()
        self.server_proxy = server_proxy
        self.GUI_name = GUI_name
        self.presamples = Presamples(server_proxy, GUI_name)
        self.postsamples = Postsamples(server_proxy, GUI_name)
        self.addWidget(self.presamples)
        self.addWidget(self.postsamples)

    def set_params(self, presamples, postsamples):
        self.presamples.set_value(presamples)
        self.postsamples.set_value(postsamples)
