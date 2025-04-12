import os
import threading
import subprocess
import time
from flask import Flask, request, jsonify, render_template
from scraper.stock_scraper import StockScraper
from data.database_manager import DatabaseManager
from preprocessing.data_preprocessor import DataPreprocessor
from models.stock_predictor import StockPredictor
from utils.model_monitor import ModelMonitor
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='ui/build', static_url_path='/')

# Initialize components
db_manager = DatabaseManager('data/stock_data.db')
stock_scraper = StockScraper(['AAPL', 'MSFT', 'GOOGL'])
preprocessor = DataPreprocessor()

# Try to load models
predictor = StockPredictor()
try:
    predictor.load_model('models/rf_stock_predictor.pkl')
    print("Loaded general prediction model")
except:
    print("General prediction model not found. Need to train first.")
    
# Initialize model monitor
model_monitor = ModelMonitor(db_manager)

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
    
    # Add technical indicators
    if not data.empty:
        data = preprocessor.add_technical_indicators(data)
    
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/predict/<symbol>', methods=['GET'])
def predict_stock(symbol):
    # Load symbol specific model if available
    try:
        symbol_predictor = StockPredictor()
        symbol_predictor.load_model(f'models/{symbol}_model.pkl')
        current_predictor = symbol_predictor
        model_version = f"{symbol}-specific-model"
    except:
        current_predictor = predictor
        model_version = "general-model"
    
    # Get historical data
    data = db_manager.get_historical_data(symbol, 30)
    
    if data.empty:
        return jsonify({"error": f"No historical data found for {symbol}"}), 404
    
    try:
        # Preprocess data
        processed_data = preprocessor.add_technical_indicators(data)
        processed_data = preprocessor.normalize_data(processed_data)
        
        # Make prediction for next day
        latest_features = processed_data.iloc[-1].drop(['date', 'symbol'], errors='ignore')
        prediction = current_predictor.predict([latest_features])[0]
        
        # Get current close price for comparison
        current_close = data.iloc[-1]['close']
        prediction_change = ((prediction - current_close) / current_close) * 100
        
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Log prediction
        model_monitor.log_prediction(
            symbol, 
            tomorrow, 
            prediction, 
            actual=None, 
            model_version=model_version
        )
        
        return jsonify({
            'symbol': symbol,
            'date': tomorrow,
            'current_close': float(current_close),
            'predicted_close': float(prediction),
            'change_percent': float(prediction_change),
            'model_version': model_version
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def initialize_if_needed():
    """Initialize the database and models if they don't exist"""
    if not os.path.exists('data/stock_data.db'):
        print("Database not found. Initializing...")
        # Run database initialization script
        subprocess.run(['python', 'scripts/initialize_db.py'])
        
        # Train initial models
        subprocess.run(['python', 'scripts/initial_model_training.py'])

def start_scheduler_thread():
    """Start the data update scheduler in a separate thread"""
    from scraper.scheduler import update_stock_data
    import schedule
    
    # Run update daily after market close
    schedule.every().day.at("18:00").do(update_stock_data)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    # Initialize if needed
    initialize_if_needed()
    
    # Start scheduler in a separate thread
    scheduler_thread = threading.Thread(target=start_scheduler_thread)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0')