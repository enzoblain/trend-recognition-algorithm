import pandas as pd
import numpy as np

def trend_recognition(df):
    if isinstance(df, dict):
        df = pd.DataFrame(df)
    elif not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected input to be of type 'DataFrame' or 'dict', but got '{type(df).__name__}' instead.")

    REQUIRED_COLUMNS = ['datetime', 'high', 'open', 'close', 'low']
    MISSING_COLUMNS = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if MISSING_COLUMNS:
        raise ValueError(f"Missing columns: {', '.join(MISSING_COLUMNS)}")
    
    df = df[REQUIRED_COLUMNS]

    if df.isna().any().sum() > 0:
        df.dropna(inplace=True)

    df.reset_index(drop=True, inplace=True)

    if len(df) < 20:
        print("WARNING: Fewer than 20 valid candles available after handling missing values. Analysis may be unreliable.")
        return []

    df['type'] = np.where(df['open'].values < df['close'].values, 'Bullish', 'Bearish')

    first_candle = df.iloc[0]
    current_trend = {
        'type': first_candle['type'],
        'high': first_candle['high'],
        'low': first_candle['low'],
        'retest': first_candle['low'] if first_candle['type'] == 'Bullish' else first_candle['high'],
        'start': first_candle['datetime'],
        'end': None
    }

    sub_trend = {'type': None, 'high': None, 'low': None, 'retest': None, 'start': None}
    TRENDS = []
    THRESHOLD = 0.005

    for candle in df.itertuples(index=False):
        if current_trend['type'] == candle.type:
            if not sub_trend['start']:
                if current_trend['type'] == 'Bullish':
                    current_trend['high'] = max(candle.high, current_trend['high'])
                else:
                    current_trend['low'] = min(candle.low, current_trend['low'])
            else:
                if (current_trend['type'] == 'Bullish' and candle.close > current_trend['high'] and (candle.high - current_trend['high']) > THRESHOLD):
                    current_trend['high'] = candle.high
                    current_trend['retest'] = sub_trend['retest']
                    sub_trend = {'type': None, 'high': None, 'low': None, 'retest': None, 'start': None}
                elif (current_trend['type'] == 'Bearish' and candle.close < current_trend['low'] and (current_trend['low'] - candle.low) > THRESHOLD):
                    current_trend['low'] = candle.low
                    current_trend['retest'] = sub_trend['retest']
                    sub_trend = {'type': None, 'high': None, 'low': None, 'retest': None, 'start': None}
                else:
                    sub_trend['high'] = max(candle.high, sub_trend['high'])
                    sub_trend['low'] = min(candle.low, sub_trend['low'])
        else:
            if sub_trend['start'] is None:
                sub_trend = {
                    'type': candle.type,
                    'high': candle.high,
                    'low': candle.low,
                    'retest': max(candle.high, current_trend['high']) if candle.type == 'Bearish' else min(candle.low, current_trend['low']),
                    'start': candle.datetime
                }
            else:
                if (current_trend['type'] == 'Bullish' and candle.close < sub_trend['retest'] and (sub_trend['retest'] - candle.close) > THRESHOLD) or \
                   (current_trend['type'] == 'Bearish' and candle.close > sub_trend['retest'] and (candle.close - sub_trend['retest']) > THRESHOLD):
                    current_trend['end'] = candle.datetime
                    TRENDS.append(current_trend)
                    current_trend = {
                        'type': candle.type,
                        'high': max(candle.high, sub_trend['high']),
                        'low': min(candle.low, sub_trend['low']),
                        'retest': candle.low if candle.type == 'Bullish' else candle.high,
                        'start': candle.datetime,
                        'end': None
                    }
                    sub_trend = {'type': None, 'high': None, 'low': None, 'retest': None, 'start': None}
                else:
                    sub_trend['high'] = max(candle.high, sub_trend['high'])
                    sub_trend['low'] = min(candle.low, sub_trend['low'])

    if current_trend['end'] is None:
        current_trend['end'] = df.iloc[-1]['datetime']
        TRENDS.append(current_trend)
    
    return TRENDS