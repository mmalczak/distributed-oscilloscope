class Channel:

    def __init__(self, ADC, ADC_channel_idx):
        self.ADC = ADC
        self.ADC_channel_idx = ADC_channel_idx
        self.range_conv = {35: 100, 69: 10, 17: 1}
        self.active = True  # TO BE REMOVED
        self.range = None
        self.termination = None
        self.offset = None
        self.timestamp_pre_post_data = None

    def update_channel_conf(self, range, termination, offset):
        self.range = self.range_conv[range]
        self.termination = termination
        self.offset = offset


class Trigger:

    def __init__(self):
        self.enable = None
        self.polarity = None
        self.delay = None
        self.type = None

    def update_trigger_conf(self, enable, polarity, delay):
        self.enable = enable
        self.polarity = polarity
        self.delay = delay


class InternalTrigger(Trigger):

    def __init__(self, ADC, ADC_trigger_idx):
        super().__init__()
        self.ADC = ADC
        self.ADC_trigger_idx = ADC_trigger_idx
        self.threshold = None
        self.type = 'internal'

    def update_trigger_conf(self, enable, polarity, delay, threshold):
        self.enable = enable
        self.polarity = polarity
        self.delay = delay
        self.threshold = threshold


class ExternalTrigger(Trigger):

    def __init__(self, ADC, ADC_trigger_idx):
        super().__init__()
        self.type = 'external'
        self.ADC = ADC
        self.ADC_trigger_idx = ADC_trigger_idx


class AcqConf:

    def __init__(self):
        self.presamples = None
        self.postsamples = None

    def update_acq_conf(self, presamples, postsamples):
        self.presamples = presamples
        self.postsamples = postsamples
