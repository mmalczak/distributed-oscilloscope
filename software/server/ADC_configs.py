class Channel:

    def __init__(self, channel_range, termination, offset, saturation,
                 unique_ADC_name, ADC_channel_idx):
        self.unique_ADC_name = unique_ADC_name
        self.ADC_channel_idx = ADC_channel_idx
        self.range_conv = {35: 100, 69: 10, 17: 1}
        self.active = True  # TO BE REMOVED
        self.channel_range = self.range_conv[channel_range]
        self.termination = termination
        self.offset = offset
        self.saturation = saturation
        self.timestamp_and_data = None

    def set_channel_range(self, channel_range):
        self.channel_range = self.range_conv[channel_range]

    def set_termination(self, termination):
        self.termination = termination

    def set_offset(self, offset):
        self.offset = offset

    def set_saturation(self, saturation):
        self.saturation = saturation

    def update_channel_conf(self, channel_range, termination, offset,
                            saturation):
        self.channel_range = self.range_conv[channel_range]
        self.termination = termination
        self.offset = offset
        self.saturation = saturation


class Trigger:

    def __init__(self, enable, polarity, delay):
        self.enable = enable
        self.polarity = polarity
        self.delay = delay
        self.type = None

    def set_enable(self, enable):
        self.enable = enable

    def set_polarity(self, polarity):
        self.polarity = polarity

    def set_delay(self, delay):
        self.delay = delay

    def update_trigger_conf(self, enable, polarity, delay):
        self.enable = enable
        self.polarity = polarity
        self.delay = delay


class InternalTrigger(Trigger):

    def __init__(self, enable, polarity, delay, threshold,
                 unique_ADC_name, ADC_trigger_idx):
        super().__init__(enable, polarity, delay)
        self.unique_ADC_name = unique_ADC_name
        self.ADC_trigger_idx = ADC_trigger_idx
        self.threshold = threshold
        self.type = 'internal'

    def set_threshold(self, threshold):
        self.threshold = threshold

    def update_trigger_conf(self, enable, polarity, delay, threshold):
        self.enable = enable
        self.polarity = polarity
        self.delay = delay
        self.threshold = threshold


class ExternalTrigger(Trigger):

    def __init__(self, enable, polarity, delay, unique_ADC_name,
                 ADC_trigger_idx):
        super().__init__(enable, polarity, delay)
        self.type = 'external'
        self.unique_ADC_name = unique_ADC_name
        self.ADC_trigger_idx = ADC_trigger_idx


class AcqConf:

    def __init__(self, presamples, postsamples):
        self.presamples = presamples
        self.postsamples = postsamples

    def set_presamples(self, presamples):
        self.presamples = presamples

    def set_postsamples(self, postsamples):
        self.postsamples = postsamples

    def update_acq_conf(self, presamples, postsamples):
        self.set_presamples(presamples)
        self.set_postsamples(postsamples)
