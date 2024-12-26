from candlesticks import WHITE_CS, BLACK_CS


def is_falling_three(htd):
    if len(htd) < 4:
        raise Exception("Sorry, falling three methods model requires minimum 4 bars")
    color = htd['color'].to_list()
    _1st_condition = falling_three_cond_1(color)
    body = htd['body'].to_list()
    _2nd_condition = falling_three_cond_2(body)
    max_oc = htd['max_OC'].to_list()
    _3rd_condition = falling_three_cond_3(max_oc)
    min_oc = htd['min_OC'].to_list()
    _4th_condition = falling_three_cond_4(min_oc)
    if _1st_condition and _2nd_condition and _3rd_condition and _4th_condition:
        return True
    return False


def is_rising_three(htd):
    if len(htd) < 4:
        raise Exception("Sorry, rising three methods model requires minimum 4 bars")
    color = htd['color'].to_list()
    _1st_condition = rising_three_cond_1(color)
    body = htd['body'].to_list()
    _2nd_condition = rising_three_cond_2(body)
    max_oc = htd['max_OC'].to_list()
    _3rd_condition = rising_three_cond_3(max_oc)
    min_oc = htd['min_OC'].to_list()
    _4th_condition = rising_three_cond_4(min_oc)
    if _1st_condition and _2nd_condition and _3rd_condition and _4th_condition:
        return True
    return False
# -----------------------------------------------Conditions------------------------------------------------------------


def falling_three_cond_1(color):
    """
    Idea:
        1. current candlestick is black/red
    :param color:
    :return:
    """
    if color[-1] == BLACK_CS:
        return True
    else:
        return False


def falling_three_cond_2(body):
    """
    Idea:
        1. current_body > 3 * prev_3_body
        2. current_body > 3 * prev_2_body
        3. current_body > 3 * prev_1_body
        (no require relationship between prev_1_body & prev_2_body & prev_3_body)
    :param body:
    :return:
    """
    if body[-1] > 3 * body[-4] and body[-1] > 3 * body[-3] and body[-1] > 3 * body[-2]:
        return True
    else:
        return False


def falling_three_cond_3(max_oc):
    """
    Idea:
        1. prev_3_max_oc < prev_2_max_oc < prev_1_max_oc
        (no require relationship between current_max & prev_1_max)
    :param max_oc:
    :return:
    """
    if max_oc[-4] < max_oc[-3] < max_oc[-2]:
        return True
    else:
        return False


def falling_three_cond_4(min_oc):
    """
    Idea:
        1. prev_3_min > current_min_oc
    :param min_oc:
    :return:
    """
    if min_oc[-4] > min_oc[-1]:
        return True
    else:
        return False


# --------------
def rising_three_cond_1(color):
    """
    Idea:
        1. current candlestick is white
    :param color:
    :return:
    """
    if color[-1] == WHITE_CS:
        return True
    else:
        return False


def rising_three_cond_2(body):
    """
    Idea:
        1. current_body > 3 * prev_3_body
        2. current_body > 3 * prev_2_body
        3. current_body > 3 * prev_1_body
        (no require relationship between prev_1_body & prev_2_body & prev_3_body)
    :param body:
    :return:
    """
    if body[-1] > 3 * body[-4] and body[-1] > 3 * body[-3] and body[-1] > 3 * body[-2]:
        return True
    else:
        return False


def rising_three_cond_3(max_oc):
    """
        Idea:
            1. prev_3_max_oc > current_max_oc
        :param max_oc:
        :return:
        """
    if max_oc[-4] < max_oc[-1]:
        return True
    else:
        return False


def rising_three_cond_4(min_oc):
    """
        Idea:
            1. prev_3_min_oc > prev_2_min_oc < prev_1_min_oc
            (no require relationship between current_min_oc & prev_1_min_oc)
        :param min_oc:
        :return:
        """
    if min_oc[-4] > min_oc[-3] > min_oc[-2]:
        return True
    else:
        return False
