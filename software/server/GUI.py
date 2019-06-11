from ADC import *
from conversion import *
from timestamp_operations import *
import logging
logger = logging.getLogger(__name__)


class HorizontalSettingsError(Exception):
    def __str__(self):
        return "Presamples or postsampls not equal in the ADCs"


def stop_and_retrieve_acquisition(func):
    def wrapper(self, *args, **kwargs):
        self.stop_acquisition_ADCs_used()
        func(self, *args, **kwargs)
        self.retrieve_acquisition_ADCs_used()
    return wrapper


class GUI():

    def __init__(self, available_ADCs, name, GUI_proxy_addr):
        self.name = name
        self.channels = {}
        self.trigger = None
        self.ADCs_used = []
        self.available_ADCs = available_ADCs
        self.GUI_proxy_addr = GUI_proxy_addr
        self.run = False

    def contains_ADC(self, unique_ADC_name):
        return unique_ADC_name in self.ADCs_used

    def remove_available_ADC(self, unique_ADC_name):
        for channel_idx, channel in self.channels.items():
            if channel.unique_ADC_name == unique_ADC_name:
                self.remove_channel(channel_idx)

    def add_channel(self, oscilloscope_channel_idx, unique_ADC_name,
                    ADC_channel_idx):
        def set_horizontal_setting_when_add_channel(self, new_ADC):
            ADC_name = self.ADCs_used[0]
            ADC = self.available_ADCs[ADC_name]
            presamples = ADC.acq_conf.presamples
            postsamples = ADC.acq_conf.postsamples
            self.set_presamples_ADC(presamples, new_ADC)
            self.set_postsamples_ADC(postsamples, new_ADC)

        channel = self.available_ADCs[unique_ADC_name].channels[ADC_channel_idx]
        self.channels[oscilloscope_channel_idx] = channel
        self.update_ADCs_used()
        set_horizontal_setting_when_add_channel(self, unique_ADC_name)

    def add_trigger(self, type, unique_ADC_name, ADC_trigger_idx):
        trigger = None
        ADC = self.available_ADCs[unique_ADC_name]
        if type == 'internal':   # consider dictionary
            trigger = ADC.internal_triggers[ADC_trigger_idx]
        else:
            trigger = ADC.external_triggers[ADC_trigger_idx]
        self.trigger = trigger
        self.update_ADCs_used()

    def remove_channel(self, oscilloscope_channel_idx):
        del self.channels[oscilloscope_channel_idx]
        self.update_ADCs_used()

    def remove_trigger(self):
        self.trigger = None
        self.update_ADCs_used()

    def update_ADCs_used(self):
        self.ADCs_used = []
        for channel_idx, channel in self.channels.items():
            if not(channel.unique_ADC_name in self.ADCs_used):
                self.ADCs_used.append(channel.unique_ADC_name)

    def configure_acquisition_ADC(self, unique_ADC_name):
        channels = []
        for channel_idx, channel in self.channels.items():
            if(channel.unique_ADC_name == unique_ADC_name):
                channels.append(channel.ADC_channel_idx)
        channels.sort()
        zmq_rpc = self.available_ADCs[unique_ADC_name].zmq_rpc
        zmq_rpc.send_RPC('configure_acquisition_retrieve_and_send_data', 
                          channels)

    def set_presamples_ADC(self, value, unique_ADC_name):
        zmq_rpc = self.available_ADCs[unique_ADC_name].zmq_rpc
        zmq_rpc.send_RPC('set_adc_parameter', 'set_presamples', value)
        ADC = self.available_ADCs[unique_ADC_name]
        ADC.update_conf()

    def set_postsamples_ADC(self, value, unique_ADC_name):
        if value == 1:
            value = 2
        """By default the value of postsamples is, but the minimum value that
        could be written is 2.
        If I read the configuration after initialization and want to write it
        back, I cannot, so then instead of writing 1, I write 2"""
        zmq_rpc = self.available_ADCs[unique_ADC_name].zmq_rpc
        zmq_rpc.send_RPC('set_adc_parameter', 'set_postsamples', value)
        ADC = self.available_ADCs[unique_ADC_name]
        ADC.update_conf()

    #@stop_and_retrieve_acquisition
    def set_presamples(self, value):
        for ADC in self.ADCs_used:
            self.set_presamples_ADC(value, ADC)
        self.check_horizontal_settings()

    #@stop_and_retrieve_acquisition
    def set_postsamples(self, value):
        for ADC in self.ADCs_used:
            self.set_postsamples_ADC(value, ADC)
        self.check_horizontal_settings()

    def run_acquisition(self, run):
        self.run = run
        if run:
            self.configure_acquisition_ADCs_used()

    def configure_acquisition_ADCs_used(self):
        if self.trigger is not None:
            for unique_ADC_name in self.ADCs_used:
                if(unique_ADC_name != self.trigger.unique_ADC_name):
                    self.configure_acquisition_ADC(unique_ADC_name)
            self.configure_acquisition_ADC(self.trigger.unique_ADC_name)
        else:
            logger.info("No trigger selected")

    def stop_acquisition_ADCs_used(self):
        for unique_ADC_name in self.ADCs_used:
            zmq_rpc = self.available_ADCs[unique_ADC_name].zmq_rpc
            zmq_rpc.send_RPC('stop_acquisition')
        for channel_idx, channel in self.channels.items():
            channel.timestamp_and_data = None

    def retrieve_acquisition_ADCs_used(self):
        if(self.run):
            self.configure_acquisition_ADCs_used()

    def check_if_ready_and_send_data(self):
        """this function is called by the oscilloscope"""
        """TODo check if data is aligned"""

        for channel_idx, channel in self.channels.items():
            if (channel.timestamp_and_data is None):
                return
        data = {}
        pre_post_samples = {}
        timestamps = []
        offsets = {}
        for channel_idx, channel in self.channels.items():
            channel_idx = str(channel_idx)  # remove with XMLRPC
            ADC = self.available_ADCs[channel.unique_ADC_name]
            data[channel_idx] = channel.timestamp_and_data[1]
            timestamps.append(channel.timestamp_and_data[0])
            tic_diff = tic_difference(*channel.timestamp_and_data[0],
                                      *timestamps[0])
            offsets[channel_idx] = str(int(tic_diff))
            pre_post_samples[channel_idx] = [ADC.acq_conf.  presamples,
                                             ADC.acq_conf.postsamples]
            channel.timestamp_and_data = None
        proxy = get_proxy(self.GUI_proxy_addr)
        proxy.update_data(data, pre_post_samples, offsets)
        """TODO make sure that the data rate is not too big for plot"""
        if self.run:
            self.configure_acquisition_ADCs_used()

    def check_horizontal_settings(self):
        ADC0 = self.ADCs_used[0]
        ADC0 = self.available_ADCs[ADC0]
        presamples = ADC0.acq_conf.presamples
        postsamples = ADC0.acq_conf.postsamples
        for ADC in self.ADCs_used:
            ADC = self.available_ADCs[ADC]
            print(ADC.acq_conf.presamples)
            print(ADC.acq_conf.postsamples)
            if (presamples != ADC.acq_conf.presamples) or\
               (postsamples != ADC.acq_conf.postsamples):
                raise HorizontalSettingsError

    def get_horizontal_settings(self):
        if self.ADCs_used:
            ADC0 = self.ADCs_used[0]
            ADC0 = self.available_ADCs[ADC0]
            presamples = ADC0.acq_conf.presamples
            postsamples = ADC0.acq_conf.postsamples
            horizontal_params = {'presamples': presamples,
                                 'postsamples': postsamples}
            return horizontal_params
        else:
            logger.warning("No ADC used to retrieve the horizontal params")

    def get_channels(self):
        oscilloscope_channels_params = {}
        for channel_idx, channel in self.channels.items():
            channel_params = {'active': channel.active,
                              'range': channel.channel_range,
                              'termination': channel.termination,
                              'offset': channel.offset}
            oscilloscope_channels_params[channel_idx] = channel_params
        return oscilloscope_channels_params

    def get_trigger(self):
        trigger = self.trigger
        if(trigger is None):
            logger.warning("No trigger available - trigger settings None")
            return
        threshold = None
        if trigger.type == 'internal':
            threshold = threshold_raw_to_mV(trigger.threshold,
                                            trigger.unique_ADC_name,
                                            trigger.ADC_trigger_idx,
                                            self.available_ADCs)
        else:
            threshold = 'not_available'
        trigger_params = {'enable': trigger.enable,
                          'polarity': trigger.polarity,
                          'delay': trigger.delay,
                          'threshold': threshold}
        return trigger_params

    def get_GUI_settings(self):
        GUI_settings = {'channels': self.get_channels(),
                        'trigger': self.get_trigger(),
                        'horizontal_settings': self.get_horizontal_settings()}
        return GUI_settings
