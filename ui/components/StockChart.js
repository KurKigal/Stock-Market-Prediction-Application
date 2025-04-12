import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine } from 'recharts';

function StockChart({ data, prediction }) {
  if (!data || data.length === 0) return <div>No data available</div>;

  // Format data for chart
  const chartData = data.map(item => ({
    date: new Date(item.date).toLocaleDateString(),
    close: item.close,
    ma5: item.MA5,
    ma20: item.MA20
  }));

  // Add prediction point
  if (prediction) {
    chartData.push({
      date: new Date(prediction.date).toLocaleDateString(),
      prediction: prediction.predicted_close
    });
  }

  return (
    <div className="chart-container">
      <h2>{data[0].symbol} Stock Price History</h2>
      <LineChart width={800} height={400} data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis domain={['auto', 'auto']} />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="close" stroke="#8884d8" dot={false} name="Close Price" />
        <Line type="monotone" dataKey="ma5" stroke="#82ca9d" dot={false} name="5-Day MA" />
        <Line type="monotone" dataKey="ma20" stroke="#ffc658" dot={false} name="20-Day MA" />
        {prediction && (
          <Line 
            type="monotone" 
            dataKey="prediction" 
            stroke="#ff7300" 
            strokeWidth={2}
            strokeDasharray="5 5" 
            name="Prediction" 
          />
        )}
      </LineChart>
    </div>
  );
}

export default StockChart;