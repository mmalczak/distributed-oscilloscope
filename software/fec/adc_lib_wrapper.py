from ctypes import *
import errno


""" Wrapper for ADC C library using ctypes
All ctypes functions have exactly the same names as the ones in the
C library. To each function corresponds python function that hides
C specific operations from the user. The names of these functions are
the sames as the ctypes functions without ADC prefix."""


class adc_conf(Structure):
    __ADC_CONF_LEN = 64          # fixme what to do about it
    _fields_ = [("type", c_int),
                ("dev_type", c_uint),
                ("route_to", c_uint),
                ("flags", c_uint),
                ("mask", c_ulong),
                ("value", c_uint * __ADC_CONF_LEN)]

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
                ("flags", c_uint)]


class timeval(Structure):
    _fields_ = [("sec", c_long),
                ("usec", c_long)]


class adc_timestamp(Structure):
    _fields_ = [("secs", c_ulong),
                ("ticks", c_ulong),
                ("bins", c_ulong)]


class ADC_Generic():
    ADC_F_USERMASK = 0xffff0000
    ADC_F_FLUSH = 0x00010000
    ADC_F_VERBOSE = 0x00020000
    ADC_F_FIXUP = 0x00400000

    FMCADC_100MS_4CH_14BIT = 0
    ADC_ZIOFAKE = 1
    ADC_GENERICFAKE = 2
    __ADC_SUPPORTED_BOARDS_LAST_INDEX = 3

    ADC_TRG_POL_POS = 0
    ADC_TRG_POL_NEG = 1

    ADC_CONF_TRG_EXT_ENABLE = 0
    ADC_CONF_TRG_EXT_POLARITY = 1
    ADC_CONF_TRG_EXT_DELAY = 2
    __ADC_CONF_TRG_EXT_LAST_INDEX = 3

    ADC_CONF_TRG_THR_ENABLE = 0
    ADC_CONF_TRG_THR_POLARITY = 1
    ADC_CONF_TRG_THR_DELAY = 2
    ADC_CONF_TRG_THR_THRESHOLD = 3
    ADC_CONF_TRG_THR_HYSTERESIS = 4
    __ADC_CONF_TRG_THR_LAST_INDEX = 5

    ADC_CONF_TRG_TIM_ENABLE = 0
    __ADC_CONF_TRG_TIM_LAST_INDEX = 1

    ADC_CONF_ACQ_N_SHOTS = 0
    ADC_CONF_ACQ_POST_SAMP = 1
    ADC_CONF_ACQ_PRE_SAMP = 2
    ADC_CONF_ACQ_UNDERSAMPLE = 3
    ADC_CONF_ACQ_FREQ_HZ = 4
    ADC_CONF_ACQ_N_BITS = 5
    __ADC_CONF_ACQ_ATTRIBUTE_LAST_INDEX = 6

    ADC_CONF_CHN_RANGE = 0
    ADC_CONF_CHN_TERMINATION = 1
    ADC_CONF_CHN_OFFSET = 2
    ADC_CONF_CHN_SATURATION = 3
    ADC_CONF_CHN_GAIN = 4
    __ADC_CONF_CHN_ATTRIBUTE_LAST_INDEX = 5

    ADC_CONF_BRD_STATUS = 0
    ADC_CONF_BRD_MAX_FREQ_HZ = 1
    ADC_CONF_BRD_MIN_FREQ_HZ = 2
    ADC_CONF_BRD_STATE_MACHINE_STATUS = 3
    ADC_CONF_BRD_N_CHAN = 4
    ADC_CONF_BRD_N_TRG_EXT = 5
    ADC_CONF_BRD_N_TRG_THR = 6
    ADC_CONF_BRD_N_TRG_TIM = 7
    ADC_CONF_UTC_TIMING_BASE_S = 8
    ADC_CONF_UTC_TIMING_BASE_T = 9
    ADC_CONF_UTC_TIMING_BASE_B = 10
    __ADC_CONF_BRD_ATTRIBUTE_LAST_INDEX = 11

    ADC_CONF_TYPE_BRD = 0
    ADC_CONF_TYPE_CHN = 1
    ADC_CONF_TYPE_ACQ = 2
    ADC_CONF_TYPE_CUS = 3
    ADC_CONF_TYPE_TRG_EXT = 4
    ADC_CONF_TYPE_TRG_THR = 5
    ADC_CONF_TYPE_TRG_TIM = 6
    __ADC_CONF_TYPE_LAST_INDEX = 7

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
        self.__ADC_CONF_LEN = 64
        """number of allocated items in each structure"""

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
        self.adc_open.argtypes = [c_char_p, c_uint, c_ulong,
                                  c_uint, c_ulong]
        self.adc_open.errcheck = self.__errcheck_pointer

        self.adc_open_by_lun = self.libc.adc_open_by_lun
        self.adc_open_by_lun.restype = c_void_p
        self.adc_open_by_lun.argtypes = [c_char_p, c_int,
                                         c_ulong, c_uint, c_ulong]
        self.adc_open_by_lun.errcheck = self.__errcheck_pointer

        self.adc_request_buffer = self.libc.adc_request_buffer
        self.adc_request_buffer.restype = POINTER(adc_buf)
        self.adc_request_buffer.argtypes = [c_void_p, c_int, c_void_p,
                                            c_uint]
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
        """self.adc_get_conf.argtypes = [c_void_p, c_uint,
                                        POINTER(c_uint)]"""
        self.adc_get_conf.errcheck = self.__errcheck_int

        self.adc_apply_config = self.libc.adc_apply_config
        self.adc_apply_config.restype = c_int
        self.adc_apply_config.argtypes = [c_void_p, c_uint, c_void_p]
        self.adc_apply_config.errcheck = self.__errcheck_int

        self.adc_acq_start = self.libc.adc_acq_start
        self.adc_acq_start.restype = c_int
        self.adc_acq_start.argtypes = [c_void_p, c_uint, c_void_p]
        self.adc_acq_start.errcheck = self.__errcheck_int

        self.adc_zio_get_file_descriptor =\
            self.libc.adc_zio_get_file_descriptor
        self.adc_zio_get_file_descriptor.restype = c_int
        self.adc_zio_get_file_descriptor.argtypes = [c_void_p]
        self.adc_zio_get_file_descriptor.errcheck = self.__errcheck_int

        self.adc_acq_poll = self.libc.adc_acq_poll
        self.adc_acq_poll.restype = c_int
        self.adc_acq_poll.argtypes = [c_void_p, c_uint, c_void_p]
        self.adc_acq_poll.errcheck = self.__errcheck_int

        self.adc_fill_buffer = self.libc.adc_fill_buffer
        self.adc_fill_buffer.restype = c_int
        self.adc_fill_buffer.argtypes = [c_void_p, c_void_p,
                                         c_uint, c_void_p]
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
        self.adc_release_buffer.argtypes = [c_void_p, c_void_p,
                                            c_void_p]
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

        """this function doesn't have body
        self.adc_reset_conf = self.libc.adc_reset_conf
        self.adc_reset_conf.restype = c_int
        self.adc_reset_conf.argtypes = [c_void_p, c_uint, c_void_p]
        self.adc_reset_conf.errcheck = self.__errcheck_int"""

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
        self.adc_get_param.argtypes = [c_void_p, c_char_p,
                                       c_char_p, c_void_p]
        self.adc_get_param.errcheck = self.__errcheck_int

        self.adc_set_param = self.libc.adc_set_param
        self.adc_set_param.restype = c_int
        self.adc_set_param.argtypes = [c_void_p, c_char_p,
                                       c_char_p, c_void_p]
        self.adc_set_param.errcheck = self.__errcheck_int

        self.adc_set_conf_mask_all = self.libc.adc_set_conf_mask_all
        self.adc_set_conf_mask_all.restype = None
        self.adc_set_conf_mask_all.argtypes = [c_void_p, c_void_p]

        self.__init()
        self.__adc_ptr = self.__open(b"fmc-adc-100m14b4cha", pci_addr,
                                 0, 0, self.ADC_F_FLUSH)
        self.adc_conf = adc_conf()

    def __del__(self):
        self.__close()
        self.__exit()

    def __init(self):
        self.adc_init()

    def __exit(self):
        self.adc_exit()

    def strerror(self, errnum):
        return self.adc_strerror(errnum)

    def get_driver_type(self):
        return self.adc_get_driver_type(self.__adc_ptr)

    def __open(self, name, dev_id, totalsamples, nbuffer, flags):
        return self.adc_open(name, dev_id, totalsamples, nbuffer, flags)

    def __open_by_lun(self, name, lun, totalsamples, nbuffer, flags):
        return self.adc_open_by_lun(name, lun, totalsamples, nbuffer,
                                    flags)

    def request_buffer(self, nsamples, alloc, flags):
        return self.adc_request_buffer(self.__adc_ptr, nsamples,
                                       alloc, flags)

    def set_conf(self, conf_index, val):
        self.adc_set_conf(byref(self.adc_conf), conf_index, val)

    def set_conf_mask(self, conf_index):
        self.adc_set_conf_mask(byref(self.adc_conf), conf_index)

    def get_conf(self, conf_index, val):
        self.adc_get_conf(byref(self.adc_conf), conf_index, val)

    def acq_start(self, flags, timeout):
        self.adc_acq_start(self.__adc_ptr, flags, timeout)

    # NON API
    def zio_get_file_descriptor(self):
        return self.adc_zio_get_file_descriptor(self.__adc_ptr)

    def acq_poll(self, flags, timeout):
        self.adc_acq_poll(self.__adc_ptr, flags, timeout)

    def fill_buffer(self, buf, flags, timeout):
        self.adc_fill_buffer(self.__adc_ptr, buf, flags, timeout)

    def acq_stop(self, flags):
        self.adc_acq_stop(self.__adc_ptr, flags)

    def tstamp_buffer(self, buf, ts):
        self.adc_tstamp_buffer(buf, ts)

    def release_buffer(self, buf, free):
        self.adc_release_buffer(self.__adc_ptr, buf, free)

    def __close(self):
        if not self.__adc_ptr:
            self.adc_close(self.__adc_ptr)
            self.__adc_ptr = 0

    def trigger_fire(self):
        self.adc_trigger_fire(self.__adc_ptr)

    def has_trigger_fire(self):
        return self.adc_has_trigger_fire(self.__adc_ptr)

    def apply_config(self, flags):
        self.adc_apply_config(self.__adc_ptr, flags, byref(self.adc_conf))
        memset(byref(self.adc_conf), 0, sizeof(adc_conf))

    def retrieve_config(self):
        self.adc_retrieve_config(self.__adc_ptr, byref(self.adc_conf))

    def get_capabilities(self, type):
        self.adc_get_capabilities(self.__adc_ptr, type)

    def get_param(self, name, sptr, iptr):
        self.adc_get_param(self.__adc_ptr, name, sptr, iptr)

    def set_param(self, name, sptr, iptr):
        self.adc_set_param(self.__adc_ptr, name, sptr, iptr)

    def set_conf_mask_all(self):
        self.adc_set_conf_mask_all(byref(self.adc_conf), self.__adc_ptr)
