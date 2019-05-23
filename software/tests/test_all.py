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
from multiprocessing import Queue
from timeit import default_timer as timer

server_addr = '128.141.79.50'
ADC_addr = '128.141.162.185'

class OscilloscopeMethods(unittest.TestCase):

    server_handler = None
    server_expose = None
    ADCs = {'ADC1':[8000, 1], 'ADC2':[8001, 2]}
    delay = 0.4
    return_queue = None
    GUI_name = None

    @classmethod
    def setUpClass(cls):
        cls.start_server(cls)
        cls.create_GUI_interface(cls)
        cls.start_zeroconf(cls)
        cls.add_ADC_FEC(cls, 'ADC1') 
        cls.add_ADC_FEC(cls, 'ADC2') 
        while not cls.return_queue.empty():
            cls.return_queue.get()

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
        self.GUI_name = GUI_name
        zeroconf_info = zeroconf.ServiceInfo("_http._tcp.local.", GUI_name,
                                             zeroconf.socket.inet_aton(addr),
                                             8000,
                                             properties={'addr': addr,
                                                         'port': str(port)})
        zeroconf_service = zeroconf.Zeroconf()
        zeroconf_service.register_service(zeroconf_info)
        time.sleep(self.delay)

    def clean_queue(self):
        while not self.return_queue.empty():
            self.return_queue.get()

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

        self.return_queue = Queue()
        self.server_expose = ThreadServerExposeTest(None, 8001,
                                                    self.return_queue)
        time.sleep(self.delay)

    def stop_GUI_interface(self):
        self.server_handler.terminate()
        time.sleep(self.delay)

    def test_add_remove_available_ADC(self):
        self.clean_queue()
        self.remove_ADC_FEC('ADC2')
        expected_port = str(self.ADCs['ADC2'][0])

        removed_ADC_name = self.return_queue.get()
        self.assertTrue(expected_port in removed_ADC_name)
        self.assertTrue('ADC' in removed_ADC_name)
        """Will think of the proper naming in the future, now just checking
        if at least the port is ok and the name starts with ADC"""

        self.add_ADC_FEC('ADC2')
        return_values = self.return_queue.get()
        added_ADC_name = return_values[0]
        number_of_channels = return_values[1]
        self.assertTrue(expected_port in added_ADC_name)
        self.assertTrue('ADC' in added_ADC_name)
        self.assertEqual(number_of_channels, 4)

    def test_channels_empty(self):
        proxy = get_proxy("http://" + server_addr + ":" + str(8000) + "/")
        channels = proxy.get_GUI_channels(self.GUI_name)
        self.assertTrue(not channels)

    def test_acquisition(self):
        results = open("results.txt", "a")
        proxy = get_proxy("http://" + server_addr + ":" + str(8000) + "/")

        ADC_idx = ADC_addr + "_" + str(self.ADCs['ADC1'][0])
        unique_ADC_name = "ADC" + "_" + ADC_idx + "._tcp.local."

        oscilloscope_channel_idx = 0
        ADC_channel = 0
        proxy.add_channel(oscilloscope_channel_idx, unique_ADC_name,
                          ADC_channel, self.GUI_name)
        time.sleep(self.delay)

        oscilloscope_channel_idx = 1
        ADC_channel = 1
        proxy.add_channel(oscilloscope_channel_idx, unique_ADC_name,
                          ADC_channel, self.GUI_name)
        time.sleep(self.delay)

        oscilloscope_channel_idx = 2
        ADC_channel = 2
        proxy.add_channel(oscilloscope_channel_idx, unique_ADC_name,
                          ADC_channel, self.GUI_name)
        time.sleep(self.delay)

        oscilloscope_channel_idx = 3
        ADC_channel = 3
        proxy.add_channel(oscilloscope_channel_idx, unique_ADC_name,
                          ADC_channel, self.GUI_name)
        time.sleep(self.delay)

        ADC_trigger_idx = 3
        proxy.add_trigger('internal', unique_ADC_name, ADC_trigger_idx,
                          self.GUI_name)


        proxy.set_ADC_parameter('internal_trigger_enable', 1 , unique_ADC_name,
                                ADC_trigger_idx)
        time.sleep(self.delay)

        proxy.set_ADC_parameter('postsamples', 2 , unique_ADC_name)
        time.sleep(self.delay)

        self.clean_queue()

        print("Send acquistion command")
        results.write("XMLRPC performance")
        proxy.single_acquisition(self.GUI_name)
        time_start = timer()
        time.sleep(self.delay)
        time_end = self.return_queue.get()
        time_diff = time_end - time_start
        time_diff_txt = str(time_diff) + '\n'
        results.write(time_diff_txt)

        time.sleep(3)
        results.close()

#    def test_add_channel(self):
#        proxy = get_proxy("http://" + server_addr + ":" + str(8000) + "/")
#        GUI_channel = 0
#        ADC_channel = 0
#        ADC_idx = ADC_addr + "_" + str(self.ADCs['ADC1'][0])
#        ADC_name = "ADC" + "_" + ADC_idx + "._tcp.local."
#        proxy.add_channel(GUI_channel, ADC_name, ADC_channel, self.GUI_name)
#        channels = proxy.get_GUI_channels(self.GUI_name)
#        print(channels)

    def test_remove_available_ADC(self):
        self.assertEqual("abc", "abc")
