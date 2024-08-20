import pandas as pd
import numpy as np

def trend_recognition(df):
    if isinstance(df, dict):
        df = df.DataFrame
    elif not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected input to be of type 'DataFrame' or 'dict', but got '{format(type(df).__name__)}' instead.")

    REQUIRED_COLUMNS = ['datetime', 'high', 'open', 'close', 'low']
    MISSING_COLUMNS = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if MISSING_COLUMNS:
        raise ValueError(f"Missing columns: {', '.join(MISSING_COLUMNS)}")
    
    df = df[REQUIRED_COLUMNS]

    MISSING_INFORMATION = df.isna().any(axis=1).sum()
    TOTAL_candleS = len(df)
    MISSING_PROPORTION = MISSING_INFORMATION / TOTAL_candleS
    MAX_MISSING_PROPORTION = 0.2

    if MISSING_PROPORTION > MAX_MISSING_PROPORTION:
        BOX_WIDTH = 80
        PADDING = 2

        WARN_TEXT = "WARNING"
        WARN_LENGTH = len(WARN_TEXT)
        WARN_PADDING = (BOX_WIDTH - WARN_LENGTH) // 2

        print(f"+{'-' * WARN_PADDING + WARN_TEXT + '-' * (WARN_PADDING - 1)}+")
        print(f'| {"There is a significant amount of missing data in the DataFrame.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f'| {f"{MISSING_INFORMATION} out of {TOTAL_candleS} candles contain missing values.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f'| {f"This represents approximately {MISSING_PROPORTION:.2%} of the data.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f'| {"This may affect the accuracy of the analysis, as not all data is available.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f"+{'-' * WARN_PADDING + WARN_TEXT + '-' * (WARN_PADDING - 1)}+")
        
    df.dropna(inplace=True)
    df = df.reset_index(drop=True)

    df['type'] = np.nan
    df['type'] = df['type'].astype('object')

    for index, candle in df.iterrows():
        if candle['open'] and candle['close']:
            if candle['open'] < candle['close']:
                df.at[index, 'type'] = 'Bullish'
            elif candle['open'] > candle['close']:
                df.at[index, 'type'] = 'Bearish'

    first_candle = df.iloc[0]

    TRENDS = []
    current_trend = {
        'type': first_candle['type'],
        'high' : first_candle['high'],
        'low': first_candle['low'],
        'retest': first_candle['low'] if first_candle['type'] == 'Bullish' else first_candle['high'],
        'start': first_candle['datetime'],
        'end': None
    }

    for index, candle in df.iterrows():
        if pd.isna(candle['type']):
            continue

        sign = 1

        if current_trend['type'] == 'Bearish':
            sign = -sign
        if candle['type'] == 'Bearish':
            sign = -sign

    return TRENDS