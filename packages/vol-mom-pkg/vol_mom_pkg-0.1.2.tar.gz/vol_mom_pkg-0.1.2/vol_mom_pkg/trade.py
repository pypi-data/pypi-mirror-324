from alpaca_trade_api.rest import REST, TimeFrame
from vol_mom_pkg.signals import calculate_portfolios
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
# Load API keys from environment variables
ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
ALPACA_API_SECRET = os.getenv("APCA_API_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("APCA_API_BASE_URL", "https://paper-api.alpaca.markets")

# Initialize Alpaca API client
api = REST(ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_BASE_URL)

def get_account_info():
    account = api.get_account()
    return float(account.equity)  # Equivalent to Net Liquidation

def place_orders(df, trade_direction):
    def place_market_order(symbol, allocation, direction):
        # Fetch the previous close price using get_bars
        bars = api.get_bars(symbol, TimeFrame.Day, limit=5).df
        
        if bars.empty:
            print(f"Unable to fetch historical data for {symbol}. Skipping...")
            return

        previous_close = bars.iloc[-1].close

        # Calculate the number of shares to trade
        quantity = int(allocation // previous_close)
        if quantity <= 0:
            print(f"Allocation too small for {symbol} at price {previous_close}. Skipping...")
            return

        side = "buy" if direction == "long" else "sell"

        # Submit the order
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side=side,
            type="market",
            time_in_force="gtc"
        )
        print(f"Placed {side.upper()} order for {quantity} shares of {symbol}.")

    for _, row in df.iterrows():
        try:
            place_market_order(row["Symbol"], row["Dollar Allocation"], trade_direction)
        except Exception as e:
            print(f"Error placing order for {row['Symbol']}: {e}")


def send_weekly_basket():
    pf = get_account_info()
    lookback = 12
    winners_from_low_vol, losers_from_high_vol, low_vol_from_winners, high_vol_from_losers = calculate_portfolios(lookback, pf)
    place_orders(losers_from_high_vol, 'long')