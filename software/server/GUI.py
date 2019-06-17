from ADC import ADC
from conversion import threshold_raw_to_mV
from timestamp_operations import check_if_not_max
from timestamp_operations import tic_difference
from timestamp_operations import check_if_equal
import logging
from publisher import Publisher
logger = logging.getLogger(__name__)

class HorizontalSettingsError(Exception):
    def __str__(self):
        return "Presamples or postsampls not equal in the ADCs"


class GUI():

    def __init__(self, osc, name, GUI_addr, GUI_port):
        self.name = name
        self.__channels = {}
        self.__trigger = None
        self.__ADCs_used = []
        self.__GUI_addr = GUI_addr
        self.__GUI_port = GUI_port
        self.__run = False
        self.__GUI_publisher = Publisher(self.__GUI_addr, self.__GUI_port)
        self.__osc = osc

    """TODO number of channels shouldn't be sent here"""
    def register_ADC(self, unique_ADC_name, number_of_channels):
        message = {'function_name': 'register_ADC',
                'args': [unique_ADC_name, number_of_channels]}
        self.__GUI_publisher.send_message(message)

    def unregister_ADC(self, unique_ADC_name):
        message = {'function_name': 'unregister_ADC', 'args': [unique_ADC_name]}
        self.__GUI_publisher.send_message(message)
        channels_to_delete = []
        for channel_idx, channel in self.channels.items():
            if channel.unique_ADC_name == unique_ADC_name:
                channels_to_delete.append(channel_idx)
        for channel_idx in channels_to_delete:
            self.remove_channel(channel_idx)


    def contains_ADC(self, unique_ADC_name):
        return unique_ADC_name in self.__ADCs_used

    def add_channel(self, oscilloscope_channel_idx, unique_ADC_name,
                    ADC_channel_idx):
        def set_horizontal_setting_when_add_channel(self, new_ADC):
            ADC_name = self.__ADCs_used[0]
            ADC = self.__osc.get_ADC(ADC_name)
            acq_conf = ADC.get_acq_conf()
            presamples = acq_conf.presamples
            postsamples = acq_conf.postsamples
            self.set_presamples_ADC(presamples, new_ADC)
            self.set_postsamples_ADC(postsamples, new_ADC)

        ADC = self.__osc.get_ADC(unique_ADC_name)
        channel = ADC.get_channel(ADC_channel_idx)
        self.__channels[oscilloscope_channel_idx] = channel
        self.update_ADCs_used()
        set_horizontal_setting_when_add_channel(self, unique_ADC_name)

    def add_trigger(self, type, unique_ADC_name, ADC_trigger_idx):
        trigger = None
        ADC = self.__osc.get_ADC(unique_ADC_name)
        if type == 'internal':   # consider dictionary
            trigger = ADC.get_internal_trigger(ADC_trigger_idx)
        else:
            trigger = ADC.get_external_trigger(ADC_trigger_idx)
        self.__trigger = trigger
        self.update_ADCs_used()

    def remove_channel(self, oscilloscope_channel_idx):
        del self.__channels[oscilloscope_channel_idx]
        self.update_ADCs_used()

    def remove_trigger(self):
        self.__trigger = None
        self.update_ADCs_used()

    def update_ADCs_used(self):
        self.__ADCs_used = []
        for channel_idx, channel in self.__channels.items():
            if not(channel.unique_ADC_name in self.__ADCs_used):
                self.__ADCs_used.append(channel.unique_ADC_name)

    def configure_acquisition_ADC(self, unique_ADC_name):
        channels = []
        for channel_idx, channel in self.__channels.items():
            if(channel.unique_ADC_name == unique_ADC_name):
                channels.append(channel.ADC_channel_idx)
        channels.sort()
        ADC = self.__osc.get_ADC(unique_ADC_name)
        zmq_rpc = ADC.zmq_rpc
        zmq_rpc.send_RPC('configure_acquisition', channels)

    def set_presamples_ADC(self, value, unique_ADC_name):
        ADC = self.__osc.get_ADC(unique_ADC_name)
        ADC.set_adc_parameter_remote('set_presamples', value)

        ADC.update_conf()

    def set_postsamples_ADC(self, value, unique_ADC_name):
        if value == 1:
            value = 2
        """By default the value of postsamples is, but the minimum value that
        could be written is 2.
        If I read the configuration after initialization and want to write it
        back, I cannot, so then instead of writing 1, I write 2"""
        ADC = self.__osc.get_ADC(unique_ADC_name)
        ADC.set_adc_parameter_remote('set_postsamples', value)

        ADC.update_conf()

    def set_presamples(self, value):
        for ADC in self.__ADCs_used:
            self.set_presamples_ADC(value, ADC)
        self.check_horizontal_settings()

    def set_postsamples(self, value):
        for ADC in self.__ADCs_used:
            self.set_postsamples_ADC(value, ADC)
        self.check_horizontal_settings()

    def run_acquisition(self, run):
        self.__run = run
        if run:
            self.configure_acquisition_ADCs_used()

    def configure_acquisition_ADCs_used(self):
        if self.__trigger is not None:
            for unique_ADC_name in self.__ADCs_used:
                if(unique_ADC_name != self.__trigger.unique_ADC_name):
                    self.configure_acquisition_ADC(unique_ADC_name)
            self.configure_acquisition_ADC(self.__trigger.unique_ADC_name)
        else:
            logger.info("No trigger selected")

    def stop_acquisition_ADCs_used(self):
        for unique_ADC_name in self.__ADCs_used:
            ADC = self.__osc.get_ADC(unique_ADC_name)
            zmq_rpc = ADC.zmq_rpc
            zmq_rpc.send_RPC('stop_acquisition')
        for channel_idx, channel in self.__channels.items():
            channel.timestamp_pre_post_data = None

    def check_if_ready_and_send_data(self):
        """this function is called by the oscilloscope"""
        """TODo check if data is aligned"""
        for channel_idx, channel in self.__channels.items():
            if (channel.timestamp_pre_post_data is None):
                return
        data = {}
        pre_post_samples = {}
        timestamps = []
        offsets = {}
        for channel_idx, channel in self.__channels.items():
            ADC = self.__osc.get_ADC(channel.unique_ADC_name)
            data[channel_idx] = channel.timestamp_pre_post_data['data_channel']
            timestamps.append(channel.timestamp_pre_post_data['timestamp'])

            tic_diff = tic_difference(*channel.timestamp_pre_post_data[
                                            'timestamp'], *timestamps[0])
            offsets[channel_idx] = str(int(tic_diff))
            pre_post = channel.timestamp_pre_post_data['pre_post']
            pre_post_samples[channel_idx] = [pre_post['presamples'],
                                             pre_post['postsamples']]
            channel.timestamp_pre_post_data = None
        data = {'function_name': 'update_data',
                'args': [data, pre_post_samples, offsets]}
        self.__GUI_publisher.send_message(data)
        """TODO make sure that the data rate is not too big for plot"""
        if self.__run:
            self.configure_acquisition_ADCs_used()

    def check_horizontal_settings(self):
        ADC0 = self.__ADCs_used[0]
        ADC0 = self.__osc.get_ADC(ADC0)
        acq_conf = ADC0.get_acq_conf()
        presamples = acq_conf.presamples
        postsamples = acq_conf.postsamples
        for ADC in self.__ADCs_used:
            acq_conf = ADC.get_acq_conf()
            ADC = self.__osc.get_ADC(ADC)
            if (presamples != acq_conf.presamples) or\
               (postsamples != acq_conf.postsamples):
                raise HorizontalSettingsError

    def get_horiz_settings_copy(self):
        if self.__ADCs_used:
            ADC0 = self.__ADCs_used[0]
            ADC0 = self.__osc.get_ADC(ADC0)
            acq_conf = ADC0.get_acq_conf()
            presamples = acq_conf.presamples
            postsamples = acq_conf.postsamples
            horizontal_params = {'presamples': presamples,
                                 'postsamples': postsamples}
            return horizontal_params
        else:
            logger.warning("No ADC used to retrieve the horizontal params")

    def get_channels_copy(self):
        oscilloscope_channels_params = {}
        for channel_idx, channel in self.__channels.items():
            channel_params = {'active': channel.active,
                              'range': channel.channel_range,
                              'termination': channel.termination,
                              'offset': channel.offset,
                              'ADC_channel_idx': channel.ADC_channel_idx}
            oscilloscope_channels_params[channel_idx] = channel_params
        return oscilloscope_channels_params

    def get_trigger_copy(self):
        trigger = self.__trigger
        if(trigger is None):
            logger.warning("No trigger available - trigger settings None")
            return
        threshold = None
        if trigger.type == 'internal':
            ADC = self.__osc.get_ADC(trigger.unique_ADC_name)
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

    def validate_data(self):
        """check if data from all ADCs is properly aligned"""
        max_timestamp = [0, 0]
        all_the_same = False
        max_offset = 300
        while(all_the_same is False):
            for ADC_name, ADC in self.ADCs.items():
                try:
                    timestamp = ADC.timestamp_pre_post_data['timestamp'][0]
                    print(ADC_name + str(timestamp))
                except Exception as e:
                    return False
                if((timestamp[0] > max_timestamp[0]) or
                   ((timestamp[0] == max_timestamp[0]) and
                   (timestamp[1] > max_timestamp[1]))):
                    max_timestamp = timestamp
                    max_timestamp_sec = max_timestamp[0]
                    max_timestamp_tic = max_timestamp[1]
            for ADC_name, ADC in self.ADCs.items():
                try:
                    timestamp = ADC.timestamp_pre_post_data['timestamp'][0]
                    timestamp_sec = timestamp[0]
                    timestamp_tic = timestamp[1]
                except Exception as e:
                    return False
                if(check_if_not_max(max_timestamp_sec, max_timestamp_tic,
                                    timestamp_sec, timestamp_tic, max_offset)):
                    ADC.timestamp_pre_post_data.pop(0)
            for ADC_name, ADC in self.ADCs.items():
                try:

                    timestamp = ADC.timestamp_pre_post_data['timestamp'][0]
                    timestamp_sec = timestamp[0]
                    timestamp_tic = timestamp[1]
                except Exception as e:
                    return False
                if(not check_if_equal(max_timestamp_sec, max_timestamp_tic,
                                      timestamp_sec, timestamp_tic,
                                      max_offset)):
                    all_the_same = False
                    break
                else:
                    """FIXME it was quick fix to include the information
                    abot the offset between the triggers now this
                    information is included in the data, as last sample"""
                    """FIXME offset calculated in ticks, the correction
                    applied in samples"""
                    offset = tic_difference(max_timestamp_sec,
                                            max_timestamp_tic,
                                            timestamp_sec, timestamp_tic)
                    for count in range(0, ADC.number_of_channels):
                        ADC.timestamp_pre_post_data['timestamp'][1][count].\
                                            append(offset)
                    all_the_same = True
        return True
