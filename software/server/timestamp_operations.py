def check_if_not_max(max_sec, max_tic, sec, tic, available_offset):
    max_tic = max_tic - available_offset
    if(max_tic >= 125e6):
        max_tic = max_tic - 125e6
        max_sec = max_sec+1
    if((sec < max_sec) or ((sec == max_sec) and (tic < max_tic))):
        return True
    return False


def tic_difference(timestamp_1, timestamp_2):
    sec_1 = timestamp_1[0]
    sec_2 = timestamp_2[0]
    tic_1 = timestamp_1[1]
    tic_2 = timestamp_2[1]

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
    sec_1 = timestamp_1[0]
    sec_2 = timestamp_2[0]
    tic_1 = timestamp_1[1]
    tic_2 = timestamp_2[1]

    if (sec_1 > sec_2) or ((sec_1 == sec_2) and (tic_1 > tic_2)):
        return True
    else:
        return False
