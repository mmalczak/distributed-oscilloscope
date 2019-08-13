from .ADC import ADC
from .conversion import threshold_raw_to_mV
import logging
import time
from DistributedOscilloscope.utilities.publisher import Publisher
logger = logging.getLogger(__name__)


class HorizontalSettingsError(Exception):
    def __str__(self):
        return "Presamples or postsampls not equal in the ADCs"


class UserApplication():

    def __init__(self, name, user_app_addr, user_app_port, connection_manager):
        self.name = name
        self.__channels = {}
        self.__trigger = None
        self.__ADCs_used = []
        self.__user_app_addr = user_app_addr
        self.__user_app_port = user_app_port
        self.__run = False
        self.connection_manager = connection_manager
        self.__user_app_publisher = Publisher(self.__user_app_addr,
                                              self.__user_app_port)

    def remove_all(self):
        if self.__trigger:
            self.remove_trigger()
        for count in range(4):
            if count in self.__channels:
                self.remove_channel(count)

    """TODO number of channels shouldn't be sent here"""
    def register_ADC(self, unique_ADC_name, number_of_channels):
        message = {'function_name': 'register_ADC',
                   'args': [unique_ADC_name, number_of_channels]}
        self.__user_app_publisher.send_message(message)

    def unregister_ADC(self, unique_ADC_name):
        message = {'function_name': 'unregister_ADC',
                   'args': [unique_ADC_name]}
        self.__user_app_publisher.send_message(message)
        channels_to_delete = []
        for channel_idx, channel in self.__channels.items():
            if channel.ADC.unique_ADC_name == unique_ADC_name:
                channels_to_delete.append(channel_idx)
        for channel_idx in channels_to_delete:
            self.remove_channel(channel_idx)
        if self.__trigger:
            self.remove_trigger()

    def set_ADC_available(self, unique_ADC_name):
        message = {'function_name': 'set_ADC_available',
                   'args': [unique_ADC_name]}
        self.__user_app_publisher.send_message(message)

    def set_ADC_unavailable(self, unique_ADC_name):
        message = {'function_name': 'set_ADC_unavailable',
                   'args': [unique_ADC_name]}
        self.__user_app_publisher.send_message(message)

    def contains_ADC(self, unique_ADC_name):
        for ADC in self.__ADCs_used:
            if unique_ADC_name == ADC.unique_ADC_name:
                return True
        return False

    def add_channel(self, user_app_channel_idx, ADC, ADC_channel_idx):
        def set_horizontal_setting_when_add_channel(self):
            ADC = self.__ADCs_used[0]
            acq_conf = ADC.get_acq_conf()
            presamples = acq_conf.presamples
            postsamples = acq_conf.postsamples
            self.set_pre_post_samples(presamples, postsamples)

        ADC.add_used_channel(ADC_channel_idx)
        channel = ADC.get_channel(ADC_channel_idx)
        self.__channels[user_app_channel_idx] = channel
        self.__update_ADCs_used()
        set_horizontal_setting_when_add_channel(self)

    def add_trigger(self, type, ADC, ADC_trigger_idx):
        if self.__trigger:
            self.remove_trigger()
        trigger = None
        if type == 'internal':   # consider dictionary
            trigger = ADC.get_internal_trigger(ADC_trigger_idx)
        else:
            trigger = ADC.get_external_trigger(ADC_trigger_idx)
        ADC.set_is_WRTD_master(True, type, ADC_trigger_idx)
        self.__trigger = trigger
        self.__update_ADCs_used()

    def remove_channel(self, user_app_channel_idx):
        del self.__channels[user_app_channel_idx]
        self.__update_ADCs_used()

    def remove_trigger(self):
        ADC = self.__trigger.ADC

        ADC.set_is_WRTD_master(False)
        self.__trigger = None
        self.__update_ADCs_used()

    def __update_ADCs_used(self):
        pr_ADCs_used = self.__ADCs_used.copy()
        self.__ADCs_used = []
        for channel_idx, channel in self.__channels.items():
            if not(channel.ADC in self.__ADCs_used):
                self.__ADCs_used.append(channel.ADC)
        if self.__trigger:
            if self.__trigger.ADC:
                if not(self.__trigger.ADC in self.__ADCs_used):
                    self.__ADCs_used.append(self.__trigger.ADC)

        for ADC in self.__ADCs_used:
            if not ADC in pr_ADCs_used:
                ADC.set_user_app(self)
                ADC.is_available = False
                self.connection_manager.set_ADC_unavailable(ADC.unique_ADC_name,
                                                            self.name)
        for ADC in pr_ADCs_used:
            if not ADC in self.__ADCs_used:
                ADC.remove_user_app()
                ADC.is_available = True
                self.connection_manager.set_ADC_available(ADC.unique_ADC_name,
                                                          self.name)

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
            if(not self.check_if_equal(max_timestamp, timestamp, 1)):
                return False
        return True

    def __remove_old_data(self, max_timestamp):
        for channel_idx, channel in self.__channels.items():
            timestamp = channel.timestamp_pre_post_data[0]['timestamp']
            if(not self.check_if_equal(max_timestamp, timestamp, 1)):
                channel.timestamp_pre_post_data.pop(0)

    def __find_max(self):
        max_timestamp = [0, 0]
        for channel_idx, channel in self.__channels.items():
            timestamp = channel.timestamp_pre_post_data[0]['timestamp']
            if self.check_if_greater(timestamp, max_timestamp):
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
        """
        Checks if the data is aligned in time, if there is any sample not
        aligned, smaller then the others, it is removed
        """
        if not self.__check_if_data_exists():
            return
        max_timestamp = self.__find_max()
        while(not self.__all_data_aligned(max_timestamp)):
            max_timestamp = self.__find_max()
            self.__remove_old_data(max_timestamp)
            if not self.__check_if_data_exists():
                return


        data = {}
        pre_post_samples = {}
        timestamps = []
        offsets = {}
        for channel_idx, channel in self.__channels.items():
            timestamp_pre_post_data = channel.timestamp_pre_post_data[0]
            data[channel_idx] = timestamp_pre_post_data['data_channel']
            timestamps.append(timestamp_pre_post_data['timestamp'])

            tic_diff = self.tic_difference(timestamp_pre_post_data['timestamp'],
                                           timestamps[0])
            offsets[channel_idx] = int(tic_diff)
            pre_post = timestamp_pre_post_data['pre_post']
            pre_post_samples[channel_idx] = [pre_post['presamples'],
                                             pre_post['postsamples']]
        for channel_idx, channel in self.__channels.items():
            """seperate loop is necessary in case th euser wants to display
            the same channel twice"""
            if channel.timestamp_pre_post_data:
                channel.timestamp_pre_post_data.pop(0)

        data = {'function_name': 'update_data',
                'args': [data, pre_post_samples, offsets]}
        self.__user_app_publisher.send_message(data)
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
        user_app_channels_params = {}
        for channel_idx, channel in self.__channels.items():
            channel_params = {'active': channel.active,
                              'range': channel.range,
                              'termination': channel.termination,
                              'offset': channel.offset,
                              'ADC_channel_idx': channel.ADC_channel_idx}
            user_app_channels_params[channel_idx] = channel_params
        return user_app_channels_params

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

    def get_user_app_settings(self):
        user_app_settings = {'channels': self.get_channels_copy(),
                        'trigger': self.get_trigger_copy(),
                        'horizontal_settings': self.get_horiz_settings_copy()}
        return user_app_settings

    def tic_difference(self, timestamp_1, timestamp_2):
        [sec_1, tic_1] = timestamp_1
        [sec_2, tic_2] = timestamp_2

        sec_diff = sec_1 - sec_2
        tic_diff = tic_1 - tic_2
        tic_diff += sec_diff*125e6

        return tic_diff

    def check_if_equal(self, timestamp_1, timestamp_2, available_offset_tics):
        tic_diff = self.tic_difference(timestamp_1, timestamp_2)
        if(tic_diff <= available_offset_tics
           and tic_diff >= -available_offset_tics):
            return True
        return False

    def check_if_greater(self, timestamp_1, timestamp_2):
        [sec_1, tic_1] = timestamp_1
        [sec_2, tic_2] = timestamp_2

        if (sec_1 > sec_2) or ((sec_1 == sec_2) and (tic_1 > tic_2)):
            return True
        else:
            return False
