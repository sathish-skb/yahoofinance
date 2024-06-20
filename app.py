
import time
import robin_stocks.robinhood as r
import os 

from order.buy_sell_order import buy_sell_stocks
from stock_data.fetch_ticker_data import fetch_and_compute_indicators
from utils.beep_sound import beep_sound

tickers = "MBIO"
interval = "1m"
period = "1d"
buy_price = 0

username = ""
password = os.environ.get("robinhood_password")


# Log in to your account
r.login(username, password,expiresIn=86400, scope='internal', by_sms=True, store_session=True)

active_stocks = r.account.get_open_stock_positions(account_number=None, info=None)
for position in active_stocks:
    stock_symbol = position['symbol']
    if stock_symbol == tickers:
        buy_price = position['average_buy_price']
        stock_info = r.stocks.get_quotes(stock_symbol)
        current_price =  stock_info[0]['last_trade_price']
r.logout()

def generate_signals(stock_data, stoploss_price):
    stock_data["declining"] = (stock_data["macd_histogram"].shift(1) > stock_data["macd_histogram"])
    stock_data["inclining"] = (stock_data["macd_histogram"].shift(1) < stock_data["macd_histogram"])
    buy_signal =  (stock_data['Low'] < stock_data['EMA9']) & stock_data["inclining"]
    stock_data.loc[buy_signal, 'Signal'] = "Buy"
    sell_signal = ((stock_data['High'] > stock_data['EMA9']) & stock_data["declining"]) | (stoploss_price >= stock_data['Close'])
    stock_data.loc[sell_signal, 'Signal'] = "Sell"
    return stock_data

def set_price(price, value):
    target_price = float(price) * value
    return target_price

def buy_sell(tickers, interval, buy_price):
    target_price = set_price(buy_price, 1.2)
    stoploss_price = set_price(buy_price, 0.8) 
    data = fetch_and_compute_indicators(tickers, interval, period)
    data_with_signals = generate_signals(data, stoploss_price)
    buy_sell_stocks(data_with_signals, tickers, target_price, stoploss_price) 
     
def back_test(tickers, interval, buy_price):
    target_price = set_price(buy_price, 1.2)
    stoploss_price = set_price(buy_price, 0.8)    
        
    while True:
        
        data = fetch_and_compute_indicators(tickers, interval, period)        
        # Getting Most recent Record
        data_with_signals = generate_signals(data, stoploss_price).tail(1)        
        close_price = data_with_signals["Close"].values[0]        
        if buy_price != 0:
            print(f"Buy: ${buy_price} | target: ${target_price:.3f} | Stoploss: ${stoploss_price:.3f} |  current_price: ${close_price:.3f} |")
        else:
            # print(data_with_signals.tail(100))
            high_price = data_with_signals["High"].values[0]
            low_price = data_with_signals["Low"].values[0]
            EMA9 = data_with_signals["EMA9"].values[0]
            macd_histogram = data_with_signals["macd_histogram"].values[0]
            declining = data_with_signals["declining"].values[0]
            inclining = data_with_signals["inclining"].values[0]
            Signal = data_with_signals["Signal"].values[0]
            print(f"High: ${high_price:.3f} | Low: ${low_price:.3f} | EMA9: ${EMA9:.3f} | macd_histogram: ${macd_histogram:.3f} | declining: {declining} | inclining: {inclining} | Signal: {Signal}")
                
        if close_price >= target_price:
            target_price = set_price(target_price, 1.1) # step 10 % if current_market_price reaches target
            stoploss_price = target_price # stoploss replaced with up most recent 
        

        if data_with_signals["Signal"].values[0] == "Buy":
            beep_sound()
                    
        # STOP the process if stop loss triggered
        if data_with_signals["Signal"].values[0] == "Sell" and buy_price != 0:
            beep_sound()
            print("-----------------------ALERT------------------------------")
            print(f"STOP LOSS TRIGGERED: SELL THE STOCKS at: ${stoploss_price:.3f}")
            print(f"Profit: {(stoploss_price - buy_price) / buy_price * 100:.2f}%")
            print("------------------------END-------------------------------")
            break
        
        # monitors stock_prce every 5 secs
        time.sleep(5)

# back_test(tickers, interval, buy_price)
buy_sell(tickers, interval, buy_price)


    

