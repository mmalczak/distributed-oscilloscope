def threshold_raw_to_mV(threshold, unique_ADC_name, idx, available_ADCs):
    channel_range = available_ADCs[unique_ADC_name].channels[idx].channel_range
    if(channel_range == 1):
        threshold = threshold/10
    elif(channel_range == 100):
        threshold = threshold/100
    return int(threshold*10000/2**16)

def threshold_mV_to_raw(threshold, unique_ADC_name, idx, available_ADCs):
    channel_range = available_ADCs[unique_ADC_name].channels[idx].channel_range
    if(channel_range == 1):
        threshold = threshold*10
    elif(channel_range == 100):
        threshold = threshold*100
    return int(threshold*2**16/10000)


