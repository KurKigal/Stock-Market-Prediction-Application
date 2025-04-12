import React, { useState, useEffect } from 'react';
import StockSelector from './components/StockSelector';
import StockChart from './components/StockChart';
import PredictionCard from './components/PredictionCard';
import './App.css';

function App() {
  const [selectedStock, setSelectedStock] = useState('AAPL');
  const [historicalData, setHistoricalData] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData(selectedStock);
  }, [selectedStock]);

  const fetchData = async (symbol) => {
    setLoading(true);
    try {
      // Fetch historical data
      const histResponse = await fetch(`/api/historical/${symbol}?days=30`);
      const histData = await histResponse.json();
      setHistoricalData(histData);

      // Fetch prediction
      const predResponse = await fetch(`/api/predict/${symbol}`);
      const predData = await predResponse.json();
      setPrediction(predData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStockChange = (symbol) => {
    setSelectedStock(symbol);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Stock Market Predictor</h1>
      </header>
      <main className="app-content">
        <StockSelector onSelectStock={handleStockChange} selectedStock={selectedStock} />
        
        {loading ? (
          <div className="loading">Loading data...</div>
        ) : (
          <>
            <StockChart data={historicalData} prediction={prediction} />
            <PredictionCard prediction={prediction} />
          </>
        )}
      </main>
    </div>
  );
}

export default App;