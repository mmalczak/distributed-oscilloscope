"""
Wrapper for WRTD C library using ctypes.

All ctypes functions have exactly the same names as the ones in the
C library. To each C function corresponds a Python function that hides
C specific operations from the user. The names of these functions are
the sames as the ctypes functions without the WRTD prefix.

Copyright (c) 2019 CERN (home.cern)

SPDX-License-Identifier: LGPL-3.0-or-later

"""

import decorator
from ctypes import *

class wrtd_dev(Structure):
    pass

class wrtd_tstamp(Structure):
    _fields_ = [("seconds", c_uint32),
                ("ns", c_uint32),
                ("frac", c_uint32)]

    def __init__(self, seconds = 0, ns = 0, frac = 0):
        self.seconds = int(seconds)
        self.ns      = int(ns)
        self.frac    = int(frac)

    def __iter__(self):
        yield 'seconds', self.seconds
        yield 'ns'     , self.ns
        yield 'frac'   , self.frac

@decorator.decorator
def encode_arguments(func, *args, **kwargs):
    """Used to convert arguments from strings to bytes"""
    encoded = []
    for arg in args:
        if(type(arg) == str):
            encoded.append(arg.encode('utf-8'))
        else:
            encoded.append(arg)
    args = tuple(encoded)
    return func(*args, **kwargs)

class PyWrtd():
    """Top-level Python wrapper class for WRTD library.

    :param resource_name: Underlying MockTurtle device ID in the form of ``MTxxx`` or\
    ``trtl-xxxx``. See also :ref:`node_id`.

    """

    WRTD_SUCCESS                      = 0
    __WRTD_ERROR_BASE                 = 0xBFFA0000
    WRTD_ERROR_INVALID_ATTRIBUTE      = __WRTD_ERROR_BASE + 0x0C
    WRTD_ERROR_ATTR_NOT_WRITEABLE     = __WRTD_ERROR_BASE + 0x0D
    WRTD_ERROR_ATTR_NOT_READABLE      = __WRTD_ERROR_BASE + 0x0E
    WRTD_ERROR_INVALID_VALUE          = __WRTD_ERROR_BASE + 0x10
    WRTD_ERROR_NOT_INITIALIZED        = __WRTD_ERROR_BASE + 0x1D
    WRTD_ERROR_UNKNOWN_CHANNEL_NAME   = __WRTD_ERROR_BASE + 0x20
    WRTD_ERROR_OUT_OF_MEMORY          = __WRTD_ERROR_BASE + 0x56
    WRTD_ERROR_NULL_POINTER           = __WRTD_ERROR_BASE + 0x58
    WRTD_ERROR_UNEXPECTED_RESPONSE    = __WRTD_ERROR_BASE + 0x59
    WRTD_ERROR_RESOURCE_UNKNOWN       = __WRTD_ERROR_BASE + 0x60
    WRTD_ERROR_BADLY_FORMED_SELECTOR  = __WRTD_ERROR_BASE + 0x66
    __WRTD_LXISYNC_ERROR_BASE         = 0xBFFA3000
    WRTD_ERROR_ALARM_EXISTS           = __WRTD_LXISYNC_ERROR_BASE + 0x07
    WRTD_ERROR_ALARM_DOES_NOT_EXIST   = __WRTD_LXISYNC_ERROR_BASE + 0x08
    __WRTD_SPECIFIC_ERROR_BASE        = 0xBFFA6000
    WRTD_ERROR_VERSION_MISMATCH       = __WRTD_SPECIFIC_ERROR_BASE + 0x00
    WRTD_ERROR_INTERNAL               = __WRTD_SPECIFIC_ERROR_BASE + 0x01
    WRTD_ERROR_UNKNOWN_LOG_TYPE       = __WRTD_SPECIFIC_ERROR_BASE + 0x02
    WRTD_ERROR_RESOURCE_ACTIVE        = __WRTD_SPECIFIC_ERROR_BASE + 0x03
    WRTD_ERROR_ATTR_GLOBAL            = __WRTD_SPECIFIC_ERROR_BASE + 0x04
    WRTD_ERROR_OUT_OF_RESOURCES       = __WRTD_SPECIFIC_ERROR_BASE + 0x05
    WRTD_ERROR_RULE_EXISTS            = __WRTD_SPECIFIC_ERROR_BASE + 0x06
    WRTD_ERROR_RULE_DOES_NOT_EXIST    = __WRTD_SPECIFIC_ERROR_BASE + 0x07

    __WRTD_ATTR_BASE                    = 1150000
    WRTD_ATTR_EVENT_LOG_EMPTY           = __WRTD_ATTR_BASE + 0x00
    WRTD_ATTR_EVENT_LOG_ENABLED         = __WRTD_ATTR_BASE + 0x01
    WRTD_ATTR_IS_TIME_SYNCHRONIZED      = __WRTD_ATTR_BASE + 0x02
    WRTD_ATTR_SYS_TIME                  = __WRTD_ATTR_BASE + 0x03
    WRTD_ATTR_ALARM_COUNT               = __WRTD_ATTR_BASE + 0x10
    WRTD_ATTR_ALARM_ENABLED             = __WRTD_ATTR_BASE + 0x11
    WRTD_ATTR_ALARM_SETUP_TIME          = __WRTD_ATTR_BASE + 0x12
    WRTD_ATTR_ALARM_TIME                = __WRTD_ATTR_BASE + 0x13
    WRTD_ATTR_ALARM_PERIOD              = __WRTD_ATTR_BASE + 0x14
    WRTD_ATTR_ALARM_REPEAT_COUNT        = __WRTD_ATTR_BASE + 0x15
    WRTD_ATTR_RULE_COUNT                = __WRTD_ATTR_BASE + 0x20
    WRTD_ATTR_RULE_ENABLED              = __WRTD_ATTR_BASE + 0x21
    WRTD_ATTR_RULE_REPEAT_COUNT         = __WRTD_ATTR_BASE + 0x22
    WRTD_ATTR_RULE_SOURCE               = __WRTD_ATTR_BASE + 0x23
    WRTD_ATTR_RULE_DESTINATION          = __WRTD_ATTR_BASE + 0x24
    WRTD_ATTR_RULE_SEND_LATE            = __WRTD_ATTR_BASE + 0x25
    WRTD_ATTR_RULE_DELAY                = __WRTD_ATTR_BASE + 0x26
    WRTD_ATTR_RULE_HOLDOFF              = __WRTD_ATTR_BASE + 0x27
    WRTD_ATTR_RULE_RESYNC_PERIOD        = __WRTD_ATTR_BASE + 0x28
    WRTD_ATTR_RULE_RESYNC_FACTOR        = __WRTD_ATTR_BASE + 0x29
    WRTD_ATTR_STAT_RULE_RX_EVENTS       = __WRTD_ATTR_BASE + 0x30
    WRTD_ATTR_STAT_RULE_RX_LAST         = __WRTD_ATTR_BASE + 0x31
    WRTD_ATTR_STAT_RULE_TX_EVENTS       = __WRTD_ATTR_BASE + 0x32
    WRTD_ATTR_STAT_RULE_TX_LAST         = __WRTD_ATTR_BASE + 0x33
    WRTD_ATTR_STAT_RULE_MISSED_LATE     = __WRTD_ATTR_BASE + 0x34
    WRTD_ATTR_STAT_RULE_MISSED_HOLDOFF  = __WRTD_ATTR_BASE + 0x35
    WRTD_ATTR_STAT_RULE_MISSED_NOSYNC   = __WRTD_ATTR_BASE + 0x36
    WRTD_ATTR_STAT_RULE_MISSED_OVERFLOW = __WRTD_ATTR_BASE + 0x37
    WRTD_ATTR_STAT_RULE_MISSED_LAST     = __WRTD_ATTR_BASE + 0x38
    WRTD_ATTR_STAT_RULE_RX_LATENCY_MIN  = __WRTD_ATTR_BASE + 0x39
    WRTD_ATTR_STAT_RULE_RX_LATENCY_MAX  = __WRTD_ATTR_BASE + 0x3A
    WRTD_ATTR_STAT_RULE_RX_LATENCY_AVG  = __WRTD_ATTR_BASE + 0x3B
    WRTD_ATTR_FW_COUNT                  = __WRTD_ATTR_BASE + 0x80
    WRTD_ATTR_FW_MAJOR_VERSION          = __WRTD_ATTR_BASE + 0x81
    WRTD_ATTR_FW_MINOR_VERSION          = __WRTD_ATTR_BASE + 0x82
    WRTD_ATTR_FW_MAJOR_VERSION_REQUIRED = __WRTD_ATTR_BASE + 0x83
    WRTD_ATTR_FW_MINOR_VERSION_REQUIRED = __WRTD_ATTR_BASE + 0x84
    WRTD_ATTR_FW_MAX_RULES              = __WRTD_ATTR_BASE + 0x85
    WRTD_ATTR_FW_MAX_ALARMS             = __WRTD_ATTR_BASE + 0x86
    WRTD_ATTR_FW_CAPABILITIES           = __WRTD_ATTR_BASE + 0x88
    WRTD_ATTR_FW_LOCAL_INPUTS           = __WRTD_ATTR_BASE + 0x8A
    WRTD_ATTR_FW_LOCAL_OUTPUTS          = __WRTD_ATTR_BASE + 0x8B

    WRTD_GLOBAL_REP_CAP_ID = 'WGRCI'

    WRTD_LOG_ENTRY_SIZE = 120

    def __init__(self, resource_name):
        self.wrtd_lib = CDLL("libwrtd.so")

        self.wrtd_lib.wrtd_init.restype  = c_int
        self.wrtd_lib.wrtd_init.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_init.argtypes = [c_char_p, c_bool, c_char_p,
                                            POINTER(POINTER(wrtd_dev))]

        self.wrtd_lib.wrtd_close.restype  = c_int
        self.wrtd_lib.wrtd_close.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_close.argtypes = [POINTER(wrtd_dev)]

        self.wrtd_lib.wrtd_reset.restype  = c_int
        self.wrtd_lib.wrtd_reset.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_reset.argtypes = [POINTER(wrtd_dev)]

        self.wrtd_lib.wrtd_get_error.restype  = c_int
        # No errcheck on the get_error function, it is used internally
        # by self._errcheck and might lead to recursive errors
        self.wrtd_lib.wrtd_get_error.argtypes = [POINTER(wrtd_dev),
                                                 POINTER(c_int),
                                                 c_int32, c_char_p]

        self.wrtd_lib.wrtd_error_message.restype  = c_int
        self.wrtd_lib.wrtd_error_message.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_error_message.argtypes = [POINTER(wrtd_dev),
                                                     c_uint, c_char_p]

        self.wrtd_lib.wrtd_set_attr_bool.restype  = c_int
        self.wrtd_lib.wrtd_set_attr_bool.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_set_attr_bool.argtypes = [POINTER(wrtd_dev),
                                                     c_char_p,
                                                     c_uint, c_bool]

        self.wrtd_lib.wrtd_get_attr_bool.restype  = c_int
        self.wrtd_lib.wrtd_get_attr_bool.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_get_attr_bool.argtypes = [POINTER(wrtd_dev),
                                                     c_char_p,
                                                     c_uint, POINTER(c_bool)]

        self.wrtd_lib.wrtd_set_attr_int32.restype  = c_int
        self.wrtd_lib.wrtd_set_attr_int32.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_set_attr_int32.argtypes = [POINTER(wrtd_dev),
                                                      c_char_p,
                                                      c_uint, c_int32]

        self.wrtd_lib.wrtd_get_attr_int32.restype  = c_int
        self.wrtd_lib.wrtd_get_attr_int32.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_get_attr_int32.argtypes = [POINTER(wrtd_dev),
                                                      c_char_p,
                                                      c_uint, POINTER(c_int32)]

        self.wrtd_lib.wrtd_set_attr_string.restype  = c_int
        self.wrtd_lib.wrtd_set_attr_string.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_set_attr_string.argtypes = [POINTER(wrtd_dev),
                                                       c_char_p,
                                                       c_uint, c_char_p]

        self.wrtd_lib.wrtd_get_attr_string.restype  = c_int
        self.wrtd_lib.wrtd_get_attr_string.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_get_attr_string.argtypes = [POINTER(wrtd_dev),
                                                       c_char_p, c_uint,
                                                       c_int32, c_char_p]

        self.wrtd_lib.wrtd_set_attr_tstamp.restype  = c_int
        self.wrtd_lib.wrtd_set_attr_tstamp.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_set_attr_tstamp.argtypes = [POINTER(wrtd_dev),
                                                       c_char_p, c_uint,
                                                       POINTER(wrtd_tstamp)]

        self.wrtd_lib.wrtd_get_attr_tstamp.restype  = c_int
        self.wrtd_lib.wrtd_get_attr_tstamp.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_get_attr_tstamp.argtypes = [POINTER(wrtd_dev),
                                                       c_char_p, c_uint,
                                                       POINTER(wrtd_tstamp)]

        self.wrtd_lib.wrtd_clear_event_log_entries.restype  = c_int
        self.wrtd_lib.wrtd_clear_event_log_entries.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_clear_event_log_entries.argtypes = [POINTER(wrtd_dev)]

        self.wrtd_lib.wrtd_get_next_event_log_entry.restype  = c_int
        self.wrtd_lib.wrtd_get_next_event_log_entry.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_get_next_event_log_entry.argtypes = [POINTER(wrtd_dev),
                                                                c_int32, c_char_p]

        self.wrtd_lib.wrtd_add_alarm.restype  = c_int
        self.wrtd_lib.wrtd_add_alarm.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_add_alarm.argtypes = [POINTER(wrtd_dev), c_char_p]

        self.wrtd_lib.wrtd_disable_all_alarms.restype  = c_int
        self.wrtd_lib.wrtd_disable_all_alarms.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_disable_all_alarms.argtypes = [POINTER(wrtd_dev)]

        self.wrtd_lib.wrtd_remove_alarm.restype  = c_int
        self.wrtd_lib.wrtd_remove_alarm.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_remove_alarm.argtypes = [POINTER(wrtd_dev), c_char_p]

        self.wrtd_lib.wrtd_remove_all_alarms.restype  = c_int
        self.wrtd_lib.wrtd_remove_all_alarms.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_remove_all_alarms.argtypes = [POINTER(wrtd_dev)]

        self.wrtd_lib.wrtd_get_alarm_name.restype  = c_int
        self.wrtd_lib.wrtd_get_alarm_name.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_get_alarm_name.argtypes = [POINTER(wrtd_dev), c_int32,
                                                      c_int32, c_char_p]

        self.wrtd_lib.wrtd_add_rule.restype  = c_int
        self.wrtd_lib.wrtd_add_rule.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_add_rule.argtypes = [POINTER(wrtd_dev), c_char_p]

        self.wrtd_lib.wrtd_disable_all_rules.restype  = c_int
        self.wrtd_lib.wrtd_disable_all_rules.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_disable_all_rules.argtypes = [POINTER(wrtd_dev)]

        self.wrtd_lib.wrtd_remove_rule.restype  = c_int
        self.wrtd_lib.wrtd_remove_rule.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_remove_rule.argtypes = [POINTER(wrtd_dev), c_char_p]

        self.wrtd_lib.wrtd_remove_all_rules.restype  = c_int
        self.wrtd_lib.wrtd_remove_all_rules.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_remove_all_rules.argtypes = [POINTER(wrtd_dev)]

        self.wrtd_lib.wrtd_get_rule_name.restype  = c_int
        self.wrtd_lib.wrtd_get_rule_name.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_get_rule_name.argtypes = [POINTER(wrtd_dev), c_int32,
                                                     c_int32, c_char_p]

        self.wrtd_lib.wrtd_reset_rule_stats.restype  = c_int
        self.wrtd_lib.wrtd_reset_rule_stats.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_reset_rule_stats.argtypes = [POINTER(wrtd_dev), c_char_p]

        self.wrtd_lib.wrtd_get_fw_name.restype  = c_int
        self.wrtd_lib.wrtd_get_fw_name.errcheck = self.__errcheck
        self.wrtd_lib.wrtd_get_fw_name.argtypes = [POINTER(wrtd_dev), c_int32,
                                                   c_int32, c_char_p]

        self.resource_name = resource_name.encode('utf-8')
        self.wrtd_p = POINTER(wrtd_dev)()
        ret = self.wrtd_lib.wrtd_init(self.resource_name, 0, None, byref(self.wrtd_p))

    def __del__(self):
        if self.wrtd_p:
            self.wrtd_lib.wrtd_close(self.wrtd_p)
            self.wrtd_p = 0

    def reset(self):
        """
        Corresponds to C library :cpp:func:`wrtd_reset`.
        """
        self.wrtd_lib.wrtd_reset(self.wrtd_p)

    def get_error(self):
        """
        Corresponds to C library :cpp:func:`wrtd_get_error`.

        :return: a tuple with the :ref:`Error Code <api_error_codes>` and the error message.
        """
        buf_size = self.wrtd_lib.wrtd_get_error(self.wrtd_p, None, 0, None)
        error_description = create_string_buffer(buf_size)
        error_c = c_int()
        self.wrtd_lib.wrtd_get_error(self.wrtd_p, byref(error_c),
                                     buf_size, error_description)
        return error_c.value, error_description.value.decode('ascii')

    def error_message(self, err_code):
        """
        Corresponds to C library :cpp:func:`wrtd_error_message`.

        :param err_code: error code to convert

        :return: error message (string)
        """
        error_message = create_string_buffer(256)
        self.wrtd_lib.wrtd_error_message(self.wrtd_p, err_code,
                                         error_message)
        return error_message.value.decode('ascii')

    @encode_arguments
    def set_attr_bool(self, rep_cap_id, id, value):
        """
        Corresponds to C library :cpp:func:`wrtd_set_attr_bool`.

        :param rep_cap_id: :ref:`rep_cap_id`
        :param id: ID of concerned :ref:`attribute`
        :param value: Value to write to the :ref:`attribute`
        """
        self.wrtd_lib.wrtd_set_attr_bool(self.wrtd_p, rep_cap_id,
                                         id, value)

    @encode_arguments
    def get_attr_bool(self, rep_cap_id, id):
        """
        Corresponds to C library :cpp:func:`wrtd_get_attr_bool`.

        :param rep_cap_id: :ref:`rep_cap_id`
        :param id: ID of concerned :ref:`attribute`

        :return: Retrieved attribute value
        """
        value = c_bool()
        self.wrtd_lib.wrtd_get_attr_bool(self.wrtd_p, rep_cap_id,
                                         id, byref(value))
        return value.value

    @encode_arguments
    def set_attr_int32(self, rep_cap_id, id, value):
        """
        Corresponds to C library :cpp:func:`wrtd_set_attr_int32`.

        :param rep_cap_id: :ref:`rep_cap_id`
        :param id: ID of concerned :ref:`attribute`
        :param value: Value to write to the :ref:`attribute`
        """
        self.wrtd_lib.wrtd_set_attr_int32(self.wrtd_p, rep_cap_id,
                                          id, value)

    @encode_arguments
    def get_attr_int32(self, rep_cap_id, id):
        """
        Corresponds to C library :cpp:func:`wrtd_get_attr_int32`.

        :param rep_cap_id: :ref:`rep_cap_id`
        :param id: ID of concerned :ref:`attribute`

        :return: Retrieved attribute value
        """
        value = c_int32()
        self.wrtd_lib.wrtd_get_attr_int32(self.wrtd_p, rep_cap_id,
                                          id, byref(value))
        return value.value

    @encode_arguments
    def set_attr_string(self, rep_cap_id, id, value):
        """
        Corresponds to C library :cpp:func:`wrtd_set_attr_string`.

        :param rep_cap_id: :ref:`rep_cap_id`
        :param id: ID of concerned :ref:`attribute`
        :param value: Value to write to the :ref:`attribute`
        """
        self.wrtd_lib.wrtd_set_attr_string(self.wrtd_p, rep_cap_id,
                                           id, value)

    @encode_arguments
    def get_attr_string(self, rep_cap_id, id):
        """
        Corresponds to C library :cpp:func:`wrtd_get_attr_string`.

        :param rep_cap_id: :ref:`rep_cap_id`
        :param id: ID of concerned :ref:`attribute`

        :return: Retrieved attribute value
        """
        buf_size = self.wrtd_lib.wrtd_get_attr_string(self.wrtd_p,
                                                      rep_cap_id, id,
                                                      0, None)
        value = create_string_buffer(buf_size)
        self.wrtd_lib.wrtd_get_attr_string(self.wrtd_p, rep_cap_id,
                                           id, buf_size, value)
        return value.value.decode('ascii')

    @encode_arguments
    def set_attr_tstamp(self, rep_cap_id, id,
                        seconds = 0, ns = 0, frac = 0):
        """
        Corresponds to C library :cpp:func:`wrtd_set_attr_tstamp`.

        :param rep_cap_id: :ref:`rep_cap_id`
        :param id: ID of concerned :ref:`attribute`
        :param seconds: Seconds value to write to the :ref:`attribute`
        :param ns: Nanoseconds value to write to the :ref:`attribute`
        :param frac: Fractional nanoseconds value to write to the :ref:`attribute`
        """
        tstamp = wrtd_tstamp(seconds, ns, frac)
        self.wrtd_lib.wrtd_set_attr_tstamp(self.wrtd_p, rep_cap_id,
                                           id, byref(tstamp))

    @encode_arguments
    def get_attr_tstamp(self, rep_cap_id, id):
        """
        Corresponds to C library :cpp:func:`wrtd_get_attr_tstamp`.

        :param rep_cap_id: :ref:`rep_cap_id`
        :param id: ID of concerned :ref:`attribute`

        :return: Retrieved attribute value\
        (Python dictionary with ``seconds``, ``ns`` and ``frac`` keys)
        """
        tstamp = wrtd_tstamp()
        self.wrtd_lib.wrtd_get_attr_tstamp(self.wrtd_p, rep_cap_id,
                                           id, byref(tstamp))
        return dict(tstamp)

    def clear_event_log_entries(self):
        """
        Corresponds to C library :cpp:func:`wrtd_clear_event_log_entries`.
        """
        self.wrtd_lib.wrtd_clear_event_log_entries(self.wrtd_p)

    def get_next_event_log_entry(self):
        """
        Corresponds to C library :cpp:func:`wrtd_get_next_event_log_entry`.
        """
        buf_size = self.WRTD_LOG_ENTRY_SIZE
        log_entry = create_string_buffer(buf_size)
        self.wrtd_lib.wrtd_get_next_event_log_entry(self.wrtd_p,
                                                    buf_size,
                                                    log_entry)
        return log_entry.value.decode('ascii')

    @encode_arguments
    def add_alarm(self, rep_cap_id):
        """
        Corresponds to C library :cpp:func:`wrtd_add_alarm`.

        :param rep_cap_id: :ref:`rep_cap_id` of new :ref:`alarm`
        """
        self.wrtd_lib.wrtd_add_alarm(self.wrtd_p, rep_cap_id)

    def disable_all_alarms(self):
        """
        Corresponds to C library :cpp:func:`wrtd_disable_all_alarms`.
        """
        self.wrtd_lib.wrtd_disable_all_alarms(self.wrtd_p)

    @encode_arguments
    def remove_alarm(self, rep_cap_id):
        """
        Corresponds to C library :cpp:func:`wrtd_remove_alarm`.

        :param rep_cap_id: :ref:`rep_cap_id` of :ref:`alarm` to remove
        """
        self.wrtd_lib.wrtd_remove_alarm(self.wrtd_p, rep_cap_id)

    def remove_all_alarms(self):
        """
        Corresponds to C library :cpp:func:`wrtd_remove_all_alarms`.
        """
        self.wrtd_lib.wrtd_remove_all_alarms(self.wrtd_p)

    def get_alarm_name(self, index):
        """
        Corresponds to C library :cpp:func:`wrtd_get_alarm_name`.

        :param index: Index of the :ref:`alarm`

        :return: :ref:`rep_cap_id` of the :ref:`alarm`
        """
        buf_size = self.wrtd_lib.wrtd_get_alarm_name(self.wrtd_p,
                                                     index,
                                                     0, None)
        name = create_string_buffer(buf_size)
        self.wrtd_lib.wrtd_get_alarm_name(self.wrtd_p, index,
                                          buf_size, name)
        return name.value.decode('ascii')

    @encode_arguments
    def add_rule(self, rep_cap_id):
        """
        Corresponds to C library :cpp:func:`wrtd_add_rule`.

        :param rep_cap_id: :ref:`rep_cap_id` of new :ref:`rule`
        """
        self.wrtd_lib.wrtd_add_rule(self.wrtd_p, rep_cap_id)

    def disable_all_rules(self):
        """
        Corresponds to C library :cpp:func:`wrtd_disable_all_alarms`.
        """
        self.wrtd_lib.wrtd_disable_all_rules(self.wrtd_p)

    @encode_arguments
    def remove_rule(self, rep_cap_id):
        """
        Corresponds to C library :cpp:func:`wrtd_remove_rule`.

        :param rep_cap_id: :ref:`rep_cap_id` of :ref:`rule` to remove
        """
        self.wrtd_lib.wrtd_remove_rule(self.wrtd_p, rep_cap_id)

    def remove_all_rules(self):
        """
        Corresponds to C library :cpp:func:`wrtd_remove_all_rules`.
        """
        self.wrtd_lib.wrtd_remove_all_rules(self.wrtd_p)

    def get_rule_name(self, index):
        """
        Corresponds to C library :cpp:func:`wrtd_get_rule_name`.

        :param index: Index of the :ref:`rule`

        :return: :ref:`rep_cap_id` of the :ref:`rule`
        """
        buf_size = self.wrtd_lib.wrtd_get_rule_name(self.wrtd_p,
                                                    index,
                                                    0, None)
        name = create_string_buffer(buf_size)
        self.wrtd_lib.wrtd_get_rule_name(self.wrtd_p, index,
                                         buf_size, name)
        return name.value.decode('ascii')

    @encode_arguments
    def reset_rule_stats(self, rep_cap_id):
        """
        Corresponds to C library :cpp:func:`wrtd_reset_rule_stats`.

        :param rep_cap_id: :ref:`rep_cap_id` of the :ref:`rule` to reset its statistics
        """
        self.wrtd_lib.wrtd_reset_rule_stats(self.wrtd_p, rep_cap_id)

    def get_fw_name(self, index):
        """
        Corresponds to C library :cpp:func:`wrtd_get_fw_name`.

        :param index: Index of the :ref:`application`

        :return: :ref:`rep_cap_id` of the :ref:`application`
        """
        buf_size = self.wrtd_lib.wrtd_get_fw_name(self.wrtd_p,
                                                  index,
                                                  0, None)
        name = create_string_buffer(buf_size)
        self.wrtd_lib.wrtd_get_fw_name(self.wrtd_p, index,
                                       buf_size, name)
        return name.value.decode('ascii')

    def __errcheck(self, ret, func, args):
        """Generic error checker for WRTD functions"""
        if ret < self.WRTD_SUCCESS:
            if self.wrtd_p:
                code, msg = self.get_error()
            else:
                code, msg = ret, self.error_message(ret)
            raise OSError(ret, 'Error {0}: {1}'.format(hex(code% (1 << 32)), msg))
        else:
            return ret
