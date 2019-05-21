import multiprocessing 
from xmlrpc.server import SimpleXMLRPCServer 

class ServerExposeTest():

    def __init__(self, GUI, port_GUI):
        super().__init__()
        self.port_GUI = port_GUI
        self.GUI = GUI

    def set_server_address(self, addr):
        pass

    def remove_available_ADC(self, *args, **kwargs):
        pass 

    def add_available_ADC(self, *args, **kwargs):
        pass 

    def update_data(self, *args, **kwargs):
        pass

    def set_horizontal_params(self, *args, **kwargs):
        pass

    def set_channel_params(self, *args, **kwargs):
        pass

    def set_trigger_params(self, *args, **kwargs):
        pass


    def monitorSlot(self):
        server = SimpleXMLRPCServer(("", self.port_GUI),
                                    allow_none=True)
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

    def __init__(self, GUI, port_GUI):
        super().__init__()
        self.server_share = ServerExposeTest(GUI, port_GUI)
        self.thread = multiprocessing.Process(
                target=self.server_share.monitorSlot)
        """The same as threading.Thread but I can terminate process 
        externally, maybe not perfect solution, but good enough as long as I 
        am using XMLRPC"""
        self.thread.start()
