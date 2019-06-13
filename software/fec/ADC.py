import threading
import subprocess
import ctypes
from WRTD import *
import selectors
from ADC_100m14b4cha import *
import zmq

delay_u = 600
delay_samples = delay_u * 100
delay_tics = delay_samples * 125 // 100

NSHOT = 1
NCHAN = 4


class ADC_100m14b4cha_extended_API_WRTD(ADC_100m14b4cha_extended_API):

    def __init__(self, pci_addr, trtl, unique_ADC_name):
        super().__init__(pci_addr)
        self.buf_ptr = 0
        self.WRTD = WRTD(trtl)
        self.WRTD_master = False
        self.trtl = trtl
        self.required_presamples = 0
        self.unique_ADC_name = unique_ADC_name
        for count in range(4):
            self.set_internal_trigger_enable(count, 0)
        self.set_external_trigger_enable(0, 0)
        if(not self.WRTD_master):
            self.set_presamples(delay_samples)
        self.WRTD.add_rule_mult_src('dist_triggers', 5)
        self.WRTD.set_rule_mult_src('dist_triggers', 0, 'LC-I', 'LAN1', 5)

        self.WRTD.add_rule('receive_trigger')
        self.WRTD.set_rule('receive_trigger', 600e6, 'LAN1', 'LC-O1')

        self.WRTD.enable_rule('receive_trigger')
        self.WRTD.disable_rule_mult_src('dist_triggers', 5)

        self.set_number_of_shots(NSHOT)
        self.set_buffer()
        self.channels = None
        self.selector = None

    def set_WRTD_master(self, WRTD_master):
        print(WRTD_master)
        self.WRTD_master = WRTD_master
        if(WRTD_master):
            self.set_presamples(self.required_presamples)
            self.WRTD.disable_rule('receive_trigger')
            self.WRTD.enable_rule_mult_src('dist_triggers', 5)

        else:
            self.set_presamples(self.required_presamples + delay_samples)
            self.WRTD.disable_rule_mult_src('dist_triggers', 5)
            self.WRTD.enable_rule('receive_trigger')

    # overwrites method from ADC_specialized
    def configure_parameter(self, function_name, args):
        if(function_name == 'set_presamples' and self.WRTD_master is False):
            self.required_presamples = args[0]
            args[0] += delay_samples
        getattr(self, function_name)(*args)
        if(function_name == 'set_presamples' or
                function_name == 'set_postsamples'):
            self.set_buffer()

    # overwrites method from ADC_specialized
    def get_current_conf(self):
        conf = self.current_config()
        if(not self.WRTD_master):
            conf['acq_conf']['presamples'] -= delay_samples
        return conf

    # overwrites method from ADC_specialized
    def stop_acquisition(self):
        self.acq_stop(0)
        try:
            self.selector.unregister(self)
        except KeyError:
            pass
        #TODO after adding logger log it

    def poll(self):
        Selector = selectors.PollSelector
        try:
            with Selector() as selector:
                print(selector.register(self, selectors.EVENT_READ))
        finally:
            pass

    def configure_acquisition_retrieve_and_send_data(self, channels):

        self.channels = channels
        self.stop_acquisition()

        self.start_acquisition()
        self.selector.register(self, zmq.POLLIN)

    def retrieve_ADC_timestamp_and_data(self, channels):
        try:
            self.fill_buf()
        except Exception as e:
            return [0, 0]
            print(e)

        try:
            data = np.ctypeslib.as_array(
                    self.buf_ptr.contents.data,
                    (self.presamples+self.postsamples, 4))
        except Exception as e:
            return([0, 0])
            print(e)

        data = np.transpose(data)
        data = data.tolist()

        data_dict = {}
        for channel in channels:
            data_dict[str(channel)] = data[channel]

        if(not self.WRTD_master):
            timestamp = self.get_timestamp(self.buf_ptr, delay_tics)
        else:
            timestamp = self.get_timestamp(self.buf_ptr, 0)
        self.acq_stop(0)
        return [timestamp, data_dict]
