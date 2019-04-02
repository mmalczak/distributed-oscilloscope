from ctypes import * 



#@enum wrtd_status
#White Rabbit Trigger Distribution warnings and errors

#enum wrtd_status {
#         Codes inspired by IVI 3.2 
WRTD_SUCCESS                            = 0
WRTD_ERROR_BASE                         = 0xBFFA3000
WRTD_ERROR_CANNOT_RECOVER               = 0xBFFA3001
WRTD_ERROR_INVALID_ATTRIBUTE            = 0xBFFA3002
WRTD_ERROR_ATTR_NOT_WRITEABLE           = 0xBFFA3003
WRTD_ERROR_ATTR_NOT_READABLE            = 0xBFFA3004
WRTD_ERROR_INVALID_VALUE                = 0xBFFA3005
WRTD_ERROR_NOT_INITIALIZED              = 0xBFFA3006
WRTD_ERROR_MISSING_OPTION_NAME          = 0xBFFA3007
WRTD_ERROR_MISSING_OPTION_VALUE         = 0xBFFA3008
WRTD_ERROR_BAD_OPTION_NAME              = 0xBFFA3009
WRTD_ERROR_BAD_OPTION_VALUE             = 0xBFFA300A
WRTD_ERROR_OUT_OF_MEMORY                = 0xBFFA300B
WRTD_ERROR_OPERATION_PENDING            = 0xBFFA300C
WRTD_ERROR_NULL_POINTER                 = 0xBFFA300D
WRTD_ERROR_UNEXPECTED_RESPONSE          = 0xBFFA300E
WRTD_ERROR_RESET_FAILED                 = 0xBFFA300F
WRTD_ERROR_RESOURCE_UNKNOWN             = 0xBFFA3010

# Resource (alar, rule) is not
# disabled and cannot be changed.      
WRTD_ERROR_RESOURCE_ACTIVE              = 0xBFFA3011

# Require global rep cap.  
WRTD_ERROR_ATTR_INVALID_REP_CAP         = 0xBFFA3012

# Feature not implemented.  
WRTD_ERROR_NOT_IMPLEMENTED              = 0xBFFA3013

# Incorrect repeated capability 
#id: too long, 
#invalid character... 
WRTD_ERROR_BAD_REP_CAP_ID               = 0xBFFA3014

# Timeout while reading log.         
WRTD_ERROR_TIMEOUT                      = 0xBFFA3015

# Output buffer is not long 
#enough.  
WRTD_ERROR_BUFFER_TOO_SHORT             = 0xBFFA3016
   
WRTD_ERROR_UNKNOWN_NAME_IN_SELECTOR     = 0xBFFA3017 # NOTE: selector == rep_cap_id
# Codes inspired by IviLxiSync
# 3.15 
WRTD_ERROR_ALARM_TIME_INVALID           = 0xBFFA3018
WRTD_ERROR_ALARM_EXISTS                 = 0xBFFA3019
WRTD_ERROR_ALARM_DOES_NOT_EXIST         = 0xBFFA301A
WRTD_ERROR_ALARM_OUT_OF_RESOURCES       = 0xBFFA301B
WRTD_ERROR_RULE_EXISTS                  = 0xBFFA301C
WRTD_ERROR_RULE_DOES_NOT_EXIST          = 0xBFFA301D
WRTD_ERROR_RULE_OUT_OF_RESOURCES        = 0xBFFA301E
WRTD_ERROR_RULE_INVALID                 = 0xBFFA301F
WRTD_ERROR_RULE_ENABLED                 = 0xBFFA3020
WRTD_ERROR_CANT_REMOVE_RESERVED_REP_CAP = 0xBFFA3021
__WRTD_ERROR_MAX_NUMBER                 = 0xBFFA3022

#
#  @enum wrtd_attr
#  White Rabbit Trigger Distribution attribute ID definions
# 
#enum wrtd_attr {
__WRTD_ATTR_BASE                             = 950000 
WRTD_MAJOR_VERSION                           = 950001     #  RO, int32
WRTD_MINOR_VERSION                           = 950002     #  RO, int32
WRTD_ATTR_EVENT_LOG_ENTRY_COUNT              = 950003     #  RO, int32
WRTD_ATTR_EVENT_LOG_ENABLED                  = 950004     # RW, bool
# TODO: add log levelsmasks here
WRTD_ATTR_IS_TIME_MASTER                     = 950005     #  RO, bool
WRTD_ATTR_IS_TIME_SYNCHRONIZED               = 950006     #  RO, bool

# Number of alarms (global attribute).
WRTD_ATTR_ALARM_COUNT                        = 950007     # RO, int32

# Enabledisable an alarm.
WRTD_ATTR_ALARM_ENABLED                      = 950008     # RW, bool

WRTD_ATTR_ALARM_SETUP_TIME                   = 950009     # RW, tstamp
WRTD_ATTR_ALARM_TIME                         = 950010     # RW, tstamp
# Specifies the alarm period.
# 0 means no repetitions.
WRTD_ATTR_ALARM_PERIOD                       = 950011     # RW, tstamp
# Specifies the number of times the 
#alarm will occur at the period 
#specified by
# WRTD_ATTR_ALARM_PERIOD. 0 means 
#infinite. 1 means exactly one alarm
# will occur.
WRTD_ATTR_ALARM_REPEAT_COUNT                 = 950012     # RW, int32

# Number of rules (global attribute).
WRTD_ATTR_RULE_COUNT                         = 950013     # RO, int32

# True if the rule is enabled 
#(ie active).
WRTD_ATTR_RULE_ENABLED                       = 950014     # RW, bool
# Number of time the rule will apply.
#0 means infinite.  When read,
# return the remaining number.
WRTD_ATTR_RULE_REPEAT_COUNT                  = 950015     # RW, int32
# Source of the event.
WRTD_ATTR_RULE_SOURCE                        = 950016     # RW, string
# Destination of the event.
WRTD_ATTR_RULE_DESTINATION                   = 950017     # RW, string
# If true, events from the past 
#are still handled; otherwise they
# are discarded.
WRTD_ATTR_RULE_SEND_LATE                     = 950018     # RW, bool
# Delay the event.
WRTD_ATTR_RULE_DELAY                         = 950019     # RW, tstamp
# Discard new events between
# the last one to this value.
WRTD_ATTR_RULE_HOLDOFF                       = 950020     # RW, tstamp
# Realign the timestamp to 
#a multiple of period and then add
# factor  period. This 
#is done after the delay.
WRTD_ATTR_RULE_RESYNC_PERIOD                 = 950021     # RW, tstamp
WRTD_ATTR_RULE_RESYNC_FACTOR                 = 950022     # RW, int32

# TODO: add __ boundaries 
#between groups to make it easier
# to do input validation
WRTD_ATTR_STAT_RULE_RX_EVENTS                = 950023     # RO, int32
WRTD_ATTR_STAT_RULE_RX_LAST                  = 950024     # RO, tstamp
WRTD_ATTR_STAT_RULE_TX_EVENTS                = 950025     # RO, int32
WRTD_ATTR_STAT_RULE_TX_LAST                  = 950026     # RO, tstamp
WRTD_ATTR_STAT_RULE_MISSED_EVENTS_LATE       = 950027     # RO, int32
WRTD_ATTR_STAT_RULE_MISSED_EVENTS_HOLDOFF    = 950028     # RO, int32
WRTD_ATTR_STAT_RULE_MISSED_EVENTS_OVERFLOW   = 950029     # RO, int32
WRTD_ATTR_STAT_RULE_MISSED_LAST              = 950030     # RO, tstamp

# Latency and period (excluding 
#events discarded due to holdoff).  
WRTD_ATTR_STAT_RULE_RX_LATENCY_MIN           = 950031     # RO, tstamp (maybe ns only valid)
WRTD_ATTR_STAT_RULE_RX_LATENCY_MAX           = 950032     # RO, tstamp (maybe ns only valid)
WRTD_ATTR_STAT_RULE_RX_LATENCY_AVG           = 950033     # RO, tstamp (maybe ns only valid)
WRTD_ATTR_STAT_RULE_RX_PERIOD_MIN            = 950034     # RO, tstamp (maybe ns only valid)
WRTD_ATTR_STAT_RULE_RX_PERIOD_MAX            = 950035     # RO, tstamp (maybe ns only valid)
WRTD_ATTR_STAT_RULE_RX_PERIOD_AVG            = 950036     # RO, tstamp (maybe ns only valid)
__WRTD_ATTR_MAX_NUMBER                       = 950037     #


#
#  A repeated capability identifier for global attributes
# 
WRTD_GLOBAL_REP_CAP_ID                       = "WGRCI"


#  @enum wrtd_log_type
#  White Rabbit Trigger Distribution log entry type
# 
#enum wrtd_log_type {
#         TODO: add log types
__WRTD_MAX_LOG_TYPE_NUMBER                   = 0


class wrtd(Structure):
    pass

class wrtd_tstamp(Structure):
    _fields_ = [("seconds", c_uint),
                ("ns", c_uint),
                ("frac", c_uint)
               ]    


wrtd_lib = CDLL("libwrtd.so")



#
#  @file libwrtd-base.c
# 
#
#  @defgroup base
#  Set of functions to manage the basic device and library configuration.
#  @{
# 
# Ideally, also be able to list possible names

wrtd_init = wrtd_lib.wrtd_init
wrtd_init.restype = c_uint 
wrtd_init.argtypes = [c_char_p, c_int, c_char_p, POINTER(POINTER(wrtd))]
#wrtd_init.argtypes = [c_char_p, c_int, c_char_p, c_void_p]

wrtd_close = wrtd_lib.wrtd_close
wrtd_close.restype = c_uint 
wrtd_close.argtypes = [c_void_p]

wrtd_reset = wrtd_lib.wrtd_reset
wrtd_reset.restype = c_uint 
wrtd_reset.argtypes = [c_void_p]

wrtd_get_error = wrtd_lib.wrtd_get_error
wrtd_get_error.restype = c_uint 
wrtd_get_error.argtypes = [c_void_p, c_void_p, c_uint, c_char_p]


wrtd_error_message = wrtd_lib.wrtd_error_message
wrtd_error_message.restype = c_uint 
wrtd_error_message.argtypes = [c_void_p, c_uint, c_char_p]

# Attributes.  
wrtd_get_attr_int32 = wrtd_lib.wrtd_get_attr_int32
wrtd_get_attr_int32.restype = c_uint 
wrtd_get_attr_int32.argtypes = [c_void_p, c_char_p, c_uint, c_void_p] 

wrtd_set_attr_int32 = wrtd_lib.wrtd_set_attr_int32
wrtd_set_attr_int32.restype = c_uint 
wrtd_set_attr_int32.argtypes = [c_void_p, c_char_p, c_uint, c_int] 

#wrtd_set_attr_int64 = wrtd_lib.wrtd_set_attr_int64
#wrtd_set_attr_int64.restype = c_uint 
#wrtd_set_attr_int64.argtypes = [c_void_p, c_char_p, c_uint, c_long] 

wrtd_get_attr_bool = wrtd_lib.wrtd_get_attr_bool
wrtd_get_attr_bool.restype = c_uint 
wrtd_get_attr_bool.argtypes = [c_void_p, c_char_p, c_uint, c_void_p]

wrtd_set_attr_bool = wrtd_lib.wrtd_set_attr_bool
wrtd_set_attr_bool.restype = c_uint 
wrtd_set_attr_bool.argtypes = [c_void_p, c_char_p, c_uint, c_int] 

#wrtd_get_attr_tstamp = wrtd_lib.wrtd_get_attr_tstamp
#wrtd_get_attr_tstamp.restype = c_uint 
#wrtd_get_attr_tstamp.argtypes = [c_void_p, c_char_p, c_uint, c_void_p]

wrtd_set_attr_tstamp = wrtd_lib.wrtd_set_attr_tstamp
wrtd_set_attr_tstamp.restype = c_uint 
wrtd_set_attr_tstamp.argtypes = [c_void_p, c_char_p, c_uint, c_void_p] 

wrtd_set_attr_string = wrtd_lib.wrtd_set_attr_string
wrtd_set_attr_string.restype = c_uint 
wrtd_set_attr_string.argtypes = [c_void_p, c_char_p, c_uint, c_char_p]

#wrtd_get_attr_int64 = wrtd_lib.wrtd_get_attr_int64
#wrtd_get_attr_int64.restype = c_uint 
#wrtd_get_attr_int64.argtypes = [c_void_p, c_char_p, c_uint, c_long]

wrtd_get_attr_string = wrtd_lib.wrtd_get_attr_string
wrtd_get_attr_string.restype = c_uint 
wrtd_get_attr_string.argtypes = [c_void_p, c_char_p, c_uint, c_int, c_char_p]



#@}
#
#
#  @file libwrtd-time.c
# 
#
#  @defgroup time
#  Set of functions to manage time
#  @{
# 
wrtd_get_sys_time = wrtd_lib.wrtd_get_sys_time
wrtd_get_sys_time.restype = c_uint 
wrtd_get_sys_time.argtypes = [c_void_p, c_void_p]



#@}
#
#
#  @file libwrtd-log.c
# 
#
#  @defgroup logging
#  Set of logging functions
#  @{
# 
wrtd_log_read = wrtd_lib.wrtd_log_read
wrtd_log_read.restype = c_uint 
wrtd_log_read.argtypes = [c_void_p, c_void_p, c_int]


# Maybe also add non-blocking wrtd_get_next_log_entry()
#wrtd_clear_log = wrtd_lib.wrtd_clear_log
#wrtd_clear_log.restype = c_uint 
#wrtd_clear_log.argtypes = [c_void_p]


#@}
#
#
#  @file libwrtd-alarm.c
# 
#
#  @defgroup alarms
#  Set of functions to configure alarms as
#  sources for the generation of events
#  @{
# 
wrtd_add_alarm = wrtd_lib.wrtd_add_alarm
wrtd_add_alarm.restype = c_uint 
wrtd_add_alarm.argtypes = [c_void_p, c_char_p]

wrtd_disable_all_alarms = wrtd_lib.wrtd_disable_all_alarms
wrtd_disable_all_alarms.restype = c_uint 
wrtd_disable_all_alarms.argtypes = [c_void_p]

wrtd_remove_alarm = wrtd_lib.wrtd_remove_alarm
wrtd_remove_alarm.restype = c_uint 
wrtd_remove_alarm.argtypes = [c_void_p, c_char_p]

wrtd_remove_all_alarms = wrtd_lib.wrtd_remove_all_alarms
wrtd_remove_all_alarms.restype = c_uint 
wrtd_remove_all_alarms.argtypes = [c_void_p]

wrtd_get_alarm_id = wrtd_lib.wrtd_get_alarm_id
wrtd_get_alarm_id.restype = c_uint 
wrtd_get_alarm_id.argtypes = [c_void_p, c_int, c_int, c_char_p]


#
#  @file libwrtd-rule.c
# 
#
#  @defgroup rules
#  Set of functions to trigger on and
#  schedule the generation of events
#  @{
# 
# rule sources can be a) reserved event ids, b) alarm c) any other string
# which will be interpreted as a net msg event id
wrtd_add_rule = wrtd_lib.wrtd_add_rule
wrtd_add_rule.restype = c_uint 
wrtd_add_rule.argtypes = [c_void_p, c_char_p]

wrtd_disable_all_rules = wrtd_lib.wrtd_disable_all_rules
wrtd_disable_all_rules.restype = c_uint 
wrtd_disable_all_rules.argtypes = [c_void_p]

wrtd_remove_rule = wrtd_lib.wrtd_remove_rule
wrtd_remove_rule.restype = c_uint 
wrtd_remove_rule.argtypes = [c_void_p, c_char_p]

wrtd_remove_all_rules = wrtd_lib.wrtd_remove_all_rules
wrtd_remove_all_rules.restype = c_uint 
wrtd_remove_all_rules.argtypes = [c_void_p]


wrtd_get_rule_id = wrtd_lib.wrtd_get_rule_id
wrtd_get_rule_id.restype = c_uint 
wrtd_get_rule_id.argtypes = [c_void_p, c_int, c_int, c_char_p]

#wrtd_reset_rule_stats = wrtd_lib.wrtd_reset_rule_stats
#wrtd_reset_rule_stats.restype = c_uint 
#wrtd_reset_rule_stats.argtypes = [c_void_p, c_char_p]

############################### NOT API ###########################
def ts_add_ps(ts, ps):
   ps = int(ps)
   frac = ps * 1<<32
   frac = frac // 1000
   frac_temp = ts.frac + frac

   ns_temp = ts.ns + frac_temp // 2**32
   ts.frac = int(frac_temp % 2**32)

   ts.seconds = int(ts.seconds + ns_temp // 1e9)
   ts.ns = int(ns_temp % 1e9)

