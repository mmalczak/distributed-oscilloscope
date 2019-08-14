"""
expose.py
============================================
Exposes the functionalities of the Server to Device Applications and to
User Applications. All communication with other applications is done using
Expose class.
For communication with the nodes it uses `ZeroMQ <https://zeromq.org/>`_
sockets.

"""

from zmq.utils.monitor import recv_monitor_message
from zmq.utils.monitor import parse_monitor_message
import zmq
import pickle
import logging
logger = logging.getLogger(__name__)
from DistributedOscilloscope.utilities.ipaddr import get_ip
from DistributedOscilloscope.utilities import serialization


class Expose():
    """
    Top level class.

    :param connection_manager: :class:`~server.connection_manager.ConnectionManager`
    :param port_user: port on which it listens for User Applications connections
    :param port_device: port on which it listens for devices connections

    """
    def __init__(self, connection_manager, port_user, port_device):
        self.__connection_manager = connection_manager
        self.__port_user = port_user
        self.__port_device = port_device
        self.run()

    def add_channel(self, oscilloscope_channel_idx, unique_ADC_name,
                    ADC_channel_idx, user_app_name):
        """
        Called by the User Application.
        Adds channel in the User Application.

        :param oscilloscope_channel_idx: index of the channel in the user\
            application
        :param unique_ADC_name: name of the Device Application (ADC)
        :param ADC_channel_index: channel index of the ADC
        :param user_app_name: name of the User Application
        """
        user_app = self.__connection_manager.get_user_app(user_app_name)
        ADC = self.__connection_manager.get_ADC(unique_ADC_name)
        user_app.add_channel(oscilloscope_channel_idx, ADC, ADC_channel_idx)

    def remove_channel(self, oscilloscope_channel_idx, user_app_name):
        """
        Called by the User Application.
        Removes channel from the User Application.

        :param oscilloscope_channel_idx: index of the channel in the user\
            application
        :param user_app_name: name of the User Application
        """

        user_app = self.__connection_manager.get_user_app(user_app_name)
        user_app.remove_channel(oscilloscope_channel_idx)

    def add_trigger(self, type, unique_ADC_name, ADC_trigger_idx,
                    user_app_name):
        """
        Called by the User Application.
        Adds trigger in the User Application.

        :param type: type of the trigger
        :param unique_ADC_name: name of the Device Application (ADC)
        :param ADC_trigger_index: trigger index of the ADC
        :param user_app_name: name of the User Application
        """
        user_app = self.__connection_manager.get_user_app(user_app_name)
        ADC = self.__connection_manager.get_ADC(unique_ADC_name)
        user_app.add_trigger(type, ADC, ADC_trigger_idx)

    def remove_trigger(self, user_app_name):
        """
        Called by the User Application.
        Removes trigger from the User Application.

        :param user_app_name: name of the User Application
        """
        user_app = self.__connection_manager.get_user_app(user_app_name)
        user_app.remove_trigger()

    def set_ADC_parameter(self, parameter_name, value, unique_ADC_name,
                          idx=None):
        """
        Called by the User Application.
        Generic function, used to modify parameters of the ADC.

        :param parameter_name: name of the parameter to be modified
        :param value: new value of the parameter
        :param unique_ADC_name: name of the Device Application (ADC)
        :param idx: index of the given parameter if applies
        """

        ADC = self.__connection_manager.get_ADC(unique_ADC_name)
        try:
            ADC.set_ADC_parameter(parameter_name, value, idx)
        except Exception as e:
            print("Set_ADC_parameter error {}".format(e))

    def single_acquisition(self, user_app_name):
        """
        Called by the User Application.
        Starts single acquisition in the given User Application.

        :param user_app_name: name of the User Application
        """
        user_app = self.__connection_manager.get_user_app(user_app_name)
        user_app.configure_acquisition_ADCs_used()

    def run_acquisition(self, run, user_app_name):
        """
        Called by the User Application.
        Starts or stops continuous acquisition in the given User Application.

        :param run: defines if the acquisition is to be started or stopped
        :param user_app_name: name of the User Application
        """

        user_app = self.__connection_manager.get_user_app(user_app_name)
        user_app.run_acquisition(run)

    def set_pre_post_samples(self, presamples, postsamples, user_app_name):
        """
        Called by the User Application.
        Defines he number of presamples and postsamples that are to be set in
        all ADCs used by the given User Application.

        :param presamples: number of presamples
        :param postsamples: number of postsamples
        :param user_app_name: name of the User Application
        """

        user_app = self.__connection_manager.get_user_app(user_app_name)
        user_app.set_pre_post_samples(presamples, postsamples)

    def get_user_app_settings(self, user_app_name):
        """
        Called by the User Application.
        Retrieves the parameters of channels and trigger used by the
        particular User Application as well as length of the acquisition.

        :param user_app_name: name of the User Application

        :return: Dictionary with required settings
        """
        user_app = self.__connection_manager.get_user_app(user_app_name)
        return user_app.get_user_app_settings()

    def register_user_app(self, user_app_name, addr, port):
        """
        Called by the User Application.
        Registers User Application in the Distributed Oscilloscope.

        :param addr: IP address of the socket of the User Application
        :param port: port of the socket of the User Application
        :param user_app_name: name of the User Application
        """
        self.__connection_manager.register_user_app(user_app_name, str(addr),
                                                    port)

    def unregister_user_app(self, user_app_name):
        """
        Called by the User Application.
        Unregisters User Application in the Distributed Oscilloscope.

        :param user_app_name: name of the User Application
        """
        self.__connection_manager.unregister_user_app(user_app_name)

    """---------------------------ADC--------------------------------------"""
    def update_data(self, timestamp, pre_post, data, unique_ADC_name):
        """
        Called by the Device Application.

        Adds the acquisition data to the acquisition data queue in the ADC.
        Every time the new data arrives, the ADC notifies the User Application
        class, which checks if all rrequired data has arrived and is properly
        aligned. If yes, it sends the data to the actuall User Application.

        :param timestamp: timestamp with the information about the time of the
            trigger
        :param pre_post: number of acquired presamples and postsamples
        :param data: dictionary with ADC channels indexes as keys, containing
            acquisition data
        :param unique_ADC_name: name of the Device Application (ADC)
        """
        if(data == 0):
            self.__connection_manager.stop_acquisition_if_user_app_contains_ADC(
                                                            unique_ADC_name)
            logger.warning("Received empty data")
            return
        ADC = self.__connection_manager.get_ADC(unique_ADC_name)
        ADC.update_data(timestamp, pre_post, data)
        return True

    def register_ADC(self, unique_ADC_name, addr, port):
        """
        Called by the Device Application.
        Registers Device Application (ADC) in the Distributed Oscilloscope.

        :param unique_ADC_name: name of the Device Application (ADC)
        :param addr: IP address of the socket of the Device Application (ADC)
        :param port: port of the socket of the Device Application (ADC)

        """
        self.__connection_manager.register_ADC(unique_ADC_name, str(addr),
                                               port)

    def unregister_ADC(self, unique_ADC_name):
        """
        Called by the Device Application.
        Unregisters ADC in the Distributed Oscilloscope.

        :param unique_ADC_name: name of the Device Application (ADC)
        """
        self.__connection_manager.unregister_ADC(unique_ADC_name)

    """---------------------------ADC--------------------------------------"""

    """----------------- TESTING ------------------------------------------"""
    def get_user_app_channels(self, user_app_name):
        user_app = self.__connection_manager.get_user_app(user_app_name)
        return user_app.get_channels_copy()
    """----------------- TESTING ------------------------------------------"""

    def run(self):
        """
        Called when the object of the class is created.
        It listens in the loop for messages from
        Device Applications (socket_ADC_listener),
        User Applications (socket_user_listener)
        and from Zeroconf (zeroconf_listener).
        The monitor socket is used to monitor the state of ZeroMQ connection.

        The message contain the name of the method to call. Since communication
        with the User Applications is synchronous, the socket_user_listener
        sends back the data returned by the called funciton. In case of
        socket_ADC_listener and zeroconf_listener the communication is
        asynchronous

        """
        EVENT_MAP = {}
        for name in dir(zmq):
            if name.startswith('EVENT_'):
                value = getattr(zmq, name)
                EVENT_MAP[value] = name

        context = zmq.Context()

        socket_user_listener = context.socket(zmq.ROUTER)
        monitor = socket_user_listener.get_monitor_socket()
        socket_ADC_listener = context.socket(zmq.ROUTER)
        socket_zeroconf_listener = context.socket(zmq.ROUTER)

        server_ip = get_ip()
        socket_user_listener.bind("tcp://" + server_ip + ":" +
                    str(self.__port_user))
        socket_ADC_listener.bind("tcp://" + server_ip + ":" +
                                 str(self.__port_device))
        socket_zeroconf_listener.bind("ipc:///tmp/zeroconf")

        poller = zmq.Poller()
        poller.register(monitor, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket_user_listener, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket_ADC_listener, zmq.POLLIN | zmq.POLLERR)
        poller.register(socket_zeroconf_listener, zmq.POLLIN | zmq.POLLERR)

        while True:
            socks = dict(poller.poll())
            if socket_user_listener in socks:
                [identity, message] = socket_user_listener.recv_multipart()
                message = pickle.loads(message)
                try:
                    func = getattr(self, message[0])
                    ret = func(*message[1:])
                    ret = pickle.dumps(ret)
                    socket_user_listener.send_multipart([identity, ret])
                except AttributeError:
                    socket_user_listener.send_multipart([identity, b"Error"])
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
