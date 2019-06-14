from wrtd_wrapper import WRTD_wrapper
from wrtd_wrapper import encode_arguments


class WRTD(WRTD_wrapper):
    def __init__(self, trtl):
        super().__init__(trtl)
        self.trtl = trtl.encode('utf-8')

        self.disable_all_rules()
        self.remove_all_rules()

    def ts_add_ps(self, ts, ps):
        ps = int(ps)
        frac = ps * 1 << 32
        frac = frac // 1000
        frac_temp = ts["frac"] + frac

        ns_temp = ts["ns"] + frac_temp // 2**32
        ts["frac"] = int(frac_temp % 2**32)

        ts["seconds"] = int(ts["seconds"] + ns_temp // 1e9)
        ts["ns"] = int(ns_temp % 1e9)

    @encode_arguments
    def set_rule(self, name, delay_ps, src_p, dst_p):
        ts = {"seconds": 0, "ns": 0, "frac": 0}
        self.ts_add_ps(ts, delay_ps)
        self.set_attr_string(name, self.WRTD_ATTR_RULE_SOURCE, src_p)
        self.set_attr_string(name, self.WRTD_ATTR_RULE_DESTINATION,
                             dst_p)
        self.set_attr_tstamp(name, self.WRTD_ATTR_RULE_DELAY, ts)

    @encode_arguments
    def enable_rule(self, name):
        self.set_attr_bool(name, self.WRTD_ATTR_RULE_ENABLED, 1)

    @encode_arguments
    def disable_rule(self, name):
        self.set_attr_bool(name, self.WRTD_ATTR_RULE_ENABLED, 0)

    def add_rule_mult_src(self, name, number):
        for count in range(1, number):
            self.add_rule(name+str(count))

    def set_rule_mult_src(self, name, delay_ps, src_p, dst_p, number):
        for count in range(1, number):
            self.set_rule(name+str(count), delay_ps, src_p+str(count),
                          dst_p)

    def enable_rule_mult_src(self, name, number):
        for count in range(1, number):
            self.enable_rule(name+str(count))

    def disable_rule_mult_src(self, name, number):
        for count in range(1, number):
            self.disable_rule(name+str(count))
