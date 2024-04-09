import pandas as pd

def fetch_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_table = pd.read_html(url, attrs={"id": "constituents"})[0]  # Fetch the first table
    sp500_tickers = sp500_table['Symbol'].tolist()  # Extract the tickers column to a list
    return sp500_tickers

