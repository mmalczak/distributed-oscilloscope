from proxy import *
from plot import *
from channels import *
from triggers import *
from horizontal_settings import *
from run_control import *
import numpy as np


class GUI_Class:

    def __init__(self, ui, GUI_name):
        self.numberOfADC = 0
        self.ui = ui
        self.available_ADCs = []
        self.GUI_name = GUI_name
        self.plot = PlotMine(ui)
        self.number_of_GUI_channels = 4
        """this information should be retrieved from the ADC"""
        self.number_of_GUI_triggers = 1
        self.channels = []
        self.triggers = []
        self.layouts = []
        self.server_proxy = Proxy()
        for count in range(self.number_of_GUI_triggers):
            self.triggers.append(TriggerClosure(self.ui.inputs_layout,
                                                self.server_proxy,
                                                self.plot,
                                                self.GUI_name, count,
                                                self.channels,
                                                self.available_ADCs))
        for count in range(self.number_of_GUI_channels):
            self.channels.append(ChannelClosure(self.ui.inputs_layout,
                                                self.server_proxy,
                                                self.plot,
                                                self.GUI_name, count,
                                                self.triggers[0].
                                                update_triggers))

        self.presamples = Presamples(self.server_proxy, self.GUI_name)
        self.postsamples = Postsamples(self.server_proxy, self.GUI_name)
        ui.horizontal_settings_layout.addWidget(self.presamples)
        ui.horizontal_settings_layout.addWidget(self.postsamples)

        self.single_acquisition = SingleAcquisitionButton(self.
                                                          server_proxy,
                                                          self.GUI_name)
        self.ui.run_control_layout.addWidget(self.single_acquisition)

        self.run_stop_acquisition = RunStopButton(self.server_proxy,
                                                  self.GUI_name)
        self.ui.run_control_layout.addWidget(self.run_stop_acquisition)

    def add_available_ADC(self, unique_ADC_name, number_of_channels):
        self.available_ADCs.append(unique_ADC_name)
        for count in range(0, self.number_of_GUI_channels):
            self.channels[count].add_available_ADC(unique_ADC_name,
                                                   number_of_channels)
        for count in range(0, self.number_of_GUI_triggers):
            self.triggers[count].menu.update_triggers()
        return True

    def remove_available_ADC(self, unique_ADC_name):
        self.available_ADCs.remove(unique_ADC_name)
        """TODO the same for the new layout"""
        for count in range(0, self.number_of_GUI_channels):
            self.channels[count].remove_available_ADC(unique_ADC_name)
        for count in range(0, self.number_of_GUI_triggers):
            self.triggers[count].remove_trigger()
            self.triggers[count].update_triggers()
        return True

    def update_data(self, data, pre_post_samples, offsets):
        for channel_idx_str, channel_data in data.items():
            [presamples, postsamples] =\
                pre_post_samples[channel_idx_str]
            offset = int(offsets[channel_idx_str])*4/5
            offset = int(offset)
            presamples = presamples + offset
            postsamples = postsamples - offset
            print('presamples: ' + str(presamples))
            print('postsamples: ' + str(postsamples))
            print('offsets: ' + str(offsets))
            axis = np.array(range(-presamples, postsamples))/100000000
            channel_idx_str = int(channel_idx_str)
            """to be removed with xmlrpc"""
            self.plot.curves[channel_idx_str].setData(axis,
                                                      channel_data,
                                                      connect="finite")

    def set_channel_params(self, channel_params):
        for GUI_channel_idx, channel_params in channel_params.items():
            GUI_channel_idx = int(GUI_channel_idx)
            """to be removed with xmlrpc"""
            channel_prop = self.channels[GUI_channel_idx].properties
            channel_prop.set_channel_params(channel_params['active'],
                                            channel_params['range'],
                                            channel_params['termination'],
                                            channel_params['offset'],
                                            channel_params['saturation'])

    def set_trigger_params(self, trigger_params):
        trig_prop = self.triggers[0].properties
        trig_prop.set_params(trigger_params['enable'],
                             trigger_params['polarity'],
                             trigger_params['delay'],
                             trigger_params['threshold'])

    def set_horizontal_params(self, horizontal_params):
        self.presamples.set_value(horizontal_params['presamples'])
        self.postsamples.set_value(horizontal_params['postsamples'])
