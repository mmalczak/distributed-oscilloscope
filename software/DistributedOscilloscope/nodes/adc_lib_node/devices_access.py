from .WRTD import WRTD
from .ADC_100m14b4cha import ADC_100m14b4cha_extended_API
import zmq
import numpy as np
import logging
logger = logging.getLogger(__name__)


delay_u = 600
delay_samples = delay_u * 100
delay_tics = delay_samples * 125 // 100

NSHOT = 1
NCHAN = 4


class DevicesAccess():

    def __init__(self, pci_addr, trtl, unique_ADC_name):
        self.user_app_name = None
        self.__WRTD = WRTD(trtl)
        self.__ADC = ADC_100m14b4cha_extended_API(pci_addr)
        self.__WRTD_master = False
        self.__required_presamples = 0
        self.unique_ADC_name = unique_ADC_name
        for count in range(4):
            self.__ADC.set_internal_trigger_enable(0, count)
        self.__ADC.set_external_trigger_enable(0, 0)
        if(not self.__WRTD_master):
            self.__ADC.set_presamples(delay_samples)
        self.__ADC.set_number_of_shots(NSHOT)
        buf_size = self.__get_required_buffer_size()
        self.__ADC.set_buffer(buf_size)
        self.__channels = None
        self.selector = None

        """Used to retrieve the acquisition when modyfing the parameters"""
        self.__acquisition_configured = False
        self.run = False

    def set_user_app_name(self, user_app_name):
        """
        Sets the name of the User Application -- this name is used to
        distinguish WRTD rules.

        :param user_app_name: Name of the User Application
        """
        self.user_app_name = user_app_name
        if user_app_name:
            self.distribute_triggers_name = 'dt_' + user_app_name[0:8]
            self.receive_triggers_name = 'rt_' + user_app_name[0:8]
        self.set_WRTD_master(False)

    def __get_required_buffer_size(self):
        acq_conf = self.get_current_adc_conf_acq()
        presamples = acq_conf['presamples']
        postsamples = acq_conf['postsamples']
        return presamples + postsamples

    def __get_pre_post_samples(self):
        acq_conf = self.get_current_adc_conf_acq()
        presamples = acq_conf['presamples']
        postsamples = acq_conf['postsamples']
        return {'presamples': presamples, 'postsamples': postsamples}

    def set_WRTD_master(self, WRTD_master, trigger_type=None,
                           ADC_trigger_idx=None):
        """
        Defines if particular device works as master or slave. The master
        distributed the triggers, the slave receives the triggers.

        Master mode:

            * enables the selected trigger
            * adds WRTD rule to distribute timestamps
            * modifies the number of presmaples and postsamples to align data\
                    from various ADCs

        Slave mode:

            * disables all triggers
            * adds WRTD rule to receive timestamps
            * modifies the number of presmaples and postsamples to align data\
                    from various ADCs

        :param WRTD_master: if True device works as master, if False device\
                works as slave
        :param trigger_type: in master mode defines the type of the trigger to\
                enable
        :param ADC_trigger_idx: in master mode dfines the index of the trigger\
                to enable
        """
        for count in range(4):
            self.__ADC.set_internal_trigger_enable(0, count)
        self.__ADC.set_external_trigger_enable(0, 0)
        if WRTD_master:
            trig_enable_name = "set_{}_trigger_enable".format(trigger_type)
            trig_enable = getattr(self.__ADC, trig_enable_name)
            trig_enable(1, ADC_trigger_idx)

        self.__WRTD_master = WRTD_master
        if(WRTD_master):
            self.__ADC.set_presamples(self.__required_presamples)
            buf_size = self.__get_required_buffer_size()
            self.__ADC.set_buffer(buf_size)
            self.__WRTD.disable_all_rules()
            self.__WRTD.remove_all_rules()
            self.__WRTD.add_rule_mult_src(self.distribute_triggers_name, 6)
            self.__WRTD.set_rule_mult_src(self.distribute_triggers_name, 0,
                                          'LC-I', 'LAN1', 6)
            self.__WRTD.enable_rule_mult_src(self.distribute_triggers_name, 6)
        else:
            self.__ADC.set_presamples(self.__required_presamples +
                                      delay_samples)
            buf_size = self.__get_required_buffer_size()
            self.__ADC.set_buffer(buf_size)
            self.__WRTD.disable_all_rules()
            self.__WRTD.remove_all_rules()
            try:
                self.__WRTD.add_rule(self.receive_triggers_name)
            except Exception as e:
                print(e)
            self.__WRTD.set_rule(self.receive_triggers_name, 600e6, 'LAN1',
                                 'LC-O1')
            self.__WRTD.enable_rule(self.receive_triggers_name)

    def configure_adc_parameter(self, function_name, *args):
        """
        Generic function to modify the ADC parameters.

        :param function_name: the name of the function, which modifies\
                particular ADC parameter
        :param *args: arguments passed to the function -- the type of\
                arguments depends on the selected function
        """
        if(function_name == 'set_presamples' and self.__WRTD_master is False):
            self.__required_presamples = args[0]
            args = list(args)
            args[0] += delay_samples
            args = tuple(args)
        getattr(self.__ADC, function_name)(*args)
        if(function_name == ('set_presamples' or 'set_postsamples')):
            buf_size = self.__get_required_buffer_size()
            self.__ADC.set_buffer(buf_size)

        if self.__acquisition_configured:
            self.configure_acquisition(self.__channels)

    def get_current_adc_conf(self):
        """
        Retrieves the configuration of the ADC.

        :return: Dictionary with ADC configurations
        """
        conf = self.__ADC.current_config()
        conf['is_WRTD_master'] = self.__WRTD_master
        if(not self.__WRTD_master):
            conf['acq_conf']['presamples'] -= delay_samples
        return conf

    def get_current_adc_conf_acq(self):
        acq_conf = self.__ADC.current_config_acq()
        if(not self.__WRTD_master):
            acq_conf['presamples'] -= delay_samples
        return acq_conf

    def configure_acquisition(self, channels):
        """
        Configures single acquisition.

        :param channels: list of channels indexes from which the data should\
                be retrieved
        """

        self.__channels = channels
        self.__ADC.stop_acquisition()
        self.__ADC.start_acquisition()
        self.selector.register(self, zmq.POLLIN)
        logger.debug("The ADC device registered in the poller selector")

        self.__acquisition_configured = True


    def run_acquisition(self, run, channels=None):
        """
        Starts or stops continuous acquisition.

        :param run: if True start acquisition, if False stop acquisition
        :param channels: list of channels indexes from which the data should\
                be retrieved
        """
        #channels could be None only if run is False
        self.run = run
        if run:
            self.configure_acquisition(channels)

    def stop_acquisition(self):
        self.__ADC.acq_stop(0)
        try:
            self.selector.unregister(self)
            logger.debug("The ADC device unregistered from the poller selector")
        except KeyError:
            logger.warning("The ADC device not available to unregister from "
                           "the poller selector stop acquisition")

        self.__acquisition_configured = False

    def fileno(self):
        return self.__ADC.fileno()

    def retrieve_ADC_data(self):
        try:
            self.__ADC.fill_buf()
        except Exception as e:
            logger.warning("Error when filling buffer: {}".format(e))
            return [0, 0, 0]

        try:
            data = np.ctypeslib.as_array(self.__ADC.buf_ptr.contents.data,
                                         (self.__get_required_buffer_size(), 4))
        except Exception as e:
            print(e)
            return([0, 0, 0])

        data = np.transpose(data)
        data_dict = {}
        for channel in self.__channels:
            data_dict[str(channel)] = data[channel]

        if(not self.__WRTD_master):
            timestamp = self.__ADC.get_timestamp(self.__ADC.buf_ptr, delay_tics)
        else:
            timestamp = self.__ADC.get_timestamp(self.__ADC.buf_ptr, 0)
        self.__ADC.acq_stop(0)
        pre_post_samples_dict = self.__get_pre_post_samples()

        self.__acquisition_configured = False

        if self.run:
            self.configure_acquisition(self.__channels)

        return [timestamp, pre_post_samples_dict, data_dict]
