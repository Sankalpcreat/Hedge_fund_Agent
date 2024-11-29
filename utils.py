import pandas as pd
import yfinance as yf
from datetime import timedelta
import os

def get_price_data(ticker, start_date, end_date):
    try:
        # Download data from Yahoo Finance
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        
        # Rename columns to match expected format
        data = data.reset_index()
        data.columns = data.columns.str.lower()
        data = data.rename(columns={'date': 'timestamp', 'close': 'price'})
        
        # Keep only required columns
        data = data[['timestamp', 'price']]
        data['timestamp'] = data['timestamp'].dt.strftime('%Y-%m-%d')
        
        return data
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")

def calculate_trading_signals(historical_data:pd.DataFrame)->dict:
    sma_5=historical_data["price"].rolling(window=5).mean()
    sma_20=historical_data["price"].rolling(window=20).mean()

    sma_5_prev, sma_5_curr = sma_5.iloc[-2:]
    sma_20_prev, sma_20_curr = sma_20.iloc[-2:]

    return {
    "current_price": historical_data["price"].iloc[-1],
    "sma_5_curr": sma_5_curr,
    "sma_5_prev": sma_5_prev,
    "sma_20_curr": sma_20_curr,
    "sma_20_prev": sma_20_prev,
}
