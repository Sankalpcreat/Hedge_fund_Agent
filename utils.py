import pandas as pd
import requests
from datetime import timedelta
import os

def get_price_data(ticker, start_date, end_date):
    headers = {"X-API-KEY": os.environ.get("FINANCIAL_DATASETS_API_KEY")}
    url = (
        f"https://api.financialdatasets.ai/prices/"
        f"?ticker={ticker}"
        f"&interval=day"
        f"&interval_multiplier=1"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
    )
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
    data = response.json()
    prices = data.get("prices")
    if not prices:
        raise ValueError("No price data returned")
    df = pd.DataFrame(prices)
    df["Date"] = pd.to_datetime(df["time"])
    df.set_index("Date", inplace=True)
    numeric_cols = ["open", "close", "high", "low", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.sort_index(inplace=True)
    return df

def calculate_trading_signals(historical_data:pd.DataFrame)->dict:
    sma_5=historical_data["close"].rolling(window=5).mean()
    sma_20=historical_data["close"].rolling(window=20).mean()

    sma_5_prev, sma_5_curr = sma_5.iloc[-2:]
    sma_20_prev, sma_20_curr = sma_20.iloc[-2:]

    return {
    "current_price": historical_data["close"].iloc[-1],
    "sma_5_curr": sma_5_curr,
    "sma_5_prev": sma_5_prev,
    "sma_20_curr": sma_20_curr,
    "sma_20_prev": sma_20_prev,
}
