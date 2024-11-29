from dotenv import load_dotenv
import os

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4", temperature=0)

def risk_management_agent(state: dict):
    portfolio = state["messages"][0].additional_kwargs["portfolio"]
    last_message = state["messages"][-1]
    
    risk_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a risk management specialist. 
            Analyze market conditions and portfolio risk.
            Provide a brief risk assessment."""),
        MessagesPlaceholder(variable_name="messages"),
        ("human", f"""Based on the market analysis below, assess the risk.
            
            Market Analysis: {last_message.content}
            
            Portfolio:
            Cash: ${portfolio['cash']:.2f}
            Current Position: {portfolio['stocks']} shares
            """)
    ])
    
    chain = risk_prompt | llm
    result = chain.invoke({"messages": state["messages"]}).content
    message = HumanMessage(
        content=f"Risk Assessment: {result}",
        name="risk_management"
    )
    return {"messages": state["messages"] + [message]}