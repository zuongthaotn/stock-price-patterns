from candlesticks import WHITE_CS, BLACK_CS, DOJI_CS


def is_morning_star(htd):
    if len(htd) < 3:
        raise Exception("Sorry, morning star model requires minimum 3 bars")
    color = htd['color'].to_list()
    _1st_condition = morning_star_cond_1(color)
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    _prev_2bars = htd.iloc[-3]
    _2nd_condition = morning_star_cond_2(_current_bar, _prev_bar, _prev_2bars)

    if _1st_condition and _2nd_condition:
        return True
    return False


def is_evening_star(htd):
    if len(htd) < 3:
        raise Exception("Sorry, evening star model requires minimum 3 bars")
    color = htd['color'].to_list()
    _1st_condition = evening_star_cond_1(color)
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    _prev_2bars = htd.iloc[-3]
    _2nd_condition = evening_star_cond_2(_current_bar, _prev_bar, _prev_2bars)

    if _1st_condition and _2nd_condition:
        return True
    return False


def is_bullish_abandoned_baby(htd, morning_star=False):
    if not morning_star:
        raise Exception("Sorry, bullish abandoned baby model requires it must be morning_star")
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    _prev_2bars = htd.iloc[-3]
    _condition = bullish_abandoned_baby_cond(_current_bar, _prev_bar, _prev_2bars)
    if _condition:
        return True
    return False


def is_bearish_abandoned_baby(htd, evening_star=False):
    if not evening_star:
        raise Exception("Sorry, bullish abandoned baby model requires it must be evening_star")
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    _prev_2bars = htd.iloc[-3]
    _condition = bearish_abandoned_baby_cond(_current_bar, _prev_bar, _prev_2bars)
    if _condition:
        return True
    return False


def is_evening_doji_star(htd, evening_star=False):
    if not evening_star:
        raise Exception("Sorry, evening doji star model requires it must be evening_star")
    _prev_bar = htd.iloc[-2]
    if _prev_bar['color'] == DOJI_CS:
        return True
    return False


def is_morning_doji_star(htd, morning_star=False):
    if not morning_star:
        raise Exception("Sorry, morning doji star model requires it must be morning_star")
    _prev_bar = htd.iloc[-2]
    if _prev_bar['color'] == DOJI_CS:
        return True
    return False


# -----------------------------------------------Conditions------------------------------------------------------------
def bullish_abandoned_baby_cond(_current_bar, _prev_bar, _prev_2bars):
    """
    Idea:
        1. low_prev_2_bar > high_prev_1_bar
        2. low_current_bar > high_prev_1_bar
    :param _current_bar:
    :param _prev_bar:
    :param _prev_2bars:
    :return:
    """
    if _prev_bar['High'] < _prev_2bars['Low'] and _prev_bar['High'] < _current_bar['Low']:
        return True
    return False


def bearish_abandoned_baby_cond(_current_bar, _prev_bar, _prev_2bars):
    """
    Idea:
        1. high_prev_2_bar < low_prev_1_bar
        2. high_current_bar > low_prev_1_bar
    :param _current_bar:
    :param _prev_bar:
    :param _prev_2bars:
    :return:
    """
    if _prev_bar['Low'] > _prev_2bars['High'] and _prev_bar['Low'] > _current_bar['High']:
        return True
    return False


def morning_star_cond_1(color):
    """
    Idea:
            1. current_color == white
            2. prev_2_color == black
    :param color:
    :return:
    """
    return True if (color[-1] == WHITE_CS and color[-3] == BLACK_CS) else False


def morning_star_cond_2(_current_bar, _prev_bar, _prev_2bars):
    """
    Idea:
        1. prev_2_min_oc > prev_1_max_oc < current_min_oc
    :param _current_bar:
    :param _prev_bar:
    :param _prev_2bars:
    :return:
    """
    if _prev_bar['max_OC'] <= _prev_2bars['min_OC'] and _prev_bar['max_OC'] <= _current_bar['min_OC']:
        return True
    return False


def evening_star_cond_1(color):
    """
    Idea:
            1. current_color == black
            2. prev_2_color == white
    :param color:
    :return:
    """
    return True if (color[-1] == BLACK_CS and color[-3] == WHITE_CS) else False


def evening_star_cond_2(_current_bar, _prev_bar, _prev_2bars):
    """
    Idea:
        1. prev_2_max_oc < prev_1_min_oc > current_max_oc
    :param _current_bar:
    :param _prev_bar:
    :param _prev_2bars:
    :return:
    """
    if _prev_2bars['max_OC'] <= _prev_bar['min_OC'] and _current_bar['max_OC'] <= _prev_bar['min_OC']:
        return True
    return False
