from stock_price_patterns import WHITE_CS, BLACK_CS


def is_bearish_stick_sandwich(htd):
    if len(htd) < 3:
        raise Exception("Sorry, stick sandwich model requires minimum 3 bars")
    max_oc = htd['max_OC'].to_list()
    min_oc = htd['min_OC'].to_list()
    color = htd['color'].to_list()
    _1st_condition = bearish_stick_sandwich_cond_1(max_oc)
    _2nd_condition = bearish_stick_sandwich_cond_2(min_oc)
    _3rd_condition = bearish_stick_sandwich_cond_3(color)
    if _1st_condition and _2nd_condition and _3rd_condition:
        return True
    return False
# --------------


def is_bullish_stick_sandwich(htd):
    if len(htd) < 3:
        raise Exception("Sorry, stick sandwich model requires minimum 3 bars")
    max_oc = htd['max_OC'].to_list()
    min_oc = htd['min_OC'].to_list()
    color = htd['color'].to_list()
    _1st_condition = bullish_stick_sandwich_cond_1(max_oc)
    _2nd_condition = bullish_stick_sandwich_cond_2(min_oc)
    _3rd_condition = bullish_stick_sandwich_cond_3(color)
    if _1st_condition and _2nd_condition and _3rd_condition:
        return True
    return False


# -----------------------------------------------Conditions------------------------------------------------------------
def bullish_stick_sandwich_cond_1(max_oc):
    """
        Idea:
            1. prev_2_max_oc > prev_1_max_oc
            2. current_max_oc > prev_1_max_oc
            3. abs(prev_2_max_oc - current_max_oc) < 0.2
    :param max_oc:
    :return:
    """
    if max_oc[-3] > max_oc[-2] and max_oc[-1] > max_oc[-2] and abs(max_oc[-3] - max_oc[-1]) < 0.2:
        return True
    else:
        return False


def bullish_stick_sandwich_cond_2(min_oc):
    """
        Idea:
            1. prev_2_min_oc < prev_1_min_oc
            2. current_min_oc < prev_1_min_oc
            3. abs(prev_2_min_oc - current_min_oc) < 0.2
    :param min_oc:
    :return:
    """
    if min_oc[-3] < min_oc[-2] and min_oc[-1] < min_oc[-2] and abs(min_oc[-3] - min_oc[-1]) < 0.2:
        return True
    else:
        return False


def bullish_stick_sandwich_cond_3(color):
    """
    Idea:
        1. current_color = black/red
        2. prev_1_color = white/green
        3. prev_2_color = black/red
    :param color:
    :return:
    """
    if color[-1] == BLACK_CS and color[-2] == WHITE_CS and color[-3] == BLACK_CS:
        return True
    else:
        return False


# --------------
def bearish_stick_sandwich_cond_1(max_oc):
    """
        Idea:
            1. prev_2_max_oc > prev_1_max_oc
            2. current_max_oc > prev_1_max_oc
            3. abs(prev_2_max_oc - current_max_oc) < 0.2
    :param max_oc:
    :return:
    """
    if max_oc[-3] > max_oc[-2] and max_oc[-1] > max_oc[-2] and abs(max_oc[-3] - max_oc[-1]) < 0.2:
        return True
    else:
        return False


def bearish_stick_sandwich_cond_2(min_oc):
    """
        Idea:
            1. prev_2_min_oc < prev_1_min_oc
            2. current_min_oc < prev_1_min_oc
            3. abs(prev_2_min_oc - current_min_oc) < 0.2
    :param min_oc:
    :return:
    """
    if min_oc[-3] < min_oc[-2] and min_oc[-1] < min_oc[-2] and abs(min_oc[-3] - min_oc[-1]) < 0.2:
        return True
    else:
        return False


def bearish_stick_sandwich_cond_3(color):
    """
    Idea:
        1. current_color = white/green
        2. prev_1_color = black/red
        3. prev_2_color = white/green
    :param color:
    :return:
    """
    if color[-1] == WHITE_CS and color[-2] == BLACK_CS and color[-3] == WHITE_CS:
        return True
    else:
        return False
