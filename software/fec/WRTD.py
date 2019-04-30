from wrtd_wrapper import *
import os

def encode_arguments(func):
    def wrapper(self, *args, **kwargs):
        encoded = []
        for arg in args:
            if(type(arg) == str):
                encoded.append(arg.encode('utf-8'))
            else:
                encoded.append(arg)
        args = tuple(encoded)
        func(self, *args, **kwargs)    
    return wrapper

class WRTD(WRTD_wrapper):
    def __init__(self, trtl):
        super().__init__()
        self.trtl = trtl.encode('utf-8')
        self.wrtd_p = POINTER(wrtd)()
        status = self.wrtd_init(self.trtl, 0, None, byref(self.wrtd_p))
        if(status != self.WRTD_SUCCESS):
            print("Cannot open WRTD: " + str(args.D[0]) + " status: 0x" + str(format(status, '08x')) + " errno: " + os.strerror(get_errno()) )
            os._exit(1)

        status = self.wrtd_disable_all_rules(self.wrtd_p)
        self.check_for_errors(status, 'disable_all_rules')

        status = self.wrtd_remove_all_rules(self.wrtd_p)
        self.check_for_errors(status, 'remove_all_rules')

    def check_for_errors(self, status, cmd):
        error_code = c_int()
        error_description = create_string_buffer(256)
        if(status != self.WRTD_SUCCESS):
            self.wrtd_get_error(self.wrtd_p, byref(error_code), 256, error_description)
            print("Error while executing command: " + str(cmd) + " : " + str(error_description.value))
            os._exit(1)

    @encode_arguments
    def add_rule(self, name):
        status = self.wrtd_add_rule(self.wrtd_p, name)
        self.check_for_errors(status, 'add_rule')
       
    @encode_arguments
    def set_rule(self, name, delay_ps, src_p, dst_p):
        ts = wrtd_tstamp()
        ts.seconds = 0
        ts.ns = 0
        ts.frac = 0
        ts_add_ps(ts, delay_ps)
        status = self.wrtd_set_attr_string(self.wrtd_p, name, self.WRTD_ATTR_RULE_SOURCE, src_p)
        self.check_for_errors(status, 'set_rule')
        status = self.wrtd_set_attr_string(self.wrtd_p, name, self.WRTD_ATTR_RULE_DESTINATION, dst_p)
        self.check_for_errors(status, 'set_rule')
        status = self.wrtd_set_attr_tstamp(self.wrtd_p, name, self.WRTD_ATTR_RULE_DELAY, byref(ts))
        self.check_for_errors(status, 'set_rule')

    @encode_arguments
    def enable_rule(self, name):
        status = self.wrtd_set_attr_bool(self.wrtd_p, name, self.WRTD_ATTR_RULE_ENABLED, 1);
        self.check_for_errors(status, 'enable_rule')

    @encode_arguments
    def disable_rule(self, name):
        status = self.wrtd_set_attr_bool(self.wrtd_p, name, self.WRTD_ATTR_RULE_ENABLED, 0);
        self.check_for_errors(status, 'disable_rule')

    def add_rule_mult_src(self, name, number):
        for count in range(1, number):
            self.add_rule(name+str(count))

    def set_rule_mult_src(self, name, delay_ps, src_p, dst_p, number):
        for count in range(1, number):
            self.set_rule(name+str(count), delay_ps, src_p+str(count), dst_p)

    def enable_rule_mult_src(self, name, number):
        for count in range(1, number):
            self.enable_rule(name+str(count))

    def disable_rule_mult_src(self, name, number):
        for count in range(1, number):
            self.disable_rule(name+str(count))


    def __del__(self):
        self.wrtd_close(self.wrtd_p)




