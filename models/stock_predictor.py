from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

class StockPredictor:
    def __init__(self):
        self.model = None
        
    def train_model(self, features, target):
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.2, shuffle=False
        )
        
        # Initialize model
        self.model = RandomForestRegressor(
            n_estimators=100, 
            random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model trained with MSE: {mse:.4f}, R²: {r2:.4f}")
        return {
            'mse': mse,
            'r2': r2,
            'model': self.model
        }
    
    def hyperparameter_tuning(self, features, target):
        # Define parameter grid
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        }
        
        # Initialize grid search
        rf = RandomForestRegressor(random_state=42)
        grid_search = GridSearchCV(
            estimator=rf,
            param_grid=param_grid,
            cv=5,
            scoring='neg_mean_squared_error',
            n_jobs=-1
        )
        
        # Perform grid search
        grid_search.fit(features, target)
        
        # Get best parameters
        best_params = grid_search.best_params_
        self.model = grid_search.best_estimator_
        
        print(f"Best parameters: {best_params}")
        return best_params
    
    def save_model(self, filepath):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.model, filepath)
        
    def load_model(self, filepath):
        self.model = joblib.load(filepath)
        
    def predict(self, features):
        if self.model is None:
            raise Exception("Model not trained or loaded")
        return self.model.predict(features)