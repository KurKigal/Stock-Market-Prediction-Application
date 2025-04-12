import React from 'react';

function PredictionCard({ prediction }) {
  if (!prediction) return null;

  const isPositive = prediction.change_percent > 0;
  const changeClass = isPositive ? 'positive-change' : 'negative-change';

  return (
    <div className="prediction-card">
      <h2>Prediction for {prediction.symbol}</h2>
      <p className="prediction-date">Date: {new Date(prediction.date).toLocaleDateString()}</p>
      <div className="prediction-details">
        <div className="prediction-item">
          <span className="label">Current Close:</span>
          <span className="value">${prediction.current_close.toFixed(2)}</span>
        </div>
        <div className="prediction-item">
          <span className="label">Predicted Close:</span>
          <span className="value">${prediction.predicted_close.toFixed(2)}</span>
        </div>
        <div className="prediction-item">
          <span className="label">Change:</span>
          <span className={`value ${changeClass}`}>
            {isPositive ? '+' : ''}{prediction.change_percent.toFixed(2)}%
          </span>
        </div>
      </div>
      <div className="prediction-summary">
        <p>
          Our model predicts that {prediction.symbol} will 
          {isPositive ? ' increase ' : ' decrease '} 
          by {Math.abs(prediction.change_percent).toFixed(2)}% tomorrow.
        </p>
      </div>
    </div>
  );
}

export default PredictionCard;