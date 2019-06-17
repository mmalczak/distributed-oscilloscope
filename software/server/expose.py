import threading
import os
from service_management import *
from conversion import threshold_mV_to_raw
import zmq
from zmq.utils.monitor import recv_monitor_message
from zmq.utils.monitor import parse_monitor_message
import pickle
from ipaddr import get_ip
import logging
logger = logging.getLogger(__name__)


class ThreadGUI_zmq_Expose(threading.Thread):
    def __init__(self, osc):
        threading.Thread.__init__(self)
        self.osc = osc

    def add_channel(self, oscilloscope_channel_idx, unique_ADC_name,
                    ADC_channel_idx, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        GUI.add_channel(oscilloscope_channel_idx, unique_ADC_name,
                                            ADC_channel_idx)

    def remove_channel(self, oscilloscope_channel_idx, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        GUI.remove_channel(oscilloscope_channel_idx)

    def add_trigger(self, type, unique_ADC_name, ADC_trigger_idx, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        GUI.add_trigger(type, unique_ADC_name, ADC_trigger_idx)
        try:
            ADC = self.osc.get_ADC(unique_ADC_name)
            ADC.set_WRTD_master(True)
            zmq_rpc = ADC.zmq_rpc
            zmq_rpc.send_RPC('set_WRTD_master', True)
        except Exception as e:
            print(e)

    def remove_trigger(self, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        trigger = GUI.trigger
        try:
            function_name = 'set_' + trigger.type + '_trigger_enable'
            self.send_RPC_request(function_name, trigger.unique_ADC_name, 0,
                                  trigger.ADC_trigger_idx)
            ADC = self.osc.get_ADC(trigger.unique_ADC_name)
            ADC.set_WRTD_master(False)
            zmq_rpc = ADC.zmq_rpc
            zmq_rpc.send_RPC('set_WRTD_master', False)
        except Exception as e:
            print(e)
        GUI.remove_trigger()

    def set_channel_range(self, range_value_str, channel_idx,
                          unique_ADC_name):
        channel_ranges = {'10V': 10, '1V': 1, '100mV': 100}
        ADC = self.osc.get_ADC(unique_ADC_name)
        zmq_rpc = ADC.zmq_rpc
        ret = zmq_rpc.send_RPC('set_adc_parameter', 'set_channel_range',
                               channel_idx,  channel_ranges[range_value_str])
        internal_trigger = ADC.get_internal_trigger(channel_idx)
        curr_threshold = internal_trigger.threshold
        channel = ADC.get_channel(idx)
        curr_range = channel.channel_range
        new_range = channel_ranges[range_value_str]
        multiplier = {(10, 10): 1, (10, 1): 10, (10, 100): 100,
                      (1, 10): 1/10, (1, 1): 1, (1, 100): 10,
                      (100, 10): 1/100, (100, 1): 10, (100, 100): 1}
        threshold = int(curr_threshold*multiplier[(curr_range, new_range)])
        if (threshold > 2**15-1 or threshold < -2**15):
            self.send_RPC_request('set_internal_trigger_enable',
                                  unique_ADC_name, 0, channel_idx)
            self.send_RPC_request('set_internal_trigger_threshold',
                                  unique_ADC_name, 0, channel_idx)
            logger.warning("Internal trigger disabled: value out of range")
            """TODO send information to the GUI"""
        else:
            self.send_RPC_request('set_internal_trigger_threshold',
                                  unique_ADC_name, threshold, channel_idx)
        ADC.update_conf()


    def set_ADC_parameter(self, parameter_name, value, unique_ADC_name,
                          idx=-1):
        function_name = 'set_' + parameter_name
        mapper_function_name = 'map_' + parameter_name
        mapper_methods_closure = self.MapperMethodsClosure()
        mapper_function = getattr(mapper_methods_closure, mapper_function_name)
        ADC = self.osc.get_ADC(unique_ADC_name)
        ADC_value = mapper_function(value, ADC, idx)
        self.send_RPC_request(function_name, unique_ADC_name, ADC_value, idx)
        ADC = self.osc.get_ADC(unique_ADC_name)
        ADC.update_conf()

    def send_RPC_request(self, function_name, unique_ADC_name, ADC_value, idx):
        ADC = self.osc.get_ADC(unique_ADC_name)
        zmq_rpc = ADC.zmq_rpc
        zmq_rpc.send_RPC('set_adc_parameter', function_name, idx, ADC_value)

    class MapperMethodsClosure():

        def __getattr__(self, *args):
            return lambda *x: x[0]

        def map_internal_trigger_threshold(self, value, *args):
            return threshold_mV_to_raw(value, *args)

        def map_channel_termination(self, value, *args):
            return int(value)

    def single_acquisition(self, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        GUI.configure_acquisition_ADCs_used()

    def run_acquisition(self, run, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        GUI.run_acquisition(run)

    def set_presamples(self, value, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        GUI.set_presamples(value)

    def set_postsamples(self, value, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        GUI.set_postsamples(value)

    def get_GUI_settings(self, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        return GUI.get_GUI_settings()

    def register_GUI(self, GUI_name, addr, port):
        self.osc.register_GUI(GUI_name, str(addr), port)

    def unregister_GUI(self, GUI_name):
        self.osc.unregister_GUI(GUI_name)


    """---------------------------ADC--------------------------------------"""
    def update_data(self, timestamp, pre_post, data, unique_ADC_name):
        self.osc.update_data(timestamp, pre_post, data, unique_ADC_name)
        return True

    def register_ADC(self, unique_ADC_name, addr, port, conf):
        self.osc.register_ADC(unique_ADC_name, conf['board_conf']['n_chan'],
                              str(addr), port)

    def unregister_ADC(self, unique_ADC_name):
        self.osc.unregister_ADC(unique_ADC_name)


    """---------------------------ADC--------------------------------------"""

    """---------------------COMMON TO ADC AND GUI--------------------------"""
    def add_service(self, name, addr, port, conf=None):
        """TODO get rid of conf"""
        if conf:  # ADC version
            add_service(name, addr, port, self.osc, conf,
                        server_addr_known=True)
        else:  # GUI version
            add_service(name, addr, port, self.osc)

    def remove_service(self, name):
        remove_service(name, self.osc)
    """---------------------COMMON TO ADC AND GUI--------------------------"""


    """----------------- TESTING ------------------------------------------"""
    def get_GUI_channels(self, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        return GUI.get_channels_copy()
    """----------------- TESTING ------------------------------------------"""


    def run(self):
        EVENT_MAP = {}
        for name in dir(zmq):
            if name.startswith('EVENT_'):
                value = getattr(zmq, name)
                EVENT_MAP[value] = name

        context = zmq.Context()
        socket = context.socket(zmq.ROUTER)
        monitor = socket.get_monitor_socket()
        socket_ADC_listener = context.socket(zmq.ROUTER)
        #socket.bind("tcp://*:8003")
        server_ip = get_ip()
        socket.bind("tcp://" + server_ip  + ":8003")
        socket_ADC_listener.bind("tcp://" + server_ip  + ":8023")

        poller = zmq.Poller()
        poller.register(monitor, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket_ADC_listener, zmq.POLLIN | zmq.POLLERR)

        while True:
            socks = dict(poller.poll())
            if socket in socks:
                [identity, message] = socket.recv_multipart()
                message = pickle.loads(message)
                try:
                    func = getattr(self, message[0])
                    ret = func(*message[1:])
                    ret = pickle.dumps(ret)
                    socket.send_multipart([identity, ret])
                except AttributeError:
                    socket.send_multipart([identity, b"Error"])
            if monitor in socks:
                evt = recv_monitor_message(monitor)
                evt.update({'description': EVENT_MAP[evt['event']]})
                logger.info("Event: {}".format(evt))
            if socket_ADC_listener in socks:
                [identity, message] = socket_ADC_listener.recv_multipart()
                data = pickle.loads(message)
                try:
                    getattr(self, data['function_name'])(*data['args'])
                except AttributeError:
                    logger.error("Attribute error")
