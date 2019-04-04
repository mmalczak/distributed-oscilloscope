import threading
import os
from proxy import *
from service_management import *

class ThreadADC_Expose(threading.Thread):
    def __init__(self, osc):
        threading.Thread.__init__(self)
        self.osc = osc
    def add_service(self, name, addr, port, conf):
        add_service(name, addr, port, self.osc, conf, server_addr_known=True)
    def remove_service(self, name):
        remove_service(name, self.osc)

    def update_data(self, timestamp_and_data, unique_ADC_name):
        self.osc.update_data(timestamp_and_data, unique_ADC_name)
        return True
    def run(self):
        self.server = SimpleXMLRPCServer(('', 7999), allow_none=True, logRequests=False)
        print("Listening on port 7999...")

        self.server.register_function(self.add_service, "add_service")
        self.server.register_function(self.remove_service, "remove_service")
        self.server.register_function(self.update_data, "update_data")
        self.server.serve_forever()


