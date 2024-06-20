from utils.beep_sound import beep_sound

def set_price(price, value):
    target_price = float(price) * value
    return target_price

def buy_sell_stocks(data, ticker, target_price, stoploss_price):
    """
    Simulates buying and selling stocks based on buy/sell signals in the 'Signal' column.
    """
    current_holding = 0
    total_profit = 0.0
    buy_price = 0
    qty = 5000
    trade = {}
    trades = []
    target_price = 0
    stoploss_price = 0  

    for index, row in data.iterrows():
        signal = row["Signal"]
        close_price = row["Close"]
        if total_profit > 10000.0:
            break

        if close_price >= target_price:
            target_price = set_price(target_price, 1.1) # step 10 % if current_market_price reaches target
            stoploss_price = target_price # stoploss replaced with up most recent 
            
        if signal == 1 and current_holding == 0:  # Buy signal and no current holding
            data.loc[index, "Buy Price"] = close_price
            buy_price = close_price
            current_holding = qty  # Buy 5000 shares
            print(
                f"{index} BUY# {ticker} {current_holding} shares at ${close_price:.2f}"
            )
            trade["Action"] = "BUY"
            trade["Quantity"] = qty
            trade["Price"] = close_price
            trades.append(trade)
            target_price = set_price(buy_price, 1.2)
            stoploss_price = set_price(buy_price, 0.8)    

        elif signal == -1 and current_holding > 0 and (stoploss_price > close_price):  # Sell signal and holding shares
            data.loc[index, "Sell Price"] = close_price
            profit = (close_price - buy_price) * current_holding
            data.loc[index, "Profit"] = profit
            total_profit += profit
            print(f"{index} SELL {ticker} {current_holding} shares at ${close_price:.2f} on Profit: ${profit:.2f}")
            print(f"{index} close_price: ${close_price:.2f} | buy_price: ${buy_price:.2f} | target_price: ${target_price:.2f}  stoploss_price: ${stoploss_price:.2f}")
            trade["Action"] = "SELL"
            trade["Quantity"] = qty
            trade["Price"] = close_price
            trade["Profit"] = profit
            trades.append(trade)
            current_holding = 0
        else:  # No action (hold or no signal)
            pass  # No change in holdings or prices
        
        # if current_holding > 0:
        #     print(f"{index} close_price: ${close_price:.2f}  target_price: ${target_price:.2f}  stoploss_price: ${stoploss_price:.2f}")
              
    print("Total Profit", total_profit)
    return data
