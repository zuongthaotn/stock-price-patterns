from .candlesticks.continuation.gap import is_bullish_gap, is_bearish_gap
from .candlesticks.continuation.neck import is_bullish_neck, is_bearish_neck
from .candlesticks.continuation.fair_value_gap import is_fair_value_rising_gap, is_fair_value_falling_gap
from .candlesticks.continuation.three_methods import is_rising_three, is_falling_three
from .candlesticks.continuation.separating_line import is_bullish_separating_line, is_bearish_separating_line
from .candlesticks.continuation.four_bars_made_n import is_rising_n, is_falling_n
#
from .candlesticks.reversal.bullish_double_candlesticks import BullishDoubleCandlestick
from .candlesticks.reversal.bearish_double_candlesticks import BearishDoubleCandlestick
from .candlesticks.reversal.bullish_triple_candlesticks import BullishTripleCandlestick
from .candlesticks.reversal.bearish_triple_candlesticks import BearishTripleCandlestick
from .candlesticks import ALLOWED_PATTERNS, GET_FULL, GET_CONTINUE, GET_REVERSAL
from .candlesticks import WHITE_CS, BLACK_CS, DOJI_CS, MARUBOZU_CS, HANGING_MAN_CS
from .candlesticks import SHOOTING_STAR_CS, SPINNING_TOP_CS, HAMMER_CS, INVERTED_HAMMER_CS


class CandlestickPatterns:
    def __init__(self, data):
        self.working_data = data.copy()
        self.added_patterns = []

    def _add(self, pattern_name):
        self.__validate(pattern_name)
        self.added_patterns.append(pattern_name)

    def pattern_modeling(self):
        prepared_data = self.prepare_data(self.working_data)
        if not len(self.added_patterns):
            prepared_data['model'] = ''
            return prepared_data
        #
        data_len = len(prepared_data)
        models = []
        for i in range(0, data_len):
            if i < 5:
                models.append('')
                continue
            _start = i - 4
            _end = i + 1
            #
            working_htd = prepared_data.iloc[_start: _end]
            if len(self.added_patterns) == 1:
                if GET_CONTINUE in self.added_patterns:
                    model = self.get_continuation_cs_pattern(working_htd)
                elif GET_REVERSAL in self.added_patterns:
                    model = self.get_reversal_cs_pattern(working_htd)
                else:
                    model = self.get_full_candlestick_pattern(working_htd)
            else:
                model = self.get_full_candlestick_pattern(working_htd)
            #
            if len(model):
                model = ', '.join(model)
            else:
                model = ''
            models.append(model)
        prepared_data['model'] = models
        return prepared_data

    def prepare_data(self, htd):
        htd['min_OC'] = htd.apply(
            lambda r: min(r['Open'], r['Close']), axis=1)
        htd['max_OC'] = htd.apply(
            lambda r: max(r['Open'], r['Close']), axis=1)
        #
        htd['upper_wick'] = htd.apply(
            lambda r: r['High'] - max(r['Open'], r['Close']), axis=1)
        htd['tail'] = htd.apply(
            lambda r: min(r['Open'], r['Close']) - r['Low'], axis=1)
        htd["oc_dif"] = htd.apply(lambda r: r['Close'] - r['Open'], axis=1)
        htd['body'] = htd["oc_dif"].abs()
        htd['color'] = htd.apply(
            lambda r: DOJI_CS if r['oc_dif'] == 0 else (
                WHITE_CS if r['oc_dif'] > 0 else BLACK_CS), axis=1)
        htd['candlestick'] = htd.apply(lambda r: self.get_candlestick(r), axis=1)
        return htd

    @staticmethod
    def get_reversal_cs_pattern(child_df, get_full=True):
        pattern = []
        #
        """" Triple candlesticks """
        bull_tc = BullishTripleCandlestick(child_df)
        if bull_tc.has_pattern():
            if bull_tc.is_morning_star():
                if bull_tc.is_bullish_abandoned_baby():
                    pattern.append('is_bullish_abandoned_baby')
                elif bull_tc.is_morning_doji_star():
                    pattern.append('is_morning_doji_star')
                else:
                    pattern.append('is_morning_star')
            elif bull_tc.is_bullish_spike():
                pattern.append('bullish_spike')
            elif bull_tc.is_bullish_stick_sandwich():
                pattern.append('bullish_stick_sandwich')
        else:
            bear_tc = BearishTripleCandlestick(child_df)
            if bear_tc.has_pattern():
                pattern.append('')
        #
        if not len(pattern):
            """" Couple candlesticks """
            bull_dc = BullishDoubleCandlestick(child_df)
            if bull_dc.has_pattern():
                if bull_dc.is_bullish_engulfing():
                    pattern.append('bullish_engulfing')
                elif bull_dc.is_piercing():
                    pattern.append('bullish_piercing')
                elif bull_dc.is_bullish_harami():
                    if bull_dc.is_bullish_harami_cross():
                        pattern.append('bullish_harami_cross')
                    else:
                        pattern.append('bullish_harami')
                elif bull_dc.is_bullish_meeting_line():
                    pattern.append('bullish_meeting_line')
                elif bull_dc.is_bullish_tasuki_line():
                    pattern.append('bullish_tasuki_line')
                elif bull_dc.is_matching_low():
                    pattern.append('bullish_matching_low')
                elif bull_dc.is_tweezers_bottom():
                    pattern.append('bullish_tweezers_bottom')
            else:
                bear_dc = BearishDoubleCandlestick(child_df)
                if bear_dc.has_pattern():
                    if bear_dc.is_bearish_engulfing():
                        pattern.append('bearish_engulfing')
                    elif bear_dc.is_dark_cloud_cover():
                        pattern.append('bearish_dark_cloud_cover')
                    elif bear_dc.is_bearish_harami():
                        if bear_dc.is_bearish_harami_cross():
                            pattern.append('bearish_harami_cross')
                        else:
                            pattern.append('bearish_harami')
                    elif bear_dc.is_bearish_meeting_line():
                        pattern.append('bearish_meeting_line')
                    elif bear_dc.is_bearish_tasuki_line():
                        pattern.append('bearish_tasuki_line')
                    elif bear_dc.is_matching_high():
                        pattern.append('bearish_matching_low')
                    elif bear_dc.is_tweezers_top():
                        pattern.append('bearish_tweezers_top')
            #
        #
        return pattern

    @staticmethod
    def get_continuation_cs_pattern(child_df):
        pattern = []
        if is_bullish_gap(child_df):
            pattern.append('bullish_gap')
        elif is_bearish_gap(child_df):
            pattern.append('bearish_gap')
        #
        if is_bullish_neck(child_df):
            pattern.append('bullish_neck')
        elif is_bearish_neck(child_df):
            pattern.append('bearish_neck')
        #
        if is_fair_value_rising_gap(child_df):
            pattern.append('fair_value_rising_gap')
        elif is_fair_value_falling_gap(child_df):
            pattern.append('fair_value_falling_gap')
        #
        if is_bullish_separating_line(child_df):
            pattern.append('bullish_separating_line')
        elif is_bearish_separating_line(child_df):
            pattern.append('bearish_separating_line')
        #
        if is_rising_three(child_df):
            pattern.append('rising_three')
        elif is_falling_three(child_df):
            pattern.append('falling_three')
        #
        if is_rising_n(child_df):
            pattern.append('rising_n')
        elif is_falling_n(child_df):
            pattern.append('falling_n')
        #
        return pattern

    def get_full_candlestick_pattern(self, child_df):
        pattern = []
        cont_patterns = self.get_continuation_cs_pattern(child_df)
        reversal_patterns = self.get_reversal_cs_pattern(child_df)
        if len(cont_patterns) or len(reversal_patterns):
            return cont_patterns + reversal_patterns
        return pattern

    @staticmethod
    def get_supported_patterns():
        return ALLOWED_PATTERNS

    @staticmethod
    def get_candlestick(r):
        if r['Low'] == r['High']:
            return ''
        if r['oc_dif'] == 0:
            return DOJI_CS
        if (r['Open'] == r['High'] and r['Close'] == r['Low']) or (r['Open'] == r['Low'] and r['Close'] == r['High']):
            return MARUBOZU_CS
        if r['upper_wick'] == 0 and r['tail'] > 2.4 * r['body']:
            return HAMMER_CS
        if r['tail'] == 0 and r['upper_wick'] > 2.4 * r['body']:
            return INVERTED_HAMMER_CS
        if r['upper_wick'] <= 0.2 and r['color'] == WHITE_CS and r['tail'] > 2.4 * r['body']:
            return HANGING_MAN_CS
        if r['tail'] <= 0.2 and r['color'] == BLACK_CS and r['upper_wick'] > 2.4 * r['body']:
            return SHOOTING_STAR_CS
        if r['tail'] > r['body'] > 0.4 and r['upper_wick'] > r['body']:
            return SPINNING_TOP_CS
        return ''

    def __validate(self, pattern_name):
        if pattern_name not in ALLOWED_PATTERNS:
            print(f"The pattern {pattern_name} is not recognized.")
            exit()
        if (pattern_name == GET_FULL and len(self.added_patterns))  or GET_FULL in self.added_patterns:
            print(f"You can not add {GET_FULL} if you added some others. Just use only {GET_FULL}.")
            exit()
        if (pattern_name == GET_REVERSAL or pattern_name == GET_CONTINUE or pattern_name == GET_FULL) and \
            (GET_REVERSAL in self.added_patterns or GET_CONTINUE in self.added_patterns or
             GET_FULL in self.added_patterns):
            print(f"You can not add {GET_REVERSAL} & {GET_CONTINUE} & {GET_FULL} together. Just use {GET_FULL} instead.")
            exit()
