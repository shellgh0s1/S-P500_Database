import sqlite3

def initialize_db(db_name='sp500database.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
            id INTEGER PRIMARY KEY,
            ticker TEXT UNIQUE,
            name TEXT,
            sector TEXT,
            pe_ratio REAL,
            forward_eps REAL,
            beta REAL,
            roe REAL,
            roa REAL,
            operating_margin REAL,
            debt_to_equity REAL,
            price_to_sales REAL,
            eps_growth REAL,
            dividend_yield REAL,
            price_to_book REAL,
            free_cash_flow REAL,
            analysis_date DATE DEFAULT CURRENT_DATE,
            sentiment TEXT,
            moving_averages TEXT  -- This could be a JSON string or separate table
        )
    ''')
    conn.commit()
    conn.close()

def insert_or_update_stock_data(db_name, stock_data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Convert moving averages dictionary to a string for storage; consider JSON for more complex data
    moving_averages_str = str(stock_data.get('Technical Analysis', {}))
    
    cursor.execute('''
        INSERT INTO stock_data(ticker, name, sector, pe_ratio, forward_eps, beta, roe, roa, 
                               operating_margin, debt_to_equity, price_to_sales, eps_growth, 
                               dividend_yield, price_to_book, free_cash_flow, sentiment, moving_averages)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(ticker) DO UPDATE SET
            name=excluded.name,
            sector=excluded.sector,
            pe_ratio=excluded.pe_ratio,
            forward_eps=excluded.forward_eps,
            beta=excluded.beta,
            roe=excluded.roe,
            roa=excluded.roa,
            operating_margin=excluded.operating_margin,
            debt_to_equity=excluded.debt_to_equity,
            price_to_sales=excluded.price_to_sales,
            eps_growth=excluded.eps_growth,
            dividend_yield=excluded.dividend_yield,
            price_to_book=excluded.price_to_book,
            free_cash_flow=excluded.free_cash_flow,
            sentiment=excluded.sentiment,
            moving_averages=excluded.moving_averages
    ''', (
        stock_data['Ticker'],
        stock_data.get('Fundamentals', {}).get('Name'),
        stock_data.get('Fundamentals', {}).get('Sector'),
        stock_data.get('Fundamentals', {}).get('PE Ratio'),
        stock_data.get('Fundamentals', {}).get('Forward EPS'),
        stock_data.get('Additional Metrics', {}).get('Beta'),
        stock_data.get('Additional Metrics', {}).get('ROE'),
        stock_data.get('Additional Metrics', {}).get('ROA'),
        stock_data.get('Additional Metrics', {}).get('Operating Margin'),
        stock_data.get('Additional Metrics', {}).get('Debt to Equity'),
        stock_data.get('Additional Metrics', {}).get('Price to Sales'),
        stock_data.get('Additional Metrics', {}).get('EPS Growth'),
        stock_data.get('Additional Metrics', {}).get('Dividend Yield'),
        stock_data.get('Additional Metrics', {}).get('Price to Book'),
        stock_data.get('Additional Metrics', {}).get('Free Cash Flow'),
        stock_data.get('Sentiment'),
        moving_averages_str
    ))
    
    conn.commit()
    conn.close()
