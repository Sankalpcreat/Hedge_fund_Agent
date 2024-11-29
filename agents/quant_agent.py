from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

def quant_agent(state: dict):
    last_message = state["messages"][-1]
    summary_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a hedge fund quant / technical analyst.
                You are given trading signals for a stock.
                Analyze the signals and provide a recommendation.
                - signal: bullish | bearish | neutral,
                - confidence: <float between 0 and 1>
                """
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                f"""Based on the trading signals below, analyze the data and provide your assessment.
                
                Trading Analysis: {last_message.content}
                
                Only include your trading signal and confidence in the output.
                """
            ),
        ]
    )

    chain=summary_prompt | llm

    result=chain.invoke(state).content
    
    message = HumanMessage(
    content=f"Here is the trading analysis and my recommendation:{result}",
    name="quant_agent",
    )
    return {"messages":state["messages"]+[message]}