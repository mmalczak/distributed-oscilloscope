from GUI import GUI
from ADC import ADC
import logging
logger = logging.getLogger(__name__)


class ConnectionManager():

    def __init__(self):
        self.__GUIs = dict()
        self.__available_ADCs = {}

    def register_ADC(self, unique_ADC_name, ip, port):
        ADC_ = ADC(unique_ADC_name, ip, port, self)
        self.__available_ADCs[unique_ADC_name] = ADC_
        for name_GUI, GUI in self.__GUIs.items():
            GUI.register_ADC(unique_ADC_name, ADC_.number_of_channels)
        logger.info("ADC {} registered".format(unique_ADC_name))

    def unregister_ADC(self, unique_ADC_name):
        if unique_ADC_name in self.__available_ADCs:
            del self.__available_ADCs[unique_ADC_name]
            for GUI_name, GUI in self.__GUIs.items():
                GUI.unregister_ADC(unique_ADC_name)
            logger.info("ADC {} unregistered".format(unique_ADC_name))
        logger.warning("ADC {} was not available to unregister".format(
                                                            unique_ADC_name))

    def register_GUI(self, GUI_name, GUI_addr, GUI_port):
        GUI_ = GUI(GUI_name, GUI_addr, GUI_port)
        self.__GUIs.update({GUI_name: GUI_})
        for unique_ADC_name, ADC in self.__available_ADCs.items():
            GUI_.register_ADC(unique_ADC_name, ADC.number_of_channels)
        logger.info("GUI {} registered".format(GUI_name))

    def unregister_GUI(self, GUI_name):
        del self.__GUIs[GUI_name]
        logger.info("GUI {} unregistered".format(GUI_name))

    def check_timing(self):
        for GUI_name, GUI in self.__GUIs.items():
            GUI.check_timing()

    def __stop_acquisition_if_GUI_contains_ADC(self, unique_ADC_name):
        for GUI_name, GUI in self.__GUIs.items():
            if GUI.contains_ADC(unique_ADC_name):
                GUI.stop_acquisition_ADCs_used()

    def get_ADC(self, unique_ADC_name):
        return self.__available_ADCs[unique_ADC_name]

    def get_GUI(self, GUI_name):
        return self.__GUIs[GUI_name]

    def set_server_address(self, unique_ADC_name, addr):
        ADC = self.get_ADC(unique_ADC_name)
        ADC.set_server_address(addr)
