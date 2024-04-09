import pandas as pd
from fetch_sp500_tickers import fetch_sp500_tickers
from FinInfo import perform_analysis
from sp500database import initialize_db, insert_or_update_stock_data
from FinInfo import perform_analysis, initialize_db, insert_or_update_stock_data


def main():
    # Initialize database
    db_name = 'sp500database.db'
    initialize_db(db_name)
    
    # Fetch S&P 500 tickers
    tickers = fetch_sp500_tickers()
    print(f"Fetched {len(tickers)} tickers.")
    
    # Analyze each ticker and save the results
    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        try:
            analysis_result = perform_analysis(ticker)
            insert_or_update_stock_data(db_name, analysis_result)
            print(f"Analysis for {ticker} saved successfully.")
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
    
    print("Finished analyzing all tickers.")

if __name__ == "__main__":
    main()
