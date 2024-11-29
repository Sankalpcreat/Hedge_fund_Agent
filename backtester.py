import pandas as pd
from datetime import timedelta
import json
import matplotlib.pyplot as plt
from utils import get_price_data

class Backtester:
    def __init__(self, agent, ticker, start_date, end_date, initial_capital):
        self.agent = agent
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.portfolio = {"cash": initial_capital, "stocks": 0}
        self.portfolio_values = []
        # Cache the price data for the entire period
        self.price_data = get_price_data(ticker, start_date, end_date)

    def parse_action(self, agent_output):
        try:
            decision = json.loads(agent_output)
            return decision["action"], decision["quantity"]
        except:
            return "hold", 0

    def execute_trade(self, action, quantity, current_price):
        if action == "buy" and quantity > 0:
            cost = quantity * current_price
            if cost <= self.portfolio["cash"]:
                self.portfolio["stocks"] += quantity
                self.portfolio["cash"] -= cost
                return quantity
            else:
                max_quantity = self.portfolio["cash"] // current_price
                if max_quantity > 0:
                    self.portfolio["stocks"] += max_quantity
                    self.portfolio["cash"] -= max_quantity * current_price
                    return max_quantity
        elif action == "sell" and quantity > 0:
            quantity = min(quantity, self.portfolio["stocks"])
            if quantity > 0:
                self.portfolio["cash"] += quantity * current_price
                self.portfolio["stocks"] -= quantity
                return quantity
        return 0

    def run_backtest(self):
        print("\nStarting backtest...")
        print("Date         Action Quantity    Price         Cash    Stock  Total Value")
        print("----------------------------------------------------------------------")

        dates = pd.date_range(start=self.start_date, end=self.end_date)
        for current_date in dates:
            current_date_str = current_date.strftime("%Y-%m-%d")
            
            # Get last 5 days of data for analysis (shorter lookback)
            lookback_start = (current_date - timedelta(days=5)).strftime("%Y-%m-%d")
            df = self.price_data[self.price_data['timestamp'] <= current_date_str].tail(5)
            
            if df.empty:
                continue
                
            current_price = df.iloc[-1]['price']
            if pd.isna(current_price):
                continue

            agent_output = self.agent(
                ticker=self.ticker,
                start_date=lookback_start,
                end_date=current_date_str,
                portfolio=self.portfolio
            )
            
            action, quantity = self.parse_action(agent_output)
            executed_quantity = self.execute_trade(action, quantity, current_price)
            total_value = self.portfolio["cash"] + self.portfolio["stocks"] * current_price
            self.portfolio["portfolio_value"] = total_value
            
            print(f"{current_date.strftime('%Y-%m-%d'):<12} {action:<6} {executed_quantity:>8} {current_price:>8.2f} {self.portfolio['cash']:>12.2f} {self.portfolio['stocks']:>8} {total_value:>12.2f}")
            self.portfolio_values.append({"Date": current_date, "Portfolio Value": total_value})

    def analyze_performance(self):
        if not self.portfolio_values:
            return pd.DataFrame()
            
        df = pd.DataFrame(self.portfolio_values)
        df.set_index("Date", inplace=True)
        
        # Plot the portfolio value over time
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df["Portfolio Value"])
        plt.title("Portfolio Value Over Time")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("portfolio_performance.png")
        plt.close()
        
        return df