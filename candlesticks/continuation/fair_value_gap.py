from candlesticks import WHITE_CS, BLACK_CS


def is_fair_value_rising_gap(htd):
    if len(htd) < 3:
        raise Exception("Sorry, fair value gap model requires minimum 3 bars")
    _current_bar = htd.iloc[-1]
    _prev_1_bar = htd.iloc[-2]
    _prev_2_bar = htd.iloc[-3]
    _1st_condition = is_passed_1st_rising_condition(_current_bar, _prev_1_bar, _prev_2_bar)
    _2nd_condition = is_passed_2nd_rising_condition(_current_bar, _prev_1_bar, _prev_2_bar)
    if _1st_condition and _2nd_condition:
        return True
    return False


def is_fair_value_falling_gap(htd):
    if len(htd) < 3:
        raise Exception("Sorry, fair value gap model requires minimum 3 bars")
    _current_bar = htd.iloc[-1]
    _prev_1_bar = htd.iloc[-2]
    _prev_2_bar = htd.iloc[-3]
    _1st_condition = is_passed_1st_falling_condition(_current_bar, _prev_1_bar, _prev_2_bar)
    _2nd_condition = is_passed_2nd_falling_condition(_current_bar, _prev_1_bar, _prev_2_bar)
    if _1st_condition and _2nd_condition:
        return True
    return False


# -----------------------------------------------Conditions------------------------------------------------------------
def is_passed_1st_rising_condition(_current_bar, _prev_1_bar, _prev_2_bar):
    """
    Idea:
        1. current_color = white
        2. _prev_1_bar_color = white
        3. _prev_2_bar_color = white
    :param _current_bar:
    :param _prev_1_bar:
    :param _prev_2_bar:
    :return:
    """
    if _current_bar['color'] == WHITE_CS and _prev_1_bar['color'] == WHITE_CS and _prev_2_bar['color'] == WHITE_CS:
        return True
    return False


def is_passed_2nd_rising_condition(_current_bar, _prev_1_bar, _prev_2_bar):
    """
        Idea:
            1. _prev_2_bar_high < current_low
        :param _current_bar:
        :param _prev_1_bar:
        :param _prev_2_bar:
        :return:
        """
    if _current_bar['Low'] > _prev_2_bar['High']:
        return True
    return False


def is_passed_1st_falling_condition(_current_bar, _prev_1_bar, _prev_2_bar):
    """
    Idea:
        1. current_color = black
        2. _prev_1_bar_color = black
        3. _prev_2_bar_color = black
    :param _current_bar:
    :param _prev_1_bar:
    :param _prev_2_bar:
    :return:
    """
    if _current_bar['color'] == BLACK_CS and _prev_1_bar['color'] == BLACK_CS and _prev_2_bar['color'] == BLACK_CS:
        return True
    return False


def is_passed_2nd_falling_condition(_current_bar, _prev_1_bar, _prev_2_bar):
    """
        Idea:
            1. _prev_2_bar_low > current_high
        :param _current_bar:
        :param _prev_1_bar:
        :param _prev_2_bar:
        :return:
        """
    if _current_bar['High'] < _prev_2_bar['Low']:
        return True
    return False
