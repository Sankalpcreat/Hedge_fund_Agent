from langchain_core.messages import HumanMessage
from utils import get_price_data,calculate_trading_signals

def market_data_agent(state: dict):
    messages = state["messages"]
    params = messages[-1].additional_kwargs
    historical_data = get_price_data(
        params["ticker"], params["start_date"], params["end_date"]
    )
    signals = calculate_trading_signals(historical_data)
    message = HumanMessage(
        content=f"""
        Here are the trading signals for {params["ticker"]}:
        Current Price: ${signals['current_price']:.2f}
        SMA 5: {signals['sma_5_curr']:.2f}
        SMA 5 Previous: {signals['sma_5_prev']:.2f}
        SMA 20: {signals['sma_20_curr']:.2f}
        SMA 20 Previous: {signals['sma_20_prev']:.2f}
        """,
        name="market_data_agent",
    )
    return {"messages": messages + [message]}