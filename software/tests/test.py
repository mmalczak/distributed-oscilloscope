import unittest
import time
import subprocess
from paramiko_connection import start_adc
import xmlrpc.client
import sys
sys.path.append('../general')
from proxy import get_proxy


class OscilloscopeMethods(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(OscilloscopeMethods, self).__init__(*args, **kwargs)
        self.server_handler = subprocess.Popen(
                        'python3 ../server/main_server.py', shell=True)
        self.ADCs = {'ADC1':[8000, 1], 'ADC2':[8001, 2]}
        time.sleep(1)
        ADC1 = self.ADCs['ADC1']
        start_adc(ADC1[0], ADC1[1])
        time.sleep(1)
        ADC2 = self.ADCs['ADC2']
        start_adc(ADC2[0], ADC2[1])
        time.sleep(1)

    def __del__(self, *args, **kwargs):
        super(OscilloscopeMethods, self).__init__(*args, **kwargs)
        time.sleep(1)
        ADC1 = self.ADCs['ADC1']
        proxy = get_proxy("http://spechost:" + str(ADC1[0]) + "/")
        try:
            proxy.exit()
        except Exception as e:
            print(e)
        """There will be error until test programm will implement XMLRPC
        server"""
        time.sleep(1)
        ADC2 = self.ADCs['ADC2']
        proxy = get_proxy("http://spechost:" + str(ADC2[0]) + "/")
        try:
            proxy.exit()
        except Exception as e:
            print(e)
        time.sleep(1)
        self.server_handler.terminate()

    def test_upper(self):
        self.assertEqual("abc", "abc")
       

