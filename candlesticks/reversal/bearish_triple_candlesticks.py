from stock_price_patterns import WHITE_CS, BLACK_CS, DOJI_CS


class BearishTripleCandlestick:
    def __init__(self, htd):
        self.child_df = htd
        self.bearish_triple_candlesticks = False
        self.evening_star = False
        self.evening_doji_star = False
        self.bearish_abandoned_baby = False
        self.bearish_spike = False
        self.bearish_stick_sandwich = False
        #
        self._current_bar = None
        self._prev_bar = None
        self._prev_2bars = None

    def has_pattern(self):
        if len(self.child_df) < 3:
            raise Exception("Sorry, the bearish triple model requires 3 candlesticks")
        self._current_bar = self.child_df.iloc[-1]
        self._prev_bar = self.child_df.iloc[-2]
        self._prev_2bars = self.child_df.iloc[-3]
        self.__validate_evening_star_pattern()
        self.__validate_bearish_spike_pattern()
        self.__validate_bearish_stick_sandwich_pattern()
        return self.bearish_triple_candlesticks

    def __validate_evening_star_pattern(self):
        """
        1. color conditions
            - current_color == black
            - prev_2_color == white
        """
        if not (self._current_bar['color'] == BLACK_CS and self._prev_2bars['color'] == WHITE_CS):
            return False
        """
        2. open-close conditions
            - prev_2_max_oc <= prev_1_min_oc >= current_max_oc
        """
        if not (self._prev_bar['min_OC'] >= self._prev_2bars['max_OC']
                and self._prev_bar['min_OC'] >= self._current_bar['max_OC']):
            return False
        self.bearish_triple_candlesticks = True
        self.evening_star = True
        self.__validate_evening_doji_star_pattern()
        self.__validate_bearish_abandoned_baby_pattern()
        return True

    def __validate_evening_doji_star_pattern(self):
        if not self._prev_bar['color'] == DOJI_CS:
            return False
        self.evening_doji_star = True
        return True

    def __validate_bearish_abandoned_baby_pattern(self):
        if not (self._prev_2bars['High'] < self._prev_bar['Low'] and self._prev_bar['Low'] > self._current_bar['High']):
            return False
        self.bearish_abandoned_baby = True
        return True

    def __validate_bearish_spike_pattern(self):
        """
        Condition:
            1. color:
                - First candlestick(_prev_2bars) is white/green
                - Last candlestick(_current_bar) is black/red
        """
        if not (self._prev_2bars['color'] == WHITE_CS and self._current_bar['color'] == BLACK_CS):
            return False
        """
        Condition:
            2. High price:
                - high_prev_2_bar < high_prev_1_bar > high_current_bar
        """
        if not (self._prev_2bars['High'] < self._prev_bar['High']
                and self._current_bar['High'] < self._prev_bar['High']):
            return False
        """
        Condition:
            3. min_oc price:
                - prev_2_min_oc < prev_1_min_oc > current_min_oc
        """
        if not (self._prev_2bars['min_OC'] < self._prev_bar['min_OC']
                and self._prev_bar['min_OC'] > self._current_bar['min_OC']):
            return False
        """
        Condition:
            4. max_oc price:
                - prev_2_max_oc > prev_1_max_oc
        """
        if not self._prev_2bars['max_OC'] < self._prev_bar['max_OC']:
            return False
        """
        Condition:
            5. body:
                - prev_2_body >= prev_1_body * 2 =< current_body
        """
        if not (2 * self._prev_bar['body'] < self._prev_2bars['body'] < self._current_bar['body']):
            return False
        """
        Condition:
            6. Close price:
                - prev_2_open >= current_close
        """
        if not self._prev_2bars['Open'] >= self._prev_bar['Close']:
            return False
        self.bearish_spike = True
        self.bearish_triple_candlesticks = True
        return True

    def __validate_bearish_stick_sandwich_pattern(self):
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
          1. current_color = white/green
          2. prev_1_color = black/red
          3. prev_2_color = white/green
        """
        if not (self._current_bar['color'] == WHITE_CS and self._prev_bar['color'] == BLACK_CS
                and self._prev_2bars['color'] == WHITE_CS):
            return False
        self.bearish_stick_sandwich = True
        self.bearish_triple_candlesticks = True
        return True

    def is_evening_star(self):
        return self.evening_star

    def is_evening_doji_star(self):
        return self.evening_doji_star

    def is_bearish_abandoned_baby(self):
        return self.bearish_abandoned_baby

    def is_bearish_spike(self):
        return self.bearish_spike

    def is_bearish_stick_sandwich(self):
        return self.bearish_stick_sandwich
