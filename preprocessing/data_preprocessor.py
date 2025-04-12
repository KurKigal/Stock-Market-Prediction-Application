import pandas as pd
import numpy as np

class DataPreprocessor:
    def __init__(self):
        pass
        
    def add_technical_indicators(self, df):
        # Create a copy to avoid modifying the original
        df = df.copy()
        
        # Moving averages
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA20'] = df['close'].rolling(window=20).mean()
        
        # Relative Strength Index (RSI)
        delta = df['close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['STD20'] = df['close'].rolling(window=20).std()
        df['upper_band'] = df['MA20'] + (df['STD20'] * 2)
        df['lower_band'] = df['MA20'] - (df['STD20'] * 2)
        
        # MACD
        df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['signal_line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        return df
        
    def normalize_data(self, df):
        # Create a copy to avoid modifying the original
        df = df.copy()
        
        # Min-max scaling
        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'MA5', 'MA20', 'RSI', 'MACD']
        for col in numeric_cols:
            if col in df.columns:
                df[f'{col}_norm'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min() + 1e-8)
        return df
        
    def prepare_for_training(self, df, prediction_window=1):
        # Create a copy to avoid modifying the original
        df = df.copy()
        
        # Create target variable (next day's closing price)
        df['target'] = df['close'].shift(-prediction_window)
        
        # Drop rows with NaN values
        df = df.dropna()
        
        # Create features and target arrays
        features = df.drop(['target', 'date', 'symbol'], axis=1, errors='ignore')
        target = df['target']
        
        return features, targets