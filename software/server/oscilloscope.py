from GUI import *
import logging
logger = logging.getLogger(__name__)


class Oscilloscope():

    def __init__(self):
        self.__GUIs = dict()
        self.__available_ADCs = {}

    def register_ADC(self, unique_ADC_name, number_of_channels, conf,
                          ip, port):
        self.__available_ADCs[unique_ADC_name] = ADC(unique_ADC_name, conf, 
                                                   ip, port)
        for name_GUI, GUI in self.__GUIs.items():
            data = {'function_name': 'register_ADC',
                    'args': [unique_ADC_name, number_of_channels]}
            GUI.GUI_publisher.send_message(data)
        logger.info("ADC {} registered".format(unique_ADC_name))


    def unregister_ADC(self, unique_ADC_name):
        """TODO: Why doesn't call GUI unregister_ADC"""
        for name_GUI, GUI in self.__GUIs.items():
            data = {'function_name': 'unregister_ADC',
                    'args': [unique_ADC_name]}
            GUI.GUI_publisher.send_message(data)
        """wait until there are no more users"""
        del self.__available_ADCs[unique_ADC_name]
        channels_to_delete = []
        for GUI_name, GUI in self.__GUIs.items():
            for channel_idx, channel in GUI.channels.items():
                if channel.unique_ADC_name == unique_ADC_name:
                    channels_to_delete.append(channel_idx)
            for channel_idx in channels_to_delete:
                GUI.remove_channel(channel_idx)
        logger.info("ADC {} unregistered".format(unique_ADC_name))


    def register_GUI(self, GUI_name, GUI_addr, GUI_port):
        GUI_ = GUI(self, GUI_name, GUI_addr, GUI_port)
        self.__GUIs.update({GUI_name: GUI_})
        for unique_ADC_name, ADC in self.__available_ADCs.items():
            data = {'function_name': 'register_ADC',
                    'args': [unique_ADC_name, ADC.number_of_channels]}
            GUI_.GUI_publisher.send_message(data)
        logger.info("GUI {} registered".format(GUI_name))

    def unregister_GUI(self, GUI_name):
        del self.__GUIs[GUI_name]
        logger.info("GUI {} unregistered".format(GUI_name))

    def update_data(self, timestamp, pre_post, data, unique_ADC_name):
        if(data ==  0):
            self.stop_acquisition_if_GUI_contains_ADC(unique_ADC_name)
            return
        """TODO add logging, do sth"""
        ADC = self.get_ADC(unique_ADC_name)
        ADC.update_data(timestamp, pre_post, data, unique_ADC_name)
        for GUI_name, GUI in self.__GUIs.items():
            GUI.check_if_ready_and_send_data()

    def stop_acquisition_if_GUI_contains_ADC(self, unique_ADC_name):
        for GUI_name, GUI in self.__GUIs.items():
            if GUI.contains_ADC(unique_ADC_name):
                GUI.stop_acquisition_ADCs_used()

    def get_ADC(self, unique_ADC_name):
        return self.__available_ADCs[unique_ADC_name]

    def get_GUI(self, GUI_name):
        return self.__GUIs[GUI_name]
