from ctypes import *
import numpy as np
import errno
import os


class adc_conf(Structure) :
    __ADC_CONF_LEN = 64          # fixme what to do about it
    _fields_ = [("type", c_int),
               ("dev_type", c_uint),
               ("route_to", c_uint),
               ("flags", c_uint),
               ("mask", c_ulong),
               ("value", c_uint * __ADC_CONF_LEN)
              ]
    def __init__(self):
        memset(byref(self), 0, sizeof(adc_conf))
    



class adc_buf(Structure):
   _fields_ = [("data", POINTER(c_short)),
               ("metadata", c_void_p),
               ("samplesize", c_int),
               ("nsamples", c_int),
               ("dev", c_void_p),
               ("mapaddr", c_void_p),
               ("maplen", c_uint),
               ("flags", c_uint)
              ]


class timeval(Structure):
   _fields_ = [("sec", c_long),
               ("usec", c_long)
              ]

class adc_timestamp(Structure):
   _fields_ = [("secs", c_ulong),
               ("ticks", c_ulong),
               ("bins", c_ulong)
              ]



class ADC_Generic():
    ADC_F_USERMASK  = 0xffff0000 # < Flag mask -- low-bits are used
                            #   by lib-int.h 
    ADC_F_FLUSH     = 0x00010000 # < Flag used to flush the buffer
                            # (used by adc_open) 
    ADC_F_VERBOSE   = 0x00020000 # < Flag used to verbose on stdout/stderr
                            # (usable by any function)
    ADC_F_FIXUP     = 0x00400000 # < Flag used to fixup a buffer when
                                 # filling it (usable by adc_fill_buffer) 
    #Enumerate all supported boards
    #enum adc_supported_boards {
    FMCADC_100MS_4CH_14BIT              = 0    # It identifies the FMC ADC 100M 14Bit 4Channel 
    ADC_ZIOFAKE                         = 1    # It identifies a generic board that supports the ZIO framework 
    ADC_GENERICFAKE                     = 2    # It identifies a generic board for testing purpose 
    __ADC_SUPPORTED_BOARDS_LAST_INDEX   = 3    # It represents the the last index of enum. It can be useful for some sort of automation 
    
    # It describes the possible polarity values
    #enum adc_trigger_polarity 
    ADC_TRG_POL_POS                   = 0 # positive edge/slope 
    ADC_TRG_POL_NEG                   = 1  # negative edge/slope 
    
    #It describes the possible configuration option for an external trigger
    #If not specified, the meaning of a configuration option depends on
    #the board in use
    #
    #@todo we should have a generic definition and then the device-specific
    #      code dealing with the conversion
    #enum adc_configuration_trigger_ext 
    ADC_CONF_TRG_EXT_ENABLE             = 0    # It enable/disable the trigger 
    ADC_CONF_TRG_EXT_POLARITY           = 1    # It is used to apply the polarity to the external triggers 
    ADC_CONF_TRG_EXT_DELAY              = 2    # acquisition delay after trigger 
    __ADC_CONF_TRG_EXT_LAST_INDEX       = 3    # It represents the the last index of this enum. It can be useful for some sort of automation 
    
    #It describes the possible configuration option for a threshold trigger
    #If not specified, the meaning of a configuration option depends on
    #the board in use
    #
    #@todo we should have a generic definition and then the device-specific
    #      code dealing with the conversion
    #enum adc_configuration_trigger_thr {
    ADC_CONF_TRG_THR_ENABLE             = 0   # It enable (1) or disable (0) the trigger 
    ADC_CONF_TRG_THR_POLARITY           = 1   # It is used to apply the polarity to thethreshold triggers 
    ADC_CONF_TRG_THR_DELAY              = 2   # It defines the acquisition delay aftertrigger 
    ADC_CONF_TRG_THR_THRESHOLD          = 3   # The threshold value that triggersthe acquisition 
    ADC_CONF_TRG_THR_HYSTERESIS         = 4   # If defines the hysteresis associatedto the threshold value 
    __ADC_CONF_TRG_THR_LAST_INDEX       = 5   # It represents the the last indexof this enum. It can be useful forsome sort of automation 
    
    #It describes the possible configuration option for a time trigger
    #If not specified, the meaning of a configuration option depends on
    #the board in use
    #@todo we should have a generic definition and then the device-specific
    #      code dealing with the conversion
    #enum adc_configuration_trigger_tim {
    ADC_CONF_TRG_TIM_ENABLE             = 0   #It enable (1) or disable (0) the trigger 
    __ADC_CONF_TRG_TIM_LAST_INDEX       = 1   #It represents the the last index of this enum. It can be useful for some sort of automation 
    
    #This represents the list of configuration options for the acquisition
    #when using ``conf->type = ADC_CONF_TYPE_ACQ``
    #enum adc_configuration_acquisition {
    ADC_CONF_ACQ_N_SHOTS                = 0   #number of shots during the acquisition 
    ADC_CONF_ACQ_POST_SAMP              = 1   #number of samples after the trigger 
    ADC_CONF_ACQ_PRE_SAMP               = 2   #number of sample before the trigger  
    ADC_CONF_ACQ_UNDERSAMPLE            = 3   #Acquisition undersample factor 
    ADC_CONF_ACQ_FREQ_HZ                = 4   #Acquisition frequency 
    ADC_CONF_ACQ_N_BITS                 = 5   #Number of bit per sample 
    __ADC_CONF_ACQ_ATTRIBUTE_LAST_INDEX = 6   #It represents the the last index of this enum. It can be useful for some sort of automation 
    
    #This represents the list of configuration options for the channels
    #when using ``conf->type = ADC_CONF_TYPE_CHN``
    #If not specified, the meaning of a configuration option depends on
    #the board in use
    #@todo we should have a generic definition and then the device-specific
    #      code dealing with the conversion
    #enum adc_configuration_channel {
    ADC_CONF_CHN_RANGE                  = 0   # Volt range 
    ADC_CONF_CHN_TERMINATION            = 1   # channel Termination 
    ADC_CONF_CHN_OFFSET                 = 2   # signal offset 
    ADC_CONF_CHN_SATURATION             = 3   # saturation value 
    ADC_CONF_CHN_GAIN                   = 4   # signal gain 
    __ADC_CONF_CHN_ATTRIBUTE_LAST_INDEX = 5   # It represents the the last index of this enum. It can be useful for some sort of automation 
    
    #This represents the list of configuration options for the board status
    #when using ``conf->type = ADC_CONF_TYPE_BRD``
    #If not specified, the meaning of a configuration option depends on
    #the board in use
    #@todo we should have a generic definition and then the device-specific
    #      code dealing with the conversion
    #enum adc_configuration_board {
    ADC_CONF_BRD_STATUS                 = 0   # Board status 
    ADC_CONF_BRD_MAX_FREQ_HZ            = 1   # Maximum frequency in HZ 
    ADC_CONF_BRD_MIN_FREQ_HZ            = 2   # Minimum frequency in HZ 
    ADC_CONF_BRD_STATE_MACHINE_STATUS   = 3   # Acquisition state machine status 
    ADC_CONF_BRD_N_CHAN                 = 4   # Number of acquisition channel 
    ADC_CONF_BRD_N_TRG_EXT              = 5   # Number of external triggers 
    ADC_CONF_BRD_N_TRG_THR              = 6   # Number of threshold triggers 
    ADC_CONF_BRD_N_TRG_TIM              = 7   # Number of timer triggers 
    # TODO seconds, ticks and bins are bit -> High - low 
    ADC_CONF_UTC_TIMING_BASE_S          = 8   #Board internal time: seconds 
    ADC_CONF_UTC_TIMING_BASE_T          = 9   #Board internal time: coarsesub-seconds 
    ADC_CONF_UTC_TIMING_BASE_B          = 10  #Board internal time: finesub-seconds
    __ADC_CONF_BRD_ATTRIBUTE_LAST_INDEX = 11  #It represents the the last index of this enum. It can be useful for some sort of automation 
    				
    #It describes the possible configuration types
    #If not specified, the meaning of a configuration option depends on
    #the board in use
    #@todo we should have a generic definition and then the device-specific
    #      code dealing with the conversion
    #enum adc_configuration_type {
    ADC_CONF_TYPE_BRD          = 0   # Configuration for the board 
    ADC_CONF_TYPE_CHN          = 1   #Configuration for an acquisition channels 
    ADC_CONF_TYPE_ACQ          = 2   #Configuration for the acquisition 
    ADC_CONF_TYPE_CUS          = 3   #Custom configuration for board-specific options for any of the possible domain: board,channel, triggers. 
    ADC_CONF_TYPE_TRG_EXT      = 4   #Configuration for external triggers 
    ADC_CONF_TYPE_TRG_THR      = 5   #Configuration for threshold triggers 
    ADC_CONF_TYPE_TRG_TIM      = 6   #Configuration for time triggers 
    __ADC_CONF_TYPE_LAST_INDEX = 7   #It represents the the last index of this enum. It can be useful for some sort of automation 

       
    def __init_lib(self):
        
        self.__ADC_CONF_LEN = 64 # number of allocated items in each structure 
        

        self.libc = CDLL("libadc.so", use_errno=True)
        self.adc_print_version = self.libc.adc_print_version
        self.adc_print_version.restype = None
        self.adc_print_version.argtypes = None
        
        self.adc_init = self.libc.adc_init
        self.adc_init.restype = c_int
        self.adc_init.argtypes = None
        self.adc_init.errcheck = self.__errcheck_int
        
        self.adc_exit = self.libc.adc_exit
        self.adc_exit.restype = None
        self.adc_exit.argtypes = None
       
        self.adc_strerror = self.libc.adc_strerror
        self.adc_strerror.restype = c_char_p
        self.adc_strerror.argtypes = [c_int]
        self.adc_strerror.errcheck = self.__errcheck_pointer
      
        self.adc_get_driver_type = self.libc.adc_get_driver_type
        self.adc_get_driver_type.restype = c_char_p
        self.adc_get_driver_type.argtypes = [c_void_p]
     
        self.adc_open = self.libc.adc_open
        self.adc_open.restype = c_void_p
        self.adc_open.argtypes = [c_char_p, c_uint, c_ulong, c_uint, c_ulong]
        self.adc_open.errcheck = self.__errcheck_pointer
    
        self.adc_open_by_lun = self.libc.adc_open_by_lun
        self.adc_open_by_lun.restype = c_void_p
        self.adc_open_by_lun.argtypes = [c_char_p, c_int, c_ulong, c_uint, c_ulong]
        self.adc_open_by_lun.errcheck = self.__errcheck_pointer
   
        self.adc_request_buffer = self.libc.adc_request_buffer
        self.adc_request_buffer.restype = POINTER(adc_buf)
        self.adc_request_buffer.argtypes = [c_void_p, c_int, c_void_p, c_uint]
        self.adc_request_buffer.errcheck = self.__errcheck_pointer
  
        self.adc_set_conf = self.libc.adc_set_conf
        self.adc_set_conf.restype = None
        self.adc_set_conf.argtypes = [c_void_p, c_uint, c_uint]
 
        self.adc_set_conf_mask = self.libc.adc_set_conf_mask
        self.adc_set_conf_mask.restype = None
        self.adc_set_conf_mask.argtypes = [c_void_p, c_uint]

        self.adc_get_conf = self.libc.adc_get_conf
        self.adc_get_conf.restype = c_int
        self.adc_get_conf.argtypes = [c_void_p, c_uint, c_void_p]
        #self.adc_get_conf.argtypes = [c_void_p, c_uint, POINTER(c_uint)]
        self.adc_get_conf.errcheck = self.__errcheck_int
        
        self.adc_apply_config = self.libc.adc_apply_config
        self.adc_apply_config.restype = c_int
        self.adc_apply_config.argtypes = [c_void_p, c_uint, c_void_p]
        self.adc_apply_config.errcheck = self.__errcheck_int
       
        self.adc_acq_start = self.libc.adc_acq_start
        self.adc_acq_start.restype = c_int
        self.adc_acq_start.argtypes = [c_void_p, c_uint, c_void_p]
        self.adc_acq_start.errcheck = self.__errcheck_int
      
        self.adc_zio_get_file_descriptor = self.libc.adc_zio_get_file_descriptor
        self.adc_zio_get_file_descriptor.restype = c_int
        self.adc_zio_get_file_descriptor.argtypes = [c_void_p]
        self.adc_zio_get_file_descriptor.errcheck = self.__errcheck_int
     
        self.adc_acq_poll = self.libc.adc_acq_poll
        self.adc_acq_poll.restype = c_int
        self.adc_acq_poll.argtypes = [c_void_p, c_uint, c_void_p]
        self.adc_acq_poll.errcheck = self.__errcheck_int
    
        self.adc_fill_buffer = self.libc.adc_fill_buffer
        self.adc_fill_buffer.restype = c_int
        self.adc_fill_buffer.argtypes = [c_void_p, c_void_p, c_uint, c_void_p]
        self.adc_fill_buffer.errcheck = self.__errcheck_int
   
        self.adc_acq_stop = self.libc.adc_acq_stop 
        self.adc_acq_stop.restype = c_int
        self.adc_acq_stop.argtypes = [c_void_p, c_uint]
        self.adc_acq_stop.errcheck = self.__errcheck_int
  
        self.adc_tstamp_buffer = self.libc.adc_tstamp_buffer
        self.adc_tstamp_buffer.restype = POINTER(adc_timestamp)
        self.adc_tstamp_buffer.argtypes = [c_void_p, c_void_p]
        self.adc_tstamp_buffer.errcheck = self.__errcheck_pointer
 
        self.adc_release_buffer = self.libc.adc_release_buffer
        self.adc_release_buffer.restype = c_int
        self.adc_release_buffer.argtypes = [c_void_p, c_void_p, c_void_p]
        self.adc_release_buffer.errcheck = self.__errcheck_int

        self.adc_close = self.libc.adc_close
        self.adc_close.restype = c_int
        self.adc_close.argtypes = [c_void_p]
        self.adc_close.errcheck = self.__errcheck_int

        self.adc_trigger_fire = self.libc.adc_trigger_fire
        self.adc_trigger_fire.restype = c_int
        self.adc_trigger_fire.argtypes = [c_void_p]
        self.adc_trigger_fire.errcheck = self.__errcheck_int

        self.adc_has_trigger_fire = self.libc.adc_has_trigger_fire
        self.adc_has_trigger_fire.restype = c_int
        self.adc_has_trigger_fire.argtypes = [c_void_p]

        #this function doesn't have body
        #self.adc_reset_conf = self.libc.adc_reset_conf
        #self.adc_reset_conf.restype = c_int 
        #self.adc_reset_conf.argtypes = [c_void_p, c_uint, c_void_p]
        #self.adc_reset_conf.errcheck = self.__errcheck_int
        
        self.adc_retrieve_config = self.libc.adc_retrieve_config
        self.adc_retrieve_config.restype = c_int
        self.adc_retrieve_config.argtypes = [c_void_p, c_void_p]
        self.adc_retrieve_config.errcheck = self.__errcheck_int
      
        self.adc_get_capabilities = self.libc.adc_get_capabilities
        self.adc_get_capabilities.restype = c_ulong
        self.adc_get_capabilities.argtypes = [c_void_p, c_int] 
        self.adc_get_capabilities.errcheck = self.__errcheck_int
     
        self.adc_get_param = self.libc.adc_get_param
        self.adc_get_param.restype = c_int
        self.adc_get_param.argtypes = [c_void_p, c_char_p, c_char_p, c_void_p]
        self.adc_get_param.errcheck = self.__errcheck_int
    
        self.adc_set_param = self.libc.adc_set_param
        self.adc_set_param.restype = c_int
        self.adc_set_param.argtypes = [c_void_p, c_char_p, c_char_p, c_void_p]
        self.adc_set_param.errcheck = self.__errcheck_int
   
        self.adc_set_conf_mask_all = self.libc.adc_set_conf_mask_all
        self.adc_set_conf_mask_all.restype = None
        self.adc_set_conf_mask_all.argtypes = [c_void_p, c_void_p]

    def __errcheck_int(self, ret, func, args):
        """Generic error checker for functions returning 0 as success
        and -1 as error"""
        if ret < 0:
            raise OSError(get_errno(),
                          self.strerror(get_errno()), "")
        else:
            return ret

    def __errcheck_pointer(self, ret, func, args):
        """Generic error handler for functions returning pointers"""
        if ret is None:
            raise OSError(get_errno(),
                          self.strerror(get_errno()), "")
        else:
            return ret

    def print_version(self):
        self.adc_print_version()

    def __init__(self, pci_addr):
        self.__init_lib()
        self.adc_init()
        self.adc_ptr = self.open(b"fmc-adc-100m14b4cha", pci_addr, 0 , 0 , self.ADC_F_FLUSH)
        self.adc_conf = adc_conf()

    def __del__(self):
        self.close()
        self.exit()

    def exit(self):
        self.adc_exit()
    
    def strerror(self, errnum):
        return self.adc_strerror(errnum)
   
    def get_driver_type(self):
        return self.adc_get_driver_type(self.adc_ptr)
  
    def open(self, name, dev_id, totalsamples, nbuffer, flags):
        return self.adc_open(name, dev_id, totalsamples, nbuffer, flags)
 
    def open_by_lun(self, name, lun, totalsamples, nbuffer, flags):
        return self.adc_open_by_lun(name, lun, totalsamples, nbuffer, flags)
   
    def request_buffer(self, nsamples, alloc, flags):
        return self.adc_request_buffer(self.adc_ptr, nsamples, alloc, flags)

    def set_conf(self, conf_index, val):
        self.adc_set_conf(byref(self.adc_conf), conf_index, val)
 
    def set_conf_mask(self, conf_index):
        self.adc_set_conf_mask(byref(self.adc_conf), conf_index)

    def get_conf(self, conf_index, val):
        self.adc_get_conf(self.adc_conf, conf_index, val)

    def acq_start(self, flags, timeout):
        self.adc_acq_start(self.adc_ptr, flags, timeout)

# NON API
    def zio_get_file_descriptor(self):
        return self.adc_zio_get_file_descriptor(self.adc_ptr)

    def acq_poll(self, flags, timeout):
        self.adc_acq_poll(self.adc_ptr, flags, timeout)

    def fill_buffer(self, buf, flags, timeout):
        self.adc_fill_buffer(self.adc_ptr, buf, flags, timeout)
   
    def acq_stop(self, flags):
        self.adc_acq_stop(self.adc_ptr, flags)
  
    def tstamp_buffer(self, buf, ts):
        self.adc_tstamp_buffer(buf, ts)
     
    def release_buffer(self, buf, free):
        self.adc_release_buffer(self.adc_ptr, buf, free)

    def close(self):
        if not self.adc_ptr:
            self.adc_close(self.adc_ptr)
            self.adc_ptr = 0

    def trigger_fire(self):
        self.adc_trigger_fire(self.adc_ptr)

    def has_trigger_fire(self): 
        return self.adc_has_trigger_fire(self.adc_ptr)

    def apply_config(self, flags):
        self.adc_apply_config(self.adc_ptr, flags, byref(self.adc_conf))
        memset(byref(self.adc_conf), 0, sizeof(adc_conf))

    def retrieve_config(self): 
        self.adc_retrieve_config(self.adc_ptr, self.adc_conf)

    def get_capabilities(self, type):
        self.adc_get_capabilities(self.adc_ptr, type)

    def get_param(self, name, sptr, iptr): 
        self.adc_get_param(self.adc_ptr, name, sptr, iptr)

    def set_param(self, name, sptr, iptr): 
        self.adc_set_param(self.adc_ptr, name, sptr, iptr)
  
    def set_conf_mask_all(self):
        self.adc_set_conf_mask_all(byref(self.adc_conf), self.adc_ptr)


class ADC_Specialized(ADC_Generic):
    def __init__(self, pci_addr):
        super().__init__(pci_addr)
        self.init_adc_100m14b4cha_lib()
        self.buf_ptr = 0

    def init_adc_100m14b4cha_lib(self):
         ######################################################
         #adc_lib_100m14b4cha_wrapper.py
         ######################################################
         self.ADC_CONF_100M14B4CHA_CHN_RANGE_N = 3
         
         #List of known voltage ranges to be used with the configuration option
         #ADC_CONF_CHN_RANGE
         
         #enum adc_configuration_100m14b4cha_channel_range {
         self.ADC_CONF_100M14B4CHA_CHN_RANGE_OPEN_DRAIN   = 0
         self.ADC_CONF_100M14B4CHA_CHN_RANGE_100mV        = 0x23
         self.ADC_CONF_100M14B4CHA_CHN_RANGE_1V           = 0x11
         self.ADC_CONF_100M14B4CHA_CHN_RANGE_10V          = 0x45
         self.ADC_CONF_100M14B4CHA_CHN_RANGE_100mV_CAL    = 0x42
         self.ADC_CONF_100M14B4CHA_CHN_RANGE_1V_CAL       = 0x40
         self.ADC_CONF_100M14B4CHA_CHN_RANGE_10V_CAL      = 0x44
         
         
         #List of possible buffer types (options for ADC_CONF_100M14B4CHA_BUF_TYPE)
         
         #enum adc_100m14b4cha_buf_type {
         self.ADC_CONF_100M14B4CHA_BUF_KMALLOC    = 0     #< buffer type 'kmalloc' 
         self.ADC_CONF_100M14B4CHA_BUF_VMALLOC    = 1     #< buffer type 'vmalloc'
         
         
         #It describes the possible configuration parameters for the
         #FMCADC100M14B4CHA card (ADC_CONF_TYPE_CUS)
         
         #enum adc_configuration_100m14b4cha {
         self.ADC_CONF_100M14B4CHA_BUF_TYPE       = 0 # < the ZIO buffer type in use */
         self.ADC_CONF_100M14B4CHA_TRG_SW_EN      = 1 # < software trigger enable/disable */
         self.ADC_CONF_100M14B4CHA_ACQ_MSHOT_MAX  = 2 # < Maximum size for a single shot
                                                 # in multi-shot mode (in samples) */
         self.ADC_CONF_100M14B4CHA_BUF_SIZE_KB    = 3 # < it manually sets the buffer size but
                                                 # only for VMALLOC buffers */
         self.ADC_CONF_100M14B4CHA_TRG_ALT_EN     = 4 # < alternate trigger enable/disable */
         self.__ADC_CONF_100M14B4CHA_LAST_INDEX   = 5 # < It represents the the last index
                                                 # of this enum. It can be useful for
                                                 # some sort of automation */
          

    def __del__(self):
        super().__del__()
        self.remove_buffer()

    def remove_buffer(self):
        if not self.buf_ptr:
            self.adc_release_buffer(self.adc_ptr, self.buf_ptr, None)
            self.buf_ptr = 0
     
    def start_acquisition(self):
        tv = timeval()
        self.acq_start(self.ADC_F_FLUSH, byref(tv))

    def set_buffer(self):
        self.release_buffer(self.buf_ptr, None)
        conf = self.get_current_conf()
        acq_conf = conf['acq_conf'] 
        self.presamples = acq_conf['presamples'] 
        self.postsamples = acq_conf['postsamples']
        self.buf_ptr = self.request_buffer(self.presamples + self.postsamples , None, 0)

    def get_current_conf(self):
        conf =  self.current_config()
        return conf

    def stop_acquisition(self):
        self.acq_stop(0)

    def configure_parameter(self, function_name, args):
        getattr(self, function_name)(*args) 
        if(function_name == 'set_presamples' or function_name == 'set_postsamples'):
            self.set_buffer()

    def fill_buf(self):
            self.fill_buffer(self.buf_ptr, 0, None)

    def fileno(self):
        return self.zio_get_file_descriptor()

    def set_presamples(self, presamples):
       self.adc_conf.type = self.ADC_CONF_TYPE_ACQ
       self.set_conf(self.ADC_CONF_ACQ_PRE_SAMP, presamples)
       self.apply_config(0)
    
    def set_postsamples(self, postsamples):
       self.adc_conf.type = self.ADC_CONF_TYPE_ACQ
       self.set_conf(self.ADC_CONF_ACQ_POST_SAMP, postsamples)
       self.apply_config(0)
     
    def set_number_of_shots(self, n_shots):
       self.adc_conf.type = self.ADC_CONF_TYPE_ACQ
       self.set_conf(self.ADC_CONF_ACQ_N_SHOTS, n_shots)
       self.apply_config(0)
    
    def get_timestamp(self, buf_ptr, offset):
       ts = adc_timestamp()
       self.adc_tstamp_buffer(buf_ptr, byref(ts))
    #cannot send 32bit int using xmlrpc
       secs = np.ctypeslib.as_array(ts.secs, (1 ,1))
       ticks = np.ctypeslib.as_array(ts.ticks, (1 ,1))
       secs = np.asscalar(secs)
       ticks = np.asscalar(ticks)
       ticks = ticks - offset
    
       #need to compensate for FIFO depth
       if(ticks<16):
          secs = secs - 1
          ticks = ticks + 125000000-16
       else:
          ticks = ticks - 16
       print('secs = ' + str(secs) + ' ticks = ' + str(ticks))
       secs_low = secs &               0x0000000000ffffff
       secs_middle = (secs >> 24) &    0x0000000000ffffff
       secs_high = (secs >> 48) &      0x0000000000ffffff
       ticks_low = ticks &             0x0000000000ffffff
       ticks_middle = (ticks >> 24) &  0x0000000000ffffff
       ticks_high = (ticks >> 48) &    0x0000000000ffffff
       #print( (secs_high << 48 ) + (secs_middle << 24) + secs_low)
       timestamp = [secs_low, secs_middle, secs_high, ticks_low, ticks_middle, ticks_high]
       return timestamp 
    
    
    def set_channel_range(self, channel, channel_range):
       # possible values :
       # 100 mV     - 100
       # 1 V        - 1
       # 10V        - 10
       # open input - 0
       self.adc_conf.type = self.ADC_CONF_TYPE_CHN
       self.adc_conf.route_to = channel
       if(channel_range == 100):
          ch_range = self.ADC_CONF_100M14B4CHA_CHN_RANGE_100mV
       elif(channel_range == 1):
          ch_range = self.ADC_CONF_100M14B4CHA_CHN_RANGE_1V
       elif(channel_range == 10):
          ch_range = self.ADC_CONF_100M14B4CHA_CHN_RANGE_10V
       elif(channel_range == 0):
          ch_range = self.ADC_CONF_100M14B4CHA_CHN_RANGE_OPEN_DRAIN
       else:
          print("Wrong channel range")
    
       self.set_conf(self.ADC_CONF_CHN_RANGE, ch_range)
       self.apply_config(0)
    
    def set_channel_termination(self, channel, termination):
       self.adc_conf.type = self.ADC_CONF_TYPE_CHN
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_CHN_TERMINATION, termination)
       self.apply_config(0)
    
    
    def set_channel_offset(self, channel, offset):
       #value of offset given in uV
       self.adc_conf.type = self.ADC_CONF_TYPE_CHN
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_CHN_OFFSET, offset)
       self.apply_config(0)
    
    def set_channel_saturation(self, channel, saturation):
       self.adc_conf.type = self.ADC_CONF_TYPE_CHN
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_CHN_SATURATION, saturation)
       self.apply_config(0, byref(self.adc_conf))
    
    def set_channel_gain(self, channel, gain):
       self.adc_conf.type = self.ADC_CONF_TYPE_CHN
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_CHN_GAIN, gain)
       self.apply_config(0)
    
    def set_external_trigger_enable(self, channel, enable):
       self.adc_conf.type = self.ADC_CONF_TYPE_TRG_EXT 
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_TRG_EXT_ENABLE, enable)
       self.apply_config(0)
    
    def set_external_trigger_polarity(self, channel, polarity):
       self.adc_conf.type = self.ADC_CONF_TYPE_TRG_EXT 
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_TRG_EXT_POLARITY, polarity)
       self.apply_config(0)
    
    def set_external_trigger_delay(self, channel, delay):
       self.adc_conf.type = self.ADC_CONF_TYPE_TRG_EXT 
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_TRG_EXT_DELAY, delay)
       self.apply_config(0)
    
    def set_internal_trigger_enable(self, channel, enable):
       self.adc_conf.type = self.ADC_CONF_TYPE_TRG_THR 
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_TRG_THR_ENABLE, enable)
       self.apply_config(0)
    
    def set_internal_trigger_polarity(self, channel, polarity):
       self.adc_conf.type = self.ADC_CONF_TYPE_TRG_THR 
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_TRG_THR_POLARITY, polarity)
       self.apply_config(0)
    
    def set_internal_trigger_delay(self, channel, delay):
       self.adc_conf.type = self.ADC_CONF_TYPE_TRG_THR 
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_TRG_THR_DELAY, delay)
       self.apply_config(0)
    
    def set_internal_trigger_threshold(self, channel, threshold):
       self.adc_conf.type = self.ADC_CONF_TYPE_TRG_THR 
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_TRG_THR_THRESHOLD, threshold)
       self.apply_config(0)
    
    def set_internal_trigger_hysteresis(self, channel, hysteresis):
       self.adc_conf.type = self.ADC_CONF_TYPE_TRG_THR 
       self.adc_conf.route_to = channel
       self.set_conf(self.ADC_CONF_TRG_THR_HYSTERESIS, hysteresis)
       self.apply_config(0)
   
    def current_config_acq(self):
       n_shots = c_uint()
       presamples = c_uint()
       postsamples = c_uint()
       undersample = c_uint()
       freq = c_uint()
       n_bits = c_uint()
     
       self.adc_conf.type = self.ADC_CONF_TYPE_ACQ
    
       self.set_conf_mask(self.ADC_CONF_ACQ_N_SHOTS                )
       self.set_conf_mask(self.ADC_CONF_ACQ_POST_SAMP)
       self.set_conf_mask(self.ADC_CONF_ACQ_PRE_SAMP)
       self.set_conf_mask(self.ADC_CONF_ACQ_UNDERSAMPLE)
       self.set_conf_mask(self.ADC_CONF_ACQ_FREQ_HZ)
       self.set_conf_mask(self.ADC_CONF_ACQ_N_BITS)
       self.adc_retrieve_config(self.adc_ptr, byref(self.adc_conf))
       
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_ACQ_N_SHOTS, byref(n_shots))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_ACQ_POST_SAMP, byref(postsamples))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_ACQ_PRE_SAMP, byref(presamples))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_ACQ_UNDERSAMPLE, byref(undersample))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_ACQ_FREQ_HZ, byref(freq))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_ACQ_N_BITS, byref(n_bits))
       acq_conf = {'n_shots':n_shots.value, 'presamples':presamples.value, 'postsamples':postsamples.value, 
                'undersample':undersample.value, 'freq':freq.value, 'n_bits':n_bits.value}
   

       memset(byref(self.adc_conf), 0, sizeof(adc_conf))
       return acq_conf
    
    def current_config_channel(self, channel):
       channel_range= c_uint()
       termination = c_uint()
       offset = c_int()  # originally it is uint
       saturation = c_uint()
       gain = c_uint()
     
       self.adc_conf.type = self.ADC_CONF_TYPE_CHN
       self.adc_conf.route_to = channel
       
       self.set_conf_mask(self.ADC_CONF_CHN_RANGE)
       self.set_conf_mask(self.ADC_CONF_CHN_TERMINATION)
       self.set_conf_mask(self.ADC_CONF_CHN_OFFSET)
       self.set_conf_mask(self.ADC_CONF_CHN_SATURATION)
    #   self.set_conf_mask(self.ADC_CONF_CHN_GAIN) doesn't work
       self.adc_retrieve_config(self.adc_ptr, byref(self.adc_conf))
      
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_CHN_RANGE, byref(channel_range))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_CHN_TERMINATION, byref(termination))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_CHN_OFFSET, byref(offset))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_CHN_SATURATION, byref(saturation))
    #   self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_CHN_GAIN, byref(gain))
      
       chn_conf = {'channel_range':channel_range.value, 'termination':termination.value, 'offset':offset.value,
                'saturation':saturation.value}
       memset(byref(self.adc_conf), 0, sizeof(adc_conf))
       return chn_conf
    
    def current_config_ext_trigger(self, channel):
       enable = c_uint()
       polarity = c_uint()
       delay = c_uint()
     
       self.adc_conf.type = self.ADC_CONF_TYPE_TRG_EXT
       self.adc_conf.route_to = channel
       
       self.set_conf_mask(self.ADC_CONF_TRG_EXT_ENABLE)
       self.set_conf_mask(self.ADC_CONF_TRG_EXT_POLARITY)
       self.set_conf_mask(self.ADC_CONF_TRG_EXT_DELAY)
       self.adc_retrieve_config(self.adc_ptr, byref(self.adc_conf))
      
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_TRG_EXT_ENABLE, byref(enable))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_TRG_EXT_POLARITY, byref(polarity))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_TRG_EXT_DELAY, byref(delay))
       ext_trg_conf = {'enable':enable.value, 'polarity':polarity.value, 'delay':delay.value}
       memset(byref(self.adc_conf), 0, sizeof(adc_conf))
       return ext_trg_conf
    
    def current_config_int_trigger(self, channel):
       enable = c_uint()
       polarity = c_uint()
       delay = c_uint()
       threshold = c_uint()
       hysteresis = c_uint()
     
       self.adc_conf.type = self.ADC_CONF_TYPE_TRG_THR
       self.adc_conf.route_to = channel
       
       self.set_conf_mask(self.ADC_CONF_TRG_THR_ENABLE)
       self.set_conf_mask(self.ADC_CONF_TRG_THR_POLARITY)
       self.set_conf_mask(self.ADC_CONF_TRG_THR_DELAY)
       self.set_conf_mask(self.ADC_CONF_TRG_THR_THRESHOLD)
    #   self.set_conf_mask(self.ADC_CONF_TRG_THR_HYSTERESIS) doesn't work
       self.adc_retrieve_config(self.adc_ptr, byref(self.adc_conf))
       
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_TRG_THR_ENABLE, byref(enable))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_TRG_THR_POLARITY, byref(polarity))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_TRG_THR_DELAY, byref(delay))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_TRG_THR_THRESHOLD, byref(threshold))
    #   self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_TRG_THR_HYSTERESIS, byref(hysteresis))
       threshold = threshold.value
       if(threshold > 0x7FFF):
          threshold = -(0x8000-(threshold - 0x8000))
       int_trg_conf = {'enable':enable.value, 'polarity':polarity.value, 'delay':delay.value,
               'threshold':threshold} 
       memset(byref(self.adc_conf), 0, sizeof(adc_conf))
       return int_trg_conf
    
    def current_config_board(self):
       n_chan = c_uint()
       n_trg_ext = c_uint()
       n_trg_int = c_uint()
     
       self.adc_conf.type = self.ADC_CONF_TYPE_BRD
       
       self.set_conf_mask(self.ADC_CONF_BRD_N_CHAN)
       self.set_conf_mask(self.ADC_CONF_BRD_N_TRG_EXT)
       self.set_conf_mask(self.ADC_CONF_BRD_N_TRG_THR)
       self.adc_retrieve_config(self.adc_ptr, byref(self.adc_conf))
       
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_BRD_N_CHAN, byref(n_chan))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_BRD_N_TRG_EXT, byref(n_trg_ext))
       self.adc_get_conf(byref(self.adc_conf), self.ADC_CONF_BRD_N_TRG_THR, byref(n_trg_int))
       board_conf = {'n_chan':n_chan.value, 'n_trg_ext':n_trg_ext.value, 'n_trg_int':n_trg_int.value}
       memset(byref(self.adc_conf), 0, sizeof(adc_conf))
       return board_conf
    
    def current_config(self):
       board_conf = self.current_config_board()
       n_chan = board_conf['n_chan']
       n_trg_ext = board_conf['n_trg_ext']
       n_trg_int = board_conf['n_trg_int']
       chn_conf = []
       ext_trg_conf = []
       int_trg_conf = [] 
       acq_conf = self.current_config_acq()
       for channel in range(0, n_chan):
          chn_conf.append(self.current_config_channel(channel))
       for channel in range(0, n_trg_ext):
          ext_trg_conf.append(self.current_config_ext_trigger(channel))
       for channel in range(0, n_trg_int): 
          int_trg_conf.append(self.current_config_int_trigger(channel))
    
       config = {'board_conf':board_conf, 'acq_conf':acq_conf, 'chn_conf':chn_conf, 'ext_trg_conf':ext_trg_conf, 'int_trg_conf':int_trg_conf}
       memset(byref(self.adc_conf), 0, sizeof(adc_conf))
       return config
    

