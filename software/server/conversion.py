""" TODO check for an overflow """


def threshold_raw_to_mV(threshold, ADC, idx):
    channel = ADC.get_channel(idx)
    channel_range = channel.channel_range
    threshold_mult = {10: 1, 1: 1/10, 100: 1/100}
    threshold = threshold * threshold_mult[channel_range]
    return int(threshold*10000/2**16)


def threshold_mV_to_raw(threshold, ADC, idx):
    channel = ADC.get_channel(idx)
    channel_range = channel.channel_range
    threshold_mult = {10: 1, 1: 10, 100: 100}
    threshold = threshold * threshold_mult[channel_range]
    return int(threshold*2**16/10000)
