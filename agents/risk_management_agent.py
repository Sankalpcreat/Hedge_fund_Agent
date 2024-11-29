from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o")

def risk_management_agent(state: dict):
    portfolio = state["messages"][0].additional_kwargs["portfolio"]
    last_message = state["messages"][-1]
    
    risk_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a risk management specialist. 
                Evaluate portfolio exposure and recommend position sizing. 
                Provide 'max_position_size' and 'risk_score' in the output."""
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                f"""Based on the trading analysis below, provide your risk assessment.
                
                Risk Management Data: {last_message.content}
                
                Portfolio:
                Cash: ${portfolio['cash']:.2f}
                Current Position: {portfolio['stock']} shares
                
                Only include 'max_position_size' and 'risk_score' in your output.
                """
            ),
        ]
    )
    
    chain = risk_prompt | llm
    result = chain.invoke(state).content
    message = HumanMessage(
        content=f"Here is the risk management recommendation: {result}",
        name="risk_management",
    )
    
    return {"messages": state["messages"] + [message]}