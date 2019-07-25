from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from parent_classes import Box
from parent_classes import Dial_Box
from parent_classes import Button
from parent_classes import Menu
from PyQt5.QtWidgets import QHBoxLayout


class TriggerClosure:

    def __init__(self, trigger_inputs_layout, trig_set_layout, zmq_rpc,
                 plot, GUI_name, GUI_trigger_idx, channels, available_ADCs,
                 GUI):
        self.unique_ADC_name = None
        self.ADC_idx = None
        self.__button = None
        self.__polarity_menu = None
        self.__delay_box = None
        self.__threshold_box = None

        self.__adc_label = QLabel('')
        self.__channel_label = QLabel('')
        self.__adc_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.__channel_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.trigger_type = 'internal'  # default one
        self.__GUI_trigger_idx = GUI_trigger_idx
        self.menu_type = TriggerTypeMenu(self)
        self.__trig_in_layout = TriggerInputsLayout(self.__adc_label)
        self.__trig_set_layout = TriggerSettingsLayout(self.menu_type,
                                                       self.__channel_label)
        self.__plot = plot
        self.__GUI_name = GUI_name
        self.__GUI = GUI
        trigger_inputs_layout.addLayout(self.__trig_in_layout)
        trig_set_layout.addLayout(self.__trig_set_layout)
        self.__zmq_rpc = zmq_rpc
        self.__GUI = GUI
        self.channels = channels
        self.available_ADCs = available_ADCs
        self.__int_trig_menu = None
        self.__ext_trig_menu = None
        self.__set_empty_trigger()

        self.__int_trig_menu = IntTriggersMenu(self, self.__GUI_trigger_idx,
                                               self.channels)
        self.__ext_trig_menu = ExtTriggersMenu(self, self.__GUI_trigger_idx)
        self.__trig_in_layout.set_menu(self.__ext_trig_menu)
        self.__trig_set_layout.set_menu(self.__int_trig_menu)

        self.set_menu()
        """Adds widgets in the GUI, when unique_ADC_name==None,
        widgets are disabled"""


    def register_ADC(self, name):
        self.__ext_trig_menu.register_ADC(name)


    def unregister_ADC(self, name):
        self.__ext_trig_menu.unregister_ADC(name)
        if self.trigger_exists():
            if(self.unique_ADC_name == name):
                self.remove_trigger(remote)

    def set_ADC_available(self, unique_ADC_name):
        self.__ext_trig_menu.set_ADC_available(unique_ADC_name)

    def set_ADC_unavailable(self, unique_ADC_name):
        self.__ext_trig_menu.set_ADC_unavailable(unique_ADC_name)

    def update_available_triggers_list(self):
        self.__int_trig_menu.update_available_triggers_list()
        #self.__ext_trig_menu.update_available_triggers_list()

    def set_menu(self):
        if(self.trigger_type == 'internal'):
            self.__int_trig_menu.setEnabled(True)
            self.__ext_trig_menu.setEnabled(False)
        else:
            self.__int_trig_menu.setEnabled(False)
            self.__ext_trig_menu.setEnabled(True)
        self.__exchange_widgets(None, None)

    def remove_trigger(self, remote=False):
        run_button = self.__GUI.run_stop_acquisition
        if run_button.is_active():
            run_button.toggle()
            run_button.action()
        if self.trigger_exists():
            self.__plot.remove_trigger()
            if not remote:
                self.__zmq_rpc.send_RPC('remove_trigger', self.__GUI_name)
        self.__remove_widgets()
        self.__set_empty_trigger()
        self.__adc_label.setText('')
        self.__channel_label.setText('')
        self.__int_trig_menu.ADCs_menu.setTitle("Select channel to trigger")

    def __exchange_widgets(self, unique_ADC_name, ADC_idx=0):
        self.__remove_widgets()
        self.unique_ADC_name = unique_ADC_name
        self.ADC_idx = ADC_idx
        self.__set_widgets()

    def set_trigger(self, unique_ADC_name, ADC_channel_idx, GUI_channel_idx):
        self.remove_trigger()
        self.__exchange_widgets(unique_ADC_name, ADC_channel_idx)
        if self.trigger_type == 'internal':
            self.__plot.add_trigger(GUI_channel_idx)
            self.__zmq_rpc.send_RPC('add_trigger', 'internal', unique_ADC_name,
                                    ADC_channel_idx, self.__GUI_name)
            self.__GUI.update_GUI_params()
            display_name = "Channel {}".format(GUI_channel_idx + 1)
            """ +1 beacause when displaying the numeration is from 1, not
            from 0"""
            self.__channel_label.setText(display_name)
        else:
            self.__zmq_rpc.send_RPC('add_trigger', 'external', unique_ADC_name,
                                    0, self.__GUI_name)
            self.__GUI.update_GUI_params()
            display_name = unique_ADC_name.replace('._tcp.local.', '')
            self.__adc_label.setText(display_name)

    def trigger_exists(self):
        return self.unique_ADC_name is not None

    def __set_empty_trigger(self):
        self.ADC_idx = None
        self.unique_ADC_name = None
        self.__set_widgets()

    def __set_widgets(self):
        self.__button = TriggerEnableButton(self.ADC_idx, self.unique_ADC_name,
                                            self.__zmq_rpc, self.trigger_type,
                                            self.__GUI)
        self.__polarity_menu = TriggerPolarity(self.ADC_idx,
                                               self.unique_ADC_name,
                                               self.__zmq_rpc,
                                               self.trigger_type,
                                               self.__GUI)
        self.__delay_box = TriggerDelay(self.ADC_idx, self.unique_ADC_name,
                                        self.__zmq_rpc, self.trigger_type,
                                        self.__GUI)
        self.__threshold_box = TriggerThreshold(self.ADC_idx,
                                                self.unique_ADC_name,
                                                self.__zmq_rpc, self.__GUI)

        self.__trig_set_layout.addWidget(self.__button)
        self.__trig_set_layout.addWidget(self.__polarity_menu)
        self.dials_layout = QHBoxLayout() 
        self.__trig_set_layout.addLayout(self.dials_layout)
        self.dials_layout.addWidget(self.__delay_box.frame)
        if self.trigger_type == 'internal':
            self.dials_layout.addWidget(self.__threshold_box.frame)

    def __remove_widgets(self):
        self.__button.deleteLater()
        self.__polarity_menu.deleteLater()
        self.__delay_box.frame.deleteLater()
        self.__threshold_box.frame.deleteLater()

    def set_params(self, enable, polarity, delay, threshold_mv):
        self.__button.set_active(enable)
        self.__delay_box.set_value(delay)
        self.__polarity_menu.set_value(polarity)
        if self.trigger_type == 'internal':
            threshold_V = threshold_mv/1000
            self.__threshold_box.set_value(threshold_mv)
            self.__plot.trigger.set_value(threshold_V)

    def set_type(self, type):
        if(self.trigger_type == type):
            pass
        else:
            self.trigger_type = type
            if self.trigger_exists():
                self.remove_trigger()
            self.set_menu()


class TriggerTypeMenu(QMenuBar):

    def __init__(self, trigger_closure):
        super().__init__()
        self.trigger_closure = trigger_closure
        print(self.trigger_closure)
        self.trig_menu = self.addMenu("Trigger Type - " +
                               self.trigger_closure.trigger_type.capitalize())
        trig = self.trig_menu.addAction("Internal")
        trig.triggered.connect(self.select_type)
        trig = self.trig_menu.addAction("External")
        trig.triggered.connect(self.select_type)

    def select_type(self):
        type = self.sender().text()
        self.trig_menu.setTitle("Trigger Type - " + type)
        type = type.lower()
        self.trigger_closure.set_type(type)


class TriggersMenu(QMenuBar):

    def __init__(self, trigger_closure, GUI_trigger_idx):
        super().__init__()
        self.__GUI_trigger_idx = GUI_trigger_idx
        self.trigger_closure = trigger_closure
        self.ADCs = {}
        self.selected_ADC = None

    def update_available_triggers_list(self):
        pass

    def __del__(self):
        self.trigger_closure.remove_trigger


class IntTriggersMenu(TriggersMenu):

    def __init__(self, trigger_closure, GUI_trigger_idx, channels):
        super().__init__(trigger_closure, GUI_trigger_idx)
        self.ADCs_menu = self.addMenu("Select channel to trigger")
        self.channels = channels
        self.actions = []

    def update_available_triggers_list(self):
        self.ADCs_menu.clear()
        none = self.ADCs_menu.addAction("Disconnect")
        none.triggered.connect(self.trigger_closure.remove_trigger)
        for channel in self.channels:
            if channel.channel_exists():
                channel_disp = str(channel.GUI_channel_idx + 1)
                chan = self.ADCs_menu.addAction("Channel: " + channel_disp)
                chan.triggered.connect(self.select_trigger)
                self.actions.append(chan)
        if self.trigger_closure.trigger_exists() and\
                self.trigger_closure.trigger_type == 'internal':
            self.add_trigger()
            """this is done in case the ADC connected to the channel on
            which I trigger changes """

    def select_trigger(self):
        str_trigg = self.sender().text()
        channel_disp = int(str_trigg.split()[1])
        self.__GUI_channel_idx = channel_disp - 1
        self.add_trigger()

    def add_trigger(self):
        selected_ADC = self.channels[self.__GUI_channel_idx].unique_ADC_name
        chan_disp = str(self.__GUI_channel_idx+1)
        self.ADCs_menu.setTitle("Channel " + chan_disp)
        """+1 is beacuse channels are indexed from 0, but displayed from 1"""
        ADC_channel_idx = self.channels[self.__GUI_channel_idx].ADC_channel_idx
        self.trigger_closure.set_trigger(selected_ADC, ADC_channel_idx,
                                         self.__GUI_channel_idx)


class ExtTriggersMenu(TriggersMenu):

    def __init__(self, trigger_closure, GUI_trigger_idx):
        super().__init__(trigger_closure, GUI_trigger_idx)
        self.ADCs_menu = self.addMenu("Select external trigger")
        self.ADCs = {}
        none = self.ADCs_menu.addAction("None")
        none.triggered.connect(self.trigger_closure.remove_trigger)

    def unregister_ADC(self, name):
        action = self.ADCs[name]
        self.ADCs_menu.removeAction(action)

    def register_ADC(self, name):
        display_name = name.replace('._tcp.local.', '')
        ADC = self.ADCs_menu.addAction(display_name)
        self.ADCs[name] = ADC
        ADC.triggered.connect(self.select_trigger)

    def set_ADC_unavailable(self, unique_ADC_name):
        self.ADCs[unique_ADC_name].setEnabled(False)

    def set_ADC_available(self, unique_ADC_name):
        self.ADCs[unique_ADC_name].setEnabled(True)

    def select_trigger(self):
        self.selected_ADC = self.sender().text() + '._tcp.local.'
        self.add_trigger()

    def add_trigger(self):
        self.trigger_closure.set_trigger(self.selected_ADC, 0, None)


class TriggerInputsLayout(QVBoxLayout):

    def __init__(self, adc_label):
        super().__init__()
        self.__adc_label = adc_label
        self.menu = None
        self.ADCs = {}
        self.trigger = None

    def set_menu(self, menu):
        if self.menu is not None:
            self.menu.deleteLater()
        self.menu = menu
        self.addWidget(self.menu)
        self.addWidget(self.__adc_label)


class TriggerSettingsLayout(QVBoxLayout):

    def __init__(self, menu_type, channel_label):
        super().__init__()
        self.menu = None
        self.menu_type = menu_type
        self.__channel_label = channel_label
        self.addWidget(self.menu_type)

    def set_menu(self, menu):
        if self.menu is not None:
            self.menu.deleteLater()
        self.menu = menu
        self.addWidget(self.menu)
        self.addWidget(self.__channel_label)


class TriggerThreshold(Dial_Box):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, GUI):
        super().__init__(idx, unique_ADC_name, "Treshold mV", 'vertical')
        self.__zmq_rpc = zmq_rpc
        self.unique_ADC_name = unique_ADC_name
        self.idx = idx
        self.__GUI = GUI
        self.box.setMinimum(-5000)
        self.dial.setMinimum(-5000)
        self.box.setMaximum(4999)
        self.dial.setMaximum(4999)

    def value_change_dial(self):
        value = self.dial.value()
        self.value_change(value)

    def value_change_box(self):
        value = self.box.value()
        self.value_change(value)

    def set_value(self, value):
        self.dial.setValue(value)
        self.box.setValue(value)

    def value_change(self, threshold):
        # threshold in mV
        self.__zmq_rpc.send_RPC('set_ADC_parameter',
                                'internal_trigger_threshold', threshold,
                                self.unique_ADC_name, self.idx)
        self.__GUI.update_GUI_params()


class TriggerEnableButton(Button):

    def __init__(self, idx, unique_ADC_name, zmq_rpc,
                 type, GUI):
        super().__init__("Enable", idx, unique_ADC_name)
        self.__zmq_rpc = zmq_rpc
        self.type = type
        self.__GUI = GUI

    def action(self):
        self.__zmq_rpc.send_RPC('set_ADC_parameter',
                                self.type + '_trigger_enable',
                                not self.isChecked(), self.unique_ADC_name,
                                self.idx)
        self.__GUI.update_GUI_params()


class TriggerPolarity(Menu):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, type, GUI):
        super().__init__(idx, unique_ADC_name)
        self.__zmq_rpc = zmq_rpc
        self.type = type
        self.__GUI = GUI
        self.polarity = self.addMenu("Polarity")
        self.polarity.setTitle("Polarity")
        polarity_0 = self.polarity.addAction("0")
        polarity_0.setText('positive')
        polarity_0.triggered.connect(self.action)
        polarity_1 = self.polarity.addAction("1")
        polarity_1.setText('negative')
        polarity_1.triggered.connect(self.action)
        self.polarity_num_map = {'positive':0, 'negative':1}
        self.num_polarity_map = {0:'positive', 1:'negative'}

    def action(self):
        polarity_str = self.sender().text()
        self.__zmq_rpc.send_RPC('set_ADC_parameter',
                                self.type + '_trigger_polarity',
                                self.polarity_num_map[polarity_str],
                                self.unique_ADC_name, self.idx)
        self.__GUI.update_GUI_params()

    def set_value(self, value):
        polarity = self.num_polarity_map[value]
        self.polarity.setTitle("Polarity " + polarity)


class TriggerDelay(Dial_Box):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, type, GUI):
        super().__init__(idx, unique_ADC_name, "Delay", 'vertical')
        self.__zmq_rpc = zmq_rpc
        self.type = type
        self.__GUI = GUI
        self.box.setMinimum(0)
        self.dial.setMinimum(0)
        self.box.setMaximum(65535)
        self.dial.setMaximum(65535)


    def value_change_dial(self):
        value = self.dial.value()
        self.value_change(value)

    def value_change_box(self):
        value = self.box.value()
        self.value_change(value)

    def set_value(self, value):
        self.dial.setValue(value)
        self.box.setValue(value)

    def value_change(self, delay):
        self.__zmq_rpc.send_RPC('set_ADC_parameter',
                                self.type + '_trigger_delay', delay,
                                self.unique_ADC_name, self.idx)
        self.__GUI.update_GUI_params()
