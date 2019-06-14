import numpy as np
from adc_lib_wrapper import *


class ADC_100m14b4cha(ADC_Generic):
    ADC_CONF_100M14B4CHA_CHN_RANGE_N = 3

    ADC_CONF_100M14B4CHA_CHN_RANGE_OPEN_DRAIN = 0
    ADC_CONF_100M14B4CHA_CHN_RANGE_100mV = 0x23
    ADC_CONF_100M14B4CHA_CHN_RANGE_1V = 0x11
    ADC_CONF_100M14B4CHA_CHN_RANGE_10V = 0x45
    ADC_CONF_100M14B4CHA_CHN_RANGE_100mV_CAL = 0x42
    ADC_CONF_100M14B4CHA_CHN_RANGE_1V_CAL = 0x40
    ADC_CONF_100M14B4CHA_CHN_RANGE_10V_CAL = 0x44


    ADC_CONF_100M14B4CHA_BUF_KMALLOC = 0
    ADC_CONF_100M14B4CHA_BUF_VMALLOC = 1

    ADC_CONF_100M14B4CHA_BUF_TYPE = 0
    ADC_CONF_100M14B4CHA_TRG_SW_EN = 1
    ADC_CONF_100M14B4CHA_ACQ_MSHOT_MAX = 2
    ADC_CONF_100M14B4CHA_BUF_SIZE_KB = 3
    ADC_CONF_100M14B4CHA_TRG_ALT_EN = 4
    __ADC_CONF_100M14B4CHA_LAST_INDEX = 5

    def __init__(self, pci_addr):
        super().__init__(pci_addr)


class ADC_100m14b4cha_extended_API(ADC_100m14b4cha):
    def __init__(self, pci_addr):
        super().__init__(pci_addr)
        self.buf_ptr = 0

    def __del__(self):
        super().__del__()
        self.remove_buffer()

    def remove_buffer(self):
        if not self.buf_ptr:
            self.release_buffer(self.buf_ptr, None)
            self.buf_ptr = 0

    def start_acquisition(self):
        tv = timeval()
        self.acq_start(self.ADC_F_FLUSH, byref(tv))

    def set_buffer(self, buf_size):
        self.release_buffer(self.buf_ptr, None)
        self.buf_ptr = self.request_buffer(buf_size, None, 0)

    def get_buffer_size(self):
        conf = self.get_current_adc_conf()
        acq_conf = conf['acq_conf']
        presamples = acq_conf['presamples']
        postsamples = acq_conf['postsamples']
        return presamples + postsamples

    def get_current_adc_conf(self):
        conf = self.current_config()
        return conf

    def stop_acquisition(self):
        self.acq_stop(0)

    def fill_buf(self):
        self.fill_buffer(self.buf_ptr, 0, None)

    def fileno(self):
        return self.zio_get_file_descriptor()

    def set_presamples(self, presamples):
        self.adc_conf.type = self.ADC_CONF_TYPE_ACQ
        self.set_conf(self.ADC_CONF_ACQ_PRE_SAMP, presamples)
        self.apply_config(0)
        buf_size = self.get_buffer_size()
        self.set_buffer(buf_size)

    def set_postsamples(self, postsamples):
        self.adc_conf.type = self.ADC_CONF_TYPE_ACQ
        self.set_conf(self.ADC_CONF_ACQ_POST_SAMP, postsamples)
        self.apply_config(0)
        buf_size = self.get_buffer_size()
        self.set_buffer(buf_size)

    def set_number_of_shots(self, n_shots):
        self.adc_conf.type = self.ADC_CONF_TYPE_ACQ
        self.set_conf(self.ADC_CONF_ACQ_N_SHOTS, n_shots)
        self.apply_config(0)

    def get_timestamp(self, buf_ptr, offset):
        ts = adc_timestamp()
        self.tstamp_buffer(buf_ptr, byref(ts))
        """cannot send 32bit int using xmlrpc"""
        secs = np.ctypeslib.as_array(ts.secs, (1, 1))
        ticks = np.ctypeslib.as_array(ts.ticks, (1, 1))
        secs = np.asscalar(secs)
        ticks = np.asscalar(ticks)
        ticks = ticks - offset

        """need to compensate for FIFO depth"""
        if(ticks < 16):
            secs = secs - 1
            ticks = ticks + 125000000-16
        else:
            ticks = ticks - 16
        timestamp = [secs, ticks]
        return timestamp

    def set_channel_range(self, channel, channel_range):
        """ possible values :
            100 mV     - 100
            1 V        - 1
            10V        - 10
            open input - 0"""
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

    def set_buffer_type(self, channel, type):
        self.adc_conf.type = self.ADC_CONF_TYPE_CUS
        self.adc_conf.route_to = channel
        self.set_conf(self.ADC_CONF_100M14B4CHA_BUF_TYPE, type)
        self.apply_config(0)

    def set_channel_termination(self, channel, termination):
        self.adc_conf.type = self.ADC_CONF_TYPE_CHN
        self.adc_conf.route_to = channel
        self.set_conf(self.ADC_CONF_CHN_TERMINATION, termination)
        self.apply_config(0)

    def set_channel_offset(self, channel, offset):
        """value of offset given in uV"""
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

        self.set_conf_mask(self.ADC_CONF_ACQ_N_SHOTS)
        self.set_conf_mask(self.ADC_CONF_ACQ_POST_SAMP)
        self.set_conf_mask(self.ADC_CONF_ACQ_PRE_SAMP)
        self.set_conf_mask(self.ADC_CONF_ACQ_UNDERSAMPLE)
        self.set_conf_mask(self.ADC_CONF_ACQ_FREQ_HZ)
        self.set_conf_mask(self.ADC_CONF_ACQ_N_BITS)
        self.retrieve_config()

        self.get_conf(self.ADC_CONF_ACQ_N_SHOTS, byref(n_shots))
        self.get_conf(self.ADC_CONF_ACQ_POST_SAMP, byref(postsamples))
        self.get_conf(self.ADC_CONF_ACQ_PRE_SAMP, byref(presamples))
        self.get_conf(self.ADC_CONF_ACQ_UNDERSAMPLE, byref(undersample))
        self.get_conf(self.ADC_CONF_ACQ_FREQ_HZ, byref(freq))
        self.get_conf(self.ADC_CONF_ACQ_N_BITS, byref(n_bits))
        acq_conf = {'n_shots': n_shots.value,
                    'presamples': presamples.value,
                    'postsamples': postsamples.value,
                    'undersample': undersample.value,
                    'freq': freq.value,
                    'n_bits': n_bits.value}

        memset(byref(self.adc_conf), 0, sizeof(adc_conf))
        return acq_conf

    def current_config_channel(self, channel):
        channel_range = c_uint()
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
        # self.set_conf_mask(self.ADC_CONF_CHN_GAIN) doesn't work
        self.retrieve_config()

        self.get_conf(self.ADC_CONF_CHN_RANGE, byref(channel_range))
        self.get_conf(self.ADC_CONF_CHN_TERMINATION, byref(termination))
        self.get_conf(self.ADC_CONF_CHN_OFFSET, byref(offset))
        self.get_conf(self.ADC_CONF_CHN_SATURATION, byref(saturation))
        # self.get_conf(self.ADC_CONF_CHN_GAIN, byref(gain))

        chn_conf = {'channel_range': channel_range.value,
                    'termination': termination.value,
                    'offset': offset.value,
                    'saturation': saturation.value}
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
        self.retrieve_config()

        self.get_conf(self.ADC_CONF_TRG_EXT_ENABLE, byref(enable))
        self.get_conf(self.ADC_CONF_TRG_EXT_POLARITY, byref(polarity))
        self.get_conf(self.ADC_CONF_TRG_EXT_DELAY, byref(delay))
        ext_trg_conf = {'enable': enable.value,
                        'polarity': polarity.value,
                        'delay': delay.value}
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
        # self.set_conf_mask(self.ADC_CONF_TRG_THR_HYSTERESIS)
        self.retrieve_config()

        self.get_conf(self.ADC_CONF_TRG_THR_ENABLE, byref(enable))
        self.get_conf(self.ADC_CONF_TRG_THR_POLARITY, byref(polarity))
        self.get_conf(self.ADC_CONF_TRG_THR_DELAY, byref(delay))
        self.get_conf(self.ADC_CONF_TRG_THR_THRESHOLD, byref(threshold))
        # self.get_conf(self.ADC_CONF_TRG_THR_HYSTERESIS,
        #                                    byref(hysteresis))
        threshold = threshold.value
        if(threshold > 0x7FFF):
            threshold = -(0x8000-(threshold - 0x8000))
        int_trg_conf = {'enable': enable.value,
                        'polarity': polarity.value,
                        'delay': delay.value,
                        'threshold': threshold}
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
        self.retrieve_config()

        self.get_conf(self.ADC_CONF_BRD_N_CHAN, byref(n_chan))
        self.get_conf(self.ADC_CONF_BRD_N_TRG_EXT, byref(n_trg_ext))
        self.get_conf(self.ADC_CONF_BRD_N_TRG_THR, byref(n_trg_int))
        board_conf = {'n_chan': n_chan.value,
                      'n_trg_ext': n_trg_ext.value,
                      'n_trg_int': n_trg_int.value}
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
            ext_trg_conf.append(self.current_config_ext_trigger(
                                                            channel))
        for channel in range(0, n_trg_int):
            int_trg_conf.append(self.current_config_int_trigger(
                                                            channel))

        config = {'board_conf': board_conf,
                  'acq_conf': acq_conf,
                  'chn_conf': chn_conf,
                  'ext_trg_conf': ext_trg_conf,
                  'int_trg_conf': int_trg_conf}
        memset(byref(self.adc_conf), 0, sizeof(adc_conf))
        return config
