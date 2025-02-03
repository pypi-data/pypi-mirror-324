import pandas as pd
import yfinance as yf
def get_constituents_and_concat():
    sp500 = 'https://yfiua.github.io/index-constituents/constituents-sp500.csv'

    sp500 = pd.read_csv(sp500)
    sp500 = sp500.sort_values("Symbol", ascending=True)
    sp500_constituents = sp500['Symbol'].to_list()
    sp500_constituents = [x.replace(".","-") for x in sp500_constituents]

    return sp500_constituents

def get_ohlc(symbols, start_date, end_date):
    data = {}
    for symbol in symbols:
        print(symbol)
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        data[symbol] = df[['Close']]
    
    # Combine the data into a single DataFrame with multi-level columns
    combined_df = pd.concat(data, axis=1)
    return combined_df