def check_if_not_max(max_sec, max_tic, sec, tic, available_offset):
    max_tic = max_tic - available_offset
    if(max_tic >= 125e6):
        max_tic = max_tic - 125e6
        max_sec = max_sec+1
    if((sec < max_sec) or ((sec == max_sec) and (tic < max_tic))):
        return True
    return False


def tic_difference(max_sec, max_tic, sec, tic):
    sec_diff = max_sec-sec
    tic_diff = max_tic - tic
    tic_diff = tic_diff + sec_diff * 125e6
    return tic_diff


def check_if_equal(max_sec, max_tic, sec, tic, available_offset):
    tic_diff = tic_difference(max_sec, max_tic, sec, tic)
    if(tic_diff <= available_offset and tic_diff >= -available_offset):
        return True
    return False
