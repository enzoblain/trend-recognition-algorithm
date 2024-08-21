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

    df['type'] = np.where(df['open'] < df['close'], 'Bullish', 'Bearish')

    # Initialisation de la première tendance basée sur la première bougie
    first_candle = df.iloc[0]
    current_trend = {
        'type': first_candle['type'],
        'high': first_candle['high'],
        'low': first_candle['low'],
        'retest': first_candle['low'] if first_candle['type'] == 'Bullish' else first_candle['high'],
        'start': first_candle['datetime'],
        'end': None
    }

    # Initialisation de la sous-tendance
    sub_trend = {'type': None, 'high': None, 'low': None, 'retest': None, 'start': None}

    # Conteneur pour stocker toutes les tendances
    TRENDS = []

    # Seuil pour ignorer les petites fluctuations
    THRESHOLD = 0.002  # Ajustez ce seuil en fonction des caractéristiques de vos données

    for _, candle in df.iterrows():
        if current_trend['type'] == 'Bullish' and candle['type'] == 'Bullish' and not sub_trend['start']:
            current_trend['high'] = max(candle['high'], current_trend['high'])
        elif current_trend['type'] == 'Bearish' and candle['type'] == 'Bearish' and not sub_trend['start']:
            current_trend['low'] = min(candle['low'], current_trend['low'])
        else:
            if not sub_trend['start']:
                sub_trend = {
                    'type': candle['type'],
                    'high': candle['high'],
                    'low': candle['low'],
                    'retest': max(candle['high'], current_trend['high']) if candle['type'] == 'Bearish' else min(candle['low'], current_trend['low']),
                    'start': candle['datetime']
                }
            else:
                if current_trend['type'] == 'Bullish' and candle['type'] == 'Bullish':
                    if candle['close'] > current_trend['high'] and (candle['high'] - current_trend['high']) > THRESHOLD:
                        current_trend['high'] = candle['high']
                        current_trend['retest'] = sub_trend['retest']
                        sub_trend = {'type': None, 'high': None, 'low': None, 'retest': None, 'start': None}
                elif current_trend['type'] == 'Bearish' and candle['type'] == 'Bearish':
                    if candle['close'] < current_trend['low'] and (current_trend['low'] - candle['low']) > THRESHOLD:
                        current_trend['low'] = candle['low']
                        current_trend['retest'] = sub_trend['retest']
                        sub_trend = {'type': None, 'high': None, 'low': None, 'retest': None, 'start': None}
                else:
                    if (current_trend['type'] == 'Bullish' and candle['close'] < sub_trend['retest'] and (sub_trend['retest'] - candle['close']) > THRESHOLD) or \
                    (current_trend['type'] == 'Bearish' and candle['close'] > sub_trend['retest'] and (candle['close'] - sub_trend['retest']) > THRESHOLD):
                        current_trend['end'] = candle['datetime']
                        TRENDS.append(current_trend)
                        current_trend = {
                            'type': candle['type'],
                            'high': max(candle['high'], sub_trend['high']),
                            'low': min(candle['low'], sub_trend['low']),
                            'retest': candle['low'] if candle['type'] == 'Bullish' else candle['high'],
                            'start': candle['datetime'],
                            'end': None
                        }
                        sub_trend = {'type': None, 'high': None, 'low': None, 'retest': None, 'start': None}
                    else:
                        sub_trend['high'] = max(candle['high'], sub_trend['high'])
                        sub_trend['low'] = min(candle['low'], sub_trend['low'])

    # Finaliser la dernière tendance
    if current_trend['end'] is None:
        current_trend['end'] = df.iloc[-1]['datetime']
        TRENDS.append(current_trend)
    
    return TRENDS