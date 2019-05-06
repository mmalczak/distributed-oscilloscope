from parent_classes import *
from PyQt5.QtWidgets import QVBoxLayout
from proxy import *


class TriggerClosure:

    def __init__(self, inputs_layout, server_proxy, plot, GUI_name,
                 GUI_trigger_idx, channels, available_ADCs):
        self.GUI_trigger_idx = GUI_trigger_idx
        self.menu_type = TriggerTypeMenu(self)
        self.layout = TriggerLayout(self.menu_type)
        self.plot = plot
        self.GUI_name = GUI_name
        inputs_layout.addLayout(self.layout)
        self.properties = None
        self.server_proxy = server_proxy
        self.trigger_type = 'internal'
        self.channels = channels
        self.available_ADCs = available_ADCs
        self.menu = None
        self.set_menu()

    def update_triggers(self):
        self.menu.update_triggers()
        try:
            if self.properties.unique_ADC_name not in self.available_ADCs:
                self.properties = None
        except:
            pass

    def set_menu(self):
        if(self.trigger_type == 'internal'):
            self.menu = IntTriggersMenu(self, self.GUI_trigger_idx,
                                        self.plot, self.channels)
        else:
            self.menu = ExtTriggersMenu(self, self.GUI_trigger_idx)
        self.layout.set_menu(self.menu)

    def remove_trigger(self):
        if self.trigger_exists():
            self.properties = None
            try:
                self.plot.remove_trigger()
            except Exception as e:
                print(e)
            proxy = get_proxy(self.server_proxy.proxy_addr)
            try:
                proxy.remove_trigger(self.GUI_name)
            except Exception as e:
                print(e)

    def set_trigger_properties(self, unique_ADC_name, idx=0):
        if(self.trigger_type == 'internal'):
            self.properties = IntTriggerProperties(unique_ADC_name, idx,
                                                   self.layout,
                                                   self.server_proxy,
                                                   self.plot,
                                                   self.GUI_name)
        else:
            self.properties = ExtTriggerProperties(unique_ADC_name, idx,
                                                   self.layout,
                                                   self.server_proxy,
                                                   self.plot,
                                                   self.GUI_name)

    def trigger_exists(self):
        if(self.properties is None):
            return False
        else:
            return True


class TriggerProperties():
    """would it be better instead of creating classes
    ExtTriggerProperties and IntTriggerProperties create and delete
    threshold trigger conditionally?"""

    def __init__(self, unique_ADC_name, ADC_idx, layout, server_proxy,
                 plot, GUI_name, type):
        self.ADC_idx = ADC_idx
        self.unique_ADC_name = unique_ADC_name
        self.layout = layout
        self.plot = plot

        if(type == 'internal'):
            name = 'IntTrigger '+str(ADC_idx)
        else:
            name = 'ExtTrigger '+str(ADC_idx)

        self.button = TriggerEnableButton(name, ADC_idx,
                                          unique_ADC_name, server_proxy,
                                          type)
        self.polarity_menu = TriggerPolarity(ADC_idx, unique_ADC_name,
                                             server_proxy, type)
        self.delay_box = TriggerDelay(ADC_idx, unique_ADC_name,
                                      server_proxy, type)
        self.threshold_box = TriggerThreshold(ADC_idx, unique_ADC_name,
                                              server_proxy)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.polarity_menu)
        self.layout.addWidget(self.delay_box)

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
    def __init__(self, unique_ADC_name, ADC_idx, layout, server_proxy,
                 plot, GUI_name):
        super().__init__(unique_ADC_name, ADC_idx, layout, server_proxy,
                         plot, GUI_name, 'external')


class IntTriggerProperties(TriggerProperties):
    def __init__(self, unique_ADC_name, ADC_idx, layout, server_proxy,
                 plot, GUI_name):
        super().__init__(unique_ADC_name, ADC_idx, layout, server_proxy,
                         plot, GUI_name, 'internal')
        self.layout.addWidget(self.threshold_box)


class TriggerTypeMenu(QMenuBar):

    def __init__(self, trigger_closure):
        super().__init__()
        self.trigger_closure = trigger_closure
        self.trig_menu = self.addMenu("Trigger Type")
        trig = self.trig_menu.addAction("Internal")
        trig.triggered.connect(self.select_type)
        trig = self.trig_menu.addAction("External")
        trig.triggered.connect(self.select_type)

    def select_type(self):
        type = self.sender().text()
        if type == 'Internal':
            type = 'internal'
        else:
            type = 'external'
        if(self.trigger_closure.trigger_type == type):
            pass
        else:
            self.trigger_closure.trigger_type = type
            self.trigger_closure.set_menu()
            self.trigger_closure.menu.update_triggers()


class TriggersMenu(QMenuBar):

    def __init__(self, trigger_closure, GUI_trigger_idx):
        super().__init__()
        self.GUI_trigger_idx = GUI_trigger_idx
        self.trigger_closure = trigger_closure
        self.ADCs_menu = self.addMenu("ADCs")
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
        self.plot = plot
        self.channels = channels
        self.actions = []

    def update_triggers(self):
        self.ADCs_menu.clear()
        none = self.ADCs_menu.addAction("None")
        none.triggered.connect(self.remove_trigger)
        for channel in self.channels:
            if channel.properties is not None:
                chan = self.ADCs_menu.addAction("Channel: " +
                                                str(channel.
                                                    channel_count))
                chan.triggered.connect(self.select_trigger)
                self.actions.append(chan)
        if self.trigger_closure.properties is not None:
            self.add_trigger()
            """this is done in case the ADC connected to the channel on
            which I trigger changes """

    def select_trigger(self):
        str_trigg = self.sender().text()
        self.GUI_channel_idx = int(str_trigg.split()[1])
        self.add_trigger()

    def add_trigger(self):
        self.remove_trigger()
        selected_ADC = self.channels[self.GUI_channel_idx].properties.\
            unique_ADC_name
        ADC_idx = self.channels[self.GUI_channel_idx].properties.idx
        self.trigger_closure.set_trigger_properties(selected_ADC,
                                                    ADC_idx)
        self.plot.add_trigger(self.GUI_channel_idx)
        proxy = get_proxy(self.trigger_closure.server_proxy.proxy_addr)
        proxy.add_trigger('internal', selected_ADC, ADC_idx,
                          self.trigger_closure.GUI_name)


class ExtTriggersMenu(TriggersMenu):

    def __init__(self, trigger_closure, GUI_trigger_idx):
        super().__init__(trigger_closure, GUI_trigger_idx)

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
        proxy = get_proxy(self.trigger_closure.server_proxy.proxy_addr)
        proxy.add_trigger('external', self.selected_ADC, 0,
                          self.trigger_closure.GUI_name)


class TriggerLayout(QVBoxLayout):

    def __init__(self, menu_type):
        super().__init__()
        self.menu = None
        self.menu_type = menu_type
        self.addWidget(self.menu_type)
        self.ADCs = {}
        self.trigger = None

    def set_menu(self, menu):
        if self.menu is not None:
            self.menu.deleteLater()
        self.menu = menu
        self.addWidget(self.menu)


class TriggerThreshold(Box):

    def __init__(self, idx, unique_ADC_name, server_proxy):
        super().__init__(idx, unique_ADC_name, "Treshold mV")
        self.server_proxy = server_proxy
        self.unique_ADC_name = unique_ADC_name
        self.idx = idx
        self.box.setMinimum(-5000)
        self.box.setMaximum(4999)

    def value_change(self):
        threshold = self.box.value()   # in mV
        proxy = get_proxy(self.server_proxy.proxy_addr)
        proxy.set_ADC_parameter('internal_trigger_threshold', threshold,
                                self.unique_ADC_name, self.idx)


class TriggerEnableButton(Button):

    def __init__(self, button_name, idx, unique_ADC_name, server_proxy,
                 type):
        super().__init__(button_name, idx, unique_ADC_name)
        self.server_proxy = server_proxy
        self.type = type

    def action(self):
        proxy = get_proxy(self.server_proxy.proxy_addr)
        proxy.set_ADC_parameter(self.type + '_trigger_enable',
                                not self.isChecked(),
                                self.unique_ADC_name, self.idx)


class TriggerPolarity(TriggerPolarity):

    def __init__(self, idx, unique_ADC_name, server_proxy, type):
        super().__init__(idx, unique_ADC_name)
        self.server_proxy = server_proxy
        self.type = type

    def action(self):
        polarity_str = self.sender().text()
        proxy = get_proxy(self.server_proxy.proxy_addr)
        proxy.set_ADC_parameter(self.type + '_trigger_polarity',
                                int(polarity_str), self.unique_ADC_name,
                                self.idx)


class TriggerDelay(Box):

    def __init__(self, idx, unique_ADC_name, server_proxy, type):
        super().__init__(idx, unique_ADC_name, "Delay")
        self.server_proxy = server_proxy
        self.type = type
        self.box.setMinimum(0)
        self.box.setMaximum(65535)

    def value_change(self):
        delay = self.box.value()
        proxy = get_proxy(self.server_proxy.proxy_addr)
        proxy.set_ADC_parameter(self.type + '_trigger_delay', delay,
                                self.unique_ADC_name, self.idx)
