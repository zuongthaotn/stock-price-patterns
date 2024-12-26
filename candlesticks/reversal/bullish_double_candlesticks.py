from candlesticks import WHITE_CS, BLACK_CS, DOJI_CS


class BullishDoubleCandlestick:
    def __init__(self, htd):
        self.child_df = htd
        self.bullish_double_candlesticks = False
        self.bullish_engulfing = False
        self.bullish_harami = False
        self.bullish_harami_cross = False
        self.piercing = False
        self.matching_low = False
        self.bullish_meeting_line = False
        self.bullish_tasuki_line = False
        self.tweezers_bottom = False
        #
        self._current_bar = None
        self._prev_bar = None

    def is_bullish_engulfing(self):
        return self.bullish_engulfing

    def is_bullish_harami(self):
        return self.bullish_harami

    def is_bullish_harami_cross(self):
        return self.bullish_harami_cross

    def is_piercing(self):
        return self.piercing

    def is_matching_low(self):
        return self.matching_low

    def is_bullish_meeting_line(self):
        return self.bullish_meeting_line

    def is_bullish_tasuki_line(self):
        return self.bullish_tasuki_line

    def is_tweezers_bottom(self):
        return self.tweezers_bottom

    def has_pattern(self):
        if len(self.child_df) < 2:
            raise Exception("Sorry, the bullish double model requires 2 candlesticks")
        self._current_bar = self.child_df.iloc[-1]
        self._prev_bar = self.child_df.iloc[-2]
        if self._current_bar['Low'] == self._current_bar['High'] or self._prev_bar['Low'] == self._prev_bar['High']:
            return False
        self.__validate_bullish_engulfing_pattern()
        self.__validate_matching_low_pattern()
        return self.bullish_double_candlesticks

    def __validate_matching_low_pattern(self):
        """
        Conditions:
            1. current_bar = black
            2. prev_bar = black
        """
        if not (self._current_bar['color'] == BLACK_CS and self._prev_bar['color'] == BLACK_CS):
            return False
        """
        Conditions:
            1. prev_bar_low = prev_bar_close
            2. current_low = current_close
            3. current_close = prev_bar_close
        """
        if not (self._prev_bar['Low'] == self._prev_bar['Close']
                and self._current_bar['Low'] == self._current_bar['Close']
                and self._current_bar['Close'] == self._prev_bar['Close']):
            return False
        self.matching_low = True
        self.bullish_double_candlesticks = True
        return True

    def __validate_bullish_engulfing_pattern(self):
        """
        Conditions:
            1. current_bar = white
            2. prev_bar = black
        """
        if not (self._current_bar['color'] == WHITE_CS and self._prev_bar['color'] == BLACK_CS):
            return False
        self.__validate_tweezers_bottom_pattern()
        self.__validate_bullish_harami_pattern()
        self.__validate_piercing_pattern()
        self.__validate_tasuki_line_pattern()
        """
        Conditions:
            1. current_min_oc <= prev_bar_min_oc
            2. current_max_oc > prev_bar_max_oc
        """
        if not (self._current_bar['min_OC'] <= self._prev_bar['min_OC']
                and self._current_bar['max_OC'] > self._prev_bar['max_OC']):
            return False
        self.bullish_engulfing = True
        self.bullish_double_candlesticks = True
        return True

    def __validate_tweezers_bottom_pattern(self):
        """
        Conditions:
            1. current_low == prev_bar_low
        """
        if not (self._current_bar['Low'] == self._prev_bar['Low']):
            return False
        self.tweezers_bottom = True
        self.bullish_double_candlesticks = True
        return True

    def __validate_tasuki_line_pattern(self):
        """
        Conditions:
            1. current_open > prev_bar_close
            2. current_close > prev_bar_high
        """
        if not (self._current_bar['Open'] > self._prev_bar['Close']
                and self._current_bar['Close'] >= self._prev_bar['High']):
            return False
        self.bullish_tasuki_line = True
        self.bullish_double_candlesticks = True
        return True

    def __validate_piercing_pattern(self):
        self.__validate_meeting_line_pattern()
        """
        Conditions:
            1. current_open < prev_bar_close
            2. current_close > (prev_bar_open + prev_bar_close) / 2
        """
        if not (self._current_bar['Open'] < self._prev_bar['Close']
                and self._current_bar['Close'] >= (self._prev_bar['Open'] + self._prev_bar['Close'])/2):
            return False
        self.piercing = True
        self.bullish_double_candlesticks = True
        return True

    def __validate_meeting_line_pattern(self):
        """
        Conditions:
            1. current_open < prev_bar_close
            2. current_close == prev_bar_close
        """
        if not (self._current_bar['Open'] < self._prev_bar['Close']
                and self._current_bar['Close'] == self._prev_bar['Close']):
            return False
        self.bullish_meeting_line = True
        self.bullish_double_candlesticks = True
        return True

    def __validate_bullish_harami_pattern(self):
        """
        Conditions:
            1. current_high <= prev_bar_max_oc
            2. current_low > prev_bar_min_oc
        """
        if not (self._current_bar['High'] <= self._prev_bar['max_OC']
                and self._current_bar['Low'] >= self._prev_bar['min_OC']):
            return False
        """
        Condition:
            1. prev_bar_body >= 2*current_body
        """
        if not self._prev_bar['body'] >= 2 * self._current_bar['body']:
            return False
        self.__validate_bullish_harami_cross_pattern()
        self.bullish_harami = True
        self.bullish_double_candlesticks = True
        return True

    def __validate_bullish_harami_cross_pattern(self):
        if not self._current_bar['color'] == DOJI_CS:
            return False
        self.bullish_harami_cross = True
        self.bullish_double_candlesticks = True
        return True
