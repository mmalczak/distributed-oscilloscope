from ADC import ADC
from conversion import threshold_raw_to_mV
from timestamp_operations import tic_difference
from timestamp_operations import check_if_equal
from timestamp_operations import check_if_greater
import logging
import time
import sys
sys.path.append('../')
from general.publisher import Publisher
logger = logging.getLogger(__name__)


class HorizontalSettingsError(Exception):
    def __str__(self):
        return "Presamples or postsampls not equal in the ADCs"


class GUI():

    def __init__(self, name, GUI_addr, GUI_port):
        self.name = name
        self.__channels = {}
        self.__trigger = None
        self.__ADCs_used = []
        self.__GUI_addr = GUI_addr
        self.__GUI_port = GUI_port
        self.__run = False
        self.__GUI_publisher = Publisher(self.__GUI_addr, self.__GUI_port)

    """TODO number of channels shouldn't be sent here"""
    def register_ADC(self, unique_ADC_name, number_of_channels):
        message = {'function_name': 'register_ADC',
                   'args': [unique_ADC_name, number_of_channels]}
        self.__GUI_publisher.send_message(message)

    def unregister_ADC(self, unique_ADC_name):
        message = {'function_name': 'unregister_ADC',
                   'args': [unique_ADC_name]}
        self.__GUI_publisher.send_message(message)
        channels_to_delete = []
        for channel_idx, channel in self.__channels.items():
            if channel.ADC.unique_ADC_name == unique_ADC_name:
                channels_to_delete.append(channel_idx)
        for channel_idx in channels_to_delete:
            self.remove_channel(channel_idx)
        if self.__trigger:
            self.remove_trigger()


    def contains_ADC(self, unique_ADC_name):
        for ADC in self.__ADCs_used:
            if unique_ADC_name == ADC.unique_ADC_name:
                return True
        return False

    def add_channel(self, GUI_channel_idx, ADC, ADC_channel_idx):
        def set_horizontal_setting_when_add_channel(self):
            ADC = self.__ADCs_used[0]
            acq_conf = ADC.get_acq_conf()
            presamples = acq_conf.presamples
            postsamples = acq_conf.postsamples
            self.set_pre_post_samples(presamples, postsamples)

        ADC.add_used_channel(ADC_channel_idx)
        channel = ADC.get_channel(ADC_channel_idx)
        self.__channels[GUI_channel_idx] = channel
        self.__update_ADCs_used()
        set_horizontal_setting_when_add_channel(self)

    def add_trigger(self, type, ADC, ADC_trigger_idx):
        trigger = None
        if type == 'internal':   # consider dictionary
            trigger = ADC.get_internal_trigger(ADC_trigger_idx)
        else:
            trigger = ADC.get_external_trigger(ADC_trigger_idx)
        ADC.set_is_WRTD_master(True, type, ADC_trigger_idx)
        self.__trigger = trigger
        self.__update_ADCs_used()

    def remove_channel(self, GUI_channel_idx):
        self.__channels[GUI_channel_idx].ADC.remove_GUI()
        del self.__channels[GUI_channel_idx]
        self.__update_ADCs_used()

    def remove_trigger(self):
        ADC = self.__trigger.ADC

        ADC.set_is_WRTD_master(False)
        self.__trigger = None
        ADC.remove_GUI()
        self.__update_ADCs_used()

    def __update_ADCs_used(self):
        self.__ADCs_used = []
        for channel_idx, channel in self.__channels.items():
            if not(channel.ADC in self.__ADCs_used):
                self.__ADCs_used.append(channel.ADC)
                channel.ADC.set_GUI(self)
                """here I set the GUI in the ADC, it is removed in methods
                remove_channel/remove_trigger"""

    def set_pre_post_samples(self, presamples, postsamples):
        for ADC in self.__ADCs_used:
            ADC.set_ADC_parameter('presamples', presamples)
        for ADC in self.__ADCs_used:
            ADC.set_ADC_parameter('postsamples', postsamples)
        self.__check_horizontal_settings()

    def run_acquisition(self, run):
        self.__run = run
        self.run_acquisition_ADCs_used(run)

    def run_acquisition_ADCs_used(self, run):
        if self.__trigger is not None:
            for ADC in self.__ADCs_used:
                if(not ADC.get_is_WRTD_master()):
                    ADC.run_acquisition(run)
            self.__trigger.ADC.run_acquisition(run)
            """This is the WRTD master"""
        else:
            logger.info("No trigger selected")



    def configure_acquisition_ADCs_used(self):
        if self.__trigger is not None:
            for ADC in self.__ADCs_used:
                if(not ADC.get_is_WRTD_master()):
                    ADC.configure_acquisition()
            self.__trigger.ADC.configure_acquisition()
            """This is the WRTD master"""
        else:
            logger.info("No trigger selected")

    def stop_acquisition_ADCs_used(self):
        for ADC in self.__ADCs_used:
            ADC.stop_acquisition()
        for channel_idx, channel in self.__channels.items():
            channel.timestamp_pre_post_data = []



    def __all_data_aligned(self, max_timestamp):
        for channel_idx, channel in self.__channels.items():
            timestamp = channel.timestamp_pre_post_data[0]['timestamp']
            if(not check_if_equal(max_timestamp, timestamp, 50)):
                return False
        return True

    def __remove_old_data(self, max_timestamp):
        for channel_idx, channel in self.__channels.items():
            timestamp = channel.timestamp_pre_post_data[0]['timestamp']
            if(not check_if_equal(max_timestamp, timestamp, 50)):
                channel.timestamp_pre_post_data.pop(0)

    def __find_max(self):
        max_timestamp = [0, 0]
        for channel_idx, channel in self.__channels.items():
            timestamp = channel.timestamp_pre_post_data[0]['timestamp']
            if check_if_greater(timestamp, max_timestamp):
                max_timestamp = timestamp
        return max_timestamp

    def __check_if_data_exists(self):
        for channel_idx, channel in self.__channels.items():
            try:
                channel.timestamp_pre_post_data[0]
            except IndexError:
                return False
        return True

    def if_ready_send_data(self):
        if not self.__check_if_data_exists():
            return
        max_timestamp = self.__find_max()
        while(not self.__all_data_aligned(max_timestamp)):
            max_timestamp = self.__find_max()
            self.__remove_old_data(max_timestamp)
            if not self.__check_if_data_exists():
                return
        """Checks if the data is aligned in time, if there is any sample not
        aligned, smalles then the others, it is removed"""


        data = {}
        pre_post_samples = {}
        timestamps = []
        offsets = {}
        for channel_idx, channel in self.__channels.items():
            timestamp_pre_post_data = channel.timestamp_pre_post_data[0]
            data[channel_idx] = timestamp_pre_post_data['data_channel']
            timestamps.append(timestamp_pre_post_data['timestamp'])

            tic_diff = tic_difference(timestamp_pre_post_data['timestamp'],
                                      timestamps[0])
            offsets[channel_idx] = int(tic_diff)
            pre_post = timestamp_pre_post_data['pre_post']
            pre_post_samples[channel_idx] = [pre_post['presamples'],
                                             pre_post['postsamples']]
        for channel_idx, channel in self.__channels.items():
            """seperate loop is necessary in case th euser wants to display
            the same channel twice"""
            channel.timestamp_pre_post_data.pop(0)

        data = {'function_name': 'update_data',
                'args': [data, pre_post_samples, offsets]}
        self.__GUI_publisher.send_message(data)
        """TODO make sure that the data rate is not too big for plot"""

    def __check_horizontal_settings(self):
        if self.__ADCs_used:
            ADC0 = self.__ADCs_used[0]
            acq_conf = ADC0.get_acq_conf()
            presamples = acq_conf.presamples
            postsamples = acq_conf.postsamples
            for ADC in self.__ADCs_used:
                acq_conf = ADC.get_acq_conf()
                if (presamples != acq_conf.presamples) or\
                   (postsamples != acq_conf.postsamples):
                    raise HorizontalSettingsError

    def get_horiz_settings_copy(self):
        if self.__ADCs_used:
            ADC0 = self.__ADCs_used[0]
            acq_conf = ADC0.get_acq_conf()
            presamples = acq_conf.presamples
            postsamples = acq_conf.postsamples
            horizontal_params = {'presamples': presamples,
                                 'postsamples': postsamples}
            return horizontal_params
        else:
            logger.warning("No ADC used to retrieve the horizontal params")

    def get_channels_copy(self):
        GUI_channels_params = {}
        for channel_idx, channel in self.__channels.items():
            channel_params = {'active': channel.active,
                              'range': channel.range,
                              'termination': channel.termination,
                              'offset': channel.offset,
                              'ADC_channel_idx': channel.ADC_channel_idx}
            GUI_channels_params[channel_idx] = channel_params
        return GUI_channels_params

    def get_trigger_copy(self):
        trigger = self.__trigger
        if(trigger is None):
            logger.warning("No trigger available - trigger settings None")
            return
        threshold = None
        if trigger.type == 'internal':
            ADC = trigger.ADC
            threshold = threshold_raw_to_mV(trigger.threshold, ADC,
                                            trigger.ADC_trigger_idx)
        else:
            threshold = 'not_available'
        trigger_params = {'enable': trigger.enable,
                          'polarity': trigger.polarity,
                          'delay': trigger.delay,
                          'threshold': threshold}
        return trigger_params

    def get_GUI_settings(self):
        GUI_settings = {'channels': self.get_channels_copy(),
                        'trigger': self.get_trigger_copy(),
                        'horizontal_settings': self.get_horiz_settings_copy()}
        return GUI_settings
