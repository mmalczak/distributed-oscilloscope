import multiprocessing 
from xmlrpc.server import SimpleXMLRPCServer 
from timeit import default_timer as timer

class ServerExposeTest():

    def __init__(self, GUI, port_GUI):
        super().__init__()
        self.port_GUI = port_GUI
        self.GUI = GUI
        self.return_queue = None

    def set_server_address(self, addr):
        print("server address set")

    def remove_available_ADC(self, unique_ADC_name):
        self.return_queue.put(unique_ADC_name)

    def add_available_ADC(self, unique_ADC_name, number_of_channels):
        self.return_queue.put((unique_ADC_name, number_of_channels))

    def update_data(self, *args, **kwargs):
        time_end = timer()
        self.return_queue.put(time_end)
        print("GUI: update GUI")

    def set_horizontal_params(self, *args, **kwargs):
        print("GUI: set_horizontal_params")

    def set_channel_params(self, *args, **kwargs):
        print("GUI: set_channel_params")

    def set_trigger_params(self, *args, **kwargs):
        print("GUI: set_trigger_params")

    def monitorSlot(self, return_queue):
        self.return_queue = return_queue
        server = SimpleXMLRPCServer(("", self.port_GUI),
                                    allow_none=True, logRequests=False)
        print("Listening on port " + str(self.port_GUI) + "...")
        server.register_function(self.add_available_ADC, "add_available_ADC")
        server.register_function(self.remove_available_ADC,
                                 "remove_available_ADC")
        server.register_function(self.set_server_address,
                                 "set_server_address")
        server.register_function(self.update_data, "update_data")
        server.register_function(self.set_horizontal_params,
                                 "set_horizontal_params")
        server.register_function(self.set_channel_params,
                                 "set_channel_params")
        server.register_function(self.set_trigger_params,
                                 "set_trigger_params")
        """server.register_function(self.set_acq_params,
                                    "set_acq_params")"""
        server.register_function(print, "print")

        server.serve_forever()


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
