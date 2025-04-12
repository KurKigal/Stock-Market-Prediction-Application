# Stock Market Prediction Application

A web application that scrapes stock market data, analyzes trends, and provides predictive insights for future stock performance.

## Features

- Web scraping for collecting historical stock data  
- Technical indicator calculations  
- Machine learning models for price prediction  
- User-friendly interface with interactive charts  
- Daily updates and predictive analytics  

## Setup and Installation

### Prerequisites

- Python 3.7 or higher  
- Node.js 14 or higher (for frontend development)  

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/yourusername/stock-predictor.git](https://github.com/KurKigal/Stock-Market-Prediction-Application.git)
   cd Stock-Market-Prediction-Application
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database and download initial data:**

   ```bash
   python scripts/initialize_db.py
   ```

5. **Train the initial prediction models:**

   ```bash
   python scripts/initial_model_training.py
   ```

6. **Install frontend dependencies:**

   ```bash
   cd ui
   npm install
   npm run build
   cd ..
   ```

## Running the Application

1. **Start the Flask server:**

   ```bash
   python app.py
   ```

2. **Open your browser and visit:**  
   `http://localhost:5000`

## Development

### Backend

- Flask API endpoints: `app.py`  
- Data scraping: `scraper` module  
- Prediction models: `models` module  

### Frontend

- React components: `ui/src/components/`  
- App entry point: `ui/src/App.js`  

## Deployment

To deploy using Docker:

```bash
docker-compose up -d
```

## License

This project is licensed under the MIT License.
