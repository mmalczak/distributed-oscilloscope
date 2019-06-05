import threading
import os
from service_management import *
from conversion import *
import zmq
from zmq.utils.monitor import recv_monitor_message
from zmq.utils.monitor import parse_monitor_message
import pickle
from ipaddr import get_ip
import logging
import logging.config
from logging_conf import DEFAULT_CONFIG

logging.config.dictConfig(DEFAULT_CONFIG)
logger = logging.getLogger(__name__)




def stop_and_retrieve_acquisition(func):
    def wrapper(self, *args, **kwargs):
        unique_ADC_name = None
        for arg in args:
            try:  # find the name of the ADC in the arguments - fixme
                if(arg[0:3] == "ADC"):
                    unique_ADC_name = arg
                    print(arg)
            except:
                pass
        try:
            self.osc.stop_acquisition_if_GUI_contains_ADC(unique_ADC_name)
            func(self, *args, **kwargs)
            self.osc.retrieve_acquisition_if_GUI_contains_ADC(unique_ADC_name)
        except Exception as e:
            print(type(e))
            print(e)
    return wrapper


def update_GUI_after(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        unique_ADC_name = None
        for arg in args:
            try:    # find the name of the ADC in the arguments - fixme
                if(arg[0:3] == "ADC"):
                    unique_ADC_name = arg
                    print(arg)
            except:
                pass
        for GUI_name, GUI in self.osc.GUIs.items():
            for channel_dx, channel_GUI in GUI.channels.items():
                if(channel_GUI.unique_ADC_name == unique_ADC_name):
                    GUI.update_conf(unique_ADC_name)
                    break
    return wrapper


class ThreadGUI_zmq_Expose(threading.Thread):
    def __init__(self, osc):
        threading.Thread.__init__(self)
        self.osc = osc

    def add_channel(self, oscilloscope_channel_idx, unique_ADC_name,
                    ADC_channel_idx, GUI_name):
        GUI = self.osc.GUIs[GUI_name]
        GUI.add_channel(oscilloscope_channel_idx, unique_ADC_name,
                                            ADC_channel_idx)

    def remove_channel(self, oscilloscope_channel_idx, GUI_name):
        self.osc.GUIs[GUI_name].remove_channel(oscilloscope_channel_idx)

    def add_trigger(self, type, unique_ADC_name, ADC_trigger_idx, GUI_name):
        self.osc.GUIs[GUI_name].add_trigger(type, unique_ADC_name,
                                            ADC_trigger_idx)
        try:
            proxy = get_proxy(self.osc.available_ADCs[unique_ADC_name].
                              ADC_proxy_addr)
            proxy.set_WRTD_master(True)
        except Exception as e:
            print(e)

    def remove_trigger(self, GUI_name):
        trigger = self.osc.GUIs[GUI_name].trigger
        try:
            function_name = 'set_' + trigger.type + '_trigger_enable'
            self.send_RPC_request(function_name, trigger.unique_ADC_name, 0,
                                  trigger.ADC_trigger_idx)
            ADC = self.osc.available_ADCs[trigger.unique_ADC_name]
            proxy = get_proxy(ADC.ADC_proxy_addr)
            proxy.set_WRTD_master(False)
        except Exception as e:
            print(e)
        self.osc.GUIs[GUI_name].remove_trigger()

    @stop_and_retrieve_acquisition
    @update_GUI_after
    def set_channel_range(self, range_value_str, channel_idx,
                          unique_ADC_name):
        channel_ranges = {'10V': 10, '1V': 1, '100mV': 100}
        ADC_proxy_addr = self.osc.available_ADCs[unique_ADC_name].\
            ADC_proxy_addr
        proxy = get_proxy(ADC_proxy_addr)
        proxy.set_channel_range(channel_ranges[range_value_str], channel_idx)
        curr_threshold = self.osc.available_ADCs[unique_ADC_name].\
            internal_triggers[channel_idx].threshold
        curr_range = self.osc.available_ADCs[unique_ADC_name].\
            channels[channel_idx].channel_range
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
            print("Internal trigger disabled: value out of range")
            for GUI_name, GUI in self.osc.GUIs.items():
                proxy = get_proxy(GUI.GUI_proxy_addr)
                proxy.print("Internal trigger disabled: value out of range")
        else:
            self.send_RPC_request('set_internal_trigger_threshold',
                                  unique_ADC_name, threshold, channel_idx)

    @stop_and_retrieve_acquisition
    @update_GUI_after
    def set_ADC_parameter(self, parameter_name, value, unique_ADC_name,
                          idx=-1):
        function_name = 'set_' + parameter_name
        mapper_function_name = 'map_' + parameter_name
        mapper_methods_closure = self.MapperMethodsClosure()
        mapper_function = getattr(mapper_methods_closure, mapper_function_name)
        ADC_value = mapper_function(value, unique_ADC_name, idx,
                                    self.osc.available_ADCs)
        self.send_RPC_request(function_name, unique_ADC_name, ADC_value, idx)

    def send_RPC_request(self, function_name, unique_ADC_name, ADC_value, idx):
        proxy = self.get_proxy(unique_ADC_name)
        if(idx == -1):
            proxy.set_adc_parameter(function_name, ADC_value)
        else:
            proxy.set_adc_parameter(function_name, ADC_value, idx)

    def get_proxy(self, unique_ADC_name):
        ADC = self.osc.available_ADCs[unique_ADC_name]
        proxy = get_proxy(ADC.ADC_proxy_addr)
        return proxy

    class MapperMethodsClosure():

        def __getattr__(self, *args):
            return lambda *x: x[0]

        def map_internal_trigger_threshold(self, value, *args):
            return threshold_mV_to_raw(value, *args)

        def map_channel_termination(self, value, *args):
            return int(value)

    def add_service(self, name, addr, port):
        add_service(name, addr, port, self.osc)

    def remove_service(self, name):
        remove_service(name, self.osc)

    def single_acquisition(self, GUI_name):
        self.osc.GUIs[GUI_name].configure_acquisition_ADCs_used()

    def run_acquisition(self, run, GUI_name):
        self.osc.GUIs[GUI_name].run_acquisition(run)

    def set_presamples(self, value, GUI_name):
        print("method set_presamples")
        self.osc.GUIs[GUI_name].set_presamples(value)

    def set_postsamples(self, value, GUI_name):
        self.osc.GUIs[GUI_name].set_postsamples(value)


    """----------------- TESTING ------------------------------------------"""
    def get_GUI_channels(self, GUI_name):
        return self.osc.GUIs[GUI_name].channels

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
        #socket.bind("tcp://*:8003")
        server_ip = get_ip()
        socket.bind("tcp://" + server_ip  + ":8003")

        poller = zmq.Poller()
        poller.register(monitor, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket, zmq.POLLIN | zmq.POLLERR)

        while True:
            socks = dict(poller.poll())
            if socket in socks:
                [identity, message] = socket.recv_multipart()
                message = pickle.loads(message)
                try:
                    func = getattr(self, message[0])
                    func(*message[1:])
                    socket.send_multipart([identity, b"Success"])
                except AttributeError:
                    socket.send_multipart([identity, b"Error"])
            if monitor in socks:
                evt = recv_monitor_message(monitor)
                evt.update({'description': EVENT_MAP[evt['event']]})
                logger.info("Event: {}".format(evt))

