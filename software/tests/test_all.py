import unittest
import time
import subprocess
from paramiko_connection import start_adc
import xmlrpc.client
import sys
sys.path.append('../general')
from proxy import get_proxy
from server_expose_test import ThreadServerExposeTest
import zeroconf
import os

class OscilloscopeMethods(unittest.TestCase):

    server_handler = None
    server_expose = None
    ADCs = {'ADC1':[8000, 1], 'ADC2':[8001, 2]}
    delay = 0.5

    @classmethod
    def setUpClass(cls):
        cls.start_server(cls)
        cls.create_GUI_interface(cls)
        cls.start_zeroconf(cls)
        cls.add_ADC_FEC(cls, 'ADC1') 
        cls.add_ADC_FEC(cls, 'ADC2') 

    @classmethod
    def tearDownClass(cls):
        cls.remove_ADC_FEC(cls, 'ADC1')
        cls.remove_ADC_FEC(cls, 'ADC2')
        cls.stop_GUI_interface(cls)
        cls.stop_server(cls)

    def start_zeroconf(self):
        #addr = os.popen("ifconfig| grep inet").read().split()[1]
        addr = '128.141.79.50'
        port = 8001
        GUI_idx = addr + "_" + str(port)
        GUI_name = "GUI" + "_" + GUI_idx + "._http._tcp.local."
        zeroconf_info = zeroconf.ServiceInfo("_http._tcp.local.",
                                             GUI_name,
                                             zeroconf.socket.inet_aton(addr),
                                             8000,
                                             properties={'addr': addr,
                                                         'port': str(port)})
        zeroconf_service = zeroconf.Zeroconf()
        zeroconf_service.register_service(zeroconf_info)
        time.sleep(self.delay)

    def add_ADC_FEC(self, name):
        ADC = self.ADCs[name]
        start_adc(ADC[0], ADC[1])
        time.sleep(self.delay)

    def remove_ADC_FEC(self, name):
        ADC = self.ADCs[name]
        proxy = get_proxy("http://spechost:" + str(ADC[0]) + "/")
        try:
            proxy.exit()
        except Exception as e:
            if type(e) is ConnectionRefusedError:
                pass
            else:
                print(e)
        """There will be an error because proxy can never return because 
        the process exits"""
        time.sleep(self.delay)

    def start_server(self):
        command = 'python3 ../server/main_server.py'
        self.server_handler = subprocess.Popen(command, shell=True)
        time.sleep(self.delay)

    def stop_server(self):
        self.server_expose.thread.terminate()
        time.sleep(self.delay)

    def create_GUI_interface(self):
        self.server_expose = ThreadServerExposeTest(None, 8001) 
        time.sleep(self.delay)

    def stop_GUI_interface(self):
        self.server_handler.terminate()
        time.sleep(self.delay)

    def test_upper(self):
        time.sleep(self.delay)
        self.assertEqual("abc", "abc")
       
    def test_upper2(self):
        time.sleep(self.delay)
        self.assertEqual("abc", "abc")
 

