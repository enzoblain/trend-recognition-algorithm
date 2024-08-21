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
    TOTAL_CANDLES = len(df)
    MISSING_PROPORTION = MISSING_INFORMATION / TOTAL_CANDLES
    MAX_MISSING_PROPORTION = 0.2

    if MISSING_PROPORTION > MAX_MISSING_PROPORTION:
        BOX_WIDTH = 100
        PADDING = 2

        WARN_TEXT = "WARNING"
        WARN_LENGTH = len(WARN_TEXT)
        WARN_PADDING = (BOX_WIDTH - WARN_LENGTH) // 2

        print(f"+{'-' * WARN_PADDING + WARN_TEXT + '-' * (WARN_PADDING - 1)}+")
        print(f'| {"There is a significant amount of missing data in the DataFrame.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f'| {f"{MISSING_INFORMATION} out of {TOTAL_CANDLES} candles contain missing values.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f'| {f"This represents approximately {MISSING_PROPORTION:.2%} of the data.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f'| {"This may affect the accuracy of the analysis, as not all data is available.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f"+{'-' * WARN_PADDING + WARN_TEXT + '-' * (WARN_PADDING - 1)}+\n")
        
    df.dropna(inplace=True)
    df = df.reset_index(drop=True)

    TOTAL_CANDLES = len(df)

    if TOTAL_CANDLES < 20:
        BOX_WIDTH = 100
        PADDING = 2

        WARN_TEXT = "WARNING"
        WARN_LENGTH = len(WARN_TEXT)
        WARN_PADDING = (BOX_WIDTH - WARN_LENGTH) // 2

        print(f"+{'-' * WARN_PADDING + WARN_TEXT + '-' * (WARN_PADDING - 1)}+")
        print(f'| {"The dataset does not contain enough valid data points.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f'| {f"Fewer than 20 correct candles ({TOTAL_CANDLES}) are available after handling missing values.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f'| {"This may impact the reliability of the analysis due to the limited dataset size.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f'| {"Please ensure that you have at least 20 valid data points to proceed with accurate analysis.".ljust(BOX_WIDTH - 2 * PADDING)} |')
        print(f"+{'-' * WARN_PADDING + WARN_TEXT + '-' * (WARN_PADDING - 1)}+\n")

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

        if current_trend['type'] == candle['type'] or not candle['type']:
            if current_trend['type'] == 'bullish':
                sign = -1
                compare = 'high'
            else:
                sign = 1
                compare = 'low'
        else:
            compare = 'retest'
            if current_trend['type'] == 'bullish':
                sign = 1
            else:
                sign = -1

        result = (sign * current_trend[compare]) > (sign * candle['close'])

        print(result)

    return TRENDS

""""
Garder dans une variable dès qu'on cange de sens pour la bougie
si on repasse au dessus alors on annule (dans le cas d'un bullish)
et on marque un nouveau retest
sinon on continue jusqu'à ce qu'on dépasse (dans le cas d'un bullish)

si on clotûre en dessous du low tu retest on change de trend et on reset la variable (dans le cas d'un bearish)
"""

# POSSIBILITIES
# expend   trend : bullish            || bearish
# bullish          high < close       || Nan
# bearish          Nan                || low > close

# switch   trend : bullish            || bearish
# bullish          Nan                || retest < close
# bearish          retest > close     || Nan





# continue trend : bullish            || bearish
# bullish          high > close       || Nan
# bearish          Nan                || Nan 

# invert   trend : bullish            || bearish
# bullish          Nan                || retest > close
# bearish          retest < close     || Nan