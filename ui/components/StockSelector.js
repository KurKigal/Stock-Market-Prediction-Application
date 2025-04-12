import React, { useState, useEffect } from 'react';

function StockSelector({ onSelectStock, selectedStock }) {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch('/api/stocks')
      .then(response => response.json())
      .then(data => setStocks(data.stocks))
      .catch(error => console.error('Error fetching stocks:', error));
  }, []);

  return (
    <div className="stock-selector">
      <label htmlFor="stock-select">Select Stock:</label>
      <select 
        id="stock-select" 
        value={selectedStock} 
        onChange={(e) => onSelectStock(e.target.value)}
      >
        {stocks.map(stock => (
          <option key={stock} value={stock}>{stock}</option>
        ))}
      </select>
    </div>
  );
}

export default StockSelector;