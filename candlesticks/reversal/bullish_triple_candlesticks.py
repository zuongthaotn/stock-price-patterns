from stock_price_patterns.candlesticks import *


class BullishTripleCandlestick:
    def __init__(self, htd, selected_patterns):
        self.child_df = htd
        self.bullish_triple_candlesticks = False
        self.morning_star = False
        self.morning_doji_star = False
        self.bullish_abandoned_baby = False
        self.bullish_spike = False
        self.bullish_stick_sandwich = False
        #
        self._current_bar = None
        self._prev_bar = None
        self._prev_2bars = None
        #
        self.patterns = selected_patterns

    def has_pattern(self):
        if len(self.child_df) < 3:
            raise Exception("Sorry, the bullish triple model requires 3 candlesticks")
        self._current_bar = self.child_df.iloc[-1]
        self._prev_bar = self.child_df.iloc[-2]
        self._prev_2bars = self.child_df.iloc[-3]
        if MORNING_STAR in self.patterns or MORNING_DOJI_STAR in self.patterns \
                or BULLISH_ABANDONED_BABY in self.patterns \
                or GET_REVERSAL in self.patterns or GET_FULL in self.patterns:
            self.__validate_morning_star_pattern()
        if BULLISH_SPIKE in self.patterns or GET_REVERSAL in self.patterns or GET_FULL in self.patterns:
            self.__validate_bullish_spike_pattern()
        if BULLISH_STICK_SANDWICH in self.patterns or GET_REVERSAL in self.patterns or GET_FULL in self.patterns:
            self.__validate_bullish_stick_sandwich_pattern()
        return self.bullish_triple_candlesticks

    def __validate_morning_star_pattern(self):
        """
        1. color conditions
            - current_color == white
            - prev_2_color == black
        """
        if not (self._current_bar['color'] == WHITE_CS and self._prev_2bars['color'] == BLACK_CS):
            return False
        """
        2. open-close conditions
            - prev_2_min_oc > prev_1_max_oc < current_min_oc
        """
        if not (self._prev_bar['max_OC'] <= self._prev_2bars['min_OC']
                and self._prev_bar['max_OC'] <= self._current_bar['min_OC']):
            return False
        self.bullish_triple_candlesticks = True
        if MORNING_DOJI_STAR in self.patterns \
                or BULLISH_ABANDONED_BABY in self.patterns \
                or GET_REVERSAL in self.patterns or GET_FULL in self.patterns:
            self.__validate_morning_doji_star_pattern()
        if BULLISH_ABANDONED_BABY in self.patterns \
                or GET_REVERSAL in self.patterns or GET_FULL in self.patterns:
            self.__validate_bullish_abandoned_baby_pattern()
        if MORNING_STAR not in self.patterns or GET_REVERSAL not in self.patterns or GET_FULL not in self.patterns:
            return False
        self.morning_star = True
        return True

    def __validate_morning_doji_star_pattern(self):
        if not self._prev_bar['color'] == DOJI_CS:
            return False
        self.morning_doji_star = True
        return True

    def __validate_bullish_abandoned_baby_pattern(self):
        if not (self._prev_2bars['Low'] > self._prev_bar['High'] and self._prev_bar['High'] < self._current_bar['Low']):
            return False
        self.bullish_abandoned_baby = True
        return True

    def __validate_bullish_spike_pattern(self):
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
                - prev_2_open <= current_close
        """
        if not (self._prev_2bars['color'] == BLACK_CS and self._current_bar['color'] == WHITE_CS):
            return False
        if not (self._prev_2bars['Low'] > self._prev_bar['Low'] and self._current_bar['Low'] > self._prev_bar['Low']):
            return False
        if not (self._prev_2bars['min_OC'] < self._prev_bar['min_OC']
                and self._prev_bar['min_OC'] > self._current_bar['min_OC']):
            return False
        if not self._prev_2bars['max_OC'] < self._prev_bar['max_OC']:
            return False
        if not (2 * self._prev_bar['body'] < self._prev_2bars['body'] < self._current_bar['body']):
            return False
        if not self._prev_2bars['Open'] <= self._prev_bar['Close']:
            return False
        self.bullish_spike = True
        self.bullish_triple_candlesticks = True
        return True

    def __validate_bullish_stick_sandwich_pattern(self):
        """
        Conditions:
          1. prev_2_max_oc > prev_1_max_oc
          2. current_max_oc > prev_1_max_oc
          3. abs(prev_2_max_oc - current_max_oc) < 0.2
        """
        if not (self._prev_2bars['max_OC'] > self._prev_bar['max_OC']
                and self._current_bar['max_OC'] > self._prev_bar['max_OC']
                and abs(self._prev_2bars['max_OC'] - self._current_bar['max_OC']) < 0.2):
            return False
        """
        Conditions:
          1. prev_2_min_oc < prev_1_min_oc
          2. current_min_oc < prev_1_min_oc
          3. abs(prev_2_min_oc - current_min_oc) < 0.2
        """
        if not (self._prev_2bars['min_OC'] < self._prev_bar['min_OC']
                and self._current_bar['min_OC'] < self._prev_bar['min_OC']
                and abs(self._prev_2bars['min_OC'] - self._current_bar['min_OC']) < 0.2):
            return False
        """
        Conditions:
          1. current_color = black/red
          2. prev_1_color = white/green
          3. prev_2_color = black/red
        """
        if not (self._current_bar['color'] == BLACK_CS and self._prev_bar['color'] == WHITE_CS
                and self._prev_2bars['color'] == BLACK_CS):
            return False
        self.bullish_stick_sandwich = True
        self.bullish_triple_candlesticks = True
        return True

    def is_morning_star(self):
        return self.morning_star

    def is_morning_doji_star(self):
        return self.morning_doji_star

    def is_bullish_abandoned_baby(self):
        return self.bullish_abandoned_baby

    def is_bullish_spike(self):
        return self.bullish_spike

    def is_bullish_stick_sandwich(self):
        return self.bullish_stick_sandwich
