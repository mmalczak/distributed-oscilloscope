import multiprocessing
from xmlrpc.server import SimpleXMLRPCServer
from timeit import default_timer as timer
import matplotlib.pyplot as plt
from test_conf import update_data_type
import sys
sys.path.append('../')
from general.ipaddr import get_ip
import zmq
import pickle
from general import serialization

class ServerExposeTest():

    def __init__(self, GUI, port_GUI):
        self.port_GUI = port_GUI
        self.GUI = GUI
        self.return_queue = None
        update_data_name = 'update_data_' + update_data_type
        self.update_data = getattr(self, update_data_name)
        self.number_of_acquisitions = 0

    def unregister_ADC(self, unique_ADC_name):
        self.return_queue.put(unique_ADC_name)

    def register_ADC(self, unique_ADC_name, number_of_channels):
        self.return_queue.put((unique_ADC_name, number_of_channels))

    def update_data_plot(self, *args, **kwargs):
        data = args[0]
        chan0 = data[0]
        chan1 = data[1]
        plt.plot(chan0, linewidth=0.5)
        plt.plot(chan1, linewidth=0.5)
        plt.show()
        self.return_queue.put("Plot closed")

    def update_data_time_measurements(self, *args, **kwargs):
        time_end = timer()
        self.return_queue.put(time_end)
        print("GUI: update GUI")

    def update_data_frequency_measurements(self, *args, **kwargs):
        self.number_of_acquisitions += 1
        time = timer()
        self.return_queue.put([self.number_of_acquisitions, time])

    def monitorSlot(self, return_queue):
        self.return_queue = return_queue
        context = zmq.Context()
        socket = context.socket(zmq.ROUTER)
        ip = get_ip()
        socket.bind("tcp://" + ip  + ":" + str(self.port_GUI))
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN | zmq.POLLERR)
        while True:
            socks = dict(poller.poll())
            if socket in socks:
                [identity, message] = socket.recv_multipart()
                data = serialization.deserialize(message)
                getattr(self, data['function_name'])(*data['args'])




class ThreadServerExposeTest():

    def __init__(self, GUI, port_GUI, return_queue):
        super().__init__()
        self.server_expose_test = ServerExposeTest(GUI, port_GUI)
        self.thread = multiprocessing.Process(
                target=self.server_expose_test.monitorSlot, args=(return_queue,))
        """The same as threading.Thread but I can terminate process
        externally, maybe not perfect solution, but good enough as long as I
        am using XMLRPC"""
        self.thread.start()
