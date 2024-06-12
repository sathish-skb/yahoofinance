
import time

from order.buy_sell_order import buy_sell_stocks
from stock_data.fetch_ticker_data import fetch_and_compute_indicators

# Fetch GOOG stock data with a 1-minute timeframe for 1 day
ticker = "TATACHEM.NS"
interval = "1m"
period = "1d"
qty = 50


def generate_signals(stock_data):
    # buy_signal =  (stock_data['Low'] > stock_data['EMA9']) & (stock_data['Signal_Line'] < stock_data['MACD'])
    # stock_data.loc[buy_signal, 'Signal'] = 1
    # sell_signal = (stock_data['High'] < stock_data['EMA9']) & (stock_data['Signal_Line'] > stock_data['MACD'])
    # stock_data.loc[sell_signal, 'Signal'] = -1

    buy_signal = (stock_data["Low"] > stock_data["EMA9"]) & (
        stock_data["Signal_Line"] < 0.0
    )
    stock_data.loc[buy_signal, "Signal"] = 1
    sell_signal = (stock_data["High"] < stock_data["EMA9"]) & (
        stock_data["Signal_Line"] > 0.0
    )
    stock_data.loc[sell_signal, "Signal"] = -1

    return stock_data


def back_test(ticker, interval, qty):
    data = fetch_and_compute_indicators(ticker, interval, period)
    data_with_signals = generate_signals(data)
    buy_sell_stocks(data_with_signals, ticker, qty)

back_test(ticker, interval, qty)
