from candlesticks import WHITE_CS, BLACK_CS, DOJI_CS


def is_bullish_spike(htd):
    if len(htd) < 3:
        raise Exception("Sorry, bullish spike model requires minimum 3 bars")
    """
        Idea:
        1. color:
            - First candlestick(_prev_2bars) is black/red
            - Last candlestick(_current_bar) is white/green
        2. Low price:
            - low_prev_2_bar > low_prev_1_bar < low_current_bar
        3. min_oc price:
            - prev_2_min_oc < prev_1_min_oc > current_min_oc
        4. max_oc price:
            - prev_2_max_oc > prev_1_max_oc
        5. body:
            - prev_2_body >= prev_1_body * 2 =< current_body
        6. Close price:
            - prev_2_close <= current_close
    """
    color = htd['color'].to_list()
    if not (color[-3] == BLACK_CS and color[-1] == WHITE_CS):
        return False
    low = htd['Low'].to_list()
    if not (low[-3] > low[-2] and low[-1] > low[-2]):
        return False
    min_oc = htd['min_OC'].to_list()
    if not (min_oc[-3] < min_oc[-2] and min_oc[-2] > min_oc[-1]):
        return False
    max_oc = htd['max_OC'].to_list()
    if not max_oc[-3] > max_oc[-2]:
        return False
    body = htd['body'].to_list()
    if not (2 * body[-2] < body[-3] < body[-1]):
        return False
    close = htd['Close'].to_list()
    if not close[-3] <= close[-1]:
        return False
    return True


def is_bearish_spike(htd):
    if len(htd) < 3:
        raise Exception("Sorry, bearish spike model requires minimum 3 bars")
    """
        Idea:
        1. color:
            - First candlestick(_prev_2bars) is white/green
            - Last candlestick(_current_bar) is black/red
        2. High price:
            - high_prev_2_bar < high_prev_1_bar > high_current_bar
        3. min_oc price:
            - prev_2_min_oc < prev_1_min_oc > current_min_oc
        4. max_oc price:
            - prev_2_max_oc > prev_1_max_oc
        5. body:
            - prev_2_body >= prev_1_body * 2 =< current_body
        6. Close price:
            - prev_2_close >= current_close
    """
    color = htd['color'].to_list()
    if not (color[-3] == WHITE_CS and color[-1] == BLACK_CS):
        return False
    high = htd['High'].to_list()
    if not (high[-3] < high[-2] and high[-1] < high[-2]):
        return False
    min_oc = htd['min_OC'].to_list()
    if not (min_oc[-3] < min_oc[-2] and min_oc[-2] > min_oc[-1]):
        return False
    max_oc = htd['max_OC'].to_list()
    if not max_oc[-3] > max_oc[-2]:
        return False
    body = htd['body'].to_list()
    if not (2 * body[-2] < body[-3] < body[-1]):
        return False
    close = htd['Close'].to_list()
    if not close[-3] >= close[-1]:
        return False
    return True
