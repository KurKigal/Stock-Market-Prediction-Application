import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.database_manager import DatabaseManager
from preprocessing.data_preprocessor import DataPreprocessor
from models.stock_predictor import StockPredictor
import os

def train_initial_models():
    print("Training initial models...")
    db_manager = DatabaseManager('data/stock_data.db')
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    for symbol in symbols:
        print(f"Training model for {symbol}...")
        
        # Get data
        data = db_manager.get_historical_data(symbol, days=365)
        
        if len(data) < 30:
            print(f"Not enough data for {symbol} to train a model. Skipping.")
            continue
            
        # Preprocess
        preprocessor = DataPreprocessor()
        processed_data = preprocessor.add_technical_indicators(data)
        processed_data = preprocessor.normalize_data(processed_data)
        
        # Prepare for training
        features, target = preprocessor.prepare_for_training(processed_data)
        
        # Train model
        predictor = StockPredictor()
        result = predictor.train_model(features, target)
        
        # Save model
        predictor.save_model(f"models/{symbol}_model.pkl")
        
        print(f"Model for {symbol} trained with MSE: {result['mse']:.4f}, R²: {result['r2']:.4f}")
    
    # Save a general model as well
    predictor.save_model("models/rf_stock_predictor.pkl")
    
    db_manager.close()
    print("Initial model training complete!")

if __name__ == "__main__":
    train_initial_models()