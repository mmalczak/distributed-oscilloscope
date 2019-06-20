from ADC_configs import Channel
from ADC_configs import InternalTrigger
from ADC_configs import ExternalTrigger
from ADC_configs import AcqConf
import sys
sys.path.append('../')
from general.zmq_rpc import ZMQ_RPC
from conversion import threshold_mV_to_raw
import logging
logger = logging.getLogger(__name__)


# fixme if your class doesnt inherit, do not add empty () after its declaration
class ADC:

    def __init__(self, unique_ADC_name, ip, port, osc):
        self.__unique_ADC_name = unique_ADC_name
        self.__ip = ip
        self.__port = port
        self.__channels = []
        self.__used_channels = []
        self.__internal_triggers = []
        self.__external_triggers = []
        self.__acq_conf = None
        self.__is_WRTD_master = None
        self.__osc = osc
        self.__zmq_rpc = ZMQ_RPC(ip, port + 8)  # remove +8 after removing xml
        conf = self.send_RPC('get_current_adc_conf')
        self.number_of_channels = conf['board_conf']['n_chan']

        for count in range(0, conf['board_conf']['n_chan']):
            channel = Channel(self, count)
            self.__channels.append(channel)
        for count in range(0, conf['board_conf']['n_trg_int']):
            int_trig = InternalTrigger(self, count)
            self.__internal_triggers.append(int_trig)

        for count in range(0, conf['board_conf']['n_trg_ext']):
            ext_trig = ExternalTrigger(self, count)
            self.__external_triggers.append(ext_trig)
        self.__acq_conf = AcqConf()
        self.update_conf()

    def suicide(self):
        self.__osc.unregister_ADC(self.__unique_ADC_name)

    def send_RPC(self, RPC_name, *args):
        try:
            return self.__zmq_rpc.send_RPC(RPC_name, *args)
        except RPC_Error:
            logger.error("Error when calling RPC: {}, closing ADC".format(
                                                                    RPC_name))
            self.suicide()

    def get_unique_ADC_name(self):
        return self.__unique_ADC_name

    def update_data(self, timestamp, pre_post, data):
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
        conf = self.send_RPC('get_current_adc_conf')
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
        self.__is_WRTD_master = conf['is_WRTD_master']

    def get_channel(self, channel_idx):
        return self.__channels[channel_idx]

    def get_internal_trigger(self, trigger_idx):
        return self.__internal_triggers[trigger_idx]

    def get_external_trigger(self, trigger_idx):
        return self.__external_triggers[trigger_idx]

    def get_acq_conf(self):
        return self.__acq_conf

    def set_is_WRTD_master(self, WRTD_master):
        self.send_RPC('set_WRTD_master', WRTD_master)
        self.update_conf()

    def get_is_WRTD_master(self):
        return self.__is_WRTD_master

    class MapperMethodsClosure():

        def __getattr__(self, *args):
            """if there is not mapper function defined, return the value
            without mapping"""
            return lambda *x: x[0]

        def map_internal_trigger_threshold(self, value, ADC, idx):
            return threshold_mV_to_raw(value, ADC, idx)

        def map_channel_termination(self, value, ADC, idx):
            return int(value)

        def map_channel_range(self, value, *args):
            channel_ranges = {'10V': 10, '1V': 1, '100mV': 100}
            return channel_ranges[value]

        def map_postsamples(self, value, *args):
            if value == 1:
                value = 2
            """By default the value of postsamples is, but the minimum value
            that could be written is 2.
            If I read the configuration after initialization and want to write
            it back, I cannot, so then instead of writing 1, I write 2"""
            return value

    class PreprocessClosure():

        def __getattr__(self, *args):
            """if the preprocess function not defined, do nothing"""
            return lambda *x: None

        def preprocess_channel_range(self, range_value_str, ADC, channel_idx):
            """ The threshold value is given with respect to range,
            therefore if range is changed, the value in mv has to be
            recalculated"""
            channel = ADC.get_channel(channel_idx)
            previous_range = channel.channel_range
            internal_trigger = ADC.get_internal_trigger(channel_idx)
            curr_threshold = internal_trigger.threshold
            channel_ranges = {'10V': 10, '1V': 1, '100mV': 100}
            new_range = channel_ranges[range_value_str]
            multiplier = {(10, 10): 1, (10, 1): 10, (10, 100): 100,
                          (1, 10): 1/10, (1, 1): 1, (1, 100): 10,
                          (100, 10): 1/100, (100, 1): 10, (100, 100): 1}
            multiplication = multiplier[(previous_range, new_range)]
            threshold = int(curr_threshold * multiplication)
            if (threshold > 2**15-1 or threshold < -2**15):
                ADC.send_RPC('set_adc_parameter',
                             'set_internal_trigger_enable', 0, channel_idx)
                ADC.send_RPC('set_adc_parameter',
                             'set_internal_trigger_threshold', 0, channel_idx)
                logger.warning("Internal trigger disabled: value out of range")
                """TODO send information to the GUI"""
            else:
                ADC.send_RPC('set_adc_parameter',
                             'set_internal_trigger_threshold', threshold,
                             channel_idx)

    def set_ADC_parameter(self, parameter_name, value, idx=None):
        function_name = 'set_' + parameter_name
        mapper_function_name = 'map_' + parameter_name
        preprocess_function_name = 'preprocess_' + parameter_name
        mapper_methods_closure = self.MapperMethodsClosure()
        preprocess_closure = self.PreprocessClosure()
        preprocess_function = getattr(preprocess_closure,
                                      preprocess_function_name)
        mapper_function = getattr(mapper_methods_closure, mapper_function_name)
        mapped_value = None
        try:
            preprocess_function(value, self, idx)
        except Exception as e:
            logger.error("Preprocessing error {}".format(e))
        try:
            mapped_value = mapper_function(value, self, idx)
        except Exception as e:
            logger.error("Mapping error {}".format(e))
        try:
            if idx:
                self.send_RPC('set_adc_parameter', function_name, mapped_value,
                              idx)
            else:
                self.send_RPC('set_adc_parameter', function_name, mapped_value)
        except Exception as e:
            logger.error("Function invocation error {}".format(e))
        self.update_conf()

    def add_used_channel(self, channel):
        self.__used_channels.append(channel)
        self.__used_channels.sort()

    def configure_acquisition(self):
        self.send_RPC('configure_acquisition', self.__used_channels)

    def stop_acquisition(self):
        self.send_RPC('stop_acquisition')

    def set_server_address(self, server_addr):
        self.send_RPC('set_server_address', server_addr)
