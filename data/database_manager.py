import sqlite3
import pandas as pd
import os

class DatabaseManager:
    def __init__(self, db_path):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
        
    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            date TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            date TEXT NOT NULL,
            predicted_close REAL NOT NULL,
            confidence REAL,
            model_version TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            prediction_date TEXT NOT NULL,
            predicted_value REAL NOT NULL,
            actual_value REAL,
            model_version TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.conn.commit()
        
    def insert_stock_data(self, df, symbol):
        df['symbol'] = symbol
        df.to_sql('stocks', self.conn, if_exists='append', index=False)
        
    def get_historical_data(self, symbol, days=30):
        query = """
        SELECT * FROM stocks 
        WHERE symbol = ? 
        ORDER BY date DESC 
        LIMIT ?
        """
        df = pd.read_sql(query, self.conn, params=(symbol, days))
        # Return data chronologically
        return df.iloc[::-1].reset_index(drop=True)
        
    def close(self):
        self.conn.close()