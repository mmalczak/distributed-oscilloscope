def threshold_raw_to_mV(threshold, unique_ADC_name, idx,
                        available_ADCs):
    channel_range = available_ADCs[unique_ADC_name].channels[idx].\
                                                        channel_range
    threshold_mult = {10: 1, 1: 1/10, 100: 1/100}
    threshold = threshold * threshold_mult[channel_range]
    return int(threshold*10000/2**16)


def threshold_mV_to_raw(threshold, unique_ADC_name, idx,
                        available_ADCs):
    channel_range = available_ADCs[unique_ADC_name].channels[idx].\
                                                        channel_range
    threshold_mult = {10: 1, 1: 10, 100: 100}
    threshold = threshold * threshold_mult[channel_range]
    return int(threshold*2**16/10000)
