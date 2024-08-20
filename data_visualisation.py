import pandas as pd
import plotly.graph_objects as go

def show_graph(df, max_rows=100):
    if max_rows > 150:
        print('You should display a maximum number of 150 candlesticks to maintain good readability in the graph')

    df = df.iloc[-max_rows:]
    df['datetime'] = pd.to_datetime(df['datetime'])

    fig = go.Figure()

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

show_graph(pd.read_csv('data/data_1.csv'))
