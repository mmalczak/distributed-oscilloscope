from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from parent_classes import Box
from parent_classes import Button
from parent_classes import TriggerPolarity


class TriggerClosure:

    def __init__(self, trigger_inputs_layout, trig_set_layout, zmq_rpc,
                 plot, GUI_name, GUI_trigger_idx, channels, available_ADCs,
                 GUI):
        self.adc_label = QLabel("")
        self.adc_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.trigger_type = 'internal'  # default one
        self.GUI_trigger_idx = GUI_trigger_idx
        self.menu_type = TriggerTypeMenu(self)
        self.trig_in_layout = TriggerInputsLayout(self.adc_label)
        self.trig_set_layout = TriggerSettingsLayout(self.menu_type)
        self.plot = plot
        self.GUI_name = GUI_name
        trigger_inputs_layout.addLayout(self.trig_in_layout)
        trig_set_layout.addLayout(self.trig_set_layout)
        self.properties = None
        self.zmq_rpc = zmq_rpc
        self.GUI = GUI
        self.channels = channels
        self.available_ADCs = available_ADCs
        self.int_trig_menu = None
        self.ext_trig_menu = None
        self.set_menu()
        self.set_trigger_properties(None, 0)
        """Adds widgets in the GUI, when unique_ADC_name==None,
        widgets are disabled"""

    def update_triggers(self):
        self.int_trig_menu.update_triggers()
        self.ext_trig_menu.update_triggers()
        try:
            if self.properties.unique_ADC_name not in self.available_ADCs:
                self.set_trigger_properties(None, 0)
        except:
            pass

    def set_menu(self):
        self.int_trig_menu = IntTriggersMenu(self, self.GUI_trigger_idx,
                                             self.plot, self.channels)
        self.ext_trig_menu = ExtTriggersMenu(self, self.GUI_trigger_idx,
                                             self.adc_label)
        if(self.trigger_type == 'internal'):
            self.int_trig_menu.setEnabled(True)
            self.ext_trig_menu.setEnabled(False)
        else:
            self.int_trig_menu.setVisible(False)
            self.ext_trig_menu.setEnabled(True)
        self.trig_in_layout.set_menu(self.ext_trig_menu)
        self.trig_set_layout.set_menu(self.int_trig_menu)

    def remove_trigger(self, remote=False):
        if self.trigger_exists():
            self.plot.remove_trigger()
            if not remote:
                self.zmq_rpc.send_RPC('remove_trigger', self.GUI_name)
        self.set_trigger_properties(None, 0)
        self.adc_label.setText('')
        self.int_trig_menu.ADCs_menu.setTitle("Select channel to trigger")

    def set_trigger_properties(self, unique_ADC_name, idx=0):
        if(self.trigger_type == 'internal'):
            self.properties = IntTriggerProperties(unique_ADC_name, idx,
                                                   self.trig_set_layout,
                                                   self.zmq_rpc,
                                                   self.plot,
                                                   self.GUI,
                                                   self.GUI_name)
        else:
            self.properties = ExtTriggerProperties(unique_ADC_name, idx,
                                                   self.trig_set_layout,
                                                   self.zmq_rpc,
                                                   self.plot,
                                                   self.GUI,
                                                   self.GUI_name)

    def trigger_exists(self):
        return self.properties.unique_ADC_name is not None


class TriggerProperties():
    """would it be better instead of creating classes
    ExtTriggerProperties and IntTriggerProperties create and delete
    threshold trigger conditionally?"""

    def __init__(self, unique_ADC_name, ADC_idx, trig_set_layout,
                 zmq_rpc, plot, GUI, GUI_name, type):
        self.ADC_idx = ADC_idx
        self.unique_ADC_name = unique_ADC_name
        self.trig_set_layout = trig_set_layout
        self.plot = plot

        self.button = TriggerEnableButton(ADC_idx, unique_ADC_name, zmq_rpc,
                                          type, GUI)
        self.polarity_menu = TriggerPolarity(ADC_idx, unique_ADC_name, zmq_rpc,
                                             type, GUI)
        self.delay_box = TriggerDelay(ADC_idx, unique_ADC_name, zmq_rpc, type,
                                      GUI)
        self.threshold_box = TriggerThreshold(ADC_idx, unique_ADC_name,
                                              zmq_rpc, GUI)

        self.trig_set_layout.addWidget(self.button)
        self.trig_set_layout.addWidget(self.polarity_menu)
        self.trig_set_layout.addWidget(self.delay_box)

    def set_active(self, value):
        self.button.set_active(value)

    def set_delay(self, delay):
        self.delay_box.set_value(delay)

    def set_polarity(self, polarity):
        self.polarity_menu.set_value(polarity)

    def set_threshold(self, threshold):
        try:
            self.threshold_box.set_value(threshold)
        except TypeError:
            pass
            """for external trigger there is not threshold, the value
            of threshold in that case is 'not_available'"""
        except Exception as e:
            print(type(e))

        try:
            self.plot.trigger.set_value(threshold)
        except AttributeError:
            pass
            """for external trigger the plot does not exist"""
        except Exception as e:
            print("Error: set value of the threshold in the plot " +
                  str(type(e)))
            print("Error: set value of the threshold in the plot "
                  + str(e))

    def set_params(self, enable, polarity, delay, threshold):
        self.set_active(enable)
        self.set_delay(delay)
        self.set_polarity(polarity)
        self.set_threshold(threshold)

    def __del__(self):
        self.button.deleteLater()
        self.polarity_menu.deleteLater()
        self.delay_box.deleteLater()
        self.threshold_box.deleteLater()


class ExtTriggerProperties(TriggerProperties):
    def __init__(self, unique_ADC_name, ADC_idx, trig_set_layout, zmq_rpc,
                 plot, GUI, GUI_name):
        super().__init__(unique_ADC_name, ADC_idx, trig_set_layout, zmq_rpc,
                         plot, GUI, GUI_name, 'external')


class IntTriggerProperties(TriggerProperties):
    def __init__(self, unique_ADC_name, ADC_idx, trig_set_layout, zmq_rpc,
                 plot, GUI, GUI_name):
        super().__init__(unique_ADC_name, ADC_idx, trig_set_layout, zmq_rpc,
                         plot, GUI, GUI_name, 'internal')
        self.trig_set_layout.addWidget(self.threshold_box)


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
        if(self.trigger_closure.trigger_type == type):
            pass
        else:
            self.trigger_closure.trigger_type = type
            self.trigger_closure.set_menu()
            self.trigger_closure.update_triggers()


class TriggersMenu(QMenuBar):

    def __init__(self, trigger_closure, GUI_trigger_idx):
        super().__init__()
        self.GUI_trigger_idx = GUI_trigger_idx
        self.trigger_closure = trigger_closure
        self.ADCs = {}
        self.selected_ADC = None

    def update_triggers(self):
        pass

    def remove_trigger(self):
        self.trigger_closure.remove_trigger()

    def __del__(self):
        self.remove_trigger()


class IntTriggersMenu(TriggersMenu):

    def __init__(self, trigger_closure, GUI_trigger_idx, plot,
                 channels):
        super().__init__(trigger_closure, GUI_trigger_idx)
        self.ADCs_menu = self.addMenu("Select channel to trigger")
        self.plot = plot
        self.channels = channels
        self.actions = []

    def update_triggers(self):
        self.ADCs_menu.clear()
        none = self.ADCs_menu.addAction("Disconnect")
        none.triggered.connect(self.remove_trigger)
        for channel in self.channels:
            if channel.properties is not None:
                channel_disp = str(channel.channel_count + 1)
                chan = self.ADCs_menu.addAction("Channel: " + channel_disp)
                chan.triggered.connect(self.select_trigger)
                self.actions.append(chan)
        if self.trigger_closure.trigger_exists():
            self.add_trigger()
            """this is done in case the ADC connected to the channel on
            which I trigger changes """

    def select_trigger(self):
        str_trigg = self.sender().text()
        channel_disp = int(str_trigg.split()[1])
        self.GUI_channel_idx = channel_disp - 1
        self.add_trigger()

    def add_trigger(self):
        self.remove_trigger()
        selected_ADC = self.channels[self.GUI_channel_idx].properties.\
            unique_ADC_name
        chan_disp = str(self.GUI_channel_idx+1)
        self.ADCs_menu.setTitle("Channel " + chan_disp)
        """+1 is beacuse channels are indexed from 0, but displayed from 1"""
        if selected_ADC is not None:
            ADC_idx = self.channels[self.GUI_channel_idx].properties.idx
            self.trigger_closure.set_trigger_properties(selected_ADC, ADC_idx)
            self.plot.add_trigger(self.GUI_channel_idx)
            rpc = self.trigger_closure.zmq_rpc
            rpc.send_RPC('add_trigger', 'internal', selected_ADC, ADC_idx,
                         self.trigger_closure.GUI_name)


class ExtTriggersMenu(TriggersMenu):

    def __init__(self, trigger_closure, GUI_trigger_idx, adc_label):
        super().__init__(trigger_closure, GUI_trigger_idx)
        self.ADCs_menu = self.addMenu("Select external trigger")
        self.adc_label = adc_label

    def update_triggers(self):
        self.ADCs_menu.clear()
        none = self.ADCs_menu.addAction("None")
        none.triggered.connect(self.remove_trigger)
        for ADC_name in self.trigger_closure.available_ADCs:
            ADC = self.ADCs_menu.addAction(ADC_name)
            self.ADCs[ADC_name] = ADC
            ADC.triggered.connect(self.select_trigger)

    def remove_available_ADC(self, name):
        self.ADCs_menu.removeAction(self.ADCs[name].menuAction())

    def select_trigger(self):
        self.selected_ADC = self.sender().text()
        self.add_trigger()

    def add_trigger(self):
        self.remove_trigger()
        self.trigger_closure.set_trigger_properties(self.selected_ADC)
        display_name = self.selected_ADC.replace('._tcp.local.', '')
        self.adc_label.setText(display_name)
        rpc = self.trigger_closure
        rpc.zmq_rpc.send_RPC('add_trigger', 'external', selected_ADC, ADC_idx,
                             self.trigger_closure.GUI_name)


class TriggerInputsLayout(QVBoxLayout):

    def __init__(self, adc_label):
        super().__init__()
        self.adc_label = adc_label
        self.menu = None
        self.ADCs = {}
        self.trigger = None

    def set_menu(self, menu):
        if self.menu is not None:
            self.menu.deleteLater()
        self.menu = menu
        self.addWidget(self.menu)
        self.addWidget(self.adc_label)


class TriggerSettingsLayout(QVBoxLayout):

    def __init__(self, menu_type):
        super().__init__()
        self.menu = None
        self.menu_type = menu_type
        self.addWidget(self.menu_type)

    def set_menu(self, menu):
        if self.menu is not None:
            self.menu.deleteLater()
        self.menu = menu
        self.addWidget(self.menu)


class TriggerThreshold(Box):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, GUI):
        super().__init__(idx, unique_ADC_name, "Treshold mV")
        self.zmq_rpc = zmq_rpc
        self.unique_ADC_name = unique_ADC_name
        self.idx = idx
        self.GUI = GUI
        self.box.setMinimum(-5000)
        self.box.setMaximum(4999)

    def value_change(self):
        threshold = self.box.value()   # in mV
        self.zmq_rpc.send_RPC('set_ADC_parameter',
                              'internal_trigger_threshold', threshold,
                              self.unique_ADC_name, self.idx)
        self.GUI.update_GUI_params()


class TriggerEnableButton(Button):

    def __init__(self, idx, unique_ADC_name, zmq_rpc,
                 type, GUI):
        super().__init__("Enable", idx, unique_ADC_name)
        self.zmq_rpc = zmq_rpc
        self.type = type
        self.GUI = GUI

    def action(self):
        self.zmq_rpc.send_RPC('set_ADC_parameter',
                              self.type + '_trigger_enable',
                              not self.isChecked(), self.unique_ADC_name,
                              self.idx)
        self.GUI.update_GUI_params()


class TriggerPolarity(TriggerPolarity):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, type, GUI):
        super().__init__(idx, unique_ADC_name)
        self.zmq_rpc = zmq_rpc
        self.type = type
        self.GUI = GUI

    def action(self):
        polarity_str = self.sender().text()
        polarity = int(polarity_str)
        self.zmq_rpc.send_RPC('set_ADC_parameter',
                              self.type + '_trigger_polarity', polarity,
                              self.unique_ADC_name, self.idx)
        self.GUI.update_GUI_params()


class TriggerDelay(Box):

    def __init__(self, idx, unique_ADC_name, zmq_rpc, type, GUI):
        super().__init__(idx, unique_ADC_name, "Delay")
        self.zmq_rpc = zmq_rpc
        self.type = type
        self.GUI = GUI
        self.box.setMinimum(0)
        self.box.setMaximum(65535)

    def value_change(self):
        delay = self.box.value()
        self.zmq_rpc.send_RPC('set_ADC_parameter',
                              self.type + '_trigger_delay', delay,
                              self.unique_ADC_name, self.idx)
        self.GUI.update_GUI_params()
