from backtester import Backtester
from workflow import run_agent
import pandas as pd

ticker="AAPL"
start_date="2024-03-01"
end_date="2024-03-10"
initial_capital=10000

backtester=Backtester(
    agent=run_agent,
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    initial_capital=initial_capital
)
backtester.run_backtest()
performance_df = backtester.analyze_performance()