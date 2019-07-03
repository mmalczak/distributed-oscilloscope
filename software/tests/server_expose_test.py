import multiprocessing 
from xmlrpc.server import SimpleXMLRPCServer 
from timeit import default_timer as timer
import matplotlib.pyplot as plt
from test_conf import plot_data
from test_conf import performance_measurements
import sys
sys.path.append('../')
from general.ipaddr import get_ip
import zmq
import pickle
from general import serialization
from general.tcp_server import TCPServer



class ServerExposeTest():

    def __init__(self, GUI, port_GUI):
        self.port_GUI = port_GUI
        self.GUI = GUI
        self.return_queue = None

    def unregister_ADC(self, unique_ADC_name):
        self.return_queue.put(unique_ADC_name)

    def register_ADC(self, unique_ADC_name, number_of_channels):
        self.return_queue.put((unique_ADC_name, number_of_channels))

    def update_data(self, *args, **kwargs):
        if plot_data:
            data = args[0]
            chan0 = data[0]
            chan1 = data[1]
            plt.plot(chan0, linewidth=0.5)
            plt.plot(chan1, linewidth=0.5)
            plt.show()
            self.return_queue.put("Plot closed")
        if performance_measurements:
            time_end = timer()
            self.return_queue.put(time_end)
        print("GUI: update GUI")

    def monitorSlot(self, return_queue):
        self.return_queue = return_queue
        context = zmq.Context() 
        ip = get_ip()    
        poller = zmq.Poller()  

        tcp_server = TCPServer(ip, self.port_GUI, poller)
        poller.register(tcp_server.socket)


        while True:
            socks = dict(poller.poll())

            if tcp_server.socket.fileno() in socks:
                tcp_server.register_connection()
            for sock, event in socks.items():
                if sock in tcp_server.fd_conn:
                    message = tcp_server.receive_packet(sock)
                    if message:
                        data = serialization.deserialize(message)
                        try:
                            getattr(self, data['function_name'])(*data['args'])
                        except AttributeError as e:
                            logger.error("Attribute error: {}".format(e))

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
