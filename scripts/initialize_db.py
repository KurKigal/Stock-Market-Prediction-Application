import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.database_manager import DatabaseManager
import pandas as pd
from datetime import datetime, timedelta
import yfinance as tf

def generate_sample_data(symbol, days=60):
    """Generate sample stock data if we can't download it"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    
    # Start with a base price and generate random walk
    base_price = 100
    daily_returns = pd.Series(np.random.normal(0.0005, 0.015, size=len(dates)))
    cumulative_returns = daily_returns.cumsum()
    prices = base_price * (1 + cumulative_returns)
    
    df = pd.DataFrame({
        'date': dates.strftime('%Y-%m-%d'),
        'open': prices * np.random.uniform(0.99, 1.01, size=len(dates)),
        'high': prices * np.random.uniform(1.01, 1.03, size=len(dates)),
        'low': prices * np.random.uniform(0.97, 0.99, size=len(dates)),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, size=len(dates))
    })
    
    df['symbol'] = symbol
    return df

def download_stock_data(symbol, days=60):
    """Download historical stock data from Yahoo Finance"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        ticker = tf.Ticker(symbol)
        data = ticker.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        
        if data.empty:
            print(f"No data found for {symbol}, generating sample data")
            return generate_sample_data(symbol, days)
        
        df = data.reset_index()
        df.columns = [col.lower() for col in df.columns]
        df = df.rename(columns={'index': 'date', 'stock splits': 'splits'})
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        df['symbol'] = symbol
        return df
    except Exception as e:
        print(f"Error downloading data for {symbol}: {e}")
        return generate_sample_data(symbol, days)

def initialize_database():
    print("Initializing database...")
    db_manager = DatabaseManager('data/stock_data.db')
    
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    for symbol in symbols:
        print(f"Loading data for {symbol}...")
        
        # Try to download data, fall back to generated data
        try:
            stock_data = download_stock_data(symbol, days=365)
        except:
            print(f"Falling back to generated data for {symbol}")
            stock_data = generate_sample_data(symbol, days=365)
            
        db_manager.insert_stock_data(stock_data, symbol)
        print(f"Added {len(stock_data)} records for {symbol}")
    
    db_manager.close()
    print("Database initialization complete!")

if __name__ == "__main__":
    initialize_database()