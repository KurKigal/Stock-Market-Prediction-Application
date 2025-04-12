from flask import Flask, request, jsonify, render_template
import pandas as pd
from datetime import datetime, timedelta
import joblib
from scraper.stock_scraper import StockScraper
from data.database_manager import DatabaseManager
from preprocessing.data_preprocessor import DataPreprocessor
from models.stock_predictor import StockPredictor

app = Flask(__name__, static_folder='ui/build', static_url_path='/')

# Initialize components
stock_scraper = StockScraper(['AAPL', 'MSFT', 'GOOGL'])
db_manager = DatabaseManager('data/stock_data.db')
preprocessor = DataPreprocessor()
predictor = StockPredictor()
predictor.load_model('models/rf_stock_predictor.pkl')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    return jsonify({'stocks': ['AAPL', 'MSFT', 'GOOGL']})

@app.route('/api/historical/<symbol>', methods=['GET'])
def get_historical_data(symbol):
    days = request.args.get('days', default=30, type=int)
    data = db_manager.get_historical_data(symbol, days)
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/predict/<symbol>', methods=['GET'])
def predict_stock(symbol):
    # Get historical data
    data = db_manager.get_historical_data(symbol, 30)
    
    # Preprocess data
    processed_data = preprocessor.add_technical_indicators(data)
    processed_data = preprocessor.normalize_data(processed_data)
    
    # Make prediction for next day
    latest_features = processed_data.iloc[-1].drop(['date', 'symbol'], errors='ignore')
    prediction = predictor.predict([latest_features])[0]
    
    # Get current close price for comparison
    current_close = data.iloc[-1]['close']
    prediction_change = ((prediction - current_close) / current_close) * 100
    
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    return jsonify({
        'symbol': symbol,
        'date': tomorrow,
        'current_close': float(current_close),
        'predicted_close': float(prediction),
        'change_percent': float(prediction_change)
    })

if __name__ == '__main__':
    app.run(debug=True)