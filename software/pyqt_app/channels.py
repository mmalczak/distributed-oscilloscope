from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect
from colors import Colors
from parent_classes import Button
from parent_classes import Menu
from parent_classes import Box
DBG = False


class ChannelClosure:

    def __init__(self, channel_inputs_layout, ver_set_layout, zmq_rpc,
                 plot, GUI_name, channel_count, update_triggers, GUI):
        self.adc_label = QLabel("")
        self.adc_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.channel_label = QLabel("")
        self.channel_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.menu = ChannelsMenu(self, channel_count, plot, self.adc_label,
                                 self.channel_label)
        self.channel_count = channel_count
        self.chan_in_layout = ChannelInputsLayout(self.menu, self.adc_label,
                                                  self.channel_label,
                                                  channel_count)
        self.chan_in_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.chan_set_layout = ChannelSettingsLayout(channel_count)
        self.plot = plot
        self.GUI_name = GUI_name
        channel_inputs_layout.addLayout(self.chan_in_layout)
        ver_set_layout.addLayout(self.chan_set_layout)
        self.properties = None
        self.zmq_rpc = zmq_rpc
        self.GUI = GUI
        """updates the list of channels for the trigger"""
        self.update_triggers = update_triggers
        """adds layout to that is shown to the user, nothing there
        should be active, None is unique_ADC_name"""
        self.set_channel_properties(None, 0)

    def add_available_ADC(self, name, number_of_channels):
        self.menu.add_available_ADC(name, number_of_channels)

    def remove_available_ADC(self, name, remote=False):
        self.menu.remove_available_ADC(name)
        if self.channel_exists():
            if(self.properties.unique_ADC_name == name):
                self.remove_channel(remote)

    def set_channel_properties(self, unique_ADC_name, idx):
        self.properties = ChannelProperties(unique_ADC_name, idx,
                                            self.chan_set_layout,
                                            self.zmq_rpc,
                                            self.plot,
                                            self.GUI,
                                            self.GUI_name,
                                            self)
        self.update_triggers()

    def remove_channel(self, remote=False):
        """unique_ADC_name is None if there is actually no channel,
        just the layout that is shown to the user. In that case
        just the properties should be removed"""
        if self.properties.unique_ADC_name is not None:
            self.plot.remove_channel(self.channel_count)
            if not remote:
                self.zmq_rpc.send_RPC('remove_channel', self.channel_count,
                                      self.GUI_name)
        """When the channel is removed the widgets should remain for
        the user, but they are disabled.
        The widgets are deleted and new are created so that they
        contain the information that they are not connected to any of
        the ADCs"""
        self.set_channel_properties(None, 0)
        self.adc_label.setText('')
        self.channel_label.setText('')

    def channel_exists(self):
        return self.properties.unique_ADC_name is not None


class ChannelProperties:

    def __init__(self, unique_ADC_name, idx, chan_set_layout,
                 zmq_rpc, plot, GUI, GUI_name, channel_closure):
        self.idx = idx
        self.unique_ADC_name = unique_ADC_name
        self.chan_set_layout = chan_set_layout
        self.zmq_rpc = zmq_rpc
        self.GUI = GUI
        self.channel_closure = channel_closure
        self.button = ChannelEnableButton(idx, unique_ADC_name, zmq_rpc,
                                          plot, GUI, GUI_name)
        self.range_menu = ChannelRange(idx, unique_ADC_name, zmq_rpc, GUI)
        self.termination_menu = ChannelTermination(idx, unique_ADC_name,
                                                   zmq_rpc, GUI)
        self.offset_box = ChannelOffset(idx, unique_ADC_name, zmq_rpc, GUI)

        self.chan_set_layout.addWidget(self.button)
        self.chan_set_layout.addWidget(self.range_menu)
        self.chan_set_layout.addWidget(self.termination_menu)
        self.chan_set_layout.addWidget(self.offset_box)

    def set_button_active(self, active):
        self.button.set_active(active)

    def set_button_range(self, value):
        self.range_menu.set_value(value)

    def set_button_termination(self, value):
        self.termination_menu.set_value(value)

    def set_button_offset(self, value):
        self.offset_box.set_value(value)

    def set_channel_params(self, active, range, termination, offset):
        self.button.set_active(active)
        self.range_menu.set_value(range)
        self.termination_menu.set_value(termination)
        self.offset_box.set_value(offset)

    def __del__(self):
        self.button.deleteLater()
        self.range_menu.deleteLater()
        self.termination_menu.deleteLater()
        self.offset_box.deleteLater()


class ChannelsMenu(QMenuBar):

    def __init__(self, channel_closure, channel_count, plot, adc_label,
                 channel_label):
        super().__init__()
        self.adc_label = adc_label
        self.channel_label = channel_label
        self.channel_count = channel_count
        self.channel_closure = channel_closure
        chan_disp = str(channel_count + 1)
        sp = "                            "
        """Don't know how ot center the channel menu"""
        self.ADCs_menu = self.addMenu(sp + "Channel " + chan_disp + sp)
        menuBr = QMenuBar(self.ADCs_menu)
        self.setCornerWidget(menuBr, Qt.TopRightCorner)
        self.ADCs = {}
        self.selected_ADC = None
        disconnect = self.ADCs_menu.addAction("Disconnect")
        disconnect.triggered.connect(self.remove_channel)
        self.plot = plot
        """+1 is beacuse channels are indexed from 0, but displayed from 1"""
        color = str((tuple(Colors().get_color(channel_count))))
        self.setStyleSheet("border: 2px solid rgb" + color + ";")

    def add_available_ADC(self, name, number_of_channels):
        display_name = name.replace('._tcp.local.', '')
        ADC = self.ADCs_menu.addMenu(display_name)
        self.ADCs[name] = ADC
        ADC.menuAction().hovered.connect(self.select_ADC)
        for count in range(0, number_of_channels):
            chan = ADC.addAction("Chan " + str(count))
            chan.triggered.connect(self.add_channel)

    def remove_available_ADC(self, name):
        self.ADCs_menu.removeAction(self.ADCs[name].menuAction())

    def select_ADC(self):
        self.selected_ADC = self.sender().text() + '._tcp.local.'

    def add_channel(self):
        if self.channel_closure.channel_exists():
            self.remove_channel()
        str_chan = self.sender().text()
        idx = int(str_chan.split()[1])
        display_name = self.selected_ADC.replace('._tcp.local.', '')
        self.adc_label.setText(display_name)
        self.channel_label.setText(str_chan)
        self.channel_closure.set_channel_properties(self.selected_ADC, idx)
        self.plot.add_channel(self.channel_count)
        rpc = self.channel_closure.zmq_rpc
        rpc.send_RPC('add_channel', self.channel_count, self.selected_ADC, idx,
                     self.channel_closure.GUI_name)

    def remove_channel(self):
        self.channel_closure.remove_channel()


class ChannelInputsLayout(QVBoxLayout):

    def __init__(self, menu, adc_label, channel_label, channel_count):
        super().__init__()
        self.menu = menu
#        GUI_chan_label = ChannelLabel(channel_count)
#        self.addWidget(GUI_chan_label)
        self.addWidget(self.menu)
        self.addWidget(adc_label)
        self.addWidget(channel_label)
        self.ADCs = {}
        self.channel = None


class ChannelSettingsLayout(QVBoxLayout):

    def __init__(self, channel_count):
        super().__init__()
        GUI_chan_label = ChannelLabel(channel_count)
        self.addWidget(GUI_chan_label)


class ChannelEnableButton(Button):

    def __init__(self, idx, unique_ADC_name, zmq_rpc,
                 plot, GUI, GUI_name):
        super().__init__("Enable", idx, unique_ADC_name)
        self.zmq_rpc = zmq_rpc
        self.plot = plot
        self.GUI_name = GUI_name  # probably to be removed
        self.GUI = GUI

    def action(self):
        active = not self.isChecked()


class ChannelRange(Menu):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, GUI):
        super().__init__(idx, unique_ADC_name)
        self.zmq_rpc = zmq_rpc
        self.GUI = GUI
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
            rpc = self.zmq_rpc
            rpc.send_RPC('set_channel_range', range_value_str, self.idx,
                         self.unique_ADC_name)
        except Exception as e:
            print(e)
        self.GUI.update_GUI_params()

    def set_value(self, value):
        if value == 100:
            self.range.setTitle("Range " + str(value) + "mV")
        else:
            self.range.setTitle("Range " + str(value) + "V")


class ChannelTermination(Menu):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, GUI):
        super().__init__(idx, unique_ADC_name)
        self.zmq_rpc = zmq_rpc
        self.GUI = GUI
        self.termination = self.addMenu("Termination")
        termination_0 = self.termination.addAction("1M\u03A9")
        termination_0.setText("1M\u03A9")
        termination_0.triggered.connect(self.action)
        termination_1 = self.termination.addAction("50\u03A9")
        termination_1.setText("50\u03A9")
        termination_1.triggered.connect(self.action)
        self.term_num_map = {"1M\u03A9": "0", "50\u03A9": "1"}
        self.num_term_map = {"0": "1M\u03A9", "1": "50\u03A9"}

    def action(self):
        termination_str = self.sender().text()
        try:
            rpc = self.zmq_rpc
            rpc.send_RPC('set_ADC_parameter', 'channel_termination',
                         self.term_num_map[termination_str],
                         self.unique_ADC_name, self.idx)
        except Exception as e:
            print(e)
        self.GUI.update_GUI_params()

    def set_value(self, value):
        term = self.num_term_map[str(value)]
        self.termination.setTitle("Term. " + term)


class ChannelOffset(Box):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, GUI):
        super().__init__(idx, unique_ADC_name, "Offset uV", 'vertical')
        self.zmq_rpc = zmq_rpc
        self.GUI = GUI
        self.box.setMinimum(-5000000)
        self.box.setMaximum(5000000)

    def value_change(self):
        offset = self.box.value()
        try:
            rpc = self.zmq_rpc
            rpc.send_RPC('set_ADC_parameter', 'channel_offset', offset,
                         self.unique_ADC_name, self.idx)
        except Exception as e:
            print(e)
        self.GUI.update_GUI_params()


class ChannelLabel(QLabel):
    def __init__(self, channel_count):
        chan_disp = str(channel_count + 1)
        """+1 is beacuse channels are indexed from 0, but displayed from 1"""
        super().__init__("Channel " + chan_disp)
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.setMaximumHeight(25)
        color = str((tuple(Colors().get_color(channel_count))))
        self.setStyleSheet("border: 2px solid rgb" + color + ";")
