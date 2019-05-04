from ADC import *
from conversion import *
from timestamp_operations import *


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

    @stop_and_retrieve_acquisition
    def add_channel(self, oscilloscope_channel_idx, unique_ADC_name,
                    ADC_channel_idx):
        try:
            self.set_horizontal_setting_when_add_channel(
                    unique_ADC_name)
        except Exception as e:
            print(e)
        channel = self.available_ADCs[unique_ADC_name].channels[
                    ADC_channel_idx]
        self.channels[oscilloscope_channel_idx] = channel
        self.update_ADCs_used()
        self.update_conf(unique_ADC_name)

    @stop_and_retrieve_acquisition
    def add_trigger(self, type, unique_ADC_name, ADC_trigger_idx):
        trigger = None
        if type == 'internal':   # consider dictionary
            trigger = self.available_ADCs[unique_ADC_name].\
                        internal_triggers[ADC_trigger_idx]
        else:
            trigger = self.available_ADCs[unique_ADC_name].\
                        external_triggers[ADC_trigger_idx]
        self.trigger = trigger
        self.update_ADCs_used()
        self.update_conf(unique_ADC_name)

    @stop_and_retrieve_acquisition
    def remove_channel(self, oscilloscope_channel_idx):
        del self.channels[oscilloscope_channel_idx]
        self.update_ADCs_used()

    @stop_and_retrieve_acquisition
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
        proxy = get_proxy(self.available_ADCs[unique_ADC_name].
                          ADC_proxy_addr)
        proxy.configure_acquisition_async(channels)

    def set_horizontal_setting_when_add_channel(self, new_ADC):
        ADC = self.ADCs_used[0]
        ADC = self.available_ADCs[ADC]
        presamples = ADC.acq_conf.presamples
        postsamples = ADC.acq_conf.postsamples
        print('presamples: ' + str(presamples))
        print('postsamples: ' + str(postsamples))
        new_ADC = self.available_ADCs[new_ADC]
        self.set_presamples_ADC(presamples, ADC)
        self.set_postsamples_ADC(postsamples, ADC)

    def set_presamples_ADC(self, value, unique_ADC_name):
        ADC = self.available_ADCs[unique_ADC_name]
        proxy = get_proxy(ADC.ADC_proxy_addr)
        proxy.set_adc_parameter('set_presamples', value)
        self.update_conf(unique_ADC_name)

    def set_postsamples_ADC(self, value, unique_ADC_name):
        ADC = self.available_ADCs[unique_ADC_name]
        proxy = get_proxy(ADC.ADC_proxy_addr)
        proxy.set_adc_parameter('set_postsamples', value)
        self.update_conf(unique_ADC_name)

    @stop_and_retrieve_acquisition
    def set_presamples(self, value):
        for ADC in self.ADCs_used:
            self.set_presamples_ADC(value, ADC)
        self.check_horizontal_settings()

    @stop_and_retrieve_acquisition
    def set_postsamples(self, value):
        for ADC in self.ADCs_used:
            self.set_postsamples_ADC(value, ADC)
        self.check_horizontal_settings()

    def run_acquisition(self, run):
        self.run = run
        if run:
            self.configure_acquisition_ADCs_used()

    def configure_acquisition_ADCs_used(self):
        for unique_ADC_name in self.ADCs_used:
            if(unique_ADC_name != self.trigger.unique_ADC_name):
                self.configure_acquisition_ADC(unique_ADC_name)
        self.configure_acquisition_ADC(self.trigger.unique_ADC_name)

    def stop_acquisition_ADCs_used(self):
        for unique_ADC_name in self.ADCs_used:
            ADC = self.available_ADCs[unique_ADC_name]
            proxy = get_proxy(ADC.ADC_proxy_addr)
            proxy.stop_acquisition()
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

    def update_conf(self, unique_ADC_name):
        ADC = self.available_ADCs[unique_ADC_name]
        ADC.update_conf()
        self.update_channels()
        self.update_trigger()
        try:
            self.update_horizontal_settings()
        except IndexError:
            pass  # get this exception if no ADC is used at the moment

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

    def update_horizontal_settings(self):
        if self.ADCs_used:
            ADC0 = self.ADCs_used[0]
            ADC0 = self.available_ADCs[ADC0]
            presamples = ADC0.acq_conf.presamples
            postsamples = ADC0.acq_conf.postsamples
            horizontal_params = {'presamples': presamples,
                                 'postsamples': postsamples}
            try:
                get_proxy(self.GUI_proxy_addr).set_horizontal_params(
                                                    horizontal_params)
            except Exception as e:
                print('Exception = : ' + str(e))

    def update_channels(self):
        oscilloscope_channels_params = {}
        for channel_idx, channel in self.channels.items():
            channel_params = {'active': channel.active,
                              'range': channel.channel_range,
                              'termination': channel.termination,
                              'offset': channel.offset,
                              'saturation': channel.saturation}
            """converting to str because of xmlrpc bug"""
            channel_idx = str(channel_idx)  # remove with XMLRPC
            oscilloscope_channels_params[channel_idx] = channel_params
        try:
            proxy = get_proxy(self.GUI_proxy_addr)
            proxy.set_channel_params(oscilloscope_channels_params)
        except Exception as e:
            print('Exception = : ' + str(e))

    def update_trigger(self):
        trigger = self.trigger
        if(trigger is None):
            return
        threshold = None
        try:
            threshold = threshold_raw_to_mV(trigger.threshold,
                                            trigger.unique_ADC_name,
                                            trigger.ADC_trigger_idx,
                                            self.available_ADCs)
        except:
            threshold = 'not_available'
        trigger_params = {'enable': trigger.enable,
                          'polarity': trigger.polarity,
                          'delay': trigger.delay,
                          'threshold': threshold}
        try:
            proxy = get_proxy(self.GUI_proxy_addr)
            proxy.set_trigger_params(trigger_params)
        except Exception as e:
            print('Exception = : ' + str(e))
