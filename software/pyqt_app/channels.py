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
                 plot, GUI_name, GUI_channel_idx, update_triggers, GUI):
        self.__adc_label = QLabel("")
        self.__adc_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.__channel_label = QLabel("")
        self.__channel_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.__menu = ChannelsMenu(self, GUI_channel_idx, GUI)
        self.GUI_channel_idx = GUI_channel_idx
        self.__chan_in_layout = ChannelInputsLayout(self.__menu, self.__adc_label,
                                             self.__channel_label)
        self.__chan_set_layout = ChannelSettingsLayout(GUI_channel_idx)
        channel_inputs_layout.addLayout(self.__chan_in_layout)
        ver_set_layout.addLayout(self.__chan_set_layout)
        self.__plot = plot
        self.__GUI_name = GUI_name
        self.__zmq_rpc = zmq_rpc
        self.__GUI = GUI
        """updates the list of channels for the trigger"""
        self.update_triggers = update_triggers
        self.__range_menu = None
        self.__termination_menu = None
        self.__offset_box = None
        self.ADC_channel_idx = None
        self.unique_ADC_name = None
        self.__set_empty_channel()

    def register_ADC(self, name, number_of_channels):
        self.__menu.register_ADC(name, number_of_channels)

    def unregister_ADC(self, name, remote=False):
        self.__menu.unregister_ADC(name)
        if self.channel_exists():
            if(self.unique_ADC_name == name):
                self.remove_channel(remote)

    def __set_empty_channel(self):
        self.ADC_channel_idx = None
        self.unique_ADC_name = None
        self.__set_widgets()

    def set_channel(self, unique_ADC_name, ADC_channel_idx):
        self.__remove_widgets()
        self.ADC_channel_idx = ADC_channel_idx
        self.unique_ADC_name = unique_ADC_name
        self.__set_widgets()
        self.update_triggers()
        self.__plot.add_channel(self.GUI_channel_idx)
        rpc = self.__zmq_rpc
        rpc.send_RPC('add_channel', self.GUI_channel_idx, self.unique_ADC_name,
                     self.ADC_channel_idx, self.__GUI_name)
        self.__GUI.update_GUI_params()
        self.__set_labels()

    def remove_channel(self, remote=False):
        if self.channel_exists():
            trigger = self.__GUI.triggers[0]
            if(trigger.ADC_idx == self.ADC_channel_idx and
               trigger.unique_ADC_name == self.unique_ADC_name):
                trigger.remove_trigger()
            self.__plot.remove_channel(self.GUI_channel_idx)
            if not remote:
                self.__zmq_rpc.send_RPC('remove_channel', self.GUI_channel_idx,
                                      self.__GUI_name)
            self.__remove_labels()
            self.ADC_channel_idx = None
            self.unique_ADC_name = None
        self.__remove_widgets()
        self.__set_empty_channel()

    def channel_exists(self):
        return self.unique_ADC_name is not None

    def set_channel_params(self, range, termination, offset):
        self.__range_menu.set_value(range)
        self.__termination_menu.set_value(termination)
        self.__offset_box.set_value(offset)

    def __set_widgets(self):
        self.__range_menu = ChannelRange(self.ADC_channel_idx,
                                       self.unique_ADC_name, self.__zmq_rpc,
                                       self.__GUI)
        self.__termination_menu = ChannelTermination(self.ADC_channel_idx,
                                                   self.unique_ADC_name,
                                                   self.__zmq_rpc, self.__GUI)
        self.__offset_box = ChannelOffset(self.ADC_channel_idx,
                                        self.unique_ADC_name, self.__zmq_rpc,
                                        self.__GUI)

        self.__chan_set_layout.addWidget(self.__range_menu)
        self.__chan_set_layout.addWidget(self.__termination_menu)
        self.__chan_set_layout.addWidget(self.__offset_box)

    def __set_labels(self):
        display_ADC_name = self.unique_ADC_name.replace('._tcp.local.', '')
        self.__adc_label.setText(display_ADC_name)
        self.__channel_label.setText('Channel ' + str(self.ADC_channel_idx))


    def __remove_widgets(self):
        self.__range_menu.deleteLater()
        self.__termination_menu.deleteLater()
        self.__offset_box.deleteLater()

    def __remove_labels(self):
        self.__adc_label.setText('')
        self.__channel_label.setText('')


class ChannelsMenu(QMenuBar):

    def __init__(self, channel_closure, GUI_channel_idx, GUI):
        super().__init__()
        self.__GUI = GUI
        self.GUI_channel_idx = GUI_channel_idx
        self.channel_closure = channel_closure
        chan_disp = str(GUI_channel_idx + 1)
        sp = "                            "
        """Don't know how to center the channel menu"""
        self.ADCs_menu = self.addMenu(sp + "Channel " + chan_disp + sp)
        menuBr = QMenuBar(self.ADCs_menu)
        self.setCornerWidget(menuBr, Qt.TopRightCorner)
        self.ADCs = {}
        self.selected_ADC = None
        disconnect = self.ADCs_menu.addAction("Disconnect")
        disconnect.triggered.connect(self.__remove_channel)
        """+1 is beacuse channels are indexed from 0, but displayed from 1"""
        color = str((tuple(Colors().get_color(GUI_channel_idx))))
        self.setStyleSheet("border: 2px solid rgb" + color + ";")

    def register_ADC(self, name, number_of_channels):
        display_name = name.replace('._tcp.local.', '')
        ADC = self.ADCs_menu.addMenu(display_name)
        self.ADCs[name] = ADC
        ADC.menuAction().hovered.connect(self.__select_ADC)
        for count in range(0, number_of_channels):
            chan = ADC.addAction("Chan " + str(count))
            chan.triggered.connect(self.__add_channel)

    def unregister_ADC(self, name):
        self.ADCs_menu.removeAction(self.ADCs[name].menuAction())

    def __select_ADC(self):
        self.selected_ADC = self.sender().text() + '._tcp.local.'

    def __add_channel(self):
        if self.channel_closure.channel_exists():
            self.__remove_channel()
        str_chan = self.sender().text()
        idx = int(str_chan.split()[1])
        self.channel_closure.set_channel(self.selected_ADC, idx)

    def __remove_channel(self):
        self.channel_closure.remove_channel()


class ChannelInputsLayout(QVBoxLayout):

    def __init__(self, menu, adc_label, channel_label):
        super().__init__()
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.addWidget(menu)
        self.addWidget(adc_label)
        self.addWidget(channel_label)


class ChannelSettingsLayout(QVBoxLayout):

    def __init__(self, GUI_channel_idx):
        super().__init__()
        GUI_chan_label = ChannelLabel(GUI_channel_idx)
        self.addWidget(GUI_chan_label)


class ChannelRange(Menu):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, GUI):
        super().__init__(idx, unique_ADC_name)
        self.__zmq_rpc = zmq_rpc
        self.__GUI = GUI
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
            rpc = self.__zmq_rpc
            rpc.send_RPC('set_ADC_parameter', 'channel_range', range_value_str,
                         self.unique_ADC_name, self.idx)
        except Exception as e:
            print(e)
        self.__GUI.update_GUI_params()

    def set_value(self, value):
        if value == 100:
            self.range.setTitle("Range " + str(value) + "mV")
        else:
            self.range.setTitle("Range " + str(value) + "V")


class ChannelTermination(Menu):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, GUI):
        super().__init__(idx, unique_ADC_name)
        self.__zmq_rpc = zmq_rpc
        self.__GUI = GUI
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
            rpc = self.__zmq_rpc
            rpc.send_RPC('set_ADC_parameter', 'channel_termination',
                         self.term_num_map[termination_str],
                         self.unique_ADC_name, self.idx)
        except Exception as e:
            print(e)
        self.__GUI.update_GUI_params()

    def set_value(self, value):
        term = self.num_term_map[str(value)]
        self.termination.setTitle("Term. " + term)


class ChannelOffset(Box):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, GUI):
        super().__init__(idx, unique_ADC_name, "Offset uV", 'vertical')
        self.__zmq_rpc = zmq_rpc
        self.__GUI = GUI
        self.box.setMinimum(-5000000)
        self.box.setMaximum(5000000)

    def value_change(self):
        offset = self.box.value()
        try:
            rpc = self.__zmq_rpc
            rpc.send_RPC('set_ADC_parameter', 'channel_offset', offset,
                         self.unique_ADC_name, self.idx)
        except Exception as e:
            print(e)
        self.__GUI.update_GUI_params()


class ChannelLabel(QLabel):
    def __init__(self, GUI_channel_idx):
        chan_disp = str(GUI_channel_idx + 1)
        """+1 is beacuse channels are indexed from 0, but displayed from 1"""
        super().__init__("Channel " + chan_disp)
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.setMaximumHeight(25)
        color = str((tuple(Colors().get_color(GUI_channel_idx))))
        self.setStyleSheet("border: 2px solid rgb" + color + ";")
