from .user_app import UserApplication
from .ADC import ADC
import logging
logger = logging.getLogger(__name__)


class ConnectionManager():
    """
    Manages connections with all nodes. Provides access to the nodes for other
    classes
    """

    def __init__(self):
        self.__user_apps = dict()
        self.__available_ADCs = {}

    def register_ADC(self, unique_ADC_name, ip, port):
        ADC_ = ADC(unique_ADC_name, ip, port, self)
        self.__available_ADCs[unique_ADC_name] = ADC_
        for name_user_app, user_app in self.__user_apps.items():
            user_app.register_ADC(unique_ADC_name, ADC_.number_of_channels)
        logger.info("ADC {} registered".format(unique_ADC_name))

    def unregister_ADC(self, unique_ADC_name):
        if unique_ADC_name in self.__available_ADCs:
            del self.__available_ADCs[unique_ADC_name]
            for user_app_name, user_app in self.__user_apps.items():
                user_app.unregister_ADC(unique_ADC_name)
            logger.info("ADC {} unregistered".format(unique_ADC_name))
        logger.warning("ADC {} was not available to unregister".format(
                                                            unique_ADC_name))

    def set_ADC_available(self, unique_ADC_name, owner_user_app):
        for user_app_name, user_app_ in self.__user_apps.items():
            if not user_app_name is owner_user_app:
                user_app_.set_ADC_available(unique_ADC_name)

    def set_ADC_unavailable(self, unique_ADC_name, owner_user_app):
        for user_app_name, user_app_ in self.__user_apps.items():
            if not user_app_name is owner_user_app:
                user_app_.set_ADC_unavailable(unique_ADC_name)

    def register_user_app(self, user_app_name, user_app_addr, user_app_port):
        user_app_ = UserApplication(user_app_name, user_app_addr,
                                    user_app_port, self)
        self.__user_apps.update({user_app_name: user_app_})
        for unique_ADC_name, ADC in self.__available_ADCs.items():
            user_app_.register_ADC(unique_ADC_name, ADC.number_of_channels)
            if not ADC.is_available:
                user_app_.set_ADC_unavailable(unique_ADC_name)
        logger.info("User application {} registered".format(user_app_name))

    def unregister_user_app(self, user_app_name):
        self.__user_apps[user_app_name].remove_all()
        del self.__user_apps[user_app_name]
        logger.info("User application {} unregistered".format(user_app_name))

    def stop_acquisition_if_user_app_contains_ADC(self, unique_ADC_name):
        for user_app_name, user_app in self.__user_apps.items():
            if user_app.contains_ADC(unique_ADC_name):
                user_app.stop_acquisition_ADCs_used()

    def get_ADC(self, unique_ADC_name):
        return self.__available_ADCs[unique_ADC_name]

    def get_user_app(self, user_app_name):
        return self.__user_apps[user_app_name]

    def set_server_address(self, unique_ADC_name, addr):
        ADC = self.get_ADC(unique_ADC_name)
        ADC.set_server_address(addr)
