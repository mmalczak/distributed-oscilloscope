from WRTD import WRTD
from ADC_100m14b4cha import ADC_100m14b4cha_extended_API
import zmq
import numpy as np


delay_u = 600
delay_samples = delay_u * 100
delay_tics = delay_samples * 125 // 100

NSHOT = 1
NCHAN = 4


class DevicesAccess():

    def __init__(self, pci_addr, trtl, unique_ADC_name):
        self.__WRTD = WRTD(trtl)
        self.__ADC = ADC_100m14b4cha_extended_API(pci_addr)
        self.__WRTD_master = False
        self.__required_presamples = 0
        self.unique_ADC_name = unique_ADC_name
        for count in range(4):
            self.__ADC.set_internal_trigger_enable(0, count)
        self.__ADC.set_external_trigger_enable(0, 0)
        if(not self.__WRTD_master):
            self.__ADC.set_presamples(delay_samples)
        self.__WRTD.add_rule_mult_src('dist_triggers', 5)
        self.__WRTD.set_rule_mult_src('dist_triggers', 0, 'LC-I', 'LAN1', 5)

        self.__WRTD.add_rule('receive_trigger')
        self.__WRTD.set_rule('receive_trigger', 600e6, 'LAN1', 'LC-O1')

        self.__WRTD.enable_rule('receive_trigger')
        self.__WRTD.disable_rule_mult_src('dist_triggers', 5)

        self.__ADC.set_number_of_shots(NSHOT)
        buf_size = self.__get_required_buffer_size()
        self.__ADC.set_buffer(buf_size)
        self.__channels = None
        self.selector = None

        """Used to retrieve the acquisition when modyfing the parameters"""
        self.__acquisition_configured = False

    def __get_required_buffer_size(self):
        conf = self.get_current_adc_conf()
        acq_conf = conf['acq_conf']
        presamples = acq_conf['presamples']
        postsamples = acq_conf['postsamples']
        return presamples + postsamples

    def __get_pre_post_samples(self):
        conf = self.get_current_adc_conf()
        acq_conf = conf['acq_conf']
        presamples = acq_conf['presamples']
        postsamples = acq_conf['postsamples']
        return {'presamples': presamples, 'postsamples': postsamples}


    def set_WRTD_master(self, WRTD_master):
        for count in range(4):
            self.__ADC.set_internal_trigger_enable(0, count)
        self.__ADC.set_external_trigger_enable(0, 0)
        self.__WRTD_master = WRTD_master
        if(WRTD_master):
            self.__ADC.set_presamples(self.__required_presamples)
            buf_size = self.__get_required_buffer_size()
            self.__ADC.set_buffer(buf_size)
            self.__WRTD.disable_rule('receive_trigger')
            self.__WRTD.enable_rule_mult_src('dist_triggers', 5)

        else:
            self.__ADC.set_presamples(self.__required_presamples + delay_samples)
            buf_size = self.__get_required_buffer_size()
            self.__ADC.set_buffer(buf_size)
            self.__WRTD.disable_rule_mult_src('dist_triggers', 5)
            self.__WRTD.enable_rule('receive_trigger')

    def configure_adc_parameter(self, function_name, args):
        if(function_name == 'set_presamples' and self.__WRTD_master is False):
            self.__required_presamples = args[0]
            args[0] += delay_samples
        getattr(self.__ADC, function_name)(*args)
        if(function_name == ('set_presamples' or 'set_postsamples')):
            buf_size = self.__get_required_buffer_size()
            self.__ADC.set_buffer(buf_size)

        if self.__acquisition_configured:
            self.configure_acquisition(self.__channels)

    def get_current_adc_conf(self):
        conf = self.__ADC.current_config()
        conf['is_WRTD_master'] = self.__WRTD_master
        if(not self.__WRTD_master):
            conf['acq_conf']['presamples'] -= delay_samples
        return conf

    def stop_acquisition(self):
        self.__ADC.acq_stop(0)
        try:
            self.selector.unregister(self)
        except KeyError:
            pass
        # TODO after adding logger log it

        self.__acquisition_configured = False

    def configure_acquisition(self, channels):

        self.__channels = channels
        self.__ADC.stop_acquisition()

        self.__ADC.start_acquisition()
        self.selector.register(self, zmq.POLLIN)

        self.__acquisition_configured = True


    def fileno(self):
        return self.__ADC.fileno()

    def retrieve_ADC_data(self):
        try:
            self.__ADC.fill_buf()
        except Exception as e:
            return [0, 0, 0]
            print(e)

        try:
            data = np.ctypeslib.as_array(self.__ADC.buf_ptr.contents.data,
                                         (self.__get_required_buffer_size(), 4))
        except Exception as e:
            print(e)
            return([0, 0, 0])

        data = np.transpose(data)
        data = data.tolist()
        data_dict = {}
        for channel in self.__channels:
            data_dict[str(channel)] = data[channel]

        if(not self.__WRTD_master):
            timestamp = self.__ADC.get_timestamp(self.__ADC.buf_ptr, delay_tics)
        else:
            timestamp = self.__ADC.get_timestamp(self.__ADC.buf_ptr, 0)
        self.__ADC.acq_stop(0)
        pre_post_samples_dict = self.__get_pre_post_samples()

        self.__acquisition_configured = False

        return [timestamp, pre_post_samples_dict, data_dict]
