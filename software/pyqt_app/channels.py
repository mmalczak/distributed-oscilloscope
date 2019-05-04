from PyQt5.QtWidgets import QVBoxLayout
from parent_classes import *
from proxy import *


DBG = False


class ChannelClosure:

    def __init__(self, ADC_Lay, server_proxy, plot, GUI_name,
                 channel_count, update_triggers):
        self.menu = ChannelsMenu(self, channel_count, plot)
        self.channel_count = channel_count
        self.layout = ChannelLayout(self.menu)
        self.plot = plot
        self.GUI_name = GUI_name
        ADC_Lay.addLayout(self.layout)
        self.properties = None
        self.server_proxy = server_proxy
        self.update_triggers = update_triggers
        """updates the list of channels for the trigger"""

    def add_available_ADC(self, name, number_of_channels):
        self.menu.add_available_ADC(name, number_of_channels)

    def remove_available_ADC(self, name):
        self.menu.remove_available_ADC(name)
        if self.channel_exists():
            if(self.properties.unique_ADC_name == name):
                self.remove_channel()

    def set_channel_properties(self, unique_ADC_name, idx):
        self.properties = ChannelProperties(unique_ADC_name, idx,
                                            self.layout,
                                            self.server_proxy,
                                            self.plot,
                                            self.GUI_name, self)
        self.update_triggers()

    def remove_channel(self):
        self.properties = None
        self.plot.remove_channel(self.channel_count)
        proxy = get_proxy(self.server_proxy.proxy_addr)
        proxy.remove_channel(self.channel_count, self.GUI_name)

    def channel_exists(self):
        return self.properties is not None


class ChannelProperties:

    def __init__(self, unique_ADC_name, idx, layout, server_proxy,
                 plot, GUI_name, channel_closure):
        self.idx = idx
        self.unique_ADC_name = unique_ADC_name
        self.layout = layout
        self.server_proxy = server_proxy
        self.channel_closure = channel_closure
        self.button = ChannelEnableButton('Channel'+str(idx), idx,
                                          unique_ADC_name, server_proxy,
                                          plot, GUI_name)
        self.range_menu = ChannelRange(idx, unique_ADC_name,
                                       server_proxy)
        self.termination_menu = ChannelTermination(idx, unique_ADC_name,
                                                   server_proxy)
        self.offset_box = ChannelOffset(idx, unique_ADC_name,
                                        server_proxy)
        self.saturation_box = ChannelSaturation(idx, unique_ADC_name,
                                                server_proxy)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.range_menu)
        self.layout.addWidget(self.termination_menu)
        self.layout.addWidget(self.offset_box)
        self.layout.addWidget(self.saturation_box)

    def set_button_active(self, active):
        self.button.set_active(active)

    def set_button_range(self, value):
        self.range_menu.set_value(value)

    def set_button_termination(self, value):
        self.termination_menu.set_value(value)

    def set_button_offset(self, value):
        self.offset_box.set_value(value)

    def set_button_saturation(self, value):
        self.saturation_box.set_value(value)

    def set_channel_params(self, active, range, termination, offset,
                           saturation):
        self.button.set_active(active)
        self.range_menu.set_value(range)
        self.termination_menu.set_value(termination)
        self.offset_box.set_value(offset)
        self.saturation_box.set_value(saturation)

    def __del__(self):
        self.button.deleteLater()
        self.range_menu.deleteLater()
        self.termination_menu.deleteLater()
        self.offset_box.deleteLater()
        self.saturation_box.deleteLater()


class ChannelsMenu(QMenuBar):

    def __init__(self, channel_closure, channel_count, plot):
        super().__init__()
        self.channel_count = channel_count
        self.channel_closure = channel_closure
        self.ADCs_menu = self.addMenu("ADCs")
        self.ADCs = {}
        self.selected_ADC = None
        none = self.ADCs_menu.addAction("None")
        none.triggered.connect(self.remove_channel)
        self.plot = plot

    def add_available_ADC(self, name, number_of_channels):
        ADC = self.ADCs_menu.addMenu(name)
        self.ADCs[name] = ADC
        ADC.menuAction().hovered.connect(self.select_ADC)
        for count in range(0, number_of_channels):
            chan = ADC.addAction("chan " + str(count))
            chan.triggered.connect(self.add_channel)

    def remove_available_ADC(self, name):
        self.ADCs_menu.removeAction(self.ADCs[name].menuAction())

    def select_ADC(self):
        self.selected_ADC = self.sender().text()

    def add_channel(self):
        if self.channel_closure.channel_exists():
            self.remove_channel()
        str_chan = self.sender().text()
        idx = int(str_chan.split()[1])
        self.channel_closure.set_channel_properties(self.selected_ADC,
                                                    idx)
        self.plot.add_channel(self.channel_count)
        proxy = get_proxy(self.channel_closure.server_proxy.proxy_addr)
        proxy.add_channel(self.channel_count, self.selected_ADC, idx,
                          self.channel_closure.GUI_name)

    def remove_channel(self):
        self.channel_closure.remove_channel()


class ChannelLayout(QVBoxLayout):

    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.addWidget(self.menu)
        self.ADCs = {}
        self.channel = None


class ChannelEnableButton(Button):

    def __init__(self, button_name, idx, unique_ADC_name, server_proxy,
                 plot, GUI_name):
        super().__init__(button_name, idx, unique_ADC_name)
        self.server_proxy = server_proxy
        self.plot = plot
        self.GUI_name = GUI_name  # probably to be removed

    def action(self):
        active = not self.isChecked()


class ChannelRange(Menu):

    def __init__(self, idx, unique_ADC_name, server_proxy):
        super().__init__(idx, unique_ADC_name)
        self.server_proxy = server_proxy
        self.range = self.addMenu("Range")
        range_10V = self.range.addAction("10V")
        range_10V.setText("10V")
        range_10V.triggered.connect(self.action)
        range_1V = self.range.addAction("1V")
        range_1V.setText("1V")
        range_1V.triggered.connect(self.action)
        range_100mV = self.range.addAction("100mV")
        range_100mV.setText("100mV")
        range_100mV.triggered.connect(self.action)

    def action(self):
        range_value_str = self.sender().text()
        try:
            proxy = get_proxy(self.server_proxy.proxy_addr)
            proxy.set_channel_range(range_value_str, self.idx,
                                    self.unique_ADC_name)
        except Exception as e:
            print(e)

    def set_value(self, value):
        self.range.setTitle("Range " + str(value))


class ChannelTermination(Menu):

    def __init__(self, idx, unique_ADC_name, server_proxy):
        super().__init__(idx, unique_ADC_name)
        self.server_proxy = server_proxy
        self.termination = self.addMenu("Termination")
        termination_0 = self.termination.addAction("0")
        termination_0.setText("0")
        termination_0.triggered.connect(self.action)
        termination_1 = self.termination.addAction("1")
        termination_1.setText("1")
        termination_1.triggered.connect(self.action)

    def action(self):
        termination_str = self.sender().text()
        try:
            proxy = get_proxy(self.server_proxy.proxy_addr)
            proxy.set_ADC_parameter('channel_termination',
                                    termination_str,
                                    self.unique_ADC_name,
                                    self.idx)
        except Exception as e:
            print(e)

    def set_value(self, value):
        self.termination.setTitle("Termination " + str(value))


class ChannelOffset(Box):

    def __init__(self, idx, unique_ADC_name, server_proxy):
        super().__init__(idx, unique_ADC_name, "Offset uV")
        self.server_proxy = server_proxy
        self.box.setMinimum(-5000000)
        self.box.setMaximum(5000000)

    def value_change(self):
        offset = self.box.value()
        try:
            proxy = get_proxy(self.server_proxy.proxy_addr)
            proxy.set_ADC_parameter('channel_offset', offset,
                                    self.unique_ADC_name, self.idx)
        except Exception as e:
            print(e)


class ChannelSaturation(Box):

    def __init__(self, idx, unique_ADC_name, server_proxy):
        super().__init__(idx, unique_ADC_name, "Saturation")
        self.server_proxy = server_proxy
        self.box.setMinimum(0)
        self.box.setMaximum(65535)

    def value_change(self):
        saturation = self.box.value()
        try:
            proxy = get_proxy(self.server_proxy.proxy_addr)
            proxy.set_ADC_parameter('channel_saturation', saturation,
                                    self.unique_ADC_name, self.idx)
        except Exception as e:
            print(e)
