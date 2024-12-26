from candlesticks import WHITE_CS, BLACK_CS, DOJI_CS


class BearishDoubleCandlestick:
    def __init__(self, htd):
        self.child_df = htd
        self.bearish_double_candlesticks = False
        self.bearish_engulfing = False
        self.bearish_harami = False
        self.bearish_harami_cross = False
        self.dark_cloud_cover = False
        self.matching_high = False
        self.bearish_meeting_line = False
        self.bearish_tasuki_line = False
        self.tweezers_top = False
        #
        self._current_bar = None
        self._prev_bar = None

    def is_bearish_engulfing(self):
        return self.bearish_engulfing

    def is_bearish_harami(self):
        return self.bearish_harami

    def is_bearish_harami_cross(self):
        return self.bearish_harami_cross

    def is_dark_cloud_cover(self):
        return self.dark_cloud_cover

    def is_matching_high(self):
        return self.matching_high

    def is_bearish_meeting_line(self):
        return self.bearish_meeting_line

    def is_bearish_tasuki_line(self):
        return self.bearish_tasuki_line

    def is_tweezers_top(self):
        return self.tweezers_top

    def has_pattern(self):
        if len(self.child_df) < 2:
            raise Exception("Sorry, the bearish double model requires 2 candlesticks")
        self._current_bar = self.child_df.iloc[-1]
        self._prev_bar = self.child_df.iloc[-2]
        if self._current_bar['Low'] == self._current_bar['High'] or self._prev_bar['Low'] == self._prev_bar['High']:
            return False
        self.__validate_bearish_engulfing_pattern()
        self.__validate_matching_high_pattern()
        return self.bearish_double_candlesticks

    def __validate_matching_high_pattern(self):
        """
        Conditions:
            1. current_bar = white
            2. prev_bar = white
        """
        if not (self._current_bar['color'] == WHITE_CS and self._prev_bar['color'] == WHITE_CS):
            return False
        """
        Conditions:
            1. prev_bar_high = prev_bar_close
            2. current_high = current_close
            3. current_close = prev_bar_close
        """
        if not (self._prev_bar['High'] == self._prev_bar['Close']
                and self._current_bar['High'] == self._current_bar['Close']
                and self._current_bar['Close'] == self._prev_bar['Close']):
            return False
        self.matching_high = True
        self.bearish_double_candlesticks = True
        return True

    def __validate_bearish_engulfing_pattern(self):
        """
        Conditions:
            1. current_bar = black
            2. prev_bar = white
        """
        if not (self._current_bar['color'] == BLACK_CS and self._prev_bar['color'] == WHITE_CS):
            return False
        self.__validate_tweezers_top_pattern()
        self.__validate_bearish_harami_pattern()
        self.__validate_dark_cloud_cover_pattern()
        self.__validate_tasuki_line_pattern()
        """
        Conditions:
            1. current_max_oc >= prev_bar_max_oc
            2. current_min_oc < prev_bar_min_oc
        """
        if not (self._current_bar['max_OC'] >= self._prev_bar['max_OC']
                and self._current_bar['min_OC'] < self._prev_bar['min_OC']):
            return False
        self.bearish_engulfing = True
        self.bearish_double_candlesticks = True
        return True

    def __validate_tweezers_top_pattern(self):
        """
        Conditions:
            1. current_high == prev_bar_high
        """
        if not (self._current_bar['High'] == self._prev_bar['High']):
            return False
        self.tweezers_top = True
        self.bearish_double_candlesticks = True
        return True

    def __validate_tasuki_line_pattern(self):
        """
        Conditions:
            1. current_open < prev_bar_close
            2. current_close <= prev_bar_low
        """
        if not (self._current_bar['Open'] < self._prev_bar['Close']
                and self._current_bar['Close'] <= self._prev_bar['Low']):
            return False
        self.bearish_tasuki_line = True
        self.bearish_double_candlesticks = True
        return True

    def __validate_dark_cloud_cover_pattern(self):
        self.__validate_meeting_line_pattern()
        """
        Conditions:
            1. current_open > prev_bar_close
            2. current_close <= (prev_bar_open + prev_bar_close) / 2
        """
        if not (self._current_bar['Open'] > self._prev_bar['Close']
                and self._current_bar['Close'] <= (self._prev_bar['Open'] + self._prev_bar['Close'])/2):
            return False
        self.dark_cloud_cover = True
        self.bearish_double_candlesticks = True
        return True

    def __validate_meeting_line_pattern(self):
        """
        Conditions:
            1. current_open > prev_bar_close
            2. current_close == prev_bar_close
        """
        if not (self._current_bar['Open'] > self._prev_bar['Close']
                and self._current_bar['Close'] == self._prev_bar['Close']):
            return False
        self.bearish_meeting_line = True
        self.bearish_double_candlesticks = True
        return True

    def __validate_bearish_harami_pattern(self):
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
        self.__validate_bearish_harami_cross_pattern()
        self.bearish_harami = True
        self.bearish_double_candlesticks = True
        return True

    def __validate_bearish_harami_cross_pattern(self):
        if not self._current_bar['color'] == DOJI_CS:
            return False
        self.bearish_harami_cross = True
        self.bearish_double_candlesticks = True
        return True
