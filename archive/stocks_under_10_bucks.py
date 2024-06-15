

import yfinance as yf

def get_us_stocks_under_10():
    price_threshold = 10.0
    
    tickers = ['KITT']

    stocks_under_10 = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        stock_info = stock.history(period="1d")
        
        if not stock_info.empty:
            latest_price = stock_info['Close'].iloc[-1]
            if latest_price < price_threshold:
                stocks_under_10.append(ticker)

    return stocks_under_10


stocks_under_10 = get_us_stocks_under_10()
print("US Stocks priced under $10:", stocks_under_10)
