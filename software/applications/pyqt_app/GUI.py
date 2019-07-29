from plot import *
from channels import ChannelClosure
from triggers import *
from horizontal_settings import *
from run_control import *
import numpy as np
from PyQt5.QtCore import pyqtSlot
import pickle
import logging
logger = logging.getLogger(__name__)
sys.path.append('../../')
from general import serialization
from timeit import default_timer as timer

SAMP_FREQ = 1e8

class GUI_Class:

    def __init__(self, ui, zmq_rpc, GUI_name):
        self.ui = ui
        self.available_ADCs = []
        self.GUI_name = GUI_name
        self.plot = PlotMine(ui)
        self.number_of_GUI_channels = 4
        self.number_of_GUI_triggers = 1
        self.channels = []
        self.triggers = []
        self.layouts = []
        self.zmq_rpc = zmq_rpc
        self.last_data_time = timer()

        for count in range(self.number_of_GUI_triggers):
            trig_clos = TriggerClosure(self.ui.trigger_inputs_layout,
                                       self.ui.triggers_settings_layout,
                                       self.zmq_rpc,
                                       self.plot,
                                       self.GUI_name,
                                       count,
                                       self.channels,
                                       self.available_ADCs,
                                       self)

            self.triggers.append(trig_clos)

        for count in range(self.number_of_GUI_channels):
            chan_clos = ChannelClosure(self.ui.channel_inputs_layout,
                                       self.ui.vertical_settings_layout,
                                       self.zmq_rpc,
                                       self.plot,
                                       self.GUI_name,
                                       count,
                                       self.triggers[0].\
                                               update_available_triggers_list,
                                       self)

            self.channels.append(chan_clos)

        self.acq_settings = AcquisitionSettings(self.zmq_rpc, self.GUI_name,
                                                self)
        ui.horizontal_settings_layout.addLayout(self.acq_settings)

        self.single_acquisition = SingleAcquisitionButton(self.zmq_rpc,
                                                          self.GUI_name)
        self.ui.run_control_layout.addWidget(self.single_acquisition)

        self.run_stop_acquisition = RunStopButton(self.zmq_rpc, self.GUI_name)
        self.ui.run_control_layout.addWidget(self.run_stop_acquisition)

    def register_ADC(self, unique_ADC_name, number_of_channels):
        self.available_ADCs.append(unique_ADC_name)
        for count in range(0, self.number_of_GUI_channels):
            self.channels[count].register_ADC(unique_ADC_name,
                                                   number_of_channels)
        for count in range(0, self.number_of_GUI_triggers):
            self.triggers[count].register_ADC(unique_ADC_name) 
        return True

    def set_ADC_unavailable(self, unique_ADC_name):
        for count in range(0, self.number_of_GUI_channels):
            self.channels[count].set_ADC_unavailable(unique_ADC_name)
        for count in range(0, self.number_of_GUI_triggers):
            self.triggers[count].set_ADC_unavailable(unique_ADC_name)

    def set_ADC_available(self, unique_ADC_name):
        for count in range(0, self.number_of_GUI_channels):
            self.channels[count].set_ADC_available(unique_ADC_name)
        for count in range(0, self.number_of_GUI_triggers):
            self.triggers[count].set_ADC_available(unique_ADC_name)

    def unregister_ADC(self, unique_ADC_name):
        self.available_ADCs.remove(unique_ADC_name)
        for count in range(0, self.number_of_GUI_channels):
            self.channels[count].unregister_ADC(unique_ADC_name, True)
        for count in range(0, self.number_of_GUI_triggers):
            #self.triggers[count].remove_trigger(True)
            self.triggers[count].unregister_ADC(unique_ADC_name)
            self.triggers[count].update_available_triggers_list()
        return True

    def update_data(self, data, pre_post_samples, offsets):
        curr_time = timer()
        time_diff = curr_time - self.last_data_time
        if(time_diff < 0.1):
            return
        self.last_data_time = curr_time
        for channel_idx, channel_data in data.items():
            [presamples, postsamples] = pre_post_samples[channel_idx]
            offset = offsets[channel_idx]*4/5
#            if(offset>10 and offset < 14):
#                offset = 12
#            presamples = presamples - offset
#            postsamples = postsamples + offset
            print('presamples: ' + str(presamples))
            print('postsamples: ' + str(postsamples))
            print('offsets: ' + str(offsets))
            axis = (np.array(range(-presamples, postsamples))+offset)/SAMP_FREQ
            """to be removed with xmlrpc"""
            self.plot.curves[channel_idx].setData(axis, channel_data)

    def set_channel_params(self, channel_params):
        for GUI_channel_idx, channel_params in channel_params.items():
            GUI_channel_idx = int(GUI_channel_idx)
            """to be removed with xmlrpc"""
            channel = self.channels[GUI_channel_idx]
            channel.set_channel_params(channel_params['range'],
                                       channel_params['termination'],
                                       channel_params['offset'])

    def set_trigger_params(self, trigger_params):
        trig= self.triggers[0]
        trig.set_params(trigger_params['enable'],
                        trigger_params['polarity'],
                        trigger_params['delay'],
                        trigger_params['threshold'])

    def set_horizontal_params(self, horizontal_params):
        self.acq_settings.set_params(horizontal_params['presamples'],
                                     horizontal_params['postsamples'])

    def update_GUI_params(self):
        GUI_settings = self.zmq_rpc.send_RPC('get_GUI_settings', self.GUI_name)
        self.set_channel_params(GUI_settings['channels'])
        if GUI_settings['trigger']:
            self.set_trigger_params(GUI_settings['trigger'])
        if GUI_settings['horizontal_settings']:
            self.set_horizontal_params(GUI_settings['horizontal_settings'])

    def socket_communication(self, data):
        data = serialization.deserialize(data)
        try:
            getattr(self, data['function_name'])(*data['args'])
        except AttributeError:
            logger.warning("Wrong function name (remote)")
