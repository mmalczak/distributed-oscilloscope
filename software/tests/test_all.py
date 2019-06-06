import unittest
import time
import subprocess
from paramiko_connection import start_adc
import xmlrpc.client
import sys
sys.path.append('../general')
from proxy import get_proxy
from server_expose_test import ThreadServerExposeTest
import os
from multiprocessing import Queue
from timeit import default_timer as timer
from test_conf import server_addr
from test_conf import performance_measurements
from zmq_rpc import ZMQ_RPC
from addresses import server_zmq_expose_port

sys.path.append('../server')
import ADC_configs
"""TODO is this the rigth thing to do???"""

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
        cls.zmq_rpc = ZMQ_RPC(server_addr, server_zmq_expose_port)
        cls.connect_to_server(cls)
        cls.add_ADC_FEC(cls, 'ADC1') 
        cls.add_ADC_FEC(cls, 'ADC2') 
        time.sleep(cls.delay)
        while not cls.return_queue.empty():
            cls.return_queue.get()

    @classmethod
    def tearDownClass(cls):
        cls.remove_ADC_FEC(cls, 'ADC1')
        cls.remove_ADC_FEC(cls, 'ADC2')
        time.sleep(cls.delay)
        cls.stop_GUI_interface(cls)
        cls.stop_server(cls)

    def setUp(self):
        if performance_measurements:
            self.results = open("results.txt", "a")

    def tearDown(self):
        if performance_measurements:
            self.results.close()

    def connect_to_server(self):
        #addr = os.popen("ifconfig| grep inet").read().split()[1]
        addr = '128.141.79.50'
        port = 8001
        GUI_idx = addr + "_" + str(port)
        GUI_name = "GUI" + "_" + GUI_idx + "._http._tcp.local."
        self.GUI_name = GUI_name
        self.zmq_rpc.send_RPC('add_service', GUI_name, addr, port)

    def clean_queue(self):
        while not self.return_queue.empty():
            self.return_queue.get()

    def add_ADC_FEC(self, name):
        ADC = self.ADCs[name]
        start_adc(ADC[0], ADC[1])

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

    def start_server(self):
        command = 'python3 ../server/main_server.py'
        self.server_handler = subprocess.Popen(command, shell=True)

    def stop_server(self):
        self.server_expose.thread.terminate()

    def create_GUI_interface(self):

        self.return_queue = Queue()
        self.server_expose = ThreadServerExposeTest(None, 8001,
                                                    self.return_queue)

    def stop_GUI_interface(self):
        self.server_handler.terminate()

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
        channels = self.zmq_rpc.send_RPC('get_GUI_channels', self.GUI_name)
        self.assertTrue(not channels)

    def add_channel(self, idx, unique_ADC_name):
        oscilloscope_channel_idx = idx
        ADC_channel = idx
        self.zmq_rpc.send_RPC('add_channel', oscilloscope_channel_idx, 
                              unique_ADC_name, ADC_channel, self.GUI_name)

    def remove_channel(self, idx):
        oscilloscope_channel_idx = idx
        ADC_channel = idx
        self.zmq_rpc.send_RPC('remove_channel', oscilloscope_channel_idx, 
                              self.GUI_name)

    def add_internal_trigger(self, idx, unique_ADC_name):
        ADC_trigger_idx = 3
        self.zmq_rpc.send_RPC('add_trigger', 'internal', unique_ADC_name, 
                              ADC_trigger_idx, self.GUI_name)
        self.zmq_rpc.send_RPC('set_ADC_parameter', 'internal_trigger_enable',
                              1 , unique_ADC_name, ADC_trigger_idx)

    def set_presamples(self, value, unique_ADC_name):
        self.zmq_rpc.send_RPC('set_ADC_parameter', 'presamples', value,
                              unique_ADC_name)

    def set_postsamples(self, value, unique_ADC_name):
        self.zmq_rpc.send_RPC('set_ADC_parameter', 'postsamples', value,
                              unique_ADC_name)

    def measure_acquisition_time(self):
        self.zmq_rpc.send_RPC('single_acquisition', self.GUI_name)
        time_start = timer()
        time_end = self.return_queue.get()
        time_diff = time_end - time_start
        return time_diff

    @unittest.skipUnless(performance_measurements, "Only for measurements")
    def test_acquisition_time(self):
        self.clean_queue()
    
        self.results.write("Internal trigger on channel 3\n"
                            "Sampled signal: 100kHz sine wave Channel 3(0-3)\n"
                            "number of presamples = 0\n\n")

        ADC_idx = ADC_addr + "_" + str(self.ADCs['ADC1'][0])
        unique_ADC_name = "ADC" + "_" + ADC_idx + "._tcp.local."

        for j in range(3, -1, -1):
            self.results.write("Number of channels: " + str(4-j) + "\n")
            self.add_channel(j, unique_ADC_name)
            if j == 3:
                self.add_internal_trigger(3, unique_ADC_name)
                self.set_presamples(0, unique_ADC_name)
            for i in range(0,6):
                postsamples = 10**i
                if postsamples == 1:
                    postsamples = 2 # that is the minimum available value
                self.set_postsamples(postsamples, unique_ADC_name)
                self.results.write("Postsamples: " + str(postsamples) + "\n")
                best_result = 100000
                for i in range(5):
                    time_diff = self.measure_acquisition_time()
                    if time_diff < best_result:
                        best_result = time_diff
                        best_result_txt = str(best_result) + '\n'
                self.results.write("Best in 5: " + best_result_txt)
        for j in range(3, -1, -1):
            self.remove_channel(j)

    def test_add_channel(self):
        GUI_channel = 0
        ADC_channel = 0
        ADC_idx = ADC_addr + "_" + str(self.ADCs['ADC1'][0])
        ADC_name = "ADC" + "_" + ADC_idx + "._tcp.local."
        self.zmq_rpc.send_RPC('add_channel', GUI_channel, ADC_name,
                               ADC_channel, self.GUI_name)
        channels = self.zmq_rpc.send_RPC('get_GUI_channels', self.GUI_name)
        self.zmq_rpc.send_RPC('remove_channel', GUI_channel, self.GUI_name)
        channel = channels[GUI_channel]
        self.assertEqual(channel.ADC_channel_idx, ADC_channel)
        self.assertEqual(len(channels), 1)

    def test_remove_available_ADC(self):
        self.assertEqual("abc", "abc")
