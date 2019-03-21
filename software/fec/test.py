from  wrtd_wrapper import *
from ctypes import *
import argparse
import os

#if(status != WRTD_SUCCESS):
#	print("Error while executing command add_rule" + wrtd_get_error_msg(wrtd_p).decode('utf-8'))
###########    error messages - talk to Tristan
#		wrtd_get_error_msg that is used in the tool is not in the official API
#		functions for getting error messages from API are not implemented



 


parser = argparse.ArgumentParser()
parser.add_argument('-D', nargs =1, help='<device>' + 'id of the device eg. trtl-0001')
parser.add_argument('--add_rule', nargs =1, help='<name>' + 'add a rule')
parser.add_argument('--set_rule', nargs =4, help='<name> <delay[sn]> <src> <dest>' + 'set rule source and destination')



args = parser.parse_args()


dev_name_p = None
error_code = c_int()
error_description = create_string_buffer(256)


if(args.D == None):
    print("No device specified")
    os._exit(1)
else:
    dev_name_p = args.D[0].encode('utf-8')    
    wrtd_p = POINTER(wrtd)()
    status = wrtd_init(dev_name_p, 0, None, byref(wrtd_p))
    if(status != WRTD_SUCCESS):
        print("Cannot open WRTD: " + str(args.D[0]) + " status: 0x" + str(format(status, '08x')) + " errno: " + os.strerror(get_errno()) )
        os._exit(1)




def check_for_errors(status, cmd):
    if(status != WRTD_SUCCESS):
        wrtd_get_error(wrtd_p, byref(error_code), 256, error_description)
        print("Error while executing command: " + str(cmd) + " : " + str(error_description.value))
        os._exit(1)

if(args.add_rule != None):
    rule_name_p = args.add_rule[0].encode('utf-8')
    status = wrtd_add_rule(wrtd_p, rule_name_p)
    check_for_errors(status, 'add_rule')
if(args.set_rule != None):
    rule_name_p = args.set_rule[0].encode('utf-8')
    delay_ps = args.set_rule[1]
    src_p = args.set_rule[2].encode('utf-8')
    dst_p = args.set_rule[3].encode('utf-8')

    ts = wrtd_tstamp()
    ts.seconds = 0
    ts.ns = 0
    ts.frac = 0
    ts_add_ps(ts, delay_ps)
    status = wrtd_set_attr_string(wrtd_p, rule_name_p, WRTD_ATTR_RULE_SOURCE, src_p)
    check_for_errors(status, 'set_rule')
    status = wrtd_set_attr_string(wrtd_p, rule_name_p, WRTD_ATTR_RULE_DESTINATION, dst_p)
    check_for_errors(status, 'set_rule')
    status = wrtd_set_attr_tstamp(wrtd_p, rule_name_p, WRTD_ATTR_RULE_DELAY, byref(ts))
    check_for_errors(status, 'set_rule')




wrtd_close(wrtd_p)


