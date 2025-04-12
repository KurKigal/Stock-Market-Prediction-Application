from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
import os

class LSTMStockPredictor:
    def __init__(self, sequence_length=10):
        self.sequence_length = sequence_length
        self.model = None
        
    def prepare_sequences(self, data):
        X, y = [], []
        for i in range(len(data) - self.sequence_length):
            X.append(data[i:i + self.sequence_length])
            y.append(data[i + self.sequence_length, 0])  # Predict close price
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape):
        self.model = Sequential()
        self.model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=50))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(units=1))
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        return self.model
    
    def train_model(self, X_train, y_train, epochs=50, batch_size=32):
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            callbacks=[early_stopping],
            verbose=1
        )
        
        return history
    
    def save_model(self, filepath):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save(filepath)
        
    def load_model(self, filepath):
        self.model = load_model(filepath)
    
    def predict(self, X_test):
        return self.model.predict(X_test)