import pandas as pd
from datetime import datetime

class ModelMonitor:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def log_prediction(self, symbol, date, predicted, actual=None, model_version="1.0"):
        # Store prediction
        query = """
        INSERT INTO prediction_log 
        (symbol, prediction_date, predicted_value, actual_value, model_version, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db_manager.cursor.execute(
            query, 
            (symbol, date, predicted, actual, model_version, datetime.now())
        )
        self.db_manager.conn.commit()
    
    def update_actual(self, prediction_id, actual_value):
        # Update with actual value when available
        query = "UPDATE prediction_log SET actual_value = ? WHERE id = ?"
        self.db_manager.cursor.execute(query, (actual_value, prediction_id))
        self.db_manager.conn.commit()
    
    def get_model_performance(self, days=30, model_version=None):
        # Query to get predictions with actuals
        query = """
        SELECT * FROM prediction_log 
        WHERE actual_value IS NOT NULL
        """
        if model_version:
            query += f" AND model_version = '{model_version}'"
        query += " ORDER BY prediction_date DESC LIMIT ?"
        
        df = pd.read_sql(query, self.db_manager.conn, params=(days,))
        
        if len(df) == 0:
            return {"error": "No data available"}
        
        # Calculate metrics
        df['error'] = df['actual_value'] - df['predicted_value']
        df['abs_error'] = abs(df['error'])
        df['squared_error'] = df['error'] ** 2
        
        # Daily direction correct
        df['actual_direction'] = df['actual_value'].diff().apply(lambda x: 1 if x > 0 else 0)
        df['pred_direction'] = df['predicted_value'].diff().apply(lambda x: 1 if x > 0 else 0)
        df['direction_correct'] = (df['actual_direction'] == df['pred_direction']).astype(int)
        
        metrics = {
            'mae': df['abs_error'].mean(),
            'mse': df['squared_error'].mean(),
            'rmse': (df['squared_error'].mean()) ** 0.5,
            'directional_accuracy': df['direction_correct'].mean()
        }
        
        return metrics