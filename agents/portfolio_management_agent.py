from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o")

def portfolio_management_agent(state: dict):
    portfolio = state["messages"][0].additional_kwargs["portfolio"]
    last_message = state["messages"][-1]
    
    portfolio_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a portfolio manager. 
                Make a trading decision based on risk management data. 
                Provide 'action' and 'quantity' in the output."""
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                f"""Based on the risk management data below, make your trading decision.
                
                Risk Management Data: {last_message.content}
                
                Portfolio:
                Cash: ${portfolio['cash']:.2f}
                Current Position: {portfolio['stock']} shares
                
                Only include 'action' and 'quantity' in your output.
                """
            ),
        ]
    )
    
    chain = portfolio_prompt | llm
    result = chain.invoke(state).content
    message = HumanMessage(
        content=f"Here is the trading decision: {result}",
        name="portfolio_management",
    )
    
    return {"messages": state["messages"] + [message]}