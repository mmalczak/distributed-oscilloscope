import unittest
import time
import subprocess
from paramiko_connection import start_adc
import xmlrpc.client
import sys
from server_expose_test import ThreadServerExposeTest
import os
from multiprocessing import Queue
from timeit import default_timer as timer
from test_conf import server_addr
from test_conf import update_data_type
sys.path.append('../../')
from general.zmq_rpc import ZMQ_RPC
from general.zmq_rpc import RPC_Error
from general.addresses import server_expose_to_user_port
import timeout_decorator
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../../server')
from server import ADC_configs
"""TODO is this the rigth thing to do???"""

server_addr = '128.141.79.50'
ADC_addr = '128.141.162.185'


class OscilloscopeMethods(unittest.TestCase):

    server_handler = None
    server_expose = None
    ADCs = {'ADC1': [8000, 1], 'ADC2': [8001, 2]}
    delay = 0.4
    return_queue = None
    GUI_name = None

    def setUp(self):
        if update_data_type == 'time_measurements' or\
           update_data_type == 'frequency_measurements' or\
           update_data_type == 'precision':
            self.results = open("results.txt", "a")
        self.start_server()
        self.create_GUI_interface()
        self.zmq_rpc = ZMQ_RPC(server_addr, server_expose_to_user_port)
        self.connect_to_server()
        self.add_ADC_FEC('ADC1')
        self.add_ADC_FEC('ADC2')
        time.sleep(self.delay)
        self.clean_queue()

    def tearDown(self):
        if update_data_type == 'time_measurements' or\
           update_data_type == 'frequency_measurements' or\
           update_data_type == 'precision':
            self.results.close()
        self.remove_ADC_FEC('ADC1')
        self.remove_ADC_FEC('ADC2')
        time.sleep(self.delay)
        self.stop_GUI_interface()
        self.stop_server()

    def connect_to_server(self):
        # addr = os.popen("ifconfig| grep inet").read().split()[1]
        addr = '128.141.79.50'
        port = 8001
        GUI_idx = addr + "_" + str(port)
        GUI_name = "GUI" + "_" + GUI_idx + "._http._tcp.local."
        self.GUI_name = GUI_name
        self.zmq_rpc.send_RPC('register_GUI', GUI_name, addr, port)

    def clean_queue(self):
        while not self.return_queue.empty():
            self.return_queue.get()

    def add_ADC_FEC(self, name):
        ADC = self.ADCs[name]
        start_adc(ADC[0], ADC[1])

    def remove_ADC_FEC(self, name):
        ADC = self.ADCs[name]
        zmq_rpc = ZMQ_RPC('spechost', ADC[0])
        zmq_rpc.set_timeout(10)
        """the timeout is small because the RPC call will never return, so
        there is no point waiting"""
        try:
            zmq_rpc.send_RPC('exit')
        except Exception as e:
            if type(e) is RPC_Error:
                pass
            else:
                print(e)
        """There will be an error because RPC can never return because
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

    @timeout_decorator.timeout(5)
    def test_register_unregister_ADC(self):
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

    @timeout_decorator.timeout(5)
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

    def measure_acquisition_time(self):
        self.zmq_rpc.send_RPC('single_acquisition', self.GUI_name)
        time_start = timer()
        time_end = self.return_queue.get()
        time_diff = time_end - time_start
        return time_diff

    def measure_acquisition_freq(self):
        self.zmq_rpc.send_RPC('run_acquisition', True, self.GUI_name)

        [initial_number, initial_time] = self.return_queue.get()

        while True:
            [number, time] = self.return_queue.get()
            time_diff = time - initial_time
            if time_diff > 0.5:
                number_diff = number - initial_number
                number_per_sec = number_diff / time_diff
                self.zmq_rpc.send_RPC('run_acquisition', False, self.GUI_name)
                return number_per_sec

    @unittest.skipUnless(update_data_type == 'frequency_measurements',
                         "Only for frequency measurements")
    def test_acquisition_frequency(self):
        self.clean_queue()

        number_of_acq = 5
        self.results.write("Internal trigger on channel 3\n"
                           "Sampled signal: 100kHz sine wave Channel 3(0-3)\n"
                           "number of presamples = 0\n"
                           "number of acquisitions = {}\n\n".format(
                                                            number_of_acq))

        ADC_idx = ADC_addr + "_" + str(self.ADCs['ADC1'][0])
        unique_ADC_name = "ADC" + "_" + ADC_idx + "._http._tcp.local."

        for j in range(3, -1, -1):
            self.results.write("Number of channels: " + str(4-j) + "\n")
            self.add_channel(j, unique_ADC_name)
            if j == 3:
                ADC_trigger_idx = 3
                send_RPC = self.zmq_rpc.send_RPC
                send_RPC('add_trigger', 'internal', unique_ADC_name,
                         ADC_trigger_idx, self.GUI_name)
                send_RPC('set_ADC_parameter', 'internal_trigger_enable', 1,
                         unique_ADC_name, ADC_trigger_idx)
            for i in range(0, 6):
                postsamples = 10**i
                if postsamples == 1:
                    postsamples = 2  # that is the minimum available value
                self.zmq_rpc.send_RPC('set_pre_post_samples', 0, postsamples,
                                      self.GUI_name)

                best_result = 0
                sum = 0
                results = []

                for i in range(number_of_acq):
                    print("measure acq freq, acq no: {}".format(i))
                    acq_freq = self.measure_acquisition_freq()
                    results.append(acq_freq)
                    sum = sum + acq_freq
                    if acq_freq > best_result:
                        best_result = acq_freq

                medium = sum / number_of_acq
                var = np.var(results, ddof=1)
                self.results.write("Postsamples: {:<7} ,".format(postsamples) +
                                   "Best: {:<1.15f}, ".format(best_result) +
                                   "medium: {:<1.15f}, ".format(medium) +
                                   "variance: {:<1.15f}, \n".format(var)
                                   )
        for j in range(3, -1, -1):
            self.remove_channel(j)

    @unittest.skipUnless(update_data_type == 'time_measurements',
                         "Only for time measurements")
    def test_acquisition_time(self):
        self.clean_queue()

        number_of_acq = 5
        self.results.write("Internal trigger on channel 3\n"
                           "Sampled signal: 100kHz sine wave Channel 3(0-3)\n"
                           "number of presamples = 0\n"
                           "number of acquisitions = {}\n\n".format(
                                                            number_of_acq))

        ADC_idx = ADC_addr + "_" + str(self.ADCs['ADC1'][0])
        unique_ADC_name = "ADC" + "_" + ADC_idx + "._http._tcp.local."

        for j in range(3, -1, -1):
            self.results.write("Number of channels: " + str(4-j) + "\n")
            self.add_channel(j, unique_ADC_name)
            if j == 3:
                ADC_trigger_idx = 3
                send_RPC = self.zmq_rpc.send_RPC
                send_RPC('add_trigger', 'internal', unique_ADC_name,
                         ADC_trigger_idx, self.GUI_name)
                send_RPC('set_ADC_parameter', 'internal_trigger_enable', 1,
                         unique_ADC_name, ADC_trigger_idx)
            for i in range(0, 6):
                postsamples = 10**i
                if postsamples == 1:
                    postsamples = 2  # that is the minimum available value
                self.zmq_rpc.send_RPC('set_pre_post_samples', 0, postsamples,
                                      self.GUI_name)

                best_result = 100000
                sum = 0
                results = []

                for i in range(number_of_acq):
                    time_diff = self.measure_acquisition_time()
                    results.append(time_diff)
                    sum = sum + time_diff
                    if time_diff < best_result:
                        best_result = time_diff

                medium = sum / number_of_acq
                var = np.var(results, ddof=1)
                self.results.write("Postsamples: {:<7} ,".format(postsamples) +
                        "Best: {:<1.15f}, ".format(best_result) +
                        "medium: {:<1.15f}, ".format(medium) +
                        "variance: {:<1.15f}, \n".format(var)
                                                             )
        for j in range(3, -1, -1):
            self.remove_channel(j)

    @unittest.skipUnless(update_data_type == 'plot', "Only for plotting")
    def test_acquisition(self):
        self.clean_queue()

        ADC_idx = ADC_addr + "_" + str(self.ADCs['ADC1'][0])
        unique_ADC_name_1 = "ADC" + "_" + ADC_idx + "._http._tcp.local."

        oscilloscope_channel_idx = 0
        ADC_channel = 3
        self.zmq_rpc.send_RPC('add_channel', oscilloscope_channel_idx,
                          unique_ADC_name_1, ADC_channel, self.GUI_name)


        ADC_idx = ADC_addr + "_" + str(self.ADCs['ADC2'][0])
        unique_ADC_name_2 = "ADC" + "_" + ADC_idx + "._http._tcp.local."

        oscilloscope_channel_idx = 1
        ADC_channel = 3
        self.zmq_rpc.send_RPC('add_channel', oscilloscope_channel_idx,
                          unique_ADC_name_2, ADC_channel, self.GUI_name)


        ADC_trigger_idx = 3
        self.zmq_rpc.send_RPC('add_trigger', 'internal', unique_ADC_name_1,
                              ADC_trigger_idx, self.GUI_name)
        self.zmq_rpc.send_RPC('set_ADC_parameter', 'internal_trigger_enable',
                              1, unique_ADC_name_1, ADC_trigger_idx)

        self.zmq_rpc.send_RPC('set_presamples', 0, self.GUI_name)
        self.zmq_rpc.send_RPC('set_postsamples', 1000, self.GUI_name)

        self.zmq_rpc.send_RPC('single_acquisition', self.GUI_name)
        self.return_queue.get()
        time.sleep(1)

    @timeout_decorator.timeout(5)
    def test_add_channel(self):
        GUI_channel = 0
        ADC_channel = 0
        ADC_idx = ADC_addr + "_" + str(self.ADCs['ADC1'][0])
        ADC_name = "ADC" + "_" + ADC_idx + "._http._tcp.local."
        self.zmq_rpc.send_RPC('add_channel', GUI_channel, ADC_name,
                              ADC_channel, self.GUI_name)
        channels = self.zmq_rpc.send_RPC('get_GUI_channels', self.GUI_name)
        self.zmq_rpc.send_RPC('remove_channel', GUI_channel, self.GUI_name)
        channel = channels[GUI_channel]
        self.assertEqual(channel['ADC_channel_idx'], ADC_channel)
        self.assertEqual(len(channels), 1)

    @timeout_decorator.timeout(5)
    def test_unregister_ADC(self):
        self.assertEqual("abc", "abc")

    def channel_zero_cross(self, channel_samples):
        chan = channel_samples  # to make it shorter
        """Samples are counted from 0 to (pre+post-1) """
        pos_sam = 0  # first positive sample
        for i in range(len(chan)):
            if chan[i] > 0:
                pos_sam = i
                break
        #self.results.write("Positive sample idx: {} \n".format(pos_sam))

        x = chan[pos_sam] / (chan[pos_sam] - chan[pos_sam - 1]) * 10
        """Distance from zero crossing to the first positive sample in ns"""
        #self.results.write("x: {} \n".format(x))

        zc = pos_sam * 10 - x
        """Zero crossing in ns form the beginning of the array"""
        #self.results.write("zc: {} \n".format(zc))
        return zc

    def measure_zero_cross_distance(self):
        self.zmq_rpc.send_RPC('single_acquisition', self.GUI_name)
        try:
            data, offsets = self.return_queue.get(timeout=0.1 )
        except:
            return None
        chan_1 = data[0]
        chan_2 = data[1]
        #self.results.write(str(chan_1) + '\n')
        #self.results.write(str(chan_2) + '\n')

        zc_1 = self.channel_zero_cross(chan_1)
        zc_2 = self.channel_zero_cross(chan_2)
        dist = zc_2 - zc_1 + offsets[1]*8
        #self.results.write("dist: {} \n".format(dist))
        return dist


    def measure_zero_cross_distances(self, number_of_acq):
        distances = []
        for i in range(number_of_acq):
            dist = self.measure_zero_cross_distance()
            if dist is not None:
                distances.append(dist)
        return distances

    def calculate_statistics(self, data):
        mean = np.mean(data)
        var = np.var(data, ddof=1)
        sigma = var**(1/2)
        return [mean, var, sigma]

    def save_histogram(self, data, name):
        mean, var, sigma = self.calculate_statistics(data)
        fig, ax = plt.subplots()
        ax.hist(data, bins=100)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        text = "Mean: {:<1.2f}\n".format(mean) +\
               "Sigma: {:<1.2f}\n".format(sigma)
        ax.text(0.80, 0.95, text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)
        plt.savefig('/home/milosz/Desktop/figures_precision/'+ name + '.svg',
                    format='svg')

    def save_data(self, data, name):
        mean, var, sigma = self.calculate_statistics(data)
        with open('/home/milosz/Desktop/figures_precision/' + name + '.txt', 'a') as fh:
            fh.write("Mean: {}\n".format(mean))
            fh.write("Var: {}\n".format(var))
            fh.write("Sigma: {}\n".format(sigma))
            fh.write("Data: {}\n".format(data))

#    @timeout_decorator.timeout(5)
    @unittest.skipUnless(update_data_type == 'precision',
                         "Only for precision measurements")
    def test_precision(self):
        self.clean_queue()

        number_of_acq = 200
        """Some data could not arrive so actual number of acquisitions could
        be smaller"""
        self.results.write("Internal trigger on channel 3\n"
                           "Sampled signal: 100kHz sine wave Channel 3(0-3)\n"
                           "number of presamples = 2\n"
                           "number of postsamples = 2\n"
                           "number of acquisitions = {}\n\n".format(
                                                            number_of_acq))

        ADC_idx = ADC_addr + "_" + str(self.ADCs['ADC1'][0])
        unique_ADC_name_1 = "ADC" + "_" + ADC_idx + "._http._tcp.local."

        ADC_idx = ADC_addr + "_" + str(self.ADCs['ADC2'][0])
        unique_ADC_name_2 = "ADC" + "_" + ADC_idx + "._http._tcp.local."


        ADC_channel = 3
        oscilloscope_channel = 0
        self.zmq_rpc.send_RPC('add_channel', oscilloscope_channel,
                              unique_ADC_name_1, ADC_channel, self.GUI_name)
        oscilloscope_channel = 1
        self.zmq_rpc.send_RPC('add_channel', oscilloscope_channel,
                              unique_ADC_name_2, ADC_channel, self.GUI_name)

        self.zmq_rpc.send_RPC('set_pre_post_samples', 50, 50, self.GUI_name)

        ADC_trigger_idx = 3

        self.zmq_rpc.send_RPC('set_ADC_parameter', 'channel_offset', -290000,
                              unique_ADC_name_1, ADC_trigger_idx)
        """Used for calibration"""

        self.zmq_rpc.send_RPC('add_trigger', 'internal', unique_ADC_name_1,
                              ADC_trigger_idx, self.GUI_name)
        name = 'WRTD_calibration'
        distances = self.measure_zero_cross_distances(number_of_acq)
        self.save_histogram(distances, name)
        self.save_data(distances, name)


#        self.zmq_rpc.send_RPC('add_trigger', 'internal', unique_ADC_name_2,
#                              ADC_trigger_idx, self.GUI_name)
#        name = 'WRTD_trig_rev'
#        distances = self.measure_zero_cross_distances(number_of_acq)
#        self.save_histogram(distances, name)
#        self.save_data(distances, name)

