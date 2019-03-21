from adc_lib_wrapper import *
from adc_lib_100m14b4cha_wrapper import *
import numpy as np


def set_presamples(adc_ptr, presamples):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_ACQ
   adc_set_conf(byref(cfg), ADC_CONF_ACQ_PRE_SAMP, presamples)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):
      print(adc_strerror(get_errno()))
      print("Cannot configure pre and post samples")

def set_postsamples(adc_ptr, postsamples):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_ACQ
   adc_set_conf(byref(cfg), ADC_CONF_ACQ_POST_SAMP, postsamples)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):
      print(adc_strerror(get_errno()))
      print("Cannot configure pre and post samples")
 
def set_number_of_shots(adc_ptr, n_shots):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_ACQ
   adc_set_conf(byref(cfg), ADC_CONF_ACQ_N_SHOTS, n_shots)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure number of shots")

def get_timestamp(buf_ptr, offset):
   ts = adc_timestamp()
   adc_tstamp_buffer(buf_ptr, byref(ts))
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
   secs_low = secs &               int('0x0000000000ffffff', 16)
   secs_middle = (secs >> 24) &    int('0x0000000000ffffff', 16)
   secs_high = (secs >> 48) &      int('0x0000000000ffffff', 16)
   ticks_low = ticks &             int('0x0000000000ffffff', 16)
   ticks_middle = (ticks >> 24) &  int('0x0000000000ffffff', 16)
   ticks_high = (ticks >> 48) &    int('0x0000000000ffffff', 16)
   #print( (secs_high << 48 ) + (secs_middle << 24) + secs_low)
   timestamp = [secs_low, secs_middle, secs_high, ticks_low, ticks_middle, ticks_high]
   return timestamp 


ADC_CONF_100M14B4CHA_CHN_RANGE_OPEN_DRAIN   = 0
ADC_CONF_100M14B4CHA_CHN_RANGE_100mV        = 0x23
ADC_CONF_100M14B4CHA_CHN_RANGE_1V           = 0x11
ADC_CONF_100M14B4CHA_CHN_RANGE_10V          = 0x45
ADC_CONF_100M14B4CHA_CHN_RANGE_100mV_CAL    = 0x42
ADC_CONF_100M14B4CHA_CHN_RANGE_1V_CAL       = 0x40
ADC_CONF_100M14B4CHA_CHN_RANGE_10V_CAL      = 0x44




def set_channel_range(adc_ptr, channel, channel_range):
   # possible values :
   # 100 mV     - 100
   # 1 V        - 1
   # 10V        - 10
   # open input - 0
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_CHN
   cfg.route_to = channel
   if(channel_range == 100):
      ch_range = ADC_CONF_100M14B4CHA_CHN_RANGE_100mV
   elif(channel_range == 1):
      ch_range = ADC_CONF_100M14B4CHA_CHN_RANGE_1V
   elif(channel_range == 10):
      ch_range = ADC_CONF_100M14B4CHA_CHN_RANGE_10V
   elif(channel_range == 0):
      ch_range = ADC_CONF_100M14B4CHA_CHN_RANGE_OPEN_DRAIN
   else:
      print("Wrong channel range")

   adc_set_conf(byref(cfg), ADC_CONF_CHN_RANGE, ch_range)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure range")

def set_channel_termination(adc_ptr, channel, termination):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_CHN
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_CHN_TERMINATION, termination)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure termination")


def set_channel_offset(adc_ptr, channel, offset):
   #value of offset given in uV
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_CHN
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_CHN_OFFSET, offset)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure offset")

def set_channel_saturation(adc_ptr, channel, saturation):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_CHN
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_CHN_SATURATION, saturation)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure saturation")

def set_channel_gain(adc_ptr, channel, gain):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_CHN
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_CHN_GAIN, gain)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure gain")

def set_external_trigger_enable(adc_ptr, channel, enable):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_TRG_EXT 
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_TRG_EXT_ENABLE, enable)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure external trigger enable")

def set_external_trigger_polarity(adc_ptr, channel, polarity):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_TRG_EXT 
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_TRG_EXT_POLARITY, polarity)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure external trigger polarity")

def set_external_trigger_delay(adc_ptr, channel, delay):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_TRG_EXT 
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_TRG_EXT_DELAY, delay)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure external trigger delay")

def set_internal_trigger_enable(adc_ptr, channel, enable):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_TRG_THR 
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_TRG_THR_ENABLE, enable)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure threshold trigger enable")

def set_internal_trigger_polarity(adc_ptr, channel, polarity):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_TRG_THR 
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_TRG_THR_POLARITY, polarity)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure threshold trigger polarity")

def set_internal_trigger_delay(adc_ptr, channel, delay):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_TRG_THR 
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_TRG_THR_DELAY, delay)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure threshold trigger delay")

def set_internal_trigger_threshold(adc_ptr, channel, threshold):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_TRG_THR 
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_TRG_THR_THRESHOLD, threshold)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure threshold trigger treshold")

def set_internal_trigger_hysteresis(adc_ptr, channel, hysteresis):
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_TRG_THR 
   cfg.route_to = channel
   adc_set_conf(byref(cfg), ADC_CONF_TRG_THR_HYSTERESIS, hysteresis)
   err = adc_apply_config(adc_ptr, 0, byref(cfg))
   if(err!=0):print("Cannot configure threshold trigger hysteresis")

def initialise_adc(pci_addr):
   err = adc_init()
   if(err!=0):print("Init error")
   adc_ptr = adc_open(b"fmc-adc-100m14b4cha", pci_addr, 0 , 0 , ADC_F_FLUSH)
   if(adc_ptr == 0): print("Cannot open device")
   return adc_ptr 
  
def close_adc(adc_ptr):
   adc_close(adc_ptr)
   adc_exit()

def current_config_acq(adc_ptr):
   n_shots = c_uint()
   presamples = c_uint()
   postsamples = c_uint()
   undersample = c_uint()
   freq = c_uint()
   n_bits = c_uint()
 
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_ACQ

   adc_set_conf_mask(byref(cfg), ADC_CONF_ACQ_N_SHOTS                )
   adc_set_conf_mask(byref(cfg), ADC_CONF_ACQ_POST_SAMP)
   adc_set_conf_mask(byref(cfg), ADC_CONF_ACQ_PRE_SAMP)
   adc_set_conf_mask(byref(cfg), ADC_CONF_ACQ_UNDERSAMPLE)
   adc_set_conf_mask(byref(cfg), ADC_CONF_ACQ_FREQ_HZ)
   adc_set_conf_mask(byref(cfg), ADC_CONF_ACQ_N_BITS)
   err = adc_retrieve_config(adc_ptr, byref(cfg))
   if(err!=0):print("Cannot retrieve config acq")
   adc_get_conf(byref(cfg), ADC_CONF_ACQ_N_SHOTS, byref(n_shots))
   adc_get_conf(byref(cfg), ADC_CONF_ACQ_POST_SAMP, byref(postsamples))
   adc_get_conf(byref(cfg), ADC_CONF_ACQ_PRE_SAMP, byref(presamples))
   adc_get_conf(byref(cfg), ADC_CONF_ACQ_UNDERSAMPLE, byref(undersample))
   adc_get_conf(byref(cfg), ADC_CONF_ACQ_FREQ_HZ, byref(freq))
   adc_get_conf(byref(cfg), ADC_CONF_ACQ_N_BITS, byref(n_bits))
   acq_conf = {'n_shots':n_shots.value, 'presamples':presamples.value, 'postsamples':postsamples.value, 
            'undersample':undersample.value, 'freq':freq.value, 'n_bits':n_bits.value}
   return acq_conf

def current_config_channel(adc_ptr, channel):
   channel_range= c_uint()
   termination = c_uint()
   offset = c_int()  # originally it is uint
   saturation = c_uint()
   gain = c_uint()
 
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_CHN
   cfg.route_to = channel
   
   adc_set_conf_mask(byref(cfg), ADC_CONF_CHN_RANGE)
   adc_set_conf_mask(byref(cfg), ADC_CONF_CHN_TERMINATION)
   adc_set_conf_mask(byref(cfg), ADC_CONF_CHN_OFFSET)
   adc_set_conf_mask(byref(cfg), ADC_CONF_CHN_SATURATION)
#   adc_set_conf_mask(byref(cfg), ADC_CONF_CHN_GAIN) doesn't work
   err = adc_retrieve_config(adc_ptr, byref(cfg))
   if(err!=0):print("Cannot retrieve config channel")
   adc_get_conf(byref(cfg), ADC_CONF_CHN_RANGE, byref(channel_range))
   adc_get_conf(byref(cfg), ADC_CONF_CHN_TERMINATION, byref(termination))
   adc_get_conf(byref(cfg), ADC_CONF_CHN_OFFSET, byref(offset))
   adc_get_conf(byref(cfg), ADC_CONF_CHN_SATURATION, byref(saturation))
#   adc_get_conf(byref(cfg), ADC_CONF_CHN_GAIN, byref(gain))
  
   chn_conf = {'channel_range':channel_range.value, 'termination':termination.value, 'offset':offset.value,
            'saturation':saturation.value}
   return chn_conf

def current_config_ext_trigger(adc_ptr, channel):
   enable = c_uint()
   polarity = c_uint()
   delay = c_uint()
 
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_TRG_EXT
   cfg.route_to = channel
   
   adc_set_conf_mask(byref(cfg), ADC_CONF_TRG_EXT_ENABLE)
   adc_set_conf_mask(byref(cfg), ADC_CONF_TRG_EXT_POLARITY)
   adc_set_conf_mask(byref(cfg), ADC_CONF_TRG_EXT_DELAY)
   err = adc_retrieve_config(adc_ptr, byref(cfg))
   if(err!=0):print("Cannot retrieve config ext trigger")
   adc_get_conf(byref(cfg), ADC_CONF_TRG_EXT_ENABLE, byref(enable))
   adc_get_conf(byref(cfg), ADC_CONF_TRG_EXT_POLARITY, byref(polarity))
   adc_get_conf(byref(cfg), ADC_CONF_TRG_EXT_DELAY, byref(delay))
   ext_trg_conf = {'enable':enable.value, 'polarity':polarity.value, 'delay':delay.value}
   return ext_trg_conf

def current_config_int_trigger(adc_ptr, channel):
   enable = c_uint()
   polarity = c_uint()
   delay = c_uint()
   threshold = c_uint()
   hysteresis = c_uint()
 
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_TRG_THR
   cfg.route_to = channel
   
   adc_set_conf_mask(byref(cfg), ADC_CONF_TRG_THR_ENABLE)
   adc_set_conf_mask(byref(cfg), ADC_CONF_TRG_THR_POLARITY)
   adc_set_conf_mask(byref(cfg), ADC_CONF_TRG_THR_DELAY)
   adc_set_conf_mask(byref(cfg), ADC_CONF_TRG_THR_THRESHOLD)
#   adc_set_conf_mask(byref(cfg), ADC_CONF_TRG_THR_HYSTERESIS) doesn't work
   err = adc_retrieve_config(adc_ptr, byref(cfg))
   if(err!=0):print("Cannot retrieve config int trigger")
   adc_get_conf(byref(cfg), ADC_CONF_TRG_THR_ENABLE, byref(enable))
   adc_get_conf(byref(cfg), ADC_CONF_TRG_THR_POLARITY, byref(polarity))
   adc_get_conf(byref(cfg), ADC_CONF_TRG_THR_DELAY, byref(delay))
   adc_get_conf(byref(cfg), ADC_CONF_TRG_THR_THRESHOLD, byref(threshold))
#   adc_get_conf(byref(cfg), ADC_CONF_TRG_THR_HYSTERESIS, byref(hysteresis))
   threshold = threshold.value
   if(threshold > 0x7FFF):
      threshold = -(0x8000-(threshold - 0x8000))
   int_trg_conf = {'enable':enable.value, 'polarity':polarity.value, 'delay':delay.value,
           'threshold':threshold} 
   return int_trg_conf

def current_config_board(adc_ptr):
   n_chan = c_uint()
   n_trg_ext = c_uint()
   n_trg_int = c_uint()
 
   cfg = adc_conf()
   memset(byref(cfg), 0, sizeof(adc_conf))
   cfg.type = ADC_CONF_TYPE_BRD
   
   adc_set_conf_mask(byref(cfg), ADC_CONF_BRD_N_CHAN)
   adc_set_conf_mask(byref(cfg), ADC_CONF_BRD_N_TRG_EXT)
   adc_set_conf_mask(byref(cfg), ADC_CONF_BRD_N_TRG_THR)
   err = adc_retrieve_config(adc_ptr, byref(cfg))
   if(err!=0):print("Cannot retrieve config board")
   adc_get_conf(byref(cfg), ADC_CONF_BRD_N_CHAN, byref(n_chan))
   adc_get_conf(byref(cfg), ADC_CONF_BRD_N_TRG_EXT, byref(n_trg_ext))
   adc_get_conf(byref(cfg), ADC_CONF_BRD_N_TRG_THR, byref(n_trg_int))
   board_conf = {'n_chan':n_chan.value, 'n_trg_ext':n_trg_ext.value, 'n_trg_int':n_trg_int.value}
   return board_conf

def current_config(adc_ptr):
   board_conf = current_config_board(adc_ptr)
   n_chan = board_conf['n_chan']
   n_trg_ext = board_conf['n_trg_ext']
   n_trg_int = board_conf['n_trg_int']
   chn_conf = []
   ext_trg_conf = []
   int_trg_conf = [] 
   acq_conf = current_config_acq(adc_ptr)
   for channel in range(0, n_chan):
      chn_conf.append(current_config_channel(adc_ptr, channel))
   for channel in range(0, n_trg_ext):
      ext_trg_conf.append(current_config_ext_trigger(adc_ptr, channel))
   for channel in range(0, n_trg_int): 
      int_trg_conf.append(current_config_int_trigger(adc_ptr, channel))

   config = {'board_conf':board_conf, 'acq_conf':acq_conf, 'chn_conf':chn_conf, 'ext_trg_conf':ext_trg_conf, 'int_trg_conf':int_trg_conf}
   return config


