from ctypes import *
import numpy as np


""" Wrapper for WRTD C library using ctypes
All ctypes functions have exactly the same names as the ones in the
C library. To each function corresponds python function that hides
C specific operations from the user. The names of these functions are
the sames as the ctypes functions without WRTD prefix."""


class wrtd(Structure):
    pass


class wrtd_tstamp(Structure):
    _fields_ = [("seconds", c_uint),
                ("ns", c_uint),
                ("frac", c_uint)]


class wrtd_event(Structure):
    _fields_ = [('wrtd_tstamp', wrtd_tstamp),
                ('id', c_char_p),
                ('seq', c_uint32),
                ('flags', c_char)]


class wrtd_log_entry(Structure):
    _fields_ = [('type', c_uint32),
                ('reason', c_uint32),
                ('wrtd_event', wrtd_event),
                ('wrtd_tstamp', wrtd_tstamp)]


class tstamp():
    def __init__(self):
        seconds = 0
        ns = 0
        frac = 0


def encode_arguments(func):
    """Used to convert arguments from strings to bytes"""
    def wrapper(self, *args, **kwargs):
        encoded = []
        for arg in args:
            if(type(arg) == str):
                encoded.append(arg.encode('utf-8'))
            else:
                encoded.append(arg)
        args = tuple(encoded)
        return func(self, *args, **kwargs)
    return wrapper


class WRTD_wrapper():
    WRTD_SUCCESS = 0
    WRTD_ERROR_BASE = 0xBFFA3000
    WRTD_ERROR_CANNOT_RECOVE = 0xBFFA3001
    WRTD_ERROR_INVALID_ATTRIBUTE = 0xBFFA3002
    WRTD_ERROR_ATTR_NOT_WRITEABLE = 0xBFFA3003
    WRTD_ERROR_ATTR_NOT_READABLE = 0xBFFA3004
    WRTD_ERROR_INVALID_VALUE = 0xBFFA3005
    WRTD_ERROR_NOT_INITIALIZED = 0xBFFA3006
    WRTD_ERROR_MISSING_OPTION_NAME = 0xBFFA3007
    WRTD_ERROR_MISSING_OPTION_VALUE = 0xBFFA3008
    WRTD_ERROR_BAD_OPTION_NAME = 0xBFFA3009
    WRTD_ERROR_BAD_OPTION_VALUE = 0xBFFA300A
    WRTD_ERROR_OUT_OF_MEMORY = 0xBFFA300B
    WRTD_ERROR_OPERATION_PENDING = 0xBFFA300C
    WRTD_ERROR_NULL_POINTER = 0xBFFA300D
    WRTD_ERROR_UNEXPECTED_RESPONSE = 0xBFFA300E
    WRTD_ERROR_RESET_FAILED = 0xBFFA300F
    WRTD_ERROR_RESOURCE_UNKNOWN = 0xBFFA3010

    WRTD_ERROR_RESOURCE_ACTIVE = 0xBFFA3011

    WRTD_ERROR_ATTR_INVALID_REP_CAP = 0xBFFA3012

    WRTD_ERROR_NOT_IMPLEMENTED = 0xBFFA3013

    WRTD_ERROR_BAD_REP_CAP_ID = 0xBFFA3014

    WRTD_ERROR_TIMEOUT = 0xBFFA3015

    WRTD_ERROR_BUFFER_TOO_SHORT = 0xBFFA3016

    WRTD_ERROR_UNKNOWN_NAME_IN_SELECTOR = 0xBFFA3017

    WRTD_ERROR_ALARM_TIME_INVALID = 0xBFFA3018
    WRTD_ERROR_ALARM_EXISTS = 0xBFFA3019
    WRTD_ERROR_ALARM_DOES_NOT_EXIST = 0xBFFA301A
    WRTD_ERROR_ALARM_OUT_OF_RESOURCES = 0xBFFA301B
    WRTD_ERROR_RULE_EXISTS = 0xBFFA301C
    WRTD_ERROR_RULE_DOES_NOT_EXIST = 0xBFFA301D
    WRTD_ERROR_RULE_OUT_OF_RESOURCES = 0xBFFA301E
    WRTD_ERROR_RULE_INVALID = 0xBFFA301F
    WRTD_ERROR_RULE_ENABLED = 0xBFFA3020
    WRTD_ERROR_CANT_REMOVE_RESERVED_REP_CAP = 0xBFFA3021
    __WRTD_ERROR_MAX_NUMBER = 0xBFFA3022


    __WRTD_ATTR_BASE = 950000
    WRTD_MAJOR_VERSION = 950001
    WRTD_MINOR_VERSION = 950002
    WRTD_ATTR_EVENT_LOG_ENTRY_COUNT = 950003
    WRTD_ATTR_EVENT_LOG_ENABLED = 950004
    WRTD_ATTR_IS_TIME_MASTER = 950005
    WRTD_ATTR_IS_TIME_SYNCHRONIZED = 950006
    WRTD_ATTR_ALARM_COUNT = 950007
    WRTD_ATTR_ALARM_ENABLED = 950008
    WRTD_ATTR_ALARM_SETUP_TIME = 950009
    WRTD_ATTR_ALARM_TIME = 950010
    WRTD_ATTR_ALARM_PERIOD = 950011
    WRTD_ATTR_ALARM_REPEAT_COUNT = 950012
    WRTD_ATTR_RULE_COUNT = 950013
    WRTD_ATTR_RULE_ENABLED = 950014
    WRTD_ATTR_RULE_REPEAT_COUNT = 950015
    WRTD_ATTR_RULE_SOURCE = 950016
    WRTD_ATTR_RULE_DESTINATION = 950017
    WRTD_ATTR_RULE_SEND_LATE = 950018
    WRTD_ATTR_RULE_DELAY = 950019
    WRTD_ATTR_RULE_HOLDOFF = 950020
    WRTD_ATTR_RULE_RESYNC_PERIOD = 950021
    WRTD_ATTR_RULE_RESYNC_FACTOR = 950022

    WRTD_ATTR_STAT_RULE_RX_EVENTS = 950023
    WRTD_ATTR_STAT_RULE_RX_LAST = 950024
    WRTD_ATTR_STAT_RULE_TX_EVENTS = 950025
    WRTD_ATTR_STAT_RULE_TX_LAST = 950026
    WRTD_ATTR_STAT_RULE_MISSED_EVENTS_LATE = 950027
    WRTD_ATTR_STAT_RULE_MISSED_EVENTS_HOLDOFF = 950028
    WRTD_ATTR_STAT_RULE_MISSED_EVENTS_OVERFLOW = 950029
    WRTD_ATTR_STAT_RULE_MISSED_LAST = 950030

    WRTD_ATTR_STAT_RULE_RX_LATENCY_MIN = 950031
    WRTD_ATTR_STAT_RULE_RX_LATENCY_MAX = 950032
    WRTD_ATTR_STAT_RULE_RX_LATENCY_AVG = 950033
    WRTD_ATTR_STAT_RULE_RX_PERIOD_MIN = 950034
    WRTD_ATTR_STAT_RULE_RX_PERIOD_MAX = 950035
    WRTD_ATTR_STAT_RULE_RX_PERIOD_AVG = 950036
    __WRTD_ATTR_MAX_NUMBER = 950037

    WRTD_GLOBAL_REP_CAP_ID = 'WGRCI'


    __WRTD_MAX_LOG_TYPE_NUMBER = 0

    def __init__(self, resource_name):
        self.wrtd_lib = CDLL("libwrtd.so")

        self.wrtd_init = self.wrtd_lib.wrtd_init
        self.wrtd_init.restype = c_uint
        self.wrtd_init.errcheck = self.__errcheck_int
        self.wrtd_init.argtypes = [c_char_p, c_int, c_char_p,
                                   POINTER(POINTER(wrtd))]
        """self.wrtd_init.argtypes = [c_char_p, c_int, c_char_p,
                                      c_void_p]"""

        self.wrtd_close = self.wrtd_lib.wrtd_close
        self.wrtd_close.restype = c_uint
        self.wrtd_close.errcheck = self.__errcheck_int
        self.wrtd_close.argtypes = [c_void_p]

        self.wrtd_reset = self.wrtd_lib.wrtd_reset
        self.wrtd_reset.restype = c_uint
        self.wrtd_reset.argtypes = [c_void_p]

        self.wrtd_get_error = self.wrtd_lib.wrtd_get_error
        self.wrtd_get_error.restype = c_uint
        self.wrtd_get_error.argtypes = [c_void_p, POINTER(c_uint32),
                                        c_uint, c_char_p]

        self.wrtd_error_message = self.wrtd_lib.wrtd_error_message
        self.wrtd_error_message.restype = c_uint
        self.wrtd_error_message.errcheck = self.__errcheck_int
        self.wrtd_error_message.argtypes = [c_void_p, c_uint, c_char_p]

        self.wrtd_get_attr_int32 = self.wrtd_lib.wrtd_get_attr_int32
        self.wrtd_get_attr_int32.restype = c_uint
        self.wrtd_get_attr_int32.errcheck = self.__errcheck_int
        self.wrtd_get_attr_int32.argtypes = [c_void_p, c_char_p,
                                             c_uint, POINTER(c_int32)]

        self.wrtd_set_attr_int32 = self.wrtd_lib.wrtd_set_attr_int32
        self.wrtd_set_attr_int32.restype = c_uint
        self.wrtd_set_attr_int32.errcheck = self.__errcheck_int
        self.wrtd_set_attr_int32.argtypes = [c_void_p, c_char_p,
                                             c_uint, c_int]

        """self.wrtd_set_attr_int64 = self.wrtd_lib.wrtd_set_attr_int64
           self.wrtd_set_attr_int64.restype = c_uint
           self.wrtd_set_attr_int64.errcheck = self.__errcheck_int
           self.wrtd_set_attr_int64.argtypes = [c_void_p, c_char_p,
                                             c_uint, c_long]"""

        self.wrtd_get_attr_bool = self.wrtd_lib.wrtd_get_attr_bool
        self.wrtd_get_attr_bool.restype = c_uint
        self.wrtd_get_attr_bool.errcheck = self.__errcheck_int
        self.wrtd_get_attr_bool.argtypes = [c_void_p, c_char_p,
                                            c_uint, c_void_p]

        self.wrtd_set_attr_bool = self.wrtd_lib.wrtd_set_attr_bool
        self.wrtd_set_attr_bool.restype = c_uint
        self.wrtd_set_attr_bool.errcheck = self.__errcheck_int
        self.wrtd_set_attr_bool.argtypes = [c_void_p, c_char_p,
                                            c_uint, c_int]

        """self.wrtd_get_attr_tstamp =\
             self.wrtd_lib.wrtd_get_attr_tstamp
           self.wrtd_get_attr_tstamp.restype = c_uint
           self.wrtd_get_attr_tstamp.errcheck = self.__errcheck_int
           self.wrtd_get_attr_tstamp.argtypes = [c_void_p, c_char_p,
                                                   c_uint, c_void_p]"""

        self.wrtd_set_attr_tstamp = self.wrtd_lib.wrtd_set_attr_tstamp
        self.wrtd_set_attr_tstamp.restype = c_uint
        self.wrtd_set_attr_tstamp.errcheck = self.__errcheck_int
        self.wrtd_set_attr_tstamp.argtypes = [c_void_p, c_char_p,
                                              c_uint, c_void_p]

        self.wrtd_set_attr_string = self.wrtd_lib.wrtd_set_attr_string
        self.wrtd_set_attr_string.restype = c_uint
        self.wrtd_set_attr_string.errcheck = self.__errcheck_int
        self.wrtd_set_attr_string.argtypes = [c_void_p, c_char_p,
                                              c_uint, c_char_p]

        """self.wrtd_get_attr_int64 = self.wrtd_lib.wrtd_get_attr_int64
           self.wrtd_get_attr_int64.restype = c_uint
           self.wrtd_get_attr_int64.errcheck = self.__errcheck_int
           self.wrtd_get_attr_int64.argtypes = [c_void_p, c_char_p,
                                                c_uint, c_long]"""

        self.wrtd_get_attr_string = self.wrtd_lib.wrtd_get_attr_string
        self.wrtd_get_attr_string.restype = c_uint
        self.wrtd_get_attr_string.errcheck = self.__errcheck_int
        self.wrtd_get_attr_string.argtypes = [c_void_p, c_char_p,
                                              c_uint, c_int, c_char_p]

        self.wrtd_get_sys_time = self.wrtd_lib.wrtd_get_sys_time
        self.wrtd_get_sys_time.restype = c_uint
        self.wrtd_get_sys_time.errcheck = self.__errcheck_int
        self.wrtd_get_sys_time.argtypes = [c_void_p, c_void_p]

        self.wrtd_log_read = self.wrtd_lib.wrtd_log_read
        self.wrtd_log_read.restype = c_uint
        self.wrtd_log_read.errcheck = self.__errcheck_int
        self.wrtd_log_read.argtypes = [c_void_p, c_void_p, c_int]

        """self.wrtd_clear_log = self.wrtd_lib.wrtd_clear_log
           self.wrtd_clear_log.restype = c_uint
           self.wrtd_clear_log.errcheck = self.__errcheck_int
           self.wrtd_clear_log.argtypes = [c_void_p]"""

        self.wrtd_add_alarm = self.wrtd_lib.wrtd_add_alarm
        self.wrtd_add_alarm.restype = c_uint
        self.wrtd_add_alarm.errcheck = self.__errcheck_int
        self.wrtd_add_alarm.argtypes = [c_void_p, c_char_p]

        self.wrtd_disable_all_alarms =\
            self.wrtd_lib.wrtd_disable_all_alarms
        self.wrtd_disable_all_alarms.restype = c_uint
        self.wrtd_disable_all_alarms.errcheck = self.__errcheck_int
        self.wrtd_disable_all_alarms.argtypes = [c_void_p]

        self.wrtd_remove_alarm = self.wrtd_lib.wrtd_remove_alarm
        self.wrtd_remove_alarm.restype = c_uint
        self.wrtd_remove_alarm.errcheck = self.__errcheck_int
        self.wrtd_remove_alarm.argtypes = [c_void_p, c_char_p]

        self.wrtd_remove_all_alarms =\
            self.wrtd_lib.wrtd_remove_all_alarms
        self.wrtd_remove_all_alarms.restype = c_uint
        self.wrtd_remove_all_alarms.errcheck = self.__errcheck_int
        self.wrtd_remove_all_alarms.argtypes = [c_void_p]

        self.wrtd_get_alarm_id = self.wrtd_lib.wrtd_get_alarm_id
        self.wrtd_get_alarm_id.restype = c_uint
        self.wrtd_get_alarm_id.errcheck = self.__errcheck_int
        self.wrtd_get_alarm_id.argtypes = [c_void_p, c_int,
                                           c_int, c_char_p]

        """rule sources can be a) reserved event ids, b) alarm
           c) any other string which will be interpreted as a net
           msg event id"""
        self.wrtd_add_rule = self.wrtd_lib.wrtd_add_rule
        self.wrtd_add_rule.restype = c_uint
        self.wrtd_add_rule.errcheck = self.__errcheck_int
        self.wrtd_add_rule.argtypes = [c_void_p, c_char_p]

        self.wrtd_disable_all_rules =\
            self.wrtd_lib.wrtd_disable_all_rules
        self.wrtd_disable_all_rules.restype = c_uint
        self.wrtd_disable_all_rules.errcheck = self.__errcheck_int
        self.wrtd_disable_all_rules.argtypes = [c_void_p]

        self.wrtd_remove_rule = self.wrtd_lib.wrtd_remove_rule
        self.wrtd_remove_rule.restype = c_uint
        self.wrtd_remove_rule.errcheck = self.__errcheck_int
        self.wrtd_remove_rule.argtypes = [c_void_p, c_char_p]

        self.wrtd_remove_all_rules =\
            self.wrtd_lib.wrtd_remove_all_rules
        self.wrtd_remove_all_rules.restype = c_uint
        self.wrtd_remove_all_rules.errcheck = self.__errcheck_int
        self.wrtd_remove_all_rules.argtypes = [c_void_p]

        self.wrtd_get_rule_id = self.wrtd_lib.wrtd_get_rule_id
        self.wrtd_get_rule_id.restype = c_uint
        self.wrtd_get_rule_id.errcheck = self.__errcheck_int
        self.wrtd_get_rule_id.argtypes = [c_void_p, c_int, c_int,
                                          c_char_p]

        """self.wrtd_reset_rule_stats =
             self.wrtd_lib.wrtd_reset_rule_stats
           self.wrtd_reset_rule_stats.restype = c_uint
           self.wrtd_reset_rule_stats.errcheck = self.__errcheck_int
           self.wrtd_reset_rule_stats.argtypes = [c_void_p, c_char_p]"""

        self.resource_name = resource_name.encode('utf-8')
        self.wrtd_p = POINTER(wrtd)()
        self.__init(0, None)

    def __del__(self):
        self.__close()

    def __init(self, reset, options_str):
        self.wrtd_init(self.resource_name, reset, options_str,
                       self.wrtd_p)

    def __close(self):
        if not self.wrtd_p:
            self.wrtd_close(self.wrtd_p)
            self.wrtd_p = 0

    def reset(self):
        self.wrtd_reset(self.wrtd_p)

    def get_error(self, buffer_size):
        error_description = create_string_buffer(buffer_size)
        error_c = c_uint()
        self.wrtd_get_error(self.wrtd_p, byref(error_c), buffer_size,
                            error_description)
        return {'error_description': error_description.value,
                'error_code': error_c.value}

    def error_message(self, err_code):
        error_message = create_string_buffer(256)
        self.wrtd_error_message(self.wrtd_p, err_code,
                                error_message)
        return error_message.value

    @encode_arguments
    def get_attr_int32(self, rep_cap_id, id):
        value = c_int32()
        self.wrtd_get_attr_int32(self.wrtd_p, rep_cap_id, id,
                                 byref(value))
        return value.value

    @encode_arguments
    def set_attr_int32(self, rep_cap_id, id, value):
        self.wrtd_set_attr_int32(self.wrtd_p, rep_cap_id, id, value)

    @encode_arguments
    def get_attr_bool(self, rep_cap_id, id):
        value = c_bool()
        self.wrtd_get_attr_bool(self.wrtd_p, rep_cap_id, id,
                                byref(value))
        return value.value

    @encode_arguments
    def set_attr_bool(self, rep_cap_id, id, value):
        self.wrtd_set_attr_bool(self.wrtd_p, rep_cap_id, id, value)

    @encode_arguments
    def set_attr_tstamp(self, rep_cap_id, id, value):
        tstamp = wrtd_tstamp(value["seconds"], value["ns"], value["frac"])
        self.wrtd_set_attr_tstamp(self.wrtd_p, rep_cap_id, id, byref(tstamp))

    @encode_arguments
    def get_attr_string(self, rep_cap_id, id, value_buf_size):
        value = create_string_buffer(value_buf_size)
        self.wrtd_get_attr_string(self.wrtd_p, rep_cap_id, id,
                                  value_buf_size, value)
        return value.value

    @encode_arguments
    def set_attr_string(self, rep_cap_id, id, value):
        self.wrtd_set_attr_string(self.wrtd_p, rep_cap_id, id, value)

    def get_sys_time(self):
        def getdict(struct):
            return dict((field, getattr(struct, field)) for field,
                        _ in struct._fields_)
        tstamp = wrtd_tstamp()
        self.wrtd_get_sys_time(self.wrtd_p, byref(tstamp))
        return getdict(tstamp)

    def log_read(self, poll_timeout):
        def getdict(struct):
            return dict((field, getattr(struct, field)) for field,
                        _ in struct._fields_)
        log = wrtd_log_entry()
        self.wrtd_log_read(self.wrtd_p, byref(log), poll_timeout)
        """TODO think of smarter way to do it"""
        log = getdict(log)
        log['wrtd_event'] = getdict(log['wrtd_event'])
        log['wrtd_tstamp'] = getdict(log['wrtd_tstamp'])
        log['wrtd_event']['wrtd_tstamp'] =\
            getdict(log['wrtd_event']['wrtd_tstamp'])
        return log

    def add_alarm(self, rep_cap_id):
        self.wrtd_add_alarm(self.wrtd_p, rep_cap_id)

    def disable_all_alarms(self):
        self.wrtd_disable_all_alarms(self.wrtd_p)

    def remove_alarm(self, rep_cap_id):
        self.wrtd_remove_alarm(self.wrtd_p, rep_cap_id)

    def get_alarm_id(self, index, name_buffer_size):
        rep_cap_id = create_string_buffer(name_buffer_size)
        self.wrtd_get_alarm_id(self.wrtd_p, index, name_buffer_size,
                               rep_cap_id)
        return rep_cap_id.value

    @encode_arguments
    def add_rule(self, rep_cap_id):
        self.wrtd_add_rule(self.wrtd_p, rep_cap_id)

    def disable_all_rules(self):
        self.wrtd_disable_all_rules(self.wrtd_p)

    def remove_rule(self, rep_cap_id):
        self.wrtd_remove_rule(self.wrtd_p, rep_cap_id)

    def remove_all_rules(self):
        self.wrtd_remove_all_rules(self.wrtd_p)

    def get_rule_id(self, index, name_buffer_size):
        rep_cap_id = create_string_buffer(name_buffer_size)
        self.wrtd_get_rule_id(self.wrtd_p, index, name_buffer_size,
                              rep_cap_id)
        return rep_cap_id.value

    # TODO check if works correctly
    def __errcheck_int(self, ret, func, args):
        """Generic error checker for functions returning 0 as success
        and -1 as error"""
        if ret != self.WRTD_SUCCESS:
            error_code = c_uint()
            error_description = create_string_buffer(256)
            self.wrtd_get_error(self.wrtd_p, byref(error_code), 256,
                                error_description)
            raise OSError(ret, str(error_description.value),
                          "")
        else:
            return ret
