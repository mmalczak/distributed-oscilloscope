from ctypes import *


class wrtd(Structure):
    pass


class wrtd_tstamp(Structure):
    _fields_ = [("seconds", c_uint),
                ("ns", c_uint),
                ("frac", c_uint)]


class WRTD_wrapper():
    """@enum wrtd_status
        White Rabbit Trigger Distribution warnings and errors

        enum wrtd_status {
             Codes inspired by IVI 3.2"""
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

    """Resource (alar, rule) is not disabled and cannot be changed"""
    WRTD_ERROR_RESOURCE_ACTIVE = 0xBFFA3011

    """Require global rep cap"""
    WRTD_ERROR_ATTR_INVALID_REP_CAP = 0xBFFA3012

    """Feature not implemented"""
    WRTD_ERROR_NOT_IMPLEMENTED = 0xBFFA3013

    """Incorrect repeated capability id: too long, 
       invalid character..."""
    WRTD_ERROR_BAD_REP_CAP_ID = 0xBFFA3014

    """Timeout while reading log"""
    WRTD_ERROR_TIMEOUT = 0xBFFA3015

    """Output buffer is not long enough."""
    WRTD_ERROR_BUFFER_TOO_SHORT = 0xBFFA3016

    WRTD_ERROR_UNKNOWN_NAME_IN_SELECTOR = 0xBFFA3017
    """NOTE: selector == rep_cap_id"""

    """Codes inspired by IviLxiSync
       3.15"""
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

    """@enum wrtd_attr
      White Rabbit Trigger Distribution attribute ID definions"""

    """enum wrtd_attr"""
    __WRTD_ATTR_BASE = 950000
    WRTD_MAJOR_VERSION = 950001
    WRTD_MINOR_VERSION = 950002
    WRTD_ATTR_EVENT_LOG_ENTRY_COUNT = 950003
    WRTD_ATTR_EVENT_LOG_ENABLED = 950004
    """TODO: add log levelsmasks here"""
    WRTD_ATTR_IS_TIME_MASTER = 950005
    WRTD_ATTR_IS_TIME_SYNCHRONIZED = 950006
    """Number of alarms (global attribute)"""
    WRTD_ATTR_ALARM_COUNT = 950007
    """Enabledisable an alarm"""
    WRTD_ATTR_ALARM_ENABLED = 950008
    WRTD_ATTR_ALARM_SETUP_TIME = 950009
    WRTD_ATTR_ALARM_TIME = 950010
    """Specifies the alarm period. 0 means no repetitions."""
    WRTD_ATTR_ALARM_PERIOD = 950011
    """Specifies the number of times the alarm will occur at the period
       specified by WRTD_ATTR_ALARM_PERIOD. 0 means infinite. 1 means
       exactly one alarm will occur"""
    WRTD_ATTR_ALARM_REPEAT_COUNT = 950012
    """Number of rules (global attribute)."""
    WRTD_ATTR_RULE_COUNT = 950013
    """True if the rule is enabled (ie active)"""
    WRTD_ATTR_RULE_ENABLED = 950014
    """Number of time the rule will apply.  0 means infinite.
       When read, return the remaining number"""
    WRTD_ATTR_RULE_REPEAT_COUNT = 950015
    """Source of the event."""
    WRTD_ATTR_RULE_SOURCE = 950016
    """Destination of the event."""
    WRTD_ATTR_RULE_DESTINATION = 950017
    """If true, events from the past are still handled; otherwise they
       are discarded"""
    WRTD_ATTR_RULE_SEND_LATE = 950018
    """Delay the event."""
    WRTD_ATTR_RULE_DELAY = 950019
    """Discard new events between the last one to this value"""
    WRTD_ATTR_RULE_HOLDOFF = 950020
    """Realign the timestamp to a multiple of period and then add factor
       period. This is done after the delay"""
    WRTD_ATTR_RULE_RESYNC_PERIOD = 950021
    WRTD_ATTR_RULE_RESYNC_FACTOR = 950022

    """TODO: add __ boundaries between groups to make it easier to do
       input validation"""
    WRTD_ATTR_STAT_RULE_RX_EVENTS = 950023
    WRTD_ATTR_STAT_RULE_RX_LAST = 950024
    WRTD_ATTR_STAT_RULE_TX_EVENTS = 950025
    WRTD_ATTR_STAT_RULE_TX_LAST = 950026
    WRTD_ATTR_STAT_RULE_MISSED_EVENTS_LATE = 950027
    WRTD_ATTR_STAT_RULE_MISSED_EVENTS_HOLDOFF = 950028
    WRTD_ATTR_STAT_RULE_MISSED_EVENTS_OVERFLOW = 950029
    WRTD_ATTR_STAT_RULE_MISSED_LAST = 950030

    """Latency and period (excluding events discarded due to holdoff)"""
    WRTD_ATTR_STAT_RULE_RX_LATENCY_MIN = 950031
    WRTD_ATTR_STAT_RULE_RX_LATENCY_MAX = 950032
    WRTD_ATTR_STAT_RULE_RX_LATENCY_AVG = 950033
    WRTD_ATTR_STAT_RULE_RX_PERIOD_MIN = 950034
    WRTD_ATTR_STAT_RULE_RX_PERIOD_MAX = 950035
    WRTD_ATTR_STAT_RULE_RX_PERIOD_AVG = 950036
    __WRTD_ATTR_MAX_NUMBER = 950037

    """A repeated capability identifier for global attributes"""
    WRTD_GLOBAL_REP_CAP_ID = "WGRCI"

    """@enum wrtd_log_type
       White Rabbit Trigger Distribution log entry type"""

    """enum wrtd_log_type {
             TODO: add log types"""
    __WRTD_MAX_LOG_TYPE_NUMBER = 0

    def __init_lib(self):
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
        self.wrtd_get_error.errcheck = self.__errcheck_int
        self.wrtd_get_error.argtypes = [c_void_p, c_void_p,
                                        c_uint, c_char_p]

        self.wrtd_error_message = self.wrtd_lib.wrtd_error_message
        self.wrtd_error_message.restype = c_uint
        self.wrtd_error_message.errcheck = self.__errcheck_int
        self.wrtd_error_message.argtypes = [c_void_p, c_uint, c_char_p]

        self.wrtd_get_attr_int32 = self.wrtd_lib.wrtd_get_attr_int32
        self.wrtd_get_attr_int32.restype = c_uint
        self.wrtd_get_attr_int32.errcheck = self.__errcheck_int
        self.wrtd_get_attr_int32.argtypes = [c_void_p, c_char_p,
                                             c_uint, c_void_p]

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

    def __init__(self, resource_name):
        self.__init_lib()
        self.resource_name = resource_name.encode('utf-8')
        self.wrtd_p = POINTER(wrtd)()

    def init(self, reset, options_str):
        self.wrtd_init(self.resource_name, reset, options_str, 
                       byref(self.wrtd_p))

    def close(self):
        self.wrtd_close(byref(self.wrtd_p))

    def reset(self):
        self.wrtd_reset(byref(self.wrtd_p))

    def get_error(self, error_code, buffer_size, error_description):
        self.wrtd_get_error(byref(self.wrtd_p), error_code, buffer_size, 
                            error_description)

    def error_message(self, err_code, err_message):
        self.wrtd_error_message(byref(self.wrtd_p), err_code, err_message)

    def get_attr_int32(self, rep_cap_id, id, value) 

extern enum wrtd_status wrtd_get_attr_int32(struct wrtd_dev *dev,
					    const char *rep_cap_id,
					    enum wrtd_attr id,
					    int32_t *value);
extern enum wrtd_status wrtd_set_attr_int32(struct wrtd_dev *dev,
					    const char *rep_cap_id,
					    enum wrtd_attr id,
					    int32_t value);
extern enum wrtd_status wrtd_set_attr_int64(struct wrtd_dev *dev,
					    const char *rep_cap_id,
					    enum wrtd_attr id,
					    int64_t value);
extern enum wrtd_status wrtd_get_attr_bool(struct wrtd_dev *dev,
					   const char *rep_cap_id,
					   enum wrtd_attr id,
					   bool *value);
extern enum wrtd_status wrtd_set_attr_bool(struct wrtd_dev *dev,
					   const char *rep_cap_id,
					   enum wrtd_attr id,
					   bool value);
extern enum wrtd_status wrtd_get_attr_tstamp(struct wrtd_dev *dev,
					     const char *rep_cap_id,
					     enum wrtd_attr id,
					     struct wrtd_tstamp *value);
extern enum wrtd_status wrtd_set_attr_tstamp(struct wrtd_dev *dev,
					     const char *rep_cap_id,
					     enum wrtd_attr id,
					     const struct wrtd_tstamp *value);
extern enum wrtd_status wrtd_set_attr_string(struct wrtd_dev *dev,
					     const char *rep_cap_id,
					     enum wrtd_attr id,
					     const char *value);
extern enum wrtd_status wrtd_get_attr_int64(struct wrtd_dev *dev,
					    const char *rep_cap_id,
					    enum wrtd_attr id,
					    int64_t *value);
extern enum wrtd_status wrtd_get_attr_string(struct wrtd_dev *dev,
					     const char *rep_cap_id,
					     enum wrtd_attr id,
					     int32_t value_buf_size,
					     char *value);

/
#
#
#   def set_attr_int32(self, 
#
#   def get_attr_bool(self, 
#
#   def set_attr_bool(self, 
#
#   def set_attr_tstamp(self, 
#
#   def set_attr_string(self, 
#
#   def get_attr_string(self, 
#
#   def get_sys_time(self, 
#
#   def log_read(self, 
#
#   def add_alarm(self, 
#
#   def disable_all_alarms(self, 
#
#   def remove_alarm(self, 
#
#   def remove_all_alarms(self, 
#
#   def get_alarm_id(self, 
#
#   def add_rule(self, 
#
#   def disable_all_rules(self, 
#
#   def remove_rule(self, 
#
#   def remove_all_rules(self, 
#
#   def get_rule_id(self, 



    def __errcheck_int(self, ret, func, args):
        """Generic error checker for functions returning 0 as success
        and -1 as error"""
        if ret != self.WRTD_SUCCESS:
            #TODO use this funciton here
            # const char *wrtd_get_error_msg(struct wrtd_dev *dev)
            #{
            #        return dev->error_msg;
            #}

            raise OSError(ret,
                          "error", "")
        else:
            return ret

 
"""############################### NOT API #########################"""


def ts_add_ps(ts, ps):
    ps = int(ps)
    frac = ps * 1 << 32
    frac = frac // 1000
    frac_temp = ts.frac + frac

    ns_temp = ts.ns + frac_temp // 2**32
    ts.frac = int(frac_temp % 2**32)

    ts.seconds = int(ts.seconds + ns_temp // 1e9)
    ts.ns = int(ns_temp % 1e9)
