import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from preprocessing.data_preprocessor import DataPreprocessor

class BackTester:
    def __init__(self, predictor, data):
        self.predictor = predictor
        self.data = data
        
    def run_backtest(self, test_size=0.3):
        # Determine split point
        split_idx = int(len(self.data) * (1 - test_size))
        train_data = self.data.iloc[:split_idx]
        test_data = self.data.iloc[split_idx:]
        
        # Track predictions vs actuals
        predictions = []
        actuals = []
        
        for i in range(len(test_data) - 1):
            # Get features up to this point
            current_idx = split_idx + i
            history = self.data.iloc[:current_idx]
            
            # Preprocess
            preprocessor = DataPreprocessor()
            processed_data = preprocessor.add_technical_indicators(history)
            processed_data = preprocessor.normalize_data(processed_data)
            
            # Get latest features
            latest_features = processed_data.iloc[-1].drop(['date', 'symbol'], axis=1, errors='ignore')
            
            # Make prediction
            pred = self.predictor.predict([latest_features])[0]
            actual = self.data.iloc[current_idx + 1]['close']
            
            predictions.append(pred)
            actuals.append(actual)
        
        # Calculate metrics
        mae = mean_absolute_error(actuals, predictions)
        mse = mean_squared_error(actuals, predictions)
        rmse = np.sqrt(mse)
        
        # Calculate directional accuracy
        direction_correct = sum(
            1 for i in range(len(predictions) - 1)
            if (predictions[i+1] > predictions[i]) == (actuals[i+1] > actuals[i])
        )
        directional_accuracy = direction_correct / (len(predictions) - 1) if len(predictions) > 1 else 0
        
        results = {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'directional_accuracy': directional_accuracy
        }
        
        return results, pd.DataFrame({
            'date': test_data['date'].iloc[:-1].values,
            'actual': actuals,
            'predicted': predictions
        })