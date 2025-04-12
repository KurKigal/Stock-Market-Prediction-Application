import schedule
import time
from datetime import datetime
from scraper.stock_scraper import StockScraper
from data.database_manager import DatabaseManager

def update_stock_data():
    db_manager = DatabaseManager('data/stock_data.db')
    scraper = StockScraper(['AAPL', 'MSFT', 'GOOGL'])
    
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    for symbol in scraper.ticker_symbols:
        data = scraper.fetch_historical_data(symbol, start_date, end_date)
        if data is not None:
            scraper.save_to_database(data, symbol, db_manager)
            
    print(f"Data updated at {datetime.now()}")

def start_scheduler():
    # Run update daily after market close
    schedule.every().day.at("18:00").do(update_stock_data)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_scheduler()