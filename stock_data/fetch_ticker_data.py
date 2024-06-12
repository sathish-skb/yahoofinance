import yfinance as yf


def fetch_and_compute_indicators(ticker, interval, period):

    stock_data = yf.Ticker(ticker).history(period=period, interval=interval)

    stock_data["EMA9"] = stock_data["Close"].ewm(span=9, adjust=False).mean()
    stock_data["EMA12"] = stock_data["Close"].ewm(span=12, adjust=False).mean()
    stock_data["EMA26"] = stock_data["Close"].ewm(span=26, adjust=False).mean()

    stock_data["MACD"] = stock_data["EMA12"] - stock_data["EMA26"]
    stock_data["Signal_Line"] = stock_data["MACD"].ewm(span=9, adjust=False).mean()

    return stock_data
