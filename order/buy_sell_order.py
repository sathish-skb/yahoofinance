from utils.beep_sound import beep_sound

def buy_sell_stocks(data, ticker, qty):
    """
    Simulates buying and selling stocks based on buy/sell signals in the 'Signal' column.
    """

    data["Buy Price"] = None
    data["Sell Price"] = None
    data["Profit"] = 0.0
    current_holding = 0
    buy_price = 0
    total_profit = 0.0
    trade = {}
    trades = []

    for index, row in data.iterrows():
        signal = row["Signal"]
        close_price = row["Close"]
        if total_profit > 10000.0:
            break

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

        elif signal == -1 and current_holding > 0:  # Sell signal and holding shares
            data.loc[index, "Sell Price"] = close_price
            profit = (close_price - buy_price) * current_holding
            data.loc[index, "Profit"] = profit
            total_profit += profit
            print(
                f"{index} SELL {ticker} {current_holding} shares at ${close_price:.2f} on Profit: ${profit:.2f}"
            )
            trade["Action"] = "SELL"
            trade["Quantity"] = qty
            trade["Price"] = close_price
            trade["Profit"] = profit
            trades.append(trade)
            current_holding = 0
        else:  # No action (hold or no signal)
            pass  # No change in holdings or prices

    print("Total Profit", total_profit)
    return data
