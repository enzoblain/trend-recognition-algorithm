import pandas as pd
import plotly.graph_objects as go
from algorithm.algo import trend_recognition

def show_graph(df):
    TRENDS = trend_recognition(pd.read_csv('data/data_test.csv'))
    fig = go.Figure()
        
    for trend in TRENDS: 
        color = 'green' if trend['type'] == 'Bullish' else 'red'

        fig.add_shape(
            type="rect",
            x0=trend['start'],
            x1=trend['end'],
            y0=min(df['low']),
            y1=max(df['high']),
            fillcolor=color,
            opacity=0.3,
            layer="below",
            line_width=0,
        )

    fig.add_trace(go.Candlestick(
        x=df['datetime'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Candlestick'
    ))

    fig.update_layout(
        title='Trading Graph',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    fig.show()

show_graph(pd.read_csv('data/data_test.csv'))