from ADC_configs import Channel
from ADC_configs import InternalTrigger
from ADC_configs import ExternalTrigger
from ADC_configs import AcqConf
import sys
sys.path.append('../')
from general.zmq_rpc import ZMQ_RPC

# fixme if your class doesnt inherit, do not add empty () after its declaration
class ADC:

    def __init__(self, unique_name, conf, ip, port):
        self.conf = conf
        self.number_of_channels = self.conf['board_conf']['n_chan']
        self.unique_name = unique_name
        self.timestamp_pre_post_data = []
        self.ip = ip
        self.port = port
        self.channels = []
        self.internal_triggers = []
        self.external_triggers = []
        self.acq_conf = None
        self.WRTD_master = True
        self.zmq_rpc = ZMQ_RPC(ip, port + 8)  # remove +8 after removing xml
        conf = self.zmq_rpc.send_RPC('get_current_adc_conf')

        for count in range(0, self.conf['board_conf']['n_chan']):
            self.channels.append(Channel(self.unique_name, count))
        for count in range(0, self.conf['board_conf']['n_trg_int']):
            self.internal_triggers.append(InternalTrigger(self.unique_name,
                                                          count))
        for count in range(0, self.conf['board_conf']['n_trg_ext']):
            self.external_triggers.append(ExternalTrigger(self.unique_name,
                                                          count))
        self.acq_conf = AcqConf()
        self.update_conf()

    def update_data(self, timestamp, pre_post, data, unique_ADC_name):
        """the value of pre and postsamples is passed together with the data
        because if it is read from the ADC structure in the server it could
        be outdated"""
        range_multiplier = {10: 1, 1: 1/10, 100: 1/100}
        for channel_idx, data_channel in data.items():
            range = self.channels[int(channel_idx)].channel_range
            mult = range_multiplier[range]
            data_channel = [value * mult for value in data_channel]
            """conversion to the 10V scale"""
            data_channel = [(value / 2**16 * 10) for value in data_channel]
            """conversionfrom raw to V"""

            self.channels[int(channel_idx)].timestamp_pre_post_data =\
                    {'timestamp': timestamp, 'pre_post': pre_post,
                     'data_channel': data_channel}

    def add_channel(self, channel_range, termination, offset, ADC_channel_idx):
        self.channels.append(Channel(channel_range, termination, offset,
                                     self.unique_name, ADC_channel_idx))

    def add_external_trigger(self, enable, polarity, delay, ADC_trigger_idx):
        self.external_triggers.append(ExternalTrigger(enable, polarity, delay,
                                                      self.unique_name,
                                                      ADC_trigger_idx))

    def add_internal_trigger(self, enable, polarity, delay, threshold,
                             ADC_trigger_idx):
        self.internal_triggers.append(InternalTrigger(enable, polarity, delay,
                                                      threshold,
                                                      self.unique_name,
                                                      ADC_trigger_idx))

    def update_conf(self):
        zmq_rpc = self.zmq_rpc
        self.conf = zmq_rpc.send_RPC('get_current_adc_conf')
        for count in range(0, self.conf['board_conf']['n_chan']):
            channel = self.conf['chn_conf'][count]
            self.channels[count].update_channel_conf(channel['channel_range'],
                                                     channel['termination'],
                                                     channel['offset'])
        for count in range(0, self.conf['board_conf']['n_trg_int']):
            trigger = self.conf['int_trg_conf'][count]
            self.internal_triggers[count].update_trigger_conf(trigger['enable'],
                                                              trigger['polarity'],
                                                              trigger['delay'],
                                                              trigger['threshold'])
        for count in range(0, self.conf['board_conf']['n_trg_ext']):
            trigger = self.conf['ext_trg_conf'][count]
            self.external_triggers[count].update_trigger_conf(trigger['enable'],
                                                              trigger['polarity'],
                                                              trigger['delay'])
        self.acq_conf.update_acq_conf(
            self.conf['acq_conf']['presamples'],
            self.conf['acq_conf']['postsamples'])
        """TODO for time triggers"""
