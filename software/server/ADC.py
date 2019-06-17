from ADC_configs import Channel
from ADC_configs import InternalTrigger
from ADC_configs import ExternalTrigger
from ADC_configs import AcqConf
import sys
sys.path.append('../')
from general.zmq_rpc import ZMQ_RPC

# fixme if your class doesnt inherit, do not add empty () after its declaration
class ADC:

    def __init__(self, unique_ADC_name, ip, port):
        self.__unique_ADC_name = unique_ADC_name
        self.__ip = ip
        self.__port = port
        self.__channels = []
        self.__internal_triggers = []
        self.__external_triggers = []
        self.__acq_conf = None
        self.__WRTD_master = True
        self.zmq_rpc = ZMQ_RPC(ip, port + 8)  # remove +8 after removing xml
        conf = self.zmq_rpc.send_RPC('get_current_adc_conf')

        for count in range(0, conf['board_conf']['n_chan']):
            channel = Channel(self.__unique_ADC_name, count)
            self.__channels.append(channel)
        for count in range(0, conf['board_conf']['n_trg_int']):
            int_trig = InternalTrigger(self.__unique_ADC_name, count)
            self.__internal_triggers.append(int_trig)

        for count in range(0, conf['board_conf']['n_trg_ext']):
            ext_trig = ExternalTrigger(self.__unique_ADC_name, count)
            self.__external_triggers.append(ext_trig)
        self.__acq_conf = AcqConf()
        self.update_conf()

    def update_data(self, timestamp, pre_post, data, unique_ADC_name):
        """the value of pre and postsamples is passed together with the data
        because if it is read from the ADC structure in the server it could
        be outdated"""
        range_multiplier = {10: 1, 1: 1/10, 100: 1/100}
        for channel_idx, data_channel in data.items():
            range = self.__channels[int(channel_idx)].channel_range
            mult = range_multiplier[range]
            data_channel = [value * mult for value in data_channel]
            """conversion to the 10V scale"""
            data_channel = [(value / 2**16 * 10) for value in data_channel]
            """conversionfrom raw to V"""

            self.__channels[int(channel_idx)].timestamp_pre_post_data =\
                    {'timestamp': timestamp, 'pre_post': pre_post,
                     'data_channel': data_channel}

    def update_conf(self):
        zmq_rpc = self.zmq_rpc
        conf = zmq_rpc.send_RPC('get_current_adc_conf')
        for count in range(0, conf['board_conf']['n_chan']):
            channel = conf['chn_conf'][count]
            self.__channels[count].update_channel_conf(
                                                channel['channel_range'],
                                                channel['termination'],
                                                channel['offset'])
        for count in range(0, conf['board_conf']['n_trg_int']):
            trigger = conf['int_trg_conf'][count]
            self.__internal_triggers[count].update_trigger_conf(
                                                    trigger['enable'],
                                                    trigger['polarity'],
                                                    trigger['delay'],
                                                    trigger['threshold'])
        for count in range(0, conf['board_conf']['n_trg_ext']):
            trigger = conf['ext_trg_conf'][count]
            self.__external_triggers[count].update_trigger_conf(
                                                    trigger['enable'],
                                                    trigger['polarity'],
                                                    trigger['delay'])
        self.__acq_conf.update_acq_conf(
            conf['acq_conf']['presamples'],
            conf['acq_conf']['postsamples'])

    def get_channel(self, channel_idx):
        return self.__channels[channel_idx]

    def get_internal_trigger(self, trigger_idx):
        return self.__internal_triggers[trigger_idx]
    
    def get_external_trigger(self, trigger_idx):
        return self.__external_triggers[trigger_idx]

    def get_acq_conf(self):
        return self.__acq_conf

    def set_WRTD_master(self, WRTD_master):
        self.__WRTD_master = WRTD_master
        self.zmq_rpc.send_RPC('set_WRTD_master', WRTD_master)

    def set_adc_parameter_remote(self, function_name, *args):
        self.zmq_rpc.send_RPC('set_adc_parameter', function_name, *args)
