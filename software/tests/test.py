import unittest
import time
import subprocess
from paramiko_connection import start_adc
import xmlrpc.client
import sys
sys.path.append('../general')
from proxy import get_proxy
from server_expose_test import ThreadServerExposeTest

class OscilloscopeMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(OscilloscopeMethods, self).__init__(*args, **kwargs)
        self.server_handler = None
        self.server_expose = None
        self.ADCs = {'ADC1':[8000, 1], 'ADC2':[8001, 2]}
        
        self.start_server()
        self.create_GUI_interface()
        self.add_ADC_FEC('ADC1') 
        self.add_ADC_FEC('ADC2') 

    def __del__(self, *args, **kwargs):
        super(OscilloscopeMethods, self).__init__(*args, **kwargs)
        self.remove_ADC_FEC('ADC1')
        self.remove_ADC_FEC('ADC2')
        self.stop_GUI_interface()
        self.stop_server()

    def add_ADC_FEC(self, name):
        ADC = self.ADCs[name]
        start_adc(ADC[0], ADC[1])
        time.sleep(0.5)

    def remove_ADC_FEC(self, name):
        ADC = self.ADCs[name]
        proxy = get_proxy("http://spechost:" + str(ADC[0]) + "/")
        try:
            proxy.exit()
        except Exception as e:
            #pass
            print(e)
        """There will be error until test programm will implement XMLRPC
        server"""
        time.sleep(0.5)

    def start_server(self):
        command = 'python3 ../server/main_server.py'
        self.server_handler = subprocess.Popen(command, shell=True)
        time.sleep(0.5)

    def stop_server(self):
        self.server_expose.thread.terminate()
        time.sleep(0.5)

    def create_GUI_interface(self):
        self.server_expose = ThreadServerExposeTest(None, 8001) 
        time.sleep(0.5)

    def stop_GUI_interface(self):
        self.server_handler.terminate()
        time.sleep(0.5)

    def test_upper(self):
        time.sleep(0.5)
        self.assertEqual("abc", "abc")
       


