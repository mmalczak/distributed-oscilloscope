from zmq.utils.monitor import recv_monitor_message
from zmq.utils.monitor import parse_monitor_message
from ipaddr import get_ip
import zmq
import pickle
import logging
logger = logging.getLogger(__name__)


class Expose():

    def __init__(self, osc):
        self.osc = osc
        self.run()

    def add_channel(self, oscilloscope_channel_idx, unique_ADC_name,
                    ADC_channel_idx, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        ADC = self.osc.get_ADC(unique_ADC_name)
        GUI.add_channel(oscilloscope_channel_idx, ADC, ADC_channel_idx)

    def remove_channel(self, oscilloscope_channel_idx, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        GUI.remove_channel(oscilloscope_channel_idx)

    def add_trigger(self, type, unique_ADC_name, ADC_trigger_idx, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        ADC = self.osc.get_ADC(unique_ADC_name)
        GUI.add_trigger(type, ADC, ADC_trigger_idx)

    def remove_trigger(self, GUI_name):
        GUI = self.osc.get_GUI(GUI_name)
        GUI.remove_trigger()

    def set_ADC_parameter(self, parameter_name, value, unique_ADC_name,
                          idx=None):
        ADC = self.osc.get_ADC(unique_ADC_name)
        try:
            ADC.set_ADC_parameter(parameter_name, value, idx)
        except Exception as e:
            print("Set_ADC_parameter error {}".format(e))

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
        server_ip = get_ip()
        socket.bind("tcp://" + server_ip + ":8003")
        socket_ADC_listener.bind("tcp://" + server_ip + ":8023")

        poller = zmq.Poller()
        poller.register(monitor, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket_ADC_listener, zmq.POLLIN | zmq.POLLERR)

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
                data = pickle.loads(message)
                try:
                    getattr(self, data['function_name'])(*data['args'])
                except AttributeError as e:
                    logger.error("Attribute error: {}".format(e))
            self.osc.check_timing()
