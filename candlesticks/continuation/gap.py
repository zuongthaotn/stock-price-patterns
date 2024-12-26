from candlesticks import WHITE_CS, BLACK_CS


def is_bullish_gap(htd):
    if len(htd) < 2:
        raise Exception("Sorry, gap model requires minimum 2 bars")
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    _1st_condition = bullish_gap_cond_1(_current_bar, _prev_bar)
    _2nd_condition = bullish_gap_cond_2(_current_bar, _prev_bar)
    if _1st_condition and _2nd_condition:
        return True
    return False


def is_bearish_gap(htd):
    if len(htd) < 2:
        raise Exception("Sorry, gap model requires minimum 2 bars")
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    _1st_condition = bearish_gap_cond_1(_current_bar, _prev_bar)
    _2nd_condition = bearish_gap_cond_2(_current_bar, _prev_bar)
    if _1st_condition and _2nd_condition:
        return True
    return False


# -----------------------------------------------Conditions------------------------------------------------------------
def bullish_gap_cond_1(_current_bar, _prev_bar):
    """
    Idea:
        1. current_color = white
        2. prev_color = white
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    return True if (_current_bar['color'] == WHITE_CS and _prev_bar['color'] == WHITE_CS) else False


def bullish_gap_cond_2(_current_bar, _prev_bar):
    """
    Idea:
        1. prev_high < current_low
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    return True if _prev_bar['High'] < _current_bar['Low'] else False


def bearish_gap_cond_1(_current_bar, _prev_bar):
    """
    Idea:
        1. current_color = black
        2. prev_color = black
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    return True if (_current_bar['color'] == BLACK_CS and _prev_bar['color'] == BLACK_CS) else False


def bearish_gap_cond_2(_current_bar, _prev_bar):
    """
    Idea:
        1. prev_low > current_high
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    return True if _prev_bar['Low'] > _current_bar['High'] else False
