
import time

from order.buy_sell_order import buy_sell_stocks
from stock_data.fetch_ticker_data import fetch_and_compute_indicators
from utils.beep_sound import beep_sound

tickers = "KITT"
interval = "1m"
period = "1d"
qty = 500


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
    buy_price = 0.10
    target_price = set_price(buy_price, 1.2)
    stoploss_price = set_price(buy_price, 0.8)    
    
    while True:
        
        data = fetch_and_compute_indicators(tickers, interval, period)        
        # Getting Most recent Record
        data_with_signals = generate_signals(data, stoploss_price).tail(1)
        
        close_price = data_with_signals["Close"].values[0]
        
        print(f"Buy: ${buy_price} | target: ${target_price:.3f} | Stoploss: ${stoploss_price:.3f} |  current_price: ${close_price:.3f} |")
        
        if close_price >= target_price:
            target_price = set_price(target_price, 1.1) # step 10 % if current_market_price reaches target
            stoploss_price = target_price # stoploss replaced with up most recent 
        
        
        # STOP the process if stop loss triggered
        if data_with_signals["Signal"].values[0] == -1:
            beep_sound()
            print("-----------------------ALERT------------------------------")
            print(f"STOP LOSS TRIGGERED: SELL THE STOCKS at: ${stoploss_price:.3f}")
            print(f"Profit: {(stoploss_price - buy_price) / buy_price * 100:.2f}%")
            print("------------------------END-------------------------------")
            break
        
        # monitors stock_prce every 5 secs
        time.sleep(5)

back_test(tickers, interval)
