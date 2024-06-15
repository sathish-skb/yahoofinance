import yfinance as yf
import pandas as pd
import numpy as np
import ta

def fetch_stock_data(ticker, interval, period):
    """Fetch historical stock data from Yahoo Finance."""
    return yf.download(tickers=ticker, interval=interval, period=period)

def compute_moving_averages(data):
    """Compute Simple Moving Averages."""
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()
    return data

def compute_parabolic_sar(data):
    """Compute Parabolic SAR."""
    data['PSAR'] = ta.trend.PSARIndicator(
        high=data['High'], low=data['Low'], close=data['Close'], step=0.02, max_step=0.2
    ).psar()
    return data

def compute_donchian_channels(data):
    """Compute Donchian Channels."""
    data['Donchian_High'] = data['High'].rolling(window=20).max()
    data['Donchian_Low'] = data['Low'].rolling(window=20).min()
    return data

def generate_signals(data):
    """Generate buy/sell signals based on trend-following strategy."""
    buy_signal = (
        (data['Close'] > data['SMA50']) &
        (data['SMA50'] > data['SMA200']) &
        (data['Close'] > data['Donchian_High'])
    )
    data.loc[buy_signal, 'Signal'] = 1

    sell_signal = (
        (data['Close'] < data['SMA50']) &
        (data['Close'] < data['Donchian_Low'])
    )
    data.loc[sell_signal, 'Signal'] = -1

    return data

def execute_trades(data, ticker, qty):
    """Simulate buy/sell orders based on signals."""
    for index, row in data.iterrows():
        if row.get('Signal') == 1:
            print(f"Buy {qty} shares of {ticker} at {row['Close']} on {index}")
        elif row.get('Signal') == -1:
            print(f"Sell {qty} shares of {ticker} at {row['Close']} on {index}")

def backtest_strategy(ticker, interval, period, qty):
    """Backtest the trend-following strategy."""
    data = fetch_stock_data(ticker, interval, period)
    data = compute_moving_averages(data)
    data = compute_parabolic_sar(data)
    data = compute_donchian_channels(data)
    data = generate_signals(data)
    execute_trades(data, ticker, qty)

# Parameters
ticker = "AAPL"
interval = "1d"
period = "1y"
qty = 100

# Run backtest
backtest_strategy(ticker, interval, period, qty)
