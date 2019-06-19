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
        self.WRTD = WRTD(trtl)
        self.ADC = ADC_100m14b4cha_extended_API(pci_addr)
        self.WRTD_master = False
        self.trtl = trtl
        self.required_presamples = 0
        self.unique_ADC_name = unique_ADC_name
        for count in range(4):
            self.ADC.set_internal_trigger_enable(0, count)
        self.ADC.set_external_trigger_enable(0, 0)
        if(not self.WRTD_master):
            self.ADC.set_presamples(delay_samples)
        self.WRTD.add_rule_mult_src('dist_triggers', 5)
        self.WRTD.set_rule_mult_src('dist_triggers', 0, 'LC-I', 'LAN1', 5)

        self.WRTD.add_rule('receive_trigger')
        self.WRTD.set_rule('receive_trigger', 600e6, 'LAN1', 'LC-O1')

        self.WRTD.enable_rule('receive_trigger')
        self.WRTD.disable_rule_mult_src('dist_triggers', 5)

        self.ADC.set_number_of_shots(NSHOT)
        buf_size = self.get_buffer_size()
        self.ADC.set_buffer(buf_size)
        self.channels = None
        self.selector = None

        """Used to retrieve the acquisition when modyfing the parameters"""
        self.acquisition_configured = False

    def get_buffer_size(self):
        conf = self.get_current_adc_conf()
        acq_conf = conf['acq_conf']
        presamples = acq_conf['presamples']
        postsamples = acq_conf['postsamples']
        return presamples + postsamples

    def get_pre_post_samples(self):
        conf = self.get_current_adc_conf()
        acq_conf = conf['acq_conf']
        presamples = acq_conf['presamples']
        postsamples = acq_conf['postsamples']
        return {'presamples': presamples, 'postsamples': postsamples}


    def set_WRTD_master(self, WRTD_master):
        print(WRTD_master)
        self.WRTD_master = WRTD_master
        if(WRTD_master):
            self.ADC.set_presamples(self.required_presamples)
            buf_size = self.get_buffer_size()
            self.ADC.set_buffer(buf_size)
            self.WRTD.disable_rule('receive_trigger')
            self.WRTD.enable_rule_mult_src('dist_triggers', 5)

        else:
            self.ADC.set_presamples(self.required_presamples + delay_samples)
            buf_size = self.get_buffer_size()
            self.ADC.set_buffer(buf_size)
            self.WRTD.disable_rule_mult_src('dist_triggers', 5)
            self.WRTD.enable_rule('receive_trigger')

    def configure_adc_parameter(self, function_name, args):
        if(function_name == 'set_presamples' and self.WRTD_master is False):
            self.required_presamples = args[0]
            args[0] += delay_samples
        getattr(self.ADC, function_name)(*args)
        if(function_name == ('set_presamples' or 'set_postsamples')):
            buf_size = self.get_buffer_size()
            self.ADC.set_buffer(buf_size)

        if self.acquisition_configured:
            self.configure_acquisition(self.channels)

    def get_current_adc_conf(self):
        conf = self.ADC.current_config()
        conf['is_WRTD_master'] = self.WRTD_master
        if(not self.WRTD_master):
            conf['acq_conf']['presamples'] -= delay_samples
        return conf

    def stop_acquisition(self):
        self.ADC.acq_stop(0)
        try:
            self.selector.unregister(self)
        except KeyError:
            pass
        # TODO after adding logger log it

        self.acquisition_configured = False

    def configure_acquisition(self, channels):

        self.channels = channels
        self.ADC.stop_acquisition()

        self.ADC.start_acquisition()
        self.selector.register(self, zmq.POLLIN)

        self.acquisition_configured = True


    def fileno(self):
        return self.ADC.fileno()

    def retrieve_ADC_data(self, channels):
        try:
            self.ADC.fill_buf()
        except Exception as e:
            return [0, 0, 0]
            print(e)

        try:
            data = np.ctypeslib.as_array(self.ADC.buf_ptr.contents.data,
                                         (self.get_buffer_size(), 4))
        except Exception as e:
            print(e)
            return([0, 0, 0])

        data = np.transpose(data)
        data = data.tolist()
        data_dict = {}
        for channel in channels:
            data_dict[str(channel)] = data[channel]

        if(not self.WRTD_master):
            timestamp = self.ADC.get_timestamp(self.ADC.buf_ptr, delay_tics)
        else:
            timestamp = self.ADC.get_timestamp(self.ADC.buf_ptr, 0)
        self.ADC.acq_stop(0)
        pre_post_samples_dict = self.get_pre_post_samples()

        self.acquisition_configured = False

        return [timestamp, pre_post_samples_dict, data_dict]
