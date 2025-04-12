from datetime import datetime
from data.database_manager import DatabaseManager
from preprocessing.data_preprocessor import DataPreprocessor
from models.stock_predictor import StockPredictor

def retrain_models():
    db_manager = DatabaseManager('data/stock_data.db')
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    
    for symbol in symbols:
        print(f"Retraining model for {symbol}...")
        
        # Get data
        data = db_manager.get_historical_data(symbol, days=365)
        
        # Preprocess
        preprocessor = DataPreprocessor()
        processed_data = preprocessor.add_technical_indicators(data)
        processed_data = preprocessor.normalize_data(processed_data)
        
        # Prepare for training
        features, target = preprocessor.prepare_for_training(processed_data)
        
        # Train model
        predictor = StockPredictor()
        result = predictor.train_model(features, target)
        
        # Save model with timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        predictor.save_model(f"models/{symbol}_model_{timestamp}.pkl")
        
        # Update active model reference
        with open(f"models/{symbol}_active_model.txt", "w") as f:
            f.write(f"{symbol}_model_{timestamp}.pkl")
        
        print(f"Model for {symbol} retrained with MSE: {result['mse']:.4f}")
    
    print(f"All models retrained at {datetime.now()}")

if __name__ == "__main__":
    print("Starting model retraining...")
    retrain_models()