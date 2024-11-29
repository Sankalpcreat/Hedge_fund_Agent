from dotenv import load_dotenv
import os

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4", temperature=0)

def portfolio_management_agent(state: dict):
    portfolio = state["messages"][0].additional_kwargs["portfolio"]
    last_message = state["messages"][-1]
    
    portfolio_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a portfolio manager. 
            Make trading decisions based on risk assessment and market data. 
            Provide 'action' and 'quantity' in the output."""),
        MessagesPlaceholder(variable_name="messages"),
        ("human", f"""Based on the market analysis below, make a trading decision.
            
            Market Analysis: {last_message.content}
            
            Portfolio:
            Cash: ${portfolio['cash']:.2f}
            Current Position: {portfolio['stocks']} shares
            
            Only include 'action' and 'quantity' in your output.
            """)
    ])
    
    chain = portfolio_prompt | llm
    result = chain.invoke({"messages": state["messages"]}).content
    message = HumanMessage(
        content=f"Trading Decision: {result}",
        name="portfolio_manager"
    )
    return {"messages": state["messages"] + [message]}