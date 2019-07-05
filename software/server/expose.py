from zmq.utils.monitor import recv_monitor_message
from zmq.utils.monitor import parse_monitor_message
import zmq
import pickle
import logging
import sys
logger = logging.getLogger(__name__)
sys.path.append('../')
from general.ipaddr import get_ip
from general.addresses import server_expose_to_user_port
from general.addresses import server_expose_to_device_port
from general import serialization

class Expose():

    def __init__(self, connection_manager):
        self.__connection_manager = connection_manager
        self.run()

    def add_channel(self, oscilloscope_channel_idx, unique_ADC_name,
                    ADC_channel_idx, GUI_name):
        GUI = self.__connection_manager.get_GUI(GUI_name)
        ADC = self.__connection_manager.get_ADC(unique_ADC_name)
        GUI.add_channel(oscilloscope_channel_idx, ADC, ADC_channel_idx)

    def remove_channel(self, oscilloscope_channel_idx, GUI_name):
        GUI = self.__connection_manager.get_GUI(GUI_name)
        GUI.remove_channel(oscilloscope_channel_idx)

    def add_trigger(self, type, unique_ADC_name, ADC_trigger_idx, GUI_name):
        GUI = self.__connection_manager.get_GUI(GUI_name)
        ADC = self.__connection_manager.get_ADC(unique_ADC_name)
        GUI.add_trigger(type, ADC, ADC_trigger_idx)

    def remove_trigger(self, GUI_name):
        GUI = self.__connection_manager.get_GUI(GUI_name)
        GUI.remove_trigger()

    def set_ADC_parameter(self, parameter_name, value, unique_ADC_name,
                          idx=None):
        ADC = self.__connection_manager.get_ADC(unique_ADC_name)
        try:
            ADC.set_ADC_parameter(parameter_name, value, idx)
        except Exception as e:
            print("Set_ADC_parameter error {}".format(e))

    def single_acquisition(self, GUI_name):
        GUI = self.__connection_manager.get_GUI(GUI_name)
        GUI.configure_acquisition_ADCs_used()

    def run_acquisition(self, run, GUI_name):
        GUI = self.__connection_manager.get_GUI(GUI_name)
        GUI.run_acquisition(run)

    def set_pre_post_samples(self, presamples, postsamples, GUI_name):
        GUI = self.__connection_manager.get_GUI(GUI_name)
        GUI.set_pre_post_samples(presamples, postsamples)

    def get_GUI_settings(self, GUI_name):
        GUI = self.__connection_manager.get_GUI(GUI_name)
        return GUI.get_GUI_settings()

    def register_GUI(self, GUI_name, addr, port):
        self.__connection_manager.register_GUI(GUI_name, str(addr), port)

    def unregister_GUI(self, GUI_name):
        self.__connection_manager.unregister_GUI(GUI_name)

    """---------------------------ADC--------------------------------------"""
    def update_data(self, timestamp, pre_post, data, unique_ADC_name):
        if(data == 0):
            self.__stop_acquisition_if_GUI_contains_ADC(unique_ADC_name)
            return
        """TODO add logging, do sth"""
        ADC = self.__connection_manager.get_ADC(unique_ADC_name)
        ADC.update_data(timestamp, pre_post, data)
        return True

    def register_ADC(self, unique_ADC_name, addr, port):
        self.__connection_manager.register_ADC(unique_ADC_name, str(addr),
                                               port)

    def unregister_ADC(self, unique_ADC_name):
        self.__connection_manager.unregister_ADC(unique_ADC_name)

    """---------------------------ADC--------------------------------------"""

    """----------------- TESTING ------------------------------------------"""
    def get_GUI_channels(self, GUI_name):
        GUI = self.__connection_manager.get_GUI(GUI_name)
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
        socket_zeroconf_listener = context.socket(zmq.ROUTER)

        server_ip = get_ip()
        socket.bind("tcp://" + server_ip + ":" +
                    str(server_expose_to_user_port))
        socket_ADC_listener.bind("tcp://" + server_ip + ":" +
                                 str(server_expose_to_device_port))
        socket_zeroconf_listener.bind("ipc:///tmp/zeroconf")

        poller = zmq.Poller()
        poller.register(monitor, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket_ADC_listener, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket_zeroconf_listener, zmq.POLLIN | zmq.POLLERR)

        while True:
            socks = dict(poller.poll(100))
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
                data = serialization.deserialize(message)
                try:
                    getattr(self, data['function_name'])(*data['args'])
                except AttributeError as e:
                    logger.error("Attribute error: {}".format(e))
            if socket_zeroconf_listener in socks:
                [identity, message] = socket_zeroconf_listener.recv_multipart()
                data = pickle.loads(message)
                try:
                    getattr(self.__connection_manager,
                            data['function_name'])(*data['args'])
                except AttributeError as e:
                    logger.error("Attribute error: {}".format(e))
