
import time
import robin_stocks.robinhood as r
import os 

from order.buy_sell_order import buy_sell_stocks
from stock_data.fetch_ticker_data import fetch_and_compute_indicators
from utils.beep_sound import beep_sound

tickers = "KITT"
interval = "1m"
period = "1d"
buy_price = 0.11

username = "sathishct2011@gmail.com"
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
    buy_signal =  (stock_data['Low'] > stock_data['EMA9']) & (stock_data['Signal_Line'] < stock_data['MACD'])
    stock_data.loc[buy_signal, 'Signal'] = 1
    sell_signal = ((stock_data['High'] < stock_data['EMA9']) & (stock_data['Signal_Line'] > stock_data['MACD'])) | (stoploss_price >= stock_data['Close'])
    stock_data.loc[sell_signal, 'Signal'] = -1
    return stock_data

def set_price(price, value):
    target_price = price * value
    return target_price
    
def back_test(tickers, interval):
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
            print(data_with_signals.tail(1))
                
        if close_price >= target_price:
            target_price = set_price(target_price, 1.1) # step 10 % if current_market_price reaches target
            stoploss_price = target_price # stoploss replaced with up most recent 
        

        if data_with_signals["Signal"].values[0] == 1:
            beep_sound()
                    
        # STOP the process if stop loss triggered
        if data_with_signals["Signal"].values[0] == -1 and buy_price != 0:
            beep_sound()
            print("-----------------------ALERT------------------------------")
            print(f"STOP LOSS TRIGGERED: SELL THE STOCKS at: ${stoploss_price:.3f}")
            print(f"Profit: {(stoploss_price - buy_price) / buy_price * 100:.2f}%")
            print("------------------------END-------------------------------")
            break
        
        # monitors stock_prce every 5 secs
        time.sleep(5)

back_test(tickers, interval)

