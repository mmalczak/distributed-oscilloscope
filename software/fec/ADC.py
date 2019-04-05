import threading
from adc_access import *
import subprocess
import ctypes
from proxy import *
from WRTD import *
import selectors

delay_u = 600
delay_samples = delay_u * 100
delay_tics = delay_samples * 125 // 100


NSHOT = 1
NCHAN = 4
 
class ADC():

    class ThreadADC(threading.Thread):
    
        def __init__(self, function, adc, *args):
            threading.Thread.__init__(self)
            self.function = function
            self.adc = adc
            self.args = args     
        def __del__(self):
            print("Thread DELETED")


        def run(self):
            self.function(self.adc, *self.args)
    
    def move_to_thread(func):
        def wrapper(self, *args, **kwargs):
            self.ThreadADC(func, self, *args).start()
        return wrapper
    
    def __init__(self, pci_addr, trtl, server_proxy, unique_ADC_name):
        self.adc_ptr = initialise_adc(pci_addr)
        self.buf_ptr = 0
        self.WRTD = WRTD(trtl)
        self.WRTD_master = False
        self.trtl = trtl
        self.required_presamples = 0
        self.server_proxy = server_proxy
        self.unique_ADC_name = unique_ADC_name
        for count in range(4):
            set_internal_trigger_enable(self.adc_ptr, count, 0)
        set_external_trigger_enable(self.adc_ptr, count, 0)
        if(not self.WRTD_master):
            set_presamples(self.adc_ptr, delay_samples)
        self.WRTD.add_rule_mult_src('dist_triggers', 5) 
        self.WRTD.set_rule_mult_src('dist_triggers', 0, 'ADCI', 'LAN1', 5) 

        self.WRTD.add_rule('receive_trigger') 
        self.WRTD.set_rule('receive_trigger', 600e6, 'LAN1', 'ADCO1') 

        self.WRTD.enable_rule('receive_trigger') 
        self.WRTD.disable_rule_mult_src('dist_triggers', 5) 

        set_number_of_shots(self.adc_ptr, NSHOT)
        self.set_buffer()
        self.channels = None
        self.selector = None
        self.adc_selector = None

    def __del__(self):
        self.remove_buffer()
        close_adc(self.adc_ptr)

    def set_WRTD_master(self, WRTD_master):
        print(WRTD_master)
        self.WRTD_master = WRTD_master
        if(WRTD_master):
            set_presamples(self.adc_ptr, self.required_presamples)
            self.WRTD.disable_rule('receive_trigger') 
            self.WRTD.enable_rule_mult_src('dist_triggers', 5) 

        else:
            set_presamples(self.adc_ptr, self.required_presamples + delay_samples)
            self.WRTD.disable_rule_mult_src('dist_triggers', 5) 
            self.WRTD.enable_rule('receive_trigger') 

    def configure_parameter(self, function_to_invoke, args):
        if(function_to_invoke == set_presamples and self.WRTD_master == False):
            self.required_presamples = args[0]
            args[0] += delay_samples
        function_to_invoke(self.adc_ptr, *args) 
        if(function_to_invoke == set_presamples or function_to_invoke == set_postsamples):
            self.set_buffer()


    def get_current_conf(self):
        conf =  current_config(self.adc_ptr)
        if(not self.WRTD_master):
            conf['acq_conf']['presamples'] -= delay_samples 
        return conf

    def set_buffer(self):
        adc_release_buffer(self.adc_ptr, self.buf_ptr, None)
        conf = self.get_current_conf()
        acq_conf = conf['acq_conf'] 
        self.presamples = acq_conf['presamples'] 
        self.postsamples = acq_conf['postsamples']
        self.buf_ptr = adc_request_buffer(self.adc_ptr, self.presamples + self.postsamples , None, 0)
        if(self.buf_ptr == 0): 
            print("Cannot allocate buffer")
            print(adc_strerror(ctypes.get_errno()))

    def remove_buffer(self):
        adc_release_buffer(self.adc_ptr, self.buf_ptr, None)
        self.buf_ptr = 0

    def stop_acquisition(self):
        err = adc_acq_stop(self.adc_ptr, 0)
        if(err!=0):
            print("Cannot stop pending acquisition")
            print(adc_strerror(ctypes.get_errno()))
            return 0 
        if self.adc_selector:
            self.selector.unregister(self)
            self.adc_selector = None

    def start_acquisition(self):
        tv = timeval()
        err = adc_acq_start(self.adc_ptr, ADC_F_FLUSH, byref(tv))
        if(err != 0): 
            print("Failed to start acq")
            print(adc_strerror(ctypes.get_errno()))
            return 0

    def fileno(self):
        return adc_zio_get_file_descriptor(self.adc_ptr)

    def poll(self):
        Selector = selectors.PollSelector
        try:        
                with Selector() as selector:
                    print(selector.register(self, selectors.EVENT_READ))# | selectors.EVENT_WRITE))
        finally:
            pass

    def fill_buffer(self):
            err = adc_fill_buffer(self.adc_ptr, self.buf_ptr, 0, None)
            if(err != 0):
                print("Failed to retrieve data")
                print(adc_strerror(ctypes.get_errno()))
                return [0, 0]


    def configure_acquisition_retrieve_and_send_data(self, channels):
        
        self.channels = channels
        self.stop_acquisition()

        self.start_acquisition()
        self.adc_selector = self.selector.register(self, selectors.EVENT_READ)

    def retrieve_ADC_timestamp_and_data(self, channels):
        try:
            self.fill_buffer()
        except Exception as e:
            return [0, 0]
            print(e)

        try:
            data = np.ctypeslib.as_array(self.buf_ptr.contents.data, (self.presamples+self.postsamples, 4))
        except Exception as e:
            return([0, 0])
            print(e)

        data = np.transpose(data)
        data = data.tolist()

        data_dict = {}
        for channel in channels:
            data_dict[str(channel)] = data[channel]
        
 
        if(not self.WRTD_master):
            timestamp = get_timestamp(self.buf_ptr, delay_tics)
        else:
            timestamp = get_timestamp(self.buf_ptr, 0)
        err = adc_acq_stop(self.adc_ptr, 0)
        if(err != 0): 
            print("Failed to stop acq")
            print(adc_strerror(ctypes.get_errno()))
        return [timestamp, data_dict] 
     
     

