import yfinance as yf
import pandas as pd
import numpy as np
from sp500database import initialize_db, insert_or_update_stock_data

# Fetch historical P/E ratios and resample yearly prices
def fetch_pe_ratios(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5y")
        yearly_prices = hist['Close'].resample('YE').mean()
        pe_ratios = stock.info.get('trailingPE', np.nan)
        return yearly_prices, pe_ratios
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.Series(dtype=float), np.nan


# Calculate forward fair value based on forward EPS and target P/E ratio
def calculate_forward_fair_value(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        forward_eps = info.get('forwardEps', np.nan)
        target_pe_ratio = info.get('trailingPE', np.nan)
        
        if not np.isnan(forward_eps) and not np.isnan(target_pe_ratio):
            fair_value_per_share = forward_eps * target_pe_ratio
        else:
            fair_value_per_share = np.nan
        return fair_value_per_share
    except Exception as e:
        print(f"Error calculating forward fair value for {ticker}: {e}")
        return np.nan

# Placeholder for sentiment analysis
def analyze_sentiment(ticker_symbol):
    sentiment_score = "Neutral"  # Placeholder
    return sentiment_score

# Placeholder for portfolio optimization
def optimize_portfolio(tickers):
    optimized_allocation = {}  # Placeholder
    return optimized_allocation

# Calculate moving averages
def calculate_moving_averages(ticker_symbol, periods=[50, 200]):
    data = yf.download(ticker_symbol, period="1y")
    moving_averages = {}
    for period in periods:
        ma = data['Close'].rolling(window=period).mean()
        moving_averages[f'{period}-day MA'] = ma.iloc[-1]
    return moving_averages

# Perform comprehensive stock analysis
def perform_analysis(ticker_symbol):
    print("Fetching Fundamentals...")
    fundamentals = fetch_fundamentals(ticker_symbol)
    
    print("Fetching Additional Metrics...")
    additional_metrics = fetch_additional_metrics(ticker_symbol)  # Fetching additional metrics

    print("Calculating Technical Indicators...")
    moving_averages = calculate_moving_averages(ticker_symbol)
    
    print("Analyzing Sentiment...")
    sentiment = analyze_sentiment(ticker_symbol)
    
    print("Analyzing Stock Value...")
    yearly_prices, _ = fetch_pe_ratios(ticker_symbol)
    current_price = yearly_prices.iloc[-1] if not yearly_prices.empty else np.nan
    forward_fair_value = calculate_forward_fair_value(ticker_symbol)
    
    formatted_current_price = "{:.2f}".format(current_price) if not np.isnan(current_price) else "N/A"
    formatted_forward_fair_value = "{:.2f}".format(forward_fair_value) if not np.isnan(forward_fair_value) else "N/A"
    
    below_fair_value = "N/A"
    above_fair_value = "N/A"
    if not np.isnan(current_price) and not np.isnan(forward_fair_value):
        below_fair_value = current_price < forward_fair_value
        above_fair_value = current_price > forward_fair_value
    
    stock_value_analysis = {
        'Current Price': formatted_current_price,
        'Forward Fair Value': formatted_forward_fair_value,
        'Below Fair Value': below_fair_value,
        'Above Fair Value': above_fair_value,
    }
    
    # Integrating the additional metrics into the final analysis dictionary
    analysis = {
        'Ticker': ticker_symbol,
        'Fundamentals': fundamentals,
        'Additional Metrics': additional_metrics,  # Adding the additional metrics to the analysis
        'Technical Analysis': moving_averages,
        'Sentiment': sentiment,
        'Stock Value Analysis': stock_value_analysis
    }
    
    return analysis
# Function to fetch fundamentals (part of perform_analysis but needs definition)
def fetch_fundamentals(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    fundamentals = {
        'Market Cap': info.get('marketCap'),
        'PE Ratio': info.get('trailingPE'),
        'EPS': info.get('trailingEps'),
        # Additional fundamental metrics can be added here
    }
    return fundamentals
def fetch_additional_metrics(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    additional_metrics = {
        'ROE': info.get('returnOnEquity'),
        'ROA': info.get('returnOnAssets'),
        'Operating Margin': info.get('operatingMargins'),
        'Debt to Equity': info.get('debtToEquity'),
        'Price to Sales': info.get('priceToSalesTrailing12Months'),
        'EPS Growth': info.get('earningsGrowth'),
        'Dividend Yield': info.get('dividendYield'),
        'Price to Book': info.get('priceToBook'),
        'Free Cash Flow': info.get('freeCashflow'),
        'Beta': info.get('beta')
    }

    # Formatting values for readability (optional)
    for key, value in additional_metrics.items():
        if value is not None:
            # Convert ratios to percentage, etc.
            if "Yield" in key or "Margin" in key or "ROE" in key or "ROA" in key:
                additional_metrics[key] = f"{value * 100:.2f}%"
            else:
                additional_metrics[key] = f"{value:.2f}"
        else:
            additional_metrics[key] = "N/A"
    
    return additional_metrics

