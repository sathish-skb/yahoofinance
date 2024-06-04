import yfinance as yf
import pandas as pd

# Fetch GOOG stock data with a 1-minute timeframe for 1 day
ticker = "SOBR"
interval = "1m"
period = "1d"

# Function to fetch stock data and compute indicators
def fetch_and_compute_indicators(ticker, interval, period):
    # Fetch stock data
    stock_data = yf.Ticker(ticker).history(period=period, interval=interval)
    
    # Calculate EMAs
    stock_data['EMA9']  = stock_data['Close'].ewm(span=9, adjust=False).mean()
    stock_data['EMA12'] = stock_data['Close'].ewm(span=12, adjust=False).mean()
    stock_data['EMA26'] = stock_data['Close'].ewm(span=26, adjust=False).mean()
    
    # Calculate MACD and Signal Line
    stock_data['MACD'] = stock_data['EMA12'] - stock_data['EMA26']
    stock_data['Signal_Line'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()
    
    return stock_data

# Function to generate buy and sell signals
def generate_signals(stock_data):
    # stock_data['Signal'] = 0  # Default value of 0 (no signal)
    
    # Buy signal
    buy_signal =  (stock_data['Low'] > stock_data['EMA9']) & (stock_data['Signal_Line'] > 0)
    stock_data.loc[buy_signal, 'Signal'] = 1
    # (stock_data['MACD'] > stock_data['Signal_Line']) &
    # # Sell signal
    sell_signal = (stock_data['High'] < stock_data['EMA9']) & (stock_data['Signal_Line'] < 0)
    stock_data.loc[sell_signal, 'Signal'] = -1
    
    return stock_data

# Main execution
data = fetch_and_compute_indicators(ticker, interval, period)
data_with_signals = generate_signals(data)

# Display the first few rows with signals
print(data_with_signals)

# Uncomment the
