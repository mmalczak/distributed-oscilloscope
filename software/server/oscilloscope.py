from GUI import *
import logging
logger = logging.getLogger(__name__)


class Oscilloscope():

    def __init__(self):
        self.GUIs = dict()
        self.available_ADCs = {}

    def add_available_ADC(self, unique_ADC_name, number_of_channels, conf,
                          ip, port):
        self.available_ADCs[unique_ADC_name] = ADC(unique_ADC_name, conf, 
                                                   ip, port)
        for name_GUI, GUI in self.GUIs.items():
            data = {'function_name': 'add_available_ADC',
                    'args': [unique_ADC_name, number_of_channels]}
            GUI.GUI_publisher.send_message(data)
        logger.info("ADC {} registered".format(unique_ADC_name))


    def unregister_ADC(self, unique_ADC_name):
        """TODO: Why doesn't call GUI unregister_ADC"""
        for name_GUI, GUI in self.GUIs.items():
            data = {'function_name': 'unregister_ADC',
                    'args': [unique_ADC_name]}
            GUI.GUI_publisher.send_message(data)
        """wait until there are no more users"""
        del self.available_ADCs[unique_ADC_name]
        channels_to_delete = []
        for GUI_name, GUI in self.GUIs.items():
            for channel_idx, channel in GUI.channels.items():
                if channel.unique_ADC_name == unique_ADC_name:
                    channels_to_delete.append(channel_idx)
            for channel_idx in channels_to_delete:
                GUI.remove_channel(channel_idx)
        logger.info("ADC {} unregistered".format(unique_ADC_name))


    def register_GUI(self, GUI_name, GUI_addr, GUI_port):
        GUI_ = GUI(self.available_ADCs, GUI_name, GUI_addr, GUI_port)
        self.GUIs.update({GUI_name: GUI_})
        for unique_ADC_name, ADC in self.available_ADCs.items():
            data = {'function_name': 'add_available_ADC',
                    'args': [unique_ADC_name, ADC.number_of_channels]}
            GUI_.GUI_publisher.send_message(data)
        logger.info("GUI {} registered".format(GUI_name))

    def unregister_GUI(self, GUI_name):
        del self.GUIs[GUI_name]
        logger.info("GUI {} unregistered".format(GUI_name))

    def update_data(self, timestamp_and_data, unique_ADC_name):
        if(timestamp_and_data == [0, 0]):
            self.stop_acquisition_if_GUI_contains_ADC(unique_ADC_name)
            return
        self.available_ADCs[unique_ADC_name].\
            update_data(timestamp_and_data, unique_ADC_name)
        for GUI_name, GUI in self.GUIs.items():
            GUI.check_if_ready_and_send_data()

    def stop_acquisition_if_GUI_contains_ADC(self, unique_ADC_name):
        for GUI_name, GUI in self.GUIs.items():
            if GUI.contains_ADC(unique_ADC_name):
                GUI.stop_acquisition_ADCs_used()

    def retrieve_acquisition_if_GUI_contains_ADC(self, unique_ADC_name):
        for GUI_name, GUI in self.GUIs.items():
            if GUI.contains_ADC(unique_ADC_name):
                GUI.retrieve_acquisition_ADCs_used()


def validate_data(GUI):
    """check if data from all ADCs is properly aligned"""
    max_timestamp = [0, 0]
    all_the_same = False
    max_offset = 300
    while(all_the_same is False):
        for ADC_name, ADC in GUI.ADCs.items():
            try:
                timestamp = ADC.timestamp_and_data[0][0]
                print(ADC_name + str(timestamp))
            except Exception as e:
                return False
            if((timestamp[0] > max_timestamp[0]) or
               ((timestamp[0] == max_timestamp[0]) and
               (timestamp[1] > max_timestamp[1]))):
                max_timestamp = timestamp
                max_timestamp_sec = max_timestamp[0]
                max_timestamp_tic = max_timestamp[1]
        for ADC_name, ADC in GUI.ADCs.items():
            try:
                timestamp = ADC.timestamp_and_data[0][0]
                timestamp_sec = timestamp[0]
                timestamp_tic = timestamp[1]
            except Exception as e:
                return False
            if(check_if_not_max(max_timestamp_sec, max_timestamp_tic,
                                timestamp_sec, timestamp_tic, max_offset)):
                ADC.timestamp_and_data.pop(0)
        for ADC_name, ADC in GUI.ADCs.items():
            try:

                timestamp = ADC.timestamp_and_data[0][0]
                timestamp_sec = timestamp[0]
                timestamp_tic = timestamp[1]
            except Exception as e:
                return False
            if(not check_if_equal(max_timestamp_sec, max_timestamp_tic,
                                  timestamp_sec, timestamp_tic,
                                  max_offset)):
                all_the_same = False
                break
            else:
                """FIXME it was quick fix to include the information
                abot the offset between the triggers now this
                information is included in the data, as last sample"""
                """FIXME offset calculated in ticks, the correction
                applied in samples"""
                offset = tic_difference(max_timestamp_sec, max_timestamp_tic,
                                        timestamp_sec, timestamp_tic)
                for count in range(0, ADC.number_of_channels):
                    ADC.timestamp_and_data[0][1][count].append(offset)
                all_the_same = True
    return True
