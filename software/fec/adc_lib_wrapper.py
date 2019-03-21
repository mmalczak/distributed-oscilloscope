from ctypes import *


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


__ADC_CONF_LEN = 64 # number of allocated items in each structure 

class adc_conf(Structure) :
   __ADC_CONF_LEN = 64          # fixme what to do about it
   _fields_ = [("type", c_int),
               ("dev_type", c_uint),
               ("route_to", c_uint),
               ("flags", c_uint),
               ("mask", c_ulong),
               ("value", c_uint * __ADC_CONF_LEN)
              ]
ADC_F_USERMASK  = 0xffff0000 # < Flag mask -- low-bits are used
                             #   by lib-int.h 
ADC_F_FLUSH     = 0x00010000 # < Flag used to flush the buffer
                             # (used by adc_open) 
ADC_F_VERBOSE   = 0x00020000 # < Flag used to verbose on stdout/stderr
                             # (usable by any function)
ADC_F_FIXUP     = 0x00400000 # < Flag used to fixup a buffer when
                             # filling it (usable by adc_fill_buffer) 


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

libc = CDLL("/home/Projects/distributed_oscilloscope/dependencies/adc-lib/lib/libadc.so")

adc_print_version = libc.adc_print_version
adc_print_version.restype = None
adc_print_version.argtypes = None

adc_init = libc.adc_init
adc_init.restype = c_int
adc_init.argtypes = None

adc_exit = libc.adc_exit
adc_exit.restype = None
adc_exit.argtypes = None

adc_strerror = libc.adc_strerror
adc_strerror.restype = c_char_p
adc_strerror.argtypes = [c_int]

adc_get_driver_type = libc.adc_get_driver_type
adc_get_driver_type.restype = c_char_p
adc_get_driver_type.argtypes = [c_void_p]

adc_open = libc.adc_open
adc_open.restype = c_void_p
adc_open.argtypes = [c_char_p, c_uint, c_ulong, c_uint, c_ulong]

adc_open_by_lun = libc.adc_open_by_lun
adc_open_by_lun.restype = c_void_p
adc_open_by_lun.argtypes = [c_char_p, c_int, c_ulong, c_uint, c_ulong]

adc_request_buffer = libc.adc_request_buffer
adc_request_buffer.restype = POINTER(adc_buf)
adc_request_buffer.argtypes = [c_void_p, c_int, c_void_p, c_uint]

adc_set_conf = libc.adc_set_conf
adc_set_conf.restype = None
adc_set_conf.argtypes = [c_void_p, c_uint, c_uint]

adc_set_conf_mask = libc.adc_set_conf_mask
adc_set_conf_mask.restype = None
adc_set_conf_mask.argtypes = [c_void_p, c_uint]

adc_get_conf = libc.adc_get_conf
adc_get_conf.restype = c_int
adc_get_conf.argtypes = [c_void_p, c_uint, c_void_p]
#adc_get_conf.argtypes = [c_void_p, c_uint, POINTER(c_uint)]

adc_apply_config = libc.adc_apply_config
adc_apply_config.restype = c_int
adc_apply_config.argtypes = [c_void_p, c_uint, c_void_p]

adc_acq_start = libc.adc_acq_start
adc_acq_start.restype = c_int
adc_acq_start.argtypes = [c_void_p, c_uint, c_void_p]

adc_acq_poll = libc.adc_acq_poll
adc_acq_poll.restype = c_int
adc_acq_poll.argtypes = [c_void_p, c_uint, c_void_p]

adc_fill_buffer = libc.adc_fill_buffer
adc_fill_buffer.restype = c_int
adc_fill_buffer.argtypes = [c_void_p, c_void_p, c_uint, c_void_p]

adc_acq_stop = libc.adc_acq_stop 
adc_acq_stop.restype = c_int
adc_acq_stop.argtypes = [c_void_p, c_uint]

adc_tstamp_buffer = libc.adc_tstamp_buffer
adc_tstamp_buffer.restype = POINTER(adc_timestamp)
adc_tstamp_buffer.argtypes = [c_void_p, c_void_p]

adc_release_buffer = libc.adc_release_buffer
adc_release_buffer.restype = c_int
adc_release_buffer.argtypes = [c_void_p, c_void_p, c_void_p]

adc_close = libc.adc_close
adc_close.restype = c_int
adc_close.argtypes = [c_void_p]

adc_trigger_fire = libc.adc_trigger_fire
adc_trigger_fire.restype = c_int
adc_trigger_fire.argtypes = [c_void_p]

adc_has_trigger_fire = libc.adc_has_trigger_fire
adc_has_trigger_fire.restype = c_int
adc_has_trigger_fire.argtypes = [c_void_p]

#this function doesn't have body
#adc_reset_conf = libc.adc_reset_conf
#adc_reset_conf.restype = c_int 
#adc_reset_conf.argtypes = [c_void_p, c_uint, c_void_p]

adc_apply_config = libc.adc_apply_config
adc_apply_config.restype = c_int
adc_apply_config.argtypes = [c_void_p, c_uint, c_void_p]

adc_retrieve_config = libc.adc_retrieve_config
adc_retrieve_config.restype = c_int
adc_retrieve_config.argtypes = [c_void_p, c_void_p]

adc_get_capabilities = libc.adc_get_capabilities
adc_get_capabilities.restype = c_ulong
adc_get_capabilities.argtypes = [c_void_p, c_int] 

adc_get_param = libc.adc_get_param
adc_get_param.restype = c_int
adc_get_param.argtypes = [c_void_p, c_char_p, c_char_p, c_void_p]

adc_set_param = libc.adc_set_param
adc_set_param.restype = c_int
adc_set_param.argtypes = [c_void_p, c_char_p, c_char_p, c_void_p]

adc_set_conf_mask_all = libc.adc_set_conf_mask_all
adc_set_conf_mask_all.restype = None
adc_set_conf_mask_all.argtypes = [c_void_p, c_void_p]


