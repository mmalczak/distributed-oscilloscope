def tic_difference(timestamp_1, timestamp_2):
    [sec_1, tic_1] = timestamp_1
    [sec_2, tic_2] = timestamp_2

    sec_diff = sec_1 - sec_2
    tic_diff = tic_1 - tic_2
    tic_diff += sec_diff*125e6

    return tic_diff

def check_if_equal(timestamp_1, timestamp_2, available_offset_tics):
    tic_diff = tic_difference(timestamp_1, timestamp_2)
    if(tic_diff <= available_offset_tics
       and tic_diff >= -available_offset_tics):
        return True
    return False

def check_if_greater(timestamp_1, timestamp_2):
    [sec_1, tic_1] = timestamp_1
    [sec_2, tic_2] = timestamp_2

    if (sec_1 > sec_2) or ((sec_1 == sec_2) and (tic_1 > tic_2)):
        return True
    else:
        return False
