from dotenv import load_dotenv
import os

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from utils import get_price_data, calculate_trading_signals

llm = ChatOpenAI(model="gpt-4", temperature=0)  # Lower temperature for more focused responses

def market_data_agent(state: dict):
    ticker = state["messages"][0].additional_kwargs["ticker"]
    start_date = state["messages"][0].additional_kwargs["start_date"]
    end_date = state["messages"][0].additional_kwargs["end_date"]
    
    historical_data = get_price_data(ticker, start_date, end_date)
    signals = calculate_trading_signals(historical_data)
    
    market_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a market data analyst. Provide a brief technical analysis."),
        ("human", f"""
        Technical Analysis for {ticker}:
        Current Price: ${signals['current_price']:.2f}
        5-day SMA: ${signals['sma_5_curr']:.2f}
        20-day SMA: ${signals['sma_20_curr']:.2f}
        
        Provide a very brief analysis focusing on price action and moving averages.
        """)
    ])
    
    chain = market_prompt | llm
    result = chain.invoke({}).content
    
    return {"messages": state["messages"] + [HumanMessage(
        content=f"Market Analysis: {result}",
        name="market_data"
    )]}