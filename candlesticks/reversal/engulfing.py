from candlesticks import WHITE_CS, BLACK_CS


def is_bullish_engulfing(htd):
    if len(htd) < 2:
        raise Exception("Sorry, morning star model requires minimum 2 bars")
    color = htd['color'].to_list()
    _1st_condition = bullish_engulfing_cond_1(color)
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    _2nd_condition = bullish_engulfing_cond_2(_current_bar, _prev_bar)
    body = htd['body'].to_list()
    _3rd_condition = engulfing_cond_3(body)
    if _1st_condition and _2nd_condition and _3rd_condition:
        return True
    return False


def is_bearish_engulfing(htd):
    if len(htd) < 2:
        raise Exception("Sorry, evening star model requires minimum 2 bars")
    color = htd['color'].to_list()
    _1st_condition = bearish_engulfing_cond_1(color)
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    _2nd_condition = bearish_engulfing_cond_2(_current_bar, _prev_bar)
    body = htd['body'].to_list()
    _3rd_condition = engulfing_cond_3(body)
    if _1st_condition and _2nd_condition and _3rd_condition:
        return True
    return False


# -----------------------------------------------Conditions------------------------------------------------------------
def bullish_engulfing_cond_1(color):
    """
    Idea:
        1. current_bar = white
        2. prev_bar = black
    :param color:
    :return:
    """
    return True if (color[-1] == WHITE_CS and color[-2] == BLACK_CS) else False


def bullish_engulfing_cond_2(_current_bar, _prev_bar):
    """
    Idea:
        1. current_min_oc <= prev_bar_min_oc
        2. current_max_oc > prev_bar_max_oc
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    if _current_bar['min_OC'] <= _prev_bar['min_OC'] and _current_bar['max_OC'] > _prev_bar['max_OC']:
        return True
    return False


def engulfing_cond_3(body):
    """
    Idea:
        1. current body > 1.4
    :param body:
    :return:
    """
    return True if body[-1] > 1.4 else False

def bearish_engulfing_cond_1(color):
    """
    Idea:
        1. current_bar = black
        2. prev_bar = white
    :param color:
    :return:
    """
    return True if (color[-1] == BLACK_CS and color[-2] == WHITE_CS) else False


def bearish_engulfing_cond_2(_current_bar, _prev_bar):
    """
    Idea:
        1. current_min_oc < prev_bar_min_oc
        2. current_max_oc >= prev_bar_max_oc
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    if _current_bar['min_OC'] < _prev_bar['min_OC'] and _current_bar['max_OC'] >= _prev_bar['max_OC']:
        return True
    return False
