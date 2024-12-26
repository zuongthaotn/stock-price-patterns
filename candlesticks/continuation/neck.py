from candlesticks import WHITE_CS, BLACK_CS


def is_bullish_neck(htd):
    if len(htd) < 2:
        raise Exception("Sorry, neck model requires minimum 2 bars")
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    _1st_condition = bullish_neck_cond_1(_current_bar, _prev_bar)
    _2nd_condition = neck_cond_2(_current_bar, _prev_bar)
    _3rd_condition = bullish_neck_cond_3(_current_bar, _prev_bar)
    if _1st_condition and _2nd_condition and _3rd_condition:
        return True
    return False


def is_bearish_neck(htd):
    if len(htd) < 2:
        raise Exception("Sorry, neck model requires minimum 2 bars")
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    _1st_condition = bearish_neck_cond_1(_current_bar, _prev_bar)
    _2nd_condition = neck_cond_2(_current_bar, _prev_bar)
    _3rd_condition = bearish_neck_cond_3(_current_bar, _prev_bar)
    if _1st_condition and _2nd_condition and _3rd_condition:
        return True
    return False


# -----------------------------------------------Conditions------------------------------------------------------------
def bullish_neck_cond_1(_current_bar, _prev_bar):
    """
    Idea:
        1. current_color = black
        2. prev_color = white
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    return True if (_current_bar['color'] == BLACK_CS and _prev_bar['color'] == WHITE_CS) else False


def neck_cond_2(_current_bar, _prev_bar):
    """
    Idea:
        1. prev_body > 2 * current_body
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    return True if _prev_bar['body'] > 2 * _current_bar['body'] else False


def bullish_neck_cond_3(_current_bar, _prev_bar):
    """
    Idea:
        1. current_close > (prev_close + prev_open) / 2
        2. current_open > prev_close
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    if _current_bar['Open'] > _prev_bar['Close'] and \
            (_current_bar['Close'] > (_prev_bar['Close'] + _prev_bar['Open']) / 2):
        return True
    return False


def bearish_neck_cond_1(_current_bar, _prev_bar):
    """
    Idea:
        1. current_color = white
        2. prev_color = black
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    return True if (_current_bar['color'] == WHITE_CS and _prev_bar['color'] == BLACK_CS) else False


def bearish_neck_cond_3(_current_bar, _prev_bar):
    """
    Idea:
        1. current_close < (prev_close + prev_open) / 2
        2. current_open < prev_close
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    if _prev_bar['Close'] > _current_bar['Open'] and \
            _current_bar['Close'] < (_prev_bar['Close'] + _prev_bar['Open']) / 2:
        return True
    return False
