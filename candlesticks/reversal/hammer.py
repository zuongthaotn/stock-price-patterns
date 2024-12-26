from candlesticks import WHITE_CS, BLACK_CS
MIN_CANDLESTICK = 4


def is_hammer(htd):
    if len(htd) < MIN_CANDLESTICK:
        raise Exception(f'Sorry, hammer model requires minimum {MIN_CANDLESTICK} candlestick(s)')
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    color = htd['color'].to_list()
    _1st_condition = hammer_cond_1(_current_bar, _prev_bar)
    _2nd_condition = is_white_after_3blacks(color)
    if _1st_condition and _2nd_condition:
        return True
    return False


def is_inverted_hammer(htd):
    if len(htd) < 1:
        raise Exception("Sorry, inverted hammer model requires minimum 1 bar")
    """
        Idea:
                1. current_tail < 0.3
                2. current_upper_wick > 3 * current_body
        :param htd:
        :return:
        """
    _current_bar = htd.iloc[-1]
    if _current_bar['tail'] < 0.3 and _current_bar['upper_wick'] > 3 * _current_bar['body'] and \
            _current_bar['upper_wick'] > 1.3:
        return True
    return False


def is_hanging_man(htd):
    if len(htd) < 4:
        raise Exception("Sorry, hanging man model requires minimum 4 bars")
    _current_bar = htd.iloc[-1]
    _prev_bar = htd.iloc[-2]
    color = htd['color'].to_list()
    _1st_condition = hanging_man_cond_1(_current_bar, _prev_bar)
    _2nd_condition = is_black_after_3whites(color)
    if _1st_condition and _2nd_condition:
        return True
    return False


# -----------------------------------------------Conditions------------------------------------------------------------
def hanging_man_cond_1(_current_bar, _prev_bar):
    """
    Idea:
            1. prev_1_upper_wick < 0.3
            2. prev_1_tail > 3 * prev_1_body
            3. current_close > prev_high
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    if _prev_bar['upper_wick'] < 0.3 and _prev_bar['tail'] > 3 * _prev_bar['body'] and _prev_bar['tail'] > 1.3 and \
            _current_bar['Close'] < _prev_bar['Low']:
        return True
    return False


def is_black_after_3whites(color):
    """
    Idea:
        1. current candlestick is black/red
        2. prev_1_color = prev_2_color = prev_3_color = white/green
    :param color:
    :return:
    """
    if color[-4] == WHITE_CS and color[-3] == WHITE_CS and color[-2] == WHITE_CS and color[-1] == BLACK_CS:
        return True
    else:
        return False


def is_white_after_3blacks(color):
    """
    Idea:
        1. current candlestick is white/green
        2. prev_1_color = prev_2_color = prev_3_color = black/red
    :param color:
    :return:
    """
    if color[-4] == BLACK_CS and color[-3] == BLACK_CS and color[-2] == BLACK_CS and color[-1] == WHITE_CS:
        return True
    else:
        return False


def hammer_cond_1(_current_bar, _prev_bar):
    """
    Idea:
            1. prev_1_upper_wick < 0.3
            2. prev_1_tail > 3 * prev_1_body
            3. current_close > prev_high
    :param _current_bar:
    :param _prev_bar:
    :return:
    """
    if _prev_bar['upper_wick'] < 0.3 and _prev_bar['tail'] > 3 * _prev_bar['body'] and _prev_bar['tail'] > 1.3 and \
            _current_bar['Close'] > _prev_bar['High']:
        return True
    return False
